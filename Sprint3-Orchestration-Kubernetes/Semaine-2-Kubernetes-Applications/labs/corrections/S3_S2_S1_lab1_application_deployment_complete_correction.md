# Correction - LAB 1 : Application Deployment complète

## Solution complète

### Étape 1 : Namespace et ConfigMap

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ecommerce

---
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: ecommerce
data:
  DATABASE_URL: 'postgresql://ecommerce:password@postgres-service:5432/ecommerce'
  REDIS_URL: 'redis://redis-service:6379'
  NODE_ENV: 'production'
  API_PORT: '3000'
  FRONTEND_PORT: '80'
```

### Étape 2 : PostgreSQL avec persistance

```yaml
# postgres-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: ecommerce
type: Opaque
data:
  username: ZWNvbW1lcmNl # ecommerce
  password: cGFzc3dvcmQ= # password

---
# postgres-pvc.yaml
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
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:13
          env:
            - name: POSTGRES_DB
              value: ecommerce
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
          ports:
            - containerPort: 5432
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
                - ecommerce
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - ecommerce
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc

---
# postgres-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: ecommerce
spec:
  selector:
    app: postgres
  ports:
    - protocol: TCP
      port: 5432
      targetPort: 5432
```

### Étape 3 : Redis pour cache

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:6-alpine
          ports:
            - containerPort: 6379
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
# redis-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: ecommerce
spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
```

### Étape 4 : API Backend Node.js

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-backend
  namespace: ecommerce
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-backend
  template:
    metadata:
      labels:
        app: api-backend
    spec:
      containers:
        - name: api
          image: node:16-alpine
          command:
            - /bin/sh
            - -c
            - |
              npm install express pg redis
              cat > server.js << 'EOF'
              const express = require('express');
              const { Pool } = require('pg');
              const redis = require('redis');

              const app = express();
              const port = process.env.API_PORT || 3000;

              // Database connection
              const pool = new Pool({
                connectionString: process.env.DATABASE_URL
              });

              // Redis connection
              const redisClient = redis.createClient({
                url: process.env.REDIS_URL
              });

              app.use(express.json());

              // Health check
              app.get('/health', async (req, res) => {
                try {
                  await pool.query('SELECT 1');
                  await redisClient.ping();
                  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
                } catch (error) {
                  res.status(500).json({ status: 'unhealthy', error: error.message });
                }
              });

              // Ready check
              app.get('/ready', async (req, res) => {
                res.json({ status: 'ready' });
              });

              // API endpoints
              app.get('/api/v1/products', async (req, res) => {
                try {
                  const result = await pool.query('SELECT * FROM products LIMIT 10');
                  res.json({ products: result.rows });
                } catch (error) {
                  res.status(500).json({ error: error.message });
                }
              });

              app.listen(port, () => {
                console.log(`API server running on port ${port}`);
              });
              EOF
              node server.js
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
            - name: NODE_ENV
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: NODE_ENV
            - name: API_PORT
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: API_PORT
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
          startupProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
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

---
# api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: ecommerce
spec:
  selector:
    app: api-backend
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
```

### Étape 5 : Frontend React avec nginx

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: ecommerce
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/conf.d
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
      volumes:
        - name: nginx-config
          configMap:
            name: nginx-config

---
# nginx-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;
        
        location / {
            try_files $uri $uri/ /index.html;
        }
        
        location /api {
            proxy_pass http://api-service:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        location /health {
            access_log off;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
    }

---
# frontend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: ecommerce
spec:
  selector:
    app: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

## Commandes de déploiement

```bash
# Déployer tous les composants
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
kubectl apply -f nginx-configmap.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

# Vérifier le déploiement
kubectl get all -n ecommerce
kubectl get pvc -n ecommerce
```

## Tests de validation

```bash
# Vérifier l'état des pods
kubectl get pods -n ecommerce

# Tester la connectivité API
kubectl port-forward -n ecommerce svc/api-service 3000:3000
curl http://localhost:3000/health

# Tester le frontend
kubectl port-forward -n ecommerce svc/frontend-service 8080:80
curl http://localhost:8080

# Vérifier les logs
kubectl logs -n ecommerce -l app=api-backend
kubectl logs -n ecommerce -l app=frontend
```

## Bonnes pratiques mises en place

1. **Séparation des environnements** avec namespace dédié
2. **Configuration externalisée** avec ConfigMaps
3. **Secrets sécurisés** pour credentials
4. **Persistance des données** avec PVC
5. **Health checks complets** (startup, liveness, readiness)
6. **Resource limits** pour tous les conteneurs
7. **Communication inter-services** via Services ClusterIP
8. **Haute disponibilité** avec replicas multiples

## Points d'amélioration possibles

- Ajouter NetworkPolicies pour isolation réseau
- Implémenter backup automatique de PostgreSQL
- Ajouter monitoring avec Prometheus
- Configurer autoscaling (HPA)
- Implémenter circuit breaker dans l'API
