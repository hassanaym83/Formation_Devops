# Correction LAB 7 - Network Policies et Micro-segmentation

## Vue d'ensemble de la solution

Cette correction présente l'implémentation complète des Network Policies pour la micro-segmentation réseau de l'application e-commerce avec isolation par tiers, contrôle d'accès granulaire, et sécurisation du trafic inter-services.

## Architecture de sécurité réseau

```
Architecture Micro-segmentée:
├── DMZ (Zone démilitarisée)
│   ├── Load Balancer/Ingress
│   └── WAF (Web Application Firewall)
├── Frontend Tier
│   ├── Web UI (React/Angular)
│   └── API Gateway
├── Application Tier
│   ├── Product Service
│   ├── Order Service
│   ├── User Service
│   └── Payment Service
├── Data Tier
│   ├── PostgreSQL Database
│   ├── Redis Cache
│   └── MongoDB Documents
└── Management Tier
    ├── Monitoring (Prometheus/Grafana)
    ├── Logging (ELK Stack)
    └── Backup Services
```

## Étape 1 : Préparation de l'environnement avec namespaces segmentés

### 1.1 Namespaces avec isolation réseau

```yaml
# network-namespaces.yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-dmz
  labels:
    tier: dmz
    security-zone: public
    network-policy: restricted
    monitoring: enabled
  annotations:
    description: 'DMZ zone for load balancers and ingress controllers'
    security-level: 'high'
    allowed-ingress: 'internet'
    allowed-egress: 'frontend'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-frontend
  labels:
    tier: frontend
    security-zone: semi-public
    network-policy: controlled
    monitoring: enabled
  annotations:
    description: 'Frontend applications and API gateway'
    security-level: 'medium-high'
    allowed-ingress: 'dmz'
    allowed-egress: 'application'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-application
  labels:
    tier: application
    security-zone: private
    network-policy: strict
    monitoring: enabled
  annotations:
    description: 'Core business logic services'
    security-level: 'high'
    allowed-ingress: 'frontend'
    allowed-egress: 'data'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-data
  labels:
    tier: data
    security-zone: restricted
    network-policy: very-strict
    monitoring: enabled
  annotations:
    description: 'Databases and persistent storage'
    security-level: 'very-high'
    allowed-ingress: 'application'
    allowed-egress: 'none'

---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-management
  labels:
    tier: management
    security-zone: admin
    network-policy: admin-only
    monitoring: enabled
  annotations:
    description: 'Monitoring, logging, and administrative tools'
    security-level: 'admin'
    allowed-ingress: 'admin-networks'
    allowed-egress: 'all-for-monitoring'
```

### 1.2 Déploiement des applications par tier

