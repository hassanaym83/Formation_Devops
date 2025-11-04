# Correction LAB 1 - RBAC et Sécurité Kubernetes

## Vue d'ensemble

Cette correction fournit les solutions complètes pour l'implémentation de RBAC, ServiceAccounts, et sécurité Kubernetes dans un environnement de production.

## Exercice 1 : ServiceAccounts et Secrets

### Solution complète : ServiceAccounts

```yaml
# serviceaccounts.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: blog-backend-sa
  namespace: blog-app
  labels:
    app: blog-app
    component: backend
    managed-by: kubernetes
  annotations:
    description: 'ServiceAccount pour les services backend du blog'
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: blog-frontend-sa
  namespace: blog-app
  labels:
    app: blog-app
    component: frontend
    managed-by: kubernetes
  annotations:
    description: 'ServiceAccount pour les services frontend du blog'
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: blog-monitoring-sa
  namespace: blog-app
  labels:
    app: blog-app
    component: monitoring
    managed-by: kubernetes
  annotations:
    description: 'ServiceAccount pour le monitoring du blog'
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: blog-admin-sa
  namespace: blog-app
  labels:
    app: blog-app
    component: admin
    managed-by: kubernetes
  annotations:
    description: "ServiceAccount pour l'administration du blog"
automountServiceAccountToken: false # Sécurité renforcée
```

### Solution complète : Secrets sécurisés

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: blog-database-secret
  namespace: blog-app
  labels:
    app: blog-app
    component: database
type: Opaque
data:
  DB_HOST: cG9zdGdyZXNxbC5kYXRhYmFzZS5zdmMuY2x1c3Rlci5sb2NhbA== # postgresql.database.svc.cluster.local
  DB_NAME: YmxvZ19kYg== # blog_db
  DB_USER: YmxvZ191c2Vy # blog_user
  DB_PASSWORD: U3VwZXJTZWN1cmVQYXNzd29yZDEyMyE= # SuperSecurePassword123!
  DB_PORT: NTQzMg== # 5432
---
apiVersion: v1
kind: Secret
metadata:
  name: blog-jwt-secret
  namespace: blog-app
  labels:
    app: blog-app
    component: auth
type: Opaque
data:
  JWT_SECRET: bXlfc3VwZXJfc2VjcmV0X2p3dF9rZXlfZm9yX2Jsb2dfYXV0aGVudGljYXRpb24= # my_super_secret_jwt_key_for_blog_authentication
  JWT_EXPIRY: ODZhMDA= # 86400 (24h)
---
apiVersion: v1
kind: Secret
metadata:
  name: blog-redis-secret
  namespace: blog-app
  labels:
    app: blog-app
    component: cache
type: Opaque
data:
  REDIS_HOST: cmVkaXMuZGF0YWJhc2Uuc3ZjLmNsdXN0ZXIubG9jYWw= # redis.database.svc.cluster.local
  REDIS_PORT: NjM3OQ== # 6379
  REDIS_PASSWORD: UmVkaXNTZWN1cmVQYXNzMTIz # RedisSecurePass123
---
apiVersion: v1
kind: Secret
metadata:
  name: blog-smtp-secret
  namespace: blog-app
  labels:
    app: blog-app
    component: notification
type: Opaque
data:
  SMTP_HOST: c210cC5nbWFpbC5jb20= # smtp.gmail.com
  SMTP_PORT: NTg3 # 587
  SMTP_USER: YmxvZ0BleGFtcGxlLmNvbQ== # blog@example.com
  SMTP_PASSWORD: YXBwX3Bhc3N3b3JkXzEyMw== # app_password_123
```

### Validation et test des ServiceAccounts

```bash
# Commandes de validation
kubectl get serviceaccounts -n blog-app
kubectl describe sa blog-backend-sa -n blog-app
kubectl get secrets -n blog-app

# Test d'accès aux secrets depuis un pod
kubectl run test-pod --image=busybox --rm -it --restart=Never \
  --serviceaccount=blog-backend-sa \
  --namespace=blog-app \
  -- /bin/sh -c "ls -la /var/run/secrets/kubernetes.io/serviceaccount/"
