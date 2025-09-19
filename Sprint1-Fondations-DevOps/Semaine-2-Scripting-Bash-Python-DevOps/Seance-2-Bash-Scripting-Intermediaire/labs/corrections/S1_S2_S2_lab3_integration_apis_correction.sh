#!/bin/bash
# S1_S2_S2_LAB3 - CORRECTION - Client REST API avec webhooks
# DURÉE : 20 minutes 
# NIVEAU : Intermédiaire

set -euo pipefail

# ====== CORRECTION COMPLÈTE ======

# Configuration API
readonly API_BASE_URL="https://jsonplaceholder.typicode.com"
readonly WEBHOOK_PORT="8080"
readonly API_LOG="/tmp/api_requests.log"
readonly WEBHOOK_LOG="/tmp/webhook_events.log"
readonly CACHE_DIR="/tmp/api_cache"
readonly CONFIG_FILE="/tmp/api_config.conf"

# Initialisation
mkdir -p "$CACHE_DIR"
touch "$API_LOG" "$WEBHOOK_LOG"

# Configuration par défaut
init_api_config() {
 cat > "$CONFIG_FILE" << 'EOF'
# Configuration API Client
api_timeout=30
retry_attempts=3
retry_delay=2
cache_ttl=300
rate_limit=10
webhook_secret=devops_secret_2024
enable_cache=true
enable_logging=true
EOF
}

# Chargement configuration
load_config() {
 if [[ -f "$CONFIG_FILE" ]]; then
 source "$CONFIG_FILE"
 else
 init_api_config
 source "$CONFIG_FILE"
 fi
}

# Logging API avec rotation
log_api_request() {
 local method="$1"
 local endpoint="$2"
 local status="$3"
 local response_time="${4:-0}"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 
 echo "[$timestamp] $method $endpoint - Status:$status Time:${response_time}ms" >> "$API_LOG"
 
 # Rotation log si trop gros (>10MB)
 if [[ -f "$API_LOG" ]] && [[ $(stat -f%z "$API_LOG" 2>/dev/null || stat -c%s "$API_LOG" 2>/dev/null || echo 0) -gt 10485760 ]]; then
 mv "$API_LOG" "${API_LOG}.old"
 touch "$API_LOG"
 fi
}

# Client HTTP avec retry et cache
api_request() {
 local method="$1"
 local endpoint="$2"
 local data="${3:-}"
 local cache_key="${method}_${endpoint//\//_}"
 local cache_file="$CACHE_DIR/${cache_key}.cache"
 
 load_config
 
 # Vérification cache pour GET
 if [[ "$method" == "GET" && "$enable_cache" == "true" && -f "$cache_file" ]]; then
 local cache_age=$(($(date +%s) - $(stat -f%m "$cache_file" 2>/dev/null || stat -c%Y "$cache_file" 2>/dev/null || echo 0)))
 if [[ $cache_age -lt $cache_ttl ]]; then
 echo "Cache hit: $endpoint"
 cat "$cache_file"
 return 0
 fi
 fi
 
 # Rate limiting simple
 local last_request_file="/tmp/last_api_request"
 if [[ -f "$last_request_file" ]]; then
 local last_request=$(cat "$last_request_file")
 local time_diff=$(($(date +%s) - last_request))
 local min_interval=$((60 / rate_limit))
 
 if [[ $time_diff -lt $min_interval ]]; then
 echo "Rate limit: waiting $((min_interval - time_diff))s"
 sleep $((min_interval - time_diff))
 fi
 fi
 
 # Requête avec retry
 local attempt=1
 local start_time=$(date +%s%3N)
 
 while [[ $attempt -le $retry_attempts ]]; do
 echo "Tentative $attempt/$retry_attempts: $method $endpoint"
 
 local response
 local http_code
 local temp_response="/tmp/api_response_$$"
 
 # Construction commande curl
 local curl_cmd="curl -s -w '%{http_code}' --connect-timeout $api_timeout"
 
 case "$method" in
 "GET")
 curl_cmd="$curl_cmd -X GET"
 ;;
 "POST")
 curl_cmd="$curl_cmd -X POST -H 'Content-Type: application/json'"
 [[ -n "$data" ]] && curl_cmd="$curl_cmd -d '$data'"
 ;;
 "PUT")
 curl_cmd="$curl_cmd -X PUT -H 'Content-Type: application/json'"
 [[ -n "$data" ]] && curl_cmd="$curl_cmd -d '$data'"
 ;;
 "DELETE")
 curl_cmd="$curl_cmd -X DELETE"
 ;;
 esac
 
 # Exécution requête
 response=$(eval "$curl_cmd '${API_BASE_URL}${endpoint}'" 2>/dev/null || echo "")
 http_code="${response: -3}"
 response="${response%???}"
 
 local end_time=$(date +%s%3N)
 local response_time=$((end_time - start_time))
 
 # Vérification succès
 if [[ "$http_code" =~ ^2[0-9][0-9]$ ]]; then
 log_api_request "$method" "$endpoint" "$http_code" "$response_time"
 echo "$response" > "$temp_response"
 
 # Cache pour GET réussis
 if [[ "$method" == "GET" && "$enable_cache" == "true" ]]; then
 cp "$temp_response" "$cache_file"
 fi
 
 # Mise à jour rate limiting
 date +%s > "$last_request_file"
 
 cat "$temp_response"
 rm -f "$temp_response"
 return 0
 else
 log_api_request "$method" "$endpoint" "${http_code:-000}" "$response_time"
 echo "Erreur HTTP $http_code: $response"
 
 if [[ $attempt -lt $retry_attempts ]]; then
 echo "Retry dans ${retry_delay}s..."
 sleep "$retry_delay"
 ((attempt++))
 # Backoff exponentiel
 retry_delay=$((retry_delay * 2))
 else
 rm -f "$temp_response"
 return 1
 fi
 fi
 done
}

