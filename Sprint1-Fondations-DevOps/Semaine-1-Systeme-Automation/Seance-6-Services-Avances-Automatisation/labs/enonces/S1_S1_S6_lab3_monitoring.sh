#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 3: Monitoring système de base
# ==================================================================================

# Énoncé du LAB 3: Monitoring système

echo "=== LAB 3: Monitoring système de base ==="
echo

## Objectif
echo "OBJECTIF:"
echo "Créer un script de surveillance système et le configurer en service"
echo "Durée estimée: 30 minutes"
echo

## Contexte
echo "CONTEXTE:"
echo "Vous devez créer un système de monitoring basique qui surveille"
echo "l'usage du CPU, de la mémoire et de l'espace disque"
echo

## Tâches à réaliser

echo "=== PARTIE 1: Création du script de monitoring (15 min) ==="
echo "1. Créer un script qui collecte les métriques système"
echo "2. Définir des seuils d'alerte"
echo "3. Écrire les résultats dans un fichier de log"
echo

echo "=== PARTIE 2: Configuration du service (10 min) ==="
echo "1. Créer un service systemd pour le monitoring"
echo "2. Créer un timer pour exécuter toutes les 2 minutes"
echo "3. Activer le service automatique"
echo

echo "=== PARTIE 3: Tests et vérifications (5 min) ==="
echo "1. Vérifier que les métriques sont collectées"
echo "2. Tester les alertes avec une charge artificielle"
echo "3. Consulter les logs de monitoring"
echo

## Instructions détaillées

echo "=== INSTRUCTIONS DÉTAILLÉES ==="
echo

echo "Étape 1: Créer le script de monitoring"
echo "sudo mkdir -p /opt/monitoring"
echo "sudo nano /opt/monitoring/check_system.sh"
echo
echo "Contenu du script (copiez ce code):"
echo "#!/bin/bash"
echo "LOG_FILE=\"/var/log/system-monitoring.log\""
echo "DATE=\$(date '+%Y-%m-%d %H:%M:%S')"
echo
echo "# Seuils d'alerte"
echo "CPU_LIMITE=80"
echo "MEMOIRE_LIMITE=85"
echo "DISQUE_LIMITE=90"
echo
echo "# Collecte des métriques"
echo "CPU_USAGE=\$(top -bn1 | grep \"Cpu(s)\" | awk '{print \$2}' | cut -d'%' -f1)"
echo "MEMOIRE_USAGE=\$(free | grep Mem | awk '{printf \"%.0f\", \$3/\$2 * 100.0}')"
echo "DISQUE_USAGE=\$(df / | tail -1 | awk '{print \$5}' | cut -d'%' -f1)"
echo
echo "# Écrire les métriques dans le log"
echo "echo \"\$DATE - CPU: \${CPU_USAGE}% | Mémoire: \${MEMOIRE_USAGE}% | Disque: \${DISQUE_USAGE}%\" >> \$LOG_FILE"
echo
echo "# Vérifier les seuils et alertes"
echo "if [ \$(echo \"\$CPU_USAGE > \$CPU_LIMITE\" | bc -l) -eq 1 ]; then"
echo "    echo \"\$DATE - ALERTE: CPU élevé (\${CPU_USAGE}%)\" >> \$LOG_FILE"
echo "fi"
echo
echo "if [ \$MEMOIRE_USAGE -gt \$MEMOIRE_LIMITE ]; then"
echo "    echo \"\$DATE - ALERTE: Mémoire élevée (\${MEMOIRE_USAGE}%)\" >> \$LOG_FILE"
echo "fi"
echo
echo "if [ \$DISQUE_USAGE -gt \$DISQUE_LIMITE ]; then"
echo "    echo \"\$DATE - ALERTE: Disque plein (\${DISQUE_USAGE}%)\" >> \$LOG_FILE"
echo "fi"
echo
echo "Rendre le script exécutable:"
echo "sudo chmod +x /opt/monitoring/check_system.sh"
echo

echo "Étape 2: Installer bc pour les calculs"
echo "sudo apt update && sudo apt install -y bc"
echo

echo "Étape 3: Tester le script manuellement"
echo "sudo /opt/monitoring/check_system.sh"
echo "sudo tail -3 /var/log/system-monitoring.log"
echo

echo "Étape 4: Créer le service systemd"
echo "sudo nano /etc/systemd/system/system-monitoring.service"
echo
echo "Contenu du service:"
echo "[Unit]"
echo "Description=Monitoring système"
echo "After=network.target"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/monitoring/check_system.sh"
echo "User=root"
echo

echo "Étape 5: Créer le timer"
echo "sudo nano /etc/systemd/system/system-monitoring.timer"
echo
echo "Contenu du timer:"
echo "[Unit]"
echo "Description=Timer pour monitoring système"
echo "Requires=system-monitoring.service"
echo
echo "[Timer]"
echo "OnCalendar=*:*:0/120"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo

echo "Étape 6: Activer le monitoring"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable system-monitoring.timer"
echo "sudo systemctl start system-monitoring.timer"
echo

## Critères de validation
echo "=== CRITÈRES DE VALIDATION ==="
echo "□ Le script collecte les métriques CPU, mémoire et disque"
echo "□ Les métriques sont sauvées dans /var/log/system-monitoring.log"
echo "□ Le timer s'exécute toutes les 2 minutes"
echo "□ Les alertes fonctionnent avec les seuils définis"
echo "□ Le service peut être démarré manuellement"
echo

## Commandes de test
echo "=== COMMANDES DE TEST ==="
echo "# Voir le statut du timer"
echo "sudo systemctl status system-monitoring.timer"
echo
echo "# Exécuter une collecte manuelle"
echo "sudo systemctl start system-monitoring.service"
echo
echo "# Voir les dernières métriques"
echo "sudo tail -10 /var/log/system-monitoring.log"
echo
echo "# Voir les logs système du service"
echo "sudo journalctl -u system-monitoring.service -f"
echo
echo "# Lister les prochaines exécutions"
echo "sudo systemctl list-timers system-monitoring*"
echo

echo "=== TEST DE CHARGE (Pour déclencher une alerte CPU) ==="
echo "# Générer une charge CPU temporaire"
echo "timeout 30s yes > /dev/null &"
echo "# Attendre et vérifier les alertes"
echo "sleep 35"
echo "sudo grep \"ALERTE.*CPU\" /var/log/system-monitoring.log"
echo

echo "=== VISUALISATION DES DONNÉES ==="
echo "# Voir l'évolution des métriques"
echo "sudo grep \$(date '+%Y-%m-%d') /var/log/system-monitoring.log"
echo
echo "# Compter les alertes du jour"
echo "sudo grep \"ALERTE\" /var/log/system-monitoring.log | grep \$(date '+%Y-%m-%d') | wc -l"
echo

echo "=== DÉPANNAGE ==="
echo "En cas de problème:"
echo "1. Vérifiez que bc est installé: which bc"
echo "2. Testez le script: /opt/monitoring/check_system.sh"
echo "3. Vérifiez les permissions: ls -la /opt/monitoring/"
echo "4. Consultez les logs: journalctl -u system-monitoring.service"
echo

echo "=== POUR ALLER PLUS LOIN (Optionnel) ==="
echo "1. Ajoutez la surveillance du load average"
echo "2. Créez des seuils différents selon l'heure"
echo "3. Ajoutez l'envoi d'emails pour les alertes critiques"
echo "4. Créez un dashboard pour visualiser les métriques"
echo

echo "Bonne chance ! Le script de correction est disponible si nécessaire."
