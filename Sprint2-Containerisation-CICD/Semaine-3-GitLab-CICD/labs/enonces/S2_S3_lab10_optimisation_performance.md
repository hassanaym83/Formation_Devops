# LAB 10 - ÉNONCÉ : Optimisation et Performance

## Objectifs pédagogiques

À la fin de ce lab, vous serez capable de :

- Optimiser les performances des pipelines GitLab CI/CD
- Implémenter des stratégies de cache avancées et intelligentes
- Analyser et améliorer les temps d'exécution des jobs
- Configurer le monitoring de performance en temps réel
- Optimiser l'utilisation des ressources et les coûts

## Contexte du lab

L'optimisation des pipelines est cruciale pour :

- **Productivité** : Réduire les temps d'attente des développeurs
- **Coûts** : Optimiser l'utilisation des runners et ressources cloud
- **Scalabilité** : Supporter une équipe et un projet en croissance
- **Qualité** : Maintenir des cycles de feedback rapides

## Prérequis

- LAB 9 terminé (Review Apps et collaboration)
- Pipeline GitLab CI/CD complexe avec multiple stages
- Connaissance des métriques et monitoring
- Notions d'optimisation système

## Architecture d'optimisation

```
┌─────────────────────────────────────────────────────────────┐
│                    Pipeline Optimisé                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Cache L1   │  │  Cache L2   │  │  Cache L3   │        │
│  │ (Project)   │  │ (Branch)    │  │ (Global)    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                │                │               │
│         ▼                ▼                ▼               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Pipeline Parallelisé                  │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │ Build   │ │ Test    │ │ Lint    │ │ Audit   │   │   │
│  │  │ (2min)  │ │ (3min)  │ │ (1min)  │ │ (1min)  │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                             │
│                              ▼                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Monitoring en Temps Réel                │   │
│  │  📊 Métriques  📈 Trends  ⚡ Alertes  🎯 KPIs     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Exercice 1 : Audit et analyse de performance (25 points)

### 1.1 Mise en place de l'audit de pipeline

**Votre tâche : Créer un système d'audit complet des performances**

1. **Script d'analyse de pipeline**

   Créez `scripts/pipeline-analyzer.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   PROJECT_ID="$CI_PROJECT_ID"
   API_TOKEN="$GITLAB_API_TOKEN"
   API_URL="$CI_API_V4_URL"
   ANALYSIS_DAYS=30

   # Fonctions utilitaires
   log() {
       echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
   }

   # Fonction pour récupérer les données de pipelines
   fetch_pipeline_data() {
       local days="$1"
       local since_date=$(date -d "$days days ago" --iso-8601)

       log "📊 Récupération des données de pipelines depuis $since_date"

       curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
           "$API_URL/projects/$PROJECT_ID/pipelines?updated_after=$since_date&per_page=100" \
           > pipelines_data.json

       log "✅ $(cat pipelines_data.json | jq length) pipelines récupérés"
   }

   # Fonction d'analyse des temps d'exécution
   analyze_execution_times() {
       log "⏱️ Analyse des temps d'exécution"

       cat > analyze_times.jq << 'EOF'
   [
     .[] |
     select(.status == "success") |
     {
       id: .id,
       duration: .duration,
       created_at: .created_at,
       ref: .ref,
       jobs_count: (.jobs // [] | length)
     }
   ] |
   {
     total_pipelines: length,
     avg_duration: (map(.duration) | add / length),
     min_duration: (map(.duration) | min),
     max_duration: (map(.duration) | max),
     median_duration: (map(.duration) | sort | .[length/2]),
     pipelines: .
   }
   EOF

       cat pipelines_data.json | jq -f analyze_times.jq > execution_analysis.json

       # Affichage des résultats
       local avg_duration=$(cat execution_analysis.json | jq -r '.avg_duration')
       local min_duration=$(cat execution_analysis.json | jq -r '.min_duration')
       local max_duration=$(cat execution_analysis.json | jq -r '.max_duration')

       log "📈 Durée moyenne: ${avg_duration}s"
       log "⚡ Durée minimale: ${min_duration}s"
       log "🐌 Durée maximale: ${max_duration}s"
   }

   # Fonction d'analyse des jobs les plus lents
   analyze_slow_jobs() {
       log "🔍 Analyse des jobs les plus lents"

       # Récupérer les détails des jobs pour les 10 derniers pipelines
       local pipeline_ids=$(cat pipelines_data.json | jq -r '.[0:10][].id')

       echo "[]" > jobs_data.json

       for pipeline_id in $pipeline_ids; do
           log "📋 Analyse du pipeline $pipeline_id"

           local jobs_response=$(curl -s -H "PRIVATE-TOKEN: $API_TOKEN" \
               "$API_URL/projects/$PROJECT_ID/pipelines/$pipeline_id/jobs")

           # Fusionner avec les données existantes
           echo "$jobs_response" | jq --slurpfile existing jobs_data.json \
               '$existing[0] + .' > jobs_data_temp.json
           mv jobs_data_temp.json jobs_data.json
       done

       # Analyser les jobs les plus lents
       cat > analyze_jobs.jq << 'EOF'
   [
     .[] |
     select(.status == "success" and .duration != null) |
     {
       name: .name,
       stage: .stage,
       duration: .duration,
       runner: .runner.description // "unknown"
     }
   ] |
   group_by(.name) |
   map({
     job_name: .[0].name,
     stage: .[0].stage,
     avg_duration: (map(.duration) | add / length),
     max_duration: (map(.duration) | max),
     runs: length
   }) |
   sort_by(.avg_duration) |
   reverse
   EOF

       cat jobs_data.json | jq -f analyze_jobs.jq > slow_jobs_analysis.json

       # Afficher le top 5 des jobs les plus lents
       log "🐌 Top 5 des jobs les plus lents:"
       cat slow_jobs_analysis.json | jq -r '.[0:5][] | "  \(.job_name): \(.avg_duration)s (stage: \(.stage))"'
   }

   # Fonction d'analyse de l'utilisation du cache
   analyze_cache_efficiency() {
       log "💾 Analyse de l'efficacité du cache"

       # Rechercher les patterns de cache dans les logs
       cat > cache_analysis.jq << 'EOF'
   [
     .[] |
     {
       id: .id,
       duration: .duration,
       ref: .ref,
       has_cache: (if .variables then
         (.variables[] | select(.key == "CACHE_ENABLED" and .value == "true")) != null
       else false end)
     }
   ] |
   {
     with_cache: [.[] | select(.has_cache)] | length,
     without_cache: [.[] | select(.has_cache | not)] | length,
     avg_duration_with_cache: ([.[] | select(.has_cache) | .duration] | if length > 0 then add / length else 0 end),
     avg_duration_without_cache: ([.[] | select(.has_cache | not) | .duration] | if length > 0 then add / length else 0 end)
   }
   EOF

       cat pipelines_data.json | jq -f cache_analysis.jq > cache_efficiency.json

       local with_cache=$(cat cache_efficiency.json | jq -r '.avg_duration_with_cache')
       local without_cache=$(cat cache_efficiency.json | jq -r '.avg_duration_without_cache')

       if [ "$with_cache" != "0" ] && [ "$without_cache" != "0" ]; then
           local improvement=$(echo "scale=2; ($without_cache - $with_cache) / $without_cache * 100" | bc)
           log "📊 Amélioration avec cache: ${improvement}%"
       fi
   }

   # Fonction de génération de rapport
   generate_performance_report() {
       log "📋 Génération du rapport de performance"

       local report_date=$(date '+%Y-%m-%d %H:%M:%S')
       local total_pipelines=$(cat execution_analysis.json | jq -r '.total_pipelines')
       local avg_duration=$(cat execution_analysis.json | jq -r '.avg_duration')

       cat > performance_report.md << EOF
   # 📊 Rapport de Performance Pipeline

   **Généré le**: $report_date
   **Période d'analyse**: $ANALYSIS_DAYS derniers jours
   **Pipelines analysés**: $total_pipelines

   ## ⏱️ Métriques de Performance

   ### Temps d'Exécution
   $(cat execution_analysis.json | jq -r '
   "- **Durée moyenne**: \(.avg_duration // 0)s
   - **Durée minimale**: \(.min_duration // 0)s
   - **Durée maximale**: \(.max_duration // 0)s
   - **Durée médiane**: \(.median_duration // 0)s"')

   ### Jobs les Plus Lents
   $(cat slow_jobs_analysis.json | jq -r '.[0:5][] | "- **\(.job_name)**: \(.avg_duration)s (stage: \(.stage), \(.runs) exécutions)"')

   ### Efficacité du Cache
   $(cat cache_efficiency.json | jq -r '
   "- **Pipelines avec cache**: \(.with_cache)
   - **Pipelines sans cache**: \(.without_cache)
   - **Durée moyenne avec cache**: \(.avg_duration_with_cache)s
   - **Durée moyenne sans cache**: \(.avg_duration_without_cache)s"')

   ## 💡 Recommandations

   ### Actions Prioritaires
   1. **Optimiser les jobs les plus lents** (gain potentiel: 20-30%)
   2. **Améliorer la stratégie de cache** (gain potentiel: 15-25%)
   3. **Paralléliser davantage les stages** (gain potentiel: 10-20%)

   ### Jobs à Optimiser
   $(cat slow_jobs_analysis.json | jq -r '.[0:3][] | "- [ ] **\(.job_name)**: \(.avg_duration)s → objectif: <\(.avg_duration * 0.7 | floor)s"')

   ## 📈 Tendances

   - **Performance globale**: $(if (( $(echo "$avg_duration < 300" | bc -l) )); then echo "✅ Bonne"; else echo "⚠️ À améliorer"; fi)
   - **Utilisation cache**: $(if (( $(cat cache_efficiency.json | jq -r '.with_cache') > $(cat cache_efficiency.json | jq -r '.without_cache') )); then echo "✅ Majoritaire"; else echo "⚠️ Insuffisante"; fi)

   ---
   *Rapport généré automatiquement par le système d'audit de performance*
   EOF

       log "✅ Rapport généré: performance_report.md"
   }

   # Fonction principale
   main() {
       log "🚀 Démarrage de l'audit de performance"

       fetch_pipeline_data "$ANALYSIS_DAYS"
       analyze_execution_times
       analyze_slow_jobs
       analyze_cache_efficiency
       generate_performance_report

       log "✅ Audit de performance terminé"
   }

   # Exécution
   case "${1:-main}" in
       "fetch")
           fetch_pipeline_data "$ANALYSIS_DAYS"
           ;;
       "times")
           analyze_execution_times
           ;;
       "jobs")
           analyze_slow_jobs
           ;;
       "cache")
           analyze_cache_efficiency
           ;;
       "report")
           generate_performance_report
           ;;
       "main")
           main
           ;;
       *)
           echo "Usage: $0 {fetch|times|jobs|cache|report|main}"
           exit 1
           ;;
   esac
   ```

2. **Configuration du monitoring continu**

   Créez `scripts/continuous-monitoring.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
   GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
   ALERT_THRESHOLD_DURATION=600  # 10 minutes

   # Fonction de collecte de métriques
   collect_pipeline_metrics() {
       log "📊 Collecte des métriques de pipeline"

       # Métriques actuelles du pipeline
       cat > pipeline_metrics.prom << EOF
   # HELP gitlab_pipeline_duration_seconds Durée du pipeline en secondes
   # TYPE gitlab_pipeline_duration_seconds gauge
   gitlab_pipeline_duration_seconds{project="$CI_PROJECT_NAME",pipeline="$CI_PIPELINE_ID",branch="$CI_COMMIT_REF_NAME"} $CI_PIPELINE_DURATION

   # HELP gitlab_pipeline_jobs_total Nombre total de jobs dans le pipeline
   # TYPE gitlab_pipeline_jobs_total gauge
   gitlab_pipeline_jobs_total{project="$CI_PROJECT_NAME",pipeline="$CI_PIPELINE_ID"} $CI_PIPELINE_JOB_COUNT

   # HELP gitlab_pipeline_success_rate Taux de succès du pipeline
   # TYPE gitlab_pipeline_success_rate gauge
   gitlab_pipeline_success_rate{project="$CI_PROJECT_NAME",branch="$CI_COMMIT_REF_NAME"} 1

   # HELP gitlab_cache_hit_rate Taux de succès du cache
   # TYPE gitlab_cache_hit_rate gauge
   gitlab_cache_hit_rate{project="$CI_PROJECT_NAME",job="$CI_JOB_NAME"} $CACHE_HIT_RATE
   EOF

       # Envoyer les métriques à Prometheus (via Pushgateway)
       if [ -n "$PROMETHEUS_PUSHGATEWAY_URL" ]; then
           curl -X POST "$PROMETHEUS_PUSHGATEWAY_URL/metrics/job/gitlab-ci/instance/$CI_RUNNER_ID" \
               --data-binary @pipeline_metrics.prom
           log "✅ Métriques envoyées à Prometheus"
       fi
   }

   # Fonction d'alertes automatiques
   check_performance_alerts() {
       log "⚠️ Vérification des alertes de performance"

       # Alerte si durée > seuil
       if [ "$CI_PIPELINE_DURATION" -gt "$ALERT_THRESHOLD_DURATION" ]; then
           send_alert "🐌 Pipeline lent détecté" \
               "Pipeline $CI_PIPELINE_ID trop lent: ${CI_PIPELINE_DURATION}s > ${ALERT_THRESHOLD_DURATION}s"
       fi

       # Alerte si taux d'échec élevé
       local failure_rate=$(calculate_failure_rate)
       if (( $(echo "$failure_rate > 0.2" | bc -l) )); then
           send_alert "❌ Taux d'échec élevé" \
               "Taux d'échec: ${failure_rate}% > 20%"
       fi
   }

   # Fonction de calcul du taux d'échec
   calculate_failure_rate() {
       local failed_jobs=$(echo "$CI_PIPELINE_JOBS" | jq -r '.[] | select(.status == "failed") | length')
       local total_jobs=$(echo "$CI_PIPELINE_JOBS" | jq -r '. | length')

       if [ "$total_jobs" -gt 0 ]; then
           echo "scale=2; $failed_jobs / $total_jobs * 100" | bc
       else
           echo "0"
       fi
   }

   # Fonction d'envoi d'alertes
   send_alert() {
       local title="$1"
       local message="$2"

       # Slack
       if [ -n "$SLACK_WEBHOOK_URL" ]; then
           curl -X POST "$SLACK_WEBHOOK_URL" \
               -H 'Content-type: application/json' \
               --data "{\"text\":\"$title\",\"attachments\":[{\"color\":\"warning\",\"text\":\"$message\"}]}"
       fi

       # Email (via API GitLab)
       if [ -n "$GITLAB_ALERT_EMAIL" ]; then
           curl -X POST \
               -H "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
               -H "Content-Type: application/json" \
               "$CI_API_V4_URL/projects/$CI_PROJECT_ID/issues" \
               -d "{\"title\":\"$title\",\"description\":\"$message\",\"labels\":[\"performance\",\"alert\"]}"
       fi
   }

   # Exécution
   collect_pipeline_metrics
   check_performance_alerts
   ```

### 1.2 Job d'audit dans le pipeline

**Votre tâche : Intégrer l'audit dans le pipeline CI/CD**

Ajoutez dans `.gitlab-ci.yml` :

```yaml
# Stage d'audit de performance
stages:
  - audit
  - build
  - test
  - deploy
  - monitor

