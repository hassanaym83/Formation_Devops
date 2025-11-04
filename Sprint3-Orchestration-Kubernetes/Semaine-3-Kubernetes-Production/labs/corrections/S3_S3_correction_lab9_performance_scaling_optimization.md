# LAB 9 - Correction : Performance et Scaling (HPA, VPA, Cluster Autoscaler)

## 📋 Vue d'ensemble de la solution

Cette correction présente la configuration complète des systèmes d'auto-scaling Kubernetes pour optimiser les performances et les coûts.

---

## 🔧 Solution complète

### Étape 1 : Installation Metrics Server

```yaml
# performance/metrics-server.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    k8s-app: metrics-server
    rbac.authorization.k8s.io/aggregate-to-admin: 'true'
    rbac.authorization.k8s.io/aggregate-to-edit: 'true'
    rbac.authorization.k8s.io/aggregate-to-view: 'true'
  name: system:aggregated-metrics-reader
rules:
  - apiGroups:
      - metrics.k8s.io
    resources:
      - pods
      - nodes
    verbs:
      - get
      - list
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
spec:
  selector:
    matchLabels:
      k8s-app: metrics-server
  strategy:
    rollingUpdate:
      maxUnavailable: 0
  template:
    metadata:
      labels:
        k8s-app: metrics-server
    spec:
      containers:
        - args:
            - --cert-dir=/tmp
            - --secure-port=4443
            - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
            - --kubelet-use-node-status-port
            - --metric-resolution=15s
            - --kubelet-insecure-tls
          image: registry.k8s.io/metrics-server/metrics-server:v0.6.4
          imagePullPolicy: IfNotPresent
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /livez
              port: https
              scheme: HTTPS
            periodSeconds: 10
          name: metrics-server
          ports:
            - containerPort: 4443
              name: https
              protocol: TCP
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /readyz
              port: https
              scheme: HTTPS
            initialDelaySeconds: 20
            periodSeconds: 10
          resources:
            requests:
              cpu: 100m
              memory: 200Mi
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 1000
          volumeMounts:
            - mountPath: /tmp
              name: tmp-dir
      nodeSelector:
        kubernetes.io/os: linux
      priorityClassName: system-cluster-critical
      serviceAccountName: metrics-server
      volumes:
        - emptyDir: {}
          name: tmp-dir
```

### Étape 2 : Configuration HPA (Horizontal Pod Autoscaler)

```yaml
# performance/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  namespace: app-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  minReplicas: 3
  maxReplicas: 50
  metrics:
    # Métriques CPU
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

    # Métriques mémoire
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

    # Métriques custom - RPS
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: '100'

    # Métriques custom - Response time
    - type: Pods
      pods:
        metric:
          name: http_request_duration_p95
        target:
          type: AverageValue
          averageValue: '500m' # 500ms

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 5
          periodSeconds: 15
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Min
---
# HPA pour base de données
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: database-read-replicas-hpa
  namespace: database
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: postgresql-read-replica
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Pods
      pods:
        metric:
          name: postgresql_active_connections
        target:
          type: AverageValue
          averageValue: '50'

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 120
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 600
      policies:
        - type: Pods
          value: 1
          periodSeconds: 180
```

### Étape 3 : Configuration VPA (Vertical Pod Autoscaler)

```bash
# Installation VPA
#!/bin/bash
# performance/install-vpa.sh

# Cloner le repository VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler/

# Installation des CRDs et composants
./hack/vpa-install.sh

# Vérification
kubectl get pods -n kube-system | grep vpa
```

```yaml
# performance/vpa.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: webapp-vpa
  namespace: app-prod
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  updatePolicy:
    updateMode: 'Auto' # Off, Initial, Auto
  resourcePolicy:
    containerPolicies:
      - containerName: webapp
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2000m
          memory: 4Gi
        controlledResources: ['cpu', 'memory']
        controlledValues: RequestsAndLimits
---
# VPA pour monitoring (mode recommandation)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: prometheus-vpa
  namespace: monitoring
spec:
  targetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: prometheus
  updatePolicy:
    updateMode: 'Off' # Mode recommandation seulement
  resourcePolicy:
    containerPolicies:
      - containerName: prometheus
        minAllowed:
          cpu: 500m
          memory: 1Gi
        maxAllowed:
          cpu: 4000m
          memory: 8Gi
```

