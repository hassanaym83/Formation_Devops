# LAB 4 - Health et Monitoring

## Objectif

Configurer health checks complets et monitoring applicatif avec Prometheus et Grafana.

## Contexte

Mettre en place une stack complète de monitoring et health checks pour l'application e-commerce avec :

- Health checks avancés (startup, liveness, readiness)
- Monitoring avec Prometheus et Grafana
- Alerting automatique sur métriques critiques
- Dashboards de performance applicative

## Prérequis

- Application e-commerce déployée (LABs 1-3)
- Cluster Kubernetes avec ressources suffisantes
- Helm installé (optionnel pour Prometheus)

## Instructions détaillées

### Étape 1 : Configurer health checks avancés

1. Mettre à jour le Deployment de l'API avec health checks complets :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-backend
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-backend
  template:
    metadata:
      labels:
        app: api-backend
    spec:
      containers:
        - name: api
          image: node:16-alpine
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: DATABASE_URL
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: REDIS_URL
          # Health checks configuration
          startupProbe:
            httpGet:
              path: /health/startup
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 30
          livenessProbe:
            httpGet:
              path: /health/live
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
```

### Étape 2 : Créer endpoints de health check dans l'API

2. Développer les endpoints de santé pour l'API Node.js :

```javascript
// health-endpoints.js
const express = require('express');
const {Pool} = require('pg');
const redis = require('redis');

class HealthChecker {
  constructor(dbPool, redisClient) {
    this.dbPool = dbPool;
    this.redisClient = redisClient;
    this.startupComplete = false;
  }

  // Startup probe - vérifie l'initialisation complète
  async checkStartup(req, res) {
    try {
      if (!this.startupComplete) {
        // Simulation d'initialisation
        await this.initializeApplication();
        this.startupComplete = true;
      }
      res.json({
        status: 'started',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
      });
    } catch (error) {
      res.status(503).json({
        status: 'starting',
        error: error.message
      });
    }
  }

  // Liveness probe - vérifie que l'app est vivante
  async checkLiveness(req, res) {
    try {
      // Vérifications basiques (mémoire, processus)
      const memUsage = process.memoryUsage();
      const cpuUsage = process.cpuUsage();

      // Seuils critiques
      if (memUsage.heapUsed > 200 * 1024 * 1024) {
        // 200MB
        throw new Error('Memory usage too high');
      }

      res.json({
        status: 'alive',
        timestamp: new Date().toISOString(),
        memory: memUsage,
        cpu: cpuUsage
      });
    } catch (error) {
      res.status(503).json({
        status: 'unhealthy',
        error: error.message
      });
    }
  }

  // Readiness probe - vérifie la capacité à traiter le trafic
  async checkReadiness(req, res) {
    try {
      // Vérifier connexions externes
      await this.dbPool.query('SELECT 1');
      await this.redisClient.ping();

      res.json({
        status: 'ready',
        timestamp: new Date().toISOString(),
        dependencies: {
          database: 'connected',
          redis: 'connected'
        }
      });
    } catch (error) {
      res.status(503).json({
        status: 'not-ready',
        error: error.message,
        dependencies: {
          database: 'error',
          redis: 'error'
        }
      });
    }
  }

  async initializeApplication() {
    // Simulation d'initialisation (chargement config, etc.)
    await new Promise((resolve) => setTimeout(resolve, 5000));
  }
}

module.exports = HealthChecker;
```

### Étape 3 : Déployer Prometheus

3. Installer Prometheus avec Helm :

```bash
# Ajouter le repo Helm Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Créer namespace pour monitoring
kubectl create namespace monitoring

# Installer Prometheus Stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.retention=30d \
  --set grafana.adminPassword=admin123
```

### Étape 4 : Configurer ServiceMonitor pour métriques applicatives

4. Créer ServiceMonitor pour collecter métriques de l'API :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-metrics
  namespace: monitoring
  labels:
    app: api-backend
spec:
  selector:
    matchLabels:
      app: api-backend
  endpoints:
    - port: metrics
      interval: 15s
      path: /metrics
  namespaceSelector:
    matchNames:
      - ecommerce
```

