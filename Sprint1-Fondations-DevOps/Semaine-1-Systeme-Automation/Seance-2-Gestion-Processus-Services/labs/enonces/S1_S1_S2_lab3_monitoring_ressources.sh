#!/bin/bash

"""
LAB 3 - Monitoring des ressources système

Objectifs :
- Surveiller les performances du système (CPU, mémoire, disque)
- Identifier les goulots d'étranglement et processus problématiques
- Utiliser les outils de monitoring pour le diagnostic DevOps

Points : 5/30

Durée estimée : 20 minutes
"""

echo "=== LAB 3 - MONITORING RESSOURCES SYSTÈME ==="
echo "Mission: Diagnostic performance serveur de production"
echo "Contexte: Analyse des ressources sous charge applicative"
echo

# EXERCICE 1 : Vue d'ensemble système (3 minutes)
echo "EXERCICE 1 : État général des ressources"
echo "uptime"
echo "free -h"
echo "df -h"
echo "Mission : Analyser charge, mémoire et espace disque"
echo

# EXERCICE 2 : Surveillance CPU (4 minutes)
echo "EXERCICE 2 : Analyse utilisation CPU"
echo "top -o %CPU"
echo "htop"
echo "ps aux --sort=-%cpu | head -10"
echo "Mission : Identifier les processus gourmands en CPU"
echo

# EXERCICE 3 : Surveillance mémoire (4 minutes)
echo "EXERCICE 3 : Analyse consommation mémoire"
echo "free -h"
echo "ps aux --sort=-%mem | head -10"
echo "cat /proc/meminfo | grep -E '(MemTotal|MemFree|MemAvailable)'"
echo "Mission : Détecter les fuites mémoire et la saturation"
echo

# EXERCICE 4 : Surveillance disque et I/O (4 minutes)
echo "EXERCICE 4 : Analyse stockage et I/O"
echo "df -h"
echo "du -sh /var/log /opt /home"
echo "iostat -x 1 3 (si disponible)"
echo "Mission : Identifier problèmes d'espace et de performance I/O"
echo

# EXERCICE 5 : Processus problématiques (3 minutes)
echo "EXERCICE 5 : Détection processus anormaux"
echo "ps aux | awk '\$8 ~ /Z/ {print \$0}'"
echo "ps aux | awk '\$8 ~ /D/ {print \$0}'"
echo "ps aux | grep -E '(100.0|99\.[0-9])' || echo 'Aucun processus à 100% CPU'"
echo "Mission : Localiser processus zombies, bloqués ou en surcharge"
echo

# EXERCICE 6 : Script de monitoring (2 minutes)
echo "EXERCICE 6 : Création monitoring automatisé"
echo "Créer un script 'system_check.sh' qui affiche :"
echo "echo '=== MONITORING SYSTÈME ==='"
echo "echo 'Date: \$(date)'"
echo "echo 'Load: \$(uptime | awk -F\"load average:\" \"{print \\\$2}\")'"
echo "echo 'Mémoire libre: \$(free -h | awk \"NR==2{print \\\$4}\")'"
echo "echo 'Disque libre: \$(df -h / | awk \"NR==2{print \\\$4}\")'"
echo

echo "=== POINTS DE CONTRÔLE ==="
echo "1. Quelle est la charge moyenne du système ?"
echo "2. Combien de mémoire est disponible ?"
echo "3. Quel processus utilise le plus de CPU ?"
echo "4. Y a-t-il des processus zombies ou bloqués ?"
echo "5. Quel système de fichiers a le moins d'espace libre ?"

echo
echo "=== FIN LAB 3 ==="

