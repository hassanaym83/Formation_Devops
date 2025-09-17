#!/bin/bash

# S1_S2_S1_LAB4 - Challenge : Script d'administration système complet
# DURÉE : 30-45 minutes (Challenge hors séance)
# NIVEAU : Défi d'approfondissement

# OBJECTIF :
# Créez un script d'administration système avancé qui combine tous les concepts vus en séance
# pour créer un outil de maintenance et de diagnostic complet.

# CONTEXTE :
# Challenge optionnel d'approfondissement - Script de maintenance préventive pour serveurs DevOps

# CONSIGNES :
# 1. Collectez des informations système complètes
# 2. Vérifiez l'espace disque et alertez si critique
# 3. Testez plusieurs services critiques  
# 4. Créez une sauvegarde automatique horodatée
# 5. Générez un rapport de santé système formaté
# 6. Gérez les paramètres en ligne de commande

# CRITÈRES D'ÉVALUATION :
# □ 5 informations système collectées
# □ Vérification espace disque avec seuil d'alerte
# □ Test d'au moins 3 services système
# □ Sauvegarde automatique fonctionnelle
# □ Rapport formaté et structuré
# □ Gestion des paramètres du script
# □ Gestion d'erreurs robuste

# RÉSULTAT ATTENDU :
# Un script professionnel d'administration qui peut être utilisé quotidiennement
# pour la maintenance préventive d'un serveur de production

# ====== TEMPLATE DE DÉPART ======

#!/bin/bash

# TODO: Ajoutez des variables de configuration globales
# BACKUP_DIR, LOG_FILE, DISK_THRESHOLD, SERVICES_TO_CHECK

echo "=========================================="
echo "    SCRIPT DE MAINTENANCE SYSTÈME"
echo "    Date: $(date)"
echo "=========================================="

# TODO: Section 1 - Collecte d'informations système
echo ""
echo "1. INFORMATIONS SYSTÈME"
echo "----------------------"

# TODO: Collectez et affichez :
# - Version du système (uname -a)
# - Uptime du système
# - Charge système (load average)
# - Mémoire disponible
# - Nombre de processus actifs

# TODO: Section 2 - Vérification espace disque
echo ""
echo "2. ESPACE DISQUE"
echo "----------------"

# TODO: Vérifiez l'espace disque sur /
# - Affichez l'utilisation actuelle
# - Si > 80% : affichez une ALERTE
# - Si > 95% : affichez un WARNING critique

# TODO: Section 3 - Vérification des services
echo ""
echo "3. SERVICES SYSTÈME"
echo "-------------------"

# TODO: Créez un tableau de services critiques
# services=("sshd" "cron" "systemd-networkd")

# TODO: Pour chaque service :
# - Testez s'il est actif
# - Affichez le statut (ACTIF/INACTIF)
# - Comptez les services inactifs

# TODO: Section 4 - Sauvegarde automatique  
echo ""
echo "4. SAUVEGARDE SYSTÈME"
echo "---------------------"

# TODO: Créez une sauvegarde horodatée
# - Répertoire : /backup/maintenance_$(date +%Y%m%d_%H%M%S)
# - Sauvegardez /etc/hostname, /etc/hosts, /etc/passwd
# - Utilisez tar pour créer l'archive
# - Affichez la taille de l'archive créée

# TODO: Section 5 - Rapport final
echo ""
echo "5. RAPPORT DE SANTÉ"
echo "-------------------"

# TODO: Générez un rapport de synthèse :
# - État global du système (OK/ATTENTION/CRITIQUE)
# - Nombre de services vérifiés/actifs
# - Espace disque utilisé
# - Sauvegarde créée
# - Recommandations d'actions

echo ""
echo "=========================================="
echo "    MAINTENANCE TERMINÉE"
echo "=========================================="

# ====== FONCTIONNALITÉS AVANCÉES (BONUS) ======

# TODO: Gestion des paramètres
# if [[ "$1" == "--help" ]]; then
#     echo "Usage: $0 [--help] [--backup-only] [--check-only]"
#     exit 0
# fi

# TODO: Mode backup uniquement
# if [[ "$1" == "--backup-only" ]]; then
#     # Exécuter seulement la section sauvegarde
# fi

# TODO: Mode vérification uniquement  
# if [[ "$1" == "--check-only" ]]; then
#     # Exécuter seulement les vérifications (pas de sauvegarde)
# fi

# ====== AIDE ET ASTUCES ======

# Commandes utiles :
# df -h /                              # Espace disque
# free -h                              # Mémoire
# uptime                               # Charge système
# ps aux | wc -l                       # Nombre de processus
# systemctl is-active service          # Test service
# du -sh /path                         # Taille d'un répertoire
# mkdir -p /path                       # Créer répertoire récursivement

# Calculs bash :
# usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
# if [[ $usage -gt 80 ]]; then echo "ALERTE"; fi

# Horodatage :
# timestamp=$(date +%Y%m%d_%H%M%S)

# ====== TESTS À EFFECTUER ======
# 1. ./script.sh                       # Exécution complète
# 2. ./script.sh --help               # Affichage aide  
# 3. ./script.sh --backup-only        # Sauvegarde seulement
# 4. ./script.sh --check-only         # Vérifications seulement
# 5. Vérifiez que les fichiers de sauvegarde sont créés
# 6. Testez sur un système avec peu d'espace disque

# OBJECTIFS D'APPRENTISSAGE :
# - Intégration de tous les concepts Bash de base
# - Scripts d'administration système réalistes  
# - Gestion robuste des erreurs
# - Code maintenable et documenté
# - Fonctionnalités avancées optionnelles