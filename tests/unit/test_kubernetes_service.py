import pytest
from unittest.mock import MagicMock, patch
from kubernetes.client.rest import ApiException

# Adjust the import path based on your project structure assuming 'oncallm' is in PYTHONPATH.
from oncallm.kubernetes_service import KubernetesService

@pytest.fixture
def mock_k8s_client_v1():
    mock_client = MagicMock()
    # Mock specific methods if needed for setup, e.g.,
    # mock_client.read_namespaced_pod.return_value = ...
    return mock_client

@pytest.fixture
def mock_k8s_client_apps_v1():
    mock_client = MagicMock()
    return mock_client

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_kubernetes_service_initialization(
    mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config,
    mock_k8s_client_v1, mock_k8s_client_apps_v1
):
    """Test that KubernetesService initializes CoreV1Api and AppsV1Api clients."""
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1

    service = KubernetesService()

    mock_load_kube_config.assert_called_once()
    mock_core_v1_api.assert_called_once()
    mock_apps_v1_api.assert_called_once()
    assert service.core_v1 is not None
    assert service.apps_v1 is not None

# Example test for one method - get_pod_details
@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_pod_details_success(
    mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, # Order matters for @patch
    mock_k8s_client_v1, mock_k8s_client_apps_v1 # These are fixtures
):
    """Test get_pod_details successfully returns pod information."""
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1

    # Create a mock pod object with proper attributes
    mock_pod = MagicMock()
    mock_pod.metadata.name = "test-pod"
    mock_pod.metadata.namespace = "default"
    mock_pod.status.phase = "Running"
    mock_pod.status.host_ip = "10.0.0.1"
    mock_pod.status.pod_ip = "10.0.0.2"
    mock_pod.status.start_time = "2024-01-01T12:00:00Z"
    mock_container = MagicMock()
    mock_container.name = "test-container"
    mock_container.image = "test-image"
    mock_pod.spec.containers = [mock_container]
    
    mock_container_status = MagicMock()
    mock_container_status.name = "test-container"
    mock_container_status.ready = True
    mock_container_status.restart_count = 0
    mock_pod.status.container_statuses = [mock_container_status]
    mock_k8s_client_v1.read_namespaced_pod.return_value = mock_pod

    service = KubernetesService()
    namespace = "default"
    pod_name = "test-pod"

    result = service.get_pod_details(namespace, pod_name)

    mock_k8s_client_v1.read_namespaced_pod.assert_called_once_with(name=pod_name, namespace=namespace)
    assert result["name"] == "test-pod"
    assert result["namespace"] == "default"
    assert result["status"] == "Running"
    assert result["host_ip"] == "10.0.0.1"
    assert result["pod_ip"] == "10.0.0.2"
    assert len(result["containers"]) == 1
    assert result["containers"][0]["name"] == "test-container"
    assert result["containers"][0]["image"] == "test-image"

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_pod_details_api_exception(
    mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config,
    mock_k8s_client_v1, mock_k8s_client_apps_v1
):
    """Test get_pod_details handles ApiException and returns an error message."""
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1

    mock_k8s_client_v1.read_namespaced_pod.side_effect = ApiException(status=404, reason="Not Found")

    service = KubernetesService()
    namespace = "default"
    pod_name = "non-existent-pod"

    result = service.get_pod_details(namespace, pod_name)

    mock_k8s_client_v1.read_namespaced_pod.assert_called_once_with(name=pod_name, namespace=namespace)
    assert isinstance(result, dict)
    assert "error" in result
    assert "status_code" in result
    assert result["status_code"] == 404
    assert "Not Found" in result["error"]

