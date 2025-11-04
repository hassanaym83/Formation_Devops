# LAB 10 - Projet d'intégration finale

## Objectif

Intégrer tous les concepts appris pour déployer une application e-commerce complète en production avec toutes les bonnes pratiques DevOps et Kubernetes.

## Contexte

Créer un déploiement production-ready incluant :

- Architecture micro-services complète
- Pipeline CI/CD automatisé
- Monitoring, logging et observabilité
- Sécurité multi-couches
- Haute disponibilité et disaster recovery
- Optimisation des performances
- Documentation opérationnelle

## Prérequis

- Cluster Kubernetes production (multi-nœuds)
- Accès à un registry privé
- Environnement CI/CD (GitLab CI/Jenkins)
- Monitoring stack (Prometheus/Grafana)
- Outils de sécurité installés

## Architecture finale

L'application comprendra :

```
├── Frontend (React/Next.js)
├── API Gateway (NGINX/Kong)
├── Services Backend
│   ├── User Service (Authentification)
│   ├── Product Service (Catalogue)
│   ├── Order Service (Commandes)
│   ├── Payment Service (Paiements)
│   └── Notification Service (Emails/SMS)
├── Bases de données
│   ├── PostgreSQL (Données relationnelles)
│   ├── Redis (Cache/Sessions)
│   └── MinIO (Stockage fichiers)
└── Services support
    ├── RabbitMQ (Messages)
    ├── Elasticsearch (Logs)
    └── Jaeger (Tracing)
```

## Instructions détaillées

### Étape 1 : Architecture et planification

1. Créer la structure des namespaces et environnements :

```yaml
# namespace-structure.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-prod
  labels:
    environment: production
    project: ecommerce
    pod-security.kubernetes.io/enforce: restricted
    network-policy: enabled
  annotations:
    scheduler.alpha.kubernetes.io/node-selector: 'environment=production'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-staging
  labels:
    environment: staging
    project: ecommerce
    pod-security.kubernetes.io/enforce: restricted
    network-policy: enabled

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-monitoring
  labels:
    purpose: monitoring
    project: ecommerce

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-logging
  labels:
    purpose: logging
    project: ecommerce

---
# ResourceQuotas pour chaque environnement
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: ecommerce-prod
spec:
  hard:
    requests.cpu: '8'
    requests.memory: 16Gi
    limits.cpu: '16'
    limits.memory: 32Gi
    persistentvolumeclaims: '10'
    services: '20'
    secrets: '20'
    configmaps: '20'

---
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: ecommerce-prod
spec:
  limits:
    - default:
        cpu: '500m'
        memory: '512Mi'
      defaultRequest:
        cpu: '100m'
        memory: '128Mi'
      type: Container
    - max:
        cpu: '2'
        memory: '2Gi'
      min:
        cpu: '50m'
        memory: '64Mi'
      type: Container
```

### Étape 2 : Services Backend avec Helm Charts

2. Créer les Helm Charts pour tous les services :

