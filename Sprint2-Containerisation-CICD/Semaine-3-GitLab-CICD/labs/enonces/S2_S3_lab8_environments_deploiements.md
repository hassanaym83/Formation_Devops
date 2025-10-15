# LAB 8 - ÉNONCÉ : Environments et Déploiements

## Objectifs pédagogiques

À la fin de ce lab, vous serez capable de :

- Configurer des environnements multiples (dev, staging, production)
- Implémenter des stratégies de déploiement avancées (blue-green, canary, rolling)
- Gérer les variables d'environnement par contexte
- Mettre en place des approbations manuelles et automatiques
- Configurer des politiques de déploiement et rollback

## Contexte du lab

La gestion des environnements est cruciale pour :

- **Isolation** : Séparer les phases de développement, test et production
- **Validation** : Tester les changements avant la mise en production
- **Sécurité** : Contrôler l'accès et les déploiements selon les environnements
- **Fiabilité** : Minimiser les risques avec des stratégies de déploiement appropriées

## Prérequis

- LAB 7 terminé (monitoring et métriques)
- Application React avec pipeline GitLab CI/CD
- Accès administrateur à GitLab
- Connaissances des concepts de déploiement

## Architecture multi-environnements

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Development    │────│    Staging      │────│   Production    │
│   (feature)     │    │   (pre-prod)    │    │    (main)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌─────────────────┐             │
         └───────────────│  Review Apps    │─────────────┘
                         │  (dynamiques)   │
                         └─────────────────┘
```

## Exercice 1 : Configuration des environnements GitLab (25 points)

### 1.1 Création des environnements

**Votre tâche : Configurer 4 environnements dans GitLab**

1. **Environment Development**

   - Nom : `development`
   - URL externe : `https://dev-react-app.example.com`
   - Déploiement automatique depuis : `develop`

2. **Environment Staging**

   - Nom : `staging`
   - URL externe : `https://staging-react-app.example.com`
   - Déploiement automatique depuis : `main`
   - Protection : Approbation requise

3. **Environment Production**

   - Nom : `production`
   - URL externe : `https://react-app.example.com`
   - Déploiement manuel uniquement
   - Protection : Approbation de 2 personnes + délai de 24h

4. **Environment Review**
   - Nom : `review/$CI_MERGE_REQUEST_IID`
   - URL externe : `https://review-$CI_MERGE_REQUEST_IID.example.com`
   - Déploiement automatique pour les MR
   - Nettoyage automatique après merge

### 1.2 Configuration des variables par environnement

**Créer le fichier `environments/variables.yml`** :

```yaml
# Votre tâche : Configurer les variables par environnement

# Variables communes
common_variables:
  # Application
  # APP_NAME: "react-devops-app"
  # APP_VERSION: "${CI_COMMIT_TAG:-${CI_COMMIT_SHORT_SHA}}"
  # NODE_ENV: sera défini par environnement

  # Build
  # BUILD_PATH: "./build"
  # PUBLIC_URL: sera défini par environnement

  # Monitoring
  # MONITORING_ENABLED: "true"
  # METRICS_ENDPOINT: "/metrics"

# Variables spécifiques par environnement
environments:
  development:
    # NODE_ENV: "development"
    # PUBLIC_URL: "https://dev-react-app.example.com"
    # API_BASE_URL: "https://api-dev.example.com"
    # DATABASE_URL: "postgresql://dev-db.example.com:5432/app_dev"
    # REDIS_URL: "redis://dev-redis.example.com:6379"
    # DEBUG_MODE: "true"
    # LOG_LEVEL: "debug"
    # CACHE_TTL: "60"
    # RATE_LIMIT: "1000"

  staging:
    # NODE_ENV: "staging"
    # PUBLIC_URL: "https://staging-react-app.example.com"
    # API_BASE_URL: "https://api-staging.example.com"
    # DATABASE_URL: "postgresql://staging-db.example.com:5432/app_staging"
    # REDIS_URL: "redis://staging-redis.example.com:6379"
    # DEBUG_MODE: "false"
    # LOG_LEVEL: "info"
    # CACHE_TTL: "300"
    # RATE_LIMIT: "500"

  production:
    # NODE_ENV: "production"
    # PUBLIC_URL: "https://react-app.example.com"
    # API_BASE_URL: "https://api.example.com"
    # DATABASE_URL: "${PROD_DATABASE_URL}" # Variable protégée
    # REDIS_URL: "${PROD_REDIS_URL}" # Variable protégée
    # DEBUG_MODE: "false"
    # LOG_LEVEL: "warn"
    # CACHE_TTL: "3600"
    # RATE_LIMIT: "100"

# Configuration des secrets par environnement
secrets:
  development:
    # API_SECRET_KEY: "${DEV_API_SECRET}"
    # JWT_SECRET: "${DEV_JWT_SECRET}"
    # ENCRYPTION_KEY: "${DEV_ENCRYPTION_KEY}"

  staging:
    # API_SECRET_KEY: "${STAGING_API_SECRET}"
    # JWT_SECRET: "${STAGING_JWT_SECRET}"
    # ENCRYPTION_KEY: "${STAGING_ENCRYPTION_KEY}"

  production:
    # API_SECRET_KEY: "${PROD_API_SECRET}"
    # JWT_SECRET: "${PROD_JWT_SECRET}"
    # ENCRYPTION_KEY: "${PROD_ENCRYPTION_KEY}"
    # SSL_CERT_PATH: "${PROD_SSL_CERT}"
    # SSL_KEY_PATH: "${PROD_SSL_KEY}"
```

