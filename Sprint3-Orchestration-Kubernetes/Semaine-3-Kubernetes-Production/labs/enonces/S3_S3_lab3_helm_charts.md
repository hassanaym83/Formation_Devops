# LAB 3 - Helm Charts création

## Objectifs

- Créer des Helm Charts complexes et réutilisables
- Maîtriser les templates et fonctions Helm
- Gérer les dépendances entre charts
- Implémenter des hooks et tests
- Publier dans un repository Helm

## Prérequis

- Helm 3.x installé
- Cluster Kubernetes fonctionnel
- Connaissance des templates Go
- Git configuré

## Contexte du LAB

Vous devez créer un Helm Chart pour une application de blog WordPress avec :

- WordPress (frontend)
- MySQL (base de données)
- Redis (cache)
- Nginx (reverse proxy)
- Monitoring (Prometheus/Grafana)

## Exercice 1 : Structure et métadonnées du Chart

### Étape 1.1 : Création du Chart

Créez la structure de base du chart `wordpress-stack` :

```bash
helm create wordpress-stack
cd wordpress-stack
```

### Étape 1.2 : Configuration Chart.yaml

Modifiez le fichier `Chart.yaml` :

```yaml
apiVersion: v2
name: wordpress-stack
description: Chart Helm pour stack WordPress complète avec monitoring
type: application
version: 1.0.0
appVersion: '6.3.0'

keywords:
  - wordpress
  - blog
  - cms
  - mysql
  - redis

home: https://github.com/votre-org/wordpress-stack
sources:
  - https://github.com/votre-org/wordpress-stack

maintainers:
  - name: Votre Nom
    email: votre.email@example.com

dependencies:
  - name: mysql
    version: 9.4.6
    repository: https://charts.bitnami.com/bitnami
    condition: mysql.enabled
  - name: redis
    version: 17.3.7
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
  - name: prometheus
    version: 15.16.1
    repository: https://prometheus-community.github.io/helm-charts
    condition: monitoring.prometheus.enabled

annotations:
  category: CMS
  licenses: GPL-2.0
```

### Étape 1.3 : Values.yaml structuré

Créez un fichier `values.yaml` complet :

```yaml
# Global settings
global:
  imageRegistry: ''
  imagePullSecrets: []
  storageClass: ''

# WordPress configuration
wordpress:
  enabled: true
  image:
    registry: docker.io
    repository: wordpress
    tag: '6.3.0-apache'
    pullPolicy: IfNotPresent

  replicaCount: 2

  # WordPress configuration
  wordpressUsername: admin
  wordpressPassword: '' # Généré automatiquement si vide
  wordpressEmail: admin@example.com
  wordpressFirstName: Admin
  wordpressLastName: User
  wordpressBlogName: 'Mon Blog WordPress'

  # Database connection
  externalDatabase:
    host: ''
    port: 3306
    user: wordpress
    password: ''
    database: wordpress

  # Persistent storage
  persistence:
    enabled: true
    storageClass: ''
    accessMode: ReadWriteOnce
    size: 10Gi

  # Resources
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

  # Security context
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000

  # Service configuration
  service:
    type: ClusterIP
    port: 80

  # Ingress
  ingress:
    enabled: true
    className: 'nginx'
    annotations:
      cert-manager.io/cluster-issuer: 'letsencrypt-prod'
      nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    hosts:
      - host: blog.example.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: wordpress-tls
        hosts:
          - blog.example.com

# MySQL configuration (subchart)
mysql:
  enabled: true
  auth:
    rootPassword: '' # Généré automatiquement
    database: wordpress
    username: wordpress
    password: '' # Généré automatiquement

  primary:
    persistence:
      enabled: true
      size: 20Gi
    resources:
      limits:
        cpu: 1000m
        memory: 1Gi
      requests:
        cpu: 500m
        memory: 512Mi

# Redis configuration (subchart)
redis:
  enabled: true
  auth:
    enabled: true
    password: '' # Généré automatiquement

  master:
    persistence:
      enabled: true
      size: 5Gi
    resources:
      limits:
        cpu: 500m
        memory: 256Mi
      requests:
        cpu: 250m
        memory: 128Mi

# Nginx reverse proxy
nginx:
  enabled: true
  image:
    registry: docker.io
    repository: nginx
    tag: '1.21-alpine'

  replicaCount: 2

  config: |
    upstream wordpress {
        server wordpress-stack-wordpress:80;
    }

    server {
        listen 80;
        server_name _;
        
        location / {
            proxy_pass http://wordpress;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

# Monitoring
monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
    adminPassword: '' # Généré automatiquement

# Security
podSecurityPolicy:
  enabled: false

networkPolicy:
  enabled: true

# Autoscaling
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

# Tests
tests:
  enabled: true
```

