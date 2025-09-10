#!/bin/bash

"""
LAB 1 - Analyse des processus système - CORRECTION

Cette correction présente une solution complète et optimisée.

Concepts démontrés :
- Analyse des processus Linux avec ps et pstree
- Surveillance des ressources CPU et mémoire
- Gestion des signaux Unix
- Détection des processus anormaux

Bonnes pratiques appliquées :
- Utilisation des options ps pour filtrage efficace
- Tri des processus par consommation de ressources
- Identification des processus critiques
- Scripts automatisés pour audit système
"""

echo "=== LAB 1 - ANALYSE PROCESSUS SYSTÈME - CORRECTION ==="
echo "Mission: Audit des processus serveur web de production"
echo "Contexte: Optimisation performance infrastructure DevOps"
echo

# EXERCICE 1 : Inventaire des processus (3 minutes)
echo "EXERCICE 1 : Inventaire général des processus"
echo "Commande principale :"
ps aux | head -20

echo
echo "Hiérarchie des processus :"
pstree -p | head -15

echo "Mission : Identifier le processus parent (PID 1) et la hiérarchie"
echo "Réponse : Le processus init/systemd a toujours le PID 1"
echo

# EXERCICE 2 : Top processus par ressources (4 minutes)
echo "EXERCICE 2 : Analyse consommation ressources"
echo "Top 5 processus CPU :"
ps aux --sort=-%cpu | head -6

echo
echo "Top 5 processus Mémoire :"
ps aux --sort=-%mem | head -6

echo "Mission : Identifier les 3 processus les plus gourmands"
echo "Analyse : Observer les colonnes %CPU et %MEM pour identifier les goulots"
echo

# EXERCICE 3 : Surveillance temps réel (4 minutes)
echo "EXERCICE 3 : Monitoring en temps réel"
echo "Commande top avec tri par CPU (utiliser 'P' dans top) :"
echo "top -o %CPU -n 1 | head -15"
top -o %CPU -n 1 | head -15

echo
echo "Alternative htop si disponible :"
which htop > /dev/null && echo "htop installé" || echo "htop non installé - utiliser: sudo apt install htop"

echo "Mission : Observer l'utilisation CPU et mémoire en direct"
echo "Analyse : La charge système (load average) doit être < nombre de CPU"
echo

# EXERCICE 4 : Gestion des signaux (2 minutes)
echo "EXERCICE 4 : Test signaux sur processus"
echo "Création processus de test :"
sleep 3600 &
TEST_PID=$!
echo "PID du processus test : $TEST_PID"

echo "Pause du processus :"
kill -STOP $TEST_PID
ps aux | grep $TEST_PID | grep -v grep

echo "Reprise du processus :"
kill -CONT $TEST_PID
ps aux | grep $TEST_PID | grep -v grep

echo "Arrêt propre du processus :"
kill -TERM $TEST_PID
sleep 1
ps aux | grep $TEST_PID | grep -v grep || echo "Processus terminé proprement"

echo "Mission : Comprendre les états des processus"
echo "États observés : T (stopped), S (sleeping), terminé"
echo

# EXERCICE 5 : Détection anomalies (2 minutes)
echo "EXERCICE 5 : Recherche processus problématiques"
echo "Recherche processus zombies :"
ZOMBIES=$(ps aux | awk '$8 ~ /Z/ {print "ZOMBIE: " $0}')
if [ -z "$ZOMBIES" ]; then
    echo "Aucun processus zombie détecté"
else
    echo "$ZOMBIES"
fi

echo
echo "Recherche processus bloqués :"
BLOCKED=$(ps aux | awk '$8 ~ /D/ {print "BLOCKED: " $0}')
if [ -z "$BLOCKED" ]; then
    echo "Aucun processus bloqué détecté"
else
    echo "$BLOCKED"
fi

echo "Mission : Détecter processus zombies ou bloqués"
echo "Analyse : Processus Z = zombies (problème), D = bloqués en I/O (critique)"
echo

echo "=== RÉPONSES AUX POINTS DE CONTRÔLE ==="
echo "1. PID du processus init : 1 (systemd sur les systèmes modernes)"
echo "2. Processus web actifs :"
ps aux | grep -E "(apache|nginx|httpd)" | grep -v grep | wc -l | xargs echo "Nombre de processus web :"

echo "3. Processus consommant le plus de CPU :"
ps aux --sort=-%cpu | head -2 | tail -1 | awk '{print $11 " (" $3 "%)"}'

echo "4. Présence de processus zombies :"
ZOMBIE_COUNT=$(ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}')
echo "Nombre de zombies : $ZOMBIE_COUNT"

echo
echo "=== SCRIPT D'AUDIT AUTOMATISÉ ==="
cat << 'EOF' > system_audit.sh
#!/bin/bash
echo "=== AUDIT SYSTÈME AUTOMATISÉ ==="
echo "Date : $(date)"
echo "Uptime : $(uptime)"
echo "Processus total : $(ps aux | wc -l)"
echo "Top 3 CPU : "
ps aux --sort=-%cpu | head -4 | tail -3 | awk '{print $11 " (" $3 "%)"}'
echo "Top 3 Mémoire : "
ps aux --sort=-%mem | head -4 | tail -3 | awk '{print $11 " (" $4 "%)"}'
echo "Zombies : $(ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}')"
echo "Load average : $(uptime | awk -F'load average:' '{print $2}')"
EOF

chmod +x system_audit.sh
echo "Script créé : system_audit.sh"
./system_audit.sh

echo
echo "=== FIN CORRECTION LAB 1 ==="
echo "Concepts maîtrisés : Analyse processus, surveillance ressources, signaux Unix"

