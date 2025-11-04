# LAB 8 - Correction : Velero - Backup et Disaster Recovery

## 📋 Vue d'ensemble de la solution

Cette correction présente l'installation et la configuration complète de Velero pour les sauvegardes et la récupération d'urgence sur Kubernetes.

---

## 🔧 Solution complète

### Étape 1 : Installation Velero

```bash
#!/bin/bash
# velero/install-velero.sh

# Variables
BUCKET_NAME="k8s-velero-backups"
REGION="eu-west-1"
NAMESPACE="velero"

# Création du bucket S3 (AWS)
aws s3 mb s3://$BUCKET_NAME --region $REGION

# Politique IAM pour Velero
cat > velero-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeVolumes",
                "ec2:DescribeSnapshots",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::$BUCKET_NAME/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::$BUCKET_NAME"
            ]
        }
    ]
}
EOF

# Créer utilisateur IAM et politique
aws iam create-user --user-name velero
aws iam put-user-policy --user-name velero --policy-name VeleroAccessPolicy --policy-document file://velero-policy.json
aws iam create-access-key --user-name velero

# Installation Velero CLI
curl -fsSL -o velero-v1.12.1-linux-amd64.tar.gz https://github.com/vmware-tanzu/velero/releases/download/v1.12.1/velero-v1.12.1-linux-amd64.tar.gz
tar -xzf velero-v1.12.1-linux-amd64.tar.gz
sudo mv velero-v1.12.1-linux-amd64/velero /usr/local/bin/

# Fichier de credentials
cat > credentials-velero <<EOF
[default]
aws_access_key_id=YOUR_ACCESS_KEY_ID
aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
EOF

# Installation Velero sur le cluster
velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.8.0 \
    --bucket $BUCKET_NAME \
    --backup-location-config region=$REGION \
    --snapshot-location-config region=$REGION \
    --secret-file ./credentials-velero \
    --namespace $NAMESPACE
```

### Étape 2 : Configuration BackupStorageLocation

```yaml
# velero/backup-storage-location.yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: k8s-velero-backups
    prefix: cluster-prod
  config:
    region: eu-west-1
    s3ForcePathStyle: 'false'
---
apiVersion: velero.io/v1
kind: VolumeSnapshotLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws
  config:
    region: eu-west-1
```

### Étape 3 : Schedules de sauvegarde

```yaml
# velero/backup-schedules.yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: '0 2 * * *' # Tous les jours à 2h
  template:
    ttl: 720h # 30 jours
    includedNamespaces:
      - app-prod
      - app-staging
      - monitoring
      - logging
    excludedResources:
      - events
      - events.events.k8s.io
    storageLocation: default
    volumeSnapshotLocations:
      - default
    hooks:
      resources:
        - name: webapp-backup-hook
          includedNamespaces:
            - app-prod
          labelSelector:
            matchLabels:
              app: webapp
          pre:
            - exec:
                command:
                  - /bin/bash
                  - -c
                  - 'curl -X POST http://localhost:8080/actuator/backup/prepare'
          post:
            - exec:
                command:
                  - /bin/bash
                  - -c
                  - 'curl -X POST http://localhost:8080/actuator/backup/complete'
---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: weekly-full-backup
  namespace: velero
spec:
  schedule: '0 1 * * 0' # Dimanche à 1h
  template:
    ttl: 2160h # 90 jours
    includedNamespaces:
      - '*'
    excludedNamespaces:
      - kube-system
      - kube-public
      - kube-node-lease
    excludedResources:
      - events
      - events.events.k8s.io
      - nodes
      - persistentvolumes
    storageLocation: default
    defaultVolumesToRestic: true
---
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: critical-app-backup
  namespace: velero
spec:
  schedule: '0 */6 * * *' # Toutes les 6h
  template:
    ttl: 168h # 7 jours
    labelSelector:
      matchLabels:
        backup: critical
    storageLocation: default
    volumeSnapshotLocations:
      - default
```

