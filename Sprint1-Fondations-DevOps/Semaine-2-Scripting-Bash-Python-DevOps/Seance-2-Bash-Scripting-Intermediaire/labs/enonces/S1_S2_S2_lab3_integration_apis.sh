#!/bin/bash
# S1_S2_S2_LAB3 - Intégration d'APIs et webhooks
# DURÉE : 20 minutes

# OBJECTIF :
# Développer un système d'intégration d'APIs avec gestion de webhooks
# pour orchestration DevOps et automation de workflows.

# CONSIGNES :
# 1. Implémentez un client API REST complet avec authentification
# 2. Créez le système de gestion des webhooks entrants
# 3. Développez la logique de retry et gestion d'erreurs
# 4. Testez l'intégration avec services DevOps simulés

# SPÉCIFICATIONS TECHNIQUES :
# - Client API REST avec méthodes GET, POST, PUT, DELETE
# - Authentification Bearer Token et API Key
# - Retry automatique avec backoff exponentiel
# - Gestion des webhooks avec parsing JSON
# - Intégration GitHub, Slack, monitoring simulées

# RÉSULTAT ATTENDU :
# Un client API robuste capable d'interagir avec services externes
# et de traiter les webhooks pour automation de workflows.

# ====== TEMPLATE DE DÉPART ======

#!/bin/bash
set -euo pipefail

# TODO: Configuration API
# readonly API_BASE_URL="https://api.example.com"
# readonly API_TOKEN="${API_TOKEN:-your_token_here}"
# readonly WEBHOOK_SECRET="${WEBHOOK_SECRET:-webhook_secret}"
# readonly MAX_RETRIES=3

# TODO: Client API REST générique
# call_api() {
# local method="$1"
# local endpoint="$2" 
# local data="$3"
# local headers="$4"
# 
# # Construisez la requête curl
# # Gérez l'authentification (Bearer token)
# # Gérez les headers Content-Type
# # Retournez la réponse
# }

# TODO: Fonctions API spécialisées
# github_api() {
# local action="$1"
# local repo="$2"
# local data="$3"
# 
# case "$action" in
# "get_repo") call_api "GET" "/repos/$repo" "" ;;
# "create_issue") call_api "POST" "/repos/$repo/issues" "$data" ;;
# "trigger_workflow") call_api "POST" "/repos/$repo/actions/workflows/deploy.yml/dispatches" "$data" ;;
# esac
# }

# TODO: Client Slack
# send_slack_notification() {
# local channel="$1"
# local message="$2"
# local webhook_url="$3"
# 
# # Formatez le payload Slack
# # Envoyez via webhook
# }

# TODO: Système de retry avec backoff
# retry_api_call() {
# local max_attempts="$1"
# local delay="$2"
# shift 2
# local command=("$@")
# 
# # Implémentez retry avec backoff exponentiel
# # Delay : 1s, 2s, 4s, 8s...
# }

# TODO: Gestionnaire de webhooks
# handle_webhook() {
# local event_type="$1"
# local payload="$2"
# local signature="$3"
# 
# # Vérifiez la signature HMAC
# # Parsez le payload JSON
# # Routez selon le type d'événement
# }

# TODO: Processeur d'événements
# process_webhook_event() {
# local event_type="$1"
# local payload="$2"
# 
# case "$event_type" in
# "push")
# trigger_deployment "$payload"
# ;;
# "pull_request")
# trigger_tests "$payload"
# ;;
# "deployment_status")
# notify_deployment_status "$payload"
# ;;
# esac
# }

# TODO: Simulation serveur webhook
# start_webhook_server() {
# local port="${1:-8080}"
# # Simulez un serveur webhook simple
# # Écoutez sur le port spécifié
# # Traitez les requêtes entrantes
# }

# TODO: Tests d'intégration
# test_api_integration() {
# # Testez les appels API
# # Testez la gestion d'erreurs
# # Testez les webhooks
# # Testez le retry
# }

# TODO: Fonction principale
# main() {
# local action="${1:-test}"
# 
# case "$action" in
# "test") test_api_integration ;;
# "webhook") start_webhook_server "${2:-8080}" ;;
# "github") github_api "${2:-get_repo}" "${3:-user/repo}" "${4:-}" ;;
# "slack") send_slack_notification "${2:-#general}" "${3:-Test message}" "${4:-}" ;;
# esac
# }

# main "$@"

# ====== TESTS À EFFECTUER ======
# 1. ./script.sh test # Tests intégration
# 2. ./script.sh github get_repo owner/repo # API GitHub
# 3. ./script.sh slack "#devops" "Test message" # Notification Slack
# 4. ./script.sh webhook 8080 # Serveur webhook

# CRITÈRES D'ÉVALUATION :
# □ Client API REST fonctionnel
# □ Authentification sécurisée
# □ Retry avec backoff implémenté
# □ Webhooks traités correctement
# □ Intégrations GitHub/Slack simulées
# □ Gestion d'erreurs robuste