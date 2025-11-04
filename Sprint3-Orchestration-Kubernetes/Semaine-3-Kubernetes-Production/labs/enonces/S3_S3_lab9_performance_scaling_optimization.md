# LAB 9 - Optimisation des performances et scaling

## Objectifs

- Analyser et optimiser les performances des applications Kubernetes
- Configurer l'autoscaling horizontal et vertical des pods
- Implémenter le cluster autoscaling
- Optimiser l'utilisation des ressources CPU et mémoire
- Configurer les stratégies de scheduling avancées

## Prérequis

- Cluster Kubernetes fonctionnel avec plusieurs nœuds
- kubectl configuré
- Metrics Server installé
- Applications déployées pour les tests
- Connaissances des concepts de scaling et performance

## Contexte du LAB

Vous allez optimiser les performances d'une plateforme e-commerce qui doit :

- Gérer des pics de trafic variables
- Optimiser l'utilisation des ressources
- Assurer une disponibilité haute
- Maintenir des temps de réponse acceptables
- S'adapter automatiquement à la charge

## Exercice 1 : Installation et configuration des outils de performance

### Étape 1.1 : Installation du Metrics Server

```bash
# Installer Metrics Server si pas déjà fait
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Vérifier l'installation
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods --all-namespaces
```

### Étape 1.2 : Installation du Vertical Pod Autoscaler

Créez `performance/vpa-install.sh` :

```bash
#!/bin/bash

set -e

echo "Installing Vertical Pod Autoscaler..."

# Cloner le repository VPA
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler

# Installer VPA
./hack/vpa-install.sh

# Vérifier l'installation
kubectl get pods -n kube-system | grep vpa

echo "VPA installation completed!"
```

### Étape 1.3 : Configuration des outils de monitoring

Créez `performance/resource-monitoring.yaml` :

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: resource-monitor
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: resource-monitor
rules:
  - apiGroups: ['']
    resources: ['nodes', 'pods', 'services']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['apps']
    resources: ['deployments', 'replicasets']
    verbs: ['get', 'list', 'watch']
  - apiGroups: ['metrics.k8s.io']
    resources: ['nodes', 'pods']
    verbs: ['get', 'list']
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: resource-monitor
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: resource-monitor
subjects:
  - kind: ServiceAccount
    name: resource-monitor
    namespace: kube-system
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: resource-usage-report
  namespace: kube-system
spec:
  schedule: '*/15 * * * *' # Toutes les 15 minutes
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: resource-monitor
          containers:
            - name: monitor
              image: bitnami/kubectl:latest
              command:
                - /bin/bash
                - -c
                - |
                  echo "=== Resource Usage Report $(date) ==="
                  echo "Node Usage:"
                  kubectl top nodes
                  echo ""
                  echo "Top CPU consuming pods:"
                  kubectl top pods --all-namespaces --sort-by=cpu | head -10
                  echo ""
                  echo "Top Memory consuming pods:"
                  kubectl top pods --all-namespaces --sort-by=memory | head -10
                  echo ""
                  echo "Pods without resource limits:"
                  kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"'
          restartPolicy: OnFailure
```

## Exercice 2 : Application de test pour le scaling

### Étape 2.1 : Application CPU-intensive

Créez `apps/cpu-app.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cpu-intensive-app
  namespace: performance-test
  labels:
    app: cpu-intensive
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cpu-intensive
  template:
    metadata:
      labels:
        app: cpu-intensive
    spec:
      containers:
        - name: cpu-load
          image: busybox
          command:
            - /bin/sh
            - -c
            - |
              while true; do
                # Simulation de charge CPU variable
                if [ "$CPU_LOAD" = "high" ]; then
                  # Charge élevée
                  for i in $(seq 1 4); do
                    dd if=/dev/zero of=/dev/null bs=1M count=100 &
                  done
                  sleep 30
                  killall dd 2>/dev/null || true
                else
                  # Charge normale
                  sleep 10
                fi
              done
          env:
            - name: CPU_LOAD
              value: 'normal'
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
          livenessProbe:
            exec:
              command:
                - /bin/true
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - /bin/true
            initialDelaySeconds: 5
            periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: cpu-intensive-service
  namespace: performance-test
spec:
  selector:
    app: cpu-intensive
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

### Étape 2.2 : Application web avec métriques

