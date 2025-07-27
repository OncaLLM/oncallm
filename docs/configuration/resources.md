# Resource Limits

Configure resource limits and requests for optimal OnCallM performance and reliability.

## Default Resource Configuration

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Sizing Guidelines

### Small Deployment (< 100 alerts/day)

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "250m"
```

**Characteristics:**
- Development or staging environments
- Low alert volume
- Single replica sufficient

### Medium Deployment (100-1000 alerts/day)

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**Characteristics:**
- Production environments
- Moderate alert volume
- 2-3 replicas recommended

### Large Deployment (> 1000 alerts/day)

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

**Characteristics:**
- High-volume production
- Multiple clusters
- 3+ replicas with auto-scaling

## Memory Requirements

### Base Memory Usage

```
Base OnCallM process: ~50MB
FastAPI framework: ~30MB
Python runtime: ~40MB
AI processing buffer: ~100MB
Total baseline: ~220MB
```

### Per-Alert Memory

```
Alert processing: ~2MB per alert
AI analysis: ~5MB per alert
Report generation: ~1MB per alert
Queue overhead: ~0.5MB per alert
Total per alert: ~8.5MB
```

### Memory Calculation

```bash
# Formula
Total Memory = Base Memory + (Concurrent Alerts × Per-Alert Memory)

# Example: 20 concurrent alerts
Total Memory = 220MB + (20 × 8.5MB) = 390MB
Recommended limit = 390MB × 1.3 (buffer) = 507MB ≈ 512MB
```

## CPU Requirements

### CPU Usage Patterns

```
Webhook processing: Low CPU (10-20%)
Data collection: Medium CPU (30-50%)
AI analysis: Variable CPU (20-80%)
Report generation: Low CPU (10-30%)
```

### CPU Calculation

```bash
# Base CPU usage
Base CPU: 50m (0.05 cores)

# Per concurrent alert
Alert processing: 15m per alert

# Example: 10 concurrent alerts
Total CPU = 50m + (10 × 15m) = 200m
Recommended limit = 200m × 2 (burst) = 400m
```

## Helm Configuration

### values.yaml

```yaml
oncallm:
  replicaCount: 2
  
  resources:
    requests:
      memory: "256Mi"
      cpu: "250m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  
  # Auto-scaling configuration
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
```

### Override for Production

```bash
helm install oncallm ./charts/oncallm \
  --set resources.requests.memory=512Mi \
  --set resources.requests.cpu=500m \
  --set resources.limits.memory=1Gi \
  --set resources.limits.cpu=1000m \
  --set replicaCount=3
```

## Kubernetes Deployment

### Complete Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oncallm
  labels:
    app: oncallm
spec:
  replicas: 2
  selector:
    matchLabels:
      app: oncallm
  template:
    metadata:
      labels:
        app: oncallm
    spec:
      containers:
      - name: oncallm
        image: oncallm/oncallm:latest
        ports:
        - containerPort: 8001
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: oncallm-secrets
              key: OPENAI_API_KEY
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Auto-scaling Configuration

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: oncallm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: oncallm
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### Vertical Pod Autoscaler

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: oncallm-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: oncallm
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: oncallm
      maxAllowed:
        cpu: 2000m
        memory: 2Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
```

## Resource Monitoring

### Prometheus Metrics

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: oncallm-metrics
spec:
  selector:
    matchLabels:
      app: oncallm
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### Key Metrics to Monitor

```promql
# CPU usage
rate(container_cpu_usage_seconds_total{pod=~"oncallm.*"}[5m])

# Memory usage
container_memory_usage_bytes{pod=~"oncallm.*"}

# Memory limits
container_spec_memory_limit_bytes{pod=~"oncallm.*"}

# Queue size
oncallm_alert_queue_size

# Processing time
oncallm_alert_processing_duration_seconds
```

### Alerting Rules

