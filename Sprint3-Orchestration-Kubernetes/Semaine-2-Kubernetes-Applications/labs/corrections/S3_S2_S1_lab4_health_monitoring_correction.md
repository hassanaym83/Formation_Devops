# Correction LAB 4 - Health Monitoring et Observabilité

## Vue d'ensemble de la solution

Cette correction présente une implémentation complète du monitoring de santé pour l'application e-commerce avec Prometheus, Grafana, alerting avancé et observabilité distribuée.

## Architecture de monitoring

```
Applications → Métriques → Prometheus → Grafana/AlertManager
     ↓
Health Checks → Probes → Kubernetes API
     ↓
Logs → Fluent Bit → Elasticsearch → Kibana
     ↓
Tracing → Jaeger → Distributed Tracing
```

## Étape 1 : Installation de la stack Prometheus

### 1.1 Déploiement Prometheus avec Helm

```bash
# Installation kube-prometheus-stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi \
  --set alertmanager.alertmanagerSpec.storage.volumeClaimTemplate.spec.resources.requests.storage=10Gi \
  --values prometheus-values.yaml
```

### 1.2 Configuration Prometheus personnalisée

```yaml
# prometheus-values.yaml
prometheus:
  prometheusSpec:
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false

    # Configuration pour scraping
    additionalScrapeConfigs:
      - job_name: 'ecommerce-services'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names: ['ecommerce']
        relabel_configs:
          - source_labels:
              [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels:
              [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__

    # External labels pour multi-cluster
    externalLabels:
      cluster: 'ecommerce-production'
      region: 'us-west-2'

grafana:
  # Configuration Grafana
  adminPassword: 'SecureAdminPassword123!'

  # Dashboards pré-configurés
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

  dashboards:
    default:
      ecommerce-overview:
        gnetId: 15757
        revision: 1
        datasource: Prometheus
      kubernetes-cluster:
        gnetId: 7249
        revision: 1
        datasource: Prometheus

alertmanager:
  config:
    global:
      smtp_smarthost: 'smtp.company.com:587'
      smtp_from: 'alerts@ecommerce.com'
      slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

    route:
      group_by: ['alertname', 'cluster', 'service']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 12h
      receiver: 'web.hook'
      routes:
        - match:
            severity: critical
          receiver: 'critical-alerts'
        - match:
            service: ecommerce
          receiver: 'ecommerce-team'

    receivers:
      - name: 'web.hook'
        slack_configs:
          - channel: '#monitoring'
            title: 'Alert - {{ .GroupLabels.alertname }}'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

      - name: 'critical-alerts'
        email_configs:
          - to: 'oncall@ecommerce.com'
            subject: '[CRITICAL] {{ .GroupLabels.alertname }}'
            html: |
              <h3>Critical Alert</h3>
              {{ range .Alerts }}
              <p><b>Alert:</b> {{ .Annotations.summary }}</p>
              <p><b>Description:</b> {{ .Annotations.description }}</p>
              <p><b>Runbook:</b> {{ .Annotations.runbook_url }}</p>
              {{ end }}
        slack_configs:
          - channel: '#critical-alerts'
            color: 'danger'
            title: '🚨 CRITICAL ALERT'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

      - name: 'ecommerce-team'
        slack_configs:
          - channel: '#ecommerce-alerts'
            color: 'warning'
            title: 'E-commerce Alert'
            text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

## Étape 2 : Configuration des Health Checks avancés

### 2.1 Applications avec probes complètes

```yaml
# ecommerce-health-enabled.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service-monitored
  namespace: ecommerce
  labels:
    app: product-service
    version: monitored
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
      version: monitored
  template:
    metadata:
      labels:
        app: product-service
        version: monitored
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: product-service
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
              name: http
            - containerPort: 8080
              name: metrics
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

          # Startup probe - pour applications lentes à démarrer
          startupProbe:
            httpGet:
              path: /startup
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 30 # 150s max pour démarrer
            successThreshold: 1

          # Liveness probe - redémarre le conteneur si échec
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
              httpHeaders:
                - name: X-Health-Check
                  value: liveness
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
            successThreshold: 1

          # Readiness probe - retire du service si échec
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
              httpHeaders:
                - name: X-Health-Check
                  value: readiness
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
            successThreshold: 1

          env:
            - name: SERVICE_NAME
              value: 'product-service'
            - name: LOG_LEVEL
              value: 'INFO'
            - name: ENABLE_METRICS
              value: 'true'

          volumeMounts:
            - name: health-config
              mountPath: /etc/nginx/conf.d
            - name: app-logs
              mountPath: /var/log/app

        # Sidecar pour logs structurés
        - name: log-forwarder
          image: fluent/fluent-bit:2.0
          volumeMounts:
            - name: app-logs
              mountPath: /var/log/app
              readOnly: true
            - name: fluent-bit-config
              mountPath: /fluent-bit/etc
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 100m
              memory: 128Mi

      volumes:
        - name: health-config
          configMap:
            name: product-health-config
        - name: app-logs
          emptyDir: {}
        - name: fluent-bit-config
          configMap:
            name: fluent-bit-config

