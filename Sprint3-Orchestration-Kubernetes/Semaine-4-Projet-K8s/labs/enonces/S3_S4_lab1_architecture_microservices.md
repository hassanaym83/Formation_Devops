# 📝 LAB 1 - ARCHITECTURE MICROSERVICES & IMPLÉMENTATION

**Durée : 3h | Niveau Bloom 5-Évaluer | Framework Hassan Sprint 2+**

---

## 🎯 OBJECTIFS LAB 1

### Objectifs Pédagogiques (Niveau Bloom 5 - ÉVALUER)

- **Analyser** les besoins métier et décomposer en microservices appropriés
- **Évaluer** différentes architectures et choisir les patterns optimaux
- **Concevoir** une architecture microservices production-ready
- **Justifier** les choix techniques et architecturaux

### Objectifs Techniques

- Déployer 4 microservices interconnectés sur Kind
- Implémenter communication synchrone (REST) et asynchrone (Events)
- Configurer service discovery et API Gateway
- Mettre en place monitoring et health checks

---

## 📋 CONTEXTE PROJET

### Plateforme DevOps Analytics

Vous devez concevoir et implémenter une **plateforme SaaS de monitoring DevOps** pour entreprises multi-cloud.

#### Besoins Business

- **Utilisateurs** : 500+ équipes DevOps, 10k+ développeurs
- **Scale** : 1000+ clusters Kubernetes monitorés
- **Performance** : <100ms réponse API, 99.9% uptime
- **Données** : 50k+ métriques/seconde, rétention 1 an

#### Fonctionnalités Principales

1. **Authentification** : SSO entreprise, RBAC granulaire
2. **Collecte métriques** : Multi-cloud, temps réel
3. **Alerting intelligent** : Règles dynamiques, escalade automatique
4. **Reporting** : Dashboards personnalisés, export automatisé

---

## 🏗️ ARCHITECTURE CIBLE

### Vue d'ensemble système

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Dashboard]
        MOBILE[Mobile App]
    end

    subgraph "API Gateway"
        GATEWAY[Nginx Ingress]
    end

    subgraph "Core Services"
        AUTH[Auth Service<br/>:8080]
        METRICS[Metrics Collector<br/>:8081]
        ALERTS[Alert Manager<br/>:8082]
        REPORTS[Report Generator<br/>:8083]
    end

    subgraph "Data Layer"
        POSTGRES[(PostgreSQL<br/>Auth DB)]
        TSDB[(TimescaleDB<br/>Metrics DB)]
        REDIS[(Redis<br/>Cache)]
        RABBITMQ[RabbitMQ<br/>Events]
    end

    WEB --> GATEWAY
    MOBILE --> GATEWAY

    GATEWAY --> AUTH
    GATEWAY --> METRICS
    GATEWAY --> ALERTS
    GATEWAY --> REPORTS

    AUTH --> POSTGRES
    METRICS --> TSDB
    METRICS --> REDIS
    ALERTS --> TSDB
    REPORTS --> TSDB

    METRICS --> RABBITMQ
    ALERTS --> RABBITMQ
    REPORTS --> RABBITMQ
```

---

## 🛠️ INSTRUCTIONS LAB 1

### Partie 1 : Setup Environnement (45min)

#### 1.1 Cluster Kind Multi-Node

Créez un cluster Kind optimisé pour microservices :

```bash
# Configuration cluster microservices
cat > kind-microservices.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: microservices-lab
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
  - containerPort: 443
    hostPort: 8443
- role: worker
  labels:
    tier: compute
- role: worker
  labels:
    tier: storage
EOF

# Créer le cluster
kind create cluster --config=kind-microservices.yaml
kubectl cluster-info --context kind-microservices-lab
```

#### 1.2 Ingress Controller et Namespace

```bash
# Installation Nginx Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Attendre déploiement complet
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Créer namespace dédié
kubectl create namespace microservices
kubectl label namespace microservices project=devops-analytics
```

### Partie 2 : Couche Données (60min)

#### 2.1 PostgreSQL pour Auth Service

Créez les manifests Kubernetes pour PostgreSQL :

```yaml
# postgres-auth-deployment.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-auth-secret
  namespace: microservices
