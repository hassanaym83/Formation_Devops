# Correction LAB 3 - Scaling et Autoscaling

## Vue d'ensemble de la solution

Cette correction présente une implémentation complète du scaling horizontal (HPA), vertical (VPA) et du cluster autoscaling pour l'application e-commerce, avec monitoring des métriques personnalisées.

## Architecture de scaling

```
Cluster Autoscaler → Nodes
       ↓
HPA → Pods (horizontal scaling)
VPA → Resources (vertical scaling)
       ↓
Metrics Server → Custom Metrics → Prometheus
```

## Étape 1 : Installation et configuration du Metrics Server

### 1.1 Déploiement Metrics Server

```yaml
# metrics-server.yaml
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
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    k8s-app: metrics-server
  name: system:metrics-server
rules:
  - apiGroups:
      - ''
    resources:
      - nodes/metrics
    verbs:
      - get
  - apiGroups:
      - ''
    resources:
      - pods
      - nodes
    verbs:
      - get
      - list
      - watch

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server-auth-reader
  namespace: kube-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: extension-apiserver-authentication-reader
subjects:
  - kind: ServiceAccount
    name: metrics-server
    namespace: kube-system

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server:system:auth-delegator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: metrics-server
    namespace: kube-system

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    k8s-app: metrics-server
  name: system:metrics-server
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:metrics-server
subjects:
  - kind: ServiceAccount
    name: metrics-server
    namespace: kube-system

---
apiVersion: v1
kind: Service
metadata:
  labels:
    k8s-app: metrics-server
  name: metrics-server
  namespace: kube-system
spec:
  ports:
    - name: https
      port: 443
      protocol: TCP
      targetPort: https
  selector:
    k8s-app: metrics-server

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
            - --kubelet-insecure-tls # Pour développement local
          image: k8s.gcr.io/metrics-server/metrics-server:v0.6.4
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

---
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  labels:
    k8s-app: metrics-server
  name: v1beta1.metrics.k8s.io
spec:
  group: metrics.k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: metrics-server
    namespace: kube-system
  version: v1beta1
  versionPriority: 100
```

### 1.2 Vérification du Metrics Server

```bash
# Installation avec Helm (alternative)
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm upgrade --install metrics-server metrics-server/metrics-server \
  --namespace kube-system \
  --set args[0]="--kubelet-insecure-tls"

# Vérification
kubectl top nodes
kubectl top pods -n ecommerce
kubectl get apiservices | grep metrics
```

## Étape 2 : Configuration des applications avec resource requests/limits

### 2.1 Applications optimisées pour autoscaling

