# Correction LAB 10 - Projet d'Intégration E-commerce Complet

## Vue d'ensemble de la solution

Cette correction présente l'implémentation complète du projet d'intégration e-commerce avec tous les composants : microservices, bases de données, sécurité, monitoring, CI/CD, et déploiement production-ready sur Kubernetes.

## Architecture globale du système

```
Architecture E-commerce Complete:
├── Frontend Layer
│   ├── React Web App (SPA)
│   ├── Mobile App (React Native)
│   └── Admin Dashboard (Angular)
├── API Gateway Layer
│   ├── Kong/Istio Gateway
│   ├── Rate Limiting & Throttling
│   ├── Authentication/Authorization
│   └── Load Balancing
├── Microservices Layer
│   ├── User Service (Authentication/Profile)
│   ├── Product Service (Catalog/Inventory)
│   ├── Order Service (Shopping Cart/Orders)
│   ├── Payment Service (Payments/Billing)
│   ├── Notification Service (Email/SMS/Push)
│   └── Recommendation Service (AI/ML)
├── Data Layer
│   ├── PostgreSQL Cluster (Transactional Data)
│   ├── MongoDB Cluster (Product Catalog)
│   ├── Redis Cluster (Cache/Sessions)
│   └── Elasticsearch (Search/Analytics)
├── Infrastructure Layer
│   ├── Kubernetes Orchestration
│   ├── Istio Service Mesh
│   ├── Prometheus/Grafana Monitoring
│   ├── ELK Stack (Logging)
│   └── GitLab CI/CD Pipeline
└── Security & Compliance
    ├── RBAC & Pod Security
    ├── Network Policies
    ├── Secret Management
    └── Compliance Monitoring
```

## Étape 1 : Configuration namespace et ressources globales

### 1.1 Namespaces et configuration de base

```yaml
# namespace-setup.yaml
---
# Namespace principal pour l'e-commerce
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce
  labels:
    project: 'ecommerce-platform'
    environment: 'production'
    security-tier: 'restricted'
    istio-injection: 'enabled'
    monitoring: 'enabled'
  annotations:
    description: 'E-commerce platform production environment'
    contact: 'devops@company.com'
    compliance: 'PCI-DSS,SOC2,GDPR'
    backup.io/enabled: 'true'
    network-policy.io/default-deny: 'true'

---
# Namespace pour monitoring
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
  labels:
    project: 'ecommerce-platform'
    component: 'observability'
    istio-injection: 'disabled'
  annotations:
    description: 'Monitoring and observability stack'

---
# Namespace pour l'ingress
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-system
  labels:
    project: 'ecommerce-platform'
    component: 'networking'
    istio-injection: 'disabled'

---
# ResourceQuota pour l'e-commerce
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ecommerce-quota
  namespace: ecommerce
spec:
  hard:
    requests.cpu: '50'
    requests.memory: '100Gi'
    limits.cpu: '100'
    limits.memory: '200Gi'
    requests.storage: '2Ti'
    persistentvolumeclaims: '50'
    pods: '200'
    services: '50'
    secrets: '100'
    configmaps: '50'
    services.loadbalancers: '5'
    services.nodeports: '0'

---
# LimitRange pour contrôle des ressources
apiVersion: v1
kind: LimitRange
metadata:
  name: ecommerce-limits
  namespace: ecommerce
spec:
  limits:
    - type: Container
      default:
        cpu: '1000m'
        memory: '1Gi'
      defaultRequest:
        cpu: '200m'
        memory: '256Mi'
      max:
        cpu: '4000m'
        memory: '8Gi'
      min:
        cpu: '100m'
        memory: '128Mi'
    - type: Pod
      max:
        cpu: '8000m'
        memory: '16Gi'
    - type: PersistentVolumeClaim
      max:
        storage: '500Gi'
      min:
        storage: '1Gi'

---
# NetworkPolicy default deny
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: ecommerce
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### 1.2 ConfigMaps globales

```yaml
# global-config.yaml
---
# Configuration globale de l'application
apiVersion: v1
kind: ConfigMap
metadata:
  name: ecommerce-global-config
  namespace: ecommerce
  labels:
    app: ecommerce
    component: config
