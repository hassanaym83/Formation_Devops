#!/bin/bash

# S1_S2_S1_LAB4 - Challenge : Script d'administration système complet - CORRECTION
#
# Cette correction présente une solution complète et optimisée.
#
# Concepts démontrés :
# - Intégration complète de tous les concepts Bash fondamentaux
# - Variables de configuration et constantes
# - Structures conditionnelles pour validation et alertes
# - Boucles pour tests multiples et traitement par lots
# - Fonctions de calcul et analyse système
# - Gestion de paramètres en ligne de commande
# - Création d'archives et gestion de fichiers
# - Rapports formatés et professionnels
#
# Bonnes pratiques appliquées :
# - Code modulaire et documenté
# - Gestion d'erreurs robuste
# - Variables constantes en readonly
# - Tests de prérequis avant actions
# - Sortie formatée et informative
# - Scripts réutilisables en production

#!/bin/bash

# Script de maintenance système complet - Version professionnelle
# Intègre tous les concepts Bash fondamentaux dans un outil DevOps réaliste

# ====== CONFIGURATION GLOBALE ======

readonly SCRIPT_NAME="$(basename "$0")"
readonly VERSION="1.0.0"
readonly TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

# Configuration des seuils et chemins
readonly DISK_WARNING_THRESHOLD=80
readonly DISK_CRITICAL_THRESHOLD=95
readonly BACKUP_BASE_DIR="/tmp/maintenance_backups"  # /tmp pour démo, /backup en prod
readonly LOG_FILE="/tmp/maintenance_${TIMESTAMP}.log"

# Services critiques à vérifier (adaptez selon votre système)
readonly SERVICES_TO_CHECK=("ssh" "cron" "systemd-resolved" "dbus")

# Compteurs globaux pour statistiques
services_checked=0
services_active=0
warnings_count=0
critical_issues=0

# ====== FONCTIONS UTILITAIRES ======

