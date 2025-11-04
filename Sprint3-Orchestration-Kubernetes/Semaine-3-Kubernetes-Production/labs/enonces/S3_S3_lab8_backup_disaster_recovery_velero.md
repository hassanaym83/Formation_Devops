# LAB 8 - Backup et Disaster Recovery avec Velero

## Objectifs

- Installer et configurer Velero pour les sauvegardes Kubernetes
- Implémenter des stratégies de backup complètes
- Configurer la sauvegarde des volumes persistants
- Tester la restauration et le disaster recovery
- Automatiser les sauvegardes avec des politiques

## Prérequis

- Cluster Kubernetes fonctionnel
- kubectl configuré
- Accès à un stockage objet (S3, MinIO, Azure Blob, etc.)
- Applications avec données persistantes déployées
- Connaissances des concepts de backup et recovery

## Contexte du LAB

Vous allez implémenter une solution complète de backup et disaster recovery pour :

- Sauvegarder les ressources Kubernetes (manifestes, secrets, configmaps)
- Sauvegarder les volumes persistants (bases de données, fichiers)
- Tester la restauration complète d'applications
- Mettre en place des sauvegardes automatiques programmées
- Préparer une stratégie de disaster recovery multi-cluster

## Exercice 1 : Installation et configuration de Velero

### Étape 1.1 : Préparation du stockage objet (MinIO)

Créez `minio/minio-deployment.yaml` :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: minio
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio
  namespace: minio
spec:
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
        - name: minio
          image: minio/minio:latest
          args:
            - server
            - /data
            - --console-address
            - ':9001'
          env:
            - name: MINIO_ROOT_USER
              value: 'minioadmin'
            - name: MINIO_ROOT_PASSWORD
              value: 'minioadmin123'
          ports:
            - containerPort: 9000
              name: api
            - containerPort: 9001
              name: console
          volumeMounts:
            - name: data
              mountPath: /data
          resources:
            requests:
              memory: '256Mi'
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '200m'
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: minio-pvc
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
  namespace: minio
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
---
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: minio
spec:
  selector:
    app: minio
  ports:
    - name: api
      port: 9000
      targetPort: 9000
    - name: console
      port: 9001
      targetPort: 9001
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minio-console
  namespace: minio
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: minio-console.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: minio
                port:
                  number: 9001
```

### Étape 1.2 : Déploiement MinIO

```bash
kubectl apply -f minio/minio-deployment.yaml

# Attendre que MinIO soit prêt
kubectl wait --for=condition=ready pod -l app=minio -n minio --timeout=300s
```

### Étape 1.3 : Configuration du bucket MinIO

Créez `scripts/setup-minio.sh` :

```bash
#!/bin/bash

set -e

MINIO_ENDPOINT="minio.minio.svc.cluster.local:9000"
ACCESS_KEY="minioadmin"
SECRET_KEY="minioadmin123"
BUCKET_NAME="velero-backups"

echo "Setting up MinIO for Velero..."

# Port-forward vers MinIO
kubectl port-forward -n minio svc/minio 9000:9000 &
FORWARD_PID=$!

# Attendre que le port-forward soit prêt
sleep 5

# Installer mc (MinIO client) si nécessaire
if ! command -v mc &> /dev/null; then
    echo "Installing MinIO client..."
    curl -L https://dl.min.io/client/mc/release/linux-amd64/mc -o /usr/local/bin/mc
    chmod +x /usr/local/bin/mc
fi

# Configurer l'alias MinIO
mc alias set minio http://localhost:9000 $ACCESS_KEY $SECRET_KEY

# Créer le bucket pour Velero
mc mb minio/$BUCKET_NAME --ignore-existing

# Créer la politique d'accès
cat << EOF > velero-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
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

# Arrêter le port-forward
kill $FORWARD_PID

echo "MinIO setup completed!"
echo "Bucket: $BUCKET_NAME"
echo "Access Key: $ACCESS_KEY"
echo "Secret Key: $SECRET_KEY"
```

### Étape 1.4 : Installation de Velero CLI

```bash
# Télécharger Velero CLI
VELERO_VERSION="v1.11.0"
wget https://github.com/vmware-tanzu/velero/releases/download/${VELERO_VERSION}/velero-${VELERO_VERSION}-linux-amd64.tar.gz