### Étape 4 : Scripts de test et récupération

```bash
#!/bin/bash
# velero/test-backup-restore.sh

set -e

echo "🧪 Test de sauvegarde et restauration Velero"

# Créer une application de test
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: test-backup
  labels:
    backup: critical
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
  namespace: test-backup
  labels:
    app: test-app
    backup: critical
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: test-app
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: data
          mountPath: /usr/share/nginx/html
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: test-data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-data
  namespace: test-backup
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-config
  namespace: test-backup
data:
  message: "Test backup data - $(date)"
EOF

# Attendre le déploiement
kubectl wait --for=condition=available deployment/test-app -n test-backup --timeout=60s

# Créer des données de test
kubectl exec -n test-backup deployment/test-app -- sh -c "echo 'Backup test $(date)' > /usr/share/nginx/html/index.html"

echo "✅ Application de test créée avec données"

# Effectuer une sauvegarde
echo "💾 Création de la sauvegarde..."
velero backup create test-backup-$(date +%Y%m%d-%H%M%S) \
    --include-namespaces test-backup \
    --wait

# Vérifier la sauvegarde
BACKUP_STATUS=$(velero backup get --output=jsonpath='{.items[0].status.phase}')
if [ "$BACKUP_STATUS" = "Completed" ]; then
    echo "✅ Sauvegarde créée avec succès"
else
    echo "❌ Échec de la sauvegarde (Status: $BACKUP_STATUS)"
    exit 1
fi

# Supprimer l'application
echo "🗑️ Suppression de l'application..."
kubectl delete namespace test-backup --wait=true

# Restaurer l'application
echo "🔄 Restauration de l'application..."
BACKUP_NAME=$(velero backup get --output=jsonpath='{.items[0].metadata.name}')
velero restore create restore-$(date +%Y%m%d-%H%M%S) \
    --from-backup $BACKUP_NAME \
    --wait

# Vérifier la restauration
kubectl wait --for=condition=available deployment/test-app -n test-backup --timeout=120s

RESTORED_DATA=$(kubectl exec -n test-backup deployment/test-app -- cat /usr/share/nginx/html/index.html)
echo "📄 Données restaurées: $RESTORED_DATA"

if [[ "$RESTORED_DATA" == *"Backup test"* ]]; then
    echo "✅ Restauration réussie avec données intactes"
else
    echo "❌ Problème avec la restauration des données"
fi

# Nettoyer
kubectl delete namespace test-backup
velero backup delete $BACKUP_NAME --confirm

echo "🎉 Test de backup/restore terminé avec succès"
```

### Étape 5 : Monitoring et alertes Velero

```yaml
# velero/monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: velero-metrics
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: velero
  namespaceSelector:
    matchNames:
      - velero
  endpoints:
    - port: http-monitoring
      interval: 30s
      path: /metrics
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: velero-alerts
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: velero.rules
      interval: 30s
      rules:
        # Backup failure
        - alert: VeleroBackupFailure
          expr: |
            increase(velero_backup_failure_total[1h]) > 0
          for: 0m
          labels:
            severity: critical
            service: velero
          annotations:
            summary: 'Velero backup failure'
            description: 'Velero backup {{ $labels.schedule }} has failed.'

        # Backup taking too long
        - alert: VeleroBackupTakingTooLong
          expr: |
            velero_backup_duration_seconds > 3600
          for: 0m
          labels:
            severity: warning
            service: velero
          annotations:
            summary: 'Velero backup taking too long'
            description: 'Velero backup {{ $labels.backup }} is taking more than 1 hour.'

        # No recent backup
        - alert: VeleroNoRecentBackup
          expr: |
            time() - velero_backup_last_successful_timestamp > 86400
          for: 0m
          labels:
            severity: warning
            service: velero
          annotations:
            summary: 'No recent Velero backup'
            description: 'No Velero backup has been completed in the last 24 hours for schedule {{ $labels.schedule }}.'

        # Restore failure
        - alert: VeleroRestoreFailure
          expr: |
            increase(velero_restore_failed_total[1h]) > 0
          for: 0m
          labels:
            severity: critical
            service: velero
          annotations:
            summary: 'Velero restore failure'
            description: 'Velero restore {{ $labels.restore }} has failed.'
```