### 1.3 Script de configuration des environnements

**Créer le fichier `scripts/setup-environments.sh`** :

```bash
#!/bin/bash
# Votre tâche : Script pour configurer automatiquement les environnements

set -euo pipefail

# Configuration
GITLAB_URL="${CI_SERVER_URL:-https://gitlab.example.com}"
PROJECT_ID="${CI_PROJECT_ID:-}"
GITLAB_TOKEN="${GITLAB_TOKEN:-}"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Fonction pour créer un environnement
create_environment() {
    local env_name="$1"
    local external_url="$2"
    local auto_stop_in="$3"

    log_info "Création de l'environnement: $env_name"

    # Données de l'environnement
    # local env_data='{
    #   "name": "'$env_name'",
    #   "external_url": "'$external_url'",
    #   "auto_stop_in": '$auto_stop_in'
    # }'

    # Créer l'environnement via API GitLab
    # curl -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/environments" \
    #   --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
    #   --header "Content-Type: application/json" \
    #   --data "$env_data" || log_warn "Environnement $env_name existe déjà"
}

# Fonction pour configurer les variables d'environnement
setup_environment_variables() {
    local env_name="$1"

    log_info "Configuration des variables pour: $env_name"

    # Lire les variables depuis le fichier YAML (simulation)
    case "$env_name" in
        "development")
            # set_variable "NODE_ENV" "development" "$env_name"
            # set_variable "API_BASE_URL" "https://api-dev.example.com" "$env_name"
            ;;
        "staging")
            # set_variable "NODE_ENV" "staging" "$env_name"
            # set_variable "API_BASE_URL" "https://api-staging.example.com" "$env_name"
            ;;
        "production")
            # set_variable "NODE_ENV" "production" "$env_name"
            # set_variable "API_BASE_URL" "https://api.example.com" "$env_name"
            ;;
    esac
}

# Fonction pour définir une variable
set_variable() {
    local key="$1"
    local value="$2"
    local environment="$3"

    # local var_data='{
    #   "key": "'$key'",
    #   "value": "'$value'",
    #   "environment_scope": "'$environment'"
    # }'

    # curl -X POST "${GITLAB_URL}/api/v4/projects/${PROJECT_ID}/variables" \
    #   --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
    #   --header "Content-Type: application/json" \
    #   --data "$var_data" || echo "Variable $key existe déjà"
}

# Fonction pour configurer les règles de protection
setup_protection_rules() {
    local env_name="$1"

    log_info "Configuration des règles de protection pour: $env_name"

    case "$env_name" in
        "production")
            # Configuration protection production
            # - Approbation de 2 personnes
            # - Délai de 24h
            # - Restriction aux mainteneurs
            ;;
        "staging")
            # Configuration protection staging
            # - Approbation de 1 personne
            # - Restriction aux développeurs+
            ;;
    esac
}

# Fonction principale
main() {
    log_info "=== CONFIGURATION DES ENVIRONNEMENTS ==="

    # Vérifier les prérequis
    if [[ -z "$GITLAB_TOKEN" ]]; then
        log_error "GITLAB_TOKEN non défini"
        exit 1
    fi

    if [[ -z "$PROJECT_ID" ]]; then
        log_error "PROJECT_ID non défini"
        exit 1
    fi

    # Créer les environnements
    # create_environment "development" "https://dev-react-app.example.com" "null"
    # create_environment "staging" "https://staging-react-app.example.com" "null"
    # create_environment "production" "https://react-app.example.com" "null"

    # Configurer les variables
    # setup_environment_variables "development"
    # setup_environment_variables "staging"
    # setup_environment_variables "production"

    # Configurer les protections
    # setup_protection_rules "staging"
    # setup_protection_rules "production"

    log_info "Configuration des environnements terminée"
}

# Exécution du script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

## Exercice 2 : Stratégies de déploiement avancées (30 points)

### 2.1 Déploiement Blue-Green

**Créer le fichier `deployment/blue-green.yml`** :

```yaml
# Votre tâche : Configurer le déploiement Blue-Green

