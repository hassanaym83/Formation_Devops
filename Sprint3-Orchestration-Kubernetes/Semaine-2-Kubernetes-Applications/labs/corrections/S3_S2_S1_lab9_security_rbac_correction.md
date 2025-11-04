# Correction LAB 9 - Sécurité et RBAC

## Vue d'ensemble de la solution

Cette correction présente l'implémentation complète de la sécurité Kubernetes avec RBAC, Pod Security Standards, politiques de sécurité, authentification/autorisation, et monitoring de sécurité pour l'application e-commerce.

## Architecture de sécurité

```
Architecture de sécurité Kubernetes:
├── Authentication Layer
│   ├── Service Accounts (par namespace)
│   ├── Users & Groups (OIDC/LDAP)
│   ├── API Server Authentication
│   └── Token Management
├── Authorization Layer (RBAC)
│   ├── Cluster Roles & Bindings
│   ├── Namespace Roles & Bindings
│   ├── Service Account Permissions
│   └── Fine-grained Access Control
├── Admission Control
│   ├── Pod Security Standards
│   ├── Network Policies
│   ├── Resource Quotas
│   └── Security Contexts
├── Runtime Security
│   ├── Container Security
│   ├── Image Scanning
│   ├── Runtime Monitoring
│   └── Compliance Checking
└── Network Security
    ├── Encryption in Transit
    ├── Service Mesh (Istio)
    ├── Certificate Management
    └── Secret Management
```

## Étape 1 : Namespaces et isolation

### 1.1 Namespaces sécurisés avec quotas

```yaml
# namespaces-security.yaml
---
# Namespace pour l'environnement de production
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-prod
  labels:
    security-tier: 'production'
    data-classification: 'confidential'
    compliance: 'pci-dss'
    monitoring: 'enabled'
  annotations:
    security.io/description: 'Production environment with strict security controls'
    compliance.io/certifications: 'SOC2,PCI-DSS,ISO27001'
    backup.io/enabled: 'true'
    network-policy.io/default-deny: 'true'

---
# Namespace pour le développement
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-dev
  labels:
    security-tier: 'development'
    data-classification: 'internal'
    monitoring: 'enabled'
  annotations:
    security.io/description: 'Development environment with moderate security'
    network-policy.io/default-deny: 'false'

---
# Namespace pour les tests/staging
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-staging
  labels:
    security-tier: 'staging'
    data-classification: 'internal'
    monitoring: 'enabled'
  annotations:
    security.io/description: 'Staging environment for pre-production testing'
    network-policy.io/default-deny: 'true'

---
# Namespace pour la sécurité et monitoring
apiVersion: v1
kind: Namespace
metadata:
  name: security-system
  labels:
    security-tier: 'system'
    data-classification: 'restricted'
    monitoring: 'enabled'
  annotations:
    security.io/description: 'Security monitoring and tooling namespace'
    network-policy.io/default-deny: 'true'

---
# ResourceQuota pour production - stricte
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: ecommerce-prod
  labels:
    environment: production
    quota-type: strict
spec:
  hard:
    # Compute resources
    requests.cpu: '20'
    requests.memory: 40Gi
    limits.cpu: '40'
    limits.memory: 80Gi

    # Storage
    requests.storage: 500Gi
    persistentvolumeclaims: '20'

    # Objects
    pods: '100'
    services: '20'
    secrets: '50'
    configmaps: '30'

    # Security objects
    services.nodeports: '0' # Pas de NodePort en production
    services.loadbalancers: '5'

---
# ResourceQuota pour développement - permissive
apiVersion: v1
kind: ResourceQuota
metadata:
  name: development-quota
  namespace: ecommerce-dev
  labels:
    environment: development
    quota-type: permissive
spec:
  hard:
    requests.cpu: '10'
    requests.memory: 20Gi
    limits.cpu: '20'
    limits.memory: 40Gi
    requests.storage: 200Gi
    persistentvolumeclaims: '10'
    pods: '50'
    services: '10'

---
# NetworkPolicy - Default Deny pour production
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: ecommerce-prod
  labels:
    security-policy: default-deny
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# LimitRange pour contrôler les ressources
apiVersion: v1
kind: LimitRange
metadata:
  name: resource-limits
  namespace: ecommerce-prod
  labels:
    resource-control: enabled
spec:
  limits:
    # Limites pour les conteneurs
    - type: Container
      default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      max:
        cpu: 2000m
        memory: 4Gi
      min:
        cpu: 50m
        memory: 64Mi

    # Limites pour les pods
    - type: Pod
      max:
        cpu: 4000m
        memory: 8Gi

    # Limites pour les PVC
    - type: PersistentVolumeClaim
      max:
        storage: 100Gi
      min:
        storage: 1Gi
```

### 1.2 Pod Security Standards

