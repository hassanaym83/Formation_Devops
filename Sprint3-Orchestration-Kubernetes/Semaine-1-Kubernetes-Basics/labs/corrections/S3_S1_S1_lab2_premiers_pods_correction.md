# Correction - LAB 2 : Premiers Pods et conteneurs

## Objectif

- Créer et manipuler des Pods simples

## Solutions rapides

1. Créer un Pod nginx :

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: nginx:stable
      ports:
        - containerPort: 80
```

2. Accéder aux logs :

```bash
kubectl logs nginx-pod
```

3. Expliquer la différence entre Pod et Deployment, et pourquoi utiliser Deployment pour la résilience.

## Bonnes pratiques

- Préférer Deployments pour production
- Ajouter probes liveness et readiness
- Ne pas exécuter des processus PID 1 non supervisés

## Tests

- kubectl apply -f pod.yaml
- kubectl get pods -o wide
- kubectl describe pod nginx-pod