```yaml
# applications-by-tier.yaml
---
# DMZ Tier - Ingress Controller
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ecommerce-dmz
  labels:
    app: nginx-ingress
    tier: dmz
    component: load-balancer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-ingress
  template:
    metadata:
      labels:
        app: nginx-ingress
        tier: dmz
        component: load-balancer
        network-policy: allow-internet
    spec:
      containers:
        - name: nginx-ingress
          image: nginx/nginx-ingress:3.3.0
          ports:
            - containerPort: 80
              name: http
            - containerPort: 443
              name: https
            - containerPort: 9113
              name: metrics
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi

---
# Frontend Tier - API Gateway
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: ecommerce-frontend
  labels:
    app: api-gateway
    tier: frontend
    component: gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
        tier: frontend
        component: gateway
        network-policy: allow-dmz
    spec:
      containers:
        - name: api-gateway
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
              name: http
            - containerPort: 8080
              name: metrics
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi

---
# Application Tier - Microservices
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecommerce-application
  labels:
    app: product-service
    tier: application
    component: microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
        tier: application
        component: microservice
        network-policy: allow-frontend
    spec:
      containers:
        - name: product-service
          image: ecommerce/product-service:v1.0.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: DB_HOST
              value: 'postgresql-service.ecommerce-data.svc.cluster.local'
            - name: CACHE_HOST
              value: 'redis-service.ecommerce-data.svc.cluster.local'
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce-application
  labels:
    app: order-service
    tier: application
    component: microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        tier: application
        component: microservice
        network-policy: allow-frontend
    spec:
      containers:
        - name: order-service
          image: ecommerce/order-service:v1.0.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: DB_HOST
              value: 'postgresql-service.ecommerce-data.svc.cluster.local'
            - name: PAYMENT_SERVICE_URL
              value: 'http://payment-service.ecommerce-application.svc.cluster.local'
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: ecommerce-application
  labels:
    app: payment-service
    tier: application
    component: microservice
    security: high
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
        tier: application
        component: microservice
        security: high
        network-policy: restricted
    spec:
      containers:
        - name: payment-service
          image: ecommerce/payment-service:v1.0.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: DB_HOST
              value: 'postgresql-service.ecommerce-data.svc.cluster.local'
            - name: ENCRYPTION_ENABLED
              value: 'true'
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi

---
# Data Tier - Databases
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: ecommerce-data
  labels:
    app: postgresql
    tier: data
    component: database
spec:
  serviceName: postgresql-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
        tier: data
        component: database
        network-policy: data-only
    spec:
      containers:
        - name: postgresql
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_DB
              value: 'ecommerce'
            - name: POSTGRES_USER
              value: 'ecommerce_user'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: postgres-storage
      spec:
        accessModes: ['ReadWriteOnce']
        resources:
          requests:
            storage: 20Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: ecommerce-data
  labels:
    app: redis
    tier: data
    component: cache
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
        tier: data
        component: cache
        network-policy: data-only
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
              name: redis
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

## Étape 2 : Network Policies par tier

### 2.1 Politique de déni par défaut

```yaml
# default-deny-policies.yaml
---
# Déni par défaut - DMZ
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-dmz
  namespace: ecommerce-dmz
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Déni par défaut - Frontend
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-frontend
  namespace: ecommerce-frontend
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Déni par défaut - Application
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-application
  namespace: ecommerce-application
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Déni par défaut - Data
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-data
  namespace: ecommerce-data
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Déni par défaut - Management
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all-management
  namespace: ecommerce-management
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 2.2 Policies d'ingress contrôlé

```yaml
# ingress-policies.yaml
---
# DMZ - Autoriser trafic Internet vers Ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-internet-to-ingress
  namespace: ecommerce-dmz
  annotations:
    description: "Permet le trafic Internet vers les contrôleurs d'ingress"
    security-impact: 'high'
    review-date: '2024-12-01'
spec:
  podSelector:
    matchLabels:
      app: nginx-ingress
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - {} # Autorise tout le trafic entrant (Internet)
  egress:
    # Autoriser vers frontend uniquement
    - to:
        - namespaceSelector:
            matchLabels:
              tier: frontend
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 443
    # Autoriser DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53

---
# Frontend - Autoriser DMZ vers API Gateway
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dmz-to-frontend
  namespace: ecommerce-frontend
  annotations:
    description: "Permet au DMZ d'accéder aux services frontend"
    security-impact: 'medium'
spec:
  podSelector:
    matchLabels:
      tier: frontend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Autoriser depuis DMZ
    - from:
        - namespaceSelector:
            matchLabels:
              tier: dmz
      ports:
        - protocol: TCP
          port: 80
        - protocol: TCP
          port: 8080
    # Autoriser monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
      ports:
        - protocol: TCP
          port: 8080 # Metrics endpoint
  egress:
    # Autoriser vers application tier
    - to:
        - namespaceSelector:
            matchLabels:
              tier: application
      ports:
        - protocol: TCP
          port: 8080
    # Autoriser DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53

---
# Application - Autoriser Frontend vers Microservices
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-application
  namespace: ecommerce-application
  annotations:
    description: "Permet au frontend d'accéder aux microservices"
    security-impact: 'medium'
spec:
  podSelector:
    matchLabels:
      tier: application
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Autoriser depuis frontend
    - from:
        - namespaceSelector:
            matchLabels:
              tier: frontend
      ports:
        - protocol: TCP
          port: 8080
    # Communication inter-microservices
    - from:
        - podSelector:
            matchLabels:
              tier: application
      ports:
        - protocol: TCP
          port: 8080
    # Autoriser monitoring
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
      ports:
        - protocol: TCP
          port: 9090 # Metrics
  egress:
    # Autoriser vers data tier
    - to:
        - namespaceSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 6379 # Redis
    # Communication inter-microservices
    - to:
        - podSelector:
            matchLabels:
              tier: application
      ports:
        - protocol: TCP
          port: 8080
    # Autoriser DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
    # Autoriser HTTPS externes pour APIs
    - to: []
      ports:
        - protocol: TCP
          port: 443

---
# Data - Autoriser Application vers Databases
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-application-to-data
  namespace: ecommerce-data
  annotations:
    description: "Permet aux microservices d'accéder aux bases de données"
    security-impact: 'high'
spec:
  podSelector:
    matchLabels:
      tier: data
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Autoriser depuis application tier uniquement
    - from:
        - namespaceSelector:
            matchLabels:
              tier: application
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 6379 # Redis
    # Autoriser monitoring limité
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
      ports:
        - protocol: TCP
          port: 9187 # PostgreSQL exporter
        - protocol: TCP
          port: 9121 # Redis exporter
    # Communication interne pour réplication
    - from:
        - podSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432
  egress:
    # Communication interne pour clustering/réplication
    - to:
        - podSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432
    # DNS uniquement
    - to: []
      ports:
        - protocol: UDP
          port: 53
```