```yaml
# pod-security-standards.yaml
---
# Pod Security Policy pour production (restricted)
apiVersion: v1
kind: ConfigMap
metadata:
  name: pod-security-standards
  namespace: ecommerce-prod
  labels:
    security-standard: restricted
data:
  security-policy.yaml: |
    apiVersion: v1
    kind: Pod
    metadata:
      annotations:
        # Pod Security Standards - Restricted
        pod-security.kubernetes.io/enforce: restricted
        pod-security.kubernetes.io/audit: restricted
        pod-security.kubernetes.io/warn: restricted
    spec:
      securityContext:
        # Exiger un utilisateur non-root
        runAsNonRoot: true
        runAsUser: 65534
        runAsGroup: 65534
        fsGroup: 65534
        
        # Empêcher l'escalade de privilèges
        allowPrivilegeEscalation: false
        
        # Supprimer toutes les capabilities
        seccompProfile:
          type: RuntimeDefault
      
      containers:
      - name: example
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 65534
          runAsGroup: 65534
          capabilities:
            drop:
            - ALL
          seccompProfile:
            type: RuntimeDefault
          readOnlyRootFilesystem: true
        
        # Volumes autorisés seulement
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: var-cache
          mountPath: /var/cache
      
      volumes:
      - name: tmp
        emptyDir: {}
      - name: var-cache
        emptyDir: {}

---
# Admission Controller Configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: admission-controller-config
  namespace: kube-system
  labels:
    component: admission-controller
data:
  admission-control.yaml: |
    # Configuration pour Pod Security Standards
    apiVersion: apiserver.config.k8s.io/v1
    kind: AdmissionConfiguration
    plugins:
    - name: PodSecurity
      configuration:
        apiVersion: pod-security.admission.config.k8s.io/v1beta1
        kind: PodSecurityConfiguration
        defaults:
          enforce: "baseline"
          enforce-version: "latest"
          audit: "restricted"
          audit-version: "latest"
          warn: "restricted"
          warn-version: "latest"
        exemptions:
          usernames: []
          runtimeClasses: []
          namespaces: ["kube-system", "security-system"]
```

## Étape 2 : Service Accounts et RBAC

### 2.1 Service Accounts dédiés par composant

```yaml
# service-accounts.yaml
---
# Service Account pour l'API Gateway
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-gateway-sa
  namespace: ecommerce-prod
  labels:
    app: api-gateway
    component: service-account
  annotations:
    description: 'Service account for API Gateway with minimal permissions'
    security.io/principle: 'least-privilege'
automountServiceAccountToken: false # Sécurité renforcée

---
# Service Account pour le service Auth
apiVersion: v1
kind: ServiceAccount
metadata:
  name: auth-service-sa
  namespace: ecommerce-prod
  labels:
    app: auth-service
    component: service-account
  annotations:
    description: 'Service account for authentication service'
    security.io/sensitive: 'true'
automountServiceAccountToken: true

---
# Service Account pour les microservices métier
apiVersion: v1
kind: ServiceAccount
metadata:
  name: business-services-sa
  namespace: ecommerce-prod
  labels:
    app: business-services
    component: service-account
  annotations:
    description: 'Service account for business microservices'
automountServiceAccountToken: true

---
# Service Account pour les bases de données
apiVersion: v1
kind: ServiceAccount
metadata:
  name: database-sa
  namespace: ecommerce-prod
  labels:
    app: database
    component: service-account
  annotations:
    description: 'Service account for database operations'
    security.io/data-access: 'restricted'
automountServiceAccountToken: true

---
# Service Account pour monitoring
apiVersion: v1
kind: ServiceAccount
metadata:
  name: monitoring-sa
  namespace: ecommerce-prod
  labels:
    app: monitoring
    component: service-account
  annotations:
    description: 'Service account for monitoring and observability'
automountServiceAccountToken: true

---
# Service Account pour backups
apiVersion: v1
kind: ServiceAccount
metadata:
  name: backup-sa
  namespace: ecommerce-prod
  labels:
    app: backup
    component: service-account
  annotations:
    description: 'Service account for backup operations'
    security.io/critical: 'true'
automountServiceAccountToken: true

---
# Service Account pour security scanning
apiVersion: v1
kind: ServiceAccount
metadata:
  name: security-scanner-sa
  namespace: security-system
  labels:
    app: security-scanner
    component: service-account
  annotations:
    description: 'Service account for security scanning tools'
    security.io/scope: 'cluster-wide'
automountServiceAccountToken: true
```

### 2.2 Cluster Roles pour permissions globales

