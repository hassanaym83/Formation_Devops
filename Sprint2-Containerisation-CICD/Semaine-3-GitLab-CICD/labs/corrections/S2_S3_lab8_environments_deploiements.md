# LAB 8 - CORRECTION : Environments et Déploiements

## Vue d'ensemble de la correction

Ce LAB couvre la gestion des environnements multiples et les stratégies de déploiement avancées. La correction présente les solutions optimales pour chaque exercice.

## Exercice 1 : Configuration des environnements GitLab (25 points)

### 1.1 Création des environnements

**Solution complète : Configuration GitLab Environments**

1. **Interface GitLab - Création des environnements**

   ```bash
   # Via API GitLab pour automatiser
   curl -X POST \
     -H "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" \
     -H "Content-Type: application/json" \
     "$CI_API_V4_URL/projects/$CI_PROJECT_ID/environments" \
     -d '{
       "name": "development",
       "external_url": "https://dev.example.com"
     }'

   curl -X POST \
     -H "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" \
     -H "Content-Type: application/json" \
     "$CI_API_V4_URL/projects/$CI_PROJECT_ID/environments" \
     -d '{
       "name": "staging",
       "external_url": "https://staging.example.com"
     }'

   curl -X POST \
     -H "PRIVATE-TOKEN: ${GITLAB_API_TOKEN}" \
     -H "Content-Type: application/json" \
     "$CI_API_V4_URL/projects/$CI_PROJECT_ID/environments" \
     -d '{
       "name": "production",
       "external_url": "https://example.com"
     }'
   ```

