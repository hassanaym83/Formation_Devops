# LAB 10 - Challenge application complète multi-tiers

## Objectifs

- Intégrer tous les concepts Kubernetes appris
- Déployer une application complète 3-tiers
- Implémenter les bonnes pratiques de production
- Démontrer la maîtrise de l'orchestration Kubernetes

## Contexte

Déploiement d'une application e-commerce complète avec frontend, backend API et base de données, en appliquant tous les concepts DevOps et Kubernetes.

## Prérequis

- Maîtrise de tous les LABs précédents
- Cluster Kubernetes fonctionnel
- Ingress Controller configuré

## Architecture cible

```
Internet
    ↓
[Ingress TLS]
    ↓
[Frontend Service] → [Frontend Pods (3 replicas)]
    ↓
[Backend Service] → [Backend Pods (2 replicas)]
    ↓
[Database Service] → [Database Pod (StatefulSet)]
    ↓
[Persistent Volume]
```

## Instructions

### 1. Configuration et secrets

```yaml
# Créer le fichier ecommerce-config.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce

---
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
  namespace: ecommerce
type: Opaque
data:
  # echo -n "postgres" | base64
  username: cG9zdGdyZXM=
  # echo -n "SecurePassword123" | base64
  password: U2VjdXJlUGFzc3dvcmQxMjM=
  # echo -n "ecommerce_db" | base64
  database: ZWNvbW1lcmNlX2Ri

---
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: ecommerce
type: Opaque
data:
  # echo -n "jwt-secret-key-super-secure-2024" | base64
  jwt_secret: and0LXNlY3JldC1rZXktc3VwZXItc2VjdXJlLTIwMjQ=
  # echo -n "stripe_sk_test_123456789" | base64
  stripe_key: c3RyaXBlX3NrX3Rlc3RfMTIzNDU2Nzg5
  # echo -n "smtp_password_secure" | base64
  email_password: c210cF9wYXNzd29yZF9zZWN1cmU=

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ecommerce
data:
  # Configuration de l'API
  api_config.yml: |
    server:
      host: "0.0.0.0"
      port: 3000
      cors_origin: "https://ecommerce.local"

    database:
      host: "postgres-service"
      port: "5432"
      max_connections: 20
      timeout: 5000

    cache:
      host: "redis-service"
      port: "6379"
      ttl: 3600

    external_services:
      payment_gateway: "https://api.stripe.com"
      email_service: "smtp.gmail.com:587"
      inventory_api: "https://api.inventory.com"

    monitoring:
      metrics_enabled: true
      health_check_path: "/health"
      metrics_path: "/metrics"

  # Configuration frontend
  frontend_config.js: |
    window.APP_CONFIG = {
      API_BASE_URL: '/api/v1',
      APP_NAME: 'E-Commerce Platform',
      VERSION: '1.0.0',
      FEATURES: {
        user_registration: true,
        payment_processing: true,
        inventory_tracking: true,
        order_management: true
      },
      UI_CONFIG: {
        theme: 'modern',
        language: 'fr',
        currency: 'EUR'
      }
    };

  # Configuration nginx pour le frontend
  nginx.conf: |
    events {
        worker_connections 1024;
    }

    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;
        
        upstream backend {
            server backend-service:3000 max_fails=3 fail_timeout=30s;
        }
        
        server {
            listen 80;
            server_name localhost;
            root /usr/share/nginx/html;
            index index.html;
            
            # Frontend routes
            location / {
                try_files $uri $uri/ /index.html;
                add_header Cache-Control "no-cache, no-store, must-revalidate";
            }
            
            # API proxy
            location /api/ {
                proxy_pass http://backend/;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_timeout 60s;
            }
            
            # Health check
            location /health {
                access_log off;
                return 200 "healthy\n";
                add_header Content-Type text/plain;
            }
        }
    }
```

### 2. Base de données PostgreSQL avec persistance

```yaml
# Créer le fichier database.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: ecommerce
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: ecommerce
spec:
  serviceName: postgres-service
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
        tier: database
    spec:
      containers:
        - name: postgres
          image: postgres:14-alpine
          env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: password
            - name: POSTGRES_DB
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: database
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
            - name: init-scripts
              mountPath: /docker-entrypoint-initdb.d
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
                - postgres
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc
        - name: init-scripts
          configMap:
            name: postgres-init-scripts

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-init-scripts
  namespace: ecommerce
data:
  01-create-tables.sql: |
    -- Users table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Products table
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(10,2) NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        category VARCHAR(100),
        image_url VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Orders table
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        shipping_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Order items table
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

  02-sample-data.sql: |
    -- Sample users
    INSERT INTO users (email, password_hash, first_name, last_name) VALUES
    ('admin@ecommerce.com', '$2b$12$hash1', 'Admin', 'User'),
    ('john@example.com', '$2b$12$hash2', 'John', 'Doe'),
    ('jane@example.com', '$2b$12$hash3', 'Jane', 'Smith')
    ON CONFLICT (email) DO NOTHING;

    -- Sample products
    INSERT INTO products (name, description, price, stock_quantity, category) VALUES
    ('Laptop Pro', 'High-performance laptop', 1299.99, 10, 'Electronics'),
    ('Smartphone X', 'Latest smartphone model', 899.99, 25, 'Electronics'),
    ('Coffee Mug', 'Premium ceramic coffee mug', 19.99, 100, 'Home'),
    ('Running Shoes', 'Comfortable running shoes', 129.99, 50, 'Sports'),
    ('Book: DevOps Guide', 'Complete DevOps handbook', 39.99, 200, 'Books')
    ON CONFLICT DO NOTHING;

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: ecommerce
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP
```