type: Opaque
data:
  username: YXV0aF91c2Vy # auth_user (base64)
  password: YXV0aF9wYXNzd29yZA== # auth_password (base64)
  database: YXV0aF9kYg== # auth_db (base64)

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-auth-pvc
  namespace: microservices
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 5Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-auth
  namespace: microservices
  labels:
    app: postgres-auth
    tier: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres-auth
  template:
    metadata:
      labels:
        app: postgres-auth
        tier: database
    spec:
      containers:
        - name: postgres
          image: postgres:14-alpine
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: password
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: database
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          ports:
            - containerPort: 5432
              name: postgres
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
                - -d
                - $(POSTGRES_DB)
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
                - -d
                - $(POSTGRES_DB)
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-auth-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-auth
  namespace: microservices
  labels:
    app: postgres-auth
spec:
  selector:
    app: postgres-auth
  ports:
    - port: 5432
      targetPort: 5432
      name: postgres
  type: ClusterIP
```

#### 2.2 TimescaleDB pour Métriques

```yaml
# timescaledb-deployment.yaml
apiVersion: v1
kind: Secret
metadata:
  name: timescaledb-secret
  namespace: microservices
type: Opaque
data:
  username: bWV0cmljc191c2Vy # metrics_user (base64)
  password: bWV0cmljc19wYXNzd29yZA== # metrics_password (base64)
  database: bWV0cmljc19kYg== # metrics_db (base64)

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: timescaledb-pvc
  namespace: microservices
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 10Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timescaledb
  namespace: microservices
  labels:
    app: timescaledb
    tier: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: timescaledb
  template:
    metadata:
      labels:
        app: timescaledb
        tier: database
    spec:
      containers:
        - name: timescaledb
          image: timescale/timescaledb:latest-pg14
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: password
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: database
          ports:
            - containerPort: 5432
              name: postgres
          volumeMounts:
            - name: timescaledb-storage
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              memory: '512Mi'
              cpu: '250m'
            limits:
              memory: '1Gi'
              cpu: '500m'
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
                - -d
                - $(POSTGRES_DB)
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - $(POSTGRES_USER)
                - -d
                - $(POSTGRES_DB)
            initialDelaySeconds: 10
            periodSeconds: 5
      volumes:
        - name: timescaledb-storage
          persistentVolumeClaim:
            claimName: timescaledb-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: timescaledb
  namespace: microservices
  labels:
    app: timescaledb
spec:
  selector:
    app: timescaledb
  ports:
    - port: 5432
      targetPort: 5432
      name: postgres
  type: ClusterIP
```

#### 2.3 Redis Cache et RabbitMQ

**Redis Cache :**

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: microservices
  labels:
    app: redis
    tier: cache
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
        tier: cache
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
              name: redis
          command: ['redis-server']
          args:
            - --appendonly yes
            - --maxmemory 256mb
            - --maxmemory-policy allkeys-lru
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          livenessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - redis-cli
                - ping
            initialDelaySeconds: 5
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: microservices
  labels:
    app: redis
spec:
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
      name: redis
  type: ClusterIP
```

**RabbitMQ Message Broker :**

```yaml
# rabbitmq-deployment.yaml
apiVersion: v1
kind: Secret
metadata:
  name: rabbitmq-secret
  namespace: microservices
type: Opaque
data:
  username: YWRtaW4= # admin (base64)
  password: cmFiYml0bXFfcGFzc3dvcmQ= # rabbitmq_password (base64)

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rabbitmq
  namespace: microservices
  labels:
    app: rabbitmq
    tier: messaging
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rabbitmq
  template:
    metadata:
      labels:
        app: rabbitmq
        tier: messaging
    spec:
      containers:
        - name: rabbitmq
          image: rabbitmq:3-management-alpine
          env:
            - name: RABBITMQ_DEFAULT_USER
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: username
            - name: RABBITMQ_DEFAULT_PASS
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: password
          ports:
            - containerPort: 5672
              name: amqp
            - containerPort: 15672
              name: management
          resources:
            requests:
              memory: '256Mi'
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '300m'
          livenessProbe:
            exec:
              command:
                - rabbitmqctl
                - status
            initialDelaySeconds: 60
            periodSeconds: 30
          readinessProbe:
            exec:
              command:
                - rabbitmqctl
                - status
            initialDelaySeconds: 20
            periodSeconds: 10

---
apiVersion: v1
kind: Service
metadata:
  name: rabbitmq
  namespace: microservices
  labels:
    app: rabbitmq
spec:
  selector:
    app: rabbitmq
  ports:
    - port: 5672
      targetPort: 5672
      name: amqp
    - port: 15672
      targetPort: 15672
      name: management
  type: ClusterIP
```

