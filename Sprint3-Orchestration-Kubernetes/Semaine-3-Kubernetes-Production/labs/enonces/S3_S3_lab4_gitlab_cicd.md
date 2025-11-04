# LAB 4 - CI/CD GitLab Kubernetes integration

## Objectifs

- Configurer l'intégration GitLab avec Kubernetes
- Créer des pipelines CI/CD pour déploiement automatique
- Implémenter des stratégies de déploiement (blue/green, canary)
- Configurer l'auto-déploiement et rollback
- Sécuriser les déploiements avec validation

## Prérequis

- Instance GitLab accessible (GitLab.com ou self-hosted)
- Cluster Kubernetes configuré
- Docker registry accessible
- Helm 3.x installé
- Connaissances GitLab CI/CD

## Contexte du LAB

Vous devez mettre en place une chaîne CI/CD complète pour une application Node.js avec :

- Build automatique des images Docker
- Tests de sécurité et qualité
- Déploiement automatique sur Kubernetes
- Monitoring des déploiements
- Rollback automatique en cas d'échec

## Exercice 1 : Configuration de l'environnement

### Étape 1.1 : Structure du projet

Créez la structure de projet suivante :

```
nodejs-app/
├── .gitlab-ci.yml
├── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── helm/
│   └── nodejs-app/
├── scripts/
│   ├── deploy.sh
│   └── rollback.sh
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
└── src/
    └── app.js
```

### Étape 1.2 : Application Node.js simple

Créez `src/app.js` :

```javascript
const express = require('express');
const prometheus = require('prom-client');
const app = express();
const port = process.env.PORT || 3000;

// Métriques Prometheus
const collectDefaultMetrics = prometheus.collectDefaultMetrics;
collectDefaultMetrics();

const httpRequestsTotal = new prometheus.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});

// Middleware pour les métriques
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    httpRequestsTotal.inc({
      method: req.method,
      route: req.route ? req.route.path : req.path,
      status: res.statusCode
    });
  });

  next();
});

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Hello from Node.js App!',
    version: process.env.APP_VERSION || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString()
  });
});

app.get('/health', (req, res) => {
  res.status(200).json({status: 'healthy'});
});

app.get('/ready', (req, res) => {
  // Vérifications de readiness ici
  res.status(200).json({status: 'ready'});
});

app.get('/metrics', (req, res) => {
  res.set('Content-Type', prometheus.register.contentType);
  res.end(prometheus.register.metrics());
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});

module.exports = app;
```

### Étape 1.3 : Dockerfile multi-stage

Créez un `Dockerfile` optimisé :

```dockerfile
# Votre Dockerfile multi-stage ici
# - Stage de build
# - Stage de production avec image minimale
# - Utilisateur non-root
# - Optimisations de sécurité
```

### Étape 1.4 : Package.json

Créez `package.json` :

```json
{
  "name": "nodejs-k8s-app",
  "version": "1.0.0",
  "description": "Node.js app for Kubernetes CI/CD",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "test": "jest",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/",
    "security": "npm audit"
  },
  "dependencies": {
    "express": "^4.18.2",
    "prom-client": "^14.2.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "eslint": "^8.39.0",
    "supertest": "^6.3.3"
  }
}
```

## Exercice 2 : Configuration GitLab CI/CD

### Étape 2.1 : Variables GitLab CI/CD

Configurez les variables dans GitLab (Settings > CI/CD > Variables) :

```bash
# Registry
DOCKER_REGISTRY = registry.gitlab.com
DOCKER_IMAGE_NAME = $CI_PROJECT_PATH

# Kubernetes
KUBECONFIG = <base64-encoded-kubeconfig>
KUBE_NAMESPACE_DEV = nodejs-app-dev
KUBE_NAMESPACE_STAGING = nodejs-app-staging
KUBE_NAMESPACE_PROD = nodejs-app-prod

# Security
SONAR_TOKEN = <sonar-token>
DOCKER_REGISTRY_TOKEN = <registry-token>
```

### Étape 2.2 : Pipeline GitLab CI/CD

Créez `.gitlab-ci.yml` :

