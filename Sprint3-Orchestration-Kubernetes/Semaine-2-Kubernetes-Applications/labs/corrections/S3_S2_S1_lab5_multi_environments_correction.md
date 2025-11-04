# Correction LAB 5 - Gestion Multi-Environnements

## Vue d'ensemble de la solution

Cette correction présente une architecture complète de gestion multi-environnements pour l'application e-commerce avec isolation des ressources, RBAC granulaire, quotas, et promotion automatisée entre environnements.

## Architecture Multi-Environnements

```
Production Cluster
├── Namespace: ecommerce-prod
├── RBAC: prod-team (read-only pour dev)
├── Quotas: CPU 16 cores, Memory 64Gi
├── Network Policies: Strict isolation
└── Backup/DR: Automated

Staging Cluster
├── Namespace: ecommerce-staging
├── RBAC: staging-team (deploy access)
├── Quotas: CPU 8 cores, Memory 32Gi
├── Network Policies: Moderate isolation
└── Auto-promotion to prod

Development Cluster
├── Namespace: ecommerce-dev
├── RBAC: dev-team (full access)
├── Quotas: CPU 4 cores, Memory 16Gi
├── Network Policies: Relaxed
└── Feature branches deployment
```

## Étape 1 : Création des namespaces avec isolation

### 1.1 Namespaces avec labels et annotations

```yaml
# namespaces-multi-env.yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-dev
  labels:
    environment: development
    team: ecommerce
    tier: development
    cost-center: dev-team
    monitoring: enabled
  annotations:
    contact: 'dev-team@ecommerce.com'
    description: 'Development environment for e-commerce application'
    deployment-policy: 'automatic'
    backup-policy: 'daily'
    retention-policy: '7-days'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-staging
  labels:
    environment: staging
    team: ecommerce
    tier: pre-production
    cost-center: qa-team
    monitoring: enabled
  annotations:
    contact: 'qa-team@ecommerce.com'
    description: 'Staging environment for e-commerce application'
    deployment-policy: 'manual-approval'
    backup-policy: 'daily'
    retention-policy: '30-days'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-prod
  labels:
    environment: production
    team: ecommerce
    tier: production
    cost-center: sre-team
    monitoring: enabled
    compliance: 'required'
  annotations:
    contact: 'sre-team@ecommerce.com'
    description: 'Production environment for e-commerce application'
    deployment-policy: 'strict-approval'
    backup-policy: 'continuous'
    retention-policy: '1-year'
    sla: '99.99'
```

### 1.2 Resource Quotas par environnement

