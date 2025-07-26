"""FastAPI application entrypoint.

This module defines the asynchronous webhook endpoint that ingests Kubernetes
alerts, queues them for large-language-model analysis, and exposes endpoints to
retrieve the analysis reports.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn

from oncallm.alerts import AlertGroup
from oncallm.llm_service import OncallmAgent
from oncallm.health_routes import router as health_router
from oncallm.template_renderer import TemplateRenderer


load_dotenv()

# Configure logging to enable INFO level.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)

# In-memory store for processed analysis reports. Keyed by alert fingerprint.
_analysis_reports: Dict[str, Any] = {}

# Queue and executor will be initialised at application startup.
_alert_queue: Optional[asyncio.Queue] = None
_executor: Optional[ThreadPoolExecutor] = None

# Template renderer for HTML pages.
_template_renderer: Optional[TemplateRenderer] = None

# Global agent instance to be initialized once at startup.
_agent: Optional[OncallmAgent] = None


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """FastAPI lifespan context manager to initialize and tear down resources.
    
    Args:
        app: The FastAPI application instance (unused but required by FastAPI).
        
    Yields:
        None: Control back to FastAPI during application runtime.
    """
    global _alert_queue, _executor, _template_renderer, _agent
    _alert_queue = asyncio.Queue()
    _executor = ThreadPoolExecutor(max_workers=10)
    _template_renderer = TemplateRenderer(os.getenv("TEMPLATE_DIR", "../templates"))
    
    # Initialize the agent once at startup to avoid expensive initialization
    # for every alert processing.
    _logger.info("Initializing OncallmAgent...")
    _agent = OncallmAgent()
    _logger.info("OncallmAgent initialized successfully")
    
    worker_task = asyncio.create_task(
        _process_alerts_worker(_alert_queue, _executor)
    )
    yield  # Application is up and running.
    worker_task.cancel()
    if _executor:
        _executor.shutdown(wait=False, cancel_futures=True)


app = FastAPI(
    title="OnCallM - Kubernetes Alert Analysis",
    description="AI-powered Kubernetes alert analysis and root cause detection",
    version="1.0.0",
    lifespan=_lifespan
)

app.include_router(health_router)


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint providing API information.
    
    Returns:
        Dictionary containing API name and available endpoints.
    """
    return {
        "name": "OnCallM Agent",
        "description": "AI-powered Kubernetes alert analysis and root cause detection",
        "version": "1.0.0",
        "available_endpoints": [
            "GET /health - Health check",
            "POST /webhook - Submit alerts for analysis", 
            "GET /reports - List all reports",
            "GET /report/{fingerprint} - View HTML report page"
        ]
    }


async def _process_alerts_worker(
    queue: asyncio.Queue, 
    executor: ThreadPoolExecutor
) -> None:
    """Background worker to process queued alerts.
    
    Args:
        queue: The asyncio queue containing alert processing tasks.
        executor: ThreadPoolExecutor for running blocking operations.
    """
    while True:
        try:
            alert_fingerprint, alert_group = await queue.get()
            _logger.info(
                "Processing alert with fingerprint: %s", alert_fingerprint
            )
            
            # Process the alert in the thread pool to avoid blocking the event
            # loop.
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                executor, _process_alert, alert_fingerprint, alert_group
            )
            
            queue.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            _logger.error("Error processing alert: %s", e)


def _process_alert(alert_fingerprint: str, alert_group: AlertGroup) -> None:
    """Process a single alert and store the analysis.
    
    Args:
        alert_fingerprint: Unique identifier for the alert.
        alert_group: The alert group data from Alertmanager.
    """
    try:
        # Use the global agent instance initialized at startup.
        if _agent is None:
            raise RuntimeError("Agent not initialized")
        
        analysis = _agent.do_analysis(alert_group)
        
        # Store the completed analysis with enhanced report data.
        _analysis_reports[alert_fingerprint] = {
            "status": "completed",
            "analysis": analysis.model_dump(),
            "alert_group": alert_group.model_dump(),
            "created_at": alert_group.alerts[0].startsAt.isoformat(),
            "fingerprint": alert_fingerprint
        }
        
        _logger.info("Completed analysis for alert: %s", alert_fingerprint)
        
    except Exception as e:
        _logger.error("Error analyzing alert %s: %s", alert_fingerprint, e)
        _analysis_reports[alert_fingerprint] = {
            "status": "failed",
            "error": str(e),
            "alert_group": alert_group.model_dump(),
            "created_at": alert_group.alerts[0].startsAt.isoformat(),
            "fingerprint": alert_fingerprint
        }