Créez `apps/web-app.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: performance-web-app
  namespace: performance-test
  labels:
    app: performance-web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: performance-web
  template:
    metadata:
      labels:
        app: performance-web
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: web-app
          image: nginx:alpine
          ports:
            - containerPort: 80
              name: http
            - containerPort: 8080
              name: metrics
          env:
            - name: RESPONSE_DELAY
              value: '100'
            - name: ERROR_RATE
              value: '5'
          volumeMounts:
            - name: nginx-config
              mountPath: /etc/nginx/conf.d
            - name: app-code
              mountPath: /usr/share/nginx/html
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 200m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: nginx-config
          configMap:
            name: nginx-performance-config
        - name: app-code
          configMap:
            name: app-performance-code
---
apiVersion: v1
kind: Service
metadata:
  name: performance-web-service
  namespace: performance-test
  labels:
    app: performance-web
spec:
  selector:
    app: performance-web
  ports:
    - name: http
      port: 80
      targetPort: 80
    - name: metrics
      port: 8080
      targetPort: 8080
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-performance-config
  namespace: performance-test
data:
  default.conf: |
    upstream backend {
        server 127.0.0.1:3000;
    }

    server {
        listen 80;
        server_name localhost;
        
        # Métriques de base
        location /nginx_status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            deny all;
        }
        
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        location /ready {
            access_log off;
            return 200 "ready\n";
            add_header Content-Type text/plain;
        }
        
        location / {
            root /usr/share/nginx/html;
            index index.html;
            try_files $uri $uri/ =404;
            
            # Headers pour le cache
            add_header Cache-Control "public, max-age=3600";
        }
        
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # Simulation de latence variable
            proxy_connect_timeout 1s;
            proxy_send_timeout 2s;
            proxy_read_timeout 2s;
        }
    }

    # Server pour métriques Prometheus
    server {
        listen 8080;
        location /metrics {
            access_log off;
            return 200 "# Nginx metrics endpoint\nnginx_up 1\n";
            add_header Content-Type text/plain;
        }
    }
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-performance-code
  namespace: performance-test
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head>
        <title>Performance Test App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .metric { background: #f0f0f0; padding: 10px; margin: 10px 0; }
            .button { padding: 10px 20px; margin: 5px; background: #007cba; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Performance Test Application</h1>
        <div class="metric">
            <strong>Pod:</strong> <span id="pod-name">Loading...</span>
        </div>
        <div class="metric">
            <strong>Response Time:</strong> <span id="response-time">-</span>ms
        </div>
        <div class="metric">
            <strong>Requests Served:</strong> <span id="request-count">0</span>
        </div>
        
        <h2>Load Testing</h2>
        <button class="button" onclick="startCpuLoad()">Start CPU Load</button>
        <button class="button" onclick="startMemoryLoad()">Start Memory Load</button>
        <button class="button" onclick="stopLoad()">Stop Load</button>
        
        <script>
            let requestCount = 0;
            let loadInterval;
            
            function updateMetrics() {
                const start = Date.now();
                fetch('/health')
                    .then(() => {
                        const duration = Date.now() - start;
                        document.getElementById('response-time').textContent = duration;
                        document.getElementById('request-count').textContent = ++requestCount;
                    });
            }
            
            function startCpuLoad() {
                console.log('Starting CPU load simulation');
                loadInterval = setInterval(() => {
                    const start = Date.now();
                    while (Date.now() - start < 100) {
                        Math.random() * Math.random();
                    }
                }, 50);
            }
            
            function startMemoryLoad() {
                console.log('Starting memory load simulation');
                const arrays = [];
                loadInterval = setInterval(() => {
                    arrays.push(new Array(100000).fill(Math.random()));
                }, 100);
            }
            
            function stopLoad() {
                console.log('Stopping load simulation');
                clearInterval(loadInterval);
            }
            
            // Mettre à jour les métriques toutes les 2 secondes
            setInterval(updateMetrics, 2000);
            updateMetrics();
        </script>
    </body>
    </html>
```

### Étape 2.3 : Création du namespace et déploiement

```bash
# Créer le namespace
kubectl create namespace performance-test

# Déployer les applications
kubectl apply -f apps/cpu-app.yaml
kubectl apply -f apps/web-app.yaml

# Vérifier les déploiements
kubectl get pods -n performance-test
kubectl get services -n performance-test
```

## Exercice 3 : Horizontal Pod Autoscaler (HPA)

