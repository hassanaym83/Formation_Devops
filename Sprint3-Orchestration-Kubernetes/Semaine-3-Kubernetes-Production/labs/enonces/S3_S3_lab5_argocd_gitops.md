# LAB 5 - ArgoCD et GitOps avec Kubernetes

## Objectifs

- Installer et configurer ArgoCD sur Kubernetes
- Implémenter une architecture GitOps complète
- Gérer les déploiements multi-environnements avec ArgoCD
- Configurer la synchronisation automatique et les hooks
- Sécuriser ArgoCD avec RBAC et authentification

## Prérequis

- Cluster Kubernetes (Minikube, kind, ou cloud)
- kubectl configuré
- Helm 3.x installé
- Git et accès à un repository Git
- Connaissances de base des concepts GitOps

## Contexte du LAB

Vous allez implémenter une architecture GitOps complète pour gérer le déploiement d'une application e-commerce multi-services avec ArgoCD. Cette architecture permettra :

- Déploiements déclaratifs et reproductibles
- Gestion des environnements dev/staging/prod
- Rollback automatique et synchronisation
- Monitoring et observabilité des déploiements

## Exercice 1 : Installation et configuration d'ArgoCD

### Étape 1.1 : Installation d'ArgoCD

Installez ArgoCD dans votre cluster :

```bash
# Créer le namespace
kubectl create namespace argocd

# Installer ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Étape 1.2 : Configuration du service ArgoCD

Créez `argocd/service-nodeport.yaml` :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: argocd-server-nodeport
  namespace: argocd
  labels:
    app.kubernetes.io/component: server
    app.kubernetes.io/name: argocd-server
    app.kubernetes.io/part-of: argocd
spec:
  type: NodePort
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: 8080
      nodePort: 30080
    - name: https
      port: 443
      protocol: TCP
      targetPort: 8080
      nodePort: 30443
  selector:
    app.kubernetes.io/name: argocd-server
```

### Étape 1.3 : Configuration ArgoCD

Créez `argocd/argocd-cm.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-cm
    app.kubernetes.io/part-of: argocd
data:
  # Permettre l'insecure mode pour les tests locaux
  server.insecure: 'true'

  # Configuration des repositories
  repositories: |
    - url: https://github.com/your-org/gitops-manifests
      name: gitops-manifests
    - url: https://charts.helm.sh/stable
      name: stable
      type: helm
    - url: https://charts.bitnami.com/bitnami
      name: bitnami
      type: helm

  # Configuration des outils personnalisés
  configManagementPlugins: |
    - name: kustomize-with-helm
      generate:
        command: ["sh", "-c"]
        args: ["kustomize build . | envsubst"]
```

### Étape 1.4 : Récupération du mot de passe admin

```bash
# Récupérer le mot de passe initial
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Étape 1.5 : Accès à l'interface ArgoCD

```bash
# Port-forward pour accéder à ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Ou utiliser le NodePort si configuré
# https://your-cluster-ip:30443
```

## Exercice 2 : Structure GitOps repository

### Étape 2.1 : Organisation du repository GitOps

Créez la structure suivante dans un repository Git :

```
gitops-ecommerce/
├── applications/
│   ├── dev/
│   │   ├── frontend-app.yaml
│   │   ├── backend-app.yaml
│   │   └── database-app.yaml
│   ├── staging/
│   └── prod/
├── environments/
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   ├── frontend/
│   │   ├── backend/
│   │   └── database/
│   ├── staging/
│   └── prod/
├── base/
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   ├── backend/
│   └── database/
├── helm-charts/
│   ├── ecommerce-frontend/
│   ├── ecommerce-backend/
│   └── postgresql/
└── scripts/
    ├── sync-apps.sh
    └── promote.sh
```

### Étape 2.2 : Application frontend de base

Créez `base/frontend/deployment.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-frontend
  labels:
    app: ecommerce-frontend
    component: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ecommerce-frontend
  template:
    metadata:
      labels:
        app: ecommerce-frontend
        component: frontend
    spec:
      containers:
        - name: frontend
          image: nginx:1.20-alpine
          ports:
            - containerPort: 80
          env:
            - name: API_URL
              value: 'http://backend-service:8080'
            - name: ENVIRONMENT
              value: 'development'
          resources:
            requests:
              memory: '64Mi'
              cpu: '50m'
            limits:
              memory: '128Mi'
              cpu: '100m'
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Étape 2.3 : Service frontend

