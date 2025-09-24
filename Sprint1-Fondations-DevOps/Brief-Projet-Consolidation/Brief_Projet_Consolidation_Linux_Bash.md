# Simplon Maghreb - Formation DevOps

# Brief Projet - Consolidation Linux et Bash Scripting

## Objectifs pédagogiques

- Consolider les fondamentaux Linux et administration système
- Appliquer les compétences Bash dans un contexte d'infrastructure
- Intégrer gestion des processus, services et monitoring
- Développer un outil DevOps complet et modulaire

## Objectifs techniques

Linux administration, Bash scripting, gestion processus, services système, monitoring, automation, scripts modulaires, gestion erreurs

## Contexte du projet

En tant qu'administrateur DevOps, vous devez créer un **outil d'administration système complet** qui automatise la surveillance et la maintenance d'un serveur Linux en production. Cet outil doit combiner vos connaissances Linux avec vos compétences en scripting Bash.

## Cahier des charges

### Mission principale

Développer **SysMonitor Pro** : un script Bash modulaire qui surveille et maintient automatiquement un serveur Linux en combinant :

- **Semaine 1** : Fondamentaux Linux (fichiers, processus, réseau, services)
- **Séance 1 Bash** : Scripts de base et structures de contrôle
- **Séance 2 Bash** : Fonctions modulaires et gestion d'erreurs avancée

### Architecture du projet

```
SysMonitor-Pro/
├── main.sh                    # Script principal
├── config/
│   ├── settings.conf          # Configuration générale
│   └── thresholds.conf        # Seuils d'alerte
├── lib/
│   ├── logger.sh              # Système de logging
│   ├── system_monitor.sh      # Monitoring système
│   ├── process_manager.sh     # Gestion des processus
│   ├── service_checker.sh     # Vérification services
│   └── network_utils.sh       # Utilitaires réseau
├── reports/
│   └── system_report_YYYYMMDD.html
└── logs/
    └── sysmonitor.log
```

## Fonctionnalités requises

### 1. Monitoring Système (Semaine 1 - Linux)

#### 1.1 Surveillance des ressources

```bash
# Fonctions à implémenter dans lib/system_monitor.sh
monitor_cpu_usage()      # Utilisation CPU avec seuils
monitor_memory_usage()   # Consommation RAM et SWAP
monitor_disk_space()     # Espace disque par partition
monitor_system_load()    # Load average et nombre de processus
```

**Compétences Semaine 1 appliquées** :

- Commandes système : `top`, `free`, `df`, `uptime`
- Lecture fichiers `/proc` : `/proc/cpuinfo`, `/proc/meminfo`
- Analyse des partitions et points de montage

#### 1.2 Gestion des processus avancée

```bash
# Fonctions à implémenter dans lib/process_manager.sh
list_top_processes()        # Top 10 processus consommateurs
find_zombie_processes()     # Détection processus zombies
monitor_specific_process()  # Surveillance processus critique
kill_problematic_process()  # Arrêt sécurisé de processus
```

**Compétences Semaine 1 appliquées** :

- Commandes processus : `ps`, `pgrep`, `pkill`, `jobs`
- Signaux système : SIGTERM, SIGKILL, SIGHUP
- États des processus : running, sleeping, zombie

### 2. Vérification Services (Semaine 1 - Services)

#### 2.1 Monitoring des services système

```bash
# Fonctions à implémenter dans lib/service_checker.sh
check_critical_services()   # Vérification services critiques
restart_failed_service()    # Redémarrage automatique
check_service_logs()        # Analyse logs d'erreur
validate_service_config()   # Validation configuration
```

**Services critiques à surveiller** :

- **SSH** : Accès distant sécurisé
- **Cron** : Planification des tâches
- **Rsyslog** : Centralisation des logs
- **NetworkManager** : Gestion réseau
- **Firewall** : Sécurité réseau

**Compétences Semaine 1 appliquées** :

- Systemd : `systemctl status/start/stop/restart`
- Analyse logs : `journalctl`, `/var/log/`
- Configuration services : fichiers `.service`

### 3. Surveillance Réseau (Semaine 1 - Réseaux)

