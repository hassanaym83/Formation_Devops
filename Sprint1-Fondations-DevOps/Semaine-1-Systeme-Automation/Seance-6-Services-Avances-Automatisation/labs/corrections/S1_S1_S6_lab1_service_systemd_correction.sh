#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 1: Création et gestion de services systemd - CORRECTION
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
install_service() {
    info "=== CORRECTION LAB 1: Service systemd ==="
    
    # Étape 1: Créer la structure de répertoires
    info "Création de la structure de répertoires..."
    mkdir -p /opt/monservice
    
    # Étape 2: Créer le script de service
    info "Création du script de service..."
    cat > /opt/monservice/service.sh << 'EOF'
#!/bin/bash
LOG_FILE="/var/log/monservice.log"

# Fonction pour gérer l'arrêt propre
cleanup() {
    echo "$(date): Service arrêté proprement" >> $LOG_FILE
    exit 0
}

# Capturer le signal SIGTERM pour arrêt propre
trap cleanup SIGTERM SIGINT

# Créer le fichier de log s'il n'existe pas
touch $LOG_FILE

echo "$(date): Service démarré" >> $LOG_FILE

# Boucle principale du service
while true; do
    echo "$(date): Service en fonctionnement - PID: $$" >> $LOG_FILE
    
    # Ajouter quelques informations système
    LOAD=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)
    echo "$(date): Load average: $LOAD" >> $LOG_FILE
    
    sleep 10
done
EOF
    
    # Rendre le script exécutable
    chmod +x /opt/monservice/service.sh
    success "Script de service créé: /opt/monservice/service.sh"
    
    # Étape 3: Créer le fichier service systemd
    info "Création du fichier service systemd..."
    cat > /etc/systemd/system/monservice.service << 'EOF'
[Unit]
Description=Mon Premier Service - Service de démonstration
Documentation=file:///opt/monservice/README.txt
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/opt/monservice/service.sh
ExecStop=/bin/kill -TERM $MAINPID
Restart=always
RestartSec=5
StartLimitBurst=3
StartLimitIntervalSec=300
User=root
Group=root

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=monservice

# Sécurité basique
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
    
    success "Fichier service créé: /etc/systemd/system/monservice.service"
    
    # Étape 4: Recharger systemd
    info "Rechargement de systemd..."
    systemctl daemon-reload
    
    # Étape 5: Démarrer et activer le service
    info "Démarrage du service..."
    systemctl start monservice
    sleep 2
    
    # Vérification du statut
    if systemctl is-active --quiet monservice; then
        success "Service démarré avec succès"
    else
        error "Échec du démarrage du service"
        systemctl status monservice
        return 1
    fi
    
    # Activer le service au démarrage
    info "Activation du service au démarrage..."
    systemctl enable monservice
    
    success "Service activé pour le démarrage automatique"
}

# Tests et validation
run_tests() {
    info "=== TESTS ET VALIDATION ==="
    
    # Test 1: Vérifier que le service est actif
    info "Test 1: Vérification du statut du service"
    if systemctl is-active --quiet monservice; then
        success "Le service est actif"
        systemctl status monservice --no-pager -l
    else
        error "Le service n'est pas actif"
        return 1
    fi
    
    # Test 2: Vérifier que le service est activé
    info "Test 2: Vérification de l'activation au démarrage"
    if systemctl is-enabled --quiet monservice; then
        success "Le service est activé pour le démarrage automatique"
    else
        warning "Le service n'est pas activé pour le démarrage automatique"
    fi
    
    # Test 3: Vérifier les logs
    info "Test 3: Vérification des logs"
    sleep 15
    if [ -f /var/log/monservice.log ]; then
        LOG_LINES=$(wc -l < /var/log/monservice.log)
        if [ $LOG_LINES -gt 0 ]; then
            success "Logs générés correctement ($LOG_LINES lignes)"
            info "Dernières lignes du log:"
            tail -5 /var/log/monservice.log
        else
            error "Fichier de log vide"
        fi
    else
        error "Fichier de log non trouvé"
    fi
    
    # Test 4: Test de redémarrage
    info "Test 4: Test de redémarrage du service"
    systemctl restart monservice
    sleep 3
    if systemctl is-active --quiet monservice; then
        success "Redémarrage réussi"
    else
        error "Échec du redémarrage"
        return 1
    fi
    
    # Test 5: Test de résilience (kill du processus)
    info "Test 5: Test de résilience (simulation de crash)"
    PID=$(systemctl show --property MainPID --value monservice)
    if [ "$PID" != "0" ]; then
        kill -KILL $PID
        info "Processus tué, attente de la récupération..."
        sleep 8
        if systemctl is-active --quiet monservice; then
            success "Service récupéré automatiquement après crash"
        else
            error "Service non récupéré après crash"
        fi
    else
        warning "Impossible de récupérer le PID du service"
    fi
}