Créez `base/frontend/service.yaml` :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  labels:
    app: ecommerce-frontend
spec:
  selector:
    app: ecommerce-frontend
  ports:
    - name: http
      port: 80
      targetPort: 80
  type: ClusterIP
```

### Étape 2.4 : Kustomization de base

Créez `base/frontend/kustomization.yaml` :

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

metadata:
  name: ecommerce-frontend-base

resources:
  - deployment.yaml
  - service.yaml

commonLabels:
  app.kubernetes.io/name: ecommerce-frontend
  app.kubernetes.io/part-of: ecommerce

images:
  - name: nginx
    newTag: 1.20-alpine
```

## Exercice 3 : Configuration environnements

### Étape 3.1 : Environnement de développement

Créez `environments/dev/frontend/kustomization.yaml` :

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-dev

resources:
  - ../../../base/frontend

patchesStrategicMerge:
  - deployment-patch.yaml

replicas:
  - name: ecommerce-frontend
    count: 1

images:
  - name: nginx
    newTag: 1.20-alpine

configMapGenerator:
  - name: frontend-config
    literals:
      - ENVIRONMENT=development
      - DEBUG=true
      - API_URL=http://backend-service.ecommerce-dev.svc.cluster.local:8080

commonLabels:
  environment: development
  version: v1.0.0-dev
```

### Étape 3.2 : Patch pour l'environnement dev

Créez `environments/dev/frontend/deployment-patch.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ecommerce-frontend
spec:
  template:
    spec:
      containers:
        - name: frontend
          env:
            - name: DEBUG
              value: 'true'
            - name: LOG_LEVEL
              value: 'debug'
          resources:
            requests:
              memory: '32Mi'
              cpu: '25m'
            limits:
              memory: '64Mi'
              cpu: '50m'
```

### Étape 3.3 : Environnement de production

Créez `environments/prod/frontend/kustomization.yaml` :

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: ecommerce-prod

resources:
  - ../../../base/frontend

patchesStrategicMerge:
  - deployment-patch.yaml
  - ingress.yaml

replicas:
  - name: ecommerce-frontend
    count: 5

images:
  - name: nginx
    newTag: 1.21-alpine

configMapGenerator:
  - name: frontend-config
    literals:
      - ENVIRONMENT=production
      - DEBUG=false
      - API_URL=https://api.ecommerce.com

commonLabels:
  environment: production
  version: v1.0.0
```

## Exercice 4 : Applications ArgoCD

### Étape 4.1 : Application frontend dev

Créez `applications/dev/frontend-app.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-frontend-dev
  namespace: argocd
  labels:
    app.kubernetes.io/name: ecommerce-frontend
    environment: development
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: ecommerce
  source:
    repoURL: https://github.com/your-org/gitops-ecommerce.git
    targetRevision: HEAD
    path: environments/dev/frontend
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

### Étape 4.2 : Application backend

Créez `applications/dev/backend-app.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-backend-dev
  namespace: argocd
  labels:
    app.kubernetes.io/name: ecommerce-backend
    environment: development
spec:
  project: ecommerce
  source:
    repoURL: https://github.com/your-org/gitops-ecommerce.git
    targetRevision: HEAD
    path: environments/dev/backend
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 3
```

### Étape 4.3 : ApplicationSet pour multi-environnements

Créez `applications/applicationset.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: ecommerce-apps
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - list:
              elements:
                - env: dev
                  cluster: https://kubernetes.default.svc
                  namespace: ecommerce-dev
                  auto-sync: true
                - env: staging
                  cluster: https://kubernetes.default.svc
                  namespace: ecommerce-staging
                  auto-sync: false
                - env: prod
                  cluster: https://kubernetes.default.svc
                  namespace: ecommerce-prod
                  auto-sync: false
          - list:
              elements:
                - app: frontend
                - app: backend
                - app: database
  template:
    metadata:
      name: 'ecommerce-{{app}}-{{env}}'
      namespace: argocd
    spec:
      project: ecommerce
      source:
        repoURL: https://github.com/your-org/gitops-ecommerce.git
        targetRevision: HEAD
        path: 'environments/{{env}}/{{app}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: '{{auto-sync}}'
          selfHeal: '{{auto-sync}}'
        syncOptions:
          - CreateNamespace=true
