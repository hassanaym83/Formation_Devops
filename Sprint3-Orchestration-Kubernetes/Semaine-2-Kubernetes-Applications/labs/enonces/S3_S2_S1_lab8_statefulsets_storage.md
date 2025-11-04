# LAB 8 - StatefulSets et Stockage Persistant

## Objectif

Déployer et gérer des applications avec état (stateful) en utilisant StatefulSets et le stockage persistant.

## Contexte

Implémenter une solution complète pour applications stateful :

- Base de données PostgreSQL en cluster
- Système de fichiers distribué
- Gestion des volumes persistants
- Backup et restauration automatisés
- Monitoring des performances de stockage

## Prérequis

- Cluster Kubernetes avec CSI driver
- StorageClass configuré avec provisioning dynamique
- Opérateur de backup (Velero recommandé)
- Application e-commerce existante

## Instructions détaillées

### Étape 1 : Configuration des StorageClasses

1. Créer des StorageClasses optimisées :

```yaml
# storage-classes.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ssd-high-performance
provisioner: kubernetes.io/aws-ebs # Adapter selon votre provider
parameters:
  type: gp3
  iops: '3000'
  throughput: '125'
  encrypted: 'true'
allowVolumeExpansion: true
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ssd-standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  encrypted: 'true'
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: Immediate

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: hdd-backup
provisioner: kubernetes.io/aws-ebs
parameters:
  type: st1
  encrypted: 'true'
allowVolumeExpansion: true
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer

---
# Pour les environnements locaux (minikube/kind)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: rancher.io/local-path
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

### Étape 2 : Déploiement PostgreSQL avec StatefulSet

2. Configurer PostgreSQL en haute disponibilité :

```yaml
# postgres-statefulset.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
  namespace: ecommerce
data:
  postgresql.conf: |
    # Configuration pour haute performance
    shared_buffers = 256MB
    effective_cache_size = 1GB
    work_mem = 4MB
    maintenance_work_mem = 64MB

    # Configuration réplication
    wal_level = replica
    max_wal_senders = 3
    max_replication_slots = 3
    hot_standby = on

    # Logging
    log_statement = 'mod'
    log_min_duration_statement = 1000

    # Checkpoint
    checkpoint_completion_target = 0.9
    wal_buffers = 16MB

  pg_hba.conf: |
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    local   all             postgres                                peer
    host    all             postgres        0.0.0.0/0               md5
    host    replication     postgres        0.0.0.0/0               md5
    host    all             ecommerce       0.0.0.0/0               md5

---
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: ecommerce
type: Opaque
data:
  postgres-password: cG9zdGdyZXNfc3VwZXJfc2VjdXJl # postgres_super_secure (base64)
  ecommerce-password: ZWNvbW1lcmNlX3NlY3VyZQ== # ecommerce_secure (base64)

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
  namespace: ecommerce
  labels:
    app: postgres
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432

---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: ecommerce
  labels:
    app: postgres
spec:
  selector:
    app: postgres
    role: master
  ports:
    - port: 5432
      targetPort: 5432

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: ecommerce
spec:
  serviceName: postgres-headless
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      initContainers:
        - name: init-postgres
          image: postgres:15-alpine
          command:
            - sh
            - -c
            - |
              if [ ! -f /var/lib/postgresql/data/PG_VERSION ]; then
                if [ "$(hostname)" = "postgres-0" ]; then
                  echo "Initializing master database..."
                  initdb -D /var/lib/postgresql/data --auth-host=md5
                else
                  echo "Waiting for master to be ready..."
                  until pg_isready -h postgres-0.postgres-headless; do sleep 1; done
                  echo "Creating replica from master..."
                  pg_basebackup -h postgres-0.postgres-headless -U postgres -D /var/lib/postgresql/data -P -W
                fi
              fi
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: postgres-password
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: postgres-password
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: postgres-config
              mountPath: /etc/postgresql
      containers:
        - name: postgres
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: ecommerce
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: postgres-password
            - name: PGUSER
              value: postgres
            - name: POSTGRES_INITDB_ARGS
              value: '--auth-host=md5'
          command:
            - sh
            - -c
            - |
              if [ "$(hostname)" = "postgres-0" ]; then
                echo "Starting as master..."
                postgres -c config_file=/etc/postgresql/postgresql.conf
              else
                echo "Starting as replica..."
                postgres -c config_file=/etc/postgresql/postgresql.conf -c primary_conninfo="host=postgres-0.postgres-headless port=5432 user=postgres"
              fi
          resources:
            requests:
              memory: '512Mi'
              cpu: '250m'
            limits:
              memory: '1Gi'
              cpu: '500m'
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: postgres-config
              mountPath: /etc/postgresql
      volumes:
        - name: postgres-config
          configMap:
            name: postgres-config
  volumeClaimTemplates:
    - metadata:
        name: postgres-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-high-performance
        resources:
          requests:
            storage: 10Gi