### 3. Backend API

```yaml
# Créer le fichier backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: ecommerce
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        tier: backend
    spec:
      containers:
        - name: backend
          image: node:18-alpine
          command: ['/bin/sh']
          args:
            [
              '-c',
              'npm install -g json-server && json-server --host 0.0.0.0 --port 3000 /data/db.json --routes /data/routes.json'
            ]
          ports:
            - containerPort: 3000
          env:
            - name: NODE_ENV
              value: 'production'
            - name: DATABASE_HOST
              value: 'postgres-service'
            - name: DATABASE_PORT
              value: '5432'
            - name: DATABASE_NAME
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: database
            - name: DATABASE_USER
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: username
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: password
            - name: JWT_SECRET
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: jwt_secret
          volumeMounts:
            - name: api-data
              mountPath: /data
            - name: app-config
              mountPath: /app/config
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: api-data
          configMap:
            name: api-data
        - name: app-config
          configMap:
            name: app-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-data
  namespace: ecommerce
data:
  db.json: |
    {
      "products": [
        {
          "id": 1,
          "name": "Laptop Pro",
          "description": "High-performance laptop for professionals",
          "price": 1299.99,
          "stock": 10,
          "category": "Electronics",
          "image": "/images/laptop-pro.jpg"
        },
        {
          "id": 2,
          "name": "Smartphone X", 
          "description": "Latest generation smartphone",
          "price": 899.99,
          "stock": 25,
          "category": "Electronics",
          "image": "/images/smartphone-x.jpg"
        },
        {
          "id": 3,
          "name": "Coffee Mug",
          "description": "Premium ceramic coffee mug",
          "price": 19.99,
          "stock": 100,
          "category": "Home",
          "image": "/images/coffee-mug.jpg"
        }
      ],
      "users": [
        {
          "id": 1,
          "email": "admin@ecommerce.com",
          "firstName": "Admin",
          "lastName": "User",
          "role": "admin"
        }
      ],
      "orders": [
        {
          "id": 1,
          "userId": 1,
          "products": [{"productId": 1, "quantity": 1}],
          "total": 1299.99,
          "status": "completed",
          "createdAt": "2024-01-15T10:00:00Z"
        }
      ]
    }

  routes.json: |
    {
      "/api/v1/*": "/$1",
      "/health": "/products"
    }

---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: ecommerce
spec:
  selector:
    app: backend
  ports:
    - port: 3000
      targetPort: 3000
  type: ClusterIP
```

### 4. Frontend web