### Partie 3 : Services Applicatifs (75min)

#### 3.1 Configuration Globale

```yaml
# platform-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: platform-config
  namespace: microservices
data:
  environment: 'development'
  log_level: 'DEBUG'
  cors_origins: '*'
  jwt_secret: 'dev-secret-key-change-in-production'
  jwt_expiry: '24h'
  database_pool_size: '10'
  cache_ttl: '300'
  rate_limit_requests: '100'
  rate_limit_window: '60s'
```

#### 3.2 Auth Service

```yaml
# auth-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: microservices
  labels:
    app: auth-service
    version: v1.0.0
    tier: application
spec:
  replicas: 2
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
        version: v1.0.0
        tier: application
    spec:
      containers:
        - name: auth-service
          # Mock avec nginx pour LAB - remplacer par vraie image en production
          image: nginx:alpine
          ports:
            - containerPort: 80
              name: http
          env:
            - name: DATABASE_URL
              value: 'postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@postgres-auth:5432/$(POSTGRES_DB)'
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: password
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: postgres-auth-secret
                  key: database
            - name: JWT_SECRET
              valueFrom:
                configMapKeyRef:
                  name: platform-config
                  key: jwt_secret
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: platform-config
                  key: log_level
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
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          # Configuration mock pour simulation
          volumeMounts:
            - name: auth-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: auth-config
          configMap:
            name: auth-service-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: auth-service-config
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Auth Service</title></head>
    <body>
      <h1>DevOps Analytics - Auth Service</h1>
      <p>Status: Ready</p>
      <p>Version: v1.0.0</p>
      <p>Environment: Development</p>
      <div>
        <h3>API Endpoints:</h3>
        <ul>
          <li>POST /auth/login</li>
          <li>POST /auth/refresh</li>
          <li>GET /auth/validate</li>
          <li>GET /users/{id}</li>
          <li>POST /users</li>
        </ul>
      </div>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: auth-service
  namespace: microservices
  labels:
    app: auth-service
spec:
  selector:
    app: auth-service
  ports:
    - port: 8080
      targetPort: 80
      name: http
  type: ClusterIP
```

#### 3.3 Metrics Collector Service

```yaml
# metrics-collector-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-collector
  namespace: microservices
  labels:
    app: metrics-collector
    version: v1.0.0
    tier: application
spec:
  replicas: 3 # Scaling pour haute charge
  selector:
    matchLabels:
      app: metrics-collector
  template:
    metadata:
      labels:
        app: metrics-collector
        version: v1.0.0
        tier: application
    spec:
      containers:
        - name: metrics-collector
          image: nginx:alpine # Mock service
          ports:
            - containerPort: 80
              name: http
          env:
            - name: TIMESCALEDB_URL
              value: 'postgresql://$(TIMESCALE_USER):$(TIMESCALE_PASSWORD)@timescaledb:5432/$(TIMESCALE_DB)'
            - name: TIMESCALE_USER
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: username
            - name: TIMESCALE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: password
            - name: TIMESCALE_DB
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: database
            - name: REDIS_URL
              value: 'redis://redis:6379'
            - name: RABBITMQ_URL
              value: 'amqp://$(RABBITMQ_USER):$(RABBITMQ_PASSWORD)@rabbitmq:5672/'
            - name: RABBITMQ_USER
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: username
            - name: RABBITMQ_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: password
            - name: AUTH_SERVICE_URL
              value: 'http://auth-service:8080'
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
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              memory: '256Mi'
              cpu: '200m'
            limits:
              memory: '512Mi'
              cpu: '400m'
          volumeMounts:
            - name: metrics-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: metrics-config
          configMap:
            name: metrics-collector-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: metrics-collector-config
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Metrics Collector</title></head>
    <body>
      <h1>DevOps Analytics - Metrics Collector</h1>
      <p>Status: Ready</p>
      <p>Version: v1.0.0</p>
      <p>Replicas: 3</p>
      <div>
        <h3>API Endpoints:</h3>
        <ul>
          <li>POST /metrics/ingest</li>
          <li>GET /metrics/query</li>
          <li>GET /metrics/aggregates</li>
        </ul>
      </div>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: metrics-collector
  namespace: microservices
  labels:
    app: metrics-collector
spec:
  selector:
    app: metrics-collector
  ports:
    - port: 8081
      targetPort: 80
      name: http
  type: ClusterIP
```