```yaml
# resource-quotas.yaml
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-compute-quota
  namespace: ecommerce-dev
spec:
  hard:
    # Compute resources
    requests.cpu: '4'
    requests.memory: 16Gi
    limits.cpu: '8'
    limits.memory: 32Gi

    # Storage resources
    requests.storage: 100Gi
    persistentvolumeclaims: '10'

    # Object counts
    count/deployments.apps: '20'
    count/services: '15'
    count/secrets: '25'
    count/configmaps: '25'
    count/pods: '50'

    # Network resources
    count/ingresses.networking.k8s.io: '5'
    services.loadbalancers: '2'

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: staging-compute-quota
  namespace: ecommerce-staging
spec:
  hard:
    # Compute resources
    requests.cpu: '8'
    requests.memory: 32Gi
    limits.cpu: '16'
    limits.memory: 64Gi

    # Storage resources
    requests.storage: 500Gi
    persistentvolumeclaims: '20'

    # Object counts
    count/deployments.apps: '30'
    count/services: '25'
    count/secrets: '30'
    count/configmaps: '30'
    count/pods: '100'

    # Network resources
    count/ingresses.networking.k8s.io: '10'
    services.loadbalancers: '3'

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: prod-compute-quota
  namespace: ecommerce-prod
spec:
  hard:
    # Compute resources
    requests.cpu: '16'
    requests.memory: 64Gi
    limits.cpu: '32'
    limits.memory: 128Gi

    # Storage resources
    requests.storage: 2Ti
    persistentvolumeclaims: '50'

    # Object counts
    count/deployments.apps: '50'
    count/services: '40'
    count/secrets: '50'
    count/configmaps: '50'
    count/pods: '200'

    # Network resources
    count/ingresses.networking.k8s.io: '20'
    services.loadbalancers: '10'

---
# Limit Ranges pour contrôler les ressources individuelles
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limit-range
  namespace: ecommerce-dev
spec:
  limits:
    - default:
        cpu: 200m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      max:
        cpu: 1000m
        memory: 2Gi
      min:
        cpu: 50m
        memory: 64Mi
      type: Container
    - max:
        cpu: 2000m
        memory: 4Gi
      min:
        cpu: 100m
        memory: 128Mi
      type: Pod

---
apiVersion: v1
kind: LimitRange
metadata:
  name: staging-limit-range
  namespace: ecommerce-staging
spec:
  limits:
    - default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 200m
        memory: 256Mi
      max:
        cpu: 2000m
        memory: 4Gi
      min:
        cpu: 100m
        memory: 128Mi
      type: Container
    - max:
        cpu: 4000m
        memory: 8Gi
      min:
        cpu: 200m
        memory: 256Mi
      type: Pod

---
apiVersion: v1
kind: LimitRange
metadata:
  name: prod-limit-range
  namespace: ecommerce-prod
spec:
  limits:
    - default:
        cpu: 1000m
        memory: 1Gi
      defaultRequest:
        cpu: 500m
        memory: 512Mi
      max:
        cpu: 4000m
        memory: 8Gi
      min:
        cpu: 200m
        memory: 256Mi
      type: Container
    - max:
        cpu: 8000m
        memory: 16Gi
      min:
        cpu: 500m
        memory: 512Mi
      type: Pod
```

## Étape 2 : Configuration RBAC multi-équipes

### 2.1 Rôles et permissions par environnement

```yaml
# rbac-multi-env.yaml
---
# Developer Role - Accès complet dev, lecture seule staging
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-dev
  name: developer
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['metrics.k8s.io']
    resources: ['*']
    verbs: ['get', 'list']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-staging
  name: developer-readonly
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['metrics.k8s.io']
    resources: ['*']
    verbs: ['get', 'list']

---
# QA Role - Accès complet staging, readonly dev et prod
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-staging
  name: qa-engineer
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['batch']
    resources: ['jobs', 'cronjobs']
    verbs: ['*']
  - apiGroups: ['metrics.k8s.io']
    resources: ['*']
    verbs: ['get', 'list']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-dev
  name: qa-readonly
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['get', 'list', 'watch']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: qa-readonly
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['get', 'list', 'watch']

---
# SRE Role - Accès complet production, deploy staging
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: sre-engineer
rules:
  - apiGroups: ['*']
    resources: ['*']
    verbs: ['*']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-staging
  name: sre-deploy
rules:
  - apiGroups: ['', 'apps', 'extensions', 'networking.k8s.io']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['batch']
    resources: ['*']
    verbs: ['*']

---
# ServiceAccounts
apiVersion: v1
kind: ServiceAccount
metadata:
  name: developer
  namespace: ecommerce-dev

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: qa-engineer
  namespace: ecommerce-staging

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sre-engineer
  namespace: ecommerce-prod

---
# RoleBindings
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: ecommerce-dev
subjects:
  - kind: ServiceAccount
    name: developer
    namespace: ecommerce-dev
  - kind: User
    name: dev-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-staging-readonly
  namespace: ecommerce-staging
subjects:
  - kind: User
    name: dev-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-readonly
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: qa-binding
  namespace: ecommerce-staging
subjects:
  - kind: ServiceAccount
    name: qa-engineer
    namespace: ecommerce-staging
  - kind: User
    name: qa-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: qa-engineer
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sre-prod-binding
  namespace: ecommerce-prod
subjects:
  - kind: ServiceAccount
    name: sre-engineer
    namespace: ecommerce-prod
  - kind: User
    name: sre-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: sre-engineer
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole pour accès cross-namespace monitoring
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-reader
rules:
  - apiGroups: ['']
    resources: ['nodes', 'nodes/metrics', 'services', 'endpoints', 'pods']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['extensions', 'apps']
    resources: ['deployments', 'replicasets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['metrics.k8s.io']
    resources: ['*']
    verbs: ['get', 'list']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: monitoring-binding
subjects:
  - kind: ServiceAccount
    name: prometheus
    namespace: monitoring
roleRef:
  kind: ClusterRole
  name: monitoring-reader
  apiGroup: rbac.authorization.k8s.io
```

