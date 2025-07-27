# AlertManager Configuration

Configure AlertManager to send alerts to OnCallM for AI-powered analysis.

## Basic Webhook Configuration

Add OnCallM as a webhook receiver in your AlertManager configuration:

```yaml
# alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alertmanager@yourcompany.com'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
  - match:
      severity: critical
    receiver: 'oncallm-webhook'
  - match:
      severity: warning
    receiver: 'oncallm-webhook'

receivers:
- name: 'web.hook'
  webhook_configs:
  - url: 'http://localhost:5001/'

- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    send_resolved: true
    max_alerts: 0
    http_config:
      bearer_token: 'optional-auth-token'
```

## Advanced Routing

### Route by Severity

Send only critical alerts to OnCallM:

```yaml
route:
  group_by: ['alertname', 'cluster']
  group_wait: 5s
  group_interval: 5s
  repeat_interval: 30m
  receiver: 'default'
  routes:
  - match:
      severity: critical
    receiver: 'oncallm-critical'
    group_wait: 1s
    repeat_interval: 5m
  - match:
      severity: warning
    receiver: 'oncallm-warning'
    repeat_interval: 1h

receivers:
- name: 'default'
  slack_configs:
  - api_url: 'YOUR_SLACK_WEBHOOK'
    channel: '#alerts'

- name: 'oncallm-critical'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    send_resolved: true
    title: 'Critical Alert - &#123;&#123; .GroupLabels.alertname &#125;&#125;'

- name: 'oncallm-warning'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    send_resolved: true
    title: 'Warning Alert - &#123;&#123; .GroupLabels.alertname &#125;&#125;'
```

### Route by Namespace

Send alerts from specific namespaces:

```yaml
route:
  routes:
  - match:
      namespace: production
    receiver: 'oncallm-production'
  - match:
      namespace: staging
    receiver: 'oncallm-staging'

receivers:
- name: 'oncallm-production'
  webhook_configs:
  - url: 'http://oncallm.production.svc.cluster.local:8001/webhook'
    send_resolved: true

- name: 'oncallm-staging'
  webhook_configs:
  - url: 'http://oncallm.staging.svc.cluster.local:8001/webhook'
    send_resolved: true
```

## Webhook Configuration Options

### Authentication

Secure your webhook endpoint:

```yaml
receivers:
- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    http_config:
      bearer_token: 'your-secret-token'
      # OR use bearer_token_file for reading from file
      # bearer_token_file: '/etc/alertmanager/token'
```

### Custom Headers

Add custom headers to webhook requests:

```yaml
receivers:
- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    http_config:
      headers:
        'X-Source': 'alertmanager'
        'X-Environment': 'production'
```

### Timeout and Retry

Configure timeout and retry behavior:

```yaml
receivers:
- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    send_resolved: true
    max_alerts: 10  # Maximum alerts per request (0 = no limit)
    http_config:
      timeout: 10s
      proxy_url: 'http://proxy.example.com:8080'
```

## Testing Configuration

### Validate Configuration

Check AlertManager configuration syntax:

```bash
# Download amtool
go install github.com/prometheus/alertmanager/cmd/amtool@latest

# Check configuration
amtool check-config alertmanager.yml
```

### Test Webhook Delivery

Test webhook connectivity:

```bash
# From AlertManager pod
kubectl exec -it alertmanager-pod -- \
  wget -O- --post-data='{"test": "data"}' \
  --header='Content-Type: application/json' \
  http://oncallm.default.svc.cluster.local:8001/webhook
```

### Trigger Test Alert

Create a test alert to verify the integration:

```bash
# Create a failing pod
kubectl run test-alert --image=nginx --restart=Never
kubectl delete pod test-alert

# Or trigger a manual alert
curl -XPOST http://alertmanager:9093/api/v1/alerts -H 'Content-Type: application/json' -d '[{
  "labels": {
    "alertname": "TestAlert",
    "service": "test-service",
    "severity": "warning",
    "instance": "test-instance"
  },
  "annotations": {
    "summary": "Test alert for OnCallM integration",
    "description": "This is a test alert to verify OnCallM integration works correctly"
  },
  "generatorURL": "http://localhost:9090/graph?g0.expr=up&g0.tab=1"
}]'
```

## Monitoring Webhook Delivery

### AlertManager Metrics

Monitor webhook delivery success:

```promql
# Webhook success rate
rate(alertmanager_notifications_total{integration="webhook"}[5m])

# Webhook failures
rate(alertmanager_notifications_failed_total{integration="webhook"}[5m])
```

### AlertManager Logs

Check AlertManager logs for webhook issues:

```bash
kubectl logs -f deployment/alertmanager
```

Look for entries like:
```
level=info ts=2024-01-15T10:30:00.000Z caller=notify.go:732 component=dispatcher receiver=oncallm-webhook integration=webhook[0] msg="Completed successfully"
```

## Troubleshooting

### Common Issues

**Webhook not receiving alerts?**

1. Check AlertManager routing:
   ```bash
   amtool config routes --config.file=alertmanager.yml
   ```

2. Verify service connectivity:
   ```bash
   kubectl get svc oncallm
   kubectl get endpoints oncallm
   ```

3. Check AlertManager logs:
   ```bash
   kubectl logs deployment/alertmanager | grep webhook
   ```

**Connection timeouts?**

1. Increase timeout in webhook config:
   ```yaml
   http_config:
     timeout: 30s
   ```

2. Check network policies:
   ```bash
   kubectl get networkpolicy
   ```

**Authentication failures?**

1. Verify bearer token is correct
2. Check OnCallM logs for authentication errors:
   ```bash
   kubectl logs deployment/oncallm | grep auth
   ```

### Debugging Tips

**Enable debug logging in AlertManager:**

```yaml
# alertmanager.yml
global:
  log_level: debug
```

**Test webhook endpoint directly:**

```bash
kubectl port-forward svc/oncallm 8001:8001
curl -X POST http://localhost:8001/webhook \
  -H 'Content-Type: application/json' \
  -d '{"alerts": [{"labels": {"alertname": "test"}}]}'
```

## Best Practices

### Performance

- **Group alerts** by alertname and instance to reduce webhook calls
- **Set reasonable group intervals** (5-10s) to batch alerts
- **Use max_alerts** to limit payload size
- **Configure appropriate timeouts** (10-30s)

### Reliability

- **Configure multiple receivers** for redundancy
- **Use resolved alerts** to track incident lifecycle
- **Monitor webhook delivery** with AlertManager metrics
- **Set up fallback receivers** for critical alerts

### Security

- **Use authentication** for webhook endpoints
- **Implement rate limiting** in OnCallM
- **Validate webhook payloads** to prevent injection
- **Use TLS** for production deployments

## Next Steps

- [Environment Configuration](./environment.md)
- [Resource Limits](./resources.md)
- [API Reference](../api/webhook.md)
- [Troubleshooting Guide](../deployment/quick-start.md#troubleshooting) 