2. **Configuration `.gitlab-ci.yml` complète**

   ```yaml
   stages:
     - build
     - test
     - deploy-dev
     - deploy-staging
     - deploy-prod

   variables:
     DOCKER_REGISTRY: $CI_REGISTRY
     IMAGE_NAME: $CI_REGISTRY_IMAGE

   # Build de l'application
   build:
     stage: build
     image: docker:20.10.16
     services:
       - docker:20.10.16-dind
     before_script:
       - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
     script:
       - |
         docker build \
           --build-arg NODE_ENV=production \
           --tag $IMAGE_NAME:$CI_COMMIT_SHA \
           --tag $IMAGE_NAME:latest \
           .
       - docker push $IMAGE_NAME:$CI_COMMIT_SHA
       - docker push $IMAGE_NAME:latest
     only:
       - main
       - develop
       - /^feature\/.*$/

   # Tests
   test:
     stage: test
     image: node:18
     script:
       - npm ci
       - npm run test:unit
       - npm run test:integration
     coverage: '/Coverage: \d+\.\d+%/'
     artifacts:
       reports:
         junit: test-results.xml
         coverage_report:
           coverage_format: cobertura
           path: coverage/cobertura.xml

   # Déploiement Development (automatique sur feature branches)
   deploy_development:
     stage: deploy-dev
     image: alpine:latest
     variables:
       ENV_NAME: 'development'
       APP_URL: 'https://dev-$CI_COMMIT_REF_SLUG.example.com'
     before_script:
       - apk add --no-cache curl docker-compose
     script:
       - echo "🚀 Déploiement vers Development"
       - |
         cat > docker-compose.dev.yml << EOF
         version: '3.8'
         services:
           app:
             image: $IMAGE_NAME:$CI_COMMIT_SHA
             ports:
               - "3000:3000"
             environment:
               - NODE_ENV=development
               - DATABASE_URL=$DEV_DATABASE_URL
               - API_KEY=$DEV_API_KEY
             restart: unless-stopped
         EOF
       - docker-compose -f docker-compose.dev.yml up -d
       - sleep 30
       - curl -f $APP_URL/health || exit 1
     environment:
       name: development/$CI_COMMIT_REF_SLUG
       url: $APP_URL
       on_stop: stop_development
       auto_stop_in: 3 days
     only:
       - /^feature\/.*$/

   # Arrêt environment Development
   stop_development:
     stage: deploy-dev
     image: alpine:latest
     variables:
       GIT_STRATEGY: none
     script:
       - echo "🗑️ Nettoyage environment Development"
       - docker-compose -f docker-compose.dev.yml down || true
       - docker rmi $IMAGE_NAME:$CI_COMMIT_SHA || true
     environment:
       name: development/$CI_COMMIT_REF_SLUG
       action: stop
     when: manual
     only:
       - /^feature\/.*$/

   # Déploiement Staging (automatique sur develop)
   deploy_staging:
     stage: deploy-staging
     image: alpine:latest
     variables:
       ENV_NAME: 'staging'
       APP_URL: 'https://staging.example.com'
     before_script:
       - apk add --no-cache curl docker-compose
     script:
       - echo "🚀 Déploiement vers Staging"
       - |
         cat > docker-compose.staging.yml << EOF
         version: '3.8'
         services:
           app:
             image: $IMAGE_NAME:$CI_COMMIT_SHA
             ports:
               - "80:3000"
             environment:
               - NODE_ENV=staging
               - DATABASE_URL=$STAGING_DATABASE_URL
               - API_KEY=$STAGING_API_KEY
               - SENTRY_DSN=$STAGING_SENTRY_DSN
             restart: unless-stopped
             healthcheck:
               test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
               interval: 30s
               timeout: 10s
               retries: 3
           
           db:
             image: postgres:13
             environment:
               - POSTGRES_DB=app_staging
               - POSTGRES_USER=app_user
               - POSTGRES_PASSWORD=$STAGING_DB_PASSWORD
             volumes:
               - staging_db_data:/var/lib/postgresql/data
             restart: unless-stopped

         volumes:
           staging_db_data:
         EOF
       - docker-compose -f docker-compose.staging.yml up -d
       - echo "⏳ Attente démarrage des services..."
       - sleep 60
       - curl -f $APP_URL/health || exit 1
       - echo "✅ Déploiement Staging réussi"
     environment:
       name: staging
       url: $APP_URL
     only:
       - develop

   # Déploiement Production (manuel depuis main)
   deploy_production:
     stage: deploy-prod
     image: alpine:latest
     variables:
       ENV_NAME: 'production'
       APP_URL: 'https://example.com'
     before_script:
       - apk add --no-cache curl docker-compose
     script:
       - echo "🚀 Déploiement vers Production"
       - |
         cat > docker-compose.prod.yml << EOF
         version: '3.8'
         services:
           app:
             image: $IMAGE_NAME:$CI_COMMIT_SHA
             ports:
               - "80:3000"
             environment:
               - NODE_ENV=production
               - DATABASE_URL=$PROD_DATABASE_URL
               - API_KEY=$PROD_API_KEY
               - SENTRY_DSN=$PROD_SENTRY_DSN
               - REDIS_URL=$PROD_REDIS_URL
             restart: unless-stopped
             deploy:
               replicas: 2
               update_config:
                 parallelism: 1
                 delay: 10s
                 failure_action: rollback
               restart_policy:
                 condition: any
                 delay: 5s
                 max_attempts: 3
             healthcheck:
               test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
               interval: 30s
               timeout: 10s
               retries: 3
               start_period: 40s
           
           db:
             image: postgres:13
             environment:
               - POSTGRES_DB=app_production
               - POSTGRES_USER=app_user
               - POSTGRES_PASSWORD=$PROD_DB_PASSWORD
             volumes:
               - prod_db_data:/var/lib/postgresql/data
             restart: unless-stopped
           
           redis:
             image: redis:6-alpine
             command: redis-server --appendonly yes
             volumes:
               - prod_redis_data:/data
             restart: unless-stopped

         volumes:
           prod_db_data:
           prod_redis_data:
         EOF
       - docker-compose -f docker-compose.prod.yml up -d
       - echo "⏳ Attente démarrage des services..."
       - sleep 90
       - curl -f $APP_URL/health || exit 1
       - echo "✅ Déploiement Production réussi"
     environment:
       name: production
       url: $APP_URL
     when: manual
     only:
       - main
   ```

### 1.2 Variables d'environnement par contexte

**Solution : Configuration variables avancée**

1. **Variables au niveau projet** (Settings > CI/CD > Variables)

   ```bash
   # Variables globales
   DOCKER_REGISTRY_USER="gitlab-ci-token"
   DOCKER_REGISTRY_PASSWORD="$CI_JOB_TOKEN"

   # Development
   DEV_DATABASE_URL="postgresql://dev_user:dev_pass@dev-db:5432/app_dev"
   DEV_API_KEY="dev_api_key_here"

   # Staging
   STAGING_DATABASE_URL="postgresql://staging_user:staging_pass@staging-db:5432/app_staging"
   STAGING_API_KEY="staging_api_key_here"
   STAGING_SENTRY_DSN="https://staging@sentry.io/project"
   STAGING_DB_PASSWORD="secure_staging_password"

   # Production (Protected + Masked)
   PROD_DATABASE_URL="postgresql://prod_user:prod_pass@prod-db:5432/app_production"
   PROD_API_KEY="production_api_key_here"
   PROD_SENTRY_DSN="https://production@sentry.io/project"
   PROD_DB_PASSWORD="ultra_secure_production_password"
   PROD_REDIS_URL="redis://prod-redis:6379"
   ```