### 2.2 Network Policies pour isolation

```yaml
# network-policies.yaml
---
# Dev Environment - Politique permissive pour développement
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: dev-allow-all-internal
  namespace: ecommerce-dev
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-dev
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - namespaceSelector:
            matchLabels:
              name: kube-system
  egress:
    - to: [] # Allow all egress for development

---
# Staging Environment - Politique modérée
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: staging-controlled-access
  namespace: ecommerce-staging
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-staging
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
    - from: []
      ports:
        - protocol: TCP
          port: 8080 # Metrics endpoint
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-staging
    - to: []
      ports:
        - protocol: TCP
          port: 53 # DNS
        - protocol: UDP
          port: 53 # DNS
        - protocol: TCP
          port: 443 # HTTPS externe
        - protocol: TCP
          port: 80 # HTTP externe

---
# Production Environment - Politique stricte
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: prod-strict-isolation
  namespace: ecommerce-prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-prod
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080 # Metrics seulement
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 80 # Application traffic
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-prod
    - to: []
      ports:
        - protocol: TCP
          port: 53
        - protocol: UDP
          port: 53
    - to: []
      ports:
        - protocol: TCP
          port: 443 # HTTPS externe seulement

---
# Politique spécifique pour base de données
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: database-access-policy
  namespace: ecommerce-prod
spec:
  podSelector:
    matchLabels:
      app: postgresql
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 5432

---
# Politique pour services externes autorisés
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: external-services-policy
  namespace: ecommerce-prod
spec:
  podSelector:
    matchLabels:
      access-external: 'true'
  policyTypes:
    - Egress
  egress:
    - to: []
      ports:
        - protocol: TCP
          port: 443
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
```

## Étape 3 : Configuration par environnement avec Kustomize

### 3.1 Structure Kustomize

```yaml
# kustomization/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app: ecommerce
  version: v1.0.0

images:
  - name: ecommerce-app
    newTag: latest
```

### 3.2 Configuration de base

```yaml
# kustomization/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ecommerce-app
  template:
    metadata:
      labels:
        app: ecommerce-app
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
    spec:
      serviceAccountName: ecommerce-sa
      containers:
        - name: app
          image: ecommerce-app:latest
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: ENVIRONMENT
              value: 'base'
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: db.host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: db.password
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5

---
# kustomization/base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: ecommerce-app
spec:
  selector:
    app: ecommerce-app
  ports:
    - name: http
      port: 80
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090

---
# kustomization/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    management.port=9090
    spring.profiles.active=default
  db.host: 'postgresql'
  redis.host: 'redis'
  log.level: 'INFO'
```

### 3.3 Overlay Development

```yaml
# kustomization/overlays/development/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-dev

resources:
  - ../../base
  - namespace.yaml
  - secrets.yaml

patchesStrategicMerge:
  - deployment-patch.yaml
  - configmap-patch.yaml

commonLabels:
  environment: development

images:
  - name: ecommerce-app
    newTag: dev-latest

replicas:
  - name: ecommerce-app
    count: 1

configMapGenerator:
  - name: dev-config
    literals:
      - DEBUG_MODE=true
      - LOG_LEVEL=DEBUG
      - FEATURE_FLAGS=experimental_ui,beta_features

secretGenerator:
  - name: dev-secrets
    literals:
      - DB_PASSWORD=devpassword
      - API_KEY=dev-api-key-12345

---
# kustomization/overlays/development/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
spec:
  template:
    spec:
      containers:
        - name: app
          env:
            - name: ENVIRONMENT
              value: 'development'
            - name: DEBUG
              value: 'true'
            - name: HOT_RELOAD
              value: 'true'
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
          volumeMounts:
            - name: dev-volume
              mountPath: /app/dev
      volumes:
        - name: dev-volume
          emptyDir: {}

---
# kustomization/overlays/development/configmap-patch.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  app.properties: |
    server.port=8080
    management.port=9090
    spring.profiles.active=development
    logging.level.com.ecommerce=DEBUG
    debug=true
    hot-reload=true
  db.host: 'postgresql-dev'
  redis.host: 'redis-dev'
  log.level: 'DEBUG'
```