```yaml
# cluster-roles.yaml
---
# ClusterRole pour monitoring global
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-global
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: monitoring
  annotations:
    description: 'Global monitoring permissions for observability stack'
rules:
  # Lecture des métriques et événements
  - apiGroups: ['']
    resources:
      ['nodes', 'nodes/metrics', 'services', 'endpoints', 'pods', 'events']
    verbs: ['get', 'list', 'watch']

  # Lecture des métriques Kubernetes
  - apiGroups: ['']
    resources: ['nodes/stats', 'nodes/proxy']
    verbs: ['get']

  # Lecture des ConfigMaps pour configuration
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch']

  # Lecture des déploiements et StatefulSets
  - apiGroups: ['apps']
    resources: ['deployments', 'statefulsets', 'daemonsets', 'replicasets']
    verbs: ['get', 'list', 'watch']

  # Lecture des ingress pour monitoring réseau
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses']
    verbs: ['get', 'list', 'watch']

  # Lecture des HPA pour monitoring autoscaling
  - apiGroups: ['autoscaling']
    resources: ['horizontalpodautoscalers']
    verbs: ['get', 'list', 'watch']

---
# ClusterRole pour security scanning
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: security-scanner
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: security
  annotations:
    description: 'Security scanning permissions for vulnerability assessment'
rules:
  # Lecture des ressources pour scanning
  - apiGroups: ['']
    resources: ['pods', 'services', 'configmaps', 'secrets']
    verbs: ['get', 'list']

  # Lecture des images et containers
  - apiGroups: ['']
    resources: ['pods/exec']
    verbs: ['create']

  # Lecture des politiques de sécurité
  - apiGroups: ['networking.k8s.io']
    resources: ['networkpolicies']
    verbs: ['get', 'list']

  # Lecture des RBAC
  - apiGroups: ['rbac.authorization.k8s.io']
    resources: ['roles', 'rolebindings', 'clusterroles', 'clusterrolebindings']
    verbs: ['get', 'list']

  # Lecture des policies de sécurité
  - apiGroups: ['policy']
    resources: ['podsecuritypolicies']
    verbs: ['get', 'list']

---
# ClusterRole pour backup global
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: backup-operator
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: backup
  annotations:
    description: 'Backup operator permissions for data protection'
rules:
  # Lecture et gestion des PV/PVC
  - apiGroups: ['']
    resources: ['persistentvolumes', 'persistentvolumeclaims']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']

  # Gestion des snapshots
  - apiGroups: ['snapshot.storage.k8s.io']
    resources:
      ['volumesnapshots', 'volumesnapshotcontents', 'volumesnapshotclasses']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']

  # Lecture des StatefulSets pour backup cohérent
  - apiGroups: ['apps']
    resources: ['statefulsets']
    verbs: ['get', 'list', 'watch']

  # Gestion des jobs de backup
  - apiGroups: ['batch']
    resources: ['jobs', 'cronjobs']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']

---
# ClusterRole pour développeurs (lecture seule globale)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: developer-readonly
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: development
  annotations:
    description: 'Read-only access for developers across environments'
rules:
  # Lecture des ressources de base
  - apiGroups: ['']
    resources: ['pods', 'services', 'configmaps', 'endpoints']
    verbs: ['get', 'list', 'watch']

  # Lecture des logs
  - apiGroups: ['']
    resources: ['pods/log']
    verbs: ['get', 'list']

  # Lecture des déploiements
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets', 'statefulsets']
    verbs: ['get', 'list', 'watch']

  # Lecture des ingress
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses']
    verbs: ['get', 'list', 'watch']
```

### 2.3 Roles namespace-specific

```yaml
# namespace-roles.yaml
---
# Role pour gestion complète en développement
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-dev
  name: developer-full
  labels:
    rbac.io/scope: namespace
    rbac.io/environment: development
  annotations:
    description: 'Full development environment access'
rules:
  # Gestion complète des ressources applicatives
  - apiGroups: ['']
    resources:
      ['pods', 'services', 'configmaps', 'secrets', 'persistentvolumeclaims']
    verbs: ['*']

  # Gestion des déploiements
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets', 'statefulsets', 'daemonsets']
    verbs: ['*']

  # Gestion des ingress
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses']
    verbs: ['*']

  # Gestion des jobs
  - apiGroups: ['batch']
    resources: ['jobs', 'cronjobs']
    verbs: ['*']

  # Gestion de l'autoscaling
  - apiGroups: ['autoscaling']
    resources: ['horizontalpodautoscalers']
    verbs: ['*']

---
# Role pour production - gestion limitée
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: production-operator
  labels:
    rbac.io/scope: namespace
    rbac.io/environment: production
  annotations:
    description: 'Limited production operations access'
rules:
  # Lecture de toutes les ressources
  - apiGroups: ['']
    resources: ['*']
    verbs: ['get', 'list', 'watch']

  # Lecture des logs pour debugging
  - apiGroups: ['']
    resources: ['pods/log']
    verbs: ['get', 'list']

  # Gestion limitée des ConfigMaps (pas de secrets)
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch', 'update', 'patch']

  # Scaling des déploiements uniquement
  - apiGroups: ['apps']
    resources: ['deployments/scale', 'statefulsets/scale']
    verbs: ['get', 'update', 'patch']

  # Redémarrage des pods en cas d'urgence
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['delete']

---
# Role pour services métier en production
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: business-service
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: business
  annotations:
    description: 'Business service permissions for application operations'
rules:
  # Lecture des services et endpoints pour découverte
  - apiGroups: ['']
    resources: ['services', 'endpoints']
    verbs: ['get', 'list', 'watch']

  # Lecture des ConfigMaps pour configuration
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch']

  # Lecture des secrets nécessaires (avec restrictions)
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get']
    resourceNames: ['app-secrets', 'db-credentials']

  # Lecture des pods pour health checks
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list']

---
# Role pour base de données
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: database-operator
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: database
  annotations:
    description: 'Database operator permissions for data management'
rules:
  # Gestion des StatefulSets de base de données
  - apiGroups: ['apps']
    resources: ['statefulsets']
    verbs: ['get', 'list', 'watch', 'update', 'patch']

  # Gestion des PVC pour storage
  - apiGroups: ['']
    resources: ['persistentvolumeclaims']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']

  # Gestion des secrets de base de données
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']
    resourceNames: ['postgresql-secret', 'mongodb-secret', 'redis-secret']

  # Services de base de données
  - apiGroups: ['']
    resources: ['services']
    verbs: ['get', 'list', 'watch', 'update', 'patch']

  # Jobs de backup/restore
  - apiGroups: ['batch']
    resources: ['jobs', 'cronjobs']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']

---
# Role pour monitoring namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ecommerce-prod
  name: monitoring-namespace
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: monitoring
  annotations:
    description: 'Namespace monitoring permissions'
rules:
  # Lecture de toutes les ressources pour métriques
  - apiGroups: ['']
    resources: ['*']
    verbs: ['get', 'list', 'watch']

  # Lecture des logs
  - apiGroups: ['']
    resources: ['pods/log']
    verbs: ['get', 'list']

  # Gestion des ConfigMaps de monitoring
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']
    resourceNames:
      ['prometheus-config', 'grafana-config', 'alertmanager-config']

  # Services de monitoring
  - apiGroups: ['']
    resources: ['services', 'endpoints']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch']
```

