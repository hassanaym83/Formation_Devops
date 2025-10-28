# LAB 7 - Volumes et persistance

## Objectifs

- Maîtriser les différents types de volumes Kubernetes
- Implémenter la persistance de données avec PersistentVolumes
- Gérer le stockage dynamique avec StorageClasses
- Comprendre le cycle de vie des données

## Contexte

Gestion de la persistance des données pour applications stateful et bases de données.

## Prérequis

- Cluster Kubernetes fonctionnel
- Connaissance des deployments et secrets

## Instructions

### 1. Volumes éphémères - emptyDir

```yaml
# Créer le fichier volume-emptydir.yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp-emptydir
spec:
  containers:
    - name: webapp
      image: nginx:1.21
      volumeMounts:
        - name: cache-volume
          mountPath: /var/cache/nginx
        - name: shared-logs
          mountPath: /var/log/nginx
    - name: log-processor
      image: busybox
      command:
        [
          'sh',
          '-c',
          'while true; do echo $(date) >> /var/log/nginx/processed.log; sleep 30; done'
        ]
      volumeMounts:
        - name: shared-logs
          mountPath: /var/log/nginx
  volumes:
    - name: cache-volume
      emptyDir: {}
    - name: shared-logs
      emptyDir:
        sizeLimit: 1Gi
```

```bash
# Déployer le pod
kubectl apply -f volume-emptydir.yaml

# Vérifier les volumes
kubectl describe pod webapp-emptydir
kubectl exec -it webapp-emptydir -c webapp -- df -h
kubectl exec -it webapp-emptydir -c webapp -- ls -la /var/log/nginx/

# Observer le partage entre conteneurs
kubectl exec -it webapp-emptydir -c log-processor -- cat /var/log/nginx/processed.log
```

### 2. Volumes host - hostPath (pour développement uniquement)

```yaml
# Créer le fichier volume-hostpath.yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp-hostpath
spec:
  containers:
    - name: webapp
      image: nginx:1.21
      volumeMounts:
        - name: host-storage
          mountPath: /usr/share/nginx/html
      ports:
        - containerPort: 80
  volumes:
    - name: host-storage
      hostPath:
        path: /tmp/webapp-data
        type: DirectoryOrCreate
```

```bash
# Créer le répertoire sur le node minikube
minikube ssh "sudo mkdir -p /tmp/webapp-data"
minikube ssh "echo '<h1>Hello from Host Volume!</h1>' | sudo tee /tmp/webapp-data/index.html"

# Déployer le pod
kubectl apply -f volume-hostpath.yaml

# Tester l'accès
kubectl port-forward webapp-hostpath 8080:80 &
curl http://localhost:8080

# Modifier depuis le host et observer
minikube ssh "echo '<h1>Modified from Host!</h1>' | sudo tee /tmp/webapp-data/index.html"
curl http://localhost:8080
```

### 3. PersistentVolumes et PersistentVolumeClaims

```yaml
# Créer le fichier persistent-volumes.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: webapp-pv
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /tmp/pv-data

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: webapp-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: manual

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-with-pvc
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-pvc
  template:
    metadata:
      labels:
        app: webapp-pvc
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          volumeMounts:
            - name: webapp-storage
              mountPath: /usr/share/nginx/html
          ports:
            - containerPort: 80
      volumes:
        - name: webapp-storage
          persistentVolumeClaim:
            claimName: webapp-pvc
```

```bash
# Créer le répertoire PV sur minikube
minikube ssh "sudo mkdir -p /tmp/pv-data"

# Appliquer la configuration
kubectl apply -f persistent-volumes.yaml

# Vérifier le binding PV/PVC
kubectl get pv
kubectl get pvc
kubectl describe pvc webapp-pvc

# Tester la persistance
kubectl exec -it deployment/webapp-with-pvc -- bash -c "echo '<h1>Persistent Data</h1>' > /usr/share/nginx/html/index.html"

# Supprimer et recréer le pod
kubectl delete pod -l app=webapp-pvc
kubectl get pods -l app=webapp-pvc

# Vérifier que les données persistent
kubectl exec -it deployment/webapp-with-pvc -- cat /usr/share/nginx/html/index.html
```

### 4. StorageClass et provisioning dynamique

```yaml
# Créer le fichier storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-storage
provisioner: k8s.io/minikube-hostpath
parameters:
  type: pd-ssd
reclaimPolicy: Delete
allowVolumeExpansion: true

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: dynamic-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: fast-storage

---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: webapp-statefulset
spec:
  serviceName: webapp-svc
  replicas: 2
  selector:
    matchLabels:
      app: webapp-stateful
  template:
    metadata:
      labels:
        app: webapp-stateful
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          volumeMounts:
            - name: webapp-data
              mountPath: /usr/share/nginx/html
          ports:
            - containerPort: 80
  volumeClaimTemplates:
    - metadata:
        name: webapp-data
      spec:
        accessModes: ['ReadWriteOnce']
        storageClassName: fast-storage
        resources:
          requests:
            storage: 500Mi
```

