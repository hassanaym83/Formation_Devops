# LAB 3 - Intégration Docker et migration Compose

**Sprint 2 - Semaine 3 - Séance 1**  
**Référence** : `S2_S3_S1_lab3_docker_migration`  
**Durée** : 35 minutes

## Objectifs

- Transformer un setup Docker Compose en pipeline GitLab CI/CD automatisé
- Maîtriser l'intégration Docker dans GitLab CI/CD
- Configurer variables et secrets pour environnements multiples
- Comprendre les GitLab Runners et exécuteurs Docker

## Contexte

Migration d'une application microservices e-commerce de la Semaine 2 (Docker Compose) vers un pipeline GitLab CI/CD complet avec build d'images, tests d'intégration et déploiement automatisé.

## Pré-requis

- Connaissances des LABs 1 et 2
- Compréhension de Docker et Docker Compose (Semaine 2)
- Accès GitLab avec Container Registry activé
- Docker disponible localement pour tests

## Architecture de l'application (rappel Semaine 2)

```
ecommerce-microservices/
├── frontend/              # React App
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── backend/               # Node.js API
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── database/              # PostgreSQL
│   └── init-scripts/
├── redis/                 # Cache Redis
├── nginx/                 # Reverse Proxy
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml     # Configuration existante
├── docker-compose.override.yml
└── .gitlab-ci.yml        # À créer
```

## Fichiers de référence (Semaine 2)

### docker-compose.yml existant

```yaml
version: '3.8'

services:
  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init-scripts:/docker-entrypoint-initdb.d
    ports:
      - '5432:5432'

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://admin:secret123@database:5432/ecommerce
      REDIS_URL: redis://redis:6379
      JWT_SECRET: super-secret-jwt-key
      NODE_ENV: development
    ports:
      - '5000:5000'
    depends_on:
      - database
      - redis
    volumes:
      - ./backend:/app
      - /app/node_modules

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      REACT_APP_API_URL: http://localhost:5000
      REACT_APP_ENV: development
    ports:
      - '3000:3000'
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    ports:
      - '80:80'
      - '443:443'
    depends_on:
      - frontend
      - backend
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf

volumes:
  postgres_data:
  redis_data:
```

### Dockerfiles existants

**frontend/Dockerfile**

```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**backend/Dockerfile**

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
EXPOSE 5000

USER node
CMD ["node", "src/server.js"]
```

**nginx/Dockerfile**

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
```

## Instructions

### Étape 1 : Analyse de la migration

Analysez la configuration Docker Compose existante et répondez :

**Questions d'architecture :**

1. **Quels services nécessitent un build d'image ?**

   - Service 1 : **\*\***\_\_\_\_**\*\***
   - Service 2 : **\*\***\_\_\_\_**\*\***
   - Service 3 : **\*\***\_\_\_\_**\*\***

2. **Quelles variables d'environnement doivent être sécurisées ?**

   - ***
   - ***
   - ***

3. **Quels services doivent être testés ensemble ?**

   - ***
   - ***

4. **Quelle stratégie de déploiement adopter ?**
   - Environnement 1 : **\*\***\_\_\_\_**\*\***
   - Environnement 2 : **\*\***\_\_\_\_**\*\***

### Étape 2 : Configuration des variables GitLab

Dans GitLab, configurez les variables suivantes :

**Variables CI/CD (Settings > CI/CD > Variables) :**

```bash
# Registry Docker
CI_REGISTRY_USER=gitlab-ci-token
CI_REGISTRY_PASSWORD=[TOKEN_AUTO]

# Database
DATABASE_URL_DEV=postgresql://admin:secret123@localhost:5432/ecommerce_dev
DATABASE_URL_PROD=postgresql://admin:prod_secret@prod-db:5432/ecommerce

# Secrets (Type: Variable, Protected: Yes, Masked: Yes)
JWT_SECRET_DEV=dev-jwt-secret-key-here
JWT_SECRET_PROD=prod-jwt-secret-key-here
POSTGRES_PASSWORD_DEV=secret123
POSTGRES_PASSWORD_PROD=prod_secret_db_2024

# URLs environnements
FRONTEND_URL_DEV=https://dev.ecommerce-app.com
FRONTEND_URL_PROD=https://ecommerce-app.com
BACKEND_URL_DEV=https://api-dev.ecommerce-app.com
BACKEND_URL_PROD=https://api.ecommerce-app.com

# Notifications
SLACK_WEBHOOK_URL=[WEBHOOK_URL]
```

### Étape 3 : Stratégie de build d'images

Créez un pipeline qui :

1. **Build les images** en parallèle pour chaque service
2. **Tag les images** avec `$CI_COMMIT_SHA` et `latest`
3. **Push vers GitLab Container Registry**
4. **Utilise des stages multiples** pour optimisation

**Template de build service :**

```yaml
build_[service]:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  variables:
    DOCKER_TLS_CERTDIR: '/certs'
    IMAGE_TAG: $CI_REGISTRY_IMAGE/[service]:$CI_COMMIT_SHA
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # À compléter
  rules:
    # À compléter
