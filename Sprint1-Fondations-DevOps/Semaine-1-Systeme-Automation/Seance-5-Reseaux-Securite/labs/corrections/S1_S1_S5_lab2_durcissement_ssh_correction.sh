#!/bin/bash

# LAB 2 - Durcissement sécurité SSH - CORRECTION
#
# Cette correction présente une solution complète et optimisée pour
# le durcissement de la sécurité SSH selon les standards DevOps
#
# Concepts démontrés :
# - Sécurisation SSH par configuration avancée
# - Changement de port pour réduction d'attaques automatisées
# - Limitation des accès et tentatives d'authentification
# - Synchronisation pare-feu avec configuration SSH
#
# Bonnes pratiques appliquées :
# - Sauvegarde systématique avant modification
# - Test de configuration avant application
# - Principe de moindre privilège (désactivation root)
# - Monitoring et traçabilité des connexions

echo "=== CORRECTION LAB 2 - DURCISSEMENT SÉCURITÉ SSH ==="
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

# Fonction de validation de configuration SSH
test_ssh_config() {
    echo "Test de la configuration SSH..."
    sudo sshd -t
    if [ $? -eq 0 ]; then
        echo "Configuration SSH valide"
        return 0
    else
        echo "ERREUR: Configuration SSH invalide"
        return 1
    fi
}

log_step "Début du durcissement sécurité SSH"

# ÉTAPE 1: Sauvegarde de la configuration existante
log_step "ÉTAPE 1: Sauvegarde de la configuration SSH actuelle"
echo "Création d'une sauvegarde de sécurité..."
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
check_error "Échec de la sauvegarde"

echo "Sauvegarde créée avec timestamp:"
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)
check_error "Échec sauvegarde timestampée"

echo "Vérification des sauvegardes:"
ls -la /etc/ssh/sshd_config*
echo ""

# ÉTAPE 2: Affichage de la configuration actuelle
log_step "ÉTAPE 2: Analyse de la configuration SSH actuelle"
echo "Port SSH actuel:"
grep "^Port\|^#Port" /etc/ssh/sshd_config | head -1

echo "Configuration root actuelle:"
grep "^PermitRootLogin\|^#PermitRootLogin" /etc/ssh/sshd_config | head -1

echo "Tentatives d'authentification actuelles:"
grep "^MaxAuthTries\|^#MaxAuthTries" /etc/ssh/sshd_config | head -1
echo ""

# ÉTAPE 3: Modification sécurisée du port SSH
log_step "ÉTAPE 3: Modification du port SSH (22 → 2222)"
echo "Changement du port SSH pour réduire les attaques automatisées..."

# Sauvegarde et modification du port
sudo sed -i.bak 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config
sudo sed -i 's/^Port 22/Port 2222/' /etc/ssh/sshd_config

echo "Nouveau port SSH configuré:"
grep "^Port" /etc/ssh/sshd_config
echo ""

# ÉTAPE 4: Désactivation de l'accès root direct
log_step "ÉTAPE 4: Désactivation de l'accès root direct"
echo "Application du principe de moindre privilège..."

sudo sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

echo "Accès root SSH désactivé:"
grep "^PermitRootLogin" /etc/ssh/sshd_config
echo ""

# ÉTAPE 5: Limitation des tentatives d'authentification
log_step "ÉTAPE 5: Limitation des tentatives de connexion"
echo "Protection contre les attaques par force brute..."

# Ajouter ou modifier MaxAuthTries
if grep -q "^MaxAuthTries" /etc/ssh/sshd_config; then
    sudo sed -i 's/^MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config
else
    echo "MaxAuthTries 3" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

echo "Limitation tentatives configurée:"
grep "^MaxAuthTries" /etc/ssh/sshd_config
echo ""

# ÉTAPE 6: Configuration déconnexion automatique
log_step "ÉTAPE 6: Configuration déconnexion sessions inactives"
echo "Sécurisation contre les sessions oubliées..."

# ClientAliveInterval (5 minutes)
if grep -q "^ClientAliveInterval" /etc/ssh/sshd_config; then
    sudo sed -i 's/^ClientAliveInterval.*/ClientAliveInterval 300/' /etc/ssh/sshd_config