```yaml
# app-with-resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-service-scalable
  namespace: ecommerce
  labels:
    app: product-service
    version: scalable
spec:
  replicas: 3
  selector:
    matchLabels:
      app: product-service
      version: scalable
  template:
    metadata:
      labels:
        app: product-service
        version: scalable
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: product-service
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
              name: http
            - containerPort: 8080
              name: metrics
          resources:
            requests:
              cpu: 200m # Baseline CPU
              memory: 256Mi # Baseline Memory
            limits:
              cpu: 500m # Maximum CPU
              memory: 512Mi # Maximum Memory
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          env:
            - name: MAX_CONNECTIONS
              value: '100'
            - name: WORKER_PROCESSES
              value: '2'
          volumeMounts:
            - name: app-config
              mountPath: /etc/nginx/conf.d
            - name: metrics-config
              mountPath: /etc/nginx/metrics
      volumes:
        - name: app-config
          configMap:
            name: product-service-config
        - name: metrics-config
          configMap:
            name: product-metrics-config

---
apiVersion: v1
kind: Service
metadata:
  name: product-service-scalable
  namespace: ecommerce
  labels:
    app: product-service
    version: scalable
spec:
  selector:
    app: product-service
    version: scalable
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 80
    - name: metrics
      protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP

---
# Configuration NGINX avec métriques
apiVersion: v1
kind: ConfigMap
metadata:
  name: product-metrics-config
  namespace: ecommerce
data:
  metrics.conf: |
    server {
        listen 8080;
        server_name localhost;
        
        location /metrics {
            content_by_lua_block {
                -- Métriques personnalisées pour Prometheus
                local metrics = {
                    'http_requests_total{method="GET",status="200"} ' .. math.random(100, 1000),
                    'http_request_duration_seconds{quantile="0.5"} ' .. (math.random(10, 100) / 1000),
                    'http_request_duration_seconds{quantile="0.9"} ' .. (math.random(100, 500) / 1000),
                    'nginx_connections_active ' .. math.random(10, 50),
                    'nginx_connections_reading ' .. math.random(1, 10),
                    'nginx_connections_writing ' .. math.random(1, 10),
                    'nginx_connections_waiting ' .. math.random(5, 20),
                    'product_service_cpu_usage ' .. math.random(20, 80),
                    'product_service_memory_usage_bytes ' .. math.random(100000000, 400000000),
                    'product_service_request_rate ' .. math.random(10, 100)
                }
                
                ngx.header.content_type = "text/plain"
                for _, metric in ipairs(metrics) do
                    ngx.say(metric)
                end
            }
        }
        
        location /health {
            return 200 '{"status":"healthy","service":"product-service"}';
            add_header Content-Type application/json;
        }
    }

---
# Configuration similaire pour order-service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-scalable
  namespace: ecommerce
  labels:
    app: order-service
    version: scalable
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
      version: scalable
  template:
    metadata:
      labels:
        app: order-service
        version: scalable
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: order-service
          image: nginx:1.21-alpine
          ports:
            - containerPort: 80
            - containerPort: 8080
          resources:
            requests:
              cpu: 150m
              memory: 200Mi
            limits:
              cpu: 400m
              memory: 400Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: order-metrics-config
              mountPath: /etc/nginx/conf.d
      volumes:
        - name: order-metrics-config
          configMap:
            name: order-metrics-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: order-metrics-config
  namespace: ecommerce
data:
  default.conf: |
    server {
        listen 80;
        listen 8080;
        server_name localhost;
        
        location / {
            return 200 '{"service":"order-service","status":"running","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }
        
        location /health {
            return 200 '{"status":"healthy"}';
            add_header Content-Type application/json;
        }
        
        location /metrics {
            content_by_lua_block {
                local metrics = {
                    'order_requests_total ' .. math.random(50, 200),
                    'order_processing_time_seconds ' .. (math.random(500, 2000) / 1000),
                    'order_service_cpu_usage ' .. math.random(15, 60),
                    'order_service_memory_usage_bytes ' .. math.random(80000000, 300000000),
                    'orders_in_queue ' .. math.random(0, 20)
                }
                
                ngx.header.content_type = "text/plain"
                for _, metric in ipairs(metrics) do
                    ngx.say(metric)
                end
            }
        }
    }

---
apiVersion: v1
kind: Service
metadata:
  name: order-service-scalable
  namespace: ecommerce
spec:
  selector:
    app: order-service
    version: scalable
  ports:
    - name: http
      port: 80
      targetPort: 80
    - name: metrics
      port: 8080
      targetPort: 8080
```

## Étape 3 : Configuration HPA (Horizontal Pod Autoscaler)

### 3.1 HPA basé sur CPU et mémoire

```yaml
# hpa-basic.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: product-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-service-scalable
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70 # Scale up when CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80 # Scale up when Memory > 80%
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60 # Wait 60s before scaling up
      policies:
        - type: Percent
          value: 50 # Increase by 50% of current replicas
          periodSeconds: 60
        - type: Pods
          value: 2 # Or add 2 pods
          periodSeconds: 60
      selectPolicy: Max # Use the policy that scales more
    scaleDown:
      stabilizationWindowSeconds: 300 # Wait 5min before scaling down
      policies:
        - type: Percent
          value: 10 # Decrease by 10% of current replicas
          periodSeconds: 60
        - type: Pods
          value: 1 # Or remove 1 pod
          periodSeconds: 60
      selectPolicy: Min # Use the policy that scales less

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service-scalable
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 65
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 75
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 100 # Double the replicas quickly for critical service
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 600 # Wait 10min before scaling down orders
      policies:
        - type: Pods
          value: 1
          periodSeconds: 120
```

