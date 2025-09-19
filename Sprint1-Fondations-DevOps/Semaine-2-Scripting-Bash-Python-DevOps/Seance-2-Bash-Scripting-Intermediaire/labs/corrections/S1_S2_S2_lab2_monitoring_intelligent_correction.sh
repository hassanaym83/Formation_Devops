#!/bin/bash
# S1_S2_S2_LAB2 - CORRECTION - Monitoring intelligent avec métriques
# DURÉE : 20 minutes
# NIVEAU : Intermédiaire

set -euo pipefail

# ====== CORRECTION COMPLÈTE ======

# Configuration monitoring
readonly METRICS_DIR="/tmp/metrics"
readonly ALERTS_FILE="/tmp/alerts.log"
readonly THRESHOLDS_CONFIG="/tmp/thresholds.conf"
readonly SERVICES=("web" "db" "cache" "api")

# Initialisation
mkdir -p "$METRICS_DIR"
touch "$ALERTS_FILE"

# Configuration des seuils par défaut
init_thresholds() {
 cat > "$THRESHOLDS_CONFIG" << 'EOF'
# Configuration seuils monitoring
cpu_warning=70
cpu_critical=85
memory_warning=80
memory_critical=90
disk_warning=75
disk_critical=85
response_time_warning=2000
response_time_critical=5000
error_rate_warning=5
error_rate_critical=10
EOF
}

# Chargement configuration
load_thresholds() {
 if [[ -f "$THRESHOLDS_CONFIG" ]]; then
 source "$THRESHOLDS_CONFIG"
 else
 init_thresholds
 source "$THRESHOLDS_CONFIG"
 fi
}

# Logging avec niveaux
log_metric() {
 local level="$1"
 local service="$2"
 local metric="$3"
 local value="$4"
 local threshold="${5:-N/A}"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 
 echo "[$timestamp] [$level] $service.$metric=$value (seuil:$threshold)" | tee -a "$ALERTS_FILE"
}

# Collecte métriques système
collect_system_metrics() {
 local service="$1"
 local timestamp=$(date +%s)
 
 # CPU utilization
 local cpu_usage
 cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 | cut -d',' -f1 || echo "50")
 
 # Memory utilization
 local memory_usage
 memory_usage=$(free | grep Mem | awk '{printf "%.1f", ($3/$2) * 100.0}' || echo "60")
 
 # Disk utilization
 local disk_usage
 disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1 || echo "40")
 
 # Load average
 local load_avg
 load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | cut -d',' -f1 || echo "1.5")
 
 # Sauvegarde métriques
 cat > "$METRICS_DIR/${service}_${timestamp}.metrics" << EOF
timestamp=$timestamp
service=$service
cpu_usage=$cpu_usage
memory_usage=$memory_usage 
disk_usage=$disk_usage
load_average=$load_avg
EOF
 
 echo "$METRICS_DIR/${service}_${timestamp}.metrics"
}

# Collecte métriques applicatives
collect_application_metrics() {
 local service="$1"
 local timestamp=$(date +%s)
 
 # Simulation métriques applicatives
 local response_time=$((RANDOM % 3000 + 500)) # 500-3500ms
 local error_rate=$((RANDOM % 15)) # 0-15%
 local throughput=$((RANDOM % 1000 + 100)) # 100-1100 req/min
 local active_sessions=$((RANDOM % 500 + 50)) # 50-550 sessions
 
 # Métriques spécifiques par service
 case "$service" in
 "web")
 local page_load_time=$((RANDOM % 2000 + 1000)) # 1-3s
 local concurrent_users=$((RANDOM % 200 + 10)) # 10-210
 echo "page_load_time=$page_load_time" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 echo "concurrent_users=$concurrent_users" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 ;;
 "db")
 local query_time=$((RANDOM % 1000 + 100)) # 100-1100ms
 local active_connections=$((RANDOM % 100 + 5)) # 5-105
 echo "query_time=$query_time" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 echo "active_connections=$active_connections" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 ;;
 "cache")
 local hit_rate=$((RANDOM % 30 + 70)) # 70-100%
 local evictions=$((RANDOM % 50)) # 0-50
 echo "hit_rate=$hit_rate" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 echo "evictions=$evictions" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 ;;
 "api")
 local api_calls=$((RANDOM % 500 + 100)) # 100-600 calls/min
 local auth_failures=$((RANDOM % 20)) # 0-20
 echo "api_calls=$api_calls" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 echo "auth_failures=$auth_failures" >> "$METRICS_DIR/${service}_${timestamp}.metrics"
 ;;
 esac
 
 # Métriques communes
 cat >> "$METRICS_DIR/${service}_${timestamp}.metrics" << EOF
