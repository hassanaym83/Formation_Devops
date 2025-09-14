#!/bin/bash

# LAB 3 - Sécurisation permissions - CORRECTION
# 
# Cette correction présente une sécurisation complète selon les bonnes pratiques DevOps.
# 
# Concepts démontrés :
# - Permissions appropriées par type de fichier
# - Principe du moindre privilège
# - Audit automatisé de sécurité
# - Vérification et validation
# 
# Bonnes pratiques appliquées :
# - Sécurité en profondeur
# - Automation des vérifications
# - Documentation des permissions
# - Reporting détaillé

# Mission: Durcissement sécuritaire serveur web selon bonnes pratiques
# Contexte: Mise en conformité avant production

echo "=== SÉCURISATION PERMISSIONS SERVEUR WEB ==="
echo "Audit sécurité: $(date)"
echo "Serveur: $(hostname)"
echo "Utilisateur: $(whoami)"
echo

# Configuration sécuritaire
WEB_ROOT="/tmp/webserver-security"
CONFIG_DIR="$WEB_ROOT/config"
LOGS_DIR="$WEB_ROOT/logs"
SECRETS_DIR="$WEB_ROOT/secrets"
PUBLIC_DIR="$WEB_ROOT/public"
SCRIPTS_DIR="$WEB_ROOT/scripts"

# Couleurs pour le retour visuel
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction utilitaire pour les messages
log_info() {
 echo -e "${GREEN}${NC} $1"
}

log_warning() {
 echo -e "${YELLOW}${NC} $1"
}

log_error() {
 echo -e "${RED}${NC} $1"
}

# Création de l'environnement de test sécurisé
echo "Initialisation environnement de test sécurisé..."
rm -rf "$WEB_ROOT" 2>/dev/null
mkdir -p "$WEB_ROOT"/{config,logs,secrets,public,scripts}
mkdir -p "$PUBLIC_DIR"/{css,js,images}

# Fichiers web publics
cat > "$PUBLIC_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Serveur Web Sécurisé</title></head>
<body>
 <h1>Environnement Web Sécurisé</h1>
 <p>Configuration selon bonnes pratiques DevOps</p>
</body>
</html>
EOF

echo "body { font-family: Arial; color: #333; }" > "$PUBLIC_DIR/css/style.css"
echo "console.log('Application sécurisée chargée');" > "$PUBLIC_DIR/js/app.js"

# Image de test
echo "Image placeholder" > "$PUBLIC_DIR/images/logo.png"

# Fichiers de configuration
cat > "$CONFIG_DIR/nginx.conf" << 'EOF'
server {
 listen 80;
 server_name localhost;
 root /var/www/html;
 
 # Sécurité headers
 add_header X-Frame-Options "SAMEORIGIN";
 add_header X-Content-Type-Options nosniff;
 add_header X-XSS-Protection "1; mode=block";
 
 # Configuration SSL (production)
 # ssl_protocols TLSv1.2 TLSv1.3;
 # ssl_ciphers HIGH:!aNULL:!MD5;
}
EOF

cat > "$CONFIG_DIR/apache.conf" << 'EOF'
<VirtualHost *:80>
 ServerName localhost
 DocumentRoot /var/www/html
 
 # Sécurité
 ServerTokens Prod
 ServerSignature Off
 
 # Headers de sécurité
 Header always set X-Frame-Options SAMEORIGIN
 Header always set X-Content-Type-Options nosniff
</VirtualHost>
EOF

# Fichiers secrets (Ã  sécuriser)
echo "database_password=SuperSecret123!" > "$SECRETS_DIR/db.conf"
echo "api_key=sk_live_abc123xyz789" > "$SECRETS_DIR/api.key"
echo "jwt_secret=UltraSecretJWTKey2024" > "$SECRETS_DIR/jwt.key"

cat > "$SECRETS_DIR/.env" << 'EOF'
# Variables d'environnement sensibles
DB_PASSWORD=ProductionPassword123
API_SECRET=prod_api_secret_key
ENCRYPTION_KEY=32_char_encryption_key_here
EOF

# Logs de test
echo "$(date) - Server started successfully" > "$LOGS_DIR/access.log"
echo "$(date) - Configuration loaded" > "$LOGS_DIR/error.log"
echo "$(date) - Application initialized" > "$LOGS_DIR/app.log"

# Scripts système
cat > "$SCRIPTS_DIR/backup.sh" << 'EOF'
#!/bin/bash
# Script de sauvegarde automatisé
echo "Backup started: $(date)"
tar -czf /backups/daily-$(date +%Y%m%d).tar.gz /var/www/
echo "Backup completed: $(date)"
EOF

