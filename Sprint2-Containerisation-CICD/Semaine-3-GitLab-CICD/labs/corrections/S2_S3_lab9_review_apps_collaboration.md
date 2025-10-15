# LAB 9 - CORRECTION : Review Apps et Collaboration

## Vue d'ensemble de la correction

Ce LAB couvre l'automatisation des Review Apps et l'optimisation des workflows collaboratifs. La correction présente des solutions industrielles pour chaque exercice.

## Exercice 1 : Configuration automatique des Review Apps (30 points)

### 1.1 Review Apps pour les Merge Requests

**Solution complète : Automatisation Review Apps avancée**

1. **Configuration `.gitlab-ci.yml` pour Review Apps**

   ```yaml
   stages:
     - build
     - test
     - review
     - staging
     - production
     - cleanup

   variables:
     DOCKER_REGISTRY: $CI_REGISTRY
     IMAGE_NAME: $CI_REGISTRY_IMAGE
     KUBE_NAMESPACE: review-apps
     REVIEW_DOMAIN: 'review.example.com'

   # Build pour toutes les branches
   build:
     stage: build
     image: docker:20.10.16
     services:
       - docker:20.10.16-dind
     before_script:
       - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
     script:
       - |
         # Build avec optimisations multi-stage
         docker build \
           --build-arg NODE_ENV=production \
           --build-arg BUILD_VERSION=$CI_COMMIT_SHA \
           --build-arg BUILD_TIME=$(date -Iseconds) \
           --target production \
           --tag $IMAGE_NAME:$CI_COMMIT_SHA \
           --tag $IMAGE_NAME:latest \
           --cache-from $IMAGE_NAME:cache \
           --cache-to $IMAGE_NAME:cache \
           .
       - docker push $IMAGE_NAME:$CI_COMMIT_SHA
       - |
         if [ "$CI_COMMIT_REF_NAME" = "main" ]; then
           docker push $IMAGE_NAME:latest
         fi
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == "main"
       - if: $CI_COMMIT_BRANCH == "develop"

   # Tests approfondis
   test:
     stage: test
     image: node:18
     cache:
       key: npm-cache
       paths:
         - node_modules/
         - .npm/
     before_script:
       - npm ci --cache .npm --prefer-offline
     script:
       - npm run lint
       - npm run test:unit
       - npm run test:integration
       - npm run test:e2e:headless
     coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
     artifacts:
       reports:
         junit: test-results.xml
         coverage_report:
           coverage_format: cobertura
           path: coverage/cobertura.xml
       paths:
         - coverage/
         - test-results/
       expire_in: 1 week
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == "main"
       - if: $CI_COMMIT_BRANCH == "develop"

   # Review App - Déploiement automatique
   review_app:
     stage: review
     image: bitnami/kubectl:latest
     variables:
       REVIEW_APP_NAME: 'app-$CI_MERGE_REQUEST_IID'
       REVIEW_URL: 'https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN'
       KUBE_NAMESPACE: 'review-apps'
     before_script:
       - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority-data="$KUBE_CA_PEM"
       - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
       - kubectl config set-context default --cluster=k8s --user=gitlab --namespace="$KUBE_NAMESPACE"
       - kubectl config use-context default
       - kubectl create namespace "$KUBE_NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
     script:
       - echo "🚀 Déploiement Review App: $REVIEW_APP_NAME"
       - |
         # Génération manifeste Kubernetes optimisé
         cat > review-app-manifest.yml << EOF
         apiVersion: apps/v1
         kind: Deployment
         metadata:
           name: $REVIEW_APP_NAME
           namespace: $KUBE_NAMESPACE
           labels:
             app: $REVIEW_APP_NAME
             version: $CI_COMMIT_SHA
             merge-request: "$CI_MERGE_REQUEST_IID"
             branch: $CI_COMMIT_REF_SLUG
         spec:
           replicas: 1
           selector:
             matchLabels:
               app: $REVIEW_APP_NAME
           template:
             metadata:
               labels:
                 app: $REVIEW_APP_NAME
                 version: $CI_COMMIT_SHA
             spec:
               containers:
               - name: app
                 image: $IMAGE_NAME:$CI_COMMIT_SHA
                 imagePullPolicy: Always
                 ports:
                 - containerPort: 3000
                   name: http
                 env:
                 - name: NODE_ENV
                   value: "review"
                 - name: DATABASE_URL
                   value: "postgresql://review_user:review_pass@postgres-service:5432/review_$CI_MERGE_REQUEST_IID"
                 - name: REDIS_URL
                   value: "redis://redis-service:6379/$(($CI_MERGE_REQUEST_IID % 16))"
                 - name: API_BASE_URL
                   value: "$REVIEW_URL/api"
                 - name: REVIEW_APP
                   value: "true"
                 - name: BUILD_VERSION
                   value: "$CI_COMMIT_SHA"
                 - name: MERGE_REQUEST_IID
                   value: "$CI_MERGE_REQUEST_IID"
                 resources:
                   requests:
                     memory: "128Mi"
                     cpu: "100m"
                   limits:
                     memory: "256Mi"
                     cpu: "200m"
                 readinessProbe:
                   httpGet:
                     path: /health
                     port: 3000
                   initialDelaySeconds: 10
                   periodSeconds: 5
                   timeoutSeconds: 3
                 livenessProbe:
                   httpGet:
                     path: /health
                     port: 3000
                   initialDelaySeconds: 30
                   periodSeconds: 10
                   timeoutSeconds: 5
               imagePullSecrets:
               - name: gitlab-registry
         ---
         apiVersion: v1
         kind: Service
         metadata:
           name: $REVIEW_APP_NAME-service
           namespace: $KUBE_NAMESPACE
           labels:
             app: $REVIEW_APP_NAME
         spec:
           type: ClusterIP
           ports:
           - port: 80
             targetPort: 3000
             protocol: TCP
             name: http
           selector:
             app: $REVIEW_APP_NAME
         ---
         apiVersion: networking.k8s.io/v1
         kind: Ingress
         metadata:
           name: $REVIEW_APP_NAME-ingress
           namespace: $KUBE_NAMESPACE
           labels:
             app: $REVIEW_APP_NAME
           annotations:
             kubernetes.io/ingress.class: nginx
             cert-manager.io/cluster-issuer: letsencrypt-prod
             nginx.ingress.kubernetes.io/ssl-redirect: "true"
             nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
             nginx.ingress.kubernetes.io/proxy-body-size: "50m"
             nginx.ingress.kubernetes.io/configuration-snippet: |
               add_header X-Review-App "$CI_MERGE_REQUEST_IID" always;
               add_header X-Build-Version "$CI_COMMIT_SHA" always;
         spec:
           tls:
           - hosts:
             - $CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN
             secretName: $REVIEW_APP_NAME-tls
           rules:
           - host: $CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN
             http:
               paths:
               - path: /
                 pathType: Prefix
                 backend:
                   service:
                     name: $REVIEW_APP_NAME-service
                     port:
                       number: 80
         EOF

       # Appliquer le manifeste
       - kubectl apply -f review-app-manifest.yml

       # Attendre que le déploiement soit prêt
       - kubectl rollout status deployment/$REVIEW_APP_NAME -n $KUBE_NAMESPACE --timeout=300s

       # Tests de santé
       - echo "🔍 Tests de santé de la Review App"
       - sleep 30
       - |
         for i in {1..10}; do
           if curl -f -s "$REVIEW_URL/health" > /dev/null; then
             echo "✅ Review App accessible: $REVIEW_URL"
             break
           fi
           echo "⏳ Tentative $i/10..."
           sleep 15
         done

       # Notification Slack
       - |
         curl -X POST -H 'Content-type: application/json' \
           --data "{
             \"text\":\"🚀 Review App déployée\",
             \"attachments\":[{
               \"color\":\"good\",
               \"fields\":[
                 {\"title\":\"URL\",\"value\":\"$REVIEW_URL\",\"short\":true},
                 {\"title\":\"MR\",\"value\":\"!$CI_MERGE_REQUEST_IID\",\"short\":true},
                 {\"title\":\"Branch\",\"value\":\"$CI_COMMIT_REF_NAME\",\"short\":true},
                 {\"title\":\"Commit\",\"value\":\"$CI_COMMIT_SHA\",\"short\":true}
               ]
             }]
           }" \
           $SLACK_WEBHOOK_URL || true

     environment:
       name: review/$CI_MERGE_REQUEST_IID
       url: $REVIEW_URL
       on_stop: stop_review_app
       auto_stop_in: 3 days
     artifacts:
       paths:
         - review-app-manifest.yml
       expire_in: 1 week
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"

   # Arrêt automatique Review App
   stop_review_app:
     stage: cleanup
     image: bitnami/kubectl:latest
     variables:
       REVIEW_APP_NAME: 'app-$CI_MERGE_REQUEST_IID'
       KUBE_NAMESPACE: 'review-apps'
       GIT_STRATEGY: none
     before_script:
       - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority-data="$KUBE_CA_PEM"
       - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
       - kubectl config set-context default --cluster=k8s --user=gitlab --namespace="$KUBE_NAMESPACE"
       - kubectl config use-context default
     script:
       - echo "🗑️ Suppression Review App: $REVIEW_APP_NAME"
       - kubectl delete deployment,service,ingress -l app=$REVIEW_APP_NAME -n $KUBE_NAMESPACE || true
       - kubectl delete secret $REVIEW_APP_NAME-tls -n $KUBE_NAMESPACE || true
       - echo "✅ Review App supprimée"

       # Notification Slack
       - |
         curl -X POST -H 'Content-type: application/json' \
           --data "{
             \"text\":\"🗑️ Review App supprimée\",
             \"attachments\":[{
               \"color\":\"warning\",
               \"fields\":[
                 {\"title\":\"MR\",\"value\":\"!$CI_MERGE_REQUEST_IID\",\"short\":true},
                 {\"title\":\"App\",\"value\":\"$REVIEW_APP_NAME\",\"short\":true}
               ]
             }]
           }" \
           $SLACK_WEBHOOK_URL || true

     environment:
       name: review/$CI_MERGE_REQUEST_IID
       action: stop
     when: manual
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
   ```

