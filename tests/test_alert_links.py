"""Test alert link functionality using fingerprints."""

from datetime import datetime
from typing import Any, Dict
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from oncallm.alerts import Alert, AlertAnnotation, AlertGroup, AlertLabel
from oncallm.llm_service import OncallK8sResponse
from oncallm.main import app


@pytest.fixture
def client() -> TestClient:
    """Create FastAPI test client.
    
    Returns:
        TestClient instance for making HTTP requests.
    """
    return TestClient(app)


@pytest.fixture
def sample_alert_with_fingerprint() -> Dict[str, Any]:
    """Create sample alert group with fingerprint.
    
    Returns:
        Dictionary containing sample alert group data.
    """
    return {
        "version": "4",
        "groupKey": "{}:{alertname='PodCrashLooping', namespace='default'}",
        "truncatedAlerts": 0,
        "status": "firing",
        "receiver": "oncallm-webhook",
        "groupLabels": {
            "alertname": "PodCrashLooping",
            "namespace": "default"
        },
        "commonLabels": {
            "alertname": "PodCrashLooping",
            "namespace": "default",
            "pod": "test-pod-123"
        },
        "commonAnnotations": {
            "summary": "Pod is crash looping",
            "description": "Pod test-pod-123 is crash looping in default namespace"
        },
        "externalURL": "http://alertmanager:9093",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "PodCrashLooping",
                    "namespace": "default",
                    "pod": "test-pod-123",
                    "severity": "critical"
                },
                "annotations": {
                    "summary": "Pod is crash looping",
                    "description": "Pod test-pod-123 is crash looping in default namespace"
                },
                "startsAt": "2024-01-01T12:00:00Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "http://prometheus:9090/graph",
                "fingerprint": "test123fingerprint"
            }
        ]
    }


@pytest.fixture
def sample_analysis_response() -> Dict[str, Any]:
    """Create sample analysis response.
    
    Returns:
        Dictionary containing sample AI analysis results.
    """
    return {
        "root_cause": "Pod is running out of memory causing crashes",
        "diagnosis": "Memory limit exceeded causing OOMKilled events",
        "summary_of_findings": "Container memory usage exceeded limits",
        "recommended_actions": "Increase memory limits or optimize application",
        "solution": "Update deployment with higher memory limits",
        "conclusion": "Memory optimization needed",
        "recommendations": "Monitor memory usage and set appropriate limits"
    }


def test_webhook_creates_fingerprint_based_reports(
    client: TestClient,
    sample_alert_with_fingerprint: Dict[str, Any]
) -> None:
    """Test that webhook creates reports using alert fingerprints.
    
    Args:
        client: FastAPI test client.
        sample_alert_with_fingerprint: Sample alert data with fingerprint.
    """
    with patch("oncallm.main._alert_queue") as mock_queue, \
         patch("oncallm.main._agent") as mock_agent:
        mock_queue.put = AsyncMock()
        
        response = client.post("/webhook", json=sample_alert_with_fingerprint)
        
        assert response.status_code == 200
        response_data = response.json()
        
        # Check response structure.
        assert response_data["status"] == "success"
        assert "report_urls" in response_data
        assert len(response_data["report_urls"]) == 1
        
        # Check report URL contains fingerprint.
        report_url = response_data["report_urls"][0]
        assert report_url["fingerprint"] == "test123fingerprint"
        assert "report_url" in report_url
        assert "/report/test123fingerprint" in report_url["report_url"]


def test_get_report_endpoint_with_fingerprint(
    client: TestClient,
    sample_analysis_response: Dict[str, Any]
) -> None:
    """Test getting report by fingerprint.
    
    Args:
        client: FastAPI test client.
        sample_analysis_response: Sample analysis response data.
    """
    # Mock a completed analysis report.
    fingerprint = "test123fingerprint"
    
    with patch("oncallm.main._analysis_reports") as mock_reports, \
         patch("oncallm.main._template_renderer") as mock_renderer:
        
        mock_reports.get.return_value = {
            "status": "completed",
            "analysis": sample_analysis_response,
            "alert_group": {
                "alerts": [{
                    "labels": {
                        "alertname": "PodCrashLooping",
                        "namespace": "default",
                        "severity": "critical"
                    },
                    "annotations": {
                        "summary": "Pod crash looping",
                        "description": "Test description"
                    },
                    "startsAt": "2024-01-01T12:00:00Z"
                }]
            },
            "created_at": "2024-01-01T12:00:00Z",
            "fingerprint": fingerprint
        }
        
        # Mock the template renderer to return HTML.
        mock_renderer.render_completed_page.return_value = f"""
        <html>
        <body>
            <h1>OnCallM Alert Analysis</h1>
            <p>Alert: PodCrashLooping</p>
            <p>ID: {fingerprint}</p>
        </body>
        </html>
        """
        
        response = client.get(f"/report/{fingerprint}")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
        # Check that HTML contains expected content.
        html_content = response.text
        assert "OnCallM Alert Analysis" in html_content
        assert "PodCrashLooping" in html_content
        assert fingerprint in html_content