---
# Configuration des endpoints de santé
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-health-config
  namespace: ecommerce
data:
  default.conf: |
    log_format structured_log escape=json
      '{'
        '"timestamp":"$time_iso8601",'
        '"request_id":"$request_id",'
        '"remote_addr":"$remote_addr",'
        '"method":"$request_method",'
        '"uri":"$request_uri",'
        '"status":"$status",'
        '"response_time":"$request_time",'
        '"body_bytes_sent":"$body_bytes_sent",'
        '"user_agent":"$http_user_agent",'
        '"service":"product-service"'
      '}';

    upstream backend_pool {
        server 127.0.0.1:80;
        keepalive 32;
    }

    server {
        listen 80;
        server_name localhost;
        
        access_log /var/log/app/access.log structured_log;
        error_log /var/log/app/error.log;
        
        location / {
            return 200 '{"service":"product-service","status":"running","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }
        
        location /products {
            # Simulation de latence variable
            set $delay 0;
            set_by_lua $delay 'return math.random(10, 100)';
            echo_sleep $delay;
            
            return 200 '{
                "products": [
                    {"id": 1, "name": "Laptop", "price": 999.99, "stock": 50},
                    {"id": 2, "name": "Phone", "price": 699.99, "stock": 100}
                ],
                "response_time_ms": '$delay',
                "timestamp": "$time_iso8601"
            }';
            add_header Content-Type application/json;
        }
    }

    server {
        listen 8080;
        server_name localhost;
        
        # Startup probe endpoint
        location /startup {
            access_log off;
            # Simuler un démarrage progressif
            if ($time_iso8601 ~ "^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:(\d{2}))") {
                set $seconds $2;
            }
            
            if ($seconds < "30") {
                return 503 '{"status":"starting","message":"Service initializing"}';
            }
            
            return 200 '{"status":"started","message":"Service ready to accept traffic"}';
            add_header Content-Type application/json;
        }
        
        # Liveness probe endpoint
        location /health/live {
            access_log off;
            
            # Vérifications internes critiques
            content_by_lua_block {
                -- Simulation de vérifications système
                local health_checks = {
                    memory_usage = math.random(20, 80),
                    cpu_usage = math.random(10, 90),
                    disk_space = math.random(30, 95),
                    thread_count = math.random(5, 50)
                }
                
                local status = "healthy"
                local issues = {}
                
                if health_checks.memory_usage > 95 then
                    status = "unhealthy"
                    table.insert(issues, "memory_critical")
                end
                
                if health_checks.cpu_usage > 95 then
                    status = "unhealthy"
                    table.insert(issues, "cpu_critical")
                end
                
                if health_checks.disk_space > 98 then
                    status = "unhealthy"
                    table.insert(issues, "disk_full")
                end
                
                local cjson = require "cjson"
                local response = {
                    status = status,
                    checks = health_checks,
                    issues = issues,
                    timestamp = ngx.time()
                }
                
                if status == "unhealthy" then
                    ngx.status = 503
                else
                    ngx.status = 200
                end
                
                ngx.header.content_type = "application/json"
                ngx.say(cjson.encode(response))
            }
        }
        
        # Readiness probe endpoint
        location /health/ready {
            access_log off;
            
            content_by_lua_block {
                local http = require "resty.http"
                local cjson = require "cjson"
                local httpc = http.new()
                
                -- Vérifier les dépendances externes
                local dependencies = {
                    {name = "database", url = "http://postgres-service:5432", timeout = 2000},
                    {name = "cache", url = "http://redis-service:6379", timeout = 1000},
                    {name = "message_queue", url = "http://rabbitmq-service:15672", timeout = 1000}
                }
                
                local status = "ready"
                local dep_status = {}
                
                for _, dep in ipairs(dependencies) do
                    local res, err = httpc:request_uri(dep.url, {
                        method = "GET",
                        timeout = dep.timeout
                    })
                    
                    if not res or res.status >= 400 then
                        status = "not_ready"
                        dep_status[dep.name] = {status = "down", error = err or "HTTP " .. (res and res.status or "timeout")}
                    else
                        dep_status[dep.name] = {status = "up"}
                    end
                end
                
                local response = {
                    status = status,
                    dependencies = dep_status,
                    timestamp = ngx.time()
                }
                
                if status == "not_ready" then
                    ngx.status = 503
                else
                    ngx.status = 200
                end
                
                ngx.header.content_type = "application/json"
                ngx.say(cjson.encode(response))
            }
        }
        
        # Metrics endpoint pour Prometheus
        location /metrics {
            access_log off;
            
            content_by_lua_block {
                -- Métriques Prometheus format
                local metrics = {
                    '# HELP product_service_requests_total Total number of requests',
                    '# TYPE product_service_requests_total counter',
                    'product_service_requests_total{method="GET",status="200"} ' .. math.random(1000, 5000),
                    'product_service_requests_total{method="POST",status="200"} ' .. math.random(100, 500),
                    'product_service_requests_total{method="GET",status="404"} ' .. math.random(10, 50),
                    'product_service_requests_total{method="GET",status="500"} ' .. math.random(0, 10),
                    
                    '# HELP product_service_request_duration_seconds Request duration',
                    '# TYPE product_service_request_duration_seconds histogram',
                    'product_service_request_duration_seconds_bucket{le="0.1"} ' .. math.random(500, 1000),
                    'product_service_request_duration_seconds_bucket{le="0.5"} ' .. math.random(800, 1500),
                    'product_service_request_duration_seconds_bucket{le="1.0"} ' .. math.random(900, 1800),
                    'product_service_request_duration_seconds_bucket{le="2.0"} ' .. math.random(950, 1900),
                    'product_service_request_duration_seconds_bucket{le="+Inf"} ' .. math.random(1000, 2000),
                    
                    '# HELP product_service_active_connections Current active connections',
                    '# TYPE product_service_active_connections gauge',
                    'product_service_active_connections ' .. math.random(10, 100),
                    
                    '# HELP product_service_database_connections Database connection pool',
                    '# TYPE product_service_database_connections gauge',
                    'product_service_database_connections{state="active"} ' .. math.random(5, 20),
                    'product_service_database_connections{state="idle"} ' .. math.random(5, 30),
                    
                    '# HELP product_service_cache_hits_total Cache hits',
                    '# TYPE product_service_cache_hits_total counter',
                    'product_service_cache_hits_total ' .. math.random(500, 2000),
                    
                    '# HELP product_service_cache_misses_total Cache misses',
                    '# TYPE product_service_cache_misses_total counter',
                    'product_service_cache_misses_total ' .. math.random(50, 200),
                    
                    '# HELP product_inventory_count Current inventory count',
                    '# TYPE product_inventory_count gauge',
                    'product_inventory_count{product="laptop"} ' .. math.random(10, 100),
                    'product_inventory_count{product="phone"} ' .. math.random(20, 200),
                    'product_inventory_count{product="tablet"} ' .. math.random(5, 50)
                }
                
                ngx.header.content_type = "text/plain"
                for _, metric in ipairs(metrics) do
                    ngx.say(metric)
                end
            }
        }
        
        # Deep health check endpoint
        location /health/deep {
            access_log off;
            
            content_by_lua_block {
                local checks = {}
                
                -- Test mémoire
                local memory_usage = math.random(20, 80)
                checks.memory = {
                    status = memory_usage < 90 and "ok" or "critical",
                    usage_percent = memory_usage,
                    threshold = 90
                }
                
                -- Test CPU
                local cpu_usage = math.random(10, 90)
                checks.cpu = {
                    status = cpu_usage < 80 and "ok" or "warning",
                    usage_percent = cpu_usage,
                    threshold = 80
                }
                
                -- Test disque
                local disk_usage = math.random(30, 95)
                checks.disk = {
                    status = disk_usage < 85 and "ok" or "critical",
                    usage_percent = disk_usage,
                    threshold = 85
                }
                
                -- Test connectivité base de données
                checks.database = {
                    status = "ok",
                    response_time_ms = math.random(5, 50),
                    active_connections = math.random(2, 10)
                }
                
                -- Test cache
                checks.cache = {
                    status = "ok",
                    hit_rate_percent = math.random(70, 95),
                    response_time_ms = math.random(1, 5)
                }
                
                local overall_status = "healthy"
                for _, check in pairs(checks) do
                    if check.status == "critical" then
                        overall_status = "unhealthy"
                        break
                    elseif check.status == "warning" and overall_status == "healthy" then
                        overall_status = "degraded"
                    end
                end
                
                local cjson = require "cjson"
                local response = {
                    overall_status = overall_status,
                    checks = checks,
                    timestamp = ngx.time(),
                    service = "product-service",
                    version = "v2.1.0"
                }
                
                if overall_status == "unhealthy" then
                    ngx.status = 503
                elseif overall_status == "degraded" then
                    ngx.status = 200
                    ngx.header["X-Health-Status"] = "degraded"
                else
                    ngx.status = 200
                end
                
                ngx.header.content_type = "application/json"
                ngx.say(cjson.encode(response))
            }
        }
    }

