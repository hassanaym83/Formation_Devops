# LAB 7 - ÉNONCÉ : Monitoring et Métriques

## 📊 Objectifs pédagogiques

À la fin de ce lab, vous serez capable de :

- ✅ Configurer un système de monitoring complet avec Prometheus et Grafana
- ✅ Créer des métriques applicatives personnalisées
- ✅ Mettre en place des alertes GitLab CI/CD
- ✅ Monitorer les performances des pipelines
- ✅ Analyser les métriques de déploiement et de santé applicative

## 🎯 Contexte du lab

Le monitoring est essentiel dans un environnement DevOps pour :

- **Observabilité** : Comprendre l'état et les performances de vos applications
- **Détection proactive** : Identifier les problèmes avant qu'ils impactent les utilisateurs
- **Optimisation** : Améliorer les performances basées sur des données concrètes
- **Compliance** : Respecter les SLA et les exigences de disponibilité

## 📋 Prérequis

- ✅ LAB 6 terminé (sécurité DevSecOps)
- ✅ Application React déployée avec Docker
- ✅ Accès administrateur à GitLab
- ✅ Connaissances de base en métriques et monitoring

## 🏗️ Architecture de monitoring

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │────│   Prometheus    │────│    Grafana      │
│     React       │    │   (Métriques)   │    │  (Dashboards)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌─────────────────┐    ┌─────────────────┐
         └───────────────│  GitLab CI/CD   │────│   AlertManager  │
                         │   (Pipelines)   │    │    (Alertes)    │
                         └─────────────────┘    └─────────────────┘
```

## 📝 Exercice 1 : Configuration de Prometheus (30 points)

### 1.1 Installation et configuration Prometheus

**Créer le fichier `monitoring/prometheus.yml`** :

```yaml
# Votre tâche : Configurer Prometheus pour monitorer l'application
global:
  # Configurer l'intervalle de scraping global : 15 secondes
  # Configurer l'évaluation des règles : 15 secondes
  # Ajouter des labels externes :
  #   - cluster: 'dev-cluster'
  #   - region: 'eu-west-1'

# Configuration des règles d'alerting
rule_files:
  # Ajouter le chemin vers les règles d'alerting
  # Fichier : "alerts/*.yml"

# Configuration Alertmanager
alerting:
  alertmanagers:
    # Configurer Alertmanager sur localhost:9093
    # Timeout : 10 secondes

# Jobs de scraping
scrape_configs:
  # JOB 1 : Prometheus lui-même
  # - job_name: 'prometheus'
  # - static_configs avec localhost:9090
  # - scrape_interval: 5s

  # JOB 2 : Application React (Node Exporter)
  # - job_name: 'react-app'
  # - static_configs avec localhost:3000
  # - scrape_interval: 10s
  # - metrics_path: '/metrics'

  # JOB 3 : GitLab Runner
  # - job_name: 'gitlab-runner'
  # - static_configs avec localhost:9252
  # - scrape_interval: 30s

  # JOB 4 : Docker containers (cAdvisor)
  # - job_name: 'cadvisor'
  # - static_configs avec localhost:8080
  # - scrape_interval: 15s
```

### 1.2 Configuration des règles d'alerting

**Créer le fichier `monitoring/alerts/app-alerts.yml`** :

```yaml
# Votre tâche : Définir les règles d'alerting
groups:
  - name: app.rules
    rules:
      # RÈGLE 1 : Application Down
      # - alert: ApplicationDown
      # - expr: up{job="react-app"} == 0
      # - for: 2m
      # - labels: severity: critical
      # - annotations:
      #   summary: "Application React indisponible"
      #   description: "L'application {{ $labels.instance }} est down depuis {{ $value }} minutes"

      # RÈGLE 2 : High Memory Usage
      # - alert: HighMemoryUsage
      # - expr: (memory usage > 80%)
      # - for: 5m
      # - labels: severity: warning

      # RÈGLE 3 : High CPU Usage
      # - alert: HighCPUUsage
      # - expr: (cpu usage > 75%)
      # - for: 3m
      # - labels: severity: warning

  - name: pipeline.rules
    rules:
      # RÈGLE 4 : Pipeline Failure Rate
      # - alert: HighPipelineFailureRate
      # - expr: (failed pipelines / total pipelines > 20%)
      # - for: 10m
      # - labels: severity: critical

      # RÈGLE 5 : Long Pipeline Duration
      # - alert: LongPipelineDuration
      # - expr: (pipeline duration > 15 minutes)
      # - for: 1m
      # - labels: severity: warning
