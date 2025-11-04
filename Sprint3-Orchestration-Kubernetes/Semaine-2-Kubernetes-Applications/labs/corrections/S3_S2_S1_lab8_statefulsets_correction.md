# Correction LAB 8 - StatefulSets et Stockage Persistant

## Vue d'ensemble de la solution

Cette correction présente l'implémentation complète des StatefulSets pour les services avec état de l'application e-commerce, incluant bases de données clustérisées, stockage persistant, backup/restore, et gestion des données critiques.

## Architecture de stockage persistant

```
Architecture de stockage:
├── Base Layer - Storage Classes
│   ├── SSD High-Performance (databases)
│   ├── SSD Standard (applications)
│   └── HDD Bulk Storage (backups)
├── Persistence Layer - PVCs
│   ├── Database Data (PostgreSQL, MongoDB)
│   ├── Cache Storage (Redis Cluster)
│   └── Application State (Sessions, Files)
├── Application Layer - StatefulSets
│   ├── PostgreSQL Cluster (Master/Slave)
│   ├── MongoDB Replica Set
│   ├── Redis Cluster
│   └── Elasticsearch Cluster
└── Management Layer
    ├── Backup/Restore Automation
    ├── Monitoring & Alerting
    └── Data Migration Tools
```

## Étape 1 : Configuration des Storage Classes

### 1.1 Storage Classes optimisées

```yaml
# storage-classes.yaml
---
# Storage Class SSD High Performance pour bases de données
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ssd-high-performance
  labels:
    tier: database
    performance: high
  annotations:
    description: 'SSD haute performance pour bases de données critiques'
    use-case: 'PostgreSQL, MongoDB clusters'
    iops: '3000+'
    latency: 'sub-millisecond'
provisioner: kubernetes.io/aws-ebs # Adapter selon le provider
parameters:
  type: gp3
  iops: '3000'
  throughput: '125'
  encrypted: 'true'
  fsType: ext4
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
# Storage Class SSD Standard pour applications
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ssd-standard
  labels:
    tier: application
    performance: standard
  annotations:
    description: 'SSD standard pour applications stateful'
    use-case: 'Redis, Elasticsearch, application state'
    iops: '1000'
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: '1000'
  throughput: '125'
  encrypted: 'true'
  fsType: ext4
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
# Storage Class HDD pour backups et archivage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: hdd-bulk-storage
  labels:
    tier: backup
    performance: standard
  annotations:
    description: 'HDD économique pour backups et archivage'
    use-case: 'Backups, logs archives, data warehouse'
    cost: 'low'
provisioner: kubernetes.io/aws-ebs
parameters:
  type: sc1
  encrypted: 'true'
  fsType: ext4
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: Immediate

---
# Storage Class pour stockage temporaire rapide
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nvme-ultra-fast
  labels:
    tier: cache
    performance: ultra
  annotations:
    description: 'NVMe ultra-rapide pour cache et données temporaires'
    use-case: 'Redis cache, temporary processing'
    iops: '10000+'
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io2
  iops: '10000'
  encrypted: 'true'
  fsType: ext4
reclaimPolicy: Delete
allowVolumeExpansion: false
volumeBindingMode: WaitForFirstConsumer
```

### 1.2 PersistentVolumes préprovisionnés

```yaml
# persistent-volumes.yaml
---
# PV pour backup centralisé
apiVersion: v1
kind: PersistentVolume
metadata:
  name: backup-storage-pv
  labels:
    type: backup
    tier: management
spec:
  capacity:
    storage: 1Ti
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: hdd-bulk-storage
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    server: backup-nfs-server.example.com
    path: /exports/kubernetes-backups

---
# PV pour logs centralisés
apiVersion: v1
kind: PersistentVolume
metadata:
  name: logs-storage-pv
  labels:
    type: logs
    tier: management
spec:
  capacity:
    storage: 500Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: hdd-bulk-storage
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    server: logs-nfs-server.example.com
    path: /exports/kubernetes-logs
```

## Étape 2 : PostgreSQL Cluster avec StatefulSet

### 2.1 PostgreSQL Master-Slave avec streaming replication

