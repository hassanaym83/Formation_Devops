# LAB 6 - Monitoring et Observabilité avec Prometheus et Grafana

## Objectifs

- Installer et configurer Prometheus sur Kubernetes
- Déployer Grafana avec dashboards personnalisés
- Configurer AlertManager pour les notifications
- Implémenter le monitoring d'applications avec métriques custom
- Mettre en place la stack de monitoring complète (Prometheus, Grafana, AlertManager, Node Exporter)

## Prérequis

- Cluster Kubernetes fonctionnel
- kubectl configuré
- Helm 3.x installé
- Connaissances de base de Prometheus et PromQL
- Application à monitorer déployée

## Contexte du LAB

Vous allez déployer une stack de monitoring complète pour superviser :

- L'infrastructure Kubernetes (nœuds, pods, services)
- Les applications métier avec métriques custom
- La santé du cluster et des workloads
- Les performances et la disponibilité

## Exercice 1 : Installation de la stack Prometheus

### Étape 1.1 : Ajout du repository Helm

```bash
# Ajouter le repository Prometheus Community
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### Étape 1.2 : Création du namespace

```bash
kubectl create namespace monitoring
```

### Étape 1.3 : Configuration des values Helm

Créez `monitoring/prometheus-values.yaml` :

```yaml
# Prometheus Operator configuration
prometheus:
  prometheusSpec:
    # Rétention des données
    retention: 30d
    retentionSize: 50GB

    # Ressources
    resources:
      requests:
        memory: 2Gi
        cpu: 1000m
      limits:
        memory: 4Gi
        cpu: 2000m

    # Storage persistant
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ['ReadWriteOnce']
          resources:
            requests:
              storage: 50Gi

    # Configuration des ServiceMonitors
    serviceMonitorSelectorNilUsesHelmValues: false
    serviceMonitorSelector: {}

    # Configuration des PodMonitors
    podMonitorSelectorNilUsesHelmValues: false
    podMonitorSelector: {}

    # Configuration des Rules
    ruleSelectorNilUsesHelmValues: false
    ruleSelector: {}

    # Configuration externe
    externalUrl: 'https://prometheus.your-domain.com'

    # Scrape configuration
    scrapeInterval: '30s'
    evaluationInterval: '30s'

    # Additional scrape configs
    additionalScrapeConfigs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels:
              [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)

# Grafana configuration
grafana:
  enabled: true

  # Admin credentials
  adminPassword: 'admin123'

  # Persistence
  persistence:
    enabled: true
    storageClassName: fast-ssd
    size: 10Gi

  # Resources
  resources:
    requests:
      memory: 256Mi
      cpu: 100m
    limits:
      memory: 512Mi
      cpu: 200m

  # Ingress
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - grafana.your-domain.com
    tls:
      - secretName: grafana-tls
        hosts:
          - grafana.your-domain.com

  # Data sources
  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-kube-prometheus-prometheus:9090
          access: proxy
          isDefault: true
        - name: Loki
          type: loki
          url: http://loki:3100
          access: proxy

  # Dashboard providers
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

  # Dashboards
  dashboards:
    default:
      kubernetes-cluster:
        gnetId: 7249
        revision: 1
        datasource: Prometheus
      kubernetes-pods:
        gnetId: 6417
        revision: 1
        datasource: Prometheus
      node-exporter:
        gnetId: 1860
        revision: 27
        datasource: Prometheus

# AlertManager configuration
alertmanager:
  alertmanagerSpec:
    # Ressources
    resources:
      requests:
        memory: 256Mi
        cpu: 100m
      limits:
        memory: 512Mi
        cpu: 200m

    # Storage
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ['ReadWriteOnce']
          resources:
            requests:
              storage: 5Gi

    # Configuration
    configSecret: alertmanager-config

    # External URL
    externalUrl: 'https://alertmanager.your-domain.com'

# Node Exporter
nodeExporter:
  enabled: true

# Kube State Metrics
kubeStateMetrics:
  enabled: true

# Additional components
kubeEtcd:
  enabled: false

