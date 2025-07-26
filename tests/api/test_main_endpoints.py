"""Tests for OnCallM main API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

# Assuming 'oncallm' is in PYTHONPATH and main.py defines 'app' and 'analysis_reports'
from oncallm.main import app, _analysis_reports
from oncallm.alerts import AlertGroup, Alert
from oncallm.llm_service import OncallK8sResponse

@pytest.fixture(scope="module")
def client():
    """Create a TestClient instance for the FastAPI app."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def clear_reports_before_each_test():
    """Ensure _analysis_reports is empty before each test."""
    _analysis_reports.clear()

@pytest.fixture
def sample_alert_group_dict():
    """Provides a sample AlertGroup as a dictionary, similar to incoming JSON."""
    return {
        "version": "4",
        "groupKey": "{}:{alertname='APITestAlert'}",
        "truncatedAlerts": 0,
        "status": "firing",
        "receiver": "api-test-receiver",
        "groupLabels": {"alertname": "APITestAlert"},
        "commonLabels": {"alertname": "APITestAlert", "severity": "warning", "namespace": "test-ns"},
        "commonAnnotations": {"summary": "API Test Alert Summary"},
        "externalURL": "http://alertmanager.example.com/api-test",
        "alerts": [
            {
                "status": "firing",
                "labels": {"alertname": "APITestAlert", "severity": "warning", "instance": "api-instance", "namespace": "test-ns"},
                "annotations": {"summary": "API Test Alert Summary", "description": "Detailed description of API test alert"},
                "startsAt": "2024-01-02T10:00:00Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "http://prometheus.example.com/graph?g0.expr=vector%282%29",
                "fingerprint": "apitestfingerprint"
            }
        ]
    }

@patch('oncallm.main._alert_queue', new_callable=lambda: AsyncMock())
@patch('oncallm.main._agent', new_callable=lambda: MagicMock())
def test_webhook_success(mock_agent, mock_alert_queue, client, sample_alert_group_dict):
    """Test successful alert ingestion via /webhook."""
    # Mock the alert queue
    mock_alert_queue.put = AsyncMock()
    
    response = client.post("/webhook", json=sample_alert_group_dict)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "success"
    assert "report_urls" in json_response
    assert len(json_response["report_urls"]) == 1
    
    # Check the report URL structure
    report_info = json_response["report_urls"][0]
    assert report_info["fingerprint"] == "apitestfingerprint"
    assert report_info["alert_name"] == "APITestAlert"
    assert report_info["namespace"] == "test-ns"
    assert "/report/apitestfingerprint" in report_info["report_url"]

    # Initially, the report should be in "processing" status
    fingerprint = "apitestfingerprint"
    assert fingerprint in _analysis_reports
    assert _analysis_reports[fingerprint]["status"] == "processing"

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "healthy"
    assert "kubernetes_access" in json_response
    assert "kubernetes_config" in json_response