```yaml
# Créer le fichier frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      containers:
        - name: frontend
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf
            - name: frontend-content
              mountPath: /usr/share/nginx/html
            - name: app-config
              mountPath: /usr/share/nginx/html/config
          resources:
            requests:
              memory: '64Mi'
              cpu: '50m'
            limits:
              memory: '128Mi'
              cpu: '100m'
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: nginx-config
          configMap:
            name: app-config
            items:
              - key: nginx.conf
                path: nginx.conf
        - name: frontend-content
          configMap:
            name: frontend-content
        - name: app-config
          configMap:
            name: app-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-content
  namespace: ecommerce
data:
  index.html: |
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>E-Commerce Platform</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
            .header { background: #2c3e50; color: white; padding: 1rem 0; }
            .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
            .nav { display: flex; justify-content: space-between; align-items: center; }
            .logo { font-size: 1.5rem; font-weight: bold; }
            .nav-links { display: flex; list-style: none; gap: 2rem; }
            .nav-links a { color: white; text-decoration: none; }
            .main { padding: 2rem 0; }
            .hero { background: white; padding: 3rem 2rem; text-align: center; border-radius: 8px; margin-bottom: 2rem; }
            .products { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
            .product-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .product-card h3 { color: #2c3e50; margin-bottom: 1rem; }
            .price { font-size: 1.2rem; font-weight: bold; color: #27ae60; }
            .btn { background: #3498db; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #2980b9; }
            .status { margin: 1rem 0; padding: 1rem; background: #e8f5e8; border-radius: 4px; }
            .footer { background: #34495e; color: white; text-align: center; padding: 2rem 0; margin-top: 3rem; }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="container">
                <nav class="nav">
                    <div class="logo">🛒 E-Commerce Platform</div>
                    <ul class="nav-links">
                        <li><a href="/">Accueil</a></li>
                        <li><a href="/products">Produits</a></li>
                        <li><a href="/cart">Panier</a></li>
                        <li><a href="/account">Compte</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <main class="main">
            <div class="container">
                <div class="hero">
                    <h1>Bienvenue sur notre plateforme E-Commerce</h1>
                    <p>Découvrez nos produits de qualité avec un service client exceptionnel</p>
                    <div class="status" id="status">
                        <strong>Statut de l'application :</strong> <span id="app-status">Vérification...</span>
                    </div>
                </div>

                <div class="products" id="products-container">
                    <div class="product-card">
                        <h3>Chargement des produits...</h3>
                        <p>Connexion à l'API en cours...</p>
                    </div>
                </div>
            </div>
        </main>

        <footer class="footer">
            <div class="container">
                <p>&copy; 2024 E-Commerce Platform - Kubernetes LAB 10 Challenge</p>
                <p>Frontend: <span id="frontend-info">Loading...</span> | Backend: <span id="backend-info">Loading...</span></p>
            </div>
        </footer>

        <script>
            // Configuration de l'application
            const API_BASE = '/api/v1';
            
            // Vérification du statut de l'application
            async function checkAppStatus() {
                try {
                    const response = await fetch('/health');
                    document.getElementById('app-status').textContent = 'Opérationnel ✅';
                    document.getElementById('frontend-info').textContent = 'OK ✅';
                } catch (error) {
                    document.getElementById('app-status').textContent = 'Problème détecté ❌';
                    document.getElementById('frontend-info').textContent = 'Error ❌';
                }
            }

            // Chargement des produits
            async function loadProducts() {
                try {
                    const response = await fetch(API_BASE + '/products');
                    const products = await response.json();
                    
                    document.getElementById('backend-info').textContent = 'OK ✅';
                    
                    const container = document.getElementById('products-container');
                    container.innerHTML = products.map(product => `
                        <div class="product-card">
                            <h3>${product.name}</h3>
                            <p>${product.description}</p>
                            <div class="price">${product.price}€</div>
                            <p>Stock: ${product.stock} unités</p>
                            <button class="btn" onclick="addToCart(${product.id})">
                                Ajouter au panier
                            </button>
                        </div>
                    `).join('');
                } catch (error) {
                    document.getElementById('backend-info').textContent = 'Error ❌';
                    document.getElementById('products-container').innerHTML = `
                        <div class="product-card">
                            <h3>Erreur de connexion à l'API</h3>
                            <p>Impossible de charger les produits. Vérifiez la connexion backend.</p>
                        </div>
                    `;
                }
            }

            function addToCart(productId) {
                alert(`Produit ${productId} ajouté au panier ! (Fonctionnalité de démonstration)`);
            }

            // Initialisation de l'application
            document.addEventListener('DOMContentLoaded', () => {
                checkAppStatus();
                loadProducts();
                
                // Mise à jour périodique du statut
                setInterval(checkAppStatus, 30000);
            });
        </script>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: ecommerce
spec:
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

### 5. Ingress avec TLS

```yaml
# Créer le fichier ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/proxy-body-size: '50m'
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'
spec:
  tls:
    - hosts:
        - ecommerce.local
      secretName: ecommerce-tls-secret
  rules:
    - host: ecommerce.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

### 6. Monitoring et observabilité

```yaml
# Créer le fichier monitoring.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: monitoring-sa
  namespace: ecommerce

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-agent
  namespace: ecommerce
spec:
  selector:
    matchLabels:
      app: monitoring-agent
  template:
    metadata:
      labels:
        app: monitoring-agent
    spec:
      serviceAccountName: monitoring-sa
      containers:
        - name: monitoring
          image: busybox
          command: ['/bin/sh']
          args:
            [
              '-c',
              "while true; do echo '[MONITOR] App Status:' $(date); sleep 60; done"
            ]
          resources:
            requests:
              memory: '32Mi'
              cpu: '10m'
            limits:
              memory: '64Mi'
              cpu: '50m'

---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: health-check-job
  namespace: ecommerce
spec:
  schedule: '*/5 * * * *' # Toutes les 5 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: health-checker
              image: curlimages/curl:latest
              command: ['/bin/sh']
              args:
                [
                  '-c',
                  'curl -f http://frontend-service/health && curl -f http://backend-service:3000/health'
                ]
          restartPolicy: OnFailure
```

### 7. Déploiement et tests complets