cat > "$SCRIPTS_DIR/monitor.sh" << 'EOF'
#!/bin/bash
# Script de monitoring
ps aux | grep -E "(nginx|apache|mysql)" | grep -v grep
EOF

log_info "Environnement de test créé"
echo

# 1. Sécurisation des fichiers web publics
echo "1. Configuration permissions fichiers web publics..."

# Dossiers publics: 755 (rwxr-xr-x)
find "$PUBLIC_DIR" -type d -exec chmod 755 {} \;
log_info "Permissions dossiers publics: 755 (rwxr-xr-x)"

# Fichiers web: 644 (rw-r--r--)
find "$PUBLIC_DIR" -type f \( -name "*.html" -o -name "*.css" -o -name "*.js" \) -exec chmod 644 {} \;
log_info "Permissions fichiers web (HTML/CSS/JS): 644 (rw-r--r--)"

# Images et assets: 644
find "$PUBLIC_DIR" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.ico" \) -exec chmod 644 {} \;
log_info "Permissions images: 644 (rw-r--r--)"

echo

# 2. Sécurisation des configurations
echo "2. Sécurisation des fichiers de configuration..."

# Dossier config: 755
chmod 755 "$CONFIG_DIR"
log_info "Permissions dossier config: 755 (rwxr-xr-x)"

# Fichiers de configuration publique: 644
find "$CONFIG_DIR" -type f \( -name "*.conf" -o -name "*.cfg" \) -exec chmod 644 {} \;
log_info "Permissions fichiers config publique: 644 (rw-r--r--)"

echo

# 3. Sécurisation maximale des secrets
echo "3. Protection maximale des fichiers secrets..."

# Dossier secrets: 700 (rwx------)
chmod 700 "$SECRETS_DIR"
log_info "Permissions dossier secrets: 700 (rwx------)"

# Tous les fichiers secrets: 600 (rw-------)
find "$SECRETS_DIR" -type f -exec chmod 600 {} \;
log_info "Permissions fichiers secrets: 600 (rw-------)"

# Protection spéciale pour .env
if [ -f "$SECRETS_DIR/.env" ]; then
 chmod 600 "$SECRETS_DIR/.env"
 log_info "Fichier .env sécurisé: 600 (rw-------)"
fi

echo

# 4. Configuration des logs
echo "4. Configuration des permissions logs..."

# Dossier logs: 750 (rwxr-x---)
chmod 750 "$LOGS_DIR"
log_info "Permissions dossier logs: 750 (rwxr-x---)"

# Fichiers de logs: 660 (rw-rw----)
find "$LOGS_DIR" -type f -name "*.log" -exec chmod 660 {} \;
log_info "Permissions fichiers logs: 660 (rw-rw----)"

echo

# 5. Sécurisation des scripts
echo "5. Sécurisation des scripts système..."

# Dossier scripts: 755
chmod 755 "$SCRIPTS_DIR"
log_info "Permissions dossier scripts: 755 (rwxr-xr-x)"

# Scripts exécutables: 755
find "$SCRIPTS_DIR" -type f -name "*.sh" -exec chmod 755 {} \;
log_info "Permissions scripts shell: 755 (rwxr-xr-x)"

echo

# 6. Fonction de vérification automatisée
echo "6. Vérification automatisée des permissions..."

verify_permissions() {
 local file="$1"
 local expected="$2"
 local description="$3"
 
 if [ ! -e "$file" ]; then
 log_error "Fichier inexistant: $file"
 return 1
 fi
 
 local current=$(stat -c "%a" "$file" 2>/dev/null)
 
 if [ "$current" = "$expected" ]; then
 log_info "$description: $file ($current) "
 return 0
 else
 log_error "$description: $file - Attendu: $expected, Actuel: $current"
 return 1
 fi
}

echo "Vérification des permissions appliquées:"

# Vérifications par catégorie
echo
echo "✓ Fichiers web publics:"
verify_permissions "$PUBLIC_DIR" "755" "Dossier public"
verify_permissions "$PUBLIC_DIR/index.html" "644" "Page HTML"
verify_permissions "$PUBLIC_DIR/css/style.css" "644" "Feuille CSS"
verify_permissions "$PUBLIC_DIR/js/app.js" "644" "Script JS"

echo
echo "✓ Configuration:"
verify_permissions "$CONFIG_DIR" "755" "Dossier config"
verify_permissions "$CONFIG_DIR/nginx.conf" "644" "Config Nginx"
verify_permissions "$CONFIG_DIR/apache.conf" "644" "Config Apache"