kubeControllerManager:
  enabled: false

kubeScheduler:
  enabled: false

# Service monitors pour components système
defaultRules:
  create: true
  rules:
    alertmanager: true
    etcd: false
    general: true
    k8s: true
    kubeApiserver: true
    kubeApiserverAvailability: true
    kubeApiserverSlos: true
    kubelet: true
    kubePrometheusGeneral: true
    kubePrometheusNodeRecording: true
    kubernetesApps: true
    kubernetesResources: true
    kubernetesStorage: true
    kubernetesSystem: true
    node: true
    nodeExporterAlerting: true
    nodeExporterRecording: true
    prometheus: true
    prometheusOperator: true
```

### Étape 1.4 : Installation avec Helm

```bash
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values monitoring/prometheus-values.yaml \
  --create-namespace
```

## Exercice 2 : Configuration AlertManager

### Étape 2.1 : Configuration AlertManager

Créez `monitoring/alertmanager-config.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-config
  namespace: monitoring
type: Opaque
stringData:
  alertmanager.yml: |
    global:
      # Configuration SMTP
      smtp_smarthost: 'smtp.gmail.com:587'
      smtp_from: 'alerts@your-company.com'
      smtp_auth_username: 'alerts@your-company.com'
      smtp_auth_password: 'your-app-password'
      
      # Configuration Slack
      slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

    # Templates
    templates:
    - '/etc/alertmanager/templates/*.tmpl'

    # Route principale
    route:
      group_by: ['alertname', 'cluster', 'service']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 1h
      receiver: 'web.hook'
      routes:
      
      # Alertes critiques -> Slack + Email
      - match:
          severity: critical
        receiver: 'critical-alerts'
        group_wait: 10s
        repeat_interval: 5m
      
      # Alertes warning -> Slack seulement
      - match:
          severity: warning
        receiver: 'warning-alerts'
        group_wait: 30s
        repeat_interval: 1h
      
      # Alertes infrastructure
      - match_re:
          alertname: 'Node.*|Kubernetes.*'
        receiver: 'infrastructure-alerts'
      
      # Alertes applications
      - match_re:
          alertname: 'Application.*|Service.*'
        receiver: 'application-alerts'

    # Définition des receivers
    receivers:
    - name: 'web.hook'
      webhook_configs:
      - url: 'http://webhook-service:8080/alerts'
        send_resolved: true

    - name: 'critical-alerts'
      slack_configs:
      - channel: '#alerts-critical'
        title: 'CRITICAL: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Severity:* {{ .Labels.severity }}
          *Instance:* {{ .Labels.instance }}
          {{ end }}
        color: 'danger'
        send_resolved: true
      email_configs:
      - to: 'devops-team@your-company.com'
        subject: 'CRITICAL Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Severity: {{ .Labels.severity }}
          Instance: {{ .Labels.instance }}
          {{ end }}

    - name: 'warning-alerts'
      slack_configs:
      - channel: '#alerts'
        title: 'WARNING: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        color: 'warning'
        send_resolved: true

    - name: 'infrastructure-alerts'
      slack_configs:
      - channel: '#infrastructure'
        title: 'Infrastructure Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        color: 'warning'

    - name: 'application-alerts'
      slack_configs:
      - channel: '#applications'
        title: 'Application Alert: {{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
        color: 'warning'

    # Inhibition rules
    inhibit_rules:
    - source_match:
        severity: 'critical'
      target_match:
        severity: 'warning'
      equal: ['alertname', 'cluster', 'service']