```

## Exercice 5 : Projets et RBAC ArgoCD

### Étape 5.1 : Projet ArgoCD

Créez `argocd/ecommerce-project.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: ecommerce
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  description: E-commerce application project

  # Sources autorisées
  sourceRepos:
    - 'https://github.com/your-org/gitops-ecommerce.git'
    - 'https://charts.helm.sh/stable'
    - 'https://charts.bitnami.com/bitnami'

  # Destinations autorisées
  destinations:
    - namespace: 'ecommerce-*'
      server: https://kubernetes.default.svc
    - namespace: argocd
      server: https://kubernetes.default.svc

  # Ressources autorisées
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRole
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRoleBinding

  namespaceResourceWhitelist:
    - group: ''
      kind: Pod
    - group: ''
      kind: Service
    - group: ''
      kind: ConfigMap
    - group: ''
      kind: Secret
    - group: 'apps'
      kind: Deployment
    - group: 'apps'
      kind: ReplicaSet
    - group: 'networking.k8s.io'
      kind: Ingress

  # Rôles du projet
  roles:
    - name: developer
      description: Developer role for ecommerce project
      policies:
        - p, proj:ecommerce:developer, applications, get, ecommerce/*, allow
        - p, proj:ecommerce:developer, applications, sync, ecommerce/*-dev, allow
        - p, proj:ecommerce:developer, applications, override, ecommerce/*-dev, allow
      groups:
        - ecommerce-developers

    - name: operator
      description: Operator role for ecommerce project
      policies:
        - p, proj:ecommerce:operator, applications, *, ecommerce/*, allow
        - p, proj:ecommerce:operator, repositories, *, *, allow
      groups:
        - ecommerce-operators

    - name: admin
      description: Admin role for ecommerce project
      policies:
        - p, proj:ecommerce:admin, *, *, ecommerce/*, allow
      groups:
        - ecommerce-admins
```

### Étape 5.2 : Configuration RBAC

Créez `argocd/rbac-cm.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-rbac-cm
    app.kubernetes.io/part-of: argocd
data:
  policy.default: role:readonly
  policy.csv: |
    # Global policies
    p, role:admin, *, *, *, allow
    p, role:developer, applications, get, */*, allow
    p, role:developer, applications, sync, */dev-*, allow

    # Group bindings
    g, ecommerce-admins, role:admin
    g, ecommerce-developers, role:developer

    # Project-specific policies are defined in AppProject
```

## Exercice 6 : Helm Charts dans GitOps

### Étape 6.1 : Chart Helm pour frontend

Créez `helm-charts/ecommerce-frontend/Chart.yaml` :

```yaml
apiVersion: v2
name: ecommerce-frontend
description: E-commerce frontend Helm chart
version: 0.1.0
appVersion: '1.0.0'
keywords:
  - ecommerce
  - frontend
  - nginx
maintainers:
  - name: DevOps Team
    email: devops@company.com
```

### Étape 6.2 : Values par défaut

Créez `helm-charts/ecommerce-frontend/values.yaml` :

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: '1.20-alpine'
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: false
  className: ''
  annotations: {}
  hosts:
    - host: frontend.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 50m
    memory: 64Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

config:
  environment: development
  apiUrl: http://backend-service:8080
  debug: true

nodeSelector: {}
tolerations: []
affinity: {}
```

### Étape 6.3 : Application ArgoCD avec Helm

Créez `applications/dev/frontend-helm-app.yaml` :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ecommerce-frontend-helm-dev
  namespace: argocd
spec:
  project: ecommerce
  source:
    repoURL: https://github.com/your-org/gitops-ecommerce.git
    targetRevision: HEAD
    path: helm-charts/ecommerce-frontend
    helm:
      valueFiles:
        - values.yaml
        - values-dev.yaml
      parameters:
        - name: image.tag
          value: '1.20-alpine'
        - name: replicaCount
          value: '1'
        - name: config.environment
          value: 'development'
  destination:
    server: https://kubernetes.default.svc
    namespace: ecommerce-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

