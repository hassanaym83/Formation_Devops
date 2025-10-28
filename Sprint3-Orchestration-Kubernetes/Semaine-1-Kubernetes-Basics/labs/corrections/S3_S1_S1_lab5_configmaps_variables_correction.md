# Correction - LAB 5 : ConfigMaps et variables

## Objectif

- Fournir de la configuration via ConfigMap et variables d'environnement

## Solution rapide

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: production
  LOG_LEVEL: info
```

Exemple de Deployment utilisant ConfigMap :

```yaml
env:
  - name: APP_MODE
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: APP_MODE
```

## Bonnes pratiques

- Ne pas mettre de secrets dans ConfigMap
- Documenter les clés attendues

## Tests

- kubectl describe configmap app-config