# Configuration Blue-Green
blue_green:
  # Environnements
  environments:
    blue:
      # name: "production-blue"
      # url: "https://blue.react-app.example.com"
      # weight: 0  # Trafic initial
    green:
      # name: "production-green"
      # url: "https://green.react-app.example.com"
      # weight: 100  # Tout le trafic

  # Load Balancer
  load_balancer:
    # type: "nginx"
    # config_path: "/etc/nginx/conf.d/app.conf"
    # health_check_path: "/health"
    # health_check_interval: "10s"

  # Stratégie de switch
  switch_strategy:
    # validation:
    #   - health_check
    #   - smoke_tests
    #   - performance_tests
    # rollback_triggers:
    #   - health_check_failure
    #   - error_rate_threshold: 0.05
    #   - response_time_threshold: 2000
    # switch_duration: "5m"

# Jobs GitLab CI pour Blue-Green
jobs:
  deploy_blue:
    # stage: deploy
    # environment: production-blue
    # script: déployer sur l'environnement blue
    # when: manual

  deploy_green:
    # stage: deploy
    # environment: production-green
    # script: déployer sur l'environnement green
    # when: manual

  switch_traffic:
    # stage: switch
    # script: basculer le trafic du load balancer
    # when: manual
    # dependencies: [deploy_blue, deploy_green]

  rollback:
    # stage: rollback
    # script: revenir à l'environnement précédent
    # when: manual
```

### 2.2 Déploiement Canary

**Créer le fichier `deployment/canary.yml`** :

```yaml
# Votre tâche : Configurer le déploiement Canary

canary:
  # Phases de déploiement Canary
  phases:
    phase_1:
      # traffic_percentage: 5
      # duration: "10m"
      # success_criteria:
      #   - error_rate < 0.01
      #   - response_time_p95 < 1500
      #   - cpu_usage < 70%

    phase_2:
      # traffic_percentage: 25
      # duration: "20m"
      # success_criteria:
      #   - error_rate < 0.005
      #   - response_time_p95 < 1000
      #   - memory_usage < 80%

    phase_3:
      # traffic_percentage: 50
      # duration: "30m"
      # success_criteria:
      #   - error_rate < 0.002
      #   - response_time_p95 < 800
      #   - user_satisfaction > 4.0

    phase_4:
      # traffic_percentage: 100
      # duration: "60m"
      # success_criteria:
      #   - error_rate < 0.001
      #   - all_health_checks_pass: true

  # Métriques de surveillance
  monitoring:
    # metrics:
    #   - name: "error_rate"
    #     query: "rate(http_requests_total{status=~\"5..\"}[5m])"
    #     threshold: 0.01
    #   - name: "response_time_p95"
    #     query: "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
    #     threshold: 1.5
    #   - name: "cpu_usage"
    #     query: "rate(container_cpu_usage_seconds_total[5m]) * 100"
    #     threshold: 70

  # Configuration de rollback automatique
  rollback:
    # triggers:
    #   - metric_threshold_exceeded
    #   - health_check_failure
    #   - manual_trigger
    # max_rollback_time: "5m"
    # notification_channels:
    #   - email: "devops@example.com"
    #   - slack: "#alerts"
```

### 2.3 Déploiement Rolling

**Créer le fichier `deployment/rolling.yml`** :

```yaml
# Votre tâche : Configurer le déploiement Rolling

rolling:
  # Configuration Rolling Update
  strategy:
    # max_unavailable: "25%"  # Maximum d'instances indisponibles
    # max_surge: "25%"        # Maximum d'instances supplémentaires
    # batch_size: 2           # Nombre d'instances par batch
    # batch_interval: "30s"   # Délai entre les batches

  # Phases de déploiement
  phases:
    preparation:
      # - validate_deployment_config
      # - check_resource_availability
      # - backup_current_version

    rolling_update:
      # - update_batch_1
      # - health_check_batch_1
      # - update_batch_2
      # - health_check_batch_2
      # - continue_until_complete

    verification:
      # - full_health_check
      # - smoke_tests
      # - performance_validation

  # Health checks
  health_checks:
    # readiness_probe:
    #   path: "/ready"
    #   interval: "10s"
    #   timeout: "5s"
    #   failure_threshold: 3
    # liveness_probe:
    #   path: "/health"
    #   interval: "30s"
    #   timeout: "10s"
    #   failure_threshold: 3
