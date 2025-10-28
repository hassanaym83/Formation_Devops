# LAB 6 - Secrets et sécurité

## Objectifs

- Maîtriser la gestion des données sensibles avec Secrets
- Comprendre les différents types de Secrets
- Implémenter les bonnes pratiques de sécurité
- Sécuriser les communications avec TLS

## Contexte

Gestion sécurisée des mots de passe, certificats et clés d'API dans un environnement Kubernetes.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des ConfigMaps

## Instructions

### 1. Créer des Secrets de différents types

```bash
# Secret générique avec des credentials
kubectl create secret generic database-credentials \
  --from-literal=username=admin \
  --from-literal=password=SuperSecretPassword123 \
  --from-literal=database=production_db

# Secret pour Docker registry
kubectl create secret docker-registry registry-credentials \
  --docker-server=registry.company.com \
  --docker-username=devops \
  --docker-password=MyRegistryPassword \
  --docker-email=devops@company.com

# Vérifier les secrets (attention : données encodées base64)
kubectl get secrets
kubectl describe secret database-credentials
kubectl get secret database-credentials -o yaml
```

### 2. Secret déclaratif avec YAML

```yaml
# Créer le fichier app-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  # Données encodées en base64
  # echo -n "postgres://admin:secret@db:5432/myapp" | base64
  database_url: cG9zdGdyZXM6Ly9hZG1pbjpzZWNyZXRAZGI6NTQzMi9teWFwcA==
  # echo -n "MySecretAPIKey123" | base64
  api_key: TXlTZWNyZXRBUElLZXkxMjM=
  # echo -n "jwt-secret-key-very-long" | base64
  jwt_secret: and0LXNlY3JldC1rZXktdmVyeS1sb25n

---
# Secret pour configuration SSH
apiVersion: v1
kind: Secret
metadata:
  name: ssh-key-secret
type: kubernetes.io/ssh-auth
data:
  # Clé privée SSH (base64 encoded)
  ssh-privatekey: |
    LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJGd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFRRUF0K3JWV1p6UFM4QU1qSytQMTBOcEN5YzJ2OFcyNU83UnJybUg3K2Y3V2lmbHNuVUVvClNTZ05IUW1sVWI4a001dCsrNThRK0Z3dHdtOEFBQUJCQkJCQkJCQkJCQkJCQkFBQUFBQUFBQUFBQUFBQUFBQUFBQUEKQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQpBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBCi0tLS0tRU5EIE9QRU5TU0ggUFJJVkFURSBLRVktLS0tLQo=
```

```bash
# Appliquer les secrets
kubectl apply -f app-secrets.yaml

# Décoder pour vérifier (attention en production!)
kubectl get secret app-secrets -o jsonpath="{.data.database_url}" | base64 -d
```

### 3. Utiliser les Secrets comme variables d'environnement

```yaml
# Créer le fichier deployment-with-secrets.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-secrets
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp-secrets
  template:
    metadata:
      labels:
        app: webapp-secrets
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          env:
            # Variable individuelle depuis Secret
            - name: DATABASE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: username
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: database-credentials
                  key: password
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: api_key
          # Toutes les clés d'un Secret
          envFrom:
            - secretRef:
                name: database-credentials
          ports:
            - containerPort: 80
```

```bash
# Déployer l'application
kubectl apply -f deployment-with-secrets.yaml

# Vérifier les variables (attention : données sensibles!)
kubectl exec -it deployment/webapp-with-secrets -- env | grep -E "(DATABASE|API)" | head -3
```

### 4. Monter les Secrets comme volumes

```yaml
# Créer le fichier deployment-secret-volumes.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-secret-volumes
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-volumes
  template:
    metadata:
      labels:
        app: webapp-volumes
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          volumeMounts:
            # Monter les credentials comme fichiers
            - name: database-creds
              mountPath: /etc/database
              readOnly: true
            # Monter la clé SSH
            - name: ssh-key
              mountPath: /etc/ssh-keys
              readOnly: true
            # Monter un secret spécifique avec mode de fichier
            - name: app-config
              mountPath: /etc/app/database_url
              subPath: database_url
              readOnly: true
          ports:
            - containerPort: 80
      volumes:
        - name: database-creds
          secret:
            secretName: database-credentials
            defaultMode: 0400 # Lecture seule pour le propriétaire
        - name: ssh-key
          secret:
            secretName: ssh-key-secret
            defaultMode: 0400
            items:
              - key: ssh-privatekey
                path: id_rsa
                mode: 0400
        - name: app-config
          secret:
            secretName: app-secrets
```

```bash
# Déployer avec volumes secrets
kubectl apply -f deployment-secret-volumes.yaml

# Vérifier les fichiers montés
kubectl exec -it deployment/webapp-secret-volumes -- ls -la /etc/database/
kubectl exec -it deployment/webapp-secret-volumes -- cat /etc/database/username
kubectl exec -it deployment/webapp-secret-volumes -- ls -la /etc/ssh-keys/
```