---
# Service avec annotations pour monitoring
apiVersion: v1
kind: Service
metadata:
  name: product-service-monitored
  namespace: ecommerce
  labels:
    app: product-service
    version: monitored
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '8080'
    prometheus.io/path: '/metrics'
spec:
  selector:
    app: product-service
    version: monitored
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
    - name: metrics
      protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
```

## Étape 3 : Configuration ServiceMonitor pour Prometheus

### 3.1 ServiceMonitors pour collecte automatique

```yaml
# service-monitors.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-services
  namespace: monitoring
  labels:
    app: ecommerce
    release: monitoring
spec:
  selector:
    matchLabels:
      app: product-service
  namespaceSelector:
    matchNames:
      - ecommerce
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
      honorLabels: true
      relabelings:
        - sourceLabels: [__meta_kubernetes_service_name]
          targetLabel: service
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod

---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-health-checks
  namespace: monitoring
  labels:
    app: ecommerce-health
    release: monitoring
spec:
  selector:
    matchLabels:
      monitor: health-checks
  namespaceSelector:
    matchNames:
      - ecommerce
  endpoints:
    - port: metrics
      interval: 30s
      path: /health/deep
      honorLabels: true
      scrapeTimeout: 10s
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'health_check_.*'
          targetLabel: __name__
          replacement: 'ecommerce_${1}'

