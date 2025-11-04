# LAB 5 - Multi-Environment Management

## Objectif

Configurer une gestion multi-environnements avec isolation complète et quotas de ressources.

## Contexte

Créer une architecture dev/staging/production avec :

- Isolation par namespaces avec RBAC
- Resource quotas et limits différenciés
- Configuration spécifique par environnement
- Pipeline de promotion entre environnements
- Monitoring séparé par environnement

## Prérequis

- Cluster Kubernetes avec RBAC activé
- Application e-commerce fonctionnelle
- kubectl configuré avec droits admin

## Instructions détaillées

### Étape 1 : Créer les namespaces avec labels

1. Créer les namespaces pour chaque environnement :

```yaml
# environments-namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-dev
  labels:
    environment: development
    team: ecommerce
    cost-center: engineering

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-staging
  labels:
    environment: staging
    team: ecommerce
    cost-center: engineering

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-prod
  labels:
    environment: production
    team: ecommerce
    cost-center: business
```

### Étape 2 : Configurer Resource Quotas par environnement

2. Créer des quotas adaptés à chaque environnement :

```yaml
# dev-resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: ecommerce-dev
spec:
  hard:
    requests.cpu: '2'
    requests.memory: 4Gi
    limits.cpu: '4'
    limits.memory: 8Gi
    pods: '10'
    persistentvolumeclaims: '3'
    services: '5'
    secrets: '10'
    configmaps: '10'
    count/deployments.apps: '5'

---
# staging-resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: staging-quota
  namespace: ecommerce-staging
spec:
  hard:
    requests.cpu: '4'
    requests.memory: 8Gi
    limits.cpu: '8'
    limits.memory: 16Gi
    pods: '20'
    persistentvolumeclaims: '5'
    services: '10'
    secrets: '15'
    configmaps: '15'
    count/deployments.apps: '8'

---
# prod-resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: prod-quota
  namespace: ecommerce-prod
spec:
  hard:
    requests.cpu: '8'
    requests.memory: 16Gi
    limits.cpu: '16'
    limits.memory: 32Gi
    pods: '50'
    persistentvolumeclaims: '10'
    services: '20'
    secrets: '20'
    configmaps: '20'
    count/deployments.apps: '15'
```

### Étape 3 : Configurer LimitRanges par environnement

3. Définir des limits par défaut pour chaque environnement :

```yaml
# dev-limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: ecommerce-dev
spec:
  limits:
    - default:
        cpu: 200m
        memory: 256Mi
      defaultRequest:
        cpu: 50m
        memory: 64Mi
      max:
        cpu: 500m
        memory: 512Mi
      min:
        cpu: 10m
        memory: 32Mi
      type: Container
    - max:
        storage: 1Gi
      min:
        storage: 100Mi
      type: PersistentVolumeClaim

---
# staging-limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: staging-limits
  namespace: ecommerce-staging
spec:
  limits:
    - default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      max:
        cpu: 1
        memory: 1Gi
      min:
        cpu: 50m
        memory: 64Mi
      type: Container
    - max:
        storage: 5Gi
      min:
        storage: 500Mi
      type: PersistentVolumeClaim

---
# prod-limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: prod-limits
  namespace: ecommerce-prod
spec:
  limits:
    - default:
        cpu: 1
        memory: 1Gi
      defaultRequest:
        cpu: 250m
        memory: 256Mi
      max:
        cpu: 2
        memory: 4Gi
      min:
        cpu: 100m
        memory: 128Mi
      type: Container
    - max:
        storage: 20Gi
      min:
        storage: 1Gi
      type: PersistentVolumeClaim
```

### Étape 4 : Créer configurations spécifiques par environnement

4. Créer des ConfigMaps différenciées :