response_time=$response_time
error_rate=$error_rate
throughput=$throughput
active_sessions=$active_sessions
EOF
}

# Analyse et alertes intelligentes
analyze_metrics_and_alert() {
 local service="$1"
 local metrics_file="$2"
 
 # Chargement métriques
 source "$metrics_file"
 
 # Chargement seuils
 load_thresholds
 
 # Analyse CPU
 if (( $(echo "$cpu_usage >= $cpu_critical" | bc -l) )); then
 log_metric "CRITICAL" "$service" "cpu_usage" "$cpu_usage%" "$cpu_critical%"
 trigger_alert "$service" "CPU" "CRITICAL" "$cpu_usage%"
 elif (( $(echo "$cpu_usage >= $cpu_warning" | bc -l) )); then
 log_metric "WARNING" "$service" "cpu_usage" "$cpu_usage%" "$cpu_warning%"
 fi
 
 # Analyse Memory
 if (( $(echo "$memory_usage >= $memory_critical" | bc -l) )); then
 log_metric "CRITICAL" "$service" "memory_usage" "$memory_usage%" "$memory_critical%" 
 trigger_alert "$service" "MEMORY" "CRITICAL" "$memory_usage%"
 elif (( $(echo "$memory_usage >= $memory_warning" | bc -l) )); then
 log_metric "WARNING" "$service" "memory_usage" "$memory_usage%" "$memory_warning%"
 fi
 
 # Analyse Disk
 if (( disk_usage >= disk_critical )); then
 log_metric "CRITICAL" "$service" "disk_usage" "$disk_usage%" "$disk_critical%"
 trigger_alert "$service" "DISK" "CRITICAL" "$disk_usage%"
 elif (( disk_usage >= disk_warning )); then
 log_metric "WARNING" "$service" "disk_usage" "$disk_usage%" "$disk_warning%"
 fi
 
 # Analyse Response Time
 if (( response_time >= response_time_critical )); then
 log_metric "CRITICAL" "$service" "response_time" "${response_time}ms" "${response_time_critical}ms"
 trigger_alert "$service" "RESPONSE_TIME" "CRITICAL" "${response_time}ms"
 elif (( response_time >= response_time_warning )); then
 log_metric "WARNING" "$service" "response_time" "${response_time}ms" "${response_time_warning}ms"
 fi
 
 # Analyse Error Rate
 if (( error_rate >= error_rate_critical )); then
 log_metric "CRITICAL" "$service" "error_rate" "$error_rate%" "$error_rate_critical%"
 trigger_alert "$service" "ERROR_RATE" "CRITICAL" "$error_rate%"
 elif (( error_rate >= error_rate_warning )); then
 log_metric "WARNING" "$service" "error_rate" "$error_rate%" "$error_rate_warning%"
 fi
 
 # Analyses spécifiques par service
 case "$service" in
 "cache")
 if (( hit_rate < 70 )); then
 log_metric "WARNING" "$service" "hit_rate" "$hit_rate%" "70%"
 fi
 ;;
 "db")
 if (( query_time > 1000 )); then
 log_metric "WARNING" "$service" "query_time" "${query_time}ms" "1000ms"
 fi
 ;;
 esac
}

# Déclenchement alertes
trigger_alert() {
 local service="$1"
 local metric="$2"
 local level="$3"
 local value="$4"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 
 # Formatage alerte
 local alert_message="[ALERT $level] $service.$metric = $value à $timestamp"
 
 # Enregistrement alerte
 echo "$alert_message" >> "$ALERTS_FILE"
 
 # Actions automatiques selon niveau
 case "$level" in
 "CRITICAL")
 echo "🚨 $alert_message"
 # Simulation notification (Slack, email, etc.)
 auto_remediation "$service" "$metric" "$value"
 ;;
 "WARNING")
 echo " $alert_message"
 ;;
 esac
}