def test_root_endpoint(client):
    """Test the root / endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == "OnCallM Agent"
    assert "available_endpoints" in json_response

def test_get_reports_empty(client):
    """Test /reports endpoint when no reports exist."""
    response = client.get("/reports")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["reports"] == []

@patch('oncallm.main._alert_queue', new_callable=lambda: AsyncMock())
@patch('oncallm.main._agent', new_callable=lambda: MagicMock())
def test_get_reports_with_data(mock_agent, mock_alert_queue, client, sample_alert_group_dict):
    """Test /reports endpoint after an alert has been processed."""
    mock_alert_queue.put = AsyncMock()
    
    # Post an alert to populate _analysis_reports
    post_response = client.post("/webhook", json=sample_alert_group_dict)
    fingerprint = "apitestfingerprint"
    
    # Simulate completion of async processing by updating the report
    mock_analysis_data = {
        "root_cause": "Report 1 Data",
        "conclusion": "Test Conclusion", 
        "diagnosis": "Test Diagnosis",
        "summary_of_findings": "Test Summary",
        "recommended_actions": "Test Actions",
        "recommendations": "Test Recommendations",
        "solution": "Test Solution"
    }
    
    _analysis_reports[fingerprint] = {
        "status": "completed",
        "analysis": mock_analysis_data,
        "created_at": "2024-01-02T10:00:00Z",
        "fingerprint": fingerprint
    }

    response = client.get("/reports")
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["reports"]) == 1
    
    report = json_response["reports"][0]
    assert report["fingerprint"] == fingerprint
    assert report["status"] == "completed"
    assert report["created_at"] == "2024-01-02T10:00:00Z"

@patch('oncallm.main._alert_queue', new_callable=lambda: AsyncMock())
@patch('oncallm.main._agent', new_callable=lambda: MagicMock())
def test_get_report_by_fingerprint_success(mock_agent, mock_alert_queue, client, sample_alert_group_dict):
    """Test retrieving a specific report by fingerprint."""
    mock_alert_queue.put = AsyncMock()
    
    post_response = client.post("/webhook", json=sample_alert_group_dict)
    fingerprint = "apitestfingerprint"
    
    # Simulate completion of async processing by updating the report
    mock_analysis_data = {
        "root_cause": "Specific Root Cause",
        "conclusion": "Specific Report Conclusion",
        "diagnosis": "Specific Diagnosis",
        "summary_of_findings": "Specific Summary",
        "recommended_actions": "Specific Actions",
        "recommendations": "Specific Recommendations",
        "solution": "Specific Solution"
    }
    
    _analysis_reports[fingerprint] = {
        "status": "completed",
        "analysis": mock_analysis_data,
        "created_at": "2024-01-02T10:00:00Z",
        "fingerprint": fingerprint
    }

    response = client.get(f"/reports/{fingerprint}")
    assert response.status_code == 200
    report_data = response.json()
    assert report_data["analysis"]["conclusion"] == "Specific Report Conclusion"
    assert report_data["status"] == "completed"
    assert report_data["fingerprint"] == fingerprint

def test_get_report_by_fingerprint_not_found(client):
    """Test retrieving a non-existent report by fingerprint."""
    response = client.get("/reports/non-existent-fingerprint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Report not found"}

@patch('oncallm.main._template_renderer')
def test_get_report_html_endpoint(mock_template_renderer, client):
    """Test the HTML report endpoint."""
    fingerprint = "test-html-fingerprint"
    
    # Create a test report
    _analysis_reports[fingerprint] = {
        "status": "completed",
        "analysis": {
            "root_cause": "Test root cause",
            "diagnosis": "Test diagnosis"
        },
        "alert_group": {
            "alerts": [{
                "labels": {"alertname": "TestAlert", "namespace": "default"},
                "annotations": {"summary": "Test summary"},
                "startsAt": "2024-01-02T10:00:00Z"
            }]
        },
        "created_at": "2024-01-02T10:00:00Z",
        "fingerprint": fingerprint
    }
    
    # Mock the template renderer
    mock_template_renderer.render_completed_page.return_value = """
    <html><body><h1>Test Report</h1></body></html>
    """
    
    response = client.get(f"/report/{fingerprint}")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Test Report" in response.text

@patch('oncallm.main._template_renderer')
def test_get_report_html_processing_state(mock_template_renderer, client):
    """Test the HTML report endpoint for processing state."""
    fingerprint = "processing-fingerprint"
    
    # Create a processing report
    _analysis_reports[fingerprint] = {"status": "processing"}
    
    # Mock the template renderer
    mock_template_renderer.render_processing_page.return_value = """
    <html><body><h1>Processing...</h1></body></html>
    """
    
    response = client.get(f"/report/{fingerprint}")
    assert response.status_code == 200
    assert "Processing..." in response.text

def test_get_report_html_not_found(client):
    """Test the HTML report endpoint for non-existent report."""
    response = client.get("/report/non-existent-fingerprint")
    assert response.status_code == 404