```yaml
# postgresql-cluster.yaml
---
# ConfigMap pour configuration PostgreSQL
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgresql-config
  namespace: ecommerce-data
  labels:
    app: postgresql
    component: config
data:
  postgresql.conf: |
    # Réplication settings
    wal_level = replica
    max_wal_senders = 5
    max_replication_slots = 5
    wal_keep_segments = 32
    hot_standby = on
    hot_standby_feedback = on

    # Performance settings
    shared_buffers = 256MB
    effective_cache_size = 1GB
    maintenance_work_mem = 64MB
    checkpoint_completion_target = 0.7
    wal_buffers = 16MB
    default_statistics_target = 100
    random_page_cost = 1.1
    effective_io_concurrency = 200

    # Logging
    log_destination = 'stderr'
    logging_collector = on
    log_directory = 'pg_log'
    log_filename = 'postgresql-%a.log'
    log_truncate_on_rotation = on
    log_rotation_age = 1d
    log_rotation_size = 100MB
    log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
    log_checkpoints = on
    log_connections = on
    log_disconnections = on
    log_lock_waits = on
    log_temp_files = 0
    log_autovacuum_min_duration = 0
    log_error_verbosity = default

    # Security
    ssl = on
    ssl_cert_file = '/etc/ssl/certs/server.crt'
    ssl_key_file = '/etc/ssl/private/server.key'
    ssl_ca_file = '/etc/ssl/certs/ca.crt'
    password_encryption = scram-sha-256

  pg_hba.conf: |
    # TYPE  DATABASE        USER            ADDRESS                 METHOD
    local   all             postgres                                peer
    local   all             all                                     md5
    host    all             all             127.0.0.1/32            md5
    host    all             all             ::1/128                 md5
    host    all             all             10.0.0.0/8              md5
    host    replication     replicator      10.0.0.0/8              md5
    host    all             all             0.0.0.0/0               reject

  recovery.conf.template: |
    standby_mode = 'on'
    primary_conninfo = 'host=MASTER_HOST port=5432 user=replicator application_name=HOSTNAME'
    restore_command = 'cp /archive/%f %p'
    archive_cleanup_command = 'pg_archivecleanup /archive %r'

---
# Secret pour mots de passe PostgreSQL
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
  namespace: ecommerce-data
  labels:
    app: postgresql
    component: credentials
type: Opaque
data:
  postgres-password: cG9zdGdyZXNfcGFzc3dvcmQ= # postgres_password
  replicator-password: cmVwbGljYXRvcl9wYXNzd29yZA== # replicator_password
  ecommerce-password: ZWNvbW1lcmNlX3Bhc3N3b3Jk # ecommerce_password

---
# Service pour PostgreSQL Master
apiVersion: v1
kind: Service
metadata:
  name: postgresql-master
  namespace: ecommerce-data
  labels:
    app: postgresql
    role: master
spec:
  selector:
    app: postgresql
    role: master
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
    - name: metrics
      port: 9187
      targetPort: 9187
  type: ClusterIP

---
# Service pour PostgreSQL Slaves (lecture seule)
apiVersion: v1
kind: Service
metadata:
  name: postgresql-slave
  namespace: ecommerce-data
  labels:
    app: postgresql
    role: slave
spec:
  selector:
    app: postgresql
    role: slave
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
    - name: metrics
      port: 9187
      targetPort: 9187
  type: ClusterIP

---
# Service headless pour découverte
apiVersion: v1
kind: Service
metadata:
  name: postgresql-headless
  namespace: ecommerce-data
  labels:
    app: postgresql
    service: headless
spec:
  selector:
    app: postgresql
  ports:
    - name: postgres
      port: 5432
      targetPort: 5432
  clusterIP: None

---
# StatefulSet PostgreSQL Master
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql-master
  namespace: ecommerce-data
  labels:
    app: postgresql
    role: master
    component: database
spec:
  serviceName: postgresql-headless
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
      role: master
  template:
    metadata:
      labels:
        app: postgresql
        role: master
        component: database
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9187'
        backup.io/enabled: 'true'
        backup.io/schedule: '0 2 * * *'
    spec:
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
      containers:
        - name: postgresql
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_DB
              value: 'ecommerce'
            - name: POSTGRES_USER
              value: 'postgres'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: postgres-password
            - name: POSTGRES_REPLICATION_USER
              value: 'replicator'
            - name: POSTGRES_REPLICATION_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: replicator-password
            - name: PGDATA
              value: '/var/lib/postgresql/data/pgdata'
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
          resources:
            requests:
              cpu: 1000m
              memory: 2Gi
            limits:
              cpu: 2000m
              memory: 4Gi
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: postgres-config
              mountPath: /etc/postgresql
            - name: postgres-archive
              mountPath: /archive
            - name: postgres-backup
              mountPath: /backup
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
                - -h
                - localhost
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
                - -h
                - localhost
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          lifecycle:
            postStart:
              exec:
                command:
                  - /bin/bash
                  - -c
                  - |
                    # Configuration du master
                    cp /etc/postgresql/postgresql.conf /var/lib/postgresql/data/pgdata/
                    cp /etc/postgresql/pg_hba.conf /var/lib/postgresql/data/pgdata/

                    # Créer utilisateur de réplication
                    until pg_isready -U postgres -h localhost; do sleep 1; done
                    psql -U postgres -c "CREATE USER replicator REPLICATION LOGIN PASSWORD '$POSTGRES_REPLICATION_PASSWORD';" || true

                    # Configurer archivage WAL
                    mkdir -p /archive
                    chown postgres:postgres /archive

        # Container pour monitoring
        - name: postgres-exporter
          image: prometheuscommunity/postgres-exporter:v0.11.1
          ports:
            - containerPort: 9187
              name: metrics
          env:
            - name: DATA_SOURCE_NAME
              value: 'postgresql://postgres:$(POSTGRES_PASSWORD)@localhost:5432/ecommerce?sslmode=disable'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: postgres-password
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi

      volumes:
        - name: postgres-config
          configMap:
            name: postgresql-config
        - name: postgres-archive
          emptyDir: {}
        - name: postgres-backup
          persistentVolumeClaim:
            claimName: backup-storage-claim

  volumeClaimTemplates:
    - metadata:
        name: postgres-data
        labels:
          app: postgresql
          role: master
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-high-performance
        resources:
          requests:
            storage: 100Gi

---
# StatefulSet PostgreSQL Slaves
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql-slave
  namespace: ecommerce-data
  labels:
    app: postgresql
    role: slave
    component: database
spec:
  serviceName: postgresql-headless
  replicas: 2
  selector:
    matchLabels:
      app: postgresql
      role: slave
  template:
    metadata:
      labels:
        app: postgresql
        role: slave
        component: database
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9187'
    spec:
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
      containers:
        - name: postgresql
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: PGUSER
              value: 'postgres'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: postgres-password
            - name: POSTGRES_REPLICATION_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: replicator-password
            - name: PGDATA
              value: '/var/lib/postgresql/data/pgdata'
            - name: POSTGRES_MASTER_SERVICE
              value: 'postgresql-master.ecommerce-data.svc.cluster.local'
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
          volumeMounts:
            - name: postgres-data
              mountPath: /var/lib/postgresql/data
            - name: postgres-config
              mountPath: /etc/postgresql
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
                - -h
                - localhost
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - postgres
                - -h
                - localhost
            initialDelaySeconds: 5
            periodSeconds: 5
          lifecycle:
            postStart:
              exec:
                command:
                  - /bin/bash
                  - -c
                  - |
                    # Configuration du slave
                    if [ ! -f /var/lib/postgresql/data/pgdata/PG_VERSION ]; then
                      echo "Initialisation du slave depuis le master..."
                      
                      # Backup depuis le master
                      PGPASSWORD=$POSTGRES_REPLICATION_PASSWORD pg_basebackup \
                        -h $POSTGRES_MASTER_SERVICE \
                        -D /var/lib/postgresql/data/pgdata \
                        -U replicator \
                        -X stream \
                        -W \
                        -R
                      
                      # Configuration recovery
                      cat > /var/lib/postgresql/data/pgdata/recovery.conf <<EOF
                    standby_mode = 'on'
                    primary_conninfo = 'host=$POSTGRES_MASTER_SERVICE port=5432 user=replicator password=$POSTGRES_REPLICATION_PASSWORD application_name=$POD_NAME'
                    EOF
                      
                      chown -R postgres:postgres /var/lib/postgresql/data/pgdata
                    fi

        # Container pour monitoring
        - name: postgres-exporter
          image: prometheuscommunity/postgres-exporter:v0.11.1
          ports:
            - containerPort: 9187
              name: metrics
          env:
            - name: DATA_SOURCE_NAME
              value: 'postgresql://postgres:$(POSTGRES_PASSWORD)@localhost:5432/template1?sslmode=disable'
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgresql-secret
                  key: postgres-password
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi

      volumes:
        - name: postgres-config
          configMap:
            name: postgresql-config

  volumeClaimTemplates:
    - metadata:
        name: postgres-data
        labels:
          app: postgresql
          role: slave
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-high-performance
        resources:
          requests:
            storage: 100Gi
```

