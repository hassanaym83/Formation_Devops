# LAB 3 - Variables et Secrets GitLab

## Contexte

Votre équipe DevOps développe une application avec plusieurs environnements (dev, staging, production) qui nécessitent des configurations différentes. Vous devez maîtriser la gestion des variables d'environnement et des secrets dans GitLab CI/CD pour sécuriser et optimiser vos déploiements.

## Objectif

Configurer et utiliser les variables d'environnement, les secrets, et les groupes de variables GitLab pour gérer différents environnements de manière sécurisée.

## Prérequis

- Projet GitLab avec pipeline fonctionnel (LAB 2 complété)
- Notions de sécurité DevOps
- Compréhension des environnements de déploiement

## Instructions détaillées

### Étape 1 : Configuration variables projet (10 minutes)

1. **Accéder aux variables** :

   - Dans votre projet GitLab
   - Aller dans Settings → CI/CD
   - Développer la section "Variables"

2. **Créer variables d'environnement** :

   **Variables générales** :

   - `APP_NAME` = `demo-react-app`
   - `APP_VERSION` = `1.0.0`
   - `NODE_ENV` = `production`
   - `BUILD_NUMBER` = `${CI_PIPELINE_ID}`

   **Variables par environnement** :

   - `API_URL_DEV` = `https://api-dev.example.com`
   - `API_URL_STAGING` = `https://api-staging.example.com`
   - `API_URL_PROD` = `https://api.example.com`

3. **Créer secrets (variables protégées)** :
   - `DATABASE_PASSWORD` = `super_secret_password` (Protected: ✓, Masked: ✓)
   - `JWT_SECRET` = `jwt_secret_key_here` (Protected: ✓, Masked: ✓)
   - `API_TOKEN` = `api_token_here` (Protected: ✓, Masked: ✓)

### Étape 2 : Modification du pipeline (15 minutes)

1. **Mettre à jour `.gitlab-ci.yml`** :

```yaml
# Pipeline avec gestion des variables et secrets
image: node:18-alpine

# Variables globales
variables:
  npm_config_cache: '$CI_PROJECT_DIR/.npm'
  REACT_APP_VERSION: '$APP_VERSION'
  REACT_APP_BUILD: '$BUILD_NUMBER'

stages:
  - validate
  - install
  - build
  - test
  - deploy

# Job de validation des variables
validate_environment:
  stage: validate
  script:
    - echo "🔍 Validation des variables d'environnement"
    - echo "APP_NAME = $APP_NAME"
    - echo "APP_VERSION = $APP_VERSION"
    - echo "NODE_ENV = $NODE_ENV"
    - echo "CI_COMMIT_SHA = $CI_COMMIT_SHA"
    - echo "CI_PIPELINE_ID = $CI_PIPELINE_ID"
    - echo "CI_COMMIT_REF_NAME = $CI_COMMIT_REF_NAME"
    - |
      if [ -z "$APP_NAME" ]; then
        echo "❌ Erreur: APP_NAME non défini"
        exit 1
      fi
    - echo "✅ Variables validées"
  only:
    - main
    - develop
    - merge_requests

# Installation avec variables
install_dependencies:
  stage: install
  script:
    - echo "🔧 Installation pour $APP_NAME v$APP_VERSION"
    - npm ci --cache .npm --prefer-offline
    - echo "✅ Dépendances installées"
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
  only:
    - main
    - develop
    - merge_requests

# Build avec variables d'environnement
build_application:
  stage: build
  script:
    - echo "🏗️ Build de $APP_NAME pour l'environnement $NODE_ENV"
    - echo "REACT_APP_VERSION=$REACT_APP_VERSION" > .env.production
    - echo "REACT_APP_BUILD=$REACT_APP_BUILD" >> .env.production
    - echo "REACT_APP_ENV=$NODE_ENV" >> .env.production
    - cat .env.production
    - npm run build
    - echo "✅ Build terminé"
    - ls -la build/
  artifacts:
    paths:
      - build/
      - .env.production
    expire_in: 1 day
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests

# Tests avec configuration
test_application:
  stage: test
  variables:
    NODE_ENV: 'test'
  script:
    - echo "🧪 Tests pour $APP_NAME en mode $NODE_ENV"
    - npm test -- --coverage --watchAll=false
    - echo "✅ Tests terminés"
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 week
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests

# Déploiement DEV
deploy_dev:
  stage: deploy
  variables:
    API_URL: '$API_URL_DEV'
    DEPLOY_ENV: 'development'
  script:
    - echo "🚀 Déploiement DEV de $APP_NAME"
    - echo "🌐 API URL: $API_URL"
    - echo "🔐 Token: ${API_TOKEN:0:8}..." # Affiche seulement les 8 premiers caractères
    - echo "📝 Création fichier de configuration"
    - |
      cat > deploy-config.json << EOF
      {
        "app": "$APP_NAME",
        "version": "$APP_VERSION",
        "environment": "$DEPLOY_ENV",
        "api_url": "$API_URL",
        "build": "$BUILD_NUMBER"
      }
      EOF
    - cat deploy-config.json
    - echo "✅ Déploiement DEV simulé"
  environment:
    name: development
    url: https://dev-demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - develop
  when: on_success

# Déploiement STAGING
deploy_staging:
  stage: deploy
  variables:
    API_URL: '$API_URL_STAGING'
    DEPLOY_ENV: 'staging'
  script:
    - echo "🚀 Déploiement STAGING de $APP_NAME"
    - echo "🌐 API URL: $API_URL"
    - echo "🔐 Token: ${API_TOKEN:0:8}..."
    - echo "📝 Création fichier de configuration"
    - |
      cat > deploy-config.json << EOF
      {
        "app": "$APP_NAME",
        "version": "$APP_VERSION",
        "environment": "$DEPLOY_ENV",
        "api_url": "$API_URL",
        "build": "$BUILD_NUMBER",
        "security": {
          "jwt_configured": true,
          "db_connected": true
        }
      }
      EOF
    - cat deploy-config.json
    - echo "✅ Déploiement STAGING simulé"
  environment:
    name: staging
    url: https://staging-demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - main
  when: manual

# Déploiement PRODUCTION
deploy_production:
  stage: deploy
  variables:
    API_URL: '$API_URL_PROD'
    DEPLOY_ENV: 'production'
  script:
    - echo "🚀 Déploiement PRODUCTION de $APP_NAME"
    - echo "🌐 API URL: $API_URL"
    - echo "🔐 Token: ${API_TOKEN:0:8}..."
    - echo "🔒 Vérification des secrets"
    - |
      if [ -z "$DATABASE_PASSWORD" ] || [ -z "$JWT_SECRET" ]; then
        echo "❌ Erreur: Secrets manquants"
        exit 1
      fi
    - echo "✅ Secrets validés"
    - echo "📝 Création fichier de configuration production"
    - |
      cat > deploy-config.json << EOF
      {
        "app": "$APP_NAME",
        "version": "$APP_VERSION",
        "environment": "$DEPLOY_ENV",
        "api_url": "$API_URL",
        "build": "$BUILD_NUMBER",
        "security": {
          "jwt_configured": true,
          "db_connected": true,
          "encryption": true
        }
      }
      EOF
    - cat deploy-config.json
    - echo "✅ Déploiement PRODUCTION simulé"
  environment:
    name: production
    url: https://demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - main
  when: manual
  allow_failure: false
```

