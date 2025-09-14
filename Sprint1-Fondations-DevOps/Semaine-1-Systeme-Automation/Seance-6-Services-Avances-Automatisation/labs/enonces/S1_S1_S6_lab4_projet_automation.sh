#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 4: Automatisation complète - Mini projet
# ==================================================================================

# Énoncé du LAB 4: Projet d'automatisation

echo "=== LAB 4: Automatisation complète - Mini projet ==="
echo

## Objectif
echo "OBJECTIF:"
echo "Créer un système d'automatisation complet combinant services et timers"
echo "Durée estimée: 45 minutes"
echo

## Contexte
echo "CONTEXTE:"
echo "Vous êtes responsable d'un serveur web. Vous devez automatiser:"
echo "- La sauvegarde quotidienne des fichiers importants"
echo "- Le monitoring des services critiques"
echo "- Le nettoyage automatique des logs"
echo "- La génération d'un rapport hebdomadaire"
echo

## Tâches à réaliser

echo "=== PARTIE 1: Setup initial (10 min) ==="
echo "1. Créer la structure des répertoires"
echo "2. Installer nginx comme service à surveiller"
echo "3. Préparer les fichiers de configuration"
echo

echo "=== PARTIE 2: Scripts d'automatisation (20 min) ==="
echo "1. Script de sauvegarde avec rotation"
echo "2. Script de vérification des services"
echo "3. Script de nettoyage des logs"
echo "4. Script de rapport hebdomadaire"
echo

echo "=== PARTIE 3: Configuration systemd (10 min) ==="
echo "1. Créer les services systemd"
echo "2. Créer les timers avec différentes fréquences"
echo "3. Activer tous les timers"
echo

echo "=== PARTIE 4: Tests et validation (5 min) ==="
echo "1. Tester chaque script individuellement"
echo "2. Vérifier les planifications"
echo "3. Simuler une panne de service"
echo

## Instructions détaillées

echo "=== INSTRUCTIONS DÉTAILLÉES ==="
echo

echo "Étape 1: Setup initial"
echo "sudo mkdir -p /opt/automation/{scripts,config,data,logs}"
echo "sudo mkdir -p /var/backups/automation"
echo "sudo apt update && sudo apt install -y nginx"
echo "sudo systemctl enable nginx && sudo systemctl start nginx"
echo

echo "Étape 2: Script de sauvegarde"
echo "sudo nano /opt/automation/scripts/backup.sh"
echo
echo "Contenu du script de sauvegarde:"
echo "#!/bin/bash"
echo "BACKUP_DIR=\"/var/backups/automation\""
echo "DATE=\$(date +%Y%m%d_%H%M%S)"
echo "LOG_FILE=\"/opt/automation/logs/backup_\$DATE.log\""
echo
echo "echo \"Début sauvegarde: \$(date)\" > \$LOG_FILE"
echo
echo "# Sauvegarder les fichiers critiques"
echo "tar -czf \"\$BACKUP_DIR/backup_\$DATE.tar.gz\" \\"
echo "    /etc/nginx/ \\"
echo "    /var/www/ \\"
echo "    /opt/automation/config/ 2>>\$LOG_FILE"
echo
echo "if [ \$? -eq 0 ]; then"
echo "    echo \"Sauvegarde réussie: backup_\$DATE.tar.gz\" >> \$LOG_FILE"
echo "else"
echo "    echo \"ERREUR: Échec de la sauvegarde\" >> \$LOG_FILE"
echo "fi"
echo
echo "# Nettoyer les sauvegardes de plus de 7 jours"
echo "find \$BACKUP_DIR -name \"backup_*.tar.gz\" -mtime +7 -delete"
echo "echo \"Fin sauvegarde: \$(date)\" >> \$LOG_FILE"
echo

echo "Étape 3: Script de vérification des services"
echo "sudo nano /opt/automation/scripts/check_services.sh"
echo
echo "Contenu du script de vérification:"
echo "#!/bin/bash"
echo "LOG_FILE=\"/opt/automation/logs/services_\$(date +%Y%m%d).log\""
echo "SERVICES=\"nginx ssh\""
echo
echo "echo \"\$(date): Vérification des services\" >> \$LOG_FILE"
echo
echo "for service in \$SERVICES; do"
echo "    if systemctl is-active --quiet \$service; then"
echo "        echo \"\$(date): \$service - OK\" >> \$LOG_FILE"
echo "    else"
echo "        echo \"\$(date): ALERTE - \$service est arrêté !\" >> \$LOG_FILE"
echo "        # Tentative de redémarrage"
echo "        systemctl start \$service"
echo "        if systemctl is-active --quiet \$service; then"
echo "            echo \"\$(date): \$service redémarré avec succès\" >> \$LOG_FILE"
echo "        else"
echo "            echo \"\$(date): ERREUR - Impossible de redémarrer \$service\" >> \$LOG_FILE"
echo "        fi"
echo "    fi"
echo "done"
echo