echo
echo "✓ Fichiers secrets:"
verify_permissions "$SECRETS_DIR" "700" "Dossier secrets"
verify_permissions "$SECRETS_DIR/db.conf" "600" "Config DB"
verify_permissions "$SECRETS_DIR/api.key" "600" "Clé API"
verify_permissions "$SECRETS_DIR/.env" "600" "Fichier .env"

echo
echo "✓ Logs système:"
verify_permissions "$LOGS_DIR" "750" "Dossier logs"
verify_permissions "$LOGS_DIR/access.log" "660" "Log accès"
verify_permissions "$LOGS_DIR/error.log" "660" "Log erreurs"

echo
echo "✓ Scripts:"
verify_permissions "$SCRIPTS_DIR" "755" "Dossier scripts"
verify_permissions "$SCRIPTS_DIR/backup.sh" "755" "Script backup"
verify_permissions "$SCRIPTS_DIR/monitor.sh" "755" "Script monitoring"

echo

# 7. Audit de sécurité complet
echo "7. Rapport d'audit de sécurité détaillé:"

echo
echo " Analyse par type de fichier:"

# Compteur de sécurité
secure_files=0
total_files=0

# Analyse des fichiers publics
echo " Fichiers web publics:"
find "$PUBLIC_DIR" -type f | while read file; do
 perm=$(stat -c "%a" "$file")
 if [ "$perm" = "644" ]; then
 echo " ✓ $(basename "$file") ($perm)"
 else
 echo " ⚠ $(basename "$file") ($perm) - Révision recommandée"
 fi
done

# Analyse des secrets
echo "Fichiers secrets:"
find "$SECRETS_DIR" -type f | while read file; do
 perm=$(stat -c "%a" "$file")
 if [ "$perm" = "600" ]; then
 echo " ✓ $(basename "$file") ($perm) - Sécurisé"
 else
 echo " $(basename "$file") ($perm) - RISQUE DE SÉCURITÉ"
 fi
done

echo
echo " Vérifications avancées:"

# Vérification des fichiers avec permissions trop permissives
echo "⚠ Fichiers avec permissions potentiellement dangereuses:"
find "$WEB_ROOT" -type f \( -perm -002 -o -perm -020 \) 2>/dev/null | while read file; do
 perm=$(stat -c "%a" "$file")
 log_warning "Permissions ouvertes: $(basename "$file") ($perm)"
done

# Vérification des fichiers exécutables
echo " Fichiers exécutables détectés:"
find "$WEB_ROOT" -type f -executable | while read file; do
 perm=$(stat -c "%a" "$file")
 if [[ "$file" == *.sh ]]; then
 log_info "Script shell: $(basename "$file") ($perm)"
 else
 log_warning "Exécutable inattendu: $(basename "$file") ($perm)"
 fi
done

echo
echo " Recommandations de sécurité:"
echo " 1. Vérifier régulièrement les permissions avec ce script"
echo " 2. Utiliser des groupes appropriés pour les accès partagés"
echo " 3. Implémenter une surveillance des modifications de permissions"
echo " 4. Configurer SELinux/AppArmor pour une sécurité renforcée"
echo " 5. Auditer les accès aux fichiers sensibles"

echo
echo " Commandes de maintenance:"
echo " # Restaurer les permissions par défaut:"
echo " find $PUBLIC_DIR -type f -exec chmod 644 {} \\;"
echo " find $SECRETS_DIR -type f -exec chmod 600 {} \\;"
echo " find $LOGS_DIR -type f -exec chmod 660 {} \\;"
echo
echo " # Vérification rapide des permissions critiques:"
echo " find $SECRETS_DIR -type f ! -perm 600 -ls"

echo
echo "=== AUDIT SÉCURITAIRE TERMINÉ ==="
echo "Configuration sécurisée selon les bonnes pratiques DevOps"
echo "Dernière vérification: $(date)"
echo "Environnement: $(basename "$WEB_ROOT")"

# Génération d'un rapport final
{
 echo "RAPPORT DE SÉCURITÉ - $(date)"
 echo "=========================="
 echo "Serveur: $(hostname)"
 echo "Chemin: $WEB_ROOT"
 echo
 echo "RÉSUMÉ DES PERMISSIONS:"
 echo "- Fichiers publics (web): 644"
 echo "- Dossiers publics: 755"
 echo "- Fichiers secrets: 600"
 echo "- Dossier secrets: 700"
 echo "- Fichiers logs: 660"
 echo "- Scripts: 755"
 echo
 echo "AUDIT TERMINÉ: $(date)"
} > "$WEB_ROOT/security-report-$(date +%Y%m%d).txt"

log_info "Rapport de sécurité généré: security-report-$(date +%Y%m%d).txt"
