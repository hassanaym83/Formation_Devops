# LAB 4 - CORRECTIONS : Intégration Docker dans GitLab CI/CD

## Solution complète

### 1. Dockerfile multi-stage optimisé

```dockerfile
# Dockerfile pour application React avec build multi-stage optimisé
# Stage 1: Build de l'application Node.js
FROM node:18-alpine AS builder

# Métadonnées pour traçabilité
LABEL maintainer="DevOps Team <devops@example.com>"
LABEL description="Demo React App for GitLab CI/CD Training"
LABEL version="1.0.0"
LABEL build-stage="builder"

# Arguments de build
ARG NODE_ENV=production
ARG REACT_APP_VERSION=1.0.0
ARG REACT_APP_BUILD=unknown
ARG REACT_APP_COMMIT_SHA=unknown

# Variables d'environnement de build
ENV NODE_ENV=$NODE_ENV
ENV CI=true
ENV GENERATE_SOURCEMAP=false

# Optimisation : installation de dumb-init pour gestion signaux
RUN apk add --no-cache dumb-init

# Création d'un utilisateur non-root pour sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S reactuser -u 1001 -G nodejs

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances en premier (optimisation cache Docker)
COPY package*.json ./

# Installation des dépendances avec optimisations
RUN npm ci --only=production --no-audit --prefer-offline && \
    npm cache clean --force

# Copie du code source (après npm install pour optimiser le cache)
COPY . .

# Changement de propriétaire des fichiers
RUN chown -R reactuser:nodejs /app

# Passage à l'utilisateur non-root
USER reactuser

# Build de l'application avec variables d'environnement
RUN echo "Building with REACT_APP_VERSION=$REACT_APP_VERSION" && \
    echo "REACT_APP_BUILD=$REACT_APP_BUILD" && \
    echo "REACT_APP_COMMIT_SHA=$REACT_APP_COMMIT_SHA" && \
    npm run build

# Vérification du build
RUN ls -la build/ && \
    echo "Build size: $(du -sh build/)"

# Stage 2: Image de production avec Nginx optimisé
FROM nginx:1.25-alpine AS production

# Métadonnées pour la production
LABEL maintainer="DevOps Team <devops@example.com>"
LABEL description="Demo React App - Production Image"
LABEL version="1.0.0"
LABEL build-stage="production"

# Installation d'outils nécessaires
RUN apk add --no-cache \
    gettext \
    curl \
    dumb-init \
    && rm -rf /var/cache/apk/*

# Variables d'environnement par défaut
ENV APP_NAME="demo-react-app"
ENV APP_VERSION="1.0.0"
ENV NGINX_WORKER_PROCESSES="auto"
ENV NGINX_WORKER_CONNECTIONS="1024"

# Copie des fichiers build depuis le stage builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copie des fichiers de configuration
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Configuration des permissions pour le script d'entrée
RUN chmod +x /docker-entrypoint.sh

# Création d'un utilisateur nginx non-root
RUN addgroup -g 1001 -S nginx && \
    adduser -S nginx -u 1001 -G nginx

# Configuration des répertoires et permissions
RUN mkdir -p /var/cache/nginx /var/log/nginx /etc/nginx/conf.d /var/run/nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx && \
    chown -R nginx:nginx /var/run/nginx && \
    chmod -R 755 /usr/share/nginx/html

# Création du fichier PID avec bonnes permissions
RUN touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Exposition du port (non-root port)
EXPOSE 8080

# Healthcheck avancé
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Passage à l'utilisateur non-root
USER nginx

# Point d'entrée avec dumb-init pour gestion des signaux
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Configuration Nginx optimisée

**Fichier `nginx.conf.template`** :

```nginx
# Configuration Nginx optimisée pour React SPA
user nginx;
worker_processes ${NGINX_WORKER_PROCESSES};
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections ${NGINX_WORKER_CONNECTIONS};
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Format de log personnalisé avec métriques
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    # Configuration des logs
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Optimisations de performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    types_hash_max_size 2048;
    server_tokens off;

    # Limites de taille
    client_max_body_size 10M;
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;

    # Configuration de compression Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        application/atom+xml
        application/geo+json
        application/javascript
        application/x-javascript
        application/json
        application/ld+json
        application/manifest+json
        application/rdf+xml
        application/rss+xml
        application/xhtml+xml
        application/xml
        font/eot
        font/otf
        font/ttf
        image/svg+xml
        text/css
        text/javascript
        text/plain
        text/xml;

    # Configuration du serveur principal
    server {
        listen 8080;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Headers de sécurité renforcés
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header X-Download-Options "noopen" always;
        add_header X-Permitted-Cross-Domain-Policies "none" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'" always;

        # Configuration pour React Router (SPA)
        location / {
            try_files $uri $uri/ /index.html;

            # Headers de cache pour HTML
            if ($uri ~* \.(html)$) {
                add_header Cache-Control "no-cache, no-store, must-revalidate" always;
                add_header Pragma "no-cache" always;
                add_header Expires "0" always;
            }
        }

        # Cache agressif pour les assets statiques avec hash
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header Vary "Accept-Encoding";

            # Optimisation pour les fichiers avec hash dans le nom
            location ~* \.[0-9a-f]{8,}\.(js|css)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Status endpoint avec informations détaillées
        location /status {
            access_log off;
            return 200 '{"status":"ok","app":"${APP_NAME}","version":"${APP_VERSION}","timestamp":"$time_iso8601"}';
            add_header Content-Type application/json;
        }

        # Métrics endpoint (simulation)
        location /metrics {
            access_log off;
            return 200 'nginx_requests_total 1\nnginx_connections_active 1\n';
            add_header Content-Type text/plain;
        }

        # Désactivation de certains endpoints sensibles
        location ~ /\. {
            deny all;
            access_log off;
            log_not_found off;
        }

        location ~ \.(conf|sql|sh|log)$ {
            deny all;
            access_log off;
            log_not_found off;
        }

        # Page d'erreur personnalisée
        error_page 404 /index.html;
        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }
}
```

### 3. Script d'entrée avancé

**Fichier `docker-entrypoint.sh`** :

```bash
#!/bin/sh
set -e