#### 3.4 Alert Manager et Report Generator

**Alert Manager :**

```yaml
# alert-manager-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alert-manager
  namespace: microservices
  labels:
    app: alert-manager
    version: v1.0.0
    tier: application
spec:
  replicas: 2
  selector:
    matchLabels:
      app: alert-manager
  template:
    metadata:
      labels:
        app: alert-manager
        version: v1.0.0
        tier: application
    spec:
      containers:
        - name: alert-manager
          image: nginx:alpine
          ports:
            - containerPort: 80
              name: http
          env:
            - name: AUTH_SERVICE_URL
              value: 'http://auth-service:8080'
            - name: METRICS_SERVICE_URL
              value: 'http://metrics-collector:8081'
            - name: RABBITMQ_URL
              value: 'amqp://$(RABBITMQ_USER):$(RABBITMQ_PASSWORD)@rabbitmq:5672/'
            - name: RABBITMQ_USER
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: username
            - name: RABBITMQ_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: rabbitmq-secret
                  key: password
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
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          volumeMounts:
            - name: alert-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: alert-config
          configMap:
            name: alert-manager-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: alert-manager-config
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Alert Manager</title></head>
    <body>
      <h1>DevOps Analytics - Alert Manager</h1>
      <p>Status: Ready</p>
      <p>Version: v1.0.0</p>
      <div>
        <h3>API Endpoints:</h3>
        <ul>
          <li>POST /alerts/rules</li>
          <li>GET /alerts/active</li>
          <li>POST /alerts/acknowledge</li>
        </ul>
      </div>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: alert-manager
  namespace: microservices
  labels:
    app: alert-manager
spec:
  selector:
    app: alert-manager
  ports:
    - port: 8082
      targetPort: 80
      name: http
  type: ClusterIP
```

**Report Generator :**

```yaml
# report-generator-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: report-generator
  namespace: microservices
  labels:
    app: report-generator
    version: v1.0.0
    tier: application
spec:
  replicas: 1
  selector:
    matchLabels:
      app: report-generator
  template:
    metadata:
      labels:
        app: report-generator
        version: v1.0.0
        tier: application
    spec:
      containers:
        - name: report-generator
          image: nginx:alpine
          ports:
            - containerPort: 80
              name: http
          env:
            - name: AUTH_SERVICE_URL
              value: 'http://auth-service:8080'
            - name: METRICS_SERVICE_URL
              value: 'http://metrics-collector:8081'
            - name: TIMESCALEDB_URL
              value: 'postgresql://$(TIMESCALE_USER):$(TIMESCALE_PASSWORD)@timescaledb:5432/$(TIMESCALE_DB)'
            - name: TIMESCALE_USER
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: username
            - name: TIMESCALE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: password
            - name: TIMESCALE_DB
              valueFrom:
                secretKeyRef:
                  name: timescaledb-secret
                  key: database
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
            initialDelaySeconds: 10
            periodSeconds: 5
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '300m'
          volumeMounts:
            - name: report-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: report-config
          configMap:
            name: report-generator-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: report-generator-config
  namespace: microservices
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Report Generator</title></head>
    <body>
      <h1>DevOps Analytics - Report Generator</h1>
      <p>Status: Ready</p>
      <p>Version: v1.0.0</p>
      <div>
        <h3>API Endpoints:</h3>
        <ul>
          <li>POST /reports/generate</li>
          <li>GET /reports/{id}</li>
          <li>POST /reports/schedule</li>
        </ul>
      </div>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: report-generator
  namespace: microservices
  labels:
    app: report-generator
spec:
  selector:
    app: report-generator
  ports:
    - port: 8083
      targetPort: 80
      name: http
  type: ClusterIP
```

### Partie 4 : API Gateway (30min)

#### 4.1 Ingress Configuration