```

## Exercice 2 : Roles et permissions

### Solution complète : Roles avec principe du moindre privilège

```yaml
# roles.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: blog-backend-role
  namespace: blog-app
  labels:
    app: blog-app
    component: backend
rules:
  # Accès aux ConfigMaps pour la configuration
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch']
    resourceNames: ['blog-config', 'app-config']
  # Accès aux Secrets nécessaires
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list']
    resourceNames:
      ['blog-database-secret', 'blog-jwt-secret', 'blog-redis-secret']
  # Accès aux Services pour la découverte
  - apiGroups: ['']
    resources: ['services']
    verbs: ['get', 'list', 'watch']
  # Accès aux Pods pour les health checks
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list', 'watch']
  # Accès aux endpoints pour la découverte de service
  - apiGroups: ['']
    resources: ['endpoints']
    verbs: ['get', 'list', 'watch']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: blog-frontend-role
  namespace: blog-app
  labels:
    app: blog-app
    component: frontend
rules:
  # Accès minimal pour le frontend
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch']
    resourceNames: ['blog-frontend-config']
  - apiGroups: ['']
    resources: ['services']
    verbs: ['get', 'list', 'watch']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: blog-monitoring-role
  namespace: blog-app
  labels:
    app: blog-app
    component: monitoring
rules:
  # Accès pour collecter les métriques
  - apiGroups: ['']
    resources: ['pods', 'services', 'endpoints', 'nodes']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets', 'statefulsets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch']
    resourceNames: ['prometheus-config', 'grafana-config']
  # Accès aux métriques non-resource URLs
  - apiGroups: ['']
    resources: ['nodes/metrics', 'nodes/stats']
    verbs: ['get']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: blog-admin-role
  namespace: blog-app
  labels:
    app: blog-app
    component: admin
rules:
  # Permissions complètes pour l'administration
  - apiGroups: ['']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['apps']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['networking.k8s.io']
    resources: ['*']
    verbs: ['*']
  - apiGroups: ['policy']
    resources: ['*']
    verbs: ['*']
```

### Solution complète : RoleBindings

```yaml
# rolebindings.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: blog-backend-binding
  namespace: blog-app
  labels:
    app: blog-app
    component: backend
subjects:
  - kind: ServiceAccount
    name: blog-backend-sa
    namespace: blog-app
roleRef:
  kind: Role
  name: blog-backend-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: blog-frontend-binding
  namespace: blog-app
  labels:
    app: blog-app
    component: frontend
subjects:
  - kind: ServiceAccount
    name: blog-frontend-sa
    namespace: blog-app
roleRef:
  kind: Role
  name: blog-frontend-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: blog-monitoring-binding
  namespace: blog-app
  labels:
    app: blog-app
    component: monitoring
subjects:
  - kind: ServiceAccount
    name: blog-monitoring-sa
    namespace: blog-app
roleRef:
  kind: Role
  name: blog-monitoring-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: blog-admin-binding
  namespace: blog-app
  labels:
    app: blog-app
    component: admin
subjects:
  - kind: ServiceAccount
    name: blog-admin-sa
    namespace: blog-app
roleRef:
  kind: Role
  name: blog-admin-role
  apiGroup: rbac.authorization.k8s.io
```

### Tests et validation RBAC

```bash
# Script de test des permissions RBAC
#!/bin/bash

echo "=== Tests des permissions RBAC ==="

# Test 1: Vérifier l'accès aux ConfigMaps pour backend
echo "Test 1: Accès ConfigMaps pour backend"
kubectl auth can-i get configmaps --as=system:serviceaccount:blog-app:blog-backend-sa -n blog-app

# Test 2: Vérifier l'accès aux Secrets pour backend
echo "Test 2: Accès Secrets pour backend"
kubectl auth can-i get secrets --as=system:serviceaccount:blog-app:blog-backend-sa -n blog-app