```

### Étape 2.2 : Application de la configuration

```bash
kubectl apply -f monitoring/alertmanager-config.yaml
```

## Exercice 3 : Règles d'alertes personnalisées

### Étape 3.1 : Règles d'infrastructure

Créez `monitoring/infrastructure-rules.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: infrastructure-rules
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: kubernetes-infrastructure
      rules:
        # Node alerts
        - alert: NodeDown
          expr: up{job="node-exporter"} == 0
          for: 5m
          labels:
            severity: critical
            category: infrastructure
          annotations:
            summary: 'Node {{ $labels.instance }} is down'
            description: 'Node {{ $labels.instance }} has been down for more than 5 minutes'

        - alert: NodeHighCPU
          expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
          for: 10m
          labels:
            severity: warning
            category: infrastructure
          annotations:
            summary: 'High CPU usage on node {{ $labels.instance }}'
            description: 'CPU usage is {{ $value }}% on node {{ $labels.instance }}'

        - alert: NodeHighMemory
          expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 80
          for: 10m
          labels:
            severity: warning
            category: infrastructure
          annotations:
            summary: 'High memory usage on node {{ $labels.instance }}'
            description: 'Memory usage is {{ $value }}% on node {{ $labels.instance }}'

        - alert: NodeDiskSpaceLow
          expr: (1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100 > 80
          for: 5m
          labels:
            severity: warning
            category: infrastructure
          annotations:
            summary: 'Low disk space on node {{ $labels.instance }}'
            description: 'Disk usage is {{ $value }}% on node {{ $labels.instance }}'

        # Kubernetes alerts
        - alert: PodCrashLooping
          expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
          for: 5m
          labels:
            severity: warning
            category: kubernetes
          annotations:
            summary: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} is crash looping'
            description: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} has restarted {{ $value }} times in the last 15 minutes'

        - alert: PodNotReady
          expr: kube_pod_status_ready{condition="false"} == 1
          for: 10m
          labels:
            severity: warning
            category: kubernetes
          annotations:
            summary: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} not ready'
            description: 'Pod {{ $labels.namespace }}/{{ $labels.pod }} has been in not ready state for more than 10 minutes'

        - alert: DeploymentReplicasMismatch
          expr: kube_deployment_spec_replicas != kube_deployment_status_available_replicas
          for: 10m
          labels:
            severity: warning
            category: kubernetes
          annotations:
            summary: 'Deployment {{ $labels.namespace }}/{{ $labels.deployment }} replica mismatch'
            description: 'Deployment {{ $labels.namespace }}/{{ $labels.deployment }} has {{ $labels.spec_replicas }} desired but {{ $labels.available_replicas }} available replicas'
```

### Étape 3.2 : Règles d'application

Créez `monitoring/application-rules.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: application-rules
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: application-metrics
      rules:
        # HTTP Error rates
        - alert: HighErrorRate
          expr: |
            (
              sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
              /
              sum(rate(http_requests_total[5m])) by (service)
            ) * 100 > 5
          for: 5m
          labels:
            severity: warning
            category: application
          annotations:
            summary: 'High error rate for service {{ $labels.service }}'
            description: 'Error rate is {{ $value }}% for service {{ $labels.service }}'

        - alert: HighLatency
          expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)) > 0.5
          for: 5m
          labels:
            severity: warning
            category: application
          annotations:
            summary: 'High latency for service {{ $labels.service }}'
            description: '95th percentile latency is {{ $value }}s for service {{ $labels.service }}'

        # Database alerts
        - alert: DatabaseConnectionsHigh
          expr: mysql_global_status_threads_connected / mysql_global_variables_max_connections * 100 > 80
          for: 5m
          labels:
            severity: warning
            category: database
          annotations:
            summary: 'High database connections'
            description: 'Database connection usage is {{ $value }}%'

        # Custom business metrics
        - alert: OrderProcessingDelayed
          expr: increase(orders_processing_time_seconds[5m]) > 300
          for: 10m
          labels:
            severity: critical
            category: business
          annotations:
            summary: 'Order processing is delayed'
            description: 'Order processing time has increased by {{ $value }}s in the last 5 minutes'
```

## Exercice 4 : Application avec métriques custom

### Étape 4.1 : Application Node.js avec métriques

Créez `app/server.js` :

```javascript
const express = require('express');
const prometheus = require('prom-client');
const app = express();
const port = process.env.PORT || 3000;

// Create a Registry to register the metrics
const register = new prometheus.Registry();

