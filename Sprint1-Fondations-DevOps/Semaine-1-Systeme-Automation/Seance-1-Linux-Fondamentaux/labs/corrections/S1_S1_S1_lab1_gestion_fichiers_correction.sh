#!/bin/bash

# LAB 1 - Gestion fichiers DevOps - CORRECTION 
# 
# Cette correction présente un setup automatisé complet pour projet web.
# 
# Concepts démontrés :
# - Structure de projet organisée
# - Templates de configuration
# - Gestion automatisée des fichiers
# - Système de sauvegarde
# 
# Bonnes pratiques appliquées :
# - Vérification d'erreurs
# - Organisation modulaire
# - Documentation des actions
# - Automation complète

# Mission: Setup automatisé projet web avec Nginx et PHP
# Contexte: Environnement de développement standardisé

echo "=== SETUP PROJET WEB DEVOPS ==="
echo "Initialisation projet: webapp-devops"
echo "Date: $(date)"
echo "Exécuté par: $(whoami)"
echo

# Configuration du projet
PROJECT_NAME="webapp-devops"
BASE_DIR="/tmp/projet-web"
WEB_DIR="$BASE_DIR/$PROJECT_NAME"
CONFIG_DIR="$BASE_DIR/config"
LOG_DIR="$BASE_DIR/logs"
BACKUP_DIR="$BASE_DIR/backups"

# Fonction utilitaire pour créer des dossiers
create_directory() {
 local dir="$1"
 if mkdir -p "$dir" 2>/dev/null; then
 echo " Créé: $dir"
 else
 echo " Erreur création: $dir"
 return 1
 fi
}

# 1. Création de l'arborescence complète
echo "1. Création de l'arborescence projet..."

# Structure principale
create_directory "$WEB_DIR/public"
create_directory "$WEB_DIR/public/css"
create_directory "$WEB_DIR/public/js"
create_directory "$WEB_DIR/public/images"
create_directory "$WEB_DIR/src"
create_directory "$WEB_DIR/src/controllers"
create_directory "$WEB_DIR/src/models"
create_directory "$CONFIG_DIR/nginx"
create_directory "$CONFIG_DIR/php"
create_directory "$LOG_DIR/nginx"
create_directory "$LOG_DIR/app"
create_directory "$BACKUP_DIR"

echo " Structure créée avec succès"
echo

# 2. Génération des templates de configuration
echo "2. Génération des templates de configuration..."

# Template Nginx
cat > "$CONFIG_DIR/nginx/default.conf" << 'EOF'
server {
 listen 80;
 server_name localhost webapp-devops.local;
 root /var/www/webapp-devops/public;
 index index.php index.html index.htm;
 
 # Logs
 access_log /var/log/nginx/webapp-access.log;
 error_log /var/log/nginx/webapp-error.log;
 
 # Configuration PHP
 location ~ \.php$ {
 fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
 fastcgi_index index.php;
 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
 include fastcgi_params;
 }
 
 # Sécurité
 location ~ /\. {
 deny all;
 }
 
 # Assets statiques
 location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
 expires 1y;
 add_header Cache-Control "public, immutable";
 }
}
EOF
echo " Template Nginx créé"

# Template PHP
cat > "$CONFIG_DIR/php/php.ini" << 'EOF'
; Configuration PHP pour développement
[PHP]
engine = On
short_open_tag = Off
precision = 14
output_buffering = 4096
zlib.output_compression = Off
implicit_flush = Off
serialize_precision = -1

; Erreurs et logging
display_errors = On
display_startup_errors = On
log_errors = On
error_log = /var/log/php/error.log
error_reporting = E_ALL

; Limites
max_execution_time = 30
max_input_time = 60
memory_limit = 128M
post_max_size = 8M
upload_max_filesize = 2M

; Extensions
extension=pdo_mysql
extension=curl
extension=json
extension=mbstring
EOF
echo " Template PHP créé"