```yaml
stages:
  - build
  - test
  - security
  - package
  - deploy-dev
  - deploy-staging
  - deploy-prod

variables:
  DOCKER_IMAGE: $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME
  HELM_CHART_PATH: ./helm/nodejs-app

# Templates
.docker-login: &docker-login
  - echo $DOCKER_REGISTRY_TOKEN | docker login $DOCKER_REGISTRY -u $CI_REGISTRY_USER --password-stdin

.kubectl-config: &kubectl-config
  - echo $KUBECONFIG | base64 -d > ~/.kube/config
  - chmod 600 ~/.kube/config

# Build stage
build:
  stage: build
  image: docker:20.0.12
  services:
    - docker:20.0.12-dind
  before_script:
    - *docker-login
  script:
    # Votre script de build ici
    # - Build de l'image Docker
    # - Tag avec commit SHA et latest
    # - Push vers le registry
  only:
    - main
    - develop
    - merge_requests

# Test stage
test:unit:
  stage: test
  image: node:18-alpine
  script:
    # Votre script de tests unitaires
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:integration:
  stage: test
  image: docker/compose:latest
  services:
    - docker:20.0.12-dind
  script:
    # Votre script de tests d'intégration
  only:
    - main
    - merge_requests

# Security stage
security:container-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    # Scan de sécurité de l'image Docker
  allow_failure: false
  only:
    - main
    - merge_requests

security:sast:
  stage: security
  image: sonarqube-scanner:latest
  script:
    # Analyse statique du code
  only:
    - main
    - merge_requests

# Package stage
package:helm:
  stage: package
  image: alpine/helm:latest
  script:
    # Package du Helm chart
    # Mise à jour de la version
    # Upload vers le registry Helm
  artifacts:
    paths:
      - '*.tgz'
  only:
    - main

# Deploy stages
deploy:dev:
  stage: deploy-dev
  image: alpine/helm:latest
  before_script:
    - *kubectl-config
  script:
    # Déploiement en développement
  environment:
    name: development
    url: https://nodejs-app-dev.example.com
  only:
    - develop

deploy:staging:
  stage: deploy-staging
  image: alpine/helm:latest
  before_script:
    - *kubectl-config
  script:
    # Déploiement en staging
  environment:
    name: staging
    url: https://nodejs-app-staging.example.com
  when: manual
  only:
    - main

deploy:production:
  stage: deploy-prod
  image: alpine/helm:latest
  before_script:
    - *kubectl-config
  script:
    # Déploiement en production avec validation
  environment:
    name: production
    url: https://nodejs-app.example.com
  when: manual
  only:
    - main
```

## Exercice 3 : Manifestes Kubernetes

### Étape 3.1 : Namespace avec labels

Créez `k8s/namespace.yaml` :

```yaml
# Namespace pour chaque environnement
# avec labels et annotations appropriés
```

### Étape 3.2 : Deployment avec stratégies

Créez `k8s/deployment.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-app
  labels:
    app: nodejs-app
    version: '1.0.0'
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: nodejs-app
  template:
    metadata:
      labels:
        app: nodejs-app
        version: '1.0.0'
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '3000'
        prometheus.io/path: '/metrics'
    spec:
      # Configuration de sécurité
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: nodejs-app
          image: # À remplir par le pipeline
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: NODE_ENV
              value: 'production'
            - name: APP_VERSION
              value: # À remplir par le pipeline
          # Probes de santé
          livenessProbe:
            # À compléter
          readinessProbe:
            # À compléter
          # Resources
          resources:
            # À compléter
          # Security context
          securityContext:
            # À compléter
```

## Exercice 4 : Scripts de déploiement

### Étape 4.1 : Script de déploiement

Créez `scripts/deploy.sh` :

```bash
#!/bin/bash

set -e

ENVIRONMENT=${1:-dev}
IMAGE_TAG=${2:-latest}
NAMESPACE="nodejs-app-$ENVIRONMENT"

echo "Deploying to $ENVIRONMENT environment..."
echo "Image tag: $IMAGE_TAG"
echo "Namespace: $NAMESPACE"

# Fonctions utilitaires
check_deployment_status() {
    echo "Checking deployment status..."
    kubectl rollout status deployment/nodejs-app -n $NAMESPACE --timeout=300s
}

run_health_check() {
    echo "Running health check..."
    # Votre script de health check ici
}

# Déploiement principal
case $ENVIRONMENT in
    "dev")
        # Déploiement développement
        ;;
    "staging")
        # Déploiement staging avec tests
        ;;
    "prod")
        # Déploiement production avec validations
        ;;
    *)
        echo "Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "Deployment completed successfully!"
```

### Étape 4.2 : Script de rollback

Créez `scripts/rollback.sh` :

```bash
#!/bin/bash

set -e

ENVIRONMENT=${1:-dev}
REVISION=${2:-}
NAMESPACE="nodejs-app-$ENVIRONMENT"

echo "Rolling back $ENVIRONMENT environment..."

# Votre logique de rollback ici
```

## Exercice 5 : Stratégies de déploiement avancées

### Étape 5.1 : Blue/Green deployment

Créez la configuration pour blue/green :

```yaml
# blue-green-deployment.yaml
# - Service principal pointant vers blue ou green
# - Deployments séparés pour blue et green
# - Script de switch entre les versions
```

### Étape 5.2 : Canary deployment

Implémentez un déploiement canary :

```yaml
# canary-deployment.yaml
# - Deployment canary avec peu de replicas
# - Service avec répartition de trafic
# - Monitoring des métriques canary
```

### Étape 5.3 : Istio pour traffic splitting

Si Istio est disponible :