else
    echo "ClientAliveInterval 300" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

# ClientAliveCountMax (2 tentatives)
if grep -q "^ClientAliveCountMax" /etc/ssh/sshd_config; then
    sudo sed -i 's/^ClientAliveCountMax.*/ClientAliveCountMax 2/' /etc/ssh/sshd_config
else
    echo "ClientAliveCountMax 2" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

echo "Déconnexion automatique configurée:"
grep "^ClientAlive" /etc/ssh/sshd_config
echo ""

# ÉTAPE 7: Durcissements additionnels de sécurité
log_step "ÉTAPE 7: Applications de durcissements supplémentaires"
echo "Configuration de sécurisations avancées..."

# Force Protocol 2
if ! grep -q "^Protocol" /etc/ssh/sshd_config; then
    echo "Protocol 2" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

# LoginGraceTime
if ! grep -q "^LoginGraceTime" /etc/ssh/sshd_config; then
    echo "LoginGraceTime 60" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

# StrictModes
if ! grep -q "^StrictModes" /etc/ssh/sshd_config; then
    echo "StrictModes yes" | sudo tee -a /etc/ssh/sshd_config > /dev/null
fi

echo "Durcissements supplémentaires appliqués"
echo ""

# ÉTAPE 8: Test critique de la configuration
log_step "ÉTAPE 8: Validation critique de la configuration"
echo "Test de syntaxe AVANT redémarrage (CRITIQUE)..."

if test_ssh_config; then
    echo "Configuration SSH validée avec succès"
else
    echo "ÉCHEC: Restauration de la configuration..."
    sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config
    echo "Configuration restaurée, vérifiez les modifications"
    exit 1
fi
echo ""

# ÉTAPE 9: Redémarrage sécurisé du service SSH
log_step "ÉTAPE 9: Application de la nouvelle configuration SSH"
echo "Redémarrage du service SSH..."

sudo systemctl restart sshd
check_error "Échec redémarrage SSH"

echo "Vérification du statut du service:"
sudo systemctl status sshd --no-pager -l
echo ""

echo "Vérification du nouveau port en écoute:"
sudo ss -tuln | grep :2222
echo ""

# ÉTAPE 10: Mise à jour synchronisée du pare-feu
log_step "ÉTAPE 10: Synchronisation du pare-feu avec SSH"
echo "Adaptation d'UFW à la nouvelle configuration..."

# Autoriser le nouveau port SSH
echo "Autorisation du nouveau port SSH (2222)..."
sudo ufw allow 2222/tcp
check_error "Échec autorisation port 2222"

# Supprimer l'ancien port SSH (si règle générale existe)
echo "Suppression de l'ancienne règle SSH (port 22)..."
sudo ufw delete allow ssh 2>/dev/null || echo "Aucune règle SSH générale à supprimer"
sudo ufw delete allow 22/tcp 2>/dev/null || echo "Aucune règle port 22 spécifique à supprimer"

echo "Configuration UFW mise à jour:"
sudo ufw status numbered
echo ""

# ÉTAPE 11: Tests de validation complète
log_step "ÉTAPE 11: Tests de validation de la configuration"
echo ""

echo "=== TESTS DE VALIDATION ==="
echo ""

# Test 1: Vérification service SSH
echo "1. Statut service SSH:"
if systemctl is-active sshd >/dev/null 2>&1; then
    echo "   SUCCESS: Service SSH actif"
else
    echo "   ERREUR: Service SSH inactif"
fi

# Test 2: Vérification port en écoute
echo "2. Port SSH en écoute:"
if sudo ss -tuln | grep -q :2222; then
    echo "   SUCCESS: Port 2222 en écoute"
else
    echo "   ERREUR: Port 2222 non détecté"
fi

# Test 3: Vérification règles pare-feu
echo "3. Règles pare-feu SSH:"
if sudo ufw status | grep -q 2222; then
    echo "   SUCCESS: Port 2222 autorisé dans UFW"
else
    echo "   ATTENTION: Port 2222 non trouvé dans UFW"
fi

# Test 4: Configuration sécurisée
echo "4. Paramètres de sécurité:"
if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config; then
    echo "   SUCCESS: Accès root désactivé"
