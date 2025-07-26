import os
import json
import logging
from datetime import datetime
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from oncallm.kubernetes_service import KubernetesService
from oncallm.prompt import get_system_prompt
from langchain.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from oncallm.alerts import OncallK8sResponse, AlertGroup
from langchain_core.messages import HumanMessage
from langfuse.langchain import CallbackHandler  # type: ignore

logger = logging.getLogger(__name__)

class OncallmAgent:

    def __init__(self):
        """Set up the agent with tools and prompts."""
        # Instantiate your KubernetesService (adjust kubeconfig_path if needed)
        k8s_service = KubernetesService()  # or provide path if needed
        # Langfuse ≥3.0: credentials are configured via environment variables
        # or the singleton Langfuse client. The CallbackHandler takes no args.
        self.langfuse_handler = CallbackHandler()

        tools = [
            Tool(
                name="get_pod_details",
                func=lambda x: k8s_service.get_pod_details(
                    namespace=x.split('/')[0],
                    pod_name=x.split('/')[1]
                ),
                description="Use this to get detailed information about a specific pod. Input should be in format 'namespace/pod_name'."
            ),
            Tool(
                name="get_service_details",
                func=lambda x: k8s_service.get_service_details(
                    namespace=x.split('/')[0],
                    service_name=x.split('/')[1]
                ),
                description="Use this to retrieve details of a specific Kubernetes service. Input should be in format 'namespace/service_name'."
            ),
            Tool(
                name="get_pod_logs",
                func=lambda x: k8s_service.get_pod_logs(
                    namespace=x.split('/')[0],
                    pod_name=x.split('/')[1]
                ),
                description="Use this to fetch the logs of a pod. Input should be in format 'namespace/pod_name'."
            ),
            Tool(
                name="list_pods_for_service",
                func=lambda x: k8s_service.list_pods_for_service(
                    namespace=x.split('/')[0],
                    service_name=x.split('/')[1]
                ),
                description="Use this to list all pods associated with a Kubernetes service. Input should be in format 'namespace/service_name'."
            ),
            Tool(
                name="get_deployment_details",
                func=lambda x: k8s_service.get_deployment_details(
                    namespace=x.split('/')[0],
                    deployment_name=x.split('/')[1]
                ),
                description="Use this to get detailed information about a deployment. Input should be in format 'namespace/deployment_name'."
            ),
        ]

        self.llm = ChatOpenAI(
            model=os.getenv("LLM_MODEL", "gpt-4.1"),
            temperature=0.4,
            openai_api_base=os.getenv("LLM_API_BASE"),
            max_tokens=1024,
        )

        system_prompt = get_system_prompt(tools)

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("placeholder", "{messages}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        self.agent = create_react_agent(self.llm, tools, prompt=prompt, response_format=OncallK8sResponse)

    def debug_request_to_string(self, debug_request: AlertGroup) -> str:
        def default_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return str(obj)

        return json.dumps(debug_request.model_dump(), indent=2, default=default_serializer)


    def do_analysis(self, alert_group):
        res = self.debug_request_to_string(alert_group)
        print("Res: ", res)
        response = self.agent.invoke({"messages": [HumanMessage(content=res)]}, config={"callbacks": [self.langfuse_handler]})
        print("Response: ", response)
        return response['structured_response']