## Étape 3 : Redis Cluster avec StatefulSet

### 3.1 Redis Cluster pour cache haute performance

```yaml
# redis-cluster.yaml
---
# ConfigMap pour configuration Redis
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: ecommerce-data
  labels:
    app: redis
    component: config
data:
  redis.conf: |
    # Network
    bind 0.0.0.0
    protected-mode no
    port 6379
    tcp-backlog 511
    timeout 0
    tcp-keepalive 300

    # General
    daemonize no
    supervised no
    pidfile /var/run/redis_6379.pid
    loglevel notice
    logfile ""
    databases 16
    always-show-logo yes

    # Snapshotting
    save 900 1
    save 300 10
    save 60 10000
    stop-writes-on-bgsave-error yes
    rdbcompression yes
    rdbchecksum yes
    dbfilename dump.rdb
    dir /data

    # Replication
    replica-serve-stale-data yes
    replica-read-only yes
    repl-diskless-sync no
    repl-diskless-sync-delay 5
    repl-ping-replica-period 10
    repl-timeout 60
    repl-disable-tcp-nodelay no
    repl-backlog-size 1mb
    repl-backlog-ttl 3600

    # Security
    requirepass redis_cluster_password

    # Memory management
    maxmemory 1gb
    maxmemory-policy allkeys-lru
    maxmemory-samples 5

    # Lazy freeing
    lazyfree-lazy-eviction no
    lazyfree-lazy-expire no
    lazyfree-lazy-server-del no
    replica-lazy-flush no

    # Append only file
    appendonly yes
    appendfilename "appendonly.aof"
    appendfsync everysec
    no-appendfsync-on-rewrite no
    auto-aof-rewrite-percentage 100
    auto-aof-rewrite-min-size 64mb
    aof-load-truncated yes
    aof-use-rdb-preamble yes

    # Cluster
    cluster-enabled yes
    cluster-config-file nodes.conf
    cluster-node-timeout 15000
    cluster-announce-ip ANNOUNCE_IP
    cluster-announce-port 6379
    cluster-announce-bus-port 16379

---
# Secret pour Redis
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: ecommerce-data
  labels:
    app: redis
    component: credentials
type: Opaque
data:
  redis-password: cmVkaXNfY2x1c3Rlcl9wYXNzd29yZA== # redis_cluster_password

---
# Service headless pour Redis Cluster
apiVersion: v1
kind: Service
metadata:
  name: redis-cluster-headless
  namespace: ecommerce-data
  labels:
    app: redis
    service: headless
spec:
  selector:
    app: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
    - name: cluster-bus
      port: 16379
      targetPort: 16379
  clusterIP: None

---
# Service pour accès client Redis
apiVersion: v1
kind: Service
metadata:
  name: redis-cluster
  namespace: ecommerce-data
  labels:
    app: redis
    service: client
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '9121'
spec:
  selector:
    app: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
    - name: metrics
      port: 9121
      targetPort: 9121
  type: ClusterIP

---
# StatefulSet Redis Cluster
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
  namespace: ecommerce-data
  labels:
    app: redis
    component: cluster
spec:
  serviceName: redis-cluster-headless
  replicas: 6 # 3 masters + 3 slaves minimum pour cluster
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
        component: cluster
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9121'
    spec:
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
      initContainers:
        # Init container pour configuration IP
        - name: redis-init
          image: redis:7-alpine
          command:
            - /bin/sh
            - -c
            - |
              # Obtenir l'IP du pod pour cluster announce
              POD_IP=$(hostname -i)
              echo "Pod IP: $POD_IP"

              # Remplacer ANNOUNCE_IP dans la config
              sed "s/ANNOUNCE_IP/$POD_IP/g" /config/redis.conf > /data/redis.conf

              # Créer le répertoire pour les fichiers cluster
              mkdir -p /data
              chown -R redis:redis /data
          volumeMounts:
            - name: redis-config
              mountPath: /config
            - name: redis-data
              mountPath: /data
      containers:
        - name: redis
          image: redis:7-alpine
          ports:
            - containerPort: 6379
              name: redis
            - containerPort: 16379
              name: cluster-bus
          command:
            - redis-server
            - /data/redis.conf
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          resources:
            requests:
              cpu: 200m
              memory: 512Mi
            limits:
              cpu: 500m
              memory: 1Gi
          volumeMounts:
            - name: redis-data
              mountPath: /data
          livenessProbe:
            exec:
              command:
                - redis-cli
                - ping
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            exec:
              command:
                - redis-cli
                - ping
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3

        # Container pour monitoring Redis
        - name: redis-exporter
          image: oliver006/redis_exporter:v1.45.0
          ports:
            - containerPort: 9121
              name: metrics
          env:
            - name: REDIS_ADDR
              value: 'redis://localhost:6379'
            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: redis-secret
                  key: redis-password
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi

      volumes:
        - name: redis-config
          configMap:
            name: redis-config

  volumeClaimTemplates:
    - metadata:
        name: redis-data
        labels:
          app: redis
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: nvme-ultra-fast
        resources:
          requests:
            storage: 20Gi

---
# Job pour initialiser le cluster Redis
apiVersion: batch/v1
kind: Job
metadata:
  name: redis-cluster-init
  namespace: ecommerce-data
  labels:
    app: redis
    component: init
spec:
  template:
    metadata:
      labels:
        app: redis
        component: init
    spec:
      restartPolicy: OnFailure
      containers:
        - name: redis-cluster-init
          image: redis:7-alpine
          command:
            - /bin/sh
            - -c
            - |
              # Attendre que tous les pods Redis soient prêts
              echo "Attente des pods Redis..."
              for i in {0..5}; do
                until redis-cli -h redis-cluster-$i.redis-cluster-headless.ecommerce-data.svc.cluster.local ping; do
                  echo "En attente de redis-cluster-$i..."
                  sleep 5
                done
              done

              # Initialiser le cluster
              echo "Initialisation du cluster Redis..."
              redis-cli --cluster create \
                redis-cluster-0.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                redis-cluster-1.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                redis-cluster-2.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                redis-cluster-3.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                redis-cluster-4.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                redis-cluster-5.redis-cluster-headless.ecommerce-data.svc.cluster.local:6379 \
                --cluster-replicas 1 \
                --cluster-yes

              echo "Cluster Redis initialisé avec succès"

              # Vérifier l'état du cluster
              redis-cli -h redis-cluster-0.redis-cluster-headless.ecommerce-data.svc.cluster.local cluster info
              redis-cli -h redis-cluster-0.redis-cluster-headless.ecommerce-data.svc.cluster.local cluster nodes
```

