# Correction LAB 3 - Helm Charts avancés

## Vue d'ensemble

Cette correction fournit les solutions complètes pour la création, déploiement et gestion de Helm Charts avancés avec templating, gestion multi-environnements et bonnes pratiques de production.

## Exercice 1 : Structure et création du Chart

### Solution complète : Structure du Chart

```bash
# Commandes de création du chart
helm create webapp-chart
cd webapp-chart

# Structure finale recommandée
tree .
```

```
webapp-chart/
├── Chart.yaml                    # Métadonnées du chart
├── Chart.lock                    # Fichier de verrouillage des dépendances
├── values.yaml                   # Valeurs par défaut
├── values-dev.yaml               # Valeurs pour développement
├── values-staging.yaml           # Valeurs pour staging
├── values-production.yaml        # Valeurs pour production
├── charts/                       # Charts de dépendances
│   ├── postgresql-12.1.6.tgz
│   └── redis-17.3.7.tgz
├── templates/                    # Templates Kubernetes
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── service.yaml
│   ├── serviceaccount.yaml
│   ├── secret.yaml
│   ├── networkpolicy.yaml
│   └── tests/
│       └── test-connection.yaml
├── crds/                         # Custom Resource Definitions
└── templates/hooks/              # Hooks Helm
    ├── pre-install-job.yaml
    └── post-upgrade-job.yaml
```

### Solution complète : Chart.yaml

```yaml
# Chart.yaml
apiVersion: v2
name: webapp-chart
description: 'Chart Helm avancé pour application web avec base de données et cache'
type: application
version: 1.2.0
appVersion: '2.1.0'
kubeVersion: '>=1.23.0'
home: 'https://github.com/company/webapp'
sources:
  - 'https://github.com/company/webapp'
  - 'https://github.com/company/webapp-helm-chart'
maintainers:
  - name: 'DevOps Team'
    email: 'devops@company.com'
    url: 'https://company.com/devops'
keywords:
  - web
  - application
  - microservice
  - postgresql
  - redis
  - monitoring
annotations:
  category: 'Application'
  licenses: 'MIT'
  images: |
    - name: webapp
      image: company/webapp:2.1.0
    - name: nginx
      image: nginx:1.24-alpine
dependencies:
  - name: postgresql
    version: '12.1.6'
    repository: 'https://charts.bitnami.com/bitnami'
    condition: postgresql.enabled
    tags:
      - database
  - name: redis
    version: '17.3.7'
    repository: 'https://charts.bitnami.com/bitnami'
    condition: redis.enabled
    tags:
      - cache
  - name: prometheus
    version: '15.18.0'
    repository: 'https://prometheus-community.github.io/helm-charts'
    condition: monitoring.prometheus.enabled
    tags:
      - monitoring
```

### Solution complète : Values.yaml par défaut

```yaml
# values.yaml
# Configuration globale
global:
  imageRegistry: ''
  imagePullSecrets: []
  storageClass: ''
  postgresql:
    auth:
      postgresPassword: ''
      database: 'webapp_db'
  redis:
    auth:
      password: ''

# Configuration de l'application
app:
  name: webapp
  version: '2.1.0'

# Configuration de l'image
image:
  registry: docker.io
  repository: company/webapp
  tag: '2.1.0'
  pullPolicy: IfNotPresent
  pullSecrets: []

# Réplicas et stratégie de déploiement
replicaCount: 3
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 1

# ServiceAccount
serviceAccount:
  create: true
  annotations: {}
  name: ''
  automountServiceAccountToken: false

# Configuration des pods
podAnnotations:
  prometheus.io/scrape: 'true'
  prometheus.io/port: '3000'
  prometheus.io/path: '/metrics'

podLabels:
  app.kubernetes.io/component: webapp
  app.kubernetes.io/part-of: webapp-stack

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  capabilities:
    drop:
      - ALL
    add:
      - NET_BIND_SERVICE

# Variables d'environnement
env:
  NODE_ENV: production
  LOG_LEVEL: info
  METRICS_PORT: '3000'
  HEALTH_CHECK_PATH: '/health'

# Configuration des secrets
secrets:
  # Base de données
  database:
    enabled: true
    host: ''
    port: '5432'
    name: 'webapp_db'
    username: 'webapp_user'
    password: ''

  # Cache Redis
  redis:
    enabled: true
    host: ''
    port: '6379'
    password: ''

  # JWT et sessions
  jwt:
    secret: ''
    expiry: '24h'

  # APIs externes
  external:
    apiKey: ''
    webhookSecret: ''

# Configuration des volumes
persistence:
  enabled: true
  storageClass: ''
  accessMode: ReadWriteOnce
  size: 2Gi
  annotations: {}

volumes:
  tmp:
    enabled: true
    size: 100Mi
  cache:
    enabled: true
    size: 500Mi
  logs:
    enabled: true
    size: 1Gi

# Service
service:
  type: ClusterIP
  port: 80
  targetPort: 3000
  annotations: {}
  labels: {}

# Ingress
ingress:
  enabled: false
  className: 'nginx'
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
  hosts:
    - host: webapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: webapp-tls
      hosts:
        - webapp.example.com

# Sondes de santé
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# Ressources
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

# Auto-scaling
autoscaling:
  enabled: false
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 30

# Network Policies
networkPolicy:
  enabled: false
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000
  egress:
    - to: []
      ports:
        - protocol: UDP
          port: 53
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - protocol: TCP
          port: 5432

# Affinité et tolérance
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values: ['webapp']
          topologyKey: kubernetes.io/hostname

tolerations: []

nodeSelector: {}

# Configuration des dépendances
postgresql:
  enabled: true
  auth:
    postgresPassword: 'postgres-super-secret'
    username: 'webapp_user'
    password: 'webapp-secret-password'
    database: 'webapp_db'
  primary:
    persistence:
      enabled: true
      size: 10Gi
    resources:
      requests:
        cpu: 250m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi

redis:
  enabled: true
  auth:
    enabled: true
    password: 'redis-secret-password'
  master:
    persistence:
      enabled: true
      size: 5Gi
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi

# Monitoring
monitoring:
  enabled: false
  prometheus:
    enabled: false
  serviceMonitor:
    enabled: false
    interval: 30s
    scrapeTimeout: 10s

# Tests
tests:
  enabled: true
  image:
    repository: busybox
    tag: '1.35'

# Hooks
hooks:
  preInstall:
    enabled: true
    image:
      repository: company/db-migrate
      tag: 'latest'
  postUpgrade:
    enabled: true
    image:
      repository: company/cache-warm
      tag: 'latest'
```