### 1.2 Base de données dédiée par Review App

**Solution : Provisioning automatique de bases de données**

1. **Script de gestion des bases de données**

   ```bash
   #!/bin/bash
   # review-db-manager.sh

   set -e

   DB_HOST="postgres-review.example.com"
   DB_ADMIN_USER="postgres"
   DB_ADMIN_PASSWORD="$POSTGRES_ADMIN_PASSWORD"

   log() {
       echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
   }

   create_review_database() {
       local mr_iid=$1
       local db_name="review_$mr_iid"
       local db_user="review_user_$mr_iid"
       local db_password=$(openssl rand -base64 32)

       log "📦 Création base de données pour MR #$mr_iid"

       # Connexion PostgreSQL admin
       export PGPASSWORD="$DB_ADMIN_PASSWORD"

       # Créer la base de données
       psql -h "$DB_HOST" -U "$DB_ADMIN_USER" -c "
         CREATE DATABASE \"$db_name\"
         WITH OWNER = $DB_ADMIN_USER
         ENCODING = 'UTF8'
         LC_COLLATE = 'en_US.UTF-8'
         LC_CTYPE = 'en_US.UTF-8';
       " || log "⚠️ Base $db_name existe déjà"

       # Créer l'utilisateur dédié
       psql -h "$DB_HOST" -U "$DB_ADMIN_USER" -c "
         CREATE USER \"$db_user\" WITH PASSWORD '$db_password';
         GRANT ALL PRIVILEGES ON DATABASE \"$db_name\" TO \"$db_user\";
       " || log "⚠️ Utilisateur $db_user existe déjà"

       # Initialiser le schéma
       if [ -f "database/schema.sql" ]; then
           log "🔧 Initialisation du schéma"
           PGPASSWORD="$db_password" psql -h "$DB_HOST" -U "$db_user" -d "$db_name" -f "database/schema.sql"
       fi

       # Données de test
       if [ -f "database/test-data.sql" ]; then
           log "📊 Insertion des données de test"
           PGPASSWORD="$db_password" psql -h "$DB_HOST" -U "$db_user" -d "$db_name" -f "database/test-data.sql"
       fi

       # Sauvegarder les credentials
       cat > "review-db-$mr_iid.env" << EOF
   DATABASE_URL=postgresql://$db_user:$db_password@$DB_HOST:5432/$db_name
   DB_NAME=$db_name
   DB_USER=$db_user
   DB_PASSWORD=$db_password
   DB_HOST=$DB_HOST
   DB_PORT=5432
   EOF

       log "✅ Base de données créée: $db_name"
   }

   cleanup_review_database() {
       local mr_iid=$1
       local db_name="review_$mr_iid"
       local db_user="review_user_$mr_iid"

       log "🗑️ Suppression base de données pour MR #$mr_iid"

       export PGPASSWORD="$DB_ADMIN_PASSWORD"

       # Forcer la déconnexion des sessions actives
       psql -h "$DB_HOST" -U "$DB_ADMIN_USER" -c "
         SELECT pg_terminate_backend(pid)
         FROM pg_stat_activity
         WHERE datname = '$db_name' AND pid <> pg_backend_pid();
       " 2>/dev/null || true

       # Supprimer la base et l'utilisateur
       psql -h "$DB_HOST" -U "$DB_ADMIN_USER" -c "
         DROP DATABASE IF EXISTS \"$db_name\";
         DROP USER IF EXISTS \"$db_user\";
       "

       # Nettoyer les fichiers
       rm -f "review-db-$mr_iid.env"

       log "✅ Base de données supprimée: $db_name"
   }

   case "$1" in
       "create")
           create_review_database "$2"
           ;;
       "cleanup")
           cleanup_review_database "$2"
           ;;
       *)
           echo "Usage: $0 {create|cleanup} <mr_iid>"
           exit 1
           ;;
   esac
   ```