```

## Exercice 3 : Pipeline multi-environnements (25 points)

### 3.1 Pipeline principal avec environnements

**Modifier `.gitlab-ci.yml` pour les environnements** :

```yaml
# Votre tâche : Configurer le pipeline multi-environnements

# Include des stratégies de déploiement
include:
  - local: 'deployment/blue-green.yml'
  - local: 'deployment/canary.yml'
  - local: 'deployment/rolling.yml'

# Variables globales
variables:
  # Configuration générale
  # DOCKER_REGISTRY: "${CI_REGISTRY}"
  # IMAGE_NAME: "${CI_REGISTRY_IMAGE}/react-app"
  # DEPLOYMENT_STRATEGY: "rolling"  # blue-green, canary, rolling

# Stages avec environnements
stages:
  - validate
  - build
  - test
  - security
  - deploy-dev
  - deploy-staging
  - deploy-production
  - post-deploy

# Templates pour les déploiements
.deploy_template: &deploy_template
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - apk add --no-cache curl jq

# === DÉPLOIEMENT DEVELOPMENT ===
deploy_development:
  <<: *deploy_template
  stage: deploy-dev
  script:
    - echo "=== DÉPLOIEMENT DEVELOPMENT ==="

    # Configuration des variables d'environnement
    - export NODE_ENV="development"
    - export API_BASE_URL="https://api-dev.example.com"
    - export PUBLIC_URL="https://dev-react-app.example.com"

    # Déploiement de l'image
    - IMAGE_TAG="${CI_COMMIT_SHORT_SHA}"
    - docker pull "${IMAGE_NAME}:${IMAGE_TAG}"

    # Simulation du déploiement
    - |
      echo "Déploiement sur l'environnement development"
      echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
      echo "URL: ${PUBLIC_URL}"

      # Ici vous ajouteriez les commandes de déploiement réelles
      # Par exemple: kubectl, docker-compose, ansible, etc.

    # Validation du déploiement
    - |
      echo "Validation du déploiement"
      # curl -f "${PUBLIC_URL}/health" || exit 1
      echo "Déploiement development réussi"

  environment:
    name: development
    url: https://dev-react-app.example.com
    on_stop: stop_development

  only:
    - develop

  artifacts:
    reports:
      deployment: deployment-dev.json
    expire_in: 1 week

# Job d'arrêt development
stop_development:
  <<: *deploy_template
  stage: deploy-dev
  script:
    - echo "Arrêt de l'environnement development"
    # Commandes pour arrêter l'environnement
  environment:
    name: development
    action: stop
  when: manual
  only:
    - develop

# === DÉPLOIEMENT STAGING ===
deploy_staging:
  <<: *deploy_template
  stage: deploy-staging
  script:
    - echo "=== DÉPLOIEMENT STAGING ==="

    # Configuration des variables d'environnement
    - export NODE_ENV="staging"
    - export API_BASE_URL="https://api-staging.example.com"
    - export PUBLIC_URL="https://staging-react-app.example.com"

    # Choix de la stratégie de déploiement
    - |
      case "${DEPLOYMENT_STRATEGY}" in
        "blue-green")
          echo "Déploiement Blue-Green"
          # ./scripts/deploy-blue-green.sh staging
          ;;
        "canary")
          echo "Déploiement Canary"
          # ./scripts/deploy-canary.sh staging
          ;;
        "rolling")
          echo "Déploiement Rolling"
          # ./scripts/deploy-rolling.sh staging
          ;;
        *)
          echo "Déploiement standard"
          ;;
      esac

    # Tests post-déploiement
    - |
      echo "Tests post-déploiement staging"
      # ./scripts/post-deploy-tests.sh staging
      echo "Tests staging réussis"

  environment:
    name: staging
    url: https://staging-react-app.example.com

  only:
    - main

  # Approbation manuelle pour staging
  when: manual

  artifacts:
    reports:
      deployment: deployment-staging.json
    expire_in: 1 month

