# LAB 5 - ConfigMaps et variables d'environnement

## Objectifs

- Maîtriser la gestion de configuration avec ConfigMaps
- Injecter des variables d'environnement dans les pods
- Séparer la configuration du code applicatif
- Utiliser les ConfigMaps comme volumes

## Contexte

Gestion externalisée de la configuration pour faciliter les déploiements multi-environnements.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des deployments

## Instructions

### 1. Créer des ConfigMaps de différentes façons

```bash
# Méthode 1 : Depuis des clés-valeurs
kubectl create configmap app-config \
  --from-literal=database_url=postgres://localhost:5432/myapp \
  --from-literal=debug_mode=true \
  --from-literal=max_connections=100

# Méthode 2 : Depuis un fichier de propriétés
cat > app.properties << EOF
database.driver=postgresql
database.host=localhost
database.port=5432
database.name=myapp
app.debug=true
app.version=1.2.3
EOF

kubectl create configmap app-properties --from-file=app.properties

# Méthode 3 : Depuis un répertoire
mkdir config-files
echo "upstream backend { server 127.0.0.1:8080; }" > config-files/nginx.conf
echo "worker_processes auto;" > config-files/nginx-main.conf

kubectl create configmap nginx-config --from-file=config-files/

# Vérifier les ConfigMaps créées
kubectl get configmaps
kubectl describe configmap app-config
kubectl get configmap app-config -o yaml
```

### 2. ConfigMap déclarative avec YAML

```yaml
# Créer le fichier webapp-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: webapp-configmap
data:
  # Configuration de l'application
  database_host: 'postgres.example.com'
  database_port: '5432'
  database_name: 'production_db'
  redis_host: 'redis.example.com'
  redis_port: '6379'

  # Fichier de configuration complet
  app-config.yml: |
    server:
      port: 8080
      host: 0.0.0.0
    database:
      driver: postgresql
      host: postgres.example.com
      port: 5432
      name: production_db
      pool_size: 20
    redis:
      host: redis.example.com
      port: 6379
      timeout: 5000
    logging:
      level: INFO
      file: /var/log/app.log

  # Configuration nginx
  nginx.conf: |
    events {
        worker_connections 1024;
    }
    http {
        upstream backend {
            server app1:8080;
            server app2:8080;
            server app3:8080;
        }
        server {
            listen 80;
            location / {
                proxy_pass http://backend;
            }
        }
    }
```

```bash
# Appliquer la ConfigMap
kubectl apply -f webapp-configmap.yaml

# Vérifier le contenu
kubectl get configmap webapp-configmap -o yaml
```

### 3. Injection comme variables d'environnement

```yaml
# Créer le fichier deployment-with-env.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-env
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp-env
  template:
    metadata:
      labels:
        app: webapp-env
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          env:
            # Variable individuelle depuis ConfigMap
            - name: DATABASE_HOST
              valueFrom:
                configMapKeyRef:
                  name: webapp-configmap
                  key: database_host
            - name: DATABASE_PORT
              valueFrom:
                configMapKeyRef:
                  name: webapp-configmap
                  key: database_port
          # Variables depuis ConfigMap complet
          envFrom:
            - configMapRef:
                name: app-config
          ports:
            - containerPort: 80
```

```bash
# Déployer l'application
kubectl apply -f deployment-with-env.yaml

# Vérifier les variables d'environnement
kubectl exec -it deployment/webapp-with-env -- env | grep -E "(DATABASE|debug|max)"
```

### 4. Monter ConfigMap comme volume

```yaml
# Créer le fichier deployment-with-volume.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-volume
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-volume
  template:
    metadata:
      labels:
        app: webapp-volume
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          volumeMounts:
            # Monter la configuration complète
            - name: app-config-volume
              mountPath: /etc/webapp
              readOnly: true
            # Monter seulement nginx.conf
            - name: nginx-config-volume
              mountPath: /etc/nginx/nginx.conf
              subPath: nginx.conf
              readOnly: true
          ports:
            - containerPort: 80
      volumes:
        # Volume pour toute la ConfigMap
        - name: app-config-volume
          configMap:
            name: webapp-configmap
        # Volume pour un fichier spécifique
        - name: nginx-config-volume
          configMap:
            name: webapp-configmap
            items:
              - key: nginx.conf
                path: nginx.conf
                mode: 0644
```