# Test 3: Vérifier que frontend ne peut pas accéder aux Secrets
echo "Test 3: Frontend ne doit pas accéder aux Secrets"
kubectl auth can-i get secrets --as=system:serviceaccount:blog-app:blog-frontend-sa -n blog-app

# Test 4: Vérifier les permissions d'admin
echo "Test 4: Permissions admin"
kubectl auth can-i delete pods --as=system:serviceaccount:blog-app:blog-admin-sa -n blog-app

# Test 5: Vérifier les permissions monitoring
echo "Test 5: Permissions monitoring"
kubectl auth can-i get pods --as=system:serviceaccount:blog-app:blog-monitoring-sa -n blog-app

echo "=== Fin des tests RBAC ==="
```

## Exercice 3 : ClusterRoles et accès multi-namespaces

### Solution complète : ClusterRoles

```yaml
# clusterroles.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: blog-metrics-reader
  labels:
    app: blog-app
    component: monitoring
rules:
  # Lecture des métriques cluster-wide
  - apiGroups: ['']
    resources: ['nodes', 'nodes/metrics', 'nodes/stats']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['pods', 'services', 'endpoints']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets', 'statefulsets', 'daemonsets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses', 'networkpolicies']
    verbs: ['get', 'list', 'watch']
  # Accès aux métriques non-resource URLs
  - nonResourceURLs: ['/metrics', '/metrics/*']
    verbs: ['get']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: blog-network-reader
  labels:
    app: blog-app
    component: network
rules:
  # Lecture des ressources réseau
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses', 'networkpolicies', 'ingressclasses']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['services', 'endpoints']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['discovery.k8s.io']
    resources: ['endpointslices']
    verbs: ['get', 'list', 'watch']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: blog-security-auditor
  labels:
    app: blog-app
    component: security