### Étape 3.1 : HPA basé sur CPU

Créez `performance/hpa-cpu.yaml` :

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cpu-intensive-hpa
  namespace: performance-test
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cpu-intensive-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Max
```

### Étape 3.2 : HPA basé sur mémoire et CPU

Créez `performance/hpa-multi-metric.yaml` :

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-hpa
  namespace: performance-test
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: performance-web-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: nginx_requests_per_second
        target:
          type: AverageValue
          averageValue: '100'
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 50
          periodSeconds: 30
        - type: Pods
          value: 3
          periodSeconds: 60
      selectPolicy: Max
```

### Étape 3.3 : HPA basé sur métriques custom

Créez `performance/hpa-custom-metrics.yaml` :

```yaml
# D'abord, déployer le custom metrics adapter
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-metrics-adapter
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: custom-metrics-adapter
  template:
    metadata:
      labels:
        app: custom-metrics-adapter
    spec:
      containers:
        - name: custom-metrics-adapter
          image: k8s.gcr.io/prometheus-adapter/prometheus-adapter:v0.11.0
          args:
            - --cert-dir=/var/run/serving-cert
            - --config=/etc/adapter/config.yaml
            - --logtostderr=true
            - --prometheus-url=http://prometheus.monitoring.svc:9090/
            - --metrics-relist-interval=1m
            - --v=4
          ports:
            - containerPort: 6443
          volumeMounts:
            - name: config
              mountPath: /etc/adapter/
            - name: tmp-vol
              mountPath: /var/run/serving-cert
      volumes:
        - name: config
          configMap:
            name: adapter-config
        - name: tmp-vol
          emptyDir: {}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: adapter-config
  namespace: kube-system
data:
  config.yaml: |
    rules:
    - seriesQuery: 'nginx_http_requests_total{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^nginx_http_requests_total"
        as: "nginx_requests_per_second"
      metricsQuery: 'rate(nginx_http_requests_total{<<.LabelMatchers>>}[2m])'
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app-custom-hpa
  namespace: performance-test
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: performance-web-app
  minReplicas: 2
  maxReplicas: 15
  metrics:
    - type: Pods
      pods:
        metric:
          name: nginx_requests_per_second
        target:
          type: AverageValue
          averageValue: '50'
    - type: Object
      object:
        metric:
          name: ingress_requests_per_second
          selector:
            matchLabels:
              app: performance-web
        target:
          type: Value
          value: '200'
```

### Étape 3.4 : Application et test des HPA

```bash
# Appliquer les HPA
kubectl apply -f performance/hpa-cpu.yaml
kubectl apply -f performance/hpa-multi-metric.yaml

# Vérifier les HPA
kubectl get hpa -n performance-test
kubectl describe hpa cpu-intensive-hpa -n performance-test

# Surveiller le scaling en temps réel
watch kubectl get hpa,pods -n performance-test
```

## Exercice 4 : Vertical Pod Autoscaler (VPA)

### Étape 4.1 : VPA en mode recommandation

Créez `performance/vpa-recommendation.yaml` :

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: cpu-app-vpa-recommendation
  namespace: performance-test
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cpu-intensive-app
  updatePolicy:
    updateMode: 'Off' # Mode recommandation seulement
  resourcePolicy:
    containerPolicies:
      - containerName: cpu-load
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 1000m
          memory: 512Mi
        controlledResources: ['cpu', 'memory']
        controlledValues: RequestsAndLimits
```

### Étape 4.2 : VPA en mode automatique

Créez `performance/vpa-auto.yaml` :

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-app-vpa-auto
  namespace: performance-test
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: performance-web-app
  updatePolicy:
    updateMode: 'Auto'
  resourcePolicy:
    containerPolicies:
      - containerName: web-app
        minAllowed:
          cpu: 25m
          memory: 32Mi
        maxAllowed:
          cpu: 500m
          memory: 256Mi
        controlledResources: ['cpu', 'memory']
        controlledValues: RequestsAndLimits
---
# VPA pour mode recreation (restart des pods)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: cpu-app-vpa-recreate
  namespace: performance-test
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cpu-intensive-app
  updatePolicy:
    updateMode: 'Recreate'
  resourcePolicy:
    containerPolicies:
      - containerName: cpu-load
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2000m
          memory: 1Gi
        controlledResources: ['cpu', 'memory']
```