echo "Étape 4: Script de nettoyage"
echo "sudo nano /opt/automation/scripts/cleanup.sh"
echo
echo "Contenu du script de nettoyage:"
echo "#!/bin/bash"
echo "LOG_FILE=\"/opt/automation/logs/cleanup_\$(date +%Y%m%d).log\""
echo
echo "echo \"Début nettoyage: \$(date)\" > \$LOG_FILE"
echo
echo "# Nettoyer les logs d'automation anciens"
echo "find /opt/automation/logs -name \"*.log\" -mtime +14 -delete"
echo "LOGS_DELETED=\$?"
echo
echo "# Nettoyer les logs nginx anciens"
echo "find /var/log/nginx -name \"*.log.*.gz\" -mtime +30 -delete"
echo
echo "# Nettoyer les fichiers temporaires"
echo "find /tmp -name \"*.tmp\" -mtime +1 -delete"
echo
echo "echo \"Nettoyage terminé: \$(date) (code: \$LOGS_DELETED)\" >> \$LOG_FILE"
echo

echo "Étape 5: Script de rapport"
echo "sudo nano /opt/automation/scripts/weekly_report.sh"
echo
echo "Contenu du script de rapport:"
echo "#!/bin/bash"
echo "REPORT_FILE=\"/opt/automation/data/rapport_\$(date +%Y%m%d).txt\""
echo
echo "cat > \$REPORT_FILE << EOF"
echo "RAPPORT HEBDOMADAIRE - \$(date)"
echo "=================================="
echo
echo "SAUVEGARDES:"
echo "Total: \$(ls /var/backups/automation/*.tar.gz 2>/dev/null | wc -l)"
echo "Dernière: \$(ls -t /var/backups/automation/*.tar.gz 2>/dev/null | head -1 | xargs ls -lh 2>/dev/null)"
echo
echo "SERVICES:"
echo "Nginx: \$(systemctl is-active nginx)"
echo "SSH: \$(systemctl is-active ssh)"
echo
echo "ESPACE DISQUE:"
echo "\$(df -h / | tail -1)"
echo
echo "MÉMOIRE:"
echo "\$(free -h | grep Mem)"
echo
echo "ALERTES DE LA SEMAINE:"
echo "\$(grep \"ALERTE\" /opt/automation/logs/services_*.log 2>/dev/null | wc -l) alertes détectées"
echo
echo "EOF"
echo
echo "echo \"Rapport généré: \$REPORT_FILE\""
echo

echo "Étape 6: Rendre tous les scripts exécutables"
echo "sudo chmod +x /opt/automation/scripts/*.sh"
echo

echo "Étape 7: Créer les services systemd"
echo "# Service de sauvegarde"
echo "sudo tee /etc/systemd/system/auto-backup.service > /dev/null << EOF"
echo "[Unit]"
echo "Description=Sauvegarde automatique"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/automation/scripts/backup.sh"
echo "EOF"
echo

echo "# Service de vérification"
echo "sudo tee /etc/systemd/system/auto-check.service > /dev/null << EOF"
echo "[Unit]"
echo "Description=Vérification des services"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/automation/scripts/check_services.sh"
echo "EOF"
echo

echo "# Service de nettoyage"
echo "sudo tee /etc/systemd/system/auto-cleanup.service > /dev/null << EOF"
echo "[Unit]"
echo "Description=Nettoyage automatique"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/automation/scripts/cleanup.sh"
echo "EOF"
echo

echo "# Service de rapport"
echo "sudo tee /etc/systemd/system/auto-report.service > /dev/null << EOF"
echo "[Unit]"
echo "Description=Rapport hebdomadaire"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/automation/scripts/weekly_report.sh"
echo "EOF"
echo

echo "Étape 8: Créer les timers"
echo "# Timer sauvegarde (quotidien à 2h)"
echo "sudo tee /etc/systemd/system/auto-backup.timer > /dev/null << EOF"
echo "[Unit]"
echo "Description=Timer sauvegarde quotidienne"
echo
echo "[Timer]"
echo "OnCalendar=*-*-* 02:00:00"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo "EOF"
echo

