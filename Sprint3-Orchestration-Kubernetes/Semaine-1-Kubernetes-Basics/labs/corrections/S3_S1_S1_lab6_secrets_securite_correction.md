# Correction - LAB 6 : Secrets et sécurité

## Objectif

- Stocker et utiliser des Secrets dans K8s

## Solution rapide

```bash
kubectl create secret generic db-credentials --from-literal=username=admin --from-literal=password=s3cret
```

Utilisation dans un Pod :

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: password
```

## Bonnes pratiques

- Utiliser External Secrets / Vault pour production
- Restreindre l'accès avec RBAC

## Tests

- kubectl get secret db-credentials -o yaml