# Configuration Docker Compose pour l'environnement
cat > "$BASE_DIR/docker-compose.yml" << 'EOF'
version: '3.8'
services:
 nginx:
 image: nginx:alpine
 ports:
 - "8080:80"
 volumes:
 - ./config/nginx:/etc/nginx/conf.d
 - ./webapp-devops/public:/var/www/webapp-devops/public
 depends_on:
 - php
 
 php:
 image: php:7.4-fpm
 volumes:
 - ./webapp-devops:/var/www/webapp-devops
 - ./config/php/php.ini:/usr/local/etc/php/php.ini
 
 mysql:
 image: mysql:8.0
 environment:
 MYSQL_ROOT_PASSWORD: devops123
 MYSQL_DATABASE: webapp_devops
 ports:
 - "3306:3306"
EOF
echo " Docker Compose créé"
echo

# 3. Création des fichiers web de test
echo "3. Création des fichiers web de test..."

# Page d'accueil
cat > "$WEB_DIR/public/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>WebApp DevOps</title>
 <link rel="stylesheet" href="css/style.css">
</head>
<body>
 <div class="container">
 <h1>WebApp DevOps</h1>
 <p>Environnement de développement configuré avec succès!</p>
 <div class="info">
 <h2>Technologies</h2>
 <ul>
 <li>Nginx (Serveur web)</li>
 <li>PHP 7.4 (Backend)</li>
 <li>MySQL 8.0 (Base de données)</li>
 <li>Docker (Containerisation)</li>
 </ul>
 </div>
 <button onclick="loadData()">Tester API</button>
 </div>
 <script src="js/app.js"></script>
</body>
</html>
EOF
echo " index.html créé"

# Feuille de style
cat > "$WEB_DIR/public/css/style.css" << 'EOF'
/* Styles pour WebApp DevOps */
* {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
}

body {
 font-family: 'Arial', sans-serif;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 color: #333;
 min-height: 100vh;
 display: flex;
 align-items: center;
 justify-content: center;
}

.container {
 background: white;
 padding: 2rem;
 border-radius: 10px;
 box-shadow: 0 10px 30px rgba(0,0,0,0.3);
 max-width: 600px;
 text-align: center;
}

h1 {
 color: #667eea;
 margin-bottom: 1rem;
 font-size: 2.5rem;
}

.info {
 margin: 2rem 0;
 text-align: left;
}

ul {
 list-style-type: none;
 padding-left: 1rem;
}

li {
 padding: 0.5rem 0;
 border-left: 3px solid #667eea;
 padding-left: 1rem;
 margin: 0.5rem 0;
}

button {
 background: #667eea;
 color: white;
 border: none;
 padding: 1rem 2rem;
 border-radius: 5px;
 cursor: pointer;
 font-size: 1rem;
}

button:hover {
 background: #764ba2;
}
EOF
echo " style.css créé"

# Script JavaScript
cat > "$WEB_DIR/public/js/app.js" << 'EOF'
// Application JavaScript pour WebApp DevOps
console.log('WebApp DevOps - Application chargée');

function loadData() {
 console.log('Test API appelé');
 
 // Simulation d'appel API
 fetch('/api/status')
 .then(response => {
 if (!response.ok) {
 throw new Error('API non disponible');
 }
 return response.json();
 })
 .then(data => {
 alert('API opérationnelle: ' + JSON.stringify(data));
 })
 .catch(error => {
 alert('Erreur API: ' + error.message);
 console.error('Erreur:', error);
 });
}

// Vérification périodique du statut
setInterval(() => {
 console.log('Vérification statut application...');
}, 30000);
EOF
echo " app.js créé"

# Fichier PHP de test
cat > "$WEB_DIR/src/app.php" << 'EOF'
<?php
/**
 * Application PHP de test pour WebApp DevOps
 */

header('Content-Type: application/json');

// Configuration
$config = [
 'app_name' => 'WebApp DevOps',
 'version' => '1.0.0',
 'environment' => 'development',
 'debug' => true
];

// Route simple API
$uri = $_SERVER['REQUEST_URI'];

if ($uri === '/api/status') {
 echo json_encode([
 'status' => 'operational',
 'timestamp' => date('Y-m-d H:i:s'),
 'config' => $config
 ]);
} else {
 http_response_code(404);
 echo json_encode([
 'error' => 'Route not found',
 'uri' => $uri
 ]);
}
?>
EOF
echo " app.php créé"
echo