### Étape 4.3 : Analyse des recommandations VPA

```bash
# Appliquer les VPA
kubectl apply -f performance/vpa-recommendation.yaml
kubectl apply -f performance/vpa-auto.yaml

# Attendre la collecte de données (quelques minutes)
sleep 300

# Voir les recommandations
kubectl describe vpa cpu-app-vpa-recommendation -n performance-test
kubectl get vpa -n performance-test -o yaml
```

## Exercice 5 : Cluster Autoscaler

### Étape 5.1 : Configuration du Cluster Autoscaler

Créez `performance/cluster-autoscaler.yaml` :

```yaml
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
      serviceAccountName: cluster-autoscaler
      containers:
        - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.26.0
          name: cluster-autoscaler
          resources:
            limits:
              cpu: 100m
              memory: 300Mi
            requests:
              cpu: 100m
              memory: 300Mi
          command:
            - ./cluster-autoscaler
            - --v=4
            - --stderrthreshold=info
            - --cloud-provider=aws # Ou votre provider
            - --skip-nodes-with-local-storage=false
            - --expander=least-waste
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/production
            - --balance-similar-node-groups
            - --skip-nodes-with-system-pods=false
            - --scale-down-enabled=true
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=10m
            - --scale-down-utilization-threshold=0.5
            - --max-node-provision-time=15m
          env:
            - name: AWS_REGION
              value: us-west-2
          volumeMounts:
            - name: ssl-certs
              mountPath: /etc/ssl/certs/ca-certificates.crt
              readOnly: true
          imagePullPolicy: 'Always'
      volumes:
        - name: ssl-certs
          hostPath:
            path: '/etc/ssl/certs/ca-bundle.crt'
---
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
    resources: ['storageclasses', 'csinodes']
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
```

### Étape 5.2 : Priority Classes pour les workloads

Créez `performance/priority-classes.yaml` :

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: 'Priority class for critical workloads'
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium-priority
value: 500
globalDefault: false
description: 'Priority class for normal workloads'
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority
value: 100
globalDefault: false
description: 'Priority class for batch workloads'
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: default-priority
value: 200
globalDefault: true
description: 'Default priority class'
```

### Étape 5.3 : Test du Cluster Autoscaler

Créez `performance/scale-test.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scale-test-workload
  namespace: performance-test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: scale-test
  template:
    metadata:
      labels:
        app: scale-test
    spec:
      priorityClassName: medium-priority
      containers:
        - name: load-generator
          image: busybox
          command:
            - sleep
            - '3600'
          resources:
            requests:
              cpu: 1000m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 1Gi
---
# Job pour déclencher le scaling
apiVersion: batch/v1
kind: Job
metadata:
  name: trigger-scale-up
  namespace: performance-test
spec:
  completions: 10
  parallelism: 10
  template:
    spec:
      containers:
        - name: resource-consumer
          image: busybox
          command:
            - sh
            - -c
            - 'sleep 300'
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
      restartPolicy: Never
```

## Exercice 6 : Optimisation des ressources

### Étape 6.1 : Analyse de l'utilisation des ressources

Créez `scripts/resource-analysis.sh` :

```bash
#!/bin/bash

set -e

echo "=== Kubernetes Resource Analysis ==="
echo "Date: $(date)"
echo

# Fonction pour analyser les nœuds
analyze_nodes() {
    echo "=== NODE ANALYSIS ==="
    echo "Total nodes: $(kubectl get nodes --no-headers | wc -l)"
    echo

    echo "Node resource utilization:"
    kubectl top nodes
    echo

    echo "Node capacity:"
    kubectl describe nodes | grep -A 5 "Capacity:"
    echo

    echo "Nodes by role:"
    kubectl get nodes --show-labels | grep -o 'node-role.kubernetes.io/[^,]*' | sort | uniq -c
    echo
}

# Fonction pour analyser les pods
analyze_pods() {
    echo "=== POD ANALYSIS ==="
    echo "Total pods: $(kubectl get pods --all-namespaces --no-headers | wc -l)"
    echo

    echo "Pods by namespace:"
    kubectl get pods --all-namespaces --no-headers | awk '{print $1}' | sort | uniq -c | sort -nr
    echo

    echo "Top CPU consuming pods:"
    kubectl top pods --all-namespaces --sort-by=cpu | head -10
    echo

    echo "Top Memory consuming pods:"
    kubectl top pods --all-namespaces --sort-by=memory | head -10
    echo

    echo "Pods without resource requests:"
    kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].resources.requests == null) | "\(.metadata.namespace)/\(.metadata.name)"' | head -10
    echo

    echo "Pods without resource limits:"
    kubectl get pods --all-namespaces -o json | jq -r '.items[] | select(.spec.containers[].resources.limits == null) | "\(.metadata.namespace)/\(.metadata.name)"' | head -10
    echo
}

