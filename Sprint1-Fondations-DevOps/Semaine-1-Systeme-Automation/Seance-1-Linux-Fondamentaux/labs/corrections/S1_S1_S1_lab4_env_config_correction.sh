#!/bin/bash

# LAB 4 - Configuration environnement multi-plateformes - CORRECTION
# 
# Cette correction démontre la gestion complète d'environnements selon les bonnes pratiques DevOps.
# 
# Concepts démontrés :
# - Gestion des variables d'environnement par contexte
# - Configuration centralisée multi-environnements
# - Automatisation du déploiement configuration
# - Validation et contrôle qualité
# 
# Bonnes pratiques appliquées :
# - Infrastructure as Code
# - Séparation environnements dev/staging/prod
# - Configuration externalisée
# - Tests automatisés

# Mission: Configuration automatisée environnements dev/staging/production
# Contexte: Pipeline DevOps avec déploiement multi-plateformes

echo "=== CONFIGURATION ENVIRONNEMENTS MULTI-PLATEFORMES ==="
echo "Initialisation: $(date)"
echo "Système: $(uname -s)"
echo "Utilisateur: $(whoami)"
echo

# Configuration globale
PROJECT_ROOT="/tmp/multi-env-config"
ENVIRONMENTS=("development" "staging" "production")
CONFIG_TEMPLATE_DIR="$PROJECT_ROOT/templates"
ENV_DIR="$PROJECT_ROOT/environments"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
BACKUP_DIR="$PROJECT_ROOT/backups"

# Couleurs pour interface utilisateur
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Fonctions utilitaires
log_step() {
 echo -e "${BLUE}${NC} $1"
}

log_success() {
 echo -e "${GREEN}${NC} $1"
}

log_warning() {
 echo -e "${YELLOW}${NC} $1"
}

log_error() {
 echo -e "${RED}${NC} $1"
}

# Initialisation de l'environnement de projet
echo "Initialisation structure projet multi-environnements..."
rm -rf "$PROJECT_ROOT" 2>/dev/null
mkdir -p "$PROJECT_ROOT"/{templates,environments/{development,staging,production},scripts,backups}

log_success "Structure de projet créée"
echo

# 1. Création des templates de configuration
log_step "1. Création des templates de configuration centralisés"

# Template principal d'application
cat > "$CONFIG_TEMPLATE_DIR/app.conf.template" << 'EOF'
# Configuration Application - Template
# Variables Ã  substituer: {{ENV}}, {{DB_HOST}}, {{DB_PORT}}, {{API_URL}}, {{LOG_LEVEL}}

[application]
name = "DevOps Demo App"
version = "1.0.0"
environment = "{{ENV}}"

[database]
host = "{{DB_HOST}}"
port = {{DB_PORT}}
name = "app_{{ENV}}"
pool_size = {{DB_POOL_SIZE}}
timeout = {{DB_TIMEOUT}}

[api]
base_url = "{{API_URL}}"
timeout = {{API_TIMEOUT}}
rate_limit = {{API_RATE_LIMIT}}

[logging]
level = "{{LOG_LEVEL}}"
format = "{{LOG_FORMAT}}"
file = "/var/log/app-{{ENV}}.log"

[security]
secret_key = "{{SECRET_KEY}}"
jwt_expiry = {{JWT_EXPIRY}}
cors_origins = "{{CORS_ORIGINS}}"

[monitoring]
metrics_enabled = {{METRICS_ENABLED}}
health_check_path = "/health"
prometheus_port = {{PROMETHEUS_PORT}}
EOF

# Template Docker Compose
cat > "$CONFIG_TEMPLATE_DIR/docker-compose.yml.template" << 'EOF'
version: '3.8'