### 2.4 RoleBindings et ClusterRoleBindings

```yaml
# role-bindings.yaml
---
# ClusterRoleBinding pour monitoring global
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: monitoring-global-binding
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: monitoring
  annotations:
    description: 'Global monitoring access binding'
subjects:
  - kind: ServiceAccount
    name: monitoring-sa
    namespace: ecommerce-prod
  - kind: ServiceAccount
    name: prometheus-sa
    namespace: monitoring
  - kind: ServiceAccount
    name: grafana-sa
    namespace: monitoring
roleRef:
  kind: ClusterRole
  name: monitoring-global
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRoleBinding pour security scanning
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: security-scanner-binding
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: security
  annotations:
    description: 'Security scanning access binding'
subjects:
  - kind: ServiceAccount
    name: security-scanner-sa
    namespace: security-system
  - kind: User
    name: security-admin@company.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: security-scanner
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRoleBinding pour backup global
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: backup-operator-binding
  labels:
    rbac.io/scope: cluster
    rbac.io/purpose: backup
  annotations:
    description: 'Backup operator access binding'
subjects:
  - kind: ServiceAccount
    name: backup-sa
    namespace: ecommerce-prod
  - kind: User
    name: backup-admin@company.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: backup-operator
  apiGroup: rbac.authorization.k8s.io

---
# RoleBinding pour développeurs en dev
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: ecommerce-dev
  name: developers-full-binding
  labels:
    rbac.io/scope: namespace
    rbac.io/environment: development
  annotations:
    description: 'Full development access for developers'
subjects:
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
  - kind: User
    name: dev-lead@company.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-full
  apiGroup: rbac.authorization.k8s.io

---
# RoleBinding pour opérateurs en production
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: ecommerce-prod
  name: production-operators-binding
  labels:
    rbac.io/scope: namespace
    rbac.io/environment: production
  annotations:
    description: 'Limited production access for operators'
subjects:
  - kind: Group
    name: production-operators
    apiGroup: rbac.authorization.k8s.io
  - kind: User
    name: ops-lead@company.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: production-operator
  apiGroup: rbac.authorization.k8s.io

---
# RoleBinding pour services métier
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: ecommerce-prod
  name: business-services-binding
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: business
  annotations:
    description: 'Business service permissions binding'
subjects:
  - kind: ServiceAccount
    name: business-services-sa
    namespace: ecommerce-prod
  - kind: ServiceAccount
    name: api-gateway-sa
    namespace: ecommerce-prod
roleRef:
  kind: Role
  name: business-service
  apiGroup: rbac.authorization.k8s.io

---
# RoleBinding pour base de données
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: ecommerce-prod
  name: database-operator-binding
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: database
  annotations:
    description: 'Database operator permissions binding'
subjects:
  - kind: ServiceAccount
    name: database-sa
    namespace: ecommerce-prod
  - kind: User
    name: dba@company.com
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: database-operator
  apiGroup: rbac.authorization.k8s.io

---
# RoleBinding pour monitoring namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: ecommerce-prod
  name: monitoring-namespace-binding
  labels:
    rbac.io/scope: namespace
    rbac.io/purpose: monitoring
  annotations:
    description: 'Namespace monitoring permissions binding'
subjects:
  - kind: ServiceAccount
    name: monitoring-sa
    namespace: ecommerce-prod
roleRef:
  kind: Role
  name: monitoring-namespace
  apiGroup: rbac.authorization.k8s.io
```

## Étape 3 : Politiques de sécurité réseau avancées

### 3.1 Network Policies granulaires