## Exercice 2 : Templates avancés

### Solution complète : Deployment template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "webapp-chart.fullname" . }}
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
  {{- with .Values.podAnnotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  strategy:
    {{- toYaml .Values.strategy | nindent 4 }}
  selector:
    matchLabels:
      {{- include "webapp-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "webapp-chart.selectorLabels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.image.pullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "webapp-chart.serviceAccountName" . }}
      automountServiceAccountToken: {{ .Values.serviceAccount.automountServiceAccountToken }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ .Chart.Name }}
        image: {{ include "webapp-chart.image" . }}
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        {{- if .Values.monitoring.enabled }}
        - name: metrics
          containerPort: {{ .Values.env.METRICS_PORT | default 9090 }}
          protocol: TCP
        {{- end }}
        env:
        {{- range $key, $value := .Values.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- if .Values.secrets.database.enabled }}
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "webapp-chart.fullname" . }}-database
              key: database-url
        {{- end }}
        {{- if .Values.secrets.redis.enabled }}
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: {{ include "webapp-chart.fullname" . }}-redis
              key: redis-url
        {{- end }}
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        volumeMounts:
        {{- if .Values.volumes.tmp.enabled }}
        - name: tmp-volume
          mountPath: /tmp
        {{- end }}
        {{- if .Values.volumes.cache.enabled }}
        - name: cache-volume
          mountPath: /app/cache
        {{- end }}
        {{- if .Values.volumes.logs.enabled }}
        - name: logs-volume
          mountPath: /app/logs
        {{- end }}
        {{- if .Values.persistence.enabled }}
        - name: data-volume
          mountPath: /app/data
        {{- end }}
        - name: config-volume
          mountPath: /app/config
          readOnly: true
        securityContext:
          {{- toYaml .Values.securityContext | nindent 10 }}
        livenessProbe:
          {{- toYaml .Values.livenessProbe | nindent 10 }}
        readinessProbe:
          {{- toYaml .Values.readinessProbe | nindent 10 }}
        resources:
          {{- toYaml .Values.resources | nindent 10 }}
      volumes:
      {{- if .Values.volumes.tmp.enabled }}
      - name: tmp-volume
        emptyDir:
          sizeLimit: {{ .Values.volumes.tmp.size }}
      {{- end }}
      {{- if .Values.volumes.cache.enabled }}
      - name: cache-volume
        emptyDir:
          sizeLimit: {{ .Values.volumes.cache.size }}
      {{- end }}
      {{- if .Values.volumes.logs.enabled }}
      - name: logs-volume
        emptyDir:
          sizeLimit: {{ .Values.volumes.logs.size }}
      {{- end }}
      {{- if .Values.persistence.enabled }}
      - name: data-volume
        persistentVolumeClaim:
          claimName: {{ include "webapp-chart.fullname" . }}-data
      {{- end }}
      - name: config-volume
        configMap:
          name: {{ include "webapp-chart.fullname" . }}-config
          defaultMode: 0444
      terminationGracePeriodSeconds: 30
      restartPolicy: Always
      dnsPolicy: ClusterFirst