```yaml
# helm-chart-values-prod.yaml
global:
  imageRegistry: registry.company.com/ecommerce
  environment: production
  domain: ecommerce.company.com

  database:
    host: postgres-cluster.ecommerce-prod.svc.cluster.local
    port: 5432

  redis:
    host: redis-cluster.ecommerce-prod.svc.cluster.local
    port: 6379

  messaging:
    rabbitmq:
      host: rabbitmq.ecommerce-prod.svc.cluster.local
      port: 5672

# User Service
userService:
  enabled: true
  replicaCount: 3
  image:
    repository: user-service
    tag: 'v2.1.0'
  resources:
    requests:
      memory: '256Mi'
      cpu: '200m'
    limits:
      memory: '512Mi'
      cpu: '500m'
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPU: 70
    targetMemory: 80
  service:
    type: ClusterIP
    port: 8080
  ingress:
    enabled: true
    path: /api/users
    annotations:
      nginx.ingress.kubernetes.io/rate-limit: '100'
      nginx.ingress.kubernetes.io/auth-jwt: 'true'

# Product Service
productService:
  enabled: true
  replicaCount: 5
  image:
    repository: product-service
    tag: 'v2.1.0'
  resources:
    requests:
      memory: '384Mi'
      cpu: '300m'
    limits:
      memory: '768Mi'
      cpu: '600m'
  autoscaling:
    enabled: true
    minReplicas: 5
    maxReplicas: 20
    targetCPU: 60
  service:
    type: ClusterIP
    port: 8080
  ingress:
    enabled: true
    path: /api/products
    annotations:
      nginx.ingress.kubernetes.io/rate-limit: '200'
      nginx.ingress.kubernetes.io/enable-cors: 'true'

# Order Service
orderService:
  enabled: true
  replicaCount: 4
  image:
    repository: order-service
    tag: 'v2.1.0'
  resources:
    requests:
      memory: '512Mi'
      cpu: '400m'
    limits:
      memory: '1Gi'
      cpu: '800m'
  autoscaling:
    enabled: true
    minReplicas: 4
    maxReplicas: 15
    targetCPU: 65
  service:
    type: ClusterIP
    port: 8080
  ingress:
    enabled: true
    path: /api/orders
    annotations:
      nginx.ingress.kubernetes.io/auth-jwt: 'true'
      nginx.ingress.kubernetes.io/rate-limit: '50'

# Payment Service (service critique)
paymentService:
  enabled: true
  replicaCount: 3
  image:
    repository: payment-service
    tag: 'v2.1.0'
  resources:
    requests:
      memory: '256Mi'
      cpu: '200m'
    limits:
      memory: '512Mi'
      cpu: '400m'
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 8
    targetCPU: 50 # Plus conservateur pour les paiements
  service:
    type: ClusterIP
    port: 8080
  ingress:
    enabled: true
    path: /api/payments
    annotations:
      nginx.ingress.kubernetes.io/auth-jwt: 'true'
      nginx.ingress.kubernetes.io/rate-limit: '20'
      nginx.ingress.kubernetes.io/ssl-redirect: 'true'
  networkPolicy:
    enabled: true
    allowedServices:
      - order-service
      - user-service

# Frontend
frontend:
  enabled: true
  replicaCount: 4
  image:
    repository: frontend
    tag: 'v2.1.0'
  resources:
    requests:
      memory: '128Mi'
      cpu: '100m'
    limits:
      memory: '256Mi'
      cpu: '200m'
  autoscaling:
    enabled: true
    minReplicas: 4
    maxReplicas: 20
    targetCPU: 70
  service:
    type: ClusterIP
    port: 80
  ingress:
    enabled: true
    host: ecommerce.company.com
    annotations:
      cert-manager.io/cluster-issuer: 'letsencrypt-prod'
      nginx.ingress.kubernetes.io/ssl-redirect: 'true'
```

### Étape 3 : Pipeline CI/CD GitLab

3. Créer un pipeline complet avec GitLab CI :

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security-scan
  - build
  - deploy-staging
  - integration-tests
  - deploy-production
  - post-deploy-tests

variables:
  DOCKER_REGISTRY: registry.company.com
  NAMESPACE_STAGING: ecommerce-staging
  NAMESPACE_PROD: ecommerce-prod
  HELM_CHART_VERSION: $CI_COMMIT_SHA

# Tests unitaires et qualité code
unit-tests:
  stage: test
  image: node:18-alpine
  services:
    - postgres:13
    - redis:7
  before_script:
    - npm install
  script:
    - npm run test:unit
    - npm run test:coverage
    - npm run lint
    - npm run security-audit
  coverage: '/Coverage: \d+\.\d+%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: test-results.xml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

# Scan de sécurité des dépendances
dependency-scan:
  stage: security-scan
  image: aquasec/trivy:latest
  script:
    - trivy fs --format template --template "@contrib/gitlab.tpl" -o gl-dependency-scanning-report.json .
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