# Fonction pour analyser l'efficacité des ressources
analyze_efficiency() {
    echo "=== RESOURCE EFFICIENCY ANALYSIS ==="

    # Calculer le ratio requests/limits
    echo "Resource requests vs limits analysis:"
    kubectl get pods --all-namespaces -o json | jq -r '
    .items[] |
    select(.spec.containers[].resources.requests != null and .spec.containers[].resources.limits != null) |
    {
        namespace: .metadata.namespace,
        name: .metadata.name,
        cpu_request: .spec.containers[0].resources.requests.cpu,
        cpu_limit: .spec.containers[0].resources.limits.cpu,
        memory_request: .spec.containers[0].resources.requests.memory,
        memory_limit: .spec.containers[0].resources.limits.memory
    }' 2>/dev/null | head -10
    echo

    # Identifier les pods sous-utilisés
    echo "Potentially over-provisioned pods (low utilization):"
    kubectl top pods --all-namespaces --containers | awk '
    NR>1 && $3 != "" && $4 != "" {
        cpu_val = $3; gsub(/[^0-9]/, "", cpu_val);
        mem_val = $4; gsub(/[^0-9]/, "", mem_val);
        if (cpu_val < 10 && mem_val < 50) print $1"/"$2
    }' | head -10
    echo
}

# Fonction pour analyser le scaling
analyze_scaling() {
    echo "=== AUTOSCALING ANALYSIS ==="

    echo "HPA status:"
    kubectl get hpa --all-namespaces
    echo

    echo "VPA status:"
    kubectl get vpa --all-namespaces 2>/dev/null || echo "VPA not installed"
    echo

    echo "Recent HPA events:"
    kubectl get events --all-namespaces --field-selector reason=SuccessfulRescale | tail -10
    echo
}

# Générer des recommandations
generate_recommendations() {
    echo "=== OPTIMIZATION RECOMMENDATIONS ==="

    echo "1. Resource Optimization:"
    echo "   - Review pods without resource limits"
    echo "   - Optimize over-provisioned pods"
    echo "   - Consider using VPA for automatic sizing"
    echo

    echo "2. Scaling Optimization:"
    echo "   - Enable HPA for variable workloads"
    echo "   - Configure cluster autoscaler for cost optimization"
    echo "   - Use priority classes for workload prioritization"
    echo

    echo "3. Node Optimization:"
    echo "   - Consider node sizes vs workload requirements"
    echo "   - Evaluate spot instances for non-critical workloads"
    echo "   - Monitor node utilization for right-sizing"
    echo
}

# Exécution de l'analyse
analyze_nodes
analyze_pods
analyze_efficiency
analyze_scaling
generate_recommendations

echo "Analysis completed at $(date)"
```

### Étape 6.2 : Optimisation automatique avec VPA recommender

Créez `performance/vpa-recommender-job.yaml` :

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: vpa-recommender-report
  namespace: performance-test
spec:
  schedule: '0 */6 * * *' # Toutes les 6 heures
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: vpa-analyzer
              image: bitnami/kubectl:latest
              command:
                - /bin/bash
                - -c
                - |
                  echo "=== VPA Recommendations Report $(date) ==="

                  # Analyser toutes les VPA
                  for vpa in $(kubectl get vpa --all-namespaces -o name); do
                    echo "Analyzing $vpa"
                    kubectl describe $vpa | grep -A 20 "Recommendation:"
                    echo "---"
                  done

                  # Générer des recommandations d'optimisation
                  echo "=== Optimization Suggestions ==="

                  # Pods avec des écarts importants entre requests et recommandations
                  kubectl get vpa --all-namespaces -o json | jq -r '
                  .items[] | 
                  select(.status.recommendation != null) |
                  {
                    name: .metadata.name,
                    namespace: .metadata.namespace,
                    recommendations: .status.recommendation.containerRecommendations
                  }'

          restartPolicy: OnFailure
```