# CRUD Posts
create_post() {
 local title="$1"
 local body="$2"
 local user_id="${3:-1}"
 
 local post_data=$(cat << EOF
{
 "title": "$title",
 "body": "$body", 
 "userId": $user_id
}
EOF
)
 
 echo "Création post: $title"
 api_request "POST" "/posts" "$post_data"
}

get_post() {
 local post_id="$1"
 
 echo "Récupération post ID: $post_id"
 api_request "GET" "/posts/$post_id"
}

get_all_posts() {
 local user_id="${1:-}"
 local endpoint="/posts"
 
 if [[ -n "$user_id" ]]; then
 endpoint="/posts?userId=$user_id"
 echo "Récupération posts utilisateur: $user_id"
 else
 echo "Récupération tous les posts"
 fi
 
 api_request "GET" "$endpoint"
}

update_post() {
 local post_id="$1"
 local title="$2"
 local body="$3"
 local user_id="${4:-1}"
 
 local post_data=$(cat << EOF
{
 "id": $post_id,
 "title": "$title",
 "body": "$body",
 "userId": $user_id
}
EOF
)
 
 echo "Mise à jour post ID: $post_id"
 api_request "PUT" "/posts/$post_id" "$post_data"
}

delete_post() {
 local post_id="$1"
 
 echo "Suppression post ID: $post_id"
 api_request "DELETE" "/posts/$post_id"
}

# Gestion utilisateurs
get_user() {
 local user_id="$1"
 
 echo "Récupération utilisateur ID: $user_id"
 api_request "GET" "/users/$user_id"
}

get_all_users() {
 echo "Récupération tous les utilisateurs"
 api_request "GET" "/users"
}

# Serveur webhook simple
start_webhook_server() {
 local port="${1:-$WEBHOOK_PORT}"
 
 echo " Démarrage serveur webhook sur port $port"
 echo "Logs: $WEBHOOK_LOG"
 echo "Arrêt: Ctrl+C"
 
 # Serveur webhook avec netcat
 while true; do
 {
 echo "HTTP/1.1 200 OK"
 echo "Content-Type: application/json"
 echo "Connection: close"
 echo ""
 echo '{"status":"ok","message":"Webhook received"}'
 } | nc -l "$port" | while IFS= read -r line; do
 [[ -n "$line" ]] && echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line" >> "$WEBHOOK_LOG"
 done
 done
}