### 2.3 Policies spécialisées par service

```yaml
# specialized-policies.yaml
---
# Payment Service - Politique stricte
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: payment-service-strict-policy
  namespace: ecommerce-application
  annotations:
    description: 'Politique très restrictive pour le service de paiement'
    security-impact: 'critical'
    compliance: 'PCI-DSS'
spec:
  podSelector:
    matchLabels:
      app: payment-service
      security: high
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Seuls les services autorisés peuvent appeler le payment service
    - from:
        - podSelector:
            matchLabels:
              app: order-service
      ports:
        - protocol: TCP
          port: 8080
    # Monitoring restreint
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
        - podSelector:
            matchLabels:
              app: prometheus
      ports:
        - protocol: TCP
          port: 9090 # Metrics endpoint
  egress:
    # Accès database avec restriction
    - to:
        - namespaceSelector:
            matchLabels:
              tier: data
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432
    # APIs externes de paiement (HTTPS uniquement)
    - to: []
      ports:
        - protocol: TCP
          port: 443
    # DNS
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Database - Politique ultra-restrictive
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgresql-ultra-strict
  namespace: ecommerce-data
  annotations:
    description: 'Politique ultra-restrictive pour PostgreSQL'
    security-impact: 'critical'
    data-classification: 'confidential'
spec:
  podSelector:
    matchLabels:
      app: postgresql
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Seuls les microservices autorisés
    - from:
        - namespaceSelector:
            matchLabels:
              tier: application
        - podSelector:
            matchLabels:
              component: microservice
      ports:
        - protocol: TCP
          port: 5432
    # Backup service autorisé
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
        - podSelector:
            matchLabels:
              app: backup-service
      ports:
        - protocol: TCP
          port: 5432
    # Réplication interne
    - from:
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432
  egress:
    # Réplication vers autres instances PostgreSQL
    - to:
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432
    # DNS minimal
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Monitoring - Accès étendu mais contrôlé
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: monitoring-controlled-access
  namespace: ecommerce-management
  annotations:
    description: 'Accès contrôlé pour les services de monitoring'
    security-impact: 'medium'
spec:
  podSelector:
    matchLabels:
      tier: management
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Accès admin depuis réseaux autorisés
    - from: []
      ports:
        - protocol: TCP
          port: 3000 # Grafana
        - protocol: TCP
          port: 9090 # Prometheus
  egress:
    # Collecte métriques depuis tous les tiers
    - to:
        - namespaceSelector:
            matchLabels:
              tier: dmz
      ports:
        - protocol: TCP
          port: 9113 # Nginx metrics
    - to:
        - namespaceSelector:
            matchLabels:
              tier: frontend
      ports:
        - protocol: TCP
          port: 8080
    - to:
        - namespaceSelector:
            matchLabels:
              tier: application
      ports:
        - protocol: TCP
          port: 9090
    - to:
        - namespaceSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 9187 # PostgreSQL exporter
        - protocol: TCP
          port: 9121 # Redis exporter
    # DNS et communication interne
    - to: []
      ports:
        - protocol: UDP
          port: 53
        - protocol: TCP
          port: 53
```

