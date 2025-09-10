#!/bin/bash

"""
LAB 1 - Analyse des processus système

Objectifs :
- Maîtriser l'analyse des processus Linux en environnement de production
- Identifier les services critiques d'une infrastructure web
- Diagnostiquer les performances et l'utilisation des ressources

Points : 5/30

Durée estimée : 15 minutes
"""

echo "=== LAB 1 - ANALYSE PROCESSUS SYSTÈME ==="
echo "Mission: Audit des processus serveur web de production"
echo "Contexte: Optimisation performance infrastructure DevOps"
echo

# EXERCICE 1 : Inventaire des processus (3 minutes)
echo "EXERCICE 1 : Inventaire général des processus"
echo "ps aux"
echo "pstree -p"
echo "Mission : Identifier le processus parent (PID 1) et la hiérarchie"
echo

# EXERCICE 2 : Top processus par ressources (4 minutes)
echo "EXERCICE 2 : Analyse consommation ressources"
echo "ps aux --sort=-%cpu | head -10"
echo "ps aux --sort=-%mem | head -10"
echo "Mission : Identifier les 3 processus les plus gourmands"
echo

# EXERCICE 3 : Surveillance temps réel (4 minutes)
echo "EXERCICE 3 : Monitoring en temps réel"
echo "top"
echo "htop (si disponible)"
echo "Mission : Observer l'utilisation CPU et mémoire en direct"
echo

# EXERCICE 4 : Gestion des signaux (2 minutes)
echo "EXERCICE 4 : Test signaux sur processus"
echo "sleep 3600 &"
echo "kill -STOP \$!"
echo "kill -CONT \$!"
echo "kill -TERM \$!"
echo "Mission : Comprendre les états des processus"
echo

# EXERCICE 5 : Détection anomalies (2 minutes)
echo "EXERCICE 5 : Recherche processus problématiques"
echo "ps aux | awk '\$8 ~ /Z/ {print \"ZOMBIE: \" \$0}'"
echo "ps aux | awk '\$8 ~ /D/ {print \"BLOCKED: \" \$0}'"
echo "Mission : Détecter processus zombies ou bloqués"
echo

echo "=== POINTS DE CONTRÔLE ==="
echo "1. Quel est le PID du processus init ?"
echo "2. Combien de processus apache/nginx sont actifs ?"
echo "3. Quel processus consomme le plus de CPU ?"
echo "4. Y a-t-il des processus zombies ?"

echo
echo "=== FIN LAB 1 ==="