```

### 1.3 Docker Compose pour monitoring

**Créer le fichier `monitoring/docker-compose.monitoring.yml`** :

```yaml
# Votre tâche : Configurer la stack de monitoring
version: '3.8'

services:
  prometheus:
    # Image : prom/prometheus:latest
    # Container name : prometheus
    # Ports : 9090:9090
    # Volumes :
    #   - ./prometheus.yml:/etc/prometheus/prometheus.yml
    #   - ./alerts:/etc/prometheus/alerts
    #   - prometheus_data:/prometheus
    # Command args :
    #   - '--config.file=/etc/prometheus/prometheus.yml'
    #   - '--storage.tsdb.path=/prometheus'
    #   - '--web.console.libraries=/etc/prometheus/console_libraries'
    #   - '--web.console.templates=/etc/prometheus/consoles'
    #   - '--storage.tsdb.retention.time=200h'
    #   - '--web.enable-lifecycle'
    #   - '--web.enable-admin-api'

  grafana:
    # Image : grafana/grafana:latest
    # Container name : grafana
    # Ports : 3001:3000
    # Environment :
    #   - GF_SECURITY_ADMIN_PASSWORD=admin123
    #   - GF_USERS_ALLOW_SIGN_UP=false
    # Volumes :
    #   - grafana_data:/var/lib/grafana
    #   - ./grafana/dashboards:/var/lib/grafana/dashboards
    #   - ./grafana/provisioning:/etc/grafana/provisioning

  alertmanager:
    # Image : prom/alertmanager:latest
    # Container name : alertmanager
    # Ports : 9093:9093
    # Volumes :
    #   - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    #   - alertmanager_data:/alertmanager

  cadvisor:
    # Image : gcr.io/cadvisor/cadvisor:latest
    # Container name : cadvisor
    # Ports : 8080:8080
    # Volumes pour monitoring Docker :
    #   - /:/rootfs:ro
    #   - /var/run:/var/run:rw
    #   - /sys:/sys:ro
    #   - /var/lib/docker/:/var/lib/docker:ro

# Volumes nommés pour persistance
volumes:
  # prometheus_data
  # grafana_data
  # alertmanager_data
```

## 📝 Exercice 2 : Métriques applicatives React (25 points)

### 2.1 Instrumentation de l'application React

**Modifier `src/App.js` pour ajouter des métriques** :

```javascript
// Votre tâche : Ajouter l'instrumentation des métriques
import React, {useState, useEffect} from 'react';
import './App.css';

// Importer prom-client pour les métriques
// const promClient = require('prom-client');

// Créer le registre des métriques
// const register = promClient.register;

// MÉTRIQUE 1 : Compteur des visites de page
// const pageViewsCounter = new promClient.Counter({
//   name: 'react_page_views_total',
//   help: 'Total number of page views',
//   labelNames: ['page', 'user_agent']
// });

// MÉTRIQUE 2 : Histogramme des temps de chargement
// const pageLoadHistogram = new promClient.Histogram({
//   name: 'react_page_load_duration_seconds',
//   help: 'Page load duration in seconds',
//   labelNames: ['page'],
//   buckets: [0.1, 0.5, 1, 2, 5]
// });

// MÉTRIQUE 3 : Gauge pour utilisateurs actifs
// const activeUsersGauge = new promClient.Gauge({
//   name: 'react_active_users',
//   help: 'Number of active users',
//   labelNames: ['session_type']
// });