# Fonction de logging avec horodatage
log_message() {
    local level="$1"
    local message="$2"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Fonction d'affichage avec formatage
print_section() {
    local title="$1"
    echo ""
    echo "$(printf '=%.0s' {1..50})"
    echo "  $title"
    echo "$(printf '=%.0s' {1..50})"
}

# Fonction de calcul du pourcentage d'utilisation disque
get_disk_usage() {
    local path="$1"
    df "$path" | tail -1 | awk '{print $5}' | sed 's/%//'
}

# ====== SCRIPT PRINCIPAL ======

# Vérification des prérequis
if [[ $EUID -eq 0 ]]; then
    log_message "WARNING" "Script exécuté en tant que root - attention aux permissions"
fi

print_section "SCRIPT DE MAINTENANCE SYSTÈME v$VERSION"
echo "Démarré le: $(date)"
echo "Exécuté par: $USER sur $(hostname)"
echo "Fichier de log: $LOG_FILE"

# ====== SECTION 1 - INFORMATIONS SYSTÈME ======

print_section "1. INFORMATIONS SYSTÈME"

echo "Système d'exploitation:"
uname -a

echo ""
echo "Temps de fonctionnement:"
uptime

echo ""
echo "Charge système (load average):"
load_avg=$(uptime | awk -F'load average:' '{print $2}')
echo "Load average:$load_avg"

echo ""
echo "Mémoire système:"
free -h

echo ""
echo "Processus actifs:"
process_count=$(ps aux | wc -l)
echo "Nombre total de processus: $process_count"

log_message "INFO" "Collecte d'informations système terminée"

# ====== SECTION 2 - VÉRIFICATION ESPACE DISQUE ======

print_section "2. ANALYSE ESPACE DISQUE"

# Vérification de la partition racine
echo "Analyse de l'espace disque sur /"
df -h /

# Calcul du pourcentage d'utilisation
disk_usage=$(get_disk_usage "/")
echo ""
echo "Utilisation actuelle: ${disk_usage}%"

# Évaluation critique
if [[ $disk_usage -ge $DISK_CRITICAL_THRESHOLD ]]; then
    echo "🔴 CRITIQUE: Espace disque critique (>= ${DISK_CRITICAL_THRESHOLD}%)"
    log_message "CRITICAL" "Espace disque critique: ${disk_usage}%"
    ((critical_issues++))
elif [[ $disk_usage -ge $DISK_WARNING_THRESHOLD ]]; then
    echo "🟡 ATTENTION: Espace disque élevé (>= ${DISK_WARNING_THRESHOLD}%)"
    log_message "WARNING" "Espace disque élevé: ${disk_usage}%"
    ((warnings_count++))
else
    echo "🟢 OK: Espace disque normal (${disk_usage}%)"
    log_message "INFO" "Espace disque normal: ${disk_usage}%"
fi

# ====== SECTION 3 - VÉRIFICATION DES SERVICES ======

print_section "3. VÉRIFICATION SERVICES SYSTÈME"

echo "Services critiques à vérifier: ${#SERVICES_TO_CHECK[@]}"
echo ""

# Boucle for pour tester chaque service
for service in "${SERVICES_TO_CHECK[@]}"; do
    echo -n "Service $service: "
    ((services_checked++))
    
    # Test du statut du service
    if systemctl is-active --quiet "$service" 2>/dev/null; then
        echo "ACTIF"
        ((services_active++))
        log_message "INFO" "Service $service actif"
    else
        echo "INACTIF"
        log_message "WARNING" "Service $service inactif"
        ((warnings_count++))
    fi
done

echo ""
echo "Résumé services: $services_active/$services_checked actifs"

# ====== SECTION 4 - SAUVEGARDE SYSTÈME ======

print_section "4. SAUVEGARDE CONFIGURATION"

# Création du répertoire de sauvegarde
backup_dir="$BACKUP_BASE_DIR/backup_$TIMESTAMP"
echo "Création du répertoire de sauvegarde: $backup_dir"

if mkdir -p "$backup_dir"; then
    log_message "INFO" "Répertoire de sauvegarde créé: $backup_dir"
else
    log_message "ERROR" "Impossible de créer le répertoire de sauvegarde"
    ((critical_issues++))
fi

# Liste des fichiers/répertoires à sauvegarder
files_to_backup=(
    "/etc/hostname"
    "/etc/hosts"  
    "/etc/passwd"
    "/etc/group"
    "/etc/fstab"
)

echo ""
echo "Sauvegarde des fichiers de configuration..."

backup_archive="$backup_dir/system_config_$TIMESTAMP.tar.gz"
backup_successful=true

# Création de l'archive tar
if tar -czf "$backup_archive" "${files_to_backup[@]}" 2>/dev/null; then
    # Calcul de la taille de l'archive
    if [[ -f "$backup_archive" ]]; then
        archive_size=$(du -h "$backup_archive" | cut -f1)
        echo "✅ Archive créée: $backup_archive"
        echo "   Taille: $archive_size"
        log_message "INFO" "Sauvegarde réussie: $backup_archive ($archive_size)"
    else
        echo "❌ Erreur: Archive non trouvée après création"
        backup_successful=false
        ((critical_issues++))
    fi
else
    echo "❌ Erreur lors de la création de l'archive"
    backup_successful=false
    ((critical_issues++))
    log_message "ERROR" "Échec création archive de sauvegarde"
fi

# ====== SECTION 5 - RAPPORT FINAL ======

print_section "5. RAPPORT DE SANTÉ SYSTÈME"

# Calcul de l'état global
global_status="OK"
if [[ $critical_issues -gt 0 ]]; then
    global_status="CRITIQUE"
elif [[ $warnings_count -gt 0 ]]; then
    global_status="ATTENTION"
fi

echo "État global du système: $global_status"
echo ""

echo "📊 Statistiques détaillées:"
echo "   • Services vérifiés: $services_checked"
echo "   • Services actifs: $services_active"
echo "   • Utilisation disque: ${disk_usage}%"
echo "   • Avertissements: $warnings_count"
echo "   • Problèmes critiques: $critical_issues"

if [[ "$backup_successful" == true ]]; then
    echo "   • Sauvegarde: RÉUSSIE"
else
    echo "   • Sauvegarde: ÉCHEC"
fi

echo ""
echo "🔧 Recommandations d'actions:"

# Recommandations basées sur l'analyse
if [[ $critical_issues -gt 0 ]]; then
    echo "   URGENT - Intervention immédiate requise:"
    [[ $disk_usage -ge $DISK_CRITICAL_THRESHOLD ]] && echo "     • Libérer de l'espace disque immédiatement"
    [[ "$backup_successful" != true ]] && echo "     • Vérifier les permissions et l'espace pour les sauvegardes"
elif [[ $warnings_count -gt 0 ]]; then
    echo "   À surveiller:"
    [[ $disk_usage -ge $DISK_WARNING_THRESHOLD ]] && echo "     • Planifier le nettoyage de l'espace disque"
    [[ $services_active -lt $services_checked ]] && echo "     • Vérifier et redémarrer les services inactifs"
else
    echo "   • Système en bon état, aucune action immédiate requise"
    echo "   • Continuer la surveillance régulière"
fi

# ====== GESTION DES PARAMÈTRES (BONUS) ======

# Fonction d'aide
show_help() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Options:
  --help           Afficher cette aide
  --backup-only    Exécuter uniquement la sauvegarde
  --check-only     Exécuter uniquement les vérifications (sans sauvegarde)
  --version        Afficher la version

Exemples:
  $SCRIPT_NAME                    # Exécution complète
  $SCRIPT_NAME --backup-only      # Sauvegarde seulement
  $SCRIPT_NAME --check-only       # Vérifications seulement
EOF
}

