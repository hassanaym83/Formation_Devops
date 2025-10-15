# LAB 7 - CORRECTIONS : Monitoring et Métriques

## Solution complète

### 1. Configuration Prometheus complète

**Fichier `monitoring/prometheus.yml`** :

```yaml
# Configuration Prometheus pour monitoring complet
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'dev-cluster'
    region: 'eu-west-1'

# Configuration des règles d'alerting
rule_files:
  - 'alerts/*.yml'

# Configuration Alertmanager
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
      timeout: 10s

# Jobs de scraping
scrape_configs:
  # JOB 1 : Prometheus lui-même
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 5s

  # JOB 2 : Application React (Node Exporter)
  - job_name: 'react-app'
    static_configs:
      - targets: ['localhost:3000']
    scrape_interval: 10s
    metrics_path: '/metrics'

  # JOB 3 : GitLab Runner
  - job_name: 'gitlab-runner'
    static_configs:
      - targets: ['localhost:9252']
    scrape_interval: 30s

  # JOB 4 : Docker containers (cAdvisor)
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['localhost:8080']
    scrape_interval: 15s

  # JOB 5 : Node Exporter
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
    scrape_interval: 15s

  # JOB 6 : Application metrics endpoint
  - job_name: 'app-metrics'
    static_configs:
      - targets: ['localhost:9464']
    scrape_interval: 10s
    metrics_path: '/metrics'
```

### 2. Règles d'alerting avancées

**Fichier `monitoring/alerts/app-alerts.yml`** :

```yaml
groups:
  - name: app.rules
    rules:
      # RÈGLE 1 : Application Down
      - alert: ApplicationDown
        expr: up{job="react-app"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: 'Application React indisponible'
          description: "L'application {{ $labels.instance }} est down depuis {{ $value }} minutes"

      # RÈGLE 2 : High Memory Usage
      - alert: HighMemoryUsage
        expr: (process_resident_memory_bytes / 1024 / 1024) > 512
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: 'Utilisation mémoire élevée'
          description: "L'application utilise {{ $value }}MB de mémoire"

      # RÈGLE 3 : High CPU Usage
      - alert: HighCPUUsage
        expr: rate(process_cpu_seconds_total[5m]) * 100 > 75
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: 'Utilisation CPU élevée'
          description: "L'application utilise {{ $value }}% de CPU"

      # RÈGLE 4 : High Error Rate
      - alert: HighErrorRate
        expr: rate(react_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Taux d'erreur élevé"
          description: "Taux d'erreur: {{ $value }} erreurs/seconde"

      # RÈGLE 5 : Slow Response Time
      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, rate(react_page_load_duration_seconds_bucket[5m])) > 2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: 'Temps de réponse lent'
          description: '95e percentile: {{ $value }} secondes'

  - name: pipeline.rules
    rules:
      # RÈGLE 6 : Pipeline Failure Rate
      - alert: HighPipelineFailureRate
        expr: |
          (
            rate(gitlab_pipeline_builds_failed_total[1h]) /
            rate(gitlab_pipeline_builds_total[1h])
          ) * 100 > 20
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Taux d'échec pipeline élevé"
          description: '{{ $value }}% des pipelines échouent'

      # RÈGLE 7 : Long Pipeline Duration
      - alert: LongPipelineDuration
        expr: gitlab_pipeline_duration_seconds > 900
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: 'Pipeline trop long'
          description: 'Pipeline durée: {{ $value }} secondes'

  - name: infrastructure.rules
    rules:
      # RÈGLE 8 : High Disk Usage
      - alert: HighDiskUsage
        expr: |
          (
            (node_filesystem_size_bytes{fstype!="tmpfs"} - node_filesystem_free_bytes{fstype!="tmpfs"}) /
            node_filesystem_size_bytes{fstype!="tmpfs"}
          ) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: 'Espace disque faible'
          description: 'Disque {{ $labels.device }} utilisé à {{ $value }}%'

      # RÈGLE 9 : Container Restart
      - alert: ContainerRestart
        expr: increase(container_start_time_seconds[5m]) > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: 'Container redémarré'
          description: 'Container {{ $labels.name }} a redémarré'
```