# Extraire et installer
tar -xzf velero-${VELERO_VERSION}-linux-amd64.tar.gz
sudo mv velero-${VELERO_VERSION}-linux-amd64/velero /usr/local/bin/
rm -rf velero-${VELERO_VERSION}-linux-amd64*

# Vérifier l'installation
velero version --client-only
```

### Étape 1.5 : Configuration des credentials

Créez `velero/credentials-velero` :

```ini
[default]
aws_access_key_id = minioadmin
aws_secret_access_key = minioadmin123
```

### Étape 1.6 : Installation de Velero sur le cluster

```bash
# Installer Velero avec configuration MinIO/S3
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.7.0 \
  --bucket velero-backups \
  --secret-file ./velero/credentials-velero \
  --use-volume-snapshots=false \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.minio.svc.cluster.local:9000 \
  --use-node-agent
```

### Étape 1.7 : Vérification de l'installation

```bash
# Vérifier les pods Velero
kubectl get pods -n velero

# Vérifier la configuration
velero backup-location get
velero plugin get
```

## Exercice 2 : Application avec données persistantes

### Étape 2.1 : Base de données PostgreSQL

Créez `apps/postgresql.yaml` :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: database
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
  namespace: database
data:
  POSTGRES_DB: ecommerce
  POSTGRES_USER: dbuser
  POSTGRES_PASSWORD: dbpassword123
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: database
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:13
          ports:
            - containerPort: 5432
          envFrom:
            - configMapRef:
                name: postgres-config
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: init-scripts
              mountPath: /docker-entrypoint-initdb.d
          resources:
            requests:
              memory: '256Mi'
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '200m'
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-pvc
        - name: init-scripts
          configMap:
            name: postgres-init
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: database
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: fast-ssd
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: database
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-init
  namespace: database
data:
  init.sql: |
    -- Create tables
    CREATE TABLE products (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        total DECIMAL(10,2) NOT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        product_id INTEGER REFERENCES products(id),
        quantity INTEGER NOT NULL,
        price DECIMAL(10,2) NOT NULL
    );

    -- Insert sample data
    INSERT INTO products (name, price, description) VALUES
    ('Laptop Pro', 1299.99, 'High-performance laptop for professionals'),
    ('Wireless Mouse', 29.99, 'Ergonomic wireless mouse'),
    ('Mechanical Keyboard', 149.99, 'RGB mechanical gaming keyboard'),
    ('4K Monitor', 399.99, '27-inch 4K UHD monitor'),
    ('Webcam HD', 79.99, 'Full HD webcam with auto-focus');

    INSERT INTO orders (user_id, total, status) VALUES
    (1001, 1329.98, 'completed'),
    (1002, 229.98, 'pending'),
    (1003, 479.98, 'processing'),
    (1004, 149.99, 'completed'),
    (1005, 109.98, 'shipped');

    INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
    (1, 1, 1, 1299.99),
    (1, 2, 1, 29.99),
    (2, 3, 1, 149.99),
    (2, 2, 1, 29.99),
    (3, 4, 1, 399.99),
    (3, 5, 1, 79.99),
    (4, 3, 1, 149.99),
    (5, 2, 2, 29.99);
```

### Étape 2.2 : Application web avec stockage de fichiers

Créez `apps/file-storage-app.yaml` :

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: files
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: file-storage-app
  namespace: files
spec:
  replicas: 2
  selector:
    matchLabels:
      app: file-storage-app
  template:
    metadata:
      labels:
        app: file-storage-app
    spec:
      containers:
        - name: app
          image: nginx:alpine
          ports:
            - containerPort: 80
          volumeMounts:
            - name: uploads
              mountPath: /usr/share/nginx/html/uploads
            - name: config
              mountPath: /etc/nginx/conf.d
      volumes:
        - name: uploads
          persistentVolumeClaim:
            claimName: uploads-pvc
        - name: config
          configMap:
            name: nginx-config
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: uploads-pvc
  namespace: files
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 2Gi
  storageClassName: nfs-client
