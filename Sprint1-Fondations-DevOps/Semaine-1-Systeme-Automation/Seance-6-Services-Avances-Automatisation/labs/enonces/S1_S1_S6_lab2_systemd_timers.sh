#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 2: Planification de tâches avec systemd timers
# ==================================================================================

# Énoncé du LAB 2: Systemd Timers

echo "=== LAB 2: Planification de tâches avec systemd timers ==="
echo

## Objectif
echo "OBJECTIF:"
echo "Apprendre à créer des tâches automatisées avec systemd timers"
echo "Durée estimée: 25 minutes"
echo

## Contexte
echo "CONTEXTE:"
echo "Vous devez automatiser une tâche qui s'exécute périodiquement"
echo "pour nettoyer des fichiers temporaires"
echo

## Tâches à réaliser

echo "=== PARTIE 1: Création du script de nettoyage (8 min) ==="
echo "1. Créer un script qui supprime les fichiers anciens"
echo "2. Tester le script manuellement"
echo "3. Ajouter des logs pour tracer l'exécution"
echo

echo "=== PARTIE 2: Création du service systemd (10 min) ==="
echo "1. Créer un service oneshot pour le script"
echo "2. Créer un timer pour planifier l'exécution"
echo "3. Configurer la fréquence d'exécution"
echo

echo "=== PARTIE 3: Tests et validation (7 min) ==="
echo "1. Activer et démarrer le timer"
echo "2. Vérifier les prochaines exécutions"
echo "3. Tester une exécution manuelle"
echo "4. Vérifier les logs"
echo

## Instructions détaillées

echo "=== INSTRUCTIONS DÉTAILLÉES ==="
echo

echo "Étape 1: Créer le script de nettoyage"
echo "sudo mkdir -p /opt/nettoyage"
echo "sudo nano /opt/nettoyage/nettoyage.sh"
echo
echo "Contenu du script (copiez ce code):"
echo "#!/bin/bash"
echo "LOG_FILE=\"/var/log/nettoyage.log\""
echo "echo \"\$(date): Début du nettoyage\" >> \$LOG_FILE"
echo
echo "# Supprimer les fichiers .tmp plus anciens que 7 jours"
echo "find /tmp -name \"*.tmp\" -mtime +7 -type f -delete 2>/dev/null"
echo "FICHIERS_SUPPRIMES=\$?"
echo
echo "# Supprimer les fichiers de log plus anciens que 30 jours"
echo "find /var/log -name \"*.log.old\" -mtime +30 -type f -delete 2>/dev/null"
echo
echo "echo \"\$(date): Nettoyage terminé (code: \$FICHIERS_SUPPRIMES)\" >> \$LOG_FILE"
echo
echo "Rendre le script exécutable:"
echo "sudo chmod +x /opt/nettoyage/nettoyage.sh"
echo

echo "Étape 2: Tester le script"
echo "sudo /opt/nettoyage/nettoyage.sh"
echo "sudo cat /var/log/nettoyage.log"
echo

echo "Étape 3: Créer le service systemd"
echo "sudo nano /etc/systemd/system/nettoyage.service"
echo
echo "Contenu du fichier service:"
echo "[Unit]"
echo "Description=Nettoyage automatique des fichiers temporaires"
echo "After=network.target"
echo
echo "[Service]"
echo "Type=oneshot"
echo "ExecStart=/opt/nettoyage/nettoyage.sh"
echo "User=root"
echo

echo "Étape 4: Créer le timer systemd"
echo "sudo nano /etc/systemd/system/nettoyage.timer"
echo
echo "Contenu du fichier timer:"
echo "[Unit]"
echo "Description=Timer pour nettoyage quotidien"
echo "Requires=nettoyage.service"
echo
echo "[Timer]"
echo "OnCalendar=daily"
echo "Persistent=true"
echo
echo "[Install]"
echo "WantedBy=timers.target"
echo

echo "Étape 5: Activer et démarrer le timer"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable nettoyage.timer"
echo "sudo systemctl start nettoyage.timer"
echo

echo "Étape 6: Vérifier le timer"
echo "sudo systemctl status nettoyage.timer"
echo "sudo systemctl list-timers nettoyage*"
echo

## Critères de validation
echo "=== CRITÈRES DE VALIDATION ==="
echo "□ Le script s'exécute sans erreur"
echo "□ Le timer est actif et programmé"
echo "□ Les logs de nettoyage sont créés"
echo "□ Le service peut être lancé manuellement"
echo "□ La prochaine exécution est visible avec list-timers"
echo

## Commandes de test
echo "=== COMMANDES DE TEST ==="
echo "# Exécuter manuellement le service"
echo "sudo systemctl start nettoyage.service"
echo
echo "# Voir le statut du timer"
echo "sudo systemctl status nettoyage.timer"
echo
echo "# Voir les prochaines exécutions"
echo "sudo systemctl list-timers"
echo
echo "# Voir les logs du service"
echo "sudo journalctl -u nettoyage.service"
echo
echo "# Voir les logs de nettoyage"
echo "sudo tail /var/log/nettoyage.log"
echo

echo "=== PLANIFICATIONS ALTERNATIVES ==="
echo "Pour changer la fréquence, modifiez OnCalendar= dans le timer:"
echo "OnCalendar=*:0/30        # Toutes les 30 minutes"
echo "OnCalendar=Mon *-*-* 09:00:00    # Tous les lundis à 9h"
echo "OnCalendar=*-*-01 02:00:00       # Le 1er de chaque mois à 2h"
echo

echo "=== DÉPANNAGE ==="
echo "En cas de problème:"
echo "1. Vérifiez les logs: journalctl -u nettoyage.service -f"
echo "2. Testez le script manuellement: /opt/nettoyage/nettoyage.sh"
echo "3. Vérifiez la syntaxe du timer: systemd-analyze verify nettoyage.timer"
echo "4. Rechargez après modification: systemctl daemon-reload"
echo

echo "=== POUR ALLER PLUS LOIN (Optionnel) ==="
echo "1. Ajoutez un compteur de fichiers supprimés"
echo "2. Envoyez un email de rapport"
echo "3. Créez plusieurs scripts avec des fréquences différentes"
echo "4. Ajoutez la randomisation avec RandomizedDelaySec="
echo

echo "Bonne chance ! Le script de correction est disponible si nécessaire."
