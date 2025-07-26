# Kubernetes Infrastructure Setup

This directory contains the necessary configurations to set up a Kubernetes cluster with Prometheus, AlertManager, RabbitMQ, and OOM kill monitoring using Kind (Kubernetes in Docker).

## Prerequisites

- Docker installed and running
- Kind v0.20.0 or later
- kubectl v1.32.0 or later
- Helm v3.0.0 or later

## Setup Instructions

### 1. Create Kind Cluster

Create a new file named `kind-config.yaml` with the following content:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  image: kindest/node:v1.32.0
```

Create the cluster:

```bash
kind create cluster --name oncallm-cluster --config kind-config.yaml
```

### 2. Install Prometheus Stack

Add the Prometheus community Helm repository:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Create the monitoring namespace:

```bash
kubectl create namespace monitoring
```

Install the kube-prometheus-stack using the provided values:

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values prometheus-alertmanager.values.yaml
```

### 3. Install RabbitMQ

Add the Bitnami Helm repository:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### 4. Apply Alert Rules

Apply the OOM kill alert rule:

```bash
kubectl apply -f oomkill-rule.yaml
```

### 5. Verify Installation

Check if all pods are running:

```bash
kubectl get pods -n monitoring
```

Verify Prometheus, AlertManager, are accessible:

```bash
kubectl port-forward svc/prometheus-operated 9090:9090 -n monitoring
kubectl port-forward svc/prometheus-alertmanager 9093:9093 -n monitoring
```

You can now access:

- Prometheus UI at http://localhost:9090
- AlertManager UI at http://localhost:9093
- RabbitMQ Management UI at http://localhost:15672 (use the credentials from step 3)

### 6. Test OOM Kill Detection (Optional)

To test the OOM kill detection, you can deploy the test pod:

```bash
kubectl apply -f oom-test.yaml
```

This will create a pod that intentionally consumes more memory than its limit, triggering an OOM kill event. You can monitor the alerts in the AlertManager UI.

## Cleanup

To delete the cluster:

```bash
kind delete cluster --name monitoring-cluster
```

## Notes

- The Prometheus and AlertManager configuration is set up to send alerts to a webhook endpoint at `http://alert-receiver.monitoring.svc.cluster.local:8080/api/k8s-alert`
- The OOM kill rule will trigger an alert when a pod is killed due to OOM conditions
- The alert will be grouped by alertname and namespace
- Alerts will be repeated every 12 hours if not resolved
- RabbitMQ is configured with:
  - Persistent storage (8Gi)
  - Prometheus metrics enabled
  - Basic authentication
  - Resource limits and requests
  - Health monitoring alerts