else
    echo "   ATTENTION: Accès root non désactivé"
fi

if grep -q "^MaxAuthTries 3" /etc/ssh/sshd_config; then
    echo "   SUCCESS: Limitation tentatives active"
else
    echo "   ATTENTION: Limitation tentatives non configurée"
fi
echo ""

# ÉTAPE 12: Documentation et monitoring
log_step "ÉTAPE 12: Documentation et procédures de monitoring"
echo ""

echo "=== RÉSUMÉ DE LA CONFIGURATION SÉCURISÉE ==="
echo ""
echo "PARAMÈTRES SSH DURCIS:"
echo "- Port: 2222 (au lieu de 22)"
echo "- Accès root: DÉSACTIVÉ"
echo "- Tentatives max: 3"
echo "- Déconnexion inactivité: 10 minutes"
echo "- Protocol: 2 (forcé)"
echo ""

echo "PARE-FEU ADAPTÉ:"
echo "- Port 2222/tcp: AUTORISÉ"
echo "- Port 22/tcp: SUPPRIMÉ"
echo ""

echo "=== PROCÉDURES DE CONNEXION ==="
echo ""
echo "Nouvelle commande de connexion SSH:"
echo "ssh -p 2222 utilisateur@adresse_serveur"
echo ""

echo "=== MONITORING DE SÉCURITÉ ==="
echo ""
echo "Surveillance des tentatives d'intrusion:"
echo "grep 'Failed password' /var/log/auth.log | tail -10"
echo ""
echo "Connexions SSH réussies:"
echo "grep 'Accepted' /var/log/auth.log | tail -5"
echo ""
echo "Surveillance en temps réel:"
echo "tail -f /var/log/auth.log"
echo ""

echo "=== PROCÉDURES D'URGENCE ==="
echo ""
echo "En cas de problème d'accès SSH:"
echo "1. Accès physique/console à la machine"
echo "2. Restaurer: sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config"
echo "3. Redémarrer: sudo systemctl restart sshd"
echo "4. Vérifier: sudo systemctl status sshd"
echo ""

# ÉTAPE 13: Test de connectivité (informatif)
log_step "ÉTAPE 13: Instructions de test connectivité"
echo ""
echo "IMPORTANT: Testez la connexion SSH avant de fermer cette session"
echo ""
echo "Test recommandé (depuis un autre terminal/machine):"
echo "ssh -p 2222 \$(whoami)@\$(hostname -I | awk '{print \$1}')"
echo ""
echo "Si le test échoue:"
echo "1. Vérifiez que le service SSH est actif"
echo "2. Vérifiez que le port 2222 est ouvert dans le pare-feu"
echo "3. Vérifiez les logs: sudo journalctl -u sshd -f"
echo ""

# Validation finale
log_step "VALIDATION FINALE DU DURCISSEMENT SSH"
echo ""
SSH_STATUS=$(sudo systemctl is-active sshd)
UFW_STATUS=$(sudo ufw status | grep 2222 | wc -l)

if [ "$SSH_STATUS" = "active" ] && [ "$UFW_STATUS" -gt 0 ]; then
    echo "SUCCESS: Durcissement SSH terminé avec succès"
    echo "Le serveur SSH est maintenant sécurisé selon les bonnes pratiques DevOps"
    echo ""
    echo "PROCHAINES ÉTAPES RECOMMANDÉES:"
    echo "1. Tester la connexion SSH depuis un autre terminal"
    echo "2. Configurer l'authentification par clés SSH"
    echo "3. Installer et configurer fail2ban"
    echo "4. Programmer la surveillance des logs d'authentification"
else
    echo "ATTENTION: Vérifiez la configuration"
    echo "Service SSH: $SSH_STATUS"
    echo "Règles UFW pour port 2222: $UFW_STATUS"
fi

echo ""
echo "=== COMPÉTENCES DEVOPS ACQUISES ==="
echo "- Durcissement SSH pour environnement de production"
echo "- Gestion sécurisée des configurations critiques"
echo "- Synchronisation pare-feu et services réseau"
echo "- Procédures de test et validation sécurité"
echo "- Monitoring et surveillance des accès SSH"
echo ""

log_step "Durcissement sécurité SSH terminé"
