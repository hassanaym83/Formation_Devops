# LAB 2 - Premiers pods et conteneurs

## Objectifs

- Créer et gérer des pods Kubernetes
- Comprendre le cycle de vie des pods
- Manipuler les conteneurs dans les pods
- Utiliser les commandes kubectl de base

## Contexte

Apprentissage des concepts fondamentaux des pods, unité de base de déploiement dans Kubernetes.

## Prérequis

- Cluster Kubernetes fonctionnel (LAB 1)
- kubectl configuré

## Instructions

### 1. Créer un pod simple

```yaml
# Créer le fichier pod-simple.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
    - name: nginx
      image: nginx:1.21
      ports:
        - containerPort: 80
```

```bash
# Appliquer la configuration
kubectl apply -f pod-simple.yaml

# Vérifier la création
kubectl get pods
kubectl describe pod nginx-pod
```

### 2. Interagir avec le pod

```bash
# Obtenir les logs
kubectl logs nginx-pod

# Exécuter une commande dans le pod
kubectl exec nginx-pod -- nginx -v

# Ouvrir une session interactive
kubectl exec -it nginx-pod -- /bin/bash

# Dans le conteneur, vérifier nginx
curl localhost
exit
```

### 3. Créer un pod multi-conteneurs

```yaml
# Créer le fichier pod-multi.yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:1.21
      ports:
        - containerPort: 80
      volumeMounts:
        - name: shared-volume
          mountPath: /usr/share/nginx/html
    - name: content-generator
      image: busybox
      command: ['/bin/sh']
      args:
        [
          '-c',
          "while true; do echo '<h1>Hello from Pod: '$(date)'</h1>' > /shared/index.html; sleep 10; done"
        ]
      volumeMounts:
        - name: shared-volume
          mountPath: /shared
  volumes:
    - name: shared-volume
      emptyDir: {}
```

```bash
# Déployer le pod multi-conteneurs
kubectl apply -f pod-multi.yaml

# Vérifier les conteneurs
kubectl get pods multi-container-pod
kubectl describe pod multi-container-pod
```

### 4. Port forwarding et test

```bash
# Créer un port forwarding vers le pod nginx
kubectl port-forward nginx-pod 8080:80

# Dans un autre terminal, tester la connexion
curl http://localhost:8080

# Tester le pod multi-conteneurs
kubectl port-forward multi-container-pod 8081:80
curl http://localhost:8081
```

### 5. Gestion du cycle de vie

```bash
# Voir les événements du pod
kubectl get events --field-selector involvedObject.name=nginx-pod

# Supprimer un pod
kubectl delete pod nginx-pod

# Vérifier la suppression
kubectl get pods

# Recréer à partir du fichier
kubectl apply -f pod-simple.yaml
```

### 6. Debugging et troubleshooting

```bash
# Créer un pod avec erreur pour tester le debugging
kubectl run debug-pod --image=nginx:invalid-tag

# Observer l'état du pod
kubectl get pods debug-pod
kubectl describe pod debug-pod
kubectl logs debug-pod

# Supprimer le pod défaillant
kubectl delete pod debug-pod
```

## Livrables attendus

1. Fichiers YAML des deux pods créés
2. Captures d'écran des commandes kubectl
3. Test de connexion aux pods via port-forward
4. Documentation des observations sur le cycle de vie

## Critères de validation

- [ ] Pod simple nginx créé et fonctionnel
- [ ] Pod multi-conteneurs déployé avec succès
- [ ] Port-forward fonctionnel vers les deux pods
- [ ] Logs accessibles depuis les conteneurs
- [ ] Commandes exec fonctionnelles
- [ ] Pods supprimés proprement

## Durée estimée

20 minutes

## Ressources utiles

### Commandes kubectl essentielles

```bash
# Gestion des pods
kubectl get pods
kubectl describe pod <nom>
kubectl logs <nom-pod>
kubectl exec -it <nom-pod> -- <commande>
kubectl delete pod <nom>

# Port forwarding
kubectl port-forward <nom-pod> <port-local>:<port-pod>

# Debugging
kubectl get events
kubectl describe node <nom-node>
```

### Spécifications Pod avancées

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: advanced-pod
  labels:
    env: dev
    tier: frontend
spec:
  containers:
    - name: app
      image: nginx:1.21
      resources:
        requests:
          memory: '64Mi'
          cpu: '100m'
        limits:
          memory: '128Mi'
          cpu: '200m'
      livenessProbe:
        httpGet:
          path: /
          port: 80
        initialDelaySeconds: 30
        periodSeconds: 10
  restartPolicy: Always
```
