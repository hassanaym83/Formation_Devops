#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 3: Monitoring système de base - CORRECTION
# ==================================================================================

# Configuration globale
set -euo pipefail

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
info() { echo -e "${BLUE}[INFO]${NC} $*"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# Vérification des privilèges
check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        error "Ce script doit être exécuté avec les privilèges root"
        error "Utilisation: sudo $0"
        exit 1
    fi
}

# Fonction principale d'installation
install_monitoring_system() {
    info "=== CORRECTION LAB 3: Monitoring système ==="
    
    # Étape 1: Installer les dépendances
    info "Installation des dépendances..."
    apt update >/dev/null 2>&1
    apt install -y bc curl >/dev/null 2>&1
    
    # Étape 2: Créer la structure de répertoires
    info "Création de la structure de répertoires..."
    mkdir -p /opt/monitoring
    
    # Étape 3: Créer le script de monitoring
    info "Création du script de monitoring..."
    cat > /opt/monitoring/check_system.sh << 'EOF'
#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/system-monitoring.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Seuils d'alerte (configurables)
CPU_LIMITE=80
MEMOIRE_LIMITE=85
DISQUE_LIMITE=90
LOAD_LIMITE=3.0

# Créer le fichier de log s'il n'existe pas
touch "$LOG_FILE"

# Fonction de logging
log_message() {
    echo "$1" >> "$LOG_FILE"
}

# Fonction pour envoyer une alerte
send_alert() {
    local level=$1
    local message=$2
    log_message "$DATE - $level: $message"
    
    # Optionnel: envoyer aussi vers syslog
    logger -t "system-monitoring" "[$level] $message"
}

# === COLLECTE DES MÉTRIQUES ===

# 1. Collecte CPU
collect_cpu_metrics() {
    # Utilisation CPU (moyenne sur 1 seconde)
    local cpu_usage
    cpu_usage=$(top -bn2 -d1 | grep "Cpu(s)" | tail -1 | awk '{print $2}' | cut -d'%' -f1)
    
    # Si top ne fonctionne pas, utiliser /proc/stat
    if [[ ! "$cpu_usage" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        cpu_usage=$(awk '/^cpu / {usage=($2+$4)*100/($2+$3+$4+$5)} END {printf "%.1f", usage}' /proc/stat)
    fi
    
    echo "${cpu_usage:-0}"
}

# 2. Collecte mémoire
collect_memory_metrics() {
    local mem_usage
    mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    echo "${mem_usage:-0}"
}

# 3. Collecte disque
collect_disk_metrics() {
    local disk_usage
    disk_usage=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    echo "${disk_usage:-0}"
}

# 4. Collecte load average
collect_load_metrics() {
    local load_avg
    load_avg=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)
    echo "${load_avg:-0}"
}

# 5. Collecte informations supplémentaires
collect_additional_info() {
    local processes users disk_io
    processes=$(ps aux | wc -l)
    users=$(who | wc -l)
    
    # Informations sur l'I/O disque (optionnel)
    if command -v iostat >/dev/null; then
        disk_io=$(iostat -d 1 1 | grep -A1 "Device" | tail -1 | awk '{print $4}' || echo "N/A")
    else
        disk_io="N/A"
    fi
    
    echo "Processes:$processes Users:$users DiskIO:$disk_io"
}

# === COLLECTE PRINCIPALE ===

# Collecter toutes les métriques
CPU_USAGE=$(collect_cpu_metrics)
MEMOIRE_USAGE=$(collect_memory_metrics)
DISQUE_USAGE=$(collect_disk_metrics)
LOAD_AVG=$(collect_load_metrics)
ADDITIONAL_INFO=$(collect_additional_info)

# Écrire les métriques dans le log
log_message "$DATE - CPU: ${CPU_USAGE}% | Mémoire: ${MEMOIRE_USAGE}% | Disque: ${DISQUE_USAGE}% | Load: ${LOAD_AVG} | $ADDITIONAL_INFO"

# === VÉRIFICATION DES SEUILS ET ALERTES ===

# Alertes CPU
if (( $(echo "$CPU_USAGE > $CPU_LIMITE" | bc -l) )); then
    send_alert "ALERTE" "CPU élevé (${CPU_USAGE}% > ${CPU_LIMITE}%)"
fi

# Alertes mémoire
if [ "$MEMOIRE_USAGE" -gt "$MEMOIRE_LIMITE" ]; then
    send_alert "ALERTE" "Mémoire élevée (${MEMOIRE_USAGE}% > ${MEMOIRE_LIMITE}%)"
fi

# Alertes disque
if [ "$DISQUE_USAGE" -gt "$DISQUE_LIMITE" ]; then
    send_alert "ALERTE" "Disque plein (${DISQUE_USAGE}% > ${DISQUE_LIMITE}%)"
fi

# Alertes load average
if (( $(echo "$LOAD_AVG > $LOAD_LIMITE" | bc -l) )); then
    send_alert "ALERTE" "Load average élevé (${LOAD_AVG} > ${LOAD_LIMITE})"
fi

# === DÉTECTION D'ANOMALIES ===

# Vérifier si des processus consomment trop de ressources
HIGH_CPU_PROCESSES=$(ps aux --sort=-%cpu | head -5 | awk 'NR>1 && $3>50 {print $11 "(" $3 "%)"}' | tr '\n' ' ')
if [ -n "$HIGH_CPU_PROCESSES" ]; then
    send_alert "INFO" "Processus gourmands CPU: $HIGH_CPU_PROCESSES"
fi

HIGH_MEM_PROCESSES=$(ps aux --sort=-%mem | head -5 | awk 'NR>1 && $4>20 {print $11 "(" $4 "%)"}' | tr '\n' ' ')
if [ -n "$HIGH_MEM_PROCESSES" ]; then
    send_alert "INFO" "Processus gourmands mémoire: $HIGH_MEM_PROCESSES"
fi

# Vérifier l'espace disque sur les autres partitions importantes
for mount_point in /var /home /tmp; do
    if mountpoint -q "$mount_point" 2>/dev/null; then
        local usage
        usage=$(df "$mount_point" | tail -1 | awk '{print $5}' | cut -d'%' -f1)
        if [ "$usage" -gt "$DISQUE_LIMITE" ]; then
            send_alert "ALERTE" "Partition $mount_point pleine (${usage}%)"
        fi
    fi
done

# Sortie avec code de retour basé sur les alertes
if grep -q "ALERTE.*$(date '+%Y-%m-%d %H:%M')" "$LOG_FILE"; then
    exit 1  # Il y a des alertes
else
    exit 0  # Pas d'alertes
fi
EOF
    
    # Rendre le script exécutable
    chmod +x /opt/monitoring/check_system.sh
    success "Script de monitoring créé: /opt/monitoring/check_system.sh"
    
    # Étape 4: Tester le script manuellement
    info "Test du script de monitoring..."
    /opt/monitoring/check_system.sh
    
    if [ -f /var/log/system-monitoring.log ]; then
        success "Script testé avec succès"
        info "Dernière entrée du log:"
        tail -1 /var/log/system-monitoring.log
    else
        error "Problème avec l'exécution du script"
        return 1
    fi
    
    # Étape 5: Créer le service systemd
    info "Création du service systemd..."
    cat > /etc/systemd/system/system-monitoring.service << 'EOF'
[Unit]
Description=Monitoring système
Documentation=file:///opt/monitoring/README.txt
After=network.target

[Service]
Type=oneshot
ExecStart=/opt/monitoring/check_system.sh
User=root
Group=root

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=system-monitoring

# Sécurité
NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=/var/log

# Timeout et retry
TimeoutStartSec=30
# En cas d'échec (alertes), ne pas redémarrer
Restart=no
EOF
    
    success "Service systemd créé: /etc/systemd/system/system-monitoring.service"
    
    # Étape 6: Créer le timer systemd
    info "Création du timer systemd..."
    cat > /etc/systemd/system/system-monitoring.timer << 'EOF'
[Unit]
Description=Timer pour monitoring système
Documentation=file:///opt/monitoring/README.txt
Requires=system-monitoring.service

[Timer]
# Exécution toutes les 2 minutes
OnCalendar=*:*:0/120
# Précision de 30 secondes
AccuracySec=30s
# Pas de persistance (trop fréquent)
Persistent=false

[Install]
WantedBy=timers.target
EOF
    
    success "Timer systemd créé: /etc/systemd/system/system-monitoring.timer"
    
    # Étape 7: Recharger systemd et activer
    info "Activation du monitoring..."
    systemctl daemon-reload
    systemctl enable system-monitoring.timer
    systemctl start system-monitoring.timer
    
    success "Monitoring activé et démarré"
}

# Création d'un script de tableau de bord
create_dashboard() {
    info "Création d'un dashboard..."
    
    cat > /opt/monitoring/dashboard.sh << 'EOF'
#!/bin/bash

# Dashboard pour le monitoring
LOG_FILE="/var/log/system-monitoring.log"

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo -e "${BOLD}${BLUE}=== DASHBOARD MONITORING SYSTÈME ===${NC}"
echo -e "${BOLD}Heure: $(date)${NC}"
echo

# Métriques actuelles
if [ -f "$LOG_FILE" ]; then
    LAST_ENTRY=$(tail -1 "$LOG_FILE")
    if echo "$LAST_ENTRY" | grep -q "CPU:"; then
        CPU=$(echo "$LAST_ENTRY" | sed 's/.*CPU: \([0-9.]*\)%.*/\1/')
        MEM=$(echo "$LAST_ENTRY" | sed 's/.*Mémoire: \([0-9]*\)%.*/\1/')
        DISK=$(echo "$LAST_ENTRY" | sed 's/.*Disque: \([0-9]*\)%.*/\1/')
        LOAD=$(echo "$LAST_ENTRY" | sed 's/.*Load: \([0-9.]*\).*/\1/')
        
        echo -e "${BOLD}MÉTRIQUES ACTUELLES:${NC}"
        
        # CPU avec couleur
        CPU_COLOR=$GREEN
        [ $(echo "$CPU > 75" | bc -l) -eq 1 ] && CPU_COLOR=$YELLOW
        [ $(echo "$CPU > 90" | bc -l) -eq 1 ] && CPU_COLOR=$RED
        echo -e "  CPU:     ${CPU_COLOR}${CPU}%${NC}"
        
        # Mémoire avec couleur
        MEM_COLOR=$GREEN
        [ "$MEM" -gt 75 ] && MEM_COLOR=$YELLOW
        [ "$MEM" -gt 90 ] && MEM_COLOR=$RED
        echo -e "  Mémoire: ${MEM_COLOR}${MEM}%${NC}"
        
        # Disque avec couleur
        DISK_COLOR=$GREEN
        [ "$DISK" -gt 80 ] && DISK_COLOR=$YELLOW
        [ "$DISK" -gt 90 ] && DISK_COLOR=$RED
        echo -e "  Disque:  ${DISK_COLOR}${DISK}%${NC}"
        
        # Load average
        LOAD_COLOR=$GREEN
        [ $(echo "$LOAD > 2" | bc -l) -eq 1 ] && LOAD_COLOR=$YELLOW
        [ $(echo "$LOAD > 4" | bc -l) -eq 1 ] && LOAD_COLOR=$RED
        echo -e "  Load:    ${LOAD_COLOR}${LOAD}${NC}"
    fi
fi

echo
echo -e "${BOLD}ALERTES RÉCENTES (dernières 24h):${NC}"
if [ -f "$LOG_FILE" ]; then
    TODAY=$(date +%Y-%m-%d)
    ALERTS=$(grep "ALERTE" "$LOG_FILE" | grep "$TODAY" | tail -5)
    
    if [ -n "$ALERTS" ]; then
        echo "$ALERTS" | while read -r alert; do
            echo -e "  ${RED}● ${alert}${NC}"
        done
    else
        echo -e "  ${GREEN}✓ Aucune alerte aujourd'hui${NC}"
    fi
else
    echo -e "  ${YELLOW}! Fichier de log non trouvé${NC}"
fi

echo
echo -e "${BOLD}STATISTIQUES:${NC}"
if [ -f "$LOG_FILE" ]; then
    TOTAL_ENTRIES=$(wc -l < "$LOG_FILE")
    TODAY_ENTRIES=$(grep "$(date +%Y-%m-%d)" "$LOG_FILE" | wc -l)
    TODAY_ALERTS=$(grep "ALERTE.*$(date +%Y-%m-%d)" "$LOG_FILE" | wc -l)
    
    echo "  Entrées totales: $TOTAL_ENTRIES"
    echo "  Entrées aujourd'hui: $TODAY_ENTRIES"
    echo "  Alertes aujourd'hui: $TODAY_ALERTS"
fi

echo
echo -e "${BOLD}COMMANDES UTILES:${NC}"
echo "  systemctl status system-monitoring.timer"
echo "  tail -f /var/log/system-monitoring.log"
echo "  journalctl -u system-monitoring.service -f"

echo
echo "Appuyez sur Ctrl+C pour quitter"

# Mode rafraîchissement automatique si demandé
if [ "${1:-}" = "auto" ]; then
    sleep 10
    exec $0 auto
fi
EOF
    
    chmod +x /opt/monitoring/dashboard.sh
    success "Dashboard créé: /opt/monitoring/dashboard.sh"
}

# Tests et validation
run_tests() {
    info "=== TESTS ET VALIDATION ==="
    
    # Test 1: Vérifier que le timer est actif
    info "Test 1: Vérification du statut du timer"
    if systemctl is-active --quiet system-monitoring.timer; then
        success "Le timer est actif"
        systemctl status system-monitoring.timer --no-pager -l
    else
        error "Le timer n'est pas actif"
        return 1
    fi
    
    # Test 2: Vérifier les prochaines exécutions
    info "Test 2: Vérification des prochaines exécutions"
    if systemctl list-timers system-monitoring.timer --no-pager | grep -q system-monitoring; then
        success "Timer planifié correctement"
        systemctl list-timers system-monitoring.timer --no-pager
    else
        error "Timer non trouvé dans la planification"
        return 1
    fi
    
    # Test 3: Exécution manuelle et vérification des logs
    info "Test 3: Exécution manuelle du monitoring"
    systemctl start system-monitoring.service
    sleep 3
    
    if [ -f /var/log/system-monitoring.log ]; then
        LOG_LINES=$(wc -l < /var/log/system-monitoring.log)
        success "Monitoring exécuté, $LOG_LINES entrées dans le log"
        info "Dernières métriques:"
        tail -2 /var/log/system-monitoring.log
    else
        error "Fichier de log non créé"
        return 1
    fi
    
    # Test 4: Test de charge CPU pour déclencher une alerte
    info "Test 4: Test de génération d'alerte CPU"
    info "Génération d'une charge CPU pendant 30 secondes..."
    
    # Créer une charge CPU
    timeout 30s bash -c 'while true; do :; done' &
    STRESS_PID=$!
    
    # Attendre un peu puis exécuter le monitoring
    sleep 20
    /opt/monitoring/check_system.sh
    
    # Nettoyer
    kill $STRESS_PID 2>/dev/null || true
    wait $STRESS_PID 2>/dev/null || true
    
    # Vérifier les alertes
    if grep -q "ALERTE.*CPU" /var/log/system-monitoring.log; then
        success "Alerte CPU générée avec succès"
    else
        warning "Aucune alerte CPU générée (charge peut-être insuffisante)"
    fi
    
    # Test 5: Vérifier les logs systemd
    info "Test 5: Vérification des logs systemd"
    if journalctl -u system-monitoring.service --since "5 minutes ago" --no-pager | grep -q "system-monitoring"; then
        success "Logs systemd présents"
    else
        warning "Pas de logs systemd récents trouvés"
    fi
    
    # Test 6: Test du dashboard
    info "Test 6: Test du dashboard"
    if /opt/monitoring/dashboard.sh | grep -q "DASHBOARD"; then
        success "Dashboard fonctionnel"
    else
        warning "Problème avec le dashboard"
    fi
}

# Affichage des informations utiles
show_info() {
    info "=== INFORMATIONS UTILES ==="
    
    echo "Gestion du monitoring:"
    echo "  systemctl status system-monitoring.timer    # Statut du timer"
    echo "  systemctl start system-monitoring.service   # Exécution manuelle"
    echo "  systemctl stop system-monitoring.timer      # Arrêter le monitoring"
    echo "  systemctl restart system-monitoring.timer   # Redémarrer le timer"
    echo
    echo "Surveillance et logs:"
    echo "  tail -f /var/log/system-monitoring.log      # Voir les métriques en temps réel"
    echo "  journalctl -u system-monitoring.service -f  # Logs systemd"
    echo "  /opt/monitoring/dashboard.sh                # Dashboard interactif"
    echo "  /opt/monitoring/dashboard.sh auto           # Dashboard auto-refresh"
    echo
    echo "Analyse des données:"
    echo "  grep ALERTE /var/log/system-monitoring.log  # Voir toutes les alertes"
    echo "  grep \$(date +%Y-%m-%d) /var/log/system-monitoring.log # Métriques du jour"
    echo "  grep 'CPU:.*9[0-9]%' /var/log/system-monitoring.log   # CPU > 90%"
    echo
    echo "Configuration:"
    echo "  Éditer /opt/monitoring/check_system.sh      # Modifier les seuils"
    echo "  Éditer /etc/systemd/system/system-monitoring.timer # Changer la fréquence"
    echo "  systemctl daemon-reload                     # Après modification"
    echo
    echo "Tests de charge:"
    echo "  stress --cpu 2 --timeout 60s               # Test CPU (si stress installé)"
    echo "  timeout 30s bash -c 'while true; do :; done' & # Test CPU"
    echo "  dd if=/dev/zero of=/tmp/bigfile bs=1M count=1000 # Test disque"
    echo
    echo "Fichiers du système:"
    echo "  /opt/monitoring/check_system.sh             # Script principal"
    echo "  /opt/monitoring/dashboard.sh                # Dashboard"
    echo "  /etc/systemd/system/system-monitoring.service # Service"
    echo "  /etc/systemd/system/system-monitoring.timer   # Timer"
    echo "  /var/log/system-monitoring.log              # Logs des métriques"
}

# Génération de documentation
create_documentation() {
    info "Génération de la documentation..."
    
    cat > /opt/monitoring/README.txt << 'EOF'
# Système de Monitoring

## Description
Système de monitoring basique qui surveille CPU, mémoire, disque et load average avec alertes automatiques.

## Composants
- Script: /opt/monitoring/check_system.sh
- Dashboard: /opt/monitoring/dashboard.sh  
- Service: /etc/systemd/system/system-monitoring.service
- Timer: /etc/systemd/system/system-monitoring.timer
- Logs: /var/log/system-monitoring.log

## Fonctionnalités
- Monitoring CPU, mémoire, disque, load average
- Seuils d'alerte configurables
- Détection des processus gourmands
- Surveillance de multiples partitions
- Logs détaillés avec horodatage
- Dashboard en temps réel
- Exécution toutes les 2 minutes
- Intégration syslog

## Seuils par défaut
- CPU: Warning > 80%, Critical > 90%
- Mémoire: Warning > 85%, Critical > 95%
- Disque: Warning > 90%, Critical > 95%
- Load Average: Warning > 3.0, Critical > 5.0

## Utilisation

### Commandes de base
```bash
# Gestion du timer
systemctl start/stop/status system-monitoring.timer

# Exécution manuelle
systemctl start system-monitoring.service
/opt/monitoring/check_system.sh

# Surveillance
tail -f /var/log/system-monitoring.log
/opt/monitoring/dashboard.sh
/opt/monitoring/dashboard.sh auto  # Auto-refresh

# Analyse
grep ALERTE /var/log/system-monitoring.log
grep $(date +%Y-%m-%d) /var/log/system-monitoring.log
```

### Personnalisation
```bash
# Modifier les seuils dans check_system.sh
CPU_LIMITE=70
MEMOIRE_LIMITE=80
DISQUE_LIMITE=85

# Modifier la fréquence dans system-monitoring.timer
OnCalendar=*:*:0/60  # Toutes les minutes
OnCalendar=*:0/5     # Toutes les 5 minutes

# Après modification
systemctl daemon-reload
systemctl restart system-monitoring.timer
```

## Format des logs
```
2024-09-14 15:30:00 - CPU: 25.5% | Mémoire: 67% | Disque: 45% | Load: 1.2 | Processes:156 Users:2
2024-09-14 15:30:00 - ALERTE: CPU élevé (85.2% > 80%)
2024-09-14 15:30:00 - INFO: Processus gourmands CPU: firefox(12.3%) chrome(8.9%)
```

## Dashboard
Le dashboard affiche:
- Métriques actuelles avec code couleur
- Alertes récentes (24h)
- Statistiques générales
- Commandes utiles

Codes couleur:
- Vert: Normal
- Jaune: Attention (seuil dépassé)  
- Rouge: Critique

## Tests de charge
```bash
# CPU
timeout 30s bash -c 'while true; do :; done' &

# Mémoire (si possible)
python3 -c "import numpy; a=numpy.zeros((100000,1000))"

# Disque
dd if=/dev/zero of=/tmp/bigfile bs=1M count=1000
```

## Dépannage
1. Timer inactif: `systemctl status system-monitoring.timer`
2. Script échoue: `/opt/monitoring/check_system.sh` (test manuel)
3. Pas de logs: Vérifier permissions `/var/log/`
4. bc non trouvé: `apt install bc`

## Extensions possibles
- Monitoring réseau (bande passante)
- Surveillance des services spécifiques
- Notifications email/Slack
- Base de données pour historique
- Interface web
- Prédictions de tendances
EOF
    
    success "Documentation créée: /opt/monitoring/README.txt"
}

# Nettoyage (fonction optionnelle)
cleanup_monitoring_system() {
    info "=== NETTOYAGE DU SYSTÈME DE MONITORING ==="
    
    # Arrêter et désactiver le timer
    systemctl stop system-monitoring.timer 2>/dev/null || true
    systemctl disable system-monitoring.timer 2>/dev/null || true
    
    # Supprimer les fichiers
    rm -f /etc/systemd/system/system-monitoring.timer
    rm -f /etc/systemd/system/system-monitoring.service
    rm -rf /opt/monitoring
    rm -f /var/log/system-monitoring.log
    
    # Recharger systemd
    systemctl daemon-reload
    systemctl reset-failed
    
    success "Système de monitoring supprimé complètement"
}

# Fonction principale
main() {
    case "${1:-install}" in
        "install")
            check_privileges
            install_monitoring_system
            create_dashboard
            run_tests
            create_documentation
            show_info
            success "Installation terminée avec succès!"
            info "Utilisez: /opt/monitoring/dashboard.sh pour voir le tableau de bord"
            ;;
        "test")
            check_privileges
            run_tests
            ;;
        "dashboard")
            /opt/monitoring/dashboard.sh "${2:-}"
            ;;
        "cleanup")
            check_privileges
            cleanup_monitoring_system
            ;;
        "info")
            show_info
            ;;
        *)
            echo "Usage: $0 [install|test|dashboard|cleanup|info]"
            echo "  install   : Installer et configurer le monitoring (défaut)"
            echo "  test      : Exécuter les tests seulement"
            echo "  dashboard : Afficher le dashboard [auto]"
            echo "  cleanup   : Supprimer complètement le système"
            echo "  info      : Afficher les informations d'utilisation"
            exit 1
            ;;
    esac
}

# Gestion des signaux
trap 'error "Script interrompu par l'\''utilisateur"; exit 1' SIGINT SIGTERM

# Exécution du script principal
main "$@"