```yaml
# dev-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ecommerce-dev
data:
  DATABASE_URL: 'postgresql://dev-user:dev-pass@postgres-dev:5432/ecommerce_dev'
  REDIS_URL: 'redis://redis-dev:6379/0'
  LOG_LEVEL: 'debug'
  ENVIRONMENT: 'development'
  REPLICAS: '1'
  ENABLE_DEBUG: 'true'
  API_RATE_LIMIT: '1000'
  SESSION_TIMEOUT: '3600'

---
# staging-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ecommerce-staging
data:
  DATABASE_URL: 'postgresql://staging-user:staging-pass@postgres-staging:5432/ecommerce_staging'
  REDIS_URL: 'redis://redis-staging:6379/0'
  LOG_LEVEL: 'info'
  ENVIRONMENT: 'staging'
  REPLICAS: '2'
  ENABLE_DEBUG: 'false'
  API_RATE_LIMIT: '500'
  SESSION_TIMEOUT: '7200'

---
# prod-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ecommerce-prod
data:
  DATABASE_URL: 'postgresql://prod-user:prod-pass@postgres-prod:5432/ecommerce_production'
  REDIS_URL: 'redis://redis-prod:6379/0'
  LOG_LEVEL: 'warn'
  ENVIRONMENT: 'production'
  REPLICAS: '5'
  ENABLE_DEBUG: 'false'
  API_RATE_LIMIT: '200'
  SESSION_TIMEOUT: '14400'
```

### Étape 5 : Configurer RBAC par environnement

5. Créer des rôles et utilisateurs par environnement :

```yaml
# dev-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-dev
  name: dev-developer
rules:
  - apiGroups: ['']
    resources: ['pods', 'services', 'configmaps', 'secrets']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']
  - apiGroups: ['']
    resources: ['pods/log', 'pods/exec']
    verbs: ['get', 'list', 'create']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-developers
  namespace: ecommerce-dev
subjects:
  - kind: User
    name: dev-team
    apiGroup: rbac.authorization.k8s.io
  - kind: ServiceAccount
    name: dev-deployer
    namespace: ecommerce-dev
roleRef:
  kind: Role
  name: dev-developer
  apiGroup: rbac.authorization.k8s.io

---
# prod-rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: prod-operator
rules:
  - apiGroups: ['']
    resources: ['pods', 'services']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['deployments']
    verbs: ['get', 'list', 'watch', 'patch'] # Seulement lecture et mise à jour
  - apiGroups: ['']
    resources: ['pods/log']
    verbs: ['get', 'list']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: prod-operators
  namespace: ecommerce-prod
subjects:
  - kind: User
    name: ops-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: prod-operator
  apiGroup: rbac.authorization.k8s.io
```

### Étape 6 : Déployer l'application dans chaque environnement

6. Créer template de déploiement paramétré :

```yaml
# app-template.yaml (utiliser envsubst pour paramétrer)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-backend
  namespace: ${ENVIRONMENT}
  labels:
    app: api-backend
    environment: ${ENVIRONMENT}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      app: api-backend
  template:
    metadata:
      labels:
        app: api-backend
        environment: ${ENVIRONMENT}
    spec:
      containers:
        - name: api
          image: ecommerce/api:${IMAGE_TAG}
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
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: LOG_LEVEL
            - name: ENVIRONMENT
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: ENVIRONMENT
          resources:
            requests:
              memory: ${MEMORY_REQUEST}
              cpu: ${CPU_REQUEST}
            limits:
              memory: ${MEMORY_LIMIT}
              cpu: ${CPU_LIMIT}
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Étape 7 : Script de déploiement automatisé

7. Créer script pour déployer dans chaque environnement :

```bash
#!/bin/bash
# deploy-environment.sh

ENVIRONMENT=$1
IMAGE_TAG=$2

if [ -z "$ENVIRONMENT" ] || [ -z "$IMAGE_TAG" ]; then
    echo "Usage: $0 <environment> <image_tag>"
    echo "Example: $0 dev v1.2.3"
    exit 1
fi

