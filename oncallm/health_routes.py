import os
import logging
from fastapi import APIRouter, Depends
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
async def health_check():
    """
    Check the health of the application.
    
    Returns:
        Health status of the application
    """
    return {
        "status": "healthy",
        "kubernetes_access": "direct API",
        "kubernetes_config": os.environ.get("KUBECONFIG_PATH", "default")
    }


@router.get("/kubernetes", response_model=Dict[str, Any])
async def kubernetes_health(
        k8s_service: KubernetesService = Depends(get_k8s_service)
):
    """
    Check the health of the Kubernetes connection.
    
    Args:
        k8s_service: Kubernetes service for direct API access
        
    Returns:
        Health status of the Kubernetes connection
    """
    try:
        # Test connection by trying to list pods in default namespace.
        pods = k8s_service.core_v1.list_namespaced_pod(namespace="default", limit=1)
        print(pods)
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


@router.get("/llm", response_model=Dict[str, Any])
async def llm_health(
        llm_service: OncallmAgent = Depends(get_llm_service)
):
    """
    Check the health of the LLM API connection.
    
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