# Variables par défaut
APP_NAME=${APP_NAME:-"demo-react-app"}
APP_VERSION=${APP_VERSION:-"1.0.0"}
NGINX_WORKER_PROCESSES=${NGINX_WORKER_PROCESSES:-"auto"}
NGINX_WORKER_CONNECTIONS=${NGINX_WORKER_CONNECTIONS:-"1024"}

# Fonction de logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Affichage des informations de démarrage
log "🚀 Starting $APP_NAME v$APP_VERSION"
log "📅 Started at: $(date)"
log "🐳 Container ID: $(hostname)"
log "👤 Running as: $(whoami)"
log "📁 Working directory: $(pwd)"

# Validation des variables d'environnement
log "🔧 Configuration validation"
if [ -z "$APP_NAME" ]; then
    log "❌ APP_NAME not set"
    exit 1
fi

log "✅ APP_NAME: $APP_NAME"
log "✅ APP_VERSION: $APP_VERSION"
log "✅ NGINX_WORKER_PROCESSES: $NGINX_WORKER_PROCESSES"
log "✅ NGINX_WORKER_CONNECTIONS: $NGINX_WORKER_CONNECTIONS"

# Substitution des variables d'environnement dans la configuration Nginx
log "📝 Generating Nginx configuration from template"
envsubst '${APP_NAME} ${APP_VERSION} ${NGINX_WORKER_PROCESSES} ${NGINX_WORKER_CONNECTIONS}' \
    < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Validation de la configuration Nginx
log "🔍 Validating Nginx configuration"
nginx -t

# Affichage des informations finales
log "📊 Container information:"
log "   - CPU cores: $(nproc)"
log "   - Memory: $(free -h | awk '/^Mem:/ {print $2}')"
log "   - Disk usage: $(df -h / | awk 'NR==2 {print $5}')"