### 3.4 Overlay Staging

```yaml
# kustomization/overlays/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-staging

resources:
  - ../../base
  - namespace.yaml
  - hpa.yaml
  - pdb.yaml

patchesStrategicMerge:
  - deployment-patch.yaml
  - configmap-patch.yaml

commonLabels:
  environment: staging

images:
  - name: ecommerce-app
    newTag: staging-v1.2.0

replicas:
  - name: ecommerce-app
    count: 3

configMapGenerator:
  - name: staging-config
    literals:
      - ENABLE_METRICS=true
      - CACHE_TTL=300
      - RATE_LIMIT=100

secretGenerator:
  - name: staging-secrets
    literals:
      - DB_PASSWORD=staging-secure-password
      - JWT_SECRET=staging-jwt-secret-key

---
# kustomization/overlays/staging/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
spec:
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
        fluentd.io/include: 'true'
    spec:
      containers:
        - name: app
          env:
            - name: ENVIRONMENT
              value: 'staging'
            - name: ENABLE_PROFILING
              value: 'true'
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi

---
# kustomization/overlays/staging/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ecommerce-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ecommerce-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

---
# kustomization/overlays/staging/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ecommerce-app-pdb
spec:
  selector:
    matchLabels:
      app: ecommerce-app
  minAvailable: 50%
```

### 3.5 Overlay Production

```yaml
# kustomization/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-prod

resources:
  - ../../base
  - namespace.yaml
  - hpa.yaml
  - pdb.yaml
  - ingress.yaml
  - servicemonitor.yaml

patchesStrategicMerge:
  - deployment-patch.yaml
  - configmap-patch.yaml
  - service-patch.yaml

commonLabels:
  environment: production
  tier: production

images:
  - name: ecommerce-app
    newTag: v1.2.0

replicas:
  - name: ecommerce-app
    count: 5

configMapGenerator:
  - name: prod-config
    literals:
      - ENABLE_METRICS=true
      - CACHE_TTL=3600
      - RATE_LIMIT=1000
      - CONNECTION_POOL_SIZE=50

secretGenerator:
  - name: prod-secrets
    literals:
      - DB_PASSWORD=super-secure-prod-password
      - JWT_SECRET=ultra-secure-jwt-secret-production

---
# kustomization/overlays/production/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-app
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%
      maxSurge: 25%
  template:
    metadata:
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
        backup.io/enable: 'true'
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: app
          env:
            - name: ENVIRONMENT
              value: 'production'
            - name: GC_TUNE
              value: 'true'
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
          volumeMounts:
            - name: tmp-volume
              mountPath: /tmp
            - name: app-logs
              mountPath: /app/logs
      volumes:
        - name: tmp-volume
          emptyDir: {}
        - name: app-logs
          emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - ecommerce-app
                topologyKey: kubernetes.io/hostname

---
# kustomization/overlays/production/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-app
  annotations:
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/rate-limit: '100'
spec:
  tls:
    - hosts:
        - ecommerce.production.com
      secretName: ecommerce-tls
  rules:
    - host: ecommerce.production.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ecommerce-app
                port:
                  number: 80
```

## Étape 4 : Promotion automatisée entre environnements

### 4.1 Pipeline GitLab CI/CD multi-environnements

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy-dev
  - test-dev
  - deploy-staging
  - test-staging
  - deploy-prod
  - post-deploy

