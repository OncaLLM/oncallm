import pytest
from unittest.mock import MagicMock, patch, ANY
from datetime import datetime

# Assuming 'oncallm' is in PYTHONPATH
from oncallm.llm_service import OncallmAgent
from oncallm.alerts import AlertGroup, Alert, AlertAnnotation, AlertLabel, OncallK8sResponse # For creating test AlertGroup

# Mock for KubernetesService if its methods are called during OncallmAgent setup
@pytest.fixture
def mock_kubernetes_service():
    service = MagicMock()
    # Mock any methods of KubernetesService that might be called by OncallmAgent's tools
    service.get_pod_details.return_value = {"name": "mocked-pod-details"}
    service.get_service_details.return_value = {"name": "mocked-service-details"}
    service.get_pod_logs.return_value = "mocked pod logs"
    service.list_pods_for_service.return_value = [{"name": "mocked-pod-in-list"}]
    service.get_deployment_details.return_value = {"name": "mocked-deployment-details"}
    return service

@pytest.fixture
def minimal_alert_group():
    """Provides a minimal AlertGroup for testing."""
    return AlertGroup(
        version="4",
        groupKey="{}:{alertname='TestAlert'}",
        truncatedAlerts=0,
        status="firing",
        receiver="test-receiver",
        groupLabels={"alertname": "TestAlert"},
        commonLabels={"alertname": "TestAlert", "severity": "critical", "namespace": "default"},
        commonAnnotations={"summary": "This is a test alert"},
        externalURL="http://alertmanager.example.com",
        alerts=[
            Alert(
                status="firing",
                labels=AlertLabel(alertname="TestAlert", severity="critical", instance="test-instance", namespace="default"),
                annotations=AlertAnnotation(summary="This is a test alert", description="Detailed description of test alert"),
                startsAt=datetime(2024, 1, 1, 12, 0, 0),
                endsAt=None, # For ongoing alert
                generatorURL="http://prometheus.example.com/graph?g0.expr=vector%281%29",
                fingerprint="testfingerprint"
            )
        ]
    )

@patch('oncallm.llm_service.KubernetesService')
@patch('oncallm.llm_service.ChatOpenAI')
@patch('oncallm.llm_service.Tool') # To verify tools are created
@patch('oncallm.llm_service.create_react_agent')
@patch('oncallm.llm_service.get_system_prompt')
@patch('oncallm.llm_service.CallbackHandler') # Mock Langfuse handler
def test_oncallm_agent_setup_agent(
    mock_callback_handler, mock_get_system_prompt, mock_create_react_agent,
    mock_tool_constructor, mock_chat_openai, mock_k8s_service_constructor,
    mock_kubernetes_service # Fixture for instance
):
    """Test the setup_agent method initializes all components correctly."""
    mock_k8s_service_constructor.return_value = mock_kubernetes_service
    mock_chat_openai_instance = MagicMock()
    mock_chat_openai.return_value = mock_chat_openai_instance

    mock_system_prompt_obj = MagicMock()
    mock_system_prompt_obj.text = "Mocked system prompt"
    mock_get_system_prompt.return_value = mock_system_prompt_obj

    mock_agent_executor = MagicMock()
    mock_create_react_agent.return_value = mock_agent_executor

    mock_langfuse_handler_instance = MagicMock()
    mock_callback_handler.return_value = mock_langfuse_handler_instance

    agent = OncallmAgent() # This calls setup_agent in __init__

    mock_k8s_service_constructor.assert_called_once()
    mock_chat_openai.assert_called_once_with(
        model=ANY, # or specific model if you want to assert 'gpt-4.1'
        temperature=ANY, # or 0.4
        openai_api_base=ANY, # os.getenv("LLM_API_BASE")
        max_tokens=ANY # or 1024
    )

    # Verify tools were created (5 tools expected)
    assert mock_tool_constructor.call_count == 5
    # Could add more detailed checks for each tool's name and description if needed

    mock_get_system_prompt.assert_called_once_with(ANY) # ANY for the list of tools

    mock_create_react_agent.assert_called_once_with(
        mock_chat_openai_instance,
        ANY, # tools list
        prompt=ANY, # ChatPromptTemplate
        response_format=OncallK8sResponse
    )
    assert agent.agent == mock_agent_executor
    mock_callback_handler.assert_called_once_with()
    assert agent.langfuse_handler == mock_langfuse_handler_instance


@patch('oncallm.llm_service.KubernetesService') # To control the instance used by agent
@patch('oncallm.llm_service.ChatOpenAI') # Mock the LLM
@patch('oncallm.llm_service.create_react_agent') # Mock the agent creation
@patch('oncallm.llm_service.get_system_prompt') # Mock system prompt
@patch('oncallm.llm_service.CallbackHandler') # Mock callback handler
def test_do_analysis(
    mock_callback_handler,
    mock_get_system_prompt,
    mock_create_react_agent,
    mock_chat_openai,
    mock_k8s_service_constructor,
    minimal_alert_group,
    mock_kubernetes_service # Fixture
):
    """Test the do_analysis method correctly invokes the agent."""
    
    # Set up all the mocks for the constructor
    mock_k8s_service_constructor.return_value = mock_kubernetes_service
    mock_chat_openai.return_value = MagicMock()
    mock_get_system_prompt.return_value = MagicMock(text="Test prompt")
    mock_callback_handler.return_value = MagicMock()
    
    # Mock the agent executor
    mock_agent_executor = MagicMock()
    mock_create_react_agent.return_value = mock_agent_executor
    
    agent_instance = OncallmAgent() # This will now use our mocked dependencies

    mock_response_data = {
        "root_cause": "Test Root Cause",
        "conclusion": "Test Conclusion",
        "diagnosis": "Test Diagnosis",
        "summary_of_findings": "Test Summary",
        "recommended_actions": "Action 1, Action 2",
        "recommendations": "Additional recommendations",
        "solution": "Test solution"
    }
    # The agent's invoke method returns a dict, and 'structured_response' is a key in it.
    # The value of 'structured_response' should be an OncallK8sResponse object.
    # However, the code being tested accesses response['structured_response'] directly.
    # So, the mock_invoke_result should be the dict that `agent.invoke` returns.
    mock_invoke_result = {
        'messages': [MagicMock()], # Placeholder for messages
        'structured_response': OncallK8sResponse(**mock_response_data) # This is what should be returned
    }
    mock_agent_executor.invoke.return_value = mock_invoke_result

    # The debug_request_to_string method should also be testable, but here we focus on do_analysis
    # For simplicity, we assume debug_request_to_string works as expected.

    result = agent_instance.do_analysis(minimal_alert_group)

    mock_agent_executor.invoke.assert_called_once_with(
        {"messages": [ANY]}, # Check that content is a HumanMessage with string content
        config={"callbacks": [agent_instance.langfuse_handler]}
    )

    # Check that the HumanMessage content is a JSON string containing the alert data
    invoked_call_args = mock_agent_executor.invoke.call_args[0][0]
    human_message_content = invoked_call_args['messages'][0].content
    import json
    parsed_content = json.loads(human_message_content)
    assert parsed_content["version"] == "4"
    assert parsed_content["status"] == "firing"
    assert parsed_content["receiver"] == "test-receiver"
    assert len(parsed_content["alerts"]) == 1
    assert parsed_content["alerts"][0]["status"] == "firing"

    assert isinstance(result, OncallK8sResponse)
    assert result.root_cause == "Test Root Cause"
    assert result.conclusion == "Test Conclusion"