# === DÉPLOIEMENT PRODUCTION ===
deploy_production:
  <<: *deploy_template
  stage: deploy-production
  script:
    - echo "=== DÉPLOIEMENT PRODUCTION ==="

    # Configuration des variables d'environnement
    - export NODE_ENV="production"
    - export API_BASE_URL="https://api.example.com"
    - export PUBLIC_URL="https://react-app.example.com"

    # Backup avant déploiement
    - |
      echo "Backup de l'environnement production"
      # ./scripts/backup-production.sh

    # Déploiement avec stratégie choisie
    - |
      echo "Déploiement production avec stratégie: ${DEPLOYMENT_STRATEGY}"
      case "${DEPLOYMENT_STRATEGY}" in
        "blue-green")
          # ./scripts/deploy-blue-green.sh production
          ;;
        "canary")
          # ./scripts/deploy-canary.sh production
          ;;
        "rolling")
          # ./scripts/deploy-rolling.sh production
          ;;
      esac

    # Validation critique post-déploiement
    - |
      echo "Validation critique production"
      # ./scripts/production-health-check.sh
      echo "Validation production réussie"

  environment:
    name: production
    url: https://react-app.example.com

  only:
    - main

  # Déploiement manuel uniquement
  when: manual

  # Nécessite l'approbation de staging
  dependencies:
    - deploy_staging

  artifacts:
    reports:
      deployment: deployment-production.json
    expire_in: 6 months

# === REVIEW APPS ===
deploy_review:
  <<: *deploy_template
  stage: deploy-dev
  script:
    - echo "=== DÉPLOIEMENT REVIEW APP ==="

    # Configuration review app
    - export REVIEW_APP_NAME="review-${CI_MERGE_REQUEST_IID}"
    - export REVIEW_URL="https://review-${CI_MERGE_REQUEST_IID}.example.com"

    # Déploiement de la review app
    - |
      echo "Déploiement review app: ${REVIEW_APP_NAME}"
      echo "URL: ${REVIEW_URL}"

      # Commandes de déploiement de la review app
      # docker run -d --name "${REVIEW_APP_NAME}" \
      #   -p "$(( 3000 + CI_MERGE_REQUEST_IID ))":3000 \
      #   "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}"

    - echo "Review app déployée: ${REVIEW_URL}"

  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: https://review-$CI_MERGE_REQUEST_IID.example.com
    on_stop: stop_review
    auto_stop_in: 1 week

  only:
    - merge_requests

  artifacts:
    reports:
      deployment: deployment-review.json
    expire_in: 1 week

# Job d'arrêt review app
stop_review:
  <<: *deploy_template
  stage: deploy-dev
  script:
    - echo "Nettoyage review app: review-${CI_MERGE_REQUEST_IID}"
    # docker stop "review-${CI_MERGE_REQUEST_IID}" || true
    # docker rm "review-${CI_MERGE_REQUEST_IID}" || true
  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  when: manual
  only:
    - merge_requests
```

### 3.2 Scripts de déploiement

**Créer le fichier `scripts/deploy-blue-green.sh`** :

```bash
#!/bin/bash
# Votre tâche : Script de déploiement Blue-Green

set -euo pipefail

ENVIRONMENT="${1:-staging}"
BLUE_URL="https://blue-${ENVIRONMENT}.example.com"
GREEN_URL="https://green-${ENVIRONMENT}.example.com"
LOAD_BALANCER_CONFIG="/etc/nginx/conf.d/${ENVIRONMENT}.conf"

# Fonctions utilitaires
log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1"
    exit 1
}

# Fonction pour vérifier la santé d'un environnement
check_health() {
    local url="$1"
    local max_attempts=30
    local attempt=1

    log_info "Vérification de la santé: $url"

    while [ $attempt -le $max_attempts ]; do
        # if curl -f "${url}/health" >/dev/null 2>&1; then
        #     log_info "Service healthy: $url"
        #     return 0
        # fi

        echo "Tentative $attempt/$max_attempts"
        sleep 10
        ((attempt++))
    done

    log_error "Service non accessible: $url"
    return 1
}

# Fonction de déploiement Blue-Green
deploy_blue_green() {
    log_info "=== DÉPLOIEMENT BLUE-GREEN ==="

    # Étape 1: Identifier l'environnement actif
    # local current_env=$(get_current_environment)
    local current_env="blue"  # Simulation
    local target_env="green"

    if [ "$current_env" = "green" ]; then
        target_env="blue"
    fi

    log_info "Environnement actuel: $current_env"
    log_info "Environnement cible: $target_env"

    # Étape 2: Déployer sur l'environnement cible
    log_info "Déploiement sur l'environnement $target_env"
    # deploy_to_environment "$target_env"

    # Étape 3: Vérifier la santé du nouvel environnement
    local target_url
    if [ "$target_env" = "blue" ]; then
        target_url="$BLUE_URL"
    else
        target_url="$GREEN_URL"
    fi

    # check_health "$target_url"

    # Étape 4: Exécuter les tests de smoke
    log_info "Exécution des tests de smoke"
    # run_smoke_tests "$target_url"

    # Étape 5: Basculer le trafic
    log_info "Basculement du trafic vers $target_env"
    # switch_traffic "$target_env"

    # Étape 6: Vérifier le nouveau déploiement
    # check_health "https://${ENVIRONMENT}.example.com"

    log_info "Déploiement Blue-Green terminé avec succès"
}