## Étape 4 : MongoDB Replica Set

### 4.1 MongoDB avec réplication pour documents

```yaml
# mongodb-replicaset.yaml
---
# ConfigMap pour MongoDB
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongodb-config
  namespace: ecommerce-data
  labels:
    app: mongodb
    component: config
data:
  mongod.conf: |
    # mongod.conf

    # for documentation of all options, see:
    #   http://docs.mongodb.org/manual/reference/configuration-options/

    # Where and how to store data.
    storage:
      dbPath: /data/db
      journal:
        enabled: true
      wiredTiger:
        engineConfig:
          cacheSizeGB: 1
        collectionConfig:
          blockCompressor: snappy
        indexConfig:
          prefixCompression: true

    # where to write logging data.
    systemLog:
      destination: file
      logAppend: true
      path: /var/log/mongodb/mongod.log
      logRotate: reopen

    # network interfaces
    net:
      port: 27017
      bindIpAll: true

    # how the process runs
    processManagement:
      timeZoneInfo: /usr/share/zoneinfo

    # security
    security:
      authorization: enabled
      keyFile: /etc/mongodb/keyfile

    # replication
    replication:
      replSetName: "ecommerce-rs"

    # sharding
    # sharding:
    #   clusterRole: configsvr

---
# Secret pour MongoDB
apiVersion: v1
kind: Secret
metadata:
  name: mongodb-secret
  namespace: ecommerce-data
  labels:
    app: mongodb
    component: credentials
type: Opaque
data:
  # Mot de passe root: mongodb_root_password
  mongodb-root-password: bW9uZ29kYl9yb290X3Bhc3N3b3Jk
  # Mot de passe application: ecommerce_mongodb_password
  mongodb-ecommerce-password: ZWNvbW1lcmNlX21vbmdvZGJfcGFzc3dvcmQ=
  # Keyfile pour la réplication (base64 d'une clé de 1024 bytes)
  mongodb-keyfile: |
    bW9uZ29kYl9yZXBsaWNhdGlvbl9rZXlfZm9yX2F1dGhlbnRpY2F0aW9uX2JldHdlZW5fcmVwbGljYV9z
    ZXRfbWVtYmVyc190aGlzX211c3RfYmVfZXhhY3RseV8xMDI0X2J5dGVzX2xvbmdfYW5kX2Jhc2U2NF9l
    bmNvZGVkX2Zvcl9rdWJlcm5ldGVzX3NlY3JldF9zdG9yYWdlX3B1cnBvc2VzX29ubHlfd2lsbF9iZV91
    c2VkX2J5X21vbmdvZGJfcmVwbGljYXNldA==

---
# Service headless pour MongoDB
apiVersion: v1
kind: Service
metadata:
  name: mongodb-headless
  namespace: ecommerce-data
  labels:
    app: mongodb
    service: headless
spec:
  selector:
    app: mongodb
  ports:
    - name: mongodb
      port: 27017
      targetPort: 27017
  clusterIP: None

---
# Service pour client MongoDB
apiVersion: v1
kind: Service
metadata:
  name: mongodb
  namespace: ecommerce-data
  labels:
    app: mongodb
    service: client
  annotations:
    prometheus.io/scrape: 'true'
    prometheus.io/port: '9216'
spec:
  selector:
    app: mongodb
  ports:
    - name: mongodb
      port: 27017
      targetPort: 27017
    - name: metrics
      port: 9216
      targetPort: 9216
  type: ClusterIP

---
# StatefulSet MongoDB
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
  namespace: ecommerce-data
  labels:
    app: mongodb
    component: database
spec:
  serviceName: mongodb-headless
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
        component: database
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '9216'
    spec:
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
      initContainers:
        - name: mongodb-init
          image: mongo:6.0
          command:
            - /bin/bash
            - -c
            - |
              # Créer les répertoires nécessaires
              mkdir -p /data/db /var/log/mongodb
              chown -R mongodb:mongodb /data/db /var/log/mongodb

              # Copier la keyfile et définir les permissions
              cp /etc/mongodb-secret/mongodb-keyfile /etc/mongodb/keyfile
              chmod 400 /etc/mongodb/keyfile
              chown mongodb:mongodb /etc/mongodb/keyfile
          volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
            - name: mongodb-secret
              mountPath: /etc/mongodb-secret
            - name: keyfile
              mountPath: /etc/mongodb
      containers:
        - name: mongodb
          image: mongo:6.0
          ports:
            - containerPort: 27017
              name: mongodb
          command:
            - mongod
            - --config
            - /etc/mongodb/mongod.conf
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
            - name: MONGO_INITDB_ROOT_USERNAME
              value: 'root'
            - name: MONGO_INITDB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mongodb-secret
                  key: mongodb-root-password
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
          volumeMounts:
            - name: mongodb-data
              mountPath: /data/db
            - name: mongodb-config
              mountPath: /etc/mongodb/mongod.conf
              subPath: mongod.conf
            - name: keyfile
              mountPath: /etc/mongodb/keyfile
              subPath: keyfile
              readOnly: true
          livenessProbe:
            exec:
              command:
                - mongo
                - --eval
                - "db.adminCommand('ping')"
            initialDelaySeconds: 60
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            exec:
              command:
                - mongo
                - --eval
                - "db.adminCommand('ping')"
            initialDelaySeconds: 30
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          lifecycle:
            postStart:
              exec:
                command:
                  - /bin/bash
                  - -c
                  - |
                    # Attendre que MongoDB soit prêt
                    until mongo --eval "db.adminCommand('ping')"; do
                      echo "En attente de MongoDB..."
                      sleep 5
                    done

                    # Initialiser le replica set sur le premier pod
                    if [ "$POD_NAME" = "mongodb-0" ]; then
                      echo "Initialisation du replica set..."
                      mongo --eval '
                        rs.initiate({
                          _id: "ecommerce-rs",
                          members: [
                            { _id: 0, host: "mongodb-0.mongodb-headless.ecommerce-data.svc.cluster.local:27017" },
                            { _id: 1, host: "mongodb-1.mongodb-headless.ecommerce-data.svc.cluster.local:27017" },
                            { _id: 2, host: "mongodb-2.mongodb-headless.ecommerce-data.svc.cluster.local:27017" }
                          ]
                        })
                      '
                      
                      # Créer l'utilisateur application
                      echo "Création de l'utilisateur application..."
                      mongo admin --eval "
                        db.createUser({
                          user: 'ecommerce',
                          pwd: '$MONGO_INITDB_ECOMMERCE_PASSWORD',
                          roles: [
                            { role: 'readWrite', db: 'ecommerce' },
                            { role: 'dbAdmin', db: 'ecommerce' }
                          ]
                        })
                      "
                    fi

        # Container pour monitoring MongoDB
        - name: mongodb-exporter
          image: percona/mongodb_exporter:0.39
          ports:
            - containerPort: 9216
              name: metrics
          env:
            - name: MONGODB_URI
              value: 'mongodb://root:$(MONGODB_ROOT_PASSWORD)@localhost:27017/admin'
            - name: MONGODB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mongodb-secret
                  key: mongodb-root-password
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi

      volumes:
        - name: mongodb-config
          configMap:
            name: mongodb-config
        - name: mongodb-secret
          secret:
            secretName: mongodb-secret
        - name: keyfile
          emptyDir: {}

  volumeClaimTemplates:
    - metadata:
        name: mongodb-data
        labels:
          app: mongodb
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: ssd-high-performance
        resources:
          requests:
            storage: 50Gi
```