```yaml
# api-gateway-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-gateway
  namespace: microservices
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/cors-allow-origin: '*'
    nginx.ingress.kubernetes.io/cors-allow-methods: 'GET, POST, PUT, DELETE, OPTIONS'
    nginx.ingress.kubernetes.io/cors-allow-headers: 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization'
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'
spec:
  rules:
    - host: api.devops-platform.local
      http:
        paths:
          # Auth Service - pas d'auth supplémentaire
          - path: /auth(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: auth-service
                port:
                  number: 8080
          # Metrics Service
          - path: /metrics(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: metrics-collector
                port:
                  number: 8081
          # Alerts Service
          - path: /alerts(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: alert-manager
                port:
                  number: 8082
          # Reports Service
          - path: /reports(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: report-generator
                port:
                  number: 8083

---
# Ingress pour RabbitMQ Management (dev only)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rabbitmq-management
  namespace: microservices
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: rabbitmq.devops-platform.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rabbitmq
                port:
                  number: 15672
```

#### 4.2 Configuration DNS Locale

```bash
# Configuration /etc/hosts pour test local
echo "127.0.0.1 api.devops-platform.local" | sudo tee -a /etc/hosts
echo "127.0.0.1 rabbitmq.devops-platform.local" | sudo tee -a /etc/hosts

# Vérification
ping -c 1 api.devops-platform.local
```

### Partie 5 : Tests et Validation (30min)

#### 5.1 Script de Déploiement

Créez un script `deploy-microservices.sh` :

```bash
#!/bin/bash
set -e

echo "🚀 Déploiement Plateforme DevOps Analytics"
echo "========================================="

# Configuration
NAMESPACE="microservices"
TIMEOUT="300s"

# Fonctions utilitaires
log_info() { echo "ℹ️  $1"; }
log_success() { echo "✅ $1"; }
log_error() { echo "❌ $1"; exit 1; }

# Étape 1: Infrastructure
log_info "Déploiement infrastructure..."
kubectl apply -f platform-config.yaml
kubectl apply -f postgres-auth-deployment.yaml
kubectl apply -f timescaledb-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f rabbitmq-deployment.yaml

# Attendre infrastructure prête
log_info "Attente infrastructure..."
kubectl wait --for=condition=ready pod -l tier=database -n $NAMESPACE --timeout=$TIMEOUT
kubectl wait --for=condition=ready pod -l tier=cache -n $NAMESPACE --timeout=60s
kubectl wait --for=condition=ready pod -l tier=messaging -n $NAMESPACE --timeout=120s
log_success "Infrastructure prête"

# Étape 2: Services applicatifs
log_info "Déploiement services applicatifs..."
kubectl apply -f auth-service-deployment.yaml
kubectl apply -f metrics-collector-deployment.yaml
kubectl apply -f alert-manager-deployment.yaml
kubectl apply -f report-generator-deployment.yaml

# Attendre services prêts
log_info "Attente services applicatifs..."
kubectl wait --for=condition=ready pod -l tier=application -n $NAMESPACE --timeout=180s
log_success "Services applicatifs prêts"

# Étape 3: API Gateway
log_info "Configuration API Gateway..."
kubectl apply -f api-gateway-ingress.yaml
log_success "API Gateway configuré"

# Validation déploiement
log_info "Validation déploiement..."
kubectl get pods -n $NAMESPACE
kubectl get svc -n $NAMESPACE
kubectl get ingress -n $NAMESPACE

log_success "Déploiement terminé avec succès!"
echo ""
echo "🌐 Accès:"
echo "   API Gateway: http://api.devops-platform.local:8080"
echo "   RabbitMQ:    http://rabbitmq.devops-platform.local:8080"
echo ""
echo "🧪 Tests:"
echo "   curl -H 'Host: api.devops-platform.local' http://localhost:8080/auth/"
echo "   curl -H 'Host: api.devops-platform.local' http://localhost:8080/metrics/"
```

#### 5.2 Tests d'Intégration