variables:
  DOCKER_REGISTRY: registry.ecommerce.com
  APP_NAME: ecommerce-app
  KUBE_NAMESPACE_DEV: ecommerce-dev
  KUBE_NAMESPACE_STAGING: ecommerce-staging
  KUBE_NAMESPACE_PROD: ecommerce-prod

build:
  stage: build
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA .
    - docker push $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA
    - docker tag $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA $DOCKER_REGISTRY/$APP_NAME:dev-latest
    - docker push $DOCKER_REGISTRY/$APP_NAME:dev-latest
  only:
    - develop
    - main

unit-tests:
  stage: test
  image: maven:3.9.4-openjdk-17
  script:
    - mvn clean test
    - mvn jacoco:report
  coverage: '/Total.*?([0-9]{1,3})%/'
  artifacts:
    reports:
      junit: target/surefire-reports/TEST-*.xml
      coverage_report:
        coverage_format: cobertura
        path: target/site/jacoco/jacoco.xml

security-scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image --format template --template "@contrib/sarif.tpl"
      -o trivy-results.sarif $DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA
  artifacts:
    reports:
      sast: trivy-results.sarif
  allow_failure: true

deploy-dev:
  stage: deploy-dev
  image: bitnami/kubectl:latest
  environment:
    name: development
    url: https://dev.ecommerce.com
  before_script:
    - kubectl config use-context development
  script:
    - cd kustomization/overlays/development
    - kustomize edit set image ecommerce-app=$DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA
    - kubectl apply -k .
    - kubectl rollout status deployment/ecommerce-app -n $KUBE_NAMESPACE_DEV
    - kubectl get pods -n $KUBE_NAMESPACE_DEV
  only:
    - develop
  when: on_success

test-dev-environment:
  stage: test-dev
  image: curlimages/curl:latest
  needs: ['deploy-dev']
  script:
    - sleep 30 # Attendre le déploiement
    - curl -f https://dev.ecommerce.com/health
    - curl -f https://dev.ecommerce.com/api/products
  retry: 3
  only:
    - develop

deploy-staging:
  stage: deploy-staging
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.ecommerce.com
  before_script:
    - kubectl config use-context staging
  script:
    - cd kustomization/overlays/staging
    - kustomize edit set image ecommerce-app=$DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA
    - kubectl apply -k .
    - kubectl rollout status deployment/ecommerce-app -n $KUBE_NAMESPACE_STAGING
    - kubectl get pods -n $KUBE_NAMESPACE_STAGING
  only:
    - main
  when: manual
  allow_failure: false

integration-tests:
  stage: test-staging
  image: postman/newman:latest
  needs: ['deploy-staging']
  script:
    - newman run tests/integration/postman-collection.json
      --environment tests/integration/staging-environment.json
      --reporters junit,cli
  artifacts:
    reports:
      junit: newman-results.xml
  only:
    - main

performance-tests:
  stage: test-staging
  image: loadimpact/k6:latest
  needs: ['deploy-staging']
  script:
    - k6 run --vus 50 --duration 5m tests/performance/load-test.js
  artifacts:
    reports:
      performance: k6-results.json
  only:
    - main

deploy-production:
  stage: deploy-prod
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://ecommerce.com
  before_script:
    - kubectl config use-context production
  script:
    # Backup before deployment
    - kubectl create backup production-backup-$CI_COMMIT_SHA -n $KUBE_NAMESPACE_PROD

    # Blue-Green deployment strategy
    - cd kustomization/overlays/production
    - kustomize edit set image ecommerce-app=$DOCKER_REGISTRY/$APP_NAME:$CI_COMMIT_SHA

    # Deploy to green environment
    - kubectl apply -k . --dry-run=client
    - kubectl apply -k .
    - kubectl rollout status deployment/ecommerce-app -n $KUBE_NAMESPACE_PROD --timeout=600s

    # Health checks
    - sleep 60
    - kubectl exec -n $KUBE_NAMESPACE_PROD deployment/ecommerce-app -- curl -f http://localhost:8080/health

    # Switch traffic (update ingress)
    - kubectl patch ingress ecommerce-app -n $KUBE_NAMESPACE_PROD -p '{"spec":{"rules":[{"host":"ecommerce.com","http":{"paths":[{"path":"/","pathType":"Prefix","backend":{"service":{"name":"ecommerce-app","port":{"number":80}}}}]}}]}}'

  only:
    - main
  when: manual
  allow_failure: false