---
apiVersion: v1
kind: Service
metadata:
  name: file-storage-app
  namespace: files
spec:
  selector:
    app: file-storage-app
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: files
data:
  default.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
        }
        
        location /uploads/ {
            alias /usr/share/nginx/html/uploads/;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
        }
        
        location /upload {
            client_max_body_size 100M;
            upload_pass @upload_handler;
            upload_store /usr/share/nginx/html/uploads;
            upload_state_store /tmp;
        }
    }
```

### Étape 2.3 : Job pour créer des données de test

Créez `apps/data-generator.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-generator
  namespace: files
spec:
  template:
    spec:
      containers:
        - name: generator
          image: busybox
          command:
            - /bin/sh
            - -c
            - |
              echo "Generating test files..."
              for i in $(seq 1 10); do
                echo "Test file content $i - $(date)" > /uploads/test-file-$i.txt
                echo "Generated file $i"
                sleep 1
              done

              # Create directory structure
              mkdir -p /uploads/documents/reports
              mkdir -p /uploads/images/thumbnails
              mkdir -p /uploads/backups/daily

              # Generate files in subdirectories
              echo "Important document content" > /uploads/documents/important.doc
              echo "Financial report Q4" > /uploads/documents/reports/financial-q4.txt
              echo "Daily backup $(date)" > /uploads/backups/daily/backup-$(date +%Y%m%d).txt

              echo "Data generation completed!"
          volumeMounts:
            - name: uploads
              mountPath: /uploads
      volumes:
        - name: uploads
          persistentVolumeClaim:
            claimName: uploads-pvc
      restartPolicy: OnFailure
```

### Étape 2.4 : Déploiement des applications

```bash
# Déployer PostgreSQL
kubectl apply -f apps/postgresql.yaml

# Déployer l'application de stockage de fichiers
kubectl apply -f apps/file-storage-app.yaml

# Générer des données de test
kubectl apply -f apps/data-generator.yaml

# Vérifier que tout fonctionne
kubectl get pods -n database
kubectl get pods -n files
kubectl get pvc -n database
kubectl get pvc -n files
```

## Exercice 3 : Premières sauvegardes avec Velero

### Étape 3.1 : Sauvegarde d'un namespace complet

```bash
# Sauvegarde du namespace database
velero backup create database-backup-1 \
  --include-namespaces database \
  --storage-location default \
  --ttl 720h0m0s

# Vérifier le statut de la sauvegarde
velero backup describe database-backup-1
velero backup logs database-backup-1
```

### Étape 3.2 : Sauvegarde avec sélecteur de labels

```bash
# Sauvegarde basée sur les labels
velero backup create postgres-backup \
  --selector app=postgres \
  --include-namespaces database

# Sauvegarde de ressources spécifiques
velero backup create configmaps-backup \
  --include-resources configmaps \
  --include-namespaces database,files
```

### Étape 3.3 : Sauvegarde avec exclusions

```bash
# Sauvegarde en excluant certaines ressources
velero backup create full-backup-excluding-logs \
  --exclude-resources logs,events \
  --include-namespaces database,files

# Sauvegarde en excluant certains labels
velero backup create backup-without-temp \
  --exclude-label-selector temp=true
```

### Étape 3.4 : Vérification des sauvegardes

```bash
# Lister toutes les sauvegardes
velero backup get

# Détails d'une sauvegarde
velero backup describe database-backup-1 --details

# Vérifier le contenu dans MinIO
kubectl port-forward -n minio svc/minio 9000:9000 &
# Accéder à http://localhost:9001 et vérifier le bucket velero-backups
```

## Exercice 4 : Tests de restauration

### Étape 4.1 : Simulation d'un désastre

```bash
# Supprimer le namespace database pour simuler une perte
kubectl delete namespace database

# Vérifier que les données sont perdues
kubectl get pods -n database
kubectl get pvc -n database
```

### Étape 4.2 : Restauration complète

```bash
# Restaurer depuis la sauvegarde
velero restore create database-restore-1 \
  --from-backup database-backup-1

