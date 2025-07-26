"""Tests for the template renderer module."""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from oncallm.template_renderer import TemplateRenderer


@pytest.fixture
def temp_template_dir():
    """Create a temporary template directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        template_dir = Path(temp_dir) / "templates"
        template_dir.mkdir()
        
        # Create sample templates for testing.
        processing_template = template_dir / "processing.html"
        processing_template.write_text("""
        <html>
        <head><title>Processing</title></head>
        <body>
            <h1>Processing Alert {{fingerprint}}</h1>
        </body>
        </html>
        """)
        
        failed_template = template_dir / "failed.html"
        failed_template.write_text("""
        <html>
        <head><title>Failed</title></head>
        <body>
            <h1>Failed Alert {{fingerprint}}</h1>
            <p>Error: {{error_message}}</p>
        </body>
        </html>
        """)
        
        completed_template = template_dir / "completed.html"
        completed_template.write_text("""
        <html>
        <head><title>{{alert_name}} Analysis</title></head>
        <body>
            <h1>Alert: {{alert_name}}</h1>
            <p>Namespace: {{namespace}}</p>
            <p>Root Cause: {{root_cause}}</p>
            <p>Diagnosis: {{diagnosis}}</p>
        </body>
        </html>
        """)
        
        yield str(template_dir)


def test_template_renderer_initialization(temp_template_dir: str) -> None:
    """Test template renderer initialization."""
    renderer = TemplateRenderer(temp_template_dir)
    assert renderer.template_dir == Path(temp_template_dir)


def test_template_renderer_nonexistent_directory() -> None:
    """Test template renderer with non-existent directory."""
    with pytest.raises(FileNotFoundError):
        TemplateRenderer("non_existent_directory")


def test_load_template_success(temp_template_dir: str) -> None:
    """Test successful template loading."""
    renderer = TemplateRenderer(temp_template_dir)
    
    template_content = renderer._load_template("processing")
    assert "Processing Alert {{fingerprint}}" in template_content


def test_load_template_not_found(temp_template_dir: str) -> None:
    """Test loading non-existent template."""
    renderer = TemplateRenderer(temp_template_dir)
    
    with pytest.raises(FileNotFoundError):
        renderer._load_template("nonexistent")


def test_render_template_with_data(temp_template_dir: str) -> None:
    """Test template rendering with data substitution."""
    renderer = TemplateRenderer(temp_template_dir)
    
    template_content = "<h1>Hello {{name}}</h1><p>Age: {{age}}</p>"
    data = {"name": "John", "age": 30}
    
    result = renderer._render_template(template_content, data)
    assert result == "<h1>Hello John</h1><p>Age: 30</p>"


def test_render_processing_page(temp_template_dir: str) -> None:
    """Test rendering processing page."""
    renderer = TemplateRenderer(temp_template_dir)
    
    result = renderer.render_processing_page("test123")
    
    assert "Processing Alert test123" in result
    assert "<title>Processing</title>" in result


def test_render_failed_page(temp_template_dir: str) -> None:
    """Test rendering failed page."""
    renderer = TemplateRenderer(temp_template_dir)
    
    result = renderer.render_failed_page("test456", "API Error")
    
    assert "Failed Alert test456" in result
    assert "Error: API Error" in result


def test_render_completed_page(temp_template_dir: str) -> None:
    """Test rendering completed page."""
    renderer = TemplateRenderer(temp_template_dir)
    
    alert_info = {
        "name": "PodCrashLooping",
        "namespace": "default",
        "service": "web-service",
        "pod": "web-pod-123",
        "severity": "critical",
        "started_at": "2024-01-01T12:00:00Z",
        "summary": "Pod is crashing",
        "description": "Pod keeps restarting"
    }
    
    analysis = {
        "root_cause": "Out of memory",
        "diagnosis": "Memory limit exceeded",
        "summary_of_findings": "High memory usage detected",
        "recommended_actions": "Increase memory limits",
        "solution": "Update deployment configuration",
        "conclusion": "Memory optimization needed",
        "recommendations": "Monitor resource usage"
    }
    
    result = renderer.render_completed_page(
        "test789", alert_info, analysis, "2024-01-01T12:30:00Z"
    )
    
    assert "Alert: PodCrashLooping" in result
    assert "Namespace: default" in result
    assert "Root Cause: Out of memory" in result
    assert "Diagnosis: Memory limit exceeded" in result
    assert "<title>PodCrashLooping Analysis</title>" in result


def test_render_completed_page_with_missing_data(temp_template_dir: str) -> None:
    """Test rendering completed page with missing data."""
    renderer = TemplateRenderer(temp_template_dir)
    
    # Empty alert info and analysis.
    alert_info = {}
    analysis = {}
    
    result = renderer.render_completed_page(
        "test999", alert_info, analysis, "Unknown"
    )
    
    # Should use default values for missing data.
    assert "Alert: Unknown" in result
    assert "Namespace: Unknown" in result
    assert "Root Cause: No root cause identified" in result
    assert "Diagnosis: No detailed diagnosis available" in result


def test_template_data_escaping(temp_template_dir: str) -> None:
    """Test that template data is properly handled (basic string conversion)."""
    renderer = TemplateRenderer(temp_template_dir)
    
    # Test with various data types.
    template_content = "Number: {{number}}, Boolean: {{boolean}}, None: {{none_value}}"
    data = {
        "number": 42,
        "boolean": True,
        "none_value": None
    }
    
    result = renderer._render_template(template_content, data)
    assert result == "Number: 42, Boolean: True, None: None"


def test_template_with_special_characters(temp_template_dir: str) -> None:
    """Test template rendering with special characters."""
    renderer = TemplateRenderer(temp_template_dir)
    
    template_content = "Message: {{message}}"
    data = {"message": "Alert: <script>alert('test')</script>"}
    
    result = renderer._render_template(template_content, data)
    # Note: This is basic string substitution, not HTML escaping.
    assert "Alert: <script>alert('test')</script>" in result


def test_multiple_placeholder_replacements(temp_template_dir: str) -> None:
    """Test that multiple instances of the same placeholder are replaced."""
    renderer = TemplateRenderer(temp_template_dir)
    
    template_content = "{{name}} said {{name}} is great. {{name}} rocks!"
    data = {"name": "Alice"}
    
    result = renderer._render_template(template_content, data)
    assert result == "Alice said Alice is great. Alice rocks!"


def test_missing_placeholder_data(temp_template_dir: str) -> None:
    """Test rendering with missing placeholder data."""
    renderer = TemplateRenderer(temp_template_dir)
    
    template_content = "Hello {{name}}, your age is {{age}}"
    data = {"name": "Bob"}  # Missing 'age' key.
    
    result = renderer._render_template(template_content, data)
    # Missing placeholders should remain unchanged.
    assert result == "Hello Bob, your age is {{age}}" 