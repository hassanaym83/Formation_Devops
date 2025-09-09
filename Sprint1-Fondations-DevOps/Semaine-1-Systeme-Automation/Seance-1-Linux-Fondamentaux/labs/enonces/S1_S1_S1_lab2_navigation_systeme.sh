#!/bin/bash

# LAB 2 - Navigation système
# 
# Objectifs :
# - Explorer l'architecture du système de fichiers Linux
# - Documenter la structure des répertoires système
# - Analyser l'espace disque et les points de montage
# - Utiliser les commandes d'analyse et monitoring système
# 
# Points : 5/30
# 
# Durée estimée : 20 minutes

# Mission: Créer un script de découverte système pour audit DevOps
# Contexte: Nouveau serveur Linux à analyser pour équipe développement

echo "=== ANALYSE SYSTÈME DE FICHIERS ==="
echo "Date d'analyse: $(date)"
echo "Serveur: $(hostname)"
echo "Utilisateur: $(whoami)"
echo

# TODO: 1. Lister le contenu de la racine avec détails
echo "1. Structure racine du système:"
echo "   Commande: ls -la /"
# TODO: Utiliser ls -la / pour afficher tous les répertoires racine avec permissions

echo

# TODO: 2. Analyser l'espace disque disponible
echo "2. Espace disque disponible:"
echo "   Commande: df -h"
# TODO: Utiliser df -h pour afficher l'espace disque en format lisible

echo

# TODO: 3. Afficher les points de montage
echo "3. Points de montage des systèmes de fichiers:"
echo "   Commande: mount | grep '^/dev'"
# TODO: Utiliser mount pour afficher les systèmes de fichiers montés

echo

# TODO: 4. Explorer les répertoires de configuration
echo "4. Répertoires de configuration système (/etc):"
echo "   Commandes: ls -la /etc/ | head -20"
# TODO: Lister les 20 premiers éléments de /etc avec détails

echo

# TODO: 5. Analyser les logs système
echo "5. Logs système principaux (/var/log):"
echo "   Commandes: find /var/log -name '*.log' -type f | head -10"
# TODO: Trouver les 10 premiers fichiers .log dans /var/log

echo

# TODO: 6. Vérifier l'utilisation de l'espace par répertoires
echo "6. Utilisation espace par répertoires principaux:"
echo "   Commande: du -sh /var /etc /home /usr 2>/dev/null"
# TODO: Utiliser du -sh pour calculer la taille des répertoires importants

echo

# TODO: 7. Informations système et performance
echo "7. Informations système:"
echo "   Architecture: uname -m"
echo "   Kernel: uname -r"
echo "   Uptime: uptime"
echo "   Mémoire: free -h"
# TODO: Utiliser uname, uptime et free pour les informations système

echo

# TODO: 8. Audit des fichiers volumineux
echo "8. Fichiers volumineux (>100MB):"
echo "   Commande: find /var -size +100M -type f 2>/dev/null | head -5"
# TODO: Rechercher les gros fichiers dans /var pour audit espace disque

echo

# TODO: 9. Comptage des utilisateurs système
echo "9. Nombre d'utilisateurs système:"
echo "   Commande: wc -l /etc/passwd"
# TODO: Compter le nombre de lignes dans /etc/passwd

echo

# TODO: 10. Vérification des services de logs actifs
echo "10. Taille des logs principaux:"
echo "    Commandes: wc -l /var/log/syslog /var/log/auth.log 2>/dev/null"
# TODO: Compter les lignes des logs système principaux

echo
echo "=== FIN DE L'ANALYSE ==="
echo "Rapport généré le: $(date)"
echo "Analyse terminée avec succès!"