### Étape 5 : Ajouter métriques custom à l'API

5. Instrumenter l'API avec des métriques Prometheus :

```javascript
// metrics.js
const promClient = require('prom-client');

// Créer un registre pour les métriques
const register = new promClient.Registry();

// Métriques par défaut (CPU, mémoire, etc.)
promClient.collectDefaultMetrics({register});

// Métriques custom
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

const databaseConnections = new promClient.Gauge({
  name: 'database_connections_active',
  help: 'Number of active database connections'
});

const redisOperations = new promClient.Counter({
  name: 'redis_operations_total',
  help: 'Total number of Redis operations',
  labelNames: ['operation', 'result']
});

// Enregistrer les métriques
register.registerMetric(httpRequestsTotal);
register.registerMetric(httpRequestDuration);
register.registerMetric(databaseConnections);
register.registerMetric(redisOperations);

// Middleware pour collecter métriques HTTP
function metricsMiddleware(req, res, next) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;

    httpRequestsTotal
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .inc();

    httpRequestDuration
      .labels(req.method, req.route?.path || req.path)
      .observe(duration);
  });

  next();
}

// Endpoint pour exposer métriques
function metricsEndpoint(req, res) {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
}

module.exports = {
  register,
  metricsMiddleware,
  metricsEndpoint,
  httpRequestsTotal,
  httpRequestDuration,
  databaseConnections,
  redisOperations
};
```

### Étape 6 : Créer dashboards Grafana

6. Configurer un dashboard Grafana pour l'application :

```json
{
  "dashboard": {
    "title": "E-commerce Application Monitoring",
    "panels": [
      {
        "title": "HTTP Requests Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{route}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Application Health",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"api-backend\"}",
            "legendFormat": "API Status"
          }
        ]
      }
    ]
  }
}
```

### Étape 7 : Configurer alerting

7. Créer règles d'alerting Prometheus :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ecommerce-alerts
  namespace: monitoring
spec:
  groups:
    - name: ecommerce.rules
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status_code=~"5.."}[5m]) > 0.1
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: 'High error rate detected'
            description: 'Error rate is {{ $value }} requests per second'

        - alert: HighResponseTime
          expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: 'High response time detected'
            description: '95th percentile response time is {{ $value }} seconds'

        - alert: DatabaseConnectionFailed
          expr: up{job="postgres"} == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: 'Database connection failed'
            description: 'PostgreSQL database is down'

        - alert: PodCrashLooping
          expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: 'Pod is crash looping'
            description: 'Pod {{ $labels.pod }} is restarting frequently'
```

### Étape 8 : Tests et validation

8. Tester les health checks et monitoring :

```bash
# Vérifier les health checks
kubectl get pods -n ecommerce
kubectl describe pod <api-pod> -n ecommerce

# Générer du trafic pour tester les métriques
kubectl run -i --tty load-test --rm --image=alpine/curl --restart=Never -- sh
# Dans le pod :
for i in {1..100}; do
  curl -s http://api-service.ecommerce.svc.cluster.local:3000/health/ready
  sleep 0.1
done

# Accéder à Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Aller sur http://localhost:3000 (admin/admin123)

# Vérifier Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Aller sur http://localhost:9090
```

## Critères de validation

- [ ] Health checks configurés et fonctionnels (startup, liveness, readiness)
- [ ] Prometheus collecte les métriques applicatives et système
- [ ] Grafana affiche les dashboards avec métriques en temps réel
- [ ] Alertes configurées et testées
- [ ] Métriques custom instrumentées dans l'application
- [ ] Pods redémarrent automatiquement en cas d'échec de liveness
- [ ] Trafic arrêté automatiquement si readiness probe échoue
- [ ] Monitoring fonctionne sous charge

## Livrables

- Manifests YAML avec health checks complets
- Code instrumenté avec métriques Prometheus
- Dashboard Grafana exporté
- Règles d'alerting configurées
- Script de test de charge et validation

## Durée estimée

50 minutes

## Points bonus

- Implémenter tracing distribué avec Jaeger
- Configurer log aggregation avec ELK Stack
- Ajouter métriques business (commandes, revenus)
- Intégrer notification Slack pour alertes