```

### Étape 3 : Déploiement Redis Cluster avec StatefulSet

3. Configurer Redis en mode cluster :

```yaml
# redis-cluster.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: ecommerce
data:
  redis.conf: |
    # Redis Cluster Configuration
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 5000
    appendonly yes
    appendfsync everysec

    # Performance
    maxmemory 512mb
    maxmemory-policy allkeys-lru

    # Security
    requirepass redispassword
    masterauth redispassword

    # Networking
    bind 0.0.0.0
    protected-mode no
    port 6379

---
apiVersion: v1
kind: Service
metadata:
  name: redis-headless
  namespace: ecommerce
spec:
  clusterIP: None
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
      name: client
    - port: 16379
      targetPort: 16379
      name: gossip

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: ecommerce
spec:
  serviceName: redis-headless
  replicas: 6 # 3 masters + 3 replicas
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      initContainers:
        - name: init-redis
          image: redis:7-alpine
          command:
            - sh
            - -c
            - |
              cp /etc/redis/redis.conf /data/
              echo "cluster-announce-ip $(hostname -i)" >> /data/redis.conf
          volumeMounts:
            - name: redis-config
              mountPath: /etc/redis
            - name: redis-data
              mountPath: /data
      containers:
        - name: redis
          image: redis:7-alpine
          command:
            - redis-server
            - /data/redis.conf
          ports:
            - containerPort: 6379
              name: client
            - containerPort: 16379
              name: gossip
          resources:
            requests:
              memory: '256Mi'
              cpu: '100m'
            limits:
              memory: '512Mi'
              cpu: '200m'
          livenessProbe:
            exec:
              command:
                - redis-cli
                - -a
                - redispassword
                - ping
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - redis-cli
                - -a
                - redispassword
                - ping
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: redis-data
              mountPath: /data
      volumes:
        - name: redis-config
          configMap:
            name: redis-config
  volumeClaimTemplates:
    - metadata:
        name: redis-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-standard
        resources:
          requests:
            storage: 5Gi

---
# Job pour initialiser le cluster Redis
apiVersion: batch/v1
kind: Job
metadata:
  name: redis-cluster-init
  namespace: ecommerce
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: redis-cluster-init
          image: redis:7-alpine
          command:
            - sh
            - -c
            - |
              # Attendre que tous les pods soient prêts
              for i in $(seq 0 5); do
                until redis-cli -h redis-$i.redis-headless -a redispassword ping; do
                  sleep 1
                done
              done

              # Créer le cluster
              redis-cli -a redispassword --cluster create \
                redis-0.redis-headless:6379 \
                redis-1.redis-headless:6379 \
                redis-2.redis-headless:6379 \
                redis-3.redis-headless:6379 \
                redis-4.redis-headless:6379 \
                redis-5.redis-headless:6379 \
                --cluster-replicas 1 --cluster-yes
```

### Étape 4 : Système de fichiers distribué (MinIO)

4. Déployer MinIO pour le stockage d'objets :

```yaml
# minio-statefulset.yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
  namespace: ecommerce
type: Opaque
data:
  root-user: bWluaW9hZG1pbg== # minioadmin
  root-password: bWluaW9wYXNzd29yZA== # miniopassword

---
apiVersion: v1
kind: Service
metadata:
  name: minio-headless
  namespace: ecommerce
spec:
  clusterIP: None
  selector:
    app: minio
  ports:
    - port: 9000
      targetPort: 9000

---
apiVersion: v1
kind: Service
metadata:
  name: minio-service
  namespace: ecommerce
spec:
  selector:
    app: minio
  ports:
    - port: 9000
      targetPort: 9000
      name: api
    - port: 9001
      targetPort: 9001
      name: console

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
  namespace: ecommerce