# Fonction pour basculer le trafic
switch_traffic() {
    local target_env="$1"

    log_info "Basculement du trafic vers: $target_env"

    # Mise à jour de la configuration du load balancer
    # update_load_balancer_config "$target_env"

    # Recharger la configuration
    # reload_load_balancer

    # Attendre la propagation
    sleep 30

    log_info "Trafic basculé vers $target_env"
}

# Fonction de rollback
rollback() {
    local previous_env="$1"

    log_info "=== ROLLBACK VERS $previous_env ==="

    # switch_traffic "$previous_env"

    log_info "Rollback terminé"
}

# Fonction principale
main() {
    case "${2:-deploy}" in
        "deploy")
            deploy_blue_green
            ;;
        "rollback")
            rollback "${3:-blue}"
            ;;
        *)
            echo "Usage: $0 <environment> <deploy|rollback> [previous_env]"
            exit 1
            ;;
    esac
}

# Exécution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

## Exercice 4 : Tests et validation multi-environnements (20 points)

### 4.1 Tests de validation par environnement

**Créer le fichier `tests/environment-tests.js`** :

```javascript
// Votre tâche : Tests de validation par environnement

const {expect} = require('chai');
const axios = require('axios');

// Configuration des environnements
const environments = {
  development: {
    baseUrl: 'https://dev-react-app.example.com',
    apiUrl: 'https://api-dev.example.com'
    // timeout: 10000,
    // retries: 3
  },
  staging: {
    baseUrl: 'https://staging-react-app.example.com',
    apiUrl: 'https://api-staging.example.com'
    // timeout: 5000,
    // retries: 2
  },
  production: {
    baseUrl: 'https://react-app.example.com',
    apiUrl: 'https://api.example.com'
    // timeout: 3000,
    // retries: 1
  }
};

// Classe pour les tests d'environnement
class EnvironmentTester {
  constructor(environment) {
    this.env = environments[environment];
    this.environment = environment;
  }

  // Test de santé basique
  async testHealth() {
    // const response = await axios.get(`${this.env.baseUrl}/health`);
    // expect(response.status).to.equal(200);
    // expect(response.data.status).to.equal('healthy');
    console.log(`Health check passed for ${this.environment}`);
  }

  // Test de chargement de l'application
  async testApplicationLoad() {
    // const response = await axios.get(this.env.baseUrl);
    // expect(response.status).to.equal(200);
    // expect(response.data).to.contain('DevOps React App');
    console.log(`Application load test passed for ${this.environment}`);
  }

  // Test des métriques
  async testMetrics() {
    // const response = await axios.get(`${this.env.baseUrl}/metrics`);
    // expect(response.status).to.equal(200);
    // expect(response.headers['content-type']).to.contain('text/plain');
    console.log(`Metrics test passed for ${this.environment}`);
  }

  // Test de l'API backend
  async testBackendAPI() {
    // const response = await axios.get(`${this.env.apiUrl}/health`);
    // expect(response.status).to.equal(200);
    console.log(`Backend API test passed for ${this.environment}`);
  }

  // Test de performance
  async testPerformance() {
    const startTime = Date.now();
    // await axios.get(this.env.baseUrl);
    const endTime = Date.now();
    const responseTime = endTime - startTime;

    // Seuils par environnement
    const thresholds = {
      development: 5000, // 5s
      staging: 3000, // 3s
      production: 1000 // 1s
    };

    const threshold = thresholds[this.environment];
    // expect(responseTime).to.be.below(threshold);
    console.log(
      `Performance test passed for ${this.environment}: ${responseTime}ms < ${threshold}ms`
    );
  }

  // Test de sécurité basique
  async testSecurity() {
    // Test des headers de sécurité
    // const response = await axios.get(this.env.baseUrl);
    // expect(response.headers['x-frame-options']).to.exist;
    // expect(response.headers['x-content-type-options']).to.equal('nosniff');
    console.log(`Security test passed for ${this.environment}`);
  }

  // Exécuter tous les tests
  async runAllTests() {
    console.log(`\n=== Tests pour l'environnement: ${this.environment} ===`);

    try {
      await this.testHealth();
      await this.testApplicationLoad();
      await this.testMetrics();
      await this.testBackendAPI();
      await this.testPerformance();
      await this.testSecurity();

      console.log(`✅ Tous les tests passés pour ${this.environment}`);
      return true;
    } catch (error) {
      console.error(
        `❌ Tests échoués pour ${this.environment}:`,
        error.message
      );
      return false;
    }
  }
}