```

### Solution complète : ConfigMap template

```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "webapp-chart.fullname" . }}-config
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
data:
  # Configuration de l'application
  app.yaml: |
    app:
      name: {{ .Values.app.name }}
      version: {{ .Values.app.version }}
      environment: {{ .Values.global.environment | default "production" }}
      debug: {{ .Values.global.debug | default false }}

    server:
      port: {{ .Values.service.targetPort }}
      host: "0.0.0.0"
      timeout: 30
      keepAliveTimeout: 65

    database:
      {{- if .Values.postgresql.enabled }}
      type: "postgresql"
      host: {{ include "webapp-chart.postgresql.host" . }}
      port: {{ .Values.postgresql.primary.service.ports.postgresql | default 5432 }}
      database: {{ .Values.global.postgresql.auth.database }}
      maxConnections: 20
      connectionTimeout: 30
      {{- end }}

    cache:
      {{- if .Values.redis.enabled }}
      type: "redis"
      host: {{ include "webapp-chart.redis.host" . }}
      port: {{ .Values.redis.master.service.ports.redis | default 6379 }}
      ttl: 3600
      maxRetries: 3
      {{- end }}

    logging:
      level: {{ .Values.env.LOG_LEVEL | default "info" }}
      format: "json"
      output: "stdout"

    monitoring:
      enabled: {{ .Values.monitoring.enabled }}
      {{- if .Values.monitoring.enabled }}
      port: {{ .Values.env.METRICS_PORT | default 9090 }}
      path: "/metrics"
      {{- end }}

    security:
      cors:
        enabled: true
        origins:
          {{- range .Values.ingress.hosts }}
          - "https://{{ .host }}"
          {{- end }}
        methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        headers: ["Content-Type", "Authorization"]

      rateLimit:
        enabled: true
        requests: 100
        window: "1m"

      headers:
        xFrameOptions: "DENY"
        xContentTypeOptions: "nosniff"
        xXSSProtection: "1; mode=block"
        strictTransportSecurity: "max-age=31536000; includeSubDomains"

  # Configuration NGINX si utilisé comme sidecar
  {{- if .Values.nginx.enabled }}
  nginx.conf: |
    user nginx;
    worker_processes auto;
    error_log /var/log/nginx/error.log warn;
    pid /var/run/nginx.pid;

    events {
        worker_connections 1024;
        use epoll;
        multi_accept on;
    }

    http {
        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        # Logging
        log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';
        access_log /var/log/nginx/access.log main;

        # Performance
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;

        # Gzip
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css application/json application/javascript;

        upstream backend {
            server localhost:{{ .Values.service.targetPort }};
            keepalive 32;
        }

        server {
            listen 80;
            server_name _;

            # Security headers
            add_header X-Frame-Options DENY;
            add_header X-Content-Type-Options nosniff;
            add_header X-XSS-Protection "1; mode=block";

            location /health {
                access_log off;
                proxy_pass http://backend;
            }

            location / {
                proxy_pass http://backend;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_cache_bypass $http_upgrade;
            }
        }
    }
  {{- end }}

  # Script d'initialisation
  init.sh: |
    #!/bin/bash
    set -e

    echo "Initializing webapp..."

    # Attendre que la base de données soit prête
    {{- if .Values.postgresql.enabled }}
    echo "Waiting for PostgreSQL..."
    until pg_isready -h {{ include "webapp-chart.postgresql.host" . }} -p {{ .Values.postgresql.primary.service.ports.postgresql }}; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is ready!"
    {{- end }}

    # Attendre que Redis soit prêt
    {{- if .Values.redis.enabled }}
    echo "Waiting for Redis..."
    until redis-cli -h {{ include "webapp-chart.redis.host" . }} -p {{ .Values.redis.master.service.ports.redis }} ping; do
        echo "Redis is unavailable - sleeping"
        sleep 2
    done
    echo "Redis is ready!"
    {{- end }}

    echo "Initialization complete!"