```

### Étape 4 : Tests d'intégration avec services

Configurez des tests qui utilisent les images buildées :

```yaml
integration_tests:
  stage: test
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
    - name: postgres:15-alpine
      alias: test-database
      variables:
        POSTGRES_DB: ecommerce_test
        POSTGRES_USER: test_user
        POSTGRES_PASSWORD: test_pass
    - name: redis:7-alpine
      alias: test-redis
  variables:
    # À configurer
  script:
    # À compléter
```

### Étape 5 : Déploiement avec Docker Compose

Créez un job de déploiement qui :

1. **Génère un docker-compose dynamique** avec les nouvelles images
2. **Configure les variables d'environnement** selon l'environnement
3. **Déploie via docker-compose** sur les serveurs cibles

**Template docker-compose de déploiement :**

```yaml
# docker-compose.deploy.yml (généré dynamiquement)
version: '3.8'
services:
  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

  redis:
    image: redis:7-alpine

  backend:
    image: ${CI_REGISTRY_IMAGE}/backend:${CI_COMMIT_SHA}
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: redis://redis:6379
      JWT_SECRET: ${JWT_SECRET}
      NODE_ENV: ${NODE_ENV}
    depends_on:
      - database
      - redis

  frontend:
    image: ${CI_REGISTRY_IMAGE}/frontend:${CI_COMMIT_SHA}
    environment:
      REACT_APP_API_URL: ${BACKEND_URL}
      REACT_APP_ENV: ${NODE_ENV}
    depends_on:
      - backend

  nginx:
    image: ${CI_REGISTRY_IMAGE}/nginx:${CI_COMMIT_SHA}
    ports:
      - '80:80'
      - '443:443'
    depends_on:
      - frontend
      - backend
```

### Étape 6 : Pipeline complet à implémenter

```yaml
# Configuration GitLab CI/CD - Migration Docker Compose
# Microservices: Frontend React + Backend Node.js + Nginx + PostgreSQL + Redis

stages:
  - build
  - test
  - deploy
  - cleanup

variables:
  # Variables Docker
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: '/certs'

  # Images de base
  POSTGRES_IMAGE: postgres:15-alpine
  REDIS_IMAGE: redis:7-alpine

  # Registry paths
  FRONTEND_IMAGE: $CI_REGISTRY_IMAGE/frontend
  BACKEND_IMAGE: $CI_REGISTRY_IMAGE/backend
  NGINX_IMAGE: $CI_REGISTRY_IMAGE/nginx

# ========================
# STAGE: BUILD
# ========================

build_backend:
  stage: build
  # À compléter

build_frontend:
  stage: build
  # À compléter

build_nginx:
  stage: build
  # À compléter

# ========================
# STAGE: TEST
# ========================

unit_tests_backend:
  stage: test
  # À compléter

unit_tests_frontend:
  stage: test
  # À compléter

integration_tests:
  stage: test
  # À compléter

security_scan:
  stage: test
  # À compléter

# ========================
# STAGE: DEPLOY
# ========================

deploy_development:
  stage: deploy
  # À compléter

deploy_staging:
  stage: deploy
  # À compléter

deploy_production:
  stage: deploy
  # À compléter

# ========================
# STAGE: CLEANUP
# ========================

cleanup_images:
  stage: cleanup
  # À compléter
```

### Étape 7 : Tests de validation

Après déploiement, implémentez des tests automatiques :

1. **Health checks** des services
2. **Tests E2E** de l'application
3. **Tests de performance** basiques
4. **Validation des logs** de déploiement

## Critères d'évaluation (12 points)

- **Migration réussie** (3 points) : Passage de Compose vers GitLab CI/CD
- **Images buildées** (3 points) : Tous les services buildent correctement
- **Tests d'intégration** (2 points) : Services testés ensemble
- **Variables sécurisées** (2 points) : Secrets bien configurés
- **Déploiement fonctionnel** (2 points) : Application accessible

## Questions de réflexion

1. **Quelles sont les différences principales entre docker-compose local et déploiement CI/CD ?**

2. **Comment sécuriser les variables sensibles dans GitLab ?**

3. **Pourquoi séparer les stages de build, test et deploy ?**

4. **Comment optimiser les temps de build d'images Docker ?**

5. **Quelle stratégie adopter pour les bases de données en CI/CD ?**

## Bonus (optionnel)

- **Multi-stage builds** pour optimiser les images
- **Registry cleanup** automatique des anciennes images
- **Blue-Green deployment** avec docker-compose
- **Monitoring** avec Prometheus/Grafana dans le pipeline
- **Rollback automatique** en cas d'échec

## Ressources

- [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [Docker in Docker (DinD)](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html)
- [GitLab CI Variables](https://docs.gitlab.com/ee/ci/variables/)
- [Docker Compose in CI](https://docs.docker.com/compose/reference/)

---

**Durée estimée :** 35 minutes
**Fichiers de rendu :** `.gitlab-ci.yml` + Configuration variables GitLab