echo "# Timer vérification (toutes les 10 minutes)"
echo "sudo tee /etc/systemd/system/auto-check.timer > /dev/null << EOF"
echo "[Unit]"
echo "Description=Timer vérification services"
echo
echo "[Timer]"
echo "OnCalendar=*:0/10"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo "EOF"
echo

echo "# Timer nettoyage (hebdomadaire dimanche 1h)"
echo "sudo tee /etc/systemd/system/auto-cleanup.timer > /dev/null << EOF"
echo "[Unit]"
echo "Description=Timer nettoyage hebdomadaire"
echo
echo "[Timer]"
echo "OnCalendar=Sun *-*-* 01:00:00"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo "EOF"
echo

echo "# Timer rapport (hebdomadaire lundi 9h)"
echo "sudo tee /etc/systemd/system/auto-report.timer > /dev/null << EOF"
echo "[Unit]"
echo "Description=Timer rapport hebdomadaire"
echo
echo "[Timer]"
echo "OnCalendar=Mon *-*-* 09:00:00"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo "EOF"
echo

echo "Étape 9: Activer tous les timers"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable --now auto-backup.timer"
echo "sudo systemctl enable --now auto-check.timer" 
echo "sudo systemctl enable --now auto-cleanup.timer"
echo "sudo systemctl enable --now auto-report.timer"
echo

## Critères de validation
echo "=== CRITÈRES DE VALIDATION ==="
echo "□ Tous les scripts s'exécutent sans erreur"
echo "□ Les 4 timers sont actifs et planifiés"
echo "□ Les sauvegardes sont créées dans /var/backups/automation"
echo "□ Les services sont surveillés automatiquement"
echo "□ Les logs sont générés correctement"
echo "□ Un rapport peut être généré"
echo

## Commandes de test
echo "=== COMMANDES DE TEST ==="
echo "# Tester tous les scripts"
echo "sudo /opt/automation/scripts/backup.sh"
echo "sudo /opt/automation/scripts/check_services.sh"
echo "sudo /opt/automation/scripts/cleanup.sh"
echo "sudo /opt/automation/scripts/weekly_report.sh"
echo
echo "# Voir tous les timers"
echo "sudo systemctl list-timers auto-*"
echo
echo "# Voir les logs récents"
echo "sudo ls -la /opt/automation/logs/"
echo "sudo ls -la /var/backups/automation/"
echo "sudo ls -la /opt/automation/data/"
echo
echo "# Tester une panne de service"
echo "sudo systemctl stop nginx"
echo "sleep 60"
echo "sudo tail /opt/automation/logs/services_\$(date +%Y%m%d).log"
echo

echo "=== TABLEAU DE BORD ==="
echo "# Créer un script de tableau de bord"
echo "sudo nano /opt/automation/scripts/dashboard.sh"
echo
echo "Contenu du dashboard:"
echo "#!/bin/bash"
echo "clear"
echo "echo \"=== TABLEAU DE BORD AUTOMATION ===\""
echo "echo \"Date: \$(date)\""
echo "echo"
echo "echo \"TIMERS:\""
echo "systemctl list-timers auto-* --no-pager"
echo "echo"
echo "echo \"SERVICES:\""
echo "echo \"Nginx: \$(systemctl is-active nginx)\""
echo "echo \"SSH: \$(systemctl is-active ssh)\""
echo "echo"
echo "echo \"DERNIERS LOGS:\""
echo "echo \"Sauvegarde: \$(ls -t /opt/automation/logs/backup_*.log 2>/dev/null | head -1 | xargs tail -1 2>/dev/null)\""
echo "echo \"Services: \$(tail -1 /opt/automation/logs/services_\$(date +%Y%m%d).log 2>/dev/null)\""
echo "echo"
echo "echo \"ESPACE DISQUE:\""
echo "df -h / | tail -1"
echo
echo "sudo chmod +x /opt/automation/scripts/dashboard.sh"
echo

echo "=== DÉPANNAGE ==="
echo "En cas de problème:"
echo "1. Vérifiez les permissions: ls -la /opt/automation/scripts/"
echo "2. Testez les scripts individuellement"
echo "3. Consultez les logs systemd: journalctl -u auto-backup.service"
echo "4. Vérifiez les timers: systemctl list-timers"
echo

echo "=== POUR ALLER PLUS LOIN (Optionnel) ==="
echo "1. Ajoutez des notifications email"
echo "2. Créez une interface web"
echo "3. Ajoutez la surveillance des métriques système"
echo "4. Implémentez une rotation avancée des sauvegardes"
echo "5. Créez des alertes Slack/Discord"
echo

echo "Bravo ! Ce mini-projet combine tous les concepts de la séance."
echo "Le script de correction est disponible si nécessaire."