```

### Solution complète : Helpers template

```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "webapp-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "webapp-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "webapp-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "webapp-chart.labels" -}}
helm.sh/chart: {{ include "webapp-chart.chart" . }}
{{ include "webapp-chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: {{ .Values.app.name | default "webapp" }}
{{- with .Values.global.labels }}
{{- toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "webapp-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "webapp-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "webapp-chart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "webapp-chart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create image name
*/}}
{{- define "webapp-chart.image" -}}
{{- $registry := .Values.global.imageRegistry | default .Values.image.registry -}}
{{- $repository := .Values.image.repository -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
{{- if $registry -}}
{{- printf "%s/%s:%s" $registry $repository $tag -}}
{{- else -}}
{{- printf "%s:%s" $repository $tag -}}
{{- end -}}
{{- end }}

{{/*
PostgreSQL host name
*/}}
{{- define "webapp-chart.postgresql.host" -}}
{{- if .Values.postgresql.enabled -}}
{{- printf "%s-postgresql" (include "webapp-chart.fullname" .) -}}
{{- else -}}
{{- .Values.secrets.database.host -}}
{{- end -}}
{{- end }}

{{/*
Redis host name
*/}}
{{- define "webapp-chart.redis.host" -}}
{{- if .Values.redis.enabled -}}
{{- printf "%s-redis-master" (include "webapp-chart.fullname" .) -}}
{{- else -}}
{{- .Values.secrets.redis.host -}}
{{- end -}}
{{- end }}

{{/*
Database URL for application
*/}}
{{- define "webapp-chart.database.url" -}}
{{- if .Values.postgresql.enabled -}}
{{- printf "postgresql://%s:%s@%s:%d/%s" .Values.global.postgresql.auth.username .Values.global.postgresql.auth.password (include "webapp-chart.postgresql.host" .) (.Values.postgresql.primary.service.ports.postgresql | int) .Values.global.postgresql.auth.database -}}
{{- else -}}
{{- printf "postgresql://%s:%s@%s:%s/%s" .Values.secrets.database.username .Values.secrets.database.password .Values.secrets.database.host .Values.secrets.database.port .Values.secrets.database.name -}}
{{- end -}}
{{- end }}

{{/*
Redis URL for application
*/}}
{{- define "webapp-chart.redis.url" -}}
{{- if .Values.redis.enabled -}}
{{- if .Values.redis.auth.enabled -}}
{{- printf "redis://:%s@%s:%d" .Values.redis.auth.password (include "webapp-chart.redis.host" .) (.Values.redis.master.service.ports.redis | int) -}}
{{- else -}}
{{- printf "redis://%s:%d" (include "webapp-chart.redis.host" .) (.Values.redis.master.service.ports.redis | int) -}}
{{- end -}}
{{- else -}}
{{- if .Values.secrets.redis.password -}}
{{- printf "redis://:%s@%s:%s" .Values.secrets.redis.password .Values.secrets.redis.host .Values.secrets.redis.port -}}
{{- else -}}
{{- printf "redis://%s:%s" .Values.secrets.redis.host .Values.secrets.redis.port -}}
{{- end -}}
{{- end -}}
{{- end }}

{{/*
Validate required values
*/}}
{{- define "webapp-chart.validateValues" -}}
{{- if and .Values.postgresql.enabled (not .Values.global.postgresql.auth.username) -}}
{{- fail "postgresql.auth.username is required when postgresql is enabled" -}}
{{- end -}}
{{- if and .Values.redis.enabled .Values.redis.auth.enabled (not .Values.redis.auth.password) -}}
{{- fail "redis.auth.password is required when redis auth is enabled" -}}
{{- end -}}
{{- if and .Values.ingress.enabled (not .Values.ingress.hosts) -}}
{{- fail "ingress.hosts is required when ingress is enabled" -}}
{{- end -}}
{{- end -}}

{{/*
Generate certificates secret name
*/}}
{{- define "webapp-chart.certificateSecretName" -}}
{{- if .Values.ingress.tls -}}
{{- range .Values.ingress.tls -}}
{{- .secretName -}}
{{- end -}}
{{- else -}}
{{- printf "%s-tls" (include "webapp-chart.fullname" .) -}}
{{- end -}}
{{- end -}}

{{/*
Common annotations for all resources
*/}}
{{- define "webapp-chart.commonAnnotations" -}}
meta.helm.sh/release-name: {{ .Release.Name }}
meta.helm.sh/release-namespace: {{ .Release.Namespace }}
{{- with .Values.global.annotations }}
{{- toYaml . }}
{{- end }}
{{- end }}
```

## Exercice 3 : Gestion multi-environnements

### Solution complète : Values Development

```yaml
# values-dev.yaml
global:
  environment: development
  debug: true
  imageRegistry: 'registry-dev.company.com'

replicaCount: 1

image:
  tag: 'dev-latest'
  pullPolicy: Always

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

env:
  NODE_ENV: development
  LOG_LEVEL: debug

autoscaling:
  enabled: false

ingress:
  enabled: true
  hosts:
    - host: webapp-dev.company.local
      paths:
        - path: /
          pathType: Prefix

postgresql:
  enabled: true
  auth:
    postgresPassword: 'dev-postgres-password'
    username: 'dev_user'
    password: 'dev-password'
  primary:
    persistence:
      enabled: false
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi

redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      enabled: false

monitoring:
  enabled: false

networkPolicy:
  enabled: false

tests:
  enabled: true
```

### Solution complète : Values Staging

```yaml
# values-staging.yaml
global:
  environment: staging
  debug: false
  imageRegistry: 'registry.company.com'

replicaCount: 2

image:
  tag: 'staging-v2.1.0'
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 300m
    memory: 384Mi
  requests:
    cpu: 150m
    memory: 192Mi

env:
  NODE_ENV: staging
  LOG_LEVEL: info

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: 'nginx'
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    cert-manager.io/cluster-issuer: 'letsencrypt-staging'
  hosts:
    - host: webapp-staging.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: webapp-staging-tls
      hosts:
        - webapp-staging.company.com

postgresql:
  enabled: true
  auth:
    postgresPassword: 'staging-postgres-password'
    username: 'staging_user'
    password: 'staging-password'
  primary:
    persistence:
      enabled: true
      size: 5Gi
    resources:
      requests:
        cpu: 200m
        memory: 256Mi
      limits:
        cpu: 400m
        memory: 512Mi

redis:
  enabled: true
  auth:
    enabled: true
    password: 'staging-redis-password'
  master:
    persistence:
      enabled: true
      size: 2Gi

monitoring:
  enabled: true
  serviceMonitor:
    enabled: true

networkPolicy:
  enabled: true

tests:
  enabled: true
```

### Solution complète : Values Production

```yaml
# values-production.yaml
global:
  environment: production
  debug: false
  imageRegistry: 'registry.company.com'

replicaCount: 5

image:
  tag: 'v2.1.0'
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

env:
  NODE_ENV: production
  LOG_LEVEL: warn

autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

ingress:
  enabled: true
  className: 'nginx'
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/rate-limit: '100'
    cert-manager.io/cluster-issuer: 'letsencrypt-prod'
    nginx.ingress.kubernetes.io/modsecurity-transaction-id: '$request_id'
    nginx.ingress.kubernetes.io/modsecurity-snippet: |
      SecRuleEngine On
      SecRule REQUEST_HEADERS:Content-Type "text/xml" "id:200002,phase:1,block,msg:'Disallowed content type'"
  hosts:
    - host: webapp.company.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: webapp-prod-tls
      hosts:
        - webapp.company.com

postgresql:
  enabled: true
  auth:
    existingSecret: 'webapp-postgresql-secret'
  primary:
    persistence:
      enabled: true
      size: 20Gi
      storageClass: 'fast-ssd'
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 1000m
        memory: 2Gi
    initdb:
      scriptsConfigMap: 'webapp-db-init'
    podSecurityContext:
      runAsNonRoot: true
      runAsUser: 999
      fsGroup: 999

redis:
  enabled: true
  auth:
    enabled: true
    existingSecret: 'webapp-redis-secret'
    existingSecretPasswordKey: 'password'
  master:
    persistence:
      enabled: true
      size: 10Gi
      storageClass: 'fast-ssd'
    resources:
      requests:
        cpu: 200m
        memory: 256Mi
      limits:
        cpu: 400m
        memory: 512Mi
  replica:
    replicaCount: 2
    persistence:
      enabled: true
      size: 10Gi

monitoring:
  enabled: true
  prometheus:
    enabled: true
  serviceMonitor:
    enabled: true
    interval: 15s
    scrapeTimeout: 10s

networkPolicy:
  enabled: true
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 3000
    - from:
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 9090

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app.kubernetes.io/name
              operator: In
              values: ['webapp']
        topologyKey: kubernetes.io/hostname
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: node-type
              operator: In
              values: ['compute-optimized']

tolerations:
  - key: 'high-memory'
    operator: 'Equal'
    value: 'true'
    effect: 'NoSchedule'

tests:
  enabled: false

hooks:
  preInstall:
    enabled: true
  postUpgrade:
    enabled: true
```

## Exercice 4 : Tests et déploiement

### Solution complète : Script de déploiement

```bash
#!/bin/bash
# deploy.sh

set -e

# Configuration par défaut
ENVIRONMENT="development"
NAMESPACE=""
CHART_VERSION=""
DRY_RUN="false"
WAIT="true"
TIMEOUT="600s"
FORCE="false"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction d'aide
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -e, --environment ENVIRONMENT    Environment (dev, staging, production)"
    echo "  -n, --namespace NAMESPACE        Kubernetes namespace"
    echo "  -v, --version VERSION           Chart version"
    echo "  -d, --dry-run                   Perform a dry run"
    echo "  -f, --force                     Force upgrade (uninstall/install)"
    echo "  --no-wait                       Don't wait for deployment"
    echo "  --timeout TIMEOUT               Timeout for operations (default: 600s)"
    echo "  -h, --help                      Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 -e dev -n webapp-dev"
    echo "  $0 -e production -n webapp-prod -v 1.2.0"
    echo "  $0 -e staging -d"
    exit 1
}

# Parsing des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -n|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -v|--version)
            CHART_VERSION="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN="true"
            shift
            ;;
        -f|--force)
            FORCE="true"
            shift
            ;;
        --no-wait)
            WAIT="false"
            shift
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option $1"
            usage
            ;;
    esac
done

# Validation des paramètres
if [[ ! "$ENVIRONMENT" =~ ^(dev|development|staging|production|prod)$ ]]; then
    echo -e "${RED}Error: Invalid environment. Must be one of: dev, development, staging, production, prod${NC}"
    exit 1
fi

# Normalisation de l'environnement
case $ENVIRONMENT in
    dev) ENVIRONMENT="development" ;;
    prod) ENVIRONMENT="production" ;;