# Vérifier le statut de la restauration
velero restore describe database-restore-1
velero restore logs database-restore-1
```

### Étape 4.3 : Vérification de la restauration

```bash
# Vérifier que les pods sont revenus
kubectl get pods -n database

# Vérifier que les données sont restaurées
kubectl exec -it -n database deployment/postgres -- psql -U dbuser -d ecommerce -c "SELECT COUNT(*) FROM products;"
kubectl exec -it -n database deployment/postgres -- psql -U dbuser -d ecommerce -c "SELECT * FROM orders LIMIT 5;"
```

### Étape 4.4 : Restauration sélective

```bash
# Créer une nouvelle sauvegarde après modifications
kubectl exec -it -n database deployment/postgres -- psql -U dbuser -d ecommerce -c "INSERT INTO products (name, price) VALUES ('New Product', 99.99);"

velero backup create database-backup-2 \
  --include-namespaces database

# Restaurer seulement certaines ressources
velero restore create selective-restore \
  --from-backup database-backup-2 \
  --include-resources persistentvolumeclaims,persistentvolumes
```

## Exercice 5 : Sauvegardes programmées

### Étape 5.1 : Planification quotidienne

Créez `velero/schedule-daily.yaml` :

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  # Sauvegarde quotidienne à 2h00
  schedule: '0 2 * * *'
  template:
    # Inclure tous les namespaces sauf système
    excludeNamespaces:
      - kube-system
      - kube-public
      - velero
      - kube-node-lease

    # Rétention de 30 jours
    ttl: 720h0m0s

    # Storage location
    storageLocation: default

    # Inclure les volumes
    defaultVolumesToRestic: true

    # Labels pour identifier cette sauvegarde
    labels:
      schedule: daily
      type: full
```

### Étape 5.2 : Planification par namespace

Créez `velero/schedule-database.yaml` :

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: database-backup-schedule
  namespace: velero
spec:
  # Toutes les 6 heures
  schedule: '0 */6 * * *'
  template:
    includeNamespaces:
      - database

    # Rétention plus longue pour les bases de données
    ttl: 2160h0m0s # 90 jours

    # Hooks pour arrêter/redémarrer la base avant/après sauvegarde
    hooks:
      resources:
        - name: postgres-backup-hook
          includedNamespaces:
            - database
          includedResources:
            - pods
          labelSelector:
            matchLabels:
              app: postgres
          pre:
            - exec:
                container: postgres
                command:
                  - /bin/bash
                  - -c
                  - 'pg_dumpall -U dbuser > /tmp/backup.sql'
          post:
            - exec:
                container: postgres
                command:
                  - /bin/bash
                  - -c
                  - 'rm -f /tmp/backup.sql'

    labels:
      schedule: database
      frequency: every-6h
```

### Étape 5.3 : Planification hebdomadaire

Créez `velero/schedule-weekly.yaml` :

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: weekly-full-backup
  namespace: velero
spec:
  # Tous les dimanches à 1h00
  schedule: '0 1 * * 0'
  template:
    # Sauvegarde complète de tout le cluster
    includeClusterResources: true

    # Rétention de 6 mois
    ttl: 4320h0m0s

    # Snapshot des volumes persistants
    snapshotVolumes: true

    labels:
      schedule: weekly
      type: full-cluster
      retention: long-term
```

### Étape 5.4 : Application des planifications

```bash
# Appliquer les schedules
kubectl apply -f velero/schedule-daily.yaml
kubectl apply -f velero/schedule-database.yaml
kubectl apply -f velero/schedule-weekly.yaml

# Vérifier les schedules
velero schedule get

# Vérifier les détails d'un schedule
velero schedule describe daily-backup
```

## Exercice 6 : Backup et restore entre clusters

### Étape 6.1 : Configuration multi-cluster

Créez `velero/backup-location-remote.yaml` :

```yaml
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: remote-cluster
  namespace: velero
spec:
  provider: aws
  objectStorage:
    bucket: velero-remote-backups
    prefix: cluster-production
  config:
    region: minio
    s3ForcePathStyle: 'true'
    s3Url: http://minio-remote.company.com:9000
  accessMode: ReadWrite
```

### Étape 6.2 : Sauvegarde pour migration