---
# PodMonitor pour monitoring direct des pods
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: ecommerce-pods
  namespace: monitoring
  labels:
    app: ecommerce-pods
    release: monitoring
spec:
  selector:
    matchLabels:
      app: product-service
  namespaceSelector:
    matchNames:
      - ecommerce
  podMetricsEndpoints:
    - port: metrics
      interval: 15s
      path: /metrics
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
        - sourceLabels: [__meta_kubernetes_pod_label_version]
          targetLabel: version
        - sourceLabels: [__meta_kubernetes_pod_node_name]
          targetLabel: node
```

## Étape 4 : Règles d'alerte PrometheusRule

### 4.1 Alertes spécifiques e-commerce

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ecommerce-alerts
  namespace: monitoring
  labels:
    app: ecommerce
    release: monitoring
spec:
  groups:
    - name: ecommerce.health
      interval: 15s
      rules:
        # Service Health Alerts
        - alert: ServiceDown
          expr: up{job="ecommerce-services"} == 0
          for: 30s
          labels:
            severity: critical
            service: '{{ $labels.service }}'
            team: ecommerce
          annotations:
            summary: 'Service {{ $labels.service }} is down'
            description: 'Service {{ $labels.service }} in namespace {{ $labels.namespace }} has been down for more than 30 seconds.'
            runbook_url: 'https://runbooks.ecommerce.com/service-down'
            dashboard_url: 'https://grafana.ecommerce.com/d/service-health'

        - alert: HighErrorRate
          expr: |
            (
              rate(product_service_requests_total{status=~"5.."}[5m]) /
              rate(product_service_requests_total[5m])
            ) * 100 > 5
          for: 2m
          labels:
            severity: warning
            service: '{{ $labels.service }}'
            team: ecommerce
          annotations:
            summary: 'High error rate detected'
            description: 'Error rate is {{ $value | humanizePercentage }} for service {{ $labels.service }}'
            runbook_url: 'https://runbooks.ecommerce.com/high-error-rate'

        - alert: HighResponseTime
          expr: |
            histogram_quantile(0.95, 
              rate(product_service_request_duration_seconds_bucket[5m])
            ) > 0.5
          for: 3m
          labels:
            severity: warning
            service: '{{ $labels.service }}'
            team: ecommerce
          annotations:
            summary: 'High response time detected'
            description: '95th percentile response time is {{ $value }}s for service {{ $labels.service }}'
            runbook_url: 'https://runbooks.ecommerce.com/high-latency'

        - alert: DatabaseConnectionsHigh
          expr: product_service_database_connections{state="active"} > 15
          for: 5m
          labels:
            severity: warning
            service: database
            team: ecommerce
          annotations:
            summary: 'High database connections'
            description: 'Active database connections ({{ $value }}) are above normal threshold'
            runbook_url: 'https://runbooks.ecommerce.com/db-connections'

        - alert: LowInventory
          expr: product_inventory_count < 10
          for: 1m
          labels:
            severity: warning
            team: inventory
            product: '{{ $labels.product }}'
          annotations:
            summary: 'Low inventory alert'
            description: 'Product {{ $labels.product }} has low inventory: {{ $value }} units remaining'
            runbook_url: 'https://runbooks.ecommerce.com/low-inventory'

        - alert: CacheHitRateLow
          expr: |
            (
              rate(product_service_cache_hits_total[5m]) /
              (rate(product_service_cache_hits_total[5m]) + rate(product_service_cache_misses_total[5m]))
            ) * 100 < 70
          for: 10m
          labels:
            severity: warning
            service: cache
            team: ecommerce
          annotations:
            summary: 'Low cache hit rate'
            description: 'Cache hit rate is {{ $value | humanizePercentage }}, below 70% threshold'
            runbook_url: 'https://runbooks.ecommerce.com/cache-performance'

    - name: ecommerce.sla
      interval: 30s
      rules:
        # SLA/SLO Monitoring
        - alert: SLAViolation
          expr: |
            (
              (
                rate(product_service_requests_total{status=~"2.."}[5m]) /
                rate(product_service_requests_total[5m])
              ) * 100
            ) < 99.9
          for: 5m
          labels:
            severity: critical
            sla: availability
            team: sre
          annotations:
            summary: 'SLA violation - Availability below 99.9%'
            description: 'Current availability is {{ $value | humanizePercentage }}'
            runbook_url: 'https://runbooks.ecommerce.com/sla-violation'

        - alert: SLOBudgetExhausted
          expr: |
            (1 - (
              rate(product_service_requests_total{status=~"2.."}[30d]) /
              rate(product_service_requests_total[30d])
            )) * 100 > 0.1
          for: 1m
          labels:
            severity: warning
            slo: error_budget
            team: sre
          annotations:
            summary: 'SLO error budget exhausted'
            description: 'Monthly error budget has been exceeded'
            runbook_url: 'https://runbooks.ecommerce.com/error-budget'

    - name: ecommerce.kubernetes
      interval: 30s
      rules:
        # Kubernetes Health
        - alert: PodCrashLooping
          expr: rate(kube_pod_container_status_restarts_total[10m]) * 60 * 10 > 3
          for: 5m
          labels:
            severity: warning
            team: platform
          annotations:
            summary: 'Pod is crash looping'
            description: 'Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} is crash looping'
            runbook_url: 'https://runbooks.ecommerce.com/pod-crash-loop'

        - alert: PodMemoryUsageHigh
          expr: |
            (
              container_memory_working_set_bytes{pod=~"product-service-.*"} /
              container_spec_memory_limit_bytes{pod=~"product-service-.*"}
            ) * 100 > 85
          for: 10m
          labels:
            severity: warning
            team: ecommerce
          annotations:
            summary: 'High memory usage'
            description: 'Pod {{ $labels.pod }} memory usage is {{ $value | humanizePercentage }}'
            runbook_url: 'https://runbooks.ecommerce.com/high-memory'

        - alert: PodCPUThrottling
          expr: |
            rate(container_cpu_cfs_throttled_periods_total[5m]) /
            rate(container_cpu_cfs_periods_total[5m]) > 0.25
          for: 5m
          labels:
            severity: warning
            team: platform
          annotations:
            summary: 'High CPU throttling'
            description: 'Pod {{ $labels.pod }} is being CPU throttled {{ $value | humanizePercentage }} of the time'
            runbook_url: 'https://runbooks.ecommerce.com/cpu-throttling'
```