### 5. Secret TLS pour HTTPS

```bash
# Générer un certificat auto-signé pour test
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt \
  -subj "/CN=webapp.local/O=webapp"

# Créer le secret TLS
kubectl create secret tls webapp-tls-secret \
  --cert=tls.crt --key=tls.key

# Vérifier le secret TLS
kubectl describe secret webapp-tls-secret
```

```yaml
# Créer le fichier deployment-with-tls.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-tls
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-tls
  template:
    metadata:
      labels:
        app: webapp-tls
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          volumeMounts:
            - name: tls-certs
              mountPath: /etc/nginx/ssl
              readOnly: true
            - name: nginx-config
              mountPath: /etc/nginx/conf.d/default.conf
              subPath: default.conf
          ports:
            - containerPort: 80
            - containerPort: 443
      volumes:
        - name: tls-certs
          secret:
            secretName: webapp-tls-secret
        - name: nginx-config
          configMap:
            name: nginx-ssl-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-ssl-config
data:
  default.conf: |
    server {
        listen 80;
        listen 443 ssl;
        ssl_certificate /etc/nginx/ssl/tls.crt;
        ssl_certificate_key /etc/nginx/ssl/tls.key;
        
        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
```

### 6. Gestion des ServiceAccounts et RBAC

```yaml
# Créer le fichier service-account-secrets.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: webapp-service-account

---
apiVersion: v1
kind: Secret
metadata:
  name: webapp-sa-token
  annotations:
    kubernetes.io/service-account.name: webapp-service-account
type: kubernetes.io/service-account-token

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
  - apiGroups: ['']
    resources: ['secrets']
    verbs: ['get', 'list']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-secrets
subjects:
  - kind: ServiceAccount
    name: webapp-service-account
    namespace: default
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-sa
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-sa
  template:
    metadata:
      labels:
        app: webapp-sa
    spec:
      serviceAccountName: webapp-service-account
      containers:
        - name: webapp
          image: nginx:1.21
          ports:
            - containerPort: 80
```

### 7. Sécurité et bonnes pratiques

```bash
# Audit des secrets
kubectl get secrets --all-namespaces
kubectl get secrets -o json | jq '.items[].metadata.name'

# Vérifier les permissions
kubectl auth can-i get secrets --as=system:serviceaccount:default:webapp-service-account

# Rotation des secrets
kubectl delete secret database-credentials
kubectl create secret generic database-credentials \
  --from-literal=username=admin \
  --from-literal=password=NewSuperSecretPassword456 \
  --from-literal=database=production_db

# Forcer la mise à jour des pods
kubectl rollout restart deployment webapp-with-secrets

# Nettoyage des certificats temporaires
rm tls.key tls.crt
```

## Livrables attendus

1. Secrets créés par différentes méthodes
2. Deployment utilisant les Secrets comme variables d'environnement
3. Deployment utilisant les Secrets comme volumes
4. Configuration TLS fonctionnelle
5. ServiceAccount avec permissions appropriées

## Critères de validation

- [ ] Secrets créés et vérifiés (données encodées base64)
- [ ] Variables d'environnement sensibles injectées correctement
- [ ] Fichiers secrets montés avec bonnes permissions (0400)
- [ ] Secret TLS fonctionnel pour HTTPS
- [ ] ServiceAccount avec RBAC configuré
- [ ] Rotation des secrets testée

## Durée estimée

30 minutes

## Bonnes pratiques de sécurité

### Principes de sécurité

- **Principle of least privilege** : Permissions minimales nécessaires
- **Defense in depth** : Sécurité multicouche
- **Rotation régulière** : Changement périodique des secrets

### Gestion des Secrets

```bash
# Éviter les secrets en variables d'environnement (visible dans processus)
# Préférer les volumes montés avec permissions restrictives

# Utiliser des outils externes pour les secrets sensibles
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
```

### Types de Secrets

```yaml
type: Opaque                    # Generic secret
type: kubernetes.io/tls         # TLS certificates
type: kubernetes.io/ssh-auth    # SSH keys
type: kubernetes.io/basic-auth  # Basic authentication
type: kubernetes.io/dockerconfigjson  # Docker registry
```

### Commandes essentielles

```bash
# Création
kubectl create secret generic <nom> --from-literal=<clé>=<valeur>
kubectl create secret tls <nom> --cert=<cert> --key=<key>

# Inspection (attention aux données sensibles!)
kubectl get secrets
kubectl describe secret <nom>
kubectl get secret <nom> -o yaml

# Debugging
kubectl auth can-i <verbe> <ressource> --as=<user>
```