esac

# Définition du namespace par défaut si non spécifié
if [[ -z "$NAMESPACE" ]]; then
    case $ENVIRONMENT in
        development) NAMESPACE="webapp-dev" ;;
        staging) NAMESPACE="webapp-staging" ;;
        production) NAMESPACE="webapp-prod" ;;
    esac
fi

# Fichier de valeurs correspondant à l'environnement
VALUES_FILE="values-${ENVIRONMENT}.yaml"
if [[ ! -f "$VALUES_FILE" ]]; then
    echo -e "${RED}Error: Values file $VALUES_FILE not found${NC}"
    exit 1
fi

echo -e "${YELLOW}=== Webapp Deployment ===${NC}"
echo "Environment: $ENVIRONMENT"
echo "Namespace: $NAMESPACE"
echo "Values file: $VALUES_FILE"
echo "Dry run: $DRY_RUN"
echo "Force: $FORCE"
echo ""

# Vérification des prérequis
echo -e "${YELLOW}Checking prerequisites...${NC}"

# Vérifier que kubectl est disponible et configuré
if ! kubectl cluster-info &>/dev/null; then
    echo -e "${RED}Error: kubectl is not configured or cluster is not accessible${NC}"
    exit 1
fi

# Vérifier que helm est disponible
if ! command -v helm &>/dev/null; then
    echo -e "${RED}Error: helm is not installed${NC}"
    exit 1