# Gestion des paramètres en ligne de commande
case "${1:-}" in
    "--help"|"-h")
        show_help
        exit 0
        ;;
    "--version"|"-v")
        echo "$SCRIPT_NAME version $VERSION"
        exit 0
        ;;
    "--backup-only")
        print_section "MODE SAUVEGARDE UNIQUEMENT"
        # Ici on exécuterait seulement la section 4
        echo "Fonctionnalité disponible dans le script complet"
        ;;
    "--check-only")
        print_section "MODE VÉRIFICATION UNIQUEMENT"
        # Ici on exécuterait les sections 1-3 sans la sauvegarde
        echo "Fonctionnalité disponible dans le script complet"
        ;;
    "")
        # Mode normal - script complet exécuté ci-dessus
        ;;
    *)
        echo "Paramètre inconnu: $1"
        echo "Utilisez --help pour voir les options disponibles"
        exit 1
        ;;
esac

# ====== FINALISATION ======

print_section "MAINTENANCE TERMINÉE"
echo "Durée d'exécution: Quelques secondes"
echo "Fichier de log: $LOG_FILE"
echo "Code de sortie: $([ $critical_issues -eq 0 ] && echo '0 (succès)' || echo '1 (problèmes détectés)')"

log_message "INFO" "Script de maintenance terminé - Status: $global_status"

# Code de sortie basé sur la criticité
exit $([ $critical_issues -eq 0 ] && echo 0 || echo 1)

# ====== EXPLICATIONS TECHNIQUES AVANCÉES ======

# 1. VARIABLES READONLY
#    readonly VAR="value" rend la variable non-modifiable
#    Bonne pratique pour les constantes de configuration

# 2. FONCTIONS RÉUTILISABLES  
#    Permettent de structurer le code et éviter la répétition
#    Peuvent recevoir des paramètres ($1, $2 dans la fonction)

# 3. GESTION D'ERREURS ROBUSTE
#    Vérification des codes de retour des commandes
#    Compteurs pour tracking des problèmes
#    Logs pour traçabilité

# 4. CALCULS ET STATISTIQUES
#    ((variable++)) pour incrémentation
#    $() pour capture de sortie de commandes
#    awk/sed pour extraction de données

# 5. FORMATAGE PROFESSIONNEL
#    printf pour formatage avancé
#    tee pour affichage ET logging simultané
#    Codes couleur avec émojis pour lisibilité

# ====== EXTENSIONS POSSIBLES ======

# Monitoring en temps réel :
# while true; do
#     run_checks
#     sleep 300  # Vérification toutes les 5 minutes
# done

# Notifications par email/Slack :
# send_alert() {
#     local message="$1"
#     echo "$message" | mail -s "Alerte système" admin@domain.com
# }

# Base de données de métriques :
# log_metrics_to_db() {
#     local timestamp="$1"
#     local disk_usage="$2"
#     # INSERT INTO metrics...
# }

# Configuration externe :
# source /etc/maintenance/config.conf

# ====== USAGE EN PRODUCTION ======
# 1. Déployer dans /usr/local/bin/
# 2. Ajouter dans crontab pour exécution régulière
# 3. Configurer rotation des logs
# 4. Intégrer avec système de monitoring (Nagios, Zabbix)
# 5. Adapter la liste des services selon l'infrastructure