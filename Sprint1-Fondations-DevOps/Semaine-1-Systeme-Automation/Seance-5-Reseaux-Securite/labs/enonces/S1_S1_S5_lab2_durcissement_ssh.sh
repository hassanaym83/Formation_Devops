#!/bin/bash

# LAB 2 - Durcissement sécurité SSH
#
# Objectifs :
# - Implémenter les mesures de sécurisation SSH essentielles
# - Protéger contre les attaques par force brute
# - Configurer SSH selon les bonnes pratiques DevOps
#
# Points : 5/30
# Durée estimée : 20 minutes
#
# Contexte : Serveur critique DevOps exposé sur Internet nécessitant
# durcissement contre les attaques par force brute et tentatives d'intrusion

echo "=== LAB 2 - DURCISSEMENT SÉCURITÉ SSH ==="
echo ""

# CONTEXTE ET ENJEUX
echo "CONTEXTE: Sécurisation SSH pour environnement DevOps de production"
echo ""
echo "PROBLÉMATIQUE:"
echo "- Serveur DevOps exposé sur Internet"
echo "- Tentatives d'intrusion SSH détectées dans les logs"
echo "- Nécessité de durcir la configuration selon les standards sécurité"
echo ""

# ÉTAPE 1: Sauvegarde de la configuration actuelle
echo "ÉTAPE 1: Sauvegarde de la configuration SSH existante"
echo "IMPORTANT: Toujours sauvegarder avant modification"
echo ""
echo "Commande à exécuter:"
echo "sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup"
echo ""
echo "Vérification de la sauvegarde:"
echo "ls -la /etc/ssh/sshd_config*"
echo ""
echo "Résultat attendu: Fichier de sauvegarde créé avec succès"
echo ""

# ÉTAPE 2: Changement du port SSH par défaut
echo "ÉTAPE 2: Modification du port SSH (sécurité par obscurité)"
echo "Pourquoi changer le port 22?"
echo "- Réduire les scans automatisés"
echo "- Diminuer le bruit dans les logs"
echo "- Première barrière contre les attaques de masse"
echo ""
echo "Configuration à modifier dans /etc/ssh/sshd_config:"
echo "# Chercher la ligne: #Port 22"
echo "# Remplacer par: Port 2222"
echo ""
echo "Commande pour édition:"
echo "sudo nano /etc/ssh/sshd_config"
echo ""
echo "Résultat attendu: Port SSH modifié de 22 vers 2222"
echo ""

# ÉTAPE 3: Désactivation de la connexion root
echo "ÉTAPE 3: Désactivation de l'accès root direct"
echo "Pourquoi interdire root?"
echo "- Principe de moindre privilège"
echo "- Force l'usage de sudo (traçabilité)"
echo "- Élimine une cible d'attaque connue"
echo ""
echo "Configuration à modifier:"
echo "# Chercher: #PermitRootLogin yes"
echo "# Remplacer par: PermitRootLogin no"
echo ""
echo "Résultat attendu: Accès root SSH désactivé"
echo ""

# ÉTAPE 4: Limitation des tentatives d'authentification
echo "ÉTAPE 4: Limitation des tentatives de connexion"
echo "Protection contre les attaques par force brute"
echo ""
echo "Configuration à ajouter/modifier:"
echo "MaxAuthTries 3"
echo ""
echo "Effet: Maximum 3 tentatives avant déconnexion"
echo ""

# ÉTAPE 5: Configuration de la déconnexion automatique
echo "ÉTAPE 5: Déconnexion des sessions inactives"
echo "Sécurisation contre les sessions oubliées"
echo ""
echo "Configuration à ajouter:"
echo "ClientAliveInterval 300"
echo "ClientAliveCountMax 2"
echo ""
echo "Effet: Déconnexion après 10 minutes d'inactivité (300s x 2)"
echo ""

# ÉTAPE 6: Autres durcissements recommandés
echo "ÉTAPE 6: Durcissements additionnels (optionnels)"
echo ""
echo "Configurations supplémentaires recommandées:"
echo "Protocol 2                    # Force SSH version 2"
echo "LoginGraceTime 60            # Limite temps de connexion"
echo "StrictModes yes              # Vérification permissions fichiers"
echo "MaxStartups 10:30:60         # Limite connexions simultanées"
echo ""