```yaml
groups:
- name: oncallm-resources
  rules:
  - alert: OnCallMHighMemoryUsage
    expr: |
      (container_memory_usage_bytes{pod=~"oncallm.*"} / 
       container_spec_memory_limit_bytes{pod=~"oncallm.*"}) > 0.85
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "OnCallM memory usage is high"
      description: "Pod &#123;&#123; $labels.pod &#125;&#125; memory usage is &#123;&#123; $value | humanizePercentage &#125;&#125;"

  - alert: OnCallMHighCPUUsage
    expr: |
      rate(container_cpu_usage_seconds_total{pod=~"oncallm.*"}[5m]) > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "OnCallM CPU usage is high"
      description: "Pod &#123;&#123; $labels.pod &#125;&#125; CPU usage is &#123;&#123; $value | humanize &#125;&#125;"
```

## Performance Tuning

### Worker Thread Configuration

```python
# Environment variables
WORKER_THREADS = int(os.getenv("WORKER_THREADS", "10"))

# Rule of thumb: 2-5 threads per CPU core
# For 500m CPU (0.5 cores): 1-3 threads
# For 1000m CPU (1 core): 2-5 threads
```

### Queue Size Limits

```python
# Prevent memory exhaustion
MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", "100"))

if queue.qsize() > MAX_QUEUE_SIZE:
    raise HTTPException(status_code=503, detail="Queue full")
```

### AI API Rate Limiting

```python
# OpenAI rate limits
OPENAI_RPM = int(os.getenv("OPENAI_RPM", "60"))  # Requests per minute
OPENAI_TPM = int(os.getenv("OPENAI_TPM", "60000"))  # Tokens per minute

# Implement rate limiting
@rate_limit(requests_per_minute=OPENAI_RPM)
def call_openai_api(prompt):
    # API call implementation
    pass
```

## Troubleshooting

### Common Resource Issues

**OOMKilled pods?**

```bash
# Check memory usage
kubectl top pods -l app=oncallm

# Check events
kubectl get events --field-selector reason=OOMKilling

# Increase memory limits
helm upgrade oncallm ./charts/oncallm \
  --set resources.limits.memory=1Gi
```

**CPU throttling?**

```bash
# Check CPU throttling metrics
kubectl exec -it oncallm-pod -- cat /sys/fs/cgroup/cpu/cpu.stat

# Increase CPU limits
helm upgrade oncallm ./charts/oncallm \
  --set resources.limits.cpu=1000m
```

**Slow response times?**

```bash
# Check queue size
curl http://oncallm:8001/health | jq .queue_size

# Scale horizontally
kubectl scale deployment oncallm --replicas=3
```

### Resource Optimization

```bash
# Monitor resource usage over time
kubectl top pods -l app=oncallm --containers=true

# Analyze resource utilization
kubectl describe hpa oncallm-hpa

# Review VPA recommendations
kubectl describe vpa oncallm-vpa
```

## Best Practices

### Resource Planning

1. **Start conservative**: Begin with small resource allocations
2. **Monitor continuously**: Use metrics to guide adjustments
3. **Plan for bursts**: Set limits higher than requests
4. **Test under load**: Validate performance with realistic traffic

### Cost Optimization

1. **Use requests efficiently**: Set appropriate resource requests
2. **Enable auto-scaling**: Scale based on actual demand
3. **Monitor unused capacity**: Regularly review resource utilization
4. **Consider spot instances**: Use preemptible nodes for cost savings

### Reliability

1. **Set resource limits**: Prevent resource exhaustion
2. **Use health checks**: Enable proper health monitoring
3. **Plan for failures**: Design for graceful degradation
4. **Monitor proactively**: Alert on resource issues before they impact users

## Next Steps

- [Environment Configuration](./environment.md)
- [AlertManager Setup](./alertmanager.md)
- [API Documentation](../api/webhook.md)
- [Monitoring Guide](../deployment/quick-start.md#troubleshooting) 