### Étape 6.3 : QoS (Quality of Service) Classes

Créez `performance/qos-examples.yaml` :

```yaml
# Guaranteed QoS - ressources requests = limits
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed-pod
  namespace: performance-test
  labels:
    qos: guaranteed
spec:
  containers:
    - name: app
      image: busybox
      command: ['sleep', '3600']
      resources:
        requests:
          cpu: 200m
          memory: 256Mi
        limits:
          cpu: 200m
          memory: 256Mi
---
# Burstable QoS - ressources requests < limits
apiVersion: v1
kind: Pod
metadata:
  name: burstable-pod
  namespace: performance-test
  labels:
    qos: burstable
spec:
  containers:
    - name: app
      image: busybox
      command: ['sleep', '3600']
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
---
# BestEffort QoS - pas de ressources spécifiées
apiVersion: v1
kind: Pod
metadata:
  name: besteffort-pod
  namespace: performance-test
  labels:
    qos: besteffort
spec:
  containers:
    - name: app
      image: busybox
      command: ['sleep', '3600']
      # Aucune ressource spécifiée
```

## Exercice 7 : Tests de charge et benchmarking

### Étape 7.1 : Générateur de charge avec K6

Créez `performance/load-test-k6.yaml` :

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: k6-load-test
  namespace: performance-test
data:
  load-test.js: |
    import http from 'k6/http';
    import { check, sleep } from 'k6';

    export let options = {
      stages: [
        { duration: '5m', target: 100 },   // Montée progressive
        { duration: '10m', target: 100 },  // Plateau
        { duration: '5m', target: 200 },   // Pic de charge
        { duration: '10m', target: 200 },  // Plateau élevé
        { duration: '5m', target: 0 },     // Descente
      ],
      thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.1'],
      },
    };

    export default function() {
      let response = http.get(`http://${__ENV.TARGET_HOST}/`);
      
      check(response, {
        'status is 200': (r) => r.status === 200,
        'response time < 500ms': (r) => r.timings.duration < 500,
      });
      
      // Test différents endpoints
      if (Math.random() < 0.3) {
        http.get(`http://${__ENV.TARGET_HOST}/health`);
      }
      
      sleep(1);
    }
---
apiVersion: batch/v1
kind: Job
metadata:
  name: k6-load-test
  namespace: performance-test
spec:
  template:
    spec:
      containers:
        - name: k6
          image: grafana/k6:latest
          command:
            - k6
            - run
            - /scripts/load-test.js
          env:
            - name: TARGET_HOST
              value: 'performance-web-service.performance-test.svc.cluster.local'
          volumeMounts:
            - name: k6-script
              mountPath: /scripts
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
      volumes:
        - name: k6-script
          configMap:
            name: k6-load-test
      restartPolicy: Never
```

### Étape 7.2 : Test de stress CPU/Mémoire

Créez `performance/stress-test.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: cpu-stress-test
  namespace: performance-test
spec:
  parallelism: 3
  completions: 3
  template:
    spec:
      containers:
        - name: stress
          image: alexeiled/stress-ng:latest
          command:
            - stress-ng
            - --cpu
            - '2'
            - --cpu-load
            - '90'
            - --timeout
            - '300s'
            - --metrics-brief
          resources:
            requests:
              cpu: 1000m
              memory: 256Mi
            limits:
              cpu: 2000m
              memory: 512Mi
      restartPolicy: Never
---
apiVersion: batch/v1
kind: Job
metadata:
  name: memory-stress-test
  namespace: performance-test
spec:
  template:
    spec:
      containers:
        - name: stress
          image: alexeiled/stress-ng:latest
          command:
            - stress-ng
            - --vm
            - '2'
            - --vm-bytes
            - '512M'
            - --vm-keep
            - --timeout
            - '300s'
            - --metrics-brief
          resources:
            requests:
              cpu: 100m
              memory: 1Gi
            limits:
              cpu: 200m
              memory: 1Gi
      restartPolicy: Never
```

### Étape 7.3 : Monitoring pendant les tests

Créez `scripts/monitor-performance.sh` :

```bash
#!/bin/bash

NAMESPACE="performance-test"
DURATION=${1:-300}  # 5 minutes par défaut

echo "Starting performance monitoring for $DURATION seconds..."

