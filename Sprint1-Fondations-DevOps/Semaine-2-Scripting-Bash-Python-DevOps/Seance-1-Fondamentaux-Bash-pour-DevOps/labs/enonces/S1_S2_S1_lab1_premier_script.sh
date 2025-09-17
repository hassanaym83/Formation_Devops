#!/bin/bash

# S1_S2_S1_LAB1 - Premier script Bash pour DevOps
# DURÉE : 15 minutes

# OBJECTIF :
# Créez votre premier script Bash d'information système pour DevOps.

# CONTEXTE :
# Script de diagnostic rapide pour vérification d'environnement DevOps

# CONSIGNES :
# 1. Ajoutez le shebang et des commentaires descriptifs
# 2. Affichez les informations système suivantes :
#    - Date et heure actuelles
#    - Nom d'utilisateur actuel
#    - Répertoire de travail actuel
#    - Version du système d'exploitation
#    - Espace disque disponible sur /
# 3. Utilisez des commandes système appropriées
# 4. Formatez la sortie de manière lisible

# CRITÈRES D'ÉVALUATION :
# □ Shebang correct (#!/bin/bash)
# □ Commentaires clairs et descriptifs
# □ 5 informations système affichées
# □ Utilisation correcte des commandes (date, whoami, pwd, uname, df)
# □ Sortie formatée et lisible

# RÉSULTAT ATTENDU :
# Un script qui affiche un rapport système basique dans un format clair et structuré

# ====== TEMPLATE DE DÉPART ======

# TODO: Ajoutez le shebang approprié

# TODO: Ajoutez un commentaire de description du script

echo "=== Script de vérification système DevOps ==="

# TODO: Affichez la date et heure actuelles avec la commande 'date'

# TODO: Affichez l'utilisateur actuel avec la commande 'whoami'

# TODO: Affichez le répertoire de travail avec la commande 'pwd'

# TODO: Affichez les informations système avec la commande 'uname'

# TODO: Affichez l'espace disque disponible avec la commande 'df'

echo "=== Fin de vérification ==="

# ====== COMMANDES UTILES ======
# date                    # Affiche la date et heure
# whoami                  # Affiche l'utilisateur actuel
# pwd                     # Affiche le répertoire courant
# uname -a                # Affiche les informations système complètes
# df -h /                 # Affiche l'espace disque en format lisible

# ====== TESTS À EFFECTUER ======
# 1. Rendez le script exécutable : chmod +x S1_S2_S1_lab1_premier_script.sh
# 2. Exécutez le script : ./S1_S2_S1_lab1_premier_script.sh
# 3. Vérifiez que toutes les informations s'affichent correctement

# AIDE :
# - Utilisez $(commande) pour capturer le résultat d'une commande
# - Utilisez echo pour afficher du texte
# - Formatez avec des "===" pour délimiter les sections