# Vérification des fichiers statiques
log "📁 Static files check:"
if [ -d "/usr/share/nginx/html" ]; then
    log "   - Files count: $(find /usr/share/nginx/html -type f | wc -l)"
    log "   - Total size: $(du -sh /usr/share/nginx/html | cut -f1)"
else
    log "❌ Static files directory not found"
    exit 1
fi

# Démarrage de Nginx en arrière-plan pour test
log "🧪 Pre-start health check"
nginx -g "daemon on;"
sleep 2

# Test de santé
if curl -f http://localhost:8080/health > /dev/null 2>&1; then
    log "✅ Health check passed"
else
    log "❌ Health check failed"
    exit 1
fi

# Arrêt de Nginx de test
nginx -s quit
sleep 1

log "🎯 All checks passed, starting main process"

# Exécution de la commande principale
exec "$@"
```

### 4. Pipeline GitLab CI/CD optimisé

```yaml
# Pipeline GitLab CI/CD avec intégration Docker complète
image: docker:24.0.5

# Services Docker-in-Docker avec configuration TLS
services:
  - name: docker:24.0.5-dind
    command: ["--tls=false"]

# Variables globales optimisées
variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_TLS_CERTDIR: ""
  DOCKER_DRIVER: overlay2
  BUILDKIT_PROGRESS: plain
  # Variables d'image
  IMAGE_NAME: "$CI_REGISTRY_IMAGE/demo-react-app"
  IMAGE_TAG: "$CI_COMMIT_REF_SLUG-$CI_COMMIT_SHORT_SHA"
  LATEST_TAG: "$CI_REGISTRY_IMAGE/demo-react-app:latest"
  # Variables de build
  DOCKER_BUILDKIT: 1

stages:
  - validate
  - build
  - test
  - docker-build
  - docker-test
  - security-scan
  - deploy

# Cache pour optimiser les builds
cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - node_modules/
    - .docker/
    - .npm/

# Template pour les jobs Docker
.docker_job_template: &docker_job
  before_script:
    - docker info
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"

# Validation complète de l'environnement
validate_environment:
  stage: validate
  <<: *docker_job
  script:
    - echo "🔍 === VALIDATION ENVIRONNEMENT DOCKER ==="
    - echo "Docker version: $(docker --version)"
    - echo "Docker info:"
    - docker info | grep -E "(Storage Driver|Kernel Version|Operating System)"
    - echo ""
    - echo "📋 Variables du pipeline:"
    - echo "  - CI_REGISTRY: $CI_REGISTRY"
    - echo "  - IMAGE_NAME: $IMAGE_NAME"
    - echo "  - IMAGE_TAG: $IMAGE_TAG"
    - echo "  - COMMIT: $CI_COMMIT_SHORT_SHA"
    - echo "  - BRANCH: $CI_COMMIT_REF_NAME"
    - echo ""
    - echo "📁 Validation des fichiers Docker:"
    - |
      files_missing=0

      if [ ! -f "Dockerfile" ]; then
        echo "❌ Dockerfile missing"
        files_missing=$((files_missing + 1))
      else
        echo "✅ Dockerfile found"
      fi

      if [ ! -f "nginx.conf.template" ]; then
        echo "❌ nginx.conf.template missing"
        files_missing=$((files_missing + 1))
      else
        echo "✅ nginx.conf.template found"
      fi

      if [ ! -f "docker-entrypoint.sh" ]; then
        echo "❌ docker-entrypoint.sh missing"
        files_missing=$((files_missing + 1))
      else
        echo "✅ docker-entrypoint.sh found"
      fi

      if [ $files_missing -gt 0 ]; then
        echo "❌ $files_missing file(s) missing"
        exit 1
      fi
    - echo "✅ Tous les fichiers Docker sont présents"
  only:
    - main
    - develop
    - merge_requests

