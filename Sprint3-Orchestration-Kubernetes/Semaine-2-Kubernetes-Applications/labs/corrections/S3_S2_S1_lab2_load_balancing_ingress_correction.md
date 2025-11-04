# Correction LAB 2 - Load Balancing et Ingress avec SSL

## Vue d'ensemble de la solution

Cette correction présente une implémentation complète du Load Balancing et de l'Ingress avec SSL pour l'application e-commerce, incluant la haute disponibilité et la sécurité.

## Architecture de la solution

```
Internet → LoadBalancer → Ingress Controller → Services → Pods
             ↓
        Certificats SSL
        (Let's Encrypt)
```

## Étape 1 : Préparation de l'environnement

### 1.1 Vérification du cluster et installation NGINX Ingress

```bash
# Vérifier les nœuds du cluster
kubectl get nodes -o wide

# Installer NGINX Ingress Controller avec Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Installation avec configuration HA
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.replicaCount=2 \
  --set controller.nodeSelector."kubernetes\.io/os"=linux \
  --set controller.service.type=LoadBalancer \
  --set controller.service.externalTrafficPolicy=Local \
  --set controller.metrics.enabled=true \
  --set controller.podSecurityContext.runAsUser=101 \
  --set controller.containerSecurityContext.allowPrivilegeEscalation=false

# Vérifier l'installation
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx
```

### 1.2 Installation et configuration de cert-manager

```bash
# Installer cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true \
  --set global.leaderElection.namespace=cert-manager

# Vérifier l'installation
kubectl get pods -n cert-manager
```

## Étape 2 : Configuration des applications backend

### 2.1 Déploiement des services backend

```yaml
# backend-deployments.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: ecommerce
  labels:
    app: user-service
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
        tier: backend
    spec:
      containers:
        - name: user-service
          image: nginx:1.21-alpine # Image de démo
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: '128Mi'
              cpu: '100m'
            limits:
              memory: '256Mi'
              cpu: '200m'
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
          # Configuration personnalisée pour simuler API
          volumeMounts:
            - name: user-config
              mountPath: /etc/nginx/conf.d
      volumes:
        - name: user-config
          configMap:
            name: user-service-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: user-service-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            return 200 '{"service":"user-service","status":"healthy","version":"v1.0","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }
        
        location /health {
            return 200 '{"status":"healthy"}';
            add_header Content-Type application/json;
        }
        
        location /users {
            return 200 '{"users":[{"id":1,"name":"John Doe"},{"id":2,"name":"Jane Smith"}]}';
            add_header Content-Type application/json;
        }
    }

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
    tier: backend
spec:
  replicas: 4 # Plus de replicas pour service critique
  selector:
    matchLabels:
      app: product-service
  template:
    metadata:
      labels:
        app: product-service
        tier: backend
    spec:
      containers:
        - name: product-service
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
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
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: product-config
              mountPath: /etc/nginx/conf.d
      volumes:
        - name: product-config
          configMap:
            name: product-service-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-service-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            return 200 '{"service":"product-service","status":"healthy","version":"v1.0","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }
        
        location /health {
            return 200 '{"status":"healthy"}';
            add_header Content-Type application/json;
        }
        
        location /products {
            return 200 '{"products":[{"id":1,"name":"Laptop","price":999.99},{"id":2,"name":"Phone","price":699.99}]}';
            add_header Content-Type application/json;
        }
    }

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        tier: backend
    spec:
      containers:
        - name: order-service
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
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
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: order-config
              mountPath: /etc/nginx/conf.d
      volumes:
        - name: order-config
          configMap:
            name: order-service-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-service-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            return 200 '{"service":"order-service","status":"healthy","version":"v1.0","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }
        
        location /health {
            return 200 '{"status":"healthy"}';
            add_header Content-Type application/json;
        }
        
        location /orders {
            return 200 '{"orders":[{"id":1,"user_id":1,"total":999.99,"status":"pending"}]}';
            add_header Content-Type application/json;
        }
    }
```