## Étape 3 : Policies avancées avec conditions

### 3.1 Policies basées sur l'heure et les IP

```yaml
# advanced-policies.yaml
---
# Politique avec restriction horaire (conceptuel - nécessite des solutions tierces)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: admin-access-business-hours
  namespace: ecommerce-management
  annotations:
    description: 'Accès admin limité aux heures de bureau'
    time-restriction: '08:00-18:00 UTC'
    implementation: 'requires-external-controller'
spec:
  podSelector:
    matchLabels:
      app: grafana
  policyTypes:
    - Ingress
  ingress:
    # Simulation de restriction IP (à implémenter avec Calico/Cilium)
    - from: []
      ports:
        - protocol: TCP
          port: 3000

---
# Politique avec whitelist IP (conceptuel)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: admin-ip-whitelist
  namespace: ecommerce-management
  annotations:
    description: 'Accès admin depuis IPs autorisées uniquement'
    allowed-ips: '10.0.1.0/24,192.168.1.100/32'
    implementation: 'requires-calico-or-cilium'
spec:
  podSelector:
    matchLabels:
      component: admin-interface
  policyTypes:
    - Ingress
  ingress:
    # Nécessite Calico/Cilium pour restrictions IP
    - from: []
      ports:
        - protocol: TCP
          port: 8080

---
# Politique de maintenance
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: maintenance-mode
  namespace: ecommerce-application
  annotations:
    description: 'Mode maintenance - accès restreint'
    maintenance-window: 'Saturday 02:00-04:00 UTC'
spec:
  podSelector:
    matchLabels:
      maintenance-mode: 'enabled'
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Seuls les administrateurs pendant la maintenance
    - from:
        - namespaceSelector:
            matchLabels:
              tier: management
        - podSelector:
            matchLabels:
              role: admin
      ports:
        - protocol: TCP
          port: 8080
  egress:
    # Accès limité pendant maintenance
    - to:
        - namespaceSelector:
            matchLabels:
              tier: data
      ports:
        - protocol: TCP
          port: 5432
```

### 3.2 Policies de segmentation par environnement

```yaml
# environment-segmentation.yaml
---
# Isolation production vs staging
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: production-isolation
  namespace: ecommerce-application
  annotations:
    description: "Isolation stricte de l'environnement production"
    environment: 'production'
spec:
  podSelector:
    matchLabels:
      environment: production
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Seuls les services production peuvent communiquer
    - from:
        - podSelector:
            matchLabels:
              environment: production
        - namespaceSelector:
            matchLabels:
              environment: production
  egress:
    # Communication uniquement vers production
    - to:
        - podSelector:
            matchLabels:
              environment: production
        - namespaceSelector:
            matchLabels:
              environment: production
    # DNS et services système
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
      ports:
        - protocol: UDP
          port: 53

---
# Cross-environment communication contrôlée
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: staging-to-shared-services
  namespace: ecommerce-application
  annotations:
    description: 'Accès staging vers services partagés uniquement'
    environment: 'staging'
spec:
  podSelector:
    matchLabels:
      environment: staging
  policyTypes:
    - Egress
  egress:
    # Accès aux services partagés (monitoring, etc.)
    - to:
        - namespaceSelector:
            matchLabels:
              tier: management
      ports:
        - protocol: TCP
          port: 9090
    # Accès aux données staging uniquement
    - to:
        - namespaceSelector:
            matchLabels:
              tier: data
        - podSelector:
            matchLabels:
              environment: staging
      ports:
        - protocol: TCP
          port: 5432
    # DNS
    - to: []
      ports:
        - protocol: UDP
          port: 53
```

## Étape 4 : Tests et validation des policies

### 4.1 Script de test complet