# Build de l'application Node.js
build_application:
  image: node:18-alpine
  stage: build
  before_script:
    - echo "🏗️ === BUILD APPLICATION REACT ==="
    - node --version
    - npm --version
  script:
    - echo "📦 Installation des dépendances"
    - npm ci --prefer-offline --no-audit
    - echo "🔨 Build de l'application"
    - npm run build
    - echo "📊 Analyse du build:"
    - ls -la build/
    - echo "💾 Taille totale: $(du -sh build/)"
    - find build/ -name "*.js" -o -name "*.css" | head -5
  artifacts:
    paths:
      - build/
      - package*.json
      - public/
      - src/
      - Dockerfile
      - nginx.conf.template
      - docker-entrypoint.sh
      - .dockerignore
    expire_in: 2 hours
  cache:
    key: npm-$CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
      - .npm/
  only:
    - main
    - develop
    - merge_requests

# Tests unitaires
test_application:
  image: node:18-alpine
  stage: test
  before_script:
    - echo "🧪 === TESTS UNITAIRES ==="
  script:
    - npm ci --prefer-offline --no-audit
    - npm test -- --coverage --watchAll=false --verbose
    - echo "📊 Couverture de code générée"
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 week
  cache:
    key: npm-$CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
  only:
    - main
    - develop
    - merge_requests

# Construction de l'image Docker avec BuildKit
docker_build:
  stage: docker-build
  <<: *docker_job
  script:
    - echo "🐳 === CONSTRUCTION IMAGE DOCKER ==="
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - echo "Registry: $CI_REGISTRY"
    - |
      # Build avec cache et arguments
      docker build \
        --build-arg NODE_ENV=production \
        --build-arg REACT_APP_VERSION="$APP_VERSION" \
        --build-arg REACT_APP_BUILD="$CI_PIPELINE_ID" \
        --build-arg REACT_APP_COMMIT_SHA="$CI_COMMIT_SHORT_SHA" \
        --tag "$IMAGE_NAME:$IMAGE_TAG" \
        --tag "$IMAGE_NAME:$CI_COMMIT_REF_SLUG" \
        --label "version=$APP_VERSION" \
        --label "commit=$CI_COMMIT_SHA" \
        --label "pipeline=$CI_PIPELINE_ID" \
        --label "branch=$CI_COMMIT_REF_NAME" \
        .
    - echo "📤 Push des images"
    - docker push "$IMAGE_NAME:$IMAGE_TAG"
    - docker push "$IMAGE_NAME:$CI_COMMIT_REF_SLUG"
    - |
      # Tag latest pour main
      if [ "$CI_COMMIT_REF_NAME" = "main" ]; then
        docker tag "$IMAGE_NAME:$IMAGE_TAG" "$LATEST_TAG"
        docker push "$LATEST_TAG"
        echo "✅ Image latest pushée"
      fi
    - echo "📊 Informations des images:"
    - docker images "$IMAGE_NAME"
    - echo "🔍 Inspection de l'image:"
    - docker inspect "$IMAGE_NAME:$IMAGE_TAG" --format='{{.Size}}' | awk '{print "Size: " $1/1024/1024 " MB"}'
  dependencies:
    - build_application
  only:
    - main
    - develop
    - merge_requests