// MÉTRIQUE 4 : Compteur d'erreurs
// const errorCounter = new promClient.Counter({
//   name: 'react_errors_total',
//   help: 'Total number of errors',
//   labelNames: ['error_type', 'component']
// });

function App() {
  const [loadTime, setLoadTime] = useState(0);
  const [errorCount, setErrorCount] = useState(0);
  const [userCount, setUserCount] = useState(1);

  useEffect(() => {
    // Mesurer le temps de chargement
    const startTime = performance.now();

    // Simuler le chargement
    setTimeout(() => {
      const endTime = performance.now();
      const duration = (endTime - startTime) / 1000;
      setLoadTime(duration);

      // Enregistrer les métriques
      // pageViewsCounter.inc({ page: 'home', user_agent: navigator.userAgent });
      // pageLoadHistogram.observe({ page: 'home' }, duration);
      // activeUsersGauge.set({ session_type: 'web' }, userCount);
    }, Math.random() * 1000);

    // Simulation d'erreurs aléatoires
    const errorInterval = setInterval(() => {
      if (Math.random() > 0.95) {
        // 5% de chance d'erreur
        setErrorCount((prev) => prev + 1);
        // errorCounter.inc({ error_type: 'network', component: 'App' });
      }
    }, 5000);

    return () => clearInterval(errorInterval);
  }, [userCount]);

  // Fonction pour simuler l'activité utilisateur
  const simulateUserActivity = () => {
    setUserCount((prev) => prev + Math.floor(Math.random() * 3));
    // activeUsersGauge.set({ session_type: 'web' }, userCount);
  };

  return (
    <div className='App'>
      <header className='App-header'>
        <h1>🚀 DevOps React App - Monitoring Lab</h1>

        <div className='metrics-dashboard'>
          <div className='metric-card'>
            <h3>⏱️ Page Load Time</h3>
            <p>{loadTime.toFixed(3)} seconds</p>
          </div>

          <div className='metric-card'>
            <h3>❌ Error Count</h3>
            <p>{errorCount}</p>
          </div>

          <div className='metric-card'>
            <h3>👥 Active Users</h3>
            <p>{userCount}</p>
          </div>
        </div>

        <div className='actions'>
          <button onClick={simulateUserActivity}>
            📈 Simulate User Activity
          </button>

          <button
            onClick={() => {
              setErrorCount((prev) => prev + 1);
              // errorCounter.inc({ error_type: 'manual', component: 'App' });
            }}
          >
            💥 Trigger Error
          </button>
        </div>

        <div className='monitoring-info'>
          <h2>📊 Monitoring Stack</h2>
          <ul>
            <li>
              🎯 <strong>Prometheus:</strong>{' '}
              <a
                href='http://localhost:9090'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:9090
              </a>
            </li>
            <li>
              📈 <strong>Grafana:</strong>{' '}
              <a
                href='http://localhost:3001'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:3001
              </a>
            </li>
            <li>
              🚨 <strong>AlertManager:</strong>{' '}
              <a
                href='http://localhost:9093'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:9093
              </a>
            </li>
            <li>
              🐳 <strong>cAdvisor:</strong>{' '}
              <a
                href='http://localhost:8080'
                target='_blank'
                rel='noopener noreferrer'
              >
                http://localhost:8080
              </a>
            </li>
          </ul>
        </div>
      </header>
    </div>
  );
}

export default App;
```

### 2.2 Endpoint des métriques

**Créer `src/metrics.js`** :

```javascript
// Votre tâche : Créer l'endpoint des métriques Prometheus
const express = require('express');
const promClient = require('prom-client');

// Créer une app Express pour servir les métriques
const app = express();
const port = 9464;

// Créer le registre des métriques
const register = promClient.register;

// Collecter les métriques par défaut (CPU, mémoire, etc.)
// promClient.collectDefaultMetrics({ register });

// MÉTRIQUE PERSONNALISÉE 1 : Build Info
// const buildInfo = new promClient.Gauge({
//   name: 'react_app_build_info',
//   help: 'Build information',
//   labelNames: ['version', 'commit', 'branch', 'build_date']
// });