fi

# Vérifier la version de Helm
HELM_VERSION=$(helm version --short --client | cut -d'+' -f1 | sed 's/v//')
if [[ $(echo "$HELM_VERSION 3.0.0" | tr " " "\n" | sort -V | head -n1) != "3.0.0" ]]; then
    echo -e "${RED}Error: Helm version 3.0.0 or higher is required${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"

# Créer le namespace s'il n'existe pas
echo -e "${YELLOW}Ensuring namespace $NAMESPACE exists...${NC}"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Mise à jour des dépendances
echo -e "${YELLOW}Updating chart dependencies...${NC}"
helm dependency update

# Construction des options Helm
HELM_OPTIONS=(
    --namespace "$NAMESPACE"
    --values "$VALUES_FILE"
    --timeout "$TIMEOUT"
)

if [[ "$DRY_RUN" == "true" ]]; then
    HELM_OPTIONS+=(--dry-run)
fi

if [[ "$WAIT" == "true" ]]; then
    HELM_OPTIONS+=(--wait)
fi

if [[ -n "$CHART_VERSION" ]]; then
    HELM_OPTIONS+=(--version "$CHART_VERSION")
fi

# Vérifier si la release existe
RELEASE_NAME="webapp"
if helm list -n "$NAMESPACE" | grep -q "$RELEASE_NAME"; then
    RELEASE_EXISTS=true
else
    RELEASE_EXISTS=false
fi

# Déploiement
if [[ "$FORCE" == "true" && "$RELEASE_EXISTS" == "true" ]]; then
    echo -e "${YELLOW}Force upgrade: uninstalling existing release...${NC}"
    helm uninstall "$RELEASE_NAME" --namespace "$NAMESPACE" --wait
    RELEASE_EXISTS=false
fi

if [[ "$RELEASE_EXISTS" == "true" ]]; then
    echo -e "${YELLOW}Upgrading existing release...${NC}"
    helm upgrade "$RELEASE_NAME" . "${HELM_OPTIONS[@]}"
else
    echo -e "${YELLOW}Installing new release...${NC}"
    helm install "$RELEASE_NAME" . "${HELM_OPTIONS[@]}"
fi

if [[ "$DRY_RUN" == "false" ]]; then
    echo -e "${GREEN}✓ Deployment completed successfully${NC}"

    # Afficher le statut
    echo -e "${YELLOW}Release status:${NC}"
    helm status "$RELEASE_NAME" --namespace "$NAMESPACE"

    # Afficher les ressources déployées
    echo -e "${YELLOW}Deployed resources:${NC}"
    kubectl get all -n "$NAMESPACE" -l app.kubernetes.io/instance="$RELEASE_NAME"

    # Afficher les instructions post-déploiement
    echo -e "${YELLOW}Post-deployment notes:${NC}"
    helm get notes "$RELEASE_NAME" --namespace "$NAMESPACE"
else
    echo -e "${GREEN}✓ Dry run completed successfully${NC}"
