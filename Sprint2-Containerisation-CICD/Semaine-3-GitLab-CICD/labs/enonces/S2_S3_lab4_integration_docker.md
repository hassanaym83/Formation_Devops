# LAB 4 - Intégration Docker dans GitLab CI/CD

## Contexte

Votre équipe DevOps souhaite containeriser l'application React et intégrer Docker dans le pipeline GitLab CI/CD. Cela permettra d'avoir des déploiements plus cohérents, portables et scalables en utilisant des images Docker optimisées.

## Objectif

Créer un Dockerfile optimisé, intégrer la construction d'images Docker dans le pipeline GitLab CI/CD, et implémenter un déploiement basé sur des containers.

## Prérequis

- LAB 3 complété (variables et secrets)
- Connaissances de base Docker
- Docker disponible sur votre machine pour les tests locaux
- Compte Docker Hub ou GitLab Container Registry

## Instructions détaillées

### Étape 1 : Création du Dockerfile optimisé (10 minutes)

1. **Créer un Dockerfile multi-stage** dans la racine du projet :

```dockerfile
# Dockerfile pour application React avec build multi-stage
# Stage 1: Build de l'application
FROM node:18-alpine AS builder

# Métadonnées
LABEL maintainer="DevOps Team <devops@example.com>"
LABEL description="Demo React App for GitLab CI/CD"
LABEL version="1.0.0"

# Variables d'environnement de build
ARG NODE_ENV=production
ARG REACT_APP_VERSION
ARG REACT_APP_BUILD
ARG REACT_APP_COMMIT_SHA

ENV NODE_ENV=$NODE_ENV
ENV CI=true

# Création utilisateur non-root pour sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S reactuser -u 1001

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation des dépendances avec optimisations
RUN npm ci --only=production --no-audit --prefer-offline && \
    npm cache clean --force

# Copie du code source
COPY . .

# Changement de propriétaire des fichiers
RUN chown -R reactuser:nodejs /app
USER reactuser

# Build de l'application
RUN npm run build

# Stage 2: Image de production avec Nginx
FROM nginx:1.25-alpine AS production

# Installation de gettext pour envsubst (substitution variables)
RUN apk add --no-cache gettext

# Variables d'environnement
ENV APP_NAME="demo-react-app"
ENV APP_VERSION="1.0.0"

# Copie des fichiers build depuis le stage builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copie de la configuration Nginx personnalisée
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Script de démarrage
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Création utilisateur nginx non-root
RUN addgroup -g 1001 -S nginx && \
    adduser -S nginx -u 1001 -G nginx

# Configuration des permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Exposition du port
EXPOSE 8080

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Utilisateur non-root
USER nginx

# Point d'entrée
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

2. **Créer le fichier de configuration Nginx** `nginx.conf.template` :

```nginx
worker_processes auto;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Optimisations de performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Configuration des logs
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    server {
        listen 8080;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Configuration pour React Router (SPA)
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Cache pour les assets statiques
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Headers de sécurité
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

3. **Créer le script d'entrée** `docker-entrypoint.sh` :

```bash
#!/bin/sh
set -e

# Substitution des variables d'environnement dans la config Nginx
envsubst '${APP_NAME} ${APP_VERSION}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Affichage des informations de démarrage
echo "🚀 Starting $APP_NAME v$APP_VERSION"
echo "📅 Started at: $(date)"
echo "🐳 Container ID: $(hostname)"

# Exécution de la commande
exec "$@"
```

### Étape 2 : Intégration Docker dans le pipeline (15 minutes)

1. **Mettre à jour `.gitlab-ci.yml`** :

```yaml
# Pipeline GitLab CI/CD avec intégration Docker
image: docker:24.0.5

# Services Docker-in-Docker
services:
  - docker:24.0.5-dind

# Variables globales
variables:
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_CERTDIR: '/certs'
  DOCKER_TLS_VERIFY: 1
  DOCKER_CERT_PATH: '$DOCKER_TLS_CERTDIR/client'
  DOCKER_DRIVER: overlay2
  # Variables d'image
  IMAGE_NAME: '$CI_REGISTRY_IMAGE'
  IMAGE_TAG: '$CI_COMMIT_REF_SLUG-$CI_COMMIT_SHORT_SHA'

stages:
  - validate
  - build
  - test
  - docker-build
  - docker-test
  - deploy

# Cache pour Docker layers
cache:
  key: docker-cache
  paths:
    - .docker/

# Validation des prérequis Docker
validate_docker:
  stage: validate
  before_script:
    - docker info
    - docker version
  script:
    - echo "🔍 Validation de l'environnement Docker"
    - echo "Docker version: $(docker --version)"
    - echo "Registry: $CI_REGISTRY"
    - echo "Image name: $IMAGE_NAME"
    - echo "Image tag: $IMAGE_TAG"
    - |
      if [ ! -f "Dockerfile" ]; then
        echo "❌ Dockerfile non trouvé"
        exit 1
      fi
    - echo "✅ Environnement Docker validé"
  only:
    - main
    - develop
    - merge_requests

# Build de l'application (stage intermédiaire)
build_app:
  image: node:18-alpine
  stage: build
  script:
    - echo "🏗️ Build de l'application React"
    - npm ci --prefer-offline
    - npm run build
    - echo "📊 Taille du build: $(du -sh build/)"
  artifacts:
    paths:
      - build/
      - package*.json
      - public/
      - src/
      - Dockerfile
      - nginx.conf.template
      - docker-entrypoint.sh
    expire_in: 1 hour
  cache:
    key: npm-cache
    paths:
      - node_modules/
      - .npm/
  only:
    - main
    - develop
    - merge_requests

# Tests de l'application
test_app:
  image: node:18-alpine
  stage: test
  script:
    - echo "🧪 Exécution des tests"
    - npm ci --prefer-offline
    - npm test -- --coverage --watchAll=false
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  cache:
    key: npm-cache
    paths:
      - node_modules/
  only:
    - main
    - develop
    - merge_requests

# Construction de l'image Docker
docker_build:
  stage: docker-build
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker info
  script:
    - echo "🐳 Construction de l'image Docker"
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - |
      docker build \
        --build-arg NODE_ENV=production \
        --build-arg REACT_APP_VERSION="$APP_VERSION" \
        --build-arg REACT_APP_BUILD="$CI_PIPELINE_ID" \
        --build-arg REACT_APP_COMMIT_SHA="$CI_COMMIT_SHORT_SHA" \
        --tag "$IMAGE_NAME:$IMAGE_TAG" \
        --tag "$IMAGE_NAME:latest" \
        .
    - echo "📤 Push de l'image vers le registry"
    - docker push "$IMAGE_NAME:$IMAGE_TAG"
    - docker push "$IMAGE_NAME:latest"
    - echo "📊 Informations de l'image:"
    - docker images "$IMAGE_NAME"
  dependencies:
    - build_app
  only:
    - main
    - develop
    - merge_requests

# Tests de l'image Docker
docker_test:
  stage: docker-test
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  script:
    - echo "🧪 Tests de l'image Docker"
    - echo "Pull de l'image: $IMAGE_NAME:$IMAGE_TAG"
    - docker pull "$IMAGE_NAME:$IMAGE_TAG"
    - echo "🚀 Démarrage du container de test"
    - |
      docker run -d \
        --name test-container \
        -p 8080:8080 \
        -e APP_NAME="demo-react-app-test" \
        -e APP_VERSION="test-$CI_PIPELINE_ID" \
        "$IMAGE_NAME:$IMAGE_TAG"
    - sleep 10
    - echo "🔍 Vérification du health check"
    - docker exec test-container curl -f http://localhost:8080/health
    - echo "📄 Test de la page d'accueil"
    - docker exec test-container curl -f http://localhost:8080/
    - echo "📋 Logs du container:"
    - docker logs test-container
    - echo "🧹 Nettoyage"
    - docker stop test-container
    - docker rm test-container
    - echo "✅ Tests Docker réussis"
  dependencies:
    - docker_build
  only:
    - main
    - develop
    - merge_requests

# Déploiement avec Docker
deploy_staging_docker:
  stage: deploy
  variables:
    DEPLOY_ENV: 'staging'
    CONTAINER_NAME: 'demo-app-staging'
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  script:
    - echo "🚀 Déploiement Docker staging"
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - echo "Container: $CONTAINER_NAME"
    - |
      # Arrêt et suppression du container existant
      docker stop "$CONTAINER_NAME" 2>/dev/null || true
      docker rm "$CONTAINER_NAME" 2>/dev/null || true
    - |
      # Démarrage du nouveau container
      docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        -p 8081:8080 \
        -e APP_NAME="$APP_NAME" \
        -e APP_VERSION="$APP_VERSION" \
        -e DEPLOY_ENV="$DEPLOY_ENV" \
        --label "environment=$DEPLOY_ENV" \
        --label "version=$APP_VERSION" \
        --label "pipeline=$CI_PIPELINE_ID" \
        "$IMAGE_NAME:$IMAGE_TAG"
    - sleep 5
    - echo "🔍 Vérification du déploiement"
    - docker ps --filter "name=$CONTAINER_NAME"
    - docker logs "$CONTAINER_NAME" --tail 10
    - echo "✅ Déploiement staging réussi"
    - echo "🌐 URL: http://localhost:8081"
  environment:
    name: staging-docker
    url: http://staging-docker.example.com
  dependencies:
    - docker_build
  only:
    - main
  when: manual

# Déploiement production avec Docker
deploy_production_docker:
  stage: deploy
  variables:
    DEPLOY_ENV: 'production'
    CONTAINER_NAME: 'demo-app-production'
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
  script:
    - echo "🚀 Déploiement Docker production"
    - echo "Image: $IMAGE_NAME:$IMAGE_TAG"
    - echo "Container: $CONTAINER_NAME"
    - |
      # Validation de sécurité
      if [ "$CI_COMMIT_REF_NAME" != "main" ]; then
        echo "❌ Déploiement production autorisé seulement depuis main"
        exit 1
      fi
    - |
      # Déploiement blue-green simulé
      BACKUP_CONTAINER="${CONTAINER_NAME}-backup"

      # Backup du container actuel
      if docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "$CONTAINER_NAME"; then
        echo "📦 Sauvegarde du container actuel"
        docker stop "$CONTAINER_NAME"
        docker rename "$CONTAINER_NAME" "$BACKUP_CONTAINER"
      fi
    - |
      # Démarrage du nouveau container
      docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        -p 8080:8080 \
        -e APP_NAME="$APP_NAME" \
        -e APP_VERSION="$APP_VERSION" \
        -e DEPLOY_ENV="$DEPLOY_ENV" \
        --label "environment=$DEPLOY_ENV" \
        --label "version=$APP_VERSION" \
        --label "pipeline=$CI_PIPELINE_ID" \
        "$IMAGE_NAME:$IMAGE_TAG"
    - sleep 10
    - echo "🔍 Test de santé post-déploiement"
    - docker exec "$CONTAINER_NAME" curl -f http://localhost:8080/health
    - |
      # Suppression du backup si succès
      if docker ps --filter "name=$BACKUP_CONTAINER" --format "{{.Names}}" | grep -q "$BACKUP_CONTAINER"; then
        echo "🧹 Suppression du backup"
        docker rm "$BACKUP_CONTAINER"
      fi
    - echo "✅ Déploiement production réussi"
    - echo "🌐 URL: http://localhost:8080"
  environment:
    name: production-docker
    url: http://production-docker.example.com
  dependencies:
    - docker_build
  only:
    - main
  when: manual
  allow_failure: false
```

### Étape 3 : Test et optimisation (5 minutes)

1. **Créer un `.dockerignore`** :

```
node_modules
npm-debug.log*
.git
.gitignore
README.md
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
coverage
.docker
```

2. **Test local** :

```bash
# Build de l'image
docker build -t demo-react-app:test .

# Test du container
docker run -d --name test -p 3000:8080 demo-react-app:test

# Vérification
curl http://localhost:3000/health
```

3. **Commit et push** vers GitLab

## Livrables attendus

### 1. Fichiers Docker

- `Dockerfile` multi-stage optimisé
- `nginx.conf.template` avec configuration sécurisée
- `docker-entrypoint.sh` fonctionnel
- `.dockerignore` approprié

### 2. Pipeline Docker intégré

- Construction d'image automatisée
- Tests de l'image Docker
- Déploiement basé sur containers
- Registry GitLab configuré

### 3. Documentation

Créer `docker_integration.md` avec :

- Architecture Docker expliquée
- Commandes de test et déploiement
- Optimisations appliquées
- Stratégie de déploiement blue-green

## Critères d'évaluation

**Total : 25 points**

- **Dockerfile optimisé (8 points)** : Multi-stage, sécurisé, non-root user
- **Pipeline Docker (10 points)** : Build, test, push image fonctionnels
- **Déploiement containers (5 points)** : Staging et production avec Docker
- **Documentation (2 points)** : Guide complet et clair

## Durée estimée

**30 minutes** réparties :

- Création Dockerfile : 10 minutes
- Intégration pipeline : 15 minutes
- Test et optimisation : 5 minutes

## Conseils

- Utiliser des images Alpine pour réduire la taille
- Implémenter un utilisateur non-root pour la sécurité
- Optimiser les layers Docker avec un build multi-stage
- Tester localement avant de pusher

## Ressources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Nginx Configuration](https://nginx.org/en/docs/)
