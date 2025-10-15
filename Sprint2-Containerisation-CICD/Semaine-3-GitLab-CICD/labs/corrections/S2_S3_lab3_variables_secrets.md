# LAB 3 - CORRECTIONS : Variables et Secrets GitLab

## Solution complète

### Configuration des variables GitLab

#### 1. Variables générales du projet

```bash
# Variables publiques (non protégées)
APP_NAME = "demo-react-app"
APP_VERSION = "1.0.0"
NODE_ENV = "production"
BUILD_NUMBER = "${CI_PIPELINE_ID}"

# Variables par environnement
API_URL_DEV = "https://api-dev.example.com"
API_URL_STAGING = "https://api-staging.example.com"
API_URL_PROD = "https://api.example.com"
```

#### 2. Secrets (variables protégées et masquées)

```bash
# Secrets avec Protected=true et Masked=true
DATABASE_PASSWORD = "super_secret_password"
JWT_SECRET = "jwt_secret_key_here"
API_TOKEN = "api_token_here"
```

### Pipeline .gitlab-ci.yml optimisé

```yaml
# Pipeline avec gestion complète des variables et secrets
image: node:18-alpine

# Variables globales du pipeline
variables:
  npm_config_cache: '$CI_PROJECT_DIR/.npm'
  REACT_APP_VERSION: '$APP_VERSION'
  REACT_APP_BUILD: '$BUILD_NUMBER'
  # Variables pour optimisation
  YARN_CACHE_FOLDER: '$CI_PROJECT_DIR/.yarn'
  CI: 'true'

stages:
  - validate
  - install
  - build
  - test
  - deploy

# Cache global optimisé
cache:
  key: ${CI_COMMIT_REF_SLUG}-${CI_PROJECT_ID}
  paths:
    - node_modules/
    - .npm/
    - .yarn/

# Job de validation des variables
validate_environment:
  stage: validate
  script:
    - echo "🔍 === VALIDATION DES VARIABLES D'ENVIRONNEMENT ==="
    - echo "📦 Application: $APP_NAME"
    - echo "🏷️  Version: $APP_VERSION"
    - echo "🌍 Environment: $NODE_ENV"
    - echo "🔢 Build Number: $BUILD_NUMBER"
    - echo "🔀 Branch: $CI_COMMIT_REF_NAME"
    - echo "📝 Commit: ${CI_COMMIT_SHA:0:8}"
    - echo "👤 Triggered by: $GITLAB_USER_LOGIN"
    - echo ""
    - echo "🔧 === VARIABLES SYSTÈME GITLAB ==="
    - echo "Pipeline ID: $CI_PIPELINE_ID"
    - echo "Job ID: $CI_JOB_ID"
    - echo "Runner: $CI_RUNNER_DESCRIPTION"
    - echo ""
    - echo "✅ === VALIDATION DES VARIABLES CRITIQUES ==="
    - |
      # Validation des variables obligatoires
      errors=0

      if [ -z "$APP_NAME" ]; then
        echo "❌ Erreur: APP_NAME non défini"
        errors=$((errors + 1))
      else
        echo "✅ APP_NAME défini: $APP_NAME"
      fi

      if [ -z "$APP_VERSION" ]; then
        echo "❌ Erreur: APP_VERSION non défini"
        errors=$((errors + 1))
      else
        echo "✅ APP_VERSION défini: $APP_VERSION"
      fi

      # Validation des secrets (vérifier existence sans exposer)
      if [ -z "$API_TOKEN" ]; then
        echo "❌ Erreur: API_TOKEN non défini"
        errors=$((errors + 1))
      else
        echo "✅ API_TOKEN défini (longueur: ${#API_TOKEN} caractères)"
      fi

      if [ $errors -gt 0 ]; then
        echo "❌ $errors erreur(s) détectée(s)"
        exit 1
      fi
    - echo "✅ Toutes les variables sont correctement définies"
  only:
    - main
    - develop
    - merge_requests
    - tags

# Installation avec gestion d'erreur
install_dependencies:
  stage: install
  before_script:
    - echo "🔧 === INSTALLATION DÉPENDANCES POUR $APP_NAME v$APP_VERSION ==="
    - echo "🐳 Image utilisée: $CI_JOB_IMAGE"
    - echo "📁 Répertoire de travail: $CI_PROJECT_DIR"
    - node --version
    - npm --version
  script:
    - echo "📦 Installation des dépendances npm"
    - npm ci --cache .npm --prefer-offline --no-audit
    - echo "📊 Analyse des dépendances installées"
    - npm list --depth=0 || echo "⚠️ Certaines dépendances optionnelles peuvent manquer"
    - echo "💾 Taille node_modules: $(du -sh node_modules/ | cut -f1)"
    - echo "✅ Installation terminée avec succès"
  artifacts:
    paths:
      - node_modules/
    expire_in: 2 hours
    reports:
      dependency_scanning: gl-dependency-scanning-report.json
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  only:
    - main
    - develop
    - merge_requests
    - tags

# Build avec variables d'environnement personnalisées
build_application:
  stage: build
  before_script:
    - echo "🏗️ === BUILD DE $APP_NAME POUR $NODE_ENV ==="
    - echo "📋 Configuration du build"
  script:
    - echo "📝 Création du fichier .env.production"
    - |
      cat > .env.production << EOF
      # Variables d'environnement pour le build
      REACT_APP_NAME=$APP_NAME
      REACT_APP_VERSION=$APP_VERSION
      REACT_APP_BUILD=$BUILD_NUMBER
      REACT_APP_ENV=$NODE_ENV
      REACT_APP_COMMIT_SHA=${CI_COMMIT_SHA:0:8}
      REACT_APP_BRANCH=$CI_COMMIT_REF_NAME
      REACT_APP_PIPELINE_URL=$CI_PIPELINE_URL
      # Timestamp de build
      REACT_APP_BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
      EOF
    - echo "📄 Contenu du fichier .env.production:"
    - cat .env.production
    - echo ""
    - echo "🔨 Lancement du build React"
    - npm run build
    - echo ""
    - echo "📊 Analyse du build généré"
    - ls -la build/
    - echo "💾 Taille du build: $(du -sh build/ | cut -f1)"
    - echo "📁 Contenu détaillé:"
    - find build/ -name "*.js" -o -name "*.css" | head -10
    - echo "✅ Build terminé avec succès"
  artifacts:
    paths:
      - build/
      - .env.production
    expire_in: 1 day
    reports:
      size_report: size-report.json
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests
    - tags

# Tests avec variables de test
test_application:
  stage: test
  variables:
    NODE_ENV: 'test'
    CI: 'true'
  before_script:
    - echo "🧪 === TESTS POUR $APP_NAME EN MODE $NODE_ENV ==="
  script:
    - echo "🔬 Configuration de l'environnement de test"
    - echo "NODE_ENV=$NODE_ENV"
    - echo "CI=$CI"
    - echo ""
    - echo "🏃 Exécution des tests unitaires"
    - npm test -- --coverage --watchAll=false --verbose
    - echo ""
    - echo "📊 Analyse de la couverture"
    - ls -la coverage/
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: coverage/junit.xml
    paths:
      - coverage/
    expire_in: 1 week
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests
    - tags

# Déploiement Development
deploy_dev:
  stage: deploy
  variables:
    API_URL: '$API_URL_DEV'
    DEPLOY_ENV: 'development'
    DEBUG: 'true'
  before_script:
    - echo "🚀 === DÉPLOIEMENT DEV DE $APP_NAME ==="
    - echo "🎯 Environnement cible: $DEPLOY_ENV"
  script:
    - echo "🌐 Configuration API: $API_URL"
    - echo "🔐 Token API: ${API_TOKEN:0:8}... (masqué pour sécurité)"
    - echo "🐛 Debug activé: $DEBUG"
    - echo ""
    - echo "📝 Génération du fichier de configuration"
    - |
      cat > deploy-config.json << EOF
      {
        "application": {
          "name": "$APP_NAME",
          "version": "$APP_VERSION",
          "build": "$BUILD_NUMBER",
          "commit": "${CI_COMMIT_SHA:0:8}",
          "branch": "$CI_COMMIT_REF_NAME"
        },
        "environment": {
          "name": "$DEPLOY_ENV",
          "api_url": "$API_URL",
          "debug": $DEBUG
        },
        "deployment": {
          "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
          "pipeline_url": "$CI_PIPELINE_URL",
          "triggered_by": "$GITLAB_USER_LOGIN"
        }
      }
      EOF
    - echo "📄 Configuration générée:"
    - cat deploy-config.json | jq '.'
    - echo ""
    - echo "🚢 Simulation du déploiement"
    - echo "✅ Déploiement DEV simulé avec succès"
  environment:
    name: development
    url: https://dev-demo-react-app.example.com
    deployment_tier: development
  artifacts:
    paths:
      - deploy-config.json
    expire_in: 1 week
  dependencies:
    - build_application
  only:
    - develop
  when: on_success

# Déploiement Staging
deploy_staging:
  stage: deploy
  variables:
    API_URL: '$API_URL_STAGING'
    DEPLOY_ENV: 'staging'
    DEBUG: 'false'
  before_script:
    - echo "🚀 === DÉPLOIEMENT STAGING DE $APP_NAME ==="
    - echo "🎯 Environnement cible: $DEPLOY_ENV"
  script:
    - echo "🌐 Configuration API: $API_URL"
    - echo "🔐 Token API: ${API_TOKEN:0:8}... (masqué pour sécurité)"
    - echo ""
    - echo "🔒 Vérification des prérequis de sécurité"
    - |
      if [ "$CI_COMMIT_REF_NAME" != "main" ]; then
        echo "⚠️ Avertissement: Déploiement staging depuis une branche non-main"
      fi
    - echo ""
    - echo "📝 Génération du fichier de configuration staging"
    - |
      cat > deploy-config.json << EOF
      {
        "application": {
          "name": "$APP_NAME",
          "version": "$APP_VERSION",
          "build": "$BUILD_NUMBER",
          "commit": "${CI_COMMIT_SHA:0:8}",
          "branch": "$CI_COMMIT_REF_NAME"
        },
        "environment": {
          "name": "$DEPLOY_ENV",
          "api_url": "$API_URL",
          "debug": $DEBUG
        },
        "security": {
          "jwt_configured": true,
          "db_connected": true,
          "ssl_enabled": true
        },
        "deployment": {
          "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
          "pipeline_url": "$CI_PIPELINE_URL",
          "triggered_by": "$GITLAB_USER_LOGIN"
        }
      }
      EOF
    - echo "📄 Configuration générée:"
    - cat deploy-config.json | jq '.'
    - echo ""
    - echo "🚢 Simulation du déploiement staging"
    - echo "✅ Déploiement STAGING simulé avec succès"
  environment:
    name: staging
    url: https://staging-demo-react-app.example.com
    deployment_tier: staging
  artifacts:
    paths:
      - deploy-config.json
    expire_in: 1 week
  dependencies:
    - build_application
  only:
    - main
  when: manual

# Déploiement Production
deploy_production:
  stage: deploy
  variables:
    API_URL: '$API_URL_PROD'
    DEPLOY_ENV: 'production'
    DEBUG: 'false'
  before_script:
    - echo "🚀 === DÉPLOIEMENT PRODUCTION DE $APP_NAME ==="
    - echo "🎯 Environnement cible: $DEPLOY_ENV"
    - echo "⚠️ ATTENTION: Déploiement en production"
  script:
    - echo "🌐 Configuration API: $API_URL"
    - echo "🔐 Token API: ${API_TOKEN:0:8}... (masqué pour sécurité)"
    - echo ""
    - echo "🔒 Validation stricte des secrets de production"
    - |
      errors=0

      if [ -z "$DATABASE_PASSWORD" ]; then
        echo "❌ Erreur: DATABASE_PASSWORD manquant"
        errors=$((errors + 1))
      else
        echo "✅ DATABASE_PASSWORD configuré (longueur: ${#DATABASE_PASSWORD})"
      fi

      if [ -z "$JWT_SECRET" ]; then
        echo "❌ Erreur: JWT_SECRET manquant"
        errors=$((errors + 1))
      else
        echo "✅ JWT_SECRET configuré (longueur: ${#JWT_SECRET})"
      fi

      if [ -z "$API_TOKEN" ]; then
        echo "❌ Erreur: API_TOKEN manquant"
        errors=$((errors + 1))
      else
        echo "✅ API_TOKEN configuré (longueur: ${#API_TOKEN})"
      fi

      if [ $errors -gt 0 ]; then
        echo "❌ $errors secret(s) manquant(s) - Arrêt du déploiement"
        exit 1
      fi
    - echo "✅ Tous les secrets sont configurés"
    - echo ""
    - echo "📝 Génération du fichier de configuration production"
    - |
      cat > deploy-config.json << EOF
      {
        "application": {
          "name": "$APP_NAME",
          "version": "$APP_VERSION",
          "build": "$BUILD_NUMBER",
          "commit": "${CI_COMMIT_SHA:0:8}",
          "branch": "$CI_COMMIT_REF_NAME"
        },
        "environment": {
          "name": "$DEPLOY_ENV",
          "api_url": "$API_URL",
          "debug": $DEBUG
        },
        "security": {
          "jwt_configured": true,
          "db_connected": true,
          "ssl_enabled": true,
          "encryption": true,
          "audit_logging": true
        },
        "deployment": {
          "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
          "pipeline_url": "$CI_PIPELINE_URL",
          "triggered_by": "$GITLAB_USER_LOGIN",
          "approval_required": true
        }
      }
      EOF
    - echo "📄 Configuration générée:"
    - cat deploy-config.json | jq '.'
    - echo ""
    - echo "🚢 Simulation du déploiement production"
    - sleep 5 # Simulation du temps de déploiement
    - echo "✅ Déploiement PRODUCTION simulé avec succès"
  environment:
    name: production
    url: https://demo-react-app.example.com
    deployment_tier: production
  artifacts:
    paths:
      - deploy-config.json
    expire_in: 1 month
  dependencies:
    - build_application
  only:
    - main
  when: manual
  allow_failure: false
```

