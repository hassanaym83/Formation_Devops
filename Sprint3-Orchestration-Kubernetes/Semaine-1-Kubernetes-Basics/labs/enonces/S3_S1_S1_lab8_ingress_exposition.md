# LAB 8 - Ingress et exposition externe

## Objectifs

- Maîtriser l'exposition d'applications avec Ingress
- Configurer le routage HTTP/HTTPS
- Implémenter la terminaison SSL/TLS
- Gérer les règles de routage avancées

## Contexte

Exposition sécurisée et routage intelligent des applications web vers l'extérieur du cluster.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des Services
- Ingress Controller installé

## Instructions

### 1. Installation et configuration de l'Ingress Controller

```bash
# Activer l'addon ingress dans minikube
minikube addons enable ingress

# Vérifier l'installation de l'Ingress Controller
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

# Obtenir l'IP du cluster pour les tests
minikube ip
```

### 2. Déploiement des applications de test

```yaml
# Créer le fichier test-applications.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
      version: v1
  template:
    metadata:
      labels:
        app: webapp
        version: v1
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          ports:
            - containerPort: 80
          volumeMounts:
            - name: webapp-content
              mountPath: /usr/share/nginx/html
      volumes:
        - name: webapp-content
          configMap:
            name: webapp-v1-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-v1-config
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>WebApp V1</title></head>
    <body>
      <h1>WebApp Version 1</h1>
      <p>Served from: webapp-v1</p>
      <p>Time: <span id="time"></span></p>
      <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
      </script>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: webapp-v1-service
spec:
  selector:
    app: webapp
    version: v1
  ports:
    - port: 80
      targetPort: 80

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-v2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
      version: v2
  template:
    metadata:
      labels:
        app: webapp
        version: v2
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          ports:
            - containerPort: 80
          volumeMounts:
            - name: webapp-content
              mountPath: /usr/share/nginx/html
      volumes:
        - name: webapp-content
          configMap:
            name: webapp-v2-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-v2-config
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>WebApp V2</title></head>
    <body style="background-color: #f0f0f0;">
      <h1>WebApp Version 2</h1>
      <p>Served from: webapp-v2</p>
      <p>Time: <span id="time"></span></p>
      <p>New features available!</p>
      <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
      </script>
    </body>
    </html>

---
apiVersion: v1
kind: Service
metadata:
  name: webapp-v2-service
spec:
  selector:
    app: webapp
    version: v2
  ports:
    - port: 80
      targetPort: 80

---
# API Backend
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-backend
spec:
  replicas: 1
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
          image: nginx:1.21
          ports:
            - containerPort: 80
          volumeMounts:
            - name: api-content
              mountPath: /usr/share/nginx/html
      volumes:
        - name: api-content
          configMap:
            name: api-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  index.html: |
    {
      "service": "API Backend",
      "version": "1.0",
      "endpoints": [
        "/users",
        "/products", 
        "/orders"
      ],
      "status": "healthy"
    }

---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api-backend
  ports:
    - port: 80
      targetPort: 80
```

```bash
# Déployer les applications
kubectl apply -f test-applications.yaml

# Vérifier les déploiements
kubectl get deployments
kubectl get services
kubectl get pods
```

### 3. Ingress basique - routage par chemin

```yaml
# Créer le fichier ingress-path-routing.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: webapp.local
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: webapp-v1-service
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: webapp-v2-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

```bash
# Appliquer l'Ingress
kubectl apply -f ingress-path-routing.yaml

# Vérifier l'Ingress
kubectl get ingress
kubectl describe ingress webapp-ingress

# Ajouter l'entrée DNS locale (remplacer <MINIKUBE-IP>)
echo "$(minikube ip) webapp.local" | sudo tee -a /etc/hosts

# Tester les différents chemins
curl http://webapp.local/v1
curl http://webapp.local/v2
curl http://webapp.local/api
```

### 4. Ingress avec routage par host

```yaml
# Créer le fichier ingress-host-routing.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-host-ingress
spec:
  rules:
    - host: v1.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-v1-service
                port:
                  number: 80
    - host: v2.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-v2-service
                port:
                  number: 80
    - host: api.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

```bash
# Appliquer l'Ingress multi-host
kubectl apply -f ingress-host-routing.yaml

# Ajouter les entrées DNS
echo "$(minikube ip) v1.webapp.local" | sudo tee -a /etc/hosts
echo "$(minikube ip) v2.webapp.local" | sudo tee -a /etc/hosts
echo "$(minikube ip) api.webapp.local" | sudo tee -a /etc/hosts

# Tester les différents hosts
curl http://v1.webapp.local
curl http://v2.webapp.local
curl http://api.webapp.local
```

### 5. Configuration HTTPS avec TLS

```bash
# Générer certificat auto-signé pour webapp.local
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout webapp-tls.key \
  -out webapp-tls.crt \
  -subj "/CN=webapp.local/O=webapp" \
  -addext "subjectAltName=DNS:webapp.local,DNS:v1.webapp.local,DNS:v2.webapp.local,DNS:api.webapp.local"

# Créer le secret TLS
kubectl create secret tls webapp-tls-secret \
  --cert=webapp-tls.crt \
  --key=webapp-tls.key
```

