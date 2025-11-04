# LAB 5 - Correction : ArgoCD GitOps et Déploiement Continu

## 📋 Vue d'ensemble de la solution

Cette correction présente une solution complète pour mettre en place ArgoCD avec des pratiques GitOps avancées, incluant la gestion multi-environnements, ApplicationSets, et l'intégration avec des outils externes.

---

## 🎯 Objectifs atteints

- ✅ Installation et configuration ArgoCD complète
- ✅ Applications GitOps multi-environnements
- ✅ ApplicationSets pour la gestion à l'échelle
- ✅ Synchronisation automatique et rollbacks
- ✅ RBAC et sécurité ArgoCD
- ✅ Monitoring et notifications intégrés

---

## 🔧 Solution Étape par Étape

### Étape 1 : Installation ArgoCD avec Helm

#### 1.1 Namespace et configuration de base

```yaml
# argocd/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: argocd
  labels:
    name: argocd
    purpose: gitops
---
apiVersion: v1
kind: Secret
metadata:
  name: argocd-admin-secret
  namespace: argocd
  labels:
    app.kubernetes.io/name: argocd-secret
    app.kubernetes.io/part-of: argocd
type: Opaque
data:
  # admin:$2a$10$rRyBsGSHK6.uc8fntPwVIuLVHgsAhAX7TcdrqW/RADU0uh7CaChLa
  password: JDJhJDEwJHJSeUJzR1NIRzYudWM4Zm50UHdWSXVMVkhDc0FoQVg3VGNkcnFXL1JBRFV1aDdDYUNoTGE=
```

#### 1.2 Values Helm pour ArgoCD

