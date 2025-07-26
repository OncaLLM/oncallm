# Prerequisites

Before deploying OnCallM, ensure your environment meets these requirements.

## Kubernetes Cluster

### Minimum Requirements

- **Kubernetes version**: v1.20 or higher
- **Node resources**: At least 1 CPU core and 1GB RAM available
- **Storage**: Persistent storage for configuration (optional)
- **Network**: Outbound HTTPS access for OpenAI API calls

### Supported Platforms

OnCallM works on any standard Kubernetes distribution:

- ✅ **Cloud Managed Kubernetes**: EKS, GKE, AKS
- ✅ **Self-managed**: kubeadm, k3s, RKE
- ✅ **Local development**: kind, minikube, Docker Desktop

## Required Tools

### Helm 3.x

OnCallM uses Helm for package management and deployment.

**Installation:**

```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Windows
choco install kubernetes-helm
```

**Verify installation:**

```bash
helm version
```

### kubectl

You need kubectl configured to access your cluster.

**Verify cluster access:**

```bash
kubectl cluster-info
kubectl get nodes
```

## Monitoring Stack

### Prometheus

OnCallM integrates with Prometheus for metrics collection.

**Quick setup with helm:**

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack
```

### AlertManager

AlertManager sends alerts to OnCallM via webhooks.

**Verify AlertManager is running:**

```bash
kubectl get pods -n monitoring -l app=alertmanager
```

## AI Provider

### OpenAI API Key

OnCallM uses OpenAI for intelligent analysis.

1. **Create an OpenAI account** at [platform.openai.com](https://platform.openai.com)
2. **Generate an API key** in the API Keys section
3. **Set usage limits** to control costs
4. **Test the key:**

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

::: warning Cost Management
AI analysis incurs OpenAI API costs. Monitor your usage and set billing limits in your OpenAI dashboard.
:::

### Alternative AI Providers

OnCallM also supports:

- **Azure OpenAI**: Enterprise-grade OpenAI in your Azure environment
- **Self-hosted models**: Compatible with OpenAI API format (e.g., ollama, vLLM)

## Network Requirements

### Outbound Connectivity

OnCallM requires outbound HTTPS access to:

- **OpenAI API**: `api.openai.com:443`
- **Package registries**: For updates and dependencies

### Inbound Connectivity

- **AlertManager**: Must reach OnCallM webhook endpoint
- **Users**: Access to OnCallM web interface (optional)

### Firewall Configuration

If you have strict network policies:

```yaml
# Example NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: oncallm-network-policy
spec:
  podSelector:
    matchLabels:
      app: oncallm
  policyTypes:
  - Egress
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS to OpenAI
```

## Resource Planning

### Compute Resources

**Minimum:**
- CPU: 250m (0.25 cores)
- Memory: 256Mi

**Recommended:**
- CPU: 500m (0.5 cores)
- Memory: 512Mi

**High volume:**
- CPU: 1000m (1 core)
- Memory: 1Gi

### Storage

OnCallM is primarily stateless, but you may want persistent storage for:

- **Configuration files**: 1GB
- **Logs**: 5-10GB (with log rotation)
- **Temporary analysis data**: 1-5GB

## Security Considerations

### RBAC Permissions

OnCallM needs minimal cluster access:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: oncallm-reader
rules:
- apiGroups: [""]
  resources: ["pods", "services", "endpoints", "events"]
  verbs: ["get", "list"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list"]
```

### Secrets Management

- **OpenAI API key**: Store in Kubernetes Secret
- **TLS certificates**: For secure webhook endpoints
- **Authentication**: For web interface access

## Verification Checklist

Before proceeding with installation, verify:

- [ ] Kubernetes cluster is accessible
- [ ] Helm 3.x is installed
- [ ] Prometheus is running and collecting metrics
- [ ] AlertManager is configured and functional
- [ ] OpenAI API key is valid and has credits
- [ ] Network policies allow required connectivity
- [ ] Sufficient compute and storage resources available

## Next Steps

Once prerequisites are met:

1. [Quick Start Installation](./quick-start.md)
2. [Helm Installation Guide](./helm.md)
3. [Configuration Options](../configuration/environment.md)

## Troubleshooting

### Common Issues

**Kubernetes version too old?**
```bash
kubectl version --short
```
Upgrade your cluster to v1.20+

**Helm not found?**
```bash
which helm
```
Install Helm 3.x from [helm.sh](https://helm.sh)

**Can't reach OpenAI?**
```bash
curl -I https://api.openai.com
```
Check network policies and firewalls

**AlertManager not running?**
```bash
kubectl get pods -A | grep alertmanager
```
Install monitoring stack first

### Getting Help

- 📖 [Installation troubleshooting](./quick-start.md#troubleshooting)
- 🐛 [Report issues on GitHub](https://github.com/OncaLLM/oncallm/issues)
- 📧 [Enterprise support](mailto:mohammad.azhdari.22@gmail.com) 