```bash
# Déployer avec volumes
kubectl apply -f deployment-with-volume.yaml

# Vérifier les fichiers montés
kubectl exec -it deployment/webapp-with-volume -- ls -la /etc/webapp/
kubectl exec -it deployment/webapp-with-volume -- cat /etc/webapp/app-config.yml
kubectl exec -it deployment/webapp-with-volume -- cat /etc/nginx/nginx.conf
```

### 5. Mise à jour dynamique des ConfigMaps

```bash
# Modifier une ConfigMap existante
kubectl patch configmap webapp-configmap --patch '{"data":{"database_host":"new-postgres.example.com"}}'

# Ou éditer directement
kubectl edit configmap webapp-configmap

# Observer le comportement selon le type d'injection
# Variables d'environnement : pas de mise à jour automatique
kubectl exec -it deployment/webapp-with-env -- env | grep DATABASE_HOST

# Volumes : mise à jour automatique (avec délai)
kubectl exec -it deployment/webapp-with-volume -- cat /etc/webapp/database_host

# Forcer la mise à jour des pods pour les variables d'environnement
kubectl rollout restart deployment webapp-with-env
```

### 6. Gestion multi-environnements

```yaml
# Créer le fichier configmaps-environments.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-dev
  namespace: development
data:
  database_host: 'postgres-dev.local'
  database_name: 'myapp_dev'
  debug_mode: 'true'
  log_level: 'DEBUG'

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config-prod
  namespace: production
data:
  database_host: 'postgres-prod.company.com'
  database_name: 'myapp_production'
  debug_mode: 'false'
  log_level: 'ERROR'

---
# Template de deployment réutilisable
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: development
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: myapp:latest
          envFrom:
            - configMapRef:
                name: app-config-dev # Changer selon l'environnement
```

### 7. Validation et troubleshooting

```bash
# Vérifier les ConfigMaps
kubectl get configmaps
kubectl describe configmap webapp-configmap

# Débugger les injections
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- env
kubectl exec -it <pod-name> -- ls -la /etc/webapp/

# Vérifier les événements
kubectl get events --field-selector involvedObject.kind=ConfigMap

# Tester la configuration
kubectl run debug-pod --image=busybox -it --rm \
  --env="DATABASE_HOST=test" \
  --env-from=configmap/app-config \
  -- /bin/sh
```

## Livrables attendus

1. ConfigMaps créées par différentes méthodes
2. Deployment utilisant les variables d'environnement
3. Deployment utilisant les volumes ConfigMap
4. Test de mise à jour dynamique des configurations
5. Documentation des différences observées

## Critères de validation

- [ ] ConfigMaps créées via CLI et YAML
- [ ] Variables d'environnement correctement injectées
- [ ] Fichiers de configuration montés comme volumes
- [ ] Mise à jour dynamique fonctionnelle pour les volumes
- [ ] Configuration multi-environnements testée
- [ ] Troubleshooting réalisé avec succès

## Durée estimée

25 minutes

## Bonnes pratiques

### Structuration des ConfigMaps

```yaml
# Séparer par fonction
app-database-config    # Configuration BDD
app-cache-config       # Configuration cache
app-logging-config     # Configuration logs
```

### Conventions de nommage

```bash
# Variables d'environnement
DATABASE_HOST=postgres.local
REDIS_PORT=6379

# Fichiers de configuration
database.yml
redis.conf
nginx.conf
```

### Commandes utiles

```bash
# Gestion ConfigMaps
kubectl create configmap <nom> --from-literal=<clé>=<valeur>
kubectl create configmap <nom> --from-file=<fichier>
kubectl get configmap <nom> -o yaml
kubectl describe configmap <nom>

# Debug injection
kubectl describe pod <pod>
kubectl exec -it <pod> -- env
kubectl exec -it <pod> -- cat <chemin-fichier>
```
