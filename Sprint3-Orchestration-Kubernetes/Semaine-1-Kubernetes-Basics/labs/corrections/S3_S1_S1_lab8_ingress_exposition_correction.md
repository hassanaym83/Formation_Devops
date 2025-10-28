# Correction - LAB 8 : Ingress et exposition

## Objectif

- Configurer Ingress pour exposer un service

## Solution rapide

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
spec:
  rules:
    - host: example.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nginx-service
                port:
                  number: 80
```

## Bonnes pratiques

- Ajouter TLS via cert-manager
- Configurer des annotations pour le contrôleur Ingress

## Tests

- kubectl get ingress
- curl -H "Host: example.local" http://<ingress-ip>/
