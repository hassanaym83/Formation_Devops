# LAB 1 - Application Deployment complète

## Objectif

Déployer une application e-commerce complète avec architecture 3-tiers sur Kubernetes.

## Contexte

Vous devez déployer une application e-commerce en production avec haute disponibilité comprenant :

- Frontend React avec serveur nginx
- API backend Node.js
- Base de données PostgreSQL
- Cache Redis pour les sessions

## Prérequis

- Cluster Kubernetes fonctionnel
- kubectl configuré
- Images Docker disponibles dans un registry

## Instructions détaillées

### Étape 1 : Préparer les namespaces et configurations

1. Créer un namespace dédié à l'application :

```bash
kubectl create namespace ecommerce
```

2. Créer ConfigMap pour la configuration de l'application :

```yaml
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
```

### Étape 2 : Déployer PostgreSQL

3. Créer Secret pour les credentials de base de données :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: ecommerce
type: Opaque
data:
  username: ZWNvbW1lcmNl # ecommerce en base64
  password: cGFzc3dvcmQ= # password en base64
```

4. Déployer PostgreSQL avec PersistentVolume :

```yaml
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
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc
```

### Étape 3 : Déployer Redis

5. Déployer Redis pour le cache des sessions

### Étape 4 : Déployer l'API Backend

6. Créer Deployment pour l'API Node.js avec :
   - 3 replicas pour haute disponibilité
   - Health checks appropriés
   - Resource limits
   - Variables d'environnement depuis ConfigMap

### Étape 5 : Déployer le Frontend

7. Créer Deployment pour le frontend React avec nginx :
   - 2 replicas
   - Configuration nginx pour SPA
   - Health checks

### Étape 6 : Créer les Services

8. Créer Services ClusterIP pour chaque composant :
   - postgres-service (port 5432)
   - redis-service (port 6379)
   - api-service (port 3000)
   - frontend-service (port 80)

### Étape 7 : Tester la communication

9. Vérifier que tous les pods sont en état Running
10. Tester la connectivité entre les services
11. Vérifier les logs de chaque composant

## Critères de validation

- [ ] Tous les pods sont en état Running
- [ ] Les services sont accessibles et ont des endpoints
- [ ] L'API peut se connecter à PostgreSQL et Redis
- [ ] Le frontend peut communiquer avec l'API
- [ ] Les health checks sont configurés et fonctionnels
- [ ] Les logs ne montrent pas d'erreurs de connexion

## Livrables

- Manifests YAML complets pour tous les composants
- Commandes de test de connectivité
- Capture d'écran des pods en état Running

## Durée estimée

45 minutes

## Ressources supplémentaires

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