### 3. Docker Compose monitoring stack

**Fichier `monitoring/docker-compose.monitoring.yml`** :

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts:/etc/prometheus/alerts
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    networks:
      - monitoring
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - '3001:3000'
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/var/lib/grafana/dashboards
      - ./grafana/provisioning:/etc/grafana/provisioning
    networks:
      - monitoring
    restart: unless-stopped
    depends_on:
      - prometheus

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    ports:
      - '9093:9093'
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    networks:
      - monitoring
    restart: unless-stopped

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - '8080:8080'
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true
    devices:
      - /dev/kmsg:/dev/kmsg
    networks:
      - monitoring
    restart: unless-stopped

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - '9100:9100'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:

networks:
  monitoring:
    driver: bridge
```

### 4. Application React instrumentée

**Fichier `src/App.js` modifié** :

```javascript
import React, {useState, useEffect} from 'react';
import './App.css';

// Métriques côté client (simulées)
const metrics = {
  pageViews: 0,
  errors: 0,
  loadTime: 0,
  activeUsers: 1
};

function App() {
  const [loadTime, setLoadTime] = useState(0);
  const [errorCount, setErrorCount] = useState(0);
  const [userCount, setUserCount] = useState(1);
  const [metricsStatus, setMetricsStatus] = useState('unknown');

  useEffect(() => {
    // Mesurer le temps de chargement
    const startTime = performance.now();

    // Simuler le chargement
    setTimeout(() => {
      const endTime = performance.now();
      const duration = (endTime - startTime) / 1000;
      setLoadTime(duration);

      // Envoyer les métriques au serveur
      sendMetricsToServer({
        type: 'page_view',
        page: 'home',
        duration: duration,
        timestamp: new Date().toISOString()
      });
    }, Math.random() * 1000);

    // Vérifier la disponibilité du serveur de métriques
    checkMetricsServer();

    // Simulation d'erreurs aléatoires
    const errorInterval = setInterval(() => {
      if (Math.random() > 0.95) {
        // 5% de chance d'erreur
        setErrorCount((prev) => prev + 1);
        sendMetricsToServer({
          type: 'error',
          error_type: 'network',
          component: 'App',
          timestamp: new Date().toISOString()
        });
      }
    }, 5000);

    return () => clearInterval(errorInterval);
  }, [userCount]);

  const checkMetricsServer = async () => {
    try {
      const response = await fetch('http://localhost:9464/health');
      if (response.ok) {
        setMetricsStatus('connected');
      } else {
        setMetricsStatus('error');
      }
    } catch (error) {
      setMetricsStatus('disconnected');
    }
  };

  const sendMetricsToServer = async (metric) => {
    try {
      await fetch('http://localhost:9464/api/metrics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(metric)
      });
    } catch (error) {
      console.warn("Impossible d'envoyer les métriques:", error);
    }
  };

  // Fonction pour simuler l'activité utilisateur
  const simulateUserActivity = () => {
    const newUserCount = userCount + Math.floor(Math.random() * 3) + 1;
    setUserCount(newUserCount);
    sendMetricsToServer({
      type: 'user_activity',
      user_count: newUserCount,
      timestamp: new Date().toISOString()
    });
  };

  const triggerError = () => {
    setErrorCount((prev) => prev + 1);
    sendMetricsToServer({
      type: 'error',
      error_type: 'manual',
      component: 'App',
      severity: 'warning',
      timestamp: new Date().toISOString()
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected':
        return '#27ae60';
      case 'disconnected':
        return '#e74c3c';
      case 'error':
        return '#f39c12';
      default:
        return '#95a5a6';
    }
  };

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>DevOps React App - Monitoring Lab</h1>

        <div
          className='metrics-status'
          style={{
            backgroundColor: getStatusColor(metricsStatus),
            padding: '10px',
            borderRadius: '5px',
            marginBottom: '20px'
          }}
        >
          <strong>Metrics Server Status:</strong> {metricsStatus}
        </div>

        <div className='metrics-dashboard'>
          <div className='metric-card'>
            <h3>Page Load Time</h3>
            <p>{loadTime.toFixed(3)} seconds</p>
            <small>95th percentile target: &lt; 2s</small>
          </div>

          <div className='metric-card'>
            <h3>Error Count</h3>
            <p>{errorCount}</p>
            <small>Error rate target: &lt; 1%</small>
          </div>

          <div className='metric-card'>
            <h3>Active Users</h3>
            <p>{userCount}</p>
            <small>Concurrent sessions</small>
          </div>

          <div className='metric-card'>
            <h3>Health Score</h3>
            <p>
              {errorCount === 0 && loadTime < 2
                ? '100%'
                : errorCount === 0
                ? '85%'
                : loadTime < 2
                ? '70%'
                : '50%'}
            </p>
            <small>Overall application health</small>
          </div>
        </div>

        <div className='actions'>
          <button onClick={simulateUserActivity}>Simulate User Activity</button>

          <button onClick={triggerError}>Trigger Error</button>

          <button onClick={checkMetricsServer}>Check Metrics Server</button>
        </div>

        <div className='monitoring-info'>
          <h2>Monitoring Stack</h2>
          <div className='monitoring-links'>
            <div className='monitoring-service'>
              <strong>Prometheus:</strong>
              <a
                href='http://localhost:9090'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:9090
              </a>
              <p>Collecte et stockage des métriques</p>
            </div>

            <div className='monitoring-service'>
              <strong>Grafana:</strong>
              <a
                href='http://localhost:3001'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:3001
              </a>
              <p>Dashboards et visualisation (admin/admin123)</p>
            </div>

            <div className='monitoring-service'>
              <strong>AlertManager:</strong>
              <a
                href='http://localhost:9093'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:9093
              </a>
              <p>Gestion des alertes et notifications</p>
            </div>

            <div className='monitoring-service'>
              <strong>cAdvisor:</strong>
              <a
                href='http://localhost:8080'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:8080
              </a>
              <p>Monitoring des containers Docker</p>
            </div>

            <div className='monitoring-service'>
              <strong>App Metrics:</strong>
              <a
                href='http://localhost:9464/metrics'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:9464/metrics
              </a>
              <p>Endpoint Prometheus de l'application</p>
            </div>
          </div>
        </div>

        <div className='sli-slo-info'>
          <h2>SLI/SLO Monitoring</h2>
          <div className='slo-targets'>
            <div className='slo-item'>
              <strong>Availability SLO:</strong> 99.9%
              <br />
              <small>Current: {errorCount === 0 ? '100%' : '99.5%'}</small>
            </div>
            <div className='slo-item'>
              <strong>Latency SLO:</strong> 95% &lt; 2s
              <br />
              <small>Current: {loadTime < 2 ? '✓' : '✗'}</small>
            </div>
            <div className='slo-item'>
              <strong>Error Rate SLO:</strong> &lt; 1%
              <br />
              <small>
                Current: {((errorCount / (userCount * 10)) * 100).toFixed(2)}%
              </small>
            </div>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
```

### 5. Serveur de métriques complet

**Fichier `src/metrics.js`** :

```javascript
const express = require('express');
const promClient = require('prom-client');
const cors = require('cors');

// Créer une app Express pour servir les métriques
const app = express();
const port = 9464;

// Middleware
app.use(cors());
app.use(express.json());

// Créer le registre des métriques
const register = promClient.register;

// Collecter les métriques par défaut (CPU, mémoire, etc.)
promClient.collectDefaultMetrics({register});

// MÉTRIQUES PERSONNALISÉES

// 1. Build Info
const buildInfo = new promClient.Gauge({
  name: 'react_app_build_info',
  help: 'Build information',
  labelNames: ['version', 'commit', 'branch', 'build_date']
});

// 2. Compteur des visites de page
const pageViewsCounter = new promClient.Counter({
  name: 'react_page_views_total',
  help: 'Total number of page views',
  labelNames: ['page', 'user_agent']
});

// 3. Histogramme des temps de chargement
const pageLoadHistogram = new promClient.Histogram({
  name: 'react_page_load_duration_seconds',
  help: 'Page load duration in seconds',
  labelNames: ['page'],
  buckets: [0.1, 0.5, 1, 2, 5, 10]
});

// 4. Gauge pour utilisateurs actifs
const activeUsersGauge = new promClient.Gauge({
  name: 'react_active_users',
  help: 'Number of active users',
  labelNames: ['session_type']
});

// 5. Compteur d'erreurs
const errorCounter = new promClient.Counter({
  name: 'react_errors_total',
  help: 'Total number of errors',
  labelNames: ['error_type', 'component', 'severity']
});

// 6. Feature Flags
const featureFlagsGauge = new promClient.Gauge({
  name: 'react_app_feature_flags',
  help: 'Feature flags status',
  labelNames: ['feature_name', 'enabled']
});

// 7. API Response Times
const apiResponseTime = new promClient.Histogram({
  name: 'react_app_api_duration_seconds',
  help: 'API response time in seconds',
  labelNames: ['method', 'endpoint', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});

// 8. Business Metrics
const businessMetricsGauge = new promClient.Gauge({
  name: 'react_app_business_metrics',
  help: 'Business metrics',
  labelNames: ['metric_name', 'metric_type']
});

// Initialiser les métriques statiques
buildInfo.set(
  {
    version: process.env.npm_package_version || '1.0.0',
    commit: process.env.CI_COMMIT_SHA || 'unknown',
    branch: process.env.CI_COMMIT_REF_NAME || 'local',
    build_date: new Date().toISOString()
  },
  1
);

// Initialiser les feature flags
featureFlagsGauge.set({feature_name: 'monitoring', enabled: 'true'}, 1);
featureFlagsGauge.set({feature_name: 'dark_mode', enabled: 'false'}, 0);
featureFlagsGauge.set({feature_name: 'analytics', enabled: 'true'}, 1);

// Middleware pour mesurer les temps de réponse
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    apiResponseTime.observe(
      {
        method: req.method,
        endpoint: req.route ? req.route.path : req.path,
        status: res.statusCode
      },
      duration
    );
  });

  next();
});

