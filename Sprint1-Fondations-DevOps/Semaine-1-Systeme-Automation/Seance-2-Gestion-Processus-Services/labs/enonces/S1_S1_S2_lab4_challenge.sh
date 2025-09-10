#!/bin/bash

"""
LAB 4 - Challenge - Analyse forensique des logs

Objectifs :
- Maîtriser l'analyse forensique des logs pour la détection d'incidents
- Corréler les événements entre différents services
- Créer un rapport d'incident complet avec timeline

Points : 15/30

Durée estimée : 30-45 minutes (Hors séance - Bonus)
"""

echo "=== LAB 4 CHALLENGE - ANALYSE FORENSIQUE ==="
echo "Mission: Investigation post-incident serveur de production"
echo "Contexte: Suspicion d'intrusion - Analyse forensique complète"
echo "Statut: Challenge bonus hors séance"
echo

# PHASE 1 : Collecte d'informations (10 minutes)
echo "PHASE 1 : COLLECTE D'INFORMATIONS SYSTÈME"
echo "=========================================="
echo

echo "1.1 - Historique système"
echo "last | head -20"
echo "uptime"
echo "who -b"
echo "systemctl list-units --failed"
echo

echo "1.2 - État des ressources critiques"
echo "free -h"
echo "df -h"
echo "lscpu | grep -E '(Model name|CPU\\(s\\)|Thread)'"
echo "uname -a"
echo

echo "1.3 - Analyse réseau"
echo "ss -tulpn | grep :80"
echo "ss -tulpn | grep :443"
echo "netstat -i"
echo

# PHASE 2 : Analyse des processus (15 minutes)
echo "PHASE 2 : ANALYSE FORENSIQUE PROCESSUS"
echo "======================================"
echo

echo "2.1 - Top processus par ressources"
echo "ps aux --sort=-%cpu | head -15"
echo "ps aux --sort=-%mem | head -15"
echo "ps aux --sort=-etime | head -10"
echo

echo "2.2 - Processus anormaux"
echo "ps aux | awk '\$8 ~ /Z/ {print \"ZOMBIE: \" \$0}'"
echo "ps aux | awk '\$8 ~ /D/ {print \"UNINTERRUPTIBLE: \" \$0}'"
echo "ps aux | awk '\$8 ~ /T/ {print \"STOPPED: \" \$0}'"
echo

echo "2.3 - Hiérarchie processus suspecte"
echo "pstree -p | grep -E '(apache|nginx|httpd|php)'"
echo "ps -eo pid,ppid,cmd,etime | grep -E '(apache|nginx|httpd)'"
echo

# PHASE 3 : Investigation logs (15 minutes)
echo "PHASE 3 : INVESTIGATION LOGS SYSTÈME"
echo "===================================="
echo

echo "3.1 - Logs système critiques"
echo "journalctl --since '2 hours ago' --priority=err --no-pager"
echo "journalctl --since '2 hours ago' -u apache2 --no-pager | tail -20"
echo "journalctl --since '2 hours ago' -u nginx --no-pager | tail -20"
echo

echo "3.2 - Logs d'authentification"
echo "tail -50 /var/log/auth.log | grep -E '(Failed|Invalid|Accepted)'"
echo "lastlog | head -10"
echo

echo "3.3 - Logs applicatifs"
echo "tail -50 /var/log/apache2/error.log"
echo "tail -50 /var/log/nginx/error.log"
echo "tail -30 /var/log/syslog | grep -i error"
echo

# CHALLENGE FINAL
echo
echo "=== CHALLENGES À RÉSOUDRE ==="
echo "=============================="
echo

echo "CHALLENGE 1 : Root Cause Analysis"
echo "- Identifier le processus responsable de la surcharge"
echo "- Déterminer depuis quand le problème existe"
echo "- Analyser l'impact sur les autres services"
echo

echo "CHALLENGE 2 : Timeline Investigation"
echo "- Reconstituer la chronologie de l'incident"
echo "- Identifier les événements déclencheurs"
echo "- Corréler les logs système avec les métriques"
echo

echo "CHALLENGE 3 : Rapport d'incident"
echo "Créer un fichier 'incident_report.txt' contenant :"
echo "1. Résumé exécutif (2-3 lignes)"
echo "2. Timeline de l'incident"
echo "3. Processus identifiés comme problématiques"
echo "4. Ressources système impactées"
echo "5. Actions correctives recommandées"
echo

echo
echo "=== LIVRABLES ATTENDUS ==="
echo "=========================="
echo "1. incident_report.txt - Rapport complet d'analyse"
echo "2. forensic_commands.log - Capture des commandes exécutées"
echo "3. evidence.txt - Preuves collectées"
echo "4. recommendations.md - Actions préventives futures"

echo
echo "=== FIN LAB 4 CHALLENGE ==="
echo "Bon challenge ! Durée : 30-45 minutes"
echo "Points bonus si terminé avec succès"