# Build et scan des images Docker
build-and-scan:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  variables:
    DOCKER_TLS_CERTDIR: '/certs'
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # Build multi-service
    - |
      for service in frontend user-service product-service order-service payment-service; do
        echo "Building $service..."
        
        # Build de l'image
        docker build -t $DOCKER_REGISTRY/ecommerce/$service:$CI_COMMIT_SHA \
          -f services/$service/Dockerfile services/$service/
        
        # Scan de sécurité Trivy
        trivy image --exit-code 1 --severity CRITICAL,HIGH $DOCKER_REGISTRY/ecommerce/$service:$CI_COMMIT_SHA
        
        # Push si scan OK
        docker push $DOCKER_REGISTRY/ecommerce/$service:$CI_COMMIT_SHA
        
        # Tag latest pour main
        if [ "$CI_COMMIT_BRANCH" = "main" ]; then
          docker tag $DOCKER_REGISTRY/ecommerce/$service:$CI_COMMIT_SHA $DOCKER_REGISTRY/ecommerce/$service:latest
          docker push $DOCKER_REGISTRY/ecommerce/$service:latest
        fi
      done
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# Déploiement Staging
deploy-staging:
  stage: deploy-staging
  image: alpine/helm:latest
  environment:
    name: staging
    url: https://staging.ecommerce.company.com
  before_script:
    - kubectl config use-context staging-cluster
  script:
    - |
      # Mise à jour des dépendances Helm
      helm dependency update helm/ecommerce

      # Déploiement avec les valeurs staging
      helm upgrade --install ecommerce-staging helm/ecommerce \
        --namespace $NAMESPACE_STAGING \
        --values helm/ecommerce/values-staging.yaml \
        --set global.imageTag=$CI_COMMIT_SHA \
        --set global.environment=staging \
        --wait --timeout=10m

      # Vérification du déploiement
      kubectl rollout status deployment -n $NAMESPACE_STAGING
      kubectl get pods -n $NAMESPACE_STAGING
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# Tests d'intégration sur staging
integration-tests:
  stage: integration-tests
  image: postman/newman:latest
  dependencies:
    - deploy-staging
  script:
    - |
      # Attendre que tous les services soient prêts
      sleep 60

      # Tests API avec Newman/Postman
      newman run tests/api-tests.postman_collection.json \
        --env-var baseUrl=https://staging.ecommerce.company.com \
        --reporters cli,junit --reporter-junit-export results.xml

      # Tests de performance avec k6
      docker run --rm -i grafana/k6 run - < tests/load-test.js
  artifacts:
    reports:
      junit: results.xml
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# Déploiement Production (manuel)
deploy-production:
  stage: deploy-production
  image: alpine/helm:latest
  environment:
    name: production
    url: https://ecommerce.company.com
  before_script:
    - kubectl config use-context production-cluster
  script:
    - |
      # Backup avant déploiement
      kubectl create job pre-deploy-backup-$(date +%s) \
        --from=cronjob/database-backup -n $NAMESPACE_PROD

      # Déploiement Blue/Green
      CURRENT_VERSION=$(helm get values ecommerce-prod --namespace $NAMESPACE_PROD | grep imageTag | cut -d'"' -f2)

      # Déploiement de la nouvelle version
      helm upgrade --install ecommerce-prod helm/ecommerce \
        --namespace $NAMESPACE_PROD \
        --values helm/ecommerce/values-production.yaml \
        --set global.imageTag=$CI_COMMIT_SHA \
        --set global.environment=production \
        --wait --timeout=15m

      # Vérification des health checks
      ./scripts/health-check.sh $NAMESPACE_PROD

      # Si échec, rollback automatique
      if [ $? -ne 0 ]; then
        echo "Health check failed, rolling back..."
        helm rollback ecommerce-prod -n $NAMESPACE_PROD
        exit 1
      fi
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

