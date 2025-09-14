#!/bin/bash

"""
LAB 3 - Monitoring des ressources système - CORRECTION

Cette correction présente une solution complète pour surveiller les ressources.

Concepts démontrés :
- Surveillance CPU, mémoire, disque avec outils système
- Analyse des processus gourmands en ressources
- Identification des goulots d'étranglement performance
- Automatisation du monitoring avec scripts

Bonnes pratiques appliquées :
- Combinaison d'outils complémentaires (top, ps, df, free)
- Interprétation correcte des métriques système
- Alertes automatisées sur seuils critiques
- Documentation des investigations performance
"""

echo "=== LAB 3 - MONITORING RESSOURCES SYSTÈME - CORRECTION ==="
echo "Mission: Surveillance performance serveur production"
echo "Contexte: Diagnostiquer ralentissements système"
echo

# EXERCICE 1 : État CPU et load average (4 minutes)
echo "EXERCICE 1 : Analyse charge CPU"
echo "Load average et CPU :"
uptime
echo

echo "Processus les plus gourmands en CPU :"
ps aux --sort=-%cpu | head -10

echo
echo "Informations CPU détaillées :"
nproc # Nombre de cœurs
cat /proc/loadavg
echo "Load average expliqué :"
echo "- 1min 5min 15min running/total last_pid"
echo "- Load < nombre_cores = OK"
echo "- Load > nombre_cores = surcharge"

echo
echo "Mission : Analyser la charge CPU système"
echo "Analyse : Load average indique la pression sur le système"
echo

# EXERCICE 2 : Utilisation mémoire (4 minutes)
echo "EXERCICE 2 : État de la mémoire"
echo "Mémoire système :"
free -h

echo
echo "Détail de l'utilisation mémoire :"
cat /proc/meminfo | grep -E "(MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree)"

echo
echo "Processus consommant le plus de mémoire :"
ps aux --sort=-%mem | head -10

echo
echo "Analyse mémoire :"
TOTAL_MEM=$(free -m | awk 'NR==2{print $2}')
USED_MEM=$(free -m | awk 'NR==2{print $3}')
PERCENT_USED=$((USED_MEM * 100 / TOTAL_MEM))
echo "Utilisation mémoire : ${PERCENT_USED}%"

if [ $PERCENT_USED -gt 80 ]; then
 echo " ALERTE : Mémoire critique (>80%)"
elif [ $PERCENT_USED -gt 60 ]; then
 echo " ATTENTION : Mémoire élevée (>60%)"
else
 echo " Mémoire normale"
fi

echo "Mission : Surveiller consommation mémoire"
echo "Analyse : Mémoire Available plus important que Free"
echo

# EXERCICE 3 : Espace disque et I/O (4 minutes)
echo "EXERCICE 3 : Surveillance stockage"
echo "Espace disque par partition :"
df -h

echo
echo "Répertoires volumineux (top 10) :"
du -h / 2>/dev/null | sort -hr | head -10

echo
echo "Inodes (fichiers disponibles) :"
df -i

echo
echo "Activité I/O (si iostat disponible) :"
if command -v iostat >/dev/null 2>&1; then
 iostat -x 1 1
else
 echo "iostat non installé - utilisation de /proc/diskstats :"
 cat /proc/diskstats | head -5
fi

echo
echo "Analyse espace disque :"
df -h | awk 'NR>1 {gsub(/%/, "", $5); if($5 > 80) print " ALERTE: " $6 " plein à " $5 "%"; else if($5 > 60) print " ATTENTION: " $6 " à " $5 "%"; else print " " $6 " OK (" $5 "%)"}'

echo "Mission : Contrôler l'espace disque disponible"
echo "Analyse : Surveiller les partitions critiques (/,/var,/tmp)"
echo

# EXERCICE 4 : Processus et ressources (4 minutes)
echo "EXERCICE 4 : Analyse des processus"
echo "Vue d'ensemble top (simulation) :"
top -b -n1 | head -20

echo
echo "Processus par état :"
ps aux | awk '{print $8}' | sort | uniq -c | sort -nr
echo "États : R=Running, S=Sleep, D=Uninterruptible, Z=Zombie, T=Stopped"

echo
echo "Processus zombies (si existants) :"
ZOMBIES=$(ps aux | awk '$8 ~ /^Z/ {print $2, $11}')
if [ -z "$ZOMBIES" ]; then
 echo " Aucun processus zombie"
else
 echo " Processus zombies détectés :"
 echo "$ZOMBIES"
fi

echo
echo "Processus par utilisateur :"
ps aux | awk '{print $1}' | sort | uniq -c | sort -nr | head -5

echo "Mission : Identifier processus problématiques"
echo "Analyse : Zombies et processus en D indiquent des problèmes"
echo