## Explications détaillées

### 1. Hiérarchie des variables GitLab

**Ordre de priorité** (du plus prioritaire au moins prioritaire) :

1. Variables définies dans le job
2. Variables définies au niveau du pipeline
3. Variables définies au niveau du projet
4. Variables définies au niveau du groupe
5. Variables définies au niveau de l'instance

### 2. Types de variables GitLab

#### Variables publiques

```yaml
# Visibles dans les logs
APP_NAME = "demo-react-app"
APP_VERSION = "1.0.0"
NODE_ENV = "production"
```

#### Variables protégées

```yaml
# Seulement disponibles sur branches/tags protégés
DATABASE_PASSWORD = "secret" # Protected: ✓
```

#### Variables masquées

```yaml
# Cachées dans les logs (remplacées par [MASKED])
API_TOKEN = "token123" # Masked: ✓
```

#### Variables protégées ET masquées

```yaml
# Maximum de sécurité
JWT_SECRET = "jwt_secret" # Protected: ✓, Masked: ✓
```

### 3. Variables prédéfinies GitLab utilisées

**Variables système** :

- `CI_COMMIT_SHA` : Hash du commit
- `CI_COMMIT_REF_NAME` : Nom de la branche/tag
- `CI_PIPELINE_ID` : ID unique du pipeline
- `CI_JOB_ID` : ID unique du job
- `CI_PROJECT_DIR` : Répertoire de travail
- `CI_PIPELINE_URL` : URL du pipeline
- `GITLAB_USER_LOGIN` : Utilisateur qui a déclenché