smoke-tests-prod:
  stage: post-deploy
  image: curlimages/curl:latest
  needs: ['deploy-production']
  script:
    - sleep 30
    - curl -f https://ecommerce.com/health
    - curl -f https://ecommerce.com/api/health/deep
    - echo "Production deployment successful!"
  only:
    - main

rollback-production:
  stage: post-deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
  script:
    - kubectl rollout undo deployment/ecommerce-app -n $KUBE_NAMESPACE_PROD
    - kubectl rollout status deployment/ecommerce-app -n $KUBE_NAMESPACE_PROD
  when: manual
  only:
    - main
```

### 4.2 Promotion automatique avec ArgoCD

```yaml
# argocd/applications/dev-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-dev
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: ecommerce
  source:
    repoURL: https://git.ecommerce.com/ecommerce-k8s-manifests.git
    targetRevision: develop
    path: kustomization/overlays/development
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

---
# argocd/applications/staging-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-staging
  namespace: argocd
spec:
  project: ecommerce
  source:
    repoURL: https://git.ecommerce.com/ecommerce-k8s-manifests.git
    targetRevision: main
    path: kustomization/overlays/staging
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-staging
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    # Pas de sync automatique pour staging
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas

---
# argocd/applications/prod-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-prod
  namespace: argocd
spec:
  project: ecommerce
  source:
    repoURL: https://git.ecommerce.com/ecommerce-k8s-manifests.git
    targetRevision: v1.2.0 # Tag spécifique pour prod
    path: kustomization/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-prod
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    # Sync manuel uniquement pour production
```

## Étape 5 : Monitoring et observabilité par environnement

### 5.1 Configuration Prometheus multi-environnements

```yaml
# prometheus-multi-env.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-multi-env
  namespace: monitoring
  labels:
    app: ecommerce-monitoring
spec:
  selector:
    matchLabels:
      app: ecommerce-app
  namespaceSelector:
    matchNames:
      - ecommerce-dev
      - ecommerce-staging
      - ecommerce-prod
  endpoints:
    - port: metrics
      interval: 15s
      relabelings:
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: environment
          regex: ecommerce-(.*)
          replacement: ${1}
        - sourceLabels: [__meta_kubernetes_pod_label_version]
          targetLabel: version

---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ecommerce-multi-env-alerts
  namespace: monitoring
spec:
  groups:
    - name: multi-environment
      rules:
        - alert: EnvironmentDown
          expr: up{job="ecommerce-multi-env"} == 0
          for: 1m
          labels:
            severity: critical
            environment: '{{ $labels.environment }}'
          annotations:
            summary: 'Environment {{ $labels.environment }} is down'

        - alert: CrossEnvironmentVersionSkew
          expr: |
            count by (environment) (
              group by (environment, version) (up{job="ecommerce-multi-env"})
            ) > 1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: 'Multiple versions running in {{ $labels.environment }}'

        - alert: ProductionStagingVersionMismatch
          expr: |
            count(
              (up{job="ecommerce-multi-env", environment="production"} 
               unless on(version) up{job="ecommerce-multi-env", environment="staging"})
            ) > 0
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: 'Production running version not tested in staging'
```

### 5.2 Dashboard Grafana multi-environnements

```json
{
  "dashboard": {
    "title": "Multi-Environment Overview",
    "panels": [
      {
        "id": 1,
        "title": "Environment Health Status",
        "type": "stat",
        "targets": [
          {
            "expr": "up{job=\"ecommerce-multi-env\"}",
            "legendFormat": "{{ environment }}"
          }
        ],
        "fieldConfig": {
          "overrides": [
            {
              "matcher": {"id": "byName", "options": "dev"},
              "properties": [
                {
                  "id": "color",
                  "value": {"mode": "fixed", "fixedColor": "blue"}
                }
              ]
            },
            {
              "matcher": {"id": "byName", "options": "staging"},
              "properties": [
                {
                  "id": "color",
                  "value": {"mode": "fixed", "fixedColor": "orange"}
                }
              ]
            },
            {
              "matcher": {"id": "byName", "options": "prod"},
              "properties": [
                {
                  "id": "color",
                  "value": {"mode": "fixed", "fixedColor": "green"}
                }
              ]
            }
          ]
        }
      },
      {
        "id": 2,
        "title": "Request Rate by Environment",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job=\"ecommerce-multi-env\"}[5m])",
            "legendFormat": "{{ environment }} - {{ method }}"
          }
        ]
      },
      {
        "id": 3,
        "title": "Resource Usage by Environment",
        "type": "graph",
        "targets": [
          {
            "expr": "avg by (environment) (container_memory_working_set_bytes{pod=~\"ecommerce-app-.*\"})",
            "legendFormat": "{{ environment }} Memory"
          },
          {
            "expr": "avg by (environment) (rate(container_cpu_usage_seconds_total{pod=~\"ecommerce-app-.*\"}[5m]))",
            "legendFormat": "{{ environment }} CPU"
          }
        ]
      }
    ]
  }
}
```

## Étape 6 : Tests et validation

### 6.1 Script de validation multi-environnements

```bash
# validate-multi-env.sh
#!/bin/bash