# Fonction pour surveiller les métriques
monitor_metrics() {
    while true; do
        echo "=== $(date) ==="

        echo "CPU Usage:"
        kubectl top pods -n $NAMESPACE --sort-by=cpu | head -10

        echo "Memory Usage:"
        kubectl top pods -n $NAMESPACE --sort-by=memory | head -10

        echo "HPA Status:"
        kubectl get hpa -n $NAMESPACE

        echo "Node Usage:"
        kubectl top nodes

        echo "---"
        sleep 30
    done
}

# Démarrer le monitoring en arrière-plan
monitor_metrics &
MONITOR_PID=$!

# Lancer les tests de charge
echo "Starting load tests..."
kubectl apply -f performance/load-test-k6.yaml
kubectl apply -f performance/stress-test.yaml

# Attendre la durée spécifiée
sleep $DURATION

# Arrêter le monitoring
kill $MONITOR_PID

echo "Performance monitoring completed"

# Collecter les résultats
echo "=== Final Results ==="
kubectl get hpa -n $NAMESPACE
kubectl get pods -n $NAMESPACE
kubectl top pods -n $NAMESPACE
kubectl top nodes
```

## Exercice 8 : Affinity et anti-affinity

### Étape 8.1 : Node Affinity

Créez `performance/node-affinity.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-performance-app
  namespace: performance-test
spec:
  replicas: 3
  selector:
    matchLabels:
      app: high-performance
  template:
    metadata:
      labels:
        app: high-performance
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values: ['c5.xlarge', 'c5.2xlarge']
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              preference:
                matchExpressions:
                  - key: topology.kubernetes.io/zone
                    operator: In
                    values: ['us-west-2a']
            - weight: 50
              preference:
                matchExpressions:
                  - key: node-type
                    operator: In
                    values: ['compute-optimized']
      containers:
        - name: app
          image: busybox
          command: ['sleep', '3600']
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
```

### Étape 8.2 : Pod Anti-Affinity

Créez `performance/pod-anti-affinity.yaml` :

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: distributed-app
  namespace: performance-test
spec:
  replicas: 4
  selector:
    matchLabels:
      app: distributed
  template:
    metadata:
      labels:
        app: distributed
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchExpressions:
                  - key: app
                    operator: In
                    values: ['distributed']
              topologyKey: 'kubernetes.io/hostname'
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: ['distributed']
                topologyKey: 'topology.kubernetes.io/zone'
      containers:
        - name: app
          image: nginx:alpine
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
```

### Étape 8.3 : Taints et Tolerations

Créez `performance/taints-tolerations.yaml` :

```yaml
# D'abord, appliquer des taints aux nœuds
# kubectl taint nodes node-gpu gpu=true:NoSchedule
# kubectl taint nodes node-ssd storage=ssd:NoSchedule

apiVersion: apps/v1
kind: Deployment
metadata:
  name: gpu-workload
  namespace: performance-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gpu-workload
  template:
    metadata:
      labels:
        app: gpu-workload
    spec:
      tolerations:
        - key: 'gpu'
          operator: 'Equal'
          value: 'true'
          effect: 'NoSchedule'
      nodeSelector:
        accelerator: 'nvidia-tesla-k80'
      containers:
        - name: gpu-app
          image: tensorflow/tensorflow:latest-gpu
          command: ['sleep', '3600']
          resources:
            requests:
              nvidia.com/gpu: 1
            limits:
              nvidia.com/gpu: 1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ssd-workload
  namespace: performance-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ssd-workload
  template:
    metadata:
      labels:
        app: ssd-workload
    spec:
      tolerations:
        - key: 'storage'
          operator: 'Equal'
          value: 'ssd'
          effect: 'NoSchedule'
      containers:
        - name: database
          image: postgres:13
          env:
            - name: POSTGRES_PASSWORD
              value: 'password'
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 1000m
              memory: 2Gi
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: ssd-pvc
```

## Exercice 9 : Monitoring et alerting des performances

### Étape 9.1 : Dashboard Grafana pour les performances

Créez `monitoring/performance-dashboard.json` :

