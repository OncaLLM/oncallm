import os
import logging
from typing import Dict, List, Optional, Any
from kubernetes import client, config
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)

class KubernetesService:
    def __init__(self):
        """
        Initialize the Kubernetes client.
        
        Tries to load in-cluster config first (for running inside Kubernetes).
        If that fails, falls back to kubeconfig (for running outside Kubernetes).
        Optionally uses KUBECONFIG environment variable or defaults to ~/.kube/config.
        """
        try:
            # Try to load in-cluster config first.
            config.load_incluster_config()
            logger.info("Kubernetes client initialized with in-cluster config.")
        except Exception as incluster_exc:
            kubeconfig_path = os.environ.get("KUBECONFIG", os.path.expanduser("~/.kube/config"))
            try:
                # Fall back to kubeconfig if not running inside a cluster.
                config.load_kube_config(config_file=kubeconfig_path)
                logger.info(f"Kubernetes client initialized with kubeconfig: {kubeconfig_path}.")
            except Exception as kubeconfig_exc:
                logger.error(f"Failed to initialize Kubernetes client: in-cluster error: {incluster_exc}, kubeconfig error: {kubeconfig_exc}")
                raise
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def get_pod_details(self, namespace: str, pod_name: str) -> Dict[str, Any]:
        """
        Get details of a specific pod.
        
        Args:
            namespace: Kubernetes namespace
            pod_name: Name of the pod
            
        Returns:
            Dictionary with pod details
        """
        try:
            logger.debug(f"🔍 K8S API: Getting pod details for {namespace}/{pod_name}")
            pod = self.core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            
            result = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "host_ip": pod.status.host_ip,
                "pod_ip": pod.status.pod_ip,
                "start_time": pod.status.start_time,
                "containers": [
                    {
                        "name": container.name,
                        "image": container.image,
                        "ready": next(
                            (status.ready for status in pod.status.container_statuses if status.name == container.name),
                            False
                        ),
                        "restart_count": next(
                            (status.restart_count for status in pod.status.container_statuses if status.name == container.name),
                            0
                        )
                    }
                    for container in pod.spec.containers
                ]
            }
            logger.debug(f"✅ K8S API: Pod details retrieved - Status: {result['status']}, Containers: {[c['name'] for c in result['containers']]}")
            return result
        except ApiException as e:
            logger.error(f"❌ K8S API: Error getting pod details: {e}")
            return {"error": str(e), "status_code": e.status}
    
    def get_service_details(self, namespace: str, service_name: str) -> Dict[str, Any]:
        """
        Get details of a specific service.
        
        Args:
            namespace: Kubernetes namespace
            service_name: Name of the service
            
        Returns:
            Dictionary with service details
        """
        try:
            service = self.core_v1.read_namespaced_service(name=service_name, namespace=namespace)
            return {
                "name": service.metadata.name,
                "namespace": service.metadata.namespace,
                "cluster_ip": service.spec.cluster_ip,
                "type": service.spec.type,
                "ports": [
                    {
                        "name": port.name,
                        "port": port.port,
                        "target_port": port.target_port,
                        "protocol": port.protocol
                    }
                    for port in service.spec.ports
                ],
                "selector": service.spec.selector
            }
        except ApiException as e:
            logger.error(f"Error getting service details: {e}")
            return {"error": str(e), "status_code": e.status}
    
    def get_pod_logs(self, namespace: str, pod_name: str, container: Optional[str] = None, 
                     tail_lines: int = 100) -> str:
        """
        Get logs from a specific pod.
        
        Args:
            namespace: Kubernetes namespace
            pod_name: Name of the pod
            container: Optional container name (if pod has multiple containers)
            tail_lines: Number of lines to get from the end of the logs
            
        Returns:
            Pod logs as a string
        """
        try:
            container_info = f" (container: {container})" if container else ""
            logger.debug(f"🔍 K8S API: Getting logs from {namespace}/{pod_name}{container_info}, tail_lines={tail_lines}")
            
            logs = self.core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                tail_lines=tail_lines
            )
            
            log_preview = logs[:200] + "..." if len(logs) > 200 else logs
            logger.debug(f"✅ K8S API: Pod logs retrieved ({len(logs)} chars) - Preview: {log_preview}")
            return logs
        except ApiException as e:
            logger.error(f"❌ K8S API: Error getting pod logs: {e}")
            return f"Error getting logs: {e}"
    
    def list_pods_for_service(self, namespace: str, service_name: str) -> List[Dict[str, Any]]:
        """
        List all pods associated with a service based on label selectors.
        
        Args:
            namespace: Kubernetes namespace
            service_name: Name of the service
            
        Returns:
            List of pod details
        """
        try:
            service = self.core_v1.read_namespaced_service(name=service_name, namespace=namespace)
            if not service.spec.selector:
                return []
            
            # Construct label selector string from the service's selector
            label_selector = ",".join([f"{k}={v}" for k, v in service.spec.selector.items()])
            
            pods = self.core_v1.list_namespaced_pod(
                namespace=namespace,
                label_selector=label_selector
            )
            
            return [
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "host_ip": pod.status.host_ip,
                    "pod_ip": pod.status.pod_ip,
                    "start_time": pod.status.start_time
                }
                for pod in pods.items
            ]
        except ApiException as e:
            logger.error(f"Error listing pods for service: {e}")
            return []
    
    def get_deployment_details(self, namespace: str, deployment_name: str) -> Dict[str, Any]:
        """
        Get details of a specific deployment.
        
        Args:
            namespace: Kubernetes namespace
            deployment_name: Name of the deployment
            
        Returns:
            Dictionary with deployment details
        """
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=deployment_name, 
                namespace=namespace
            )
            
            return {
                "name": deployment.metadata.name,
                "namespace": deployment.metadata.namespace,
                "replicas": {
                    "desired": deployment.spec.replicas,
                    "available": deployment.status.available_replicas,
                    "ready": deployment.status.ready_replicas,
                    "unavailable": deployment.status.unavailable_replicas
                },
                "strategy": deployment.spec.strategy.type,
                "selector": deployment.spec.selector.match_labels,
                "containers": [
                    {
                        "name": container.name,
                        "image": container.image,
                        "resources": {
                            "requests": container.resources.requests if container.resources and container.resources.requests else {},
                            "limits": container.resources.limits if container.resources and container.resources.limits else {}
                        }
                    }
                    for container in deployment.spec.template.spec.containers
                ]
            }
        except ApiException as e:
            logger.error(f"Error getting deployment details: {e}")
            return {"error": str(e), "status_code": e.status}