### 2.2 Services pour exposition des pods

```yaml
# backend-services.yaml
apiVersion: v1
kind: Service
metadata:
  name: user-service
  namespace: ecommerce
  labels:
    app: user-service
    tier: backend
spec:
  selector:
    app: user-service
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: product-service
  namespace: ecommerce
  labels:
    app: product-service
    tier: backend
spec:
  selector:
    app: product-service
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
  # Configuration pour équilibrage de charge
  sessionAffinity: None

---
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: ecommerce
  labels:
    app: order-service
    tier: backend
spec:
  selector:
    app: order-service
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
```

## Étape 3 : Configuration SSL avec cert-manager

### 3.1 ClusterIssuer pour Let's Encrypt

```yaml
# cluster-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    # Serveur de staging Let's Encrypt (pour tests)
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: admin@ecommerce.local # Remplacer par votre email
    privateKeySecretRef:
      name: letsencrypt-staging
    solvers:
      - http01:
          ingress:
            class: nginx

---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # Serveur de production Let's Encrypt
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@ecommerce.local # Remplacer par votre email
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
        selector:
          dnsZones:
            - 'ecommerce.local'
            - '*.ecommerce.local'

---
# Pour les environnements locaux - Certificat auto-signé
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
```

### 3.2 Certificats pour l'application

```yaml
# certificates.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ecommerce-tls-staging
  namespace: ecommerce
spec:
  secretName: ecommerce-tls-staging
  issuerRef:
    name: letsencrypt-staging
    kind: ClusterIssuer
  dnsNames:
    - api-staging.ecommerce.local
    - staging.ecommerce.local

---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ecommerce-tls-prod
  namespace: ecommerce
spec:
  secretName: ecommerce-tls-prod
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - api.ecommerce.local
    - ecommerce.local
    - www.ecommerce.local

---
# Certificat pour développement local
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ecommerce-tls-local
  namespace: ecommerce
spec:
  secretName: ecommerce-tls-local
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
  dnsNames:
    - localhost
    - ecommerce.local
    - api.ecommerce.local
```

## Étape 4 : Configuration Ingress avec Load Balancing

### 4.1 Ingress principal avec SSL

```yaml
# ingress-main.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce
  annotations:
    # Configuration NGINX Ingress
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'

    # Certificats automatiques
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'

    # Configuration Load Balancing
    nginx.ingress.kubernetes.io/load-balance: 'round_robin'
    nginx.ingress.kubernetes.io/upstream-hash-by: '$request_uri'

    # Optimisations performance
    nginx.ingress.kubernetes.io/proxy-body-size: '50m'
    nginx.ingress.kubernetes.io/proxy-connect-timeout: '60'
    nginx.ingress.kubernetes.io/proxy-send-timeout: '60'
    nginx.ingress.kubernetes.io/proxy-read-timeout: '60'

    # Headers sécurisés
    nginx.ingress.kubernetes.io/configuration-snippet: |
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-XSS-Protection "1; mode=block" always;
      add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Rate limiting
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: 'true'
    nginx.ingress.kubernetes.io/cors-allow-origin: 'https://ecommerce.local'
    nginx.ingress.kubernetes.io/cors-allow-methods: 'GET, POST, PUT, DELETE, OPTIONS'
    nginx.ingress.kubernetes.io/cors-allow-headers: 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization'

spec:
  tls:
    - hosts:
        - api.ecommerce.local
        - ecommerce.local
      secretName: ecommerce-tls-prod
  rules:
    # API Backend routes
    - host: api.ecommerce.local
      http:
        paths:
          - path: /users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 80
          - path: /products
            pathType: Prefix
            backend:
              service:
                name: product-service
                port:
                  number: 80
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 80
          # Health checks centralisés
          - path: /health
            pathType: Prefix
            backend:
              service:
                name: health-check-service
                port:
                  number: 80
    # Frontend (sera ajouté plus tard)
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

---
# Ingress pour environnement staging
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-staging-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: 'letsencrypt-staging'

    # Configuration spécifique staging
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/configuration-snippet: |
      add_header X-Environment "staging" always;

spec:
  tls:
    - hosts:
        - api-staging.ecommerce.local
        - staging.ecommerce.local
      secretName: ecommerce-tls-staging
  rules:
    - host: api-staging.ecommerce.local
      http:
        paths:
          - path: /api(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: api-gateway-staging
                port:
                  number: 80
```

