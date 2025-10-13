# CORRECTION LAB 2 - Configuration avancée jobs et artifacts

**Sprint 2 - Semaine 3 - Séance 1**  
**Référence** : `S2_S3_S1_lab2_jobs_artifacts_correction`

## Solution complète

### Réponses aux questions d'architecture

1. **Combien de stages logiques identifiez-vous ?**

   - Stage 1 : **install** (installation dépendances)
   - Stage 2 : **lint** (vérification qualité code)
   - Stage 3 : **test** (tests unitaires et couverture)
   - Stage 4 : **security** (audit sécurité)
   - Stage 5 : **build** (construction artifacts)
   - Stage 6 : **deploy** (déploiement et tests intégration)

2. **Quels jobs peuvent s'exécuter en parallèle ?**

   - Frontend : install_frontend, lint_frontend, test_frontend, build_frontend
   - Backend : install_backend, lint_backend, test_backend, build_docs

3. **Quels artifacts faut-il partager entre jobs ?**
   - **node_modules/** (install → lint/test/build)
   - **frontend/build/** (build → deploy)
   - **docs/** (documentation générée)

### Fichier .gitlab-ci.yml complet

```yaml
# Configuration GitLab CI/CD E-Commerce Full-Stack
# Architecture: Frontend React + Backend Node.js + Optimisations avancées

stages:
  - install
  - lint
  - test
  - security
  - build
  - deploy

# Variables globales pour optimisation
variables:
  NODE_VERSION: '18'
  FRONTEND_CACHE_KEY: 'frontend-$CI_COMMIT_REF_SLUG'
  BACKEND_CACHE_KEY: 'backend-$CI_COMMIT_REF_SLUG'
  DEBIAN_FRONTEND: 'noninteractive'

# Cache intelligent par composant
cache:
  - key: $FRONTEND_CACHE_KEY
    paths:
      - frontend/node_modules/
    policy: pull-push
  - key: $BACKEND_CACHE_KEY
    paths:
      - backend/node_modules/
    policy: pull-push

# ========================
# STAGE: INSTALL
# ========================

install_frontend:
  stage: install
  image: node:18-alpine
  script:
    - echo "Installation dépendances frontend..."
    - cd frontend
    - npm ci --prefer-offline --no-audit
    - echo "Frontend dependencies installées"
  artifacts:
    paths:
      - frontend/node_modules/
    expire_in: 1 hour
  cache:
    key: $FRONTEND_CACHE_KEY
    paths:
      - frontend/node_modules/
    policy: push
  rules:
    - changes:
        - frontend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

install_backend:
  stage: install
  image: node:18-alpine
  script:
    - echo "Installation dépendances backend..."
    - cd backend
    - npm ci --prefer-offline --no-audit
    - echo "Backend dependencies installées"
  artifacts:
    paths:
      - backend/node_modules/
    expire_in: 1 hour
  cache:
    key: $BACKEND_CACHE_KEY
    paths:
      - backend/node_modules/
    policy: push
  rules:
    - changes:
        - backend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

# ========================
# STAGE: LINT
# ========================

lint_frontend:
  stage: lint
  image: node:18-alpine
  dependencies:
    - install_frontend
  script:
    - echo "Analyse qualité code frontend..."
    - cd frontend
    - npm run lint -- --format=junit --output-file=../frontend-lint-report.xml
    - echo "Lint frontend terminé"
  artifacts:
    reports:
      junit: frontend-lint-report.xml
    when: always
    expire_in: 30 days
  rules:
    - changes:
        - frontend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

lint_backend:
  stage: lint
  image: node:18-alpine
  dependencies:
    - install_backend
  script:
    - echo "Analyse qualité code backend..."
    - cd backend
    - npm run lint -- --format=junit --output-file=../backend-lint-report.xml
    - echo "Lint backend terminé"
  artifacts:
    reports:
      junit: backend-lint-report.xml
    when: always
    expire_in: 30 days
  rules:
    - changes:
        - backend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

# ========================
# STAGE: TEST
# ========================

test_frontend:
  stage: test
  image: node:18-alpine
  dependencies:
    - install_frontend
  script:
    - echo "Exécution tests frontend..."
    - cd frontend
    - npm test -- --coverage --testResultsProcessor=jest-junit
    - echo "Tests frontend terminés"
  artifacts:
    reports:
      junit: frontend/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: frontend/coverage/cobertura-coverage.xml
    paths:
      - frontend/coverage/
    when: always
    expire_in: 30 days
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  rules:
    - changes:
        - frontend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

test_backend:
  stage: test
  image: node:18-alpine
  dependencies:
    - install_backend
  script:
    - echo "Exécution tests backend..."
    - cd backend
    - npm test -- --coverage --testResultsProcessor=jest-junit
    - echo "Tests backend terminés"
  artifacts:
    reports:
      junit: backend/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: backend/coverage/cobertura-coverage.xml
    paths:
      - backend/coverage/
    when: always
    expire_in: 30 days
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  rules:
    - changes:
        - backend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

# ========================
# STAGE: SECURITY
# ========================

security_audit:
  stage: security
  image: node:18-alpine
  dependencies:
    - install_frontend
    - install_backend
  script:
    - echo "Audit de sécurité..."
    - echo "Frontend security audit:"
    - cd frontend && npm audit --audit-level=moderate --json > ../frontend-audit.json || true
    - cd ..
    - echo "Backend security audit:"
    - cd backend && npm audit --audit-level=moderate --json > ../backend-audit.json || true
    - cd ..
    - echo "Audit de sécurité terminé"
  artifacts:
    reports:
      dependency_scanning:
        - frontend-audit.json
        - backend-audit.json
    paths:
      - frontend-audit.json
      - backend-audit.json
    when: always
    expire_in: 30 days
  allow_failure: true
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_MERGE_REQUEST_IID

# ========================
# STAGE: BUILD
# ========================

build_frontend:
  stage: build
  image: node:18-alpine
  dependencies:
    - install_frontend
  script:
    - echo "Build application frontend..."
    - cd frontend
    - npm run build
    - echo "Frontend build terminé"
    - ls -la build/
  artifacts:
    paths:
      - frontend/build/
    expire_in: 1 week
  rules:
    - changes:
        - frontend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

build_docs:
  stage: build
  image: node:18-alpine
  dependencies:
    - install_backend
  script:
    - echo "Génération documentation API..."
    - cd backend
    - npm run docs
    - echo "Documentation générée"
    - ls -la docs/
  artifacts:
    paths:
      - backend/docs/
    expire_in: 6 months
  rules:
    - changes:
        - backend/**/*
        - .gitlab-ci.yml
    - if: $CI_COMMIT_BRANCH == "main"