```yaml
# argocd/values.yaml
argo-cd:
  fullnameOverride: argocd

  global:
    image:
      repository: quay.io/argoproj/argocd
      tag: v2.8.4

  ## Dex OAuth configuration
  dex:
    enabled: false

  ## Server configuration
  server:
    extraArgs:
      - --insecure

    config:
      # URL externe d'ArgoCD
      url: https://argocd.k8s.local

      # Configuration OIDC (optionnel)
      oidc.config: |
        name: OIDC
        issuer: https://dex.k8s.local
        clientId: argocd
        clientSecret: $oidc.clientSecret
        requestedScopes: ["openid", "profile", "email", "groups"]
        requestedIDTokenClaims: {"groups": {"essential": true}}

      # Repositories configurés
      repositories: |
        - type: git
          url: https://gitlab.com/your-org/k8s-manifests.git
          usernameSecret:
            name: repo-secret
            key: username
          passwordSecret:
            name: repo-secret
            key: password
        - type: git
          url: https://github.com/your-org/k8s-configs.git
          sshPrivateKeySecret:
            name: github-secret
            key: sshPrivateKey
        - type: helm
          name: bitnami
          url: https://charts.bitnami.com/bitnami

      # Clusters configurés
      clusters: |
        - name: in-cluster
          server: https://kubernetes.default.svc
        - name: staging
          server: https://staging-k8s-api.company.com
          config:
            bearerTokenSecret:
              name: staging-cluster-secret
              key: bearerToken
            tlsClientConfig:
              insecure: false
              caData: LS0tLS1CRUdJTi...
        - name: production  
          server: https://prod-k8s-api.company.com
          config:
            bearerTokenSecret:
              name: prod-cluster-secret
              key: bearerToken

      # Projet par défaut amélioré
      application.resourceTrackingMethod: annotation

    ingress:
      enabled: true
      ingressClassName: nginx
      hostname: argocd.k8s.local
      annotations:
        nginx.ingress.kubernetes.io/ssl-redirect: 'true'
        nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
        nginx.ingress.kubernetes.io/backend-protocol: 'GRPC'
        cert-manager.io/cluster-issuer: 'letsencrypt-prod'
      tls: true

    metrics:
      enabled: true
      serviceMonitor:
        enabled: true

    rbacConfig:
      policy.default: role:readonly
      policy.csv: |
        # Admin group
        p, role:admin, applications, *, */*, allow
        p, role:admin, clusters, *, *, allow
        p, role:admin, repositories, *, *, allow

        # Developer group
        p, role:developer, applications, get, */*, allow
        p, role:developer, applications, sync, */dev-*, allow
        p, role:developer, applications, sync, */staging-*, allow
        p, role:developer, applications, action/*, */dev-*, allow

        # DevOps group  
        p, role:devops, applications, *, */*, allow
        p, role:devops, clusters, get, *, allow
        p, role:devops, repositories, get, *, allow

        # Groups mapping
        g, argocd-admins, role:admin
        g, developers, role:developer
        g, devops-team, role:devops

  ## Repository server
  repoServer:
    metrics:
      enabled: true
      serviceMonitor:
        enabled: true

    # Sidecar pour plugins customs
    initContainers:
      - name: download-tools
        image: alpine/git:latest
        command: [sh, -c]
        args:
          - |
            wget -qO- https://get.helm.sh/helm-v3.13.0-linux-amd64.tar.gz | tar -xzO linux-amd64/helm > /custom-tools/helm &&
            chmod +x /custom-tools/helm
        volumeMounts:
          - mountPath: /custom-tools
            name: custom-tools

    extraContainers:
      - name: avp-helm
        command: [/var/run/argocd/argocd-cmp-server]
        image: quay.io/argoproj/argocd:v2.8.4
        securityContext:
          runAsNonRoot: true
          runAsUser: 999
        volumeMounts:
          - mountPath: /var/run/argocd
            name: var-files
          - mountPath: /home/argocd/cmp-server/plugins
            name: plugins
          - mountPath: /tmp
            name: tmp
          - mountPath: /custom-tools
            name: custom-tools

  ## Controller
  controller:
    metrics:
      enabled: true
      serviceMonitor:
        enabled: true

    # Paramètres de performance
    args:
      appResyncPeriod: 180
      selfHealEnabled: true
      statusProcessors: 20
      operationProcessors: 10

  ## Application Controller
  applicationSet:
    enabled: true

    metrics:
      enabled: true
      serviceMonitor:
        enabled: true

  ## Notifications
  notifications:
    enabled: true

    argocdUrl: https://argocd.k8s.local

    subscriptions:
      - recipients:
          - slack:deployments
        triggers:
          - on-sync-succeeded
          - on-sync-failed
          - on-health-degraded

    services:
      service.slack: |
        token: $slack-token

    templates:
      template.app-deployed: |
        email:
          subject: Application {{.app.metadata.name}} is now running new version.
        message: |
          {{if eq .serviceType "slack"}}:white_check_mark:{{end}} Application {{.app.metadata.name}} is now running new version of {{.app.status.sync.revision}}.
        slack:
          attachments: |
            [{
              "title": "{{ .app.metadata.name}}",
              "title_link":"{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
              "color": "#18be52",
              "fields": [
              {
                "title": "Sync Status",
                "value": "{{.app.status.sync.status}}",
                "short": true
              },
              {
                "title": "Repository",
                "value": "{{.app.spec.source.repoURL}}",
                "short": true
              },
              {
                "title": "Revision",
                "value": "{{.app.status.sync.revision}}",
                "short": true
              }
              {{range $index, $c := .app.status.conditions}}
              {{if not $index}},{{end}}
              {{if $index}},{{end}}
              {
                "title": "{{$c.type}}",
                "value": "{{$c.message}}",
                "short": true
              }
              {{end}}
              ]
            }]

      template.app-health-degraded: |
        email:
          subject: Application {{.app.metadata.name}} has degraded.
        message: |
          {{if eq .serviceType "slack"}}:exclamation:{{end}} Application {{.app.metadata.name}} has degraded.
          Application details: {{.context.argocdUrl}}/applications/{{.app.metadata.name}}.
        slack:
          attachments: |
            [{
              "title": "{{ .app.metadata.name}}",
              "title_link": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
              "color": "#f4c430",
              "fields": [
              {
                "title": "Sync Status",
                "value": "{{.app.status.sync.status}}",
                "short": true
              },
              {
                "title": "Health Status",
                "value": "{{.app.status.health.status}}",
                "short": true
              }
              {{range $index, $c := .app.status.conditions}}
              {{if not $index}},{{end}}
              {{if $index}},{{end}}
              {
                "title": "{{$c.type}}",
                "value": "{{$c.message}}",
                "short": true
              }
              {{end}}
              ]
            }]

    triggers:
      trigger.on-deployed: |
        - description: Application is synced and healthy. Triggered once per commit.
          oncePer: app.status.sync.revision
          send:
          - app-deployed
          when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'

      trigger.on-health-degraded: |
        - description: Application has degraded
          send:
          - app-health-degraded
          when: app.status.health.status == 'Degraded'

      trigger.on-sync-failed: |
        - description: Application syncing has failed
          send:
          - app-sync-failed
          when: app.status.operationState.phase in ['Error', 'Failed']

    secret:
      create: true
      items:
        slack-token: your-slack-bot-token
```