// MÉTRIQUE PERSONNALISÉE 2 : Feature Flags
// const featureFlagsGauge = new promClient.Gauge({
//   name: 'react_app_feature_flags',
//   help: 'Feature flags status',
//   labelNames: ['feature_name', 'enabled']
// });

// MÉTRIQUE PERSONNALISÉE 3 : API Response Times
// const apiResponseTime = new promClient.Histogram({
//   name: 'react_app_api_duration_seconds',
//   help: 'API response time in seconds',
//   labelNames: ['method', 'endpoint', 'status'],
//   buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
// });

// Initialiser les métriques statiques
// buildInfo.set({
//   version: process.env.npm_package_version || '1.0.0',
//   commit: process.env.CI_COMMIT_SHA || 'unknown',
//   branch: process.env.CI_COMMIT_REF_NAME || 'local',
//   build_date: new Date().toISOString()
// }, 1);

// Middleware pour CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});

// Endpoint de santé
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Endpoint des métriques Prometheus
app.get('/metrics', async (req, res) => {
  try {
    // Retourner les métriques au format Prometheus
    // res.set('Content-Type', register.contentType);
    // const metrics = await register.metrics();
    // res.end(metrics);
  } catch (error) {
    console.error('Erreur lors de la collecte des métriques:', error);
    res.status(500).send('Erreur interne du serveur');
  }
});

// Fonction utilitaire pour enregistrer des métriques API
function recordApiMetric(method, endpoint, duration, status) {
  // apiResponseTime.observe({ method, endpoint, status }, duration);
}

// Démarrer le serveur des métriques
if (require.main === module) {
  app.listen(port, () => {
    console.log(`🎯 Serveur de métriques démarré sur le port ${port}`);
    console.log(
      `📊 Métriques disponibles sur http://localhost:${port}/metrics`
    );
    console.log(`❤️ Health check sur http://localhost:${port}/health`);
  });
}

module.exports = {app, recordApiMetric};
```

### 2.3 Configuration package.json

**Ajouter les dépendances et scripts dans `package.json`** :

```json
{
  "scripts": {
    "start": "react-scripts start",
    "metrics": "node src/metrics.js",
    "start:with-metrics": "concurrently \"npm run metrics\" \"npm start\"",
    "monitoring:up": "docker-compose -f monitoring/docker-compose.monitoring.yml up -d",
    "monitoring:down": "docker-compose -f monitoring/docker-compose.monitoring.yml down"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "prom-client": "^14.2.0",
    "express": "^4.18.2",
    "concurrently": "^7.6.0"
  }
}
```

## 📝 Exercice 3 : Configuration Grafana Dashboards (20 points)

### 3.1 Provisioning des datasources

**Créer `monitoring/grafana/provisioning/datasources/prometheus.yml`** :

```yaml
# Votre tâche : Configurer la datasource Prometheus
apiVersion: 1

datasources:
  # Configuration Prometheus
  # - name: Prometheus
  # - type: prometheus
  # - access: proxy
  # - url: http://prometheus:9090
  # - isDefault: true
  # - editable: true
  # - jsonData:
  #     httpMethod: POST
  #     timeInterval: "15s"