```bash
# Test 1: Santé des services
echo "=== Test Santé Services ==="
for service in auth-service metrics-collector alert-manager report-generator; do
    echo "Testing $service..."
    kubectl exec -n microservices deployment/$service -- wget -qO- localhost
done

# Test 2: Communication inter-services
echo "=== Test Communication Inter-Services ==="
kubectl exec -n microservices deployment/metrics-collector -- wget -qO- auth-service:8080
kubectl exec -n microservices deployment/alert-manager -- wget -qO- metrics-collector:8081

# Test 3: Connectivité bases de données
echo "=== Test Bases de Données ==="
kubectl exec -n microservices deployment/postgres-auth -- pg_isready
kubectl exec -n microservices deployment/timescaledb -- pg_isready
kubectl exec -n microservices deployment/redis -- redis-cli ping

# Test 4: API Gateway
echo "=== Test API Gateway ==="
curl -H "Host: api.devops-platform.local" http://localhost:8080/auth/
curl -H "Host: api.devops-platform.local" http://localhost:8080/metrics/
curl -H "Host: api.devops-platform.local" http://localhost:8080/alerts/
curl -H "Host: api.devops-platform.local" http://localhost:8080/reports/

# Test 5: RabbitMQ
echo "=== Test RabbitMQ ==="
kubectl exec -n microservices deployment/rabbitmq -- rabbitmqctl list_queues
curl -H "Host: rabbitmq.devops-platform.local" http://localhost:8080/
```

---

## 📊 LIVRABLES LAB 1

### 1. Architecture Documentation

Créez `ARCHITECTURE.md` avec :

- **Vue d'ensemble** : Diagramme architecture complète
- **Services** : Description détaillée de chaque microservice
- **Communication** : Patterns sync/async utilisés
- **Data Management** : Stratégie "database per service"
- **Justifications** : Choix techniques argumentés

### 2. Manifests Kubernetes

Organisez vos fichiers :

```
lab1-microservices/
├── infrastructure/
│   ├── namespace.yaml
│   ├── postgres-auth.yaml
│   ├── timescaledb.yaml
│   ├── redis.yaml
│   └── rabbitmq.yaml
├── services/
│   ├── auth-service.yaml
│   ├── metrics-collector.yaml
│   ├── alert-manager.yaml
│   └── report-generator.yaml
├── gateway/
│   └── api-gateway-ingress.yaml
├── config/
│   └── platform-config.yaml
├── scripts/
│   ├── deploy.sh
│   └── test.sh
└── docs/
    ├── ARCHITECTURE.md
    └── README.md
```

### 3. Tests et Validation

Créez `TEST-RESULTS.md` avec résultats :

- **Santé services** : Tous pods Running
- **Communication** : Inter-service OK
- **Databases** : Connectivité validée
- **API Gateway** : Routing fonctionnel
- **Performance** : Temps réponse mesurés

---

## 🎯 ÉVALUATION LAB 1

### Critères Techniques (15 points)

| Critère                | Points | Description                    |
| ---------------------- | ------ | ------------------------------ |
| Déploiement complet    | 4      | Tous services fonctionnels     |
| Communication services | 3      | REST + Service discovery       |
| Bases de données       | 3      | PostgreSQL, TimescaleDB, Redis |
| API Gateway            | 3      | Ingress avec routing correct   |
| Health checks          | 2      | Probes fonctionnelles          |

### Critères Architecture (10 points)

| Critère                | Points | Description             |
| ---------------------- | ------ | ----------------------- |
| Décomposition services | 3      | Responsabilités claires |
| Patterns communication | 2      | Sync/Async appropriés   |
| Data ownership         | 2      | Database per service    |
| Scalabilité            | 2      | Réplicas optimisés      |
| Documentation          | 1      | Architecture documentée |

### Critères Bloom Niveau 5 (5 points)

| Critère                 | Points | Description             |
| ----------------------- | ------ | ----------------------- |
| Analyse besoins         | 2      | Décomposition justifiée |
| Évaluation patterns     | 2      | Choix argumentés        |
| Conception architecture | 1      | Design production-ready |

**Total : 30 points | Seuil : 23 points (75%)**

---

## 🔄 SUITE LAB 2-3

### LAB 2 - Intégration CI/CD + Monitoring (3h)

- Pipeline GitLab multi-services
- Prometheus/Grafana observabilité
- Tests automatisés d'intégration

### LAB 3 - Production + Optimisation (2h)

- Performance tuning et scaling
- Security policies RBAC
- Disaster recovery procedures

---

**LAB 1 Semaine 4 - Architecture Microservices | Framework Hassan Sprint 2+ | 3h**