# 4. Organisation des logs par date
echo "4. Organisation des logs..."

# Logs Nginx
current_date=$(date '+%Y-%m-%d')
echo "[$current_date 10:00:00] Server started" > "$LOG_DIR/nginx/access-$current_date.log"
echo "[$current_date 10:00:01] No errors on startup" > "$LOG_DIR/nginx/error-$current_date.log"

# Logs application
echo "[$current_date 10:00:02] Application initialized" > "$LOG_DIR/app/application-$current_date.log"
echo "[$current_date 10:00:03] Database connection established" > "$LOG_DIR/app/database-$current_date.log"

# Script de rotation des logs
cat > "$BASE_DIR/rotate-logs.sh" << 'EOF'
#!/bin/bash
# Script de rotation des logs quotidienne

LOG_DIR="/tmp/projet-web/logs"
ARCHIVE_DIR="$LOG_DIR/archives"
DATE=$(date '+%Y-%m-%d')

mkdir -p "$ARCHIVE_DIR"

# Archiver les logs de plus de 7 jours
find "$LOG_DIR" -name "*.log" -mtime +7 -exec mv {} "$ARCHIVE_DIR/" \;

# Compresser les archives anciennes
find "$ARCHIVE_DIR" -name "*.log" -mtime +1 -exec gzip {} \;

echo "Rotation logs terminée: $DATE"
EOF
chmod +x "$BASE_DIR/rotate-logs.sh"
echo " Logs organisés et script de rotation créé"
echo

# 5. Script de sauvegarde
echo "5. Création du script de sauvegarde..."

cat > "$BASE_DIR/backup.sh" << 'EOF'
#!/bin/bash
# Script de sauvegarde automatisé

BACKUP_DIR="/tmp/projet-web/backups"
PROJECT_DIR="/tmp/projet-web"
DATE=$(date '+%Y%m%d_%H%M%S')
BACKUP_NAME="webapp-devops-backup-$DATE"

echo "Début sauvegarde: $(date)"

# Créer archive des fichiers critiques
tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" \
 --exclude="$BACKUP_DIR" \
 --exclude="*/logs/archives/*" \
 "$PROJECT_DIR"

if [ $? -eq 0 ]; then
 echo " Sauvegarde créée: $BACKUP_NAME.tar.gz"
 
 # Vérifier la taille
 size=$(du -h "$BACKUP_DIR/$BACKUP_NAME.tar.gz" | cut -f1)
 echo " Taille: $size"
 
 # Nettoyer anciennes sauvegardes (garder 5 dernières)
 cd "$BACKUP_DIR"
 ls -t webapp-devops-backup-*.tar.gz | tail -n +6 | xargs -r rm
 
 echo " Nettoyage anciennes sauvegardes terminé"
else
 echo " Erreur lors de la sauvegarde"
 exit 1
fi

echo "Fin sauvegarde: $(date)"
EOF
chmod +x "$BASE_DIR/backup.sh"
echo " Script de sauvegarde créé et rendu exécutable"
echo

# 6. Affichage de la structure créée
echo "6. Vérification de la structure créée:"

if command -v tree >/dev/null 2>&1; then
 tree "$BASE_DIR" -L 3
else
 find "$BASE_DIR" -type d | head -20 | sort
fi

echo
echo "Résumé des fichiers créés:"
find "$BASE_DIR" -type f | wc -l | xargs echo " Total fichiers:"
find "$BASE_DIR" -name "*.sh" | wc -l | xargs echo " Scripts shell:"
find "$BASE_DIR" -name "*.conf" -o -name "*.ini" | wc -l | xargs echo " Fichiers config:"
find "$BASE_DIR" -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.php" | wc -l | xargs echo " Fichiers web:"

echo
echo "=== SETUP TERMINÉ ==="
echo "Projet configuré dans: $BASE_DIR"
echo "Pour démarrer l'environnement:"
echo " cd $BASE_DIR"
echo " docker-compose up -d"
echo " ./backup.sh"
