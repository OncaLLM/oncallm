"""HTML template renderer for OnCallM alert reports.

This module provides functionality to load and render HTML templates
for different alert report states (processing, failed, completed).
"""

from pathlib import Path
from typing import Any, Dict


class TemplateRenderer:
    """Renders HTML templates with data substitution."""
    
    def __init__(self, template_dir: str = "templates") -> None:
        """Initialize the template renderer.
        
        Args:
            template_dir: Directory containing HTML templates.
        """
        self.template_dir = Path(template_dir)
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {template_dir}")
    
    def _load_template(self, template_name: str) -> str:
        """Load a template file from disk.
        
        Args:
            template_name: Name of the template file (without .html extension).
            
        Returns:
            Template content as string.
            
        Raises:
            FileNotFoundError: If template file doesn't exist.
        """
        template_path = self.template_dir / f"{template_name}.html"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render a template with data substitution.
        
        Args:
            template_content: Raw template content with {{placeholder}} markers.
            data: Dictionary of data to substitute in the template.
            
        Returns:
            Rendered HTML with data substituted.
        """
        rendered = template_content
        
        # Replace all {{key}} placeholders with corresponding values.
        for key, value in data.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        
        return rendered
    
    def render_processing_page(self, fingerprint: str) -> str:
        """Render the processing state page.
        
        Args:
            fingerprint: Unique fingerprint of the alert.
            
        Returns:
            Rendered HTML for processing page.
        """
        template = self._load_template("processing")
        data = {
            "fingerprint": fingerprint
        }
        return self._render_template(template, data)
    
    def render_failed_page(self, fingerprint: str, error_message: str) -> str:
        """Render the failed analysis page.
        
        Args:
            fingerprint: Unique fingerprint of the alert.
            error_message: Error message to display.
            
        Returns:
            Rendered HTML for failed page.
        """
        template = self._load_template("failed")
        data = {
            "fingerprint": fingerprint,
            "error_message": error_message
        }
        return self._render_template(template, data)
    
    def render_completed_page(
        self, 
        fingerprint: str, 
        alert_info: Dict[str, str], 
        analysis: Dict[str, Any],
        created_at: str
    ) -> str:
        """Render the completed analysis page.
        
        Args:
            fingerprint: Unique fingerprint of the alert.
            alert_info: Dictionary containing alert information.
            analysis: Dictionary containing AI analysis results.
            created_at: Timestamp when analysis was completed.
            
        Returns:
            Rendered HTML for completed analysis page.
        """
        template = self._load_template("completed")
        
        # Prepare data for template rendering.
        data = {
            "fingerprint": fingerprint,
            "alert_name": alert_info.get("name", "Unknown"),
            "namespace": alert_info.get("namespace", "Unknown"),
            "service": alert_info.get("service", "N/A"),
            "pod": alert_info.get("pod", "N/A"),
            "severity": alert_info.get("severity", "Unknown"),
            "started_at": alert_info.get("started_at", "Unknown"),
            "summary": alert_info.get("summary", "No summary"),
            "description": alert_info.get("description", "No description"),
            "root_cause": analysis.get("root_cause", "No root cause identified"),
            "diagnosis": analysis.get("diagnosis", "No detailed diagnosis available"),
            "summary_of_findings": analysis.get("summary_of_findings", "No summary available"),
            "recommended_actions": analysis.get("recommended_actions", "No recommendations available"),
            "solution": analysis.get("solution", "No solution provided"),
            "conclusion": analysis.get("conclusion", "No conclusion available"),
            "recommendations": analysis.get("recommendations", "No additional recommendations"),
            "created_at": created_at
        }
        
        return self._render_template(template, data)