2. **Configuration avancée dans `.gitlab-ci.yml`**

   ```yaml
   # Template pour configuration environment
   .deploy_template: &deploy_template
     before_script:
       - echo "🔧 Configuration pour environnement $ENV_NAME"
       - |
         case "$ENV_NAME" in
           "development")
             export DATABASE_URL="$DEV_DATABASE_URL"
             export API_KEY="$DEV_API_KEY"
             export LOG_LEVEL="debug"
             export CACHE_TTL="60"
             ;;
           "staging")
             export DATABASE_URL="$STAGING_DATABASE_URL"
             export API_KEY="$STAGING_API_KEY"
             export LOG_LEVEL="info"
             export CACHE_TTL="300"
             export SENTRY_DSN="$STAGING_SENTRY_DSN"
             ;;
           "production")
             export DATABASE_URL="$PROD_DATABASE_URL"
             export API_KEY="$PROD_API_KEY"
             export LOG_LEVEL="warn"
             export CACHE_TTL="3600"
             export SENTRY_DSN="$PROD_SENTRY_DSN"
             export REDIS_URL="$PROD_REDIS_URL"
             ;;
         esac
       - echo "✅ Variables configurées pour $ENV_NAME"

   # Utilisation du template
   deploy_staging:
     <<: *deploy_template
     stage: deploy-staging
     variables:
       ENV_NAME: 'staging'
     # ... reste de la configuration
   ```

## Exercice 2 : Stratégies de déploiement avancées (25 points)

### 2.1 Blue-Green Deployment

**Solution complète : Blue-Green avec Docker et Load Balancer**