### Étape 3 : Test et validation (5 minutes)

1. **Commit et push** :

   - Message : "Add environment variables and secrets management"
   - Push vers develop puis main

2. **Vérifier le pipeline** :

   - Observer le job `validate_environment`
   - Contrôler que les variables sont bien affichées
   - Vérifier que les secrets sont masqués dans les logs

3. **Tester les déploiements** :
   - Déclencher deploy_dev sur develop
   - Déclencher deploy_staging sur main
   - Analyser les différentes configurations générées

## Livrables attendus

### 1. Configuration des variables

Capture d'écran de :

- Variables du projet avec APP_NAME, APP_VERSION, etc.
- Variables d'environnement (API*URL*\*)
- Secrets protégés et masqués

### 2. Pipeline fonctionnel

- Job validate_environment qui affiche les variables
- Builds différenciés par environnement
- Déploiements avec configurations spécifiques

### 3. Document d'analyse

Créer `variables_analysis.md` avec :

- Liste complète des variables utilisées
- Stratégie de gestion des secrets
- Différences entre environnements
- Bonnes pratiques appliquées

## Critères d'évaluation

**Total : 20 points**

- **Configuration variables (8 points)** : Toutes les variables créées et configurées
- **Secrets sécurisés (5 points)** : Protected et Masked correctement
- **Pipeline adapté (5 points)** : Jobs utilisent les variables appropriées
- **Documentation (2 points)** : Analyse complète des variables

## Durée estimée

**30 minutes** réparties :

- Configuration variables : 10 minutes
- Modification pipeline : 15 minutes
- Test et validation : 5 minutes

## Conseils

- Ne jamais exposer de vrais secrets dans les logs
- Utiliser les variables prédéfinies GitLab (CI\_\*)
- Tester la hiérarchie des variables (projet > groupe > instance)
- Documenter les variables pour l'équipe

## Bonnes pratiques à retenir

1. **Nommage cohérent** : PREFIX_COMPONENT_PURPOSE
2. **Variables par environnement** : API_URL_DEV, API_URL_PROD
3. **Secrets protégés** : Toujours Protected + Masked
4. **Validation** : Vérifier la présence des variables critiques
5. **Documentation** : Maintenir la liste des variables à jour

## Ressources

- [GitLab CI/CD Variables](https://docs.gitlab.com/ee/ci/variables/)
- [Predefined Variables](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
- [Protected Variables](https://docs.gitlab.com/ee/ci/variables/#protected-cicd-variables)
