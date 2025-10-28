# Correction - LAB 3 : Services et networking

## Objectif

- Exposer un Pod via Service ClusterIP/NodePort

## Solutions rapides

1. Service ClusterIP :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
```

2. Service NodePort :

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080
```

## Bonnes pratiques

- Utiliser ClusterIP pour services internes
- Utiliser NetworkPolicy pour restreindre l'accès

## Tests

- kubectl get svc
- curl http://<node-ip>:30080