# ÉTAPE 7: Test de la configuration
echo "ÉTAPE 7: Validation de la configuration SSH"
echo "CRITIQUE: Tester AVANT le redémarrage du service"
echo ""
echo "Commande de test:"
echo "sudo sshd -t"
echo ""
echo "Résultat attendu: Aucune erreur de syntaxe"
echo "Si erreur: corriger avant redémarrage"
echo ""

# ÉTAPE 8: Redémarrage du service SSH
echo "ÉTAPE 8: Application de la configuration"
echo "ATTENTION: Assurez-vous d'avoir un accès alternatif (console physique)"
echo ""
echo "Commande de redémarrage:"
echo "sudo systemctl restart sshd"
echo ""
echo "Vérification du service:"
echo "sudo systemctl status sshd"
echo ""
echo "Résultat attendu: Service SSH actif sur nouveau port"
echo ""

# ÉTAPE 9: Mise à jour du pare-feu
echo "ÉTAPE 9: Adaptation du pare-feu au nouveau port"
echo "Synchronisation UFW avec la nouvelle configuration SSH"
echo ""
echo "Commandes à exécuter:"
echo "sudo ufw allow 2222/tcp      # Autoriser nouveau port"
echo "sudo ufw delete allow ssh    # Supprimer ancienne règle port 22"
echo ""
echo "Vérification:"
echo "sudo ufw status numbered"
echo ""

# ÉTAPE 10: Tests de connectivité
echo "ÉTAPE 10: Test de la nouvelle configuration"
echo ""
echo "Test de connexion SSH sur nouveau port:"
echo "ssh -p 2222 utilisateur@adresse_serveur"
echo ""
echo "Vérification port en écoute:"
echo "sudo ss -tuln | grep 2222"
echo ""
echo "Résultat attendu: Connexion SSH fonctionnelle sur port 2222"
echo ""

echo "=== CRITÈRES D'ÉVALUATION ==="
echo ""
echo "1. Changement de port sécurisé (1 point)"
echo "   - Port SSH modifié de 22 vers 2222"
echo "   - Configuration testée avant application"
echo ""
echo "2. Désactivation root et limitations appropriées (2 points)"
echo "   - PermitRootLogin no configuré"
echo "   - MaxAuthTries 3 configuré"
echo "   - ClientAliveInterval configuré"
echo ""
echo "3. Mise à jour pare-feu cohérente (2 points)"
echo "   - Nouveau port SSH autorisé dans UFW"
echo "   - Ancien port SSH supprimé du pare-feu"
echo "   - Test connectivité réussi"
echo ""

echo "=== DOCUMENTATION À PRODUIRE ==="
echo ""
echo "1. Copie de la configuration SSH modifiée"
echo "2. Résultat du test 'sudo sshd -t'"
echo "3. Statut UFW après modification"
echo "4. Preuve de connexion SSH sur nouveau port"
echo ""

echo "=== PROCÉDURES DE RÉCUPÉRATION ==="
echo ""
echo "# Si vous perdez l'accès SSH:"
echo "# 1. Accès physique à la machine (console/KVM/IPMI)"
echo "# 2. Restaurer la configuration:"
echo "#    sudo cp /etc/ssh/sshd_config.backup /etc/ssh/sshd_config"
echo "# 3. Redémarrer SSH: sudo systemctl restart sshd"
echo ""
echo "# Vérification du port SSH actuel:"
echo "# sudo ss -tuln | grep ssh"
echo "# ou"
echo "# grep '^Port' /etc/ssh/sshd_config"
echo ""

echo "=== MONITORING SÉCURITÉ SSH ==="
echo ""
echo "# Surveillance tentatives d'intrusion:"
echo "grep 'Failed password' /var/log/auth.log | tail -10"
echo ""
echo "# Connexions SSH réussies:"
echo "grep 'Accepted' /var/log/auth.log | tail -5"
echo ""
echo "# Surveillance en temps réel:"
echo "tail -f /var/log/auth.log"