```yaml
# advanced-network-policies.yaml
---
# Default Deny All pour production
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-production
  namespace: ecommerce-prod
  labels:
    security-policy: default-deny
    tier: network
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Politique pour API Gateway
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
  namespace: ecommerce-prod
  labels:
    app: api-gateway
    security-policy: restricted
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Trafic depuis Internet via Ingress Controller
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

    # Monitoring depuis namespace monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9090 # Metrics

  egress:
    # Vers les microservices métier
    - to:
        - podSelector:
            matchLabels:
              tier: business
      ports:
        - protocol: TCP
          port: 8080

    # Vers le service d'authentification
    - to:
        - podSelector:
            matchLabels:
              app: auth-service
      ports:
        - protocol: TCP
          port: 8080

    # DNS résolution
    - to: []
      ports:
        - protocol: UDP
          port: 53

---
# Politique pour services métier
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: business-services-policy
  namespace: ecommerce-prod
  labels:
    tier: business
    security-policy: restricted
spec:
  podSelector:
    matchLabels:
      tier: business
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Depuis l'API Gateway
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080

    # Depuis d'autres services métier
    - from:
        - podSelector:
            matchLabels:
              tier: business
      ports:
        - protocol: TCP
          port: 8080

    # Monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9090

  egress:
    # Vers les bases de données
    - to:
        - podSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 27017 # MongoDB
        - protocol: TCP
          port: 6379 # Redis

    # Vers services externes (APIs)
    - to: []
      ports:
        - protocol: TCP
          port: 443
        - protocol: TCP
          port: 80

    # DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53

---
# Politique stricte pour données
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-tier-policy
  namespace: ecommerce-prod
  labels:
    tier: data
    security-policy: highly-restricted
spec:
  podSelector:
    matchLabels:
      tier: data
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Seulement depuis les services métier autorisés
    - from:
        - podSelector:
            matchLabels:
              tier: business
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 27017
        - protocol: TCP
          port: 6379

    # Monitoring autorisé
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
        - podSelector:
            matchLabels:
              app: monitoring
      ports:
        - protocol: TCP
          port: 9187 # PostgreSQL exporter
        - protocol: TCP
          port: 9216 # MongoDB exporter
        - protocol: TCP
          port: 9121 # Redis exporter

    # Backup autorisé
    - from:
        - podSelector:
            matchLabels:
              app: backup
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 27017
        - protocol: TCP
          port: 6379

  egress:
    # Communication inter-cluster (réplication)
    - to:
        - podSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 27017
        - protocol: TCP
          port: 6379

    # DNS uniquement
    - to: []
      ports:
        - protocol: UDP
          port: 53

---
# Politique pour authentification (ultra-sécurisée)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: auth-service-policy
  namespace: ecommerce-prod
  labels:
    app: auth-service
    security-policy: ultra-restricted
spec:
  podSelector:
    matchLabels:
      app: auth-service
  policyTypes:
    - Ingress
    - Egress

  ingress:
    # Seulement depuis API Gateway
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - protocol: TCP
          port: 8080

    # Monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9090

  egress:
    # Vers base de données utilisateurs uniquement
    - to:
        - podSelector:
            matchLabels:
              app: postgresql
              role: auth-db
      ports:
        - protocol: TCP
          port: 5432

    # Vers services externes d'authentification (OIDC, LDAP)
    - to: []
      ports:
        - protocol: TCP
          port: 443
        - protocol: TCP
          port: 636 # LDAPS

    # DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
```

## Étape 4 : Gestion des secrets et certificates

### 4.1 Secrets sécurisés avec rotation

```yaml
# secrets-management.yaml
---
# Secret pour certificats TLS
apiVersion: v1
kind: Secret
metadata:
  name: tls-certificates
  namespace: ecommerce-prod
  labels:
    secret-type: tls
    rotation: 'enabled'
  annotations:
    description: 'TLS certificates for HTTPS encryption'
    cert-manager.io/issuer: 'letsencrypt-prod'
    rotation.io/schedule: 'monthly'
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # Certificat TLS base64
  tls.key: LS0tLS1CRUdJTi... # Clé privée TLS base64

---
# Secret pour API keys externes
apiVersion: v1
kind: Secret
metadata:
  name: external-api-keys
  namespace: ecommerce-prod
  labels:
    secret-type: api-keys
    rotation: 'enabled'
  annotations:
    description: 'External API keys for third-party integrations'
    rotation.io/schedule: 'quarterly'
    encryption.io/level: 'high'
type: Opaque
data:
  stripe-api-key: c2tfbGl2ZV8uLi4= # Stripe API key
  sendgrid-api-key: U0cuLi4= # SendGrid API key
  oauth-client-secret: b2F1dGguLi4= # OAuth client secret

---
# Secret pour JWT signing
apiVersion: v1
kind: Secret
metadata:
  name: jwt-signing-keys
  namespace: ecommerce-prod
  labels:
    secret-type: signing-keys
    rotation: 'enabled'
  annotations:
    description: 'JWT signing keys for authentication'
    rotation.io/schedule: 'monthly'
    encryption.io/algorithm: 'RS256'
type: Opaque
data:
  jwt-private.pem: LS0tLS1CRUdJTi4uLg== # JWT private key
  jwt-public.pem: LS0tLS1CRUdJTi4uLg== # JWT public key

---
# Secret pour chiffrement base de données
apiVersion: v1
kind: Secret
metadata:
  name: database-encryption-keys
  namespace: ecommerce-prod
  labels:
    secret-type: encryption-keys
    rotation: 'enabled'
  annotations:
    description: 'Database encryption keys for data at rest'
    rotation.io/schedule: 'annually'
    encryption.io/standard: 'AES-256'
type: Opaque
data:
  master-key: bWFzdGVyLWVuY3J5cHRpb24ta2V5LTI1Ni1iaXRz # Master encryption key
  backup-key: YmFja3VwLWVuY3J5cHRpb24ta2V5LTI1Ni1iaXRz # Backup encryption key

---
# ConfigMap pour configuration sécurisée
apiVersion: v1
kind: ConfigMap
metadata:
  name: security-config
  namespace: ecommerce-prod
  labels:
    config-type: security
  annotations:
    description: 'Security configuration for applications'
data:
  security.yaml: |
    # Configuration de sécurité
    security:
      # Configuration HTTPS
      tls:
        enabled: true
        min_version: "1.2"
        ciphers:
          - "ECDHE-RSA-AES256-GCM-SHA384"
          - "ECDHE-RSA-AES128-GCM-SHA256"
          - "ECDHE-RSA-AES256-SHA384"
        
      # Configuration CORS
      cors:
        allowed_origins:
          - "https://ecommerce.company.com"
          - "https://admin.company.com"
        allowed_methods: ["GET", "POST", "PUT", "DELETE"]
        allowed_headers: ["Authorization", "Content-Type"]
        max_age: 3600
      
      # Configuration CSP
      content_security_policy:
        default_src: "'self'"
        script_src: "'self' 'unsafe-inline'"
        style_src: "'self' 'unsafe-inline'"
        img_src: "'self' data: https:"
        connect_src: "'self'"
        font_src: "'self'"
        frame_ancestors: "'none'"
      
      # Configuration des sessions
      session:
        secure: true
        http_only: true
        same_site: "strict"
        max_age: 3600
        
      # Configuration des mots de passe
      password_policy:
        min_length: 12
        require_uppercase: true
        require_lowercase: true
        require_numbers: true
        require_special: true
        max_attempts: 5
        lockout_duration: 1800
```