// Fonction pour tester un environnement spécifique
async function testEnvironment(environmentName) {
  const tester = new EnvironmentTester(environmentName);
  return await tester.runAllTests();
}

// Fonction pour tester tous les environnements
async function testAllEnvironments() {
  console.log('=== TESTS MULTI-ENVIRONNEMENTS ===');

  const results = {};

  for (const env of Object.keys(environments)) {
    results[env] = await testEnvironment(env);
  }

  // Rapport final
  console.log('\n=== RAPPORT FINAL ===');
  Object.entries(results).forEach(([env, passed]) => {
    console.log(`${env}: ${passed ? '✅ SUCCÈS' : '❌ ÉCHEC'}`);
  });

  const allPassed = Object.values(results).every((result) => result);

  if (allPassed) {
    console.log('\n🎉 Tous les environnements sont validés');
    process.exit(0);
  } else {
    console.log('\n💥 Certains environnements ont échoué');
    process.exit(1);
  }
}

// Exécution selon les arguments
if (require.main === module) {
  const environment = process.argv[2];

  if (environment && environments[environment]) {
    testEnvironment(environment);
  } else if (environment === 'all') {
    testAllEnvironments();
  } else {
    console.log(
      'Usage: node environment-tests.js <development|staging|production|all>'
    );
    process.exit(1);
  }
}

module.exports = {EnvironmentTester, testEnvironment};
```

### 4.2 Smoke tests

**Créer le fichier `tests/smoke-tests.sh`** :

```bash
#!/bin/bash
# Votre tâche : Tests de smoke pour validation des déploiements

set -euo pipefail

ENVIRONMENT="${1:-staging}"
BASE_URL="${2:-https://${ENVIRONMENT}-react-app.example.com}"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fonctions utilitaires
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Test 1: Health Check
test_health_check() {
    log_info "Test 1: Health Check"

    # if curl -f "${BASE_URL}/health" >/dev/null 2>&1; then
    #     log_info "✅ Health check réussi"
    #     return 0
    # else
    #     log_error "❌ Health check échoué"
    #     return 1
    # fi

    log_info "✅ Health check réussi (simulé)"
    return 0
}

# Test 2: Page d'accueil
test_homepage() {
    log_info "Test 2: Page d'accueil"

    # local response=$(curl -s "${BASE_URL}")
    # if echo "$response" | grep -q "DevOps React App"; then
    #     log_info "✅ Page d'accueil chargée"
    #     return 0
    # else
    #     log_error "❌ Page d'accueil non accessible"
    #     return 1
    # fi

    log_info "✅ Page d'accueil chargée (simulé)"
    return 0
}

# Test 3: Endpoint des métriques
test_metrics() {
    log_info "Test 3: Endpoint des métriques"

    # if curl -f "${BASE_URL}/metrics" >/dev/null 2>&1; then
    #     log_info "✅ Métriques accessibles"
    #     return 0
    # else
    #     log_error "❌ Métriques non accessibles"
    #     return 1
    # fi

    log_info "✅ Métriques accessibles (simulé)"
    return 0
}

# Test 4: Performance basique
test_performance() {
    log_info "Test 4: Performance basique"

    local start_time=$(date +%s.%N)
    # curl -s "${BASE_URL}" >/dev/null
    local end_time=$(date +%s.%N)

    local duration=$(echo "$end_time - $start_time" | bc)
    local threshold=3.0

    # if (( $(echo "$duration < $threshold" | bc -l) )); then
    #     log_info "✅ Performance acceptable: ${duration}s < ${threshold}s"
    #     return 0
    # else
    #     log_error "❌ Performance dégradée: ${duration}s >= ${threshold}s"
    #     return 1
    # fi

    log_info "✅ Performance acceptable: 0.5s < ${threshold}s (simulé)"
    return 0
}