# Tests post-déploiement production
post-deploy-tests:
  stage: post-deploy-tests
  image: curlimages/curl:latest
  dependencies:
    - deploy-production
  script:
    - |
      # Tests de smoke sur la production
      echo "Running smoke tests on production..."

      # Test de base
      curl -f https://ecommerce.company.com/health

      # Tests critiques
      curl -f https://ecommerce.company.com/api/products?limit=1
      curl -f https://ecommerce.company.com/api/users/health

      # Vérification des métriques
      curl -f https://ecommerce.company.com/metrics

      echo "All smoke tests passed!"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Étape 4 : Monitoring et observabilité complète

4. Stack de monitoring complète :

```yaml
# monitoring-stack.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: ecommerce-monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    rule_files:
      - "/etc/prometheus/rules/*.yml"

    alerting:
      alertmanagers:
      - static_configs:
        - targets:
          - alertmanager:9093

    scrape_configs:
    # Métriques Kubernetes
    - job_name: 'kubernetes-apiservers'
      kubernetes_sd_configs:
      - role: endpoints
      scheme: https
      tls_config:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

    # Services ecommerce
    - job_name: 'ecommerce-services'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['ecommerce-prod', 'ecommerce-staging']
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

    # PostgreSQL
    - job_name: 'postgresql'
      static_configs:
      - targets: ['postgres-exporter:9187']
      
    # Redis
    - job_name: 'redis'
      static_configs:
      - targets: ['redis-exporter:9121']

    # NGINX Ingress
    - job_name: 'nginx-ingress'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['ingress-nginx']
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app_kubernetes_io_name]
        action: keep
        regex: ingress-nginx

---
# Règles d'alerting spécifiques e-commerce
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-rules
  namespace: ecommerce-monitoring
data:
  ecommerce-alerts.yml: |
    groups:
    - name: ecommerce.rules
      rules:
      # SLI/SLO pour l'e-commerce
      - alert: HighErrorRate
        expr: |
          (
            rate(http_requests_total{job=~"ecommerce-.*", code=~"5.."}[5m]) /
            rate(http_requests_total{job=~"ecommerce-.*"}[5m])
          ) > 0.05
        for: 2m
        labels:
          severity: critical
          service: "{{ $labels.job }}"
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.job }}"
      
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            rate(http_request_duration_seconds_bucket{job=~"ecommerce-.*"}[5m])
          ) > 0.5
        for: 5m
        labels:
          severity: warning
          service: "{{ $labels.job }}"
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s for {{ $labels.job }}"
      
      - alert: PaymentServiceDown
        expr: up{job="payment-service"} == 0
        for: 30s
        labels:
          severity: critical
          service: payment
        annotations:
          summary: "Payment service is down"
          description: "Payment service has been down for more than 30 seconds"
      
      - alert: DatabaseConnectionHigh
        expr: pg_stat_activity_count > 80
        for: 5m
        labels:
          severity: warning
          service: database
        annotations:
          summary: "High database connections"
          description: "Database has {{ $value }} active connections"
      
      - alert: MemoryUsageHigh
        expr: |
          (
            container_memory_working_set_bytes{pod=~"ecommerce-.*"} /
            container_spec_memory_limit_bytes{pod=~"ecommerce-.*"}
          ) > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Pod {{ $labels.pod }} memory usage is {{ $value | humanizePercentage }}"

---
# Configuration AlertManager
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: ecommerce-monitoring
data:
  alertmanager.yml: |
    global:
      smtp_smarthost: 'smtp.company.com:587'
      smtp_from: 'alerts@company.com'

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
      - match:
          service: payment
        receiver: 'payment-team'

    receivers:
    - name: 'web.hook'
      slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#ecommerce-alerts'
        title: 'Kubernetes Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

    - name: 'critical-alerts'
      email_configs:
      - to: 'oncall@company.com'
        subject: '[CRITICAL] {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
      pagerduty_configs:
      - service_key: 'YOUR-PAGERDUTY-KEY'

    - name: 'payment-team'
      email_configs:
      - to: 'payment-team@company.com'
        subject: '[PAYMENT] {{ .GroupLabels.alertname }}'
```