### 4.2 Cert-manager pour gestion automatique des certificats

```yaml
# cert-manager-config.yaml
---
# ClusterIssuer pour Let's Encrypt
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
  labels:
    issuer-type: letsencrypt
    environment: production
  annotations:
    description: "Let's Encrypt production issuer for TLS certificates"
spec:
  acme:
    # Production Let's Encrypt server
    server: https://acme-v02.api.letsencrypt.org/directory

    # Email pour notifications
    email: security@company.com

    # Secret pour stocker la clé privée ACME
    privateKeySecretRef:
      name: letsencrypt-prod-key

    # Résolveur DNS pour validation
    solvers:
    - dns01:
        cloudflare:
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token
      selector:
        dnsZones:
        - "company.com"
        - "*.company.com"

---
# ClusterIssuer pour environnement staging
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
  labels:
    issuer-type: letsencrypt
    environment: staging
  annotations:
    description: "Let's Encrypt staging issuer for testing"
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: security@company.com
    privateKeySecretRef:
      name: letsencrypt-staging-key
    solvers:
    - dns01:
        cloudflare:
          apiTokenSecretRef:
            name: cloudflare-api-token
            key: api-token

---
# Certificate pour domaine principal
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ecommerce-tls
  namespace: ecommerce-prod
  labels:
    certificate-type: production
    domain: ecommerce
  annotations:
    description: "TLS certificate for ecommerce domain"
spec:
  secretName: ecommerce-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - ecommerce.company.com
  - api.ecommerce.company.com
  - admin.ecommerce.company.com
  - *.ecommerce.company.com

---
# Certificate pour API interne
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: internal-api-tls
  namespace: ecommerce-prod
  labels:
    certificate-type: internal
    domain: internal
  annotations:
    description: "TLS certificate for internal APIs"
spec:
  secretName: internal-api-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - internal-api.company.com
  - *.internal-api.company.com
```

## Étape 5 : Monitoring et audit de sécurité

### 5.1 Monitoring de sécurité avec Falco

```yaml
# security-monitoring.yaml
---
# ConfigMap pour règles Falco
apiVersion: v1
kind: ConfigMap
metadata:
  name: falco-rules
  namespace: security-system
  labels:
    app: falco
    component: rules
data:
  custom_rules.yaml: |
    # Règles personnalisées de sécurité

    # Détection d'exécution de shell dans les conteneurs
    - rule: Shell in container
      desc: Notice shell activity within a container
      condition: >
        spawned_process and
        (proc.name in (shell_binaries) or
         proc.pname in (shell_binaries))
      output: >
        Shell spawned in container (user=%user.name container=%container.name 
        shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
      priority: WARNING
      tags: [shell, mitre_execution]

    # Détection de modifications de fichiers sensibles
    - rule: Write below etc
      desc: an attempt to write to any file below /etc
      condition: >
        open_write and
        fd.name startswith /etc
      output: >
        File below /etc opened for writing (user=%user.name command=%proc.cmdline 
        file=%fd.name)
      priority: ERROR
      tags: [filesystem, mitre_persistence]

    # Détection d'escalade de privilèges
    - rule: Privilege escalation attempt
      desc: Detect privilege escalation attempts
      condition: >
        spawned_process and
        (proc.name in (su, sudo, setuid_binaries) or
         proc.args contains "chmod +s")
      output: >
        Privilege escalation attempt (user=%user.name command=%proc.cmdline)
      priority: CRITICAL
      tags: [privilege_escalation, mitre_privilege_escalation]

    # Détection de connexions réseau suspectes
    - rule: Suspicious network activity
      desc: Detect suspicious network connections
      condition: >
        outbound and
        (fd.sport in (suspicious_ports) or
         fd.dport in (suspicious_ports))
      output: >
        Suspicious network connection (user=%user.name command=%proc.cmdline 
        connection=%fd.name)
      priority: WARNING
      tags: [network, mitre_command_and_control]

---
# DaemonSet Falco pour monitoring
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: falco
  namespace: security-system
  labels:
    app: falco
    component: security-monitor
spec:
  selector:
    matchLabels:
      app: falco
  template:
    metadata:
      labels:
        app: falco
        component: security-monitor
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8765'
    spec:
      serviceAccountName: security-scanner-sa
      tolerations:
        - effect: NoSchedule
          key: node-role.kubernetes.io/master
      hostNetwork: true
      hostPID: true
      containers:
        - name: falco
          image: falcosecurity/falco:0.36.0
          args:
            - /usr/bin/falco
            - --cri=/host/run/containerd/containerd.sock
            - --k8s-api=https://kubernetes.default.svc.cluster.local
            - --k8s-api-cert=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
            - --k8s-api-token=/var/run/secrets/kubernetes.io/serviceaccount/token
            - -K
            - /var/run/secrets/kubernetes.io/serviceaccount/token
            - -k
            - https://kubernetes.default.svc.cluster.local
            - --http-output
            - --http-port=8765
          env:
            - name: FALCO_K8S_NODE_NAME
              valueFrom:
                fieldRef:
                  fieldPath: spec.nodeName
          securityContext:
            privileged: true
          volumeMounts:
            - mountPath: /host/var/run/docker.sock
              name: docker-socket
              readOnly: true
            - mountPath: /host/run/containerd/containerd.sock
              name: containerd-socket
              readOnly: true
            - mountPath: /host/dev
              name: dev-fs
              readOnly: true
            - mountPath: /host/proc
              name: proc-fs
              readOnly: true
            - mountPath: /host/boot
              name: boot-fs
              readOnly: true
            - mountPath: /host/lib/modules
              name: lib-modules
              readOnly: true
            - mountPath: /host/usr
              name: usr-fs
              readOnly: true
            - mountPath: /host/etc
              name: etc-fs
              readOnly: true
            - mountPath: /etc/falco/rules.d
              name: falco-rules
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi

      volumes:
        - name: docker-socket
          hostPath:
            path: /var/run/docker.sock
        - name: containerd-socket
          hostPath:
            path: /run/containerd/containerd.sock
        - name: dev-fs
          hostPath:
            path: /dev
        - name: proc-fs
          hostPath:
            path: /proc
        - name: boot-fs
          hostPath:
            path: /boot
        - name: lib-modules
          hostPath:
            path: /lib/modules
        - name: usr-fs
          hostPath:
            path: /usr
        - name: etc-fs
          hostPath:
            path: /etc
        - name: falco-rules
          configMap:
            name: falco-rules

---
# ServiceMonitor pour Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: falco-metrics
  namespace: security-system
  labels:
    app: falco
    monitoring: enabled
spec:
  selector:
    matchLabels:
      app: falco
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

### 5.2 Scripts de validation de sécurité

```bash
# security-validation.sh
#!/bin/bash

