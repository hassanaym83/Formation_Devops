#!/bin/bash

"""
LAB 4 CHALLENGE - Investigation forensique système - CORRECTION

Cette correction présente une approche méthodologique d'investigation système.

Concepts avancés démontrés :
- Analyse forensique de processus suspects
- Investigation de performance et goulots d'étranglement
- Corrélation logs système et événements
- Méthodologie de diagnostic structurée

Techniques expertes appliquées :
- Combinaison d'outils d'investigation (ps, lsof, strace, netstat)
- Analyse temporelle des événements système
- Identification de patterns anormaux
- Documentation complète des investigations
"""

echo "=== LAB 4 CHALLENGE - INVESTIGATION FORENSIQUE - CORRECTION ==="
echo "Mission: Diagnostic expert d'un serveur en production"
echo "Contexte: Problèmes de performance et comportements suspects"
echo "Niveau: Challenge technique avancé"
echo

# PHASE 1 : Reconnaissance initiale (10 minutes)
echo "PHASE 1 : RECONNAISSANCE SYSTÈME"
echo "========================================="
echo "Collecte d'informations de base :"

echo "1. Informations système :"
echo " Hostname : $(hostname)"
echo " Uptime : $(uptime)"
echo " Kernel : $(uname -r)"
echo " Charge : $(cat /proc/loadavg)"

echo
echo "2. État général des ressources :"
echo " CPU Cores: $(nproc)"
echo " RAM Total: $(free -h | awk 'NR==2{print $2}')"
echo " RAM Libre: $(free -h | awk 'NR==2{print $7}')"
echo " Disque / : $(df -h / | awk 'NR==2{print $4}') libre"

echo
echo "3. Services critiques :"
CRITICAL_SERVICES=("ssh" "sshd" "systemd" "NetworkManager" "dbus")
for service in "${CRITICAL_SERVICES[@]}"; do
 if systemctl is-active "$service" >/dev/null 2>&1; then
 echo " $service : ACTIF"
 else
 echo " $service : INACTIF ou inexistant"
 fi
done

echo
echo "Mission : Établir l'état de référence du système"
echo "Analyse : Base de données pour comparaisons futures"
echo

# PHASE 2 : Analyse des processus suspects (10 minutes)
echo "PHASE 2 : INVESTIGATION PROCESSUS"
echo "========================================="

echo "1. Top processus par consommation CPU :"
ps aux --sort=-%cpu | head -10

echo
echo "2. Top processus par consommation mémoire :"
ps aux --sort=-%mem | head -10

echo
echo "3. Processus avec beaucoup de threads :"
ps -eLf | awk '{print $4}' | sort | uniq -c | sort -nr | head -10

echo
echo "4. Recherche de processus suspects :"
echo " Processus sans TTY (daemons malveillants potentiels) :"
ps aux | awk '$7 == "?" && $1 != "root" {print $1, $2, $11}' | head -5

echo
echo " Processus avec noms suspects :"
ps aux | grep -E "(tmp|dev|shm)" | grep -v grep

echo
echo " Processus zombies :"
ZOMBIES=$(ps aux | awk '$8 ~ /^Z/ {print $2, $11}')
if [ -z "$ZOMBIES" ]; then
 echo " Aucun processus zombie détecté"
else
 echo " Processus zombies :"
 echo "$ZOMBIES"
fi

echo
echo "5. Analyse des connexions processus :"
echo " Processus avec plus de connexions réseau :"
lsof -i 2>/dev/null | awk '{print $2}' | sort | uniq -c | sort -nr | head -5

echo "Mission : Identifier les processus anormaux"
echo "Analyse : Processus suspects = consommation excessive + noms étranges + comportement anormal"
echo

# PHASE 3 : Investigation réseau (8 minutes)
echo "PHASE 3 : ANALYSE RÉSEAU"
echo "========================================="

echo "1. Connexions réseau actives :"
netstat -tuln 2>/dev/null | head -10 || ss -tuln | head -10