### Étape 5 : Tests de charge et performance

5. Suite complète de tests de performance :

```javascript
// tests/load-test.js - Test K6
import http from 'k6/http';
import {check, sleep} from 'k6';
import {Rate, Trend} from 'k6/metrics';

// Métriques personnalisées
const errorRate = new Rate('errors');
const checkoutTrend = new Trend('checkout_duration');

export const options = {
  stages: [
    {duration: '2m', target: 10}, // Montée progressive
    {duration: '5m', target: 50}, // Charge normale
    {duration: '2m', target: 100}, // Pic de charge
    {duration: '5m', target: 100}, // Sustain peak
    {duration: '2m', target: 0} // Descente
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% sous 500ms
    errors: ['rate<0.05'], // Moins de 5% d'erreurs
    checkout_duration: ['p(95)<2000'] // Checkout sous 2s
  }
};

const BASE_URL = 'https://ecommerce.company.com';

export function setup() {
  // Créer un utilisateur de test
  const authResponse = http.post(`${BASE_URL}/api/auth/register`, {
    email: `test-${Date.now()}@example.com`,
    password: 'testpass123',
    firstName: 'Test',
    lastName: 'User'
  });

  return {
    token: authResponse.json('token'),
    userId: authResponse.json('userId')
  };
}

export default function (data) {
  const headers = {
    Authorization: `Bearer ${data.token}`,
    'Content-Type': 'application/json'
  };

  // Test 1: Browse products
  let response = http.get(`${BASE_URL}/api/products?page=1&limit=20`);
  check(response, {
    'products loaded': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200
  }) || errorRate.add(1);

  sleep(1);

  // Test 2: View product details
  const productId = Math.floor(Math.random() * 1000) + 1;
  response = http.get(`${BASE_URL}/api/products/${productId}`);
  check(response, {
    'product details loaded': (r) => r.status === 200
  }) || errorRate.add(1);

  sleep(1);

  // Test 3: Add to cart
  response = http.post(
    `${BASE_URL}/api/cart/add`,
    JSON.stringify({
      productId: productId,
      quantity: 1
    }),
    {headers}
  );
  check(response, {
    'added to cart': (r) => r.status === 200
  }) || errorRate.add(1);

  // Test 4: Checkout process (plus lourd)
  if (Math.random() < 0.3) {
    // 30% font un checkout
    const checkoutStart = Date.now();

    // Get cart
    response = http.get(`${BASE_URL}/api/cart`, {headers});
    check(response, {'cart retrieved': (r) => r.status === 200});

    // Create order
    response = http.post(
      `${BASE_URL}/api/orders`,
      JSON.stringify({
        items: [{productId: productId, quantity: 1, price: 29.99}],
        paymentMethod: 'credit_card',
        shippingAddress: {
          street: '123 Test St',
          city: 'Test City',
          zip: '12345'
        }
      }),
      {headers}
    );

    const checkoutSuccess = check(response, {
      'order created': (r) => r.status === 201
    });

    if (!checkoutSuccess) errorRate.add(1);

    const checkoutDuration = Date.now() - checkoutStart;
    checkoutTrend.add(checkoutDuration);
  }

  sleep(2);
}

export function teardown(data) {
  // Cleanup: delete test user
  http.del(`${BASE_URL}/api/users/${data.userId}`, {
    headers: {Authorization: `Bearer ${data.token}`}
  });
}
```

### Étape 6 : Documentation opérationnelle

6. Créer la documentation complète :

````markdown
# Guide Opérationnel E-commerce

## Architecture de Production

### Vue d'ensemble

