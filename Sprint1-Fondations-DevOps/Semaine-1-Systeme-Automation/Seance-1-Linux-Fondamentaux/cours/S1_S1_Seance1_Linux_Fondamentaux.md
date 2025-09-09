# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 1 : Linux Fondamentaux

## Objectifs pédagogiques

- Maîtriser la navigation dans le système de fichiers Linux
- Gérer efficacement les fichiers et dossiers en ligne de commande
- Comprendre et appliquer le système de permissions Unix
- Configurer et utiliser les variables d'environnement système

## Objectifs techniques

Linux, bash, système de fichiers, permissions Unix, variables environnement, commandes de base

## Table des matières

1. [Système de fichiers Linux](#1-système-de-fichiers-linux)
2. [Commandes de navigation et manipulation](#2-commandes-de-navigation-et-manipulation)
3. [Système de permissions Unix](#3-système-de-permissions-unix)
4. [Variables d'environnement et configuration](#4-variables-denvironnement-et-configuration)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)
6. [Ressources complémentaires](#6-ressources-complémentaires)

---

## 1. Système de fichiers Linux

### 1.1 Définitions et concepts fondamentaux

#### Système de fichiers (Filesystem)

**Définition :** Un système de fichiers est une méthode d'organisation et de stockage des données sur un support de stockage, définissant comment les fichiers sont nommés, organisés et accédés.

**Terminologie bilingue :**

- **Français :** Système de fichiers, arborescence
- **Anglais :** Filesystem, directory tree

**Contexte d'utilisation :** Essential pour l'administration système, le déploiement d'applications et la gestion des configurations DevOps.

#### FHS (Filesystem Hierarchy Standard)

**Définition :** Standard définissant l'organisation des répertoires et fichiers sur les systèmes Unix/Linux, garantissant la cohérence entre distributions.

**Contexte DevOps :** Permet l'automatisation et la portabilité des scripts entre environnements Linux différents.

### 1.2 Architecture du système de fichiers Linux

Le système de fichiers Linux suit une **hiérarchie standard** appelée **FHS (Filesystem Hierarchy Standard)**. Contrairement à Windows qui utilise des lettres de lecteur (C:, D:), Linux organise tout sous une **racine unique** notée `/`.

#### Schéma conceptuel de l'arborescence Linux

```
📁 / (Racine - Root Directory)
├── 📁 bin/     → Binaires essentiels du système
├── 📁 etc/     → Fichiers de configuration
├── 📁 home/    → Répertoires des utilisateurs
│   ├── 📁 user1/
│   └── 📁 user2/
├── 📁 var/     → Données variables (logs, caches)
│   └── 📁 log/   → Journaux système
├── 📁 usr/     → Programmes utilisateur
│   └── 📁 bin/   → Binaires utilisateur
├── 📁 tmp/     → Fichiers temporaires
└── 📁 opt/     → Logiciels optionnels
```

### 1.3 Répertoires système critiques pour DevOps

#### `/etc/` - Configuration système

**Définition :** Répertoire contenant les fichiers de configuration système et des services.

**Contexte DevOps :** Zone critique pour l'automatisation des configurations via Ansible, Puppet ou scripts de déploiement.

**Exemples de fichiers clés :**

```bash
/etc/hosts          # Configuration DNS locale
/etc/passwd         # Informations utilisateurs
/etc/ssh/sshd_config # Configuration serveur SSH
/etc/nginx/nginx.conf # Configuration web server
```

#### `/var/log/` - Journalisation système

**Définition :** Répertoire contenant les logs (journaux) du système et des applications.

**Contexte DevOps :** Essentiel pour le monitoring, debugging et observabilité des services.

**Exemples de logs critiques :**

```bash
/var/log/syslog     # Messages système généraux
/var/log/auth.log   # Tentatives d'authentification
/var/log/nginx/     # Logs serveur web
/var/log/application/ # Logs applicatifs
```

#### `/home/` - Espaces utilisateurs

**Définition :** Répertoires personnels des utilisateurs du système.

**Contexte DevOps :** Stockage des clés SSH, configurations personnelles et projets de développement.

#### `/usr/bin/` et `/usr/local/bin/` - Binaires utilisateur

**Définition :** Répertoires contenant les programmes et commandes installés.

**Contexte DevOps :** Localisation des outils CLI (git, docker, kubectl, terraform).

### 1.4 Concepts de navigation : Chemins absolus et relatifs

#### Chemin absolu (Absolute Path)

**Définition :** Chemin complet depuis la racine du système (/) vers un fichier ou répertoire.

**Terminologie bilingue :**

- **Français :** Chemin absolu
- **Anglais :** Absolute path

**Caractéristiques :**

```bash
# Exemples de chemins absolus (commencent toujours par /)
/home/user/documents/projet.txt
/etc/nginx/nginx.conf
/var/log/syslog
```

#### Chemin relatif (Relative Path)

**Définition :** Chemin défini par rapport au répertoire de travail actuel, sans partir de la racine.

**Terminologie bilingue :**

- **Français :** Chemin relatif
- **Anglais :** Relative path

**Caractéristiques :**

```bash
# Exemples de chemins relatifs (ne commencent PAS par /)
documents/projet.txt    # Sous-répertoire du répertoire actuel
../parent/fichier.txt   # Remonte d'un niveau puis descend
./script.sh            # Fichier dans le répertoire actuel
```

#### Répertoires spéciaux de navigation

**Définitions essentielles :**

```bash
.     # Répertoire actuel (current directory)
..    # Répertoire parent (parent directory)
~     # Répertoire home de l'utilisateur
/     # Racine du système (root directory)
```

### 1.5 Chemins absolus et relatifs

#### Exemples pratiques commentés

```bash
# Navigation avec chemins absolus
cd /home/devops/projets/webapp    # Aller directement au projet webapp
ls /etc/nginx/                    # Lister les fichiers de configuration nginx
cat /var/log/syslog              # Afficher le log système

# Navigation avec chemins relatifs (depuis /home/devops/)
cd projets/webapp                 # Descendre dans projets puis webapp
cd ../config/                     # Remonter puis aller dans config
cd ~/                            # Retourner au répertoire home
```

## 2. Commandes de navigation et manipulation

### 2.1 Définitions des commandes de base

#### pwd (Print Working Directory)

**Définition :** Commande affichant le chemin absolu du répertoire de travail actuel.

**Terminologie bilingue :**

- **Français :** Répertoire de travail, répertoire courant
- **Anglais :** Working directory, current directory

**Syntaxe et utilisation :**

```bash
pwd                              # Affiche le répertoire actuel
# Exemple de sortie : /home/devops/projets
```

**Contexte DevOps :** Essentiel dans les scripts pour vérifier la localisation avant exécution d'opérations.

#### ls (List)

**Définition :** Commande permettant de lister le contenu d'un répertoire.

**Syntaxe et options courantes :**

```bash
ls                              # Liste simple du contenu
ls -l                           # Liste détaillée (permissions, taille, date)
ls -la                          # Liste tout (y compris fichiers cachés)
ls -lh                          # Liste avec tailles lisibles (K, M, G)
```

**Contexte DevOps :** Inspection des déploiements, vérification des permissions, audit des fichiers.

#### cd (Change Directory)

**Définition :** Commande permettant de changer le répertoire de travail actuel.

**Syntaxe et exemples commentés :**

```bash
cd /path/to/directory           # Aller vers un répertoire spécifique
cd ~                            # Retourner au répertoire home
cd ..                           # Remonter d'un niveau
cd -                            # Retourner au répertoire précédent
```

#### mkdir (Make Directory)

**Définition :** Commande pour créer des répertoires.

**Terminologie bilingue :**

- **Français :** Créer un répertoire/dossier
- **Anglais :** Make directory, create folder

**Syntaxe et options :**

```bash
mkdir repertoire                # Créer un répertoire simple
mkdir -p path/to/deep/dir       # Créer l'arborescence complète (-p = parents)
mkdir -m 755 secure_dir         # Créer avec permissions spécifiques
```

#### cp (Copy)

**Définition :** Commande pour copier fichiers et répertoires.

**Syntaxe et exemples :**

```bash
cp fichier.txt copie.txt        # Copier un fichier
cp -r repertoire/ backup/       # Copier un répertoire (-r = récursif)
cp -p fichier.txt backup/       # Conserver les permissions (-p = preserve)
```

#### mv (Move)

**Définition :** Commande pour déplacer ou renommer fichiers et répertoires.

**Utilisation duale :**

```bash
mv ancien.txt nouveau.txt       # Renommer un fichier
mv fichier.txt /autre/path/     # Déplacer un fichier
mv repertoire/ /destination/    # Déplacer un répertoire
```

#### rm (Remove)

**Définition :** Commande pour supprimer fichiers et répertoires.

**Syntaxe et options critiques :**

```bash
rm fichier.txt                  # Supprimer un fichier
rm -r repertoire/               # Supprimer un répertoire (-r = récursif)
rm -f fichier.txt               # Forcer la suppression (-f = force)
rm -rf repertoire/              # Supprimer récursivement sans confirmation
```

**Attention DevOps :** Toujours vérifier avant d'utiliser `rm -rf` en production !

#### find

**Définition :** Commande pour rechercher des fichiers et répertoires selon différents critères.

**Syntaxe et options critiques :**

```bash
find /var/log -name "*.log"     # Trouver tous les fichiers .log
find . -type f -size +10M       # Fichiers de plus de 10MB
find /etc -name "nginx*"        # Fichiers commençant par nginx
find /tmp -mtime +7             # Fichiers modifiés il y a plus de 7 jours
```

**Contexte DevOps :** Localisation logs, audit fichiers, nettoyage disque, debugging.

#### grep

**Définition :** Commande pour rechercher du texte dans les fichiers selon des motifs.

**Syntaxe et options principales :**

```bash
grep "erreur" /var/log/app.log  # Rechercher "erreur" dans un fichier
grep -r "config" /etc/nginx/    # Recherche récursive dans répertoire
grep -i "error" *.log           # Recherche insensible à la casse
grep -n "port" config.conf      # Afficher numéros de lignes
```

**Contexte DevOps :** Analyse logs, debugging, recherche configuration, monitoring erreurs.

### 2.2 Application pratique - Gestion de fichiers

📝 **LAB 1** - Gestion fichiers DevOps : `S1_S1_S1_lab1_gestion_fichiers.sh`

**Énoncé du LAB 1** :
Créer automatiquement une structure de projet web complète avec des templates de configuration.

- **Objectif** : Automatiser la création d'environnement de développement web
- **Contexte** : Setup automatisé d'un projet web avec Nginx et PHP pour équipe DevOps
- **Instructions** :

1. Créer l'arborescence complète du projet (public, src, config, logs, backups)
2. Générer des templates de configuration (Nginx, PHP)
3. Créer des fichiers web de test (HTML, CSS, PHP)
4. Organiser les logs par date
5. Implémenter un script de sauvegarde automatique

- **Critères d'évaluation** : Structure organisée, templates fonctionnels, automation complète
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S1_S1_lab1_gestion_fichiers.sh`

### 2.3 Commandes d'analyse et monitoring système

Ces commandes sont essentielles pour l'audit système et le monitoring en environnement DevOps. Elles permettent d'analyser l'état des ressources, localiser les fichiers critiques et surveiller les performances.

#### df (Disk Free)

**Définition :** Commande affichant l'espace disque utilisé et disponible pour chaque système de fichiers monté.

**Terminologie bilingue :**

- **Français :** Espace disque libre, utilisation disque
- **Anglais :** Disk free space, disk usage

**Syntaxe et options principales :**

```bash
df                              # Affichage simple en blocs
df -h                           # Affichage lisible (K, M, G)
df -i                           # Utilisation des inodes
df /path/to/directory           # Espace pour un répertoire spécifique
```

**Contexte DevOps :** Monitoring des serveurs, prévention saturation disque, dimensionnement infrastructure.

**Exemples pratiques :**

```bash
df -h                           # Vue d'ensemble espace disque
df -h /var/log                  # Espace disponible pour logs
df -h | grep -E "(8[0-9]%|9[0-9]%|100%)"  # Partitions critiques >80%
```

#### mount

**Définition :** Commande pour afficher ou gérer les points de montage des systèmes de fichiers.

**Terminologie bilingue :**

- **Français :** Montage, point de montage
- **Anglais :** Mount, mount point

**Syntaxe et utilisation :**

```bash
mount                           # Afficher tous les montages
mount | grep /dev               # Montages physiques seulement
mount -t ext4                   # Montages d'un type spécifique
findmnt                         # Vue arborescente (si disponible)
```

**Contexte DevOps :** Analyse infrastructure, gestion stockage, troubleshooting montages.

#### find

**Définition :** Commande de recherche avancée de fichiers et répertoires selon des critères multiples.

**Syntaxe et options critiques :**

```bash
find /path -name "pattern"      # Recherche par nom
find /path -type f              # Fichiers seulement (-type d pour dossiers)
find /path -size +100M          # Fichiers > 100MB
find /path -mtime -7            # Modifiés dans les 7 derniers jours
```

**Contexte DevOps :** Localisation logs, cleanup automatique, audit sécurité.

**Exemples pour l'audit système :**

```bash
find /var/log -name "*.log" -type f         # Tous les fichiers de logs
find /etc -name "*.conf" -type f            # Fichiers de configuration
find /home -size +1G -type f                # Gros fichiers utilisateurs
```

#### du (Disk Usage)

**Définition :** Commande calculant l'espace disque utilisé par les fichiers et répertoires.

**Terminologie bilingue :**

- **Français :** Utilisation disque, taille répertoire
- **Anglais :** Disk usage, directory size

**Syntaxe et options :**

```bash
du -h /path                     # Taille lisible d'un répertoire
du -sh /path                    # Résumé total seulement
du -h --max-depth=1 /path       # Profondeur limitée
```

**Contexte DevOps :** Analyse consommation, optimisation stockage, capacity planning.

#### wc (Word Count)

**Définition :** Commande de comptage (lignes, mots, caractères) dans les fichiers.

**Options principales :**

```bash
wc -l fichier.txt               # Nombre de lignes
wc -w fichier.txt               # Nombre de mots
wc -c fichier.txt               # Nombre de caractères
```

**Contexte DevOps :** Analyse logs, métriques fichiers, monitoring croissance.

**Exemples d'audit :**

```bash
wc -l /var/log/syslog           # Taille du log système
wc -l /etc/passwd               # Nombre d'utilisateurs
```

#### free

**Définition :** Commande affichant l'utilisation de la mémoire vive (RAM) et du swap.

**Syntaxe :**

```bash
free                            # Affichage en bytes
free -h                         # Affichage lisible
free -m                         # Affichage en MB
```

**Contexte DevOps :** Monitoring performance, dimensionnement serveurs, détection fuites mémoire.

#### uname

**Définition :** Commande affichant les informations système du kernel et de l'architecture.

**Options principales :**

```bash
uname -a                        # Toutes les informations
uname -r                        # Version du kernel
uname -m                        # Architecture (x86_64, arm64)
uname -o                        # Nom du système d'exploitation
```

**Contexte DevOps :** Documentation infrastructure, compatibilité logiciels, audit sécurité.

#### uptime

**Définition :** Commande affichant le temps de fonctionnement du système et la charge moyenne.

**Informations fournies :**

```bash
uptime                          # Temps fonctionnement + charge
# Exemple sortie : 10:30:01 up 15 days, 3:45, 2 users, load average: 0.08, 0.12, 0.09
```

**Interprétation :**

- **Temps de fonctionnement** : Depuis le dernier reboot
- **Utilisateurs connectés** : Sessions actives
- **Load average** : Charge système (1, 5, 15 minutes)

**Contexte DevOps :** Monitoring stabilité, métriques performance, planification maintenance.

### 2.4 Application pratique

📝 **LAB 2** - Navigation système : `S1_S1_S1_lab2_navigation_systeme.sh`

**Énoncé du LAB 2** :
Créer un script de découverte du système de fichiers Linux pour analyser l'architecture d'un serveur de développement.

- **Objectif** : Explorer et documenter la structure du système de fichiers
- **Contexte** : Audit d'un nouveau serveur Linux pour équipe DevOps
- **Instructions** :

1. Analyser la structure racine et identifier les répertoires critiques système
2. Explorer les répertoires de configuration (/etc) et documenter les services
3. Vérifier l'espace disque disponible et identifier les partitions montées
4. Localiser et examiner les logs système principaux (/var/log)
5. Générer un rapport complet de l'infrastructure système découverte

- **Critères d'évaluation** : Script fonctionnel, analyse complète, documentation claire
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S1_S1_lab2_navigation_systeme.sh`

## 3. Système de permissions Unix

### 3.1 Définitions et concepts fondamentaux

#### Système de permissions Unix

**Définition :** Mécanisme de contrôle d'accès définissant qui peut lire, écrire ou exécuter un fichier ou répertoire.

**Terminologie bilingue :**

- **Français :** Permissions, droits d'accès
- **Anglais :** Permissions, access rights

**Contexte DevOps :** Sécurisation des applications, configuration des services, protection des clés et secrets.

### 3.2 Structure des permissions

#### Schéma conceptuel des permissions

```
Fichier: -rwxr-xr-- user group 1024 Jan 15 10:30 script.sh
  ▲       ▲▲▲ ▲▲▲ ▲▲▲
  │       │││ │││ │││
  │       │││ │││ └──→ Autres (Others): r--
  │       │││ └─────→ Groupe (Group): r-x
  │       └────────→ Propriétaire (Owner): rwx
  └─────────────────→ Type: - (fichier régulier)
```

#### Types d'entités et permissions

**Entités :**

```bash
u (user)     # Propriétaire du fichier
g (group)    # Groupe propriétaire
o (others)   # Tous les autres utilisateurs
a (all)      # Toutes les entités (u+g+o)
```

**Permissions de base :**

```bash
r (read)     # Lecture - valeur octale: 4
w (write)    # Écriture - valeur octale: 2
x (execute)  # Exécution - valeur octale: 1
```

### 3.3 Représentations des permissions

#### Notation symbolique

**Structure :** `[type][user][group][others]`

```bash
-rwxr-xr--   # Fichier: rwx pour user, r-x pour group, r-- pour others
drwxr-xr-x   # Répertoire: rwx pour user, r-x pour group, r-x pour others
```

#### Notation octale

**Calcul des valeurs :**

```bash
rwx = 4+2+1 = 7    # Toutes permissions
r-x = 4+0+1 = 5    # Lecture et exécution
r-- = 4+0+0 = 4    # Lecture seule
--- = 0+0+0 = 0    # Aucune permission
```

**Exemples courants :**

```bash
755  # rwxr-xr-x  - Exécutable standard
644  # rw-r--r--  - Fichier de données
600  # rw-------  - Fichier privé (clés SSH)
700  # rwx------  # Répertoire privé
```

### 3.4 Commandes de gestion des permissions

#### chmod (Change Mode)

**Définition :** Commande pour modifier les permissions d'accès aux fichiers et répertoires.

**Syntaxe avec notation octale :**

```bash
chmod 755 script.sh             # Permissions rwxr-xr-x
chmod 600 ~/.ssh/id_rsa         # Clé SSH privée (lecture/écriture owner seul)
chmod 644 config.yml            # Fichier de config (lecture pour tous)
chmod 700 ~/.ssh/               # Répertoire SSH privé
```

**Syntaxe avec notation symbolique :**

```bash
chmod u+x script.sh             # Ajouter exécution pour user
chmod g-w fichier.txt           # Retirer écriture pour group
chmod o-r secret.txt            # Retirer lecture pour others
chmod a+r public.txt            # Ajouter lecture pour all
```

#### chown (Change Owner)

**Définition :** Commande pour changer le propriétaire et le groupe d'un fichier ou répertoire.

```bash
chown user:group fichier.txt         # Changer user et group
chown user fichier.txt               # Changer seulement user
chown :group fichier.txt             # Changer seulement group
chown -R user:group repertoire/      # Récursif sur un répertoire
```

### 3.5 Cas d'usage DevOps critiques

#### Sécurisation des clés SSH

```bash
chmod 700 ~/.ssh/                    # Répertoire SSH privé
chmod 600 ~/.ssh/id_rsa              # Clé privée
chmod 644 ~/.ssh/id_rsa.pub          # Clé publique
chmod 644 ~/.ssh/authorized_keys     # Clés autorisées
```

#### Scripts de déploiement

```bash
chmod 755 deploy.sh                 # Script exécutable
chmod 640 config.env                # Variables d'environnement
chmod 600 secrets.conf              # Fichier de secrets
```

### 3.6 Application pratique

📝 **LAB 3** - Sécurisation permissions : `S1_S1_S1_lab3_permissions_securite.sh`

**Énoncé du LAB 3** :
Configurer un environnement sécurisé pour une application web avec permissions appropriées et gestion des utilisateurs.

- **Objectif** : Appliquer les bonnes pratiques de sécurité via les permissions Unix
- **Contexte** : Déploiement sécurisé d'une application web sur serveur de production
- **Instructions** :

1. Configurer les permissions des répertoires web avec propriétaires appropriés
2. Sécuriser les fichiers de configuration avec accès restreint (600/640)
3. Protéger les clés SSH et certificats avec permissions strictes (400)
4. Mettre en place des groupes d'utilisateurs pour la gestion collaborative
5. Valider et documenter toutes les permissions avec audit de sécurité

- **Critères d'évaluation** : Sécurité renforcée, permissions appropriées, tests validés
- **Durée estimée** : 25 minutes
- **Fichier de travail** : `S1_S1_S1_lab3_permissions_securite.sh`

---

## 4. Variables d'environnement et configuration

### 4.1 Définitions et concepts

#### Variable d'environnement (Environment Variable)

**Définition :** Variable dynamique qui affecte les processus en cours d'exécution sur un système, stockant des informations de configuration.

**Terminologie bilingue :**

- **Français :** Variable d'environnement, variable système
- **Anglais :** Environment variable, system variable

**Contexte DevOps :** Configuration d'applications, gestion des secrets, paramétrage des déploiements.

### 4.2 Types de variables

#### Variables système globales

**Définition :** Variables disponibles pour tous les utilisateurs et processus du système.

**Variables critiques pour DevOps :**

```bash
PATH         # Répertoires de recherche des commandes
HOME         # Répertoire utilisateur
USER         # Nom de l'utilisateur actuel
SHELL        # Shell par défaut
PWD          # Répertoire de travail actuel
```

#### Variables de session

**Définition :** Variables temporaires disponibles uniquement dans la session shell actuelle.

**Exemples d'utilisation DevOps :**

```bash
export API_KEY="secret123"           # Clé API temporaire
export NODE_ENV="production"         # Environnement d'exécution
export DATABASE_URL="postgresql://..." # Configuration base de données
```

### 4.3 Commandes de gestion des variables

#### Affichage des variables

```bash
env                    # Toutes les variables d'environnement
echo $VARIABLE         # Afficher une variable spécifique
printenv PATH          # Afficher PATH spécifiquement
set                    # Variables shell et d'environnement
```

#### Définition et export

```bash
# Variable locale (session actuelle seulement)
VARIABLE="valeur"

# Variable d'environnement (héritée par processus enfants)
export VARIABLE="valeur"

# Variable temporaire pour une commande
VARIABLE="valeur" commande
```

### 4.4 Configuration persistante

#### Fichiers de profil système

**Définition :** Fichiers exécutés automatiquement lors de l'ouverture d'une session shell.

**Hiérarchie des fichiers de profil :**

```bash
/etc/profile              # Configuration système globale
/etc/bash.bashrc          # Configuration bash globale
~/.bashrc                 # Configuration utilisateur (bash)
~/.profile                # Configuration utilisateur (tous shells)
~/.bash_profile           # Configuration bash utilisateur (login)
```

#### Ordre d'exécution

```
Séquence de chargement lors du login :
1. /etc/profile
2. ~/.bash_profile (ou ~/.profile si inexistant)
3. ~/.bashrc (si appelé depuis bash_profile)
```

#### Exemples de configuration DevOps

**Fichier ~/.bashrc :**

```bash
# Alias DevOps courants
alias ll='ls -la'
alias la='ls -A'
alias k='kubectl'
alias tf='terraform'

# Variables d'environnement
export EDITOR='vim'
export KUBECONFIG='~/.kube/config'
export GOPATH='~/go'

# Ajout de répertoires au PATH
export PATH="$PATH:~/bin:/usr/local/go/bin"

# Historique amélioré
export HISTSIZE=10000
export HISTFILESIZE=20000
```

### 4.5 Cas d'usage DevOps

#### Configuration d'outils

```bash
# Docker
export DOCKER_HOST="tcp://localhost:2376"

# Kubernetes
export KUBECONFIG="~/.kube/prod-config"

# Cloud providers
export AWS_PROFILE="production"
export AZURE_SUBSCRIPTION_ID="xxx-xxx-xxx"
```

#### Gestion des secrets

```bash
# Via fichier .env (non versionné)
source .env

# Via gestionnaire de secrets
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id prod/db --query SecretString --output text)
```

### 4.6 Application pratique

# Conversion binaire -> octal

rwx = 111 (binaire) = 7 (octal)
r-x = 101 (binaire) = 5 (octal)
r-- = 100 (binaire) = 4 (octal)

# Exemples courants

644 = rw-r--r-- # Fichier standard
755 = rwxr-xr-x # Script exécutable
600 = rw------- # Fichier privé

````

### 3.3 Modification des permissions

```bash
# Syntaxe symbolique
chmod u+x script.sh # Ajouter exécution pour propriétaire
chmod g-w fichier.txt # Retirer écriture pour groupe
chmod o=r fichier.txt # Autres: lecture seule

# Syntaxe octale
chmod 755 script.sh # rwxr-xr-x
chmod 644 config.yml # rw-r--r--
chmod 600 secret.key # rw-------
````

### 3.4 Propriété des fichiers

```bash
# Changer le propriétaire
sudo chown devops:devops fichier.txt
sudo chown -R nginx:nginx /var/www/

# Changer seulement le groupe
sudo chgrp developers projet/
```

---

## 4. Variables d'environnement et configuration

### 4.1 Concept des variables d'environnement

Les **variables d'environnement** sont des valeurs stockées par le système d'exploitation qui peuvent être utilisées par les programmes. Elles configurent le comportement des applications et scripts.

```bash
# Afficher toutes les variables
env

# Afficher une variable spécifique
echo $HOME # Répertoire personnel
echo $PATH # Chemins des exécutables
echo $USER # Nom d'utilisateur
```

### 4.2 Variables système importantes

```bash
# Variables essentielles
HOME=/home/devops # Répertoire personnel
PATH=/usr/bin:/bin:/usr/local/bin # Chemins exécutables
USER=devops # Utilisateur courant
SHELL=/bin/bash # Shell par défaut
PWD=/current/directory # Répertoire courant
```

### 4.3 Définir des variables

```bash
# Variable temporaire (session courante)
export DATABASE_URL="postgresql://localhost:5432/app"
export API_KEY="abc123xyz789"

# Vérifier la variable
echo $DATABASE_URL

# Variable dans un script
#!/bin/bash
ENVIRONMENT="production"
CONFIG_FILE="/etc/app/config.yml"
```

### 4.4 Configuration permanente

```bash
# Fichier ~/.bashrc (utilisateur)
echo 'export NODE_ENV=development' >> ~/.bashrc
echo 'export PORT=3000' >> ~/.bashrc

# Fichier /etc/environment (système)
sudo echo 'JAVA_HOME=/usr/lib/jvm/java-11' >> /etc/environment

# Recharger la configuration
source ~/.bashrc
```

### 4.5 Variables pour DevOps

```bash
# Configuration application
export APP_ENV=production
export DEBUG=false
export LOG_LEVEL=info

# Configuration base de données
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=webapp

# Configuration services
export REDIS_URL=redis://localhost:6379
export NGINX_PORT=80
```

### 4.6 Application pratique avancée

📝 **LAB 4 - Challenge** - Configuration environnement DevOps : `S1_S1_S1_lab4_env_config.sh`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge optionnel permet d'approfondir les concepts de configuration système et d'explorer des applications avancées en autonomie.

Configurer un environnement de développement multi-projets avec variables d'environnement pour une application web.

- **Objectif** : Créer un setup complet d'environnement de développement automatisé
- **Statut** : Activité bonus, hors des 2 heures de séance
- **Contexte** : Configuration d'un poste de développement pour équipe DevOps multi-projets
- **Niveau** : Avancé, concepts d'excellence
- **Instructions** :

1.  Créer un script de configuration d'environnement de développement
2.  Définir les variables pour différents environnements (dev, staging, prod)
3.  Configurer les chemins et outils de développement
4.  Créer un système de profils d'environnement commutables
5.  Ajouter des fonctions de validation et de debugging

- **Critères d'évaluation** : Configuration complète, flexibilité, validation, documentation
- **Durée estimée** : 30-45 minutes (hors séance)
- **Fichier de travail** : `S1_S1_S1_lab4_env_config.sh`

---

## 5. Récapitulatif et prochaines étapes

### 5.1 Concepts maîtrisés

À l'issue de cette séance, vous maîtrisez :

- **Navigation système** : Hiérarchie FHS et chemins Linux
- **Gestion fichiers** : Création, modification, organisation
- **Permissions Unix** : Sécurisation et contrôle d'accès
- **Variables d'environnement** : Configuration et personnalisation

### 5.2 Compétences DevOps acquises

- Automatisation de tâches système avec scripts bash
- Configuration sécurisée d'environnements de développement
- Gestion des permissions selon les bonnes pratiques
- Préparation d'infrastructures pour déploiements

### 5.3 Prochaines étapes

**Séance 2 - Gestion des processus et services :**

- Surveillance et contrôle des processus système
- Administration des services avec systemd
- Planification des tâches avec cron
- Monitoring des performances système

**Préparation recommandée :**

- Réviser les LABs de cette séance
- Pratiquer les commandes de base en autonomie
- Lire la documentation systemd (liens en ressources)

---

## 6. Ressources complémentaires

### 6.1 Documentation officielle

- [Linux Documentation Project](https://tldp.org/)
- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/fhs.shtml)

### 6.2 Commandes de référence

```bash
# Aide sur les commandes
man ls # Manuel complet
ls --help # Aide rapide
info bash # Documentation détaillée

# Historique et navigation
history # Historique des commandes
!! # Répéter dernière commande
!grep # Répéter dernière commande commençant par grep
```

### 6.3 Outils d'administration

- **htop** : Monitoring processus interactif
- **tree** : Affichage arborescent
- **ncdu** : Analyse d'espace disque
- **tmux** : Multiplexeur de terminaux

---

_Formateur : Hassan ESSADIK | Sprint 1 - Séance 1 : Linux Fondamentaux_