// Routes

// Endpoint de santé
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: process.env.npm_package_version || '1.0.0'
  });
});

// Endpoint des métriques Prometheus
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    const metrics = await register.metrics();
    res.end(metrics);
  } catch (error) {
    console.error('Erreur lors de la collecte des métriques:', error);
    res.status(500).send('Erreur interne du serveur');
  }
});

// API pour recevoir les métriques côté client
app.post('/api/metrics', (req, res) => {
  try {
    const {type, ...data} = req.body;

    switch (type) {
      case 'page_view':
        pageViewsCounter.inc({
          page: data.page,
          user_agent: req.headers['user-agent'] || 'unknown'
        });

        if (data.duration) {
          pageLoadHistogram.observe({page: data.page}, data.duration);
        }
        break;

      case 'error':
        errorCounter.inc({
          error_type: data.error_type || 'unknown',
          component: data.component || 'unknown',
          severity: data.severity || 'error'
        });
        break;

      case 'user_activity':
        activeUsersGauge.set({session_type: 'web'}, data.user_count);
        break;

      case 'business':
        businessMetricsGauge.set(
          {
            metric_name: data.name,
            metric_type: data.metric_type || 'gauge'
          },
          data.value
        );
        break;

      default:
        console.warn('Type de métrique inconnu:', type);
    }

    res.json({status: 'success', message: 'Métrique enregistrée'});
  } catch (error) {
    console.error("Erreur lors de l'enregistrement de la métrique:", error);
    res.status(400).json({status: 'error', message: error.message});
  }
});

