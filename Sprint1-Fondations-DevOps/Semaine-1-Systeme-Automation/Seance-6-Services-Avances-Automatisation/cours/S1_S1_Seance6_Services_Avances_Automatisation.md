# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 6 : Services Avancés et Automatisation Linux

## Objectifs pédagogiques

- Maîtriser l'administration avancée des services systemd avec gestion des dépendances
- Implémenter l'automatisation des tâches avec cron et systemd timers
- Configurer le monitoring proactif et la supervision des services critiques
- Développer des scripts robustes pour l'automatisation DevOps

## Objectifs techniques

systemd, timers, cron, monitoring, alerting, scripting bash, logrotate, rsyslog, supervision, automation, services dependencies, health checks

## Table des matières

1. [Administration avancée des services systemd](#1-administration-avancée-des-services-systemd)
2. [Automatisation avec cron et systemd timers](#2-automatisation-avec-cron-et-systemd-timers)
3. [Monitoring et supervision des services](#3-monitoring-et-supervision-des-services)
4. [Scripting avancé pour l'automatisation DevOps](#4-scripting-avancé-pour-lautomatisation-devops)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)
6. [Ressources complémentaires](#6-ressources-complémentaires)

---

## 1. Administration avancée des services systemd

### Architecture systemd et gestion des dépendances

**systemd** est le gestionnaire de système et de services moderne qui remplace les anciens systèmes d'initialisation comme SysV init. Il offre une gestion sophistiquée des services avec support des dépendances, parallélisation et surveillance avancée.

#### Hiérarchie des unités systemd

```
Architecture des unités systemd :

┌─────────────────────────────────────────────────────────────────┐
│                     UNITÉS SYSTEMD                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ SERVICES (.service)              TIMERS (.timer)               │
│ ├─ Processus métier              ├─ Planification tâches        │
│ ├─ Démons système                ├─ Remplacement cron           │
│ └─ Applications web              └─ Exécution différée          │
│                                                                 │
│ TARGETS (.target)                SOCKETS (.socket)              │
│ ├─ Groupes de services           ├─ Activation à la demande     │
│ ├─ États système                 ├─ Communication IPC           │
│ └─ Points de synchronisation     └─ Écoute réseau              │
│                                                                 │
│ MOUNTS (.mount)                  PATHS (.path)                  │
│ ├─ Points de montage             ├─ Surveillance fichiers       │
│ ├─ Systèmes de fichiers          ├─ Déclencheurs événements     │
│ └─ Stockage réseau               └─ Automatisation réactive     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Configuration des dépendances entre services

```bash
# Service avec dépendances complexes
# /etc/systemd/system/webapp.service

[Unit]
Description=Application Web Production
Documentation=https://docs.company.com/webapp
After=network.target postgresql.service redis.service
Requires=postgresql.service
Wants=redis.service
Conflicts=webapp-dev.service

[Service]
Type=notify
User=webapp
Group=webapp
WorkingDirectory=/opt/webapp

# Commandes de cycle de vie
ExecStartPre=/opt/webapp/scripts/health-check.sh
ExecStart=/opt/webapp/bin/webapp-server
ExecStartPost=/opt/webapp/scripts/warmup.sh
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/opt/webapp/scripts/graceful-shutdown.sh

# Gestion des redémarrages
Restart=on-failure
RestartSec=10
StartLimitBurst=3
StartLimitIntervalSec=300

# Monitoring
WatchdogSec=30
NotifyAccess=main

# Sécurité
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/webapp /var/log/webapp

[Install]
WantedBy=multi-user.target
```

#### Types de dépendances systemd

```bash
# Types de relations entre services

# After= : Ordre de démarrage (séquentiel)
After=network.target database.service
# Démarrer APRÈS ces services, mais ne les impose pas

# Before= : Priorité de démarrage
Before=nginx.service
# Démarrer AVANT nginx si nginx démarre

# Requires= : Dépendance forte (obligatoire)
Requires=postgresql.service
# Échec si postgresql.service ne démarre pas

# Wants= : Dépendance souple (optionnelle)
Wants=redis.service
# Essayer de démarrer redis, continuer si échec

# Conflicts= : Incompatibilité
Conflicts=apache2.service
# Ne peut pas coexister avec apache2

# PartOf= : Cycle de vie lié
PartOf=webapp-stack.target
# Si webapp-stack s'arrête, arrêter ce service aussi
```

**LAB 1** - Configuration service avec dépendances : `S1_S1_S6_lab1_service_systemd.sh`

**Énoncé du LAB 1** :

- **Objectif** : Créer un service systemd avec dépendances complexes pour une application web
- **Durée estimée** : 15 minutes
- **Points** : 5 points
- **Contexte** : Configuration d'un service web nécessitant PostgreSQL et Redis
- **Fichier de travail** : `S1_S1_S6_lab1_service_systemd.sh`

### Gestion avancée des services

#### États et transitions des services

```bash
# Commandes d'analyse des services
systemctl list-units --type=service --state=active
systemctl list-units --type=service --state=failed
systemctl list-dependencies nginx.service
systemctl list-dependencies --reverse nginx.service

# Analyse des performances de démarrage
systemd-analyze                    # Temps total de boot
systemd-analyze blame              # Services les plus lents
systemd-analyze critical-chain     # Chemin critique
systemd-analyze plot > boot.svg    # Graphique timeline

# Inspection détaillée d'un service
systemctl show nginx.service
systemctl cat nginx.service
systemd-analyze verify nginx.service
```

#### Configuration avancée des services

```bash
# Service robuste avec gestion d'erreurs
# /etc/systemd/system/api-service.service

[Unit]
Description=API Service avec monitoring avancé
After=network-online.target database.service
Wants=network-online.target
Requires=database.service

[Service]
Type=notify
User=api-service
Group=api-service
WorkingDirectory=/opt/api-service

# Variables d'environnement
Environment="NODE_ENV=production"
Environment="LOG_LEVEL=info"
EnvironmentFile=/etc/api-service/config.env

# Commandes avec gestion d'erreurs
ExecStartPre=/bin/bash -c 'until pg_isready -h localhost; do sleep 2; done'
ExecStartPre=/opt/api-service/scripts/migration.sh
ExecStart=/opt/api-service/bin/server
ExecStartPost=/opt/api-service/scripts/register-service.sh
ExecReload=/bin/kill -SIGUSR1 $MAINPID
ExecStopPost=/opt/api-service/scripts/cleanup.sh

# Politique de redémarrage intelligente
Restart=always
RestartSec=5
StartLimitBurst=5
StartLimitIntervalSec=600

# Timeouts appropriés
TimeoutStartSec=60
TimeoutStopSec=30
TimeoutReloadSec=10

# Health monitoring
WatchdogSec=30
NotifyAccess=main

# Limites de ressources
MemoryLimit=512M
CPUQuota=200%
TasksMax=50

# Sécurité renforcée
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/var/lib/api-service /var/log/api-service

# Logging structuré
StandardOutput=journal
StandardError=journal
SyslogIdentifier=api-service

[Install]
WantedBy=multi-user.target
```

---

## 2. Automatisation avec cron et systemd timers

### Planification de tâches avec cron

#### Syntaxe et exemples cron

```bash
# Format cron : minute heure jour mois jour_semaine commande
# Champs : 0-59 0-23 1-31 1-12 0-7 (0 et 7 = dimanche)

# Exemples de planification
0 2 * * *           # Tous les jours à 2h00
30 14 * * 1-5       # Lundi à vendredi à 14h30
0 */4 * * *         # Toutes les 4 heures
15 3 1 * *          # Le 1er de chaque mois à 3h15
0 6 * * 1           # Tous les lundis à 6h00
*/15 * * * *        # Toutes les 15 minutes

# Variables d'environnement dans crontab
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=admin@company.com

# Tâches avec redirection des logs
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
30 1 * * 0 /opt/scripts/cleanup.sh > /var/log/cleanup.log 2>&1
```

#### Gestion des crontabs

```bash
# Gestion crontab utilisateur
crontab -e          # Éditer crontab actuel
crontab -l          # Lister tâches cron
crontab -r          # Supprimer toutes les tâches
crontab -u user -e  # Éditer crontab d'un autre utilisateur

# Crontabs système
/etc/crontab        # Crontab système principal
/etc/cron.d/        # Répertoire de crontabs supplémentaires
/etc/cron.daily/    # Scripts quotidiens
/etc/cron.weekly/   # Scripts hebdomadaires
/etc/cron.monthly/  # Scripts mensuels

# Exemple de fichier /etc/cron.d/monitoring
# Surveillance système toutes les 5 minutes
*/5 * * * * monitoring /opt/monitoring/check-services.sh
# Rapport quotidien à 7h00
0 7 * * * monitoring /opt/monitoring/daily-report.sh
```

### systemd Timers - Alternative moderne à cron

#### Avantages des systemd timers

```
Comparaison cron vs systemd timers :

┌─────────────────────────────────────────────────────────────────┐
│                    CRON vs SYSTEMD TIMERS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ CRON TRADITIONNEL             SYSTEMD TIMERS                   │
│ ├─ Syntaxe complexe           ├─ Syntaxe claire et lisible      │
│ ├─ Granularité minute         ├─ Granularité microseconde       │
│ ├─ Pas de rattrapage          ├─ Rattrapage si système éteint   │
│ ├─ Logs dispersés             ├─ Logs centralisés (journald)    │
│ ├─ Pas de dépendances         ├─ Gestion dépendances services   │
│ ├─ Exécution isolée           ├─ Intégration systemd complète   │
│ └─ Gestion erreurs basique    └─ Gestion erreurs sophistiquée   │
│                                                                 │
│ Usage recommandé :                                              │
│ • Cron : Scripts simples, compatibilité legacy                 │
│ • Timers : Services système, orchestration complexe            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Configuration des systemd timers

```bash
# Timer pour sauvegarde quotidienne
# /etc/systemd/system/backup.timer

[Unit]
Description=Timer de sauvegarde quotidienne
Requires=backup.service

[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=1800

[Install]
WantedBy=timers.target

# Service associé
# /etc/systemd/system/backup.service

[Unit]
Description=Service de sauvegarde système
After=network-online.target

[Service]
Type=oneshot
User=backup
Group=backup
ExecStart=/opt/scripts/backup.sh
TimeoutStartSec=3600
StandardOutput=journal
StandardError=journal

[Install]
# Service déclenché par timer, pas d'activation directe
```

#### Syntaxe OnCalendar avancée

```bash
# Exemples de planification OnCalendar

# Formats simples
OnCalendar=minutely              # Chaque minute
OnCalendar=hourly                # Chaque heure
OnCalendar=daily                 # Quotidien (minuit)
OnCalendar=weekly                # Hebdomadaire (dimanche)
OnCalendar=monthly               # Mensuel (1er du mois)

# Formats précis
OnCalendar=*-*-* 02:30:00        # Chaque jour à 2h30
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 18:00:00  # Jours ouvrés 18h
OnCalendar=*-*-01 04:00:00       # 1er de chaque mois à 4h
OnCalendar=2024-12-25 09:00:00   # Date spécifique

# Intervalles
OnCalendar=*:0/15                # Toutes les 15 minutes
OnCalendar=*-*-* 09..17:00/2:00  # De 9h à 17h, toutes les 2h
OnCalendar=Mon..Fri *-*-* 08:30:00  # Lundi-vendredi 8h30

# Test de syntaxe
systemd-analyze calendar "Mon..Fri *-*-* 18:00:00"
```

**LAB 2** - Configuration systemd timers : `S1_S1_S6_lab2_systemd_timers.sh`

**Énoncé du LAB 2** :

- **Objectif** : Créer des timers systemd pour automatiser les tâches de maintenance
- **Durée estimée** : 20 minutes
- **Points** : 5 points
- **Contexte** : Configuration de tâches automatisées (sauvegarde, nettoyage, monitoring)
- **Fichier de travail** : `S1_S1_S6_lab2_systemd_timers.sh`

### Gestion des timers

```bash
# Gestion des timers
systemctl enable backup.timer
systemctl start backup.timer
systemctl status backup.timer

# Liste des timers actifs
systemctl list-timers
systemctl list-timers --all

# Forcer l'exécution manuelle
systemctl start backup.service

# Logs des timers
journalctl -u backup.timer
journalctl -u backup.service --since "1 day ago"
```

---

## 3. Monitoring et supervision des services

### Monitoring proactif des services

#### Script de surveillance multi-services

```bash
#!/bin/bash
# /opt/monitoring/service-monitor.sh
# Surveillance complète des services critiques

set -euo pipefail

# Configuration
readonly SERVICES=("nginx" "postgresql" "redis" "elasticsearch" "webapp")
readonly LOG_FILE="/var/log/monitoring/service-monitor.log"
readonly ALERT_EMAIL="devops@company.com"
readonly WEBHOOK_URL="${SLACK_WEBHOOK:-}"

# Codes de sortie
readonly EXIT_OK=0
readonly EXIT_WARNING=1
readonly EXIT_CRITICAL=2

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

send_alert() {
    local service="$1"
    local status="$2"
    local message="$3"

    log "ALERT: $service - $status - $message"

    # Email
    echo "$message" | mail -s "Service Alert: $service" "$ALERT_EMAIL"

    # Slack webhook
    if [[ -n "$WEBHOOK_URL" ]]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\" Service Alert: $service - $status\\n$message\"}" \
            "$WEBHOOK_URL" 2>/dev/null || true
    fi
}

check_service_health() {
    local service="$1"
    local service_unit="${service}.service"

    # Vérifier si le service existe
    if ! systemctl list-unit-files | grep -q "^${service_unit}"; then
        log "WARNING: Service $service_unit n'existe pas"
        return $EXIT_WARNING
    fi

    # Vérifier l'état du service
    if ! systemctl is-active --quiet "$service_unit"; then
        local status="CRITICAL"
        local message="Service $service n'est pas actif"
        send_alert "$service" "$status" "$message"

        # Tentative de redémarrage automatique
        log "Tentative de redémarrage de $service"
        if systemctl restart "$service_unit"; then
            sleep 5
            if systemctl is-active --quiet "$service_unit"; then
                log "Service $service redémarré avec succès"
                send_alert "$service" "RECOVERED" "Service redémarré automatiquement"
            else
                send_alert "$service" "CRITICAL" "Échec du redémarrage automatique"
                return $EXIT_CRITICAL
            fi
        else
            send_alert "$service" "CRITICAL" "Impossible de redémarrer le service"
            return $EXIT_CRITICAL
        fi
    fi

    # Tests spécifiques par service
    case "$service" in
        "nginx")
            if ! curl -s --max-time 5 http://localhost >/dev/null; then
                send_alert "$service" "WARNING" "Nginx ne répond pas aux requêtes HTTP"
                return $EXIT_WARNING
            fi
            ;;
        "postgresql")
            if ! sudo -u postgres pg_isready -q; then
                send_alert "$service" "CRITICAL" "PostgreSQL ne répond pas"
                return $EXIT_CRITICAL
            fi
            ;;
        "redis")
            if ! redis-cli ping | grep -q "PONG"; then
                send_alert "$service" "CRITICAL" "Redis ne répond pas au ping"
                return $EXIT_CRITICAL
            fi
            ;;
        "webapp")
            if ! curl -s --max-time 10 http://localhost:3000/health | grep -q "OK"; then
                send_alert "$service" "CRITICAL" "Application ne répond pas au health check"
                return $EXIT_CRITICAL
            fi
            ;;
    esac

    log "Service $service : OK"
    return $EXIT_OK
}

check_system_resources() {
    log "Vérification des ressources système"

    # CPU
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > 90" | bc -l) )); then
        send_alert "system" "WARNING" "Utilisation CPU élevée: ${cpu_usage}%"
    fi

    # Mémoire
    local mem_usage=$(free | awk '/^Mem:/{printf "%.1f", $3/$2*100}')
    if (( $(echo "$mem_usage > 85" | bc -l) )); then
        send_alert "system" "WARNING" "Utilisation mémoire élevée: ${mem_usage}%"
    fi

    # Espace disque
    while read -r line; do
        local usage=$(echo "$line" | awk '{print $5}' | cut -d'%' -f1)
        local mount=$(echo "$line" | awk '{print $6}')

        if [[ "$usage" -gt 90 ]]; then
            send_alert "system" "CRITICAL" "Espace disque critique sur $mount: ${usage}%"
        elif [[ "$usage" -gt 80 ]]; then
            send_alert "system" "WARNING" "Espace disque élevé sur $mount: ${usage}%"
        fi
    done < <(df -h | grep -E "^/dev")
}

generate_report() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local report_file="/var/log/monitoring/health-report-$(date '+%Y%m%d').txt"

    {
        echo "==============================================="
        echo "Rapport de santé système - $timestamp"
        echo "==============================================="
        echo
        echo "Services surveillés:"
        for service in "${SERVICES[@]}"; do
            local status=$(systemctl is-active "${service}.service" 2>/dev/null || echo "unknown")
            printf "  %-15s : %s\n" "$service" "$status"
        done
        echo
        echo "Ressources système:"
        echo "  CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')"
        echo "  Mémoire: $(free -h | awk '/^Mem:/{print $3"/"$2}')"
        echo "  Charge: $(uptime | awk -F'load average:' '{print $2}')"
        echo
        echo "Espace disque:"
        df -h | grep -E "^/dev" | while read -r line; do
            echo "  $line"
        done
        echo
    } >> "$report_file"
}

main() {
    log "=== Début de la surveillance des services ==="

    local overall_status=$EXIT_OK

    # Vérifier chaque service
    for service in "${SERVICES[@]}"; do
        if ! check_service_health "$service"; then
            overall_status=$EXIT_CRITICAL
        fi
    done

    # Vérifier les ressources système
    check_system_resources

    # Générer rapport
    generate_report

    log "=== Fin de la surveillance - Status: $overall_status ==="

    exit $overall_status
}

# Exécution
main "$@"
```

### Gestion des logs avec rsyslog et logrotate

#### Configuration rsyslog avancée

```bash
# /etc/rsyslog.d/50-applications.conf
# Configuration logs applicatifs

# Logs par application
if $programname == 'webapp' then /var/log/webapp/webapp.log
& stop

if $programname == 'api-service' then /var/log/api-service/api.log
& stop

# Logs par niveau de sévérité
*.emerg                         /var/log/emergency.log
*.alert                         /var/log/alert.log
*.crit                          /var/log/critical.log

# Logs réseau centralisés (si serveur de logs)
$ModLoad imudp
$UDPServerRun 514
$UDPServerAddress 0.0.0.0

# Template personnalisé avec JSON
$template JSONFormat,"{\"timestamp\":\"%timegenerated:::date-rfc3339%\",\"host\":\"%hostname%\",\"severity\":\"%syslogseverity-text%\",\"facility\":\"%syslogfacility-text%\",\"program\":\"%programname%\",\"message\":\"%msg:::sp-if-no-1st-sp%%msg:::drop-last-lf%\"}\n"

# Utiliser le template JSON pour certains logs
*.info;mail.none;authpriv.none;cron.none    /var/log/messages;JSONFormat
```

#### Configuration logrotate

```bash
# /etc/logrotate.d/applications
# Rotation des logs applicatifs

/var/log/webapp/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 webapp webapp
    postrotate
        systemctl reload webapp.service
    endscript
}

/var/log/api-service/*.log {
    weekly
    missingok
    rotate 12
    compress
    delaycompress
    notifempty
    create 644 api-service api-service
    sharedscripts
    postrotate
        /bin/kill -HUP $(cat /var/run/api-service.pid 2>/dev/null) 2>/dev/null || true
    endscript
}

# Logs système critiques - rétention longue
/var/log/auth.log /var/log/syslog {
    daily
    missingok
    rotate 365
    compress
    delaycompress
    notifempty
    create 640 root adm
    postrotate
        systemctl reload rsyslog
    endscript
}
```

**LAB 3** - Système de monitoring complet : `S1_S1_S6_lab3_monitoring.sh`

**Énoncé du LAB 3** :

- **Objectif** : Développer un système de monitoring avec alertes proactives
- **Durée estimée** : 20 minutes
- **Points** : 5 points
- **Contexte** : Surveillance complète de l'infrastructure avec tableau de bord
- **Fichier de travail** : `S1_S1_S6_lab3_monitoring.sh`

### Alerting intelligent

#### Script d'alerting avancé avec seuils adaptatifs

```bash
#!/bin/bash
# /opt/monitoring/smart-alerting.sh
# Système d'alerting intelligent avec seuils adaptatifs

set -euo pipefail

readonly CONFIG_FILE="/etc/monitoring/alerting.conf"
readonly STATE_FILE="/var/lib/monitoring/alerting.state"
readonly LOG_FILE="/var/log/monitoring/alerting.log"

# Seuils par défaut
declare -A DEFAULT_THRESHOLDS=(
    ["cpu_warning"]="70"
    ["cpu_critical"]="90"
    ["memory_warning"]="80"
    ["memory_critical"]="95"
    ["disk_warning"]="85"
    ["disk_critical"]="95"
    ["load_warning"]="5.0"
    ["load_critical"]="10.0"
)

# État des alertes (pour éviter spam)
declare -A alert_state
declare -A last_alert_time
declare -A alert_count

load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        source "$CONFIG_FILE"
    fi
}

load_state() {
    if [[ -f "$STATE_FILE" ]]; then
        source "$STATE_FILE"
    fi
}

save_state() {
    {
        for key in "${!alert_state[@]}"; do
            echo "alert_state[$key]=${alert_state[$key]}"
        done
        for key in "${!last_alert_time[@]}"; do
            echo "last_alert_time[$key]=${last_alert_time[$key]}"
        done
        for key in "${!alert_count[@]}"; do
            echo "alert_count[$key]=${alert_count[$key]}"
        done
    } > "$STATE_FILE"
}

log_alert() {
    local level="$1"
    local metric="$2"
    local value="$3"
    local threshold="$4"
    local message="$5"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $metric=$value (seuil: $threshold) - $message" >> "$LOG_FILE"
}

should_send_alert() {
    local alert_key="$1"
    local current_time=$(date +%s)
    local last_time=${last_alert_time[$alert_key]:-0}
    local min_interval=300  # 5 minutes minimum entre alertes

    # Vérifier si assez de temps s'est écoulé
    if [[ $((current_time - last_time)) -lt $min_interval ]]; then
        return 1
    fi

    return 0
}

send_alert() {
    local level="$1"
    local metric="$2"
    local value="$3"
    local threshold="$4"
    local message="$5"

    local alert_key="${metric}_${level}"

    if ! should_send_alert "$alert_key"; then
        return
    fi

    # Couleur selon niveau
    local color
    case "$level" in
        "CRITICAL") color="danger" ;;
        "WARNING") color="warning" ;;
        *) color="good" ;;
    esac

    # Webhook Slack
    if [[ -n "${SLACK_WEBHOOK:-}" ]]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{
                \"attachments\": [{
                    \"color\": \"$color\",
                    \"title\": \"Alert: $metric\",
                    \"fields\": [
                        {\"title\": \"Level\", \"value\": \"$level\", \"short\": true},
                        {\"title\": \"Value\", \"value\": \"$value\", \"short\": true},
                        {\"title\": \"Threshold\", \"value\": \"$threshold\", \"short\": true},
                        {\"title\": \"Message\", \"value\": \"$message\", \"short\": false}
                    ]
                }]
            }" \
            "$SLACK_WEBHOOK" 2>/dev/null || true
    fi

    # Email
    if [[ -n "${ALERT_EMAIL:-}" ]]; then
        echo "$message" | mail -s "[$level] Alert: $metric" "$ALERT_EMAIL"
    fi

    # Mettre à jour l'état
    alert_state[$alert_key]="$level"
    last_alert_time[$alert_key]=$(date +%s)
    alert_count[$alert_key]=$((${alert_count[$alert_key]:-0} + 1))

    log_alert "$level" "$metric" "$value" "$threshold" "$message"
}

check_metric() {
    local metric="$1"
    local current_value="$2"
    local warning_threshold="$3"
    local critical_threshold="$4"
    local unit="$5"

    local message

    if (( $(echo "$current_value >= $critical_threshold" | bc -l) )); then
        message="Valeur critique détectée pour $metric: ${current_value}${unit}"
        send_alert "CRITICAL" "$metric" "${current_value}${unit}" "${critical_threshold}${unit}" "$message"
    elif (( $(echo "$current_value >= $warning_threshold" | bc -l) )); then
        message="Valeur élevée détectée pour $metric: ${current_value}${unit}"
        send_alert "WARNING" "$metric" "${current_value}${unit}" "${warning_threshold}${unit}" "$message"
    else
        # Récupération d'une alerte
        local alert_key="${metric}_CRITICAL"
        if [[ "${alert_state[$alert_key]:-}" == "CRITICAL" ]] || [[ "${alert_state[$alert_key]:-}" == "WARNING" ]]; then
            message="Récupération détectée pour $metric: ${current_value}${unit}"
            send_alert "RECOVERY" "$metric" "${current_value}${unit}" "${warning_threshold}${unit}" "$message"
            unset alert_state[$alert_key]
        fi
    fi
}

check_cpu() {
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    check_metric "CPU" "$cpu_usage" "${DEFAULT_THRESHOLDS[cpu_warning]}" "${DEFAULT_THRESHOLDS[cpu_critical]}" "%"
}

check_memory() {
    local mem_usage=$(free | awk '/^Mem:/{printf "%.1f", $3/$2*100}')
    check_metric "Memory" "$mem_usage" "${DEFAULT_THRESHOLDS[memory_warning]}" "${DEFAULT_THRESHOLDS[memory_critical]}" "%"
}

check_disk() {
    while read -r line; do
        local usage=$(echo "$line" | awk '{print $5}' | cut -d'%' -f1)
        local mount=$(echo "$line" | awk '{print $6}')

        if [[ "$usage" -gt 0 ]]; then
            check_metric "Disk_$mount" "$usage" "${DEFAULT_THRESHOLDS[disk_warning]}" "${DEFAULT_THRESHOLDS[disk_critical]}" "%"
        fi
    done < <(df | grep -E "^/dev" | grep -v "/boot")
}

check_load() {
    local load_avg=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | cut -d',' -f1 | xargs)
    check_metric "Load" "$load_avg" "${DEFAULT_THRESHOLDS[load_warning]}" "${DEFAULT_THRESHOLDS[load_critical]}" ""
}

main() {
    load_config
    load_state

    check_cpu
    check_memory
    check_disk
    check_load

    save_state
}

main "$@"
```

---

## 4. Scripting avancé pour l'automatisation DevOps

### Bonnes pratiques pour scripts robustes

#### Template de script professionnel

```bash
#!/bin/bash
# Template de script robuste pour DevOps
# Version: 2.0
# Auteur: DevOps Team

# === CONFIGURATION STRICTE ===
set -euo pipefail                 # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'                      # Secure Internal Field Separator

# === VARIABLES GLOBALES ===
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="2.0"
readonly LOG_DIR="/var/log/scripts"
readonly LOG_FILE="$LOG_DIR/${SCRIPT_NAME%.sh}.log"
readonly CONFIG_FILE="/etc/scripts/${SCRIPT_NAME%.sh}.conf"
readonly LOCK_FILE="/var/run/${SCRIPT_NAME%.sh}.lock"

# Variables de configuration avec valeurs par défaut
DRY_RUN=${DRY_RUN:-false}
VERBOSE=${VERBOSE:-false}
DEBUG=${DEBUG:-false}

# === FONCTIONS UTILITAIRES ===
log() {
    local level="$1"
    local color="$2"
    shift 2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] [$level] $*"

    # Couleurs pour la console
    local red='\033[0;31m'
    local yellow='\033[1;33m'
    local green='\033[0;32m'
    local blue='\033[0;34m'
    local nc='\033[0m'

    # Affichage console avec couleur
    echo -e "${color}${message}${nc}" >&2

    # Log dans fichier sans couleur
    echo "$message" >> "$LOG_FILE"
}

log_debug() { [[ "$DEBUG" == "true" ]] && log "DEBUG" '\033[0;36m' "$@" || true; }
log_info() { [[ "$VERBOSE" == "true" ]] && log "INFO" '\033[0;32m' "$@" || true; }
log_warn() { log "WARN" '\033[1;33m' "$@"; }
log_error() { log "ERROR" '\033[0;31m' "$@"; }
log_fatal() { log "FATAL" '\033[1;31m' "$@"; exit 1; }

# Fonction pour exécution avec protection dry-run
execute() {
    local description="$1"
    shift

    log_info "Exécution: $description"
    log_debug "Commande: $*"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_warn "DRY-RUN: $*"
        return 0
    fi

    if ! "$@"; then
        log_error "Échec de l'exécution: $description"
        return 1
    fi

    log_debug "Succès: $description"
    return 0
}

# Vérification des prérequis
check_prerequisites() {
    log_info "Vérification des prérequis"

    # Vérifier les commandes requises
    local required_commands=("curl" "jq" "rsync" "systemctl")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" >/dev/null 2>&1; then
            log_fatal "Commande requise manquante: $cmd"
        fi
    done

    # Vérifier les permissions
    if [[ $EUID -ne 0 ]] && [[ "${REQUIRE_ROOT:-true}" == "true" ]]; then
        log_fatal "Ce script nécessite les privilèges root"
    fi

    # Créer les répertoires nécessaires
    execute "Création répertoire logs" mkdir -p "$LOG_DIR"

    # Charger la configuration si elle existe
    if [[ -f "$CONFIG_FILE" ]]; then
        log_info "Chargement configuration: $CONFIG_FILE"
        source "$CONFIG_FILE"
    fi

    log_info "Prérequis validés"
}

# Gestion du verrou pour éviter les exécutions multiples
acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local pid=$(cat "$LOCK_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log_fatal "Script déjà en cours d'exécution (PID: $pid)"
        else
            log_warn "Fichier verrou orphelin détecté, suppression"
            rm -f "$LOCK_FILE"
        fi
    fi

    echo $$ > "$LOCK_FILE"
    log_debug "Verrou acquis: $LOCK_FILE"
}

release_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        rm -f "$LOCK_FILE"
        log_debug "Verrou libéré: $LOCK_FILE"
    fi
}

# Fonction de nettoyage appelée à la sortie
cleanup() {
    local exit_code=$?

    log_info "Nettoyage en cours (code de sortie: $exit_code)"

    # Libérer le verrou
    release_lock

    # Nettoyage personnalisé
    cleanup_custom

    # Log de fin
    if [[ $exit_code -eq 0 ]]; then
        log_info "Script terminé avec succès"
    else
        log_error "Script terminé avec erreur (code: $exit_code)"
    fi
}

cleanup_custom() {
    # Fonction à surcharger pour nettoyage spécifique
    :
}

# Gestion des signaux
handle_signal() {
    local signal="$1"
    log_warn "Signal reçu: $signal"
    cleanup
    exit 130
}

# Configuration des gestionnaires de signaux
trap 'handle_signal SIGINT' INT
trap 'handle_signal SIGTERM' TERM
trap cleanup EXIT

# Fonction d'aide
usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Description: Script template pour automatisation DevOps

Options:
    -h, --help      Afficher cette aide
    -v, --verbose   Mode verbeux
    -d, --debug     Mode debug
    -n, --dry-run   Mode simulation (pas d'exécution réelle)
    --version       Afficher la version

Variables d'environnement:
    DRY_RUN         Mode simulation (true/false)
    VERBOSE         Mode verbeux (true/false)
    DEBUG           Mode debug (true/false)

Exemples:
    $SCRIPT_NAME --verbose
    DRY_RUN=true $SCRIPT_NAME
    $SCRIPT_NAME --debug --dry-run

EOF
}

# Analyse des arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -d|--debug)
                DEBUG=true
                VERBOSE=true  # Debug implique verbose
                shift
                ;;
            -n|--dry-run)
                DRY_RUN=true
                shift
                ;;
            --version)
                echo "$SCRIPT_NAME version $SCRIPT_VERSION"
                exit 0
                ;;
            *)
                log_error "Option inconnue: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# === FONCTIONS MÉTIER ===
# Remplacer par la logique spécifique du script

main_logic() {
    log_info "Début de la logique principale"

    # Exemple d'opérations
    execute "Test de connectivité" ping -c 1 google.com
    execute "Vérification espace disque" df -h
    execute "État des services" systemctl status --no-pager

    log_info "Logique principale terminée"
}

# === FONCTION PRINCIPALE ===
main() {
    log_info "Démarrage de $SCRIPT_NAME v$SCRIPT_VERSION"

    parse_arguments "$@"
    check_prerequisites
    acquire_lock

    # Logique principale
    main_logic

    log_info "Exécution réussie"
}

# === POINT D'ENTRÉE ===
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

**LAB 4 - Challenge** - Automation complète : `S1_S1_S6_lab4_projet_automation.sh`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge optionnel permet d'approfondir tous les concepts vus en séance
et de créer une infrastructure d'automatisation complète en autonomie.

- **Objectif** : Développer une solution d'automatisation DevOps complète avec services, monitoring et alerting
- **Statut** : Activité bonus, hors des 2 heures de séance
- **Durée estimée** : 45-60 minutes
- **Niveau** : Avancé, intégration de tous les concepts
- **Contexte** : Infrastructure de production avec haute disponibilité
- **Livrables** : Services systemd, timers, scripts monitoring, dashboard de supervision
- **Points** : 15 points (challenge d'excellence)

### Application pratique avancée

Les concepts suivants seront mis en application dans le LAB 4 Challenge :

### Scripts d'automatisation spécialisés

#### Script de sauvegarde intelligent

```bash
#!/bin/bash
# Script de sauvegarde intelligent avec rotation et vérification
# /opt/scripts/intelligent-backup.sh

source /opt/scripts/common-functions.sh

# Configuration
readonly BACKUP_SOURCES=("/etc" "/var/www" "/opt/applications" "/home")
readonly BACKUP_DESTINATION="/backup/$(hostname)"
readonly RETENTION_DAYS=30
readonly COMPRESSION_LEVEL=6
readonly ENCRYPTION_KEY="/etc/backup/backup.key"

backup_directory() {
    local source="$1"
    local dest="$2"
    local date_suffix=$(date '+%Y%m%d_%H%M%S')
    local backup_name="$(basename "$source")_${date_suffix}"
    local backup_path="$dest/$backup_name"

    log_info "Sauvegarde de $source vers $backup_path"

    # Créer archive compressée
    execute "Création archive $backup_name" \
        tar -czf "$backup_path.tar.gz" \
        --exclude='*.tmp' \
        --exclude='*.log' \
        --exclude='.cache' \
        -C "$(dirname "$source")" \
        "$(basename "$source")"

    # Chiffrement si clé disponible
    if [[ -f "$ENCRYPTION_KEY" ]]; then
        execute "Chiffrement archive $backup_name" \
            gpg --symmetric --cipher-algo AES256 \
            --passphrase-file "$ENCRYPTION_KEY" \
            --batch --yes \
            "$backup_path.tar.gz"

        execute "Suppression archive non chiffrée" \
            rm -f "$backup_path.tar.gz"

        backup_path="$backup_path.tar.gz.gpg"
    else
        backup_path="$backup_path.tar.gz"
    fi

    # Vérification intégrité
    local checksum=$(sha256sum "$backup_path" | awk '{print $1}')
    echo "$checksum  $backup_path" > "$backup_path.sha256"

    log_info "Sauvegarde terminée: $backup_path"
    echo "$backup_path"
}

cleanup_old_backups() {
    local backup_dir="$1"

    log_info "Nettoyage des sauvegardes anciennes (>${RETENTION_DAYS} jours)"

    find "$backup_dir" -type f -name "*.tar.gz*" -mtime +$RETENTION_DAYS -delete
    find "$backup_dir" -type f -name "*.sha256" -mtime +$RETENTION_DAYS -delete

    log_info "Nettoyage terminé"
}

verify_backup() {
    local backup_file="$1"
    local checksum_file="$backup_file.sha256"

    if [[ ! -f "$checksum_file" ]]; then
        log_warn "Fichier checksum manquant: $checksum_file"
        return 1
    fi

    if sha256sum -c "$checksum_file" >/dev/null 2>&1; then
        log_info "Vérification intégrité réussie: $backup_file"
        return 0
    else
        log_error "Échec vérification intégrité: $backup_file"
        return 1
    fi
}

send_backup_report() {
    local status="$1"
    local backup_files=("${@:2}")

    local report_file="/tmp/backup-report-$(date '+%Y%m%d').txt"

    {
        echo "Rapport de sauvegarde - $(date)"
        echo "=============================="
        echo "Statut: $status"
        echo "Serveur: $(hostname)"
        echo "Sauvegardes créées:"
        for file in "${backup_files[@]}"; do
            echo "  - $file ($(du -h "$file" | cut -f1))"
        done
        echo
        echo "Espace disque backup:"
        df -h "$BACKUP_DESTINATION"
    } > "$report_file"

    if [[ -n "${BACKUP_EMAIL:-}" ]]; then
        mail -s "Rapport sauvegarde $(hostname)" "$BACKUP_EMAIL" < "$report_file"
    fi

    rm -f "$report_file"
}

main_logic() {
    local backup_files=()
    local failed_backups=()

    # Créer répertoire de destination
    execute "Création répertoire backup" mkdir -p "$BACKUP_DESTINATION"

    # Sauvegarder chaque source
    for source in "${BACKUP_SOURCES[@]}"; do
        if [[ -d "$source" ]]; then
            if backup_file=$(backup_directory "$source" "$BACKUP_DESTINATION"); then
                if verify_backup "$backup_file"; then
                    backup_files+=("$backup_file")
                else
                    failed_backups+=("$source")
                fi
            else
                failed_backups+=("$source")
            fi
        else
            log_warn "Source inexistante: $source"
        fi
    done

    # Nettoyage des anciennes sauvegardes
    cleanup_old_backups "$BACKUP_DESTINATION"

    # Rapport
    if [[ ${#failed_backups[@]} -eq 0 ]]; then
        send_backup_report "SUCCESS" "${backup_files[@]}"
        log_info "Toutes les sauvegardes réussies"
    else
        send_backup_report "PARTIAL_FAILURE" "${backup_files[@]}"
        log_error "Échecs de sauvegarde: ${failed_backups[*]}"
        exit 1
    fi
}
```

---

## 5. Récapitulatif et prochaines étapes

### Points clés de la séance

Cette séance a couvert l'administration avancée des services et l'automatisation Linux :

#### Compétences acquises

- **Administration systemd** : Configuration de services complexes avec dépendances, monitoring et sécurité
- **Automatisation** : Planification avec cron et systemd timers, scripts robustes pour DevOps
- **Monitoring** : Surveillance proactive des services, gestion des logs et alerting intelligent
- **Scripting avancé** : Bonnes pratiques pour scripts de production, gestion d'erreurs et logging

#### Technologies maîtrisées

- **systemd** : Units, dependencies, timers, security settings
- **cron** : Planification traditionnelle, crontabs système et utilisateur
- **rsyslog/logrotate** : Gestion centralisée des logs avec rotation automatique
- **bash scripting** : Scripts robustes avec gestion d'erreurs et logging professionnel

### Applications pratiques

Les compétences développées s'appliquent directement à :

- **Infrastructure as Code** : Automatisation du déploiement et de la configuration
- **Site Reliability Engineering** : Monitoring, alerting et incident response
- **CI/CD Pipelines** : Scripts d'automatisation pour intégration continue
- **Production Operations** : Gestion quotidienne des services en production

### Préparation pour les séances suivantes

Cette séance prépare aux modules avancés :

- **Séance 5** : Scripting bash avancé et automation complexe
- **Sprint 2** : Containerisation avec Docker (services containerisés)
- **Sprint 3** : Orchestration Kubernetes (services distribués)
- **Sprint 5** : Observabilité et SRE (monitoring avancé)

---

## 6. Ressources complémentaires

### Documentation officielle

- **systemd** : https://systemd.io/ - Documentation complète
- **cron** : https://linux.die.net/man/5/crontab - Format crontab
- **rsyslog** : https://www.rsyslog.com/doc/ - Configuration logging
- **logrotate** : https://linux.die.net/man/8/logrotate - Rotation des logs

### Outils recommandés

- **systemd-analyze** : Analyse des performances de démarrage
- **journalctl** : Consultation des logs systemd
- **htop/top** : Monitoring des ressources système
- **prometheus/grafana** : Stack de monitoring moderne

### Bonnes pratiques DevOps

- **Infrastructure as Code** : Versionner les configurations systemd
- **Monitoring proactif** : Alerter avant que les problèmes deviennent critiques
- **Documentation** : Documenter tous les services et processus automatisés
- **Tests** : Valider les scripts en environnement de développement
- **Sécurité** : Appliquer le principe du moindre privilège

### Formation continue

- **Certification** : Linux Professional Institute (LPIC), Red Hat (RHCSA/RHCE)
- **Veille technologique** : Suivre les évolutions systemd et bonnes pratiques DevOps
- **Communauté** : Participer aux forums Linux et DevOps

---

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 6_