```bash
# test-network-policies.sh
#!/bin/bash

set -e

echo "🔒 Test complet des Network Policies"

NAMESPACES=("ecommerce-dmz" "ecommerce-frontend" "ecommerce-application" "ecommerce-data" "ecommerce-management")

# Fonction de test de connectivité
test_connectivity() {
    local source_ns=$1
    local source_pod=$2
    local target_ns=$3
    local target_service=$4
    local target_port=$5
    local expected_result=$6  # "success" ou "blocked"

    echo "Test: $source_ns/$source_pod -> $target_ns/$target_service:$target_port"

    # Lancer le test de connectivité
    local test_result
    if kubectl exec -n $source_ns $source_pod -- timeout 5 nc -zv $target_service.$target_ns.svc.cluster.local $target_port >/dev/null 2>&1; then
        test_result="success"
    else
        test_result="blocked"
    fi

    # Vérifier le résultat attendu
    if [ "$test_result" == "$expected_result" ]; then
        echo "✅ Test réussi: $test_result (attendu: $expected_result)"
        return 0
    else
        echo "❌ Test échoué: $test_result (attendu: $expected_result)"
        return 1
    fi
}

# Fonction de déploiement des pods de test
deploy_test_pods() {
    echo "=== Déploiement des pods de test ==="

    for ns in "${NAMESPACES[@]}"; do
        echo "Déploiement pod de test dans $ns..."

        kubectl run test-pod-$ns --image=busybox:1.35 -n $ns --restart=Never -- sleep 3600 2>/dev/null || true

        # Attendre que le pod soit ready
        kubectl wait --for=condition=ready pod/test-pod-$ns -n $ns --timeout=60s
    done

    echo "✅ Pods de test déployés"
}

# Fonction de nettoyage des pods de test
cleanup_test_pods() {
    echo "=== Nettoyage des pods de test ==="

    for ns in "${NAMESPACES[@]}"; do
        kubectl delete pod test-pod-$ns -n $ns --ignore-not-found
    done

    echo "✅ Pods de test supprimés"
}

# Fonction de test des communications autorisées
test_allowed_communications() {
    echo "=== Test des communications AUTORISÉES ==="

    local failed_tests=0

    # DMZ -> Frontend (autorisé)
    test_connectivity "ecommerce-dmz" "test-pod-ecommerce-dmz" "ecommerce-frontend" "api-gateway" "80" "success" || ((failed_tests++))

    # Frontend -> Application (autorisé)
    test_connectivity "ecommerce-frontend" "test-pod-ecommerce-frontend" "ecommerce-application" "product-service" "8080" "success" || ((failed_tests++))

    # Application -> Data (autorisé)
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-data" "postgresql" "5432" "success" || ((failed_tests++))
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-data" "redis" "6379" "success" || ((failed_tests++))

    # Inter-microservices (autorisé)
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-application" "order-service" "8080" "success" || ((failed_tests++))

    # Monitoring vers tous les tiers (autorisé)
    test_connectivity "ecommerce-management" "test-pod-ecommerce-management" "ecommerce-application" "product-service" "9090" "success" || ((failed_tests++))

    echo "Communications autorisées - Tests échoués: $failed_tests"
    return $failed_tests
}

# Fonction de test des communications bloquées
test_blocked_communications() {
    echo "=== Test des communications BLOQUÉES ==="

    local failed_tests=0

    # Frontend -> Data (doit être bloqué)
    test_connectivity "ecommerce-frontend" "test-pod-ecommerce-frontend" "ecommerce-data" "postgresql" "5432" "blocked" || ((failed_tests++))

    # Data -> Application (doit être bloqué - sens inverse)
    test_connectivity "ecommerce-data" "test-pod-ecommerce-data" "ecommerce-application" "product-service" "8080" "blocked" || ((failed_tests++))

    # DMZ -> Data (doit être bloqué - saut de tier)
    test_connectivity "ecommerce-dmz" "test-pod-ecommerce-dmz" "ecommerce-data" "postgresql" "5432" "blocked" || ((failed_tests++))

    # Application -> DMZ (doit être bloqué - sens inverse)
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-dmz" "nginx-ingress" "80" "blocked" || ((failed_tests++))

    # Data -> Internet (doit être bloqué)
    test_connectivity "ecommerce-data" "test-pod-ecommerce-data" "external" "google.com" "80" "blocked" || ((failed_tests++))

    echo "Communications bloquées - Tests échoués: $failed_tests"
    return $failed_tests
}

# Fonction de test des ports spécifiques
test_port_restrictions() {
    echo "=== Test des restrictions de ports ==="

    local failed_tests=0

    # Application peut accéder à PostgreSQL sur 5432 mais pas 22
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-data" "postgresql" "5432" "success" || ((failed_tests++))
    test_connectivity "ecommerce-application" "test-pod-ecommerce-application" "ecommerce-data" "postgresql" "22" "blocked" || ((failed_tests++))

    # Monitoring peut accéder aux métriques mais pas aux ports applicatifs
    test_connectivity "ecommerce-management" "test-pod-ecommerce-management" "ecommerce-application" "product-service" "9090" "success" || ((failed_tests++))
    test_connectivity "ecommerce-management" "test-pod-ecommerce-management" "ecommerce-application" "product-service" "8080" "blocked" || ((failed_tests++))

    echo "Restrictions de ports - Tests échoués: $failed_tests"
    return $failed_tests
}

# Fonction de test du DNS
test_dns_resolution() {
    echo "=== Test de résolution DNS ==="

    local failed_tests=0

    # DNS doit fonctionner depuis tous les namespaces
    for ns in "${NAMESPACES[@]}"; do
        echo "Test DNS depuis $ns..."
        if kubectl exec -n $ns test-pod-$ns -- nslookup kubernetes.default.svc.cluster.local >/dev/null 2>&1; then
            echo "✅ DNS OK depuis $ns"
        else
            echo "❌ DNS échoué depuis $ns"
            ((failed_tests++))
        fi
    done

    echo "Tests DNS - Tests échoués: $failed_tests"
    return $failed_tests
}

# Fonction de génération du rapport
generate_report() {
    local total_failed=$1

    echo ""
    echo "📊 RAPPORT DE TEST DES NETWORK POLICIES"
    echo "======================================"
    echo "Date: $(date)"
    echo "Cluster: $(kubectl config current-context)"
    echo ""

    if [ $total_failed -eq 0 ]; then
        echo "🎉 TOUS LES TESTS SONT PASSÉS"
        echo "Les Network Policies fonctionnent correctement."
    else
        echo "⚠️ $total_failed TESTS ONT ÉCHOUÉ"
        echo "Vérifiez la configuration des Network Policies."
    fi

    echo ""
    echo "État des Network Policies par namespace:"
    for ns in "${NAMESPACES[@]}"; do
        local policy_count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
        echo "  $ns: $policy_count policies"
    done

    echo ""
    echo "Détails des Network Policies:"
    for ns in "${NAMESPACES[@]}"; do
        echo "--- $ns ---"
        kubectl get networkpolicy -n $ns -o custom-columns="NAME:.metadata.name,PODS:.spec.podSelector" 2>/dev/null || echo "Aucune policy"
    done
}

# Fonction principale
main() {
    echo "🚀 Début des tests des Network Policies"

    # Vérifier que les namespaces existent
    echo "Vérification des namespaces..."
    for ns in "${NAMESPACES[@]}"; do
        if ! kubectl get namespace $ns >/dev/null 2>&1; then
            echo "❌ Namespace $ns non trouvé"
            exit 1
        fi
    done
    echo "✅ Tous les namespaces sont présents"

    # Vérifier que les Network Policies sont déployées
    echo "Vérification des Network Policies..."
    local total_policies=0
    for ns in "${NAMESPACES[@]}"; do
        local count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
        total_policies=$((total_policies + count))
    done

    if [ $total_policies -eq 0 ]; then
        echo "❌ Aucune Network Policy trouvée - Déployez d'abord les policies"
        exit 1
    fi
    echo "✅ $total_policies Network Policies trouvées"

    # Déployer les pods de test
    deploy_test_pods

    # Attendre stabilisation
    echo "Attente stabilisation des policies (30s)..."
    sleep 30

    # Exécuter les tests
    local total_failed=0

    test_allowed_communications || total_failed=$((total_failed + $?))
    test_blocked_communications || total_failed=$((total_failed + $?))
    test_port_restrictions || total_failed=$((total_failed + $?))
    test_dns_resolution || total_failed=$((total_failed + $?))

    # Nettoyer
    cleanup_test_pods

    # Générer le rapport
    generate_report $total_failed

    # Code de retour
    if [ $total_failed -eq 0 ]; then
        echo "✅ Tests des Network Policies terminés avec succès"
        exit 0
    else
        echo "❌ Tests des Network Policies terminés avec des erreurs"
        exit 1
    fi
}

# Gestion des signaux
cleanup() {
    echo "Script interrompu - Nettoyage..."
    cleanup_test_pods
    exit 1
}

trap cleanup INT TERM

# Lancement du script principal
main "$@"
```