### Étape 4 : Cluster Autoscaler

```yaml
# performance/cluster-autoscaler.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
  name: cluster-autoscaler
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-autoscaler
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
rules:
  - apiGroups: ['']
    resources: ['events', 'endpoints']
    verbs: ['create', 'patch']
  - apiGroups: ['']
    resources: ['pods/eviction']
    verbs: ['create']
  - apiGroups: ['']
    resources: ['pods/status']
    verbs: ['update']
  - apiGroups: ['']
    resources: ['endpoints']
    resourceNames: ['cluster-autoscaler']
    verbs: ['get', 'update']
  - apiGroups: ['']
    resources: ['nodes']
    verbs: ['watch', 'list', 'get', 'update']
  - apiGroups: ['']
    resources:
      [
        'namespaces',
        'pods',
        'services',
        'replicationcontrollers',
        'persistentvolumeclaims',
        'persistentvolumes'
      ]
    verbs: ['watch', 'list', 'get']
  - apiGroups: ['extensions']
    resources: ['replicasets', 'daemonsets']
    verbs: ['watch', 'list', 'get']
  - apiGroups: ['policy']
    resources: ['poddisruptionbudgets']
    verbs: ['watch', 'list']
  - apiGroups: ['apps']
    resources: ['statefulsets', 'replicasets', 'daemonsets']
    verbs: ['watch', 'list', 'get']
  - apiGroups: ['storage.k8s.io']
    resources:
      ['storageclasses', 'csinodes', 'csidrivers', 'csistoragecapacities']
    verbs: ['watch', 'list', 'get']
  - apiGroups: ['batch', 'extensions']
    resources: ['jobs']
    verbs: ['get', 'list', 'watch', 'patch']
  - apiGroups: ['coordination.k8s.io']
    resources: ['leases']
    verbs: ['create']
  - apiGroups: ['coordination.k8s.io']
    resourceNames: ['cluster-autoscaler']
    resources: ['leases']
    verbs: ['get', 'update']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-autoscaler
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-autoscaler
subjects:
  - kind: ServiceAccount
    name: cluster-autoscaler
    namespace: kube-system
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    app: cluster-autoscaler
spec:
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8085'
    spec:
      priorityClassName: system-cluster-critical
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
        fsGroup: 65534
      serviceAccountName: cluster-autoscaler
      containers:
        - image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.27.3
          name: cluster-autoscaler
          resources:
            limits:
              cpu: 100m
              memory: 600Mi
            requests:
              cpu: 100m
              memory: 600Mi
          command:
            - ./cluster-autoscaler
            - --v=4
            - --stderrthreshold=info
            - --cloud-provider=aws
            - --skip-nodes-with-local-storage=false
            - --expander=least-waste
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/prod-cluster
            - --balance-similar-node-groups
            - --scale-down-enabled=true
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=10m
            - --scale-down-utilization-threshold=0.5
            - --max-node-provision-time=15m
            - --nodes=1:10:prod-cluster-workers
          volumeMounts:
            - name: ssl-certs
              mountPath: /etc/ssl/certs/ca-certificates.crt
              readOnly: true
          imagePullPolicy: 'Always'
          securityContext:
            allowPrivilegeEscalation: false
            capabilities:
              drop:
                - ALL
            readOnlyRootFilesystem: true
      volumes:
        - name: ssl-certs
          hostPath:
            path: '/etc/ssl/certs/ca-bundle.crt'
```

### Étape 5 : Tests de charge et validation