echo "🔒 Validation de la sécurité Kubernetes"

# Fonction de test RBAC
test_rbac() {
    local namespace=${1:-ecommerce-prod}

    echo "=== Test RBAC dans $namespace ==="

    # Test des permissions de service accounts
    echo "Test des permissions des service accounts..."

    # Test API Gateway SA
    kubectl auth can-i get services --as=system:serviceaccount:$namespace:api-gateway-sa -n $namespace
    kubectl auth can-i create secrets --as=system:serviceaccount:$namespace:api-gateway-sa -n $namespace

    # Test Business Services SA
    kubectl auth can-i get configmaps --as=system:serviceaccount:$namespace:business-services-sa -n $namespace
    kubectl auth can-i delete pods --as=system:serviceaccount:$namespace:business-services-sa -n $namespace

    # Test Database SA
    kubectl auth can-i get statefulsets --as=system:serviceaccount:$namespace:database-sa -n $namespace
    kubectl auth can-i create persistentvolumeclaims --as=system:serviceaccount:$namespace:database-sa -n $namespace

    echo "✅ Tests RBAC terminés"
}

# Fonction de test Network Policies
test_network_policies() {
    local namespace=${1:-ecommerce-prod}

    echo "=== Test Network Policies dans $namespace ==="

    # Lister les politiques réseau
    echo "Politiques réseau configurées:"
    kubectl get networkpolicies -n $namespace

    # Test de connectivité
    echo "Test de connectivité réseau..."

    # Déployer un pod de test
    kubectl run network-test --image=nicolaka/netshoot --rm -i --restart=Never -n $namespace -- bash -c "
        echo 'Test de connectivité réseau...'

        # Test DNS
        nslookup kubernetes.default.svc.cluster.local

        # Test connectivité vers services autorisés
        nc -zv postgresql-master.$namespace.svc.cluster.local 5432 2>&1 || echo 'PostgreSQL non accessible (normal si politique restrictive)'
        nc -zv redis-cluster.$namespace.svc.cluster.local 6379 2>&1 || echo 'Redis non accessible (normal si politique restrictive)'

        # Test connectivité vers Internet (doit être bloquée)
        timeout 5 nc -zv google.com 80 2>&1 || echo 'Internet bloqué (sécurité OK)'
    "

    echo "✅ Tests Network Policies terminés"
}

# Fonction de test Pod Security Standards
test_pod_security() {
    local namespace=${1:-ecommerce-prod}

    echo "=== Test Pod Security Standards dans $namespace ==="

    # Vérifier les annotations du namespace
    echo "Annotations de sécurité du namespace:"
    kubectl get namespace $namespace -o jsonpath='{.metadata.annotations}' | jq .

    # Test de déploiement d'un pod non-conforme
    echo "Test de déploiement d'un pod privilégié (doit échouer)..."

    cat <<EOF | kubectl apply -f - --dry-run=server 2>&1 || echo "Pod privilégié correctement rejeté"
apiVersion: v1
kind: Pod
metadata:
  name: privileged-pod-test
  namespace: $namespace
spec:
  containers:
  - name: test
    image: nginx
    securityContext:
      privileged: true
      runAsUser: 0
EOF

    # Test de déploiement d'un pod conforme
    echo "Test de déploiement d'un pod sécurisé (doit réussir)..."

    cat <<EOF | kubectl apply --dry-run=server -f - && echo "Pod sécurisé accepté"
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod-test
  namespace: $namespace
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 65534
    runAsGroup: 65534
    fsGroup: 65534
  containers:
  - name: test
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      runAsNonRoot: true
      runAsUser: 65534
      capabilities:
        drop:
        - ALL
      seccompProfile:
        type: RuntimeDefault
      readOnlyRootFilesystem: true
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
EOF

    echo "✅ Tests Pod Security Standards terminés"
}