rules:
  # Audit de sécurité
  - apiGroups: ['rbac.authorization.k8s.io']
    resources: ['roles', 'rolebindings', 'clusterroles', 'clusterrolebindings']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['serviceaccounts', 'secrets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['policy']
    resources: ['podsecuritypolicies', 'poddisruptionbudgets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['networking.k8s.io']
    resources: ['networkpolicies']
    verbs: ['get', 'list', 'watch']
```

### Solution complète : ClusterRoleBindings

```yaml
# clusterrolebindings.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: blog-metrics-reader-binding
  labels:
    app: blog-app
    component: monitoring
subjects:
  - kind: ServiceAccount
    name: blog-monitoring-sa
    namespace: blog-app
  # Également pour Prometheus dans le namespace monitoring
  - kind: ServiceAccount
    name: prometheus
    namespace: monitoring
roleRef:
  kind: ClusterRole
  name: blog-metrics-reader
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: blog-network-reader-binding
  labels:
    app: blog-app
    component: network
subjects:
  - kind: ServiceAccount
    name: blog-admin-sa
    namespace: blog-app
roleRef:
  kind: ClusterRole
  name: blog-network-reader
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: blog-security-auditor-binding
  labels:
    app: blog-app
    component: security
subjects:
  - kind: ServiceAccount
    name: blog-admin-sa
    namespace: blog-app
  # Groupe d'auditeurs de sécurité
  - kind: Group
    name: security-auditors
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: blog-security-auditor
  apiGroup: rbac.authorization.k8s.io
```

## Exercice 4 : Déploiement avec ServiceAccounts

### Solution complète : Deployment backend sécurisé

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog-backend
  namespace: blog-app
  labels:
    app: blog-app
    component: backend
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: blog-app
      component: backend
  template:
    metadata:
      labels:
        app: blog-app
        component: backend
        version: v1.0.0
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '3000'
        prometheus.io/path: '/metrics'
    spec:
      serviceAccountName: blog-backend-sa
      automountServiceAccountToken: true
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: component
                      operator: In
                      values: ['backend']
                topologyKey: kubernetes.io/hostname
      containers:
        - name: blog-backend
          image: blog/backend:v1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
            - name: metrics
              containerPort: 9090
              protocol: TCP
          env:
            - name: NODE_ENV
              value: 'production'
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          envFrom:
            - secretRef:
                name: blog-database-secret
            - secretRef:
                name: blog-jwt-secret
            - secretRef:
                name: blog-redis-secret
            - configMapRef:
                name: blog-config
          volumeMounts:
            - name: tmp-volume
              mountPath: /tmp
            - name: cache-volume
              mountPath: /app/cache
            - name: logs-volume
              mountPath: /app/logs
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
              httpHeaders:
                - name: X-Health-Check
                  value: liveness
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
              httpHeaders:
                - name: X-Health-Check
                  value: readiness
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
            runAsGroup: 1000
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
      volumes:
        - name: tmp-volume
          emptyDir: {}
        - name: cache-volume
          emptyDir: {}
        - name: logs-volume
          emptyDir: {}
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      terminationGracePeriodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: blog-backend-service
  namespace: blog-app
  labels:
    app: blog-app
    component: backend
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
    - name: metrics
      port: 9090
      targetPort: 9090
      protocol: TCP
  selector:
    app: blog-app
    component: backend
```

### Solution complète : Deployment frontend sécurisé

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog-frontend
  namespace: blog-app
  labels:
    app: blog-app
    component: frontend
    version: v1.0.0
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: blog-app
      component: frontend
  template:
    metadata:
      labels:
        app: blog-app
        component: frontend
        version: v1.0.0
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '80'
        prometheus.io/path: '/metrics'
    spec:
      serviceAccountName: blog-frontend-sa
      automountServiceAccountToken: false # Frontend n'a pas besoin d'accès à l'API
      securityContext:
        runAsNonRoot: true
        runAsUser: 101 # nginx user
        runAsGroup: 101
        fsGroup: 101
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: blog-frontend
          image: blog/frontend:v1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          env:
            - name: BACKEND_URL
              value: 'http://blog-backend-service.blog-app.svc.cluster.local'
            - name: API_TIMEOUT
              value: '30000'
          envFrom:
            - configMapRef:
                name: blog-frontend-config
          volumeMounts:
            - name: nginx-cache
              mountPath: /var/cache/nginx
            - name: nginx-run
              mountPath: /var/run
            - name: tmp-volume
              mountPath: /tmp
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 101
            runAsGroup: 101
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
      volumes:
        - name: nginx-cache
          emptyDir: {}
        - name: nginx-run
          emptyDir: {}
        - name: tmp-volume
          emptyDir: {}
      dnsPolicy: ClusterFirst
      restartPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: blog-frontend-service
  namespace: blog-app
  labels:
    app: blog-app
    component: frontend
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 80
      protocol: TCP
  selector:
    app: blog-app
    component: frontend
```

## Exercice 5 : Tests et validation

### Script de validation complète

```bash
#!/bin/bash
# validate-rbac.sh

set -e

NAMESPACE="blog-app"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Validation complète RBAC ===${NC}"

# Fonction pour tester les permissions
test_permission() {
    local sa=$1
    local resource=$2
    local verb=$3
    local expected=$4

    result=$(kubectl auth can-i $verb $resource --as=system:serviceaccount:$NAMESPACE:$sa -n $NAMESPACE 2>/dev/null)

    if [[ "$result" == "$expected" ]]; then
        echo -e "${GREEN}✓${NC} $sa peut $verb $resource: $result"
        return 0
    else
        echo -e "${RED}✗${NC} $sa ne peut pas $verb $resource: attendu $expected, obtenu $result"
        return 1
    fi
}

echo "1. Test des ServiceAccounts..."
kubectl get sa -n $NAMESPACE

echo -e "\n2. Test des permissions backend..."
test_permission "blog-backend-sa" "configmaps" "get" "yes"
test_permission "blog-backend-sa" "secrets" "get" "yes"
test_permission "blog-backend-sa" "pods" "delete" "no"

echo -e "\n3. Test des permissions frontend..."
test_permission "blog-frontend-sa" "configmaps" "get" "yes"
test_permission "blog-frontend-sa" "secrets" "get" "no"

echo -e "\n4. Test des permissions monitoring..."
test_permission "blog-monitoring-sa" "pods" "get" "yes"
test_permission "blog-monitoring-sa" "services" "get" "yes"

echo -e "\n5. Test des permissions admin..."
test_permission "blog-admin-sa" "pods" "delete" "yes"
test_permission "blog-admin-sa" "deployments" "create" "yes"

echo -e "\n6. Validation des Secrets..."
kubectl get secrets -n $NAMESPACE -o name | while read secret; do
    echo "Checking $secret..."
    kubectl get $secret -n $NAMESPACE -o jsonpath='{.data}' | base64 -d 2>/dev/null || true
    echo ""
done

echo -e "\n7. Test des ClusterRoles..."
kubectl auth can-i get nodes --as=system:serviceaccount:$NAMESPACE:blog-monitoring-sa
kubectl auth can-i get clusterroles --as=system:serviceaccount:$NAMESPACE:blog-admin-sa

echo -e "\n8. Validation des déploiements..."
kubectl get deployments -n $NAMESPACE
kubectl get pods -n $NAMESPACE

echo -e "\n${GREEN}=== Validation terminée ===${NC}"
```

### Test d'accès aux secrets depuis un pod

```bash
#!/bin/bash
# test-secrets-access.sh

NAMESPACE="blog-app"

echo "=== Test d'accès aux secrets depuis les pods ==="

# Test 1: Backend peut accéder aux secrets DB
echo "Test 1: Backend accède aux secrets DB"
kubectl run test-backend --image=busybox --rm -it --restart=Never \
  --serviceaccount=blog-backend-sa \
  --namespace=$NAMESPACE \
  --command -- /bin/sh -c "
    echo 'Secrets montés:'
    ls -la /var/run/secrets/kubernetes.io/serviceaccount/
    echo 'Test d accès aux variables d environnement:'
    env | grep DB_ || echo 'Aucune variable DB trouvée'
  "

# Test 2: Frontend ne peut pas accéder aux secrets sensibles
echo "Test 2: Frontend ne doit pas voir les secrets DB"
kubectl run test-frontend --image=busybox --rm -it --restart=Never \
  --serviceaccount=blog-frontend-sa \
  --namespace=$NAMESPACE \
  --command -- /bin/sh -c "
    echo 'Variables d environnement frontend:'
    env | grep -E '(DB_|JWT_|REDIS_)' || echo 'Aucun secret sensible accessible'
  "
```

## Bonnes pratiques implémentées

### 1. Principe du moindre privilège

- Chaque ServiceAccount a uniquement les permissions nécessaires
- Accès granulaire aux ressources spécifiques
- Séparation des rôles par composant

### 2. Sécurité des secrets

- Secrets encodés en base64
- Rotation périodique recommandée
- Accès restreint par RBAC

### 3. Configuration sécurisée des pods

- `runAsNonRoot: true`
- `readOnlyRootFilesystem: true`
- `allowPrivilegeEscalation: false`
- Capabilities minimales

### 4. Monitoring et audit

- ServiceAccount dédié pour le monitoring
- Accès en lecture seule aux métriques
- Logging des accès aux ressources sensibles

## Points de validation

### ✅ Critères de réussite

1. **ServiceAccounts créés** : 4 SA avec annotations appropriées
2. **Secrets sécurisés** : Toutes les données sensibles chiffrées
3. **RBAC fonctionnel** : Permissions validées par tests
4. **Déploiements sécurisés** : Pods avec contexte de sécurité
5. **Tests passants** : Tous les scripts de validation réussis

### 🔍 Points d'audit

1. Aucun SA avec permissions excessives
2. Pas de secrets en plain text
3. Tous les pods utilisent un SA dédié
4. ClusterRoles limités aux besoins spécifiques
5. Network policies complémentaires recommandées

Cette correction démontre une implémentation complète et sécurisée de RBAC dans Kubernetes, suivant les meilleures pratiques de sécurité en production.