2. **Intégration dans le pipeline**

   ```yaml
   # Job de préparation de la base de données
   prepare_review_db:
     stage: review
     image: postgres:13
     before_script:
       - apt-get update && apt-get install -y openssl
       - chmod +x scripts/review-db-manager.sh
     script:
       - ./scripts/review-db-manager.sh create "$CI_MERGE_REQUEST_IID"
     artifacts:
       paths:
         - review-db-$CI_MERGE_REQUEST_IID.env
       expire_in: 3 days
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
     needs: []

   # Mise à jour du job Review App pour utiliser la DB
   review_app:
     stage: review
     # ... configuration précédente
     before_script:
       - kubectl config set-cluster k8s --server="$KUBE_URL" --certificate-authority-data="$KUBE_CA_PEM"
       - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
       - kubectl config set-context default --cluster=k8s --user=gitlab --namespace="$KUBE_NAMESPACE"
       - kubectl config use-context default
       # Charger les variables de la base de données
       - source review-db-$CI_MERGE_REQUEST_IID.env
       - export DATABASE_URL
     script:
       # Dans le manifeste, utiliser $DATABASE_URL au lieu de la valeur hardcodée
       # ... reste du script
     needs:
       - job: build
         artifacts: true
       - job: prepare_review_db
         artifacts: true
   ```

## Exercice 2 : Tests automatisés End-to-End (25 points)

### 2.1 Tests E2E avec Cypress

**Solution complète : Tests E2E automatisés dans Review Apps**