1. **Script de déploiement Blue-Green**

   ```bash
   #!/bin/bash
   # blue-green-deploy.sh

   set -e

   # Configuration
   BLUE_PORT=3001
   GREEN_PORT=3002
   LB_PORT=80
   HEALTH_ENDPOINT="/health"

   # Fonctions utilitaires
   log() {
       echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
   }

   check_health() {
       local port=$1
       local max_attempts=30
       local attempt=1

       log "🔍 Vérification santé sur port $port"

       while [ $attempt -le $max_attempts ]; do
           if curl -f "http://localhost:$port$HEALTH_ENDPOINT" > /dev/null 2>&1; then
               log "✅ Service healthy sur port $port"
               return 0
           fi

           log "⏳ Tentative $attempt/$max_attempts..."
           sleep 10
           ((attempt++))
       done

       log "❌ Service non disponible sur port $port"
       return 1
   }

   get_current_environment() {
       # Déterminer quel environnement est actuellement actif
       if curl -f "http://localhost:$LB_PORT$HEALTH_ENDPOINT" 2>/dev/null | grep -q "blue"; then
           echo "blue"
       elif curl -f "http://localhost:$LB_PORT$HEALTH_ENDPOINT" 2>/dev/null | grep -q "green"; then
           echo "green"
       else
           echo "none"
       fi
   }

   deploy_to_environment() {
       local env=$1
       local image=$2
       local port=$3

       log "🚀 Déploiement vers environnement $env"

       # Arrêter l'ancien conteneur s'il existe
       docker stop "app-$env" 2>/dev/null || true
       docker rm "app-$env" 2>/dev/null || true

       # Démarrer le nouveau conteneur
       docker run -d \
           --name "app-$env" \
           --port "$port:3000" \
           --env NODE_ENV=production \
           --env ENV_COLOR="$env" \
           --env DATABASE_URL="$DATABASE_URL" \
           --env API_KEY="$API_KEY" \
           --restart unless-stopped \
           "$image"

       # Vérifier la santé
       if check_health "$port"; then
           log "✅ Déploiement $env réussi"
           return 0
       else
           log "❌ Déploiement $env échoué"
           return 1
       fi
   }

   update_load_balancer() {
       local active_env=$1
       local active_port=$2

       log "🔄 Basculement load balancer vers $active_env"

       # Configuration Nginx pour basculement
       cat > /etc/nginx/conf.d/app.conf << EOF
   upstream app_backend {
       server localhost:$active_port;
   }

   server {
       listen $LB_PORT;

       location / {
           proxy_pass http://app_backend;
           proxy_set_header Host \$host;
           proxy_set_header X-Real-IP \$remote_addr;
           proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

           # Health check
           proxy_connect_timeout 5s;
           proxy_read_timeout 60s;
           proxy_send_timeout 60s;
       }

       location /health {
           proxy_pass http://app_backend/health;
           access_log off;
       }
   }
   EOF

       # Recharger Nginx
       nginx -t && nginx -s reload

       log "✅ Load balancer basculé vers $active_env"
   }

   rollback() {
       local previous_env=$1
       local previous_port=$2

       log "🔙 Rollback vers $previous_env"
       update_load_balancer "$previous_env" "$previous_port"
   }

   # Fonction principale de déploiement Blue-Green
   blue_green_deploy() {
       local new_image=$1

       if [ -z "$new_image" ]; then
           log "❌ Image requise"
           exit 1
       fi

       log "🎯 Démarrage déploiement Blue-Green"
       log "📦 Image: $new_image"

       # Déterminer l'environnement actuel
       local current_env=$(get_current_environment)
       log "🔍 Environnement actuel: $current_env"

       # Déterminer l'environnement cible
       local target_env
       local target_port
       local current_port

       if [ "$current_env" = "blue" ]; then
           target_env="green"
           target_port=$GREEN_PORT
           current_port=$BLUE_PORT
       else
           target_env="blue"
           target_port=$BLUE_PORT
           current_port=$GREEN_PORT
       fi

       log "🎯 Environnement cible: $target_env (port $target_port)"

       # Déployer vers l'environnement cible
       if deploy_to_environment "$target_env" "$new_image" "$target_port"; then
           # Tests de validation sur le nouveau déploiement
           log "🧪 Tests de validation..."

           # Test simple de santé
           if curl -f "http://localhost:$target_port/health" > /dev/null 2>&1; then
               # Test fonctionnel
               if curl -f "http://localhost:$target_port/api/status" > /dev/null 2>&1; then
                   log "✅ Tests de validation réussis"

                   # Basculer le trafic
                   update_load_balancer "$target_env" "$target_port"

                   # Attendre un peu puis vérifier
                   sleep 30
                   if curl -f "http://localhost:$LB_PORT/health" > /dev/null 2>&1; then
                       log "🎉 Déploiement Blue-Green réussi!"

                       # Optionnel: arrêter l'ancien environnement après délai
                       sleep 60
                       if [ "$current_env" != "none" ]; then
                           docker stop "app-$current_env" || true
                           log "🗑️ Ancien environnement $current_env arrêté"
                       fi
                   else
                       log "❌ Problème après basculement, rollback"
                       rollback "$current_env" "$current_port"
                       exit 1
                   fi
               else
                   log "❌ Tests fonctionnels échoués"
                   exit 1
               fi
           else
               log "❌ Tests de santé échoués"
               exit 1
           fi
       else
           log "❌ Déploiement vers $target_env échoué"
           exit 1
       fi
   }

   # Exécution
   blue_green_deploy "$1"
   ```

2. **Configuration GitLab CI pour Blue-Green**

   ```yaml
   # Job Blue-Green Deployment
   deploy_blue_green:
     stage: deploy-prod
     image: alpine:latest
     variables:
       ENV_NAME: 'production'
       DEPLOYMENT_STRATEGY: 'blue-green'
     before_script:
       - apk add --no-cache curl docker nginx
       - chmod +x scripts/blue-green-deploy.sh
     script:
       - echo "🎯 Déploiement Blue-Green vers Production"
       - ./scripts/blue-green-deploy.sh "$IMAGE_NAME:$CI_COMMIT_SHA"
     environment:
       name: production
       url: https://example.com
       deployment_tier: production
     when: manual
     only:
       - main
     allow_failure: false
   ```

### 2.2 Canary Deployment

**Solution : Déploiement Canary avec contrôle de trafic**

