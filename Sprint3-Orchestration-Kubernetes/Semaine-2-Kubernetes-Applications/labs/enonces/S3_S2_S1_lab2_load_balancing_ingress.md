# LAB 2 - Load Balancing et Ingress avancé

## Objectif

Configurer un Ingress Controller avec load balancing avancé et SSL/TLS automatique.

## Contexte

Exposer l'application e-commerce du LAB 1 vers l'extérieur avec :

- SSL/TLS automatique via cert-manager
- Rate limiting pour protection DDoS
- Routage basé sur l'host et le path
- Monitoring des métriques Ingress

## Prérequis

- Application déployée du LAB 1
- Cluster Kubernetes avec Ingress Controller
- Nom de domaine configuré (ou simulation locale)

## Instructions détaillées

### Étape 1 : Installer NGINX Ingress Controller

1. Installer NGINX Ingress Controller :

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

2. Vérifier l'installation :

```bash
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx
```

### Étape 2 : Configurer cert-manager pour SSL automatique

3. Installer cert-manager :

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.11.0/cert-manager.yaml
```

4. Créer ClusterIssuer pour Let's Encrypt :

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx
```

### Étape 3 : Créer Ingress avec fonctionnalités avancées

5. Créer Ingress avec SSL, rate limiting et routage :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/rate-limit: '100'
    nginx.ingress.kubernetes.io/rate-limit-window: '1m'
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - ecommerce.example.com
        - api.ecommerce.example.com
      secretName: ecommerce-tls
  rules:
    - host: ecommerce.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
    - host: api.ecommerce.example.com
      http:
        paths:
          - path: /api/v1
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 3000
          - path: /health
            pathType: Exact
            backend:
              service:
                name: api-service
                port:
                  number: 3000
```

### Étape 4 : Configurer des policies avancées

6. Ajouter authentification basique pour l'admin :

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: admin-ingress
  namespace: ecommerce
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: admin-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - Admin'
spec:
  rules:
    - host: admin.ecommerce.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: admin-service
                port:
                  number: 80
```

### Étape 5 : Tester et monitorer

7. Créer script de test de load balancing
8. Vérifier la distribution du trafic
9. Tester le rate limiting avec Apache Bench
10. Vérifier les certificats SSL

## Critères de validation

- [ ] Ingress Controller installé et fonctionnel
- [ ] SSL/TLS configuré automatiquement
- [ ] Rate limiting actif et testé
- [ ] Routage host-based et path-based fonctionnel
- [ ] Load balancing distribue le trafic équitablement
- [ ] Métriques Ingress collectées

## Tests pratiques

```bash
# Test SSL
curl -I https://ecommerce.example.com

# Test rate limiting
ab -n 200 -c 10 https://ecommerce.example.com/

# Test routage API
curl https://api.ecommerce.example.com/api/v1/health
```

## Durée estimée

40 minutes