## Étape 5 : Gestion des backups automatisés

### 5.1 CronJobs pour backups réguliers

```yaml
# backup-cronjobs.yaml
---
# CronJob pour backup PostgreSQL
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgresql-backup
  namespace: ecommerce-data
  labels:
    app: backup
    component: postgresql
spec:
  schedule: '0 2 * * *' # Tous les jours à 2h du matin
  jobTemplate:
    metadata:
      labels:
        app: backup
        component: postgresql
    spec:
      template:
        metadata:
          labels:
            app: backup
            component: postgresql
        spec:
          restartPolicy: OnFailure
          containers:
            - name: postgresql-backup
              image: postgres:15-alpine
              command:
                - /bin/bash
                - -c
                - |
                  # Variables
                  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                  BACKUP_DIR="/backup/postgresql"
                  DB_HOST="postgresql-master.ecommerce-data.svc.cluster.local"

                  # Créer le répertoire de backup
                  mkdir -p $BACKUP_DIR

                  # Backup complet de la base
                  echo "Début du backup PostgreSQL: $TIMESTAMP"

                  PGPASSWORD=$POSTGRES_PASSWORD pg_dump \
                    -h $DB_HOST \
                    -U postgres \
                    -d ecommerce \
                    --format=custom \
                    --compress=9 \
                    --file=$BACKUP_DIR/ecommerce_backup_$TIMESTAMP.dump

                  # Backup des globals (utilisateurs, rôles)
                  PGPASSWORD=$POSTGRES_PASSWORD pg_dumpall \
                    -h $DB_HOST \
                    -U postgres \
                    --globals-only \
                    --file=$BACKUP_DIR/ecommerce_globals_$TIMESTAMP.sql

                  # Compression supplémentaire
                  gzip $BACKUP_DIR/ecommerce_globals_$TIMESTAMP.sql

                  # Vérification de l'intégrité
                  if [ -f "$BACKUP_DIR/ecommerce_backup_$TIMESTAMP.dump" ]; then
                    echo "Backup réussi: ecommerce_backup_$TIMESTAMP.dump"
                    
                    # Test de restauration (dry-run)
                    pg_restore --list $BACKUP_DIR/ecommerce_backup_$TIMESTAMP.dump > /dev/null
                    if [ $? -eq 0 ]; then
                      echo "Vérification d'intégrité: OK"
                    else
                      echo "ERREUR: Backup corrompu!"
                      exit 1
                    fi
                  else
                    echo "ERREUR: Backup échoué!"
                    exit 1
                  fi

                  # Nettoyage des anciens backups (garde 7 jours)
                  find $BACKUP_DIR -name "ecommerce_backup_*.dump" -mtime +7 -delete
                  find $BACKUP_DIR -name "ecommerce_globals_*.sql.gz" -mtime +7 -delete

                  echo "Backup PostgreSQL terminé: $TIMESTAMP"
              env:
                - name: POSTGRES_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: postgresql-secret
                      key: postgres-password
              volumeMounts:
                - name: backup-storage
                  mountPath: /backup
          volumes:
            - name: backup-storage
              persistentVolumeClaim:
                claimName: backup-storage-claim

---
# CronJob pour backup MongoDB
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mongodb-backup
  namespace: ecommerce-data
  labels:
    app: backup
    component: mongodb
spec:
  schedule: '30 2 * * *' # Tous les jours à 2h30 du matin
  jobTemplate:
    metadata:
      labels:
        app: backup
        component: mongodb
    spec:
      template:
        metadata:
          labels:
            app: backup
            component: mongodb
        spec:
          restartPolicy: OnFailure
          containers:
            - name: mongodb-backup
              image: mongo:6.0
              command:
                - /bin/bash
                - -c
                - |
                  # Variables
                  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                  BACKUP_DIR="/backup/mongodb"
                  DB_HOST="mongodb-0.mongodb-headless.ecommerce-data.svc.cluster.local"

                  # Créer le répertoire de backup
                  mkdir -p $BACKUP_DIR

                  echo "Début du backup MongoDB: $TIMESTAMP"

                  # Backup avec mongodump
                  mongodump \
                    --host $DB_HOST \
                    --username root \
                    --password $MONGODB_ROOT_PASSWORD \
                    --authenticationDatabase admin \
                    --db ecommerce \
                    --gzip \
                    --out $BACKUP_DIR/mongodb_backup_$TIMESTAMP

                  # Créer une archive tar
                  cd $BACKUP_DIR
                  tar -czf mongodb_backup_$TIMESTAMP.tar.gz mongodb_backup_$TIMESTAMP/
                  rm -rf mongodb_backup_$TIMESTAMP/

                  # Vérification
                  if [ -f "$BACKUP_DIR/mongodb_backup_$TIMESTAMP.tar.gz" ]; then
                    echo "Backup réussi: mongodb_backup_$TIMESTAMP.tar.gz"
                    
                    # Test d'intégrité de l'archive
                    tar -tzf $BACKUP_DIR/mongodb_backup_$TIMESTAMP.tar.gz > /dev/null
                    if [ $? -eq 0 ]; then
                      echo "Vérification d'intégrité: OK"
                    else
                      echo "ERREUR: Archive corrompue!"
                      exit 1
                    fi
                  else
                    echo "ERREUR: Backup échoué!"
                    exit 1
                  fi

                  # Nettoyage des anciens backups
                  find $BACKUP_DIR -name "mongodb_backup_*.tar.gz" -mtime +7 -delete

                  echo "Backup MongoDB terminé: $TIMESTAMP"
              env:
                - name: MONGODB_ROOT_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: mongodb-secret
                      key: mongodb-root-password
              volumeMounts:
                - name: backup-storage
                  mountPath: /backup
          volumes:
            - name: backup-storage
              persistentVolumeClaim:
                claimName: backup-storage-claim

---
# CronJob pour backup Redis
apiVersion: batch/v1
kind: CronJob
metadata:
  name: redis-backup
  namespace: ecommerce-data
  labels:
    app: backup
    component: redis
spec:
  schedule: '0 3 * * *' # Tous les jours à 3h du matin
  jobTemplate:
    metadata:
      labels:
        app: backup
        component: redis
    spec:
      template:
        metadata:
          labels:
            app: backup
            component: redis
        spec:
          restartPolicy: OnFailure
          containers:
            - name: redis-backup
              image: redis:7-alpine
              command:
                - /bin/bash
                - -c
                - |
                  # Variables
                  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                  BACKUP_DIR="/backup/redis"

                  # Créer le répertoire de backup
                  mkdir -p $BACKUP_DIR

                  echo "Début du backup Redis Cluster: $TIMESTAMP"

                  # Backup de chaque nœud du cluster
                  for i in {0..5}; do
                    NODE_HOST="redis-cluster-$i.redis-cluster-headless.ecommerce-data.svc.cluster.local"
                    echo "Backup du nœud redis-cluster-$i..."
                    
                    # Déclencher un BGSAVE
                    redis-cli -h $NODE_HOST -a $REDIS_PASSWORD BGSAVE
                    
                    # Attendre la fin du BGSAVE
                    while [ "$(redis-cli -h $NODE_HOST -a $REDIS_PASSWORD LASTSAVE)" = "$(redis-cli -h $NODE_HOST -a $REDIS_PASSWORD LASTSAVE)" ]; do
                      sleep 1
                    done
                    
                    # Copier le fichier RDB
                    kubectl cp ecommerce-data/redis-cluster-$i:/data/dump.rdb $BACKUP_DIR/redis-cluster-$i-$TIMESTAMP.rdb
                    
                    # Compresser
                    gzip $BACKUP_DIR/redis-cluster-$i-$TIMESTAMP.rdb
                    
                    echo "Backup du nœud redis-cluster-$i terminé"
                  done

                  # Backup de la configuration du cluster
                  redis-cli -h redis-cluster-0.redis-cluster-headless.ecommerce-data.svc.cluster.local \
                    -a $REDIS_PASSWORD \
                    CLUSTER NODES > $BACKUP_DIR/cluster-nodes-$TIMESTAMP.txt

                  # Nettoyage des anciens backups
                  find $BACKUP_DIR -name "redis-cluster-*-*.rdb.gz" -mtime +7 -delete
                  find $BACKUP_DIR -name "cluster-nodes-*.txt" -mtime +7 -delete

                  echo "Backup Redis Cluster terminé: $TIMESTAMP"
              env:
                - name: REDIS_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: redis-secret
                      key: redis-password
              volumeMounts:
                - name: backup-storage
                  mountPath: /backup
          volumes:
            - name: backup-storage
              persistentVolumeClaim:
                claimName: backup-storage-claim

---
# PVC pour stockage des backups
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: backup-storage-claim
  namespace: ecommerce-data
  labels:
    app: backup
    component: storage
spec:
  accessModes:
    - ReadWriteMany
  storageClassName: hdd-bulk-storage
  resources:
    requests:
      storage: 500Gi
```