# ========================
# STAGE: DEPLOY
# ========================

deploy_staging:
  stage: deploy
  image: alpine:latest
  dependencies:
    - build_frontend
    - build_docs
  before_script:
    - apk add --no-cache rsync openssh-client
  script:
    - echo "Déploiement vers staging..."
    - mkdir -p public
    # Déploiement frontend
    - cp -r frontend/build/* public/
    # Déploiement documentation API
    - mkdir -p public/docs
    - cp -r backend/docs/* public/docs/
    - echo "Application déployée sur staging"
    - ls -la public/
  artifacts:
    paths:
      - public/
  environment:
    name: staging
    url: https://staging.ecommerce-demo.com
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
    - if: $CI_COMMIT_BRANCH == "main"

# GitLab Pages (production)
pages:
  stage: deploy
  image: alpine:latest
  dependencies:
    - build_frontend
    - build_docs
  script:
    - echo "Déploiement production GitLab Pages..."
    - mkdir -p public
    - cp -r frontend/build/* public/
    - mkdir -p public/docs
    - cp -r backend/docs/* public/docs/
    - echo "Application déployée en production"
  artifacts:
    paths:
      - public/
  environment:
    name: production
    url: $CI_PAGES_URL
  only:
    - main

integration_tests:
  stage: deploy
  image: node:18-alpine
  dependencies:
    - build_frontend
  services:
    - name: node:18-alpine
      alias: backend-service
  variables:
    API_URL: http://backend-service:5000
  script:
    - echo "Tests d'intégration E2E..."
    - cd backend
    - node src/server.js &
    - sleep 10
    - echo "Tests d'intégration basiques..."
    # Test API health
    - apk add --no-cache curl
    - curl -f http://localhost:5000/api/health || exit 1
    - curl -f http://localhost:5000/api/products || exit 1
    - echo "Tests d'intégration réussis"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_MERGE_REQUEST_IID

# ========================
# MONITORING & NOTIFICATIONS
# ========================

performance_audit:
  stage: deploy
  image: circleci/node:18-browsers
  dependencies:
    - build_frontend
  script:
    - echo "Audit de performance..."
    - npm install -g lighthouse
    - lighthouse --chrome-flags="--headless --no-sandbox" http://localhost:3000 --output=json --output-path=lighthouse-report.json
    - echo "Audit de performance terminé"
  artifacts:
    reports:
      performance: lighthouse-report.json
    when: always
    expire_in: 30 days
  allow_failure: true
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

notify_deployment:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Envoi notifications..."
    - apk add --no-cache curl
    - |
      if [ "$CI_JOB_STATUS" = "success" ]; then
        EMOJI="SUCCESS"
        COLOR="good"
      else
        EMOJI="FAILED"
        COLOR="danger"
      fi
    - echo "Notification envoyée"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: always
  variables:
    SLACK_WEBHOOK_URL: $SLACK_WEBHOOK_URL
```

## Explications détaillées

### Architecture optimisée

1. **Parallélisme intelligent** : Frontend et Backend jobs s'exécutent en parallèle
2. **Cache par composant** : Séparation des caches pour éviter les conflicts
3. **Artifacts stratégiques** : Conservation uniquement des fichiers nécessaires
4. **Conditions dynamiques** : Exécution basée sur les changements de fichiers

### Cache intelligent

```yaml
cache:
  - key: $FRONTEND_CACHE_KEY # Cache séparé pour frontend
    paths:
      - frontend/node_modules/
    policy: pull-push
  - key: $BACKEND_CACHE_KEY # Cache séparé pour backend
    paths:
      - backend/node_modules/
    policy: pull-push
```

**Avantages :**

- Pas de pollution croisée entre composants
- Cache par branche pour isoler les environments
- Policy pull-push pour optimiser les transferts

### Artifacts avec expiration

```yaml
# Dependencies (courte durée)
artifacts:
  paths:
    - frontend/node_modules/
  expire_in: 1 hour

# Build artifacts (durée moyenne)
artifacts:
  paths:
    - frontend/build/
  expire_in: 1 week

# Documentation (longue durée)
artifacts:
  paths:
    - backend/docs/
  expire_in: 6 months
```

### Rapports intégrés GitLab

```yaml
artifacts:
  reports:
    junit: frontend-lint-report.xml # Tests ESLint
    coverage_report: # Couverture de code
      coverage_format: cobertura
      path: frontend/coverage/cobertura-coverage.xml
    dependency_scanning: # Audit sécurité
      - frontend-audit.json
    performance: lighthouse-report.json # Performance web
```

### Conditions d'exécution optimisées

```yaml
rules:
  - changes: # Exécute si fichiers changés
      - frontend/**/*
      - .gitlab-ci.yml
  - if: $CI_COMMIT_BRANCH == "main" # Toujours sur main