// Add a default label which is added to all metrics
register.setDefaultLabels({
  app: 'ecommerce-api',
  version: process.env.APP_VERSION || '1.0.0'
});

// Enable the collection of default metrics
prometheus.collectDefaultMetrics({register});

// Custom metrics
const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register]
});

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5],
  registers: [register]
});

const activeUsers = new prometheus.Gauge({
  name: 'active_users_total',
  help: 'Total number of active users',
  registers: [register]
});

const ordersProcessingTime = new prometheus.Histogram({
  name: 'orders_processing_time_seconds',
  help: 'Time taken to process orders',
  labelNames: ['status'],
  buckets: [1, 5, 10, 30, 60, 120],
  registers: [register]
});

// Middleware pour mesurer les requêtes
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route ? req.route.path : req.path;

    httpRequestsTotal.inc({
      method: req.method,
      route: route,
      status: res.statusCode
    });

    httpRequestDuration.observe(
      {
        method: req.method,
        route: route,
        status: res.statusCode
      },
      duration
    );
  });

  next();
});

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'E-commerce API',
    version: process.env.APP_VERSION || '1.0.0'
  });
});

app.get('/health', (req, res) => {
  res
    .status(200)
    .json({status: 'healthy', timestamp: new Date().toISOString()});
});

app.get('/metrics', (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
});

// API routes avec métriques
app.get('/api/orders', (req, res) => {
  const start = Date.now();

  // Simulate order processing
  setTimeout(() => {
    const duration = (Date.now() - start) / 1000;
    ordersProcessingTime.observe({status: 'success'}, duration);

    res.json({
      orders: [
        {id: 1, product: 'Laptop', amount: 999.99},
        {id: 2, product: 'Mouse', amount: 29.99}
      ]
    });
  }, Math.random() * 1000);
});

app.post('/api/orders', (req, res) => {
  const start = Date.now();

  // Simulate order creation
  setTimeout(() => {
    const duration = (Date.now() - start) / 1000;
    const success = Math.random() > 0.1; // 90% success rate

    ordersProcessingTime.observe(
      {
        status: success ? 'success' : 'error'
      },
      duration
    );

    if (success) {
      res.status(201).json({id: Date.now(), status: 'created'});
    } else {
      res.status(500).json({error: 'Failed to create order'});
    }
  }, Math.random() * 2000);
});

// Simulate active users updates
setInterval(() => {
  const users = Math.floor(Math.random() * 1000) + 100;
  activeUsers.set(users);
}, 30000);

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
```

### Étape 4.2 : Dockerfile pour l'application

Créez `app/Dockerfile` :

```dockerfile
FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY server.js ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

EXPOSE 3000

CMD ["node", "server.js"]
```

### Étape 4.3 : Package.json

Créez `app/package.json` :

```json
{
  "name": "ecommerce-api",
  "version": "1.0.0",
  "description": "E-commerce API with Prometheus metrics",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "prom-client": "^14.2.0"
  }
}
```

## Exercice 5 : Déploiement et monitoring de l'application

### Étape 5.1 : Manifestes Kubernetes

Créez `k8s/deployment.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-api
  namespace: default
  labels:
    app: ecommerce-api
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ecommerce-api
  template:
    metadata:
      labels:
        app: ecommerce-api
        version: v1.0.0
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '3000'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: api
          image: ecommerce-api:latest
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: APP_VERSION
              value: 'v1.0.0'
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: ecommerce-api
  namespace: default
  labels:
    app: ecommerce-api
spec:
  selector:
    app: ecommerce-api
  ports:
    - name: http
      port: 80
      targetPort: 3000
  type: ClusterIP
```

### Étape 5.2 : ServiceMonitor

Créez `monitoring/servicemonitor.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-api
  namespace: monitoring
  labels:
    app: ecommerce-api
spec:
  selector:
    matchLabels:
      app: ecommerce-api
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
  namespaceSelector:
    matchNames:
      - default
```

### Étape 5.3 : PodMonitor pour monitoring par pods

Créez `monitoring/podmonitor.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: ecommerce-api-pods
  namespace: monitoring
  labels:
    app: ecommerce-api
