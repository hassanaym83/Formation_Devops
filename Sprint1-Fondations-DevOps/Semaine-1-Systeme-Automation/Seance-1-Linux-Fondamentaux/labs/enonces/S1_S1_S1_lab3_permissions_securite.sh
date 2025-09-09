#!/bin/bash

# LAB 3 - Sécurisation permissions
# 
# Objectifs :
# - Appliquer les permissions appropriées pour un serveur web
# - Sécuriser les fichiers de configuration selon les bonnes pratiques
# - Créer un système de vérification automatisé
# 
# Points : 5/30
# 
# Durée estimée : 20 minutes

# Mission: Durcissement sécuritaire d'un serveur web Apache/Nginx
# Contexte: Mise en conformité sécuritaire avant mise en production

echo "=== SÉCURISATION PERMISSIONS SERVEUR WEB ==="
echo "Audit sécurité: $(date)"
echo "Serveur: $(hostname)"
echo

# Configuration sécuritaire
WEB_ROOT="/tmp/webserver-security" # Simulation environnement web
CONFIG_DIR="$WEB_ROOT/config"
LOGS_DIR="$WEB_ROOT/logs"
SECRETS_DIR="$WEB_ROOT/secrets"
PUBLIC_DIR="$WEB_ROOT/public"

# Création de l'environnement de test
echo "Création environnement de test..."
mkdir -p "$WEB_ROOT"/{config,logs,secrets,public,scripts}
mkdir -p "$PUBLIC_DIR"/{css,js,images}

# Création de fichiers de test
echo "<h1>Test Web</h1>" > "$PUBLIC_DIR/index.html"
echo "body { color: blue; }" > "$PUBLIC_DIR/css/style.css"
echo "console.log('app');" > "$PUBLIC_DIR/js/app.js"

echo "server { listen 80; }" > "$CONFIG_DIR/nginx.conf"
echo "database_password=secret123" > "$SECRETS_DIR/db.conf"
echo "api_key=xyz789abc" > "$SECRETS_DIR/api.key"

echo "$(date) - Server started" > "$LOGS_DIR/access.log"
echo "$(date) - No errors" > "$LOGS_DIR/error.log"

echo

# TODO: 1. Sécuriser les fichiers web publics
echo "1. Configuration permissions fichiers web..."
# Appliquer les permissions appropriées:
# - Dossiers publics: 755 (lecture/exécution pour tous)
# - Fichiers web (HTML, CSS, JS): 644 (lecture pour tous)
# - Fichiers images: 644

echo

# TODO: 2. Sécuriser les configurations
echo "2. Sécurisation des configurations..."
# Appliquer les permissions:
# - Fichiers config publique (nginx.conf): 644
# - Dossier config: 755

echo

# TODO: 3. Sécuriser les secrets
echo "3. Protection des fichiers secrets..."
# Appliquer les permissions les plus restrictives:
# - Fichiers secrets (db.conf, api.key): 600 (propriétaire seulement)
# - Dossier secrets: 700

echo

# TODO: 4. Configurer les logs
echo "4. Configuration des logs..."
# Permissions pour les logs:
# - Fichiers de logs: 660 (propriétaire + groupe)
# - Dossier logs: 750

echo

# TODO: 5. Créer script de vérification
echo "5. Script de vérification des permissions..."

# Fonction de vérification
verify_permissions() {
 local file="$1"
 local expected="$2"
 local current=$(stat -c "%a" "$file" 2>/dev/null)
 
 if [ "$current" = "$expected" ]; then
 echo "OK: $file ($current)"
 else
 echo "ERREUR: $file - Attendu: $expected, Actuel: $current"
 fi
}

# TODO: Vérifier toutes les permissions définies ci-dessus
echo "Vérification des permissions appliquées:"

echo

# TODO: 6. Audit de sécurité
echo "6. Rapport d'audit de sécurité:"
# Générer un rapport avec:
# - Permissions par type de fichier
# - Fichiers avec permissions trop permissives
# - Recommandations d'amélioration

echo "=== AUDIT SÉCURITAIRE TERMINÉ ==="
