# LAB 6 - Correction : Monitoring avec Prometheus et Grafana

## 📋 Vue d'ensemble de la solution

Cette correction présente une solution complète pour déployer un stack de monitoring production-ready avec Prometheus, Grafana, Alertmanager et les exporters associés sur Kubernetes.

---

## 🎯 Objectifs atteints

- ✅ Stack Prometheus/Grafana complet
- ✅ ServiceMonitors et règles d'alertes
- ✅ Dashboards Grafana personnalisés
- ✅ Monitoring multi-niveaux (infrastructure + applications)
- ✅ Alerting intelligent et notifications
- ✅ Observabilité complète du cluster

---

## 🔧 Solution Étape par Étape

### Étape 1 : Installation du stack Prometheus avec Helm

#### 1.1 Values Helm pour kube-prometheus-stack

```yaml
# monitoring/values-prometheus.yaml
kube-prometheus-stack:
  fullnameOverride: monitoring

  defaultRules:
    create: true
    rules:
      alertmanager: true
      etcd: true
      configReloaders: true
      general: true
      k8s: true
      kubeApiserverAvailability: true
      kubeApiserverBurnrate: true
      kubeApiserverHistogram: true
      kubeApiserverSlos: true
      kubelet: true
      kubeProxy: true
      kubePrometheusGeneral: true
      kubePrometheusNodeRecording: true
      kubernetesApps: true
      kubernetesResources: true
      kubernetesStorage: true
      kubernetesSystem: true
      kubeScheduler: true
      kubeStateMetrics: true
      network: true
      node: true
      nodeExporterAlerting: true
      nodeExporterRecording: true
      prometheus: true
      prometheusOperator: true

  alertmanager:
    enabled: true
    fullnameOverride: alertmanager

    config:
      global:
        smtp_smarthost: 'smtp.company.com:587'
        smtp_from: 'alerts@company.com'
        smtp_auth_username: 'alerts@company.com'
        smtp_auth_password: 'smtp-password'
        slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

      route:
        group_by: ['alertname', 'cluster', 'service']
        group_wait: 10s
        group_interval: 10s
        repeat_interval: 1h
        receiver: 'web.hook'
        routes:
          - match:
              severity: critical
            receiver: 'critical-alerts'
            group_wait: 0s
            repeat_interval: 5m
          - match:
              severity: warning
            receiver: 'warning-alerts'
            repeat_interval: 30m
          - match_re:
              service: '^(webapp|api|frontend).*'
            receiver: 'application-alerts'

      receivers:
        - name: 'web.hook'
          webhook_configs:
            - url: 'http://webhook-service:5000/webhook'

        - name: 'critical-alerts'
          slack_configs:
            - channel: '#alerts-critical'
              title: 'CRITICAL Alert - {{ .GroupLabels.alertname }}'
              text: |
                {{ range .Alerts }}
                Alert: {{ .Annotations.summary }}
                Description: {{ .Annotations.description }}
                {{ end }}
              send_resolved: true
          email_configs:
            - to: 'devops-team@company.com'
              subject: 'CRITICAL Alert - {{ .GroupLabels.alertname }}'
              body: |
                {{ range .Alerts }}
                Alert: {{ .Annotations.summary }}
                Description: {{ .Annotations.description }}
                {{ end }}

        - name: 'warning-alerts'
          slack_configs:
            - channel: '#alerts-warning'
              title: 'Warning - {{ .GroupLabels.alertname }}'
              text: |
                {{ range .Alerts }}
                Alert: {{ .Annotations.summary }}
                {{ end }}
              send_resolved: true

        - name: 'application-alerts'
          slack_configs:
            - channel: '#app-alerts'
              title: 'Application Alert - {{ .GroupLabels.alertname }}'
              text: |
                Application: {{ .GroupLabels.service }}
                {{ range .Alerts }}
                Issue: {{ .Annotations.summary }}
                {{ end }}

    ingress:
      enabled: true
      ingressClassName: nginx
      hosts:
        - alertmanager.k8s.local
      paths:
        - /
      tls:
        - secretName: alertmanager-tls
          hosts:
            - alertmanager.k8s.local

  grafana:
    enabled: true
    fullnameOverride: grafana

    admin:
      existingSecret: grafana-admin-secret
      userKey: admin-user
      passwordKey: admin-password

    env:
      GF_SECURITY_ALLOW_EMBEDDING: true
      GF_AUTH_ANONYMOUS_ENABLED: false
      GF_INSTALL_PLUGINS: grafana-piechart-panel,grafana-worldmap-panel,grafana-clock-panel

    grafana.ini:
      analytics:
        check_for_updates: false
        reporting_enabled: false
      security:
        cookie_secure: true
        cookie_samesite: strict
      users:
        allow_sign_up: false
        auto_assign_org: true
        auto_assign_org_role: Viewer
      auth.ldap:
        enabled: false
      smtp:
        enabled: true
        host: smtp.company.com:587
        user: alerts@company.com
        password: smtp-password
        from_address: grafana@company.com
        from_name: Grafana

    datasources:
      datasources.yaml:
        apiVersion: 1
        datasources:
          - name: Prometheus
            type: prometheus
            url: http://monitoring-prometheus:9090
            access: proxy
            isDefault: true
            editable: false
          - name: Loki
            type: loki
            url: http://loki:3100
            access: proxy
            editable: false
          - name: Jaeger
            type: jaeger
            url: http://jaeger-query:16686
            access: proxy
            editable: false

    dashboardProviders:
      dashboardproviders.yaml:
        apiVersion: 1
        providers:
          - name: 'default'
            orgId: 1
            folder: ''
            type: file
            disableDeletion: false
            editable: true
            options:
              path: /var/lib/grafana/dashboards/default
          - name: 'kubernetes'
            orgId: 1
            folder: 'Kubernetes'
            type: file
            disableDeletion: false
            editable: true
            options:
              path: /var/lib/grafana/dashboards/kubernetes
          - name: 'applications'
            orgId: 1
            folder: 'Applications'
            type: file
            disableDeletion: false
            editable: true
            options:
              path: /var/lib/grafana/dashboards/applications

    dashboards:
      kubernetes:
        cluster-overview:
          gnetId: 15757
          revision: 37
          datasource: Prometheus
        node-exporter:
          gnetId: 1860
          revision: 31
          datasource: Prometheus
        kubernetes-pods:
          gnetId: 6417
          revision: 1
          datasource: Prometheus
        kubernetes-deployments:
          gnetId: 8588
          revision: 1
          datasource: Prometheus

      applications:
        webapp-dashboard:
          file: dashboards/webapp-dashboard.json
        api-performance:
          file: dashboards/api-performance.json

    ingress:
      enabled: true
      ingressClassName: nginx
      hosts:
        - grafana.k8s.local
      path: /
      tls:
        - secretName: grafana-tls
          hosts:
            - grafana.k8s.local

    persistence:
      enabled: true
      size: 10Gi
      storageClassName: fast-ssd

    resources:
      limits:
        cpu: 500m
        memory: 1Gi
      requests:
        cpu: 200m
        memory: 512Mi

  prometheus:
    enabled: true
    fullnameOverride: prometheus

    prometheusSpec:
      retention: 30d
      retentionSize: 50GB

      storageSpec:
        volumeClaimTemplate:
          spec:
            storageClassName: fast-ssd
            accessModes: ['ReadWriteOnce']
            resources:
              requests:
                storage: 100Gi

      resources:
        limits:
          cpu: 2000m
          memory: 4Gi
        requests:
          cpu: 500m
          memory: 2Gi

      ruleSelector:
        matchLabels:
          prometheus: kube-prometheus
          role: alert-rules

      serviceMonitorSelector:
        matchLabels:
          prometheus: kube-prometheus

      podMonitorSelector:
        matchLabels:
          prometheus: kube-prometheus

      additionalScrapeConfigs:
        - job_name: 'blackbox'
          metrics_path: /probe
          params:
            module: [http_2xx]
          static_configs:
            - targets:
                - https://grafana.k8s.local
                - https://webapp.k8s.local
          relabel_configs:
            - source_labels: [__address__]
              target_label: __param_target
            - source_labels: [__param_target]
              target_label: instance
            - target_label: __address__
              replacement: blackbox-exporter:9115

        - job_name: 'custom-apps'
          kubernetes_sd_configs:
            - role: endpoints
          relabel_configs:
            - source_labels:
                [__meta_kubernetes_service_annotation_prometheus_io_scrape]
              action: keep
              regex: true
            - source_labels:
                [__meta_kubernetes_service_annotation_prometheus_io_path]
              action: replace
              target_label: __metrics_path__
              regex: (.+)

    ingress:
      enabled: true
      ingressClassName: nginx
      hosts:
        - prometheus.k8s.local
      paths:
        - /
      tls:
        - secretName: prometheus-tls
          hosts:
            - prometheus.k8s.local

  nodeExporter:
    enabled: true

  kubeStateMetrics:
    enabled: true

  prometheusOperator:
    enabled: true

    admissionWebhooks:
      enabled: true
      patch:
        enabled: true
```