```yaml
# istio-traffic-split.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: nodejs-app
spec:
  http:
    - match:
        - headers:
            canary:
              exact: 'true'
      route:
        - destination:
            host: nodejs-app
            subset: canary
    - route:
        - destination:
            host: nodejs-app
            subset: stable
          weight: 90
        - destination:
            host: nodejs-app
            subset: canary
          weight: 10
```

## Exercice 6 : Tests automatisés

### Étape 6.1 : Tests unitaires

Créez `tests/unit/app.test.js` :

```javascript
const request = require('supertest');
const app = require('../../src/app');

describe('Node.js App', () => {
  test('GET / should return app info', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('message');
    expect(response.body).toHaveProperty('version');
  });

  test('GET /health should return healthy status', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('healthy');
  });

  // Ajoutez plus de tests
});
```

### Étape 6.2 : Tests d'intégration

Créez `tests/integration/k8s.test.js` :

```javascript
// Tests d'intégration pour vérifier le déploiement Kubernetes
const axios = require('axios');

describe('Kubernetes Integration Tests', () => {
  const baseURL = process.env.APP_URL || 'http://localhost:3000';

  test('App should be accessible', async () => {
    // Votre test ici
  });

  test('Health endpoint should work', async () => {
    // Votre test ici
  });

  test('Metrics endpoint should return Prometheus metrics', async () => {
    // Votre test ici
  });
});
```

## Exercice 7 : Monitoring et alerting

### Étape 7.1 : ServiceMonitor pour Prometheus

Créez `k8s/servicemonitor.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: nodejs-app
  labels:
    app: nodejs-app
spec:
  selector:
    matchLabels:
      app: nodejs-app
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

### Étape 7.2 : Alertes Prometheus

Créez `k8s/prometheus-rules.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: nodejs-app-alerts
spec:
  groups:
    - name: nodejs-app.rules
      rules:
        - alert: NodeJSAppDown
          expr: up{job="nodejs-app"} == 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: 'NodeJS App is down'

        - alert: NodeJSAppHighErrorRate
          expr: # Votre expression ici
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: 'High error rate in NodeJS App'
```

## Exercice 8 : Sécurité du pipeline

### Étape 8.1 : Scan de vulnérabilités

Ajoutez au pipeline :

```yaml
security:dependency-check:
  stage: security
  image: owasp/dependency-check:latest
  script:
    - /usr/share/dependency-check/bin/dependency-check.sh --scan . --format XML --out dependency-check-report.xml
  artifacts:
    reports:
      dependency_scanning: dependency-check-report.xml
```

### Étape 8.2 : Validation des manifestes

```yaml
security:k8s-manifest-validation:
  stage: security
  image: aquasec/kube-bench:latest
  script:
    # Validation des manifestes Kubernetes
```

## Exercice 9 : GitOps avec ArgoCD

### Étape 9.1 : Repository GitOps

Créez un repository séparé pour GitOps :

```
gitops-nodejs-app/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── applications/
    └── nodejs-app.yaml
```

### Étape 9.2 : Application ArgoCD

Créez `applications/nodejs-app.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nodejs-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://gitlab.com/your-org/gitops-nodejs-app.git
    targetRevision: HEAD
    path: environments/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: nodejs-app-prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Exercice 10 : Cas pratique complet

Implémentez un pipeline complet qui :

1. **Build** : Compile l'application et créé l'image Docker
2. **Test** : Exécute tests unitaires et d'intégration
3. **Security** : Scan de sécurité et validation
4. **Deploy Dev** : Déploiement automatique en dev
5. **Deploy Staging** : Déploiement manuel en staging
6. **Tests E2E** : Tests end-to-end en staging
7. **Deploy Prod** : Déploiement manuel en production
8. **Monitoring** : Vérification des métriques post-déploiement
9. **Rollback** : Procédure automatique de rollback si échec

## Questions de validation

1. Comment gérer les secrets sensibles dans GitLab CI/CD ?
2. Quelle est la différence entre les stratégies de déploiement blue/green et canary ?
3. Comment déboguer un échec de déploiement Kubernetes ?
4. Comment implémenter un rollback automatique basé sur les métriques ?

## Livrables attendus

1. **Application Node.js** complète avec métriques
2. **Dockerfile** multi-stage optimisé
3. **Pipeline GitLab CI/CD** complet
4. **Manifestes Kubernetes** pour tous les environnements
5. **Scripts de déploiement** et rollback
6. **Tests automatisés** (unitaires et intégration)
7. **Configuration monitoring** (ServiceMonitor, alertes)
8. **Documentation** du processus CI/CD
9. **Stratégies de déploiement** avancées implémentées

## Critères d'évaluation

- **Automatisation** : Pipeline entièrement automatisé
- **Sécurité** : Scans de sécurité et validation des images
- **Qualité** : Tests complets et coverage > 80%
- **Monitoring** : Métriques et alertes configurées
- **Résilience** : Stratégies de rollback fonctionnelles
- **Documentation** : Processus bien documenté

## Ressources utiles

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Prometheus Monitoring](https://prometheus.io/docs/)

---

**Durée estimée : 6-7 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