## Exercice 2 : Templates de base

### Étape 2.1 : Template deployment WordPress

Créez `templates/wordpress-deployment.yaml` :

```yaml
{{- if .Values.wordpress.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-wordpress
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
    app.kubernetes.io/component: wordpress
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.wordpress.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "wordpress-stack.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: wordpress
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/wordpress-configmap.yaml") . | sha256sum }}
      labels:
        {{- include "wordpress-stack.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: wordpress
    spec:
      {{- with .Values.global.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      securityContext:
        {{- toYaml .Values.wordpress.securityContext | nindent 8 }}
      containers:
      - name: wordpress
        image: "{{ .Values.wordpress.image.registry }}/{{ .Values.wordpress.image.repository }}:{{ .Values.wordpress.image.tag }}"
        imagePullPolicy: {{ .Values.wordpress.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 80
          protocol: TCP
        env:
        - name: WORDPRESS_DB_HOST
          value: {{ include "wordpress-stack.databaseHost" . | quote }}
        - name: WORDPRESS_DB_PORT
          value: {{ include "wordpress-stack.databasePort" . | quote }}
        - name: WORDPRESS_DB_NAME
          value: {{ include "wordpress-stack.databaseName" . | quote }}
        - name: WORDPRESS_DB_USER
          value: {{ include "wordpress-stack.databaseUser" . | quote }}
        - name: WORDPRESS_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "wordpress-stack.secretName" . }}
              key: wordpress-password
        {{- if .Values.redis.enabled }}
        - name: WORDPRESS_REDIS_HOST
          value: "{{ include "wordpress-stack.fullname" . }}-redis-master"
        - name: WORDPRESS_REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "wordpress-stack.secretName" . }}
              key: redis-password
        {{- end }}
        livenessProbe:
          httpGet:
            path: /wp-admin/install.php
            port: http
          initialDelaySeconds: 120
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 6
        readinessProbe:
          httpGet:
            path: /wp-login.php
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          successThreshold: 1
          failureThreshold: 3
        resources:
          {{- toYaml .Values.wordpress.resources | nindent 12 }}
        volumeMounts:
        - name: wordpress-data
          mountPath: /var/www/html
      volumes:
      - name: wordpress-data
        {{- if .Values.wordpress.persistence.enabled }}
        persistentVolumeClaim:
          claimName: {{ include "wordpress-stack.fullname" . }}-wordpress
        {{- else }}
        emptyDir: {}
        {{- end }}
{{- end }}
```

### Étape 2.2 : Template helpers