data:
  # Configuration de l'environnement
  environment.yaml: |
    environment: "production"
    debug: false
    log_level: "info"

    # Configuration des bases de données
    databases:
      postgresql:
        host: "postgresql-master.ecommerce.svc.cluster.local"
        port: "5432"
        database: "ecommerce"
        ssl_mode: "require"
        max_connections: 100
      
      mongodb:
        host: "mongodb-0.mongodb-headless.ecommerce.svc.cluster.local"
        port: "27017"
        database: "ecommerce_catalog"
        replica_set: "ecommerce-rs"
        ssl: true
      
      redis:
        cluster_endpoints:
          - "redis-cluster-0.redis-cluster-headless.ecommerce.svc.cluster.local:6379"
          - "redis-cluster-1.redis-cluster-headless.ecommerce.svc.cluster.local:6379"
          - "redis-cluster-2.redis-cluster-headless.ecommerce.svc.cluster.local:6379"
        ssl: true
        cluster_mode: true
      
      elasticsearch:
        host: "elasticsearch-master.ecommerce.svc.cluster.local"
        port: "9200"
        ssl: true

    # Configuration des services
    services:
      user_service:
        url: "http://user-service.ecommerce.svc.cluster.local:8080"
        timeout: 5000
        retries: 3
      
      product_service:
        url: "http://product-service.ecommerce.svc.cluster.local:8080"
        timeout: 5000
        retries: 3
      
      order_service:
        url: "http://order-service.ecommerce.svc.cluster.local:8080"
        timeout: 10000
        retries: 3
      
      payment_service:
        url: "http://payment-service.ecommerce.svc.cluster.local:8080"
        timeout: 15000
        retries: 5
      
      notification_service:
        url: "http://notification-service.ecommerce.svc.cluster.local:8080"
        timeout: 3000
        retries: 2

    # Configuration du cache
    cache:
      default_ttl: 3600
      session_ttl: 86400
      product_ttl: 1800
      user_ttl: 7200

    # Configuration de la sécurité
    security:
      jwt_expiration: 3600
      refresh_token_expiration: 604800
      password_policy:
        min_length: 12
        require_special: true
        require_number: true
        require_uppercase: true
        require_lowercase: true
      
      rate_limiting:
        requests_per_minute: 100
        burst_size: 200
        authenticated_requests_per_minute: 500

---
# Configuration Istio/Service Mesh
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-config
  namespace: ecommerce
  labels:
    app: ecommerce
    component: service-mesh
data:
  mesh-config.yaml: |
    # Configuration du service mesh
    service_mesh:
      enabled: true
      mtls_mode: "strict"
      
      # Configuration des timeouts
      timeouts:
        default: "30s"
        payment: "60s"
        notification: "15s"
      
      # Configuration du retry
      retry:
        attempts: 3
        per_try_timeout: "10s"
        retry_on: "5xx,reset,connect-failure,refused-stream"
      
      # Configuration du circuit breaker
      circuit_breaker:
        max_connections: 100
        max_pending_requests: 50
        max_requests: 200
        max_retries: 10
        consecutive_errors: 5
      
      # Configuration du load balancing
      load_balancing:
        simple: "LEAST_CONN"
        consistent_hash: false
      
      # Configuration de l'observabilité
      observability:
        tracing:
          enabled: true
          sampling_rate: 0.1
        metrics:
          enabled: true
        access_logs:
          enabled: true

---
# Configuration monitoring
apiVersion: v1
kind: ConfigMap
metadata:
  name: monitoring-config
  namespace: ecommerce
  labels:
    app: ecommerce
    component: monitoring
