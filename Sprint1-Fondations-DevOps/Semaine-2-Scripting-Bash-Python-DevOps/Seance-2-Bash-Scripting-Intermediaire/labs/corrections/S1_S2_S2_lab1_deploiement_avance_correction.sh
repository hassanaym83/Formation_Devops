#!/bin/bash
# S1_S2_S2_LAB1 - CORRECTION - Déploiement multi-environnement avec rollback
# DURÉE : 15 minutes
# NIVEAU : Intermédiaire

set -euo pipefail

# ====== CORRECTION COMPLÈTE ======

# Configuration globale
readonly ENVIRONMENTS=("dev" "staging" "production")
readonly DEPLOYMENT_LOG="/tmp/deployment.log"
readonly VERSIONS_FILE="/tmp/versions.txt"
readonly BACKUP_DIR="/tmp/backups"

# Initialisation
mkdir -p "$BACKUP_DIR"
touch "$DEPLOYMENT_LOG" "$VERSIONS_FILE"

# Fonction de logging structuré
log_deployment() {
 local level="$1"
 local message="$2"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 echo "[$timestamp] [$level] $message" | tee -a "$DEPLOYMENT_LOG"
}

# Validation environnement
validate_environment() {
 local env="$1"
 
 log_deployment "INFO" "Validation environnement: $env"
 
 if [[ ! " ${ENVIRONMENTS[*]} " =~ " $env " ]]; then
 log_deployment "ERROR" "Environnement invalide: $env"
 return 1
 fi
 
 # Vérifications spécifiques par environnement
 case "$env" in
 "production")
 if [[ ! -f "/tmp/prod_approval.txt" ]]; then
 log_deployment "WARN" "Approval manquante pour production"
 # echo "approved" > /tmp/prod_approval.txt # Simulation
 fi
 ;;
 "staging")
 if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
 log_deployment "WARN" "Connectivité réseau limitée"
 fi
 ;;
 esac
 
 log_deployment "INFO" "Environnement $env validé"
 return 0
}

# Sauvegarde version actuelle
backup_current_version() {
 local env="$1"
 local current_version
 
 # Récupération version actuelle
 current_version=$(grep "^$env:" "$VERSIONS_FILE" | cut -d: -f2 || echo "v0.0.0")
 
 log_deployment "INFO" "Sauvegarde version actuelle $env: $current_version"
 
 # Simulation sauvegarde
 cat > "$BACKUP_DIR/${env}_${current_version}.backup" << EOF
# Backup $env - $current_version
timestamp=$(date)
environment=$env
version=$current_version
config_hash=$(echo "$env$current_version" | md5sum | cut -d' ' -f1)
EOF
 
 log_deployment "INFO" "Sauvegarde créée: ${env}_${current_version}.backup"
}

# Déploiement avec tests
deploy_with_tests() {
 local env="$1"
 local version="$2"
 local rollback_version="${3:-}"
 
 log_deployment "INFO" "Début déploiement $version vers $env"
 
 # Étapes de déploiement
 local steps=("download" "validate" "deploy" "test" "activate")
 
 for step in "${steps[@]}"; do
 log_deployment "INFO" "Étape: $step"
 
 case "$step" in
 "download")
 # Simulation téléchargement
 sleep 1
 if [[ "$version" == "v999.0.0" ]]; then
 log_deployment "ERROR" "Version inexistante: $version"
 return 1
 fi
 ;;
 "validate")
 # Validation package
 if [[ ${#version} -lt 5 ]]; then
 log_deployment "ERROR" "Format version invalide: $version"
 return 1
 fi
 ;;
 "deploy")
 # Déploiement
 sleep 2
 log_deployment "INFO" "Application déployée: $version"
 ;;
 "test")
 # Tests smoke
 run_smoke_tests "$env" "$version"
 if [[ $? -ne 0 ]]; then
 log_deployment "ERROR" "Tests smoke échoués"
 return 1
 fi
 ;;
 "activate")
 # Activation
 echo "$env:$version" >> "$VERSIONS_FILE"
 log_deployment "INFO" "Version $version activée pour $env"
 ;;
 esac
 done
 
 log_deployment "SUCCESS" "Déploiement $version vers $env réussi"
 return 0
}

# Tests smoke intégrés
run_smoke_tests() {
 local env="$1"
 local version="$2"
 
 log_deployment "INFO" "Exécution tests smoke pour $env:$version"
 
 # Tests par environnement
 case "$env" in
 "dev")
 # Tests basiques dev
 [[ "$version" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || return 1
 ;;
 "staging")
 # Tests intégration
 [[ "$version" != *"alpha"* ]] || return 1
 ;;
 "production")
 # Tests complets production
 [[ "$version" =~ ^v[1-9][0-9]*\.[0-9]+\.[0-9]+$ ]] || return 1
 ;;
 esac
 
 # Simulation tests HTTP
 local response_code=$((RANDOM % 10))
 if [[ $response_code -lt 2 ]]; then
 log_deployment "ERROR" "Test HTTP échoué (code: $response_code)"
 return 1
 fi
 
 log_deployment "SUCCESS" "Tests smoke réussis"
 return 0
}