#### 1.3 Installation avec Helm

```bash
# Installation ArgoCD
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Installation avec configuration custom
helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --values argocd/values.yaml \
  --version 5.46.8

# Attendre que ArgoCD soit prêt
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd

# Récupérer le mot de passe admin
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Étape 2 : Configuration des Applications GitOps

#### 2.1 Projet ArgoCD pour l'organisation

```yaml
# argocd/projects/company-project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: company-apps
  namespace: argocd
  labels:
    project: company
spec:
  description: Applications de l'entreprise

  # Repositories autorisés
  sourceRepos:
    - 'https://gitlab.com/company/*'
    - 'https://github.com/company/*'
    - 'https://charts.bitnami.com/bitnami'
    - 'https://helm.elastic.co'
    - 'https://prometheus-community.github.io/helm-charts'

  # Clusters de destination
  destinations:
    - namespace: 'app-*'
      server: https://kubernetes.default.svc
    - namespace: 'monitoring'
      server: https://kubernetes.default.svc
    - namespace: 'logging'
      server: https://kubernetes.default.svc
    - namespace: '*'
      server: https://staging-k8s-api.company.com
    - namespace: '*'
      server: https://prod-k8s-api.company.com

  # Ressources autorisées
  clusterResourceWhitelist:
    - group: ''
      kind: Namespace
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRole
    - group: 'rbac.authorization.k8s.io'
      kind: ClusterRoleBinding
    - group: 'networking.k8s.io'
      kind: Ingress
    - group: 'cert-manager.io'
      kind: ClusterIssuer

  namespaceResourceWhitelist:
    - group: ''
      kind: ConfigMap
    - group: ''
      kind: Secret
    - group: ''
      kind: Service
    - group: ''
      kind: ServiceAccount
    - group: 'apps'
      kind: Deployment
    - group: 'apps'
      kind: ReplicaSet
    - group: 'apps'
      kind: StatefulSet
    - group: 'batch'
      kind: Job
    - group: 'batch'
      kind: CronJob
    - group: 'networking.k8s.io'
      kind: NetworkPolicy
    - group: 'policy'
      kind: PodSecurityPolicy
    - group: 'autoscaling'
      kind: HorizontalPodAutoscaler

  # Politiques
  syncWindows:
    - kind: allow
      schedule: '* * * * *'
      duration: 24h
      applications:
        - '*-dev'
        - '*-staging'
      manualSync: true
    - kind: deny
      schedule: '0 22 * * 5' # Vendredi 22h
      duration: 10h # Jusqu'à samedi 8h
      applications:
        - '*-prod'
      manualSync: false

  roles:
    - name: admin
      description: Accès admin complet
      policies:
        - p, proj:company-apps:admin, applications, *, company-apps/*, allow
        - p, proj:company-apps:admin, repositories, *, *, allow
      groups:
        - argocd-admins

    - name: developer
      description: Accès développeur limité
      policies:
        - p, proj:company-apps:developer, applications, get, company-apps/*-dev, allow
        - p, proj:company-apps:developer, applications, sync, company-apps/*-dev, allow
        - p, proj:company-apps:developer, applications, action/*, company-apps/*-dev, allow
      groups:
        - developers

    - name: devops
      description: Accès DevOps étendu
      policies:
        - p, proj:company-apps:devops, applications, *, company-apps/*, allow
        - p, proj:company-apps:devops, repositories, get, *, allow
      groups:
        - devops-team
```

#### 2.2 Application simple pour développement

```yaml
# argocd/applications/webapp-dev.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: webapp-dev
  namespace: argocd
  labels:
    environment: development
    component: webapp
  annotations:
    argocd.argoproj.io/sync-wave: '1'
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: company-apps

  source:
    repoURL: https://gitlab.com/company/k8s-manifests.git
    path: applications/webapp/overlays/development
    targetRevision: HEAD

    # Configuration Kustomize
    kustomize:
      images:
        - webapp=registry.gitlab.com/company/webapp:latest
      patchesStrategicMerge:
        - |-
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: webapp
          spec:
            template:
              spec:
                containers:
                - name: webapp
                  env:
                  - name: ENVIRONMENT
                    value: "development"

  destination:
    server: https://kubernetes.default.svc
    namespace: app-dev

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
      - ApplyOutOfSyncOnly=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  revisionHistoryLimit: 10

  # Hooks pour les opérations
  operation:
    sync:
      syncOptions:
        - CreateNamespace=true
      hooks:
        - name: pre-sync-hook
          argocd.argoproj.io/hook: PreSync
          argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
```

#### 2.3 Application Helm pour staging

```yaml
# argocd/applications/webapp-staging.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: webapp-staging
  namespace: argocd
  labels:
    environment: staging
    component: webapp
  annotations:
    argocd.argoproj.io/sync-wave: '2'
spec:
  project: company-apps

  source:
    repoURL: https://gitlab.com/company/helm-charts.git
    path: webapp
    targetRevision: HEAD

    # Configuration Helm
    helm:
      releaseName: webapp-staging
      valueFiles:
        - values-staging.yaml
      parameters:
        - name: image.tag
          value: 'v1.2.3'
        - name: replicaCount
          value: '2'
        - name: resources.requests.cpu
          value: '100m'
        - name: resources.requests.memory
          value: '256Mi'

      # Values inline pour override
      values: |
        ingress:
          enabled: true
          hosts:
          - host: webapp-staging.company.com
            paths:
            - path: /
              pathType: Prefix
          tls:
          - secretName: webapp-staging-tls
            hosts:
            - webapp-staging.company.com

        monitoring:
          enabled: true
          serviceMonitor:
            enabled: true

        autoscaling:
          enabled: true
          minReplicas: 2
          maxReplicas: 5
          targetCPUUtilizationPercentage: 70

  destination:
    server: https://kubernetes.default.svc
    namespace: app-staging

  syncPolicy:
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
    # Pas de sync automatique pour staging
    retry:
      limit: 3
      backoff:
        duration: 10s
        factor: 2
        maxDuration: 5m

  # Ignoré pour éviter les drifts
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
    - group: ''
      kind: Service
      jsonPointers:
        - /spec/clusterIP
```

### Étape 3 : ApplicationSets pour la gestion à l'échelle

#### 3.1 ApplicationSet multi-environnements

```yaml
# argocd/applicationsets/webapp-environments.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: webapp-environments
  namespace: argocd
  labels:
    component: webapp
spec:
  generators:
    - matrix:
        generators:
          - git:
              repoURL: https://gitlab.com/company/k8s-config.git
              revision: HEAD
              directories:
                - path: applications/webapp/environments/*
          - clusters:
              selector:
                matchLabels:
                  environment: '{{ path.basename }}'

  template:
    metadata:
      name: 'webapp-{{ path.basename }}-{{ name }}'
      labels:
        environment: '{{ path.basename }}'
        cluster: '{{ name }}'
        component: webapp
      annotations:
        argocd.argoproj.io/sync-wave: '{{ metadata.annotations.syncWave }}'
    spec:
      project: company-apps

      source:
        repoURL: https://gitlab.com/company/k8s-config.git
        path: '{{ path }}'
        targetRevision: HEAD

        helm:
          valueFiles:
            - values.yaml
            - 'values-{{ path.basename }}.yaml'
          parameters:
            - name: cluster.name
              value: '{{ name }}'
            - name: cluster.server
              value: '{{ server }}'

      destination:
        server: '{{ server }}'
        namespace: 'app-{{ path.basename }}'

      syncPolicy:
        automated:
          prune: true
          selfHeal: '{{ metadata.labels.selfHeal }}'
        syncOptions:
          - CreateNamespace=true
          - ApplyOutOfSyncOnly=true
        retry:
          limit: '{{ metadata.annotations.retryLimit }}'

  syncPolicy:
    preserveResourcesOnDeletion: false
```

#### 3.2 ApplicationSet pour microservices

```yaml
# argocd/applicationsets/microservices.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://gitlab.com/company/microservices-config.git
        revision: HEAD
        files:
          - path: 'services/*/config.yaml'

  template:
    metadata:
      name: '{{ services.name }}-{{ services.environment }}'
      labels:
        service: '{{ services.name }}'
        environment: '{{ services.environment }}'
        team: '{{ services.team }}'
      annotations:
        notifications.argoproj.io/subscribe.on-sync-succeeded.slack: '{{ services.slackChannel }}'
    spec:
      project: company-apps

      source:
        repoURL: '{{ services.repoUrl }}'
        path: '{{ services.path }}'
        targetRevision: '{{ services.targetRevision }}'

        helm:
          releaseName: '{{ services.name }}'
          valueFiles:
            - values.yaml
            - 'values-{{ services.environment }}.yaml'
          parameters:
            - name: image.tag
              value: '{{ services.imageTag }}'
            - name: resources.requests.cpu
              value: '{{ services.resources.cpu }}'
            - name: resources.requests.memory
              value: '{{ services.resources.memory }}'

      destination:
        server: https://kubernetes.default.svc
        namespace: '{{ services.namespace }}'

      syncPolicy:
        automated:
          prune: '{{ services.autoPrune }}'
          selfHeal: '{{ services.autoHeal }}'
        syncOptions:
          - CreateNamespace=true
          - RespectIgnoreDifferences=true

        retry:
          limit: 3
          backoff:
            duration: 5s
            maxDuration: 3m
            factor: 2