### 3.2 HPA avec métriques personnalisées

```yaml
# hpa-custom-metrics.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: product-service-custom-hpa
  namespace: ecommerce
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-service-scalable
  minReplicas: 3
  maxReplicas: 20
  metrics:
    # Métriques standard
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

    # Métriques personnalisées (nécessite custom metrics API)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: '30' # Scale when > 30 RPS per pod

    - type: Pods
      pods:
        metric:
          name: response_time_p95
        target:
          type: AverageValue
          averageValue: '500m' # Scale when response time > 500ms

    # Métriques externes (files d'attente, base de données)
    - type: External
      external:
        metric:
          name: pubsub_ecommerce_queue_size
          selector:
            matchLabels:
              queue: product_processing
        target:
          type: AverageValue
          averageValue: '10' # Scale when queue > 10 messages per replica

  behavior:
    scaleUp:
      stabilizationWindowSeconds: 45
      policies:
        - type: Percent
          value: 50
          periodSeconds: 45
        - type: Pods
          value: 3
          periodSeconds: 45
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 180
      policies:
        - type: Percent
          value: 20
          periodSeconds: 60
      selectPolicy: Min

---
# Configuration pour métriques personnalisées avec Prometheus Adapter
apiVersion: v1
kind: ConfigMap
metadata:
  name: adapter-config
  namespace: custom-metrics
data:
  config.yaml: |
    rules:
    - seriesQuery: 'http_requests_per_second{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^http_requests_per_second"
        as: "http_requests_per_second"
      metricsQuery: 'sum(rate(http_requests_total[2m])) by (<<.GroupBy>>)'

    - seriesQuery: 'http_request_duration_seconds{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^http_request_duration_seconds"
        as: "response_time_p95"
      metricsQuery: 'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[2m])) by (le, <<.GroupBy>>))'
```

## Étape 4 : Configuration VPA (Vertical Pod Autoscaler)

### 4.1 Installation VPA

```bash
# Installer VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler/
./hack/vpa-install.sh

# Ou avec Helm
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm install vpa cowboysysop/vertical-pod-autoscaler --namespace kube-system
```

### 4.2 Configuration VPA

```yaml
# vpa-config.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: user-service-vpa
  namespace: ecommerce
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  updatePolicy:
    updateMode: 'Auto' # Automatically apply recommendations
  resourcePolicy:
    containerPolicies:
      - containerName: user-service
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 1
          memory: 1Gi
        controlledResources: ['cpu', 'memory']
        controlledValues: RequestsAndLimits

---
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: product-service-vpa
  namespace: ecommerce
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: product-service-scalable
  updatePolicy:
    updateMode: 'Off' # Only provide recommendations, don't apply
  resourcePolicy:
    containerPolicies:
      - containerName: product-service
        minAllowed:
          cpu: 150m
          memory: 200Mi
        maxAllowed:
          cpu: 2
          memory: 2Gi
        controlledResources: ['cpu', 'memory']

---
# VPA en mode recommandation seulement
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: database-vpa
  namespace: ecommerce
spec:
  targetRef:
    apiVersion: apps/v1
    kind: StatefulSet
    name: postgres
  updatePolicy:
    updateMode: 'Initial' # Apply only on pod creation
  resourcePolicy:
    containerPolicies:
      - containerName: postgres
        minAllowed:
          cpu: 500m
          memory: 1Gi
        maxAllowed:
          cpu: 4
          memory: 8Gi
        controlledResources: ['memory'] # Only manage memory for DB
```

## Étape 5 : Cluster Autoscaler

### 5.1 Configuration Cluster Autoscaler (AWS EKS exemple)