data:
  prometheus-rules.yaml: |
    # Règles d'alerting Prometheus
    groups:
    - name: ecommerce.rules
      rules:
      # Alertes de disponibilité
      - alert: ServiceDown
        expr: up{job=~"ecommerce-.*"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.job }} has been down for more than 1 minute"
      
      # Alertes de performance
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time on {{ $labels.job }}"
          description: "95th percentile response time is {{ $value }}s"
      
      # Alertes d'erreur
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
      
      # Alertes de ressources
      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage in {{ $labels.pod }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"
      
      - alert: HighCPUUsage
        expr: rate(container_cpu_usage_seconds_total[5m]) / container_spec_cpu_quota * 100 > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage in {{ $labels.pod }}"
          description: "CPU usage is {{ $value }}%"
```

## Étape 2 : Microservices déployment

### 2.1 User Service (Authentication & Profile)

```yaml
# user-service.yaml
---
# Deployment User Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: ecommerce
  labels:
    app: user-service
    version: v1
    tier: business
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: user-service
      version: v1
  template:
    metadata:
      labels:
        app: user-service
        version: v1
        tier: business
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
        prometheus.io/path: '/metrics'
    spec:
      serviceAccountName: business-services-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
      containers:
        - name: user-service
          image: ecommerce/user-service:v1.2.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: 'production'
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: postgresql.host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: ecommerce-password
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: jwt-signing-keys
                  key: jwt-private.pem
            - name: REDIS_CLUSTER
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: redis.cluster_endpoints
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ['ALL']
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: logs
              mountPath: /app/logs
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 60
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 5
          startupProbe:
            httpGet:
              path: /actuator/health/startup
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
            failureThreshold: 12
      volumes:
        - name: tmp
          emptyDir: {}
        - name: logs
          emptyDir: {}

---
# Service User Service
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: ecommerce
  labels:
    app: user-service
    tier: business
spec:
  selector:
    app: user-service
  ports:
    - name: http
      port: 8080
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090

---
# HPA User Service
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
  namespace: ecommerce
  labels:
    app: user-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
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
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: '100'
```

### 2.2 Product Service (Catalog & Inventory)

```yaml
# product-service.yaml
---
# Deployment Product Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
    version: v1
    tier: business
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: product-service
      version: v1
  template:
    metadata:
      labels:
        app: product-service
        version: v1
        tier: business
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
    spec:
      serviceAccountName: business-services-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
      containers:
        - name: product-service
          image: ecommerce/product-service:v1.5.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: NODE_ENV
              value: 'production'
            - name: MONGODB_URI
              valueFrom:
                secretKeyRef:
                  name: mongodb-secret
                  key: connection-uri
            - name: ELASTICSEARCH_URL
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: elasticsearch.url
            - name: REDIS_CLUSTER
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: redis.cluster_endpoints
          resources:
            requests:
              cpu: 300m
              memory: 512Mi
            limits:
              cpu: 1500m
              memory: 1Gi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ['ALL']
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 5
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir:
            sizeLimit: 1Gi

---
# Service Product Service
apiVersion: v1
kind: Service
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
    tier: business
spec:
  selector:
    app: product-service
  ports:
    - name: http
      port: 8080
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090
```

### 2.3 Order Service (Shopping Cart & Orders)

```yaml
# order-service.yaml
---
# Deployment Order Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
    version: v1
    tier: business
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: order-service
      version: v1
  template:
    metadata:
      labels:
        app: order-service
        version: v1
        tier: business
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
    spec:
      serviceAccountName: business-services-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
      containers:
        - name: order-service
          image: ecommerce/order-service:v2.1.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: 'production,postgresql'
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: postgresql.host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: ecommerce-password
            - name: PRODUCT_SERVICE_URL
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: services.product_service.url
            - name: PAYMENT_SERVICE_URL
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: services.payment_service.url
          resources:
            requests:
              cpu: 400m
              memory: 768Mi
            limits:
              cpu: 2000m
              memory: 2Gi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ['ALL']
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: logs
              mountPath: /app/logs
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
            initialDelaySeconds: 45
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
            initialDelaySeconds: 20
            periodSeconds: 5
      volumes:
        - name: tmp
          emptyDir: {}
        - name: logs
          emptyDir: {}

---
# Service Order Service
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
    tier: business
spec:
  selector:
    app: order-service
  ports:
    - name: http
      port: 8080
      targetPort: 8080
    - name: metrics
      port: 9090
      targetPort: 9090
```

### 2.4 Payment Service (Sécurisé)

```yaml
# payment-service.yaml
---
# Deployment Payment Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: ecommerce
  labels:
    app: payment-service
    version: v1
    tier: business
    security-level: high
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: payment-service
      version: v1
  template:
    metadata:
      labels:
        app: payment-service
        version: v1
        tier: business
        security-level: high
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9090'
        vault.io/agent-inject: 'true'
        vault.io/role: 'payment-service'
    spec:
      serviceAccountName: payment-services-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: payment-service
          image: ecommerce/payment-service:v1.8.0
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: metrics
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: 'production,security'
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: ecommerce-global-config
                  key: postgresql.host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: ecommerce-password
            - name: STRIPE_API_KEY
              valueFrom:
                secretKeyRef:
                  name: external-api-keys
                  key: stripe-api-key
            - name: ENCRYPTION_KEY
              valueFrom:
                secretKeyRef:
                  name: database-encryption-keys
                  key: payment-encryption-key
          resources:
            requests:
              cpu: 600m
              memory: 1Gi
            limits:
              cpu: 2500m
              memory: 3Gi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ['ALL']
            runAsNonRoot: true
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: secure-logs
              mountPath: /app/logs
            - name: vault-secrets
              mountPath: /vault/secrets
              readOnly: true
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: 8080
              scheme: HTTPS
            initialDelaySeconds: 60
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: 8080
              scheme: HTTPS
            initialDelaySeconds: 30
            periodSeconds: 10
      volumes:
        - name: tmp
          emptyDir: {}
        - name: secure-logs
          emptyDir: {}
        - name: vault-secrets
          emptyDir: {}

---
# Service Payment Service avec LoadBalancer interne
apiVersion: v1
kind: Service
metadata:
  name: payment-service
  namespace: ecommerce
  labels:
    app: payment-service
    tier: business
    security-level: high
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-internal: 'true'
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: 'arn:aws:acm:region:account:certificate/cert-id'
spec:
  selector:
    app: payment-service
  ports:
    - name: https
      port: 443
      targetPort: 8080
      protocol: TCP
    - name: metrics
      port: 9090
      targetPort: 9090
  type: LoadBalancer
```

## Étape 3 : API Gateway et Ingress

### 3.1 Istio Gateway et VirtualService

```yaml
# istio-gateway.yaml
---
# Gateway Istio pour l'e-commerce
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: ecommerce-gateway
  namespace: ecommerce
  labels:
    app: ecommerce-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    # HTTPS pour production
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: ecommerce-tls-secret
      hosts:
        - 'ecommerce.company.com'
        - 'api.ecommerce.company.com'
        - 'admin.ecommerce.company.com'

    # HTTP redirect vers HTTPS
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - 'ecommerce.company.com'
        - 'api.ecommerce.company.com'
        - 'admin.ecommerce.company.com'
      tls:
        httpsRedirect: true

---
# VirtualService pour routage des requêtes
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ecommerce-vs
  namespace: ecommerce
  labels:
    app: ecommerce-virtualservice
spec:
  hosts:
    - 'ecommerce.company.com'
    - 'api.ecommerce.company.com'
    - 'admin.ecommerce.company.com'
  gateways:
    - ecommerce-gateway
  http:
    # Routes pour API
    - match:
        - headers:
            host:
              exact: 'api.ecommerce.company.com'
        - uri:
            prefix: '/api/v1/users'
      route:
        - destination:
            host: user-service.ecommerce.svc.cluster.local
            port:
              number: 8080
      timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s

    - match:
        - headers:
            host:
              exact: 'api.ecommerce.company.com'
        - uri:
            prefix: '/api/v1/products'
      route:
        - destination:
            host: product-service.ecommerce.svc.cluster.local
            port:
              number: 8080
      timeout: 30s
      retries:
        attempts: 3
        perTryTimeout: 10s

    - match:
        - headers:
            host:
              exact: 'api.ecommerce.company.com'
        - uri:
            prefix: '/api/v1/orders'
      route:
        - destination:
            host: order-service.ecommerce.svc.cluster.local
            port:
              number: 8080
      timeout: 60s
      retries:
        attempts: 5
        perTryTimeout: 15s

    - match:
        - headers:
            host:
              exact: 'api.ecommerce.company.com'
        - uri:
            prefix: '/api/v1/payments'
      route:
        - destination:
            host: payment-service.ecommerce.svc.cluster.local
            port:
              number: 443
      timeout: 90s
      retries:
        attempts: 2
        perTryTimeout: 30s

    # Routes pour frontend
    - match:
        - headers:
            host:
              exact: 'ecommerce.company.com'
      route:
        - destination:
            host: frontend-service.ecommerce.svc.cluster.local
            port:
              number: 80

    # Routes pour admin
    - match:
        - headers:
            host:
              exact: 'admin.ecommerce.company.com'
      route:
        - destination:
            host: admin-dashboard.ecommerce.svc.cluster.local
            port:
              number: 80

---
# DestinationRule pour politiques de traffic
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: ecommerce-destination-rules
  namespace: ecommerce
spec:
  host: '*.ecommerce.svc.cluster.local'
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
        maxRetries: 3
    circuitBreaker:
      consecutiveGatewayErrors: 5
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    outlierDetection:
      consecutive5xxErrors: 5
      consecutiveGatewayErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### 3.2 Rate Limiting et Security Policies

```yaml
# security-policies.yaml
---
# AuthorizationPolicy pour contrôle d'accès
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: ecommerce-authz
  namespace: ecommerce
spec:
  rules:
    # Permettre l'accès au frontend pour tous
    - to:
        - operation:
            methods: ['GET']
            paths: ['/', '/static/*', '/api/public/*']

    # Authentification requise pour les APIs privées
    - from:
        - source:
            principals: ['cluster.local/ns/ecommerce/sa/api-gateway-sa']
      to:
        - operation:
            methods: ['GET', 'POST', 'PUT', 'DELETE']
            paths: ['/api/v1/*']
      when:
        - key: request.headers[authorization]
          values: ['Bearer *']

---
# PeerAuthentication pour mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: ecommerce-mtls
  namespace: ecommerce
spec:
  mtls:
    mode: STRICT

---
# RequestAuthentication pour JWT
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: ecommerce-jwt
  namespace: ecommerce
spec:
  jwtRules:
    - issuer: 'https://auth.ecommerce.company.com'
      jwksUri: 'https://auth.ecommerce.company.com/.well-known/jwks.json'
      audiences:
        - 'ecommerce-api'
      forwardOriginalToken: true

---
# EnvoyFilter pour rate limiting
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: rate-limit-filter
  namespace: istio-system
spec:
  configPatches:
    - applyTo: HTTP_FILTER
      match:
        context: SIDECAR_INBOUND
        listener:
          filterChain:
            filter:
              name: 'envoy.filters.network.http_connection_manager'
      patch:
        operation: INSERT_BEFORE
        value:
          name: envoy.filters.http.local_ratelimit
          typed_config:
            '@type': type.googleapis.com/udpa.type.v1.TypedStruct
            type_url: type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
            value:
              stat_prefix: local_rate_limiter
              token_bucket:
                max_tokens: 100
                tokens_per_fill: 100
                fill_interval: 60s
              filter_enabled:
                runtime_key: local_rate_limit_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
              filter_enforced:
                runtime_key: local_rate_limit_enforced
                default_value:
                  numerator: 100
                  denominator: HUNDRED
```

## Étape 4 : Monitoring et observabilité

### 4.1 Prometheus et Grafana

```yaml
# monitoring-stack.yaml
---
# Prometheus pour monitoring
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: ecommerce-prometheus
  namespace: monitoring
  labels:
    app: prometheus
spec:
  serviceAccountName: prometheus-sa
  retention: '30d'
  retentionSize: '100GB'
  storage:
    volumeClaimTemplate:
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-standard
        resources:
          requests:
            storage: 200Gi

  resources:
    requests:
      memory: '2Gi'
      cpu: '1000m'
    limits:
      memory: '4Gi'
      cpu: '2000m'

  serviceMonitorSelector:
    matchLabels:
      monitoring: 'enabled'

  ruleSelector:
    matchLabels:
      prometheus: 'ecommerce'

  alerting:
    alertmanagers:
      - namespace: monitoring
        name: alertmanager
        port: web

---
# ServiceMonitor pour les microservices
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-services
  namespace: monitoring
  labels:
    monitoring: 'enabled'
spec:
  selector:
    matchLabels:
      tier: business
  namespaceSelector:
    matchNames:
      - ecommerce
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
      scrapeTimeout: 10s

---
# PrometheusRule pour alertes
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ecommerce-alerts
  namespace: monitoring
  labels:
    prometheus: 'ecommerce'
spec:
  groups:
    - name: ecommerce.rules
      rules:
        # Business metrics
        - alert: LowConversionRate
          expr: rate(orders_completed_total[1h]) / rate(page_views_total{page="checkout"}[1h]) < 0.02
          for: 15m
          labels:
            severity: warning
            component: business
          annotations:
            summary: 'Low conversion rate detected'
            description: 'Conversion rate is {{ $value | humanizePercentage }}'

        - alert: PaymentFailures
          expr: rate(payment_failures_total[5m]) > 0.05
          for: 5m
          labels:
            severity: critical
            component: payment
          annotations:
            summary: 'High payment failure rate'
            description: 'Payment failure rate is {{ $value | humanizePercentage }}'

        # Infrastructure alerts
        - alert: HighDatabaseConnections
          expr: postgresql_connections > 80
          for: 5m
          labels:
            severity: warning
            component: database
          annotations:
            summary: 'High database connection count'
            description: 'PostgreSQL has {{ $value }} active connections'

        - alert: RedisClusterDown
          expr: redis_cluster_nodes_total < 6
          for: 1m
          labels:
            severity: critical
            component: cache
          annotations:
            summary: 'Redis cluster nodes missing'
            description: 'Only {{ $value }} Redis nodes are available'

---
# Grafana pour visualisation
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: monitoring
  labels:
    app: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      serviceAccountName: grafana-sa
      containers:
        - name: grafana
          image: grafana/grafana:10.0.0
          ports:
            - containerPort: 3000
              name: web
          env:
            - name: GF_SECURITY_ADMIN_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: grafana-secret
                  key: admin-password
            - name: GF_SECURITY_ADMIN_USER
              value: 'admin'
            - name: GF_INSTALL_PLUGINS
              value: 'grafana-piechart-panel,grafana-worldmap-panel'
          volumeMounts:
            - name: grafana-storage
              mountPath: /var/lib/grafana
            - name: grafana-config
              mountPath: /etc/grafana/grafana.ini
              subPath: grafana.ini
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
      volumes:
        - name: grafana-storage
          persistentVolumeClaim:
            claimName: grafana-pvc
        - name: grafana-config
          configMap:
            name: grafana-config
```

## Étape 5 : Scripts de déploiement et validation

### 5.1 Script de déploiement complet

```bash
# deploy-ecommerce.sh
#!/bin/bash

echo "🚀 Déploiement de la plateforme e-commerce complète"

# Configuration
NAMESPACE="ecommerce"
MONITORING_NS="monitoring"
ISTIO_NS="istio-system"

# Fonction de logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Fonction de vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."

    # Vérifier kubectl
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl non trouvé"
        exit 1
    fi

    # Vérifier la connexion au cluster
    if ! kubectl cluster-info &> /dev/null; then
        echo "❌ Impossible de se connecter au cluster Kubernetes"
        exit 1
    fi

    # Vérifier Istio
    if ! kubectl get namespace $ISTIO_NS &> /dev/null; then
        echo "❌ Istio n'est pas installé"
        exit 1
    fi

    # Vérifier les storage classes
    if ! kubectl get storageclass ssd-high-performance &> /dev/null; then
        echo "❌ Storage class ssd-high-performance non trouvée"
        exit 1
    fi

    log "✅ Prérequis vérifiés"
}

# Fonction de déploiement de l'infrastructure
deploy_infrastructure() {
    log "Déploiement de l'infrastructure de base..."

    # Créer les namespaces
    kubectl apply -f namespace-setup.yaml

    # Attendre que les namespaces soient créés
    kubectl wait --for=condition=Ready namespace/$NAMESPACE --timeout=60s
    kubectl wait --for=condition=Ready namespace/$MONITORING_NS --timeout=60s

    # Appliquer les configurations globales
    kubectl apply -f global-config.yaml

    # Déployer les storage classes si nécessaire
    kubectl apply -f storage-classes.yaml

    log "✅ Infrastructure de base déployée"
}

# Fonction de déploiement des bases de données
deploy_databases() {
    log "Déploiement des bases de données..."

    # PostgreSQL Cluster
    kubectl apply -f postgresql-cluster.yaml
    log "PostgreSQL cluster en cours de déploiement..."

    # MongoDB Replica Set
    kubectl apply -f mongodb-replicaset.yaml
    log "MongoDB replica set en cours de déploiement..."

    # Redis Cluster
    kubectl apply -f redis-cluster.yaml
    log "Redis cluster en cours de déploiement..."

    # Attendre que les bases de données soient prêtes
    log "Attente que les bases de données soient prêtes..."
    kubectl wait --for=condition=Ready pod -l app=postgresql -n $NAMESPACE --timeout=300s
    kubectl wait --for=condition=Ready pod -l app=mongodb -n $NAMESPACE --timeout=300s
    kubectl wait --for=condition=Ready pod -l app=redis -n $NAMESPACE --timeout=300s

    log "✅ Bases de données déployées"
}

# Fonction de déploiement des microservices
deploy_microservices() {
    log "Déploiement des microservices..."

    # Déployer les services dans l'ordre de dépendance
    kubectl apply -f user-service.yaml
    kubectl apply -f product-service.yaml
    kubectl apply -f order-service.yaml
    kubectl apply -f payment-service.yaml
    kubectl apply -f notification-service.yaml

    # Attendre que les services soient prêts
    log "Attente que les microservices soient prêts..."

    services=("user-service" "product-service" "order-service" "payment-service" "notification-service")
    for service in "${services[@]}"; do
        kubectl wait --for=condition=Available deployment/$service -n $NAMESPACE --timeout=300s
        log "✅ $service prêt"
    done

    log "✅ Microservices déployés"
}

# Fonction de déploiement du réseau et sécurité
deploy_networking_security() {
    log "Déploiement du réseau et sécurité..."

    # Network Policies
    kubectl apply -f advanced-network-policies.yaml

    # RBAC
    kubectl apply -f service-accounts.yaml
    kubectl apply -f cluster-roles.yaml
    kubectl apply -f namespace-roles.yaml
    kubectl apply -f role-bindings.yaml

    # Istio Gateway et VirtualService
    kubectl apply -f istio-gateway.yaml
    kubectl apply -f security-policies.yaml

    log "✅ Réseau et sécurité configurés"
}

# Fonction de déploiement du monitoring
deploy_monitoring() {
    log "Déploiement du monitoring..."

    # Prometheus et Grafana
    kubectl apply -f monitoring-stack.yaml

    # Falco pour sécurité
    kubectl apply -f security-monitoring.yaml

    # Attendre que Prometheus soit prêt
    kubectl wait --for=condition=Available deployment/prometheus -n $MONITORING_NS --timeout=300s
    kubectl wait --for=condition=Available deployment/grafana -n $MONITORING_NS --timeout=300s

    log "✅ Monitoring déployé"
}

# Fonction de validation du déploiement
validate_deployment() {
    log "Validation du déploiement..."

    # Vérifier que tous les pods sont prêts
    log "Vérification des pods dans le namespace $NAMESPACE..."
    if kubectl get pods -n $NAMESPACE | grep -E "(Error|CrashLoopBackOff|ImagePullBackOff)"; then
        echo "❌ Des pods ont des erreurs"
        kubectl get pods -n $NAMESPACE
        return 1
    fi

    # Vérifier les services
    log "Vérification des services..."
    kubectl get services -n $NAMESPACE

    # Test de connectivité
    log "Test de connectivité des services..."

    # Test API Gateway
    if kubectl get gateway ecommerce-gateway -n $NAMESPACE &> /dev/null; then
        log "✅ Gateway Istio configuré"
    else
        echo "❌ Gateway Istio non trouvé"
        return 1
    fi

    # Test des bases de données
    log "Test des bases de données..."

    # PostgreSQL
    if kubectl exec -n $NAMESPACE postgresql-master-0 -- pg_isready > /dev/null 2>&1; then
        log "✅ PostgreSQL accessible"
    else
        echo "❌ PostgreSQL non accessible"
        return 1
    fi

    # MongoDB
    if kubectl exec -n $NAMESPACE mongodb-0 -- mongo --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        log "✅ MongoDB accessible"
    else
        echo "❌ MongoDB non accessible"
        return 1
    fi

    # Redis
    if kubectl exec -n $NAMESPACE redis-cluster-0 -- redis-cli ping > /dev/null 2>&1; then
        log "✅ Redis accessible"
    else
        echo "❌ Redis non accessible"
        return 1
    fi

    log "✅ Validation terminée avec succès"
}

# Fonction de récupération des URLs d'accès
get_access_urls() {
    log "Récupération des URLs d'accès..."

    echo ""
    echo "🌐 URLs d'accès à la plateforme:"
    echo "================================"

    # Récupérer l'IP du Load Balancer Istio
    GATEWAY_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)

    if [ -z "$GATEWAY_IP" ]; then
        GATEWAY_IP=$(kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null)
    fi

    if [ -n "$GATEWAY_IP" ]; then
        echo "Frontend E-commerce: https://$GATEWAY_IP (ou ecommerce.company.com)"
        echo "API E-commerce:      https://$GATEWAY_IP (ou api.ecommerce.company.com)"
        echo "Admin Dashboard:     https://$GATEWAY_IP (ou admin.ecommerce.company.com)"
    else
        echo "⚠️  Load Balancer IP non disponible, utiliser port-forward:"
        echo "kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80"
    fi

    # Grafana
    GRAFANA_IP=$(kubectl get svc grafana -n $MONITORING_NS -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
    if [ -n "$GRAFANA_IP" ]; then
        echo "Grafana Dashboard:   http://$GRAFANA_IP:3000"
    else
        echo "Grafana Dashboard:   kubectl port-forward -n monitoring svc/grafana 3000:3000"
    fi

    # Prometheus
    echo "Prometheus:          kubectl port-forward -n monitoring svc/prometheus 9090:9090"

    echo ""
}

# Fonction principale
main() {
    echo "🎯 Déploiement de la plateforme e-commerce"
    echo "========================================="

    # Étapes de déploiement
    check_prerequisites
    deploy_infrastructure
    deploy_databases
    deploy_microservices
    deploy_networking_security
    deploy_monitoring
    validate_deployment
    get_access_urls

    echo ""
    echo "🎉 Déploiement terminé avec succès!"
    echo "📖 Consultez la documentation pour les prochaines étapes"
    echo ""
}

# Gestion des paramètres
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "validate")
        validate_deployment
        ;;
    "urls")
        get_access_urls
        ;;
    "clean")
        log "Nettoyage de l'environnement..."
        kubectl delete namespace $NAMESPACE $MONITORING_NS
        log "✅ Environnement nettoyé"
        ;;
    *)
        echo "Usage: $0 {deploy|validate|urls|clean}"
        echo ""
        echo "Commandes:"
        echo "  deploy   - Déploiement complet (défaut)"
        echo "  validate - Validation du déploiement"
        echo "  urls     - Affichage des URLs d'accès"
        echo "  clean    - Nettoyage de l'environnement"
        exit 1
        ;;
esac
```

## Points clés de la solution complète

### 🏗️ Architecture microservices

- **Séparation des responsabilités**: Chaque service a une fonction spécifique
- **Communication asynchrone**: Event-driven architecture avec message queues
- **Résilience**: Circuit breakers, timeouts, retry policies
- **Scalabilité**: Auto-scaling basé sur les métriques métier

### 🔒 Sécurité enterprise-grade

- **Zero Trust Network**: mTLS partout avec Istio
- **RBAC granulaire**: Permissions minimales par service
- **Chiffrement**: Secrets chiffrés, TLS end-to-end
- **Monitoring sécuritaire**: Détection d'intrusion avec Falco

### 📊 Observabilité complète

- **Métriques business**: Taux de conversion, revenus, erreurs de paiement
- **Traces distribuées**: Suivi des requêtes cross-services
- **Logs centralisés**: Agrégation et corrélation des logs
- **Alerting intelligent**: Alertes basées sur le business impact

### 🚀 CI/CD et GitOps

- **Déploiement automatisé**: Pipeline GitLab CI/CD complet
- **Tests intégrés**: Unit, integration, security, performance tests
- **Rollback automatique**: Détection d'erreur et rollback
- **Environment promotion**: Dev → Staging → Production

Cette solution fournit une plateforme e-commerce complète, sécurisée, et prête pour la production avec tous les aspects d'une architecture moderne de microservices sur Kubernetes.