1. **Configuration Cypress avancée**

   ```javascript
   // cypress.config.js
   const {defineConfig} = require('cypress');

   module.exports = defineConfig({
     e2e: {
       baseUrl: process.env.CYPRESS_BASE_URL || 'http://localhost:3000',
       viewportWidth: 1280,
       viewportHeight: 720,
       video: true,
       screenshot: true,
       screenshotOnRunFailure: true,
       videoCompression: 32,
       videosFolder: 'cypress/videos',
       screenshotsFolder: 'cypress/screenshots',
       supportFile: 'cypress/support/e2e.js',
       specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',

       setupNodeEvents(on, config) {
         // Plugins
         require('cypress-mochawesome-reporter/plugin')(on);

         // Configuration dynamique par environnement
         if (config.env.review_app) {
           config.baseUrl = config.env.review_url;
           config.env.api_url = `${config.env.review_url}/api`;
         }

         // Gestion des échecs
         on('task', {
           log(message) {
             console.log(message);
             return null;
           },

           // Notification Slack en cas d'échec
           notifySlack(data) {
             const {url, status, error} = data;

             if (process.env.SLACK_WEBHOOK_URL) {
               const payload = {
                 text: '🚨 Tests E2E échoués',
                 attachments: [
                   {
                     color: 'danger',
                     fields: [
                       {title: 'URL', value: url, short: true},
                       {title: 'Status', value: status, short: true},
                       {title: 'Error', value: error, short: false}
                     ]
                   }
                 ]
               };

               require('axios')
                 .post(process.env.SLACK_WEBHOOK_URL, payload)
                 .catch((err) =>
                   console.log('Slack notification failed:', err.message)
                 );
             }

             return null;
           }
         });

         return config;
       }
     },

     component: {
       devServer: {
         framework: 'react',
         bundler: 'vite'
       }
     }
   });
   ```

2. **Tests E2E pour Review Apps**

   ```javascript
   // cypress/e2e/review-app.cy.js
   describe('Review App - Tests critiques', () => {
     beforeEach(() => {
       // Configuration pour Review App
       cy.visit('/');

       // Vérifier que c'est bien une Review App
       cy.window().then((win) => {
         expect(win.location.hostname).to.include(
           Cypress.env('CI_MERGE_REQUEST_IID')
         );
       });
     });

     it("🏠 Page d'accueil se charge correctement", () => {
       cy.get('[data-testid="app-header"]').should('be.visible');
       cy.get('[data-testid="main-content"]').should('be.visible');
       cy.get('[data-testid="footer"]').should('be.visible');

       // Vérifier les méta-données de build
       cy.get('meta[name="build-version"]').should(
         'have.attr',
         'content',
         Cypress.env('CI_COMMIT_SHA')
       );
     });

     it('🔐 Authentification complète', () => {
       // Test de connexion
       cy.get('[data-testid="login-btn"]').click();
       cy.get('[data-testid="email-input"]').type('test@example.com');
       cy.get('[data-testid="password-input"]').type('password123');
       cy.get('[data-testid="submit-login"]').click();

       // Vérifier la redirection post-connexion
       cy.url().should('include', '/dashboard');
       cy.get('[data-testid="user-menu"]').should('be.visible');

       // Vérifier les données utilisateur
       cy.get('[data-testid="user-name"]').should('contain', 'Test User');
     });

     it('📊 API fonctionne correctement', () => {
       // Test d'appel API
       cy.request({
         method: 'GET',
         url: `${Cypress.env('api_url')}/health`,
         failOnStatusCode: false
       }).then((response) => {
         expect(response.status).to.eq(200);
         expect(response.body).to.have.property('status', 'ok');
         expect(response.body).to.have.property('version');
         expect(response.body).to.have.property('environment', 'review');
       });

       // Test d'API avec authentification
       cy.window().then((win) => {
         const token = win.localStorage.getItem('auth_token');
         if (token) {
           cy.request({
             method: 'GET',
             url: `${Cypress.env('api_url')}/user/profile`,
             headers: {
               Authorization: `Bearer ${token}`
             }
           }).then((response) => {
             expect(response.status).to.eq(200);
             expect(response.body).to.have.property('id');
             expect(response.body).to.have.property('email');
           });
         }
       });
     });

     it('🛍️ Workflow e-commerce complet', () => {
       // Connexion
       cy.login('customer@example.com', 'password123');

       // Navigation vers catalogue
       cy.get('[data-testid="catalog-link"]').click();
       cy.url().should('include', '/catalog');

       // Recherche de produit
       cy.get('[data-testid="search-input"]').type('laptop');
       cy.get('[data-testid="search-btn"]').click();
       cy.get('[data-testid="product-card"]').should('have.length.at.least', 1);

       // Ajout au panier
       cy.get('[data-testid="product-card"]')
         .first()
         .within(() => {
           cy.get('[data-testid="add-to-cart"]').click();
         });

       // Vérification panier
       cy.get('[data-testid="cart-icon"]').click();
       cy.get('[data-testid="cart-items"]').should('have.length', 1);

       // Processus de commande
       cy.get('[data-testid="checkout-btn"]').click();
       cy.url().should('include', '/checkout');

       // Remplir informations de livraison
       cy.get('[data-testid="shipping-form"]').within(() => {
         cy.get('input[name="firstName"]').type('John');
         cy.get('input[name="lastName"]').type('Doe');
         cy.get('input[name="address"]').type('123 Test Street');
         cy.get('input[name="city"]').type('Test City');
         cy.get('input[name="zipCode"]').type('12345');
       });

       // Finaliser commande (sans vraie transaction)
       cy.get('[data-testid="place-order"]').click();
       cy.get('[data-testid="order-confirmation"]').should('be.visible');
       cy.get('[data-testid="order-number"]').should('exist');
     });

     it('📱 Responsive Design', () => {
       // Test desktop
       cy.viewport(1280, 720);
       cy.get('[data-testid="desktop-nav"]').should('be.visible');
       cy.get('[data-testid="mobile-menu"]').should('not.be.visible');

       // Test tablet
       cy.viewport(768, 1024);
       cy.get('[data-testid="main-content"]').should('be.visible');

       // Test mobile
       cy.viewport(375, 667);
       cy.get('[data-testid="mobile-menu"]').should('be.visible');
       cy.get('[data-testid="mobile-menu"]').click();
       cy.get('[data-testid="mobile-nav"]').should('be.visible');
     });

     it('⚡ Performance et accessibilité', () => {
       // Test de performance basique
       cy.window().then((win) => {
         cy.wrap(win.performance.timing).should('exist');

         const loadTime =
           win.performance.timing.loadEventEnd -
           win.performance.timing.navigationStart;
         expect(loadTime).to.be.lessThan(5000); // 5 secondes max
       });

       // Tests d'accessibilité basiques
       cy.get('img').each(($img) => {
         cy.wrap($img).should('have.attr', 'alt');
       });

       cy.get('button, a').each(($el) => {
         cy.wrap($el).should('be.visible');
         cy.wrap($el).should('not.have.css', 'font-size', '0px');
       });
     });

     afterEach(() => {
       // Collecte des métriques
       cy.window().then((win) => {
         const performance = win.performance.timing;
         const metrics = {
           loadTime: performance.loadEventEnd - performance.navigationStart,
           domReady:
             performance.domContentLoadedEventEnd - performance.navigationStart,
           firstPaint: performance.responseStart - performance.navigationStart
         };

         cy.task('log', `Métriques de performance: ${JSON.stringify(metrics)}`);
       });
     });
   });

   // cypress/support/commands.js
   Cypress.Commands.add('login', (email, password) => {
     cy.session([email, password], () => {
       cy.visit('/login');
       cy.get('[data-testid="email-input"]').type(email);
       cy.get('[data-testid="password-input"]').type(password);
       cy.get('[data-testid="submit-login"]').click();
       cy.url().should('include', '/dashboard');
     });
   });
   ```

