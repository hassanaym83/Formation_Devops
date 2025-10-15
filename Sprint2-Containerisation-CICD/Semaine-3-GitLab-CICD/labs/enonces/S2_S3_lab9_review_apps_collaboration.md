# LAB 9 - ÉNONCÉ : Review Apps et Collaboration

## Objectifs pédagogiques

À la fin de ce lab, vous serez capable de :

- Configurer des Review Apps automatiques pour chaque merge request
- Implémenter des workflows collaboratifs avec GitLab
- Gérer le cycle de vie des environnements dynamiques
- Intégrer des notifications et des commentaires automatiques
- Optimiser les coûts et performances des Review Apps

## Contexte du lab

Les Review Apps permettent de :

- **Validation** : Tester visuellement chaque changement avant fusion
- **Collaboration** : Faciliter la revue de code avec un environnement live
- **Intégration** : Valider l'intégration complète des fonctionnalités
- **Feedback** : Accélérer les cycles de retour et d'amélioration

## Prérequis

- LAB 8 terminé (environments et déploiements)
- Application React avec pipeline GitLab CI/CD
- Connaissance des merge requests GitLab
- Notions de Docker et environnements ephémères

## Architecture Review Apps

```
┌─────────────────────────────────────────────────────────────┐
│                     GitLab Repository                      │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ Feature/123   │  │ Feature/456   │  │ Feature/789   │   │
│  │ (MR !123)     │  │ (MR !456)     │  │ (MR !789)     │   │
│  └───────────────┘  └───────────────┘  └───────────────┘   │
└─────────────┬─────────────────┬─────────────────┬─────────────┘
              │                 │                 │
              ▼                 ▼                 ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │   Review App    │ │   Review App    │ │   Review App    │
    │ review-123.app  │ │ review-456.app  │ │ review-789.app  │
    │  [Auto Deploy]  │ │  [Auto Deploy]  │ │  [Auto Deploy]  │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
              │                 │                 │
              ▼                 ▼                 ▼
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │  Auto Cleanup   │ │  Auto Cleanup   │ │  Auto Cleanup   │
    │  [After Merge]  │ │  [After Merge]  │ │  [After Merge]  │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

## Exercice 1 : Configuration Review Apps de base (25 points)

### 1.1 Préparation de l'environnement

**Votre tâche : Préparer le projet pour les Review Apps**

1. **Configuration Docker avancée**

   Créez `Dockerfile.review` optimisé pour les Review Apps :

   ```dockerfile
   # Image de base légère
   FROM node:18-alpine AS base

   # Installer les dépendances système
   RUN apk add --no-cache \
       curl \
       git \
       && rm -rf /var/cache/apk/*

   WORKDIR /app

   # Stage dependencies
   FROM base AS deps
   COPY package*.json ./
   RUN npm ci --only=production \
       && npm cache clean --force

   # Stage build
   FROM base AS build
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   # Stage finale pour Review App
   FROM nginx:alpine AS review

   # Configuration Nginx pour SPA
   COPY --from=build /app/dist /usr/share/nginx/html
   COPY nginx.review.conf /etc/nginx/conf.d/default.conf

   # Script de santé personnalisé
   COPY healthcheck.sh /usr/local/bin/
   RUN chmod +x /usr/local/bin/healthcheck.sh

   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD /usr/local/bin/healthcheck.sh

   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Configuration Nginx pour Review Apps**

   Créez `nginx.review.conf` :

   ```nginx
   server {
       listen 80;
       server_name _;
       root /usr/share/nginx/html;
       index index.html;

       # Configuration SPA
       location / {
           try_files $uri $uri/ /index.html;
       }

       # Headers de sécurité
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-Content-Type-Options "nosniff" always;
       add_header X-XSS-Protection "1; mode=block" always;

       # Cache pour assets statiques
       location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
           expires 1y;
           add_header Cache-Control "public, immutable";
       }

       # Health check endpoint
       location /health {
           access_log off;
           return 200 "healthy\n";
           add_header Content-Type text/plain;
       }

       # Pas de cache pour index.html
       location = /index.html {
           add_header Cache-Control "no-cache, no-store, must-revalidate";
       }
   }
   ```

3. **Script de santé**

   Créez `healthcheck.sh` :

   ```bash
   #!/bin/sh

   # Test connectivité
   curl -f http://localhost/health > /dev/null 2>&1 || exit 1

   # Test présence index.html
   [ -f /usr/share/nginx/html/index.html ] || exit 1

   # Test Nginx process
   pgrep nginx > /dev/null || exit 1

   echo "Health check passed"
   exit 0
   ```

### 1.2 Pipeline Review Apps

**Votre tâche : Configurer le pipeline pour Review Apps**

Modifiez `.gitlab-ci.yml` :

```yaml
stages:
  - validate
  - build
  - test
  - review
  - deploy
  - cleanup

variables:
  # Configuration générale
  DOCKER_REGISTRY: $CI_REGISTRY
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  REVIEW_DOMAIN: 'review-apps.example.com'

  # Configuration Review Apps
  REVIEW_APP_NAME: 'review-$CI_MERGE_REQUEST_IID'
  REVIEW_APP_URL: 'https://$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN'

# Template pour Review Apps
.review_template: &review_template
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  only:
    - merge_requests
  except:
    - main

# Build image pour Review App
build_review:
  <<: *review_template
  stage: build
  script:
    # Build image Review App
    - |
      docker build \
        -f Dockerfile.review \
        --build-arg BUILD_ENV=review \
        --build-arg API_URL=$REVIEW_API_URL \
        --tag $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID \
        --tag $IMAGE_NAME/review:mr-$CI_MERGE_REQUEST_IID-$CI_COMMIT_SHORT_SHA \
        .

    # Push vers registry
    - docker push $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID
    - docker push $IMAGE_NAME/review:mr-$CI_MERGE_REQUEST_IID-$CI_COMMIT_SHORT_SHA

    # Scan sécurité rapide
    - |
      docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy:latest image \
        --severity HIGH,CRITICAL \
        --exit-code 0 \
        $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID

  artifacts:
    reports:
      container_scanning: trivy-report.json
    expire_in: 1 day

# Tests spécifiques Review App
test_review_app:
  <<: *review_template
  stage: test
  needs: [build_review]
  script:
    # Test de l'image Review App
    - |
      docker run -d --name test-review \
        -p 8080:80 \
        $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID

    # Attendre que le service soit prêt
    - sleep 10

    # Tests de santé
    - curl -f http://localhost:8080/health
    - curl -f http://localhost:8080/ | grep -q "<!DOCTYPE html>"

    # Nettoyage
    - docker stop test-review
    - docker rm test-review

# Déploiement Review App
deploy_review:
  <<: *review_template
  stage: review
  needs: [build_review, test_review_app]
  script:
    # Déploiement avec Docker Compose
    - |
      cat > docker-compose.review.yml << EOF
      version: '3.8'
      services:
        review-app:
          image: $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID
          container_name: $REVIEW_APP_NAME
          ports:
            - "80:80"
          environment:
            - NODE_ENV=review
            - API_URL=$REVIEW_API_URL
            - SENTRY_ENVIRONMENT=review-$CI_MERGE_REQUEST_IID
          labels:
            - "traefik.enable=true"
            - "traefik.http.routers.$REVIEW_APP_NAME.rule=Host(\`$CI_MERGE_REQUEST_IID.$REVIEW_DOMAIN\`)"
            - "traefik.http.routers.$REVIEW_APP_NAME.entrypoints=web"
          restart: unless-stopped
          healthcheck:
            test: ["CMD", "/usr/local/bin/healthcheck.sh"]
            interval: 30s
            timeout: 10s
            retries: 3
            start_period: 40s
      EOF

    # Déploiement
    - docker-compose -f docker-compose.review.yml up -d

    # Vérification déploiement
    - |
      for i in {1..30}; do
        if curl -f $REVIEW_APP_URL/health > /dev/null 2>&1; then
          echo "✅ Review App déployée avec succès"
          break
        fi
        echo "⏳ Attente du déploiement... ($i/30)"
        sleep 10
      done

    # Commentaire automatique MR
    - |
      curl -X POST \
        -H "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
          \"body\": \"🚀 **Review App déployée !**\n\n📱 **URL**: $REVIEW_APP_URL\n🔗 **Image**: \`$IMAGE_NAME/review:$CI_MERGE_REQUEST_IID\`\n⏰ **Déployé le**: $(date)\n\n---\n*Cette Review App sera automatiquement supprimée à la fermeture de la MR.*\"
        }" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"

  environment:
    name: review/$CI_MERGE_REQUEST_IID
    url: $REVIEW_APP_URL
    on_stop: stop_review
    auto_stop_in: 7 days

# Arrêt Review App
stop_review:
  <<: *review_template
  stage: cleanup
  variables:
    GIT_STRATEGY: none
  script:
    # Arrêt et suppression du conteneur
    - docker stop $REVIEW_APP_NAME || true
    - docker rm $REVIEW_APP_NAME || true

    # Nettoyage des images
    - docker rmi $IMAGE_NAME/review:$CI_MERGE_REQUEST_IID || true

    # Commentaire automatique MR
    - |
      curl -X POST \
        -H "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
          \"body\": \"🗑️ **Review App supprimée**\n\nL'environnement de test a été nettoyé automatiquement.\"
        }" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes" || true

  environment:
    name: review/$CI_MERGE_REQUEST_IID
    action: stop
  when: manual
  allow_failure: true
```

### 1.3 Points d'évaluation Exercice 1 (25 points)

- [ ] **Dockerfile.review optimisé** (5 points)
- [ ] **Configuration Nginx appropriée** (5 points)
- [ ] **Script healthcheck fonctionnel** (3 points)
- [ ] **Pipeline Review Apps configuré** (7 points)
- [ ] **Déploiement automatique MR** (3 points)
- [ ] **Cleanup automatique** (2 points)

## Exercice 2 : Workflows collaboratifs avancés (25 points)

### 2.1 Notifications et intégrations

**Votre tâche : Automatiser les notifications et commentaires**

1. **Script de notifications avancées**

   Créez `scripts/review-notifications.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   PROJECT_ID="$CI_PROJECT_ID"
   MR_IID="$CI_MERGE_REQUEST_IID"
   API_TOKEN="$GITLAB_API_TOKEN"
   API_URL="$CI_API_V4_URL"
   REVIEW_URL="$REVIEW_APP_URL"

   # Fonction pour poster un commentaire
   post_comment() {
       local message="$1"
       local comment_body=$(cat <<EOF
   {
     "body": "$message"
   }
   EOF
   )

       curl -s -X POST \
           -H "PRIVATE-TOKEN: $API_TOKEN" \
           -H "Content-Type: application/json" \
           -d "$comment_body" \
           "$API_URL/projects/$PROJECT_ID/merge_requests/$MR_IID/notes"
   }

   # Fonction pour obtenir les détails de la MR
   get_mr_details() {
       curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
           "$API_URL/projects/$PROJECT_ID/merge_requests/$MR_IID"
   }

   # Fonction pour générer le rapport de déploiement
   generate_deployment_report() {
       local mr_details=$(get_mr_details)
       local author=$(echo "$mr_details" | jq -r '.author.name')
       local title=$(echo "$mr_details" | jq -r '.title')
       local source_branch=$(echo "$mr_details" | jq -r '.source_branch')
       local target_branch=$(echo "$mr_details" | jq -r '.target_branch')

       local report=$(cat <<EOF
   ## 🚀 Review App Déployée

   ### 📋 Informations
   - **Auteur**: $author
   - **Titre**: $title
   - **Branche**: \`$source_branch\` → \`$target_branch\`
   - **Commit**: \`$CI_COMMIT_SHORT_SHA\`
   - **Pipeline**: [#$CI_PIPELINE_ID]($CI_PIPELINE_URL)

   ### 🔗 Liens utiles
   - 🌐 **Review App**: [$REVIEW_URL]($REVIEW_URL)
   - 📊 **Logs**: [$CI_JOB_URL]($CI_JOB_URL)
   - 🐳 **Image**: \`$IMAGE_NAME/review:$MR_IID\`

   ### ✅ Tests automatiques
   - [x] Build réussi
   - [x] Tests passés
   - [x] Scan sécurité OK
   - [x] Health check OK

   ### 🎯 Actions recommandées
   1. Tester les fonctionnalités ajoutées/modifiées
   2. Vérifier la responsivité sur différents appareils
   3. Valider l'accessibilité
   4. Tester les cas d'erreur

   ---
   *🤖 Commentaire automatique généré le $(date)*
   *⚡ Cette Review App sera automatiquement supprimée à la fermeture de la MR*
   EOF
   )

       echo "$report"
   }

   # Action en fonction du paramètre
   case "${1:-deploy}" in
       "deploy")
           message=$(generate_deployment_report)
           post_comment "$message"
           echo "✅ Notification de déploiement envoyée"
           ;;
       "cleanup")
           message="🗑️ **Review App supprimée**\n\nL'environnement de test a été nettoyé automatiquement.\n\n*Merci d'avoir utilisé la Review App !*"
           post_comment "$message"
           echo "✅ Notification de nettoyage envoyée"
           ;;
       "error")
           message="❌ **Erreur lors du déploiement de la Review App**\n\nVeuillez vérifier les logs du pipeline : [$CI_JOB_URL]($CI_JOB_URL)\n\n*Contactez l'équipe DevOps si le problème persiste.*"
           post_comment "$message"
           echo "✅ Notification d'erreur envoyée"
           ;;
       *)
           echo "Usage: $0 {deploy|cleanup|error}"
           exit 1
           ;;
   esac
   ```

2. **Intégration Slack/Teams**

   Créez `scripts/slack-notification.sh` :

   ```bash
   #!/bin/bash

   # Configuration Slack
   SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL"

   # Fonction pour envoyer notification Slack
   send_slack_notification() {
       local status="$1"
       local color="$2"
       local pretext="$3"

       local payload=$(cat <<EOF
   {
     "attachments": [
       {
         "color": "$color",
         "pretext": "$pretext",
         "fields": [
           {
             "title": "Projet",
             "value": "$CI_PROJECT_NAME",
             "short": true
           },
           {
             "title": "Branche",
             "value": "$CI_COMMIT_REF_NAME",
             "short": true
           },
           {
             "title": "Auteur",
             "value": "$GITLAB_USER_NAME",
             "short": true
           },
           {
             "title": "Commit",
             "value": "$CI_COMMIT_SHORT_SHA",
             "short": true
           },
           {
             "title": "Review App",
             "value": "<$REVIEW_APP_URL|Voir l'application>",
             "short": false
           },
           {
             "title": "Pipeline",
             "value": "<$CI_PIPELINE_URL|#$CI_PIPELINE_ID>",
             "short": true
           }
         ],
         "footer": "GitLab CI/CD",
         "ts": $(date +%s)
       }
     ]
   }
   EOF
   )

       curl -X POST \
           -H 'Content-type: application/json' \
           --data "$payload" \
           "$SLACK_WEBHOOK_URL"
   }

   # Action selon le statut
   case "${1:-success}" in
       "success")
           send_slack_notification "success" "good" "✅ Review App déployée avec succès !"
           ;;
       "failure")
           send_slack_notification "failure" "danger" "❌ Échec du déploiement de la Review App"
           ;;
       "cleanup")
           send_slack_notification "cleanup" "warning" "🗑️ Review App supprimée"
           ;;
   esac
   ```

### 2.2 Tests automatisés des Review Apps

**Votre tâche : Implémenter des tests automatiques sur les Review Apps**

1. **Tests E2E avec Cypress**

   Créez `cypress/e2e/review-app.cy.js` :

   ```javascript
   describe('Review App E2E Tests', () => {
     const baseUrl = Cypress.env('REVIEW_APP_URL') || 'http://localhost:3000';

     beforeEach(() => {
       cy.visit(baseUrl);
     });

     describe('Navigation et UI', () => {
       it("devrait charger la page d'accueil", () => {
         cy.get('h1').should('be.visible');
         cy.title().should('not.be.empty');
       });

       it('devrait avoir un header responsive', () => {
         cy.get('header').should('be.visible');

         // Test mobile
         cy.viewport('iphone-6');
         cy.get('header').should('be.visible');

         // Test desktop
         cy.viewport(1280, 720);
         cy.get('header').should('be.visible');
       });

       it('devrait naviguer entre les pages', () => {
         cy.get('[data-testid="nav-about"]').click();
         cy.url().should('include', '/about');
         cy.go('back');
         cy.url().should('eq', baseUrl + '/');
       });
     });

     describe('Fonctionnalités métier', () => {
       it('devrait permettre la recherche', () => {
         cy.get('[data-testid="search-input"]').type('test search');
         cy.get('[data-testid="search-button"]').click();
         cy.get('[data-testid="search-results"]').should('be.visible');
       });

       it('devrait gérer les formulaires', () => {
         cy.get('[data-testid="contact-form"]').within(() => {
           cy.get('input[name="name"]').type('Test User');
           cy.get('input[name="email"]').type('test@example.com');
           cy.get('textarea[name="message"]').type('Test message');
           cy.get('button[type="submit"]').click();
         });

         cy.get('[data-testid="success-message"]').should('be.visible');
       });
     });

     describe('Performance et accessibilité', () => {
       it('devrait charger en moins de 3 secondes', () => {
         cy.visit(baseUrl, {
           onBeforeLoad: (win) => {
             win.performance.mark('start');
           },
           onLoad: (win) => {
             win.performance.mark('end');
             win.performance.measure('pageLoad', 'start', 'end');
             const measure = win.performance.getEntriesByName('pageLoad')[0];
             expect(measure.duration).to.be.lessThan(3000);
           }
         });
       });

       it('devrait être accessible', () => {
         cy.injectAxe();
         cy.checkA11y();
       });
     });

     describe('APIs et intégrations', () => {
       it('devrait avoir un endpoint de santé', () => {
         cy.request(baseUrl + '/health').then((response) => {
           expect(response.status).to.eq(200);
           expect(response.body).to.include('healthy');
         });
       });

       it('devrait gérer les erreurs API', () => {
         cy.intercept('GET', '/api/data', {statusCode: 500}).as('apiError');
         cy.get('[data-testid="load-data"]').click();
         cy.wait('@apiError');
         cy.get('[data-testid="error-message"]').should('be.visible');
       });
     });
   });
   ```

2. **Configuration Cypress pour Review Apps**

   Créez `cypress.review.config.js` :

   ```javascript
   const {defineConfig} = require('cypress');

   module.exports = defineConfig({
     e2e: {
       baseUrl: process.env.REVIEW_APP_URL || 'http://localhost:3000',
       supportFile: 'cypress/support/e2e.js',
       specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
       video: true,
       screenshotOnRunFailure: true,

       // Configuration pour CI
       browser: 'chrome',
       headless: true,

       // Timeouts adaptés aux Review Apps
       defaultCommandTimeout: 10000,
       requestTimeout: 10000,
       responseTimeout: 10000,
       pageLoadTimeout: 30000,

       // Variables d'environnement
       env: {
         REVIEW_APP_URL: process.env.REVIEW_APP_URL,
         API_URL: process.env.API_URL
       },

       setupNodeEvents(on, config) {
         // Plugin pour rapport JUnit
         require('cypress-junit-reporter/src/plugin')(on);

         // Plugin pour accessibilité
         require('cypress-axe/src/plugin')(on);

         return config;
       }
     },

     reporter: 'cypress-multi-reporters',
     reporterOptions: {
       configFile: 'cypress-reporter-config.json'
     }
   });
   ```

3. **Job de test E2E Review App**

   Ajoutez dans `.gitlab-ci.yml` :

   ```yaml
   # Tests E2E sur Review App
   test_e2e_review:
     stage: test
     image: cypress/included:12.0.0
     needs: [deploy_review]
     variables:
       CYPRESS_baseUrl: $REVIEW_APP_URL
       CYPRESS_RECORD_KEY: $CYPRESS_RECORD_KEY
     script:
       # Attendre que la Review App soit prête
       - |
         echo "🔄 Attente de la Review App..."
         for i in {1..30}; do
           if curl -f $REVIEW_APP_URL/health > /dev/null 2>&1; then
             echo "✅ Review App prête"
             break
           fi
           echo "⏳ Tentative $i/30..."
           sleep 10
         done

       # Installation des dépendances si nécessaire
       - npm ci

       # Lancement des tests E2E
       - npx cypress run --config-file cypress.review.config.js

     artifacts:
       when: always
       paths:
         - cypress/videos/
         - cypress/screenshots/
         - cypress/reports/
       reports:
         junit: cypress/reports/junit/*.xml
       expire_in: 7 days

     only:
       - merge_requests

     allow_failure: true # Ne pas bloquer la MR si tests E2E échouent
   ```

### 2.3 Points d'évaluation Exercice 2 (25 points)

- [ ] **Script notifications avancées** (7 points)
- [ ] **Intégration Slack/Teams** (5 points)
- [ ] **Tests E2E Cypress configurés** (8 points)
- [ ] **Configuration Cypress appropriée** (3 points)
- [ ] **Job test E2E fonctionnel** (2 points)

## Exercice 3 : Optimisation et gestion du cycle de vie (25 points)

### 3.1 Optimisation des performances et coûts

**Votre tâche : Optimiser les Review Apps pour les performances et les coûts**

1. **Configuration de mise en cache intelligente**

   Créez `scripts/smart-cache.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   REGISTRY="$CI_REGISTRY"
   PROJECT="$CI_PROJECT_PATH"
   BRANCH="$CI_COMMIT_REF_SLUG"
   MR_IID="$CI_MERGE_REQUEST_IID"

   # Fonction de nettoyage des images anciennes
   cleanup_old_images() {
       echo "🧹 Nettoyage des images anciennes..."

       # Supprimer les images de plus de 7 jours
       docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}" \
           | grep "$REGISTRY/$PROJECT/review" \
           | awk '$3 ~ /[0-9]+ (day|week|month)s? ago/ && $3 !~ /[0-6] days? ago/ {print $1":"$2}' \
           | xargs -r docker rmi || true
   }

   # Fonction d'optimisation de la taille d'image
   optimize_image() {
       local image="$1"

       echo "🔧 Optimisation de l'image $image"

       # Analyse avec dive
       docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
           wagoodman/dive:latest "$image" --json > dive-analysis.json

       # Extraction des métriques
       local efficiency=$(cat dive-analysis.json | jq -r '.efficiency')
       local wasted_bytes=$(cat dive-analysis.json | jq -r '.wastedBytes')

       echo "📊 Efficacité de l'image: $efficiency"
       echo "💾 Bytes gaspillés: $wasted_bytes"

       # Alerte si efficacité < 95%
       if (( $(echo "$efficiency < 0.95" | bc -l) )); then
           echo "⚠️ Efficacité de l'image faible. Optimisation recommandée."
       fi
   }

   # Fonction de cache intelligent
   smart_cache_strategy() {
       local cache_key="review-$MR_IID-$BRANCH"
       local fallback_key="review-main"

       echo "🎯 Stratégie de cache: $cache_key"

       # Essayer de récupérer le cache spécifique
       if docker pull "$REGISTRY/$PROJECT/cache:$cache_key" 2>/dev/null; then
           echo "✅ Cache spécifique trouvé"
           export CACHE_FROM="--cache-from $REGISTRY/$PROJECT/cache:$cache_key"
       elif docker pull "$REGISTRY/$PROJECT/cache:$fallback_key" 2>/dev/null; then
           echo "📦 Cache fallback utilisé"
           export CACHE_FROM="--cache-from $REGISTRY/$PROJECT/cache:$fallback_key"
       else
           echo "🆕 Pas de cache disponible"
           export CACHE_FROM=""
       fi
   }

   # Fonction de monitoring des ressources
   monitor_resources() {
       echo "📊 Monitoring des ressources..."

       # Usage Docker
       docker system df

       # Usage disque
       df -h

       # Mémoire
       free -h

       # Alertes si usage > 80%
       local disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
       if [ "$disk_usage" -gt 80 ]; then
           echo "⚠️ ALERTE: Usage disque élevé ($disk_usage%)"
       fi
   }

   # Exécution des fonctions
   case "${1:-all}" in
       "cleanup")
           cleanup_old_images
           ;;
       "optimize")
           optimize_image "$2"
           ;;
       "cache")
           smart_cache_strategy
           ;;
       "monitor")
           monitor_resources
           ;;
       "all")
           cleanup_old_images
           smart_cache_strategy
           monitor_resources
           ;;
       *)
           echo "Usage: $0 {cleanup|optimize|cache|monitor|all}"
           exit 1
           ;;
   esac
   ```

2. **Configuration auto-scaling des Review Apps**

   Créez `docker-compose.review-optimized.yml` :

   ```yaml
   version: '3.8'

   services:
     review-app:
       image: ${IMAGE_NAME}/review:${CI_MERGE_REQUEST_IID}
       container_name: ${REVIEW_APP_NAME}

       # Configuration des ressources
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
           reservations:
             cpus: '0.1'
             memory: 128M
         restart_policy:
           condition: unless-stopped
           delay: 5s
           max_attempts: 3
           window: 120s

       # Variables d'environnement optimisées
       environment:
         - NODE_ENV=review
         - API_URL=${REVIEW_API_URL}
         - SENTRY_ENVIRONMENT=review-${CI_MERGE_REQUEST_IID}
         - MEMORY_LIMIT=512
         - CPU_LIMIT=0.5

         # Configuration cache
         - REDIS_URL=${REDIS_URL}
         - CACHE_TTL=300

         # Configuration monitoring
         - METRICS_ENABLED=true
         - LOG_LEVEL=info

       # Labels pour monitoring et routing
       labels:
         - 'traefik.enable=true'
         - 'traefik.http.routers.${REVIEW_APP_NAME}.rule=Host(`${CI_MERGE_REQUEST_IID}.${REVIEW_DOMAIN}`)'
         - 'traefik.http.routers.${REVIEW_APP_NAME}.entrypoints=web'

         # Configuration cache et compression
         - 'traefik.http.middlewares.${REVIEW_APP_NAME}-compress.compress=true'
         - 'traefik.http.middlewares.${REVIEW_APP_NAME}-cache.headers.customResponseHeaders.Cache-Control=public, max-age=3600'
         - 'traefik.http.routers.${REVIEW_APP_NAME}.middlewares=${REVIEW_APP_NAME}-compress,${REVIEW_APP_NAME}-cache'

         # Labels monitoring
         - 'monitoring.type=review-app'
         - 'monitoring.mr=${CI_MERGE_REQUEST_IID}'
         - 'monitoring.project=${CI_PROJECT_NAME}'

       # Health check optimisé
       healthcheck:
         test: ['CMD-SHELL', 'curl -f http://localhost/health || exit 1']
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s

       # Logs optimisés
       logging:
         driver: 'json-file'
         options:
           max-size: '10m'
           max-file: '3'

       # Sécurité
       security_opt:
         - no-new-privileges:true
       read_only: true
       tmpfs:
         - /tmp
         - /var/cache/nginx

     # Service de cache Redis partagé (optionnel)
     redis-cache:
       image: redis:7-alpine
       container_name: ${REVIEW_APP_NAME}-redis
       command: redis-server --maxmemory 64mb --maxmemory-policy allkeys-lru

       deploy:
         resources:
           limits:
             cpus: '0.1'
             memory: 64M
           reservations:
             cpus: '0.05'
             memory: 32M

       volumes:
         - redis-cache:/data

       healthcheck:
         test: ['CMD', 'redis-cli', 'ping']
         interval: 30s
         timeout: 3s
         retries: 3

   volumes:
     redis-cache:
       driver: local

   networks:
     default:
       name: review-network-${CI_MERGE_REQUEST_IID}
   ```

### 3.2 Automatisation de la gestion du cycle de vie

**Votre tâche : Automatiser la gestion complète du cycle de vie des Review Apps**

1. **Script de gestion du cycle de vie**

   Créez `scripts/lifecycle-manager.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   PROJECT_ID="$CI_PROJECT_ID"
   API_TOKEN="$GITLAB_API_TOKEN"
   API_URL="$CI_API_V4_URL"
   MAX_REVIEW_APPS=10
   MAX_AGE_DAYS=7

   # Fonction pour lister les MRs ouvertes
   list_open_mrs() {
       curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
           "$API_URL/projects/$PROJECT_ID/merge_requests?state=opened" \
           | jq -r '.[].iid'
   }

   # Fonction pour lister les environnements Review Apps
   list_review_environments() {
       curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
           "$API_URL/projects/$PROJECT_ID/environments" \
           | jq -r '.[] | select(.name | startswith("review/")) | .name'
   }

   # Fonction pour supprimer un environnement
   delete_environment() {
       local env_name="$1"
       local env_id=$(curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
           "$API_URL/projects/$PROJECT_ID/environments" \
           | jq -r ".[] | select(.name == \"$env_name\") | .id")

       if [ "$env_id" != "null" ] && [ -n "$env_id" ]; then
           curl -s -X DELETE -H "PRIVATE-TOKEN: $API_TOKEN" \
               "$API_URL/projects/$PROJECT_ID/environments/$env_id"
           echo "🗑️ Environnement $env_name supprimé"
       fi
   }

   # Fonction de nettoyage des Review Apps orphelines
   cleanup_orphaned_review_apps() {
       echo "🔍 Recherche des Review Apps orphelines..."

       local open_mrs=($(list_open_mrs))
       local review_envs=($(list_review_environments))

       for env in "${review_envs[@]}"; do
           local mr_iid=$(echo "$env" | sed 's/review\///')

           # Vérifier si la MR existe encore
           if [[ ! " ${open_mrs[@]} " =~ " ${mr_iid} " ]]; then
               echo "🧹 Review App orpheline détectée: $env"

               # Arrêter et supprimer le conteneur
               docker stop "review-$mr_iid" 2>/dev/null || true
               docker rm "review-$mr_iid" 2>/dev/null || true

               # Supprimer l'environnement GitLab
               delete_environment "$env"

               # Supprimer les images
               docker rmi "$CI_REGISTRY_IMAGE/review:$mr_iid" 2>/dev/null || true
           fi
       done
   }

   # Fonction de limitation du nombre de Review Apps
   limit_review_apps() {
       echo "📊 Vérification du nombre de Review Apps..."

       local review_count=$(docker ps --filter "label=monitoring.type=review-app" --format "table {{.Names}}" | wc -l)

       if [ "$review_count" -gt "$MAX_REVIEW_APPS" ]; then
           echo "⚠️ Trop de Review Apps ($review_count > $MAX_REVIEW_APPS)"

           # Supprimer les plus anciennes
           docker ps --filter "label=monitoring.type=review-app" \
               --format "table {{.Names}}\t{{.CreatedAt}}" \
               | sort -k2 \
               | head -n $((review_count - MAX_REVIEW_APPS)) \
               | awk '{print $1}' \
               | xargs -r docker stop

           echo "🧹 Review Apps les plus anciennes supprimées"
       fi
   }

   # Fonction de nettoyage basé sur l'âge
   cleanup_old_review_apps() {
       echo "⏰ Nettoyage des Review Apps anciennes (> $MAX_AGE_DAYS jours)..."

       # Trouver les conteneurs anciens
       local old_containers=$(docker ps --filter "label=monitoring.type=review-app" \
           --format "table {{.Names}}\t{{.CreatedAt}}" \
           | awk -v days="$MAX_AGE_DAYS" '
               /^review-/ {
                   cmd = "date -d \"" $2 " " $3 "\" +%s 2>/dev/null || date -j -f \"%Y-%m-%d %H:%M:%S\" \"" $2 " " $3 "\" +%s"
                   cmd | getline created
                   close(cmd)

                   cmd = "date +%s"
                   cmd | getline now
                   close(cmd)

                   age_days = (now - created) / 86400
                   if (age_days > days) print $1
               }')

       if [ -n "$old_containers" ]; then
           echo "$old_containers" | xargs -r docker stop
           echo "🗑️ Review Apps anciennes supprimées"
       else
           echo "✅ Aucune Review App ancienne trouvée"
       fi
   }

   # Fonction de génération de rapport
   generate_report() {
       echo "📋 Génération du rapport de gestion..."

       local total_review_apps=$(docker ps --filter "label=monitoring.type=review-app" -q | wc -l)
       local total_images=$(docker images | grep "/review:" | wc -l)
       local disk_usage=$(docker system df --format "table {{.Type}}\t{{.Size}}" | grep "Images" | awk '{print $2}')

       local report=$(cat <<EOF
   ## 📊 Rapport Review Apps

   ### 📈 Statistiques
   - **Review Apps actives**: $total_review_apps
   - **Images Review**: $total_images
   - **Usage disque images**: $disk_usage
   - **Date du rapport**: $(date)

   ### 🔧 Actions effectuées
   - Nettoyage des Review Apps orphelines
   - Vérification des limites
   - Suppression des anciennes instances

   ### 💡 Recommandations
   - Limiter les MRs ouvertes simultanément
   - Optimiser la taille des images Docker
   - Surveiller l'usage des ressources
   EOF
   )

       echo "$report"

       # Sauvegarder le rapport
       echo "$report" > "review-apps-report-$(date +%Y%m%d).md"
   }

   # Fonction principale
   main() {
       echo "🚀 Démarrage de la gestion du cycle de vie des Review Apps"

       cleanup_orphaned_review_apps
       limit_review_apps
       cleanup_old_review_apps
       generate_report

       echo "✅ Gestion du cycle de vie terminée"
   }

   # Exécution selon le paramètre
   case "${1:-main}" in
       "cleanup")
           cleanup_orphaned_review_apps
           ;;
       "limit")
           limit_review_apps
           ;;
       "old")
           cleanup_old_review_apps
           ;;
       "report")
           generate_report
           ;;
       "main")
           main
           ;;
       *)
           echo "Usage: $0 {cleanup|limit|old|report|main}"
           exit 1
           ;;
   esac
   ```

2. **Job de maintenance automatique**

   Ajoutez dans `.gitlab-ci.yml` :

   ```yaml
   # Maintenance des Review Apps (job schedulé)
   review_apps_maintenance:
     stage: .post
     image: docker:20.10.16
     services:
       - docker:20.10.16-dind
     script:
       # Préparation
       - apk add --no-cache curl jq bc
       - chmod +x scripts/lifecycle-manager.sh scripts/smart-cache.sh

       # Exécution de la maintenance
       - ./scripts/smart-cache.sh cleanup
       - ./scripts/lifecycle-manager.sh main

       # Monitoring des ressources
       - ./scripts/smart-cache.sh monitor

       # Génération du rapport final
       - |
         echo "## 🎯 Résumé de la maintenance" >> maintenance-report.md
         echo "- **Date**: $(date)" >> maintenance-report.md
         echo "- **Review Apps actives**: $(docker ps --filter 'label=monitoring.type=review-app' -q | wc -l)" >> maintenance-report.md
         echo "- **Images nettoyées**: Oui" >> maintenance-report.md
         echo "- **Ressources optimisées**: Oui" >> maintenance-report.md

     artifacts:
       paths:
         - '*.md'
       expire_in: 30 days

     rules:
       # Exécuter tous les jours à 2h du matin
       - if: $CI_PIPELINE_SOURCE == "schedule"
       # Ou manuellement
       - when: manual
         allow_failure: true
   ```

### 3.3 Points d'évaluation Exercice 3 (25 points)

- [ ] **Script smart-cache fonctionnel** (8 points)
- [ ] **Configuration auto-scaling** (5 points)
- [ ] **Script lifecycle-manager complet** (8 points)
- [ ] **Job maintenance automatique** (3 points)
- [ ] **Monitoring et rapports** (1 point)

## Livrables et évaluation finale

### Livrables attendus (100 points total)

1. **Configuration Review Apps complète** (25 points)

   - Dockerfile.review optimisé
   - Configuration Nginx appropriée
   - Pipeline automatisé
   - Scripts de déploiement/cleanup

2. **Workflows collaboratifs** (25 points)

   - Notifications automatiques avancées
   - Intégrations Slack/Teams
   - Tests E2E automatisés
   - Commentaires MR intelligents

3. **Optimisation et cycle de vie** (25 points)

   - Gestion intelligente du cache
   - Optimisation des ressources
   - Automatisation de la maintenance
   - Monitoring et rapports

4. **Documentation et bonnes pratiques** (25 points)
   - README détaillé des Review Apps
   - Guide d'utilisation pour les développeurs
   - Procédures de débogage
   - Métriques et KPIs

### Critères de réussite

- **Déploiement automatique** : Review App créée automatiquement pour chaque MR
- **Nettoyage automatique** : Suppression automatique à la fermeture de la MR
- **Notifications fonctionnelles** : Commentaires et intégrations actifs
- **Tests automatisés** : Tests E2E qui s'exécutent sur chaque Review App
- **Optimisation des ressources** : Limitation et nettoyage automatique
- **Monitoring opérationnel** : Métriques et alertes configurées

### Bonus (10 points supplémentaires)

- **Intégration advanced** : SSO, authentification, base de données temporaire
- **A/B Testing** : Comparaison automatique entre versions
- **Performance monitoring** : Métriques de performance temps réel
- **Cost optimization** : Stratégies avancées d'économie de ressources

---

**Temps estimé** : 6-8 heures
**Difficulté** : ★★★★☆ (Expert)
**Prérequis** : LABs 1-8 terminés

> **Note importante** : Ce lab simule un environnement de production réel avec Review Apps. Les concepts appris sont directement applicables en entreprise pour améliorer les workflows de développement collaboratif.