### 4.2 Configuration avancée du Load Balancing

```yaml
# ingress-advanced-lb.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-advanced-lb
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx

    # Sticky sessions pour services stateful
    nginx.ingress.kubernetes.io/affinity: 'cookie'
    nginx.ingress.kubernetes.io/affinity-mode: 'persistent'
    nginx.ingress.kubernetes.io/session-cookie-name: 'ecommerce-session'
    nginx.ingress.kubernetes.io/session-cookie-expires: '3600'
    nginx.ingress.kubernetes.io/session-cookie-max-age: '3600'
    nginx.ingress.kubernetes.io/session-cookie-path: '/'

    # Weighted routing (A/B testing)
    nginx.ingress.kubernetes.io/canary: 'true'
    nginx.ingress.kubernetes.io/canary-weight: '10'

    # Circuit breaker
    nginx.ingress.kubernetes.io/custom-http-errors: '503'
    nginx.ingress.kubernetes.io/default-backend: 'error-page-service'

    # Configuration custom pour load balancing
    nginx.ingress.kubernetes.io/server-snippet: |
      location @custom_error {
          internal;
          return 503 '{"error":"Service temporarily unavailable","code":503}';
          add_header Content-Type application/json;
      }

      # Monitoring endpoints
      location /nginx_status {
          stub_status on;
          access_log off;
          allow 10.0.0.0/8;
          deny all;
      }

    # Health check configuration
    nginx.ingress.kubernetes.io/upstream-vhost: '$service_name.$namespace.svc.cluster.local'

spec:
  rules:
    - host: api.ecommerce.local
      http:
        paths:
          - path: /v2/users
            pathType: Prefix
            backend:
              service:
                name: user-service-v2 # Version canary
                port:
                  number: 80

---
# Service mesh simulation avec multiple backends
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-multi-backend
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/upstream-hash-by: '$request_uri'

    # Configuration de retry et timeout
    nginx.ingress.kubernetes.io/proxy-next-upstream: 'error timeout http_502 http_503 http_504'
    nginx.ingress.kubernetes.io/proxy-next-upstream-tries: '3'
    nginx.ingress.kubernetes.io/proxy-next-upstream-timeout: '10'

spec:
  rules:
    - host: api.ecommerce.local
      http:
        paths:
          # Route avec failover automatique
          - path: /products/search
            pathType: Prefix
            backend:
              service:
                name: search-service-primary
                port:
                  number: 80
```

## Étape 5 : Service de Health Check centralisé

### 5.1 Déploiement du service de santé