```

### 3.2 Dashboard applicatif

**Créer `monitoring/grafana/dashboards/app-dashboard.json`** :

Votre tâche : Créer un dashboard JSON avec les panels suivants :

1. **Panel 1 - Overview Row**

   - Type: Row
   - Title: "📊 Application Overview"

2. **Panel 2 - Page Views**

   - Type: Stat
   - Metric: `rate(react_page_views_total[5m])`
   - Title: "Page Views per Second"

3. **Panel 3 - Active Users**

   - Type: Gauge
   - Metric: `react_active_users`
   - Title: "Active Users"
   - Min: 0, Max: 100

4. **Panel 4 - Error Rate**

   - Type: Stat
   - Metric: `rate(react_errors_total[5m])`
   - Title: "Error Rate"
   - Color: Rouge si > 0.1

5. **Panel 5 - Response Time**

   - Type: Time series
   - Metric: `histogram_quantile(0.95, rate(react_page_load_duration_seconds_bucket[5m]))`
   - Title: "95th Percentile Response Time"

6. **Panel 6 - Memory Usage**
   - Type: Time series
   - Metric: `process_resident_memory_bytes`
   - Title: "Memory Usage"

### 3.3 Dashboard Infrastructure

**Créer `monitoring/grafana/dashboards/infrastructure-dashboard.json`** :

Votre tâche : Créer un dashboard avec :

1. **Panel Docker Overview**

   - Containers en cours d'exécution
   - Utilisation CPU des containers
   - Utilisation mémoire des containers
   - Trafic réseau

2. **Panel System Metrics**
   - CPU système
   - Mémoire système
   - Espace disque
   - Load average

## 📝 Exercice 4 : Pipeline CI/CD avec métriques (15 points)

### 4.1 Intégration monitoring dans GitLab CI

**Modifier `.gitlab-ci.yml` pour inclure le monitoring** :

```yaml
# Votre tâche : Ajouter les étapes de monitoring
include:
  - local: 'monitoring/gitlab-monitoring.yml'

variables:
  # Variables de monitoring
  METRICS_ENABLED: 'true'
  PROMETHEUS_URL: 'http://prometheus:9090'
  GRAFANA_URL: 'http://grafana:3000'

stages:
  - validate
  - build
  - test
  - security
  - deploy
  - monitor # Nouvelle étape
  - notify

# Template pour les métriques de pipeline
.pipeline_metrics_template: &pipeline_metrics
  before_script:
    - echo "🎯 Début job: $CI_JOB_NAME à $(date)"
    - start_time=$(date +%s)
  after_script:
    - end_time=$(date +%s)
    - duration=$((end_time - start_time))
    - echo "⏱️ Durée job $CI_JOB_NAME: ${duration}s"
    # Envoyer les métriques à Prometheus
    - |
      if [ "$METRICS_ENABLED" = "true" ]; then
        curl -X POST "${PROMETHEUS_URL}/api/v1/query" \
          --data "query=gitlab_pipeline_job_duration_seconds{job=\"$CI_JOB_NAME\",pipeline=\"$CI_PIPELINE_ID\"}" \
          --data "value=$duration" || echo "Erreur envoi métriques"
      fi

# Job de monitoring des métriques
monitor_application:
  stage: monitor
  image: curlimages/curl:latest
  <<: *pipeline_metrics
  script:
    - echo "📊 === MONITORING APPLICATION ==="

    # Vérifier la disponibilité des métriques
    - |
      echo "🔍 Vérification endpoint métriques"
      if ! curl -f http://localhost:9464/metrics; then
        echo "❌ Endpoint métriques indisponible"
        exit 1
      fi
      echo "✅ Endpoint métriques accessible"

    # Vérifier Prometheus
    - |
      echo "🎯 Vérification Prometheus"
      if ! curl -f "${PROMETHEUS_URL}/-/healthy"; then
        echo "❌ Prometheus indisponible"
        exit 1
      fi
      echo "✅ Prometheus accessible"

    # Vérifier Grafana
    - |
      echo "📈 Vérification Grafana"
      if ! curl -f "${GRAFANA_URL}/api/health"; then
        echo "❌ Grafana indisponible"
        exit 1
      fi
      echo "✅ Grafana accessible"

    # Collecter les métriques clés
    - |
      echo "📊 Collecte des métriques clés"

      # Métriques de l'application
      app_up=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=up{job=\"react-app\"}" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
      error_rate=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=rate(react_errors_total[5m])" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
      response_time=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=histogram_quantile(0.95,rate(react_page_load_duration_seconds_bucket[5m]))" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")

      echo "Application UP: $app_up"
      echo "Error Rate: $error_rate"
      echo "95th Percentile Response Time: ${response_time}s"

      # Vérifier les seuils
      if [ "$app_up" != "1" ]; then
        echo "❌ Application down détectée"
        exit 1
      fi

      if [ "$(echo "$error_rate > 0.1" | bc)" -eq 1 ]; then
        echo "⚠️ Taux d'erreur élevé: $error_rate"
      fi

      if [ "$(echo "$response_time > 2" | bc)" -eq 1 ]; then
        echo "⚠️ Temps de réponse élevé: ${response_time}s"
      fi

    - echo "✅ Monitoring terminé"
  only:
    - main
    - develop

