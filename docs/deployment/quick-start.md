# Quick Start

Get OnCallM running in your Kubernetes cluster in under 5 minutes.

## Prerequisites

Before starting, ensure you have:

- ✅ Kubernetes cluster (v1.20+)
- ✅ Helm 3.x installed
- ✅ Prometheus & AlertManager running
- ✅ OpenAI API key

::: tip
Need help with prerequisites? Check our [detailed prerequisites guide](./prerequisites.md).
:::

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/OncaLLM/oncallm.git
cd oncallm
```

### 2. Configure Values

Create your local configuration file:

```bash
cp charts/oncallm/values.yaml values.local.yaml
```

Edit `values.local.yaml` with your settings:

```yaml
oncallm:
  env:
    OPENAI_API_KEY: "your-openai-api-key-here"
    APP_HOST: "0.0.0.0"
    APP_PORT: "8001"
  
  service:
    type: ClusterIP
    port: 8001
  
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
```

### 3. Deploy with Helm

Install OnCallM to your cluster:

```bash
helm install oncallm ./charts/oncallm -f values.local.yaml
```

### 4. Verify Installation

Check that OnCallM is running:

```bash
kubectl get pods -l app=oncallm
kubectl logs -l app=oncallm
```

You should see output similar to:

```
NAME                      READY   STATUS    RESTARTS   AGE
oncallm-7d4b8c9f5-xk2m8   1/1     Running   0          30s
```

### 5. Configure AlertManager

Add OnCallM webhook to your AlertManager configuration:

```yaml
# alertmanager.yml
global:
  # ... your global config

route:
  # ... your routing config
  routes:
  - match:
      severity: critical
    receiver: 'oncallm-webhook'

receivers:
- name: 'oncallm-webhook'
  webhook_configs:
  - url: 'http://oncallm.default.svc.cluster.local:8001/webhook'
    send_resolved: true
    max_alerts: 0
```

### 6. Test the Integration

Trigger a test alert to verify the integration:

```bash
# Create a test alert
kubectl run test-alert --image=nginx --restart=Never
kubectl delete pod test-alert
```

## What's Next?

🎉 **Congratulations!** OnCallM is now running in your cluster.

### Check Your First Report

1. Access the OnCallM service:
   ```bash
   kubectl port-forward svc/oncallm 8001:8001
   ```

2. Visit `http://localhost:8001/reports` to see analysis reports

3. When alerts are triggered, you'll see detailed analysis at `http://localhost:8001/report/{fingerprint}`

### Next Steps

- [Configure AlertManager properly](../configuration/alertmanager.md)
- [Set up resource limits](../configuration/resources.md)
- [Learn about the API](../api/webhook.md)
- [Configure monitoring](../configuration/environment.md)

## Troubleshooting

### Common Issues

**Pod not starting?**
```bash
kubectl describe pod -l app=oncallm
kubectl logs -l app=oncallm
```

**Can't connect to OpenAI?**
- Verify your API key is correct
- Check network policies allow outbound HTTPS
- Ensure the secret is properly mounted

**AlertManager not sending webhooks?**
- Verify the webhook URL is reachable from AlertManager
- Check AlertManager logs for webhook delivery errors
- Test connectivity: `kubectl exec -it alertmanager-pod -- wget -O- http://oncallm.default.svc.cluster.local:8001/health`

### Getting Help

- 📖 [Read the full documentation](../guide/getting-started.md)
- 🐛 [Report issues on GitHub](https://github.com/OncaLLM/oncallm/issues)
- 📧 [Enterprise support](mailto:mohammad.azhdari.22@gmail.com)

::: tip Need Enterprise Support?
For professional deployment assistance, custom configurations, and dedicated support, [contact our team](mailto:mohammad.azhdari.22@gmail.com?subject=OnCallM%20Enterprise%20Support).
::: 