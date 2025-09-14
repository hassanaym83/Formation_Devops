#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 2: Planification de tâches avec systemd timers - CORRECTION
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
install_timer_system() {
    info "=== CORRECTION LAB 2: Systemd Timers ==="
    
    # Étape 1: Créer la structure de répertoires
    info "Création de la structure de répertoires..."
    mkdir -p /opt/nettoyage
    
    # Étape 2: Créer le script de nettoyage
    info "Création du script de nettoyage..."
    cat > /opt/nettoyage/nettoyage.sh << 'EOF'
#!/bin/bash
set -euo pipefail

LOG_FILE="/var/log/nettoyage.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Fonction de logging
log_message() {
    echo "$DATE - $1" >> "$LOG_FILE"
}

# Créer le fichier de log s'il n'existe pas
touch "$LOG_FILE"

log_message "=== DÉBUT DU NETTOYAGE ==="

# Compteurs pour les statistiques
FICHIERS_TEMP_SUPPRIMES=0
FICHIERS_LOG_SUPPRIMES=0
ERREURS=0

# Nettoyage des fichiers temporaires
log_message "Nettoyage des fichiers .tmp plus anciens que 7 jours..."
if TEMP_FILES=$(find /tmp -name "*.tmp" -mtime +7 -type f 2>/dev/null); then
    if [ -n "$TEMP_FILES" ]; then
        echo "$TEMP_FILES" | while read -r file; do
            if rm "$file" 2>/dev/null; then
                ((FICHIERS_TEMP_SUPPRIMES++))
            else
                ((ERREURS++))
            fi
        done
        log_message "Fichiers .tmp supprimés: $FICHIERS_TEMP_SUPPRIMES"
    else
        log_message "Aucun fichier .tmp ancien trouvé"
    fi
else
    log_message "Erreur lors de la recherche de fichiers .tmp"
    ((ERREURS++))
fi

# Nettoyage des anciens logs
log_message "Nettoyage des logs plus anciens que 30 jours..."
if LOG_FILES=$(find /var/log -name "*.log.old" -mtime +30 -type f 2>/dev/null); then
    if [ -n "$LOG_FILES" ]; then
        echo "$LOG_FILES" | while read -r file; do
            if rm "$file" 2>/dev/null; then
                ((FICHIERS_LOG_SUPPRIMES++))
            else
                ((ERREURS++))
            fi
        done
        log_message "Anciens logs supprimés: $FICHIERS_LOG_SUPPRIMES"
    else
        log_message "Aucun ancien log trouvé"
    fi
else
    log_message "Erreur lors de la recherche d'anciens logs"
    ((ERREURS++))
fi

# Nettoyage des caches système (ajout bonus)
log_message "Nettoyage des caches système..."
CACHE_SIZE_BEFORE=0
CACHE_SIZE_AFTER=0

if [ -d /var/cache/apt/archives/ ]; then
    CACHE_SIZE_BEFORE=$(du -sm /var/cache/apt/archives/ | cut -f1)
    apt-get clean >/dev/null 2>&1 || true
    CACHE_SIZE_AFTER=$(du -sm /var/cache/apt/archives/ | cut -f1)
    CACHE_FREED=$((CACHE_SIZE_BEFORE - CACHE_SIZE_AFTER))
    log_message "Cache APT nettoyé: ${CACHE_FREED}MB libérés"
fi

# Résumé du nettoyage
log_message "=== RÉSUMÉ ==="
log_message "Fichiers temporaires supprimés: $FICHIERS_TEMP_SUPPRIMES"
log_message "Anciens logs supprimés: $FICHIERS_LOG_SUPPRIMES"
log_message "Erreurs rencontrées: $ERREURS"
log_message "=== FIN DU NETTOYAGE ==="

# Code de sortie basé sur les erreurs
if [ $ERREURS -eq 0 ]; then
    exit 0
else
    exit 1
fi
EOF
    
    # Rendre le script exécutable
    chmod +x /opt/nettoyage/nettoyage.sh
    success "Script de nettoyage créé: /opt/nettoyage/nettoyage.sh"
    
    # Étape 3: Installer bc pour les calculs (nécessaire pour certains tests)
    info "Installation des dépendances..."
    apt update >/dev/null 2>&1
    apt install -y bc >/dev/null 2>&1
    
    # Étape 4: Tester le script manuellement
    info "Test du script de nettoyage..."
    /opt/nettoyage/nettoyage.sh
    
    if [ -f /var/log/nettoyage.log ]; then
        success "Script testé avec succès"
        info "Dernières lignes du log:"
        tail -3 /var/log/nettoyage.log
    else
        error "Problème avec l'exécution du script"
        return 1
    fi
    
    # Étape 5: Créer le service systemd
    info "Création du service systemd..."
    cat > /etc/systemd/system/nettoyage.service << 'EOF'
[Unit]
Description=Nettoyage automatique des fichiers temporaires
Documentation=file:///opt/nettoyage/README.txt
After=network.target

[Service]
Type=oneshot
ExecStart=/opt/nettoyage/nettoyage.sh
User=root
Group=root

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nettoyage

# Sécurité
NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=/var/log /tmp /var/cache

# Timeout
TimeoutStartSec=300
EOF
    
    success "Service systemd créé: /etc/systemd/system/nettoyage.service"
    
    # Étape 6: Créer le timer systemd
    info "Création du timer systemd..."
    cat > /etc/systemd/system/nettoyage.timer << 'EOF'
[Unit]
Description=Timer pour nettoyage quotidien
Documentation=file:///opt/nettoyage/README.txt
Requires=nettoyage.service

[Timer]
# Exécution quotidienne à minuit
OnCalendar=daily
# Persistance pour rattraper les exécutions manquées
Persistent=true
# Randomisation pour éviter les pics de charge
RandomizedDelaySec=300
# Précision
AccuracySec=1min

[Install]
WantedBy=timers.target
EOF
    
    success "Timer systemd créé: /etc/systemd/system/nettoyage.timer"
    
    # Étape 7: Recharger systemd et activer
    info "Activation du timer..."
    systemctl daemon-reload
    systemctl enable nettoyage.timer
    systemctl start nettoyage.timer
    
    success "Timer activé et démarré"
}