## Étape 5 : Dashboard Grafana personnalisé

### 5.1 Dashboard E-commerce complet

```json
{
  "dashboard": {
    "id": null,
    "title": "E-commerce Application Health Dashboard",
    "tags": ["ecommerce", "health", "monitoring"],
    "timezone": "browser",
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "panels": [
      {
        "id": 1,
        "title": "Service Health Status",
        "type": "stat",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "up{job=\"ecommerce-services\"}",
            "legendFormat": "{{ service }}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {"type": "value", "value": "0", "text": "Down"},
              {"type": "value", "value": "1", "text": "Up"}
            ],
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "green", "value": 1}
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Request Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "rate(product_service_requests_total[5m])",
            "legendFormat": "{{ method }} {{ status }}"
          }
        ],
        "yAxes": [{"label": "Requests/sec", "min": 0}]
      },
      {
        "id": 3,
        "title": "Response Time Percentiles",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(product_service_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, rate(product_service_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(product_service_request_duration_seconds_bucket[5m]))",
            "legendFormat": "99th percentile"
          }
        ],
        "yAxes": [{"label": "Response Time (s)", "min": 0}]
      },
      {
        "id": 4,
        "title": "Error Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "rate(product_service_requests_total{status=~\"4..\"}[5m])",
            "legendFormat": "4xx Errors"
          },
          {
            "expr": "rate(product_service_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx Errors"
          }
        ],
        "yAxes": [{"label": "Errors/sec", "min": 0}]
      },
      {
        "id": 5,
        "title": "Database Connections",
        "type": "graph",
        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 16},
        "targets": [
          {
            "expr": "product_service_database_connections{state=\"active\"}",
            "legendFormat": "Active"
          },
          {
            "expr": "product_service_database_connections{state=\"idle\"}",
            "legendFormat": "Idle"
          }
        ]
      },
      {
        "id": 6,
        "title": "Cache Performance",
        "type": "graph",
        "gridPos": {"h": 8, "w": 8, "x": 8, "y": 16},
        "targets": [
          {
            "expr": "rate(product_service_cache_hits_total[5m])",
            "legendFormat": "Cache Hits"
          },
          {
            "expr": "rate(product_service_cache_misses_total[5m])",
            "legendFormat": "Cache Misses"
          }
        ]
      },
      {
        "id": 7,
        "title": "Inventory Levels",
        "type": "graph",
        "gridPos": {"h": 8, "w": 8, "x": 16, "y": 16},
        "targets": [
          {
            "expr": "product_inventory_count",
            "legendFormat": "{{ product }}"
          }
        ],
        "alert": {
          "conditions": [
            {
              "query": {"params": ["A", "5m", "now"]},
              "reducer": {"params": [], "type": "last"},
              "evaluator": {"params": [10], "type": "lt"}
            }
          ],
          "executionErrorState": "alerting",
          "for": "5m",
          "frequency": "10s",
          "handler": 1,
          "name": "Low Inventory Alert",
          "noDataState": "no_data",
          "notifications": []
        }
      }
    ]
  }
}
```