#### 1.2 Installation du stack

```bash
# Installation du namespace
kubectl create namespace monitoring

# Secrets pour Grafana
kubectl create secret generic grafana-admin-secret \
  --from-literal=admin-user=admin \
  --from-literal=admin-password=securepassword123 \
  -n monitoring

# Installation avec Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values monitoring/values-prometheus.yaml \
  --version 51.2.0

# Vérification du déploiement
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

### Étape 2 : ServiceMonitors pour applications custom

#### 2.1 ServiceMonitor pour webapp

```yaml
# monitoring/servicemonitors/webapp-servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: webapp-metrics
  namespace: monitoring
  labels:
    app: webapp
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: webapp
      component: backend
  namespaceSelector:
    matchNames:
      - app-dev
      - app-staging
      - app-prod
  endpoints:
    - port: http
      path: /actuator/prometheus
      interval: 30s
      scrapeTimeout: 10s
      honorLabels: true
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'go_.*|process_.*|promhttp_.*'
          action: drop
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: webapp-jvm-metrics
  namespace: monitoring
  labels:
    app: webapp
    component: jvm
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: webapp
  namespaceSelector:
    matchNames:
      - app-dev
      - app-staging
      - app-prod
  endpoints:
    - port: http
      path: /actuator/prometheus
      interval: 15s
      scrapeTimeout: 10s
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'jvm_.*|tomcat_.*|spring_.*'
          action: keep