```yaml
# Créer le fichier ingress-tls.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-tls-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
spec:
  tls:
    - hosts:
        - webapp.local
        - v1.webapp.local
        - v2.webapp.local
        - api.webapp.local
      secretName: webapp-tls-secret
  rules:
    - host: webapp.local
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service:
                name: webapp-v1-service
                port:
                  number: 80
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: webapp-v2-service
                port:
                  number: 80
    - host: v1.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-v1-service
                port:
                  number: 80
    - host: api.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

```bash
# Appliquer l'Ingress TLS
kubectl apply -f ingress-tls.yaml

# Tester HTTPS (accepter le certificat auto-signé)
curl -k https://webapp.local/v1
curl -k https://v1.webapp.local
curl -k https://api.webapp.local

# Vérifier la redirection HTTP vers HTTPS
curl -I http://webapp.local/v1
```

### 6. Annotations avancées et règles de routage

```yaml
# Créer le fichier ingress-advanced.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: advanced-ingress
  annotations:
    # Réécritures d'URL
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    # Limite de taille pour uploads
    nginx.ingress.kubernetes.io/proxy-body-size: '10m'
    # Timeout personnalisés
    nginx.ingress.kubernetes.io/proxy-read-timeout: '300'
    nginx.ingress.kubernetes.io/proxy-send-timeout: '300'
    # CORS
    nginx.ingress.kubernetes.io/enable-cors: 'true'
    nginx.ingress.kubernetes.io/cors-allow-origin: '*'
    # Rate limiting
    nginx.ingress.kubernetes.io/rate-limit: '100'
    # Authentification basique
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth-secret
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required'
spec:
  tls:
    - hosts:
        - advanced.webapp.local
      secretName: webapp-tls-secret
  rules:
    - host: advanced.webapp.local
      http:
        paths:
          # Routage avec capture de groupes pour réécriture
          - path: /app(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: webapp-v2-service
                port:
                  number: 80
          # API avec authentification
          - path: /secure-api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

```bash
# Créer le secret pour l'authentification basique
htpasswd -c auth admin
kubectl create secret generic basic-auth-secret --from-file=auth

# Ajouter l'entrée DNS
echo "$(minikube ip) advanced.webapp.local" | sudo tee -a /etc/hosts

# Appliquer l'Ingress avancé
kubectl apply -f ingress-advanced.yaml

# Tester les différentes fonctionnalités
curl -k https://advanced.webapp.local/app/
curl -k -u admin:password https://advanced.webapp.local/secure-api
```

### 7. Load balancing et canary deployment

```yaml
# Créer le fichier ingress-canary.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-main
spec:
  rules:
    - host: canary.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-v1-service
                port:
                  number: 80

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: 'true'
    nginx.ingress.kubernetes.io/canary-weight: '20'
spec:
  rules:
    - host: canary.webapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: webapp-v2-service
                port:
                  number: 80
```

```bash
# Ajouter l'entrée DNS
echo "$(minikube ip) canary.webapp.local" | sudo tee -a /etc/hosts

# Appliquer le canary deployment
kubectl apply -f ingress-canary.yaml

# Tester la répartition (20% vers v2, 80% vers v1)
for i in {1..10}; do
  curl -s http://canary.webapp.local | grep "Version"
done
```

### 8. Monitoring et troubleshooting

```bash
# Vérifier l'état des Ingress
kubectl get ingress -A
kubectl describe ingress webapp-tls-ingress

# Logs de l'Ingress Controller
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Vérifier la configuration nginx générée
kubectl exec -n ingress-nginx -it <controller-pod> -- cat /etc/nginx/nginx.conf

# Debug avec verbose
curl -v -k https://webapp.local/v1

# Nettoyer les certificats
rm webapp-tls.key webapp-tls.crt auth
```

## Livrables attendus

1. Applications déployées avec Services
2. Ingress avec routage par chemin et par host
3. Configuration HTTPS/TLS fonctionnelle
4. Annotations avancées testées
5. Canary deployment implémenté

## Critères de validation

- [ ] Ingress Controller installé et fonctionnel
- [ ] Routage par chemins (/v1, /v2, /api) opérationnel
- [ ] Routage par hosts (v1.webapp.local, v2.webapp.local) opérationnel
- [ ] HTTPS avec certificats TLS configuré
- [ ] Annotations avancées (rate limiting, auth) testées
- [ ] Canary deployment avec répartition de trafic

## Durée estimée

40 minutes

## Concepts clés Ingress

### Types de routage

- **Path-based** : Routage par URL `/app1`, `/app2`
- **Host-based** : Routage par domaine `app1.com`, `app2.com`
- **Canary** : Répartition de trafic pour tests A/B

### Annotations utiles

```yaml
# Réécritures
nginx.ingress.kubernetes.io/rewrite-target: /
# Sécurité
nginx.ingress.kubernetes.io/ssl-redirect: 'true'
# Performance
nginx.ingress.kubernetes.io/proxy-body-size: '10m'
# Canary
nginx.ingress.kubernetes.io/canary: 'true'
nginx.ingress.kubernetes.io/canary-weight: '10'
```

### Commandes essentielles

```bash
# Gestion Ingress
kubectl get ingress
kubectl describe ingress <nom>
kubectl edit ingress <nom>

# Debug
kubectl logs -n ingress-nginx <controller-pod>
minikube addons enable ingress
```
