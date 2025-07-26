# Webhook API

OnCallM receives alerts from AlertManager via webhook endpoints.

## Webhook Endpoint

```
POST /webhook
```

Receives alerts from AlertManager for AI analysis.

### Request Format

OnCallM expects AlertManager webhook format:

```json
{
  "receiver": "oncallm-webhook",
  "status": "firing",
  "alerts": [
    {
      "status": "firing",
      "labels": {
        "alertname": "HighCPUUsage",
        "instance": "node-1:9100",
        "job": "node-exporter",
        "severity": "warning",
        "namespace": "production"
      },
      "annotations": {
        "summary": "CPU usage is above 80%",
        "description": "CPU usage on node-1 has been above 80% for more than 5 minutes"
      },
      "startsAt": "2024-01-15T10:30:00.000Z",
      "endsAt": "0001-01-01T00:00:00Z",
      "generatorURL": "http://prometheus:9090/graph?g0.expr=...",
      "fingerprint": "abc123def456"
    }
  ],
  "groupLabels": {
    "alertname": "HighCPUUsage"
  },
  "commonLabels": {
    "job": "node-exporter",
    "severity": "warning"
  },
  "commonAnnotations": {},
  "externalURL": "http://alertmanager:9093",
  "version": "4",
  "groupKey": "{}:{alertname=\"HighCPUUsage\"}"
}
```

### Response Format

```json
{
  "status": "success",
  "message": "Alerts queued for analysis",
  "report_urls": [
    {
      "fingerprint": "abc123def456",
      "alert_name": "HighCPUUsage",
      "namespace": "production",
      "report_url": "https://oncallm.example.com/report/abc123def456"
    }
  ]
}
```

### Error Responses

#### 400 Bad Request

```json
{
  "detail": "Invalid alert format"
}
```

#### 503 Service Unavailable

```json
{
  "detail": "Service not initialised"
}
```

## Authentication

### Bearer Token

Configure bearer token authentication:

```yaml
# alertmanager.yml
receivers:
- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm:8001/webhook'
    http_config:
      bearer_token: 'your-secret-token'
```

OnCallM validates the token:

```python
# Verify bearer token
authorization = request.headers.get("Authorization")
if authorization != f"Bearer {expected_token}":
    raise HTTPException(status_code=401, detail="Unauthorized")
```

## Testing

### Manual Test

```bash
curl -X POST http://localhost:8001/webhook \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your-token' \
  -d '{
    "alerts": [{
      "labels": {
        "alertname": "TestAlert",
        "severity": "warning"
      },
      "annotations": {
        "summary": "Test alert for integration"
      },
      "startsAt": "2024-01-15T10:30:00.000Z",
      "fingerprint": "test123"
    }]
  }'
```

### Expected Response

```json
{
  "status": "success",
  "message": "Alerts queued for analysis",
  "report_urls": [
    {
      "fingerprint": "test123",
      "alert_name": "TestAlert",
      "namespace": "Unknown",
      "report_url": "http://localhost:8001/report/test123"
    }
  ]
}
```

## Rate Limiting

OnCallM implements rate limiting to prevent abuse:

- **Per IP**: 100 requests per minute
- **Global**: 1000 requests per minute
- **Per Alert**: Duplicate alerts within 60 seconds are deduplicated

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642249200
```

### Rate Limit Response

```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

## Monitoring

### Metrics

OnCallM exposes webhook metrics:

```promql
# Total webhook requests
oncallm_webhook_requests_total

# Webhook request duration
oncallm_webhook_duration_seconds

# Webhook errors
oncallm_webhook_errors_total
```

### Health Check

Monitor webhook health:

```bash
curl http://localhost:8001/health
```

```json
{
  "status": "healthy",
  "webhook_endpoint": "available",
  "ai_service": "connected",
  "queue_size": 5
}
```

## Troubleshooting

### Common Issues

**Webhook not receiving requests?**

1. Check AlertManager configuration:
   ```bash
   amtool config show --config.file=alertmanager.yml
   ```

2. Verify network connectivity:
   ```bash
   kubectl port-forward svc/oncallm 8001:8001
   curl http://localhost:8001/health
   ```

3. Check AlertManager logs:
   ```bash
   kubectl logs deployment/alertmanager | grep webhook
   ```

**Authentication failures?**

1. Verify bearer token in AlertManager config
2. Check OnCallM logs:
   ```bash
   kubectl logs deployment/oncallm | grep "Unauthorized"
   ```

**Rate limiting issues?**

1. Check rate limit headers in responses
2. Implement exponential backoff in client
3. Contact support for higher limits

## Integration Examples

### Slack Integration

Combine OnCallM with Slack notifications:

```yaml
receivers:
- name: 'oncallm-and-slack'
  webhook_configs:
  - url: 'http://oncallm:8001/webhook'
  slack_configs:
  - api_url: 'YOUR_SLACK_WEBHOOK'
    channel: '#alerts'
    title: 'Alert: {{ .GroupLabels.alertname }}'
    text: 'AI Analysis: http://oncallm:8001/report/{{ .Alerts.0.Fingerprint }}'
```

### PagerDuty Integration

Route critical alerts to both OnCallM and PagerDuty:

```yaml
receivers:
- name: 'critical-alerts'
  webhook_configs:
  - url: 'http://oncallm:8001/webhook'
  pagerduty_configs:
  - routing_key: 'YOUR_PAGERDUTY_KEY'
    description: 'Critical alert - AI analysis available'
```

## Next Steps

- [Health Endpoints](./health.md)
- [Reports API](./reports.md)
- [AlertManager Configuration](../configuration/alertmanager.md) 