# Tests et validation
run_tests() {
    info "=== TESTS ET VALIDATION ==="
    
    # Test 1: Vérifier que le timer est actif
    info "Test 1: Vérification du statut du timer"
    if systemctl is-active --quiet nettoyage.timer; then
        success "Le timer est actif"
        systemctl status nettoyage.timer --no-pager -l
    else
        error "Le timer n'est pas actif"
        return 1
    fi
    
    # Test 2: Vérifier que le timer est activé
    info "Test 2: Vérification de l'activation"
    if systemctl is-enabled --quiet nettoyage.timer; then
        success "Le timer est activé"
    else
        warning "Le timer n'est pas activé"
    fi
    
    # Test 3: Vérifier les prochaines exécutions
    info "Test 3: Vérification des prochaines exécutions"
    if systemctl list-timers nettoyage.timer --no-pager | grep -q nettoyage; then
        success "Timer visible dans la liste des timers"
        info "Prochaines exécutions:"
        systemctl list-timers nettoyage.timer --no-pager
    else
        error "Timer non trouvé dans la liste"
        return 1
    fi
    
    # Test 4: Exécution manuelle du service
    info "Test 4: Exécution manuelle du service"
    systemctl start nettoyage.service
    sleep 2
    
    # Vérifier les logs
    if journalctl -u nettoyage.service --since "2 minutes ago" --no-pager | grep -q "nettoyage"; then
        success "Service exécuté manuellement avec succès"
    else
        warning "Pas de logs récents trouvés pour le service"
    fi
    
    # Test 5: Vérifier le fichier de log
    info "Test 5: Vérification des logs de nettoyage"
    if [ -f /var/log/nettoyage.log ]; then
        LOG_LINES=$(wc -l < /var/log/nettoyage.log)
        success "Fichier de log créé avec $LOG_LINES lignes"
        info "Dernières entrées:"
        tail -5 /var/log/nettoyage.log
    else
        error "Fichier de log non trouvé"
    fi
    
    # Test 6: Créer des fichiers de test et tester le nettoyage
    info "Test 6: Test fonctionnel avec fichiers temporaires"
    
    # Créer des fichiers de test anciens
    touch /tmp/test1.tmp /tmp/test2.tmp
    # Simuler des fichiers anciens (modifier la date)
    find /tmp -name "test*.tmp" -exec touch -d "8 days ago" {} \;
    
    # Exécuter le nettoyage
    /opt/nettoyage/nettoyage.sh
    
    # Vérifier que les fichiers ont été supprimés
    if [ ! -f /tmp/test1.tmp ] && [ ! -f /tmp/test2.tmp ]; then
        success "Nettoyage fonctionnel: fichiers test supprimés"
    else
        warning "Fichiers test non supprimés (vérifiez les permissions)"
    fi
}