# Rollback intelligent
intelligent_rollback() {
 local env="$1"
 local target_version="${2:-}"
 
 log_deployment "INFO" "Début rollback pour $env"
 
 # Détermination version cible
 if [[ -z "$target_version" ]]; then
 target_version=$(grep "^$env:" "$VERSIONS_FILE" | tail -2 | head -1 | cut -d: -f2 || echo "v1.0.0")
 log_deployment "INFO" "Version rollback automatique: $target_version"
 fi
 
 # Validation version rollback
 if [[ ! -f "$BACKUP_DIR/${env}_${target_version}.backup" ]]; then
 log_deployment "ERROR" "Backup introuvable: ${env}_${target_version}.backup"
 return 1
 fi
 
 # Processus rollback
 log_deployment "INFO" "Rollback vers $target_version"
 
 # Restauration depuis backup
 local backup_info
 backup_info=$(cat "$BACKUP_DIR/${env}_${target_version}.backup")
 log_deployment "INFO" "Restauration: $backup_info"
 
 # Simulation rollback
 sleep 2
 
 # Tests post-rollback
 run_smoke_tests "$env" "$target_version"
 if [[ $? -eq 0 ]]; then
 echo "$env:$target_version" >> "$VERSIONS_FILE"
 log_deployment "SUCCESS" "Rollback vers $target_version réussi"
 return 0
 else
 log_deployment "ERROR" "Rollback échoué - tests smoke KO"
 return 1
 fi
}

# Dashboard déploiement
display_deployment_status() {
 local env="${1:-all}"
 
 echo "====== DASHBOARD DÉPLOIEMENTS ======"
 echo "Timestamp: $(date)"
 echo
 
 if [[ "$env" == "all" ]]; then
 for environment in "${ENVIRONMENTS[@]}"; do
 show_environment_status "$environment"
 done
 else
 show_environment_status "$env"
 fi
 
 echo
 echo "====== LOGS RÉCENTS ======"
 tail -5 "$DEPLOYMENT_LOG"
}

# Status environnement
show_environment_status() {
 local env="$1"
 local current_version
 local last_deployment
 
 current_version=$(grep "^$env:" "$VERSIONS_FILE" | tail -1 | cut -d: -f2 || echo "Non déployé")
 last_deployment=$(grep "$env" "$DEPLOYMENT_LOG" | tail -1 | cut -d']' -f1-2 || echo "Jamais")
 
 echo "[$env]"
 echo " Version: $current_version"
 echo " Dernier déploiement: $last_deployment"
 echo " Backups: $(ls "$BACKUP_DIR" | grep -c "$env" || echo 0)"
 echo
}

# Tests complets du système
test_deployment_system() {
 local test_env="test_env"
 
 echo "====== TESTS SYSTÈME DÉPLOIEMENT ======"
 
 # Test 1: Déploiement normal
 echo "[TEST 1] Déploiement normal"
 validate_environment "dev" && echo "✓ Validation OK" || echo "✗ Validation KO"
 
 # Test 2: Backup
 echo "[TEST 2] Système backup"
 backup_current_version "dev" && echo "✓ Backup OK" || echo "✗ Backup KO"
 
 # Test 3: Déploiement avec succès
 echo "[TEST 3] Déploiement réussi"
 deploy_with_tests "dev" "v2.1.0" && echo "✓ Déploiement OK" || echo "✗ Déploiement KO"
 
 # Test 4: Rollback
 echo "[TEST 4] Rollback"
 intelligent_rollback "dev" "v2.0.0" && echo "✓ Rollback OK" || echo "✗ Rollback KO"
 
 # Test 5: Dashboard
 echo "[TEST 5] Dashboard"
 display_deployment_status "dev" >/dev/null && echo "✓ Dashboard OK" || echo "✗ Dashboard KO"
 
 echo "====== FIN TESTS ======"
}

# Fonction principale
main() {
 local action="${1:-help}"
 local environment="${2:-dev}"
 local version="${3:-v1.0.0}"
 
 case "$action" in
 "deploy")
 validate_environment "$environment" && \
 backup_current_version "$environment" && \
 deploy_with_tests "$environment" "$version"
 ;;
 "rollback")
 intelligent_rollback "$environment" "$version"
 ;;
 "status")
 display_deployment_status "$environment"
 ;;
 "test")
 test_deployment_system
 ;;
 "help"|*)
 cat << EOF
Usage: $0 {deploy|rollback|status|test} [environment] [version]

Commands:
 deploy - Déploie une version vers un environnement
 rollback - Effectue un rollback intelligent
 status - Affiche le status des déploiements
 test - Lance les tests du système

Examples:
 $0 deploy dev v2.1.0
 $0 rollback production v2.0.0
 $0 status production
 $0 test
EOF
 ;;
 esac
}

# Point d'entrée
main "$@"

# ====== RÉSULTATS ATTENDUS ======
# ✓ Déploiement multi-environnement fonctionnel
# ✓ Système de backup automatique
# ✓ Tests smoke intégrés
# ✓ Rollback intelligent avec validation
# ✓ Logging structuré complet
# ✓ Dashboard temps-réel
# ✓ Gestion d'erreurs robuste
# ✓ Tests système automatisés

# POINTS CLÉS TECHNIQUES :
# - Validation stricte des paramètres
# - Gestion d'erreurs avec set -euo pipefail
# - Logging structuré avec niveaux
# - Backup automatique avant déploiement
# - Tests smoke par environnement
# - Rollback avec validation backup
# - Dashboard informatif
# - Tests système complets