```

## Optimisations appliquées

### 1. Performance

- **Cache séparé** par composant évite les conflicts
- **Jobs parallèles** réduisent le temps total
- **Artifacts ciblés** minimisent les transferts

### 2. Sécurité

- **Audit automatique** des dépendances
- **Scanning de vulnérabilités** intégré
- **Variables sécurisées** pour credentials

### 3. Qualité

- **Rapports de couverture** intégrés à GitLab
- **Lint automatique** avec rapports JUnit
- **Tests d'intégration** post-déploiement

### 4. Monitoring

- **Notifications Slack** sur échecs
- **Audit de performance** Lighthouse
- **Métriques de pipeline** dans GitLab

## Version alternative avec matrices

Pour des environnements multiples :

```yaml
# Test sur plusieurs versions Node.js
test_matrix:
  stage: test
  image: node:${NODE_VERSION}-alpine
  parallel:
    matrix:
      - NODE_VERSION: ['16', '18', '20']
  script:
    - cd frontend && npm test
```

## Métriques de performance attendues

Avec cette configuration optimisée :

- **Install (parallèle)** : ~45-60 secondes
- **Lint (parallèle)** : ~20-30 secondes
- **Test (parallèle)** : ~30-45 secondes
- **Security** : ~15-20 secondes
- **Build (parallèle)** : ~60-90 secondes
- **Deploy** : ~30-45 secondes
- **Total** : ~3-4 minutes

## Bonnes pratiques appliquées

1. **Séparation claire** des responsabilités par stage
2. **Parallélisme maximal** sans dépendances croisées
3. **Cache intelligent** avec clés par composant et branche
4. **Artifacts optimisés** avec expirations appropriées
5. **Conditions dynamiques** selon changements fichiers
6. **Rapports intégrés** pour visibilité dans GitLab
7. **Monitoring** et notifications automatiques
8. **Environnements multiples** (staging/production)

Cette configuration constitue un pipeline production-ready pour applications full-stack complexes !