# Démonstration des différentes planifications
show_scheduling_examples() {
    info "=== EXEMPLES DE PLANIFICATION ==="
    
    cat << 'EOF'
Exemples de OnCalendar pour différents besoins:

1. Fréquences de base:
   OnCalendar=minutely          # Toutes les minutes
   OnCalendar=hourly            # Toutes les heures
   OnCalendar=daily             # Quotidien à minuit
   OnCalendar=weekly            # Hebdomadaire (lundi)
   OnCalendar=monthly           # Mensuel (1er du mois)

2. Horaires spécifiques:
   OnCalendar=*-*-* 02:00:00    # Tous les jours à 2h
   OnCalendar=Mon *-*-* 09:00:00 # Tous les lundis à 9h
   OnCalendar=*-*-01 06:00:00   # Le 1er de chaque mois à 6h

3. Intervalles:
   OnCalendar=*:0/15            # Toutes les 15 minutes
   OnCalendar=*-*-* *:30:00     # Toutes les heures à 30min
   OnCalendar=*:0/10            # Toutes les 10 minutes

4. Planifications complexes:
   OnCalendar=Mon..Fri 08:00:00 # Lundi à vendredi à 8h
   OnCalendar=Sat,Sun 10:00:00  # Week-end à 10h
   OnCalendar=*-01,07 01:00:00  # Janvier et juillet à 1h

Options utiles du timer:
- Persistent=true              # Rattraper les exécutions manquées
- RandomizedDelaySec=300       # Randomiser l'exécution (±5min)
- AccuracySec=1s              # Précision de déclenchement
EOF
}

# Affichage des informations utiles
show_info() {
    info "=== INFORMATIONS UTILES ==="
    
    echo "Gestion du timer:"
    echo "  systemctl status nettoyage.timer     # Voir le statut du timer"
    echo "  systemctl start nettoyage.timer      # Démarrer le timer"
    echo "  systemctl stop nettoyage.timer       # Arrêter le timer"
    echo "  systemctl enable nettoyage.timer     # Activer au boot"
    echo "  systemctl disable nettoyage.timer    # Désactiver au boot"
    echo
    echo "Gestion du service:"
    echo "  systemctl start nettoyage.service    # Exécution manuelle"
    echo "  systemctl status nettoyage.service   # Statut du service"
    echo
    echo "Surveillance:"
    echo "  systemctl list-timers                # Voir tous les timers"
    echo "  systemctl list-timers nettoyage*     # Voir ce timer"
    echo "  journalctl -u nettoyage.service -f   # Logs systemd en temps réel"
    echo "  tail -f /var/log/nettoyage.log       # Logs du script"
    echo
    echo "Fichiers créés:"
    echo "  /opt/nettoyage/nettoyage.sh           # Script de nettoyage"
    echo "  /etc/systemd/system/nettoyage.service # Définition du service"
    echo "  /etc/systemd/system/nettoyage.timer   # Définition du timer"
    echo "  /var/log/nettoyage.log                # Logs du nettoyage"
    echo
    echo "Tests manuels:"
    echo "  /opt/nettoyage/nettoyage.sh           # Exécuter directement"
    echo "  systemctl start nettoyage.service    # Exécuter via systemd"
}