echo "🏗️ Validation de l'architecture multi-environnements"

ENVIRONMENTS=("dev" "staging" "prod")

# Test 1: Vérifier les namespaces et quotas
echo "=== Test des namespaces et quotas ==="
for env in "${ENVIRONMENTS[@]}"; do
    echo "Environment: $env"

    # Vérifier namespace
    kubectl get namespace ecommerce-$env || echo "❌ Namespace ecommerce-$env non trouvé"

    # Vérifier quotas
    kubectl describe resourcequota -n ecommerce-$env

    # Vérifier limit ranges
    kubectl describe limitrange -n ecommerce-$env

    echo "---"
done

# Test 2: Vérifier RBAC
echo "=== Test RBAC ==="
kubectl auth can-i create pods --namespace=ecommerce-dev --as=system:serviceaccount:ecommerce-dev:developer
kubectl auth can-i delete deployments --namespace=ecommerce-prod --as=system:serviceaccount:ecommerce-dev:developer
kubectl auth can-i get pods --namespace=ecommerce-staging --as=system:serviceaccount:ecommerce-staging:qa-engineer

# Test 3: Vérifier network policies
echo "=== Test Network Policies ==="
for env in "${ENVIRONMENTS[@]}"; do
    echo "Network policies pour $env:"
    kubectl get networkpolicies -n ecommerce-$env
done

# Test 4: Test de déploiement avec Kustomize
echo "=== Test déploiements Kustomize ==="
for env in "${ENVIRONMENTS[@]}"; do
    echo "Test déploiement $env avec Kustomize..."

    cd kustomization/overlays/$env
    kustomize build . > /tmp/manifest-$env.yaml

    # Validation du manifest
    kubectl apply --dry-run=client -f /tmp/manifest-$env.yaml

    if [ $? -eq 0 ]; then
        echo "✅ Manifest $env valide"
    else
        echo "❌ Erreur dans manifest $env"
    fi

    cd - > /dev/null
done

# Test 5: Test de connectivité réseau
echo "=== Test connectivité réseau ==="

# Déployer pod de test dans chaque environnement
for env in "${ENVIRONMENTS[@]}"; do
    kubectl run network-test-$env --image=busybox:1.35 --rm -i -n ecommerce-$env -- sleep 3600 &
done

sleep 10

# Test connectivité cross-namespace (doit échouer selon les policies)
echo "Test connectivité dev -> staging (doit réussir):"
kubectl exec -n ecommerce-dev network-test-dev -- nslookup ecommerce-app.ecommerce-staging.svc.cluster.local

echo "Test connectivité dev -> prod (doit échouer):"
kubectl exec -n ecommerce-dev network-test-dev -- timeout 5 nc -v ecommerce-app.ecommerce-prod.svc.cluster.local 80