- **Namespaces**: `ecommerce-prod`, `ecommerce-staging`, `ecommerce-monitoring`
- **Services**: 5 micro-services + frontend
- **Bases de données**: PostgreSQL (HA), Redis Cluster, MinIO
- **Monitoring**: Prometheus/Grafana/AlertManager
- **Logging**: ELK Stack
- **Sécurité**: RBAC, NetworkPolicies, Pod Security Standards

### Procédures Opérationnelles

#### Déploiement

1. **Staging**: Automatique via GitLab CI sur `main`
2. **Production**: Manuel après validation staging
3. **Rollback**: `helm rollback ecommerce-prod`

#### Monitoring

- **Dashboards**: https://grafana.company.com/d/ecommerce
- **Alertes**: Slack #ecommerce-alerts + PagerDuty
- **SLOs**:
  - Availability: 99.9%
  - Error Rate: < 0.1%
  - Latency P95: < 500ms

#### Incident Response

1. **Alertes critiques**: Escalade automatique PagerDuty
2. **Procédure**: Voir playbook incidents
3. **Communication**: Slack + Status page
4. **Post-mortem**: Obligatoire pour severity 1-2

### Commandes Utiles

```bash
# Status général
kubectl get all -n ecommerce-prod

# Logs d'un service
kubectl logs -f deployment/user-service -n ecommerce-prod

# Scaler manuellement
kubectl scale deployment order-service --replicas=10 -n ecommerce-prod

# Accès à la base de données
kubectl exec -it postgres-0 -n ecommerce-prod -- psql -U postgres ecommerce

# Backup manuel
kubectl create job backup-$(date +%s) --from=cronjob/database-backup -n ecommerce-prod

# Métriques en live
kubectl top pods -n ecommerce-prod
```
````

### Troubleshooting

#### Pod en CrashLoopBackOff

```bash
kubectl describe pod <pod-name> -n ecommerce-prod
kubectl logs <pod-name> -n ecommerce-prod --previous
```

#### Performance dégradée

1. Vérifier les métriques Grafana
2. Analyser les logs avec Kibana
3. Vérifier les ressources: `kubectl top nodes`
4. Analyser les requêtes DB lentes

#### Indisponibilité service

1. Vérifier les NetworkPolicies
2. Tester la connectivité inter-pods
3. Vérifier les secrets et ConfigMaps
4. Analyser les health checks

````

## Critères de validation finale

- [ ] Application complète déployée en production
- [ ] Pipeline CI/CD fonctionnel avec tests
- [ ] Monitoring et alerting opérationnels
- [ ] Sécurité multi-niveaux implémentée
- [ ] Tests de performance validés
- [ ] Haute disponibilité démontrée
- [ ] Procedures de backup/restore testées
- [ ] Documentation opérationnelle complète
- [ ] Formation équipe ops réalisée
- [ ] Plan de disaster recovery validé

## Tests de validation finale

```bash
# 1. Déploiement complet
helm upgrade --install ecommerce-prod ./helm/ecommerce \
  --namespace ecommerce-prod --create-namespace \
  --values ./helm/ecommerce/values-production.yaml

# 2. Tests de santé
./scripts/health-check-all.sh

# 3. Tests de charge
k6 run tests/load-test.js

# 4. Tests de sécurité
./scripts/security-audit.sh

# 5. Tests de disaster recovery
./scripts/test-disaster-recovery.sh

# 6. Validation SLOs
curl -s "http://prometheus:9090/api/v1/query?query=slo_compliance" | jq
````

## Livrables finaux

1. **Code source** avec tous les services
2. **Helm Charts** pour déploiement
3. **Pipeline CI/CD** GitLab configuré
4. **Stack monitoring** complète
5. **Documentation technique** et opérationnelle
6. **Tests automatisés** (unit, integration, performance)
7. **Procedures d'incident** et runbooks
8. **Plan de formation** équipe

## Durée estimée

120 minutes (2h)

## Présentation finale

Préparer une présentation de 15 minutes couvrant :

- Architecture technique
- Choix de conception
- Métriques de performance
- Leçons apprises
- Recommandations pour la suite
