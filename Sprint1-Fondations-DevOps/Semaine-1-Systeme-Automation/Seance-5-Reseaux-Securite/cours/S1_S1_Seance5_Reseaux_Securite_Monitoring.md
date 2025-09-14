# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 5 : Réseaux - Sécurité et Monitoring

## Objectifs pédagogiques

- Sécuriser les communications réseau avec des pare-feu Linux pour protéger les services DevOps
- Configurer et durcir SSH pour l'administration distante sécurisée des serveurs
- Surveiller le trafic réseau et détecter les anomalies avec les outils de monitoring Linux
- Automatiser la surveillance réseau pour des alertes proactives en environnement DevOps

## Objectifs techniques

iptables, ufw, SSH, fail2ban, tcpdump, ss, netstat, monitoring réseau, alertes, sécurité DevOps

## Table des matières

1. [Pare-feu Linux - Protection des services](#1-pare-feu-linux---protection-des-services)
2. [Sécurisation SSH pour administration DevOps](#2-sécurisation-ssh-pour-administration-devops)
3. [Monitoring réseau et détection d'incidents](#3-monitoring-réseau-et-détection-dincidents)
4. [Automatisation de la surveillance réseau](#4-automatisation-de-la-surveillance-réseau)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)

---

## 1. Pare-feu Linux - Protection des services

### 1.1 Comprendre le pare-feu Linux

**Définition** : Un pare-feu (firewall) est un dispositif de sécurité qui contrôle le trafic réseau entrant et sortant selon des règles prédéfinies.

**Analogie** : Un pare-feu Linux est comme un garde de sécurité à l'entrée d'un immeuble - il vérifie l'identité de chaque visiteur (paquet réseau) et décide s'il peut entrer selon les règles établies.

**Rôle en DevOps** :

- **Protection des services** : Seuls les ports nécessaires sont ouverts
- **Isolation des environnements** : Contrôle du trafic entre dev/staging/prod
- **Conformité sécurité** : Respect des politiques entreprise
- **Audit et traçabilité** : Logging des connexions pour investigation

### 1.2 UFW - Pare-feu simplifié

**UFW (Uncomplicated Firewall)** est l'interface simplifiée recommandée pour débuter :

```bash
# Vérifier le statut UFW
sudo ufw status

# Activer UFW (attention: peut couper SSH si mal configuré)
sudo ufw enable

# Politique par défaut (recommandée pour serveur)
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Règles de base pour serveur DevOps** :

```bash
# Autoriser SSH (OBLIGATOIRE avant d'activer UFW)
sudo ufw allow ssh
# ou plus spécifique
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS pour serveur web
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Autoriser depuis un réseau spécifique (management)
sudo ufw allow from 192.168.10.0/24 to any port 3000
```

### 1.3 Gestion des règles UFW

**Lister et gérer les règles** :

```bash
# Voir toutes les règles avec numérotation
sudo ufw status numbered

# Supprimer une règle par numéro
sudo ufw delete 3

# Supprimer une règle par description
sudo ufw delete allow 80/tcp

# Réinitialiser toutes les règles
sudo ufw --force reset
```

### 1.4 Mention d'iptables

**iptables** est l'outil de pare-feu avancé sous-jacent (UFW utilise iptables en arrière-plan) :

```bash
# Voir les règles iptables actuelles (informatif)
sudo iptables -L -n -v

# Exemple de règle iptables directe (complexe)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

**Note** : UFW est recommandé pour débuter car il simplifie grandement la gestion d'iptables.

### 1.5 Application pratique

📝 **LAB 1** - Configuration pare-feu pour serveur web : `S1_S1_S5_lab1_parefeu_serveur_web.sh`

**Énoncé du LAB 1** :

Vous devez sécuriser un nouveau serveur web DevOps en configurant un pare-feu approprié pour les besoins de production.

**Objectif** : Configurer UFW pour protéger un serveur web tout en permettant les accès nécessaires

**Contexte** : Serveur web de production hébergeant une application DevOps critique nécessitant protection contre les intrusions

**Instructions** :

1. Vérifiez l'état actuel d'UFW avec `sudo ufw status`
2. Si UFW est inactif, configurez d'abord SSH : `sudo ufw allow ssh`
3. Définissez la politique par défaut : deny incoming, allow outgoing
4. Autorisez les services web : HTTP (80) et HTTPS (443)
5. Autorisez l'accès SSH depuis le réseau management uniquement (192.168.10.0/24)
6. Activez UFW avec `sudo ufw enable`
7. Vérifiez la configuration finale avec `sudo ufw status numbered`
8. Testez l'accès aux services autorisés (si possible)

**Critères d'évaluation** :

- Configuration sécurisée par défaut (1 point)
- Autorisation SSH sécurisée (2 points)
- Configuration services web appropriée (2 points)

**Durée estimée** : 15 minutes  
**Fichier de travail** : `S1_S1_S5_lab1_parefeu_serveur_web.sh`

---

## 2. Sécurisation SSH pour administration DevOps

### 2.1 SSH - Administration distante sécurisée

**Définition** : SSH (Secure Shell) est un protocole réseau qui permet d'accéder à distance à un système Linux de manière sécurisée et chiffrée.

**Analogie** : SSH est comme un tunnel sécurisé entre votre bureau et un serveur distant - personne ne peut voir ou modifier les données qui transitent dans ce tunnel.

**Importance en DevOps** :

- **Administration distante** : Gestion des serveurs sans accès physique
- **Déploiement automatisé** : Scripts et CI/CD utilisent SSH
- **Transfert de fichiers** : scp/rsync via SSH pour déploiements
- **Tunneling sécurisé** : Accès à des services internes via SSH

### 2.2 Configuration SSH sécurisée

**Fichier de configuration** : `/etc/ssh/sshd_config`

**Principales sécurisations recommandées** :

```bash
# Éditer la configuration SSH
sudo nano /etc/ssh/sshd_config

# Changements de sécurité recommandés :
Port 2222                    # Changer le port par défaut (au lieu de 22)
PermitRootLogin no          # Interdire connexion root directe
PasswordAuthentication no   # Privilégier les clés SSH
MaxAuthTries 3             # Limiter les tentatives de connexion
ClientAliveInterval 300    # Déconnecter sessions inactives (5 min)
```

**Redémarrer SSH après modification** :

```bash
# Tester la configuration avant redémarrage
sudo sshd -t

# Redémarrer le service SSH
sudo systemctl restart sshd

# Vérifier que SSH fonctionne sur nouveau port
sudo ss -tuln | grep 2222
```

### 2.3 Authentification par clés SSH

**Génération d'une paire de clés** :

```bash
# Générer une paire de clés forte (sur votre machine locale)
ssh-keygen -t rsa -b 4096 -C "admin@entreprise.com"

# Ou plus moderne avec ed25519
ssh-keygen -t ed25519 -C "admin@entreprise.com"
```

**Déploiement de la clé publique** :

```bash
# Copier la clé vers le serveur distant
ssh-copy-id -i ~/.ssh/id_rsa.pub user@192.168.1.100

# Ou manuellement
cat ~/.ssh/id_rsa.pub | ssh user@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Connexion avec clé** :

```bash
# Connexion automatique avec clé
ssh user@192.168.1.100

# Spécifier une clé particulière
ssh -i ~/.ssh/cle_specifique user@192.168.1.100
```

### 2.4 Protection contre les attaques - fail2ban

**Installation et configuration basique** :

```bash
# Installer fail2ban
sudo apt install fail2ban

# Créer configuration locale
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Configuration basique pour SSH
sudo nano /etc/fail2ban/jail.local
```

**Configuration recommandée pour SSH** :

```bash
[sshd]
enabled = true
port    = 2222
filter  = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

### 2.5 Application pratique

📝 **LAB 2** - Durcissement sécurité SSH : `S1_S1_S5_lab2_durcissement_ssh.sh`

**Énoncé du LAB 2** :

Votre serveur DevOps de production subit des tentatives d'intrusion SSH. Vous devez renforcer sa sécurité selon les bonnes pratiques.

**Objectif** : Implémenter les mesures de sécurisation SSH essentielles pour un environnement de production

**Contexte** : Serveur critique DevOps exposé sur Internet nécessitant durcissement contre les attaques par force brute

**Instructions** :

1. Sauvegardez la configuration SSH actuelle : `sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup`
2. Modifiez le port SSH de 22 vers 2222 dans `/etc/ssh/sshd_config`
3. Désactivez la connexion root directe : `PermitRootLogin no`
4. Limitez les tentatives d'authentification : `MaxAuthTries 3`
5. Configurez une déconnexion automatique : `ClientAliveInterval 300`
6. Testez la configuration : `sudo sshd -t`
7. Redémarrez SSH : `sudo systemctl restart sshd`
8. Mettez à jour UFW pour le nouveau port : `sudo ufw allow 2222/tcp`
9. Supprimez l'ancienne règle SSH : `sudo ufw delete allow ssh`
10. Documentez les changements effectués et testez la connexion

**Critères d'évaluation** :

- Changement de port sécurisé (1 point)
- Désactivation root et limitations appropriées (2 points)
- Mise à jour pare-feu cohérente (2 points)

**Durée estimée** : 20 minutes  
**Fichier de travail** : `S1_S1_S5_lab2_durcissement_ssh.sh`

---

## 3. Monitoring réseau et détection d'incidents

### 3.1 Surveillance du trafic réseau

**Définition** : Le monitoring réseau consiste à surveiller en temps réel les communications réseau pour détecter des anomalies, performances dégradées ou tentatives d'intrusion.

**Analogie** : Le monitoring réseau est comme un système de vidéosurveillance pour votre infrastructure - il observe constamment ce qui se passe et vous alerte en cas d'activité suspecte.

**Objectifs DevOps** :

- **Détection précoce** : Identifier les problèmes avant impact utilisateur
- **Analyse de performance** : Optimiser les applications et services
- **Sécurité** : Détecter intrusions et comportements anormaux
- **Capacité** : Planifier l'évolution de l'infrastructure

### 3.2 Outils de surveillance en temps réel

**ss - Socket Statistics (moderne)** :

```bash
# Connexions actives avec processus
ss -tulpn

# Connexions établies seulement
ss -tu state established

# Statistiques par protocole
ss -s

# Surveiller un port spécifique
watch -n 2 'ss -tuln | grep :80'
```

**netstat - Outil traditionnel** :

```bash
# Connexions avec programmes
sudo netstat -tulpn

# Statistiques d'interface
netstat -i

# Tables de routage
netstat -rn
```

### 3.3 Capture et analyse de trafic

**tcpdump - Capture de paquets** :

```bash
# Capture basique sur interface
sudo tcpdump -i eth0

# Capture avec filtre par port
sudo tcpdump -i eth0 port 80

# Capture vers fichier pour analyse
sudo tcpdump -i eth0 -w capture.pcap

# Analyser une capture existante
tcpdump -r capture.pcap
```

**Exemples de filtres utiles DevOps** :

```bash
# Trafic HTTP uniquement
sudo tcpdump -i eth0 'port 80 or port 443'

# Trafic depuis/vers une IP spécifique
sudo tcpdump -i eth0 'host 192.168.1.100'

# Connexions SSH
sudo tcpdump -i eth0 'port 22'

# Trafic non-standard (suspect)
sudo tcpdump -i eth0 'not port 22 and not port 80 and not port 443'
```

### 3.4 Surveillance des logs de sécurité

**Fichiers de logs importants** :

```bash
# Logs d'authentification (SSH, sudo)
sudo tail -f /var/log/auth.log

# Logs système généraux
sudo tail -f /var/log/syslog

# Logs du pare-feu UFW
sudo tail -f /var/log/ufw.log
```

**Recherche d'incidents dans les logs** :

```bash
# Tentatives de connexion SSH échouées
grep "Failed password" /var/log/auth.log

# Connexions SSH réussies
grep "Accepted password\|Accepted publickey" /var/log/auth.log

# Activité sudo suspecte
grep "sudo" /var/log/auth.log | tail -10
```

### 3.5 Application pratique

📝 **LAB 3** - Monitoring sécurisé du trafic : `S1_S1_S5_lab3_monitoring_securise.sh`

**Énoncé du LAB 3** :

Des anomalies de performance ont été détectées sur votre infrastructure DevOps. Vous devez mettre en place un monitoring pour identifier la source du problème.

**Objectif** : Surveiller le trafic réseau et analyser les connexions pour détecter des anomalies de sécurité ou performance

**Contexte** : Applications web DevOps avec ralentissements suspects et tentatives de connexion non-autorisées détectées

**Instructions** :

1. Surveillez les connexions actives avec `ss -tulpn` et identifiez les services en écoute
2. Capturez 30 secondes de trafic HTTP avec `sudo tcpdump -i eth0 port 80 -c 50`
3. Analysez les logs d'authentification : `grep "Failed password" /var/log/auth.log | tail -10`
4. Vérifiez les connexions SSH récentes : `grep "sshd.*Accepted" /var/log/auth.log | tail -5`
5. Surveillez en temps réel les nouvelles connexions : `watch -n 2 'ss -tu state established | wc -l'`
6. Identifiez les processus consommant le plus de bande passante avec `ss -tulpn | grep ESTABLISHED`
7. Recherchez des tentatives de scan de ports suspectes dans les logs UFW
8. Documentez vos observations et recommandations sécurité

**Critères d'évaluation** :

- Surveillance connexions appropriée (2 points)
- Analyse logs sécurité méthodique (2 points)
- Identification anomalies et recommandations (1 point)

**Durée estimée** : 20 minutes  
**Fichier de travail** : `S1_S1_S5_lab3_monitoring_securise.sh`

---

## 4. Automatisation de la surveillance réseau

### 4.1 Scripts de monitoring automatisé

**Définition** : L'automatisation de la surveillance consiste à créer des scripts qui vérifient régulièrement l'état du réseau et alertent en cas de problème détecté.

**Analogie** : Les scripts de monitoring sont comme un gardien automatique qui fait des rondes 24h/24 et vous réveille seulement s'il détecte quelque chose d'anormal.

**Avantages DevOps** :

- **Surveillance continue** : 24h/24 sans intervention humaine
- **Détection rapide** : Alertes immédiates en cas de problème
- **Historique** : Données pour analyse post-incident
- **Scalabilité** : Surveillance de nombreux serveurs simultanément

### 4.2 Script de vérification réseau basique

**Exemple de script de monitoring** :

```bash
#!/bin/bash
# network_monitor.sh - Surveillance réseau automatisée

LOG_FILE="/var/log/network_monitor.log"

# Fonction de logging avec timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Test connectivité passerelle
check_gateway() {
    GATEWAY=$(ip route | grep default | awk '{print $3}' | head -n1)
    if ping -c 3 -W 5 "$GATEWAY" >/dev/null 2>&1; then
        log_message "OK: Passerelle $GATEWAY accessible"
        return 0
    else
        log_message "ALERTE: Passerelle $GATEWAY inaccessible"
        return 1
    fi
}

# Test résolution DNS
check_dns() {
    if nslookup google.com >/dev/null 2>&1; then
        log_message "OK: Résolution DNS fonctionnelle"
        return 0
    else
        log_message "ALERTE: Problème résolution DNS"
        return 1
    fi
}

# Surveillance connexions SSH suspectes
check_ssh_attempts() {
    FAILED_COUNT=$(grep "Failed password" /var/log/auth.log | grep "$(date '+%b %d')" | wc -l)
    if [ "$FAILED_COUNT" -gt 10 ]; then
        log_message "ALERTE: $FAILED_COUNT tentatives SSH échouées aujourd'hui"
        return 1
    else
        log_message "OK: Activité SSH normale ($FAILED_COUNT échecs)"
        return 0
    fi
}

# Exécution des vérifications
log_message "=== Début surveillance réseau ==="
check_gateway
check_dns
check_ssh_attempts
log_message "=== Fin surveillance réseau ==="
```

### 4.3 Automatisation avec cron

**Programmer l'exécution régulière** :

```bash
# Éditer la crontab
crontab -e

# Exécuter toutes les 5 minutes
*/5 * * * * /home/user/scripts/network_monitor.sh

# Exécuter toutes les heures
0 * * * * /home/user/scripts/network_monitor.sh

# Rapport quotidien à 6h00
0 6 * * * /home/user/scripts/daily_network_report.sh
```

### 4.4 Alertes par email (configuration basique)

**Installation d'un client email simple** :

```bash
# Installer mailutils
sudo apt install mailutils

# Test d'envoi (si serveur SMTP configuré)
echo "Test alerte réseau" | mail -s "Alerte Monitoring" admin@entreprise.com
```

**Intégration dans le script de monitoring** :

```bash
# Fonction d'alerte email
send_alert() {
    MESSAGE="$1"
    echo "$MESSAGE" | mail -s "Alerte Réseau DevOps" admin@entreprise.com
    log_message "ALERTE ENVOYÉE: $MESSAGE"
}

# Utilisation dans les vérifications
if ! check_gateway; then
    send_alert "Passerelle réseau inaccessible sur serveur $(hostname)"
fi
```

### 4.5 Application pratique

📝 **LAB 4 - Challenge** - Système de monitoring automatisé : `S1_S1_S5_lab4_challenge_monitoring_auto.sh`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge avancé consiste à créer un système complet de monitoring réseau automatisé avec alertes intelligentes pour une infrastructure DevOps.

**Objectif** : Développer et déployer un système de surveillance réseau automatisé avec alertes multi-niveaux

**Contexte** : Infrastructure DevOps critique nécessitant surveillance 24h/24 avec escalade automatique des incidents

**Instructions** :

1. Créez un script de monitoring avancé qui vérifie :
   - Connectivité vers 3 serveurs critiques (ping + ports spécifiques)
   - Utilisation bande passante (détection pics anormaux)
   - Nombre de connexions actives par service (HTTP, SSH, DB)
   - Tentatives d'intrusion (analyse logs en temps réel)
   - État des services réseau critiques (SSH, HTTP, DNS)
2. Implémentez un système de seuils d'alerte à 3 niveaux :
   - INFO : Fonctionnement normal avec métriques
   - WARNING : Anomalies détectées nécessitant surveillance
   - CRITICAL : Pannes ou incidents de sécurité graves
3. Configurez une rotation de logs automatique pour éviter saturation disque
4. Créez un tableau de bord textuel avec résumé état infrastructure
5. Programmez l'exécution avec cron (toutes les 2 minutes pour tests)
6. Implémentez une fonction de test en mode simulation (sans vraie infrastructure)
7. Ajoutez une fonction de rapport quotidien avec statistiques
8. Documentez le déploiement et la configuration du système

**Critères d'évaluation** :

- Script de monitoring complet et robuste (4 points)
- Système d'alertes à niveaux multiples (3 points)
- Gestion logs et rotation appropriée (2 points)
- Tableau de bord informatif (2 points)
- Configuration cron et automatisation (2 points)
- Documentation déploiement complète (2 points)

**Statut** : Activité bonus, hors des 2 heures de séance  
**Durée estimée** : 30-45 minutes  
**Fichier de travail** : `S1_S1_S5_lab4_challenge_monitoring_auto.sh`

---

## 5. Récapitulatif et prochaines étapes

### Concepts maîtrisés

- **Pare-feu Linux (UFW)** : Protection des services avec règles granulaires
- **Sécurisation SSH** : Administration distante durcie contre les intrusions
- **Monitoring réseau** : Surveillance trafic et détection d'anomalies avec tcpdump/ss
- **Automatisation surveillance** : Scripts de monitoring avec alertes proactives

### Compétences DevOps acquises

- **Sécurisation infrastructure** : Protection pare-feu et SSH pour environnements critiques
- **Surveillance proactive** : Détection précoce d'incidents réseau et sécurité
- **Automatisation monitoring** : Scripts de surveillance continue avec alertes
- **Analyse post-incident** : Investigation avec logs et captures de trafic

### Préparation séance suivante

La **Séance 6 : Services avancés et automatisation** abordera :

- Configuration et gestion des serveurs web (Apache/Nginx)
- Gestion des bases de données en environnement DevOps
- Automatisation des déploiements avec scripts
- Planification des tâches avec cron et systemd timers

### Sécurité réseau et écosystème DevOps

Ces compétences de sécurité réseau sont essentielles pour :

- **Conteneurs sécurisés** : Isolation réseau Docker et Kubernetes
- **CI/CD sécurisé** : Pipelines avec communications chiffrées
- **Cloud sécurité** : Configuration security groups et firewalls cloud
- **Compliance** : Respect des standards de sécurité (ANSSI, ISO 27001)

### Bonnes pratiques de sécurité retenues

- **Principe de moindre privilège** : Ouvertures réseau minimales nécessaires
- **Défense en profondeur** : Pare-feu + SSH durci + monitoring
- **Surveillance continue** : Monitoring automatisé 24h/24
- **Response rapide** : Alertes immédiates pour incidents critiques
- **Documentation sécurité** : Procédures d'incident et configuration à jour

### Architecture de sécurité réseau DevOps

Cette séance complète la trilogie réseau avec une approche sécurité complète :

1. **Séance 3** : Fondations techniques (interfaces, connectivité, DNS)
2. **Séance 4** : Architecture et routage (segmentation, communication inter-réseaux)
3. **Séance 5** : Sécurité et monitoring (protection, surveillance, alertes)

Cette progression permet une maîtrise complète des réseaux Linux pour DevOps, de la configuration basique à la surveillance avancée, en respectant les bonnes pratiques de sécurité essentielles pour des environnements de production.

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 5_
