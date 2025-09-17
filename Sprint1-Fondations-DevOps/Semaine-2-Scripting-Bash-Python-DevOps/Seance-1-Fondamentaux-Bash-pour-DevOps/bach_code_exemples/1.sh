#!/bin/bash
# Script de démonstration des variables d'environnement

# Variables d'environnement courantes : disponibles dans tout le système
echo "Variables système importantes:"

# $USER : nom de l'utilisateur connecté (prédéfinie par le système)
echo "Utilisateur actuel: $USER"

# $HOME : chemin vers le répertoire personnel de l'utilisateur
echo "Répertoire personnel: $HOME"

# $PWD : répertoire de travail actuel (Print Working Directory)
echo "Répertoire de travail: $PWD"

# $PATH : liste des répertoires où chercher les commandes exécutables
echo "Chemin des commandes: $PATH"

# Définir des variables d'environnement personnalisées pour DevOps
# export : rend la variable accessible aux processus enfants

# Variable d'environnement pour l'environnement de déploiement
export DEPLOY_ENV="production"

# Variable d'environnement pour l'URL de l'API
export API_URL="https://api.monapp.com"

# Variable d'environnement pour le serveur de base de données
export DB_HOST="db-prod.internal"

echo "Variables DevOps personnalisées:"
echo "Environnement de déploiement: $DEPLOY_ENV"
echo "URL de l'API: $API_URL"
echo "Serveur de base de données: $DB_HOST"


public int add(int a, int b) {
    return a + b;
}

add(2, 5)