```bash
# Générer le certificat TLS
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ecommerce-tls.key \
  -out ecommerce-tls.crt \
  -subj "/CN=ecommerce.local/O=ecommerce"

# Créer le secret TLS
kubectl create secret tls ecommerce-tls-secret \
  --cert=ecommerce-tls.crt \
  --key=ecommerce-tls.key \
  --namespace=ecommerce

# Déployer l'application complète
kubectl apply -f ecommerce-config.yaml
kubectl apply -f database.yaml
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f ingress.yaml
kubectl apply -f monitoring.yaml

# Ajouter l'entrée DNS locale
echo "$(minikube ip) ecommerce.local" | sudo tee -a /etc/hosts

# Attendre que tous les services soient prêts
kubectl wait --for=condition=ready pod -l app=postgres -n ecommerce --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend -n ecommerce --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n ecommerce --timeout=300s

# Vérifier le déploiement
kubectl get all -n ecommerce
kubectl get ingress -n ecommerce

# Tests d'intégration
echo "=== TESTS D'INTEGRATION ==="

# Test du frontend
echo "1. Test frontend..."
curl -k https://ecommerce.local

# Test de l'API backend
echo "2. Test backend API..."
curl -k https://ecommerce.local/api/v1/products

# Test de la base de données (via backend)
echo "3. Test connectivité base de données..."
kubectl exec -n ecommerce -it statefulset/postgres -- psql -U postgres -d ecommerce_db -c "SELECT COUNT(*) FROM products;"

# Test des health checks
echo "4. Test health checks..."
kubectl exec -n ecommerce -it deployment/frontend -- wget -qO- http://localhost/health
kubectl exec -n ecommerce -it deployment/backend -- wget -qO- http://localhost:3000/health

# Test de charge basique
echo "5. Test de charge basique..."
for i in {1..10}; do
  curl -s -k https://ecommerce.local > /dev/null && echo "Request $i: OK" || echo "Request $i: FAILED"
done

# Vérifier les métriques
echo "6. Métriques des ressources..."
kubectl top pods -n ecommerce

echo "=== ARCHITECTURE DEPLOYEE ==="
kubectl get pods,svc,ingress -n ecommerce -o wide
```

### 8. Simulation de pannes et récupération

```bash
# Test de résilience
echo "=== TESTS DE RESILIENCE ==="

# Simuler la panne d'un pod frontend
kubectl delete pod -n ecommerce -l app=frontend --force --grace-period=0
echo "Pod frontend supprimé, vérification de la récupération..."
sleep 10
kubectl get pods -n ecommerce -l app=frontend

# Simuler la panne du backend
kubectl scale deployment backend -n ecommerce --replicas=0
echo "Backend arrêté, test de l'impact sur le frontend..."
curl -k https://ecommerce.local
sleep 5
kubectl scale deployment backend -n ecommerce --replicas=2
echo "Backend redémarré, attente de la récupération..."
kubectl wait --for=condition=ready pod -l app=backend -n ecommerce --timeout=120s

# Test de persistence après redémarrage de la base
kubectl delete pod -n ecommerce -l app=postgres --force --grace-period=0
echo "Base de données redémarrée, vérification de la persistence..."
kubectl wait --for=condition=ready pod -l app=postgres -n ecommerce --timeout=300s
kubectl exec -n ecommerce -it statefulset/postgres -- psql -U postgres -d ecommerce_db -c "SELECT name FROM products LIMIT 3;"
```

## Livrables attendus

1. Application 3-tiers complètement déployée et fonctionnelle
2. Certificat TLS et exposition sécurisée via Ingress
3. Persistance des données validée
4. Monitoring et health checks opérationnels
5. Tests de résilience et récupération documentés
6. Architecture et choix techniques justifiés

## Critères de validation

- [ ] Namespace ecommerce créé avec tous les objets
- [ ] Base PostgreSQL avec données persistantes
- [ ] API backend exposant des endpoints fonctionnels
- [ ] Frontend web accessible via HTTPS
- [ ] Ingress avec routage et TLS configuré
- [ ] Health checks et monitoring déployés
- [ ] Résilience testée (redémarrage pods, scaling)
- [ ] Architecture 3-tiers complète et sécurisée

## Durée estimée

60 minutes

## Points d'excellence

### Architecture production-ready

- Séparation des couches (frontend/backend/database)
- Configuration externalisée (ConfigMaps/Secrets)
- Persistance des données (StatefulSet + PVC)
- Sécurité (TLS, secrets, resource limits)

### Observabilité complète

- Health checks sur tous les composants
- Monitoring avec métriques
- Logs structurés et accessibles
- Alerting automatisé

### Résilience et haute disponibilité

- Replicas multiples pour frontend/backend
- Rolling updates sans interruption
- Récupération automatique des pannes
- Load balancing intégré

Félicitations ! Vous avez déployé une application Kubernetes complète en production ! 🎉