# Variables de performance
variables:
  PERFORMANCE_MONITORING: 'true'
  CACHE_HIT_RATE: '0'
  ALERT_THRESHOLD_DURATION: '600'

# Audit de performance pré-build
performance_audit:
  stage: audit
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq bc git
    - chmod +x scripts/pipeline-analyzer.sh
  script:
    # Audit des performances historiques
    - ./scripts/pipeline-analyzer.sh main

    # Vérification des seuils
    - |
      if [ -f execution_analysis.json ]; then
        avg_duration=$(cat execution_analysis.json | jq -r '.avg_duration')
        if (( $(echo "$avg_duration > $ALERT_THRESHOLD_DURATION" | bc -l) )); then
          echo "⚠️ ALERTE: Durée moyenne élevée ($avg_duration s)"
          echo "PERFORMANCE_ALERT=true" >> performance.env
        fi
      fi

    # Recommandations d'optimisation
    - |
      if [ -f slow_jobs_analysis.json ]; then
        echo "📋 Jobs à optimiser en priorité:"
        cat slow_jobs_analysis.json | jq -r '.[0:3][] | "- \(.job_name): \(.avg_duration)s"'
      fi

  artifacts:
    reports:
      dotenv: performance.env
    paths:
      - '*.json'
      - '*.md'
    expire_in: 7 days

  rules:
    - if: $PERFORMANCE_MONITORING == "true"