**Variables d'environnement** :

- `CI_JOB_IMAGE` : Image Docker utilisée
- `CI_RUNNER_DESCRIPTION` : Description du runner

### 4. Techniques de sécurisation

#### Masquage partiel des secrets

```bash
echo "Token: ${API_TOKEN:0:8}..."  # Affiche seulement 8 premiers caractères
echo "Password length: ${#DATABASE_PASSWORD}"  # Affiche la longueur
```

#### Validation des secrets

```bash
if [ -z "$SECRET_VAR" ]; then
  echo "❌ Secret manquant"
  exit 1
fi
```

#### Éviter l'exposition accidentelle

```bash
# ❌ MAUVAIS - expose le secret
echo "Password is: $DATABASE_PASSWORD"

# ✅ BON - confirme la présence sans exposer
echo "Password configured: $([ -n "$DATABASE_PASSWORD" ] && echo "✅" || echo "❌")"
```

### 5. Configuration par environnement

#### Structure recommandée

```bash
# Variables générales
APP_NAME = "demo-react-app"
APP_VERSION = "1.0.0"

# Variables par environnement
API_URL_DEV = "https://api-dev.example.com"
API_URL_STAGING = "https://api-staging.example.com"
API_URL_PROD = "https://api.example.com"

# Secrets par environnement (si nécessaire)
DB_PASSWORD_DEV = "dev_password"
DB_PASSWORD_PROD = "prod_password"  # Protected + Masked
```