echo
echo "2. Connexions établies par IP :"
netstat -tun 2>/dev/null | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr || \
ss -tun | grep ESTAB | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr

echo
echo "3. Ports en écoute suspects :"
echo " Ports non standard en écoute :"
netstat -tuln 2>/dev/null | awk '$4 ~ /:/ {split($4,a,":"); if(a[2] > 1024 && a[2] != 8080 && a[2] != 3000) print $0}' || \
ss -tuln | awk '$4 ~ /:/ {split($4,a,":"); if(a[2] > 1024 && a[2] != 8080 && a[2] != 3000) print $0}'

echo
echo "4. Analyse trafic :"
echo " Statistiques interfaces réseau :"
cat /proc/net/dev | awk 'NR>2 {print $1, "RX:", $2, "TX:", $10}' | head -5

echo "Mission : Détecter activités réseau suspectes"
echo "Analyse : Connexions vers IPs inconnues + ports non standard"
echo

# PHASE 4 : Analyse des fichiers et accès (7 minutes)
echo "PHASE 4 : INVESTIGATION FICHIERS"
echo "========================================="

echo "1. Fichiers récemment modifiés (dernière heure) :"
find /tmp -type f -mmin -60 2>/dev/null | head -10
find /var/log -type f -mmin -60 2>/dev/null | head -5

echo
echo "2. Fichiers avec permissions suspectes :"
echo " Fichiers SUID suspects :"
find /tmp /home -type f -perm -4000 2>/dev/null | head -5

echo " Fichiers world-writable :"
find /tmp -type f -perm -002 2>/dev/null | head -5

echo
echo "3. Gros fichiers récents :"
find / -type f -size +100M -mtime -1 2>/dev/null | head -5

echo
echo "4. Fichiers ouverts par processus suspects :"
echo " Fichiers ouverts en écriture :"
lsof +L1 2>/dev/null | head -5

echo "Mission : Identifier fichiers et accès suspects"
echo "Analyse : Fichiers récents + permissions anormales + gros fichiers"
echo

# PHASE 5 : Corrélation logs et timeline (10 minutes)
echo "PHASE 5 : ANALYSE TEMPORELLE"
echo "========================================="

echo "1. Erreurs système récentes :"
journalctl -p err --since "2 hours ago" --no-pager | tail -10

echo
echo "2. Authentifications suspectes :"
journalctl _SYSTEMD_UNIT=ssh.service --since "2 hours ago" --no-pager | grep -i "failed\|invalid" | tail -5
journalctl _SYSTEMD_UNIT=sshd.service --since "2 hours ago" --no-pager | grep -i "failed\|invalid" | tail -5

echo
echo "3. Timeline des événements critiques :"
echo " Démarrages de services (dernière heure) :"
journalctl --since "1 hour ago" --no-pager | grep -i "started\|stopped" | tail -10

echo
echo "4. Analyse des patterns :"
echo " Activité par heure :"
journalctl --since "6 hours ago" --no-pager | awk '{print $1" "$2" "$3}' | sort | uniq -c | tail -10

echo "Mission : Construire chronologie des événements"
echo "Analyse : Corrélation temporelle révèle causes et effets"
echo

# PHASE 6 : Rapport d'investigation (5 minutes)
echo "PHASE 6 : RAPPORT FORENSIQUE"
echo "========================================="

# Génération du rapport complet
REPORT_FILE="/tmp/forensic_report_$(date +%Y%m%d_%H%M%S).txt"
cat << EOF > "$REPORT_FILE"
╔══════════════════════════════════════════════════════════════╗
║ RAPPORT D'INVESTIGATION ║
║ ANALYSE FORENSIQUE ║
╚══════════════════════════════════════════════════════════════╝

Date d'investigation : $(date)
Système analysé : $(hostname)
Investigateur : DevOps Team
Durée d'analyse : 45 minutes

═══════════════════════════════════════════════════════════════
RÉSUMÉ EXÉCUTIF
═══════════════════════════════════════════════════════════════

