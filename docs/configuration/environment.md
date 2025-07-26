# Environment Variables

Configure OnCallM using environment variables for deployment customization.

## Required Variables

### OpenAI Configuration

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY="sk-your-openai-api-key-here"

# OpenAI API Base URL (Optional)
OPENAI_API_BASE="https://api.openai.com/v1"

# OpenAI Model (Optional)
OPENAI_MODEL="gpt-4"
```

### Application Settings

```bash
# Application Host (Default: 0.0.0.0)
APP_HOST="0.0.0.0"

# Application Port (Default: 8001)
APP_PORT="8001"

# Template Directory (Default: ../templates)
TEMPLATE_DIR="../templates"

# Base URL for report links (Optional)
ONCALLM_BASE_URL="https://oncallm.yourcompany.com"
```

## Optional Variables

### Logging Configuration

```bash
# Log Level (Default: INFO)
LOG_LEVEL="INFO"

# Log Format (Default: JSON)
LOG_FORMAT="json"
```

### Performance Tuning

```bash
# Worker Thread Pool Size (Default: 10)
WORKER_THREADS="10"

# Request Timeout (Default: 30s)
REQUEST_TIMEOUT="30"

# AI Analysis Timeout (Default: 60s)
AI_TIMEOUT="60"
```

## Kubernetes Configuration

### Using ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: oncallm-config
data:
  APP_HOST: "0.0.0.0"
  APP_PORT: "8001"
  LOG_LEVEL: "INFO"
  WORKER_THREADS: "10"
```

### Using Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: oncallm-secrets
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-your-key-here"
```

### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oncallm
spec:
  template:
    spec:
      containers:
      - name: oncallm
        image: oncallm/oncallm:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: oncallm-secrets
              key: OPENAI_API_KEY
        envFrom:
        - configMapRef:
            name: oncallm-config
```

## Development Environment

### .env File

Create a `.env` file in your project root:

```bash
# .env
OPENAI_API_KEY=sk-your-development-key
APP_HOST=localhost
APP_PORT=8001
LOG_LEVEL=DEBUG
```

### Docker Configuration

```bash
# Run with environment variables
docker run -d \
  -e OPENAI_API_KEY=sk-your-key \
  -e APP_PORT=8001 \
  -p 8001:8001 \
  oncallm/oncallm:latest
```

## Validation

OnCallM validates environment variables on startup:

```python
# Required variables check
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is required")

# Port validation
port = int(os.getenv("APP_PORT", "8001"))
if port < 1 or port > 65535:
    raise ValueError("APP_PORT must be between 1 and 65535")
```

## Next Steps

- [AlertManager Setup](./alertmanager.md)
- [Resource Limits](./resources.md)
- [Quick Start Guide](../deployment/quick-start.md) 