```yaml
# cluster-autoscaler.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
  name: cluster-autoscaler
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT-ID:role/cluster-autoscaler-role

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
kind: Role
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
rules:
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['create', 'list', 'watch']
  - apiGroups: ['']
    resources: ['configmaps']
    resourceNames:
      ['cluster-autoscaler-status', 'cluster-autoscaler-priority-expander']
    verbs: ['delete', 'get', 'update', 'watch']

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
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cluster-autoscaler
  namespace: kube-system
  labels:
    k8s-addon: cluster-autoscaler.addons.k8s.io
    k8s-app: cluster-autoscaler
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
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
        - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
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
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/ecommerce-cluster
            - --balance-similar-node-groups
            - --skip-nodes-with-system-pods=false
            - --scale-down-enabled=true
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=10m
            - --scale-down-utilization-threshold=0.5
          volumeMounts:
            - name: ssl-certs
              mountPath: /etc/ssl/certs/ca-certificates.crt
              readOnly: true
          imagePullPolicy: 'Always'
          env:
            - name: AWS_REGION
              value: us-west-2
      volumes:
        - name: ssl-certs
          hostPath:
            path: '/etc/ssl/certs/ca-bundle.crt'
```

### 5.2 PodDisruptionBudget pour la stabilité

```yaml
# pdb-config.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: product-service-pdb
  namespace: ecommerce
spec:
  minAvailable: 2 # Garder au moins 2 pods disponibles
  selector:
    matchLabels:
      app: product-service
      version: scalable

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: order-service-pdb
  namespace: ecommerce
spec:
  maxUnavailable: 1 # Maximum 1 pod indisponible
  selector:
    matchLabels:
      app: order-service
      version: scalable

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: user-service-pdb
  namespace: ecommerce
spec:
  minAvailable: 50% # Garder au moins 50% des pods
  selector:
    matchLabels:
      app: user-service
```

## Étape 6 : Tests de charge et validation

### 6.1 Générateur de charge

```yaml
# load-generator.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: load-generator
  namespace: ecommerce
spec:
  replicas: 1
  selector:
    matchLabels:
      app: load-generator
  template:
    metadata:
      labels:
        app: load-generator
    spec:
      containers:
        - name: load-generator
          image: busybox:1.35
          command:
            - /bin/sh
            - -c
            - |
              while true; do
                # Charge CPU intensive
                for i in $(seq 1 100); do
                  wget -q -O- http://product-service-scalable/products
                  wget -q -O- http://order-service-scalable/orders
                  sleep 0.01
                done
                
                echo "Load generation cycle completed at $(date)"
                sleep 30
              done
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi

---
# Load generator avancé avec hey
apiVersion: batch/v1
kind: Job
metadata:
  name: hey-load-test
  namespace: ecommerce
spec:
  template:
    spec:
      containers:
        - name: hey
          image: rcmorano/hey
          command:
            - hey
            - -z
            - '5m' # Duration: 5 minutes
            - -c
            - '50' # Concurrency: 50 requests
            - -q
            - '10' # QPS: 10 queries per second per worker
            - http://product-service-scalable/products
      restartPolicy: Never
  backoffLimit: 4

---
# Apache Bench load test
apiVersion: batch/v1
kind: Job
metadata:
  name: ab-stress-test
  namespace: ecommerce
spec:
  template:
    spec:
      containers:
        - name: apache-bench
          image: httpd:2.4-alpine
          command:
            - /bin/sh
            - -c
            - |
              # Install ab if not available
              apk add --no-cache apache2-utils

              echo "Starting load test with Apache Bench..."

              # Test product service
              ab -n 10000 -c 100 -t 300 http://product-service-scalable/products

              # Test order service
              ab -n 5000 -c 50 -t 300 http://order-service-scalable/orders

              echo "Load test completed"
      restartPolicy: Never
```

### 6.2 Scripts de test et monitoring