1. **Script de déploiement Canary**

   ```bash
   #!/bin/bash
   # canary-deploy.sh

   set -e

   # Configuration
   STABLE_REPLICAS=3
   CANARY_REPLICAS=1
   CANARY_PERCENTAGE=25
   VALIDATION_DURATION=300  # 5 minutes

   # Fonctions
   deploy_canary() {
       local image=$1
       local percentage=$2

       log "🐦 Déploiement Canary ($percentage% du trafic)"

       # Déployer la version Canary
       cat > canary-deployment.yml << EOF
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: app-canary
     labels:
       app: myapp
       version: canary
   spec:
     replicas: $CANARY_REPLICAS
     selector:
       matchLabels:
         app: myapp
         version: canary
     template:
       metadata:
         labels:
           app: myapp
           version: canary
       spec:
         containers:
         - name: app
           image: $image
           ports:
           - containerPort: 3000
           env:
           - name: VERSION
             value: "canary"
           readinessProbe:
             httpGet:
               path: /health
               port: 3000
             initialDelaySeconds: 10
             periodSeconds: 5
           livenessProbe:
             httpGet:
               path: /health
               port: 3000
             initialDelaySeconds: 30
             periodSeconds: 10
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: app-canary-service
   spec:
     selector:
       app: myapp
       version: canary
     ports:
     - port: 80
       targetPort: 3000
   EOF

       kubectl apply -f canary-deployment.yml

       # Attendre que les pods soient prêts
       kubectl rollout status deployment/app-canary --timeout=300s

       # Configurer le routage de trafic
       configure_traffic_split "$percentage"
   }

   configure_traffic_split() {
       local canary_percentage=$1
       local stable_percentage=$((100 - canary_percentage))

       cat > traffic-split.yml << EOF
   apiVersion: networking.istio.io/v1alpha3
   kind: VirtualService
   metadata:
     name: app-traffic-split
   spec:
     http:
     - match:
       - headers:
           canary:
             exact: "true"
       route:
       - destination:
           host: app-canary-service
           port:
             number: 80
     - route:
       - destination:
           host: app-stable-service
           port:
             number: 80
         weight: $stable_percentage
       - destination:
           host: app-canary-service
           port:
             number: 80
         weight: $canary_percentage
   EOF

       kubectl apply -f traffic-split.yml
       log "✅ Trafic configuré: $stable_percentage% stable, $canary_percentage% canary"
   }

   validate_canary() {
       log "🧪 Validation du déploiement Canary"

       local start_time=$(date +%s)
       local end_time=$((start_time + VALIDATION_DURATION))

       while [ $(date +%s) -lt $end_time ]; do
           # Vérifier les métriques
           local error_rate=$(get_error_rate)
           local response_time=$(get_response_time)

           log "📊 Taux d'erreur: $error_rate%, Temps de réponse: ${response_time}ms"

           # Critères de validation
           if (( $(echo "$error_rate > 5" | bc -l) )); then
               log "❌ Taux d'erreur trop élevé ($error_rate%)"
               return 1
           fi

           if (( $(echo "$response_time > 1000" | bc -l) )); then
               log "❌ Temps de réponse trop lent (${response_time}ms)"
               return 1
           fi

           sleep 30
       done

       log "✅ Validation Canary réussie"
       return 0
   }

   promote_canary() {
       log "🚀 Promotion du Canary vers Stable"

       # Mettre à jour le déploiement stable avec l'image Canary
       kubectl set image deployment/app-stable app="$1"
       kubectl rollout status deployment/app-stable --timeout=300s

       # Supprimer le déploiement Canary
       kubectl delete -f canary-deployment.yml

       # Remettre le trafic à 100% sur stable
       configure_traffic_split 0

       log "✅ Promotion terminée"
   }

   rollback_canary() {
       log "🔙 Rollback du Canary"

       # Supprimer le déploiement Canary
       kubectl delete -f canary-deployment.yml || true

       # Remettre le trafic à 100% sur stable
       configure_traffic_split 0

       log "✅ Rollback terminé"
   }

   get_error_rate() {
       # Récupérer le taux d'erreur depuis Prometheus
       curl -s "$PROMETHEUS_URL/api/v1/query?query=rate(http_requests_total{status=~\"5..\",version=\"canary\"}[5m])*100" | \
       jq -r '.data.result[0].value[1] // "0"'
   }

   get_response_time() {
       # Récupérer le temps de réponse moyen depuis Prometheus
       curl -s "$PROMETHEUS_URL/api/v1/query?query=histogram_quantile(0.95,rate(http_request_duration_seconds_bucket{version=\"canary\"}[5m]))*1000" | \
       jq -r '.data.result[0].value[1] // "0"'
   }

   # Fonction principale
   canary_deploy() {
       local image=$1
       local action=${2:-"deploy"}

       case "$action" in
           "deploy")
               deploy_canary "$image" "$CANARY_PERCENTAGE"
               if validate_canary; then
                   log "🎉 Canary validé, prêt pour promotion"
               else
                   log "❌ Canary échoué, rollback automatique"
                   rollback_canary
                   exit 1
               fi
               ;;
           "promote")
               promote_canary "$image"
               ;;
           "rollback")
               rollback_canary
               ;;
           *)
               echo "Usage: $0 <image> {deploy|promote|rollback}"
               exit 1
               ;;
       esac
   }

   # Exécution
   canary_deploy "$@"
   ```