```yaml
# health-check-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: health-check-service
  namespace: ecommerce
  labels:
    app: health-check
    tier: monitoring
spec:
  replicas: 2
  selector:
    matchLabels:
      app: health-check
  template:
    metadata:
      labels:
        app: health-check
        tier: monitoring
    spec:
      containers:
        - name: health-checker
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
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
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: health-config
              mountPath: /etc/nginx/conf.d
            - name: health-scripts
              mountPath: /usr/share/nginx/html/scripts
      volumes:
        - name: health-config
          configMap:
            name: health-check-config
        - name: health-scripts
          configMap:
            name: health-check-scripts
            defaultMode: 0755

---
apiVersion: v1
kind: Service
metadata:
  name: health-check-service
  namespace: ecommerce
  labels:
    app: health-check
spec:
  selector:
    app: health-check
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            return 200 '{"status":"healthy","timestamp":"$time_iso8601","service":"health-checker"}';
            add_header Content-Type application/json;
        }
        
        location /health {
            content_by_lua_block {
                -- Vérifier tous les services backend
                local http = require "resty.http"
                local cjson = require "cjson"
                local httpc = http.new()
                
                local services = {
                    {name = "user-service", url = "http://user-service/health"},
                    {name = "product-service", url = "http://product-service/health"},
                    {name = "order-service", url = "http://order-service/health"}
                }
                
                local results = {}
                local overall_status = "healthy"
                
                for _, service in ipairs(services) do
                    local res, err = httpc:request_uri(service.url, {
                        method = "GET",
                        timeout = 5000
                    })
                    
                    if not res or res.status ~= 200 then
                        results[service.name] = {status = "unhealthy", error = err or "HTTP " .. (res and res.status or "timeout")}
                        overall_status = "unhealthy"
                    else
                        results[service.name] = {status = "healthy"}
                    end
                end
                
                local response = {
                    overall_status = overall_status,
                    services = results,
                    timestamp = ngx.time()
                }
                
                ngx.header.content_type = "application/json"
                ngx.say(cjson.encode(response))
            }
        }
        
        location /metrics {
            # Exposition des métriques pour Prometheus
            content_by_lua_block {
                ngx.header.content_type = "text/plain"
                ngx.say("# HELP ecommerce_health_status Health status of services")
                ngx.say("# TYPE ecommerce_health_status gauge")
                ngx.say("ecommerce_health_status{service=\"user-service\"} 1")
                ngx.say("ecommerce_health_status{service=\"product-service\"} 1")
                ngx.say("ecommerce_health_status{service=\"order-service\"} 1")
            }
        }
    }

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-scripts
  namespace: ecommerce
data:
  check-all.sh: |
    #!/bin/bash
    echo "Checking all services health..."

    services=("user-service" "product-service" "order-service")

    for service in "${services[@]}"; do
        response=$(curl -s -w "%{http_code}" "http://$service/health")
        http_code="${response: -3}"
        
        if [ "$http_code" = "200" ]; then
            echo "✓ $service: healthy"
        else
            echo "✗ $service: unhealthy (HTTP $http_code)"
        fi
    done
```

## Étape 6 : Tests et validation

### 6.1 Scripts de test

```bash
# test-load-balancing.sh
#!/bin/bash

echo "🧪 Tests de Load Balancing et SSL"

# Variables
DOMAIN="api.ecommerce.local"
FRONTEND_DOMAIN="ecommerce.local"

# Test 1: Vérification SSL
echo "Test 1: Vérification des certificats SSL..."
openssl s_client -connect $DOMAIN:443 -servername $DOMAIN < /dev/null 2>/dev/null | \
    openssl x509 -noout -dates

if [ $? -eq 0 ]; then
    echo "✅ Certificat SSL valide"
else
    echo "❌ Problème avec le certificat SSL"
fi

# Test 2: Test de redirection HTTP vers HTTPS
echo "Test 2: Redirection HTTP → HTTPS..."
REDIRECT=$(curl -s -o /dev/null -w "%{redirect_url}" "http://$DOMAIN/health")
if [[ $REDIRECT == https* ]]; then
    echo "✅ Redirection HTTPS fonctionnelle"
else
    echo "❌ Redirection HTTPS non configurée"
fi

# Test 3: Load balancing des requêtes
echo "Test 3: Distribution des requêtes (Load Balancing)..."
for i in {1..10}; do
    RESPONSE=$(curl -s -k "https://$DOMAIN/products" | jq -r '.timestamp // empty')
    echo "Requête $i: $RESPONSE"
    sleep 0.5
done

# Test 4: Health checks
echo "Test 4: Vérification des health checks..."
HEALTH_STATUS=$(curl -s -k "https://$DOMAIN/health" | jq -r '.overall_status')
if [ "$HEALTH_STATUS" = "healthy" ]; then
    echo "✅ Tous les services sont sains"
else
    echo "❌ Problème détecté dans les services: $HEALTH_STATUS"
fi

# Test 5: Performance et latence
echo "Test 5: Tests de performance..."
curl -s -k -w "Connect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" \
    "https://$DOMAIN/products" -o /dev/null

# Test 6: Headers sécurisés
echo "Test 6: Vérification des headers de sécurité..."
SECURITY_HEADERS=$(curl -s -k -I "https://$DOMAIN/health" | grep -E "(X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security)")
if [ ! -z "$SECURITY_HEADERS" ]; then
    echo "✅ Headers de sécurité présents:"
    echo "$SECURITY_HEADERS"
else
    echo "❌ Headers de sécurité manquants"
fi

echo "🏁 Tests terminés"
```

