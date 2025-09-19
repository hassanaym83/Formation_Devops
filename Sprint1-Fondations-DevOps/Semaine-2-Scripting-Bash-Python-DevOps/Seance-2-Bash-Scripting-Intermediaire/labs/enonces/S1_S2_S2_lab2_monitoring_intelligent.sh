#!/bin/bash
# S1_S2_S2_LAB2 - Monitoring intelligent et alertes
# DURÉE : 20 minutes

# OBJECTIF :
# Implémenter un système de monitoring avec collecte de métriques 
# et alertes automatiques pour infrastructure de production.

# CONSIGNES :
# 1. Implémentez la collecte de métriques système (CPU, RAM, disque)
# 2. Créez le système de définition et vérification de seuils
# 3. Développez le système d'alertes (email, webhook, Slack)
# 4. Testez avec différents scénarios de charge

# SPÉCIFICATIONS TECHNIQUES :
# - Métriques : CPU, mémoire, disque, services
# - Seuils configurables par métrique
# - Alertes : email, webhook, notifications
# - Dashboard temps-réel en console
# - Historique des métriques avec timestamp

# RÉSULTAT ATTENDU :
# Un système de monitoring proactif qui surveille l'infrastructure,
# détecte les anomalies et envoie des alertes automatiques.

# ====== TEMPLATE DE DÉPART ======

#!/bin/bash
set -euo pipefail

# TODO: Configuration des seuils d'alerte
# readonly CPU_THRESHOLD=80
# readonly MEMORY_THRESHOLD=85
# readonly DISK_THRESHOLD=90
# readonly LOG_FILE="/var/log/monitoring.log"

# TODO: Fonction de collecte de métriques
# collect_system_metrics() {
# # Collectez CPU : top -bn1 | grep "Cpu(s)"
# # Collectez mémoire : free | grep Mem
# # Collectez disque : df -h /
# # Retournez format: "CPU:XX,MEM:XX,DISK:XX"
# }

# TODO: Fonction de vérification des seuils
# check_thresholds() {
# local metrics="$1"
# # Parsez les métriques
# # Comparez avec les seuils
# # Déclenchez des alertes si nécessaire
# }

# TODO: Fonction d'envoi d'alertes
# send_alert() {
# local metric="$1"
# local value="$2"
# local threshold="$3"
# # Loggez l'alerte
# # Envoyez email (simulation)
# # Envoyez webhook (simulation)
# # Notifiez Slack (simulation)
# }

# TODO: Fonction de monitoring des services
# check_services() {
# local services=("nginx" "mysql" "redis")
# # Vérifiez chaque service avec systemctl
# # Alertez si service arrêté
# }

# TODO: Dashboard temps-réel
# display_dashboard() {
# # Affichez métriques en temps-réel
# # Utilisez clear + sleep pour actualisation
# # Format : tableau avec couleurs
# }

# TODO: Fonction de monitoring continu
# start_monitoring() {
# local interval="${1:-30}"
# # Boucle de monitoring
# # Collecte → Vérification → Alertes → Attente
# }

# TODO: Fonction principale
# main() {
# local mode="${1:-once}"
# 
# case "$mode" in
# "once") 
# collect_system_metrics
# check_thresholds "$metrics"
# ;;
# "continuous")
# start_monitoring 30
# ;;
# "dashboard")
# display_dashboard
# ;;
# esac
# }

# main "$@"

# ====== TESTS À EFFECTUER ======
# 1. ./script.sh once # Vérification unique
# 2. ./script.sh continuous # Monitoring continu
# 3. ./script.sh dashboard # Dashboard temps-réel
# 4. Simuler charge élevée pour tester alertes

# CRITÈRES D'ÉVALUATION :
# □ Métriques collectées (CPU, mémoire, disque)
# □ Seuils configurables
# □ Alertes fonctionnelles
# □ Monitoring des services
# □ Dashboard temps-réel
# □ Logs structurés avec timestamp