# Job de création d'alertes
setup_alerts:
  stage: monitor
  image: alpine:latest
  script:
    - echo "🚨 === CONFIGURATION ALERTES ==="

    # Installer les outils nécessaires
    - apk add --no-cache curl jq

    # Créer des alertes GitLab via API
    - |
      echo "📧 Configuration des alertes GitLab"

      # Alerte pour pipeline failure
      curl -X POST "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/integrations/prometheus" \
        --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        --data "active=true" \
        --data "prometheus_url=${PROMETHEUS_URL}" \
        --data "manual_configuration=false" || echo "Erreur configuration Prometheus"

      # Alerte pour application down
      curl -X POST "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/alert_management/alerts" \
        --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
        --header "Content-Type: application/json" \
        --data '{
          "title": "Application Down Alert",
          "description": "Alert when React app is down",
          "monitoring_tool": "Prometheus",
          "service": "react-app"
        }' || echo "Erreur création alerte"

    - echo "✅ Alertes configurées"
  when: manual
  only:
    - main

# Job de rapport de performance
performance_report:
  stage: monitor
  image: node:18-alpine
  <<: *pipeline_metrics
  script:
    - echo "📈 === RAPPORT DE PERFORMANCE ==="
    - apk add --no-cache curl jq bc

    # Générer un rapport de performance
    - |
      cat > performance-report.json << EOF
      {
        "pipeline_id": "$CI_PIPELINE_ID",
        "commit": "$CI_COMMIT_SHA",
        "branch": "$CI_COMMIT_REF_NAME",
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "metrics": {}
      }
      EOF

    # Collecter les métriques de performance
    - |
      if [ "$METRICS_ENABLED" = "true" ]; then
        echo "📊 Collecte des métriques de performance"
        
        # Temps de build
        build_duration=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=gitlab_pipeline_job_duration_seconds{job=\"build\"}" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
        
        # Temps de test
        test_duration=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=gitlab_pipeline_job_duration_seconds{job=\"test\"}" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
        
        # Temps total du pipeline
        total_duration=$(curl -s "${PROMETHEUS_URL}/api/v1/query?query=gitlab_pipeline_duration_seconds{pipeline=\"$CI_PIPELINE_ID\"}" | jq -r '.data.result[0].value[1]' 2>/dev/null || echo "0")
        
        # Mise à jour du rapport
        jq --arg build "$build_duration" --arg test "$test_duration" --arg total "$total_duration" \
          '.metrics = {"build_duration": ($build | tonumber), "test_duration": ($test | tonumber), "total_duration": ($total | tonumber)}' \
          performance-report.json > tmp.json && mv tmp.json performance-report.json
        
        echo "Build Duration: ${build_duration}s"
        echo "Test Duration: ${test_duration}s"
        echo "Total Duration: ${total_duration}s"
        
        # Comparaison avec les seuils
        if [ "$(echo "$total_duration > 900" | bc)" -eq 1 ]; then
          echo "⚠️ Pipeline trop long (> 15min): ${total_duration}s"
        fi
      fi

    - echo "✅ Rapport de performance généré"
    - cat performance-report.json
  artifacts:
    reports:
      performance: performance-report.json
    paths:
      - performance-report.json
    expire_in: 30 days
  only:
    - main
    - develop
```

## 📝 Exercice 5 : AlertManager et notifications (10 points)

### 5.1 Configuration AlertManager

**Créer `monitoring/alertmanager.yml`** :

```yaml
# Votre tâche : Configurer AlertManager
global:
  # SMTP settings pour les emails
  # smtp_smarthost: 'localhost:587'
  # smtp_from: 'alertmanager@example.com'
  # smtp_auth_username: 'alertmanager@example.com'
  # smtp_auth_password: 'password'

# Templates pour les notifications
templates:
  # - '/etc/alertmanager/templates/*.tmpl'

# Configuration du routing
route:
  # group_by: ['alertname']
  # group_wait: 10s
  # group_interval: 10s
  # repeat_interval: 1h
  # receiver: 'web.hook'
  routes:
    # Route pour les alertes critiques
    # - match:
    #     severity: critical
    #   receiver: critical-alerts
    #   group_wait: 5s
    #   repeat_interval: 15m

    # Route pour les alertes de warning
    # - match:
    #     severity: warning
    #   receiver: warning-alerts
    #   group_wait: 30s
    #   repeat_interval: 1h

# Récepteurs de notifications
receivers:
  # Webhook par défaut
  # - name: 'web.hook'
  #   webhook_configs:
  #     - url: 'http://localhost:8080/webhook'

  # Alertes critiques (email + Slack)
  # - name: 'critical-alerts'
  #   email_configs:
  #     - to: 'devops@example.com'
  #       subject: '🚨 ALERTE CRITIQUE: {{ .GroupLabels.alertname }}'
  #       body: |
  #         {{ range .Alerts }}
  #         Alerte: {{ .Annotations.summary }}
  #         Description: {{ .Annotations.description }}
  #         Sévérité: {{ .Labels.severity }}
  #         Instance: {{ .Labels.instance }}
  #         {{ end }}
  #   slack_configs:
  #     - api_url: 'YOUR_SLACK_WEBHOOK_URL'
  #       channel: '#alerts'
  #       title: '🚨 Alerte Critique'
  #       text: '{{ .CommonAnnotations.summary }}'

  # Alertes de warning (email uniquement)
  # - name: 'warning-alerts'
  #   email_configs:
  #     - to: 'team@example.com'
  #       subject: '⚠️ AVERTISSEMENT: {{ .GroupLabels.alertname }}'

# Suppression d'alertes (silences)
inhibit_rules:
  # Supprimer les alertes de warning si critique active
  # - source_match:
  #     severity: 'critical'
  #   target_match:
  #     severity: 'warning'
  #   equal: ['alertname', 'dev', 'instance']
```

### 5.2 Intégration GitLab

**Créer `scripts/gitlab-webhook.js`** :

```javascript
// Votre tâche : Créer un webhook pour recevoir les alertes
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

// Configuration GitLab
const GITLAB_TOKEN = process.env.GITLAB_TOKEN;
const GITLAB_PROJECT_ID = process.env.CI_PROJECT_ID;
const GITLAB_API_URL = process.env.CI_API_V4_URL;

// Webhook pour recevoir les alertes d'AlertManager
app.post('/webhook', async (req, res) => {
  try {
    const alerts = req.body.alerts;

    for (const alert of alerts) {
      // Créer une issue GitLab pour chaque alerte critique
      if (alert.labels.severity === 'critical') {
        // await createGitLabIssue(alert);
      }

      // Envoyer une notification
      // await sendNotification(alert);
    }

    res.status(200).send('OK');
  } catch (error) {
    console.error('Erreur traitement webhook:', error);
    res.status(500).send('Erreur');
  }
});

async function createGitLabIssue(alert) {
  // Votre tâche : Créer une issue GitLab
  const issueData = {
    // title: `🚨 Alerte: ${alert.annotations.summary}`,
    // description: `
    // ## 🚨 Alerte Critique
    //
    // **Description:** ${alert.annotations.description}
    // **Sévérité:** ${alert.labels.severity}
    // **Instance:** ${alert.labels.instance}
    // **Début:** ${alert.startsAt}
    //
    // ### Actions à prendre:
    // - [ ] Investiguer la cause
    // - [ ] Appliquer un correctif
    // - [ ] Vérifier la résolution
    //
    // **Généré automatiquement par AlertManager**
    // `,
    // labels: ['alert', 'critical', 'monitoring']
  };

  try {
    // const response = await axios.post(
    //   `${GITLAB_API_URL}/projects/${GITLAB_PROJECT_ID}/issues`,
    //   issueData,
    //   {
    //     headers: {
    //       'PRIVATE-TOKEN': GITLAB_TOKEN,
    //       'Content-Type': 'application/json'
    //     }
    //   }
    // );
    // console.log('Issue GitLab créée:', response.data.web_url);
  } catch (error) {
    console.error('Erreur création issue GitLab:', error.message);
  }
}

async function sendNotification(alert) {
  // Votre tâche : Envoyer une notification
  console.log(`📧 Notification: ${alert.annotations.summary}`);

  // Exemple d'intégration Slack
  // if (process.env.SLACK_WEBHOOK_URL) {
  //   await axios.post(process.env.SLACK_WEBHOOK_URL, {
  //     text: `🚨 ${alert.annotations.summary}`,
  //     attachments: [{
  //       color: alert.labels.severity === 'critical' ? 'danger' : 'warning',
  //       fields: [
  //         { title: 'Instance', value: alert.labels.instance, short: true },
  //         { title: 'Sévérité', value: alert.labels.severity, short: true }
  //       ]
  //     }]
  //   });
  // }
}

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`🎯 Webhook server démarré sur le port ${port}`);
});
```

## 🎯 Livrables attendus

### Fichiers à créer/modifier :

1. **Configuration Monitoring** :

   - `monitoring/prometheus.yml` ✅
   - `monitoring/alerts/app-alerts.yml` ✅
   - `monitoring/docker-compose.monitoring.yml` ✅
   - `monitoring/alertmanager.yml` ✅

2. **Application React instrumentée** :

   - `src/App.js` modifié avec métriques ✅
   - `src/metrics.js` endpoint Prometheus ✅
   - `package.json` avec dépendances monitoring ✅

3. **Dashboards Grafana** :

   - `monitoring/grafana/provisioning/datasources/prometheus.yml` ✅
   - `monitoring/grafana/dashboards/app-dashboard.json` ✅
   - `monitoring/grafana/dashboards/infrastructure-dashboard.json` ✅

4. **Pipeline CI/CD** :

   - `.gitlab-ci.yml` avec étapes monitoring ✅
   - `scripts/gitlab-webhook.js` intégration alertes ✅

5. **Documentation** :
   - `README-monitoring.md` guide d'utilisation ✅

## 📊 Grille d'évaluation (100 points)

| Critère                      | Points | Description                                                     |
| ---------------------------- | ------ | --------------------------------------------------------------- |
| **Configuration Prometheus** | 30     | Fichiers de config, règles d'alerting, jobs de scraping         |
| **Métriques applicatives**   | 25     | Instrumentation React, endpoint /metrics, métriques custom      |
| **Dashboards Grafana**       | 20     | Provisioning, panels application, panels infrastructure         |
| **Pipeline monitoring**      | 15     | Jobs CI/CD monitoring, métriques pipeline, rapports performance |
| **AlertManager**             | 10     | Configuration alertes, notifications, intégration GitLab        |

## 🎓 Points bonus (10 points)

- ✅ **Métriques business** : Métriques métier personnalisées (+3)
- ✅ **SLI/SLO monitoring** : Définition et suivi d'objectifs (+3)
- ✅ **Monitoring multi-environnements** : Dev/Staging/Prod (+2)
- ✅ **Documentation avancée** : Runbooks et guides troubleshooting (+2)

## 📚 Ressources utiles

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [GitLab Monitoring](https://docs.gitlab.com/ee/operations/metrics/)
- [Best Practices Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)

## 🔄 Étapes suivantes

Après avoir terminé ce lab :

1. ✅ Vérifier que tous les services de monitoring fonctionnent
2. ✅ Tester les alertes en simulant des problèmes
3. ✅ Analyser les dashboards Grafana
4. ✅ Valider l'intégration avec GitLab CI/CD
5. ➡️ Passer au **LAB 8 : Environments et Déploiements avancés**

---

💡 **Conseil** : Le monitoring n'est pas juste de la supervision, c'est un outil de développement qui aide à comprendre et améliorer vos applications !