# Tests complets de l'image Docker
docker_test:
  stage: docker-test
  <<: *docker_job
  script:
    - echo "🧪 === TESTS IMAGE DOCKER ==="
    - echo "Test de l'image: $IMAGE_NAME:$IMAGE_TAG"
    - docker pull "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Test de sécurité : vérification utilisateur non-root
      echo "🔒 Test sécurité - Utilisateur non-root"
      USER_ID=$(docker run --rm "$IMAGE_NAME:$IMAGE_TAG" id -u)
      if [ "$USER_ID" != "0" ]; then
        echo "✅ Container s'exécute avec l'utilisateur $USER_ID (non-root)"
      else
        echo "❌ Container s'exécute en root - ÉCHEC SÉCURITÉ"
        exit 1
      fi
    - |
      # Test fonctionnel complet
      echo "🚀 Démarrage du container de test"
      docker run -d \
        --name test-container \
        --health-cmd="curl -f http://localhost:8080/health || exit 1" \
        --health-interval=10s \
        --health-timeout=5s \
        --health-retries=3 \
        -p 8080:8080 \
        -e APP_NAME="demo-react-app-test" \
        -e APP_VERSION="test-$CI_PIPELINE_ID" \
        "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Attente et vérification du health check
      echo "⏳ Attente du démarrage (30s max)"
      timeout=30
      while [ $timeout -gt 0 ]; do
        health_status=$(docker inspect test-container --format='{{.State.Health.Status}}')
        if [ "$health_status" = "healthy" ]; then
          echo "✅ Container healthy"
          break
        elif [ "$health_status" = "unhealthy" ]; then
          echo "❌ Container unhealthy"
          docker logs test-container
          exit 1
        fi
        sleep 2
        timeout=$((timeout - 2))
      done
    - |
      # Tests des endpoints
      echo "🔍 Tests des endpoints"

      # Health check
      echo "Testing /health endpoint"
      docker exec test-container curl -f http://localhost:8080/health

      # Status endpoint
      echo "Testing /status endpoint"
      docker exec test-container curl -f http://localhost:8080/status

      # Page principale
      echo "Testing main page"
      response=$(docker exec test-container curl -f http://localhost:8080/)
      if echo "$response" | grep -q "<title>React App</title>"; then
        echo "✅ Page principale accessible"
      else
        echo "❌ Page principale invalide"
        exit 1
      fi
    - |
      # Tests de performance
      echo "📊 Tests de performance basiques"
      echo "Response time for /health:"
      docker exec test-container curl -w "@-" -o /dev/null -s http://localhost:8080/health << 'EOF'
      time_total: %{time_total}s
      time_connect: %{time_connect}s
      time_starttransfer: %{time_starttransfer}s
      EOF
    - |
      # Nettoyage
      echo "🧹 Nettoyage"
      docker logs test-container --tail 20
      docker stop test-container
      docker rm test-container
    - echo "✅ Tous les tests Docker réussis"
  dependencies:
    - docker_build
  only:
    - main
    - develop
    - merge_requests

# Scan de sécurité avec Trivy
security_scan:
  stage: security-scan
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  <<: *docker_job
  script:
    - echo "🔒 === SCAN DE SÉCURITÉ TRIVY ==="
    - echo "Scan de l'image: $IMAGE_NAME:$IMAGE_TAG"
    - docker pull "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Scan de vulnérabilités
      trivy image \
        --exit-code 0 \
        --no-progress \
        --format table \
        --severity HIGH,CRITICAL \
        "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Scan avec rapport JSON
      trivy image \
        --exit-code 0 \
        --no-progress \
        --format json \
        --output security-report.json \
        "$IMAGE_NAME:$IMAGE_TAG"
    - echo "✅ Scan de sécurité terminé"
  artifacts:
    paths:
      - security-report.json
    expire_in: 1 week
    reports:
      security: security-report.json
  dependencies:
    - docker_build
  allow_failure: true
  only:
    - main
    - develop
    - merge_requests

# Déploiement staging avec monitoring
deploy_staging_docker:
  stage: deploy
  variables:
    DEPLOY_ENV: "staging"
    CONTAINER_NAME: "demo-app-staging"
    CONTAINER_PORT: "8081"
  <<: *docker_job
  script:
    - echo "🚀 === DÉPLOIEMENT DOCKER STAGING ==="
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - echo "Container: $CONTAINER_NAME"
    - echo "Port: $CONTAINER_PORT"
    - |
      # Arrêt gracieux du container existant
      if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo "🛑 Arrêt du container existant"
        docker stop "$CONTAINER_NAME" --time 30
        docker rm "$CONTAINER_NAME"
      fi
    - |
      # Démarrage du nouveau container avec configuration complète
      docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        -p "$CONTAINER_PORT:8080" \
        -e APP_NAME="$APP_NAME" \
        -e APP_VERSION="$APP_VERSION" \
        -e DEPLOY_ENV="$DEPLOY_ENV" \
        -e NGINX_WORKER_PROCESSES="auto" \
        -e NGINX_WORKER_CONNECTIONS="1024" \
        --label "environment=$DEPLOY_ENV" \
        --label "version=$APP_VERSION" \
        --label "pipeline=$CI_PIPELINE_ID" \
        --label "deployed_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --health-cmd="curl -f http://localhost:8080/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Vérification du déploiement
      echo "⏳ Vérification du démarrage"
      sleep 10

      # Status du container
      docker ps --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

      # Health check
      timeout=60
      while [ $timeout -gt 0 ]; do
        health_status=$(docker inspect "$CONTAINER_NAME" --format='{{.State.Health.Status}}')
        if [ "$health_status" = "healthy" ]; then
          echo "✅ Container healthy"
          break
        elif [ "$health_status" = "unhealthy" ]; then
          echo "❌ Container unhealthy"
          docker logs "$CONTAINER_NAME" --tail 50
          exit 1
        fi
        sleep 5
        timeout=$((timeout - 5))
      done
    - |
      # Tests post-déploiement
      echo "🔍 Tests post-déploiement"
      docker logs "$CONTAINER_NAME" --tail 10
      echo "✅ Déploiement staging réussi"
      echo "🌐 URL: http://localhost:$CONTAINER_PORT"
  environment:
    name: staging-docker
    url: http://staging-docker.example.com:8081
  dependencies:
    - docker_build
  only:
    - main
  when: manual

# Déploiement production avec stratégie blue-green
deploy_production_docker:
  stage: deploy
  variables:
    DEPLOY_ENV: "production"
    CONTAINER_NAME: "demo-app-production"
    CONTAINER_PORT: "8080"
  <<: *docker_job
  script:
    - echo "🚀 === DÉPLOIEMENT DOCKER PRODUCTION ==="
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - echo "Container: $CONTAINER_NAME"
    - |
      # Validation stricte pour production
      if [ "$CI_COMMIT_REF_NAME" != "main" ]; then
        echo "❌ Déploiement production autorisé seulement depuis main"
        exit 1
      fi
    - |
      # Stratégie blue-green
      BACKUP_CONTAINER="${CONTAINER_NAME}-backup"
      NEW_CONTAINER="${CONTAINER_NAME}-new"

      echo "🔄 Déploiement blue-green"

      # Étape 1: Démarrage du nouveau container (green)
      echo "🟢 Démarrage du nouveau container"
      docker run -d \
        --name "$NEW_CONTAINER" \
        --restart unless-stopped \
        -p "8082:8080" \
        -e APP_NAME="$APP_NAME" \
        -e APP_VERSION="$APP_VERSION" \
        -e DEPLOY_ENV="$DEPLOY_ENV" \
        --label "environment=$DEPLOY_ENV" \
        --label "version=$APP_VERSION" \
        --label "pipeline=$CI_PIPELINE_ID" \
        --health-cmd="curl -f http://localhost:8080/health || exit 1" \
        --health-interval=10s \
        --health-timeout=5s \
        --health-retries=5 \
        "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Étape 2: Vérification de santé du nouveau container
      echo "⏳ Vérification de santé (60s max)"
      timeout=60
      while [ $timeout -gt 0 ]; do
        health_status=$(docker inspect "$NEW_CONTAINER" --format='{{.State.Health.Status}}')
        if [ "$health_status" = "healthy" ]; then
          echo "✅ Nouveau container healthy"
          break
        elif [ "$health_status" = "unhealthy" ]; then
          echo "❌ Nouveau container unhealthy - Rollback"
          docker logs "$NEW_CONTAINER" --tail 50
          docker stop "$NEW_CONTAINER"
          docker rm "$NEW_CONTAINER"
          exit 1
        fi
        sleep 5
        timeout=$((timeout - 5))
      done
    - |
      # Étape 3: Swap des containers (blue-green switch)
      echo "🔄 Switch blue-green"

      # Backup de l'ancien container s'il existe
      if docker ps -q --filter "name=$CONTAINER_NAME" | grep -q .; then
        echo "💾 Backup de l'ancien container"
        docker stop "$CONTAINER_NAME" --time 30
        docker rename "$CONTAINER_NAME" "$BACKUP_CONTAINER"
      fi

      # Switch du nouveau container vers le nom de production
      docker stop "$NEW_CONTAINER" --time 10
      docker rename "$NEW_CONTAINER" "$CONTAINER_NAME"

      # Redémarrage avec le bon port
      docker rm "$CONTAINER_NAME"
      docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        -p "$CONTAINER_PORT:8080" \
        -e APP_NAME="$APP_NAME" \
        -e APP_VERSION="$APP_VERSION" \
        -e DEPLOY_ENV="$DEPLOY_ENV" \
        --label "environment=$DEPLOY_ENV" \
        --label "version=$APP_VERSION" \
        --label "pipeline=$CI_PIPELINE_ID" \
        --health-cmd="curl -f http://localhost:8080/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        "$IMAGE_NAME:$IMAGE_TAG"
    - |
      # Étape 4: Validation finale
      echo "✅ Validation finale"
      sleep 15

      # Test de santé final
      health_status=$(docker inspect "$CONTAINER_NAME" --format='{{.State.Health.Status}}')
      if [ "$health_status" != "healthy" ]; then
        echo "❌ Échec validation finale - Rollback"
        exit 1
      fi

      # Suppression du backup si succès
      if docker ps -a -q --filter "name=$BACKUP_CONTAINER" | grep -q .; then
        echo "🧹 Suppression du backup"
        docker rm "$BACKUP_CONTAINER"
      fi
    - echo "✅ Déploiement production réussi"
    - echo "🌐 URL: http://localhost:$CONTAINER_PORT"
    - docker ps --filter "name=$CONTAINER_NAME"
  environment:
    name: production-docker
    url: http://production-docker.example.com
  dependencies:
    - docker_build
  needs:
    - security_scan
  only:
    - main
  when: manual
  allow_failure: false
```

## Optimisations appliquées

### 1. Dockerfile multi-stage

**Avantages** :

- **Réduction de taille** : Image finale ~50MB vs ~500MB sans multi-stage
- **Sécurité** : Séparation build/runtime, pas d'outils de développement en production
- **Performance** : Cache optimisé, layers réutilisables

### 2. Configuration Nginx optimisée

**Performance** :

- Compression Gzip pour tous les types de fichiers appropriés
- Cache agressif pour les assets statiques
- Configuration keepalive optimisée

**Sécurité** :

- Headers de sécurité complets (CSP, XSS Protection, etc.)
- Utilisateur non-root
- Endpoints sensibles désactivés

### 3. Pipeline Docker avancé

**Fonctionnalités** :

- Build avec BuildKit pour performance
- Tests de sécurité automatisés
- Health checks intégrés
- Déploiement blue-green pour production

**Monitoring** :

- Métriques de performance dans les logs
- Health checks complets
- Validation post-déploiement

## Bonnes pratiques implémentées

### 1. Sécurité

- ✅ Utilisateur non-root dans les containers
- ✅ Scan de vulnérabilités avec Trivy
- ✅ Headers de sécurité HTTP
- ✅ Validation des images avant déploiement

### 2. Performance

- ✅ Build multi-stage pour réduire la taille
- ✅ Cache Docker optimisé
- ✅ Compression et optimisation Nginx
- ✅ Health checks pour disponibilité

### 3. Observabilité

- ✅ Logs structurés
- ✅ Métriques de base
- ✅ Endpoints de monitoring (/health, /status, /metrics)
- ✅ Traçabilité complète (labels, métadonnées)

## Résultats attendus

### Métriques d'image

- **Taille finale** : ~45-60 MB (vs 400+ MB sans optimisation)
- **Layers** : 8-12 layers optimisés
- **Temps de build** : 2-4 minutes
- **Temps de démarrage** : 5-10 secondes

### Performance

- **Temps de réponse** : <100ms pour /health
- **Débit** : Support 1000+ req/s avec configuration standard
- **Mémoire** : ~20-50 MB RAM par container
- **CPU** : <5% CPU usage en idle
