# OncaLLM Agent

An LLM-powered agent that helps with Kubernetes debugging based on alerts received from monitoring systems.

## Overview

This application provides an API that can:

1. Receive Kubernetes alert webhooks (e.g., from Prometheus Alertmanager).
2. Utilize a LangGraph-based agent (`OncallmAgent`) to analyze these alerts.
3. The agent uses various tools, including direct Kubernetes API access via `KubernetesService`, to gather context.
4. Analyze the gathered information to determine potential root causes and generate recommendations.
5. Store analysis reports and provide API endpoints to retrieve them.

## Features

- **Alert Webhook Integration**: Receives alerts from Prometheus Alertmanager.
- **LangGraph Powered Analysis**: Uses a ReAct agent built with LangGraph for intelligent analysis.
- **Direct Kubernetes API Integration**: `KubernetesService` interacts directly with your Kubernetes cluster to fetch information about pods, services, deployments, and logs.
- **Automated Analysis**: The LLM agent analyzes alert data and cluster information to identify potential root causes.
- **Recommendation Generation**: Provides actionable recommendations to resolve issues.
- **Report Storage & API**: Stores analysis reports and offers endpoints to list all reports or fetch specific ones by ID.

## Prerequisites

- Python 3.8+
- Access to a Kubernetes cluster (the agent will use the standard kubeconfig resolution, e.g., `~/.kube/config` or in-cluster service account).
- OpenAI API key (or other compatible LLM provider configured in `oncallm/llm_service.py`).
- [Docker](https://docs.docker.com/get-docker/) installed and running.
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) installed.
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) installed and configured.
- Helm (if OncaLLM deployment uses Helm - TBD).


## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory-name> # e.g., oncallm-agent
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file by copying from `.env.example` (if provided, otherwise create new) with your configuration:

    ```dotenv
    # FastAPI settings
    APP_HOST=0.0.0.0
    APP_PORT=8001 # Default port for oncallm.main

    # Kubernetes settings (optional, if not using default kubeconfig resolution or in-cluster auth)
    # KUBECONFIG_PATH=/path/to/your/kubeconfig

    # LLM settings
    OPENAI_API_KEY=your_openai_api_key
    LLM_MODEL=gpt-4-turbo # Or your preferred model
    # LLM_API_BASE=your_llm_api_base_if_not_openai_default # Optional, for self-hosted or proxy

    # Langfuse Observability (Optional)
    # LANGFUSE_PUBLIC_KEY=pk-lf-...
    # LANGFUSE_SECRET_KEY=sk-lf-...
    # LANGFUSE_HOST=https://cloud.langfuse.com # or your self-hosted instance
    ```

## Usage

### Starting the Server

```bash
python -m oncallm.main
```

The server will start on the configured host and port (default: `0.0.0.0:8001`).

### API Endpoints

- **GET /**: Root endpoint with API information.
- **GET /health**: Health check endpoint.
- **POST /webhook**: Endpoint to receive alerts from Alertmanager.
- **GET /reports**: Lists all analysis reports.
- **GET /reports/{report_id}**: Retrieves a specific analysis report by its ID.

### Configuring Alertmanager

To configure Prometheus Alertmanager to send alerts to this service, add the following to your `alertmanager.yml`:

```yaml
receivers:
  - name: 'oncallm-webhook'
    webhook_configs:
      - url: 'http://<your-oncallm-service-url>:8001/webhook' # Replace with actual URL
        send_resolved: true
```

## Development

### Running Tests

The project uses `pytest` for unit and API testing.

- **To run all unit tests:**
  
    ```bash
    pytest tests/unit
    ```

- **To run all API tests:**

    ```bash
    pytest tests/api
    ```

- **To run all tests (unit and API):**

    ```bash
    pytest tests/
    ```

Ensure you have installed the necessary dependencies, including `pytest` from `requirements.txt`.

## License

[MIT License](LICENSE)

## Contributing

We welcome contributions!

- Please read the project roadmap to understand priorities and milestones: [ROADMAP.md](./ROADMAP.md).
- Coding style: follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) in codes.
- Simplicity first: prefer clear, minimal solutions and small, focused PRs.

Please feel free to submit a Pull Request.