# Génération de documentation
create_documentation() {
    info "Génération de la documentation..."
    
    cat > /opt/nettoyage/README.txt << 'EOF'
# Système de Nettoyage Automatique

## Description
Timer systemd qui exécute quotidiennement un script de nettoyage des fichiers temporaires et anciens logs.

## Composants
- Script: /opt/nettoyage/nettoyage.sh
- Service: /etc/systemd/system/nettoyage.service  
- Timer: /etc/systemd/system/nettoyage.timer
- Logs: /var/log/nettoyage.log

## Fonctionnalités
- Suppression des fichiers .tmp > 7 jours
- Suppression des logs .old > 30 jours  
- Nettoyage du cache APT
- Logs détaillés avec statistiques
- Exécution quotidienne à minuit
- Rattrapage des exécutions manquées

## Gestion
```bash
# Timer
systemctl start/stop/status nettoyage.timer
systemctl enable/disable nettoyage.timer

# Service (exécution manuelle)
systemctl start nettoyage.service

# Surveillance
systemctl list-timers nettoyage*
journalctl -u nettoyage.service
tail -f /var/log/nettoyage.log
```

## Personnalisation
Modifier /opt/nettoyage/nettoyage.sh pour:
- Changer les critères de suppression
- Ajouter d'autres types de fichiers
- Modifier les logs

Modifier /etc/systemd/system/nettoyage.timer pour:
- Changer la fréquence (OnCalendar=)
- Ajouter la randomisation (RandomizedDelaySec=)
- Modifier la persistance

Après modification: systemctl daemon-reload

## Sécurité
- Exécution en tant que root (nécessaire pour /var/log)
- Isolation: PrivateTmp=true, NoNewPrivileges=true
- Chemins limités: ReadWritePaths spécifiés
- Timeout de sécurité: 5 minutes maximum
EOF
    
    success "Documentation créée: /opt/nettoyage/README.txt"
}

# Nettoyage (fonction optionnelle)
cleanup_timer_system() {
    info "=== NETTOYAGE DU SYSTÈME DE TIMERS ==="
    
    # Arrêter et désactiver le timer
    systemctl stop nettoyage.timer 2>/dev/null || true
    systemctl disable nettoyage.timer 2>/dev/null || true
    
    # Supprimer les fichiers
    rm -f /etc/systemd/system/nettoyage.timer
    rm -f /etc/systemd/system/nettoyage.service
    rm -rf /opt/nettoyage
    rm -f /var/log/nettoyage.log
    
    # Recharger systemd
    systemctl daemon-reload
    systemctl reset-failed
    
    success "Système de nettoyage supprimé complètement"
}

# Fonction principale
main() {
    case "${1:-install}" in
        "install")
            check_privileges
            install_timer_system
            run_tests
            create_documentation
            show_scheduling_examples
            show_info
            success "Installation terminée avec succès!"
            ;;
        "test")
            check_privileges
            run_tests
            ;;
        "cleanup")
            check_privileges
            cleanup_timer_system
            ;;
        "info")
            show_info
            ;;
        "examples")
            show_scheduling_examples
            ;;
        *)
            echo "Usage: $0 [install|test|cleanup|info|examples]"
            echo "  install  : Installer et configurer le système (défaut)"
            echo "  test     : Exécuter les tests seulement"
            echo "  cleanup  : Supprimer complètement le système"
            echo "  info     : Afficher les informations d'utilisation"
            echo "  examples : Afficher les exemples de planification"
            exit 1
            ;;
    esac
}

# Gestion des signaux
trap 'error "Script interrompu par l'\''utilisateur"; exit 1' SIGINT SIGTERM

# Exécution du script principal
main "$@"
