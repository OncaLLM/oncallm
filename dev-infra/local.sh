docker pull registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.5.3
docker pull quay.io/prometheus-operator/prometheus-operator:v0.82.2
docker pull quay.io/prometheus-operator/prometheus-operator:v0.82.2
docker pull registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.15.0
docker pull quay.io/kiwigrid/k8s-sidecar:1.30.0
docker pull docker.io/grafana/grafana:12.0.0
docker pull quay.io/prometheus/node-exporter:v1.9.1
docker pull quay.io/prometheus/prometheus:v3.4.0
docker pull quay.io/prometheus/alertmanager:v0.28.1
docker pull quay.io/prometheus-operator/prometheus-config-reloader:v0.82.2
docker pull polinux/stress
docker pull docker.io/library/nginx:1.28.0-alpine3.21

kind load docker-image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.5.3 -n oncallm
kind load docker-image quay.io/prometheus-operator/prometheus-operator:v0.82.2 -n oncallm
kind load docker-image quay.io/prometheus-operator/prometheus-operator:v0.82.2 -n oncallm
kind load docker-image registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.15.0 -n oncallm
kind load docker-image quay.io/kiwigrid/k8s-sidecar:1.30.0 -n oncallm
kind load docker-image docker.io/grafana/grafana:12.0.0 -n oncallm
kind load docker-image quay.io/prometheus/node-exporter:v1.9.1 -n oncallm
kind load docker-image quay.io/prometheus/prometheus:v3.4.0 -n oncallm
kind load docker-image quay.io/prometheus/alertmanager:v0.28.1 -n oncallm
kind load docker-image quay.io/prometheus-operator/prometheus-config-reloader:v0.82.2 -n oncallm
kind load docker-image polinux/stress -n oncallm
kind load docker-image oncallm:1.0.0 -n oncallm
kind load docker-image docker.io/library/nginx:1.28.0-alpine3.21 -n oncallm