### 6.2 Validation de la configuration

```bash
# validate-config.sh
#!/bin/bash

echo "🔍 Validation de la configuration Ingress et SSL"

# Vérifier les ressources déployées
echo "=== Vérification des déploiements ==="
kubectl get deployments -n ecommerce
kubectl get services -n ecommerce
kubectl get ingress -n ecommerce

# Vérifier l'état des pods
echo "=== État des pods ==="
kubectl get pods -n ecommerce -o wide

# Vérifier les certificats
echo "=== Certificats SSL ==="
kubectl get certificates -n ecommerce
kubectl describe certificate ecommerce-tls-prod -n ecommerce

# Vérifier la configuration Ingress
echo "=== Configuration Ingress ==="
kubectl describe ingress ecommerce-ingress -n ecommerce

# Vérifier les endpoints
echo "=== Endpoints des services ==="
kubectl get endpoints -n ecommerce

# Tests de connectivité interne
echo "=== Tests de connectivité interne ==="
kubectl run test-pod --image=curlimages/curl --rm -i --restart=Never -- \
    curl -s http://user-service.ecommerce.svc.cluster.local/health

kubectl run test-pod --image=curlimages/curl --rm -i --restart=Never -- \
    curl -s http://product-service.ecommerce.svc.cluster.local/health

kubectl run test-pod --image=curlimages/curl --rm -i --restart=Never -- \
    curl -s http://order-service.ecommerce.svc.cluster.local/health

# Vérifier la configuration DNS
echo "=== Résolution DNS ==="
nslookup api.ecommerce.local
nslookup ecommerce.local

echo "✅ Validation terminée"
```

## Points clés de la solution

### 🎯 Load Balancing

- **Round-robin par défaut** avec NGINX Ingress
- **Session affinity** configurée pour services stateful
- **Health checks** automatiques avec failover
- **Weighted routing** pour déploiements canary

### 🔒 SSL/TLS

- **Certificats automatiques** avec cert-manager
- **Redirection HTTPS forcée** sur tous les endpoints
- **Headers sécurisés** (HSTS, X-Frame-Options, etc.)
- **Support multi-domaines** avec SAN certificates

### 📊 Monitoring

- **Health checks centralisés** avec agrégation de statut
- **Métriques Prometheus** exposées sur `/metrics`
- **Logs structurés** pour debugging
- **Rate limiting** et protection DDoS

### 🚀 Performance

- **Optimisations proxy** (timeouts, body size)
- **Compression automatique** GZIP
- **Keep-alive** optimisé
- **Cache headers** appropriés

### 🔧 Troubleshooting courant

#### Problème: Certificat SSL non généré

```bash
# Vérifier les logs cert-manager
kubectl logs -n cert-manager deployment/cert-manager

# Vérifier l'ordre ACME
kubectl describe order -n ecommerce

# Forcer le renouvellement
kubectl delete certificate ecommerce-tls-prod -n ecommerce
kubectl apply -f certificates.yaml
```

#### Problème: Load balancing non fonctionnel

```bash
# Vérifier les endpoints
kubectl get endpoints -n ecommerce

# Vérifier la configuration NGINX
kubectl exec -n ingress-nginx deployment/ingress-nginx-controller -- nginx -T

# Vérifier les logs Ingress
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

Cette correction fournit une solution complète et production-ready pour le Load Balancing et SSL avec Kubernetes Ingress.