```

#### 2.2 ServiceMonitor pour base de données

```yaml
# monitoring/servicemonitors/database-servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: postgresql-metrics
  namespace: monitoring
  labels:
    app: postgresql
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: postgresql
      component: metrics
  namespaceSelector:
    matchNames:
      - database
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: redis-metrics
  namespace: monitoring
  labels:
    app: redis
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app: redis
      component: metrics
  namespaceSelector:
    matchNames:
      - database
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

### Étape 3 : Règles d'alertes personnalisées

#### 3.1 Alertes application

```yaml
# monitoring/rules/application-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: application-alerts
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: webapp.rules
      interval: 30s
      rules:
        # Application down
        - alert: WebAppDown
          expr: up{job="webapp-metrics"} == 0
          for: 1m
          labels:
            severity: critical
            service: webapp
          annotations:
            summary: 'WebApp instance is down'
            description: 'WebApp instance {{ $labels.instance }} has been down for more than 1 minute.'

        # High error rate
        - alert: WebAppHighErrorRate
          expr: |
            (
              rate(http_requests_total{job="webapp-metrics",status=~"5.."}[5m]) /
              rate(http_requests_total{job="webapp-metrics"}[5m])
            ) * 100 > 5
          for: 5m
          labels:
            severity: warning
            service: webapp
          annotations:
            summary: 'WebApp high error rate'
            description: 'WebApp error rate is {{ $value }}% for more than 5 minutes.'

        # High response time
        - alert: WebAppHighLatency
          expr: |
            histogram_quantile(0.95, 
              rate(http_request_duration_seconds_bucket{job="webapp-metrics"}[5m])
            ) > 2
          for: 10m
          labels:
            severity: warning
            service: webapp
          annotations:
            summary: 'WebApp high latency'
            description: 'WebApp 95th percentile latency is {{ $value }}s for more than 10 minutes.'

        # High memory usage
        - alert: WebAppHighMemoryUsage
          expr: |
            (
              jvm_memory_used_bytes{job="webapp-metrics",area="heap"} /
              jvm_memory_max_bytes{job="webapp-metrics",area="heap"}
            ) * 100 > 80
          for: 15m
          labels:
            severity: warning
            service: webapp
          annotations:
            summary: 'WebApp high memory usage'
            description: 'WebApp JVM heap usage is {{ $value }}% for more than 15 minutes.'

        # Database connection pool exhaustion
        - alert: WebAppDBConnectionPoolExhaustion
          expr: |
            (
              tomcat_jdbc_connections_active_current{job="webapp-metrics"} /
              tomcat_jdbc_connections_max{job="webapp-metrics"}
            ) * 100 > 90
          for: 5m
          labels:
            severity: critical
            service: webapp
          annotations:
            summary: 'WebApp database connection pool exhaustion'
            description: 'WebApp DB connection pool usage is {{ $value }}% for more than 5 minutes.'

    - name: database.rules
      interval: 30s
      rules:
        # PostgreSQL down
        - alert: PostgreSQLDown
          expr: pg_up == 0
          for: 1m
          labels:
            severity: critical
            service: postgresql
          annotations:
            summary: 'PostgreSQL is down'
            description: 'PostgreSQL instance {{ $labels.instance }} is down.'

        # High connections
        - alert: PostgreSQLHighConnections
          expr: |
            (
              pg_stat_database_numbackends /
              pg_settings_max_connections
            ) * 100 > 80
          for: 5m
          labels:
            severity: warning
            service: postgresql
          annotations:
            summary: 'PostgreSQL high connections'
            description: 'PostgreSQL connections usage is {{ $value }}%.'

        # Slow queries
        - alert: PostgreSQLSlowQueries
          expr: pg_stat_activity_max_tx_duration > 300
          for: 10m
          labels:
            severity: warning
            service: postgresql
          annotations:
            summary: 'PostgreSQL slow queries detected'
            description: 'PostgreSQL has queries running for more than 5 minutes.'

        # Redis down
        - alert: RedisDown
          expr: redis_up == 0
          for: 1m
          labels:
            severity: critical
            service: redis
          annotations:
            summary: 'Redis is down'
            description: 'Redis instance {{ $labels.instance }} is down.'

        # High memory usage
        - alert: RedisHighMemoryUsage
          expr: |
            (
              redis_memory_used_bytes /
              redis_config_maxmemory
            ) * 100 > 90
          for: 10m
          labels:
            severity: warning
            service: redis
          annotations:
            summary: 'Redis high memory usage'
            description: 'Redis memory usage is {{ $value }}%.'
```