def test_get_report_processing_state(client: TestClient) -> None:
    """Test getting report in processing state.
    
    Args:
        client: FastAPI test client.
    """
    fingerprint = "processing123"
    
    with patch("oncallm.main._analysis_reports") as mock_reports, \
         patch("oncallm.main._template_renderer") as mock_renderer:
        
        mock_reports.get.return_value = {"status": "processing"}
        
        # Mock the template renderer to return processing HTML.
        mock_renderer.render_processing_page.return_value = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="5">
        </head>
        <body>
            <h1>Analyzing Alert...</h1>
            <div class="spinner"></div>
        </body>
        </html>
        """
        
        response = client.get(f"/report/{fingerprint}")
        
        assert response.status_code == 200
        html_content = response.text
        
        # Check processing indicators.
        assert "Analyzing Alert" in html_content
        assert "refresh" in html_content.lower()
        assert "spinner" in html_content.lower()


def test_get_report_failed_state(client: TestClient) -> None:
    """Test getting report in failed state.
    
    Args:
        client: FastAPI test client.
    """
    fingerprint = "failed123"
    error_message = "OpenAI API error"
    
    with patch("oncallm.main._analysis_reports") as mock_reports, \
         patch("oncallm.main._template_renderer") as mock_renderer:
        
        mock_reports.get.return_value = {
            "status": "failed",
            "error": error_message
        }
        
        # Mock the template renderer to return failed HTML.
        mock_renderer.render_failed_page.return_value = f"""
        <html>
        <body>
            <h1>Analysis Failed</h1>
            <p>Error: {error_message}</p>
        </body>
        </html>
        """
        
        response = client.get(f"/report/{fingerprint}")
        
        assert response.status_code == 200
        html_content = response.text
        
        # Check error display.
        assert "Analysis Failed" in html_content
        assert error_message in html_content


def test_get_report_not_found(client: TestClient) -> None:
    """Test getting non-existent report.
    
    Args:
        client: FastAPI test client.
    """
    fingerprint = "nonexistent123"
    
    with patch("oncallm.main._analysis_reports") as mock_reports:
        mock_reports.get.return_value = None
        
        response = client.get(f"/report/{fingerprint}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


def test_list_reports_endpoint(client: TestClient) -> None:
    """Test listing all reports endpoint.
    
    Args:
        client: FastAPI test client.
    """
    sample_reports = {
        "fingerprint1": {
            "status": "completed",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "fingerprint2": {
            "status": "processing",
            "created_at": "2024-01-01T12:30:00Z"
        }
    }
    
    with patch("oncallm.main._analysis_reports", sample_reports):
        response = client.get("/reports")
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert "reports" in response_data
        assert len(response_data["reports"]) == 2
        
        # Check report metadata.
        for report in response_data["reports"]:
            assert "fingerprint" in report
            assert "status" in report
            assert "created_at" in report


def test_legacy_reports_endpoint(client: TestClient) -> None:
    """Test legacy reports endpoint for backward compatibility.
    
    Args:
        client: FastAPI test client.
    """
    report_id = "legacy123"
    sample_report = {
        "status": "completed",
        "analysis": {"root_cause": "Test cause"},
        "created_at": "2024-01-01T12:00:00Z"
    }
    
    with patch("oncallm.main._analysis_reports") as mock_reports:
        mock_reports.__contains__.return_value = True
        mock_reports.__getitem__.return_value = sample_report
        
        response = client.get(f"/reports/{report_id}")
        
        assert response.status_code == 200
        assert response.json() == sample_report


@patch("oncallm.main._agent")
def test_process_alert_function(
    mock_agent: Any,
    sample_alert_with_fingerprint: Dict[str, Any],
    sample_analysis_response: Dict[str, Any]
) -> None:
    """Test the _process_alert function.
    
    Args:
        mock_agent: Mocked global agent instance.
        sample_alert_with_fingerprint: Sample alert data.
        sample_analysis_response: Sample analysis response.
    """
    from oncallm.main import _process_alert
    
    # Setup mock agent.
    mock_analysis = OncallK8sResponse(**sample_analysis_response)
    mock_agent.do_analysis.return_value = mock_analysis
    
    # Create alert group from sample data.
    alert_group = AlertGroup(**sample_alert_with_fingerprint)
    fingerprint = "test123fingerprint"
    
    with patch("oncallm.main._analysis_reports") as mock_reports:
        _process_alert(fingerprint, alert_group)
        
        # Verify agent was called correctly.
        mock_agent.do_analysis.assert_called_once_with(alert_group)
        
        # Verify report was stored.
        mock_reports.__setitem__.assert_called_once()
        stored_report = mock_reports.__setitem__.call_args[0][1]
        assert stored_report["status"] == "completed"
        assert stored_report["fingerprint"] == fingerprint


@patch("oncallm.main._agent")
def test_process_alert_handles_errors(
    mock_agent: Any,
    sample_alert_with_fingerprint: Dict[str, Any]
) -> None:
    """Test that _process_alert handles errors gracefully.
    
    Args:
        mock_agent: Mocked global agent instance.
        sample_alert_with_fingerprint: Sample alert data.
    """
    from oncallm.main import _process_alert
    
    # Setup mock to raise an error.
    mock_agent.do_analysis.side_effect = Exception("API error")
    
    alert_group = AlertGroup(**sample_alert_with_fingerprint)
    fingerprint = "test123fingerprint"
    
    with patch("oncallm.main._analysis_reports") as mock_reports:
        _process_alert(fingerprint, alert_group)
        
        # Verify error was handled and stored.
        mock_reports.__setitem__.assert_called_once()
        stored_report = mock_reports.__setitem__.call_args[0][1]
        assert stored_report["status"] == "failed"
        assert "API error" in stored_report["error"]


def test_extract_alert_info_function() -> None:
    """Test the _extract_alert_info function."""
    from oncallm.main import _extract_alert_info
    
    sample_alert_group = {
        "alerts": [{
            "labels": {
                "alertname": "TestAlert",
                "namespace": "production",
                "pod": "test-pod-456",
                "service": "test-service",
                "severity": "warning"
            },
            "annotations": {
                "summary": "Test summary",
                "description": "Test description"
            },
            "startsAt": "2024-01-01T12:00:00Z"
        }]
    }
    
    result = _extract_alert_info(sample_alert_group)
    
    assert result["name"] == "TestAlert"
    assert result["namespace"] == "production"
    assert result["pod"] == "test-pod-456"
    assert result["service"] == "test-service"
    assert result["severity"] == "warning"
    assert result["summary"] == "Test summary"
    assert result["description"] == "Test description"
    assert result["started_at"] == "2024-01-01T12:00:00Z"


def test_extract_alert_info_with_empty_data() -> None:
    """Test _extract_alert_info with empty or missing data."""
    from oncallm.main import _extract_alert_info
    
    # Test with empty dict.
    result = _extract_alert_info({})
    assert result == {}
    
    # Test with missing alerts key.
    result = _extract_alert_info({"other_key": "value"})
    assert result == {}


def test_template_renderer_initialization() -> None:
    """Test that template renderer is properly initialized."""
    from oncallm.template_renderer import TemplateRenderer
    
    # Test that renderer can be created with default template directory.
    renderer = TemplateRenderer()
    assert renderer.template_dir.name == "templates"


def test_template_renderer_with_custom_directory() -> None:
    """Test template renderer with custom template directory."""
    from oncallm.template_renderer import TemplateRenderer
    import pytest
    
    # Test with non-existent directory should raise FileNotFoundError.
    with pytest.raises(FileNotFoundError):
        TemplateRenderer("non_existent_directory") 