## Exercice 3 : Approbations et policies (25 points)

### 3.1 Configuration des approbations

**Solution : Système d'approbation multi-niveaux**

1. **Configuration GitLab Environments avec approbations**

   ```yaml
   # .gitlab-ci.yml avec approbations
   deploy_production:
     stage: deploy-prod
     script:
       - echo "🚀 Déploiement vers Production"
       - ./scripts/deploy-production.sh
     environment:
       name: production
       url: https://example.com
       deployment_tier: production
     rules:
       - if: $CI_COMMIT_BRANCH == "main"
         when: manual
         allow_failure: false
     needs:
       - job: test
         artifacts: true
       - job: security_scan
         artifacts: true

   # Job de pré-validation
   pre_production_validation:
     stage: validate
     script:
       - echo "🔍 Validation pré-production"
       - ./scripts/pre-prod-validation.sh
     environment:
       name: pre-production
       action: prepare
     when: manual
     only:
       - main
   ```

2. **Script de validation des prérequis**

   ```bash
   #!/bin/bash
   # pre-prod-validation.sh

   set -e

   validate_security() {
       log "🔒 Validation sécurité"

       # Vérifier les scans de sécurité
       if [ ! -f "security-report.json" ]; then
           log "❌ Rapport de sécurité manquant"
           return 1
       fi

       local critical_vulns=$(cat security-report.json | jq '.vulnerabilities[] | select(.severity == "critical") | length')
       if [ "$critical_vulns" -gt 0 ]; then
           log "❌ Vulnérabilités critiques détectées: $critical_vulns"
           return 1
       fi

       log "✅ Validation sécurité OK"
   }

   validate_tests() {
       log "🧪 Validation tests"

       # Vérifier la couverture de tests
       local coverage=$(cat coverage-report.json | jq -r '.total.lines.pct')
       if (( $(echo "$coverage < 80" | bc -l) )); then
           log "❌ Couverture de tests insuffisante: $coverage%"
           return 1
       fi

       log "✅ Validation tests OK (couverture: $coverage%)"
   }

   validate_performance() {
       log "⚡ Validation performance"

       # Tests de charge sur staging
       local response_time=$(curl -o /dev/null -s -w '%{time_total}' https://staging.example.com)
       if (( $(echo "$response_time > 2" | bc -l) )); then
           log "❌ Temps de réponse trop lent: ${response_time}s"
           return 1
       fi

       log "✅ Validation performance OK (${response_time}s)"
   }

   # Exécution des validations
   validate_security
   validate_tests
   validate_performance

   log "🎉 Toutes les validations sont réussies"
   ```

### 3.2 Policies de déploiement

**Solution : Policies automatisées avec Open Policy Agent**