#### 3.2 Alertes infrastructure

```yaml
# monitoring/rules/infrastructure-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: infrastructure-alerts
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: node.rules
      interval: 30s
      rules:
        # Node CPU usage
        - alert: NodeHighCPUUsage
          expr: |
            (
              1 - (
                avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)
              )
            ) * 100 > 80
          for: 15m
          labels:
            severity: warning
            component: node
          annotations:
            summary: 'Node high CPU usage'
            description: 'Node {{ $labels.instance }} CPU usage is {{ $value }}% for more than 15 minutes.'

        # Node memory usage
        - alert: NodeHighMemoryUsage
          expr: |
            (
              (
                node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes
              ) / node_memory_MemTotal_bytes
            ) * 100 > 85
          for: 10m
          labels:
            severity: warning
            component: node
          annotations:
            summary: 'Node high memory usage'
            description: 'Node {{ $labels.instance }} memory usage is {{ $value }}%.'

        # Node disk usage
        - alert: NodeHighDiskUsage
          expr: |
            (
              (
                node_filesystem_size_bytes{fstype!="tmpfs"} - 
                node_filesystem_avail_bytes{fstype!="tmpfs"}
              ) / node_filesystem_size_bytes{fstype!="tmpfs"}
            ) * 100 > 85
          for: 10m
          labels:
            severity: warning
            component: node
          annotations:
            summary: 'Node high disk usage'
            description: 'Node {{ $labels.instance }} disk usage is {{ $value }}% on {{ $labels.mountpoint }}.'

        # Node load average
        - alert: NodeHighLoadAverage
          expr: node_load15 > (count by (instance) (node_cpu_seconds_total{mode="idle"})) * 1.5
          for: 10m
          labels:
            severity: warning
            component: node
          annotations:
            summary: 'Node high load average'
            description: 'Node {{ $labels.instance }} load average is {{ $value }}.'

    - name: kubernetes.rules
      interval: 30s
      rules:
        # Pod CrashLooping
        - alert: PodCrashLooping
          expr: |
            rate(kube_pod_container_status_restarts_total[5m]) * 60 * 5 > 0
          for: 5m
          labels:
            severity: warning
            component: kubernetes
          annotations:
            summary: 'Pod is crash looping'
            description: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping.'

        # Pod not ready
        - alert: PodNotReady
          expr: |
            kube_pod_status_ready{condition="false"} == 1
          for: 15m
          labels:
            severity: warning
            component: kubernetes
          annotations:
            summary: 'Pod not ready'
            description: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} has been not ready for more than 15 minutes.'

        # Deployment replica mismatch
        - alert: DeploymentReplicasMismatch
          expr: |
            kube_deployment_spec_replicas != kube_deployment_status_available_replicas
          for: 10m
          labels:
            severity: warning
            component: kubernetes
          annotations:
            summary: 'Deployment replicas mismatch'
            description: 'Deployment {{ $labels.namespace }}/{{ $labels.deployment }} has {{ $labels.spec_replicas }} desired but {{ $labels.available_replicas }} available replicas.'

        # PVC usage high
        - alert: PVCUsageHigh
          expr: |
            (
              kubelet_volume_stats_used_bytes /
              kubelet_volume_stats_capacity_bytes
            ) * 100 > 85
          for: 10m
          labels:
            severity: warning
            component: kubernetes
          annotations:
            summary: 'PVC usage high'
            description: 'PVC {{ $labels.namespace }}/{{ $labels.persistentvolumeclaim }} usage is {{ $value }}%.'
```