# Tests for get_service_details
@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_service_details_success(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    # Create a mock service object with proper attributes
    mock_service = MagicMock()
    mock_service.metadata.name = "test-service"
    mock_service.metadata.namespace = "default"
    mock_service.spec.cluster_ip = "10.0.0.100"
    mock_service.spec.type = "ClusterIP"
    mock_port = MagicMock()
    mock_port.name = "http"
    mock_port.port = 80
    mock_port.target_port = 8080
    mock_port.protocol = "TCP"
    mock_service.spec.ports = [mock_port]
    mock_service.spec.selector = {"app": "test-app"}
    mock_k8s_client_v1.read_namespaced_service.return_value = mock_service

    service = KubernetesService()
    result = service.get_service_details("default", "test-service")

    mock_k8s_client_v1.read_namespaced_service.assert_called_once_with(name="test-service", namespace="default")
    assert result["name"] == "test-service"
    assert result["namespace"] == "default"
    assert result["cluster_ip"] == "10.0.0.100"
    assert result["type"] == "ClusterIP"
    assert len(result["ports"]) == 1
    assert result["ports"][0]["name"] == "http"
    assert result["ports"][0]["port"] == 80

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_service_details_api_exception(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    mock_k8s_client_v1.read_namespaced_service.side_effect = ApiException(status=404, reason="Not Found")

    service = KubernetesService()
    result = service.get_service_details("default", "test-service")

    assert isinstance(result, dict)
    assert "error" in result
    assert "status_code" in result
    assert result["status_code"] == 404
    assert "Not Found" in result["error"]

# Tests for get_pod_logs
@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_pod_logs_success(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    expected_logs = "Log line 1\nLog line 2"
    mock_k8s_client_v1.read_namespaced_pod_log.return_value = expected_logs

    service = KubernetesService()
    result = service.get_pod_logs("default", "test-pod")

    mock_k8s_client_v1.read_namespaced_pod_log.assert_called_once_with(name="test-pod", namespace="default", container=None, tail_lines=100)
    assert result == expected_logs

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_pod_logs_api_exception(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    mock_k8s_client_v1.read_namespaced_pod_log.side_effect = ApiException(status=500, reason="Server Error")

    service = KubernetesService()
    result = service.get_pod_logs("default", "test-pod")

    assert isinstance(result, str)
    assert "Error getting logs" in result
    assert "500" in result
    assert "Server Error" in result

# Tests for list_pods_for_service
@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_list_pods_for_service_success(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1

    # Mock service to get selectors
    mock_service_info = MagicMock()
    mock_service_info.spec.selector = {"app": "my-app"}
    mock_k8s_client_v1.read_namespaced_service.return_value = mock_service_info

    # Mock pods list
    mock_pod_list = MagicMock()
    mock_pod1 = MagicMock()
    mock_pod1.metadata.name = "pod1"
    mock_pod1.metadata.namespace = "default"
    mock_pod1.status.phase = "Running"
    mock_pod1.status.host_ip = "10.0.0.1"
    mock_pod1.status.pod_ip = "10.0.0.2"
    mock_pod1.status.start_time = "2024-01-01T12:00:00Z"
    
    mock_pod2 = MagicMock()
    mock_pod2.metadata.name = "pod2"
    mock_pod2.metadata.namespace = "default"
    mock_pod2.status.phase = "Running"
    mock_pod2.status.host_ip = "10.0.0.3"
    mock_pod2.status.pod_ip = "10.0.0.4"
    mock_pod2.status.start_time = "2024-01-01T12:00:00Z"
    
    mock_pod_list.items = [mock_pod1, mock_pod2]
    mock_k8s_client_v1.list_namespaced_pod.return_value = mock_pod_list

    service = KubernetesService()
    result = service.list_pods_for_service("default", "test-service")

    mock_k8s_client_v1.read_namespaced_service.assert_called_once_with(name="test-service", namespace="default")
    mock_k8s_client_v1.list_namespaced_pod.assert_called_once_with(namespace="default", label_selector="app=my-app")
    assert len(result) == 2
    assert result[0]["name"] == "pod1"
    assert result[1]["name"] == "pod2"

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_list_pods_for_service_no_selector(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    mock_service_info = MagicMock()
    mock_service_info.spec.selector = None # No selector
    mock_k8s_client_v1.read_namespaced_service.return_value = mock_service_info

    service = KubernetesService()
    result = service.list_pods_for_service("default", "test-service")

    assert result == []
    mock_k8s_client_v1.list_namespaced_pod.assert_not_called()

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_list_pods_for_service_api_exception_on_get_service(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    mock_k8s_client_v1.read_namespaced_service.side_effect = ApiException(status=404, reason="Not Found")

    service = KubernetesService()
    result = service.list_pods_for_service("default", "test-service")

    assert result == []

# Tests for get_deployment_details
@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api') # CoreV1Api is not used by get_deployment_details, but patch order
@patch('kubernetes.client.AppsV1Api')
def test_get_deployment_details_success(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1 # Not strictly needed by this test but for consistency
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    # Create a mock deployment object with proper attributes
    mock_deployment = MagicMock()
    mock_deployment.metadata.name = "test-deployment"
    mock_deployment.metadata.namespace = "default"
    mock_deployment.spec.replicas = 3
    mock_deployment.status.available_replicas = 3
    mock_deployment.status.ready_replicas = 3
    mock_deployment.status.unavailable_replicas = 0
    mock_deployment.spec.strategy.type = "RollingUpdate"
    mock_deployment.spec.selector.match_labels = {"app": "test-app"}
    mock_container = MagicMock()
    mock_container.name = "test-container"
    mock_container.image = "test-image:latest"
    mock_container.resources.requests = {"cpu": "100m", "memory": "128Mi"}
    mock_container.resources.limits = {"cpu": "200m", "memory": "256Mi"}
    mock_deployment.spec.template.spec.containers = [mock_container]
    mock_k8s_client_apps_v1.read_namespaced_deployment.return_value = mock_deployment

    service = KubernetesService()
    result = service.get_deployment_details("default", "test-deployment")

    mock_k8s_client_apps_v1.read_namespaced_deployment.assert_called_once_with(name="test-deployment", namespace="default")
    assert result["name"] == "test-deployment"
    assert result["namespace"] == "default"
    assert result["replicas"]["desired"] == 3
    assert result["replicas"]["available"] == 3
    assert result["strategy"] == "RollingUpdate"
    assert len(result["containers"]) == 1
    assert result["containers"][0]["name"] == "test-container"

@patch('kubernetes.config.load_kube_config')
@patch('kubernetes.client.CoreV1Api')
@patch('kubernetes.client.AppsV1Api')
def test_get_deployment_details_api_exception(mock_apps_v1_api, mock_core_v1_api, mock_load_kube_config, mock_k8s_client_v1, mock_k8s_client_apps_v1):
    mock_core_v1_api.return_value = mock_k8s_client_v1
    mock_apps_v1_api.return_value = mock_k8s_client_apps_v1
    mock_k8s_client_apps_v1.read_namespaced_deployment.side_effect = ApiException(status=403, reason="Forbidden")

    service = KubernetesService()
    result = service.get_deployment_details("default", "test-deployment")

    assert isinstance(result, dict)
    assert "error" in result
    assert "status_code" in result
    assert result["status_code"] == 403
    assert "Forbidden" in result["error"]