// API pour obtenir les métriques actuelles (JSON)
app.get('/api/metrics/current', async (req, res) => {
  try {
    const metrics = await register.getMetricsAsJSON();
    res.json({
      timestamp: new Date().toISOString(),
      metrics: metrics
    });
  } catch (error) {
    console.error('Erreur lors de la récupération des métriques:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Fonction utilitaire pour enregistrer des métriques API
function recordApiMetric(method, endpoint, duration, status) {
  apiResponseTime.observe({method, endpoint, status}, duration);
}

// Simulation de métriques business
setInterval(() => {
  // Simuler des métriques business
  businessMetricsGauge.set(
    {metric_name: 'revenue', metric_type: 'currency'},
    Math.random() * 1000
  );
  businessMetricsGauge.set(
    {metric_name: 'conversion_rate', metric_type: 'percentage'},
    Math.random() * 10
  );
  businessMetricsGauge.set(
    {metric_name: 'customer_satisfaction', metric_type: 'score'},
    4 + Math.random()
  );
}, 30000);

// Démarrer le serveur des métriques
if (require.main === module) {
  app.listen(port, () => {
    console.log(`Serveur de métriques démarré sur le port ${port}`);
    console.log(`Métriques disponibles sur http://localhost:${port}/metrics`);
    console.log(`Health check sur http://localhost:${port}/health`);
    console.log(`API métriques sur http://localhost:${port}/api/metrics`);
  });
}

module.exports = {app, recordApiMetric};
```

### 6. Configuration Grafana Datasource

**Fichier `monitoring/grafana/provisioning/datasources/prometheus.yml`** :

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
    jsonData:
      httpMethod: POST
      timeInterval: '15s'
      queryTimeout: '60s'
      timeRange: '1h'
```

### 7. Dashboard Application Grafana

**Fichier `monitoring/grafana/dashboards/app-dashboard.json`** :

```json
{
  "dashboard": {
    "id": null,
    "title": "Application React - Monitoring",
    "tags": ["react", "monitoring", "devops"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Application Overview",
        "type": "row",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Page Views per Second",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(react_page_views_total[5m])",
            "legendFormat": "Page Views/sec"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "reqps"
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 1}
      },
      {
        "id": 3,
        "title": "Active Users",
        "type": "gauge",
        "targets": [
          {
            "expr": "react_active_users",
            "legendFormat": "Active Users"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "min": 0,
            "max": 100,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 50},
                {"color": "red", "value": 80}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 6, "y": 1}
      },
      {
        "id": 4,
        "title": "Error Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(react_errors_total[5m])",
            "legendFormat": "Error Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "thresholds"},
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.05},
                {"color": "red", "value": 0.1}
              ]
            }
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 12, "y": 1}
      },
      {
        "id": 5,
        "title": "95th Percentile Response Time",
        "type": "timeseries",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(react_page_load_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(react_page_load_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "s"
          }
        },
        "gridPos": {"h": 8, "w": 6, "x": 18, "y": 1}
      },
      {
        "id": 6,
        "title": "Memory Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "process_resident_memory_bytes / 1024 / 1024",
            "legendFormat": "Memory Usage (MB)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "MB"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 9}
      },
      {
        "id": 7,
        "title": "CPU Usage",
        "type": "timeseries",
        "targets": [
          {
            "expr": "rate(process_cpu_seconds_total[5m]) * 100",
            "legendFormat": "CPU Usage (%)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "color": {"mode": "palette-classic"},
            "unit": "percent"
          }
        },
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 9}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "10s"
  }
}
```

### 8. Configuration AlertManager

**Fichier `monitoring/alertmanager.yml`** :

```yaml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'alertmanager@example.com'
  smtp_auth_password: 'password'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
  routes:
    - match:
        severity: critical
      receiver: critical-alerts
      group_wait: 5s
      repeat_interval: 15m

    - match:
        severity: warning
      receiver: warning-alerts
      group_wait: 30s
      repeat_interval: 1h

receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://localhost:8080/webhook'

  - name: 'critical-alerts'
    email_configs:
      - to: 'devops@example.com'
        subject: 'ALERTE CRITIQUE: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alerte: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          Sévérité: {{ .Labels.severity }}
          Instance: {{ .Labels.instance }}
          Début: {{ .StartsAt }}
          {{ end }}
    webhook_configs:
      - url: 'http://localhost:8080/webhook'
        send_resolved: true

  - name: 'warning-alerts'
    email_configs:
      - to: 'team@example.com'
        subject: 'AVERTISSEMENT: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alerte: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'dev', 'instance']
```

### 9. Pipeline GitLab CI/CD avec monitoring

**Ajout dans `.gitlab-ci.yml`** :

```yaml
# Variables de monitoring
variables:
  METRICS_ENABLED: 'true'
  PROMETHEUS_URL: 'http://prometheus:9090'
  GRAFANA_URL: 'http://grafana:3000'
  MONITORING_STACK: 'docker-compose -f monitoring/docker-compose.monitoring.yml'

stages:
  - validate
  - build
  - test
  - security
  - deploy
  - monitor
  - notify

# Template pour les métriques de pipeline
.pipeline_metrics_template: &pipeline_metrics
  before_script:
    - echo "Début job: $CI_JOB_NAME à $(date)"
    - export JOB_START_TIME=$(date +%s)
  after_script:
    - export JOB_END_TIME=$(date +%s)
    - export JOB_DURATION=$((JOB_END_TIME - JOB_START_TIME))
    - echo "Durée job $CI_JOB_NAME: ${JOB_DURATION}s"
    - |
      if [ "$METRICS_ENABLED" = "true" ]; then
        echo "gitlab_pipeline_job_duration_seconds{job=\"$CI_JOB_NAME\",pipeline=\"$CI_PIPELINE_ID\"} $JOB_DURATION $(date +%s)" | curl -X POST --data-binary @- http://prometheus:9091/metrics/job/gitlab-ci
      fi

# Job de démarrage du monitoring
start_monitoring:
  stage: validate
  image: docker/compose:latest
  services:
    - docker:24.0.5-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  script:
    - echo "Démarrage de la stack de monitoring"
    - cd monitoring
    - docker-compose -f docker-compose.monitoring.yml up -d
    - sleep 30
    - echo "Vérification des services de monitoring"
    - docker-compose -f docker-compose.monitoring.yml ps
  only:
    - main
    - develop

# Job de monitoring des métriques
monitor_application:
  stage: monitor
  image: curlimages/curl:latest
  <<: *pipeline_metrics
  script:
    - echo "=== MONITORING APPLICATION ==="

    # Vérifier la disponibilité des métriques
    - |
      echo "Vérification endpoint métriques"
      for i in {1..5}; do
        if curl -f http://localhost:9464/metrics; then
          echo "Endpoint métriques accessible"
          break
        else
          echo "Tentative $i/5 - Endpoint métriques indisponible"
          sleep 10
        fi
      done

    # Vérifier Prometheus
    - |
      echo "Vérification Prometheus"
      if curl -f "${PROMETHEUS_URL}/-/healthy"; then
        echo "Prometheus accessible"
      else
        echo "Prometheus indisponible"
        exit 1
      fi

    # Collecter les métriques clés
    - |
      echo "Collecte des métriques clés"

      # Métriques de l'application
      app_up=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=up{job=\"react-app\"}" | grep -o '"value":\[[^]]*\]' | grep -o '[0-9.]*' | tail -1 || echo "0")
      error_rate=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=rate(react_errors_total[5m])" | grep -o '"value":\[[^]]*\]' | grep -o '[0-9.]*' | tail -1 || echo "0")

      echo "Application UP: $app_up"
      echo "Error Rate: $error_rate"

      # Vérifier les seuils
      if [ "$app_up" != "1" ]; then
        echo "Application down détectée"
        exit 1
      fi

    - echo "Monitoring terminé"
  dependencies:
    - start_monitoring
  only:
    - main
    - develop

# Job de rapport de performance
performance_report:
  stage: monitor
  image: node:18-alpine
  <<: *pipeline_metrics
  script:
    - echo "=== RAPPORT DE PERFORMANCE ==="
    - apk add --no-cache curl jq

    # Générer un rapport de performance
    - |
      cat > performance-report.json << EOF
      {
        "pipeline_id": "$CI_PIPELINE_ID",
        "commit": "$CI_COMMIT_SHA",
        "branch": "$CI_COMMIT_REF_NAME",
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "metrics": {},
        "slo_compliance": {}
      }
      EOF

    # Collecter les métriques de performance si disponibles
    - |
      if [ "$METRICS_ENABLED" = "true" ] && curl -s "${PROMETHEUS_URL}/-/healthy" > /dev/null; then
        echo "Collecte des métriques de performance"
        
        # Calculer le temps total du pipeline
        pipeline_start=$(date -d "$CI_PIPELINE_CREATED_AT" +%s)
        current_time=$(date +%s)
        total_duration=$((current_time - pipeline_start))
        
        # Mise à jour du rapport
        jq --arg total "$total_duration" \
          '.metrics.total_duration = ($total | tonumber)' \
          performance-report.json > tmp.json && mv tmp.json performance-report.json
        
        echo "Total Duration: ${total_duration}s"
        
        # Vérification SLO
        slo_met="true"
        if [ "$total_duration" -gt 900 ]; then
          echo "Pipeline trop long (> 15min): ${total_duration}s"
          slo_met="false"
        fi
        
        jq --arg slo "$slo_met" \
          '.slo_compliance.pipeline_duration = ($slo == "true")' \
          performance-report.json > tmp.json && mv tmp.json performance-report.json
      fi

    - echo "Rapport de performance généré"
    - cat performance-report.json
  artifacts:
    reports:
      performance: performance-report.json
    paths:
      - performance-report.json
    expire_in: 30 days
  dependencies:
    - start_monitoring
  only:
    - main
    - develop

# Job de nettoyage du monitoring
cleanup_monitoring:
  stage: notify
  image: docker/compose:latest
  services:
    - docker:24.0.5-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  script:
    - echo "Nettoyage de la stack de monitoring"
    - cd monitoring
    - docker-compose -f docker-compose.monitoring.yml down
  when: manual
  only:
    - main
    - develop
```

### 10. Package.json mis à jour

**Fichier `package.json`** :

```json
{
  "name": "devops-react-monitoring",
  "version": "1.0.0",
  "description": "Application React avec monitoring Prometheus",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "metrics": "node src/metrics.js",
    "start:with-metrics": "concurrently \"npm run metrics\" \"npm start\"",
    "monitoring:up": "docker-compose -f monitoring/docker-compose.monitoring.yml up -d",
    "monitoring:down": "docker-compose -f monitoring/docker-compose.monitoring.yml down",
    "monitoring:logs": "docker-compose -f monitoring/docker-compose.monitoring.yml logs -f",
    "monitoring:status": "docker-compose -f monitoring/docker-compose.monitoring.yml ps"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "devDependencies": {
    "prom-client": "^14.2.0",
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "concurrently": "^7.6.0"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

## Guide d'utilisation

### 1. Démarrage de la stack de monitoring

```bash
# Démarrer tous les services de monitoring
npm run monitoring:up

# Vérifier le statut
npm run monitoring:status

# Voir les logs
npm run monitoring:logs
```

### 2. Démarrage de l'application avec métriques

```bash
# Démarrer l'application et le serveur de métriques
npm run start:with-metrics
```

### 3. Accès aux interfaces

- **Application React**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin123)
- **AlertManager**: http://localhost:9093
- **cAdvisor**: http://localhost:8080
- **Métriques App**: http://localhost:9464/metrics

### 4. Tests et validation

```bash
# Tester les métriques
curl http://localhost:9464/health
curl http://localhost:9464/metrics

# Vérifier Prometheus
curl http://localhost:9090/-/healthy

# Tester une alerte
curl -X POST http://localhost:9464/api/metrics \
  -H "Content-Type: application/json" \
  -d '{"type":"error","error_type":"test","component":"manual"}'
```

## Métriques et SLI/SLO

### SLI (Service Level Indicators)

- **Availability**: `up{job="react-app"}`
- **Latency**: `histogram_quantile(0.95, rate(react_page_load_duration_seconds_bucket[5m]))`
- **Error Rate**: `rate(react_errors_total[5m]) / rate(react_page_views_total[5m])`
- **Throughput**: `rate(react_page_views_total[5m])`

### SLO (Service Level Objectives)

- **Availability**: 99.9% uptime
- **Latency**: 95% of requests < 2 seconds
- **Error Rate**: < 1% error rate
- **Pipeline Duration**: < 15 minutes

### Alertes configurées

- Application Down (Critical)
- High Error Rate (Critical)
- Slow Response Time (Warning)
- High Memory/CPU Usage (Warning)
- Pipeline Failure Rate (Critical)
- Long Pipeline Duration (Warning)

Cette solution complète fournit un système de monitoring robuste avec toutes les bonnes pratiques DevOps intégrées.