### Étape 4 : Dashboards Grafana personnalisés

#### 4.1 Dashboard application overview

```json
# monitoring/dashboards/webapp-dashboard.json
{
  "dashboard": {
    "id": null,
    "title": "WebApp Overview",
    "tags": ["webapp", "application"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Application Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"webapp-metrics\"}",
            "legendFormat": "{{ instance }}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "mappings": [
              {
                "options": {
                  "0": {
                    "text": "DOWN"
                  },
                  "1": {
                    "text": "UP"
                  }
                },
                "type": "value"
              }
            ],
            "thresholds": {
              "steps": [
                {
                  "color": "red",
                  "value": null
                },
                {
                  "color": "green",
                  "value": 1
                }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "HTTP Requests Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"webapp-metrics\"}[5m])",
            "legendFormat": "{{ method }} {{ status }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{job=\"webapp-metrics\"}[5m]))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"webapp-metrics\"}[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job=\"webapp-metrics\"}[5m]))",
            "legendFormat": "99th percentile"
          }
        ]
      },
      {
        "id": 4,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"webapp-metrics\",status=~\"5..\"}[5m]) / rate(http_requests_total{job=\"webapp-metrics\"}[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      },
      {
        "id": 5,
        "title": "JVM Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "jvm_memory_used_bytes{job=\"webapp-metrics\",area=\"heap\"}",
            "legendFormat": "Heap Used"
          },
          {
            "expr": "jvm_memory_max_bytes{job=\"webapp-metrics\",area=\"heap\"}",
            "legendFormat": "Heap Max"
          }
        ]
      },
      {
        "id": 6,
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "tomcat_jdbc_connections_active_current{job=\"webapp-metrics\"}",
            "legendFormat": "Active Connections"
          },
          {
            "expr": "tomcat_jdbc_connections_max{job=\"webapp-metrics\"}",
            "legendFormat": "Max Connections"
          }
        ]
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "30s"
  }
}
```

### Étape 5 : Tests et validation

#### 5.1 Script de test du monitoring