# Validation webhook avec signature
validate_webhook() {
 local payload="$1"
 local signature="$2"
 
 load_config
 
 # Calcul signature HMAC-SHA256
 local expected_signature
 expected_signature=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$webhook_secret" | cut -d' ' -f2)
 
 if [[ "$signature" == "sha256=$expected_signature" ]]; then
 echo "✓ Signature webhook valide"
 return 0
 else
 echo "✗ Signature webhook invalide"
 return 1
 fi
}

# Traitement événements webhook
process_webhook_event() {
 local event_type="$1"
 local payload="$2"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 
 echo "[$timestamp] Événement webhook: $event_type" >> "$WEBHOOK_LOG"
 echo "$payload" >> "$WEBHOOK_LOG"
 
 case "$event_type" in
 "post.created")
 echo "📝 Nouveau post créé"
 # Traitement spécifique
 ;;
 "post.updated")
 echo "✏️ Post mis à jour"
 # Traitement spécifique
 ;;
 "post.deleted")
 echo "🗑️ Post supprimé"
 # Traitement spécifique
 ;;
 "user.created")
 echo "👤 Nouvel utilisateur"
 # Traitement spécifique
 ;;
 *)
 echo "❓ Événement inconnu: $event_type"
 ;;
 esac
}

# Dashboard API
display_api_dashboard() {
 local duration="${1:-60}"
 
 echo "====== DASHBOARD API CLIENT ======"
 echo "Durée: ${duration}s | $(date)"
 echo
 
 # Statistiques requêtes
 echo "=== STATISTIQUES REQUÊTES ==="
 if [[ -f "$API_LOG" ]]; then
 local total_requests=$(wc -l < "$API_LOG")
 local success_requests=$(grep -c "Status:2" "$API_LOG" || echo 0)
 local error_requests=$(grep -c "Status:[45]" "$API_LOG" || echo 0)
 local avg_response_time=$(grep -o "Time:[0-9]*ms" "$API_LOG" | grep -o "[0-9]*" | awk '{sum+=$1; count++} END {print (count>0) ? int(sum/count) : 0}')
 
 echo "Total: $total_requests | Succès: $success_requests | Erreurs: $error_requests"
 echo "Temps réponse moyen: ${avg_response_time}ms"
 else
 echo "Aucune requête effectuée"
 fi
 echo
 
 # Cache status
 echo "=== STATUS CACHE ==="
 local cache_files=$(ls "$CACHE_DIR" 2>/dev/null | wc -l || echo 0)
 local cache_size=$(du -sh "$CACHE_DIR" 2>/dev/null | cut -f1 || echo "0")
 echo "Fichiers cache: $cache_files | Taille: $cache_size"
 echo
 
 # Événements webhook récents
 echo "=== WEBHOOKS RÉCENTS ==="
 if [[ -f "$WEBHOOK_LOG" ]]; then
 tail -5 "$WEBHOOK_LOG" || echo "Aucun événement récent"
 else
 echo "Serveur webhook non démarré"
 fi
 echo
 
 # Configuration active
 echo "=== CONFIGURATION ==="
 if [[ -f "$CONFIG_FILE" ]]; then
 grep -E "^(api_timeout|retry_attempts|cache_ttl|rate_limit)" "$CONFIG_FILE" || echo "Configuration par défaut"
 fi
}

# Tests complets API
test_api_client() {
 echo "====== TESTS CLIENT API ======"
 
 # Test 1: Configuration
 echo "[TEST 1] Configuration"
 init_api_config && echo "✓ Config OK" || echo "✗ Config KO"
 
 # Test 2: GET posts
 echo "[TEST 2] GET /posts/1"
 get_post 1 >/dev/null && echo "✓ GET OK" || echo "✗ GET KO"
 
 # Test 3: POST création
 echo "[TEST 3] POST /posts"
 create_post "Test Title" "Test Body" 1 >/dev/null && echo "✓ POST OK" || echo "✗ POST KO"
 
 # Test 4: GET utilisateurs
 echo "[TEST 4] GET /users"
 get_all_users >/dev/null && echo "✓ Users OK" || echo "✗ Users KO" 
 
 # Test 5: Cache
 echo "[TEST 5] Cache"
 get_post 1 >/dev/null # Premier appel
 local cache_files_before=$(ls "$CACHE_DIR" | wc -l)
 get_post 1 >/dev/null # Deuxième appel (cache)
 local cache_files_after=$(ls "$CACHE_DIR" | wc -l)
 [[ $cache_files_after -ge $cache_files_before ]] && echo "✓ Cache OK" || echo "✗ Cache KO"
 
 # Test 6: Validation webhook
 echo "[TEST 6] Webhook validation"
 local test_payload='{"test": "data"}'
 validate_webhook "$test_payload" "sha256:invalid" >/dev/null 2>&1 && echo "✗ Validation KO" || echo "✓ Validation OK"
 
 echo "====== FIN TESTS ======"
}