# Nettoyer
for env in "${ENVIRONMENTS[@]}"; do
    kubectl delete pod network-test-$env -n ecommerce-$env --ignore-not-found
done

echo "✅ Tests de validation terminés"
```

### 6.2 Test de promotion entre environnements

```bash
# test-promotion-pipeline.sh
#!/bin/bash

echo "🚀 Test du pipeline de promotion multi-environnements"

# Simuler un changement de code
echo "=== Simulation changement de code ==="
git checkout develop
echo "$(date): New feature added" >> CHANGELOG.md
git add CHANGELOG.md
git commit -m "feat: add new feature for testing promotion"

# Trigger deploy dev (automatique)
echo "=== Déclenchement deploy dev ==="
git push origin develop

# Attendre le déploiement dev
echo "Attente déploiement dev..."
sleep 60

# Vérifier déploiement dev
kubectl rollout status deployment/ecommerce-app -n ecommerce-dev
kubectl get pods -n ecommerce-dev -l app=ecommerce-app

# Test fonctionnel dev
echo "=== Test fonctionnel dev ==="
DEV_URL=$(kubectl get ingress -n ecommerce-dev -o jsonpath='{.items[0].spec.rules[0].host}')
curl -f http://$DEV_URL/health || echo "❌ Health check dev failed"

# Merge vers main pour déclencher staging
echo "=== Promotion vers staging ==="
git checkout main
git merge develop
git push origin main

# Attendre validation manuelle staging
echo "⏳ Déploiement staging nécessite validation manuelle"
echo "Consultez GitLab CI/CD pipeline pour approuver"

# Simulation approbation staging (en réalité via GitLab UI)
read -p "Appuyer sur Entrée quand le déploiement staging est approuvé..."

# Vérifier déploiement staging
kubectl rollout status deployment/ecommerce-app -n ecommerce-staging
kubectl get pods -n ecommerce-staging -l app=ecommerce-app

# Test fonctionnel staging
echo "=== Test fonctionnel staging ==="
STAGING_URL=$(kubectl get ingress -n ecommerce-staging -o jsonpath='{.items[0].spec.rules[0].host}')
curl -f https://$STAGING_URL/health || echo "❌ Health check staging failed"

# Tests d'intégration staging
echo "=== Tests d'intégration staging ==="
newman run tests/integration/postman-collection.json \
  --environment tests/integration/staging-environment.json

# Tag pour production si tests OK
if [ $? -eq 0 ]; then
    echo "✅ Tests staging réussis, création du tag pour production"
    git tag -a v1.2.0 -m "Release v1.2.0 - ready for production"
    git push origin v1.2.0

    echo "⏳ Déploiement production nécessite validation manuelle"
    echo "Utilisez le tag v1.2.0 pour déployer en production"
else
    echo "❌ Tests staging échoués, pas de promotion vers production"
    exit 1
fi

echo "🏁 Pipeline de promotion testé avec succès"
```

## Points clés de la solution

### 🏗️ Architecture multi-environnements

- **Isolation complète**: Namespaces dédiés avec quotas et limit ranges
- **RBAC granulaire**: Permissions spécifiques par équipe et environnement
- **Network policies**: Isolation réseau progressive (permissive → stricte)
- **Configuration par environnement**: Kustomize overlays pour personnalisation

### 🔄 Promotion automatisée

- **GitOps workflow**: ArgoCD pour déploiements déclaratifs
- **Pipeline CI/CD**: Validation automatique et promotion conditionnelle
- **Gating strategy**: Tests obligatoires entre environnements
- **Rollback capability**: Retour arrière rapide en cas de problème

### 📊 Observabilité centralisée

- **Monitoring unifié**: Métriques agrégées multi-environnements
- **Alerting contextualisé**: Alertes spécifiques par environnement
- **Dashboards comparatifs**: Vue globale des performances
- **Audit trail**: Traçabilité des déploiements et modifications

Cette correction fournit une solution complète et production-ready pour la gestion d'applications Kubernetes dans un contexte multi-environnements d'entreprise.
