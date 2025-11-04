# LAB 10 - Challenge Final : Déploiement d'une plateforme e-commerce complète

## Objectifs

- Intégrer tous les concepts appris dans les LABs précédents
- Déployer une architecture e-commerce production-ready complète
- Implémenter la sécurité, monitoring, scaling et resilience
- Valider les bonnes pratiques DevOps et Kubernetes
- Créer une documentation complète d'architecture

## Prérequis

- Tous les LABs précédents complétés
- Cluster Kubernetes multi-nœuds
- Outils de monitoring et sécurité installés
- Accès à un registry d'images Docker
- Domaine ou sous-domaines pour les services

## Contexte du Challenge

Vous êtes l'équipe DevOps d'une startup e-commerce qui lance sa plateforme. Vous devez déployer une architecture complète qui doit gérer :

- **10,000 utilisateurs simultanés** minimum
- **99.9% de disponibilité** (SLA)
- **Sécurité renforcée** (PCI DSS compliance)
- **Scaling automatique** pour Black Friday
- **Monitoring complet** et observabilité
- **Disaster recovery** avec RTO < 4h

## Architecture Cible

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                ┌─────▼─────┐
                │    CDN    │
                │ (Static)  │
                └─────┬─────┘
                      │
                ┌─────▼─────┐
                │  INGRESS  │
                │ (NGINX)   │
                └─────┬─────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼───┐    ┌───▼───┐    ┌────▼────┐
   │Frontend│    │  API  │    │ Admin   │
   │ (React)│    │Gateway│    │ Panel   │
   └────┬───┘    └───┬───┘    └────┬────┘
        │            │             │
        └────────────┼─────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐      ┌────▼────┐      ┌───▼───┐
│Product│      │   User  │      │Order  │
│Service│      │ Service │      │Service│
└───┬───┘      └────┬────┘      └───┬───┘
    │               │               │
    └───────────────┼───────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼───┐  ┌───▼───┐  ┌────▼────┐
   │MongoDB │  │Redis  │  │PostgreSQL│
   │(NoSQL) │  │(Cache)│  │  (ACID)  │
   └────────┘  └───────┘  └─────────┘
```

## Exercice 1 : Préparation de l'infrastructure

### Étape 1.1 : Structure du projet

Créez la structure complète du projet :

```
ecommerce-platform/
├── README.md
├── docker-compose.yml                    # Développement local
├── k8s/
│   ├── namespaces/
│   ├── base/                            # Manifestes de base
│   ├── overlays/                        # Environnements (dev/staging/prod)
│   └── monitoring/                      # Stack monitoring
├── applications/
│   ├── frontend/                        # React SPA
│   ├── api-gateway/                     # Gateway service
│   ├── user-service/                    # Service utilisateurs
│   ├── product-service/                 # Service produits
│   ├── order-service/                   # Service commandes
│   └── notification-service/            # Service notifications
├── infrastructure/
│   ├── helm/                           # Charts Helm
│   ├── terraform/                      # Infrastructure as Code
│   └── scripts/                        # Scripts d'automatisation
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── alertmanager/
├── security/
│   ├── rbac/
│   ├── network-policies/
│   └── pod-security/
├── ci-cd/
│   ├── gitlab-ci/
│   ├── github-actions/
│   └── argocd/
└── docs/
    ├── architecture.md
    ├── deployment.md
    └── operations.md
```

### Étape 1.2 : Namespaces et labels

Créez `k8s/namespaces/namespaces.yaml` :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-frontend
  labels:
    name: ecommerce-frontend
    tier: frontend
    env: production
    app.kubernetes.io/name: ecommerce
    app.kubernetes.io/component: frontend
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-backend
  labels:
    name: ecommerce-backend
    tier: backend
    env: production
    app.kubernetes.io/name: ecommerce
    app.kubernetes.io/component: backend
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-data
  labels:
    name: ecommerce-data
    tier: data
    env: production
    app.kubernetes.io/name: ecommerce
    app.kubernetes.io/component: database
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-monitoring
  labels:
    name: ecommerce-monitoring
    tier: monitoring
    env: production
    app.kubernetes.io/name: ecommerce
    app.kubernetes.io/component: monitoring
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-security
  labels:
    name: ecommerce-security
    tier: security
    env: production
    app.kubernetes.io/name: ecommerce
    app.kubernetes.io/component: security
```

