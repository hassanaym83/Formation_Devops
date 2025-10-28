# LAB 9 - Monitoring et debugging

## Objectifs

- Maîtriser les outils de monitoring natifs Kubernetes
- Implémenter les health checks et probes
- Diagnostiquer et résoudre les problèmes courants
- Utiliser les métriques et logs pour l'observabilité

## Contexte

Mise en place d'un système de surveillance et de diagnostic pour maintenir la santé des applications.

## Prérequis

- Cluster Kubernetes fonctionnel
- Applications déployées (LABs précédents)

## Instructions

### 1. Configuration des Health Checks

```yaml
# Créer le fichier webapp-health-checks.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-health-checks
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp-health
  template:
    metadata:
      labels:
        app: webapp-health
    spec:
      containers:
        - name: webapp
          image: nginx:1.21
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: '64Mi'
              cpu: '100m'
            limits:
              memory: '128Mi'
              cpu: '200m'
          # Startup Probe - pour les applications lentes à démarrer
          startupProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 10
          # Liveness Probe - redémarre le conteneur si échec
          livenessProbe:
            httpGet:
              path: /
              port: 80
              httpHeaders:
                - name: Custom-Header
                  value: liveness-check
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          # Readiness Probe - retire du service si échec
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2
          # Health check endpoint personnalisé
          volumeMounts:
            - name: health-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: health-config
          configMap:
            name: health-check-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: health-check-config
data:
  index.html: |
    <!DOCTYPE html>
    <html>
    <head><title>Health Check App</title></head>
    <body>
      <h1>Application Health Check</h1>
      <p>Status: <span style="color: green;">Healthy</span></p>
      <p>Pod: <span id="hostname"></span></p>
      <p>Timestamp: <span id="time"></span></p>
      <script>
        document.getElementById('hostname').textContent = window.location.hostname;
        document.getElementById('time').textContent = new Date().toISOString();
      </script>
    </body>
    </html>
  health.html: |
    {
      "status": "healthy",
      "timestamp": "$(date -Iseconds)",
      "checks": {
        "database": "connected",
        "cache": "available", 
        "external_api": "reachable"
      }
    }

---
apiVersion: v1
kind: Service
metadata:
  name: webapp-health-service
spec:
  selector:
    app: webapp-health
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
```

```bash
# Déployer l'application avec health checks
kubectl apply -f webapp-health-checks.yaml

# Observer le démarrage des pods avec les probes
kubectl get pods -l app=webapp-health -w

# Vérifier les détails des probes
kubectl describe pod -l app=webapp-health
```

### 2. Simulation d'erreurs et debugging

```yaml
# Créer le fichier faulty-app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: faulty-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: faulty-app
  template:
    metadata:
      labels:
        app: faulty-app
    spec:
      containers:
        - name: app
          image: busybox
          command: ['/bin/sh']
          args: ['-c', 'sleep 30 && exit 1'] # Simule une app qui crash
          livenessProbe:
            exec:
              command: ['sh', '-c', 'exit 0']
            initialDelaySeconds: 10
            periodSeconds: 5
          readinessProbe:
            exec:
              command: ['sh', '-c', 'exit 1'] # Toujours en échec
            initialDelaySeconds: 5
            periodSeconds: 3

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: slow-startup-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: slow-startup
  template:
    metadata:
      labels:
        app: slow-startup
    spec:
      containers:
        - name: app
          image: nginx:1.21
          command: ['/bin/sh']
          args: ['-c', "sleep 60 && nginx -g 'daemon off;'"] # Démarrage lent
          ports:
            - containerPort: 80
          startupProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 10
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
```

```bash
# Déployer les applications défaillantes
kubectl apply -f faulty-app.yaml

# Observer les différents états d'erreur
kubectl get pods -l app=faulty-app -w
kubectl get pods -l app=slow-startup -w

# Analyser les événements
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe pod -l app=faulty-app
```

### 3. Logs et troubleshooting