3. **Job GitLab CI pour tests E2E**

   ```yaml
   # Tests E2E sur Review App
   e2e_tests_review:
     stage: review
     image: cypress/included:12.17.0
     variables:
       CYPRESS_BASE_URL: 'https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN'
       CYPRESS_RECORD_KEY: '$CYPRESS_RECORD_KEY'
     script:
       - echo "🧪 Exécution tests E2E sur Review App"
       - echo "URL cible: $CYPRESS_BASE_URL"

       # Attendre que la Review App soit disponible
       - |
         for i in {1..20}; do
           if curl -f -s "$CYPRESS_BASE_URL/health" > /dev/null; then
             echo "✅ Review App accessible"
             break
           fi
           echo "⏳ Attente Review App... ($i/20)"
           sleep 15
         done

       # Configuration environnement Cypress
       - export CYPRESS_CI_MERGE_REQUEST_IID="$CI_MERGE_REQUEST_IID"
       - export CYPRESS_CI_COMMIT_SHA="$CI_COMMIT_SHA"
       - export CYPRESS_review_app=true
       - export CYPRESS_review_url="$CYPRESS_BASE_URL"
       - export CYPRESS_api_url="$CYPRESS_BASE_URL/api"

       # Exécution des tests avec recording
       - |
         if [ -n "$CYPRESS_RECORD_KEY" ]; then
           npx cypress run \
             --record \
             --key "$CYPRESS_RECORD_KEY" \
             --tag "review-app,mr-$CI_MERGE_REQUEST_IID" \
             --group "Review App Tests" \
             --parallel \
             --ci-build-id "$CI_PIPELINE_ID-$CI_MERGE_REQUEST_IID"
         else
           npx cypress run
         fi

     artifacts:
       when: always
       paths:
         - cypress/videos/
         - cypress/screenshots/
         - cypress/reports/
       reports:
         junit: cypress/results/junit.xml
       expire_in: 1 week

     coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'

     retry:
       max: 1
       when:
         - runner_system_failure
         - stuck_or_timeout_failure

     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"

     needs:
       - job: review_app
         artifacts: false

     allow_failure: false
   ```

## Exercice 3 : Notifications et intégrations (20 points)

### 3.1 Notifications Slack/Teams avancées

**Solution : Système de notifications intelligent**

