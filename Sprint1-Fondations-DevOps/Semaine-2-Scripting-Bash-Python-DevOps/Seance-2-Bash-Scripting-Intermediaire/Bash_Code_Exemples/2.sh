#!/bin/bash

# Fonction d'information système
obtenir_info_systeme() {
    echo "=== Informations Système ==="
    echo "Hostname: $(hostname)"
    echo "Uptime: $(uptime -p)"
    echo "Charge: $(uptime | awk -F'load average:' '{print $2}')"
}

# Fonction de vérification des services
verifier_services() {
    local services=("sshd" "nginx" "mysql")
    echo "=== Vérification Services ==="

    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service"; then
            echo "Service $service: ACTIF"
        else
            echo "Service $service: INACTIF"
        fi
    done
}

# Fonction de maintenance
effectuer_maintenance() {
    echo "=== Maintenance Système ==="
    echo "Nettoyage des logs anciens..."
    find /var/log -name "*.log" -mtime +30 -type f
    echo "Vérification de l'espace disque..."
    df -h | grep -E '^/dev/'
}

# Fonction principale - orchestration
main() {
    echo "Début du script de monitoring - $(date)"
    echo "======================================="

    obtenir_info_systeme
    echo
    verifier_services
    echo
    effectuer_maintenance

    echo "======================================="
    echo "Fin du script - $(date)"
}

# Exécution du script principal
main "$@"