```bash
# Consulter les logs des applications
kubectl logs -l app=webapp-health
kubectl logs -l app=faulty-app
kubectl logs -l app=faulty-app --previous  # Logs du conteneur précédent

# Logs en temps réel
kubectl logs -f deployment/webapp-health-checks

# Logs avec timestamps
kubectl logs --timestamps=true -l app=webapp-health

# Exporter les logs vers un fichier
kubectl logs -l app=webapp-health --since=1h > webapp-logs.txt

# Debug interactif
kubectl exec -it deployment/webapp-health-checks -- /bin/bash

# Si bash n'est pas disponible
kubectl exec -it deployment/webapp-health-checks -- /bin/sh

# Copier des fichiers depuis/vers un pod
kubectl cp webapp-logs.txt <pod-name>:/tmp/
kubectl cp <pod-name>:/var/log/nginx/access.log ./access.log
```

### 4. Métriques et monitoring avec kubectl

```bash
# Métriques des nodes
kubectl top nodes

# Métriques des pods
kubectl top pods
kubectl top pods --containers
kubectl top pods -l app=webapp-health

# Utilisation des ressources par namespace
kubectl top pods --all-namespaces

# Tri par utilisation CPU/Memory
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory

# Surveiller l'utilisation en temps réel
watch kubectl top pods -l app=webapp-health
```

### 5. Monitoring avancé avec Prometheus (simulation)

```yaml
# Créer le fichier monitoring-stack.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus-simulation
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: prometheus-config
              mountPath: /etc/prometheus
          command:
            - prometheus
            - --config.file=/etc/prometheus/prometheus.yml
            - --storage.tsdb.path=/prometheus/
            - --web.console.libraries=/etc/prometheus/console_libraries
            - --web.console.templates=/etc/prometheus/consoles
      volumes:
        - name: prometheus-config
          configMap:
            name: prometheus-config

---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
spec:
  selector:
    app: prometheus
  ports:
    - port: 9090
      targetPort: 9090
  type: ClusterIP

---
# Application avec métriques Prometheus
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: metrics-app
  template:
    metadata:
      labels:
        app: metrics-app
      annotations:
        prometheus.io/scrape: 'true'
        prometheus.io/port: '8080'
        prometheus.io/path: '/metrics'
    spec:
      containers:
        - name: app
          image: nginx:1.21
          ports:
            - containerPort: 80
            - containerPort: 8080 # Port pour métriques
          volumeMounts:
            - name: metrics-config
              mountPath: /usr/share/nginx/html
      volumes:
        - name: metrics-config
          configMap:
            name: metrics-config

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: metrics-config
data:
  metrics: |
    # TYPE http_requests_total counter
    http_requests_total{method="GET",status="200"} 1234
    http_requests_total{method="POST",status="200"} 567
    http_requests_total{method="GET",status="404"} 89

    # TYPE http_request_duration_seconds histogram
    http_request_duration_seconds_bucket{le="0.1"} 100
    http_request_duration_seconds_bucket{le="0.5"} 200
    http_request_duration_seconds_bucket{le="1.0"} 300
    http_request_duration_seconds_bucket{le="+Inf"} 350
    http_request_duration_seconds_sum 87.5
    http_request_duration_seconds_count 350

    # TYPE memory_usage_bytes gauge
    memory_usage_bytes 67108864

    # TYPE cpu_usage_percent gauge  
    cpu_usage_percent 23.5
```

```bash
# Déployer le stack de monitoring
kubectl apply -f monitoring-stack.yaml

# Port-forward pour accéder à Prometheus
kubectl port-forward service/prometheus-service 9090:9090 &

# Tester l'accès aux métriques
curl http://localhost:8080/metrics
```

### 6. Alerting et notifications

```yaml
# Créer le fichier alerting-rules.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alert-rules
data:
  alerts.yml: |
    groups:
    - name: kubernetes-alerts
      rules:
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"
          description: "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} has restarted {{ $value }} times in the last 15 minutes"
      
      - alert: PodNotReady
        expr: kube_pod_status_ready{condition="false"} == 1
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} not ready"
          
      - alert: HighMemoryUsage
        expr: (container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage detected"

---
# Simulateur d'alertes
apiVersion: v1
kind: Pod
metadata:
  name: alert-simulator
spec:
  containers:
    - name: simulator
      image: busybox
      command: ['/bin/sh']
      args:
        [
          '-c',
          "while true; do echo 'Alert: High CPU usage detected at $(date)'; sleep 60; done"
        ]
```