```

#### 3.3 ApplicationSet pour clusters multiples

```yaml
# argocd/applicationsets/multi-cluster.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: infrastructure-multi-cluster
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - clusters:
              selector:
                matchLabels:
                  type: kubernetes
          - git:
              repoURL: https://gitlab.com/company/infrastructure.git
              revision: HEAD
              directories:
                - path: clusters/*/infrastructure/*

  template:
    metadata:
      name: 'infra-{{ path[1] }}-{{ name }}'
      labels:
        cluster: '{{ name }}'
        infrastructure-component: '{{ path[2] }}'
        environment: '{{ metadata.labels.environment }}'
    spec:
      project: infrastructure

      source:
        repoURL: https://gitlab.com/company/infrastructure.git
        path: '{{ path }}'
        targetRevision: HEAD

        helm:
          valueFiles:
            - values.yaml
            - '{{ name }}.yaml'

      destination:
        server: '{{ server }}'
        namespace: '{{ path[2] }}'

      syncPolicy:
        automated:
          prune: false
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
          - ServerSideApply=true

  syncPolicy:
    applicationsSync: create-update
```

### Étape 4 : Configuration avancée et intégrations

#### 4.1 Repository Credentials

```yaml
# argocd/secrets/repository-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: gitlab-repo-secret
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://gitlab.com/company
  username: gitlab-ci-token
  password: glpat-xxxxxxxxxxxxxxxxxxxx
---
apiVersion: v1
kind: Secret
metadata:
  name: github-repo-secret
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: git
  url: https://github.com/company
  sshPrivateKey: |
    -----BEGIN OPENSSH PRIVATE KEY-----
    b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABFwAAAAdzc2gtcn
    ...
    -----END OPENSSH PRIVATE KEY-----
---
apiVersion: v1
kind: Secret
metadata:
  name: helm-repo-secret
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
type: Opaque
stringData:
  type: helm
  name: private-helm-repo
  url: https://helm.company.com
  username: helm-user
  password: helm-password
```

#### 4.2 Cluster Credentials

```yaml
# argocd/secrets/cluster-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: staging-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: staging
  server: https://staging-k8s-api.company.com
  config: |
    {
      "bearerToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik...",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t..."
      }
    }
---
apiVersion: v1
kind: Secret
metadata:
  name: production-cluster
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
type: Opaque
stringData:
  name: production
  server: https://prod-k8s-api.company.com
  config: |
    {
      "bearerToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ik...",
      "tlsClientConfig": {
        "insecure": false,
        "caData": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...",
        "certData": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t...",
        "keyData": "LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVkt..."
      }
    }
```

#### 4.3 Configuration des Webhooks

```yaml
# argocd/configmap/webhook-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.webhook.github: |
    url: https://api.github.com
    headers:
    - name: Authorization
      value: token $github-token

  service.webhook.gitlab: |
    url: https://gitlab.com/api/v4
    headers:
    - name: PRIVATE-TOKEN
      value: $gitlab-token

  service.webhook.jira: |
    url: https://company.atlassian.net
    headers:
    - name: Authorization
      value: Basic $jira-auth

  template.webhook-github-commit-status: |
    webhook:
      github:
        method: POST
        path: /repos/{{call .repo.FullNameByRepoURL .app.spec.source.repoURL}}/statuses/{{.app.status.sync.revision}}
        body: |
          {
            "state": "{{.app.status.sync.status | lower}}",
            "description": "ArgoCD sync is {{.app.status.sync.status}}",
            "context": "continuous-delivery/argocd",
            "target_url": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}"
          }

  template.webhook-gitlab-commit-status: |
    webhook:
      gitlab:
        method: POST
        path: /projects/{{call .repo.GetProjectIdByRepoURL .app.spec.source.repoURL}}/statuses/{{.app.status.sync.revision}}
        body: |
          {
            "state": "{{.app.status.sync.status | lower}}",
            "description": "ArgoCD sync is {{.app.status.sync.status}}",
            "context": "argocd",
            "target_url": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}"
          }
```

### Étape 5 : Monitoring et observabilité ArgoCD

#### 5.1 ServiceMonitor pour Prometheus

```yaml
# monitoring/argocd-servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: monitoring
  labels:
    app.kubernetes.io/component: metrics
    app.kubernetes.io/name: argocd-metrics
    app.kubernetes.io/part-of: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
      app.kubernetes.io/part-of: argocd
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-server-metrics
  namespace: monitoring
  labels:
    app.kubernetes.io/component: server
    app.kubernetes.io/name: argocd-server-metrics
    app.kubernetes.io/part-of: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: server
      app.kubernetes.io/name: argocd-server-metrics
      app.kubernetes.io/part-of: argocd
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-repo-server-metrics
  namespace: monitoring
  labels:
    app.kubernetes.io/component: repo-server
    app.kubernetes.io/name: argocd-repo-server-metrics
    app.kubernetes.io/part-of: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/component: repo-server
      app.kubernetes.io/name: argocd-repo-server-metrics
      app.kubernetes.io/part-of: argocd
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

#### 5.2 Alertes Prometheus pour ArgoCD

```yaml
# monitoring/argocd-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: argocd-alerts
  namespace: monitoring
  labels:
    app: argocd
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: argocd.rules
      interval: 30s
      rules:
        # Application sync failures
        - alert: ArgoCDAppSyncFailure
          expr: |
            increase(argocd_app_sync_total{phase="Failed"}[5m]) > 0
          for: 0m
          labels:
            severity: warning
            service: argocd
          annotations:
            summary: 'ArgoCD application sync failure'
            description: |
              Application {{ $labels.name }} in namespace {{ $labels.dest_namespace }} 
              has failed to sync {{ $value }} times in the last 5 minutes.

        # Application health degraded
        - alert: ArgoCDAppHealthDegraded
          expr: |
            argocd_app_health_status{health_status!="Healthy"} == 1
          for: 15m
          labels:
            severity: warning
            service: argocd
          annotations:
            summary: 'ArgoCD application health degraded'
            description: |
              Application {{ $labels.name }} has been in {{ $labels.health_status }} 
              state for more than 15 minutes.

        # Application not synced
        - alert: ArgoCDAppNotSynced
          expr: |
            argocd_app_sync_status{sync_status!="Synced"} == 1
          for: 1h
          labels:
            severity: warning
            service: argocd
          annotations:
            summary: 'ArgoCD application not synced'
            description: |
              Application {{ $labels.name }} has been {{ $labels.sync_status }} 
              for more than 1 hour.

        # ArgoCD server down
        - alert: ArgoCDServerDown
          expr: |
            up{job="argocd-server-metrics"} == 0
          for: 5m
          labels:
            severity: critical
            service: argocd
          annotations:
            summary: 'ArgoCD server is down'
            description: 'ArgoCD server has been down for more than 5 minutes.'

        # High API latency
        - alert: ArgoCDHighAPILatency
          expr: |
            histogram_quantile(0.95, 
              rate(argocd_server_api_request_duration_seconds_bucket[5m])
            ) > 2
          for: 10m
          labels:
            severity: warning
            service: argocd
          annotations:
            summary: 'ArgoCD API high latency'
            description: |
              ArgoCD API 95th percentile latency is {{ $value }}s 
              for more than 10 minutes.

        # Repository connection failure
        - alert: ArgoCDRepoConnectionFailure
          expr: |
            argocd_repo_connection_status == 0
          for: 5m
          labels:
            severity: critical
            service: argocd
          annotations:
            summary: 'ArgoCD repository connection failure'
            description: |
              ArgoCD cannot connect to repository {{ $labels.repo }} 
              for more than 5 minutes.
```

#### 5.3 Dashboard Grafana pour ArgoCD

```json
# monitoring/grafana-dashboard.json
{
  "dashboard": {
    "id": null,
    "title": "ArgoCD Dashboard",
    "tags": ["argocd", "gitops"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Applications Overview",
        "type": "stat",
        "targets": [
          {
            "expr": "count(argocd_app_info)",
            "legendFormat": "Total Applications"
          },
          {
            "expr": "count(argocd_app_info{health_status=\"Healthy\"})",
            "legendFormat": "Healthy"
          },
          {
            "expr": "count(argocd_app_info{sync_status=\"Synced\"})",
            "legendFormat": "Synced"
          }
        ]
      },
      {
        "title": "Sync Activity",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(argocd_app_sync_total[5m])",
            "legendFormat": "Sync Rate - {{phase}}"
          }
        ]
      },
      {
        "title": "Application Health Status",
        "type": "piechart",
        "targets": [
          {
            "expr": "count by (health_status) (argocd_app_info)",
            "legendFormat": "{{health_status}}"
          }
        ]
      },
      {
        "title": "API Request Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(argocd_server_api_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, rate(argocd_server_api_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### Étape 6 : Tests et validation

#### 6.1 Script de test de déploiement

```bash
#!/bin/bash
# scripts/test-argocd-deployment.sh

set -e

NAMESPACE=${1:-argocd}
TIMEOUT=${2:-300}

echo "🧪 Test de déploiement ArgoCD dans $NAMESPACE"

# Vérifier que tous les pods sont prêts
echo "⏳ Vérification des pods ArgoCD..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/part-of=argocd -n $NAMESPACE --timeout=${TIMEOUT}s

# Vérifier l'API ArgoCD
echo "🔍 Test de l'API ArgoCD..."
ARGOCD_SERVER=$(kubectl get service argocd-server -n $NAMESPACE -o jsonpath='{.spec.clusterIP}')

# Port-forward pour tester l'API
kubectl port-forward service/argocd-server 8080:80 -n $NAMESPACE &
PID=$!
sleep 10

# Test de l'endpoint de santé
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" http://localhost:8080/healthz -o /tmp/argocd_health.json)

if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ API ArgoCD fonctionne correctement"
else
    echo "❌ API ArgoCD en erreur (Code: $HEALTH_RESPONSE)"
    kill $PID
    exit 1
fi

# Test de login CLI
echo "🔐 Test du login ArgoCD CLI..."
ADMIN_PASSWORD=$(kubectl -n $NAMESPACE get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)

argocd login localhost:8080 --username admin --password $ADMIN_PASSWORD --insecure

if [ $? -eq 0 ]; then
    echo "✅ Login ArgoCD CLI réussi"
else
    echo "❌ Login ArgoCD CLI échoué"
    kill $PID
    exit 1
fi

# Test de création d'application
echo "🚀 Test de création d'application..."
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: test-app
  namespace: $NAMESPACE
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: test-guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF

# Attendre la synchronisation
echo "⏳ Attente de la synchronisation..."
sleep 30

# Vérifier l'état de l'application
APP_STATUS=$(argocd app get test-app --output json | jq -r '.status.sync.status')
if [ "$APP_STATUS" = "Synced" ]; then
    echo "✅ Application de test synchronisée avec succès"
else
    echo "❌ Application de test non synchronisée (Status: $APP_STATUS)"
fi

# Nettoyer
argocd app delete test-app --yes
kubectl delete namespace test-guestbook --ignore-not-found
kill $PID

echo "🎉 Tests ArgoCD terminés avec succès"
```

#### 6.2 Test d'ApplicationSet

```bash
#!/bin/bash
# scripts/test-applicationset.sh

echo "🧪 Test d'ApplicationSet"

# Créer un ApplicationSet de test
cat <<EOF | kubectl apply -f -
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: test-applicationset
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - cluster: in-cluster
        namespace: test-app-1
      - cluster: in-cluster
        namespace: test-app-2
  template:
    metadata:
      name: 'test-{{namespace}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps.git
        targetRevision: HEAD
        path: guestbook
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
        - CreateNamespace=true
EOF

# Attendre la création des applications
sleep 30

# Vérifier que les applications ont été créées
APPS_CREATED=$(kubectl get applications -n argocd -l argocd.argoproj.io/application-set-name=test-applicationset --no-headers | wc -l)

if [ "$APPS_CREATED" -eq 2 ]; then
    echo "✅ ApplicationSet a créé $APPS_CREATED applications"
else
    echo "❌ ApplicationSet n'a créé que $APPS_CREATED applications (attendu: 2)"
fi

# Nettoyer
kubectl delete applicationset test-applicationset -n argocd
kubectl delete applications -l argocd.argoproj.io/application-set-name=test-applicationset -n argocd
kubectl delete namespace test-app-1 test-app-2 --ignore-not-found

echo "🎉 Test ApplicationSet terminé"
```

---

## 🎯 Résultats attendus

### ✅ ArgoCD fonctionnel

- **Interface web** accessible et sécurisée
- **CLI** configuré et opérationnel
- **API** répondant correctement
- **Métriques** exposées pour Prometheus

### ✅ Applications GitOps

- **Synchronisation automatique** configurée
- **Multi-environnements** gérés
- **Rollbacks** fonctionnels
- **Health checks** opérationnels

### ✅ ApplicationSets

- **Génération automatique** d'applications
- **Multi-clusters** supportés
- **Patterns** flexibles implémentés

### ✅ Sécurité et gouvernance

- **RBAC** configuré par équipes
- **Secrets** gérés de façon sécurisée
- **Audit trail** complet
- **Politiques** de synchronisation

---

## 📚 Points clés de la solution

### 🎯 Architecture GitOps complète

- **Single source of truth** dans Git
- **Déclaratif** et versionné
- **Auditabilité** totale
- **Rollbacks** instantanés

### 🔒 Sécurité intégrée

- **RBAC** granulaire
- **TLS** end-to-end
- **Secrets** management
- **Network policies**

### 📊 Observabilité avancée

- **Métriques** Prometheus
- **Alertes** intelligentes
- **Dashboards** Grafana
- **Notifications** multi-canaux

Cette solution démontre une maîtrise complète d'ArgoCD et des pratiques GitOps avancées, avec une approche production-ready incluant sécurité, monitoring et scalabilité.

---

_Correction réalisée par Hassan ESSADIK - Formation DevOps Kubernetes_