#### 3.1 Monitoring de la connectivité

```bash
# Fonctions à implémenter dans lib/network_utils.sh
check_network_connectivity()  # Test connectivité internet
monitor_network_interfaces()  # État interfaces réseau
check_open_ports()           # Scan des ports ouverts
monitor_network_traffic()    # Analyse du trafic réseau
```

**Compétences Semaine 1 appliquées** :

- Commandes réseau : `ping`, `netstat`, `ss`, `ip`
- Configuration réseau : `/etc/network/interfaces`
- Diagnostic : `traceroute`, `nslookup`, `dig`

### 4. Scripts Bash Modulaires (Séances 1-2)

#### 4.1 Structure modulaire (Séance 2)

```bash
# main.sh - Script principal avec orchestration
source "$(dirname "$0")/lib/logger.sh"
source "$(dirname "$0")/lib/system_monitor.sh"
source "$(dirname "$0")/config/settings.conf"

main() {
    log_info "Début monitoring SysMonitor Pro"

    # Validation environnement
    validate_prerequisites || exit 1

    # Modules de surveillance
    run_system_monitoring
    run_process_monitoring
    run_service_monitoring
    run_network_monitoring

    # Génération rapport
    generate_system_report

    log_success "Monitoring terminé avec succès"
}

# Gestion d'erreurs avec trap (Séance 2)
cleanup() {
    log_info "Nettoyage en cours..."
    [[ -n "$TEMP_DIR" ]] && rm -rf "$TEMP_DIR"
    exit $?
}
trap cleanup EXIT INT TERM

main "$@"
```

#### 4.2 Gestion d'erreurs robuste (Séance 2)

```bash
# Configuration stricte
set -e          # Arrêt en cas d'erreur
set -u          # Erreur variables non définies
set -o pipefail # Erreur dans les pipes

# Validation des paramètres
validate_input() {
    local input="$1"
    local type="$2"

    case "$type" in
        "threshold")
            [[ "$input" =~ ^[0-9]+$ ]] || return 1
            [[ "$input" -ge 0 && "$input" -le 100 ]] || return 1
            ;;
        "service")
            systemctl list-unit-files | grep -q "^$input" || return 1
            ;;
    esac
    return 0
}
```

#### 4.3 Structures de contrôle avancées (Séance 1)

```bash
# Boucles et conditions (Séance 1)
check_multiple_services() {
    local services=("ssh" "cron" "rsyslog" "networking")
    local failed_services=()

    for service in "${services[@]}"; do
        if ! systemctl is-active --quiet "$service"; then
            failed_services+=("$service")
            log_error "Service $service inactif"
        fi
    done

    # Gestion des échecs multiples
    if [[ ${#failed_services[@]} -gt 0 ]]; then
        log_critical "Services en échec: ${failed_services[*]}"
        return 1
    fi

    return 0
}
```

### 5. Système de Logging et Rapports

#### 5.1 Logging structuré

```bash
# lib/logger.sh - Système de logging avancé
log_with_level() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_file="${LOG_DIR}/sysmonitor.log"

    # Format: [TIMESTAMP] [LEVEL] MESSAGE
    echo "[$timestamp] [$level] $message" | tee -a "$log_file"

    # Envoi syslog pour erreurs critiques
    if [[ "$level" == "CRITICAL" ]]; then
        logger -p local0.err "SysMonitor: $message"
    fi
}

log_info() { log_with_level "INFO" "$1"; }
log_warning() { log_with_level "WARNING" "$1"; }
log_error() { log_with_level "ERROR" "$1"; }
log_critical() { log_with_level "CRITICAL" "$1"; }
```

#### 5.2 Génération de rapports HTML

```bash
generate_system_report() {
    local report_file="reports/system_report_$(date +%Y%m%d_%H%M%S).html"

    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>SysMonitor Pro - Rapport Système</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .critical { background: #e74c3c; color: white; }
        .warning { background: #f39c12; color: white; }
        .success { background: #27ae60; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Rapport SysMonitor Pro</h1>
        <p>Généré le: $(date)</p>
        <p>Serveur: $(hostname)</p>
    </div>
EOF

    # Ajout des sections de monitoring
    add_system_metrics_section >> "$report_file"
    add_process_analysis_section >> "$report_file"
    add_service_status_section >> "$report_file"
    add_network_analysis_section >> "$report_file"

    echo "</body></html>" >> "$report_file"
    log_info "Rapport généré: $report_file"
}
```