# EXERCICE 5 : Surveillance réseau (2 minutes)
echo "EXERCICE 5 : Activité réseau"
echo "Connexions réseau actives :"
netstat -tuln 2>/dev/null | head -10 || ss -tuln | head -10

echo
echo "Connexions établies :"
netstat -tun 2>/dev/null | grep ESTABLISHED | wc -l || ss -tun | grep ESTAB | wc -l

echo
echo "Statistiques réseau :"
cat /proc/net/dev | head -5

echo "Mission : Contrôler activité réseau"
echo "Analyse : Détecter connexions anormales et saturation"
echo

# EXERCICE 6 : Alertes automatisées (2 minutes)
echo "EXERCICE 6 : Système d'alertes"
echo "Création script de surveillance :"

cat << 'EOF' > system_monitor.sh
#!/bin/bash
# Script de monitoring système avec alertes

LOG_FILE="/tmp/system_monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Début monitoring" >> $LOG_FILE

# Seuils d'alerte
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=80

# CPU Load
LOAD_1MIN=$(uptime | awk -F'load average:' '{print $2}' | awk -F',' '{print $1}' | sed 's/ //g')
CORES=$(nproc)
CPU_LOAD=$(echo "$LOAD_1MIN * 100 / $CORES" | bc -l 2>/dev/null | cut -d. -f1)

# Mémoire
MEM_USED=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')

# Disque
DISK_USED=$(df / | awk 'NR==2{print $5}' | sed 's/%//')

# Vérifications et alertes
echo "=== RAPPORT MONITORING ===" >> $LOG_FILE
echo "CPU Load: ${CPU_LOAD:-0}%" >> $LOG_FILE
echo "Mémoire: ${MEM_USED}%" >> $LOG_FILE 
echo "Disque /: ${DISK_USED}%" >> $LOG_FILE

# Alertes
if [ "${CPU_LOAD:-0}" -gt $CPU_THRESHOLD ]; then
 echo " ALERTE CPU: ${CPU_LOAD}% > $CPU_THRESHOLD%" >> $LOG_FILE
fi

if [ "$MEM_USED" -gt $MEM_THRESHOLD ]; then
 echo " ALERTE MÉMOIRE: ${MEM_USED}% > $MEM_THRESHOLD%" >> $LOG_FILE
fi

if [ "$DISK_USED" -gt $DISK_THRESHOLD ]; then
 echo " ALERTE DISQUE: ${DISK_USED}% > $DISK_THRESHOLD%" >> $LOG_FILE
fi

echo "=========================" >> $LOG_FILE
echo ""
EOF

chmod +x system_monitor.sh
echo "Script créé : system_monitor.sh"

echo "Exécution du monitoring :"
./system_monitor.sh

echo "Contenu du rapport :"
cat /tmp/system_monitor.log

echo "Mission : Automatiser la surveillance"
echo "Analyse : Scripts permettent monitoring continu et alertes"
echo

echo "=== RÉPONSES AUX POINTS DE CONTRÔLE ==="
echo "1. Processus CPU élevé :"
ps aux --sort=-%cpu | awk 'NR==2{print $11 ": " $3 "%"}'

echo "2. Mémoire disponible :"
free -m | awk 'NR==2{print "Disponible: " $7 "MB / " $2 "MB total"}'

echo "3. Partition la plus pleine :"
df -h | awk 'NR>1 && $5+0 > max {max=$5+0; line=$0} END{print line}'

echo "4. Load average actuel :"
uptime | awk -F'load average:' '{print "Load:" $2}'

echo "5. Processus zombies :"
ZOMBIE_COUNT=$(ps aux | awk '$8 ~ /^Z/' | wc -l)
echo "Zombies détectés : $ZOMBIE_COUNT"

echo
echo "=== DASHBOARD SYSTÈME COMPLET ==="
cat << 'EOF' > dashboard.sh
#!/bin/bash
clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║ DASHBOARD SYSTÈME ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

echo " CPU & LOAD:"
echo " $(uptime)"
echo

echo " MÉMOIRE:"
echo " $(free -h | grep Mem)"
echo

echo " DISQUE:"
df -h | awk 'NR==1 || $5+0 > 50'
echo

echo "TOP PROCESSUS CPU:"
ps aux --sort=-%cpu | head -6
echo

echo " TOP PROCESSUS MÉMOIRE:"
ps aux --sort=-%mem | head -6
echo

echo "RÉSEAU:"
echo " Connexions actives: $(netstat -tun 2>/dev/null | grep ESTABLISHED | wc -l || ss -tun | grep ESTAB | wc -l)"
echo
EOF

chmod +x dashboard.sh
echo "Dashboard créé : dashboard.sh"
./dashboard.sh

echo
echo "=== FIN CORRECTION LAB 3 ==="
echo "Concepts maîtrisés : monitoring, ressources, alertes, diagnostic performance"

