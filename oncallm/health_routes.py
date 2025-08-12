import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from oncallm.kubernetes_service import KubernetesService
from oncallm.llm_service import OncallmAgent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])

def get_k8s_service() -> KubernetesService:
    """Dependency to get a Kubernetes service instance."""
    # Try to use the configured kubeconfig path
    kubeconfig_path = os.environ.get("KUBECONFIG_PATH")
    return KubernetesService()

def get_llm_service() -> OncallmAgent:
    """Dependency to get an LLM service instance."""
    return OncallmAgent()

@router.get("/", response_model=Dict[str, Any])
async def health_check(
    k8s_service: KubernetesService = Depends(get_k8s_service),
    llm_service: OncallmAgent = Depends(get_llm_service)
):
    """
    Check the overall health of the application by testing all components.
    
    Args:
        k8s_service: Kubernetes service for direct API access
        llm_service: LLM service
        
    Returns:
        Comprehensive health status of all application components
    """
    k8s_health = _check_kubernetes_health(k8s_service)
    llm_health_result = _check_llm_health(llm_service)
    
    # Check if any component is unhealthy.
    if k8s_health["status"] != "healthy" or llm_health_result["status"] != "healthy":
        # Identify which components are unhealthy
        unhealthy_components = []
        if k8s_health["status"] != "healthy":
            unhealthy_components.append("kubernetes")
        if llm_health_result["status"] != "healthy":
            unhealthy_components.append("llm")
        
        # Return 503 Service Unavailable with detailed error information
        error_details = {
            "status": "unhealthy",
            "message": f"The following components are unhealthy: {', '.join(unhealthy_components)}",
            "unhealthy_components": unhealthy_components,
            "application": {
                "name": "OnCallM",
                "version": "1.0.0",
                "description": "AI-powered Kubernetes alert analysis"
            },
            "components": {
                "kubernetes": k8s_health,
                "llm": llm_health_result
            },
            "configuration": {
                "kubeconfig_path": os.environ.get("KUBECONFIG_PATH", "default"),
                "openai_api_configured": bool(os.environ.get("OPENAI_API_KEY"))
            }
        }
        raise HTTPException(status_code=503, detail=error_details)
    
    # All components are healthy
    return {
        "status": "healthy",
        "application": {
            "name": "OnCallM",
            "version": "1.0.0",
            "description": "AI-powered Kubernetes alert analysis"
        },
        "components": {
            "kubernetes": k8s_health,
            "llm": llm_health_result
        },
        "configuration": {
            "kubeconfig_path": os.environ.get("KUBECONFIG_PATH", "default"),
            "openai_api_configured": bool(os.environ.get("OPENAI_API_KEY"))
        }
    }

def _check_kubernetes_health(k8s_service: KubernetesService) -> Dict[str, Any]:
    """
    Internal function to check Kubernetes health.
    
    Args:
        k8s_service: Kubernetes service for direct API access
        
    Returns:
        Health status of the Kubernetes connection
    """
    try:
        # Test connection by trying to list pods in default namespace.
        _ = k8s_service.core_v1.list_namespaced_pod(namespace="default", limit=1)
        return {
            "status": "healthy",
            "connection_type": "direct API",
            "test_result": "Successfully connected to Kubernetes API"
        }
    except Exception as e:
        logger.error(f"Error checking Kubernetes health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

def _check_llm_health(llm_service: OncallmAgent) -> Dict[str, Any]:
    """
    Internal function to check LLM health.
    
    Args:
        llm_service: LLM service
        
    Returns:
        Health status of the LLM API connection
    """
    try:
        # Check if the OpenAI API key is set in environment variables
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            # Get model information from the LLM instance
            model_name = getattr(llm_service.llm, 'model_name', 'unknown')
            return {
                "status": "healthy",
                "model": model_name,
                "api_configured": True
            }
        else:
            return {
                "status": "unhealthy",
                "error": "No OpenAI API key configured",
                "api_configured": False
            }
    except Exception as e:
        logger.error(f"Error checking LLM API health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }
