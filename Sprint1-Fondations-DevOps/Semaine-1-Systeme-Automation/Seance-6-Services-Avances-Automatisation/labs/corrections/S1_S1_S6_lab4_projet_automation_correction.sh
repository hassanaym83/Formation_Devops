#!/bin/bash

# ==================================================================================
# Simplon Maghreb - Formation DevOps
# Sprint 1 - Semaine 1 - Séance 6 
# LAB 4: Projet d'automatisation complet - CORRECTION
# ==================================================================================

# Configuration globale
set -euo pipefail

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Fonction de logging
info() { echo -e "${BLUE}[INFO]${NC} $*"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# Vérification des privilèges
check_privileges() {
    if [[ $EUID -ne 0 ]]; then
        error "Ce script doit être exécuté avec les privilèges root"
        error "Utilisation: sudo $0"
        exit 1
    fi
}

# Variables globales
PROJECT_DIR="/opt/webserver-automation"
LOG_DIR="/var/log/webserver-automation"
WEB_USER="webserver"
WEB_PORT="8080"

# === ÉTAPE 1: PRÉPARATION DE L'ENVIRONNEMENT ===

setup_environment() {
    info "=== ÉTAPE 1: Préparation de l'environnement ==="
    
    # Installer les dépendances nécessaires
    info "Installation des paquets requis..."
    apt update >/dev/null 2>&1
    apt install -y nginx python3 python3-pip curl bc jq >/dev/null 2>&1
    
    # Créer l'utilisateur dédié
    info "Création de l'utilisateur dédié: $WEB_USER"
    if ! id "$WEB_USER" >/dev/null 2>&1; then
        useradd -r -s /bin/bash -m -d "/home/$WEB_USER" "$WEB_USER"
        success "Utilisateur $WEB_USER créé"
    else
        warning "Utilisateur $WEB_USER existe déjà"
    fi
    
    # Créer la structure de répertoires
    info "Création de la structure de répertoires..."
    mkdir -p "$PROJECT_DIR"/{scripts,configs,web,backups}
    mkdir -p "$LOG_DIR"
    mkdir -p "/home/$WEB_USER/backups"
    
    # Permissions appropriées
    chown -R "$WEB_USER:$WEB_USER" "/home/$WEB_USER"
    chown -R "$WEB_USER:$WEB_USER" "$PROJECT_DIR"
    chown -R "$WEB_USER:$WEB_USER" "$LOG_DIR"
    
    success "Environnement préparé avec succès"
}

# === ÉTAPE 2: CRÉATION DE L'APPLICATION WEB ===

create_web_application() {
    info "=== ÉTAPE 2: Création de l'application web ==="
    
    # Créer une application Python avec Flask
    info "Installation de Flask..."
    pip3 install flask >/dev/null 2>&1
    
    # Créer l'application web
    info "Création de l'application web..."
    cat > "$PROJECT_DIR/web/app.py" << 'EOF'
#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import os
import platform
import psutil
import datetime
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    """API endpoint pour le statut du système"""
    try:
        # Informations système
        system_info = {
            'hostname': platform.node(),
            'platform': platform.platform(),
            'uptime': str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Métriques système
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu': {
                'usage_percent': cpu_usage,
                'count': psutil.cpu_count()
            },
            'memory': {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent': memory.percent
            },
            'disk': {
                'total_gb': round(disk.total / (1024**3), 2),
                'free_gb': round(disk.free / (1024**3), 2),
                'percent': round((disk.used / disk.total) * 100, 2)
            }
        }
        
        # Processus top 5 CPU
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_info = proc.info
                if proc_info['cpu_percent'] > 0:
                    processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
        
        return jsonify({
            'status': 'healthy',
            'system': system_info,
            'metrics': metrics,
            'top_processes': top_processes
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    """Endpoint de santé"""
    return jsonify({
        'status': 'healthy',
        'service': 'webserver-automation',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    # En production, utiliser Gunicorn
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
EOF

    # Créer le template HTML
    mkdir -p "$PROJECT_DIR/web/templates"
    cat > "$PROJECT_DIR/web/templates/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Serveur Web Automatisé</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: #f8f9fa; padding: 20px; border-radius: 6px; border-left: 4px solid #007bff; }
        .metric-value { font-size: 2em; font-weight: bold; color: #007bff; }
        .metric-label { color: #666; margin-bottom: 5px; }
        .status { padding: 10px; border-radius: 4px; margin: 20px 0; text-align: center; }
        .status.healthy { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .processes { background: #f8f9fa; padding: 20px; border-radius: 6px; }
        .process { padding: 8px; border-bottom: 1px solid #ddd; display: flex; justify-content: space-between; }
        .process:last-child { border-bottom: none; }
        .refresh-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 10px 0; }
        .refresh-btn:hover { background: #0056b3; }
        .timestamp { color: #666; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Serveur Web Automatisé</h1>
        
        <div id="status" class="status">Chargement...</div>
        
        <button class="refresh-btn" onclick="loadStatus()">Actualiser</button>
        
        <div class="metrics" id="metrics">
            <!-- Les métriques seront chargées ici -->
        </div>
        
        <div class="processes" id="processes">
            <!-- Les processus seront chargés ici -->
        </div>
        
        <div class="timestamp" id="timestamp"></div>
    </div>

    <script>
        async function loadStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                
                if (data.status === 'healthy') {
                    document.getElementById('status').innerHTML = 'Système fonctionnel';
                    document.getElementById('status').className = 'status healthy';
                    
                    // Afficher les métriques
                    const metrics = data.metrics;
                    document.getElementById('metrics').innerHTML = `
                        <div class="metric-card">
                            <div class="metric-label">CPU</div>
                            <div class="metric-value">${metrics.cpu.usage_percent.toFixed(1)}%</div>
                            <div>${metrics.cpu.count} cœurs</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Mémoire</div>
                            <div class="metric-value">${metrics.memory.percent.toFixed(1)}%</div>
                            <div>${metrics.memory.available_gb}GB / ${metrics.memory.total_gb}GB libres</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Disque</div>
                            <div class="metric-value">${metrics.disk.percent}%</div>
                            <div>${metrics.disk.free_gb}GB / ${metrics.disk.total_gb}GB libres</div>
                        </div>
                    `;
                    
                    // Afficher les processus
                    let processHtml = '<h3>Top 5 Processus (CPU)</h3>';
                    data.top_processes.forEach(proc => {
                        processHtml += `<div class="process">
                            <span><strong>${proc.name}</strong> (PID: ${proc.pid})</span>
                            <span>CPU: ${proc.cpu_percent.toFixed(1)}% | Mem: ${proc.memory_percent.toFixed(1)}%</span>
                        </div>`;
                    });
                    document.getElementById('processes').innerHTML = processHtml;
                    
                    // Timestamp
                    document.getElementById('timestamp').textContent = 
                        `Dernière mise à jour: ${new Date(data.system.timestamp).toLocaleString('fr-FR')}`;
                        
                } else {
                    document.getElementById('status').innerHTML = 'Erreur système: ' + data.message;
                    document.getElementById('status').className = 'status error';
                }
            } catch (error) {
                document.getElementById('status').innerHTML = 'Erreur de connexion: ' + error.message;
                document.getElementById('status').className = 'status error';
            }
        }
        
        // Charger au démarrage
        loadStatus();
        
        // Auto-refresh toutes les 10 secondes
        setInterval(loadStatus, 10000);
    </script>
</body>
</html>
EOF

    # Installer psutil pour Python
    pip3 install psutil >/dev/null 2>&1
    
    # Permissions
    chown -R "$WEB_USER:$WEB_USER" "$PROJECT_DIR/web"
    
    success "Application web créée avec succès"
}

# === ÉTAPE 3: CRÉATION DU SERVICE SYSTEMD ===

create_systemd_service() {
    info "=== ÉTAPE 3: Création du service systemd ==="
    
    # Créer le script de démarrage
    cat > "$PROJECT_DIR/scripts/start_webapp.sh" << EOF
#!/bin/bash
cd "$PROJECT_DIR/web"
export PORT=$WEB_PORT
python3 app.py
EOF
    
    chmod +x "$PROJECT_DIR/scripts/start_webapp.sh"
    
    # Créer le service systemd
    cat > /etc/systemd/system/webserver-automation.service << EOF
[Unit]
Description=Serveur Web Automatisé - Projet DevOps
Documentation=file://$PROJECT_DIR/README.txt
After=network.target
Wants=network.target

[Service]
Type=simple
User=$WEB_USER
Group=$WEB_USER
WorkingDirectory=$PROJECT_DIR/web
Environment=PORT=$WEB_PORT
Environment=PYTHONPATH=$PROJECT_DIR/web
ExecStart=/usr/bin/python3 $PROJECT_DIR/web/app.py
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
TimeoutStartSec=30
TimeoutStopSec=30

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=webserver-automation

# Sécurité
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$LOG_DIR
ReadWritePaths=/tmp

# Limites de ressources
LimitNOFILE=65536
MemoryMax=512M

[Install]
WantedBy=multi-user.target
EOF

    success "Service systemd créé: webserver-automation.service"
}

# === ÉTAPE 4: SCRIPTS D'AUTOMATISATION ===

create_automation_scripts() {
    info "=== ÉTAPE 4: Création des scripts d'automatisation ==="
    
    # Script de sauvegarde
    info "Création du script de sauvegarde..."
    cat > "$PROJECT_DIR/scripts/backup.sh" << 'EOF'
#!/bin/bash

# Script de sauvegarde automatique
set -euo pipefail

# Configuration
BACKUP_DIR="/opt/webserver-automation/backups"
LOG_FILE="/var/log/webserver-automation/backup.log"
RETENTION_DAYS=7
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Fonction de logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

log "Début de la sauvegarde - $TIMESTAMP"

# Créer le répertoire de sauvegarde
mkdir -p "$BACKUP_DIR"

# Sauvegarder l'application
tar -czf "$BACKUP_DIR/webapp_${TIMESTAMP}.tar.gz" -C /opt/webserver-automation web/ scripts/ configs/ 2>/dev/null

# Sauvegarder les logs
tar -czf "$BACKUP_DIR/logs_${TIMESTAMP}.tar.gz" -C /var/log webserver-automation/ 2>/dev/null

# Sauvegarder la configuration systemd
cp /etc/systemd/system/webserver-automation.* "$BACKUP_DIR/" 2>/dev/null || true

# Nettoyer les anciennes sauvegardes
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>/dev/null

# Statistiques
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

log "Sauvegarde terminée - $BACKUP_COUNT fichiers, taille totale: $BACKUP_SIZE"
EOF
    
    # Script de monitoring personnalisé
    info "Création du script de monitoring..."
    cat > "$PROJECT_DIR/scripts/monitor.sh" << 'EOF'
#!/bin/bash

# Script de monitoring pour l'application web
set -euo pipefail

LOG_FILE="/var/log/webserver-automation/monitor.log"
WEB_URL="http://localhost:8080/health"
SERVICE_NAME="webserver-automation"

# Fonction de logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Vérifier le service systemd
check_service() {
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log "OK - Service $SERVICE_NAME actif"
        return 0
    else
        log "ERREUR - Service $SERVICE_NAME inactif"
        return 1
    fi
}

# Vérifier la connectivité web
check_web() {
    if curl -s --max-time 10 "$WEB_URL" | grep -q '"status": "healthy"'; then
        log "OK - Application web répond correctement"
        return 0
    else
        log "ERREUR - Application web ne répond pas"
        return 1
    fi
}

# Vérifier les ressources système
check_resources() {
    # CPU
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    log "INFO - CPU: ${CPU}%"
    
    # Mémoire
    MEM=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    log "INFO - Mémoire: ${MEM}%"
    
    # Disque
    DISK=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
    log "INFO - Disque: ${DISK}%"
    
    # Vérifications des seuils
    if (( $(echo "$CPU > 80" | bc -l) )); then
        log "ALERTE - CPU élevé: ${CPU}%"
    fi
    
    if [ "$MEM" -gt 80 ]; then
        log "ALERTE - Mémoire élevée: ${MEM}%"
    fi
    
    if [ "$DISK" -gt 85 ]; then
        log "ALERTE - Disque plein: ${DISK}%"
    fi
}

# Redémarrer le service si nécessaire
restart_if_needed() {
    if ! check_service || ! check_web; then
        log "ATTENTION - Tentative de redémarrage du service"
        systemctl restart "$SERVICE_NAME"
        sleep 10
        
        if check_service && check_web; then
            log "OK - Service redémarré avec succès"
        else
            log "ERREUR - Impossible de redémarrer le service"
        fi
    fi
}

# Exécution principale
log "Début du monitoring"
check_service
check_web
check_resources
restart_if_needed
log "Monitoring terminé"
EOF
    
    # Script de déploiement
    info "Création du script de déploiement..."
    cat > "$PROJECT_DIR/scripts/deploy.sh" << 'EOF'
#!/bin/bash

# Script de déploiement automatique
set -euo pipefail

LOG_FILE="/var/log/webserver-automation/deploy.log"
SERVICE_NAME="webserver-automation"

# Fonction de logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Fonction de déploiement
deploy() {
    log "Début du déploiement"
    
    # Sauvegarder avant déploiement
    /opt/webserver-automation/scripts/backup.sh
    
    # Arrêter le service
    log "Arrêt du service"
    systemctl stop "$SERVICE_NAME"
    
    # Ici on pourrait:
    # - Récupérer une nouvelle version de l'application
    # - Mettre à jour les dépendances
    # - Modifier la configuration
    
    # Recharger systemd si nécessaire
    systemctl daemon-reload
    
    # Redémarrer le service
    log "Redémarrage du service"
    systemctl start "$SERVICE_NAME"
    
    # Vérifier le déploiement
    sleep 10
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log "Déploiement réussi - Service actif"
        # Test de l'application
        if curl -s http://localhost:8080/health | grep -q "healthy"; then
            log "Déploiement réussi - Application fonctionnelle"
        else
            log "Déploiement partiellement réussi - Application ne répond pas correctement"
        fi
    else
        log "Déploiement échoué - Service inactif"
        return 1
    fi
}

# Exécution
deploy
EOF
    
    # Rendre les scripts exécutables
    chmod +x "$PROJECT_DIR/scripts"/*.sh
    chown -R "$WEB_USER:$WEB_USER" "$PROJECT_DIR/scripts"
    
    success "Scripts d'automatisation créés"
}

# === ÉTAPE 5: CONFIGURATION DES TIMERS ===

create_timers() {
    info "=== ÉTAPE 5: Configuration des timers systemd ==="
    
    # Timer pour les sauvegardes (quotidien à 2h)
    cat > /etc/systemd/system/webserver-backup.timer << EOF
[Unit]
Description=Timer pour sauvegarde automatique du serveur web
Documentation=file://$PROJECT_DIR/README.txt

[Timer]
OnCalendar=daily
# Exécution à 02:00
OnCalendar=*-*-* 02:00:00
# Persistance pour rattraper les exécutions manquées
Persistent=true
# Précision
AccuracySec=1min

[Install]
WantedBy=timers.target
EOF
    
    # Service pour les sauvegardes
    cat > /etc/systemd/system/webserver-backup.service << EOF
[Unit]
Description=Sauvegarde automatique du serveur web
Documentation=file://$PROJECT_DIR/README.txt

[Service]
Type=oneshot
User=$WEB_USER
Group=$WEB_USER
ExecStart=$PROJECT_DIR/scripts/backup.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=webserver-backup
EOF
    
    # Timer pour le monitoring (toutes les 5 minutes)
    cat > /etc/systemd/system/webserver-monitor.timer << EOF
[Unit]
Description=Timer pour monitoring du serveur web
Documentation=file://$PROJECT_DIR/README.txt

[Timer]
# Toutes les 5 minutes
OnCalendar=*:0/5
# Pas de persistance (trop fréquent)
Persistent=false
# Précision
AccuracySec=30s

[Install]
WantedBy=timers.target
EOF
    
    # Service pour le monitoring
    cat > /etc/systemd/system/webserver-monitor.service << EOF
[Unit]
Description=Monitoring du serveur web
Documentation=file://$PROJECT_DIR/README.txt

[Service]
Type=oneshot
User=root
Group=root
ExecStart=$PROJECT_DIR/scripts/monitor.sh
StandardOutput=journal
StandardError=journal
SyslogIdentifier=webserver-monitor
EOF
    
    success "Timers systemd créés"
}

# === ÉTAPE 6: CONFIGURATION NGINX (optionnel) ===

setup_nginx_proxy() {
    info "=== ÉTAPE 6: Configuration du proxy Nginx ==="
    
    # Créer la configuration Nginx
    cat > /etc/nginx/sites-available/webserver-automation << EOF
server {
    listen 80;
    server_name localhost;
    
    # Logs
    access_log /var/log/nginx/webserver-automation.access.log;
    error_log /var/log/nginx/webserver-automation.error.log;
    
    # Proxy vers l'application Python
    location / {
        proxy_pass http://127.0.0.1:$WEB_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Healthcheck direct
    location /nginx-health {
        access_log off;
        return 200 "nginx ok\n";
        add_header Content-Type text/plain;
    }
}
EOF
    
    # Activer le site
    ln -sf /etc/nginx/sites-available/webserver-automation /etc/nginx/sites-enabled/
    
    # Désactiver le site par défaut
    rm -f /etc/nginx/sites-enabled/default
    
    # Tester la configuration
    if nginx -t >/dev/null 2>&1; then
        systemctl reload nginx
        success "Nginx configuré et rechargé"
    else
        error "Erreur dans la configuration Nginx"
        return 1
    fi
}

# === TESTS ET VALIDATION ===

run_comprehensive_tests() {
    info "=== TESTS ET VALIDATION COMPLÈTE ==="
    
    # Test 1: Services systemd
    info "Test 1: Services systemd"
    systemctl daemon-reload
    
    for service in webserver-automation webserver-backup webserver-monitor; do
        if systemctl is-enabled --quiet "$service.timer" 2>/dev/null || systemctl is-enabled --quiet "$service.service" 2>/dev/null; then
            success "Service/Timer $service configuré"
        else
            warning "Service/Timer $service non configuré"
        fi
    done
    
    # Test 2: Démarrage de l'application
    info "Test 2: Démarrage de l'application web"
    systemctl start webserver-automation
    sleep 15
    
    if systemctl is-active --quiet webserver-automation; then
        success "Application web démarrée"
    else
        error "Échec du démarrage de l'application"
        journalctl -u webserver-automation --no-pager -n 10
        return 1
    fi
    
    # Test 3: Test de connectivité
    info "Test 3: Test de connectivité"
    if curl -s --max-time 10 "http://localhost:$WEB_PORT/health" | grep -q "healthy"; then
        success "Application répond correctement"
    else
        error "Application ne répond pas"
        return 1
    fi
    
    # Test 4: Test de l'interface web
    info "Test 4: Test de l'interface web"
    if curl -s --max-time 10 "http://localhost:$WEB_PORT/" | grep -q "Serveur Web"; then
        success "Interface web accessible"
    else
        warning "Interface web non accessible"
    fi
    
    # Test 5: Test des scripts
    info "Test 5: Test des scripts d'automatisation"
    
    # Test backup
    sudo -u "$WEB_USER" "$PROJECT_DIR/scripts/backup.sh"
    if [ -d "$PROJECT_DIR/backups" ] && [ "$(ls -A $PROJECT_DIR/backups 2>/dev/null | wc -l)" -gt 0 ]; then
        success "Script de sauvegarde fonctionnel"
    else
        warning "Problème avec le script de sauvegarde"
    fi
    
    # Test monitoring
    "$PROJECT_DIR/scripts/monitor.sh"
    if [ -f "$LOG_DIR/monitor.log" ]; then
        success "Script de monitoring fonctionnel"
    else
        warning "Problème avec le script de monitoring"
    fi
    
    # Test 6: Test des timers
    info "Test 6: Activation des timers"
    systemctl enable --now webserver-backup.timer
    systemctl enable --now webserver-monitor.timer
    
    if systemctl is-active --quiet webserver-backup.timer && systemctl is-active --quiet webserver-monitor.timer; then
        success "Timers activés avec succès"
    else
        warning "Problème avec l'activation des timers"
    fi
    
    # Test 7: Test Nginx si configuré
    if systemctl is-active --quiet nginx; then
        info "Test 7: Test du proxy Nginx"
        if curl -s --max-time 10 "http://localhost/health" | grep -q "healthy"; then
            success "Proxy Nginx fonctionnel"
        else
            warning "Proxy Nginx ne fonctionne pas correctement"
        fi
    fi
    
    # Résumé des tests
    info "=== RÉSUMÉ DES TESTS ==="
    systemctl status webserver-automation --no-pager -l
    echo
    info "Prochaines exécutions planifiées:"
    systemctl list-timers webserver-* --no-pager
}

# === DOCUMENTATION ET INFORMATIONS ===

create_project_documentation() {
    info "Création de la documentation du projet..."
    
    cat > "$PROJECT_DIR/README.txt" << EOF
# Projet d'Automatisation - Serveur Web

## Description
Projet complet d'automatisation d'un serveur web incluant:
- Application web Python/Flask avec monitoring système
- Service systemd pour la gestion
- Scripts d'automatisation (sauvegarde, monitoring, déploiement)
- Timers systemd pour l'exécution automatique
- Proxy Nginx (optionnel)
- Interface web de surveillance

## Architecture

### Composants
1. **Application Web** (Python/Flask)
   - Endpoint principal: http://localhost:8080/
   - API status: http://localhost:8080/status
   - Healthcheck: http://localhost:8080/health
   
2. **Service systemd**: webserver-automation.service
   - Démarrage automatique
   - Redémarrage en cas d'échec
   - Logging centralisé

3. **Scripts d'automatisation**:
   - backup.sh: Sauvegarde quotidienne
   - monitor.sh: Surveillance toutes les 5 min
   - deploy.sh: Déploiement automatisé

4. **Timers systemd**:
   - webserver-backup.timer: Sauvegarde à 02:00
   - webserver-monitor.timer: Monitoring toutes les 5 min

### Structure des fichiers
```
/opt/webserver-automation/
├── web/
│   ├── app.py              # Application Flask
│   └── templates/
│       └── index.html      # Interface web
├── scripts/
│   ├── backup.sh           # Script de sauvegarde
│   ├── monitor.sh          # Script de monitoring
│   └── deploy.sh           # Script de déploiement
├── configs/                # Configurations
├── backups/                # Sauvegardes
└── README.txt              # Cette documentation

/var/log/webserver-automation/
├── backup.log              # Logs des sauvegardes
├── monitor.log             # Logs du monitoring
└── deploy.log              # Logs des déploiements

/etc/systemd/system/
├── webserver-automation.service
├── webserver-backup.service
├── webserver-backup.timer
├── webserver-monitor.service
└── webserver-monitor.timer
```

## Utilisation

### Commandes de base
```bash
# Gestion du service principal
systemctl start/stop/restart webserver-automation
systemctl status webserver-automation
systemctl enable webserver-automation  # Démarrage auto

# Gestion des timers
systemctl start/stop webserver-backup.timer
systemctl start/stop webserver-monitor.timer
systemctl list-timers webserver-*

# Exécution manuelle des scripts
sudo -u webserver /opt/webserver-automation/scripts/backup.sh
/opt/webserver-automation/scripts/monitor.sh
/opt/webserver-automation/scripts/deploy.sh

# Surveillance des logs
tail -f /var/log/webserver-automation/monitor.log
journalctl -u webserver-automation -f
```

### Interface Web
- Page principale: http://localhost/
- Métriques en temps réel: CPU, mémoire, disque
- Top 5 processus gourmands
- Statut système et timestamp
- Auto-refresh toutes les 10 secondes

### API Endpoints
```bash
    # Healthcheck direct
curl http://localhost:8080/health

# Métriques détaillées (JSON)
curl http://localhost:8080/status | jq .

# Via Nginx (si configuré)
curl http://localhost/health
```

## Configuration

### Paramètres modifiables
Dans les scripts:
- Seuils d'alerte CPU/mémoire/disque
- Fréquence de monitoring
- Rétention des sauvegardes
- Port de l'application

Dans les timers:
- Heure de sauvegarde
- Fréquence de monitoring
- Persistance des tâches

### Personnalisation de l'application
```python
# Modifier /opt/webserver-automation/web/app.py
# Ajouter des endpoints
# Modifier les métriques collectées
# Personnaliser l'interface HTML
```

### Sécurisation
- Service isolé avec utilisateur dédié
- Restrictions systemd (NoNewPrivileges, PrivateTmp)
- Logs centralisés
- Limites de ressources

## Monitoring et Alertes

### Métriques surveillées
- CPU (seuil: 80%)
- Mémoire (seuil: 80%)
- Disque (seuil: 85%)
- Status de l'application
- Processus gourmands

### Types d'alertes
- INFO: Statistiques normales
- ALERTE: Seuil dépassé
- ERREUR: Service arrêté ou inaccessible

### Logs
```bash
# Monitoring
tail -f /var/log/webserver-automation/monitor.log

# Sauvegardes
tail -f /var/log/webserver-automation/backup.log

# Application (systemd)
journalctl -u webserver-automation -f

# Timers
journalctl -u webserver-backup.timer -f
```

## Maintenance

### Sauvegardes
- Automatiques: tous les jours à 02:00
- Rétention: 7 jours
- Contenu: application, scripts, configs, logs
- Localisation: /opt/webserver-automation/backups/

### Déploiement
```bash
# Déploiement automatique avec sauvegarde
/opt/webserver-automation/scripts/deploy.sh

# Mise à jour manuelle
systemctl stop webserver-automation
# ... modifications ...
systemctl start webserver-automation
```

### Dépannage
```bash
# Vérifier le statut
systemctl status webserver-automation

# Logs d'erreur
journalctl -u webserver-automation --since "1 hour ago"

# Test de connectivité
curl -v http://localhost:8080/health

# Redémarrage d'urgence
systemctl restart webserver-automation

# Vérifier les permissions
ls -la /opt/webserver-automation/
ls -la /var/log/webserver-automation/
```

## Extensions possibles

### Fonctionnalités avancées
- Base de données pour historique des métriques
- Notifications par email/Slack
- Interface web d'administration
- API REST complète
- Déploiement avec Git hooks
- Tests automatisés
- Monitoring de services externes
- Gestion multi-environnement

### Intégrations
- Grafana pour les métriques
- Prometheus pour la collecte
- ELK Stack pour les logs
- Docker pour le déploiement
- CI/CD avec GitLab/Jenkins
- Load balancer avec HAProxy

## Sécurité

### Bonnes pratiques implémentées
- Utilisateur dédié non-privilégié
- Isolation des processus
- Logs séparés et protégés
- Validation des entrées
- Timeouts et limites de ressources
- Redémarrage automatique sécurisé

### Améliorations possibles
- HTTPS avec certificats
- Authentification sur l'interface
- Rate limiting
- Firewall application (fail2ban)
- Audit trails
- Chiffrement des sauvegardes
EOF
    
    # Créer un guide rapide
    cat > "$PROJECT_DIR/QUICKSTART.txt" << EOF
# Guide de Démarrage Rapide

## Installation
sudo ./S1_S1_S6_lab4_projet_automation_correction.sh install

## Vérification
curl http://localhost:8080/health
# Réponse attendue: {"status": "healthy", ...}

## Interface Web
Ouvrir: http://localhost/ (via Nginx)
Ou: http://localhost:8080/ (direct)

## Commandes essentielles
systemctl status webserver-automation       # Statut
tail -f /var/log/webserver-automation/monitor.log  # Logs
systemctl list-timers webserver-*          # Planification

## Tests
./S1_S1_S6_lab4_projet_automation_correction.sh test

## Nettoyage
./S1_S1_S6_lab4_projet_automation_correction.sh cleanup
EOF
    
    chown -R "$WEB_USER:$WEB_USER" "$PROJECT_DIR"
    success "Documentation créée"
}

# === FONCTIONS UTILITAIRES ===

show_project_info() {
    info "=== INFORMATIONS DU PROJET ==="
    
    echo "URLs d'accès:"
    echo "  Interface web: http://localhost:$WEB_PORT/"
    if systemctl is-active --quiet nginx; then
        echo "  Via Nginx: http://localhost/"
    fi
    echo "  API Health: http://localhost:$WEB_PORT/health"
    echo "  API Status: http://localhost:$WEB_PORT/status"
    echo
    echo "Services:"
    echo "  systemctl status webserver-automation"
    echo "  systemctl status webserver-backup.timer"
    echo "  systemctl status webserver-monitor.timer"
    echo
    echo "Logs en temps réel:"
    echo "  tail -f /var/log/webserver-automation/monitor.log"
    echo "  journalctl -u webserver-automation -f"
    echo
    echo "Scripts:"
    echo "  $PROJECT_DIR/scripts/backup.sh     # Sauvegarde manuelle"
    echo "  $PROJECT_DIR/scripts/monitor.sh    # Monitoring manuel"
    echo "  $PROJECT_DIR/scripts/deploy.sh     # Déploiement manuel"
    echo
    echo "Fichiers de configuration:"
    echo "  $PROJECT_DIR/web/app.py           # Application Flask"
    echo "  /etc/systemd/system/webserver-*   # Services systemd"
    echo "  /etc/nginx/sites-available/webserver-automation  # Nginx"
    echo
    echo "Tests et validation:"
    echo "  curl -s http://localhost:$WEB_PORT/health | jq ."
    echo "  systemctl list-timers webserver-*"
    echo "  ls -la $PROJECT_DIR/backups/"
}

# Nettoyage complet
cleanup_project() {
    info "=== NETTOYAGE DU PROJET ==="
    
    # Arrêter et désactiver les services
    for service in webserver-automation webserver-backup webserver-monitor; do
        systemctl stop "$service.service" 2>/dev/null || true
        systemctl stop "$service.timer" 2>/dev/null || true
        systemctl disable "$service.service" 2>/dev/null || true
        systemctl disable "$service.timer" 2>/dev/null || true
    done
    
    # Supprimer les fichiers systemd
    rm -f /etc/systemd/system/webserver-*
    
    # Supprimer la configuration Nginx
    rm -f /etc/nginx/sites-available/webserver-automation
    rm -f /etc/nginx/sites-enabled/webserver-automation
    systemctl reload nginx 2>/dev/null || true
    
    # Supprimer les répertoires du projet
    rm -rf "$PROJECT_DIR"
    rm -rf "$LOG_DIR"
    
    # Supprimer l'utilisateur (optionnel)
    if id "$WEB_USER" >/dev/null 2>&1; then
        userdel -r "$WEB_USER" 2>/dev/null || true
    fi
    
    # Recharger systemd
    systemctl daemon-reload
    systemctl reset-failed
    
    success "Projet supprimé complètement"
}

# === FONCTION PRINCIPALE ===

main() {
    case "${1:-install}" in
        "install")
            check_privileges
            setup_environment
            create_web_application
            create_systemd_service
            create_automation_scripts
            create_timers
            setup_nginx_proxy
            run_comprehensive_tests
            create_project_documentation
            show_project_info
            success "Projet d'automatisation installé avec succès!"
            info "Accédez à http://localhost/ pour voir l'interface web"
            ;;
        "test")
            check_privileges
            run_comprehensive_tests
            ;;
        "info")
            show_project_info
            ;;
        "cleanup")
            check_privileges
            cleanup_project
            ;;
        "backup")
            sudo -u "$WEB_USER" "$PROJECT_DIR/scripts/backup.sh"
            ;;
        "monitor")
            "$PROJECT_DIR/scripts/monitor.sh"
            ;;
        "deploy")
            check_privileges
            "$PROJECT_DIR/scripts/deploy.sh"
            ;;
        *)
            echo "Usage: $0 [install|test|info|cleanup|backup|monitor|deploy]"
            echo "  install   : Installer le projet complet (défaut)"
            echo "  test      : Exécuter les tests seulement"
            echo "  info      : Afficher les informations d'utilisation"
            echo "  cleanup   : Supprimer complètement le projet"
            echo "  backup    : Exécuter une sauvegarde manuelle"
            echo "  monitor   : Exécuter le monitoring manuel"
            echo "  deploy    : Exécuter un déploiement"
            exit 1
            ;;
    esac
}

# Gestion des signaux
trap 'error "Script interrompu par l'\''utilisateur"; exit 1' SIGINT SIGTERM

# Exécution du script principal
main "$@"
