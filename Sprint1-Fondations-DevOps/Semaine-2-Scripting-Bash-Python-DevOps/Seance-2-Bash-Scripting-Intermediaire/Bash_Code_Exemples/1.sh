#!/bin/bash

# Fonction simple d'information
afficher_info_systeme() {
 echo "=== Informations Système ==="
 echo "Date: $(date)"
 echo "Utilisateur: $(whoami)"
 echo "Système: $(uname -s)"
}

# Fonction avec paramètres
verifier_service() {
 local service_name="$1"

 if systemctl is-active "$service_name" >/dev/null 2>&1; then
 echo " Service $service_name est actif"
 return 0
 else
 echo " Service $service_name est inactif"
 return 1
 fi
}