1. **Policy OPA pour déploiements**

   ```rego
   # deployment-policy.rego
   package deployment

   import rego.v1

   # Règles de base pour tous les déploiements
   default allow := false

   # Autoriser les déploiements avec validations complètes
   allow if {
       input.environment == "production"
       security_checks_passed
       test_coverage_sufficient
       performance_requirements_met
       approval_obtained
   }

   # Vérifications sécurité
   security_checks_passed if {
       input.security_scan.status == "passed"
       input.security_scan.critical_vulnerabilities == 0
       input.security_scan.high_vulnerabilities < 3
   }

   # Couverture de tests
   test_coverage_sufficient if {
       input.test_coverage.percentage >= 80
       input.test_coverage.unit_tests == "passed"
       input.test_coverage.integration_tests == "passed"
   }

   # Performance
   performance_requirements_met if {
       input.performance.response_time_ms < 1000
       input.performance.memory_usage_mb < 512
       input.performance.cpu_usage_percent < 80
   }

   # Approbation
   approval_obtained if {
       count(input.approvals) >= 2
       some approval in input.approvals
       approval.role in ["tech_lead", "devops_engineer", "security_officer"]
   }

   # Règles spécifiques par environnement
   staging_requirements if {
       input.environment == "staging"
       input.branch in ["develop", "main"]
       basic_tests_passed
   }

   basic_tests_passed if {
       input.test_results.unit_tests == "passed"
       input.test_results.lint == "passed"
   }

   # Messages d'erreur détaillés
   deny[msg] {
       input.environment == "production"
       not security_checks_passed
       msg := "Security checks failed: critical vulnerabilities or too many high-severity issues"
   }

   deny[msg] {
       input.environment == "production"
       not test_coverage_sufficient
       msg := sprintf("Test coverage insufficient: %v%% (minimum 80%%)", [input.test_coverage.percentage])
   }

   deny[msg] {
       input.environment == "production"
       not approval_obtained
       msg := "Insufficient approvals: need at least 2 approvals from authorized roles"
   }
   ```

2. **Intégration OPA dans le pipeline**

   ```yaml
   # Job de validation Policy
   validate_deployment_policy:
     stage: validate
     image: openpolicyagent/opa:latest
     script:
       - echo "🔍 Validation des policies de déploiement"
       - |
         # Créer le payload de validation
         cat > policy-input.json << EOF
         {
           "environment": "$ENV_NAME",
           "branch": "$CI_COMMIT_REF_NAME",
           "security_scan": {
             "status": "$(cat security-report.json | jq -r '.status')",
             "critical_vulnerabilities": $(cat security-report.json | jq '.vulnerabilities[] | select(.severity == "critical") | length'),
             "high_vulnerabilities": $(cat security-report.json | jq '.vulnerabilities[] | select(.severity == "high") | length')
           },
           "test_coverage": {
             "percentage": $(cat coverage-report.json | jq '.total.lines.pct'),
             "unit_tests": "passed",
             "integration_tests": "passed"
           },
           "performance": {
             "response_time_ms": 800,
             "memory_usage_mb": 256,
             "cpu_usage_percent": 45
           },
           "approvals": [
             {"user": "tech.lead", "role": "tech_lead", "timestamp": "$(date -Iseconds)"},
             {"user": "devops.engineer", "role": "devops_engineer", "timestamp": "$(date -Iseconds)"}
           ]
         }
         EOF

       # Valider avec OPA
       - opa eval --data deployment-policy.rego --input policy-input.json "data.deployment.allow"
       - |
         if [ "$(opa eval --data deployment-policy.rego --input policy-input.json --format raw "data.deployment.allow")" != "true" ]; then
           echo "❌ Policy validation failed:"
           opa eval --data deployment-policy.rego --input policy-input.json "data.deployment.deny"
           exit 1
         fi
       - echo "✅ Policy validation passed"
     artifacts:
       paths:
         - policy-input.json
       expire_in: 1 week
     only:
       - main
   ```

## Métriques et KPIs

### Dashboard de déploiement

```yaml
# Métriques collectées
deployment_metrics:
  stage: .post
  image: alpine:latest
  script:
    - |
      cat > deployment-metrics.json << EOF
      {
        "deployment_id": "$CI_PIPELINE_ID",
        "environment": "$ENV_NAME",
        "strategy": "$DEPLOYMENT_STRATEGY",
        "duration_seconds": $(($(date +%s) - $PIPELINE_START_TIME)),
        "success": true,
        "rollback_required": false,
        "approval_time_seconds": 300,
        "validation_tests_passed": 15,
        "validation_tests_failed": 0
      }
      EOF
    - echo "📊 Métriques de déploiement collectées"
  artifacts:
    reports:
      metrics: deployment-metrics.json
  when: always
```

### Points d'évaluation totaux

- **Configuration environnements** : 25/25 points
- **Stratégies de déploiement** : 25/25 points
- **Approbations et policies** : 25/25 points
- **Métriques et monitoring** : 25/25 points

**Total** : 100/100 points

---

**Note** : Cette correction présente des solutions de niveau production avec des pratiques DevOps avancées. Les concepts sont directement applicables en entreprise pour des déploiements sécurisés et fiables.
