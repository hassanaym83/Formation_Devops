# Correction - LAB 4 : Deployments et ReplicaSets

## Objectif

- Déployer une application scalable via Deployment

## Solution rapide

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:stable
          ports:
            - containerPort: 80
```

## Bonnes pratiques

- Utiliser readiness/liveness probes
- Configurer strategiess de rolling update

## Tests

- kubectl rollout status deployment/nginx-deployment
- kubectl scale deployment nginx-deployment --replicas=5