```bash
# test-autoscaling.sh
#!/bin/bash

echo "🧪 Tests d'Autoscaling Kubernetes"

# Configuration
NAMESPACE="ecommerce"
PRODUCT_SERVICE="product-service-scalable"
ORDER_SERVICE="order-service-scalable"

# Fonction de monitoring
monitor_pods() {
    local service=$1
    echo "=== Monitoring $service ==="
    kubectl get hpa -n $NAMESPACE
    kubectl get pods -n $NAMESPACE -l app=$service -o wide
    kubectl top pods -n $NAMESPACE -l app=$service
}

# Test 1: État initial
echo "📊 État initial des services"
monitor_pods $PRODUCT_SERVICE
monitor_pods $ORDER_SERVICE

# Test 2: Lancement du générateur de charge
echo "🚀 Démarrage du générateur de charge..."
kubectl apply -f load-generator.yaml

# Monitoring pendant 10 minutes
for i in {1..20}; do
    echo "=== Minute $((i/2)) ==="
    monitor_pods $PRODUCT_SERVICE

    # Vérifier les métriques HPA
    echo "Métriques HPA:"
    kubectl get hpa product-service-hpa -n $NAMESPACE -o yaml | grep -A5 -B5 currentMetrics

    sleep 30
done

# Test 3: Arrêt de la charge
echo "🛑 Arrêt du générateur de charge..."
kubectl delete deployment load-generator -n $NAMESPACE

# Monitoring de la descente en charge
echo "📉 Monitoring de la descente en charge..."
for i in {1..10}; do
    echo "=== Scale Down - Minute $i ==="
    monitor_pods $PRODUCT_SERVICE
    sleep 60
done

# Test 4: VPA recommendations
echo "📈 Recommandations VPA:"
kubectl describe vpa -n $NAMESPACE

# Test 5: Événements d'autoscaling
echo "📝 Événements d'autoscaling:"
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | grep -i -E "(scaled|hpa)"

echo "✅ Tests d'autoscaling terminés"
```

### 6.3 Dashboard de monitoring

```yaml
# monitoring-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: autoscaling-dashboard
  namespace: ecommerce
data:
  dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "Kubernetes Autoscaling Dashboard",
        "tags": ["kubernetes", "autoscaling"],
        "timezone": "browser",
        "panels": [
          {
            "id": 1,
            "title": "Pod Count",
            "type": "graph",
            "targets": [
              {
                "expr": "kube_deployment_status_replicas{deployment=\"product-service-scalable\"}",
                "legendFormat": "Product Service Replicas"
              },
              {
                "expr": "kube_deployment_status_replicas{deployment=\"order-service-scalable\"}",
                "legendFormat": "Order Service Replicas"
              }
            ],
            "yAxes": [
              {
                "label": "Pod Count",
                "min": 0
              }
            ]
          },
          {
            "id": 2,
            "title": "CPU Utilization",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(container_cpu_usage_seconds_total{pod=~\"product-service-scalable-.*\"}[5m]) * 100",
                "legendFormat": "{{pod}} CPU %"
              }
            ]
          },
          {
            "id": 3,
            "title": "Memory Usage",
            "type": "graph",
            "targets": [
              {
                "expr": "container_memory_working_set_bytes{pod=~\"product-service-scalable-.*\"} / 1024 / 1024",
                "legendFormat": "{{pod}} Memory (MB)"
              }
            ]
          },
          {
            "id": 4,
            "title": "HPA Status",
            "type": "table",
            "targets": [
              {
                "expr": "kube_hpa_status_current_replicas",
                "format": "table"
              }
            ]
          }
        ]
      }
    }
```

## Points clés de la solution

### ⚡ Horizontal Pod Autoscaling (HPA)

- **Métriques multiples**: CPU, mémoire, métriques personnalisées
- **Comportements configurés**: Politiques de montée/descente en charge
- **Stabilisation**: Fenêtres de temps pour éviter le flapping
- **Limites sécurisées**: Min/max replicas pour contrôler les coûts

### 📏 Vertical Pod Autoscaling (VPA)

- **Modes flexibles**: Auto, Off, Initial
- **Contraintes de ressources**: Min/max allowed resources
- **Recommandations**: Analyse continue des besoins réels
- **Contrôle granulaire**: Par conteneur et type de ressource

### 🔧 Cluster Autoscaling

- **Auto-discovery**: Détection automatique des node groups
- **Politiques intelligentes**: least-waste, priority-based
- **Seuils configurables**: Scale-down thresholds
- **Intégration cloud**: AWS, GCP, Azure

### 📊 Monitoring et métriques

- **Metrics Server**: Métriques de base CPU/mémoire
- **Custom metrics**: Intégration Prometheus pour métriques business
- **Dashboards**: Visualisation temps réel des scaling events
- **Alerting**: Notifications sur les événements de scaling

Cette solution fournit un système d'autoscaling complet et robuste pour une application e-commerce en production.