```bash
# Vérifier les StorageClasses disponibles
kubectl get storageclass

# Appliquer la configuration
kubectl apply -f storage-class.yaml

# Observer le provisioning automatique
kubectl get pvc
kubectl get pv
kubectl describe statefulset webapp-statefulset
```

### 5. Base de données avec persistance

```yaml
# Créer le fichier mysql-persistent.yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
type: Opaque
data:
  # echo -n "rootpassword" | base64
  mysql-root-password: cm9vdHBhc3N3b3Jk
  # echo -n "myapp" | base64
  mysql-database: bXlhcHA=
  # echo -n "appuser" | base64
  mysql-user: YXBwdXNlcg==
  # echo -n "apppassword" | base64
  mysql-password: YXBwcGFzc3dvcmQ=

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8.0
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: mysql-root-password
            - name: MYSQL_DATABASE
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: mysql-database
            - name: MYSQL_USER
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: mysql-user
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: mysql-password
          ports:
            - containerPort: 3306
          volumeMounts:
            - name: mysql-storage
              mountPath: /var/lib/mysql
          livenessProbe:
            exec:
              command:
                - mysqladmin
                - ping
                - -h
                - localhost
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - mysql
                - -h
                - localhost
                - -u
                - root
                - -p$(MYSQL_ROOT_PASSWORD)
                - -e
                - 'SELECT 1'
            initialDelaySeconds: 5
            periodSeconds: 2
      volumes:
        - name: mysql-storage
          persistentVolumeClaim:
            claimName: mysql-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  selector:
    app: mysql
  ports:
    - port: 3306
      targetPort: 3306
  type: ClusterIP
```

```bash
# Déployer MySQL avec persistance
kubectl apply -f mysql-persistent.yaml

# Attendre que MySQL soit prêt
kubectl wait --for=condition=ready pod -l app=mysql --timeout=300s

# Tester la connexion à la base
kubectl run mysql-client --image=mysql:8.0 -it --rm --restart=Never -- \
  mysql -h mysql-service -u appuser -papppassword myapp

# Dans le client MySQL :
# CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(50));
# INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob');
# SELECT * FROM users;
# exit

# Supprimer le pod MySQL pour tester la persistance
kubectl delete pod -l app=mysql

# Attendre le redémarrage et retester
kubectl wait --for=condition=ready pod -l app=mysql --timeout=300s
kubectl run mysql-client --image=mysql:8.0 -it --rm --restart=Never -- \
  mysql -h mysql-service -u appuser -papppassword -e "SELECT * FROM users;" myapp
```

### 6. Backup et restauration

```bash
# Créer un job de backup
kubectl run mysql-backup --image=mysql:8.0 --restart=OnFailure -- \
  bash -c "mysqldump -h mysql-service -u appuser -papppassword myapp > /tmp/backup.sql && cat /tmp/backup.sql"

# Vérifier les logs du backup
kubectl logs mysql-backup

# Simulation de restauration
kubectl run mysql-restore --image=mysql:8.0 -it --rm --restart=Never -- \
  bash -c "echo 'CREATE TABLE test (id INT);' | mysql -h mysql-service -u appuser -papppassword myapp"
```

### 7. Gestion des volumes et nettoyage

```bash
# Analyser l'utilisation du stockage
kubectl describe pvc
kubectl get pv -o custom-columns=NAME:.metadata.name,SIZE:.spec.capacity.storage,STATUS:.status.phase

# Étendre un PVC (si supporté par la StorageClass)
kubectl patch pvc dynamic-pvc -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'

# Nettoyage
kubectl delete deployment webapp-with-pvc mysql
kubectl delete pvc webapp-pvc mysql-pvc dynamic-pvc
kubectl delete pv webapp-pv
kubectl delete pod webapp-emptydir webapp-hostpath
```

## Livrables attendus

1. Pods avec différents types de volumes
2. PersistentVolume et PersistentVolumeClaim fonctionnels
3. Base de données MySQL avec données persistantes
4. Test de backup/restauration
5. Documentation des observations sur la persistance

## Critères de validation

- [ ] Volume emptyDir partagé entre conteneurs
- [ ] HostPath fonctionnel (développement uniquement)
- [ ] PVC binding réussi avec PV
- [ ] Provisioning dynamique avec StorageClass
- [ ] MySQL avec données persistantes après redémarrage
- [ ] Backup et vérification de la restauration

## Durée estimée

35 minutes

## Types de volumes Kubernetes

### Volumes éphémères

- **emptyDir** : Partagé entre conteneurs du même pod
- **configMap/secret** : Configuration montée comme fichiers

### Volumes persistants

- **hostPath** : Montage d'un répertoire du node (dev uniquement)
- **PersistentVolume** : Abstraction du stockage persistent

### Volumes cloud

- **awsElasticBlockStore** : AWS EBS
- **azureDisk** : Azure Disk Storage
- **gcePersistentDisk** : Google Persistent Disk

### Commandes utiles

```bash
# Volumes et stockage
kubectl get pv,pvc
kubectl describe pvc <nom>
kubectl get storageclass

# StatefulSets (pour apps avec état)
kubectl get statefulset
kubectl scale statefulset <nom> --replicas=<nombre>

# Debug
kubectl describe pod <nom>
kubectl exec -it <pod> -- df -h
```