Créez/modifiez `templates/_helpers.tpl` :

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "wordpress-stack.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "wordpress-stack.fullname" -}}
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
{{- define "wordpress-stack.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "wordpress-stack.labels" -}}
helm.sh/chart: {{ include "wordpress-stack.chart" . }}
{{ include "wordpress-stack.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "wordpress-stack.selectorLabels" -}}
app.kubernetes.io/name: {{ include "wordpress-stack.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Database host
*/}}
{{- define "wordpress-stack.databaseHost" -}}
{{- if .Values.mysql.enabled }}
{{- printf "%s-mysql" (include "wordpress-stack.fullname" .) }}
{{- else }}
{{- .Values.wordpress.externalDatabase.host }}
{{- end }}
{{- end }}

{{/*
Database port
*/}}
{{- define "wordpress-stack.databasePort" -}}
{{- if .Values.mysql.enabled }}
{{- print "3306" }}
{{- else }}
{{- .Values.wordpress.externalDatabase.port }}
{{- end }}
{{- end }}

{{/*
Database name
*/}}
{{- define "wordpress-stack.databaseName" -}}
{{- if .Values.mysql.enabled }}
{{- .Values.mysql.auth.database }}
{{- else }}
{{- .Values.wordpress.externalDatabase.database }}
{{- end }}
{{- end }}

{{/*
Database user
*/}}
{{- define "wordpress-stack.databaseUser" -}}
{{- if .Values.mysql.enabled }}
{{- .Values.mysql.auth.username }}
{{- else }}
{{- .Values.wordpress.externalDatabase.user }}
{{- end }}
{{- end }}

{{/*
Secret name
*/}}
{{- define "wordpress-stack.secretName" -}}
{{- printf "%s-secrets" (include "wordpress-stack.fullname" .) }}
{{- end }}

{{/*
Generate passwords
*/}}
{{- define "wordpress-stack.passwords" -}}
{{- $secret := lookup "v1" "Secret" .Release.Namespace (include "wordpress-stack.secretName" .) }}
{{- if $secret }}
wordpress-password: {{ index $secret.data "wordpress-password" }}
mysql-password: {{ index $secret.data "mysql-password" }}
redis-password: {{ index $secret.data "redis-password" }}
{{- else }}
wordpress-password: {{ randAlphaNum 16 | b64enc }}
mysql-password: {{ randAlphaNum 16 | b64enc }}
redis-password: {{ randAlphaNum 16 | b64enc }}
{{- end }}
{{- end }}
```

## Exercice 3 : Templates avancés

### Étape 3.1 : ConfigMap avec logique conditionnelle

Créez `templates/wordpress-configmap.yaml` :

```yaml
{{- if .Values.wordpress.enabled }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-config
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
data:
  # Configuration WordPress
  wordpress-config.php: |
    <?php
    // Configuration WordPress générée par Helm

    // Database settings
    define('DB_NAME', '{{ include "wordpress-stack.databaseName" . }}');
    define('DB_USER', '{{ include "wordpress-stack.databaseUser" . }}');
    define('DB_HOST', '{{ include "wordpress-stack.databaseHost" . }}:{{ include "wordpress-stack.databasePort" . }}');

    // Security keys (you should change these)
    {{- $secret := lookup "v1" "Secret" .Release.Namespace (printf "%s-auth-keys" (include "wordpress-stack.fullname" .)) }}
    {{- if $secret }}
    define('AUTH_KEY',         '{{ index $secret.data "auth-key" | b64dec }}');
    define('SECURE_AUTH_KEY',  '{{ index $secret.data "secure-auth-key" | b64dec }}');
    define('LOGGED_IN_KEY',    '{{ index $secret.data "logged-in-key" | b64dec }}');
    define('NONCE_KEY',        '{{ index $secret.data "nonce-key" | b64dec }}');
    {{- else }}
    define('AUTH_KEY',         '{{ randAlphaNum 64 }}');
    define('SECURE_AUTH_KEY',  '{{ randAlphaNum 64 }}');
    define('LOGGED_IN_KEY',    '{{ randAlphaNum 64 }}');
    define('NONCE_KEY',        '{{ randAlphaNum 64 }}');
    {{- end }}

    {{- if .Values.redis.enabled }}
    // Redis configuration
    define('WP_REDIS_HOST', '{{ include "wordpress-stack.fullname" . }}-redis-master');
    define('WP_REDIS_PORT', 6379);
    define('WP_CACHE', true);
    {{- end }}

    // WordPress debugging
    {{- if eq .Values.global.environment "development" }}
    define('WP_DEBUG', true);
    define('WP_DEBUG_LOG', true);
    {{- else }}
    define('WP_DEBUG', false);
    {{- end }}

    // WordPress URLs
    define('WP_HOME','https://{{ (index .Values.wordpress.ingress.hosts 0).host }}');
    define('WP_SITEURL','https://{{ (index .Values.wordpress.ingress.hosts 0).host }}');

    // Security configurations
    define('DISALLOW_FILE_EDIT', true);
    define('AUTOMATIC_UPDATER_DISABLED', true);

    $table_prefix = 'wp_';

    if ( !defined('ABSPATH') )
        define('ABSPATH', dirname(__FILE__) . '/');

    require_once(ABSPATH . 'wp-settings.php');
{{- end }}
```

### Étape 3.2 : Secret avec génération automatique

Créez `templates/secrets.yaml` :

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "wordpress-stack.secretName" . }}
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-1"
type: Opaque
data:
  {{- include "wordpress-stack.passwords" . | nindent 2 }}
---
{{- if .Values.wordpress.enabled }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-auth-keys
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "-1"
type: Opaque
data:
  auth-key: {{ randAlphaNum 64 | b64enc }}
  secure-auth-key: {{ randAlphaNum 64 | b64enc }}
  logged-in-key: {{ randAlphaNum 64 | b64enc }}
  nonce-key: {{ randAlphaNum 64 | b64enc }}
{{- end }}
```

## Exercice 4 : Hooks et Jobs

### Étape 4.1 : Hook de pre-install

Créez `templates/hooks/pre-install-job.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-pre-install
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    metadata:
      labels:
        {{- include "wordpress-stack.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: pre-install
    spec:
      restartPolicy: Never
      containers:
      - name: pre-install
        image: busybox:1.35
        command:
        - /bin/sh
        - -c
        - |
          echo "Starting pre-install checks..."

          # Vérifier la connectivité réseau
          {{- if .Values.mysql.enabled }}
          echo "Checking MySQL connectivity..."
          nc -z {{ include "wordpress-stack.fullname" . }}-mysql 3306 || exit 1
          {{- end }}

          {{- if .Values.redis.enabled }}
          echo "Checking Redis connectivity..."
          nc -z {{ include "wordpress-stack.fullname" . }}-redis-master 6379 || exit 1
          {{- end }}

          echo "Pre-install checks completed successfully!"
```

### Étape 4.2 : Hook de post-install

Créez `templates/hooks/post-install-job.yaml` :

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-post-install
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    metadata:
      labels:
        {{- include "wordpress-stack.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: post-install
    spec:
      restartPolicy: Never
      containers:
      - name: post-install
        image: wordpress:cli-2.7
        command:
        - /bin/sh
        - -c
        - |
          echo "Configuring WordPress..."

          # Attendre que WordPress soit disponible
          until wp core is-installed --allow-root --path=/var/www/html; do
            echo "Waiting for WordPress to be available..."
            sleep 10
          done

          # Configuration initiale WordPress
          wp core install \
            --url="https://{{ (index .Values.wordpress.ingress.hosts 0).host }}" \
            --title="{{ .Values.wordpress.wordpressBlogName }}" \
            --admin_user="{{ .Values.wordpress.wordpressUsername }}" \
            --admin_password="${WORDPRESS_PASSWORD}" \
            --admin_email="{{ .Values.wordpress.wordpressEmail }}" \
            --allow-root \
            --path=/var/www/html

          {{- if .Values.redis.enabled }}
          # Installer et activer le plugin Redis
          wp plugin install redis-cache --activate --allow-root --path=/var/www/html
          wp redis enable --allow-root --path=/var/www/html
          {{- end }}

          echo "WordPress configuration completed!"
        env:
        - name: WORDPRESS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {{ include "wordpress-stack.secretName" . }}
              key: wordpress-password
        volumeMounts:
        - name: wordpress-data
          mountPath: /var/www/html
      volumes:
      - name: wordpress-data
        persistentVolumeClaim:
          claimName: {{ include "wordpress-stack.fullname" . }}-wordpress
```

## Exercice 5 : Tests Helm

### Étape 5.1 : Test de connectivité

Créez `templates/tests/connectivity-test.yaml` :

```yaml
{{- if .Values.tests.enabled }}
apiVersion: v1
kind: Pod
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-test-connectivity
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "1"
spec:
  restartPolicy: Never
  containers:
  - name: connectivity-test
    image: busybox:1.35
    command:
    - /bin/sh
    - -c
    - |
      echo "Testing WordPress connectivity..."

      # Test WordPress service
      nc -z {{ include "wordpress-stack.fullname" . }}-wordpress 80
      if [ $? -eq 0 ]; then
        echo "✓ WordPress service is accessible"
      else
        echo "✗ WordPress service is not accessible"
        exit 1
      fi

      {{- if .Values.mysql.enabled }}
      # Test MySQL service
      nc -z {{ include "wordpress-stack.fullname" . }}-mysql 3306
      if [ $? -eq 0 ]; then
        echo "✓ MySQL service is accessible"
      else
        echo "✗ MySQL service is not accessible"
        exit 1
      fi
      {{- end }}

      {{- if .Values.redis.enabled }}
      # Test Redis service
      nc -z {{ include "wordpress-stack.fullname" . }}-redis-master 6379
      if [ $? -eq 0 ]; then
        echo "✓ Redis service is accessible"
      else
        echo "✗ Redis service is not accessible"
        exit 1
      fi
      {{- end }}

      echo "All connectivity tests passed!"
{{- end }}
```

### Étape 5.2 : Test fonctionnel WordPress

Créez `templates/tests/wordpress-test.yaml` :

```yaml
{{- if .Values.tests.enabled }}
apiVersion: v1
kind: Pod
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-test-wordpress
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-weight": "2"
spec:
  restartPolicy: Never
  containers:
  - name: wordpress-test
    image: curlimages/curl:7.85.0
    command:
    - /bin/sh
    - -c
    - |
      echo "Testing WordPress functionality..."

      # Test page d'accueil
      RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        http://{{ include "wordpress-stack.fullname" . }}-wordpress/)

      if [ "$RESPONSE" = "200" ]; then
        echo "✓ WordPress homepage is accessible (HTTP 200)"
      else
        echo "✗ WordPress homepage returned HTTP $RESPONSE"
        exit 1
      fi

      # Test page de login
      RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        http://{{ include "wordpress-stack.fullname" . }}-wordpress/wp-login.php)

      if [ "$RESPONSE" = "200" ]; then
        echo "✓ WordPress login page is accessible (HTTP 200)"
      else
        echo "✗ WordPress login page returned HTTP $RESPONSE"
        exit 1
      fi

      # Test contenu de la page
      CONTENT=$(curl -s http://{{ include "wordpress-stack.fullname" . }}-wordpress/ | grep -i wordpress)
      if [ -n "$CONTENT" ]; then
        echo "✓ WordPress content detected on homepage"
      else
        echo "✗ No WordPress content found on homepage"
        exit 1
      fi

      echo "All WordPress tests passed!"
{{- end }}
```

## Exercice 6 : Gestion des dépendances

### Étape 6.1 : Mise à jour des dépendances

```bash
# Mettre à jour les dépendances
helm dependency update

# Vérifier les dépendances
helm dependency list
```

### Étape 6.2 : Configuration des subcharts

Créez des fichiers de configuration pour personnaliser les subcharts :

`charts/mysql/values-override.yaml` :

```yaml
architecture: replication
auth:
  replicationUser: replicator
  replicationPassword: replicapass123

primary:
  configuration: |-
    [mysqld]
    max_connections=200
    innodb_buffer_pool_size=1G
    innodb_log_file_size=256M
    slow_query_log=1
    long_query_time=2

secondary:
  replicaCount: 1
```

## Exercice 7 : Publication et versioning

### Étape 7.1 : Package du chart

```bash
# Créer le package
helm package .

# Vérifier le chart
helm lint .

# Tester l'installation (dry-run)
helm install wordpress-test . --dry-run --debug
```

### Étape 7.2 : Repository Helm

Créez un repository Helm local :

```bash
# Créer le repository
mkdir helm-repo
helm repo index helm-repo --url http://localhost:8080

# Serveur local
cd helm-repo
python3 -m http.server 8080
```

### Étape 7.3 : CI/CD pour le chart

Créez `.github/workflows/helm-release.yaml` :

```yaml
name: Release Helm Chart

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name "$GITHUB_ACTOR"
          git config user.email "$GITHUB_ACTOR@users.noreply.github.com"

      - name: Install Helm
        uses: azure/setup-helm@v3
        with:
          version: v3.10.0

      - name: Run chart-releaser
        uses: helm/chart-releaser-action@v1.4.1
        env:
          CR_TOKEN: '${{ secrets.GITHUB_TOKEN }}'
```

## Exercice 8 : Déploiement multi-environnements

### Étape 8.1 : Values pour différents environnements

Créez `values-dev.yaml` :

```yaml
global:
  environment: development

wordpress:
  replicaCount: 1
  ingress:
    hosts:
      - host: blog-dev.example.com
        paths:
          - path: /
            pathType: Prefix

mysql:
  primary:
    persistence:
      size: 5Gi
  auth:
    database: wordpress_dev

monitoring:
  enabled: false
```

Créez `values-prod.yaml` :

```yaml
global:
  environment: production

wordpress:
  replicaCount: 3
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

mysql:
  primary:
    persistence:
      size: 50Gi
  secondary:
    replicaCount: 1

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10

monitoring:
  enabled: true
```

### Étape 8.2 : Script de déploiement

Créez `deploy.sh` :

```bash
#!/bin/bash

ENV=${1:-dev}
NAMESPACE="wordpress-$ENV"

echo "Deploying WordPress stack to $ENV environment..."

# Créer le namespace s'il n'existe pas
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Déployer avec les bonnes values
helm upgrade --install wordpress-$ENV . \
  --namespace $NAMESPACE \
  --values values-$ENV.yaml \
  --wait \
  --timeout 10m

# Lancer les tests
helm test wordpress-$ENV --namespace $NAMESPACE

echo "Deployment completed for $ENV environment!"
```

## Exercice 9 : Monitoring et observabilité

### Étape 9.1 : ServiceMonitor pour Prometheus

Créez `templates/monitoring/servicemonitor.yaml` :

```yaml
{{- if and .Values.monitoring.enabled .Values.monitoring.prometheus.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "wordpress-stack.fullname" . }}
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "wordpress-stack.selectorLabels" . | nindent 6 }}
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
{{- end }}
```

### Étape 9.2 : Dashboard Grafana

Créez `templates/monitoring/grafana-dashboard.yaml` :

```yaml
{{- if and .Values.monitoring.enabled .Values.monitoring.grafana.enabled }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "wordpress-stack.fullname" . }}-dashboard
  labels:
    {{- include "wordpress-stack.labels" . | nindent 4 }}
    grafana_dashboard: "1"
data:
  wordpress-dashboard.json: |-
    {
      "dashboard": {
        "title": "WordPress Stack Dashboard",
        "panels": [
          {
            "title": "WordPress Response Time",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service=\"{{ include "wordpress-stack.fullname" . }}-wordpress\"}[5m])) by (le))"
              }
            ]
          }
        ]
      }
    }
{{- end }}
```

## Questions de validation

1. Comment gérer les secrets sensibles dans un Helm Chart ?
2. Quelle est la différence entre les hooks pre-install et post-install ?
3. Comment déboguer un template Helm qui ne fonctionne pas ?
4. Comment gérer les montées de version de chart avec des breaking changes ?

## Livrables attendus

1. `Chart.yaml` - Métadonnées complètes du chart
2. `values.yaml` - Configuration par défaut complète
3. `templates/` - Tous les templates Kubernetes
4. `templates/_helpers.tpl` - Fonctions helpers personnalisées
5. `templates/hooks/` - Hooks pre/post install
6. `templates/tests/` - Tests Helm
7. `values-{env}.yaml` - Configurations par environnement
8. `deploy.sh` - Script de déploiement
9. `README.md` - Documentation du chart
10. Package `.tgz` - Chart packageé

## Critères d'évaluation

- **Complétude** : Tous les composants de l'architecture sont présents
- **Réutilisabilité** : Chart configurable pour différents environnements
- **Sécurité** : Gestion sécurisée des secrets et configurations
- **Qualité** : Templates bien structurés et helpers réutilisables
- **Tests** : Tests fonctionnels et de connectivité
- **Documentation** : README complet avec exemples d'utilisation

## Ressources utiles

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Go Templates](https://pkg.go.dev/text/template)
- [Helm Functions](https://helm.sh/docs/chart_template_guide/function_list/)

---

**Durée estimée : 5-6 heures**  
**Difficulté : ⭐⭐⭐⭐⭐**