spec:
  serviceName: minio-headless
  replicas: 4 # Cluster distribué
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
          command:
            - /bin/bash
            - -c
          args:
            - |
              minio server \
                http://minio-{0...3}.minio-headless.ecommerce.svc.cluster.local/data \
                --console-address ":9001"
          env:
            - name: MINIO_ROOT_USER
              valueFrom:
                secretKeyRef:
                  name: minio-secret
                  key: root-user
            - name: MINIO_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: minio-secret
                  key: root-password
            - name: MINIO_DISTRIBUTED_MODE_ENABLED
              value: 'yes'
            - name: MINIO_DISTRIBUTED_NODES
              value: 'minio-{0...3}.minio-headless.ecommerce.svc.cluster.local/data'
          ports:
            - containerPort: 9000
              name: api
            - containerPort: 9001
              name: console
          resources:
            requests:
              memory: '512Mi'
              cpu: '250m'
            limits:
              memory: '1Gi'
              cpu: '500m'
          livenessProbe:
            httpGet:
              path: /minio/health/live
              port: 9000
            initialDelaySeconds: 30
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /minio/health/ready
              port: 9000
            initialDelaySeconds: 10
            periodSeconds: 10
          volumeMounts:
            - name: minio-data
              mountPath: /data
  volumeClaimTemplates:
    - metadata:
        name: minio-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-standard
        resources:
          requests:
            storage: 20Gi
```

### Étape 5 : Backup et restauration automatisés

5. Configurer Velero pour les sauvegardes :

```yaml
# backup-configuration.yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-credentials
  namespace: velero
data:
  cloud: # Credentials selon votre provider cloud

---
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: default
  namespace: velero
spec:
  provider: aws # ou gcp, azure
  objectStorage:
    bucket: ecommerce-kubernetes-backups
    prefix: velero
  config:
    region: us-east-1
    s3ForcePathStyle: 'false'

---
# Backup quotidien des StatefulSets
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-statefulset-backup
  namespace: velero
spec:
  schedule: '0 2 * * *' # Tous les jours à 2h du matin
  template:
    includedNamespaces:
      - ecommerce
    includedResources:
      - statefulsets
      - persistentvolumes
      - persistentvolumeclaims
      - secrets
      - configmaps
    labelSelector:
      matchLabels:
        backup: 'enabled'
    ttl: 720h # 30 jours de rétention

---
# Backup avant mise à jour
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: pre-update-backup
  namespace: velero
spec:
  schedule: '0 1 * * 0' # Dimanche 1h du matin
  template:
    includedNamespaces:
      - ecommerce
    includedResources:
      - '*'
    ttl: 168h # 7 jours de rétention

---
# Script de backup manuel
apiVersion: v1
kind: ConfigMap
metadata:
  name: backup-scripts
  namespace: ecommerce
data:
  backup-postgres.sh: |
    #!/bin/bash

    NAMESPACE=${1:-ecommerce}
    BACKUP_NAME="postgres-$(date +%Y%m%d-%H%M%S)"

    echo "🗄️ Création backup PostgreSQL: $BACKUP_NAME"

    # Backup via Velero
    velero backup create $BACKUP_NAME \
      --include-namespaces $NAMESPACE \
      --include-resources statefulsets,pvc,secrets \
      --selector app=postgres \
      --wait

    # Backup logique de la base de données
    kubectl exec postgres-0 -n $NAMESPACE -- \
      pg_dumpall -U postgres > /tmp/postgres-dump-$(date +%Y%m%d).sql

    echo "✅ Backup terminé: $BACKUP_NAME"

  restore-postgres.sh: |
    #!/bin/bash

    BACKUP_NAME=$1
    NAMESPACE=${2:-ecommerce}

    if [ -z "$BACKUP_NAME" ]; then
      echo "Usage: $0 <backup_name> [namespace]"
      exit 1
    fi

    echo "🔄 Restauration PostgreSQL depuis: $BACKUP_NAME"

    # Arrêter l'application
    kubectl scale statefulset postgres --replicas=0 -n $NAMESPACE

    # Restaurer via Velero
    velero restore create --from-backup $BACKUP_NAME --wait

    # Redémarrer
    kubectl scale statefulset postgres --replicas=3 -n $NAMESPACE

    echo "✅ Restauration terminée"