## Étape 6 : Tests de santé et validation

### 6.1 Scripts de test complet

```bash
# health-check-validation.sh
#!/bin/bash

echo "🏥 Validation complète du monitoring de santé"

NAMESPACE="ecommerce"
SERVICE="product-service-monitored"

# Test 1: Vérifier les endpoints de santé
echo "=== Test des endpoints de santé ==="

# Startup probe
echo "Test Startup probe..."
kubectl exec -n $NAMESPACE deployment/$SERVICE -- curl -s http://localhost:8080/startup | jq

# Liveness probe
echo "Test Liveness probe..."
kubectl exec -n $NAMESPACE deployment/$SERVICE -- curl -s http://localhost:8080/health/live | jq

# Readiness probe
echo "Test Readiness probe..."
kubectl exec -n $NAMESPACE deployment/$SERVICE -- curl -s http://localhost:8080/health/ready | jq

# Deep health check
echo "Test Deep health check..."
kubectl exec -n $NAMESPACE deployment/$SERVICE -- curl -s http://localhost:8080/health/deep | jq

# Test 2: Vérifier les métriques Prometheus
echo "=== Test des métriques Prometheus ==="
kubectl exec -n $NAMESPACE deployment/$SERVICE -- curl -s http://localhost:8080/metrics | head -20

# Test 3: Vérifier la collecte par Prometheus
echo "=== Test de collecte Prometheus ==="
kubectl port-forward -n monitoring svc/monitoring-prometheus 9090:9090 &
PF_PID=$!
sleep 5

# Vérifier que les targets sont UP
curl -s "http://localhost:9090/api/v1/targets" | jq '.data.activeTargets[] | select(.labels.job=="ecommerce-services") | {health: .health, labels: .labels}'

# Test des requêtes métriques
echo "Test des requêtes de métriques..."
curl -s "http://localhost:9090/api/v1/query?query=up{job=\"ecommerce-services\"}" | jq '.data.result[]'

curl -s "http://localhost:9090/api/v1/query?query=rate(product_service_requests_total[5m])" | jq '.data.result[]'

kill $PF_PID

# Test 4: Simulation de panne
echo "=== Test de simulation de panne ==="

# Créer une panne temporaire
kubectl patch deployment $SERVICE -n $NAMESPACE -p '{"spec":{"template":{"spec":{"containers":[{"name":"product-service","livenessProbe":{"httpGet":{"path":"/nonexistent"}}}]}}}}'

echo "Attendre la détection de la panne..."
sleep 60

# Vérifier les alertes
echo "Vérifier les alertes générées..."
kubectl port-forward -n monitoring svc/monitoring-alertmanager 9093:9093 &
AM_PID=$!
sleep 5

curl -s "http://localhost:9093/api/v1/alerts" | jq '.data[] | select(.labels.alertname=="ServiceDown")'

kill $AM_PID

# Restaurer le service
echo "Restauration du service..."
kubectl rollout undo deployment/$SERVICE -n $NAMESPACE
kubectl rollout status deployment/$SERVICE -n $NAMESPACE

# Test 5: Vérifier Grafana
echo "=== Test Grafana Dashboard ==="
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 &
GRAFANA_PID=$!
sleep 5

# Test de connexion Grafana (nécessite les credentials)
echo "Grafana accessible sur http://localhost:3000"
echo "Login: admin / Password: admin123"

kill $GRAFANA_PID

echo "✅ Tests de validation terminés"
```