```json
{
  "dashboard": {
    "title": "Kubernetes Performance Monitoring",
    "panels": [
      {
        "title": "HPA Scaling Events",
        "type": "graph",
        "targets": [
          {
            "expr": "kube_horizontalpodautoscaler_status_current_replicas",
            "legendFormat": "{{ horizontalpodautoscaler }} - Current"
          },
          {
            "expr": "kube_horizontalpodautoscaler_status_desired_replicas",
            "legendFormat": "{{ horizontalpodautoscaler }} - Desired"
          }
        ]
      },
      {
        "title": "Resource Utilization vs Requests",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total[5m]) / on(pod) group_left() kube_pod_container_resource_requests{resource=\"cpu\"}",
            "legendFormat": "CPU Utilization Ratio"
          },
          {
            "expr": "container_memory_working_set_bytes / on(pod) group_left() kube_pod_container_resource_requests{resource=\"memory\"}",
            "legendFormat": "Memory Utilization Ratio"
          }
        ]
      }
    ]
  }
}
```

### Étape 9.2 : Alertes de performance

Créez `monitoring/performance-alerts.yaml` :

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: performance-alerts
  namespace: monitoring
spec:
  groups:
    - name: performance.rules
      rules:
        - alert: HPAMaxReplicasReached
          expr: kube_horizontalpodautoscaler_status_current_replicas == kube_horizontalpodautoscaler_spec_max_replicas
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: 'HPA has reached maximum replicas'
            description: 'HPA {{ $labels.horizontalpodautoscaler }} has reached its maximum of {{ $value }} replicas'

        - alert: PodResourceLimitExceeded
          expr: container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9
          for: 2m
          labels:
            severity: critical
          annotations:
            summary: 'Pod exceeding memory limit'
            description: 'Pod {{ $labels.pod }} is using {{ $value | humanizePercentage }} of its memory limit'

        - alert: NodeResourceExhaustion
          expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.85
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: 'Node memory usage is high'
            description: 'Node {{ $labels.instance }} memory usage is {{ $value | humanizePercentage }}'

        - alert: ClusterScalingIssues
          expr: increase(cluster_autoscaler_failed_scale_ups_total[10m]) > 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: 'Cluster autoscaler failed to scale up'
            description: 'Cluster autoscaler has failed to scale up {{ $value }} times in the last 10 minutes'
```

## Exercice 10 : Cas pratique complet

### Objectif

Optimisez complètement la plateforme e-commerce pour :

1. **Gérer 10x plus de trafic** avec scaling automatique
2. **Optimiser les coûts** en réduisant le gaspillage de ressources
3. **Maintenir les SLA** de performance (latence < 200ms, availability > 99.9%)
4. **Assurer la résilience** avec distribution géographique

### Tests à effectuer

1. **Test de montée en charge progressive** (1 → 1000 utilisateurs)
2. **Test de pic de trafic soudain** (Black Friday simulation)
3. **Test de resilience** (panne de nœuds pendant la charge)
4. **Test d'optimisation** (avant/après VPA/HPA)
5. **Test de coût** (utilisation des ressources vs demande)

### Architecture finale attendue

- **Auto-scaling** : HPA, VPA, Cluster Autoscaler configurés
- **Optimisation** : QoS classes, priority classes, resource quotas
- **Distribution** : Anti-affinity, taints/tolerations, zone spreading
- **Monitoring** : Métriques temps réel, alertes proactives
- **Automation** : Scripts de test et validation automatiques

## Questions de validation

1. Quelle est la différence entre HPA et VPA ? Quand utiliser chacun ?
2. Comment configurer une stratégie de scaling réactive vs prédictive ?
3. Expliquez l'impact des QoS classes sur le scheduling
4. Comment optimiser les coûts avec le cluster autoscaler ?
5. Quelles métriques surveiller pour les performances ?

## Livrables attendus

1. **Applications** avec scaling automatique configuré
2. **HPA et VPA** configurés et testés
3. **Cluster Autoscaler** déployé et fonctionnel
4. **Tests de charge** automatisés avec rapports
5. **Optimisation des ressources** documentée
6. **Monitoring** des performances en temps réel
7. **Alertes** pour les problèmes de performance
8. **Documentation** des stratégies de scaling
9. **Scripts** d'automatisation et de test

## Critères d'évaluation

- **Scaling** : Réactivité et efficacité du scaling automatique
- **Optimisation** : Réduction du gaspillage de ressources
- **Performance** : Maintien des SLA sous charge
- **Monitoring** : Observabilité complète des performances
- **Automation** : Tests et validations automatisés
- **Documentation** : Stratégies et procédures claires

## Ressources utiles

- [Kubernetes HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)
- [Cluster Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler)
- [Resource Management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

---

**Durée estimée : 8-9 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