# Remédiation automatique
auto_remediation() {
 local service="$1"
 local metric="$2"
 local value="$3"
 
 log_metric "INFO" "$service" "auto_remediation" "started" "$metric:$value"
 
 case "$metric" in
 "CPU"|"MEMORY")
 echo " Redémarrage service $service (surcharge $metric)"
 # service $service restart
 ;;
 "DISK")
 echo "🧹 Nettoyage disque pour $service"
 # find /tmp -name "*.log" -mtime +7 -delete
 ;;
 "RESPONSE_TIME")
 echo " Optimisation cache pour $service"
 # cache warmup or scaling
 ;;
 "ERROR_RATE")
 echo " Investigation erreurs $service"
 # log analysis and error tracking
 ;;
 esac
 
 log_metric "INFO" "$service" "auto_remediation" "completed" "$metric"
}

# Dashboard monitoring en temps réel
display_monitoring_dashboard() {
 local service="${1:-all}"
 local duration="${2:-60}" # secondes
 
 clear
 echo "====== DASHBOARD MONITORING TEMPS-RÉEL ======"
 echo "Service: $service | Durée: ${duration}s | $(date)"
 echo
 
 if [[ "$service" == "all" ]]; then
 for svc in "${SERVICES[@]}"; do
 show_service_metrics "$svc"
 done
 else
 show_service_metrics "$service"
 fi
 
 echo
 echo "====== ALERTES RÉCENTES ======"
 tail -5 "$ALERTS_FILE" 2>/dev/null || echo "Aucune alerte récente"
 
 echo
 echo "====== MÉTRIQUES TEMPS-RÉEL ======"
 for ((i=1; i<=duration; i++)); do
 printf "Progress: [%-50s] %d%%\r" \
 "$(printf "%*s" $((i*50/duration)) "" | tr ' ' '=')" \
 $((i*100/duration))
 sleep 1
 done
 echo
}

# Affichage métriques service
show_service_metrics() {
 local service="$1"
 local latest_metrics
 
 # Récupération dernières métriques
 latest_metrics=$(ls -t "$METRICS_DIR/${service}_"*.metrics 2>/dev/null | head -1)
 
 if [[ -f "$latest_metrics" ]]; then
 source "$latest_metrics"
 
 echo "[$service]"
 echo " CPU: ${cpu_usage}% | Memory: ${memory_usage}%"
 echo " Disk: ${disk_usage}% | Load: $load_average"
 echo " Response: ${response_time}ms | Errors: ${error_rate}%"
 echo " Throughput: $throughput req/min"
 
 # Métriques spécifiques
 case "$service" in
 "web")
 echo " Page Load: ${page_load_time:-N/A}ms | Users: ${concurrent_users:-N/A}"
 ;;
 "db")
 echo " Query Time: ${query_time:-N/A}ms | Connections: ${active_connections:-N/A}"
 ;;
 "cache")
 echo " Hit Rate: ${hit_rate:-N/A}% | Evictions: ${evictions:-N/A}"
 ;;
 "api")
 echo " API Calls: ${api_calls:-N/A}/min | Auth Failures: ${auth_failures:-N/A}"
 ;;
 esac
 echo
 else
 echo "[$service] - Aucune métrique disponible"
 echo
 fi
}

# Monitoring continu en arrière-plan
start_continuous_monitoring() {
 local interval="${1:-30}" # secondes
 local services_list="${2:-${SERVICES[*]}}"
 
 echo " Démarrage monitoring continu (intervalle: ${interval}s)"
 echo "Services: $services_list"
 
 # Boucle monitoring
 while true; do
 for service in $services_list; do
 # Collecte métriques
 local metrics_file
 metrics_file=$(collect_system_metrics "$service")
 collect_application_metrics "$service"
 
 # Analyse et alertes
 analyze_metrics_and_alert "$service" "$metrics_file"
 done
 
 sleep "$interval"
 done
}