```bash
#!/bin/bash
# scripts/test-monitoring-stack.sh

set -e

NAMESPACE=${1:-monitoring}
TIMEOUT=${2:-300}

echo "🧪 Test du stack de monitoring dans $NAMESPACE"

# Vérifier que tous les pods sont prêts
echo "⏳ Vérification des pods..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=kube-prometheus-stack -n $NAMESPACE --timeout=${TIMEOUT}s

# Test Prometheus
echo "🔍 Test de Prometheus..."
PROMETHEUS_URL=$(kubectl get service monitoring-prometheus -n $NAMESPACE -o jsonpath='{.spec.clusterIP}')
kubectl port-forward service/monitoring-prometheus 9090:9090 -n $NAMESPACE &
PROM_PID=$!
sleep 10

PROMETHEUS_HEALTH=$(curl -s http://localhost:9090/-/healthy)
if [ "$PROMETHEUS_HEALTH" = "Prometheus is Healthy." ]; then
    echo "✅ Prometheus fonctionne"
else
    echo "❌ Prometheus non accessible"
    kill $PROM_PID
    exit 1
fi

# Test des métriques
METRICS_COUNT=$(curl -s "http://localhost:9090/api/v1/label/__name__/values" | jq -r '.data | length')
echo "📊 Nombre de métriques collectées: $METRICS_COUNT"

if [ "$METRICS_COUNT" -gt 100 ]; then
    echo "✅ Métriques collectées correctement"
else
    echo "❌ Peu de métriques collectées"
fi

kill $PROM_PID

# Test Grafana
echo "🔍 Test de Grafana..."
kubectl port-forward service/grafana 3000:80 -n $NAMESPACE &
GRAF_PID=$!
sleep 10

GRAFANA_HEALTH=$(curl -s -w "%{http_code}" http://localhost:3000/api/health -o /dev/null)
if [ "$GRAFANA_HEALTH" = "200" ]; then
    echo "✅ Grafana accessible"
else
    echo "❌ Grafana non accessible (Code: $GRAFANA_HEALTH)"
fi

kill $GRAF_PID

# Test Alertmanager
echo "🔍 Test d'Alertmanager..."
kubectl port-forward service/alertmanager 9093:9093 -n $NAMESPACE &
AM_PID=$!
sleep 10

ALERTMANAGER_HEALTH=$(curl -s -w "%{http_code}" http://localhost:9093/-/healthy -o /dev/null)
if [ "$ALERTMANAGER_HEALTH" = "200" ]; then
    echo "✅ Alertmanager fonctionne"
else
    echo "❌ Alertmanager non accessible"
fi

kill $AM_PID

echo "🎉 Tests du stack de monitoring terminés"
```

#### 5.2 Test des alertes

```bash
#!/bin/bash
# scripts/test-alerts.sh

echo "🧪 Test des alertes"

# Créer une application de test qui va générer des alertes
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app-alerts
  namespace: default
  labels:
    app: test-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: test-app
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "1Mi"
            cpu: "1m"
          limits:
            memory: "2Mi"  # Très faible pour déclencher des alertes
            cpu: "2m"
---
apiVersion: v1
kind: Service
metadata:
  name: test-app-service
  namespace: default
  labels:
    app: test-app
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "80"
spec:
  selector:
    app: test-app
  ports:
  - port: 80
    targetPort: 80
EOF

echo "⏳ Attente de la montée en charge..."
sleep 60

# Vérifier les alertes dans Prometheus
echo "🔍 Vérification des alertes actives..."
kubectl port-forward service/monitoring-prometheus 9090:9090 -n monitoring &
PID=$!
sleep 10

ALERTS=$(curl -s "http://localhost:9090/api/v1/alerts" | jq -r '.data.alerts | length')
echo "📊 Nombre d'alertes actives: $ALERTS"

kill $PID

# Nettoyer
kubectl delete deployment test-app-alerts -n default
kubectl delete service test-app-service -n default

echo "🎉 Test des alertes terminé"
```

---

## 🎯 Résultats attendus

### ✅ Stack monitoring complet

- **Prometheus** collectant toutes les métriques
- **Grafana** avec dashboards personnalisés
- **Alertmanager** configuré avec notifications
- **Exporters** pour infrastructure et applications

### ✅ Observabilité 360°

- **Métriques** infrastructure (CPU, mémoire, disque)
- **Métriques** applicatives (latence, erreurs, throughput)
- **Alertes** intelligentes et graduées
- **Dashboards** par service et par équipe

### ✅ Production-ready

- **Haute disponibilité** avec persistance
- **Sécurité** (TLS, RBAC)
- **Performance** optimisée
- **Rétention** des données configurée

---

_Correction réalisée par Hassan ESSADIK - Formation DevOps Kubernetes_