### 4.2 Script de monitoring en temps réel

```bash
# monitor-network-policies.sh
#!/bin/bash

echo "📡 Monitoring des Network Policies en temps réel"

# Fonction de monitoring des connexions
monitor_connections() {
    echo "=== Monitoring des connexions réseau ==="

    while true; do
        echo "--- $(date) ---"

        # Compter les connexions par namespace
        for ns in ecommerce-dmz ecommerce-frontend ecommerce-application ecommerce-data ecommerce-management; do
            if kubectl get namespace $ns >/dev/null 2>&1; then
                local pod_count=$(kubectl get pods -n $ns --no-headers 2>/dev/null | wc -l)
                local policy_count=$(kubectl get networkpolicy -n $ns --no-headers 2>/dev/null | wc -l)
                echo "$ns: $pod_count pods, $policy_count policies"
            fi
        done

        echo ""

        # Surveiller les événements réseau
        echo "Événements récents:"
        kubectl get events --all-namespaces --field-selector type=Warning | grep -i "network\|policy\|denied" | tail -5

        echo "=================="
        sleep 30
    done
}

# Fonction d'audit des policies
audit_policies() {
    echo "=== Audit des Network Policies ==="

    for ns in ecommerce-dmz ecommerce-frontend ecommerce-application ecommerce-data ecommerce-management; do
        echo "--- Namespace: $ns ---"

        # Lister les policies
        kubectl get networkpolicy -n $ns -o custom-columns="NAME:.metadata.name,PODS:.spec.podSelector,INGRESS:.spec.ingress,EGRESS:.spec.egress" 2>/dev/null || echo "Aucune policy"

        # Vérifier les pods affectés
        local pods=$(kubectl get pods -n $ns --no-headers 2>/dev/null | wc -l)
        if [ $pods -eq 0 ]; then
            echo "⚠️ Aucun pod dans ce namespace"
        else
            echo "ℹ️ $pods pods affectés par les policies"
        fi

        echo ""
    done
}

# Lancement du monitoring
if [ "$1" == "audit" ]; then
    audit_policies
else
    monitor_connections
fi
```

## Points clés de la solution

### 🛡️ Architecture de sécurité

- **Micro-segmentation**: Isolation par tiers avec DMZ, Frontend, Application, Data
- **Principe du moindre privilège**: Accès minimal nécessaire uniquement
- **Défense en profondeur**: Multiple niveaux de contrôle d'accès
- **Zones de sécurité**: Classification et isolation par niveau de sensibilité

### 🔒 Policies granulaires

- **Default deny**: Blocage par défaut avec autorisations explicites
- **Port-specific**: Contrôle au niveau des ports pour service spécifique
- **Service-to-service**: Communication inter-microservices contrôlée
- **Environment isolation**: Séparation production/staging étanche

### 📊 Validation et monitoring

- **Tests automatisés**: Validation continue des policies réseau
- **Monitoring temps réel**: Surveillance des connexions et violations
- **Audit trails**: Traçabilité des accès et modifications
- **Compliance reporting**: Rapports pour conformité sécurité

Cette correction fournit une solution complète de micro-segmentation réseau pour une architecture e-commerce sécurisée et conforme aux standards enterprise.