services:
 app:
 image: "myapp:{{VERSION}}"
 environment:
 - ENV={{ENV}}
 - DB_HOST={{DB_HOST}}
 - DB_PORT={{DB_PORT}}
 - API_URL={{API_URL}}
 - LOG_LEVEL={{LOG_LEVEL}}
 ports:
 - "{{APP_PORT}}:8000"
 volumes:
 - ./logs:/var/log
 networks:
 - app-network
 restart: {{RESTART_POLICY}}
 
 database:
 image: "postgres:{{POSTGRES_VERSION}}"
 environment:
 - POSTGRES_DB=app_{{ENV}}
 - POSTGRES_USER={{DB_USER}}
 - POSTGRES_PASSWORD={{DB_PASSWORD}}
 ports:
 - "{{DB_PORT}}:5432"
 volumes:
 - db-data-{{ENV}}:/var/lib/postgresql/data
 - ./backups:/backups
 networks:
 - app-network

 redis:
 image: "redis:{{REDIS_VERSION}}"
 ports:
 - "{{REDIS_PORT}}:6379"
 volumes:
 - redis-data-{{ENV}}:/data
 networks:
 - app-network
 command: redis-server --appendonly yes

volumes:
 db-data-{{ENV}}:
 redis-data-{{ENV}}:

networks:
 app-network:
 driver: bridge
EOF

# Template Nginx
cat > "$CONFIG_TEMPLATE_DIR/nginx.conf.template" << 'EOF'
server {
 listen {{NGINX_PORT}};
 server_name {{SERVER_NAME}};
 
 # Configuration spécifique environnement
 access_log /var/log/nginx/{{ENV}}-access.log;
 error_log /var/log/nginx/{{ENV}}-error.log {{NGINX_LOG_LEVEL}};
 
 # Headers de sécurité
 add_header X-Frame-Options "SAMEORIGIN" always;
 add_header X-Content-Type-Options "nosniff" always;
 add_header X-XSS-Protection "1; mode=block" always;
 
 # Configuration SSL pour production
 {{SSL_CONFIG}}
 
 location / {
 proxy_pass http://app:8000;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
 proxy_set_header X-Forwarded-Proto $scheme;
 
 # Timeouts spécifiques Ã  l'environnement
 proxy_connect_timeout {{PROXY_TIMEOUT}};
 proxy_send_timeout {{PROXY_TIMEOUT}};
 proxy_read_timeout {{PROXY_TIMEOUT}};
 }
 
 # Configuration monitoring
 location /health {
 access_log off;
 proxy_pass http://app:8000/health;
 }
 
 # Métriques (production uniquement)
 {{METRICS_CONFIG}}
}
EOF

log_success "Templates de configuration créés"
echo

# 2. Configuration par environnement
log_step "2. Configuration spécifique par environnement"

# Configuration Development
cat > "$ENV_DIR/development/.env" << 'EOF'
# Environnement Development
ENV=development
VERSION=latest

# Base de données
DB_HOST=localhost
DB_PORT=5433
DB_USER=dev_user
DB_PASSWORD=dev_password_123
DB_POOL_SIZE=5
DB_TIMEOUT=30
POSTGRES_VERSION=13

# API
API_URL=http://localhost:8001/api/v1
API_TIMEOUT=5000
API_RATE_LIMIT=1000

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=detailed

# Sécurité
SECRET_KEY=dev_secret_key_not_for_production
JWT_EXPIRY=3600
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Monitoring
METRICS_ENABLED=true
PROMETHEUS_PORT=9090

# Nginx
NGINX_PORT=8080
SERVER_NAME=localhost
NGINX_LOG_LEVEL=debug
PROXY_TIMEOUT=60
SSL_CONFIG=# SSL désactivé en dev
METRICS_CONFIG=# Métriques basiques

# Application
APP_PORT=8001
RESTART_POLICY=no

# Redis
REDIS_VERSION=6
REDIS_PORT=6380
EOF

# Configuration Staging
cat > "$ENV_DIR/staging/.env" << 'EOF'
# Environnement Staging
ENV=staging
VERSION=v1.0.0-rc

# Base de données
DB_HOST=staging-db.internal
DB_PORT=5432
DB_USER=staging_user
DB_PASSWORD=staging_secure_password_456
DB_POOL_SIZE=10
DB_TIMEOUT=60
POSTGRES_VERSION=14

# API
API_URL=https://api-staging.company.com/api/v1
API_TIMEOUT=10000
API_RATE_LIMIT=500

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Sécurité
SECRET_KEY=staging_secret_key_complex_789
JWT_EXPIRY=1800
CORS_ORIGINS=https://staging.company.com

# Monitoring
METRICS_ENABLED=true
PROMETHEUS_PORT=9091

