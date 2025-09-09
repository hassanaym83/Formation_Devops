#!/bin/bash

# LAB 4 - Configuration environnement DevOps
# 
# Objectifs :
# - Créer un système de configuration d'environnement multi-projets
# - Implémenter des profils commutables (dev/staging/prod)
# - Développer des outils de validation et debugging
# 
# Points : 15/30
# 
# Durée estimée : 20 minutes

# Mission: Setup complet d'environnement de développement pour équipe DevOps
# Contexte: Configuration standardisée pour 3 environnements (dev, staging, prod)

echo "=== CONFIGURATION ENVIRONNEMENT DEVOPS ==="
echo "Setup multi-environnements: $(date)"
echo "Machine: $(hostname)"
echo "Utilisateur: $(whoami)"
echo

# Configuration des profils d'environnement
DEVOPS_HOME="$HOME/.devops"
PROFILES_DIR="$DEVOPS_HOME/profiles"
TOOLS_DIR="$DEVOPS_HOME/tools"

# TODO: 1. Initialiser la structure DevOps
echo "1. Initialisation structure DevOps..."
# Créer la structure:
# - $DEVOPS_HOME/profiles/{dev,staging,prod}
# - $DEVOPS_HOME/tools
# - $DEVOPS_HOME/logs
# - $DEVOPS_HOME/config

echo

# TODO: 2. Créer les profils d'environnement
echo "2. Création des profils d'environnement..."

# Profil DEVELOPMENT
# Créer $PROFILES_DIR/dev.env avec:
# export ENVIRONMENT="development"
# export DEBUG="true"
# export LOG_LEVEL="debug"
# export DB_HOST="localhost"
# export DB_PORT="5432"
# export DB_NAME="webapp_dev"
# export API_URL="http://localhost:3000"
# export NGINX_PORT="8080"
# export NODE_ENV="development"

# Profil STAGING
# Créer $PROFILES_DIR/staging.env avec:
# export ENVIRONMENT="staging"
# export DEBUG="false"
# export LOG_LEVEL="info"
# export DB_HOST="staging-db.company.com"
# export DB_PORT="5432"
# export DB_NAME="webapp_staging"
# export API_URL="https://api-staging.company.com"
# export NGINX_PORT="80"
# export NODE_ENV="staging"

# Profil PRODUCTION
# Créer $PROFILES_DIR/prod.env avec:
# export ENVIRONMENT="production"
# export DEBUG="false"
# export LOG_LEVEL="warn"
# export DB_HOST="prod-db.company.com"
# export DB_PORT="5432"
# export DB_NAME="webapp_prod"
# export API_URL="https://api.company.com"
# export NGINX_PORT="80"
# export NODE_ENV="production"

echo

# TODO: 3. Créer les outils de développement
echo "3. Configuration des outils DevOps..."

# Script de changement d'environnement
# Créer $TOOLS_DIR/switch-env.sh qui:
# - Charge le profil demandé
# - Sauvegarde l'environnement précédent
# - Valide la configuration
# - Affiche le résumé des changements

# Script de validation d'environnement
# Créer $TOOLS_DIR/validate-env.sh qui:
# - Vérifie toutes les variables requises
# - Teste les connexions (DB, API)
# - Valide les ports disponibles
# - Génère un rapport de santé

echo

# TODO: 4. Configurer les chemins et alias
echo "4. Configuration des chemins système..."

# Ajouter au PATH:
# - $DEVOPS_HOME/tools
# - $DEVOPS_HOME/bin
# - /usr/local/bin

# Créer des alias utiles:
# alias devenv="source $TOOLS_DIR/switch-env.sh dev"
# alias stagingenv="source $TOOLS_DIR/switch-env.sh staging"
# alias prodenv="source $TOOLS_DIR/switch-env.sh prod"
# alias checkenv="$TOOLS_DIR/validate-env.sh"

echo

# TODO: 5. Fonction de debugging d'environnement
echo "5. Outils de debugging..."

# Créer $TOOLS_DIR/debug-env.sh qui affiche:
# - Toutes les variables d'environnement actuelles
# - Variables manquantes par rapport au profil
# - Historique des changements d'environnement
# - Tests de connectivité

debug_environment() {
 echo "=== DEBUG ENVIRONNEMENT ==="
 echo "Profil actuel: ${ENVIRONMENT:-'NON DÉFINI'}"
 echo "Variables définies:"
 env | grep -E "(ENVIRONMENT|DEBUG|LOG_LEVEL|DB_|API_|NGINX_|NODE_)" | sort
 echo
 echo "Processus écoutant sur les ports:"
 # Afficher les ports en écoute (netstat ou ss)
 echo
}

echo

# TODO: 6. Système de logs d'environnement
echo "6. Configuration du logging..."

# Créer un système qui log:
# - Changements d'environnement avec timestamp
# - Erreurs de validation
# - Accès aux outils DevOps

log_env_change() {
 local old_env="${ENVIRONMENT:-'undefined'}"
 local new_env="$1"
 local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
 
 echo "[$timestamp] Environment changed: $old_env -> $new_env" >> "$DEVOPS_HOME/logs/env-changes.log"
}

echo

# TODO: 7. Tests d'intégration
echo "7. Tests de validation complète..."

# Tester chaque environnement:
# - Charger le profil
# - Valider toutes les variables
# - Tester les connexions simulées
# - Vérifier les outils disponibles

test_environment() {
 local env_name="$1"
 echo "Test environnement: $env_name"
 
 # Charger le profil de test
 # Valider les variables requises
 # Simuler les tests de connectivité
 # Rapporter les résultats
}

echo

# TODO: 8. Documentation et aide
echo "8. Génération de la documentation..."

# Créer un fichier d'aide README.md avec:
# - Description du système
# - Guide d'utilisation
# - Exemples de commandes
# - Troubleshooting

echo

echo "=== CONFIGURATION DEVOPS TERMINÉE ==="
echo "Utilisation:"
echo " source ~/.devops/tools/switch-env.sh [dev|staging|prod]"
echo " ~/.devops/tools/validate-env.sh"
echo " ~/.devops/tools/debug-env.sh"