État système : $(if [ $(cat /proc/loadavg | cut -d' ' -f1 | cut -d'.' -f1) -lt 2 ]; then echo "NORMAL"; else echo "SOUS CHARGE"; fi)
Sécurité : $(if [ $(ps aux | awk '$8 ~ /^Z/' | wc -l) -eq 0 ]; then echo "OK"; else echo "ATTENTION - Processus zombies"; fi)
Performance : $(if [ $(free | awk 'NR==2{printf "%.0f", $3*100/$2}') -lt 80 ]; then echo "ACCEPTABLE"; else echo "DÉGRADÉE"; fi)

═══════════════════════════════════════════════════════════════
INDICATEURS TECHNIQUES
═══════════════════════════════════════════════════════════════

CPU Load : $(cat /proc/loadavg | cut -d' ' -f1-3)
Mémoire : $(free -h | awk 'NR==2{print $3"/"$2}') utilisée
Processus : $(ps aux | wc -l) total
Connexions : $(netstat -tun 2>/dev/null | grep ESTABLISHED | wc -l || echo "N/A") établies

Top 3 CPU : $(ps aux --sort=-%cpu | awk 'NR<=4 && NR>1 {print $11}' | tr '\n' ' ')
Top 3 RAM : $(ps aux --sort=-%mem | awk 'NR<=4 && NR>1 {print $11}' | tr '\n' ' ')

═══════════════════════════════════════════════════════════════
RÉSULTATS D'INVESTIGATION
═══════════════════════════════════════════════════════════════

1. PROCESSUS SUSPECTS :
 $(if [ $(ps aux | awk '$1 != "root" && $7 == "?"' | wc -l) -gt 0 ]; then echo " Processus sans TTY détectés"; else echo " Aucun processus suspect"; fi)

2. ACTIVITÉ RÉSEAU :
 $(if [ $(netstat -tuln 2>/dev/null | awk '$4 ~ /:/ {split($4,a,":"); if(a[2] > 10000) print $0}' | wc -l || echo 0) -gt 0 ]; then echo " Ports non standard en écoute"; else echo " Activité réseau normale"; fi)

3. FICHIERS SYSTÈME :
 $(if [ $(find /tmp -type f -perm -4000 2>/dev/null | wc -l) -gt 0 ]; then echo " Fichiers SUID suspects trouvés"; else echo " Permissions fichiers normales"; fi)

4. LOGS SYSTÈME :
 $(if [ $(journalctl -p err --since "1 hour ago" --no-pager | wc -l) -gt 5 ]; then echo " Erreurs système fréquentes"; else echo " Logs système propres"; fi)

═══════════════════════════════════════════════════════════════
RECOMMANDATIONS
═══════════════════════════════════════════════════════════════

1. IMMÉDIAT :
 • Surveiller les processus à forte consommation
 • Vérifier les connexions réseau non autorisées
 • Contrôler l'espace disque

2. À COURT TERME :
 • Implémenter monitoring automatisé
 • Configurer alertes sur seuils critiques
 • Documenter baseline de performance

3. À LONG TERME :
 • Audit sécurité complet
 • Plan de monitoring proactif
 • Procédures d'incident

═══════════════════════════════════════════════════════════════
CONCLUSION
═══════════════════════════════════════════════════════════════

Le système présente $(if [ $(free | awk 'NR==2{printf "%.0f", $3*100/$2}') -lt 70 ] && [ $(cat /proc/loadavg | cut -d'.' -f1) -lt 2 ]; then echo "un état normal avec des performances acceptables."; else echo "des signes de stress nécessitant surveillance."; fi)

Niveau de risque : $(if [ $(ps aux | awk '$8 ~ /^Z/' | wc -l) -eq 0 ] && [ $(free | awk 'NR==2{printf "%.0f", $3*100/$2}') -lt 80 ]; then echo "FAIBLE"; else echo "MODÉRÉ"; fi)

Prochaine action recommandée : Monitoring continu pendant 24h

Rapport généré automatiquement par le système d'investigation forensique.
EOF