```bash
# Créer une sauvegarde pour migration vers un autre cluster
velero backup create migration-backup \
  --storage-location remote-cluster \
  --include-namespaces database,files \
  --exclude-resources events,logs

# Attendre la fin de la sauvegarde
velero backup wait migration-backup
```

### Étape 6.3 : Script de migration

Créez `scripts/migrate-to-cluster.sh` :

```bash
#!/bin/bash

set -e

SOURCE_BACKUP="migration-backup"
TARGET_CLUSTER_CONTEXT="target-cluster"
STORAGE_LOCATION="remote-cluster"

echo "Starting cluster migration..."

# Sauvegarder le contexte actuel
CURRENT_CONTEXT=$(kubectl config current-context)

# Vérifier que la sauvegarde existe
velero backup describe $SOURCE_BACKUP

# Basculer vers le cluster cible
kubectl config use-context $TARGET_CLUSTER_CONTEXT

# Vérifier que Velero est installé sur le cluster cible
kubectl get pods -n velero

# Synchroniser les sauvegardes depuis le stockage
velero backup-location get

# Restaurer sur le cluster cible
velero restore create migration-restore \
  --from-backup $SOURCE_BACKUP \
  --restore-volumes=true

# Attendre la fin de la restauration
velero restore wait migration-restore

# Vérifier la restauration
kubectl get pods -n database
kubectl get pods -n files

echo "Migration completed successfully!"

# Retourner au contexte original
kubectl config use-context $CURRENT_CONTEXT
```

## Exercice 7 : Hooks de sauvegarde

### Étape 7.1 : Hooks pour base de données

Créez `apps/postgres-with-hooks.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-with-hooks
  namespace: database
  annotations:
    # Hooks Velero pour cohérence des données
    pre.hook.backup.velero.io/container: postgres
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "pg_dumpall -U $POSTGRES_USER > /tmp/backup.sql && sync"]'
    post.hook.backup.velero.io/container: postgres
    post.hook.backup.velero.io/command: '["/bin/bash", "-c", "rm -f /tmp/backup.sql"]'
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres-hooks
  template:
    metadata:
      labels:
        app: postgres-hooks
      annotations:
        # Annotations pour les hooks au niveau du pod
        backup.velero.io/backup-volumes: postgres-data
    spec:
      containers:
        - name: postgres
          image: postgres:13
          env:
            - name: POSTGRES_DB
              value: 'testdb'
            - name: POSTGRES_USER
              value: 'testuser'
            - name: POSTGRES_PASSWORD
              value: 'testpass'
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: backup-scripts
              mountPath: /backup-scripts
      volumes:
        - name: postgres-data
          persistentVolumeClaim:
            claimName: postgres-hooks-pvc
        - name: backup-scripts
          configMap:
            name: backup-scripts
            defaultMode: 0755
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-hooks-pvc
  namespace: database
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
  name: backup-scripts
  namespace: database
data:
  pre-backup.sh: |
    #!/bin/bash
    echo "Starting database backup preparation..."
    pg_dumpall -U $POSTGRES_USER > /tmp/db-backup-$(date +%Y%m%d-%H%M%S).sql
    echo "Database dump completed"

  post-backup.sh: |
    #!/bin/bash
    echo "Cleaning up backup artifacts..."
    rm -f /tmp/db-backup-*.sql
    echo "Cleanup completed"
```

### Étape 7.2 : Test des hooks

```bash
# Déployer l'application avec hooks
kubectl apply -f apps/postgres-with-hooks.yaml

# Créer une sauvegarde pour tester les hooks
velero backup create hooks-test \
  --include-namespaces database \
  --selector app=postgres-hooks

# Vérifier les logs des hooks
velero backup logs hooks-test
```

## Exercice 8 : Monitoring et alerting

### Étape 8.1 : Métriques Prometheus

Créez `monitoring/velero-servicemonitor.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: velero-metrics
  namespace: velero
spec:
  selector:
    matchLabels:
      component: velero
  endpoints:
    - port: http-monitoring
      path: /metrics
      interval: 30s
```

### Étape 8.2 : Règles d'alertes