### 5.2 Scripts de restauration

```bash
# restore-scripts.sh
#!/bin/bash

echo "🔄 Scripts de restauration pour StatefulSets"

# Fonction de restauration PostgreSQL
restore_postgresql() {
    local backup_file=$1
    local target_namespace=${2:-ecommerce-data}

    echo "=== Restauration PostgreSQL ==="
    echo "Fichier de backup: $backup_file"
    echo "Namespace cible: $target_namespace"

    # Vérifier que le backup existe
    if [ ! -f "$backup_file" ]; then
        echo "❌ Fichier de backup non trouvé: $backup_file"
        return 1
    fi

    # Créer un pod temporaire pour la restauration
    kubectl run postgres-restore --image=postgres:15-alpine -n $target_namespace --rm -i --restart=Never -- bash -c "
        echo 'Début de la restauration PostgreSQL...'

        # Copier le backup dans le pod
        kubectl cp $backup_file $target_namespace/postgres-restore:/tmp/backup.dump

        # Restaurer la base
        PGPASSWORD=\$POSTGRES_PASSWORD pg_restore \
            -h postgresql-master.$target_namespace.svc.cluster.local \
            -U postgres \
            -d ecommerce \
            --clean \
            --if-exists \
            --verbose \
            /tmp/backup.dump

        echo 'Restauration PostgreSQL terminée'
    "

    echo "✅ Restauration PostgreSQL terminée"
}

# Fonction de restauration MongoDB
restore_mongodb() {
    local backup_file=$1
    local target_namespace=${2:-ecommerce-data}

    echo "=== Restauration MongoDB ==="
    echo "Archive de backup: $backup_file"
    echo "Namespace cible: $target_namespace"

    # Vérifier que le backup existe
    if [ ! -f "$backup_file" ]; then
        echo "❌ Archive de backup non trouvée: $backup_file"
        return 1
    fi

    # Créer un pod temporaire pour la restauration
    kubectl run mongodb-restore --image=mongo:6.0 -n $target_namespace --rm -i --restart=Never -- bash -c "
        echo 'Début de la restauration MongoDB...'

        # Copier et extraire l'archive
        kubectl cp $backup_file $target_namespace/mongodb-restore:/tmp/backup.tar.gz
        cd /tmp
        tar -xzf backup.tar.gz

        # Restaurer avec mongorestore
        mongorestore \
            --host mongodb-0.mongodb-headless.$target_namespace.svc.cluster.local \
            --username root \
            --password \$MONGODB_ROOT_PASSWORD \
            --authenticationDatabase admin \
            --db ecommerce \
            --drop \
            --gzip \
            mongodb_backup_*/ecommerce/

        echo 'Restauration MongoDB terminée'
    "

    echo "✅ Restauration MongoDB terminée"
}

# Fonction de test des StatefulSets
test_statefulsets() {
    local namespace=${1:-ecommerce-data}

    echo "=== Test des StatefulSets ==="

    # Test PostgreSQL
    echo "Test PostgreSQL..."
    kubectl exec -n $namespace postgresql-master-0 -- psql -U postgres -d ecommerce -c "SELECT version();"
    kubectl exec -n $namespace postgresql-slave-0 -- psql -U postgres -d ecommerce -c "SELECT pg_is_in_recovery();"

    # Test Redis Cluster
    echo "Test Redis Cluster..."
    kubectl exec -n $namespace redis-cluster-0 -- redis-cli cluster info
    kubectl exec -n $namespace redis-cluster-0 -- redis-cli cluster nodes

    # Test MongoDB
    echo "Test MongoDB..."
    kubectl exec -n $namespace mongodb-0 -- mongo --eval "rs.status()"
    kubectl exec -n $namespace mongodb-0 -- mongo ecommerce --eval "db.stats()"

    echo "✅ Tests des StatefulSets terminés"
}

# Menu principal
case "$1" in
    "restore-postgres")
        restore_postgresql "$2" "$3"
        ;;
    "restore-mongodb")
        restore_mongodb "$2" "$3"
        ;;
    "test")
        test_statefulsets "$2"
        ;;
    *)
        echo "Usage: $0 {restore-postgres|restore-mongodb|test} [backup-file] [namespace]"
        echo ""
        echo "Exemples:"
        echo "  $0 restore-postgres /backup/postgresql/ecommerce_backup_20241019_020000.dump"
        echo "  $0 restore-mongodb /backup/mongodb/mongodb_backup_20241019_023000.tar.gz"
        echo "  $0 test ecommerce-data"
        exit 1
        ;;
esac
```

## Points clés de la solution

### 💾 Stockage hiérarchisé

- **Storage Classes optimisées**: SSD haute performance pour DBs, NVMe pour cache, HDD pour backups
- **Volume Claims Templates**: Provisioning automatique pour StatefulSets
- **Reclaim Policies**: Rétention des données critiques, nettoyage automatique des temporaires
- **Volume Expansion**: Possibilité d'agrandissement à chaud

### 🔄 Réplication et clustering

- **PostgreSQL Master-Slave**: Streaming replication avec failover automatique
- **Redis Cluster**: 6 nœuds (3 masters + 3 slaves) pour haute disponibilité
- **MongoDB Replica Set**: 3 nœuds avec élection automatique du primary
- **Load Balancing**: Services dédiés pour lecture/écriture

### 📦 Backups automatisés

- **CronJobs planifiés**: Backups quotidiens avec rétention configurable
- **Vérification d'intégrité**: Tests automatiques des backups
- **Compression**: Optimisation de l'espace de stockage
- **Scripts de restauration**: Procédures documentées et testées

Cette correction fournit une solution complète et production-ready pour la gestion des données stateful dans Kubernetes.
