#!/bin/bash

# LAB 1 - Gestion fichiers DevOps
# 
# Objectifs :
# - Créer une structure de projet web organisée
# - Automatiser la gestion des fichiers de configuration
# - Implémenter un système de sauvegarde
# 
# Points : 5/30
# 
# Durée estimée : 20 minutes

# Mission: Setup automatisé d'un projet web avec Nginx et PHP
# Contexte: Initialisation d'environnement de développement pour équipe

echo "=== SETUP PROJET WEB DEVOPS ==="
echo "Initialisation projet: webapp-devops"
echo "Date: $(date)"
echo "Exécuté par: $(whoami)"
echo

# Configuration du projet
PROJECT_NAME="webapp-devops"
BASE_DIR="/tmp/projet-web" # Utilisation de /tmp pour les tests
WEB_DIR="$BASE_DIR/$PROJECT_NAME"
CONFIG_DIR="$BASE_DIR/config"
LOG_DIR="$BASE_DIR/logs"
BACKUP_DIR="$BASE_DIR/backups"

# TODO: 1. Créer l'arborescence du projet
echo "1. Création de l'arborescence projet..."
# Créer la structure complète:
# - $WEB_DIR/public (fichiers web publics)
# - $WEB_DIR/src (code source)
# - $CONFIG_DIR/nginx (config nginx)
# - $CONFIG_DIR/php (config php)
# - $LOG_DIR/nginx (logs nginx)
# - $LOG_DIR/app (logs application)
# - $BACKUP_DIR

echo

# TODO: 2. Créer des templates de configuration
echo "2. Génération des templates de configuration..."

# Template Nginx basique
# Créer $CONFIG_DIR/nginx/default.conf avec:
# server {
# listen 80;
# server_name localhost;
# root /var/www/webapp-devops/public;
# index index.php index.html;
# }

# Template PHP
# Créer $CONFIG_DIR/php/php.ini avec configuration basique

echo

# TODO: 3. Créer des fichiers web de test
echo "3. Création des fichiers web de test..."
# - index.html dans public/
# - app.php dans src/
# - style.css dans public/css/

echo

# TODO: 4. Organiser les logs par date
echo "4. Organisation des logs..."
# Créer des fichiers de logs avec timestamp
# - access.log et error.log pour nginx
# - application.log pour l'app

echo

# TODO: 5. Script de sauvegarde
echo "5. Création du script de sauvegarde..."
# Créer un script backup.sh qui archive:
# - Les fichiers de configuration
# - Le code source
# - Les logs récents

echo

# TODO: 6. Affichage du résultat
echo "6. Vérification de la structure créée:"
# Utiliser tree ou ls -la pour afficher l'arborescence complète

echo "=== SETUP TERMINÉ ==="