#### Utilisation dans le pipeline

```yaml
deploy_dev:
  variables:
    API_URL: '$API_URL_DEV'
    DB_PASSWORD: '$DB_PASSWORD_DEV'

deploy_prod:
  variables:
    API_URL: '$API_URL_PROD'
    DB_PASSWORD: '$DB_PASSWORD_PROD'
```

## Bonnes pratiques appliquées

### 1. Nommage des variables

- **Convention** : `PREFIX_COMPONENT_PURPOSE`
- **Exemples** : `APP_NAME`, `API_URL_PROD`, `DB_PASSWORD_STAGING`

### 2. Gestion des secrets

- Toujours utiliser Protected + Masked pour les secrets
- Valider la présence sans exposer la valeur
- Utiliser des variables d'environnement spécifiques

### 3. Documentation et traçabilité

- Logger les variables non-sensibles pour le debug
- Inclure des informations de build (commit, branch, timestamp)
- Générer des fichiers de configuration pour audit

### 4. Validation et sécurité

- Valider la présence des variables critiques
- Implémenter des checks de sécurité par environnement
- Utiliser `allow_failure: false` pour la production

## Problèmes courants et solutions

### 1. Variable non définie

**Symptôme** : Job échoue avec "variable not found"
**Solution** :

```bash
# Vérification avec valeur par défaut
API_URL=${API_URL:-"https://api-default.example.com"}
```

### 2. Secret exposé dans les logs

**Symptôme** : Secret visible en plain text
**Solution** :

- Activer "Masked" pour la variable
- Utiliser des techniques de masquage partiel

### 3. Variable non accessible dans job

**Symptôme** : Variable vide dans certains jobs
**Solution** :

- Vérifier si la variable est "Protected" et la branche protégée
- Définir la variable au bon niveau (job, pipeline, projet)

### 4. Conflits de variables

**Symptôme** : Variable a une valeur inattendue
**Solution** :

- Comprendre la hiérarchie des variables
- Utiliser des noms uniques et explicites

## Métriques et validation

### Sécurité

- ✅ Aucun secret exposé dans les logs
- ✅ Variables protégées seulement sur branches protégées
- ✅ Validation des secrets avant déploiement production

### Configuration

- ✅ Variables spécifiques par environnement
- ✅ Configuration générée automatiquement
- ✅ Traçabilité complète (commit, pipeline, utilisateur)

### Performance

- ✅ Variables mises en cache quand approprié
- ✅ Validation rapide des prérequis
- ✅ Configuration optimisée par environnement
