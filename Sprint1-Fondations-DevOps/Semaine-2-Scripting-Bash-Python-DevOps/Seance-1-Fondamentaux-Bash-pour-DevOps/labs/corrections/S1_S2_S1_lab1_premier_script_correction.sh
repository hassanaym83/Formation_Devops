#!/bin/bash

# S1_S2_S1_LAB1 - Premier script Bash pour DevOps - CORRECTION
#
# Cette correction présente une solution complète et optimisée.
#
# Concepts démontrés :
# - Structure de base d'un script Bash avec shebang
# - Utilisation de commentaires descriptifs
# - Commandes système de base (date, whoami, pwd, uname, df)
# - Formatage de sortie lisible
# - Capture de résultats de commandes avec $()
#
# Bonnes pratiques appliquées :
# - Shebang en première ligne
# - Commentaires explicatifs
# - Formatage cohérent avec délimiteurs
# - Utilisation de commandes système appropriées
# - Structure claire et lisible

#!/bin/bash

# Script de vérification système DevOps
# Affiche les informations essentielles du système pour diagnostic rapide

echo "=== Script de vérification système DevOps ==="

# Affichage de la date et heure actuelles
echo "Date et heure: $(date)"

# Affichage de l'utilisateur actuel 
echo "Utilisateur actuel: $(whoami)"

# Affichage du répertoire de travail courant
echo "Répertoire de travail: $(pwd)"

# Affichage des informations système complètes
echo "Système: $(uname -a)"

# Affichage de l'espace disque disponible sur la partition racine
echo "Espace disque disponible sur / :"
df -h /

echo "=== Fin de vérification ==="

# ====== EXPLICATIONS TECHNIQUES ======

# 1. SHEBANG (#!/bin/bash)
#    Indique au système d'utiliser Bash comme interpréteur
#    Doit être la première ligne du fichier, sans espace avant #

# 2. COMMENTAIRES
#    Lignes commençant par # sont ignorées lors de l'exécution
#    Utilisées pour documenter le code et expliquer les actions

# 3. SUBSTITUTION DE COMMANDES $(commande)
#    $(date) exécute la commande 'date' et insère le résultat
#    Plus moderne que les backticks `commande`

# 4. COMMANDES SYSTÈME UTILISÉES
#    date     : Affiche la date et heure système
#    whoami   : Affiche le nom de l'utilisateur actuel
#    pwd      : Print Working Directory (répertoire courant)
#    uname -a : Unix Name avec toutes les informations système
#    df -h /  : Disk Free en format lisible pour la racine

# 5. FORMATAGE DE SORTIE
#    echo permet d'afficher du texte
#    Délimiteurs === pour structurer visuellement
#    Information descriptive avant chaque résultat

# ====== VARIANTES POSSIBLES ======

# Version avec variables intermédiaires :
# current_date=$(date)
# current_user=$(whoami)
# echo "Date: $current_date"
# echo "Utilisateur: $current_user"

# Version avec informations supplémentaires :
# echo "Nombre de processus: $(ps aux | wc -l)"
# echo "Charge système: $(uptime | cut -d',' -f3-)"
# echo "Mémoire libre: $(free -h | grep Mem | awk '{print $7}')"

# ====== UTILISATION PRATIQUE ======
# 1. Diagnostic rapide d'un serveur
# 2. Vérification d'environnement avant déploiement  
# 3. Collecte d'informations pour rapport de système
# 4. Base pour scripts de monitoring plus complexes