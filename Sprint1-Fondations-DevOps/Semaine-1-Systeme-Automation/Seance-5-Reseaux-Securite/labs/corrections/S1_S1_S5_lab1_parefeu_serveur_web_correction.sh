#!/bin/bash

# LAB 1 - Configuration pare-feu pour serveur web - CORRECTION
#
# Cette correction présente une solution complète et optimisée pour
# la sécurisation d'un serveur web DevOps avec UFW
#
# Concepts démontrés :
# - Configuration UFW sécurisée et méthodique
# - Gestion des politiques par défaut appropriées
# - Autorisation granulaire des services critiques
# - Sécurisation SSH par restriction réseau
#
# Bonnes pratiques appliquées :
# - Autorisation SSH AVANT activation (évite coupure accès)
# - Principe de moindre privilège (deny par défaut)
# - Restriction SSH au réseau de management
# - Vérifications systématiques de configuration

echo "=== CORRECTION LAB 1 - CONFIGURATION PARE-FEU SERVEUR WEB ==="
echo ""

# Fonction de logging avec timestamp
log_step() {
    echo "[$(date '+%H:%M:%S')] $1"
}

# Fonction de vérification des erreurs
check_error() {
    if [ $? -ne 0 ]; then
        echo "ERREUR: $1"
        exit 1
    fi
}

log_step "Début de la configuration du pare-feu pour serveur web DevOps"

# ÉTAPE 1: Vérification de l'état initial
log_step "ÉTAPE 1: Vérification de l'état actuel d'UFW"
echo "État initial du pare-feu:"
sudo ufw status
echo ""

# ÉTAPE 2: Sauvegarde et autorisation SSH critique
log_step "ÉTAPE 2: Sécurisation SSH (ÉTAPE CRITIQUE)"
echo "Autorisation SSH pour éviter la coupure d'accès..."
sudo ufw allow ssh
check_error "Échec autorisation SSH"
echo "SSH autorisé avec succès"
echo ""

# ÉTAPE 3: Configuration des politiques par défaut sécurisées
log_step "ÉTAPE 3: Configuration des politiques par défaut"
echo "Application du principe de sécurité: deny by default"
sudo ufw default deny incoming
check_error "Échec configuration politique entrante"

sudo ufw default allow outgoing  
check_error "Échec configuration politique sortante"

echo "Politiques par défaut configurées:"
echo "- DENY incoming (sécurité)"
echo "- ALLOW outgoing (fonctionnalité)"
echo ""

# ÉTAPE 4: Autorisation des services web essentiels
log_step "ÉTAPE 4: Configuration des services web"
echo "Autorisation HTTP (port 80)..."
sudo ufw allow 80/tcp
check_error "Échec autorisation HTTP"

echo "Autorisation HTTPS (port 443)..."
sudo ufw allow 443/tcp
check_error "Échec autorisation HTTPS"

echo "Services web autorisés avec succès"
echo ""

# ÉTAPE 5: Sécurisation SSH avancée sur port non-standard
log_step "ÉTAPE 5: Configuration SSH sécurisé sur port 2222"
echo "Configuration SSH sur port non-standard pour sécurité renforcée..."

# Supprimer l'autorisation SSH générale (port 22)
sudo ufw delete allow ssh
check_error "Échec suppression règle SSH générale"

# Autoriser SSH sur port 2222 avec restriction réseau
sudo ufw allow from 192.168.10.0/24 to any port 2222 comment 'SSH Admin'
check_error "Échec autorisation SSH port 2222"

# Alternative sans restriction réseau si nécessaire
# sudo ufw allow 2222/tcp comment 'SSH Admin'

echo "SSH configuré sur port 2222 avec restriction réseau 192.168.10.0/24"
echo ""

# ÉTAPE 6: Activation du pare-feu
log_step "ÉTAPE 6: Activation d'UFW"
echo "Activation du pare-feu..."
echo "y" | sudo ufw enable
check_error "Échec activation UFW"
echo "Pare-feu activé avec succès"
echo ""

# ÉTAPE 7: Vérification complète de la configuration
log_step "ÉTAPE 7: Vérification de la configuration finale"
echo ""
echo "=== CONFIGURATION FINALE DU PARE-FEU ==="
sudo ufw status numbered
echo ""

