# LAB 4 - Deployments et ReplicaSets

## Objectifs

- Maîtriser les Deployments pour gérer les applications
- Comprendre le rôle des ReplicaSets
- Implémenter le scaling horizontal
- Gérer les mises à jour rolling updates

## Contexte

Gestion avancée des applications avec haute disponibilité et mises à jour sans interruption.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des pods et services

## Instructions

### 1. Créer un Deployment basique

```yaml
# Créer le fichier webapp-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
        version: v1
    spec:
      containers:
        - name: webapp
          image: nginx:1.20
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: '64Mi'
              cpu: '100m'
            limits:
              memory: '128Mi'
              cpu: '200m'
```

```bash
# Déployer l'application
kubectl apply -f webapp-deployment.yaml

# Vérifier le déploiement
kubectl get deployments
kubectl get replicasets
kubectl get pods -l app=webapp
```

### 2. Scaling horizontal

```bash
# Scaler manuellement à 5 replicas
kubectl scale deployment webapp-deployment --replicas=5

# Vérifier le scaling
kubectl get pods -l app=webapp
kubectl describe deployment webapp-deployment

# Scaler via le fichier YAML (modifier replicas: 2)
kubectl apply -f webapp-deployment.yaml

# Observer le scaling down
kubectl get pods -l app=webapp -w
```

### 3. Rolling Updates

```bash
# Mettre à jour l'image
kubectl set image deployment/webapp-deployment webapp=nginx:1.21

# Observer le rolling update
kubectl rollout status deployment webapp-deployment
kubectl get pods -l app=webapp -w

# Vérifier l'historique des déploiements
kubectl rollout history deployment webapp-deployment
```

### 4. Gestion des versions et rollback

```yaml
# Modifier webapp-deployment.yaml pour v2
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
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
          env:
            - name: VERSION
              value: 'v2'
          resources:
            requests:
              memory: '64Mi'
              cpu: '100m'
            limits:
              memory: '128Mi'
              cpu: '200m'
```

```bash
# Appliquer la version v2
kubectl apply -f webapp-deployment.yaml --record

# Voir l'historique détaillé
kubectl rollout history deployment webapp-deployment --revision=2

# Simuler un problème et rollback
kubectl set image deployment/webapp-deployment webapp=nginx:invalid-tag

# Observer l'échec du déploiement
kubectl rollout status deployment webapp-deployment

# Rollback à la version précédente
kubectl rollout undo deployment webapp-deployment

# Rollback à une révision spécifique
kubectl rollout undo deployment webapp-deployment --to-revision=1
```

### 5. Stratégies de déploiement

```yaml
# Créer le fichier deployment-strategies.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-rolling
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 2
  selector:
    matchLabels:
      app: webapp-rolling
  template:
    metadata:
      labels:
        app: webapp-rolling
    spec:
      containers:
        - name: webapp
          image: nginx:1.20
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-recreate
spec:
  replicas: 3
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: webapp-recreate
  template:
    metadata:
      labels:
        app: webapp-recreate
    spec:
      containers:
        - name: webapp
          image: nginx:1.20
          ports:
            - containerPort: 80
```

```bash
# Tester les différentes stratégies
kubectl apply -f deployment-strategies.yaml

# Mettre à jour avec RollingUpdate
kubectl set image deployment/webapp-rolling webapp=nginx:1.21

# Observer le comportement
kubectl get pods -l app=webapp-rolling -w

# Mettre à jour avec Recreate
kubectl set image deployment/webapp-recreate webapp=nginx:1.21

# Observer la différence
kubectl get pods -l app=webapp-recreate -w
```

### 6. Monitoring et observabilité

```bash
# Créer un service pour tester
kubectl expose deployment webapp-deployment --port=80 --type=ClusterIP

# Monitoring continu des pods
kubectl get pods -l app=webapp -w &

# Simuler une charge pour observer le comportement
kubectl run load-generator --image=busybox -it --rm -- /bin/sh
# Dans le pod :
while true; do wget -q --timeout=2 --spider http://webapp-deployment; done
```

### 7. Troubleshooting des deployments

```bash
# Diagnostiquer un deployment bloqué
kubectl describe deployment webapp-deployment
kubectl describe replicaset <rs-name>

# Vérifier les événements
kubectl get events --sort-by=.metadata.creationTimestamp

# Analyser les logs
kubectl logs -l app=webapp --previous

# Forcer la recréation d'un deployment
kubectl rollout restart deployment webapp-deployment
```

## Livrables attendus

1. Fichiers YAML des deployments avec différentes stratégies
2. Démonstration du scaling horizontal
3. Test des rolling updates et rollbacks
4. Documentation des observations sur les stratégies

## Critères de validation

- [ ] Deployment créé avec 3 replicas fonctionnels
- [ ] Scaling up et down réalisé avec succès
- [ ] Rolling update exécuté sans interruption de service
- [ ] Rollback fonctionnel vers version précédente
- [ ] Différences entre stratégies RollingUpdate et Recreate observées
- [ ] Monitoring des pods pendant les opérations

## Durée estimée

30 minutes

## Concepts clés

### Deployment vs ReplicaSet vs Pod

- **Pod** : Unité de déploiement
- **ReplicaSet** : Maintient un nombre de pods
- **Deployment** : Gère les ReplicaSets et les updates

### Stratégies de déploiement

```yaml
strategy:
  type: RollingUpdate # ou Recreate
  rollingUpdate:
    maxUnavailable: 25% # ou nombre absolu
    maxSurge: 25% # ou nombre absolu
```

### Commandes essentielles

```bash
# Gestion des deployments
kubectl create deployment <nom> --image=<image>
kubectl scale deployment <nom> --replicas=<nombre>
kubectl set image deployment/<nom> <container>=<image>

# Rolling updates
kubectl rollout status deployment/<nom>
kubectl rollout history deployment/<nom>
kubectl rollout undo deployment/<nom>
kubectl rollout restart deployment/<nom>

# Monitoring
kubectl get deployments -w
kubectl describe deployment <nom>
kubectl logs deployment/<nom>
```