### Étape 6 : Scripts de récupération d'urgence

```bash
#!/bin/bash
# velero/disaster-recovery.sh

# Script de récupération d'urgence complète
BACKUP_NAME=${1:-latest}
TARGET_CLUSTER=${2:-current}

echo "🚨 Début de la récupération d'urgence"
echo "Backup: $BACKUP_NAME"
echo "Cluster: $TARGET_CLUSTER"

# Si backup_name est "latest", prendre le dernier backup
if [ "$BACKUP_NAME" = "latest" ]; then
    BACKUP_NAME=$(velero backup get --output=jsonpath='{.items[0].metadata.name}')
    echo "📦 Utilisation du dernier backup: $BACKUP_NAME"
fi

# Vérifier que le backup existe et est complet
BACKUP_STATUS=$(velero backup describe $BACKUP_NAME --output=jsonpath='{.status.phase}')
if [ "$BACKUP_STATUS" != "Completed" ]; then
    echo "❌ Backup $BACKUP_NAME n'est pas complet (Status: $BACKUP_STATUS)"
    exit 1
fi

echo "✅ Backup validé, début de la restauration..."

# Restauration par ordre de priorité
echo "🔄 Restauration des ressources critiques..."

# 1. Namespaces et RBAC
velero restore create dr-namespaces-$(date +%Y%m%d-%H%M%S) \
    --from-backup $BACKUP_NAME \
    --include-resources namespaces,roles,rolebindings,clusterroles,clusterrolebindings,serviceaccounts \
    --wait

# 2. Secrets et ConfigMaps
velero restore create dr-configs-$(date +%Y%m%d-%H%M%S) \
    --from-backup $BACKUP_NAME \
    --include-resources secrets,configmaps \
    --wait

# 3. PVCs et storage
velero restore create dr-storage-$(date +%Y%m%d-%H%M%S) \
    --from-backup $BACKUP_NAME \
    --include-resources persistentvolumeclaims,persistentvolumes \
    --wait

# 4. Applications
velero restore create dr-apps-$(date +%Y%m%d-%H%M%S) \
    --from-backup $BACKUP_NAME \
    --include-resources deployments,statefulsets,services,ingresses \
    --wait

echo "⏳ Attente de la stabilisation du cluster..."
sleep 60

# Vérification de la santé post-restauration
echo "🏥 Vérification de la santé du cluster..."

# Vérifier les pods critiques
UNHEALTHY_PODS=$(kubectl get pods --all-namespaces --field-selector=status.phase!=Running --no-headers | wc -l)
echo "🔍 Pods non-Running: $UNHEALTHY_PODS"

# Vérifier les services essentiels
CRITICAL_SERVICES=("app-prod/webapp-service" "monitoring/prometheus" "logging/elasticsearch")
for service in "${CRITICAL_SERVICES[@]}"; do
    namespace=$(echo $service | cut -d'/' -f1)
    svc_name=$(echo $service | cut -d'/' -f2)

    if kubectl get service $svc_name -n $namespace >/dev/null 2>&1; then
        echo "✅ Service $service disponible"
    else
        echo "❌ Service $service manquant"
    fi
done

echo "🎉 Récupération d'urgence terminée"
echo "📊 Statistiques de restauration:"
velero restore get --output=table
```

---

## 🎯 Résultats

✅ **Velero installé** avec sauvegarde S3  
✅ **Schedules automatiques** (quotidien, hebdomadaire)  
✅ **Tests validés** backup/restore  
✅ **Monitoring intégré** avec alertes  
✅ **Scripts DR** pour récupération d'urgence

---

_Correction réalisée par Hassan ESSADIK - Formation DevOps Kubernetes_