spec:
  selector:
    matchLabels:
      app: ecommerce-api
  podMetricsEndpoints:
    - port: http
      path: /metrics
      interval: 30s
  namespaceSelector:
    matchNames:
      - default
```

## Exercice 6 : Dashboards Grafana personnalisés

### Étape 6.1 : Dashboard infrastructure

Créez `grafana/dashboards/infrastructure.json` :

```json
{
  "dashboard": {
    "id": null,
    "title": "Kubernetes Infrastructure",
    "tags": ["kubernetes", "infrastructure"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Cluster CPU Usage",
        "type": "stat",
        "targets": [
          {
            "expr": "100 - (avg(irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 70},
                {"color": "red", "value": 90}
              ]
            },
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Cluster Memory Usage",
        "type": "stat",
        "targets": [
          {
            "expr": "100 * (1 - (sum(node_memory_MemAvailable_bytes) / sum(node_memory_MemTotal_bytes)))",
            "legendFormat": "Memory Usage %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {
              "mode": "thresholds"
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 70},
                {"color": "red", "value": 90}
              ]
            },
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "id": 3,
        "title": "Pods by Namespace",
        "type": "piechart",
        "targets": [
          {
            "expr": "sum by (namespace) (kube_pod_info)",
            "legendFormat": "{{ namespace }}"
          }
        ],
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "10s"
  }
}
```

### Étape 6.2 : Dashboard application

Créez `grafana/dashboards/application.json` :

```json
{
  "dashboard": {
    "id": null,
    "title": "E-commerce API Metrics",
    "tags": ["application", "ecommerce"],
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{ service }}"
          }
        ],
        "yAxes": [
          {
            "label": "Requests/sec",
            "min": 0
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service) * 100",
            "legendFormat": "{{ service }}"
          }
        ],
        "yAxes": [
          {
            "label": "Error Rate %",
            "min": 0,
            "max": 100
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      },
      {
        "id": 3,
        "title": "Response Time (95th percentile)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{ service }}"
          }
        ],
        "yAxes": [
          {
            "label": "Seconds",
            "min": 0
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
      },
      {
        "id": 4,
        "title": "Active Users",
        "type": "stat",
        "targets": [
          {
            "expr": "active_users_total",
            "legendFormat": "Active Users"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
      }
    ]
  }
}
```

## Exercice 7 : Tests de charge et monitoring

### Étape 7.1 : Script de test de charge

Créez `scripts/load-test.sh` :

```bash
#!/bin/bash

set -e

API_URL=${1:-"http://localhost:30080"}
CONCURRENT_USERS=${2:-10}
DURATION=${3:-300}

echo "Starting load test..."
echo "API URL: $API_URL"
echo "Concurrent users: $CONCURRENT_USERS"
echo "Duration: $DURATION seconds"

# Function to make requests
make_requests() {
    local user_id=$1
    local end_time=$(($(date +%s) + DURATION))

    while [ $(date +%s) -lt $end_time ]; do
        # GET requests
        curl -s "$API_URL/api/orders" > /dev/null
        sleep $((RANDOM % 3 + 1))

        # POST requests (some will fail intentionally)
        curl -s -X POST "$API_URL/api/orders" \
             -H "Content-Type: application/json" \
             -d '{"product":"test","amount":100}' > /dev/null
        sleep $((RANDOM % 2 + 1))

        # Health checks
        curl -s "$API_URL/health" > /dev/null
        sleep 1
    done

    echo "User $user_id finished"
}

# Start concurrent users
for i in $(seq 1 $CONCURRENT_USERS); do
    make_requests $i &
done

# Wait for all background jobs
wait

echo "Load test completed!"
```

### Étape 7.2 : Monitoring pendant le test

```bash
# Terminal 1: Lancer le test de charge
./scripts/load-test.sh http://ecommerce-api.default.svc.cluster.local 50 600

# Terminal 2: Surveiller les métriques
watch -n 2 'kubectl top nodes && echo "---" && kubectl top pods'

