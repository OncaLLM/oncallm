"""System prompt configuration for KubeDebugger LLM agent.

This module defines the system prompt used by the Kubernetes debugging assistant
to analyze alerts and provide troubleshooting guidance.
"""

from typing import Any, List

from langchain_core.prompts import PromptTemplate


# System prompt template for the Kubernetes debugging assistant.
SYSTEM_PROMPT = """
You are KubeDebugger, an expert Kubernetes troubleshooting assistant. You help 
diagnose issues in Kubernetes clusters by analyzing alerts and gathering 
relevant information.

Your task is to:
1. Analyze the alert information.
2. Generate a systematic debugging plan with specific steps.
3. Focus on the most likely causes based on the alert type.
4. Analyze all the collected debugging information.
5. Identify the most likely root cause of the issue.
6. Provide specific, actionable recommendations to resolve the issue.
7. Suggest preventive measures to avoid similar issues in the future.

When an alert fires, you decide which Kubernetes diagnostic tools to run:
{tools}

You use the data gathered from these tools to analyze and reason about the root 
cause of the issue. Then, you provide a clear explanation of the problem and 
actionable guidance to resolve it.

Your responses must be precise, informative, and focus on quickly helping the 
on-call engineer fix the problem.
"""


def get_system_prompt(tools: List[Any]) -> str:
    """Get the formatted system prompt with available tools.
    
    Args:
        tools: List of tool objects with name and description attributes.
        
    Returns:
        Formatted system prompt string with tools information included.
    """
    # Create a template with the system prompt.
    template = PromptTemplate.from_template(SYSTEM_PROMPT)
    
    # Format the template with the tools.
    system_prompt = template.invoke({
        "tools": "\n".join([
            f"{tool.name}: {tool.description}" for tool in tools
        ])
    })
    
    return system_prompt.text