## Livrables attendus

### 1. Code source complet

- **main.sh** : Script principal orchestrateur
- **lib/\*** : Modules fonctionnels (5 fichiers)
- **config/\*** : Fichiers de configuration (2 fichiers)

### 2. Documentation technique

- **README.md** : Guide d'installation et utilisation
- **ARCHITECTURE.md** : Documentation de l'architecture
- **CONFIGURATION.md** : Guide de configuration

### 3. Tests et validation

- **tests/** : Scripts de test unitaire pour chaque module
- **Validation** : Preuve de fonctionnement sur système Linux

### 4. Démonstration

- **Exécution live** : Démonstration du monitoring en temps réel
- **Rapport généré** : Présentation du rapport HTML produit
- **Gestion d'erreurs** : Démonstration de la robustesse

## Évaluation par Compétences

### Compétences du Référentiel DevOps Visées

Ce projet permet de valider les compétences suivantes du référentiel officiel DevOps :

#### **C1 - Définir un environnement de développement commun**

**Niveau 1 - Fondamentaux**

- Produire les sources nécessaires (scripts modulaires, configurations)
- Choisir les outils d'automation (Bash, Linux natif)
- Appliquer les principes d'Infrastructure as Code
- Automatiser l'installation et la configuration

**Niveau 2 - Intermédiaire**

- Créer des environnements standardisés et reproductibles
- Intégrer les outils de développement dans l'automation
- Gérer la configuration centralisée et versionnée

#### **C3 - Concevoir les éléments de configuration de l'infrastructure**

**Niveau 1 - **

- Utiliser des gestionnaires de configuration (scripts Bash)
- Automatiser les actions de gestion et provisionnement
- Configurer l'infrastructure de manière déclarative

**Niveau 2 - **

- Créer des configurations complexes multi-services
- Gérer les dépendances entre composants d'infrastructure
- Implémenter des processus de validation de configuration

#### **C6 - Automatiser le monitorage des éléments d'infrastructure et des applications**

**Niveau 1 - **

- Configurer les outils de monitoring système
- Définir les métriques critiques à surveiller
- Mettre en place des alertes automatiques

**Niveau 2 - **

- Développer des outils de monitoring personnalisés
- Créer des dashboards et rapports automatisés
- Implémenter une surveillance prédictive

### Critères de Validation par Compétence

#### **C1 - Définir un environnement de développement commun** VALIDE/NON VALIDE

**Niveau 1 - Validation**

**Critères de validation** :

- [ ] Les scripts d'installation automatisent complètement le déploiement
- [ ] L'architecture modulaire permet la reproductibilité
- [ ] Les configurations sont externalisées et versionnables
- [ ] Les principes Infrastructure as Code sont appliqués

**Preuves attendues** :

- Structure modulaire SysMonitor-Pro fonctionnelle
- Scripts d'installation automatique (main.sh + modules)
- Configuration externalisée (settings.conf, thresholds.conf)
- Documentation de l'architecture et des choix techniques

**Modalités de validation** :

- Démonstration installation automatique sur système Linux
- Test de reproductibilité avec différentes configurations
- Vérification du respect des principes Infrastructure as Code
- Validation de la modularité et réutilisabilité du code

**Niveau 2 - Validation**

**Critères de validation** :

- [ ] Environnement standardisé pour monitoring multi-serveurs
- [ ] Intégration native avec l'écosystème Linux/DevOps
- [ ] Configuration centralisée et gestion des profils
- [ ] Templates et personnalisation avancée

**Preuves attendues** :

- SysMonitor-Pro déployable sur multiples environnements
- Intégration avec outils système existants (systemd, syslog)
- Système de profils et templates de configuration
- Processus de standardisation documenté et testé

#### **C3 - Concevoir les éléments de configuration de l'infrastructure** VALIDE/NON VALIDE

**Niveau 1 - Validation**

**Critères de validation** :

- [ ] Scripts Bash gèrent automatiquement la configuration
- [ ] Provisionnement automatisé des services de monitoring
- [ ] Configuration déclarative via fichiers externes
- [ ] Processus de validation de configuration implémentés

**Preuves attendues** :

- Modules lib/\*.sh automatisent la configuration des services
- Provisionnement automatique du monitoring système
- Fichiers de configuration déclaratifs (settings.conf, thresholds.conf)
- Validation automatique des paramètres et seuils

**Modalités de validation** :

- Revue des scripts de configuration automatisée
- Test du provisionnement automatique des services
- Validation de l'approche déclarative vs impérative
- Vérification des processus de validation de configuration

**Niveau 2 - Validation**

**Critères de validation** :

- [ ] Configuration complexe multi-services maîtrisée
- [ ] Gestion avancée des dépendances entre composants
- [ ] Processus de validation sophistiqués implémentés
- [ ] Architecture évolutive et extensible

**Preuves attendues** :

- Monitoring intégré de services interdépendants (SSH, cron, réseau)
- Gestion automatique des dépendances de services
- Validation multi-niveaux (paramètres, services, connectivité)
- Architecture permettant l'ajout facile de nouveaux modules

#### **C6 - Automatiser le monitorage des éléments d'infrastructure et des applications** VALIDE/NON VALIDE

**Niveau 1 - Validation**

**Critères de validation** :

- [ ] Monitoring système automatisé et opérationnel
- [ ] Métriques critiques définies et collectées
- [ ] Système d'alertes automatiques fonctionnel
- [ ] Rapports de monitoring générés automatiquement

**Preuves attendues** :

- Modules de monitoring fonctionnels (system_monitor.sh, process_manager.sh, etc.)
- Collecte automatique de métriques (CPU, mémoire, disque, processus, services)
- Système d'alertes configuré avec seuils personnalisables
- Génération automatique de rapports HTML structurés

**Modalités de validation** :

- Démonstration du monitoring en temps réel
- Test des alertes avec dépassement de seuils
- Validation de la collecte de métriques système
- Vérification de la génération automatique de rapports

**Niveau 2 - Validation**

**Critères de validation** :

- [ ] Outils de monitoring personnalisés développés
- [ ] Dashboards avancés et visualisations interactives
- [ ] Analyse prédictive et détection d'anomalies
- [ ] Intégration avec systèmes externes d'alerting

**Preuves attendues** :

- SysMonitor-Pro avec fonctionnalités avancées personnalisées
- Rapports HTML avec graphiques et visualisations interactives
- Algorithmes de détection d'anomalies implémentés
- Intégration avec syslog, email ou webhooks pour alertes

### Validation Globale du Projet

**Statut de validation** : VALIDE / NON VALIDE

**Conditions de validation** :

- **Validation de base** : C1 Niveau 1 + C3 Niveau 1 + C6 Niveau 1
- **Validation avancée** : Au moins 2 compétences Niveau 2 validées
- **Validation excellente** : Toutes les compétences Niveau 2 validées

**Actions en cas de non-validation** :

1. **Diagnostic précis** des compétences non validées avec le formateur
2. **Plan de remédiation** personnalisé par compétence manquante
3. **Accompagnement technique** ciblé sur les lacunes identifiées
4. **Nouvelle évaluation** avec critères ajustés selon les besoins

### Modalités d'Évaluation

#### **Évaluation Pratique**

**Démonstration technique** (20 minutes) :

1. **Installation automatique** : Déploiement de SysMonitor-Pro (5 min)
2. **Monitoring en action** : Démonstration des modules de surveillance (10 min)
3. **Gestion d'erreurs** : Test de robustesse et récupération (5 min)

**Questions de validation** :

- Expliquez l'architecture modulaire de votre solution
- Démontrez la configuration déclarative de votre monitoring
- Comment votre solution respecte-t-elle les principes Infrastructure as Code ?
- Présentez le système d'alertes et de rapports automatiques

#### **Évaluation Documentaire**

**Code source** :

- Structure modulaire et organisation du code
- Qualité des scripts Bash et gestion d'erreurs
- Configuration externalisée et documentation

**Documentation technique** :

- Architecture et choix techniques justifiés
- Guide d'installation et configuration
- Procédures de maintenance et troubleshooting

#### **Critères Transversaux**

**Innovation et qualité** :

- Fonctionnalités avancées au-delà des exigences minimales
- Optimisations techniques et bonnes pratiques
- Extensibilité et évolutivité de la solution

**Professionnalisme** :

- Respect des standards DevOps et Linux
- Documentation complète et maintenue
- Code propre et maintenable

## Planning de réalisation

### Phase 1 : Architecture et fondations (2 jours)

- **Jour 1** : Structure du projet et modules de base
- **Jour 2** : Système de logging et configuration

### Phase 2 : Modules de monitoring (3 jours)

- **Jour 3** : Module système (CPU, mémoire, disque)
- **Jour 4** : Module processus et services
- **Jour 5** : Module réseau et connectivité

### Phase 3 : Intégration et finition (2 jours)

- **Jour 6** : Intégration complète et tests
- **Jour 7** : Documentation et démonstration

## Ressources et outils

### Commandes Linux essentielles

```bash
# Monitoring système
top, htop, free, df, du, uptime, vmstat, iostat

# Gestion processus
ps, pgrep, pkill, jobs, nohup, screen, tmux

# Services système
systemctl, journalctl, service, chkconfig

# Réseau
ping, netstat, ss, ip, iptables, tcpdump, nmap

# Fichiers et logs
find, grep, awk, sed, tail, head, less
```

### Documentation de référence

- **Linux** : Man pages système (`man systemctl`, `man ps`)
- **Bash** : Advanced Bash-Scripting Guide
- **Administration** : Linux System Administrator's Guide
- **DevOps** : Site Reliability Engineering (Google)

## Évaluation Finale et Soutenance

### Soutenance par Compétences (30 minutes)

#### **Phase 1 : Présentation Architecture (8 minutes)**

- **Architecture modulaire** : Explication de la structure SysMonitor-Pro
- **Choix techniques** : Justification des solutions Infrastructure as Code
- **Configuration** : Démonstration de l'approche déclarative

_Validation : C1 et C3 - Conception et architecture_

#### **Phase 2 : Démonstration Technique (15 minutes)**

- **Installation automatique** : Déploiement complet de la solution (3 min)
- **Monitoring en action** : Surveillance système temps réel (8 min)
- **Gestion d'erreurs** : Test de robustesse et récupération (4 min)

_Validation : C1, C3, C6 - Fonctionnement opérationnel_

#### **Phase 3 : Questions Compétences (7 minutes)**

- **C1** : "Comment votre solution garantit-elle la reproductibilité ?"
- **C3** : "Expliquez votre approche de configuration déclarative"
- **C6** : "Démontrez l'efficacité de votre système d'alertes"

_Validation : Maîtrise conceptuelle des compétences_

### Grille de Validation par Compétence

#### **C1 - Environnement de développement commun**

| Niveau       | Critères de Validation                                                      | Statut              |
| ------------ | --------------------------------------------------------------------------- | ------------------- |
| **Niveau 1** | Structure modulaire + Installation automatique + Configuration externalisée | VALIDE / NON VALIDE |
| **Niveau 2** | Standardisation multi-environnements + Templates + Intégration avancée      | VALIDE / NON VALIDE |

#### **C3 - Configuration de l'infrastructure**

| Niveau       | Critères de Validation                                                | Statut              |
| ------------ | --------------------------------------------------------------------- | ------------------- |
| **Niveau 1** | Scripts de configuration + Provisionnement automatique + Validation   | VALIDE / NON VALIDE |
| **Niveau 2** | Configuration complexe + Gestion dépendances + Architecture évolutive | VALIDE / NON VALIDE |

#### **C6 - Automatisation du monitorage**

| Niveau       | Critères de Validation                                           | Statut              |
| ------------ | ---------------------------------------------------------------- | ------------------- |
| **Niveau 1** | Monitoring automatique + Métriques définies + Alertes + Rapports | VALIDE / NON VALIDE |
| **Niveau 2** | Outils personnalisés + Dashboards avancés + Détection anomalies  | VALIDE / NON VALIDE |

### Résultats de Validation Globale

#### **Validation de Base** ✅

**Condition** : C1 Niveau 1 + C3 Niveau 1 + C6 Niveau 1 = TOUTES VALIDÉES

**Signification** : Maîtrise des fondamentaux DevOps pour l'infrastructure et le monitoring

#### **Validation Avancée** ⭐

**Condition** : Validation de Base + Au moins 2 compétences Niveau 2 validées

**Signification** : Compétences DevOps intermédiaires avec spécialisation

#### **Validation Excellente** 🏆

**Condition** : Toutes les compétences Niveau 2 validées

**Signification** : Maîtrise avancée complète de l'infrastructure et monitoring DevOps

### Actions de Remédiation

#### **En cas de compétence NON VALIDÉE**

**Processus de remédiation** :

1. **Diagnostic immédiat** : Identification précise des lacunes
2. **Plan personnalisé** : Actions correctives spécifiques à la compétence
3. **Accompagnement ciblé** : Support technique sur les points faibles
4. **Nouvelle évaluation** : Test de validation dans un délai adapté

**Exemples de remédiation** :

**C1 NON VALIDÉE** :

- Revoir l'architecture modulaire et la séparation des responsabilités
- Améliorer les scripts d'installation automatique
- Renforcer la configuration externalisée et la documentation

**C3 NON VALIDÉE** :

- Approfondir les scripts de configuration et provisionnement
- Améliorer la gestion des dépendances entre services
- Renforcer la validation de configuration

**C6 NON VALIDÉE** :

- Revoir les modules de monitoring et collecte de métriques
- Améliorer le système d'alertes et seuils
- Perfectionner la génération de rapports automatiques

### Conseils pour la Réussite

#### **Préparation de la soutenance**

**Pour C1 - Environnement de développement** :

- Préparez une démonstration d'installation automatique fluide
- Documentez clairement votre architecture modulaire
- Justifiez vos choix d'Infrastructure as Code

**Pour C3 - Configuration infrastructure** :

- Montrez la robustesse de vos scripts de configuration
- Démontrez la validation automatique des paramètres
- Expliquez la gestion des dépendances entre services

**Pour C6 - Monitoring automatisé** :

- Préparez des scénarios de test pour déclencher les alertes
- Montrez des rapports HTML générés automatiquement
- Démontrez la surveillance en temps réel

#### **Pièges à éviter**

- **Ne pas tester** : Validez chaque fonctionnalité avant la soutenance
- **Documentation incomplète** : Chaque compétence doit être documentée
- **Démo non préparée** : Répétez la démonstration technique
- **Manque de justification** : Préparez les argumentaires techniques

---

**Cette évaluation par compétences vous permet de valider précisément vos acquis DevOps et d'identifier les domaines d'amélioration pour votre progression professionnelle.**

## Conseils de réalisation

### Méthodologie recommandée

1. **Commencer simple** : Version basique fonctionnelle d'abord
2. **Tester fréquemment** : Validation à chaque étape
3. **Documenter au fur et à mesure** : Éviter la documentation de fin
4. **Gérer les erreurs tôt** : Intégrer la robustesse dès le début

### Pièges à éviter

- **Complexité excessive** : Privilégier la simplicité fonctionnelle
- **Scripts monolithiques** : Respecter la modularité
- **Gestion d'erreurs négligée** : Anticiper les cas d'échec
- **Documentation insuffisante** : Code auto-documenté

### Optimisations possibles

- **Cache des résultats** : Éviter les re-calculs coûteux
- **Parallélisation** : Monitoring simultané des modules
- **Configuration dynamique** : Rechargement sans redémarrage
- **Intégration CI/CD** : Tests automatisés du monitoring

---

**Ce brief projet représente la synthèse parfaite entre les fondamentaux Linux de la Semaine 1 et les compétences Bash avancées des Séances 1-2, dans un contexte DevOps réaliste et professionnel.**

_Formateur : Hassan ESSADIK | Sprint 1 - Consolidation Linux & Bash_