## Exercice 7 : Hooks et synchronisation avancée

### Étape 7.1 : PreSync Hook

Créez `environments/prod/hooks/presync-backup.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: database-backup-presync
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-weight: '-1'
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
        - name: backup
          image: postgres:13
          command:
            - /bin/bash
            - -c
            - |
              echo "Creating database backup before deployment..."
              pg_dump $DATABASE_URL > /backup/backup-$(date +%Y%m%d-%H%M%S).sql
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: url
          volumeMounts:
            - name: backup-storage
              mountPath: /backup
      volumes:
        - name: backup-storage
          persistentVolumeClaim:
            claimName: backup-pvc
      restartPolicy: OnFailure
```

### Étape 7.2 : PostSync Hook

Créez `environments/prod/hooks/postsync-test.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: smoke-tests-postsync
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-weight: '1'
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
        - name: smoke-tests
          image: curlimages/curl:latest
          command:
            - /bin/sh
            - -c
            - |
              echo "Running smoke tests..."
              curl -f http://frontend-service/health || exit 1
              curl -f http://backend-service/health || exit 1
              echo "All smoke tests passed!"
      restartPolicy: OnFailure
  backoffLimit: 3
```

### Étape 7.3 : Sync Wave

Créez des ressources avec des sync waves :

```yaml
# Database (wave 0)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
  annotations:
    argocd.argoproj.io/sync-wave: "0"

# Backend (wave 1)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  annotations:
    argocd.argoproj.io/sync-wave: "1"

# Frontend (wave 2)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  annotations:
    argocd.argoproj.io/sync-wave: "2"
```

## Exercice 8 : Configuration avancée ArgoCD

### Étape 8.1 : Repository credentials

Créez `argocd/repository-secret.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: private-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://github.com/your-org/private-gitops-repo.git
  username: git-username
  password: git-token
```

### Étape 8.2 : Cluster external

Créez `argocd/cluster-secret.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: staging-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: staging-cluster
  server: https://staging-k8s-api.company.com
  config: |
    {
      "bearerToken": "...",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "..."
      }
    }
```

### Étape 8.3 : Configuration des notifications

Créez `argocd/argocd-notifications-cm.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token

  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now running new version.

  template.app-health-degraded: |
    message: |
      Application {{.app.metadata.name}} has degraded health.

  trigger.on-deployed: |
    - when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
      send: [app-deployed]

  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]

  subscriptions: |
    - recipients:
      - slack:general
      triggers:
      - on-deployed
      - on-health-degraded
```

## Exercice 9 : Scripts d'automatisation

### Étape 9.1 : Script de synchronisation

Créez `scripts/sync-apps.sh` :

```bash
#!/bin/bash

set -e

ENVIRONMENT=${1:-dev}
APP_NAME=${2:-}
DRY_RUN=${3:-false}

echo "Synchronizing applications for environment: $ENVIRONMENT"

# Configuration ArgoCD CLI
export ARGOCD_SERVER="localhost:8080"
export ARGOCD_OPTS="--insecure"

# Login (utiliser un token en production)
argocd login $ARGOCD_SERVER --username admin --password $ARGOCD_PASSWORD

# Fonction de sync
sync_app() {
    local app_name=$1
    echo "Syncing application: $app_name"

    if [ "$DRY_RUN" = "true" ]; then
        argocd app diff $app_name
    else
        argocd app sync $app_name --prune
        argocd app wait $app_name --health
    fi
}

# Sync applications
if [ -z "$APP_NAME" ]; then
    # Sync toutes les apps de l'environnement
    apps=$(argocd app list -o name | grep "$ENVIRONMENT")
    for app in $apps; do
        sync_app $app
    done
else
    # Sync app spécifique
    sync_app "ecommerce-$APP_NAME-$ENVIRONMENT"
fi

echo "Synchronization completed!"
```

### Étape 9.2 : Script de promotion

Créez `scripts/promote.sh` :