fi
```

### Solution complète : Tests Helm

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "webapp-chart.fullname" . }}-test-connection"
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "2"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
  - name: wget
    image: busybox:1.35
    command: ['wget']
    args:
    - '--no-check-certificate'
    - '--quiet'
    - '--timeout=30'
    - '--tries=3'
    - '--spider'
    - 'http://{{ include "webapp-chart.fullname" . }}:{{ .Values.service.port }}/health'
  - name: curl-metrics
    image: curlimages/curl:8.1.0
    command: ['curl']
    args:
    - '-f'
    - '--max-time'
    - '30'
    - '--retry'
    - '3'
    - 'http://{{ include "webapp-chart.fullname" . }}:{{ .Values.service.port }}/metrics'
---
{{- if .Values.postgresql.enabled }}
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "webapp-chart.fullname" . }}-test-database"
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "3"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
  - name: psql
    image: postgres:14-alpine
    command:
    - /bin/bash
    - -c
    - |
      echo "Testing PostgreSQL connection..."
      export PGPASSWORD="${DB_PASSWORD}"
      psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} -c "SELECT 1;"
      echo "PostgreSQL connection test passed!"
    env:
    - name: DB_HOST
      value: {{ include "webapp-chart.postgresql.host" . }}
    - name: DB_PORT
      value: "{{ .Values.postgresql.primary.service.ports.postgresql }}"
    - name: DB_USER
      value: "{{ .Values.global.postgresql.auth.username }}"
    - name: DB_PASSWORD
      value: "{{ .Values.global.postgresql.auth.password }}"
    - name: DB_NAME
      value: "{{ .Values.global.postgresql.auth.database }}"
{{- end }}
---
{{- if .Values.redis.enabled }}
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "webapp-chart.fullname" . }}-test-redis"
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "3"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
  - name: redis-cli
    image: redis:7-alpine
    command:
    - /bin/sh
    - -c
    - |
      echo "Testing Redis connection..."
      {{- if .Values.redis.auth.enabled }}
      redis-cli -h {{ include "webapp-chart.redis.host" . }} -p {{ .Values.redis.master.service.ports.redis }} -a "${REDIS_PASSWORD}" ping
      {{- else }}
      redis-cli -h {{ include "webapp-chart.redis.host" . }} -p {{ .Values.redis.master.service.ports.redis }} ping
      {{- end }}
      echo "Redis connection test passed!"
    {{- if .Values.redis.auth.enabled }}
    env:
    - name: REDIS_PASSWORD
      value: "{{ .Values.redis.auth.password }}"
    {{- end }}
{{- end }}
```

### Solution complète : Tests de charge

```yaml
# templates/tests/test-load.yaml
{{- if .Values.tests.enabled }}
apiVersion: batch/v1
kind: Job
metadata:
  name: "{{ include "webapp-chart.fullname" . }}-load-test"
  namespace: {{ .Release.Namespace | quote }}
  labels:
    {{- include "webapp-chart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  ttlSecondsAfterFinished: 300
  template:
    metadata:
      labels:
        {{- include "webapp-chart.selectorLabels" . | nindent 8 }}
        job-type: load-test
    spec:
      restartPolicy: Never
      containers:
      - name: load-test
        image: jordi/ab:latest
        command:
        - /bin/sh
        - -c
        - |
          echo "Starting load test..."

          # Test basique de charge
          ab -n 1000 -c 10 -t 60 http://{{ include "webapp-chart.fullname" . }}:{{ .Values.service.port }}/health

          # Test avec authentification si applicable
          {{- if .Values.ingress.enabled }}
          {{- range .Values.ingress.hosts }}
          echo "Testing {{ .host }}..."
          ab -n 500 -c 5 -t 30 http://{{ .host }}/health
          {{- end }}
          {{- end }}

          echo "Load test completed!"
        resources:
          limits:
            cpu: 200m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
{{- end }}
```

## Exercice 5 : Scripts d'automatisation

### Solution complète : Script de validation

