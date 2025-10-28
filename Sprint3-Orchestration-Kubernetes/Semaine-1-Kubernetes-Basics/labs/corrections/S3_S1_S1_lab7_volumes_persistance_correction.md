# Correction - LAB 7 : Volumes et persistance

## Objectif

- Utiliser PersistentVolume / PersistentVolumeClaim

## Solution rapide

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-data
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

Montage dans un pod :

```yaml
volumes:
  - name: data
    persistentVolumeClaim:
      claimName: pvc-data
```

## Bonnes pratiques

- Utiliser StorageClass adaptée au cloud
- Sauvegarder les données critiques

## Tests

- kubectl get pvc
- kubectl describe pvc pvc-data