1. **Script de notifications enrichies**

   ```bash
   #!/bin/bash
   # smart-notifications.sh

   set -e

   # Configuration
   SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL"
   TEAMS_WEBHOOK_URL="$TEAMS_WEBHOOK_URL"
   JIRA_API_URL="$JIRA_API_URL"
   JIRA_TOKEN="$JIRA_TOKEN"

   send_slack_notification() {
       local event_type=$1
       local status=$2
       local mr_data=$3

       case "$event_type" in
           "review_app_deployed")
               local color="good"
               local emoji="🚀"
               local title="Review App Déployée"
               ;;
           "tests_passed")
               local color="good"
               local emoji="✅"
               local title="Tests Réussis"
               ;;
           "tests_failed")
               local color="danger"
               local emoji="❌"
               local title="Tests Échoués"
               ;;
           "review_app_expired")
               local color="warning"
               local emoji="⏰"
               local title="Review App Expirée"
               ;;
       esac

       # Parse MR data
       local mr_title=$(echo "$mr_data" | jq -r '.title')
       local mr_author=$(echo "$mr_data" | jq -r '.author.name')
       local mr_url=$(echo "$mr_data" | jq -r '.web_url')
       local review_url="https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN"

       # Construire payload Slack enrichi
       local payload=$(cat << EOF
   {
     "username": "GitLab CI/CD",
     "icon_emoji": ":gitlab:",
     "text": "$emoji $title",
     "attachments": [
       {
         "color": "$color",
         "title": "$mr_title",
         "title_link": "$mr_url",
         "fields": [
           {
             "title": "Auteur",
             "value": "$mr_author",
             "short": true
           },
           {
             "title": "Branche",
             "value": "$CI_COMMIT_REF_NAME",
             "short": true
           },
           {
             "title": "Pipeline",
             "value": "<$CI_PIPELINE_URL|#$CI_PIPELINE_ID>",
             "short": true
           },
           {
             "title": "Commit",
             "value": "<$CI_PROJECT_URL/-/commit/$CI_COMMIT_SHA|${CI_COMMIT_SHA:0:8}>",
             "short": true
           }
         ],
         "actions": [
           {
             "type": "button",
             "text": "🔍 Voir Review App",
             "url": "$review_url"
           },
           {
             "type": "button",
             "text": "📋 Voir MR",
             "url": "$mr_url"
           },
           {
             "type": "button",
             "text": "📊 Pipeline",
             "url": "$CI_PIPELINE_URL"
           }
         ],
         "footer": "GitLab CI/CD",
         "footer_icon": "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png",
         "ts": $(date +%s)
       }
     ]
   }
   EOF
   )

       # Envoyer la notification
       curl -X POST \
            -H 'Content-type: application/json' \
            --data "$payload" \
            "$SLACK_WEBHOOK_URL"
   }

   send_teams_notification() {
       local event_type=$1
       local status=$2
       local mr_data=$3

       case "$event_type" in
           "review_app_deployed")
               local color="28a745"
               local title="🚀 Review App Déployée"
               ;;
           "tests_failed")
               local color="dc3545"
               local title="❌ Tests Échoués"
               ;;
       esac

       local mr_title=$(echo "$mr_data" | jq -r '.title')
       local mr_author=$(echo "$mr_data" | jq -r '.author.name')
       local mr_url=$(echo "$mr_data" | jq -r '.web_url')
       local review_url="https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN"

       local payload=$(cat << EOF
   {
     "@type": "MessageCard",
     "@context": "http://schema.org/extensions",
     "themeColor": "$color",
     "summary": "$title",
     "sections": [{
       "activityTitle": "$title",
       "activitySubtitle": "$mr_title",
       "activityImage": "https://about.gitlab.com/images/press/logo/png/gitlab-icon-rgb.png",
       "facts": [
         {"name": "Auteur", "value": "$mr_author"},
         {"name": "Branche", "value": "$CI_COMMIT_REF_NAME"},
         {"name": "Pipeline", "value": "#$CI_PIPELINE_ID"},
         {"name": "Commit", "value": "${CI_COMMIT_SHA:0:8}"}
       ],
       "markdown": true
     }],
     "potentialAction": [
       {
         "@type": "OpenUri",
         "name": "Voir Review App",
         "targets": [{"os": "default", "uri": "$review_url"}]
       },
       {
         "@type": "OpenUri",
         "name": "Voir MR",
         "targets": [{"os": "default", "uri": "$mr_url"}]
       }
     ]
   }
   EOF
   )

       curl -X POST \
            -H 'Content-Type: application/json' \
            --data "$payload" \
            "$TEAMS_WEBHOOK_URL"
   }

   update_jira_ticket() {
       local mr_data=$1
       local review_url="https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN"

       # Extraire le numéro de ticket JIRA depuis le titre/branche
       local jira_ticket=$(echo "$CI_COMMIT_REF_NAME" | grep -oP '[A-Z]+-\d+' | head -1)

       if [ -n "$jira_ticket" ]; then
           echo "🎫 Mise à jour ticket JIRA: $jira_ticket"

           local comment=$(cat << EOF
   h3. 🚀 Review App Déployée

   *Pipeline:* [$CI_PIPELINE_ID|$CI_PIPELINE_URL]
   *Branche:* $CI_COMMIT_REF_NAME
   *Commit:* [$CI_COMMIT_SHA|$CI_PROJECT_URL/-/commit/$CI_COMMIT_SHA]

   *Review App:* [$review_url|$review_url]

   La Review App est maintenant disponible pour test et validation.
   EOF
   )

           curl -X POST \
                -H "Authorization: Bearer $JIRA_TOKEN" \
                -H "Content-Type: application/json" \
                --data "{
                  \"body\": \"$comment\"
                }" \
                "$JIRA_API_URL/rest/api/3/issue/$jira_ticket/comment"
       fi
   }

   # Récupérer les informations de la MR
   get_mr_data() {
       curl -s --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
            "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID"
   }

   # Fonction principale
   notify() {
       local event_type=$1
       local status=${2:-"success"}

       echo "📢 Envoi notifications pour: $event_type ($status)"

       # Récupérer les données de la MR
       local mr_data=$(get_mr_data)

       # Envoyer notifications selon les canaux configurés
       if [ -n "$SLACK_WEBHOOK_URL" ]; then
           send_slack_notification "$event_type" "$status" "$mr_data"
       fi

       if [ -n "$TEAMS_WEBHOOK_URL" ]; then
           send_teams_notification "$event_type" "$status" "$mr_data"
       fi

       if [ -n "$JIRA_API_URL" ] && [ -n "$JIRA_TOKEN" ]; then
           update_jira_ticket "$mr_data"
       fi

       echo "✅ Notifications envoyées"
   }

   # Exécution
   notify "$@"
   ```