echo "Rapport forensique généré : $REPORT_FILE"
echo
echo "Aperçu du rapport :"
head -30 "$REPORT_FILE"
echo "..."
tail -10 "$REPORT_FILE"

echo
echo "=== SCRIPT D'INVESTIGATION AUTOMATISÉ ==="
cat << 'EOF' > forensic_toolkit.sh
#!/bin/bash
# Toolkit d'investigation forensique automatisé

echo " INVESTIGATION FORENSIQUE AUTOMATISÉE"
echo "========================================"

# Détection d'anomalies
detect_anomalies() {
 echo "Détection d'anomalies :"
 
 # Processus suspects
 SUSPECT_PROCS=$(ps aux | awk '$7 == "?" && $1 != "root"' | wc -l)
 echo " Processus sans TTY non-root : $SUSPECT_PROCS"
 
 # Charge système
 LOAD=$(cat /proc/loadavg | cut -d' ' -f1 | cut -d'.' -f1)
 echo " Load average : $LOAD (seuil alerte: 2)"
 
 # Mémoire
 MEM_USED=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
 echo " Utilisation mémoire : ${MEM_USED}% (seuil alerte: 80%)"
 
 # Connexions réseau
 CONNECTIONS=$(netstat -tun 2>/dev/null | grep ESTABLISHED | wc -l || echo "0")
 echo " Connexions actives : $CONNECTIONS"
}

# Analyse rapide
quick_scan() {
 echo " Scan rapide :"
 echo " Zombies : $(ps aux | awk '$8 ~ /^Z/' | wc -l)"
 echo " Erreurs récentes : $(journalctl -p err --since '1h ago' --no-pager | wc -l)"
 echo " Fichiers /tmp récents : $(find /tmp -type f -mmin -30 2>/dev/null | wc -l)"
}

detect_anomalies
echo
quick_scan

echo
echo "Investigation complète disponible dans le rapport détaillé."
EOF

chmod +x forensic_toolkit.sh
echo "Toolkit créé : forensic_toolkit.sh"
./forensic_toolkit.sh

echo
echo "=== RÉPONSES AUX DÉFIS ==="
echo "1. Processus le plus gourmand :"
ps aux --sort=-%cpu | awk 'NR==2{print $11 " (CPU: " $3 "%, MEM: " $4 "%)"}'

echo "2. Service suspect identifié :"
SUSPECT_COUNT=$(ps aux | awk '$7 == "?" && $1 != "root"' | wc -l)
if [ "$SUSPECT_COUNT" -gt 0 ]; then
 echo " $SUSPECT_COUNT processus sans TTY non-root détectés"
else
 echo " Aucun service suspect évident"
fi

echo "3. Problème de performance :"
PERF_ISSUE="AUCUN"
if [ $(cat /proc/loadavg | cut -d'.' -f1) -gt 2 ]; then
 PERF_ISSUE="CHARGE CPU ÉLEVÉE"
elif [ $(free | awk 'NR==2{printf "%.0f", $3*100/$2}') -gt 80 ]; then
 PERF_ISSUE="MÉMOIRE SATURÉE"
elif [ $(df / | awk 'NR==2{print $5}' | sed 's/%//') -gt 90 ]; then
 PERF_ISSUE="DISQUE PLEIN"
fi
echo " Problème détecté : $PERF_ISSUE"

echo "4. Action corrective :"
if [ "$PERF_ISSUE" != "AUCUN" ]; then
 echo " Action : Redémarrer services gourmands + monitoring"
else
 echo " Action : Surveillance préventive continue"
fi

echo "5. Plan de surveillance :"
echo " Monitoring CPU/MEM/DISK toutes les 5min"
echo " Alertes sur seuils : CPU>80%, MEM>80%, DISK>85%"
echo " Rapport hebdomadaire automatisé"

echo
echo "=== FIN CORRECTION LAB 4 CHALLENGE ==="
echo "Concepts maîtrisés : investigation forensique, diagnostic avancé, corrélation événements"
echo "Niveau atteint : Expert en analyse système et troubleshooting"