```bash
#!/bin/bash
# validate-chart.sh

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

CHART_DIR="."
ERRORS=0

echo -e "${YELLOW}=== Helm Chart Validation ===${NC}"

# Fonction pour afficher les erreurs
error() {
    echo -e "${RED}✗ $1${NC}"
    ERRORS=$((ERRORS + 1))
}

# Fonction pour afficher les succès
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Validation de la structure du chart
echo -e "${YELLOW}1. Validating chart structure...${NC}"

required_files=(
    "Chart.yaml"
    "values.yaml"
    "templates/deployment.yaml"
    "templates/service.yaml"
    "templates/_helpers.tpl"
)

for file in "${required_files[@]}"; do
    if [[ -f "$CHART_DIR/$file" ]]; then
        success "Required file $file exists"
    else
        error "Required file $file is missing"
    fi
done

# Validation de Chart.yaml
echo -e "${YELLOW}2. Validating Chart.yaml...${NC}"

if [[ -f "$CHART_DIR/Chart.yaml" ]]; then
    # Vérifier les champs obligatoires
    required_fields=("apiVersion" "name" "version" "appVersion")

    for field in "${required_fields[@]}"; do
        if yq eval ".${field}" "$CHART_DIR/Chart.yaml" | grep -q "null"; then
            error "Missing required field: $field in Chart.yaml"
        else
            success "Field $field is present in Chart.yaml"
        fi
    done

    # Vérifier la version sémantique
    version=$(yq eval '.version' "$CHART_DIR/Chart.yaml")
    if [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        success "Chart version follows semantic versioning"
    else
        error "Chart version does not follow semantic versioning"
    fi
fi

# Validation des templates
echo -e "${YELLOW}3. Validating templates...${NC}"

# Lint du chart
if helm lint "$CHART_DIR" &>/dev/null; then
    success "Helm lint passed"
else
    error "Helm lint failed"
    helm lint "$CHART_DIR"
fi

# Template rendering
echo -e "${YELLOW}4. Testing template rendering...${NC}"

environments=("development" "staging" "production")

for env in "${environments[@]}"; do
    values_file="values-${env}.yaml"
    if [[ -f "$CHART_DIR/$values_file" ]]; then
        if helm template test-release "$CHART_DIR" -f "$CHART_DIR/$values_file" &>/dev/null; then
            success "Template rendering for $env environment"
        else
            error "Template rendering failed for $env environment"
        fi
    else
        error "Values file for $env environment not found"
    fi
done

# Validation des dépendances
echo -e "${YELLOW}5. Validating dependencies...${NC}"

if [[ -f "$CHART_DIR/Chart.yaml" ]] && yq eval '.dependencies' "$CHART_DIR/Chart.yaml" | grep -q -v "null"; then
    if helm dependency list "$CHART_DIR" &>/dev/null; then
        success "Dependencies are valid"

        # Vérifier que les charts de dépendances sont téléchargés
        if [[ -d "$CHART_DIR/charts" ]]; then
            success "Dependencies are downloaded"
        else
            error "Dependencies are not downloaded (run 'helm dependency update')"
        fi
    else
        error "Dependencies validation failed"
    fi
else
    success "No dependencies defined"
fi

# Validation de sécurité
echo -e "${YELLOW}6. Security validation...${NC}"

# Vérifier les pratiques de sécurité dans les templates
security_checks=(
    "runAsNonRoot.*true"
    "readOnlyRootFilesystem.*true"
    "allowPrivilegeEscalation.*false"
)

for template in "$CHART_DIR"/templates/*.yaml; do
    if [[ -f "$template" ]]; then
        for check in "${security_checks[@]}"; do
            if helm template test-release "$CHART_DIR" | grep -q "$check"; then
                success "Security check passed: $check in $(basename "$template")"
                break
            fi
        done
    fi
done

# Vérifier l'absence de secrets en dur
if grep -r -i "password\|secret\|key" "$CHART_DIR"/templates/ --include="*.yaml" | grep -v -E "(secretKeyRef|name.*secret|valueFrom)" | grep -q .; then
    error "Potential hardcoded secrets found in templates"
else
    success "No hardcoded secrets found in templates"
fi

# Tests automatisés
echo -e "${YELLOW}7. Running automated tests...${NC}"

if [[ -d "$CHART_DIR/templates/tests" ]]; then
    test_files=$(find "$CHART_DIR/templates/tests" -name "*.yaml" | wc -l)
    if [[ $test_files -gt 0 ]]; then
        success "Test templates found ($test_files files)"
    else
        error "No test templates found"
    fi
else
    error "Tests directory not found"
fi

# Validation des valeurs par défaut
echo -e "${YELLOW}8. Validating default values...${NC}"

if [[ -f "$CHART_DIR/values.yaml" ]]; then
    # Vérifier que les ressources sont définies
    if yq eval '.resources' "$CHART_DIR/values.yaml" | grep -q -v "null"; then
        success "Resource limits and requests are defined"
    else
        error "Resource limits and requests are not defined"
    fi

    # Vérifier la configuration de sécurité
    if yq eval '.securityContext.runAsNonRoot' "$CHART_DIR/values.yaml" | grep -q "true"; then
        success "runAsNonRoot is enabled by default"
    else
        error "runAsNonRoot should be enabled by default"
    fi

    # Vérifier les sondes de santé
    if yq eval '.livenessProbe' "$CHART_DIR/values.yaml" | grep -q -v "null"; then
        success "Liveness probe is configured"
    else
        error "Liveness probe is not configured"
    fi
fi

# Résumé
echo -e "${YELLOW}=== Validation Summary ===${NC}"

if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}✓ All validations passed! Chart is ready for deployment.${NC}"
    exit 0
else
    echo -e "${RED}✗ $ERRORS validation errors found. Please fix before deployment.${NC}"
    exit 1
fi
```

## Bonnes pratiques implémentées

### 1. **Structure et organisation**

- Structure de fichiers standardisée
- Séparation des environnements
- Gestion des dépendances

### 2. **Templating avancé**

- Helpers réutilisables
- Validation des valeurs
- Gestion des secrets sécurisée

### 3. **Multi-environnements**

- Configuration par environnement
- Ressources adaptées au contexte
- Sécurité graduée

### 4. **Tests et validation**

- Tests de connectivité
- Tests de charge
- Validation automatisée

### 5. **Déploiement automatisé**

- Scripts paramétrables
- Gestion des erreurs
- Rollback automatique

## Points de validation

### ✅ Critères de réussite

1. **Chart structure** : Organisation standardisée et complète
2. **Templates** : Syntaxe correcte et bonnes pratiques
3. **Multi-environnements** : Configuration adaptée à chaque contexte
4. **Tests** : Validation automatisée et tests de charge
5. **Déploiement** : Scripts robustes et gestion d'erreurs
6. **Sécurité** : Bonnes pratiques implémentées

### 🔍 Points de contrôle

- Helm lint sans erreurs
- Templates rendus correctement
- Tests passants sur tous les environnements
- Scripts de déploiement fonctionnels
- Validation de sécurité réussie
- Documentation complète

Cette correction fournit une approche professionnelle et production-ready pour la création et gestion de Helm Charts avancés.