```bash
#!/bin/bash

set -e

SOURCE_ENV=${1:-dev}
TARGET_ENV=${2:-staging}
APP_NAME=${3:-}

echo "Promoting from $SOURCE_ENV to $TARGET_ENV"

# Récupérer la version actuelle en source
get_image_tag() {
    local app_name=$1
    local env=$2

    kubectl get deployment $app_name -n ecommerce-$env -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d':' -f2
}

# Mettre à jour le manifeste target
update_manifest() {
    local app_name=$1
    local tag=$2
    local target_env=$3

    local manifest_file="environments/$target_env/$app_name/kustomization.yaml"

    # Mettre à jour le tag d'image
    yq eval ".images[0].newTag = \"$tag\"" -i $manifest_file

    # Commit et push
    git add $manifest_file
    git commit -m "Promote $app_name to $target_env with tag $tag"
    git push origin main
}

# Promotion des applications
if [ -z "$APP_NAME" ]; then
    for app in frontend backend; do
        tag=$(get_image_tag $app $SOURCE_ENV)
        echo "Promoting $app with tag $tag"
        update_manifest $app $tag $TARGET_ENV
    done
else
    tag=$(get_image_tag $APP_NAME $SOURCE_ENV)
    echo "Promoting $APP_NAME with tag $tag"
    update_manifest $APP_NAME $tag $TARGET_ENV
fi

echo "Promotion completed! ArgoCD will sync automatically."
```

## Exercice 10 : Monitoring et observabilité

### Étape 10.1 : Métriques ArgoCD

Configurez le monitoring d'ArgoCD avec Prometheus :

```yaml
# argocd/servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

### Étape 10.2 : Dashboard Grafana

Créez un dashboard pour ArgoCD :

```json
{
  "dashboard": {
    "title": "ArgoCD Overview",
    "panels": [
      {
        "title": "Application Health",
        "type": "stat",
        "targets": [
          {
            "expr": "argocd_app_health_status"
          }
        ]
      },
      {
        "title": "Sync Status",
        "type": "stat",
        "targets": [
          {
            "expr": "argocd_app_sync_total"
          }
        ]
      }
    ]
  }
}
```

### Étape 10.3 : Alertes ArgoCD

Créez `argocd/prometheus-rules.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: argocd-alerts
  namespace: argocd
spec:
  groups:
    - name: argocd.rules
      rules:
        - alert: ArgoCDAppNotSynced
          expr: argocd_app_info{sync_status!="Synced"} == 1
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: 'ArgoCD Application not synced'
            description: 'Application {{ $labels.name }} is not synced for more than 10 minutes'

        - alert: ArgoCDAppUnhealthy
          expr: argocd_app_info{health_status!="Healthy"} == 1
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: 'ArgoCD Application unhealthy'
            description: 'Application {{ $labels.name }} is unhealthy'
```

## Questions de validation

1. Quelle est la différence entre GitOps et CI/CD traditionnel ?
2. Comment gérer les secrets dans une architecture GitOps ?
3. Expliquez les concepts de sync waves et hooks dans ArgoCD
4. Comment implémenter un rollback avec ArgoCD ?
5. Quelles sont les bonnes pratiques pour structurer un repository GitOps ?

## Livrables attendus

1. **ArgoCD installé** et configuré avec RBAC
2. **Repository GitOps** avec structure multi-environnements
3. **Applications ArgoCD** pour tous les composants
4. **ApplicationSet** pour gestion multi-environnements
5. **Projet ArgoCD** avec RBAC et politiques
6. **Helm Charts** intégrés dans GitOps
7. **Hooks et sync waves** configurés
8. **Scripts d'automatisation** (sync, promotion)
9. **Monitoring ArgoCD** avec métriques et alertes
10. **Documentation** complète du workflow GitOps

## Critères d'évaluation

- **Installation** : ArgoCD correctement installé et accessible
- **Structure** : Repository GitOps bien organisé
- **Automatisation** : Sync automatique fonctionnel
- **Sécurité** : RBAC et projets correctement configurés
- **Monitoring** : Métriques et alertes en place
- **Documentation** : Processus GitOps documenté

## Ressources utiles

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [GitOps Principles](https://www.gitops.tech/)
- [Kustomize Documentation](https://kustomize.io/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

---

**Durée estimée : 8-9 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