### 7. Dashboard et observabilité

```bash
# Créer un dashboard simple en CLI
kubectl create configmap dashboard-config --from-literal=config.json='{
  "dashboard": {
    "title": "Kubernetes Overview",
    "panels": [
      {"title": "Pod Status", "query": "kube_pod_status_phase"},
      {"title": "CPU Usage", "query": "rate(cpu_usage_seconds_total[5m])"},
      {"title": "Memory Usage", "query": "memory_usage_bytes"}
    ]
  }
}'

# Script de monitoring en temps réel
cat > monitor.sh << 'EOF'
#!/bin/bash
while true; do
  clear
  echo "=== KUBERNETES CLUSTER OVERVIEW ==="
  echo "Date: $(date)"
  echo

  echo "=== NODES ==="
  kubectl top nodes 2>/dev/null || echo "Metrics server not available"
  echo

  echo "=== PODS BY STATUS ==="
  kubectl get pods --all-namespaces --field-selector=status.phase!=Running | tail -n +2 | wc -l | xargs echo "Non-running pods:"
  kubectl get pods --all-namespaces | grep -E "(Error|CrashLoop|Pending)" || echo "All pods healthy"
  echo

  echo "=== TOP RESOURCE CONSUMERS ==="
  kubectl top pods --all-namespaces --sort-by=memory 2>/dev/null | head -5 || echo "Metrics not available"
  echo

  echo "=== RECENT EVENTS ==="
  kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -5

  sleep 30
done
EOF

chmod +x monitor.sh
./monitor.sh
```

### 8. Debugging avancé et root cause analysis

```bash
# Analyser un pod en échec
POD_NAME=$(kubectl get pods -l app=faulty-app -o jsonpath='{.items[0].metadata.name}')

# Informations détaillées
kubectl describe pod $POD_NAME

# Logs détaillés avec contexte
kubectl logs $POD_NAME --previous --timestamps=true

# Vérifier les ressources limitantes
kubectl describe node $(kubectl get pod $POD_NAME -o jsonpath='{.spec.nodeName}')

# Débugger les problèmes réseau
kubectl exec -it $POD_NAME -- nslookup kubernetes.default
kubectl exec -it $POD_NAME -- ping google.com

# Analyser les configurations
kubectl get pod $POD_NAME -o yaml
kubectl get events --field-selector involvedObject.name=$POD_NAME

# Créer un pod de debug temporaire
kubectl run debug-pod --image=nicolaka/netshoot -it --rm --restart=Never -- /bin/bash

# Nettoyage
kubectl delete -f faulty-app.yaml
kubectl delete -f monitoring-stack.yaml
rm monitor.sh webapp-logs.txt
```

## Livrables attendus

1. Application avec health checks configurés
2. Simulation et résolution d'erreurs
3. Collection et analyse de logs
4. Dashboard de monitoring fonctionnel
5. Script de surveillance automatisé

## Critères de validation

- [ ] Health checks (startup, liveness, readiness) opérationnels
- [ ] Debugging d'applications défaillantes réussi
- [ ] Logs collectés et analysés correctement
- [ ] Métriques système consultées avec kubectl top
- [ ] Monitoring stack déployé et accessible
- [ ] Alerting et dashboard configurés

## Durée estimée

35 minutes

## Concepts clés monitoring

### Types de Health Checks

- **startupProbe** : Vérifie le démarrage initial
- **livenessProbe** : Redémarre si échec
- **readinessProbe** : Retire du load balancer si échec

### Métriques importantes

```bash
# Ressources système
kubectl top nodes/pods

# États des objets
kubectl get pods/services/ingress

# Événements système
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Commandes de debugging

```bash
# Logs
kubectl logs <pod> --previous --timestamps
kubectl logs -f deployment/<name>

# Debug interactif
kubectl exec -it <pod> -- /bin/bash
kubectl describe pod/node/service <name>

# Métriques
kubectl top nodes/pods
watch kubectl get pods
```