# Configuration par environnement
case $ENVIRONMENT in
    "ecommerce-dev")
        REPLICAS=1
        MEMORY_REQUEST="64Mi"
        CPU_REQUEST="50m"
        MEMORY_LIMIT="256Mi"
        CPU_LIMIT="200m"
        ;;
    "ecommerce-staging")
        REPLICAS=2
        MEMORY_REQUEST="128Mi"
        CPU_REQUEST="100m"
        MEMORY_LIMIT="512Mi"
        CPU_LIMIT="500m"
        ;;
    "ecommerce-prod")
        REPLICAS=5
        MEMORY_REQUEST="256Mi"
        CPU_REQUEST="250m"
        MEMORY_LIMIT="1Gi"
        CPU_LIMIT="1"
        ;;
    *)
        echo "Environment non supporté: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "🚀 Déploiement dans $ENVIRONMENT avec l'image $IMAGE_TAG"

# Export des variables pour envsubst
export ENVIRONMENT REPLICAS IMAGE_TAG MEMORY_REQUEST CPU_REQUEST MEMORY_LIMIT CPU_LIMIT

# Déployer la configuration
envsubst < app-template.yaml | kubectl apply -f -

# Attendre le rollout
kubectl rollout status deployment/api-backend -n $ENVIRONMENT --timeout=300s

# Vérifier le déploiement
kubectl get pods -n $ENVIRONMENT -l app=api-backend

echo "✅ Déploiement terminé dans $ENVIRONMENT"
```

### Étape 8 : Monitoring séparé par environnement

8. Configurer ServiceMonitor par environnement :

```yaml
# monitoring-per-env.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-dev-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: api-backend
      environment: development
  endpoints:
    - port: metrics
      interval: 30s
  namespaceSelector:
    matchNames:
      - ecommerce-dev

---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-staging-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: api-backend
      environment: staging
  endpoints:
    - port: metrics
      interval: 15s
  namespaceSelector:
    matchNames:
      - ecommerce-staging

---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api-prod-metrics
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: api-backend
      environment: production
  endpoints:
    - port: metrics
      interval: 5s
  namespaceSelector:
    matchNames:
      - ecommerce-prod
```

### Étape 9 : Tests et validation

9. Tester l'isolation et les quotas :

```bash
# Vérifier les quotas
kubectl describe resourcequota -n ecommerce-dev
kubectl describe resourcequota -n ecommerce-staging
kubectl describe resourcequota -n ecommerce-prod

# Tester les limits
kubectl run test-limits --image=nginx --dry-run=server -n ecommerce-dev

# Vérifier RBAC
kubectl auth can-i create pods --as=dev-team -n ecommerce-dev
kubectl auth can-i delete pods --as=dev-team -n ecommerce-prod

# Déployer dans chaque environnement
./deploy-environment.sh ecommerce-dev v1.0.0
./deploy-environment.sh ecommerce-staging v1.0.0
./deploy-environment.sh ecommerce-prod v1.0.0

# Vérifier isolation réseau (optionnel avec NetworkPolicies)
kubectl get networkpolicy -A
```

## Critères de validation

- [ ] Namespaces créés avec labels appropriés
- [ ] Resource quotas configurés et respectés
- [ ] LimitRanges appliquées automatiquement
- [ ] Configurations spécifiques par environnement
- [ ] RBAC fonctionnel avec restrictions appropriées
- [ ] Application déployée dans les 3 environnements
- [ ] Isolation entre environnements vérifiée
- [ ] Monitoring séparé par environnement
- [ ] Script de déploiement automatisé fonctionnel

## Bonnes pratiques implémentées

- **Isolation multi-niveau** : namespaces, RBAC, ressources
- **Configuration externalisée** par environnement
- **Quotas adaptatifs** selon l'usage
- **Sécurité par défaut** avec RBAC restrictif
- **Monitoring différencié** par criticité
- **Déploiement automatisé** avec validation

## Durée estimée

40 minutes