2. **Intégration dans les jobs GitLab CI**

   ```yaml
   # Job de notification après déploiement Review App
   notify_review_deployed:
     stage: review
     image: alpine:latest
     before_script:
       - apk add --no-cache curl jq
       - chmod +x scripts/smart-notifications.sh
     script:
       - ./scripts/smart-notifications.sh "review_app_deployed" "success"
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
     needs:
       - job: review_app
     when: on_success
     allow_failure: true

   # Job de notification si tests échouent
   notify_tests_failed:
     stage: .post
     image: alpine:latest
     before_script:
       - apk add --no-cache curl jq
       - chmod +x scripts/smart-notifications.sh
     script:
       - ./scripts/smart-notifications.sh "tests_failed" "failure"
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
         when: on_failure
     allow_failure: true
   ```

## Exercice 4 : Optimisation des workflows (25 points)

### 4.1 Pipeline parallélisation et optimisation

**Solution : Optimisation avancée des pipelines**

1. **Configuration pipeline optimisée**

   ```yaml
   # Pipeline ultra-optimisé pour Review Apps
   stages:
     - prepare
     - build
     - test
     - security
     - review
     - notify
     - cleanup

   # Variables globales optimisées
   variables:
     DOCKER_DRIVER: overlay2
     DOCKER_TLS_CERTDIR: "/certs"
     FF_USE_FASTZIP: "true"
     ARTIFACT_COMPRESSION_LEVEL: "fast"
     CACHE_COMPRESSION_LEVEL: "fast"
     GIT_CLEAN_FLAGS: -ffdx -e node_modules/ -e .npm/

   # Cache global
   .cache_template: &cache_template
     key:
       files:
         - package-lock.json
         - yarn.lock
       prefix: $CI_JOB_NAME
     paths:
       - node_modules/
       - .npm/
       - .yarn-cache/
     policy: pull-push

   # Template de base
   .base_job: &base_job
     image: node:18-alpine
     cache: *cache_template
     before_script:
       - npm ci --cache .npm --prefer-offline

   # Préparation des dépendances (job unique)
   prepare_dependencies:
     stage: prepare
     <<: *base_job
     script:
       - echo "📦 Installation des dépendances"
       - npm ci --cache .npm --prefer-offline
       - npm run postinstall || true
     cache:
       <<: *cache_template
       policy: push
     artifacts:
       paths:
         - node_modules/
       expire_in: 1 hour
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == "main"
       - if: $CI_COMMIT_BRANCH == "develop"

   # Build optimisé avec cache Docker
   build_optimized:
     stage: build
     image: docker:20.10.16
     services:
       - docker:20.10.16-dind
     variables:
       DOCKER_BUILDKIT: 1
       BUILDKIT_PROGRESS: plain
     before_script:
       - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
       - docker info
     script:
       - echo "🔨 Build optimisé avec BuildKit"
       - |
         # Multi-stage build avec cache mount
         docker build \
           --build-arg BUILDKIT_INLINE_CACHE=1 \
           --build-arg NODE_ENV=production \
           --cache-from $CI_REGISTRY_IMAGE:cache-deps \
           --cache-from $CI_REGISTRY_IMAGE:cache-build \
           --cache-from $CI_REGISTRY_IMAGE:cache-runtime \
           --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA \
           --tag $CI_REGISTRY_IMAGE:latest \
           --target production \
           --push \
           .

       # Push cache layers
       - |
         docker build \
           --target dependencies \
           --cache-from $CI_REGISTRY_IMAGE:cache-deps \
           --tag $CI_REGISTRY_IMAGE:cache-deps \
           --push \
           . || true

         docker build \
           --target builder \
           --cache-from $CI_REGISTRY_IMAGE:cache-build \
           --tag $CI_REGISTRY_IMAGE:cache-build \
           --push \
           . || true

     needs:
       - job: prepare_dependencies
         artifacts: false

     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
       - if: $CI_COMMIT_BRANCH == "main"
       - if: $CI_COMMIT_BRANCH == "develop"

   # Tests parallélisés
   test_unit:
     stage: test
     <<: *base_job
     script:
       - echo "🧪 Tests unitaires"
       - npm run test:unit -- --coverage --ci --maxWorkers=2
     coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
     artifacts:
       reports:
         junit: junit.xml
         coverage_report:
           coverage_format: cobertura
           path: coverage/cobertura.xml
       paths:
         - coverage/
     parallel:
       matrix:
         - TEST_SUITE: [unit-auth, unit-api, unit-utils, unit-components]
     script:
       - npm run test:unit:$TEST_SUITE -- --coverage --ci
     needs:
       - job: prepare_dependencies
         artifacts: true

   test_integration:
     stage: test
     <<: *base_job
     services:
       - postgres:13
       - redis:6-alpine
     variables:
       POSTGRES_DB: test_db
       POSTGRES_USER: test_user
       POSTGRES_PASSWORD: test_pass
       DATABASE_URL: postgresql://test_user:test_pass@postgres:5432/test_db
       REDIS_URL: redis://redis:6379
     script:
       - echo "🔗 Tests d'intégration"
       - npm run test:integration -- --ci --maxWorkers=1
     artifacts:
       reports:
         junit: integration-junit.xml
     needs:
       - job: prepare_dependencies
         artifacts: true

   test_lint:
     stage: test
     <<: *base_job
     script:
       - echo "📏 Linting"
       - npm run lint -- --format junit --output-file lint-report.xml
       - npm run prettier:check
       - npm run type-check
     artifacts:
       reports:
         junit: lint-report.xml
     needs:
       - job: prepare_dependencies
         artifacts: true

   # Scan sécurité parallélisé
   security_sast:
     stage: security
     image: registry.gitlab.com/gitlab-org/security-products/analyzers/semgrep:latest
     script:
       - echo "🔒 Analyse SAST"
       - /analyzer run
     artifacts:
       reports:
         sast: gl-sast-report.json
     needs: []
     rules:
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"

   security_dependency:
     stage: security
     <<: *base_job
     script:
       - echo "📦 Audit des dépendances"
       - npm audit --audit-level=high --json > npm-audit.json || true
       - npx audit-ci --high --json-report
     artifacts:
       reports:
         dependency_scanning: npm-audit.json
     needs:
       - job: prepare_dependencies
         artifacts: true

   # Review App optimisée
   review_app_optimized:
     stage: review
     image: bitnami/kubectl:latest
     variables:
       REVIEW_APP_NAME: "app-$CI_MERGE_REQUEST_IID"
       REVIEW_URL: "https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN"
       KUBE_NAMESPACE: "review-apps"
     script:
       - echo "🚀 Déploiement Review App optimisé"

       # Configuration Kubernetes optimisée
       - |
         cat > review-app-optimized.yml << EOF
         apiVersion: apps/v1
         kind: Deployment
         metadata:
           name: $REVIEW_APP_NAME
           namespace: $KUBE_NAMESPACE
           labels:
             app: $REVIEW_APP_NAME
             version: $CI_COMMIT_SHA
         spec:
           replicas: 1
           strategy:
             type: RollingUpdate
             rollingUpdate:
               maxSurge: 1
               maxUnavailable: 0
           selector:
             matchLabels:
               app: $REVIEW_APP_NAME
           template:
             metadata:
               labels:
                 app: $REVIEW_APP_NAME
                 version: $CI_COMMIT_SHA
             spec:
               containers:
               - name: app
                 image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
                 imagePullPolicy: Always
                 ports:
                 - containerPort: 3000
                 env:
                 - name: NODE_ENV
                   value: "review"
                 - name: REVIEW_APP
                   value: "true"
                 resources:
                   requests:
                     memory: "64Mi"
                     cpu: "50m"
                   limits:
                     memory: "128Mi"
                     cpu: "100m"
                 readinessProbe:
                   httpGet:
                     path: /health
                     port: 3000
                   initialDelaySeconds: 5
                   periodSeconds: 5
                   timeoutSeconds: 3
                 livenessProbe:
                   httpGet:
                     path: /health
                     port: 3000
                   initialDelaySeconds: 15
                   periodSeconds: 10
         EOF

       - kubectl apply -f review-app-optimized.yml
       - kubectl rollout status deployment/$REVIEW_APP_NAME -n $KUBE_NAMESPACE --timeout=180s

     environment:
       name: review/$CI_MERGE_REQUEST_IID
       url: $REVIEW_URL
       on_stop: stop_review_app
       auto_stop_in: 2 days

     needs:
       - job: build_optimized
         artifacts: false
       - job: test_unit
         artifacts: false
       - job: test_integration
         artifacts: false
       - job: security_sast
         artifacts: false

   # E2E tests optimisés
   e2e_critical_path:
     stage: review
     image: cypress/included:12.17.0
     variables:
       CYPRESS_BASE_URL: "https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN"
     script:
       - echo "🧪 Tests E2E - Parcours critiques"
       - npx cypress run --spec "cypress/e2e/critical/**/*"
     artifacts:
       when: always
       paths:
         - cypress/videos/
         - cypress/screenshots/
       expire_in: 3 days
     parallel: 2
     needs:
       - job: review_app_optimized

   # Nettoyage automatique des anciennes Review Apps
   cleanup_old_review_apps:
     stage: cleanup
     image: bitnami/kubectl:latest
     variables:
       KUBE_NAMESPACE: "review-apps"
       MAX_AGE_DAYS: 7
     script:
       - echo "🧹 Nettoyage des anciennes Review Apps"
       - |
         # Supprimer les déploiements plus anciens que MAX_AGE_DAYS
         kubectl get deployments -n $KUBE_NAMESPACE -o json | \
         jq -r ".items[] | select(.metadata.creationTimestamp | fromdateiso8601 < (now - ($MAX_AGE_DAYS * 86400))) | .metadata.name" | \
         xargs -r kubectl delete deployment -n $KUBE_NAMESPACE

         # Supprimer les services orphelins
         kubectl get services -n $KUBE_NAMESPACE -o json | \
         jq -r '.items[] | select(.metadata.labels.app | startswith("app-")) | select(.spec.selector.app as $app | [.spec.selector.app] | inside([.metadata.labels.app]) | not) | .metadata.name' | \
         xargs -r kubectl delete service -n $KUBE_NAMESPACE

     rules:
       - if: $CI_PIPELINE_SOURCE == "schedule"
       - if: $CI_PIPELINE_SOURCE == "merge_request_event"
         when: manual
         allow_failure: true
   ```

### Points d'évaluation totaux

- **Configuration Review Apps** : 30/30 points
- **Tests E2E automatisés** : 25/25 points
- **Notifications et intégrations** : 20/20 points
- **Optimisation workflows** : 25/25 points

**Total** : 100/100 points

---

**Note** : Cette correction présente des solutions de niveau industriel pour l'automatisation des Review Apps et l'optimisation des workflows collaboratifs. Les techniques utilisées sont directement applicables en environnement de production pour améliorer la vélocité des équipes de développement.