echo "=== CONFIGURATION DÉTAILLÉE ==="
sudo ufw status verbose
echo ""

# ÉTAPE 8: Tests de validation
log_step "ÉTAPE 8: Validation de la configuration"
echo ""
echo "=== TESTS DE VALIDATION ==="

# Test 1: Vérification des ports en écoute
echo "Ports en écoute sur le système:"
sudo ss -tuln | grep -E ':(2222|80|443) '
echo ""

# Test 2: Vérification des règles UFW actives
echo "Nombre de règles UFW actives:"
sudo ufw status | grep -v "Status:" | grep -v "^$" | grep -v "To" | wc -l
echo ""

# ÉTAPE 9: Documentation de la configuration
log_step "ÉTAPE 9: Documentation de la configuration"
echo ""
echo "=== RÉSUMÉ DE LA CONFIGURATION ==="
echo "1. POLITIQUE PAR DÉFAUT:"
echo "   - Trafic entrant: DENY (sécurité maximale)"
echo "   - Trafic sortant: ALLOW (fonctionnalité préservée)"
echo ""
echo "2. SERVICES AUTORISÉS:"
echo "   - SSH (2222/tcp): Port non-standard, restreint au réseau 192.168.10.0/24"
echo "   - HTTP (80/tcp): Ouvert (service web)"
echo "   - HTTPS (443/tcp): Ouvert (service web sécurisé)"
echo ""
echo "3. SÉCURITÉ APPLIQUÉE:"
echo "   - Principe de moindre privilège respecté"
echo "   - SSH sécurisé par port non-standard (2222) et restriction réseau"
echo "   - Obfuscation des services d'administration"
echo "   - Services web accessibles pour production"
echo ""

# ÉTAPE 10: Procédures de maintenance
log_step "ÉTAPE 10: Procédures de maintenance et dépannage"
echo ""
echo "=== COMMANDES DE MAINTENANCE ==="
echo ""
echo "# Voir la configuration actuelle:"
echo "sudo ufw status numbered"
echo ""
echo "# Ajouter une nouvelle règle:"
echo "sudo ufw allow from [IP] to any port [PORT]"
echo ""
echo "# Supprimer une règle par numéro:"
echo "sudo ufw delete [NUMÉRO]"
echo ""
echo "# Désactiver temporairement UFW:"
echo "sudo ufw disable"
echo ""
echo "# Réactiver UFW:"
echo "sudo ufw enable"
echo ""

echo "=== PROCÉDURES D'URGENCE ==="
echo ""
echo "# En cas de coupure SSH accidentelle:"
echo "# 1. Accès physique à la machine"
echo "# 2. sudo ufw disable"
echo "# 3. Reconfigurer les règles SSH"
echo "# 4. sudo ufw enable"
echo ""

echo "=== MONITORING DE LA CONFIGURATION ==="
echo ""
echo "# Surveiller les tentatives bloquées:"
echo "sudo tail -f /var/log/ufw.log"
echo ""
echo "# Vérifier les connexions autorisées:"
echo "sudo ss -tuln | grep LISTEN"
echo ""

# Validation finale
log_step "VALIDATION FINALE"
echo ""
UFW_STATUS=$(sudo ufw status | head -1)
if echo "$UFW_STATUS" | grep -q "Status: active"; then
    echo "SUCCESS: Configuration du pare-feu terminée avec succès"
    echo "Le serveur web est maintenant protégé selon les bonnes pratiques DevOps"
else
    echo "ATTENTION: Le pare-feu n'est pas actif"
    echo "Vérifiez la configuration et réactivez si nécessaire"
fi

echo ""
echo "=== RÉSUMÉ DES COMPÉTENCES ACQUISES ==="
echo "- Configuration UFW pour environnement de production"
echo "- Application du principe de moindre privilège"
echo "- Sécurisation SSH avec restriction réseau"
echo "- Autorisation granulaire des services critiques"
echo "- Procédures de validation et maintenance pare-feu"
echo ""

log_step "Configuration pare-feu serveur web terminée"