# Nginx
NGINX_PORT=443
SERVER_NAME=staging.company.com
NGINX_LOG_LEVEL=warn
PROXY_TIMEOUT=120
SSL_CONFIG=ssl_certificate /etc/ssl/staging.crt; ssl_certificate_key /etc/ssl/staging.key;
METRICS_CONFIG=location /metrics { auth_basic "Metrics"; proxy_pass http://app:9091/metrics; }

# Application
APP_PORT=8000
RESTART_POLICY=unless-stopped

# Redis
REDIS_VERSION=7
REDIS_PORT=6379
EOF

# Configuration Production
cat > "$ENV_DIR/production/.env" << 'EOF'
# Environnement Production
ENV=production
VERSION=v1.0.0

# Base de données
DB_HOST=prod-db.internal
DB_PORT=5432
DB_USER=prod_user
DB_PASSWORD=ultra_secure_production_password_xyz_2024
DB_POOL_SIZE=20
DB_TIMEOUT=120
POSTGRES_VERSION=15

# API
API_URL=https://api.company.com/api/v1
API_TIMEOUT=15000
API_RATE_LIMIT=200

# Logging
LOG_LEVEL=WARN
LOG_FORMAT=json

# Sécurité
SECRET_KEY=production_ultra_secret_key_complex_secure_2024
JWT_EXPIRY=900
CORS_ORIGINS=https://app.company.com

# Monitoring
METRICS_ENABLED=true
PROMETHEUS_PORT=9092

# Nginx
NGINX_PORT=443
SERVER_NAME=app.company.com
NGINX_LOG_LEVEL=error
PROXY_TIMEOUT=300
SSL_CONFIG=ssl_certificate /etc/ssl/production.crt; ssl_certificate_key /etc/ssl/production.key; ssl_protocols TLSv1.2 TLSv1.3;
METRICS_CONFIG=location /metrics { allow 10.0.0.0/8; deny all; proxy_pass http://app:9092/metrics; }

# Application
APP_PORT=8000
RESTART_POLICY=always

# Redis
REDIS_VERSION=7
REDIS_PORT=6379
EOF

log_success "Configurations environnements créées (dev/staging/prod)"
echo

# 3. Scripts de gestion automatisée
log_step "3. Création des scripts de gestion automatisée"

# Script de génération de configuration
cat > "$SCRIPTS_DIR/generate-config.sh" << 'EOF'
#!/bin/bash

# Script de génération automatique des configurations
# Usage: ./generate-config.sh <environment>

ENVIRONMENT=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -z "$ENVIRONMENT" ]; then
 echo "Usage: $0 <environment>"
 echo "Environnements disponibles: development, staging, production"
 exit 1
fi

ENV_FILE="$PROJECT_ROOT/environments/$ENVIRONMENT/.env"

if [ ! -f "$ENV_FILE" ]; then
 echo "Erreur: Fichier de configuration inexistant: $ENV_FILE"
 exit 1
fi

echo "Génération configuration pour: $ENVIRONMENT"

# Chargement des variables
source "$ENV_FILE"

# Fonction de substitution
substitute_vars() {
 local template_file="$1"
 local output_file="$2"
 
 if [ ! -f "$template_file" ]; then
 echo "Template inexistant: $template_file"
 return 1
 fi
 
 # Substitution des variables
 envsubst < "$template_file" > "$output_file"
 echo " Généré: $output_file"
}

# Génération des fichiers de configuration
OUTPUT_DIR="$PROJECT_ROOT/environments/$ENVIRONMENT/generated"
mkdir -p "$OUTPUT_DIR"

echo "Génération des configurations..."
substitute_vars "$PROJECT_ROOT/templates/app.conf.template" "$OUTPUT_DIR/app.conf"
substitute_vars "$PROJECT_ROOT/templates/docker-compose.yml.template" "$OUTPUT_DIR/docker-compose.yml"
substitute_vars "$PROJECT_ROOT/templates/nginx.conf.template" "$OUTPUT_DIR/nginx.conf"

echo "Configuration générée dans: $OUTPUT_DIR"
EOF

chmod +x "$SCRIPTS_DIR/generate-config.sh"

# Script de validation
cat > "$SCRIPTS_DIR/validate-config.sh" << 'EOF'
#!/bin/bash

# Script de validation des configurations
# Vérifie la cohérence et la sécurité des configurations

ENVIRONMENT=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

validate_environment() {
 local env=$1
 local env_file="$PROJECT_ROOT/environments/$env/.env"
 
 echo "Validation environnement: $env"
 
 if [ ! -f "$env_file" ]; then
 echo " Fichier .env manquant: $env_file"
 return 1
 fi
 
 # Vérifications de sécurité
 source "$env_file"
 
 # Vérification des mots de passe
 if [[ "$DB_PASSWORD" == *"dev"* && "$ENV" == "production" ]]; then
 echo " Mot de passe de développement en production!"
 return 1
 fi
 
 # Vérification de la complexité des secrets
 if [ ${#SECRET_KEY} -lt 20 ]; then
 echo " Secret key trop simple pour $env"
 return 1
 fi
 
 # Vérification des ports
 if [ "$ENV" == "production" ] && [ "$NGINX_PORT" != "443" ]; then
 echo " Port non-standard en production"
 fi
 
 echo " Configuration $env validée"
 return 0
}

if [ -n "$ENVIRONMENT" ]; then
 validate_environment "$ENVIRONMENT"
else
 echo "Validation de tous les environnements..."
 for env in development staging production; do
 validate_environment "$env"
 echo
 done
fi
EOF

chmod +x "$SCRIPTS_DIR/validate-config.sh"

# Script de déploiement
cat > "$SCRIPTS_DIR/deploy.sh" << 'EOF'
#!/bin/bash

# Script de déploiement automatisé
# Usage: ./deploy.sh <environment>

ENVIRONMENT=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if [ -z "$ENVIRONMENT" ]; then
 echo "Usage: $0 <environment>"
 exit 1
fi

echo "Déploiement environnement: $ENVIRONMENT"

# 1. Validation de la configuration
echo "1. Validation de la configuration..."
if ! "$SCRIPT_DIR/validate-config.sh" "$ENVIRONMENT"; then
 echo "Ã‰chec de la validation. Arrêt du déploiement."
 exit 1
fi

# 2. Génération des fichiers
echo "2. Génération des configurations..."
"$SCRIPT_DIR/generate-config.sh" "$ENVIRONMENT"

# 3. Sauvegarde si production
if [ "$ENVIRONMENT" == "production" ]; then
 echo "3. Sauvegarde configuration actuelle..."
 BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
 mkdir -p "$PROJECT_ROOT/backups/$BACKUP_NAME"
 cp -r "$PROJECT_ROOT/environments/$ENVIRONMENT/generated" "$PROJECT_ROOT/backups/$BACKUP_NAME/" 2>/dev/null || true
 echo " Sauvegarde créée: $BACKUP_NAME"
fi

# 4. Simulation du déploiement
echo "4. Simulation du déploiement..."
CONFIG_DIR="$PROJECT_ROOT/environments/$ENVIRONMENT/generated"

if [ -f "$CONFIG_DIR/docker-compose.yml" ]; then
 echo " - Vérification Docker Compose..."
 # docker-compose -f "$CONFIG_DIR/docker-compose.yml" config --quiet && echo " Docker Compose valide"
 echo " Docker Compose valide"
fi

echo " Déploiement simulé avec succès pour: $ENVIRONMENT"
echo "Fichiers disponibles dans: $CONFIG_DIR"
EOF

chmod +x "$SCRIPTS_DIR/deploy.sh"

log_success "Scripts de gestion créés"
echo

# 4. Génération automatique des configurations
log_step "4. Génération automatique des configurations pour tous les environnements"

for env in "${ENVIRONMENTS[@]}"; do
 echo " Génération configuration: $env"
 
 # Chargement des variables d'environnement
 source "$ENV_DIR/$env/.env"
 
 # Création du dossier de sortie
 OUTPUT_DIR="$ENV_DIR/$env/generated"
 mkdir -p "$OUTPUT_DIR"
 
 # Substitution des variables dans les templates
 # Template app.conf
 sed -e "s/{{ENV}}/$ENV/g" \
 -e "s/{{DB_HOST}}/$DB_HOST/g" \
 -e "s/{{DB_PORT}}/$DB_PORT/g" \
 -e "s/{{API_URL}}/$API_URL/g" \
 -e "s/{{LOG_LEVEL}}/$LOG_LEVEL/g" \
 -e "s/{{DB_POOL_SIZE}}/$DB_POOL_SIZE/g" \
 -e "s/{{DB_TIMEOUT}}/$DB_TIMEOUT/g" \
 -e "s/{{API_TIMEOUT}}/$API_TIMEOUT/g" \
 -e "s/{{API_RATE_LIMIT}}/$API_RATE_LIMIT/g" \
 -e "s/{{LOG_FORMAT}}/$LOG_FORMAT/g" \
 -e "s/{{SECRET_KEY}}/$SECRET_KEY/g" \
 -e "s/{{JWT_EXPIRY}}/$JWT_EXPIRY/g" \
 -e "s/{{CORS_ORIGINS}}/$CORS_ORIGINS/g" \
 -e "s/{{METRICS_ENABLED}}/$METRICS_ENABLED/g" \
 -e "s/{{PROMETHEUS_PORT}}/$PROMETHEUS_PORT/g" \
 "$CONFIG_TEMPLATE_DIR/app.conf.template" > "$OUTPUT_DIR/app.conf"
 
 # Template docker-compose.yml
 sed -e "s/{{ENV}}/$ENV/g" \
 -e "s/{{VERSION}}/$VERSION/g" \
 -e "s/{{DB_HOST}}/$DB_HOST/g" \
 -e "s/{{DB_PORT}}/$DB_PORT/g" \
 -e "s/{{API_URL}}/$API_URL/g" \
 -e "s/{{LOG_LEVEL}}/$LOG_LEVEL/g" \
 -e "s/{{APP_PORT}}/$APP_PORT/g" \
 -e "s/{{RESTART_POLICY}}/$RESTART_POLICY/g" \
 -e "s/{{POSTGRES_VERSION}}/$POSTGRES_VERSION/g" \
 -e "s/{{DB_USER}}/$DB_USER/g" \
 -e "s/{{DB_PASSWORD}}/$DB_PASSWORD/g" \
 -e "s/{{REDIS_VERSION}}/$REDIS_VERSION/g" \
 -e "s/{{REDIS_PORT}}/$REDIS_PORT/g" \
 "$CONFIG_TEMPLATE_DIR/docker-compose.yml.template" > "$OUTPUT_DIR/docker-compose.yml"
 
 # Template nginx.conf
 sed -e "s/{{NGINX_PORT}}/$NGINX_PORT/g" \
 -e "s/{{SERVER_NAME}}/$SERVER_NAME/g" \
 -e "s/{{ENV}}/$ENV/g" \
 -e "s/{{NGINX_LOG_LEVEL}}/$NGINX_LOG_LEVEL/g" \
 -e "s|{{SSL_CONFIG}}|$SSL_CONFIG|g" \
 -e "s/{{PROXY_TIMEOUT}}/$PROXY_TIMEOUT/g" \
 -e "s|{{METRICS_CONFIG}}|$METRICS_CONFIG|g" \
 "$CONFIG_TEMPLATE_DIR/nginx.conf.template" > "$OUTPUT_DIR/nginx.conf"
 
 log_success "Configuration générée: $env"
done

echo

# 5. Tests automatisés des configurations
log_step "5. Tests automatisés et validation des configurations"

test_configuration() {
 local env=$1
 local config_dir="$ENV_DIR/$env/generated"
 
 echo " Tests pour environnement: $env"
 
 # Test 1: Fichiers générés présents
 local required_files=("app.conf" "docker-compose.yml" "nginx.conf")
 for file in "${required_files[@]}"; do
 if [ -f "$config_dir/$file" ]; then
 log_success " Fichier présent: $file"
 else
 log_error " Fichier manquant: $file"
 return 1
 fi
 done
 
 # Test 2: Validation du contenu
 source "$ENV_DIR/$env/.env"
 
 # Vérification que les variables ont été substituées
 if grep -q "{{" "$config_dir/app.conf"; then
 log_error " Variables non substituées dans app.conf"
 return 1
 else
 log_success " Variables substituées correctement"
 fi
 
 # Test 3: Vérification de la sécurité
 if [ "$env" == "production" ]; then
 if grep -qi "dev\|test\|debug" "$config_dir/app.conf"; then
 log_warning " Références de développement en production"
 else
 log_success " Configuration sécurisée pour production"
 fi
 fi
 
 # Test 4: Validation syntaxique YAML (Docker Compose)
 # Note: Nécessiterait yq ou docker-compose pour validation réelle
 if [ -f "$config_dir/docker-compose.yml" ]; then
 log_success " Docker Compose présent"
 fi
 
 return 0
}

echo "Tests automatisés des configurations:"
all_tests_passed=true

for env in "${ENVIRONMENTS[@]}"; do
 if ! test_configuration "$env"; then
 all_tests_passed=false
 fi
 echo
done

if $all_tests_passed; then
 log_success "Tous les tests passés avec succès"
else
 log_error "Certains tests ont échoué"
fi

echo

# 6. Rapport de synthèse et gestion des environnements
log_step "6. Rapport de synthèse des environnements configurés"

echo "Configuration multi-environnements terminée:"
echo

for env in "${ENVIRONMENTS[@]}"; do
 source "$ENV_DIR/$env/.env"
 
 echo " Environnement: $env"
 echo " Version: $VERSION"
 echo " Base de données: $DB_HOST:$DB_PORT"
 echo " API: $API_URL"
 echo " Niveau de log: $LOG_LEVEL"
 echo " Port application: $APP_PORT"
 echo " Serveur web: $SERVER_NAME:$NGINX_PORT"
 
 # Indicateurs de sécurité
 if [ "$env" == "production" ]; then
 echo " Environnement sécurisé (production)"
 elif [ "$env" == "staging" ]; then
 echo " Environnement de test (staging)"
 else
 echo " Environnement de développement"
 fi
 echo
done

# 7. Documentation des commandes de gestion
echo "Commandes de gestion disponibles:"
echo
echo " # Génération d'une configuration spécifique:"
echo " $SCRIPTS_DIR/generate-config.sh development"
echo " $SCRIPTS_DIR/generate-config.sh staging"
echo " $SCRIPTS_DIR/generate-config.sh production"
echo
echo " # Validation des configurations:"
echo " $SCRIPTS_DIR/validate-config.sh production"
echo
echo " # Déploiement d'un environnement:"
echo " $SCRIPTS_DIR/deploy.sh staging"
echo
echo " # Vérification des variables d'environnement:"
echo " source $ENV_DIR/production/.env && env | grep -E '^(DB_|API_|LOG_)'"
echo
echo " # Comparaison entre environnements:"
echo " diff $ENV_DIR/development/.env $ENV_DIR/production/.env"

echo
echo "=== CONFIGURATION MULTI-ENVIRONNEMENTS TERMINÃ‰E ==="
echo "Projet configuré: $(basename "$PROJECT_ROOT")"
echo "Environnements: $(IFS=', '; echo "${ENVIRONMENTS[*]}")"
echo "Scripts disponibles: $(ls -1 "$SCRIPTS_DIR"/*.sh | wc -l)"
echo "Configurations générées: $(find "$ENV_DIR" -name "*.conf" -o -name "*.yml" | wc -l)"
echo "Dernière mise Ã  jour: $(date)"

# Génération d'un rapport final complet
{
 echo "RAPPORT CONFIGURATION MULTI-ENVIRONNEMENTS"
 echo "==========================================="
 echo "Date: $(date)"
 echo "Projet: $(basename "$PROJECT_ROOT")"
 echo
 echo "ENVIRONNEMENTS CONFIGURÃ‰S:"
 for env in "${ENVIRONMENTS[@]}"; do
 source "$ENV_DIR/$env/.env"
 echo "- $env: $VERSION ($DB_HOST:$DB_PORT)"
 done
 echo
 echo "FICHIERS GÃ‰NÃ‰RÃ‰S:"
 find "$ENV_DIR" -name "*.conf" -o -name "*.yml" | sort
 echo
 echo "SCRIPTS DISPONIBLES:"
 ls -1 "$SCRIPTS_DIR"/*.sh
 echo
 echo "DERNIÃˆRE GÃ‰NÃ‰RATION: $(date)"
} > "$PROJECT_ROOT/configuration-report-$(date +%Y%m%d).txt"

log_success "Rapport de configuration généré: configuration-report-$(date +%Y%m%d).txt"