```

### 1.3 Points d'évaluation Exercice 1 (25 points)

- [ ] **Script pipeline-analyzer complet** (10 points)
- [ ] **Script monitoring continu** (8 points)
- [ ] **Job d'audit intégré** (5 points)
- [ ] **Alertes automatiques** (2 points)

## Exercice 2 : Optimisation du cache intelligent (25 points)

### 2.1 Stratégies de cache multi-niveaux

**Votre tâche : Implémenter un système de cache intelligent à plusieurs niveaux**

1. **Configuration cache hiérarchique**

   Créez `scripts/smart-cache-strategy.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration des niveaux de cache
   CACHE_L1_KEY="l1-${CI_PROJECT_ID}-${CI_COMMIT_REF_SLUG}-${CI_PIPELINE_ID}"
   CACHE_L2_KEY="l2-${CI_PROJECT_ID}-${CI_COMMIT_REF_SLUG}"
   CACHE_L3_KEY="l3-${CI_PROJECT_ID}-main"
   CACHE_FALLBACK_KEY="fallback-${CI_PROJECT_ID}"

   # Chemins de cache
   CACHE_PATHS=(
       "node_modules/"
       ".npm/"
       "vendor/"
       ".composer/"
       "target/"
       ".cargo/"
       ".cache/"
   )

   # Fonction de détection des dépendances
   detect_dependencies() {
       log "🔍 Détection des fichiers de dépendances"

       local dep_files=()

       # Node.js
       [ -f "package-lock.json" ] && dep_files+=("package-lock.json")
       [ -f "yarn.lock" ] && dep_files+=("yarn.lock")

       # PHP
       [ -f "composer.lock" ] && dep_files+=("composer.lock")

       # Python
       [ -f "requirements.txt" ] && dep_files+=("requirements.txt")
       [ -f "Pipfile.lock" ] && dep_files+=("Pipfile.lock")

       # Java
       [ -f "pom.xml" ] && dep_files+=("pom.xml")
       [ -f "build.gradle" ] && dep_files+=("build.gradle")

       # Rust
       [ -f "Cargo.lock" ] && dep_files+=("Cargo.lock")

       echo "${dep_files[@]}"
   }

   # Fonction de génération de hash des dépendances
   generate_dependency_hash() {
       local dep_files=($(detect_dependencies))

       if [ ${#dep_files[@]} -eq 0 ]; then
           echo "no-deps"
           return
       fi

       local combined_hash=""
       for file in "${dep_files[@]}"; do
           if [ -f "$file" ]; then
               local file_hash=$(sha256sum "$file" | cut -d' ' -f1)
               combined_hash="${combined_hash}${file_hash}"
           fi
       done

       echo "$combined_hash" | sha256sum | cut -d' ' -f1 | head -c 12
   }

   # Fonction de cache intelligent
   setup_intelligent_cache() {
       local dep_hash=$(generate_dependency_hash)
       local final_cache_key=""

       log "📦 Configuration du cache intelligent"
       log "🔑 Hash des dépendances: $dep_hash"

       # Stratégie de cache hiérarchique
       cat > .gitlab-ci-cache.yml << EOF
   .cache_strategy:
     cache:
       # Cache niveau 1: Spécifique au pipeline
       - key: "${CACHE_L1_KEY}-${dep_hash}"
         paths: $(printf '"%s" ' "${CACHE_PATHS[@]}")
         policy: pull-push
         when: always

       # Cache niveau 2: Spécifique à la branche
       - key: "${CACHE_L2_KEY}-${dep_hash}"
         paths: $(printf '"%s" ' "${CACHE_PATHS[@]}")
         policy: pull
         when: on_failure

       # Cache niveau 3: Cache global du projet
       - key: "${CACHE_L3_KEY}-${dep_hash}"
         paths: $(printf '"%s" ' "${CACHE_PATHS[@]}")
         policy: pull
         when: on_failure

       # Cache fallback
       - key: "${CACHE_FALLBACK_KEY}"
         paths: $(printf '"%s" ' "${CACHE_PATHS[@]}")
         policy: pull
         when: on_failure
   EOF

       log "✅ Configuration de cache générée"
   }

   # Fonction de warming du cache
   warm_cache() {
       log "🔥 Warming du cache"

       # Identifier les paths qui existent
       local existing_paths=()
       for path in "${CACHE_PATHS[@]}"; do
           if [ -d "$path" ] || [ -f "$path" ]; then
               existing_paths+=("$path")
           fi
       done

       if [ ${#existing_paths[@]} -gt 0 ]; then
           log "📂 Paths de cache trouvés: ${existing_paths[*]}"
           export CACHE_HIT_RATE="1"
       else
           log "❌ Aucun cache trouvé, build complet nécessaire"
           export CACHE_HIT_RATE="0"
       fi
   }

   # Fonction de validation du cache
   validate_cache() {
       log "✅ Validation du cache"

       local cache_valid=true
       local dep_files=($(detect_dependencies))

       for file in "${dep_files[@]}"; do
           if [ -f "$file" ]; then
               local expected_dir=""
               case "$file" in
                   "package-lock.json"|"yarn.lock")
                       expected_dir="node_modules"
                       ;;
                   "composer.lock")
                       expected_dir="vendor"
                       ;;
                   "requirements.txt"|"Pipfile.lock")
                       expected_dir=".venv"
                       ;;
                   "pom.xml"|"build.gradle")
                       expected_dir="target"
                       ;;
                   "Cargo.lock")
                       expected_dir="target"
                       ;;
               esac

               if [ -n "$expected_dir" ] && [ ! -d "$expected_dir" ]; then
                   log "⚠️ Cache invalide pour $file (manque $expected_dir)"
                   cache_valid=false
               fi
           fi
       done

       if [ "$cache_valid" = true ]; then
           log "✅ Cache valide"
           export CACHE_VALIDATION="valid"
       else
           log "❌ Cache invalide, reconstruction nécessaire"
           export CACHE_VALIDATION="invalid"
       fi
   }

   # Fonction de nettoyage du cache
   cleanup_cache() {
       log "🧹 Nettoyage du cache"

       # Nettoyer les caches de plus de 7 jours
       find ~/.cache -type f -mtime +7 -delete 2>/dev/null || true

       # Nettoyer node_modules si package.json a changé
       if [ -f "package.json" ] && [ -f "node_modules/.cache-timestamp" ]; then
           if [ "package.json" -nt "node_modules/.cache-timestamp" ]; then
               log "📦 package.json modifié, nettoyage node_modules"
               rm -rf node_modules/
           fi
       fi

       # Créer timestamp pour le prochain contrôle
       if [ -d "node_modules" ]; then
           touch node_modules/.cache-timestamp
       fi
   }

   # Fonction principale
   main() {
       case "${1:-setup}" in
           "setup")
               setup_intelligent_cache
               ;;
           "warm")
               warm_cache
               ;;
           "validate")
               validate_cache
               ;;
           "cleanup")
               cleanup_cache
               ;;
           "all")
               setup_intelligent_cache
               warm_cache
               validate_cache
               ;;
           *)
               echo "Usage: $0 {setup|warm|validate|cleanup|all}"
               exit 1
               ;;
       esac
   }

   # Exécution
   main "$@"
   ```

2. **Templates de cache optimisés**

   Créez `.gitlab-ci-templates.yml` :

   ```yaml
   # Templates de cache optimisés

   .cache_node: &cache_node
     cache:
       - key:
           files:
             - package-lock.json
           prefix: node-v1
         paths:
           - node_modules/
           - .npm/
         policy: pull-push
       - key: node-fallback-v1
         paths:
           - node_modules/
         policy: pull
         when: on_failure

   .cache_php: &cache_php
     cache:
       - key:
           files:
             - composer.lock
           prefix: php-v1
         paths:
           - vendor/
           - .composer/
         policy: pull-push
       - key: php-fallback-v1
         paths:
           - vendor/
         policy: pull
         when: on_failure

   .cache_python: &cache_python
     cache:
       - key:
           files:
             - requirements.txt
             - Pipfile.lock
           prefix: python-v1
         paths:
           - .venv/
           - .pip-cache/
         policy: pull-push
       - key: python-fallback-v1
         paths:
           - .venv/
         policy: pull
         when: on_failure

   .cache_java: &cache_java
     cache:
       - key:
           files:
             - pom.xml
             - build.gradle
           prefix: java-v1
         paths:
           - target/
           - .m2/repository/
           - .gradle/
         policy: pull-push
       - key: java-fallback-v1
         paths:
           - target/
           - .m2/repository/
         policy: pull
         when: on_failure

   .cache_docker: &cache_docker
     cache:
       - key: docker-layers-${CI_COMMIT_REF_SLUG}
         paths:
           - /var/lib/docker/
         policy: pull-push
       - key: docker-layers-main
         paths:
           - /var/lib/docker/
         policy: pull
         when: on_failure

   # Template d'optimisation générale
   .performance_optimized:
     before_script:
       - echo "🚀 Démarrage optimisation performance"
       - chmod +x scripts/smart-cache-strategy.sh
       - ./scripts/smart-cache-strategy.sh all
       - source performance.env || true
     after_script:
       - echo "📊 Collecte des métriques de performance"
       - echo "CACHE_HIT_RATE=$CACHE_HIT_RATE" >> performance.env
       - echo "JOB_DURATION=$(($(date +%s) - $JOB_START_TIME))" >> performance.env
     artifacts:
       reports:
         dotenv: performance.env
   ```

### 2.2 Cache distribué et partagé

**Votre tâche : Implémenter un système de cache distribué**

1. **Configuration cache externe**

   Créez `scripts/distributed-cache.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Configuration
   S3_BUCKET="${CACHE_S3_BUCKET:-gitlab-ci-cache}"
   REDIS_URL="${CACHE_REDIS_URL:-redis://localhost:6379}"
   CACHE_TTL=86400  # 24 heures

   # Fonction d'upload vers S3
   upload_to_s3() {
       local local_path="$1"
       local s3_key="$2"

       if [ ! -d "$local_path" ] && [ ! -f "$local_path" ]; then
           log "⚠️ Path $local_path n'existe pas"
           return 1
       fi

       log "⬆️ Upload vers S3: $local_path → s3://$S3_BUCKET/$s3_key"

       # Créer une archive
       local archive_name="${s3_key}.tar.gz"
       tar -czf "$archive_name" -C "$(dirname "$local_path")" "$(basename "$local_path")"

       # Upload vers S3
       aws s3 cp "$archive_name" "s3://$S3_BUCKET/$s3_key.tar.gz" \
           --metadata "project=$CI_PROJECT_ID,branch=$CI_COMMIT_REF_NAME,created=$(date +%s)"

       # Nettoyage
       rm -f "$archive_name"

       log "✅ Upload terminé"
   }

   # Fonction de download depuis S3
   download_from_s3() {
       local s3_key="$1"
       local local_path="$2"

       log "⬇️ Download depuis S3: s3://$S3_BUCKET/$s3_key → $local_path"

       # Vérifier si le fichier existe
       if ! aws s3 ls "s3://$S3_BUCKET/$s3_key.tar.gz" > /dev/null 2>&1; then
           log "❌ Fichier non trouvé sur S3"
           return 1
       fi

       # Download et extraction
       local archive_name="${s3_key}.tar.gz"
       aws s3 cp "s3://$S3_BUCKET/$s3_key.tar.gz" "$archive_name"

       # Créer le répertoire parent si nécessaire
       mkdir -p "$(dirname "$local_path")"

       # Extraire
       tar -xzf "$archive_name" -C "$(dirname "$local_path")"

       # Nettoyage
       rm -f "$archive_name"

       log "✅ Download terminé"
   }

   # Fonction de cache Redis pour métadonnées
   cache_metadata_to_redis() {
       local key="$1"
       local metadata="$2"

       if [ -n "$REDIS_URL" ]; then
           echo "$metadata" | redis-cli -u "$REDIS_URL" -x SETEX "cache:metadata:$key" "$CACHE_TTL"
           log "📝 Métadonnées sauvées dans Redis"
       fi
   }

   # Fonction de récupération métadonnées Redis
   get_metadata_from_redis() {
       local key="$1"

       if [ -n "$REDIS_URL" ]; then
           local metadata=$(redis-cli -u "$REDIS_URL" GET "cache:metadata:$key")
           if [ -n "$metadata" ] && [ "$metadata" != "(nil)" ]; then
               echo "$metadata"
               return 0
           fi
       fi

       return 1
   }

   # Fonction de cache intelligent distribué
   smart_distributed_cache() {
       local action="$1"
       local cache_key="$2"
       local local_path="$3"

       case "$action" in
           "save")
               log "💾 Sauvegarde cache distribué: $cache_key"

               # Métadonnées
               local metadata=$(cat <<EOF
   {
     "key": "$cache_key",
     "project": "$CI_PROJECT_ID",
     "branch": "$CI_COMMIT_REF_NAME",
     "commit": "$CI_COMMIT_SHA",
     "created": "$(date +%s)",
     "size": "$(du -sb "$local_path" 2>/dev/null | cut -f1 || echo 0)"
   }
   EOF
   )

               # Sauvegarder métadonnées dans Redis
               cache_metadata_to_redis "$cache_key" "$metadata"

               # Sauvegarder données dans S3
               upload_to_s3 "$local_path" "$cache_key"
               ;;

           "restore")
               log "📦 Restauration cache distribué: $cache_key"

               # Vérifier métadonnées
               local metadata=$(get_metadata_from_redis "$cache_key")
               if [ $? -eq 0 ]; then
                   log "📋 Métadonnées trouvées: $metadata"

                   # Vérifier si pas trop ancien
                   local created=$(echo "$metadata" | jq -r '.created')
                   local now=$(date +%s)
                   local age=$((now - created))

                   if [ "$age" -lt "$CACHE_TTL" ]; then
                       download_from_s3 "$cache_key" "$local_path"
                       export CACHE_HIT_RATE="1"
                       return 0
                   else
                       log "⏰ Cache trop ancien ($age s > $CACHE_TTL s)"
                   fi
               fi

               export CACHE_HIT_RATE="0"
               return 1
               ;;

           "clean")
               log "🧹 Nettoyage cache distribué"

               # Nettoyer les caches expirés dans Redis
               if [ -n "$REDIS_URL" ]; then
                   redis-cli -u "$REDIS_URL" --scan --pattern "cache:metadata:*" | \
                   while read key; do
                       local ttl=$(redis-cli -u "$REDIS_URL" TTL "$key")
                       if [ "$ttl" -lt 0 ]; then
                           redis-cli -u "$REDIS_URL" DEL "$key"
                       fi
                   done
               fi

               # Nettoyer S3 (objets de plus de 7 jours)
               aws s3api list-objects-v2 --bucket "$S3_BUCKET" \
                   --query "Contents[?LastModified<=\`$(date -d '7 days ago' --iso-8601)\`].Key" \
                   --output text | \
               while read key; do
                   if [ -n "$key" ] && [ "$key" != "None" ]; then
                       aws s3 rm "s3://$S3_BUCKET/$key"
                   fi
               done
               ;;
       esac
   }

   # Exécution
   smart_distributed_cache "$@"
   ```

### 2.3 Points d'évaluation Exercice 2 (25 points)

- [ ] **Stratégie cache multi-niveaux** (10 points)
- [ ] **Templates cache optimisés** (5 points)
- [ ] **Cache distribué S3/Redis** (8 points)
- [ ] **Validation et warming** (2 points)

## Exercice 3 : Parallélisation et optimisation des jobs (25 points)

### 3.1 Parallélisation intelligente

**Votre tâche : Optimiser la parallélisation des jobs pour réduire le temps total**

1. **Analyse des dépendances et optimisation**

   Créez `scripts/job-optimizer.sh` :

   ```bash
   #!/bin/bash

   set -e

   # Fonction d'analyse des dépendances
   analyze_job_dependencies() {
       log "🔍 Analyse des dépendances entre jobs"

       # Créer un graphe des dépendances
       cat > job_dependencies.py << 'EOF'
   import yaml
   import json
   import sys
   from collections import defaultdict, deque

   def analyze_gitlab_ci(file_path):
       with open(file_path, 'r') as f:
           config = yaml.safe_load(f)

       jobs = {}
       stages = config.get('stages', [])

       # Extraire les jobs
       for key, value in config.items():
           if not key.startswith('.') and isinstance(value, dict) and 'script' in value:
               job = {
                   'name': key,
                   'stage': value.get('stage', 'test'),
                   'needs': value.get('needs', []),
                   'dependencies': value.get('dependencies', []),
                   'parallel': value.get('parallel', 1)
               }
               jobs[key] = job

       # Calculer les chemins critiques
       graph = defaultdict(list)
       in_degree = defaultdict(int)

       for job_name, job in jobs.items():
           for need in job['needs']:
               if isinstance(need, str):
                   graph[need].append(job_name)
                   in_degree[job_name] += 1
               elif isinstance(need, dict) and 'job' in need:
                   graph[need['job']].append(job_name)
                   in_degree[job_name] += 1

       # Tri topologique pour trouver le chemin critique
       queue = deque([job for job in jobs if in_degree[job] == 0])
       levels = defaultdict(list)
       job_levels = {}

       level = 0
       while queue:
           level_size = len(queue)
           for _ in range(level_size):
               job = queue.popleft()
               levels[level].append(job)
               job_levels[job] = level

               for neighbor in graph[job]:
                   in_degree[neighbor] -= 1
                   if in_degree[neighbor] == 0:
                       queue.append(neighbor)
           level += 1

       # Analyse des optimisations possibles
       optimizations = []

       # 1. Jobs qui peuvent être parallélisés
       for level_jobs in levels.values():
           if len(level_jobs) > 1:
               optimizations.append({
                   'type': 'parallel_opportunity',
                   'jobs': level_jobs,
                   'description': f'Ces {len(level_jobs)} jobs peuvent s\'exécuter en parallèle'
               })

       # 2. Jobs sans dépendances qui pourraient être dans des stages plus précoces
       for job_name, job in jobs.items():
           if not job['needs'] and not job['dependencies']:
               current_stage_index = stages.index(job['stage']) if job['stage'] in stages else len(stages)
               if current_stage_index > 0:
                   optimizations.append({
                       'type': 'stage_optimization',
                       'job': job_name,
                       'current_stage': job['stage'],
                       'suggested_stage': stages[0] if stages else 'build',
                       'description': f'Job {job_name} peut être déplacé vers un stage plus précoce'
                   })

       return {
           'jobs': jobs,
           'levels': dict(levels),
           'optimizations': optimizations,
           'critical_path_length': level
       }

   if __name__ == '__main__':
       result = analyze_gitlab_ci('.gitlab-ci.yml')
       print(json.dumps(result, indent=2))
   EOF

       python3 job_dependencies.py > dependency_analysis.json

       log "📊 Analyse terminée, résultats dans dependency_analysis.json"
   }

   # Fonction de génération de pipeline optimisé
   generate_optimized_pipeline() {
       log "⚡ Génération du pipeline optimisé"

       cat > pipeline_optimizer.py << 'EOF'
   import json
   import yaml

   def optimize_pipeline():
       # Charger l'analyse
       with open('dependency_analysis.json', 'r') as f:
           analysis = json.load(f)

       # Charger la configuration actuelle
       with open('.gitlab-ci.yml', 'r') as f:
           config = yaml.safe_load(f)

       optimized_config = config.copy()

       # Appliquer les optimisations
       for opt in analysis['optimizations']:
           if opt['type'] == 'stage_optimization':
               job_name = opt['job']
               if job_name in optimized_config:
                   optimized_config[job_name]['stage'] = opt['suggested_stage']
                   print(f"✅ {job_name}: {opt['current_stage']} → {opt['suggested_stage']}")

           elif opt['type'] == 'parallel_opportunity':
               for job_name in opt['jobs']:
                   if job_name in optimized_config:
                       # Ajouter parallélisation si pas déjà présente
                       current_parallel = optimized_config[job_name].get('parallel', 1)
                       if current_parallel == 1:
                           # Suggestion de parallélisation basée sur la nature du job
                           if 'test' in job_name.lower():
                               optimized_config[job_name]['parallel'] = {
                                   'matrix': [
                                       {'TEST_SUITE': 'unit'},
                                       {'TEST_SUITE': 'integration'},
                                       {'TEST_SUITE': 'e2e'}
                                   ]
                               }
                               print(f"✅ {job_name}: Parallélisation par test suite")

       # Sauvegarder la configuration optimisée
       with open('.gitlab-ci.optimized.yml', 'w') as f:
           yaml.dump(optimized_config, f, default_flow_style=False, sort_keys=False)

       print("📝 Configuration optimisée sauvée dans .gitlab-ci.optimized.yml")

       # Calculer les gains estimés
       current_stages = len(set(job.get('stage', 'test') for job in config.values() if isinstance(job, dict)))
       optimized_stages = len(set(job.get('stage', 'test') for job in optimized_config.values() if isinstance(job, dict)))

       print(f"📊 Stages: {current_stages} → {optimized_stages}")
       print(f"🚀 Gain estimé: {max(0, (current_stages - optimized_stages) * 30)}s")

   if __name__ == '__main__':
       optimize_pipeline()
   EOF

       python3 pipeline_optimizer.py
   }

   # Fonction de parallélisation des tests
   parallelize_tests() {
       log "🧪 Optimisation de la parallélisation des tests"

       # Analyser les fichiers de test pour groupage intelligent
       cat > test_parallelizer.py << 'EOF'
   import os
   import json
   import glob
   from pathlib import Path

   def analyze_test_files():
       test_patterns = [
           'test/**/*.js',
           'tests/**/*.js',
           'spec/**/*.js',
           'test/**/*.py',
           'tests/**/*.py',
           'test/**/*.php',
           'tests/**/*.php'
       ]

       test_files = []
       for pattern in test_patterns:
           test_files.extend(glob.glob(pattern, recursive=True))

       # Grouper les tests par taille et type
       groups = {
           'unit': [],
           'integration': [],
           'e2e': [],
           'performance': []
       }

       for test_file in test_files:
           file_size = os.path.getsize(test_file)
           file_name = os.path.basename(test_file).lower()

           # Classification basée sur le nom et la taille
           if 'e2e' in file_name or 'end-to-end' in file_name:
               groups['e2e'].append(test_file)
           elif 'integration' in file_name or 'int' in file_name:
               groups['integration'].append(test_file)
           elif 'performance' in file_name or 'perf' in file_name:
               groups['performance'].append(test_file)
           else:
               groups['unit'].append(test_file)

       # Créer la configuration de parallélisation
       parallel_config = []

       for group_name, files in groups.items():
           if files:
               # Diviser en chunks pour parallélisation
               chunk_size = max(1, len(files) // 3)  # 3 jobs parallèles max par groupe
               chunks = [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

               for i, chunk in enumerate(chunks):
                   parallel_config.append({
                       'TEST_GROUP': group_name,
                       'TEST_CHUNK': i + 1,
                       'TEST_FILES': ' '.join(chunk[:5]),  # Limiter pour éviter les commandes trop longues
                       'CHUNK_SIZE': len(chunk)
                   })

       return parallel_config

   def generate_test_jobs():
       parallel_config = analyze_test_files()

       job_template = """
   test_parallel:
     stage: test
     parallel:
       matrix:
   """

       for config in parallel_config:
           job_template += f"""      - TEST_GROUP: "{config['TEST_GROUP']}"
           TEST_CHUNK: {config['TEST_CHUNK']}
           TEST_FILES: "{config['TEST_FILES']}"
   """

       job_template += """
     script:
       - echo "Running tests for group $TEST_GROUP, chunk $TEST_CHUNK"
       - |
         case "$TEST_GROUP" in
           "unit")
             npm run test:unit -- $TEST_FILES
             ;;
           "integration")
             npm run test:integration -- $TEST_FILES
             ;;
           "e2e")
             npm run test:e2e -- $TEST_FILES
             ;;
           "performance")
             npm run test:performance -- $TEST_FILES
             ;;
         esac
     artifacts:
       reports:
         junit: test-results-$TEST_GROUP-$TEST_CHUNK.xml
         coverage: coverage/lcov-$TEST_GROUP-$TEST_CHUNK.info
   """

       print(job_template)

       with open('optimized-test-jobs.yml', 'w') as f:
           f.write(job_template)

       print(f"✅ Génération terminée: {len(parallel_config)} jobs parallèles créés")

   if __name__ == '__main__':
       generate_test_jobs()
   EOF

       python3 test_parallelizer.py
   }

   # Exécution
   case "${1:-all}" in
       "analyze")
           analyze_job_dependencies
           ;;
       "optimize")
           generate_optimized_pipeline
           ;;
       "parallelize")
           parallelize_tests
           ;;
       "all")
           analyze_job_dependencies
           generate_optimized_pipeline
           parallelize_tests
           ;;
       *)
           echo "Usage: $0 {analyze|optimize|parallelize|all}"
           exit 1
           ;;
   esac
   ```

2. **Configuration de jobs optimisés**

   Créez `.gitlab-ci.optimized.yml` avec la structure optimisée :

   ```yaml
   # Pipeline optimisé pour performance maximale

   stages:
     - prepare
     - build
     - test
     - quality
     - deploy

   variables:
     PERFORMANCE_MODE: 'true'
     PARALLEL_JOBS: '3'

   # Job de préparation ultrarapide
   prepare:
     stage: prepare
     image: alpine:latest
     script:
       - echo "🚀 Préparation optimisée"
       - echo "PIPELINE_START_TIME=$(date +%s)" >> pipeline.env
     artifacts:
       reports:
         dotenv: pipeline.env
       expire_in: 1 hour

   # Build parallélisé par composants
   build_frontend:
     stage: build
     extends: .cache_node
     script:
       - cd frontend
       - npm ci --prefer-offline
       - npm run build
     parallel:
       matrix:
         - BUILD_TYPE: ['development', 'production']
     artifacts:
       paths:
         - frontend/dist/
       expire_in: 2 hours

   build_backend:
     stage: build
     extends: .cache_node
     script:
       - cd backend
       - npm ci --prefer-offline
       - npm run build
     artifacts:
       paths:
         - backend/dist/
       expire_in: 2 hours

   # Tests ultra-parallélisés
   test_unit:
     stage: test
     needs: ['prepare']
     extends: .cache_node
     parallel:
       matrix:
         - TEST_SUITE: ['auth', 'api', 'utils', 'components']
     script:
       - npm run test:unit -- --testNamePattern="$TEST_SUITE"
     artifacts:
       reports:
         junit: test-results-unit-$TEST_SUITE.xml
         coverage: coverage/unit-$TEST_SUITE.xml

   test_integration:
     stage: test
     needs: ['build_frontend', 'build_backend']
     parallel: 2
     script:
       - npm run test:integration -- --shard=$CI_NODE_INDEX/$CI_NODE_TOTAL
     artifacts:
       reports:
         junit: test-results-integration-$CI_NODE_INDEX.xml

   # Analyse qualité en parallèle
   quality_lint:
     stage: quality
     needs: ['prepare']
     parallel:
       matrix:
         - TOOL: ['eslint', 'stylelint', 'prettier']
     script:
       - npm run $TOOL

   quality_security:
     stage: quality
     needs: ['prepare']
     parallel:
       matrix:
         - SCAN_TYPE: ['sast', 'dependency', 'secrets']
     script:
       - run_security_scan.sh $SCAN_TYPE
   ```

### 3.2 Points d'évaluation Exercice 3 (25 points)

- [ ] **Analyse des dépendances** (8 points)
- [ ] **Génération pipeline optimisé** (8 points)
- [ ] **Parallélisation intelligente des tests** (6 points)
- [ ] **Configuration jobs optimisés** (3 points)

## Livrables et évaluation finale

### Livrables attendus (100 points total)

1. **Système d'audit complet** (25 points)

   - Script d'analyse de performance
   - Monitoring continu avec alertes
   - Job d'audit intégré au pipeline
   - Rapports automatisés

2. **Cache intelligent multi-niveaux** (25 points)

   - Stratégies de cache hiérarchiques
   - Templates optimisés par technologie
   - Cache distribué avec S3/Redis
   - Validation et warming automatique

3. **Optimisation des jobs** (25 points)

   - Analyse des dépendances
   - Parallélisation intelligente
   - Configuration optimisée
   - Tests parallélisés par type

4. **Monitoring et métriques** (25 points)
   - Dashboard de performance
   - KPIs temps réel
   - Alertes automatiques
   - Rapports d'optimisation

### Critères de réussite

- **Réduction temps pipeline** : Au moins 30% de gain sur la durée totale
- **Efficacité cache** : Taux de hit cache > 80%
- **Parallélisation** : Jobs exécutés en parallèle quand possible
- **Monitoring** : Métriques collectées et alertes fonctionnelles
- **Automatisation** : Optimisations appliquées automatiquement

### Bonus (15 points supplémentaires)

- **Machine Learning** : Prédiction des temps d'exécution et optimisation automatique
- **Scaling dynamique** : Adaptation du nombre de runners selon la charge
- **Cross-project cache** : Partage de cache entre projets similaires
- **Performance regression detection** : Détection automatique des régressions

---

**Temps estimé** : 8-10 heures
**Difficulté** : ★★★★★ (Expert avancé)
**Prérequis** : LABs 1-9 terminés, connaissances système et optimisation

> **Note importante** : Ce lab représente le niveau expert en optimisation CI/CD. Les techniques apprises permettent d'atteindre des performances de niveau production pour des équipes importantes.