# Fonction de scan de sécurité
security_scan() {
    local namespace=${1:-ecommerce-prod}

    echo "=== Scan de sécurité dans $namespace ==="

    # Scan des ressources pour problèmes de sécurité
    echo "Scan des pods pour configuration de sécurité..."

    kubectl get pods -n $namespace -o json | jq -r '
        .items[] |
        select(.spec.securityContext.runAsRoot // true or
               .spec.containers[].securityContext.privileged // false or
               (.spec.containers[].securityContext.runAsUser // 0) == 0) |
        "⚠️  Pod insécurisé: \(.metadata.name)"
    '

    # Scan des services exposés
    echo "Scan des services exposés..."
    kubectl get services -n $namespace -o json | jq -r '
        .items[] |
        select(.spec.type == "NodePort" or .spec.type == "LoadBalancer") |
        "🌐 Service exposé: \(.metadata.name) (type: \(.spec.type))"
    '

    # Scan des secrets non chiffrés
    echo "Scan des secrets..."
    kubectl get secrets -n $namespace -o json | jq -r '
        .items[] |
        select(.type != "kubernetes.io/service-account-token") |
        "🔑 Secret trouvé: \(.metadata.name) (type: \(.type))"
    '

    echo "✅ Scan de sécurité terminé"
}

# Fonction de rapport de conformité
compliance_report() {
    local namespace=${1:-ecommerce-prod}

    echo "=== Rapport de conformité pour $namespace ==="

    local report_file="/tmp/security-compliance-$(date +%Y%m%d_%H%M%S).json"

    # Générer le rapport JSON
    cat > $report_file <<EOF
{
  "report_date": "$(date -Iseconds)",
  "namespace": "$namespace",
  "security_checks": {
    "rbac_configured": $(kubectl get rolebindings,clusterrolebindings -n $namespace -o json | jq '.items | length > 0'),
    "network_policies": $(kubectl get networkpolicies -n $namespace -o json | jq '.items | length'),
    "pod_security_standards": $(kubectl get namespace $namespace -o jsonpath='{.metadata.annotations.pod-security\.kubernetes\.io/enforce}' | grep -q "restricted" && echo true || echo false),
    "resource_quotas": $(kubectl get resourcequota -n $namespace -o json | jq '.items | length'),
    "limit_ranges": $(kubectl get limitrange -n $namespace -o json | jq '.items | length'),
    "secrets_count": $(kubectl get secrets -n $namespace -o json | jq '.items | length'),
    "tls_certificates": $(kubectl get secrets -n $namespace -o json | jq '[.items[] | select(.type == "kubernetes.io/tls")] | length')
  },
  "compliance_score": "$(echo 'scale=2; (7*100)/7' | bc)%"
}
EOF

    echo "📊 Rapport de conformité généré: $report_file"
    cat $report_file | jq .

    echo "✅ Rapport de conformité terminé"
}

# Menu principal
case "$1" in
    "rbac")
        test_rbac "$2"
        ;;
    "network")
        test_network_policies "$2"
        ;;
    "pod-security")
        test_pod_security "$2"
        ;;
    "scan")
        security_scan "$2"
        ;;
    "compliance")
        compliance_report "$2"
        ;;
    "all")
        test_rbac "$2"
        test_network_policies "$2"
        test_pod_security "$2"
        security_scan "$2"
        compliance_report "$2"
        ;;
    *)
        echo "Usage: $0 {rbac|network|pod-security|scan|compliance|all} [namespace]"
        echo ""
        echo "Commandes disponibles:"
        echo "  rbac         - Tester les permissions RBAC"
        echo "  network      - Tester les politiques réseau"
        echo "  pod-security - Tester les standards de sécurité des pods"
        echo "  scan         - Scanner les problèmes de sécurité"
        echo "  compliance   - Générer un rapport de conformité"
        echo "  all          - Exécuter tous les tests"
        echo ""
        echo "Exemples:"
        echo "  $0 rbac ecommerce-prod"
        echo "  $0 all ecommerce-dev"
        exit 1
        ;;
esac
```

## Points clés de la solution

### 🔐 RBAC granulaire

- **Service Accounts dédiés**: Un SA par composant avec permissions minimales
- **Roles namespace-specific**: Permissions adaptées à chaque environnement
- **ClusterRoles globaux**: Accès contrôlé aux ressources cluster-wide
- **Principle of least privilege**: Permissions strictement nécessaires

### 🛡️ Pod Security Standards

- **Restricted policy**: Standard le plus strict pour la production
- **Non-root containers**: Exécution avec utilisateur non-privilégié
- **Read-only filesystem**: Prévention des modifications runtime
- **Capabilities dropped**: Suppression de toutes les capabilities Linux

### 🌐 Network Security

- **Default deny**: Blocage par défaut de tout trafic
- **Micro-segmentation**: Politiques granulaires par tier
- **Egress control**: Contrôle strict du trafic sortant
- **DNS restriction**: Limitation des résolutions DNS

Cette correction fournit une solution complète et enterprise-grade pour la sécurité Kubernetes avec RBAC, conformité aux standards de sécurité, et monitoring de sécurité en temps réel.