### Étape 1.3 : Resource Quotas

Créez `k8s/base/resource-quotas.yaml` :

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: frontend-quota
  namespace: ecommerce-frontend
spec:
  hard:
    requests.cpu: '2'
    requests.memory: 4Gi
    limits.cpu: '4'
    limits.memory: 8Gi
    pods: '10'
    persistentvolumeclaims: '2'
    services: '5'
    secrets: '10'
    configmaps: '10'
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: backend-quota
  namespace: ecommerce-backend
spec:
  hard:
    requests.cpu: '8'
    requests.memory: 16Gi
    limits.cpu: '16'
    limits.memory: 32Gi
    pods: '50'
    persistentvolumeclaims: '5'
    services: '20'
    secrets: '20'
    configmaps: '20'
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: data-quota
  namespace: ecommerce-data
spec:
  hard:
    requests.cpu: '4'
    requests.memory: 8Gi
    limits.cpu: '8'
    limits.memory: 16Gi
    pods: '10'
    persistentvolumeclaims: '10'
    services: '10'
    requests.storage: '100Gi'
---
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: ecommerce-backend
spec:
  limits:
    - default:
        cpu: 200m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      type: Container
```

## Exercice 2 : Services de données

### Étape 2.1 : PostgreSQL (Données transactionnelles)

Créez `k8s/base/databases/postgresql.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
  namespace: ecommerce-data
type: Opaque
data:
  POSTGRES_USER: ZWNvbW1lcmNl # ecommerce (base64)
  POSTGRES_PASSWORD: UGFzcHc0cmQxMjM= # Pasw4rd123 (base64)
  POSTGRES_DB: ZWNvbW1lcmNlX2Ri # ecommerce_db (base64)
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgresql-config
  namespace: ecommerce-data