```bash
#!/bin/bash
# performance/load-test.sh

echo "🧪 Tests de performance et scaling"

# Installation hey pour les tests de charge
curl -L https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64 -o hey
chmod +x hey
sudo mv hey /usr/local/bin/

# Test de charge progressive
echo "📈 Test de charge progressive..."

# URL de l'application
APP_URL="http://webapp.k8s.local"

# État initial
echo "📊 État initial:"
kubectl get hpa webapp-hpa -n app-prod
kubectl get pods -n app-prod -l app=webapp

# Test 1: Charge légère (10 RPS)
echo "🔥 Test 1: Charge légère (10 RPS pendant 2 minutes)"
hey -z 2m -c 10 -q 10 $APP_URL &
LOAD_PID=$!

sleep 30
echo "📊 État après 30s de charge légère:"
kubectl get hpa webapp-hpa -n app-prod
kubectl get pods -n app-prod -l app=webapp

wait $LOAD_PID

# Test 2: Charge moyenne (50 RPS)
echo "🔥 Test 2: Charge moyenne (50 RPS pendant 3 minutes)"
hey -z 3m -c 25 -q 50 $APP_URL &
LOAD_PID=$!

sleep 60
echo "📊 État après 1 minute de charge moyenne:"
kubectl get hpa webapp-hpa -n app-prod
kubectl get pods -n app-prod -l app=webapp

wait $LOAD_PID

# Test 3: Charge élevée (200 RPS)
echo "🔥 Test 3: Charge élevée (200 RPS pendant 5 minutes)"
hey -z 5m -c 50 -q 200 $APP_URL &
LOAD_PID=$!

# Surveiller le scaling
for i in {1..10}; do
    sleep 30
    echo "📊 État après ${i}*30s de charge élevée:"
    kubectl get hpa webapp-hpa -n app-prod
    kubectl get pods -n app-prod -l app=webapp | grep Running | wc -l
done

wait $LOAD_PID

# Attendre le scale-down
echo "⏳ Attente du scale-down (10 minutes)..."
sleep 600

echo "📊 État final après scale-down:"
kubectl get hpa webapp-hpa -n app-prod
kubectl get pods -n app-prod -l app=webapp

echo "🎉 Tests de performance terminés"
```

### Étape 6 : Optimisation des ressources

```yaml
# performance/pod-disruption-budget.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: webapp-pdb
  namespace: app-prod
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: webapp
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: database-pdb
  namespace: database
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: postgresql
```

```yaml
# performance/priority-classes.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-apps
value: 1000
globalDefault: false
description: 'Priority class for critical applications'
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-priority-apps
value: 500
globalDefault: false
description: 'Priority class for standard applications'
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority-batch
value: 100
globalDefault: false
description: 'Priority class for batch jobs'
preemptionPolicy: PreemptLowerPriority
```

### Étape 7 : Monitoring des performances

```yaml
# performance/performance-monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: performance-alerts
  namespace: monitoring
  labels:
    prometheus: kube-prometheus
    role: alert-rules
spec:
  groups:
    - name: autoscaling.rules
      interval: 30s
      rules:
        # HPA not scaling
        - alert: HPANotScaling
          expr: |
            kube_horizontalpodautoscaler_status_current_replicas != kube_horizontalpodautoscaler_status_desired_replicas
          for: 10m
          labels:
            severity: warning
            component: autoscaling
          annotations:
            summary: 'HPA not scaling properly'
            description: 'HPA {{ $labels.namespace }}/{{ $labels.horizontalpodautoscaler }} current replicas ({{ $labels.current_replicas }}) != desired replicas ({{ $labels.desired_replicas }}) for more than 10 minutes.'

        # Resource utilization high
        - alert: HighResourceUtilization
          expr: |
            (
              kube_pod_container_resource_requests{resource="cpu"} / 
              kube_node_status_allocatable{resource="cpu"}
            ) * 100 > 80
          for: 15m
          labels:
            severity: warning
            component: resources
          annotations:
            summary: 'High resource utilization'
            description: 'Node {{ $labels.node }} CPU utilization is {{ $value }}%.'

        # Cluster autoscaler not working
        - alert: ClusterAutoscalerNotWorking
          expr: |
            increase(cluster_autoscaler_failed_scale_ups_total[1h]) > 3
          for: 5m
          labels:
            severity: critical
            component: autoscaling
          annotations:
            summary: 'Cluster Autoscaler failing to scale up'
            description: 'Cluster Autoscaler has failed to scale up {{ $value }} times in the last hour.'
```

---

## 🎯 Résultats

✅ **HPA configuré** avec métriques CPU, mémoire et custom  
✅ **VPA installé** pour optimisation automatique  
✅ **Cluster Autoscaler** pour scaling des nodes  
✅ **Tests de charge** validant le scaling  
✅ **Monitoring** et alertes de performance

---

_Correction réalisée par Hassan ESSADIK - Formation DevOps Kubernetes_