# Test 5: Headers de sécurité
test_security_headers() {
    log_info "Test 5: Headers de sécurité"

    local required_headers=(
        "X-Frame-Options"
        "X-Content-Type-Options"
        "Content-Security-Policy"
    )

    local missing_headers=()

    for header in "${required_headers[@]}"; do
        # if ! curl -I -s "${BASE_URL}" | grep -i "$header" >/dev/null; then
        #     missing_headers+=("$header")
        # fi
        log_info "Vérification header: $header (simulé)"
    done

    if [ ${#missing_headers[@]} -eq 0 ]; then
        log_info "✅ Tous les headers de sécurité sont présents"
        return 0
    else
        log_error "❌ Headers de sécurité manquants: ${missing_headers[*]}"
        return 1
    fi
}

# Test 6: Fonctionnalités critiques
test_critical_features() {
    log_info "Test 6: Fonctionnalités critiques"

    # Test spécifique selon l'environnement
    case "$ENVIRONMENT" in
        "production")
            # Tests plus stricts pour la production
            log_info "Tests production stricts"
            # test_user_authentication
            # test_data_integrity
            ;;
        "staging")
            # Tests de pré-production
            log_info "Tests staging complets"
            # test_integration_apis
            # test_database_connectivity
            ;;
        "development")
            # Tests de développement
            log_info "Tests development basiques"
            # test_debug_endpoints
            ;;
    esac

    log_info "✅ Fonctionnalités critiques validées (simulé)"
    return 0
}

# Test 7: Connectivité backend
test_backend_connectivity() {
    log_info "Test 7: Connectivité backend"

    local api_urls=(
        "https://api-${ENVIRONMENT}.example.com/health"
        "https://api-${ENVIRONMENT}.example.com/version"
    )

    for url in "${api_urls[@]}"; do
        # if curl -f "$url" >/dev/null 2>&1; then
        #     log_info "✅ Backend accessible: $url"
        # else
        #     log_error "❌ Backend non accessible: $url"
        #     return 1
        # fi
        log_info "✅ Backend accessible: $url (simulé)"
    done

    return 0
}

# Fonction principale de test
run_smoke_tests() {
    log_info "=== SMOKE TESTS POUR $ENVIRONMENT ==="
    log_info "URL de base: $BASE_URL"
    log_info "Timestamp: $(date)"

    local tests=(
        "test_health_check"
        "test_homepage"
        "test_metrics"
        "test_performance"
        "test_security_headers"
        "test_critical_features"
        "test_backend_connectivity"
    )

    local passed=0
    local failed=0
    local failed_tests=()

    for test in "${tests[@]}"; do
        if $test; then
            ((passed++))
        else
            ((failed++))
            failed_tests+=("$test")
        fi
        echo
    done

    # Rapport final
    log_info "=== RAPPORT DES SMOKE TESTS ==="
    log_info "Tests réussis: $passed"
    log_info "Tests échoués: $failed"

    if [ $failed -eq 0 ]; then
        log_info "🎉 Tous les smoke tests sont passés"
        return 0
    else
        log_error "💥 $failed test(s) ont échoué: ${failed_tests[*]}"
        return 1
    fi
}

# Point d'entrée
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_smoke_tests
fi
```

## Livrables attendus

### Fichiers à créer/modifier :

1. **Configuration environnements** :

   - `environments/variables.yml` ✅
   - `scripts/setup-environments.sh` ✅

2. **Stratégies de déploiement** :

   - `deployment/blue-green.yml` ✅
   - `deployment/canary.yml` ✅
   - `deployment/rolling.yml` ✅
   - `scripts/deploy-blue-green.sh` ✅

3. **Pipeline multi-environnements** :

   - `.gitlab-ci.yml` modifié ✅

4. **Tests et validation** :

   - `tests/environment-tests.js` ✅
   - `tests/smoke-tests.sh` ✅

5. **Documentation** :
   - `README-environments.md` ✅

## Grille d'évaluation (100 points)

| Critère                          | Points | Description                          |
| -------------------------------- | ------ | ------------------------------------ |
| **Configuration environnements** | 25     | Setup GitLab, variables, protection  |
| **Stratégies déploiement**       | 30     | Blue-Green, Canary, Rolling          |
| **Pipeline multi-env**           | 25     | Jobs par environnement, approbations |
| **Tests validation**             | 20     | Smoke tests, tests environnements    |

## Points bonus (10 points)

- Feature flags par environnement (+3)
- Rollback automatique (+3)
- Monitoring multi-environnements (+2)
- Documentation complète (+2)

## Ressources utiles

- [GitLab Environments](https://docs.gitlab.com/ee/ci/environments/)
- [Deployment Strategies](https://docs.gitlab.com/ee/ci/environments/deployment_safety.html)
- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Canary Releases](https://martinfowler.com/bliki/CanaryRelease.html)

## Étapes suivantes

Après avoir terminé ce lab :

1. Vérifier les environnements GitLab
2. Tester les stratégies de déploiement
3. Valider les tests multi-environnements
4. Passer au **LAB 9 : Review Apps et Collaboration**

---

Le LAB 8 vous donne une maîtrise complète de la gestion des environnements et des stratégies de déploiement avancées !