# Affichage des informations utiles
show_info() {
    info "=== INFORMATIONS UTILES ==="
    
    echo "Commandes de gestion du service:"
    echo "  systemctl status monservice      # Voir le statut"
    echo "  systemctl start monservice       # Démarrer"
    echo "  systemctl stop monservice        # Arrêter"
    echo "  systemctl restart monservice     # Redémarrer"
    echo "  systemctl enable monservice      # Activer au boot"
    echo "  systemctl disable monservice     # Désactiver au boot"
    echo
    echo "Consultation des logs:"
    echo "  tail -f /var/log/monservice.log        # Logs de l'application"
    echo "  journalctl -u monservice -f            # Logs systemd"
    echo "  journalctl -u monservice --since today # Logs du jour"
    echo
    echo "Fichiers créés:"
    echo "  /opt/monservice/service.sh              # Script principal"
    echo "  /etc/systemd/system/monservice.service # Définition du service"
    echo "  /var/log/monservice.log                 # Fichier de logs"
    echo
    echo "Tests supplémentaires:"
    echo "  systemctl is-active monservice         # Vérifie si actif"
    echo "  systemctl is-enabled monservice        # Vérifie si activé"
    echo "  systemctl list-dependencies monservice # Voir les dépendances"
}

# Génération de documentation
create_documentation() {
    info "Génération de la documentation..."
    
    cat > /opt/monservice/README.txt << 'EOF'
# Mon Premier Service systemd

## Description
Service de démonstration qui écrit périodiquement dans un fichier de log.

## Fichiers
- /opt/monservice/service.sh : Script principal
- /etc/systemd/system/monservice.service : Définition systemd
- /var/log/monservice.log : Fichier de logs

## Gestion
```bash
# Démarrer le service
systemctl start monservice

# Arrêter le service
systemctl stop monservice

# Redémarrer le service
systemctl restart monservice

# Voir le statut
systemctl status monservice

# Activer au démarrage
systemctl enable monservice

# Voir les logs
tail -f /var/log/monservice.log
journalctl -u monservice -f
```

## Caractéristiques
- Redémarrage automatique en cas de panne
- Arrêt propre avec gestion des signaux
- Logging détaillé
- Sécurité de base (NoNewPrivileges, PrivateTmp)
- Limitation des tentatives de redémarrage

## Dépannage
En cas de problème:
1. Vérifier les logs: journalctl -u monservice
2. Vérifier le statut: systemctl status monservice
3. Tester le script manuellement: /opt/monservice/service.sh
4. Recharger systemd: systemctl daemon-reload
EOF
    
    success "Documentation créée: /opt/monservice/README.txt"
}

# Nettoyage (fonction optionnelle)
cleanup_service() {
    info "=== NETTOYAGE DU SERVICE ==="
    
    # Arrêter et désactiver le service
    systemctl stop monservice 2>/dev/null || true
    systemctl disable monservice 2>/dev/null || true
    
    # Supprimer les fichiers
    rm -f /etc/systemd/system/monservice.service
    rm -rf /opt/monservice
    rm -f /var/log/monservice.log
    
    # Recharger systemd
    systemctl daemon-reload
    systemctl reset-failed
    
    success "Service nettoyé complètement"
}

# Fonction principale
main() {
    case "${1:-install}" in
        "install")
            check_privileges
            install_service
            run_tests
            create_documentation
            show_info
            success "Installation terminée avec succès!"
            ;;
        "test")
            check_privileges
            run_tests
            ;;
        "cleanup")
            check_privileges
            cleanup_service
            ;;
        "info")
            show_info
            ;;
        *)
            echo "Usage: $0 [install|test|cleanup|info]"
            echo "  install  : Installer et configurer le service (défaut)"
            echo "  test     : Exécuter les tests seulement"
            echo "  cleanup  : Supprimer complètement le service"
            echo "  info     : Afficher les informations d'utilisation"
            exit 1
            ;;
    esac
}

# Gestion des signaux
trap 'error "Script interrompu par l'\''utilisateur"; exit 1' SIGINT SIGTERM

# Exécution du script principal
main "$@"