Créez `monitoring/velero-alerts.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: velero-alerts
  namespace: velero
spec:
  groups:
    - name: velero.rules
      rules:
        - alert: VeleroBackupFailed
          expr: velero_backup_failure_total > 0
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: 'Velero backup failed'
            description: 'Velero backup {{ $labels.schedule }} has failed'

        - alert: VeleroBackupTooOld
          expr: time() - velero_backup_last_successful_timestamp > 86400
          for: 1h
          labels:
            severity: warning
          annotations:
            summary: 'Velero backup is too old'
            description: 'No successful backup in the last 24 hours'

        - alert: VeleroRestoreFailed
          expr: velero_restore_failed_total > 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: 'Velero restore failed'
            description: 'Velero restore {{ $labels.restore }} has failed'

        - alert: VeleroBackupStorageLocationUnavailable
          expr: velero_backup_storage_location_available == 0
          for: 10m
          labels:
            severity: critical
          annotations:
            summary: 'Velero backup storage location unavailable'
            description: 'Backup storage location {{ $labels.location }} is unavailable'
```

### Étape 8.3 : Dashboard Grafana

Créez `monitoring/velero-dashboard.json` :

```json
{
  "dashboard": {
    "title": "Velero Backup & Restore",
    "panels": [
      {
        "title": "Backup Success Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "velero_backup_success_total / (velero_backup_success_total + velero_backup_failure_total) * 100"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 80},
                {"color": "green", "value": 95}
              ]
            }
          }
        }
      },
      {
        "title": "Backup Duration",
        "type": "graph",
        "targets": [
          {
            "expr": "velero_backup_duration_seconds",
            "legendFormat": "{{ schedule }}"
          }
        ]
      },
      {
        "title": "Backup Storage Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "velero_backup_total_size_bytes",
            "legendFormat": "Total Size"
          }
        ]
      }
    ]
  }
}
```

## Exercice 9 : Tests de disaster recovery

### Étape 9.1 : Plan de disaster recovery

Créez `disaster-recovery/dr-plan.md` :

````markdown
# Plan de Disaster Recovery

## Objectifs RTO/RPO

- RTO (Recovery Time Objective): 4 heures
- RPO (Recovery Point Objective): 6 heures

## Scénarios de désastre

### Scénario 1: Perte d'un namespace

- **Détection**: Monitoring automatique
- **Action**: Restauration automatique depuis la dernière sauvegarde
- **RTO**: 30 minutes

### Scénario 2: Perte de cluster complet

- **Détection**: Monitoring externe
- **Action**: Restauration sur cluster de secours
- **RTO**: 4 heures

### Scénario 3: Corruption de données

- **Détection**: Vérification d'intégrité
- **Action**: Restauration point-in-time
- **RTO**: 2 heures

## Procédures

### 1. Vérification quotidienne des sauvegardes

```bash
#!/bin/bash
velero backup get --output table
velero schedule get --output table
```
````

### 2. Test de restauration mensuel

```bash
#!/bin/bash
# Test sur environnement de staging
velero backup create monthly-test --include-namespaces staging
velero restore create monthly-test-restore --from-backup monthly-test
```

### 3. Restauration d'urgence

```bash
#!/bin/bash
# Identifier la dernière sauvegarde valide
LAST_BACKUP=$(velero backup get --output name | head -1)
# Restaurer
velero restore create emergency-restore --from-backup $LAST_BACKUP
```

````

### Étape 9.2 : Script de test DR
Créez `scripts/dr-test.sh` :