# Terminal 3: Vérifier les alertes
kubectl logs -n monitoring deployment/alertmanager-kube-prometheus-alertmanager -f
```

## Exercice 8 : Configuration avancée

### Étape 8.1 : Recording rules

Créez `monitoring/recording-rules.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: recording-rules
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: api.rules
      interval: 30s
      rules:
        - record: api:http_requests:rate5m
          expr: sum(rate(http_requests_total[5m])) by (service, method, status)

        - record: api:http_requests:error_rate5m
          expr: |
            sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
            /
            sum(rate(http_requests_total[5m])) by (service)

        - record: api:http_request_duration:p95_5m
          expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

        - record: instance:cpu_usage:rate5m
          expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### Étape 8.2 : Configuration Prometheus externalisée

Créez `monitoring/prometheus-config.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 30s
      evaluation_interval: 30s
      external_labels:
        cluster: 'production'
        region: 'eu-west-1'

    rule_files:
    - "/etc/prometheus/rules/*.yml"

    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093

    scrape_configs:
    - job_name: 'prometheus'
      static_configs:
      - targets: ['localhost:9090']

    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

    - job_name: 'kubernetes-services'
      kubernetes_sd_configs:
      - role: endpoints
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
        action: replace
        target_label: __scheme__
        regex: (https?)
```

## Exercice 9 : Haute disponibilité

### Étape 9.1 : Prometheus HA

Configurez Prometheus en mode haute disponibilité :

```yaml
# Dans prometheus-values.yaml
prometheus:
  prometheusSpec:
    replicas: 2

    # Configuration pour HA
    retention: 15d
    retentionSize: 25GB

    # External labels pour identifier les replicas
    externalLabels:
      cluster: production
      replica: '$(POD_NAME)'

    # Configuration de stockage externe (Thanos)
    thanos:
      image: quay.io/thanos/thanos:v0.31.0
      objectStorageConfig:
        key: thanos.yaml
        name: thanos-objstore-secret
```

### Étape 9.2 : AlertManager HA

```yaml
alertmanager:
  alertmanagerSpec:
    replicas: 3

    # Configuration cluster
    clusterAdvertiseAddress: false
    clusterGossipInterval: '2s'
    clusterPushpullInterval: '60s'
```

## Exercice 10 : Cas pratique complet

### Objectif

Déployez une stack de monitoring complète qui surveille :

1. **Infrastructure** : CPU, mémoire, disque, réseau des nœuds
2. **Kubernetes** : Pods, deployments, services, ingress
3. **Application** : Métriques métier, performance, erreurs
4. **Base de données** : Connexions, requêtes, performance
5. **Sécurité** : Tentatives d'accès, anomalies

### Livrables attendus

1. **Stack Prometheus** installée et configurée
2. **AlertManager** avec routage des alertes
3. **Grafana** avec dashboards personnalisés
4. **Application instrumentée** avec métriques custom
5. **Règles d'alertes** pour infrastructure et applications
6. **ServiceMonitors** et PodMonitors configurés
7. **Tests de charge** et validation des alertes
8. **Documentation** complète du monitoring

## Questions de validation

1. Quelle est la différence entre un ServiceMonitor et un PodMonitor ?
2. Comment configurer des règles d'alertes avec des seuils adaptatifs ?
3. Expliquez le concept de recording rules et leur utilité
4. Comment assurer la haute disponibilité de Prometheus ?
5. Quelles sont les bonnes pratiques pour les métriques custom ?

## Critères d'évaluation

- **Installation** : Stack complète déployée et fonctionnelle
- **Configuration** : AlertManager et règles correctement configurés
- **Métriques** : Application instrumentée avec métriques pertinentes
- **Dashboards** : Visualisations utiles et bien organisées
- **Alerting** : Notifications fonctionnelles et pertinentes
- **Documentation** : Guide complet d'utilisation

## Ressources utiles

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Kube-Prometheus-Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/)

---

**Durée estimée : 8-9 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