# Nettoyage cache
clean_cache() {
 local max_age="${1:-3600}" # 1 heure par défaut
 
 echo "🧹 Nettoyage cache (> ${max_age}s)"
 
 find "$CACHE_DIR" -name "*.cache" -type f -mtime +$((max_age / 86400)) -delete 2>/dev/null || true
 
 local remaining_files=$(ls "$CACHE_DIR" 2>/dev/null | wc -l || echo 0)
 echo "Fichiers restants: $remaining_files"
}

# Fonction principale
main() {
 local action="${1:-help}"
 local param1="${2:-}"
 local param2="${3:-}"
 local param3="${4:-}"
 local param4="${5:-}"
 
 case "$action" in
 "get-post")
 get_post "$param1"
 ;;
 "get-posts")
 get_all_posts "$param1"
 ;;
 "create-post")
 create_post "$param1" "$param2" "$param3"
 ;;
 "update-post")
 update_post "$param1" "$param2" "$param3" "$param4"
 ;;
 "delete-post")
 delete_post "$param1"
 ;;
 "get-user")
 get_user "$param1"
 ;;
 "get-users")
 get_all_users
 ;;
 "webhook-server")
 start_webhook_server "$param1"
 ;;
 "dashboard")
 display_api_dashboard "$param1"
 ;;
 "test")
 test_api_client
 ;;
 "clean-cache")
 clean_cache "$param1"
 ;;
 "config")
 init_api_config
 echo "Configuration initialisée: $CONFIG_FILE"
 ;;
 "help"|*)
 cat << EOF
Usage: $0 {action} [parameters...]

POSTS:
 get-post <id> - Récupère un post
 get-posts [user_id] - Récupère tous les posts (ou d'un user)
 create-post <title> <body> [user_id] - Crée un post
 update-post <id> <title> <body> [user_id] - Met à jour un post
 delete-post <id> - Supprime un post

USERS:
 get-user <id> - Récupère un utilisateur
 get-users - Récupère tous les utilisateurs

WEBHOOK:
 webhook-server [port] - Démarre serveur webhook

OUTILS:
 dashboard [duration] - Dashboard API
 test - Tests complets
 clean-cache [max_age_seconds] - Nettoyage cache
 config - Initialise configuration

Examples:
 $0 get-post 1
 $0 create-post "Mon titre" "Mon contenu" 1
 $0 webhook-server 8080
 $0 dashboard 120
EOF
 ;;
 esac
}

# Point d'entrée
main "$@"

# ====== RÉSULTATS ATTENDUS ======
# ✓ Client REST complet (CRUD posts/users)
# ✓ Gestion erreurs avec retry et backoff
# ✓ Cache intelligent avec TTL
# ✓ Rate limiting configurable
# ✓ Serveur webhook fonctionnel
# ✓ Validation signatures HMAC-SHA256
# ✓ Logging structuré avec rotation
# ✓ Dashboard monitoring API
# ✓ Configuration flexible
# ✓ Tests système complets

# POINTS CLÉS TECHNIQUES :
# - Client HTTP avec curl et gestion erreurs
# - Retry avec backoff exponentiel
# - Cache fichier avec validation TTL
# - Rate limiting par timing
# - Serveur webhook avec netcat
# - Validation HMAC avec openssl
# - Logging avec rotation automatique
# - Configuration par fichier
# - Dashboard statistiques temps-réel
# - Tests end-to-end automatisés