### 6.2 Test de charge avec monitoring

```bash
# load-test-with-monitoring.sh
#!/bin/bash

echo "🚀 Test de charge avec monitoring en temps réel"

NAMESPACE="ecommerce"
SERVICE="product-service-monitored"

# Démarrer le monitoring en temps réel
echo "=== Démarrage du monitoring temps réel ==="

# Port-forward pour Grafana
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 &
GRAFANA_PID=$!

# Port-forward pour Prometheus
kubectl port-forward -n monitoring svc/monitoring-prometheus 9090:9090 &
PROM_PID=$!

sleep 10

echo "📊 Dashboards disponibles:"
echo "- Grafana: http://localhost:3000"
echo "- Prometheus: http://localhost:9090"

# Démarrer la génération de charge
echo "=== Génération de charge progressive ==="

# Phase 1: Charge légère
echo "Phase 1: Charge légère (10 RPS)"
kubectl run load-test-light --image=busybox:1.35 --rm -i --restart=Never -- /bin/sh -c "
for i in \$(seq 1 600); do
  wget -q -O- http://$SERVICE.$NAMESPACE/products >/dev/null 2>&1
  sleep 0.1
done
echo 'Phase 1 terminée'
" &

sleep 60

# Phase 2: Charge modérée
echo "Phase 2: Charge modérée (50 RPS)"
kubectl run load-test-medium --image=busybox:1.35 --rm -i --restart=Never -- /bin/sh -c "
for i in \$(seq 1 300); do
  for j in \$(seq 1 5); do
    wget -q -O- http://$SERVICE.$NAMESPACE/products >/dev/null 2>&1 &
  done
  sleep 0.1
done
wait
echo 'Phase 2 terminée'
" &

sleep 60

# Phase 3: Charge élevée
echo "Phase 3: Charge élevée (100 RPS)"
kubectl run load-test-high --image=busybox:1.35 --rm -i --restart=Never -- /bin/sh -c "
for i in \$(seq 1 180); do
  for j in \$(seq 1 10); do
    wget -q -O- http://$SERVICE.$NAMESPACE/products >/dev/null 2>&1 &
  done
  sleep 0.1
done
wait
echo 'Phase 3 terminée'
" &

# Monitoring pendant le test
echo "=== Monitoring en temps réel ==="

for i in {1..10}; do
    echo "--- Minute $i ---"

    # Métriques de base
    echo "Pods actifs:"
    kubectl get pods -n $NAMESPACE -l app=product-service --no-headers | wc -l

    echo "CPU/Mémoire:"
    kubectl top pods -n $NAMESPACE -l app=product-service

    # Métriques Prometheus via API
    echo "Taux de requêtes (dernière minute):"
    RATE=$(curl -s "http://localhost:9090/api/v1/query?query=rate(product_service_requests_total[1m])" | jq -r '.data.result[0].value[1] // "0"')
    echo "Requêtes/sec: $RATE"

    echo "Temps de réponse P95:"
    P95=$(curl -s "http://localhost:9090/api/v1/query?query=histogram_quantile(0.95, rate(product_service_request_duration_seconds_bucket[1m]))" | jq -r '.data.result[0].value[1] // "0"')
    echo "P95 latency: ${P95}s"

    echo "Taux d'erreur:"
    ERROR_RATE=$(curl -s "http://localhost:9090/api/v1/query?query=rate(product_service_requests_total{status=~\"5..\"}[1m])" | jq -r '.data.result[0].value[1] // "0"')
    echo "Erreurs/sec: $ERROR_RATE"

    sleep 60
done

# Nettoyer
wait  # Attendre la fin des tests de charge
kill $GRAFANA_PID $PROM_PID

echo "🏁 Test de charge terminé"
echo "📈 Consultez les dashboards pour l'analyse détaillée"
```

## Points clés de la solution

### 🎯 Health Checks multi-niveaux

- **Startup probe**: Gère les démarrages lents
- **Liveness probe**: Redémarre automatiquement les conteneurs défaillants
- **Readiness probe**: Retire du load balancing les pods non prêts
- **Deep health check**: Vérifications complètes des dépendances

### 📊 Monitoring complet

- **Métriques business**: Inventaire, commandes, cache hit ratio
- **Métriques système**: CPU, mémoire, connexions DB
- **Métriques SLA/SLO**: Availability, error budget, response time
- **Alerting intelligent**: Seuils adaptatifs et escalade

### 🔧 Observabilité

- **Logs structurés**: Format JSON avec correlation IDs
- **Distributed tracing**: Suivi des requêtes cross-services
- **Custom dashboards**: Vues métier et technique
- **Runbooks intégrés**: Liens vers procédures de résolution

Cette correction fournit une solution complète de monitoring et d'observabilité pour une application e-commerce production-ready.