```bash
#!/bin/bash

set -e

NAMESPACE="dr-test"
BACKUP_NAME="dr-test-backup-$(date +%Y%m%d-%H%M%S)"

echo "Starting Disaster Recovery test..."

# 1. Créer un namespace de test avec des données
echo "Creating test environment..."
kubectl create namespace $NAMESPACE

kubectl run test-pod --image=nginx --namespace=$NAMESPACE
kubectl create configmap test-config --from-literal=key=value --namespace=$NAMESPACE

# Attendre que le pod soit prêt
kubectl wait --for=condition=ready pod/test-pod --namespace=$NAMESPACE --timeout=60s

# 2. Créer une sauvegarde
echo "Creating backup..."
velero backup create $BACKUP_NAME --include-namespaces $NAMESPACE

# Attendre la fin de la sauvegarde
velero backup wait $BACKUP_NAME

# 3. Simuler un désastre
echo "Simulating disaster..."
kubectl delete namespace $NAMESPACE

# Attendre que le namespace soit supprimé
kubectl wait --for=delete namespace/$NAMESPACE --timeout=60s

# 4. Tester la restauration
echo "Testing restore..."
velero restore create ${BACKUP_NAME}-restore --from-backup $BACKUP_NAME

# Attendre la fin de la restauration
velero restore wait ${BACKUP_NAME}-restore

# 5. Vérifier la restauration
echo "Verifying restore..."
kubectl wait --for=condition=ready pod/test-pod --namespace=$NAMESPACE --timeout=120s
kubectl get configmap test-config --namespace=$NAMESPACE

echo "DR test completed successfully!"

# Nettoyage
kubectl delete namespace $NAMESPACE
velero backup delete $BACKUP_NAME --confirm
velero restore delete ${BACKUP_NAME}-restore --confirm
````

### Étape 9.3 : Automatisation des tests

Créez `k8s/dr-test-cronjob.yaml` :

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dr-test
  namespace: velero
spec:
  # Tous les premiers du mois à 3h00
  schedule: '0 3 1 * *'
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: dr-test
              image: velero/velero:latest
              command:
                - /bin/bash
                - -c
                - |
                  # Script de test DR automatisé
                  echo "Running automated DR test..."

                  # Créer une sauvegarde de test
                  velero backup create dr-auto-test-$(date +%Y%m%d) \
                    --include-namespaces default \
                    --selector env=test

                  # Vérifier le succès
                  velero backup describe dr-auto-test-$(date +%Y%m%d)

                  echo "DR test completed"
              env:
                - name: VELERO_NAMESPACE
                  value: velero
              volumeMounts:
                - name: velero-config
                  mountPath: /etc/velero
          volumes:
            - name: velero-config
              secret:
                secretName: cloud-credentials
          restartPolicy: OnFailure
```

## Exercice 10 : Cas pratique complet

### Objectif

Implémenter une solution complète de backup et disaster recovery qui :

1. **Sauvegarde automatique** de toutes les applications critiques
2. **Tests réguliers** de restauration
3. **Monitoring** et alerting sur les échecs
4. **Documentation** des procédures DR
5. **Automation** des processus de récupération

### Tests à effectuer

1. **Sauvegarde complète** du cluster
2. **Restauration sélective** d'un namespace
3. **Migration** vers un autre cluster
4. **Test de performance** des sauvegardes
5. **Validation** de l'intégrité des données

## Questions de validation

1. Quelle est la différence entre snapshot et backup de volume ?
2. Comment gérer les hooks pour assurer la cohérence des données ?
3. Expliquez les concepts RTO et RPO dans le contexte Kubernetes
4. Comment automatiser les tests de disaster recovery ?
5. Quelles sont les bonnes pratiques pour la sécurité des sauvegardes ?

## Livrables attendus

1. **Velero installé** et configuré avec stockage objet
2. **Applications** avec données persistantes déployées
3. **Sauvegardes programmées** configurées
4. **Procédures de restauration** testées et documentées
5. **Hooks de sauvegarde** pour cohérence des données
6. **Monitoring** des sauvegardes avec alertes
7. **Plan de disaster recovery** complet
8. **Scripts d'automatisation** pour tests DR
9. **Documentation** des procédures d'urgence

## Critères d'évaluation

- **Installation** : Velero correctement configuré
- **Sauvegardes** : Planifications automatiques fonctionnelles
- **Restauration** : Procédures testées et validées
- **Monitoring** : Alertes et métriques en place
- **Automation** : Tests DR automatisés
- **Documentation** : Procédures claires et complètes

## Ressources utiles

- [Velero Documentation](https://velero.io/docs/)
- [Kubernetes Backup Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/backup/)
- [Disaster Recovery Strategies](https://cloud.google.com/architecture/dr-scenarios-planning-guide)

---

**Durée estimée : 8-9 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