# Tests système monitoring
test_monitoring_system() {
 echo "====== TESTS SYSTÈME MONITORING ======"
 
 # Test 1: Collecte métriques
 echo "[TEST 1] Collecte métriques"
 local test_metrics
 test_metrics=$(collect_system_metrics "test_service")
 [[ -f "$test_metrics" ]] && echo "✓ Collecte OK" || echo "✗ Collecte KO"
 
 # Test 2: Configuration seuils
 echo "[TEST 2] Configuration seuils"
 init_thresholds
 [[ -f "$THRESHOLDS_CONFIG" ]] && echo "✓ Configuration OK" || echo "✗ Configuration KO"
 
 # Test 3: Analyse métriques
 echo "[TEST 3] Analyse métriques"
 collect_application_metrics "test_service"
 analyze_metrics_and_alert "test_service" "$test_metrics" && echo "✓ Analyse OK" || echo "✗ Analyse KO"
 
 # Test 4: Alerting
 echo "[TEST 4] Système d'alertes"
 trigger_alert "test_service" "CPU" "WARNING" "75%" && echo "✓ Alertes OK" || echo "✗ Alertes KO"
 
 # Test 5: Dashboard
 echo "[TEST 5] Dashboard"
 show_service_metrics "test_service" >/dev/null && echo "✓ Dashboard OK" || echo "✗ Dashboard KO"
 
 echo "====== FIN TESTS ======"
}

# Fonction principale
main() {
 local action="${1:-help}"
 local service="${2:-all}"
 local duration="${3:-30}"
 
 case "$action" in
 "collect")
 echo " Collecte métriques pour $service"
 if [[ "$service" == "all" ]]; then
 for svc in "${SERVICES[@]}"; do
 metrics_file=$(collect_system_metrics "$svc")
 collect_application_metrics "$svc"
 analyze_metrics_and_alert "$svc" "$metrics_file"
 done
 else
 metrics_file=$(collect_system_metrics "$service")
 collect_application_metrics "$service"
 analyze_metrics_and_alert "$service" "$metrics_file"
 fi
 ;;
 "monitor")
 start_continuous_monitoring "$duration" "$service"
 ;;
 "dashboard")
 display_monitoring_dashboard "$service" "$duration" 
 ;;
 "alerts")
 echo "====== ALERTES ACTIVES ======"
 tail -20 "$ALERTS_FILE" 2>/dev/null || echo "Aucune alerte"
 ;;
 "test")
 test_monitoring_system
 ;;
 "config")
 init_thresholds
 echo "Configuration seuils initialisée: $THRESHOLDS_CONFIG"
 ;;
 "help"|*)
 cat << EOF
Usage: $0 {collect|monitor|dashboard|alerts|test|config} [service] [duration]

Commands:
 collect - Collecte métriques et analyse
 monitor - Monitoring continu en arrière-plan
 dashboard - Dashboard temps-réel
 alerts - Affiche alertes récentes
 test - Tests système monitoring
 config - Initialise configuration seuils

Services: web, db, cache, api, all
Duration: en secondes (défaut: 30)

Examples:
 $0 collect web
 $0 monitor all 60
 $0 dashboard db 120
 $0 alerts
EOF
 ;;
 esac
}

# Point d'entrée
main "$@"

# ====== RÉSULTATS ATTENDUS ======
# ✓ Collecte métriques système et applicatives
# ✓ Configuration seuils flexible
# ✓ Analyse intelligente avec alertes
# ✓ Remédiation automatique
# ✓ Dashboard temps-réel
# ✓ Monitoring continu
# ✓ Logging structuré
# ✓ Tests système complets

# POINTS CLÉS TECHNIQUES :
# - Métriques système via outils standard (top, free, df)
# - Métriques applicatives simulées par service
# - Seuils configurables par fichier
# - Alertes avec niveaux (WARNING, CRITICAL)
# - Remédiation automatique par type métrique 
# - Dashboard interactif temps-réel
# - Monitoring continu avec boucle
# - Tests validation complets