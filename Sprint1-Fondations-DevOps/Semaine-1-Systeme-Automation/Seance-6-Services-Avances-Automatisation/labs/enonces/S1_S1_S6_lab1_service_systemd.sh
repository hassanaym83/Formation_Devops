#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 1: Création et gestion de services systemd 
# ==================================================================================

# Énoncé du LAB 1: Services systemd de base

echo "=== LAB 1: Création et gestion de services systemd ==="
echo

## Objectif
echo "OBJECTIF:"
echo "Apprendre à créer et gérer des services systemd de base"
echo "Durée estimée: 20 minutes"
echo

## Contexte
echo "CONTEXTE:"
echo "Vous devez créer un service systemd qui démarre automatiquement"
echo "et qui peut être contrôlé avec systemctl"
echo

## Tâches à réaliser

echo "=== PARTIE 1: Création d'un script de service (5 min) ==="
echo "1. Créer un répertoire /opt/monservice"
echo "2. Créer un script de service qui écrit dans un fichier de log"
echo "3. Rendre le script exécutable"
echo

echo "=== PARTIE 2: Création du service systemd (10 min) ==="
echo "1. Créer un fichier service dans /etc/systemd/system/"
echo "2. Configurer les sections [Unit], [Service], et [Install]"
echo "3. Recharger systemd"
echo

echo "=== PARTIE 3: Tests et validation (5 min) ==="
echo "1. Démarrer le service"
echo "2. Vérifier le statut"
echo "3. Activer le démarrage automatique"
echo "4. Tester l'arrêt et le redémarrage"
echo

## Instructions détaillées

echo "=== INSTRUCTIONS DÉTAILLÉES ==="
echo

echo "Étape 1: Créer le script de service"
echo "sudo mkdir -p /opt/monservice"
echo "sudo nano /opt/monservice/service.sh"
echo
echo "Contenu du script (copiez ce code):"
echo "#!/bin/bash"
echo "LOG_FILE=\"/var/log/monservice.log\""
echo "while true; do"
echo "    echo \"\$(date): Service en fonctionnement\" >> \$LOG_FILE"
echo "    sleep 10"
echo "done"
echo
echo "Rendre le script exécutable:"
echo "sudo chmod +x /opt/monservice/service.sh"
echo

echo "Étape 2: Créer le fichier service systemd"
echo "sudo nano /etc/systemd/system/monservice.service"
echo
echo "Contenu du fichier service (copiez ce code):"
echo "[Unit]"
echo "Description=Mon Premier Service"
echo "After=network.target"
echo
echo "[Service]"
echo "Type=simple"
echo "ExecStart=/opt/monservice/service.sh"
echo "Restart=always"
echo "User=root"
echo
echo "[Install]"
echo "WantedBy=multi-user.target"
echo

echo "Étape 3: Recharger systemd"
echo "sudo systemctl daemon-reload"
echo

echo "Étape 4: Gérer le service"
echo "# Démarrer le service"
echo "sudo systemctl start monservice"
echo
echo "# Vérifier le statut"
echo "sudo systemctl status monservice"
echo
echo "# Activer au démarrage"
echo "sudo systemctl enable monservice"
echo
echo "# Voir les logs"
echo "tail -f /var/log/monservice.log"
echo

## Critères de validation
echo "=== CRITÈRES DE VALIDATION ==="
echo "□ Le service démarre sans erreur"
echo "□ Le statut indique 'active (running)'"
echo "□ Le fichier de log se remplit automatiquement"
echo "□ Le service redémarre automatiquement après un 'kill'"
echo "□ Le service est activé pour le démarrage automatique"
echo

## Commandes de test
echo "=== COMMANDES DE TEST ==="
echo "# Tester si le service fonctionne"
echo "sudo systemctl is-active monservice"
echo
echo "# Tester si le service est activé"
echo "sudo systemctl is-enabled monservice"
echo
echo "# Voir les dernières lignes du log"
echo "sudo tail -5 /var/log/monservice.log"
echo
echo "# Redémarrer le service"
echo "sudo systemctl restart monservice"
echo

echo "=== DÉPANNAGE ==="
echo "En cas de problème:"
echo "1. Vérifiez les logs: journalctl -u monservice -f"
echo "2. Vérifiez la syntaxe du fichier service"
echo "3. Assurez-vous que le script est exécutable"
echo "4. Rechargez systemd après chaque modification"
echo

echo "=== POUR ALLER PLUS LOIN (Optionnel) ==="
echo "1. Modifiez le script pour qu'il affiche aussi l'usage CPU"
echo "2. Ajoutez une option de configuration dans /etc/"
echo "3. Créez un script d'arrêt propre avec ExecStop"
echo

echo "Bonne chance ! Le script de correction est disponible si nécessaire."