data:
  postgresql.conf: |
    # Performance tuning
    shared_buffers = 256MB
    effective_cache_size = 1GB
    maintenance_work_mem = 64MB
    checkpoint_completion_target = 0.9
    wal_buffers = 16MB
    default_statistics_target = 100
    random_page_cost = 1.1
    effective_io_concurrency = 200

    # Logging
    log_destination = 'stderr'
    logging_collector = on
    log_directory = 'pg_log'
    log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
    log_statement = 'mod'
    log_min_duration_statement = 1000

    # Connection settings
    max_connections = 200

  init.sql: |
    -- Create schemas
    CREATE SCHEMA IF NOT EXISTS users;
    CREATE SCHEMA IF NOT EXISTS products;
    CREATE SCHEMA IF NOT EXISTS orders;

    -- Create tables
    CREATE TABLE users.users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE products.categories (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE products.products (
        id SERIAL PRIMARY KEY,
        category_id INTEGER REFERENCES products.categories(id),
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        sku VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE orders.orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users.users(id),
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        shipping_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE orders.order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders.orders(id),
        product_id INTEGER REFERENCES products.products(id),
        quantity INTEGER NOT NULL,
        price DECIMAL(10,2) NOT NULL
    );

    -- Insert sample data
    INSERT INTO products.categories (name, description) VALUES
    ('Electronics', 'Electronic devices and accessories'),
    ('Clothing', 'Fashion and apparel'),
    ('Books', 'Books and educational materials'),
    ('Home & Garden', 'Home improvement and garden supplies');

    INSERT INTO products.products (category_id, name, description, price, stock_quantity, sku) VALUES
    (1, 'Smartphone Pro Max', 'Latest flagship smartphone', 999.99, 100, 'PHONE-001'),
    (1, 'Wireless Earbuds', 'Premium wireless earbuds', 249.99, 200, 'AUDIO-001'),
    (2, 'Designer Jeans', 'Premium denim jeans', 89.99, 50, 'CLOTH-001'),
    (3, 'Programming Book', 'Learn advanced programming', 39.99, 75, 'BOOK-001');
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql
  namespace: ecommerce-data
  labels:
    app: postgresql
    component: database
spec:
  serviceName: postgresql-headless
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
        component: database
    spec:
      securityContext:
        fsGroup: 999
      containers:
        - name: postgresql
          image: postgres:14-alpine
          ports:
            - containerPort: 5432
              name: postgresql
          envFrom:
            - secretRef:
                name: postgresql-secret
          env:
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - name: postgresql-data
              mountPath: /var/lib/postgresql/data
            - name: postgresql-config
              mountPath: /etc/postgresql/postgresql.conf
              subPath: postgresql.conf
            - name: postgresql-config
              mountPath: /docker-entrypoint-initdb.d/init.sql
              subPath: init.sql
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
          livenessProbe:
            exec:
              command:
                - /bin/sh
                - -c
                - exec pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h 127.0.0.1 -p 5432
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
          readinessProbe:
            exec:
              command:
                - /bin/sh
                - -c
                - exec pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h 127.0.0.1 -p 5432
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
      volumes:
        - name: postgresql-config
          configMap:
            name: postgresql-config
  volumeClaimTemplates:
    - metadata:
        name: postgresql-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 20Gi
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
  namespace: ecommerce-data
  labels:
    app: postgresql
spec:
  selector:
    app: postgresql
  ports:
    - name: postgresql
      port: 5432
      targetPort: 5432
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: postgresql-headless
  namespace: ecommerce-data
  labels:
    app: postgresql
spec:
  selector:
    app: postgresql
  ports:
    - name: postgresql
      port: 5432
      targetPort: 5432
  clusterIP: None
```

### Étape 2.2 : Redis (Cache et sessions)

Créez `k8s/base/databases/redis.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: ecommerce-data
data:
  redis.conf: |
    # Redis configuration for production
    bind 0.0.0.0
    port 6379

    # Memory management
    maxmemory 512mb
    maxmemory-policy allkeys-lru

    # Persistence
    save 900 1
    save 300 10
    save 60 10000
    rdbcompression yes
    rdbchecksum yes

    # Security
    requirepass Redis123!

    # Performance
    timeout 300
    tcp-keepalive 300

    # Logging
    loglevel notice
    logfile ""
---
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: ecommerce-data
type: Opaque
data:
  REDIS_PASSWORD: UmVkaXMxMjMh # Redis123! (base64)
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: ecommerce-data
  labels:
    app: redis
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
        component: cache
    spec:
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
              name: redis
          command:
            - redis-server
            - /etc/redis/redis.conf
          volumeMounts:
            - name: redis-config
              mountPath: /etc/redis
            - name: redis-data
              mountPath: /data
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 200m
              memory: 512Mi
          livenessProbe:
            exec:
              command:
                - redis-cli
                - --raw
                - incr
                - ping
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - redis-cli
                - --raw
                - incr
                - ping
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: redis-config
          configMap:
            name: redis-config
        - name: redis-data
          persistentVolumeClaim:
            claimName: redis-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: ecommerce-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: fast-ssd
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: ecommerce-data
  labels:
    app: redis
spec:
  selector:
    app: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
  type: ClusterIP
```

### Étape 2.3 : MongoDB (Données de produits)

Créez `k8s/base/databases/mongodb.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mongodb-secret
  namespace: ecommerce-data
type: Opaque
data:
  MONGO_INITDB_ROOT_USERNAME: YWRtaW4= # admin (base64)
  MONGO_INITDB_ROOT_PASSWORD: TW9uZ284ODgh # Mongo888! (base64)
  MONGO_INITDB_DATABASE: ZWNvbW1lcmNl # ecommerce (base64)
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongodb-init
  namespace: ecommerce-data
data:
  init.js: |
    // Initialize MongoDB for ecommerce
    use admin;

    // Create application user
    db.createUser({
      user: "ecommerce_user",
      pwd: "EcomUser123!",
      roles: [
        { role: "readWrite", db: "ecommerce" },
        { role: "readWrite", db: "products" }
      ]
    });

    // Switch to ecommerce database
    use ecommerce;

    // Create collections with validation
    db.createCollection("products", {
      validator: {
        $jsonSchema: {
          bsonType: "object",
          required: ["name", "price", "category"],
          properties: {
            name: { bsonType: "string" },
            price: { bsonType: "number", minimum: 0 },
            category: { bsonType: "string" },
            description: { bsonType: "string" },
            inventory: { bsonType: "number", minimum: 0 },
            tags: { bsonType: "array", items: { bsonType: "string" } }
          }
        }
      }
    });

    // Insert sample products
    db.products.insertMany([
      {
        name: "Gaming Laptop",
        price: 1299.99,
        category: "electronics",
        description: "High-performance gaming laptop",
        inventory: 25,
        tags: ["gaming", "laptop", "nvidia"],
        specifications: {
          cpu: "Intel i7-12700H",
          gpu: "RTX 3070",
          ram: "16GB DDR4",
          storage: "1TB SSD"
        },
        reviews: [],
        rating: 4.5,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        name: "Mechanical Keyboard",
        price: 149.99,
        category: "accessories",
        description: "RGB mechanical gaming keyboard",
        inventory: 100,
        tags: ["keyboard", "mechanical", "rgb"],
        specifications: {
          switches: "Cherry MX Blue",
          backlight: "RGB",
          connectivity: "USB-C"
        },
        reviews: [],
        rating: 4.8,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ]);

    // Create indexes for performance
    db.products.createIndex({ "name": "text", "description": "text" });
    db.products.createIndex({ "category": 1 });
    db.products.createIndex({ "price": 1 });
    db.products.createIndex({ "tags": 1 });
    db.products.createIndex({ "rating": -1 });
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
  namespace: ecommerce-data
  labels:
    app: mongodb
    component: database
spec:
  serviceName: mongodb-headless
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
        component: database
    spec:
      containers:
        - name: mongodb
          image: mongo:6.0
          ports:
            - containerPort: 27017
              name: mongodb
          envFrom:
            - secretRef:
                name: mongodb-secret
          volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
            - name: mongodb-init
              mountPath: /docker-entrypoint-initdb.d
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
          livenessProbe:
            exec:
              command:
                - mongosh
                - --eval
                - "db.adminCommand('ping')"
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
          readinessProbe:
            exec:
              command:
                - mongosh
                - --eval
                - "db.adminCommand('ping')"
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
      volumes:
        - name: mongodb-init
          configMap:
            name: mongodb-init
  volumeClaimTemplates:
    - metadata:
        name: mongodb-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: fast-ssd
        resources:
          requests:
            storage: 20Gi
---
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  namespace: ecommerce-data
  labels:
    app: mongodb
spec:
  selector:
    app: mongodb
  ports:
    - name: mongodb
      port: 27017
      targetPort: 27017
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: mongodb-headless
  namespace: ecommerce-data
  labels:
    app: mongodb
spec:
  selector:
    app: mongodb
  ports:
    - name: mongodb
      port: 27017
      targetPort: 27017
  clusterIP: None
```

## Exercice 3 : Services Backend

### Étape 3.1 : User Service

Créez `k8s/base/backend/user-service.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: user-service-config
  namespace: ecommerce-backend
data:
  APP_ENV: 'production'
  DATABASE_URL: 'postgresql://ecommerce:Pasw4rd123@postgresql.ecommerce-data.svc.cluster.local:5432/ecommerce_db'
  REDIS_URL: 'redis://:Redis123!@redis.ecommerce-data.svc.cluster.local:6379'
  JWT_SECRET: 'super-secret-jwt-key-change-in-prod'
  SESSION_SECRET: 'super-secret-session-key'
  BCRYPT_ROUNDS: '12'
  RATE_LIMIT_REQUESTS: '100'
  RATE_LIMIT_WINDOW: '900000'
---
apiVersion: v1
kind: Secret
metadata:
  name: user-service-secret
  namespace: ecommerce-backend
type: Opaque
data:
  DB_PASSWORD: UGFzdzRyZDEyMw== # Pasw4rd123 (base64)
  REDIS_PASSWORD: UmVkaXMxMjMh # Redis123! (base64)
  JWT_SECRET: c3VwZXItc2VjcmV0LWp3dC1rZXk= # base64 encoded
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: ecommerce-backend
  labels:
    app: user-service
    component: microservice
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        component: microservice
        tier: backend
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '3000'
        prometheus.io/path: '/metrics'
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: ['user-service']
                topologyKey: kubernetes.io/hostname
      containers:
        - name: user-service
          image: ecommerce/user-service:v1.0.0
          ports:
            - containerPort: 3000
              name: http
            - containerPort: 9090
              name: metrics
          envFrom:
            - configMapRef:
                name: user-service-config
            - secretRef:
                name: user-service-secret
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
      securityContext:
        fsGroup: 1000
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: ecommerce-backend
  labels:
    app: user-service
spec:
  selector:
    app: user-service
  ports:
    - name: http
      port: 80
      targetPort: 3000
    - name: metrics
      port: 9090
      targetPort: 9090
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
  namespace: ecommerce-backend
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 30
        - type: Pods
          value: 3
          periodSeconds: 60
      selectPolicy: Max
```

### Étape 3.2 : Product Service

Créez `k8s/base/backend/product-service.yaml` avec une structure similaire mais :

- Connecté à MongoDB
- Cache Redis pour les recherches
- Configuration spécifique aux produits

### Étape 3.3 : Order Service

Créez `k8s/base/backend/order-service.yaml` avec :

- Connexion PostgreSQL pour les commandes
- Intégration avec les autres services
- Gestion des transactions

### Étape 3.4 : API Gateway

Créez `k8s/base/backend/api-gateway.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-gateway-config
  namespace: ecommerce-backend
data:
  kong.yml: |
    _format_version: "3.0"

    services:
    - name: user-service
      url: http://user-service.ecommerce-backend.svc.cluster.local
      routes:
      - name: users-route
        paths:
        - /api/v1/users
        - /api/v1/auth
        methods:
        - GET
        - POST
        - PUT
        - DELETE
        
    - name: product-service
      url: http://product-service.ecommerce-backend.svc.cluster.local
      routes:
      - name: products-route
        paths:
        - /api/v1/products
        - /api/v1/categories
        methods:
        - GET
        - POST
        - PUT
        - DELETE
        
    - name: order-service
      url: http://order-service.ecommerce-backend.svc.cluster.local
      routes:
      - name: orders-route
        paths:
        - /api/v1/orders
        - /api/v1/cart
        methods:
        - GET
        - POST
        - PUT
        - DELETE

    plugins:
    - name: rate-limiting
      config:
        minute: 100
        hour: 1000
        
    - name: cors
      config:
        origins:
        - "https://ecommerce.yourdomain.com"
        - "https://admin.ecommerce.yourdomain.com"
        methods:
        - GET
        - POST
        - PUT
        - DELETE
        - OPTIONS
        headers:
        - Authorization
        - Content-Type
        - Accept
        exposed_headers:
        - X-Total-Count
        credentials: true
        
    - name: prometheus
      config:
        per_consumer: true
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: ecommerce-backend
  labels:
    app: api-gateway
    component: gateway
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
        component: gateway
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8100'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: kong
          image: kong:3.0
          ports:
            - containerPort: 8000
              name: proxy
            - containerPort: 8443
              name: proxy-ssl
            - containerPort: 8001
              name: admin
            - containerPort: 8444
              name: admin-ssl
            - containerPort: 8100
              name: metrics
          env:
            - name: KONG_DATABASE
              value: 'off'
            - name: KONG_DECLARATIVE_CONFIG
              value: '/kong/kong.yml'
            - name: KONG_PROXY_ACCESS_LOG
              value: '/dev/stdout'
            - name: KONG_ADMIN_ACCESS_LOG
              value: '/dev/stdout'
            - name: KONG_PROXY_ERROR_LOG
              value: '/dev/stderr'
            - name: KONG_ADMIN_ERROR_LOG
              value: '/dev/stderr'
            - name: KONG_ADMIN_LISTEN
              value: '0.0.0.0:8001'
            - name: KONG_ADMIN_GUI_URL
              value: 'http://localhost:8002'
            - name: KONG_PLUGINS
              value: 'bundled,prometheus'
          volumeMounts:
            - name: kong-config
              mountPath: /kong
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /status
              port: 8001
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /status
              port: 8001
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: kong-config
          configMap:
            name: api-gateway-config
---
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
  namespace: ecommerce-backend
  labels:
    app: api-gateway
spec:
  selector:
    app: api-gateway
  ports:
    - name: proxy
      port: 80
      targetPort: 8000
    - name: proxy-ssl
      port: 443
      targetPort: 8443
    - name: admin
      port: 8001
      targetPort: 8001
    - name: metrics
      port: 8100
      targetPort: 8100
  type: ClusterIP
```

## Exercice 4 : Frontend et Ingress

### Étape 4.1 : Frontend React

Créez `k8s/base/frontend/frontend.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config
  namespace: ecommerce-frontend
data:
  nginx.conf: |
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log notice;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
        use epoll;
        multi_accept on;
    }

    http {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
        
        # Logging
        log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
        access_log /var/log/nginx/access.log main;
        
        # Performance
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        
        # Gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_proxied any;
        gzip_comp_level 6;
        gzip_types
            text/plain
            text/css
            text/xml
            text/javascript
            application/json
            application/javascript
            application/xml+rss
            application/atom+xml
            image/svg+xml;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        
        # Rate limiting
        limit_req_zone $binary_remote_addr zone=main:10m rate=10r/s;
        
        upstream api_backend {
            server api-gateway.ecommerce-backend.svc.cluster.local;
            keepalive 32;
        }
        
        server {
            listen 80;
            server_name _;
            root /usr/share/nginx/html;
            index index.html;
            
            # Security
            server_tokens off;
            
            # Rate limiting
            limit_req zone=main burst=20 nodelay;
            
            # Health checks
            location /health {
                access_log off;
                return 200 "healthy\n";
                add_header Content-Type text/plain;
            }
            
            # Static files with caching
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
                add_header Vary Accept-Encoding;
                try_files $uri =404;
            }
            
            # API proxy
            location /api/ {
                proxy_pass http://api_backend/;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_cache_bypass $http_upgrade;
                
                # Timeouts
                proxy_connect_timeout 5s;
                proxy_send_timeout 10s;
                proxy_read_timeout 10s;
            }
            
            # React Router (SPA)
            location / {
                try_files $uri $uri/ /index.html;
                
                # No cache for index.html
                location = /index.html {
                    add_header Cache-Control "no-cache, no-store, must-revalidate";
                    add_header Pragma "no-cache";
                    add_header Expires "0";
                }
            }
            
            # Error pages
            error_page 404 /404.html;
            error_page 500 502 503 504 /50x.html;
            location = /50x.html {
                root /usr/share/nginx/html;
            }
        }
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ecommerce-frontend
  labels:
    app: frontend
    component: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        component: frontend
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '80'
        prometheus.io/path: '/nginx_status'
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: ['frontend']
                topologyKey: kubernetes.io/hostname
      containers:
        - name: frontend
          image: ecommerce/frontend:v1.0.0
          ports:
            - containerPort: 80
              name: http
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf
            - name: nginx-cache
              mountPath: /var/cache/nginx
            - name: nginx-run
              mountPath: /var/run
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            runAsUser: 101
            runAsGroup: 101
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
      volumes:
        - name: nginx-config
          configMap:
            name: frontend-config
        - name: nginx-cache
          emptyDir: {}
        - name: nginx-run
          emptyDir: {}
      securityContext:
        fsGroup: 101
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: ecommerce-frontend
  labels:
    app: frontend
spec:
  selector:
    app: frontend
  ports:
    - name: http
      port: 80
      targetPort: 80
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: ecommerce-frontend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
```

### Étape 4.2 : Ingress NGINX

Créez `k8s/base/ingress/ingress.yaml` :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce-frontend
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/use-regex: 'true'
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'
    nginx.ingress.kubernetes.io/proxy-buffer-size: '8k'
    nginx.ingress.kubernetes.io/proxy-buffers-number: '4'
    nginx.ingress.kubernetes.io/client-max-body-size: '10m'
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "X-Frame-Options: DENY";
      more_set_headers "X-Content-Type-Options: nosniff";
      more_set_headers "X-XSS-Protection: 1; mode=block";
      more_set_headers "Referrer-Policy: strict-origin-when-cross-origin";
      more_set_headers "Strict-Transport-Security: max-age=31536000; includeSubDomains";
spec:
  tls:
    - hosts:
        - ecommerce.yourdomain.com
        - api.ecommerce.yourdomain.com
        - admin.ecommerce.yourdomain.com
      secretName: ecommerce-tls
  rules:
    - host: ecommerce.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
    - host: api.ecommerce.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-gateway
                port:
                  number: 80
    - host: admin.ecommerce.yourdomain.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-panel
                port:
                  number: 80
```

## Exercice 5 : Sécurité complète

### Étape 5.1 : RBAC

Créez `security/rbac/rbac.yaml` :

```yaml
# ServiceAccounts
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-backend-sa
  namespace: ecommerce-backend
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-frontend-sa
  namespace: ecommerce-frontend
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecommerce-data-sa
  namespace: ecommerce-data
---
# Roles
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: backend-role
  namespace: ecommerce-backend
rules:
  - apiGroups: ['']
    resources: ['configmaps', 'secrets', 'services']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets']
    verbs: ['get', 'list', 'watch', 'create', 'update', 'patch', 'delete']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: data-role
  namespace: ecommerce-data
rules:
  - apiGroups: ['']
    resources: ['configmaps', 'secrets', 'persistentvolumeclaims']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['pods']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['statefulsets']
    verbs: ['get', 'list', 'watch']
---
# RoleBindings
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: backend-rolebinding
  namespace: ecommerce-backend
subjects:
  - kind: ServiceAccount
    name: ecommerce-backend-sa
    namespace: ecommerce-backend
roleRef:
  kind: Role
  name: backend-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: data-rolebinding
  namespace: ecommerce-data
subjects:
  - kind: ServiceAccount
    name: ecommerce-data-sa
    namespace: ecommerce-data
roleRef:
  kind: Role
  name: data-role
  apiGroup: rbac.authorization.k8s.io
---
# ClusterRole pour les métriques
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ecommerce-metrics-reader
rules:
  - apiGroups: ['']
    resources: ['nodes', 'nodes/metrics', 'services', 'endpoints', 'pods']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get']
  - apiGroups: ['networking.k8s.io']
    resources: ['ingresses']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['']
    resources: ['nodes/metrics']
    verbs: ['get']
  - nonResourceURLs: ['/metrics']
    verbs: ['get']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ecommerce-metrics-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ecommerce-metrics-reader
subjects:
  - kind: ServiceAccount
    name: ecommerce-backend-sa
    namespace: ecommerce-backend
```

### Étape 5.2 : Network Policies

Créez `security/network-policies/network-policies.yaml` :

```yaml
# Deny all traffic by default in backend namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: ecommerce-backend
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
---
# Allow frontend to backend communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: ecommerce-backend
spec:
  podSelector:
    matchLabels:
      component: gateway
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-frontend
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8000
---
# Allow backend services to communicate with each other
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-internal
  namespace: ecommerce-backend
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              tier: backend
      ports:
        - protocol: TCP
          port: 3000
---
# Allow backend to access databases
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-data
  namespace: ecommerce-backend
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-data
      ports:
        - protocol: TCP
          port: 5432 # PostgreSQL
        - protocol: TCP
          port: 6379 # Redis
        - protocol: TCP
          port: 27017 # MongoDB
---
# Allow data namespace internal communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-data-access
  namespace: ecommerce-data
spec:
  podSelector:
    matchLabels:
      component: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-backend
      ports:
        - protocol: TCP
          port: 5432
        - protocol: TCP
          port: 6379
        - protocol: TCP
          port: 27017
---
# Allow monitoring access
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-monitoring
  namespace: ecommerce-backend
spec:
  podSelector:
    matchLabels:
      tier: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ecommerce-monitoring
      ports:
        - protocol: TCP
          port: 9090 # Métriques Prometheus
```

### Étape 5.3 : Pod Security Standards

Créez `security/pod-security/pod-security-standards.yaml` :

```yaml
# Appliquer Pod Security Standards aux namespaces
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-backend
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-frontend
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce-data
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
# Pod Security Policy (si PSP est activé)
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: ecommerce-restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  readOnlyRootFilesystem: true
```

## Exercice 6 : Monitoring et observabilité

### Étape 6.1 : ServiceMonitors

Créez `monitoring/servicemonitors.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-backend
  namespace: ecommerce-monitoring
  labels:
    app: ecommerce
    tier: backend
spec:
  selector:
    matchLabels:
      tier: backend
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
  namespaceSelector:
    matchNames:
      - ecommerce-backend
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ecommerce-databases
  namespace: ecommerce-monitoring
  labels:
    app: ecommerce
    tier: data
spec:
  selector:
    matchLabels:
      component: database
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
  namespaceSelector:
    matchNames:
      - ecommerce-data
```

### Étape 6.2 : Alertes métier

Créez `monitoring/business-alerts.yaml` avec des alertes spécifiques :

- Taux d'erreur de commande > 5%
- Latence API > 500ms
- Échec de paiement > 2%
- Stock produit épuisé

## Exercice 7 : Tests de charge et validation

### Étape 7.1 : Scenario de test Black Friday

Créez `tests/black-friday-test.yaml` qui simule :

- Montée progressive de 100 à 10,000 utilisateurs
- Pics de trafic soudains
- Tests de resilience

### Étape 7.2 : Validation des SLA

- Disponibilité > 99.9%
- Latence p95 < 200ms
- Débit > 1000 RPS

## Exercice 8 : CI/CD et GitOps

### Étape 8.1 : Pipeline GitLab CI

Créez `.gitlab-ci.yml` complet avec :

- Build et test des applications
- Scan de sécurité
- Déploiement multi-environnements
- Tests automatisés

### Étape 8.2 : Configuration ArgoCD

Applications ArgoCD pour chaque service avec sync automatique.

## Exercice 9 : Disaster Recovery

### Étape 9.1 : Plan DR complet

- Backup automatique avec Velero
- Réplication multi-zone
- Procédures de failover

### Étape 9.2 : Tests DR automatisés

Scripts de test mensuel du plan de disaster recovery.

## Exercice 10 : Documentation et handover

### Étape 10.1 : Architecture Decision Records (ADR)

### Étape 10.2 : Runbooks opérationnels

### Étape 10.3 : Guide de troubleshooting

## Validation finale

### Critères de réussite

1. **Architecture** : Tous les composants déployés et communicants
2. **Sécurité** : RBAC, Network Policies, Pod Security
3. **Performance** : SLA respectés sous charge
4. **Monitoring** : Observabilité complète
5. **Resilience** : Tests de panne passés
6. **Automation** : CI/CD fonctionnel
7. **Documentation** : Complète et à jour

### Tests d'acceptance

- [ ] Déploiement end-to-end en 1 commande
- [ ] Montée en charge Black Friday réussie
- [ ] Recovery en moins de 4h
- [ ] Sécurité validée par audit
- [ ] Monitoring 100% des composants
- [ ] Zéro downtime deployments

## Livrables finaux

1. **Code source** complet de la plateforme
2. **Manifestes Kubernetes** pour tous les environnements
3. **Pipeline CI/CD** fonctionnel
4. **Monitoring** et alerting configurés
5. **Tests automatisés** (unitaires, intégration, performance)
6. **Documentation** complète (architecture, déploiement, opérations)
7. **Plan de disaster recovery** testé
8. **Rapport de performance** et recommandations

---

**Durée estimée : 16-20 heures (sur plusieurs jours)**  
**Difficulté : ⭐⭐⭐⭐⭐⭐**

Ce challenge final intègre tous les concepts des 9 LABs précédents dans un projet réel et production-ready. Il représente le niveau d'expertise attendu d'un DevOps senior capable de concevoir et déployer des architectures Kubernetes complexes.
