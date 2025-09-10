# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 1 - Séance 2 : Gestion des Processus et Services

## Objectifs pédagogiques

- Maîtriser la gestion des processus Linux pour l'administration système
- Configurer et superviser les services avec systemd en production
- Surveiller les ressources système et analyser les performances
- Analyser les logs système pour le troubleshooting DevOps

## Objectifs techniques

ps, top, htop, systemctl, journalctl, systemd, monitoring, processus, services, logs, ressources système

## Table des matières

1. [Fondamentaux des processus Linux](#1-fondamentaux-des-processus-linux)
2. [Outils d'analyse et de surveillance des processus](#2-outils-danalyse-et-de-surveillance-des-processus)
3. [Services systemd en production](#3-services-systemd-en-production)
4. [Monitoring des ressources système](#4-monitoring-des-ressources-système)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)
6. [Ressources complémentaires](#6-ressources-complémentaires)

## 1. Fondamentaux des processus Linux

### Définitions et terminologie

**Processus (Process)** : En informatique système, un processus est une instance active d'un programme en cours d'exécution dans l'espace mémoire du système d'exploitation. Il constitue l'unité fondamentale d'allocation de ressources par le noyau Linux.

**Programme vs Processus** : Un programme est un fichier exécutable statique stocké sur disque, tandis qu'un processus est l'instance dynamique de ce programme chargée en mémoire avec ses ressources allouées.

**PID (Process Identifier)** : Numéro entier unique (1-32768) attribué séquentiellement par le noyau Linux à chaque nouveau processus pour son identification univoque dans le système.

**PPID (Parent Process Identifier)** : Identifiant numérique du processus créateur, établissant la relation hiérarchique parent-enfant essentielle à la gestion des processus Linux.

### Architecture conceptuelle des processus

Les processus Linux s'organisent selon une structure arborescente hiérarchique où chaque processus possède un parent unique, à l'exception du processus init (systemd) qui constitue la racine de l'arbre.

**Schéma hiérarchique des processus :**

```
Niveau 0:  systemd (PID=1, PPID=0)
           │
Niveau 1:  ├── NetworkManager (PID=742, PPID=1)
           ├── sshd (PID=1234, PPID=1)
           └── mysql (PID=2345, PPID=1)
           │
Niveau 2:  sshd ──> bash (PID=1456, PPID=1234)
           │
Niveau 3:  bash ──> nginx (PID=1789, PPID=1456)
```

**Diagramme des relations parent-enfant :**

```
┌─────────────┐
│  systemd    │  ← Processus racine (init)
│   PID=1     │
└──────┬──────┘
       │
   ┌───┴───┐
   │ sshd  │  ← Processus parent (daemon SSH)
   │ 1234  │
   └───┬───┘
       │
   ┌───┴───┐
   │ bash  │  ← Processus enfant (shell utilisateur)
   │ 1456  │
   └───┬───┘
       │
   ┌───┴───┐
   │ nginx │  ← Processus petit-enfant (serveur web)
   │ 1789  │
   └───────┘
```

### États et cycle de vie des processus

**État de processus** : Statut instantané décrivant l'activité actuelle d'un processus dans le système d'exploitation. Linux définit cinq états principaux gouvernant le comportement des processus.

**Diagramme des transitions d'états :**

```
    [NEW]
      │
      ▼
   [READY] ◄──┐
      │       │
      ▼       │
  [RUNNING] ──┤
      │       │
      ├───────┘
      │
      ▼
 [WAITING] ──┐
      │      │ Interruption
      │      │ ou signal
      ▼      ▼
 [TERMINATED]
```

**Table des états processus :**

**Note importante** : Le diagramme ci-dessus utilise les états théoriques génériques des systèmes d'exploitation, tandis que Linux utilise des codes spécifiques pour ses états réels. Cette distinction est essentielle pour comprendre la différence entre la théorie OS et la pratique Linux.

| État (Français) | Code Linux | Équivalence théorique | Description technique       | Cas d'usage DevOps          |
| --------------- | ---------- | --------------------- | --------------------------- | --------------------------- |
| En cours        | R          | RUNNING               | Processus actif ou prêt     | Application en production   |
| Endormi         | S          | WAITING               | Attente événement ext.      | Service réseau inactif      |
| Sommeil profond | D          | WAITING (bloqué)      | Attente I/O critique        | Opération disque/réseau     |
| Zombie          | Z          | TERMINATED (partiel)  | Terminé, en attente cleanup | Processus parent défaillant |
| Arrêté          | T          | READY (suspendu)      | Suspendu par signal/debug   | Maintenance ou débogage     |

**Explication de la différence** :

- **Modèle théorique** : NEW → READY → RUNNING → WAITING → TERMINATED (5 états génériques)
- **Implémentation Linux** : R, S, D, Z, T (codes spécifiques avec nuances techniques)
- **Correspondance** : WAITING se divise en S (interruptible) et D (non-interruptible) dans Linux

### Exemple simple d'analyse d'état

```bash
# Visualiser l'état du processus init (PID 1)
ps aux | head -2
```

**Sortie réelle de la commande :**

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  1.2 167384 12724 ?        Ss   Sep08   0:01 /sbin/init
```

**Analyse détaillée ligne par ligne :**

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  1.2 167384 12724 ?        Ss   Sep08   0:01 /sbin/init
│              │   │    │      │     │   │        │     │      │     │
│              │   │    │      │     │   │        │     │      │     └─ Commande complète
│              │   │    │      │     │   │        │     │      └─ Temps CPU cumulé (0:01)
│              │   │    │      │     │   │        │     └─ Date démarrage (Sep08)
│              │   │    │      │     │   │        └─ État : Ss (Sleep + session leader)
│              │   │    │      │     │   └─ Terminal : ? (processus système)
│              │   │    │      │     └─ Mémoire résidente RSS (12724 KB = 12.4 MB)
│              │   │    │      └─ Mémoire virtuelle VSZ (167384 KB = 163.5 MB)
│              │   │    └─ Pourcentage mémoire physique utilisée (1.2%)
│              │   └─ Pourcentage utilisation CPU actuelle (0.0%)
│              └─ Process ID = 1 (processus racine système)
└─ Utilisateur propriétaire (root)
```

**Analyse technique spécialisée DevOps :**

- **PID = 1** : Processus init/systemd, racine de tous les processus système
- **USER = root** : Privilèges administrateur requis pour l'initialisation système
- **STAT = Ss** :
  - `S` = Sleeping (en attente, comportement normal pour init)
  - `s` = Session leader (chef de session, rôle d'init)
- **TTY = ?** : Aucun terminal associé (processus système pur)
- **VSZ vs RSS** : 163.5 MB virtuels vs 12.4 MB réels (optimisation mémoire)
- **%CPU = 0.0** : Consommation CPU minimale (init reste en veille)
- **TIME = 0:01** : Très peu de temps CPU depuis le démarrage (efficacité)

- **Signification pour l'administration système :**

- Processus critique : Ne jamais arrêter le PID 1
- Indicateur de stabilité : init stable = système stable
- Point de référence : Tous les autres processus descendent de celui-ci

## 2. Outils d'analyse et de surveillance des processus

### Définitions et concepts fondamentaux

**Commande ps (Process Status)** : Utilitaire système Unix/Linux permettant d'afficher un instantané des processus actifs au moment de l'exécution. Elle constitue l'outil de base pour l'inspection des processus.

**Commande top (Table of Processes)** : Programme interactif de surveillance en temps réel affichant dynamiquement la liste des processus triés par consommation de ressources système.

**Signal Unix** : Mécanisme de communication inter-processus (IPC) permettant l'envoi d'instructions de contrôle aux processus via le noyau. Les signaux constituent l'interface standard de gestion des processus Linux.

### Architecture des outils de gestion

**Diagramme des outils de surveillance :**

```
┌─────────────────────────────────────────┐
│           ESPACE UTILISATEUR            │
├─────────────┬─────────────┬─────────────┤
│     ps      │    top      │    htop     │
│ (statique)  │ (dynamique) │ (amélioré)  │
└─────────────┴─────────────┴─────────────┘
              │
┌─────────────▼─────────────────────────────┐
│         ESPACE NOYAU                      │
│  /proc/[PID]/stat, /proc/[PID]/status     │
│         (pseudo-filesystem)               │
└───────────────────────────────────────────┘
```

### Commandes de visualisation fondamentales

#### Syntaxe ps et options

```bash
# Affichage standard BSD
ps aux
```

**Explication détaillée de la syntaxe ps aux :**

- `a` : Affiche tous les processus de tous les utilisateurs
- `u` : Format orienté utilisateur avec colonnes détaillées
- `x` : Inclut les processus sans terminal de contrôle

**Structure de sortie ps aux :**

```
USER   PID %CPU %MEM    VSZ   RSS TTY STAT START   TIME COMMAND
www    1234  0.5  2.1  45208 8764  ?   S    12:30   0:05 nginx
│      │     │    │     │     │    │   │    │       │    │
│      │     │    │     │     │    │   │    │       │    └─ Commande
│      │     │    │     │     │    │   │    │       └─ Temps CPU total
│      │     │    │     │     │    │   │    └─ Heure démarrage
│      │     │    │     │     │    │   └─ État processus
│      │     │    │     │     │    └─ Terminal (? = aucun)
│      │     │    │     │     └─ Mémoire résidente (KB)
│      │     │    │     └─ Mémoire virtuelle (KB)
│      │     │    └─ % mémoire physique
│      │     └─ % utilisation CPU
│      └─ PID unique
└─ Utilisateur propriétaire
```

#### Tri et filtrage simple

```bash
# Top 5 processus CPU
ps aux --sort=-%cpu | head -6

# Top 5 processus mémoire
ps aux --sort=-%mem | head -6
```

### Monitoring temps réel

**Interface top** : Programme de surveillance interactive offrant une vue dynamique actualisée automatiquement des processus système triés par consommation de ressources.

**Schéma interface top :**

```
┌─────────────────────────────────────────────────────┐
│ En-tête système (load, CPU, mémoire)               │
├─────────────────────────────────────────────────────┤
│ PID USER %CPU %MEM   TIME+ COMMAND                 │
│ 1234 www   15.2  3.4  0:45.2 nginx                │
│ 5678 mysql 12.1  8.7  2:15.8 mysqld               │
│ └─ Processus triés par consommation               │
└─────────────────────────────────────────────────────┘
```

**Raccourcis top essentiels :**

- `P` : Tri par CPU
- `M` : Tri par mémoire
- `q` : Quitter

### Gestion des signaux Unix

**Qu'est-ce qu'un signal Unix ?**

Un signal est comme un "message" que le système d'exploitation peut envoyer à un programme qui tourne sur l'ordinateur. C'est un peu comme si vous tapiez sur l'épaule de quelqu'un pour lui dire quelque chose d'important.

**Pourquoi utilise-t-on les signaux ?**

Les signaux permettent de communiquer avec les programmes sans les interrompre brutalement. Par exemple :

- Demander à un programme de s'arrêter proprement (comme fermer la porte en sortant)
- Demander à un programme de relire sa configuration (comme dire "regarde, j'ai changé tes paramètres")
- Forcer un programme bloqué à s'arrêter (comme débrancher un appareil qui ne répond plus)

**Les 3 signaux les plus importants pour un débutant :**

| Signal  | Numéro | Ce que ça fait                     | Exemple simple                        |
| ------- | ------ | ---------------------------------- | ------------------------------------- |
| SIGTERM | 15     | Demande poliment d'arrêter         | "Peux-tu t'arrêter s'il te plaît ?"   |
| SIGKILL | 9      | Force l'arrêt immédiat             | "STOP ! Tu t'arrêtes maintenant !"    |
| SIGHUP  | 1      | Demande de relire la configuration | "Va regarder tes nouveaux paramètres" |

**Analogie avec la vraie vie :**

Imaginez que vous gérez une équipe :

- **SIGTERM** = Vous dites : "Finissez votre tâche actuelle puis rentrez chez vous"
- **SIGKILL** = Vous dites : "Tout le monde sort MAINTENANT !"
- **SIGHUP** = Vous dites : "Il y a de nouvelles consignes, allez les lire"

**Comment envoyer un signal (commande simple) :**

```bash
# Envoyer SIGTERM (arrêt poli) au processus 1234
kill 1234

# Envoyer SIGKILL (arrêt forcé) au processus 1234
kill -9 1234

# Envoyer SIGHUP (recharger config) au processus 1234
kill -1 1234
```

**Retenir l'essentiel :**

- Signal = message au programme
- SIGTERM (15) = arrêt poli
- SIGKILL (9) = arrêt forcé
- SIGHUP (1) = recharge configuration

📝 **LAB 1** - Analyse des processus système : `S1_S1_S1_lab1_analyse_processus.sh`

**Énoncé du LAB 1** :

Vous êtes administrateur système d'un serveur web de production. Votre mission est d'analyser l'état des processus pour identifier les services critiques et optimiser les performances.

- **Objectif** : Maîtriser l'analyse des processus Linux en environnement de production
- **Contexte** : Audit de performance sur serveur web avec base de données
- **Instructions** :
  1. Lister tous les processus actifs avec leurs attributs (ps aux)
  2. Identifier la hiérarchie des processus (pstree)
  3. Localiser les processus consommant le plus de CPU et mémoire
  4. Analyser les services web et base de données actifs
  5. Créer un rapport d'audit système automatisé
- **Critères d'évaluation** : Identification correcte des services critiques, analyse pertinente des ressources
- **Durée estimée** : 15 minutes
- **Fichier de travail** : `S1_S1_S1_lab1_analyse_processus.sh`

## 3. Services systemd en production

### Définitions et terminologie systemd

**systemd** :

- C'est le "chef d'orchestre" du système Linux moderne. Dès que l'ordinateur démarre, systemd (prononcé "system D") est le tout premier programme lancé (PID 1).
- Il s'occupe de démarrer, arrêter et surveiller tous les autres programmes importants (appelés "services").
- Il remplace l'ancien système appelé SysV init.

**Service (service systemd)** :

- Un service est un programme qui tourne en arrière-plan (ex : serveur web, base de données, gestionnaire réseau).
- Exemple : nginx (serveur web), mysql (base de données), sshd (accès à distance).
- Les services sont gérés par systemd pour garantir qu'ils démarrent, s'arrêtent ou redémarrent correctement.

**Unité (unit systemd)** :

- Une "unité" est un objet que systemd sait gérer. Il existe plusieurs types d'unités :
  - Les services (.service)
  - Les timers (.timer) pour les tâches planifiées
  - Les points de montage (.mount) pour les disques
  - Les sockets (.socket) pour la communication
  - Les targets (.target) pour regrouper plusieurs unités
- Chaque unité a un fichier de configuration qui explique à systemd comment la gérer.

**Target (target systemd)** :

- Un "target" est un groupe d'unités qui permet de définir un état du système (par exemple, "mode multi-utilisateur" ou "mode graphique").
- C'est comme un "profil" qui active plusieurs services en même temps.

**Exemple illustré** :

Imaginons que vous démarrez votre ordinateur :

1. systemd se lance (c'est le chef d'orchestre).
2. Il lit la liste des services à démarrer (ex : réseau, affichage, SSH).
3. Il démarre chaque service dans le bon ordre, selon les besoins.
4. Si un service tombe en panne, systemd peut le relancer automatiquement.

**Schéma simplifié :**

```
         [Ordinateur démarre]
                 |
             [systemd]
                 |
   +------+------+-------+
   |      |      |       |
[réseau][ssh][web][autres]
```

**Résumé :**

- systemd = chef d'orchestre
- service = musicien (programme important)
- unité = partition (fichier de configuration)
- target = groupe de musiciens (ensemble de services)

> Retenez : Pour gérer les services sur Linux, on utilise systemd et la commande `systemctl`.

### Architecture conceptuelle systemd

**Comment systemd est organisé ?**

systemd fonctionne comme une entreprise bien organisée avec différents départements et outils de gestion.

**Schéma simple de l'organisation systemd :**

```
         [Vous = Administrateur]
                 |
        [Outils de commande]
     systemctl | journalctl | autres
                 |
            [systemd]
         (Le chef principal)
                 |
    +--------+--------+--------+
    |        |        |        |
[Services] [Targets] [Timers] [Mounts]
```

**Analogie avec une entreprise :**

- **Vous** = Le directeur qui donne les ordres
- **systemctl** = Votre assistante qui transmet vos demandes
- **systemd** = Le chef d'équipe principal
- **Services** = Les employés qui font le travail quotidien
- **Targets** = Les équipes de projet
- **Timers** = Le planning des tâches répétitives

**Les outils que vous utilisez tous les jours :**

| Outil      | À quoi ça sert             | Exemple d'usage                     |
| ---------- | -------------------------- | ----------------------------------- |
| systemctl  | Contrôler les services     | Démarrer, arrêter nginx             |
| journalctl | Voir les logs (historique) | Vérifier pourquoi un service plante |

### Types d'unités systemd (expliqués simplement)

**Qu'est-ce qu'une "unité" ?**

Une unité, c'est comme un "dossier" que systemd utilise pour organiser les différents éléments du système. Chaque type d'unité a un rôle spécifique.

**Les 6 types d'unités les plus importants :**

| Type    | Extension | Qu'est-ce que c'est ?                   | Exemples concrets                            |
| ------- | --------- | --------------------------------------- | -------------------------------------------- |
| Service | .service  | Programmes qui tournent en permanence   | nginx (serveur web), mysql (base de données) |
| Target  | .target   | Groupes de services à démarrer ensemble | "mode serveur", "mode graphique"             |
| Timer   | .timer    | Tâches programmées (comme un réveil)    | Sauvegarde automatique tous les soirs        |
| Socket  | .socket   | Points de communication                 | Connexions réseau, APIs                      |
| Mount   | .mount    | Disques et dossiers à monter            | Clé USB, disque dur externe                  |
| Path    | .path     | Surveillance de fichiers/dossiers       | "Fais quelque chose si ce fichier change"    |

**Exemples pratiques :**

- **Service nginx.service** = "Lance le serveur web nginx et garde-le actif"
- **Target multi-user.target** = "Démarre tous les services nécessaires pour un serveur"
- **Timer backup.timer** = "Lance la sauvegarde tous les jours à 2h du matin"

**Retenez l'essentiel :**

- systemd = chef d'orchestre du système
- systemctl = votre outil principal pour le contrôler
- Services = programmes importants qui tournent
- Targets = groupes de services
- Autres types = fonctions spécialisées

### Commandes systemctl fondamentales

**systemctl** : Interface de commande principale pour contrôler le gestionnaire systemd et les services qu'il supervise.

#### Gestion du cycle de vie

```bash
# Démarrage d'un service
systemctl start nginx

# Arrêt d'un service
systemctl stop nginx

# Redémarrage complet
systemctl restart nginx
```

#### États et vérifications

```bash
# État détaillé d'un service
systemctl status nginx

# Vérification simple active/inactive
systemctl is-active nginx

# Vérification activation au boot
systemctl is-enabled nginx
```

**Diagramme des états de service :**

```
[disabled] ──enable──► [enabled] ──start──► [active]
     ▲                    │                    │
     │                    │                    │
     └───── disable ──────┘       stop ───────┘
                                   │
                              [inactive]
```

### Configuration d'un service simple

> Cette section explique comment créer un fichier de configuration pour systemd, étape par étape.

**Qu'est-ce qu'un fichier .service ?**

Un fichier .service est comme une "carte d'identité" pour un programme. Il explique à systemd :

- Qui est ce programme
- Comment le démarrer
- Quand le démarrer
- Que faire s'il plante

**Structure d'un fichier .service (avec commentaires détaillés) :**

```ini
# Nom du fichier : /etc/systemd/system/webapp.service
# (Les lignes qui commencent par # sont des commentaires)

# === SECTION [Unit] : Informations générales ===
[Unit]
# Description : nom affiché quand on liste les services
Description=Application Web DevOps

# After : attend que le réseau soit disponible avant de démarrer
# (comme dire "attends que le wifi soit connecté")
After=network.target

# === SECTION [Service] : Comment lancer le programme ===
[Service]
# Type=simple : le programme reste au premier plan
# (pas besoin de chercher son PID)
Type=simple

# ExecStart : la commande exacte pour lancer le programme
# (comme double-cliquer sur une icône)
ExecStart=/opt/webapp/bin/server

# Restart=always : si le programme plante, le relancer automatiquement
# (comme un gardien qui surveille)
Restart=always

# === SECTION [Install] : Quand démarrer automatiquement ===
[Install]
# WantedBy : démarrer avec le "target" multi-user
# (quand le système est prêt pour les utilisateurs)
WantedBy=multi-user.target
```

**Explication des 3 sections principales :**

| Section     | À quoi ça sert                                 | Analogie                      |
| ----------- | ---------------------------------------------- | ----------------------------- |
| `[Unit]`    | Informations générales et dépendances          | Carte d'identité du programme |
| `[Service]` | Instructions pour lancer et gérer le programme | Mode d'emploi du programme    |
| `[Install]` | Règles de démarrage automatique                | Programmation d'un réveil     |

**Exemple concret : créer un service pour une application web**

```bash
# 1. Créer le fichier de configuration
sudo nano /etc/systemd/system/monapp.service

# 2. Dire à systemd de lire le nouveau fichier
sudo systemctl daemon-reload

# 3. Activer le service (démarrage automatique)
sudo systemctl enable monapp

# 4. Démarrer le service maintenant
sudo systemctl start monapp

# 5. Vérifier que ça marche
sudo systemctl status monapp
```

**Points importants à retenir :**

- **Emplacement** : Les fichiers .service vont dans `/etc/systemd/system/`
- **Extension** : Toujours finir par `.service`
- **Rechargement** : Faire `systemctl daemon-reload` après chaque modification
- **Test** : Toujours vérifier avec `systemctl status nom-du-service`

### 3.1 Application pratique

📝 **LAB 2** - Gestion des services systemd : `S1_S1_S1_lab2_gestion_services.sh`

**Énoncé du LAB 2** :

Vous devez configurer et gérer les services d'une infrastructure web incluant nginx et une base de données. L'objectif est de maîtriser systemctl pour les opérations de production.

- **Objectif** : Maîtriser les commandes systemctl pour la gestion des services en production
- **Contexte** : Configuration d'un serveur web avec base de données MySQL
- **Instructions** :
  1. Vérifier l'état des services nginx et mysql
  2. Démarrer et arrêter les services de manière contrôlée
  3. Configurer le démarrage automatique au boot
  4. Recharger les configurations sans interruption
  5. Analyser les dépendances entre services
- **Critères d'évaluation** : Manipulation correcte des services, compréhension des états
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S1_S1_lab2_gestion_services.sh`

## 4. Monitoring des ressources système

### Définitions et concepts du monitoring

**Monitoring système** : Processus continu de surveillance et de mesure des ressources informatiques pour assurer la performance, la disponibilité et la stabilité des services en production.

**Ressource système** : Composant matériel ou logiciel mesurable dont la disponibilité et l'utilisation impactent les performances globales du système (CPU, mémoire, disque, réseau).

**Métriques (Metrics)** : Valeurs numériques quantifiables représentant l'état d'une ressource système à un instant donné. Les métriques constituent la base de l'observabilité.

**Load Average** : Métrique Linux représentant le nombre moyen de processus actifs ou en attente d'exécution sur une période donnée (1, 5, 15 minutes).

### Architecture du monitoring Linux

**Diagramme des sources de métriques :**

```
┌─────────────────────────────────────────────────────┐
│              OUTILS DE MONITORING                   │
├─────────────┬─────────────┬─────────────┬───────────┤
│    top      │    free     │     df      │  iostat   │
│  (CPU/proc) │ (mémoire)   │  (disque)   │ (I/O)     │
└─────────────┴─────────────┴─────────────┴───────────┘
              │
┌─────────────▼─────────────────────────────────────────┐
│               FILESYSTEM /proc                      │
├─────────────┬─────────────┬─────────────┬─────────────┤
│ /proc/stat  │/proc/meminfo│/proc/diskstats│/proc/net │
│ (CPU stats) │(mémoire)    │(disque I/O) │(réseau)   │
└─────────────┴─────────────┴─────────────┴─────────────┘
              │
┌─────────────▼─────────────────────────────────────────┐
│                  NOYAU LINUX                        │
│           (collecte des statistiques)               │
└─────────────────────────────────────────────────────┘
```

### Surveillance CPU et charge système

#### Métriques CPU fondamentales

**CPU Time** : Temps processeur consommé par les processus, mesuré en cycles d'horloge et converti en pourcentages d'utilisation.

**États CPU Linux :**

- `us` (user) : Temps en mode utilisateur
- `sy` (system) : Temps en mode noyau
- `id` (idle) : Temps d'inactivité
- `wa` (wait) : Attente opérations I/O

#### Analyse du load average

**Qu'est-ce que le load average ?**

Le load average, c'est comme un "indicateur de charge" qui mesure à quel point votre ordinateur est occupé. Imaginez votre processeur comme une route :

- **Load average bas** = Route fluide, peu de voitures
- **Load average élevé** = Embouteillage, beaucoup de voitures qui attendent

**Comment lire la sortie de la commande uptime :**

```bash
uptime
# Exemple de sortie :
# 10:30:01 up 15 days, 3:45, 2 users, load average: 0.08, 0.12, 0.09
#    │        │        │       │           │     │     │
#    │        │        │       │           │     │     └─ Charge sur 15 minutes
#    │        │        │       │           │     └─ Charge sur 5 minutes
#    │        │        │       │           └─ Charge sur 1 minute
#    │        │        │       └─ Nombre d'utilisateurs connectés
#    │        │        └─ Temps de connexion (heures:minutes)
#    │        └─ Temps depuis le dernier redémarrage
#    └─ Heure actuelle
```

**Interprétation du load average (règle simple) :**

| Load Average | État du système | Analogie                    | Action recommandée |
| ------------ | --------------- | --------------------------- | ------------------ |
| 0.00 - 0.70  | Très bien       | Route fluide                | Rien à faire       |
| 0.70 - 1.00  | Acceptable      | Route avec un peu de trafic | Surveiller         |
| 1.00 - 1.50  | Attention       | Début d'embouteillage       | Investiguer        |
| > 1.50       | Problème        | Gros embouteillage          | Action urgente     |

**Règle d'or pour évaluer le load average :**

- **Serveur 1 processeur** : Load > 1.0 = surchargé
- **Serveur 2 processeurs** : Load > 2.0 = surchargé
- **Serveur 4 processeurs** : Load > 4.0 = surchargé

**Exemple pratique d'analyse :**

```bash
# 1. Vérifier la charge actuelle
uptime
# Sortie : load average: 0.75, 1.20, 2.10

# 2. Vérifier le nombre de processeurs
nproc
# Sortie : 2

# 3. Analyse :
# - Load 1 min = 0.75 (OK, en dessous de 2.0)
# - Load 5 min = 1.20 (OK, en dessous de 2.0)
# - Load 15 min = 2.10 (ATTENTION, au-dessus de 2.0)
# Conclusion : Le système était surchargé il y a 15 minutes mais ça s'améliore
```

**Pourquoi 3 valeurs de temps ?**

- **1 minute** : Situation actuelle (photo instantanée)
- **5 minutes** : Tendance récente (film court)
- **15 minutes** : Tendance générale (film long)

**Commandes utiles pour investiguer une charge élevée :**

```bash
# Voir les processus qui consomment le plus de CPU
ps aux --sort=-%cpu | head -5

# Surveiller en temps réel
top

# Historique de charge
uptime
```

### Surveillance mémoire système

**Mémoire physique (RAM)** : Mémoire volatile directement accessible par le processeur pour stocker les données et programmes actifs.

**Mémoire virtuelle** : Espace d'adressage logique alloué aux processus, pouvant dépasser la mémoire physique grâce au mécanisme de swap.

**Swap** : Espace disque utilisé comme extension de la mémoire physique quand celle-ci est saturée.

#### Structure mémoire Linux

**Diagramme allocation mémoire :**

```
┌─────────────────────────────────────────┐ ← Mémoire totale
│              MÉMOIRE LIBRE              │
├─────────────────────────────────────────┤
│              BUFFERS/CACHE              │ ← Cache système
├─────────────────────────────────────────┤
│            PROCESSUS ACTIFS             │ ← Mémoire utilisée
├─────────────────────────────────────────┤
│               NOYAU                     │ ← Système
└─────────────────────────────────────────┘
```

#### Exemple simple surveillance mémoire

```bash
# Vue globale mémoire
free -h

# Processus gourmands mémoire
ps aux --sort=-%mem | head -4
```

### Surveillance disque et I/O

**I/O (Input/Output)** : Opérations de lecture/écriture entre le processeur et les périphériques de stockage. Les I/O constituent souvent le goulot d'étranglement principal des systèmes.

**IOPS** : Input/Output Operations Per Second, métrique mesurant le nombre d'opérations I/O qu'un périphérique peut traiter par seconde.

#### Exemple simple surveillance disque

```bash
# Espace disque par partition
df -h

# Utilisation par répertoire
du -sh /var/log
```

### Gestion des logs avec journalctl

**journalctl** : Utilitaire systemd pour consulter et analyser les logs du système. Il offre une interface unifiée pour accéder aux journaux systemd stockés de manière structurée.

**Journal systemd** : Système de logging binaire centralisé qui collecte et structure tous les messages du système, des services et des applications.

#### Filtrage et recherche de logs

```bash
# Logs d'un service spécifique
journalctl -u nginx

# Filtrage temporel simple
journalctl --since "1 hour ago"

# Logs d'erreur uniquement
journalctl -p err
```

**Niveaux de priorité syslog :**

| Niveau | Nom     | Description         |
| ------ | ------- | ------------------- |
| 0      | emerg   | Urgence système     |
| 1      | alert   | Alerte immédiate    |
| 2      | crit    | Condition critique  |
| 3      | err     | Erreur              |
| 4      | warning | Avertissement       |
| 5      | notice  | Notice importante   |
| 6      | info    | Information         |
| 7      | debug   | Message de débogage |

### 4.1 Application pratique

📝 **LAB 3** - Monitoring des ressources système : `S1_S1_S1_lab3_monitoring_ressources.sh`

**Énoncé du LAB 3** :

Vous devez surveiller les performances d'un serveur de production et identifier les goulots d'étranglement. L'objectif est de maîtriser les outils de monitoring pour assurer la stabilité du système.

- **Objectif** : Surveiller les ressources système et analyser les performances
- **Contexte** : Diagnostic de performance sur serveur web sous charge
- **Instructions** :
  1. Analyser l'utilisation CPU avec top et htop
  2. Surveiller la consommation mémoire et le swap
  3. Vérifier l'espace disque et l'activité I/O
  4. Identifier les processus consommateurs de ressources
  5. Créer un script de monitoring automatisé
- **Critères d'évaluation** : Identification correcte des problèmes de performance
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S1_S1_lab3_monitoring_ressources.sh`

### 4.2 Application pratique avancée

📝 **LAB 4 - Challenge** - Analyse forensique des logs : `S1_S1_S1_lab4_challenge.sh`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge optionnel permet d'approfondir les concepts vus en séance et d'explorer des applications avancées en autonomie.

- **Objectif** : Maîtriser l'analyse forensique des logs pour la détection d'incidents
- **Statut** : Activité bonus, hors des 2 heures de séance
- **Contexte** : Investigation sur serveur après suspicion d'intrusion
- **Instructions** :
  1. Analyser les logs d'authentification sur plusieurs jours
  2. Corréler les événements entre différents services
  3. Identifier les patterns d'attaque automatisés
  4. Tracer l'activité suspecte et son impact
  5. Créer un rapport d'incident complet avec timeline
- **Critères d'évaluation** : Méthodologie d'investigation, pertinence des conclusions
- **Durée estimée** : 30-45 minutes
- **Niveau** : Avancé, concepts d'excellence
- **Fichier de travail** : `S1_S1_S1_lab4_challenge.sh`

* : Activité bonus, hors des 2 heures de séance

- **Contexte** : Investigation sur serveur après suspicion d'intrusion
- **Instructions** :
  1. Analyser les logs d'authentification sur plusieurs jours
  2. Corréler les événements entre différents services
  3. Identifier les patterns d'attaque automatisés
  4. Tracer l'activité suspecte et son impact
  5. Créer un rapport d'incident complet avec timeline
- **Critères d'évaluation** : Méthodologie d'investigation, pertinence des conclusions
- **Durée estimée** : 30-45 minutes
- **Niveau** : Avancé, concepts d'excellence
- **Fichier de travail** : `S1_S1_S2_lab4_challenge.sh`

## 5. Récapitulatif et prochaines étapes

Cette séance a permis de maîtriser les concepts essentiels de la gestion des processus et services Linux pour l'environnement DevOps :

**Processus Linux** : Compréhension des états, hiérarchie et gestion via ps, top, htop

**Signaux Unix** : Contrôle des processus avec kill, gestion graceful vs forcée

**systemd moderne** : Gestion des services, configuration, supervision automatique

**Monitoring système** : Surveillance CPU, mémoire, disque pour la production

**Logs centralisés** : Analyse avec journalctl pour le troubleshooting

### Bonnes pratiques DevOps

- Toujours privilégier systemd pour les services de production
- Configurer le redémarrage automatique des services critiques
- Surveiller proactivement les métriques système
- Centraliser et analyser régulièrement les logs
- Documenter les procédures d'incident

### Prochaine séance

**Séance 3 : Réseaux et Sécurité Linux**

- Configuration réseau et interfaces
- Pare-feu et iptables/ufw
- SSH et authentification sécurisée
- Diagnostics réseau avancés

## 6. Ressources complémentaires

### Documentation officielle

- `man systemctl` - Manuel systemctl complet
- `man journalctl` - Guide journalctl et filtres
- `man ps` - Options avancées de ps
- [systemd.io](https://systemd.io) - Documentation systemd

### Outils recommandés

- **htop** : Monitoring interactif amélioré
- **iotop** : Surveillance I/O par processus
- **systemd-analyze** : Analyse performance boot
- **ncdu** : Analyse utilisation disque interactive

### Commandes de référence rapide

```bash
# Processus
ps aux --sort=-%cpu | head -10
top -o %MEM
kill -HUP $(pidof nginx)

# Services
systemctl status --all
systemctl list-units --failed
systemctl daemon-reload

# Monitoring
uptime && free -h && df -h
journalctl -p err --since "1 hour ago"
iostat -x 1 3
```

---

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 1 - Séance 2 : Gestion des Processus et Services_