@app.post("/webhook", response_model=Dict[str, Any])
async def webhook(alert_group: AlertGroup) -> Dict[str, Any]:
    """Queue an incoming alert for asynchronous analysis.

    Args:
        alert_group: Raw alert body forwarded by AlertManager.

    Returns:
        A JSON map containing status, report_urls with links to detailed 
        reports for each alert in the group.
        
    Raises:
        HTTPException: If the service is not properly initialized.
    """
    if _alert_queue is None or _agent is None:
        # Should never happen unless startup failed.
        raise HTTPException(
            status_code=503, detail="Service not initialised"
        )

    _logger.info("Received alert group, queuing for processing")

    # Create report URLs for each alert using their fingerprints.
    report_urls = []
    base_url = os.getenv("ONCALLM_BASE_URL", "http://localhost:8001")
    
    for alert in alert_group.alerts:
        fingerprint = alert.fingerprint
        report_url = f"{base_url}/report/{fingerprint}"
        report_urls.append({
            "fingerprint": fingerprint,
            "alert_name": alert.labels.alertname,
            "namespace": alert.labels.namespace,
            "report_url": report_url
        })
        
        # Mark report as pending so clients can poll for completion.
        _analysis_reports[fingerprint] = {"status": "processing"}
        
        # Queue for processing.
        await _alert_queue.put((fingerprint, alert_group))

    return {
        "status": "success", 
        "message": "Alerts queued for analysis",
        "report_urls": report_urls
    }


@app.get("/report/{fingerprint}", response_class=HTMLResponse)
async def get_alert_report(fingerprint: str) -> str:
    """Serve the alert analysis report as an HTML page.
    
    Args:
        fingerprint: The unique fingerprint of the alert.
        
    Returns:
        HTML page with the alert analysis report.
        
    Raises:
        HTTPException: If the alert report is not found.
    """
    report = _analysis_reports.get(fingerprint)
    if not report:
        raise HTTPException(status_code=404, detail="Alert report not found")
    
    # Generate HTML report page using template renderer.
    return _generate_report_html(fingerprint, report)


def _generate_report_html(fingerprint: str, report: Dict[str, Any]) -> str:
    """Generate HTML report page for an alert.
    
    Args:
        fingerprint: The unique fingerprint of the alert.
        report: The report data containing status and analysis.
        
    Returns:
        Complete HTML page as a string.
    """
    if not _template_renderer:
        raise HTTPException(status_code=503, detail="Template renderer not initialized")
    
    if report["status"] == "processing":
        return _template_renderer.render_processing_page(fingerprint)
    elif report["status"] == "failed":
        error_message = report.get("error", "Unknown error occurred")
        return _template_renderer.render_failed_page(fingerprint, error_message)
    else:
        # Extract alert information for completed reports.
        alert_group = report.get("alert_group", {})
        alert_info = _extract_alert_info(alert_group)
        analysis = report.get("analysis", {})
        created_at = report.get("created_at", "Unknown")
        
        return _template_renderer.render_completed_page(
            fingerprint, alert_info, analysis, created_at
        )


def _extract_alert_info(alert_group: Dict[str, Any]) -> Dict[str, str]:
    """Extract alert information from alert group.
    
    Args:
        alert_group: The alert group data.
        
    Returns:
        Dictionary containing extracted alert information.
    """
    alert_info = {}
    if alert_group and "alerts" in alert_group:
        first_alert = alert_group["alerts"][0]
        alert_info = {
            "name": first_alert.get("labels", {}).get("alertname", "Unknown"),
            "namespace": first_alert.get("labels", {}).get(
                "namespace", "Unknown"
            ),
            "pod": first_alert.get("labels", {}).get("pod", "N/A"),
            "service": first_alert.get("labels", {}).get("service", "N/A"),
            "severity": first_alert.get("labels", {}).get(
                "severity", "Unknown"
            ),
            "summary": first_alert.get("annotations", {}).get(
                "summary", "No summary"
            ),
            "description": first_alert.get("annotations", {}).get(
                "description", "No description"
            ),
            "started_at": first_alert.get("startsAt", "Unknown")
        }
    return alert_info


@app.get("/reports")
async def list_reports() -> Dict[str, List[Dict[str, str]]]:
    """List all available reports.
    
    Returns:
        Dictionary containing list of reports with their metadata.
    """
    return {
        "reports": [
            {
                "fingerprint": fingerprint,
                "status": report["status"],
                "created_at": report.get("created_at", "Unknown")
            }
            for fingerprint, report in _analysis_reports.items()
        ]
          }


def main() -> None:
    """Main function to run the application."""
    # Use environment variables for configuration.
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8001"))
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
