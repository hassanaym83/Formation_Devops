#!/bin/bash

# LAB 2 - Navigation système - CORRECTION
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

# 1. Lister le contenu de la racine avec détails
echo "1. Structure racine du système:"
echo " Commande: ls -la /"
echo "-------------------------------------------"
ls -la /
echo

# 2. Analyser l'espace disque disponible
echo "2. Espace disque disponible:"
echo " Commande: df -h"
echo "-------------------------------------------"
df -h
echo

# 3. Afficher les points de montage
echo "3. Points de montage des systèmes de fichiers:"
echo " Commande: mount | grep '^/dev'"
echo "-------------------------------------------"
mount | grep '^/dev'
echo

# 4. Explorer les répertoires de configuration
echo "4. Répertoires de configuration système (/etc):"
echo " Commandes: ls -la /etc/ | head -20"
echo "-------------------------------------------"
ls -la /etc/ | head -20
echo

# 5. Analyser les logs système
echo "5. Logs système principaux (/var/log):"
echo " Commandes: find /var/log -name '*.log' -type f | head -10"
echo "-------------------------------------------"
find /var/log -name '*.log' -type f 2>/dev/null | head -10
echo

# 6. Vérifier l'utilisation de l'espace par répertoires
echo "6. Utilisation espace par répertoires principaux:"
echo " Commande: du -sh /var /etc /home /usr 2>/dev/null"
echo "-------------------------------------------"
du -sh /var /etc /home /usr 2>/dev/null
echo

# 7. Informations système et performance
echo "7. Informations système:"
echo "-------------------------------------------"
echo " Architecture: $(uname -m)"
echo " Kernel: $(uname -r)"
echo " Système: $(uname -o)"
echo " Uptime et charge:"
uptime
echo " Utilisation mémoire:"
free -h
echo

# 8. Audit des fichiers volumineux
echo "8. Fichiers volumineux (>100MB):"
echo " Commande: find /var -size +100M -type f 2>/dev/null | head -5"
echo "-------------------------------------------"
find /var -size +100M -type f 2>/dev/null | head -5
echo " (Si aucun résultat, aucun fichier >100MB trouvé dans /var)"
echo

# 9. Comptage des utilisateurs système
echo "9. Nombre d'utilisateurs système:"
echo " Commande: wc -l /etc/passwd"
echo "-------------------------------------------"
echo " Nombre total d'utilisateurs: $(wc -l < /etc/passwd)"
echo " Utilisateurs humains (UID >= 1000):"
awk -F: '$3 >= 1000 && $1 != "nobody" {print $1}' /etc/passwd | wc -l
echo

# 10. Vérification des services de logs actifs
echo "10. Taille des logs principaux:"
echo " Commandes: wc -l /var/log/syslog /var/log/auth.log 2>/dev/null"
echo "-------------------------------------------"
if [ -f /var/log/syslog ]; then
 echo " Syslog: $(wc -l < /var/log/syslog) lignes"
else
 echo " Syslog: fichier non trouvé"
fi

if [ -f /var/log/auth.log ]; then
 echo " Auth.log: $(wc -l < /var/log/auth.log) lignes"
else
 echo " Auth.log: fichier non trouvé"
fi

# Analyse supplémentaire des logs disponibles
echo " Logs disponibles dans /var/log:"
ls -lh /var/log/*.log 2>/dev/null | head -5

echo
echo "=== RAPPORT DE SYNTHÈSE ==="
echo "-------------------------------------------"
echo " Analyse du système terminée avec succès"
echo " Répertoires analysés: /, /etc, /var, /home, /usr"
echo " Espace disque vérifié sur toutes les partitions"
echo " Points de montage identifiés"
echo " Logs système localisés et analysés"
echo " Performances système évaluées"
echo "Utilisateurs système comptabilisés"
echo "Audit des fichiers volumineux effectué"
echo
echo " RECOMMANDATIONS DevOps:"
echo " 1. Surveiller l'espace disque régulièrement (df -h)"
echo " 2. Monitorer les logs de croissance (/var/log/)"
echo " 3. Vérifier les permissions critiques (/etc/)"
echo " 4. Planifier le nettoyage des fichiers temporaires"
echo " 5. Documenter l'architecture pour l'équipe"
echo
echo "=== FIN DE L'ANALYSE ==="
echo "Rapport généré le: $(date)"
echo "Analyse terminée avec succès par: $(whoami)"