```

### Étape 6 : Monitoring des performances de stockage

6. Configurer le monitoring des volumes :

```yaml
# storage-monitoring.yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: postgres-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: postgres-exporter
  endpoints:
    - port: metrics

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-exporter
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres-exporter
  template:
    metadata:
      labels:
        app: postgres-exporter
    spec:
      containers:
        - name: postgres-exporter
          image: prometheuscommunity/postgres-exporter:latest
          env:
            - name: DATA_SOURCE_NAME
              value: 'postgresql://postgres:$(POSTGRES_PASSWORD)@postgres-service:5432/?sslmode=disable'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: postgres-password
          ports:
            - containerPort: 9187
              name: metrics
          resources:
            requests:
              memory: '64Mi'
              cpu: '50m'
            limits:
              memory: '128Mi'
              cpu: '100m'

---
# Dashboard Grafana pour StatefulSets
apiVersion: v1
kind: ConfigMap
metadata:
  name: statefulset-dashboard
  namespace: monitoring
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "StatefulSets & Storage",
        "panels": [
          {
            "title": "PVC Usage",
            "type": "stat",
            "targets": [
              {
                "expr": "kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes * 100",
                "legendFormat": "{{persistentvolumeclaim}}"
              }
            ]
          },
          {
            "title": "PostgreSQL Connections",
            "type": "graph",
            "targets": [
              {
                "expr": "pg_stat_database_numbackends",
                "legendFormat": "{{datname}}"
              }
            ]
          },
          {
            "title": "PostgreSQL Query Duration",
            "type": "graph",
            "targets": [
              {
                "expr": "pg_stat_activity_max_tx_duration",
                "legendFormat": "Max Transaction Duration"
              }
            ]
          },
          {
            "title": "Redis Memory Usage",
            "type": "graph",
            "targets": [
              {
                "expr": "redis_memory_used_bytes",
                "legendFormat": "{{instance}}"
              }
            ]
          }
        ]
      }
    }
```

### Étape 7 : Tests de haute disponibilité

7. Scripts pour tester la résilience :

```bash
# test-statefulset-ha.sh
#!/bin/bash

echo "🧪 Tests de haute disponibilité des StatefulSets"

# Test 1: Redémarrage d'un pod PostgreSQL
echo "Test 1: Redémarrage PostgreSQL master..."
kubectl delete pod postgres-0 -n ecommerce
sleep 30

# Vérifier la récupération
kubectl wait --for=condition=Ready pod/postgres-0 -n ecommerce --timeout=300s
if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL master récupéré"
else
    echo "❌ Échec récupération PostgreSQL master"
fi

# Test 2: Simulation panne de nœud
echo "Test 2: Simulation panne de nœud..."
NODE=$(kubectl get pod postgres-1 -n ecommerce -o jsonpath='{.spec.nodeName}')
kubectl cordon $NODE
kubectl delete pod postgres-1 -n ecommerce

# Vérifier la migration
sleep 60
NEW_NODE=$(kubectl get pod postgres-1 -n ecommerce -o jsonpath='{.spec.nodeName}')
if [ "$NODE" != "$NEW_NODE" ]; then
    echo "✅ Pod migré vers nouveau nœud: $NEW_NODE"
else
    echo "❌ Pod non migré"
fi

# Réactiver le nœud
kubectl uncordon $NODE

# Test 3: Test de performance de stockage
echo "Test 3: Performance de stockage..."
kubectl exec postgres-0 -n ecommerce -- \
    pgbench -i -s 10 ecommerce
kubectl exec postgres-0 -n ecommerce -- \
    pgbench -c 10 -j 2 -t 1000 ecommerce

echo "🏁 Tests terminés"
```

## Critères de validation

- [ ] StatefulSets PostgreSQL et Redis déployés
- [ ] Volumes persistants correctement montés
- [ ] Réplication et clustering fonctionnels
- [ ] Backup automatique configuré
- [ ] Monitoring des performances actif
- [ ] Tests de haute disponibilité passés
- [ ] Procedures de restauration validées
- [ ] Documentation des opérations

## Tests pratiques

```bash
# Déploiement complet
kubectl apply -f storage-classes.yaml
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f redis-cluster.yaml
kubectl apply -f minio-statefulset.yaml

# Vérifier le statut
kubectl get statefulsets -n ecommerce
kubectl get pvc -n ecommerce

# Tester la persistance
kubectl exec postgres-0 -n ecommerce -- psql -U postgres -c "SELECT version();"

# Backup manuel
kubectl create job manual-backup --image=velero/velero:latest -- velero backup create manual-$(date +%s) --include-namespaces ecommerce

# Tests HA
bash test-statefulset-ha.sh
```

## Durée estimée

55 minutes
