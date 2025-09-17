# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 2 - Séance 1 : Fondamentaux Bash pour DevOps

## Objectifs pédagogiques

- Découvrir les bases du scripting Bash et la syntaxe fondamentale
- Créer ses premiers scripts d'administration système DevOps
- Manipuler les variables, paramètres et structures de contrôle
- Automatiser des tâches administratives simples avec des scripts basiques

## Objectifs techniques

Scripts Bash de base, variables, paramètres, structures conditionnelles, boucles, redirection I/O, pipes, scripts administration système

## Table des matières

1. [Introduction au Scripting Bash](#1-introduction-au-scripting-bash)
2. [Variables et Paramètres](#2-variables-et-paramètres)
3. [Structures de Contrôle](#3-structures-de-contrôle)
4. [Structures Répétitives - Boucles](#4-structures-répétitives---boucles)
5. [Scripts d'Administration Système](#5-scripts-dadministration-système)

## 1. Introduction au Scripting Bash

### Définition : Script Bash

Un **script Bash** est un fichier texte contenant une séquence de commandes shell qui peuvent être exécutées automatiquement. Il permet d'automatiser les tâches répétitives d'administration système.

**Terminologie technique** :

- **Shebang** : Ligne `#!/bin/bash` indiquant l'interpréteur à utiliser (anglais : shebang)
- **Commande** : Instruction exécutable par le shell (anglais : command)
- **Script** : Fichier de commandes automatisées (anglais : script)

### Contexte d'utilisation DevOps

Les scripts Bash sont utilisés pour automatiser les déploiements, la configuration des serveurs, le monitoring et la maintenance d'infrastructure. Ils constituent la base de l'automation DevOps.

### Premier Script Bash

```bash
#!/bin/bash
# Shebang : indique au système d'utiliser l'interpréteur Bash pour exécuter ce script

# Mon premier script DevOps
# Commentaire de description : explique le but du script

# Affichage d'un en-tête formaté pour identifier le début du script
echo "=== Script de vérification système ==="

# Commande date : affiche la date et l'heure actuelles du système
echo "Date: $(date)"

# Commande whoami : affiche le nom de l'utilisateur qui exécute le script
echo "Utilisateur: $(whoami)"

# Commande pwd : affiche le répertoire courant (Print Working Directory)
echo "Répertoire: $(pwd)"

# Affichage d'un pied de page pour marquer la fin du script
echo "=== Fin de vérification ==="
```

**Schéma conceptuel** :

```
Structure Script Bash
├── Shebang (#!/bin/bash)
├── Commentaires (# description)
├── Commandes (echo, date, etc.)
└── Logique métier (DevOps)
```

### Application pratique

📝 **LAB 1** - Premier script Bash : `S1_S2_S1_lab1_premier_script.sh`

**Énoncé du LAB 1** :
Créez votre premier script Bash d'information système pour DevOps.

- **Objectif** : Écrire un script Bash basique qui affiche des informations système utiles
- **Contexte** : Script de diagnostic rapide pour vérification d'environnement DevOps
- **Instructions** : Créer un script avec shebang, commentaires et commandes d'information système
- **Critères d'évaluation** : Shebang correct, commentaires clairs, 5 informations système affichées
- **Durée estimée** : 15 minutes
- **Fichier de travail** : `S1_S2_S1_lab1_premier_script.sh`

## 2. Variables et Paramètres

### Définition : Variables Bash

Une **variable Bash** est un nom symbolique associé à une valeur qui peut être utilisée et modifiée durant l'exécution du script. Elle permet de stocker et manipuler des données.

**Terminologie technique** :

- **Variable** : Conteneur nommé pour stocker des données (anglais : variable)
- **Paramètre positionnel** : Variable automatique contenant les arguments du script (anglais : positional parameter)
- **Variable d'environnement** : Variable accessible à tous les processus (anglais : environment variable)

### Contexte d'utilisation DevOps

Les variables permettent de rendre les scripts configurables et réutilisables. Dans DevOps, elles stockent les chemins de configuration, les paramètres de déploiement et les informations d'environnement.

### Exemples de Paramètres Positionnels

**Les paramètres positionnels** ($1, $2, $3, etc.) récupèrent les arguments passés au script :

```bash
#!/bin/bash
# Shebang : indique l'interpréteur à utiliser (Bash)

# Fichier: deploy.sh
# Description : Script de déploiement automatisé pour applications DevOps

# Usage: ./deploy.sh web-app production v2.1.0
# Exemple d'utilisation avec 3 paramètres : nom app, environnement, version

echo "Script de déploiement DevOps"

# $1 : Premier paramètre positionnel (nom de l'application)
echo "Application à déployer: $1"

# $2 : Deuxième paramètre positionnel (environnement cible)
echo "Environnement cible: $2"

# $3 : Troisième paramètre positionnel (version de l'application)
echo "Version: $3"

# $# : Variable spéciale contenant le nombre total d'arguments passés
echo "Nombre total d'arguments: $#"

# $@ : Variable spéciale contenant tous les arguments sous forme de liste
echo "Tous les arguments: $@"
```

**Exécution :**

```bash
$ ./deploy.sh web-app production v2.1.0
Script de déploiement DevOps
Application à déployer: web-app
Environnement cible: production
Version: v2.1.0
Nombre total d'arguments: 3
Tous les arguments: web-app production v2.1.0
```

### Exemples de Variables d'Environnement

**Les variables d'environnement** sont accessibles par tous les processus et scripts :

```bash
#!/bin/bash
# Script de démonstration des variables d'environnement

# Variables d'environnement courantes : disponibles dans tout le système
echo "Variables système importantes:"

# $USER : nom de l'utilisateur connecté (prédéfinie par le système)
echo "Utilisateur actuel: $USER"

# $HOME : chemin vers le répertoire personnel de l'utilisateur
echo "Répertoire personnel: $HOME"

# $PWD : répertoire de travail actuel (Print Working Directory)
echo "Répertoire de travail: $PWD"

# $PATH : liste des répertoires où chercher les commandes exécutables
echo "Chemin des commandes: $PATH"

# Définir des variables d'environnement personnalisées pour DevOps
# export : rend la variable accessible aux processus enfants

# Variable d'environnement pour l'environnement de déploiement
export DEPLOY_ENV="production"

# Variable d'environnement pour l'URL de l'API
export API_URL="https://api.monapp.com"

# Variable d'environnement pour le serveur de base de données
export DB_HOST="db-prod.internal"

echo "Variables DevOps personnalisées:"
echo "Environnement de déploiement: $DEPLOY_ENV"
echo "URL de l'API: $API_URL"
echo "Serveur de base de données: $DB_HOST"
```

**Utilisation avancée :**

```bash
# Vérification de l'existence d'une variable d'environnement critique

# Test -z : vérifie si la variable est vide ou non définie
if [ -z "$API_KEY" ]; then
    # Si la variable est vide, afficher un message d'erreur
    echo "ERREUR: Variable API_KEY non définie"
    # exit 1 : terminer le script avec un code d'erreur
    exit 1
else
    # Si la variable est définie, afficher seulement les premiers caractères par sécurité
    # ${API_KEY:0:8} : extraction des 8 premiers caractères de la variable
    echo "API_KEY configurée: ${API_KEY:0:8}..."
fi
```

### Conventions de Nommage des Variables

**Règles importantes de nommage** :

```bash
#!/bin/bash
# Démonstration des conventions de nommage des variables en Bash

# BONNES PRATIQUES - Variables locales (portée limitée au script)
# Convention : minuscules avec underscores pour séparer les mots

nom_serveur="web-01"           # Variable locale : nom du serveur
port_application=8080          # Variable locale : numéro de port
chemin_config="/etc/myapp"     # Variable locale : chemin de configuration

# BONNES PRATIQUES - Variables d'environnement (accessibles partout)
# Convention : MAJUSCULES avec underscores, export pour les rendre globales

export DEPLOY_ENV="production"                                # Environnement de déploiement
export API_KEY="abc123"                                       # Clé d'API sécurisée
export DB_CONNECTION_STRING="mysql://user:pass@host/db"       # Chaîne de connexion BDD

# BONNES PRATIQUES - Variables système (prédéfinies par le système)
# Convention : MAJUSCULES, déjà définies par le système

echo "Utilisateur: $USER"     # Variable système : utilisateur connecté
echo "Répertoire: $HOME"      # Variable système : répertoire personnel
echo "Shell: $SHELL"          # Variable système : shell par défaut

# À ÉVITER - Mauvaises conventions qui créent de la confusion

Nom_Serveur="web-01"          # MAUVAIS : mélange majuscule/minuscule
portApplication=8080          # MAUVAIS : CamelCase (convention d'autres langages)
```

**Pourquoi ces conventions ?**

- **Variables locales en minuscules** : Évite les conflits avec les variables système
- **Variables d'environnement en MAJUSCULES** : Convention Unix/Linux standard
- **Lisibilité** : Distinction immédiate entre local et environnement

**Exemple DevOps complet :**

```bash
#!/bin/bash
# Script de déploiement avec bonnes conventions de nommage

# Variables locales du script (minuscules avec underscores)
# Ces variables ne sont accessibles que dans ce script

app_name="mon-application"                    # Nom de l'application à déployer
version_number="1.2.3"                       # Version de l'application
timestamp=$(date +%Y%m%d_%H%M%S)             # Horodatage généré dynamiquement

# Variables d'environnement (MAJUSCULES avec export)
# Ces variables seront accessibles aux processus enfants

export ENVIRONMENT="production"                          # Environnement cible
export DOCKER_REGISTRY="registry.monentreprise.com"     # Registre Docker d'entreprise
export KUBERNETES_NAMESPACE="prod-apps"                  # Namespace Kubernetes

# Affichage des informations de déploiement
echo "Déploiement de $app_name v$version_number"
echo "Environnement: $ENVIRONMENT"
echo "Registry: $DOCKER_REGISTRY"
echo "Timestamp: $timestamp"
```

### Déclaration et Utilisation de Variables

```bash
#!/bin/bash
# Exemple de déclaration et utilisation de variables locales

# DÉCLARATION : Variables locales avec convention minuscules_underscores
# Pas d'espaces autour du signe = (important en Bash!)

nom_serveur="prod-web-01"     # Chaîne de caractères : nom du serveur
port_application=8080         # Nombre entier : port d'écoute
version_app="v1.2.0"          # Chaîne : version de l'application

# UTILISATION : Variables appelées avec le préfixe $ (dollar)
echo "Serveur: $nom_serveur"
echo "Port: $port_application"
echo "Version: $version_app"
```

**Diagramme conceptuel** :

```
Variables DevOps
├── Configuration (serveurs, ports, chemins)
├── Paramètres dynamiques ($1, $2, $3...)
├── Variables système ($HOME, $PATH...)
└── Variables calculées (dates, checksums...)
```

### Paramètres de Script

```bash
#!/bin/bash
# Script démontrant l'utilisation des paramètres positionnels

# Récupération des paramètres passés au script
# $1, $2, $3... correspondent aux arguments dans l'ordre

environnement=$1                    # Premier argument : environnement de déploiement
application=$2                      # Deuxième argument : nom de l'application

# ${3:-"latest"} : valeur par défaut si $3 est vide ou non fourni
version=${3:-"latest"}              # Troisième argument avec valeur par défaut

# Affichage des paramètres récupérés
echo "Déploiement de $application"
echo "Environnement: $environnement"
echo "Version: $version"
```

## 3. Structures de Contrôle

### Définition : Structures de Contrôle

Les **structures de contrôle** sont des constructions syntaxiques qui permettent de modifier l'ordre d'exécution des commandes en fonction de conditions logiques ou de répétitions programmées. Elles constituent la base de la logique algorithmique en scripts Bash.

**Terminologie technique** :

- **Condition** : Test logique déterminant le flux d'exécution (anglais : condition)
- **Boucle** : Structure répétitive d'exécution (anglais : loop)
- **Branchement conditionnel** : Choix entre plusieurs chemins d'exécution (anglais : conditional branching)
- **Test de comparaison** : Opération évaluant l'égalité ou l'inégalité (anglais : comparison test)
- **Opérateur logique** : Symbole combinant plusieurs conditions (anglais : logical operator)

### Contexte d'utilisation DevOps

Les structures de contrôle permettent d'automatiser la prise de décision dans les scripts DevOps : vérifications de prérequis avant déploiement, traitement en lot de serveurs multiples, tentatives de reconnexion avec retry automatique, et validation d'états système.

### Diagramme Conceptuel des Structures de Contrôle

```
STRUCTURES DE CONTRÔLE BASH
│
├── CONDITIONNELLES (if/else)
│   ├── Test simple → Action unique
│   ├── Test avec alternative → Action A ou Action B
│   └── Tests imbriqués → Logique complexe
│
├── RÉPÉTITIVES (boucles)
│   ├── for → Itération sur liste/tableau
│   ├── while → Répétition tant que condition vraie
│   └── until → Répétition jusqu'à condition vraie
│
└── COMBINÉES
    ├── if + for → Conditions dans boucles
    ├── for + if → Boucles avec conditions
    └── Logique multicritère → Tests complexes
```

### Structures Conditionnelles - Concepts Fondamentaux

#### Syntaxe de Base des Conditions

Les **conditions if/else** permettent d'exécuter du code selon qu'une condition soit vraie ou fausse :

```bash
#!/bin/bash
# Structure conditionnelle de base en Bash

# Structure if/else : permet de prendre des décisions dans le script
if [[ condition ]]; then
    # Bloc exécuté si la condition est VRAIE (true)
    # Remplacez "condition" par un test réel (voir exemples ci-dessous)
else
    # Bloc exécuté si la condition est FAUSSE (false)
    # Le bloc else est optionnel
fi
# fi : mot-clé obligatoire pour fermer la structure if
```

#### Opérateurs de Test - Fondamentaux Obligatoires

Avant d'utiliser les conditions, il faut maîtriser les **opérateurs de test** qui permettent de vérifier différents états :

##### Tests de Fichiers et Répertoires

| Opérateur | Description                                     | Exemple d'usage                 |
| --------- | ----------------------------------------------- | ------------------------------- |
| `-f`      | Fichier existe et est un fichier régulier       | `[[ -f "/etc/passwd" ]]`        |
| `-d`      | Répertoire existe                               | `[[ -d "/var/log" ]]`           |
| `-e`      | Fichier/répertoire existe (peu importe le type) | `[[ -e "/tmp/script.sh" ]]`     |
| `-r`      | Fichier lisible                                 | `[[ -r "/etc/hosts" ]]`         |
| `-w`      | Fichier modifiable                              | `[[ -w "/tmp/data.txt" ]]`      |
| `-x`      | Fichier exécutable                              | `[[ -x "/usr/bin/docker" ]]`    |
| `-s`      | Fichier existe et n'est pas vide                | `[[ -s "/var/log/nginx.log" ]]` |

##### Tests de Comparaison de Chaînes

| Opérateur   | Description           | Exemple d'usage                |
| ----------- | --------------------- | ------------------------------ |
| `=` ou `==` | Égalité de chaînes    | `[[ "$status" == "active" ]]`  |
| `!=`        | Différence de chaînes | `[[ "$env" != "production" ]]` |
| `-z`        | Chaîne vide           | `[[ -z "$variable" ]]`         |
| `-n`        | Chaîne non vide       | `[[ -n "$user" ]]`             |

##### Tests de Comparaison Numérique

| Opérateur | Description       | Exemple d'usage        |
| --------- | ----------------- | ---------------------- |
| `-eq`     | Égal à            | `[[ $port -eq 80 ]]`   |
| `-ne`     | Différent de      | `[[ $port -ne 443 ]]`  |
| `-lt`     | Inférieur à       | `[[ $load -lt 5 ]]`    |
| `-le`     | Inférieur ou égal | `[[ $memory -le 80 ]]` |
| `-gt`     | Supérieur à       | `[[ $cpu -gt 90 ]]`    |
| `-ge`     | Supérieur ou égal | `[[ $disk -ge 50 ]]`   |

#### Exemples Pratiques des Opérateurs

```bash
#!/bin/bash
# Script de démonstration des opérateurs de test en Bash

# === SECTION 1: TESTS DE FICHIERS ET RÉPERTOIRES ===
echo "=== Tests de fichiers ==="

# Test -f : vérifie qu'un fichier régulier existe (pas un répertoire ou lien)
if [[ -f "/etc/nginx/nginx.conf" ]]; then
    echo "SUCCÈS: Fichier de config Nginx trouvé"
fi

# Test -d : vérifie qu'un répertoire existe (pas un fichier)
if [[ -d "/var/log" ]]; then
    echo "SUCCÈS: Répertoire de logs existe"
fi

# Test -x : vérifie qu'un fichier existe ET possède les permissions d'exécution
if [[ -x "/usr/bin/docker" ]]; then
    echo "SUCCÈS: Docker est installé et exécutable"
fi

# === SECTION 2: TESTS DE CHAÎNES DE CARACTÈRES ===
echo "=== Tests de chaînes ==="

# Variables de test pour les exemples
status="active"          # Variable simulant le retour de systemctl
env="production"         # Variable d'environnement

# Test == : comparaison exacte de chaînes (sensible à la casse)
if [[ "$status" == "active" ]]; then
    echo "SUCCÈS: Service actif"
fi

# Test -n : vérifie que la chaîne n'est pas vide (not null)
if [[ -n "$env" ]]; then
    echo "SUCCÈS: Environnement défini : $env"
fi

# === SECTION 3: TESTS NUMÉRIQUES ===
echo "=== Tests numériques ==="

# Variables numériques pour les exemples
port=80                  # Port à vérifier
cpu_usage=75            # Pourcentage d'utilisation CPU

# Test -eq : égalité numérique (equal - différent de == pour les nombres)
if [[ $port -eq 80 ]]; then
    echo "SUCCÈS: Port HTTP standard"
fi

# Test -gt : supérieur à (greater than)
if [[ $cpu_usage -gt 70 ]]; then
    echo "ALERTE: CPU usage élevé : ${cpu_usage}%"
fi
```

#### Maintenant : Exemples Pratiques DevOps avec Opérateurs

```bash
#!/bin/bash
# Exemple pratique DevOps : vérification de configuration Nginx

# Variable contenant le chemin vers le fichier de configuration Nginx
config_file="/etc/nginx/nginx.conf"

# Test de l'existence du fichier de configuration
if [[ -f "$config_file" ]]; then
    # Si le fichier existe, afficher des informations positives
    echo "Configuration Nginx trouvée : $config_file"

    # Commande du : affiche la taille du fichier de manière lisible
    # cut -f1 : extrait le premier champ (la taille)
    echo "Taille du fichier : $(du -h $config_file | cut -f1)"
else
    # Si le fichier n'existe pas, afficher un message d'erreur
    echo "ERREUR : Configuration Nginx manquante"
    echo "Veuillez installer Nginx avant de continuer"

    # exit 1 : terminer le script avec un code d'erreur (non-zéro)
    exit 1
fi
```

#### Syntaxes de Tests - Alternatives et Comparaisons

**Question importante** : Les doubles crochets `[[ ]]` ne sont **PAS obligatoires**. Bash offre plusieurs syntaxes pour les tests :

##### 1. Doubles crochets `[[ ]]` (Recommandé - Bash moderne)

```bash
# Syntaxe moderne et robuste
if [[ -f "$config_file" ]]; then
    echo "Fichier existe"
fi

# Avantages des doubles crochets [[]]
# - Gestion automatique des espaces dans les noms de fichiers
# - Opérateurs logiques && et || natifs
# - Comparaisons de patterns avec ==
# - Plus sûr avec les variables vides
```

##### 2. Crochets simples `[ ]` (Compatible POSIX)

```bash
# Syntaxe classique compatible tous les shells
if [ -f "$config_file" ]; then
    echo "Fichier existe"
fi

# Syntaxe équivalente avec test
if test -f "$config_file"; then
    echo "Fichier existe"
fi
```

##### 3. Commandes directes (Sans crochets)

```bash
# Test direct avec commandes
if systemctl is-active --quiet nginx; then
    echo "Nginx actif"
fi

# Test avec code de retour
if ping -c 1 google.com >/dev/null 2>&1; then
    echo "Connexion internet OK"
fi
```

**IMPORTANT** : Dans ces exemples, vous **NE POUVEZ PAS** utiliser `[]` ou `[[]]` !

**Pourquoi ?** Ces commandes (`systemctl`, `ping`) retournent directement un **code de retour** :

- Code 0 = succès (condition vraie)
- Code ≠ 0 = échec (condition fausse)

**Exemples INCORRECTS** (ne fonctionnent pas) :

```bash
# ERREUR - syntaxe invalide : les commandes ne peuvent pas être dans les crochets
if [[ systemctl is-active --quiet nginx ]]; then
    echo "Ceci ne marchera jamais"
fi

# ERREUR - syntaxe invalide : ping retourne un code, pas une valeur testable
if [ ping -c 1 google.com ]; then
    echo "Ceci non plus"
fi
```

**Alternative si vous voulez absolument utiliser `[[]]`** :

```bash
# ALTERNATIVE COMPLEXE - Capturer d'abord le résultat dans une variable
nginx_status=$(systemctl is-active nginx 2>/dev/null)
if [[ "$nginx_status" == "active" ]]; then
    echo "Nginx actif"
fi

# ALTERNATIVE LOURDE - Tester le code de retour explicitement
if systemctl is-active --quiet nginx; then
    status="success"
else
    status="failed"
fi

if [[ "$status" == "success" ]]; then
    echo "Nginx actif"
fi
```

**Recommandation** : Pour les commandes système, utilisez la syntaxe directe (plus simple et naturelle).

#### Tableau Comparatif des Syntaxes

| Syntaxe   | Compatibilité | Sécurité | Lisibilité | Usage DevOps      |
| --------- | ------------- | -------- | ---------- | ----------------- |
| `[[ ]]`   | Bash/Zsh      | Élevée   | Excellente | **Recommandé**    |
| `[ ]`     | POSIX/Tous    | Moyenne  | Bonne      | Scripts portables |
| `test`    | POSIX/Tous    | Moyenne  | Correcte   | Scripts anciens   |
| Commandes | Universel     | Variable | Excellente | Tests spécifiques |

#### Exemples Comparatifs Pratiques

```bash
#!/bin/bash

fichier="/etc/nginx/nginx.conf"

# OPTION 1 : Doubles crochets (RECOMMANDÉ pour Bash)
if [[ -f "$fichier" ]]; then
    echo "Méthode 1 : Fichier trouvé avec [[]]"
fi

# OPTION 2 : Crochets simples (COMPATIBLE partout)
if [ -f "$fichier" ]; then
    echo "Méthode 2 : Fichier trouvé avec []"
fi

# OPTION 3 : Commande test (ÉQUIVALENT à [])
if test -f "$fichier"; then
    echo "Méthode 3 : Fichier trouvé avec test"
fi

# OPTION 4 : Test avec commande système
if ls "$fichier" >/dev/null 2>&1; then
    echo "Méthode 4 : Fichier trouvé avec ls"
fi
```

#### Recommandations DevOps

- **Scripts Bash purs** : Utilisez `[[ ]]` (plus robuste)
- **Scripts portables** : Utilisez `[ ]` (compatible sh/dash)
- **Tests de services** : Utilisez les commandes directement
- **Débutants** : Commencez avec `[[ ]]` (plus sûr)

**Résumé** : `[[ ]]` n'est pas obligatoire, mais **recommandé en Bash** pour sa robustesse et sa lisibilité.

#### Exemples Pratiques DevOps - Tests de Services

```bash
#!/bin/bash
# Script de vérification et gestion de services système

# Variable contenant le nom du service à vérifier
service_name="docker"

# systemctl is-active : commande qui vérifie si un service est actif
# --quiet : supprime la sortie, seul le code de retour compte
# if sans crochets : teste directement le code de retour de la commande
if systemctl is-active --quiet "$service_name"; then
    # Si le service est actif (code de retour 0)
    echo "Service $service_name : ACTIF"

    # Affichage de la version Docker pour confirmation
    # $(docker --version) : substitution de commande pour capturer la sortie
    echo "Version : $(docker --version)"
else
    # Si le service est inactif (code de retour non-zéro)
    echo "Service $service_name : INACTIF"
    echo "Tentative de démarrage..."

    # sudo : exécution avec privilèges administrateur
    # systemctl start : commande pour démarrer un service
    sudo systemctl start "$service_name"
fi
```

#### Conditions Imbriquées et Logique Complexe

```bash
#!/bin/bash
# Script de vérification complète d'environnement Docker pour déploiement

# ÉTAPE 1 : Vérification de l'installation de Docker
# Test -f : vérifie que le binaire Docker existe sur le système
if [[ -f "/usr/bin/docker" ]]; then
    echo "ÉTAPE 1: Docker installé"

    # ÉTAPE 2 : Vérification du service Docker (imbriquée dans ÉTAPE 1)
    # systemctl is-active : teste si le service systemd est en cours d'exécution
    if systemctl is-active --quiet docker; then
        echo "ÉTAPE 2: Docker actif"

        # ÉTAPE 3 : Vérification de la communication avec le daemon Docker (imbriquée dans ÉTAPE 2)
        # docker info : commande qui interroge le daemon Docker
        # >/dev/null 2>&1 : redirige toute sortie vers /dev/null (silencieux)
        if docker info >/dev/null 2>&1; then
            echo "ÉTAPE 3: Docker fonctionnel"
            echo "RÉSULTAT: Environnement prêt pour déploiement"
        else
            echo "ÉCHEC ÉTAPE 3: Docker dysfonctionnel (daemon inaccessible)"
            # exit 1 : code d'erreur pour signaler un problème au système appelant
            exit 1
        fi
    else
        echo "ÉCHEC ÉTAPE 2: Docker inactif (service arrêté)"
        exit 1
    fi
else
    echo "ÉCHEC ÉTAPE 1: Docker non installé (binaire manquant)"
    exit 1
fi
```

**Diagramme de flux conditionnel** :

```
START
  │
  ▼
[Docker installé ?] ──NON──► ERREUR & EXIT
  │ OUI
  ▼
[Docker actif ?] ──NON──► ERREUR & EXIT
  │ OUI
  ▼
[Docker fonctionnel ?] ──NON──► ERREUR & EXIT
  │ OUI
  ▼
SUCCÈS : Environnement prêt
  │
  ▼
END
```

### Application pratique

📝 **LAB 2** - Structures conditionnelles : `S1_S2_S1_lab2_structures_conditionnelles.sh`

**Énoncé du LAB 2** :
Développez un script de diagnostic d'environnement DevOps qui utilise les structures conditionnelles pour valider et analyser la configuration système avant déploiement.

- **Objectif** : Maîtriser les structures conditionnelles (if/else/elif) et les opérateurs de test dans un contexte DevOps professionnel
- **Contexte** : Script de pré-validation d'environnement pour pipeline CI/CD
- **Instructions** :
  - Vérifier l'existence et les permissions de fichiers critiques DevOps
  - Tester la disponibilité des outils et services essentiels
  - Implémenter des conditions imbriquées pour validation complexe
  - Utiliser les opérateurs de fichiers (-f, -d, -x), chaînes (==, !=, -z) et numériques (-eq, -gt)
- **Critères d'évaluation** : 4 types de tests différents, 2 conditions imbriquées minimum, gestion d'erreurs appropriée, messages informatifs clairs
- **Durée estimée** : 25 minutes
- **Fichier de travail** : `S1_S2_S1_lab2_structures_conditionnelles.sh`

## 4. Structures Répétitives - Boucles

### Définition : Structure Répétitive (Boucle)

Une **structure répétitive** ou **boucle** (anglais : loop) est une structure de contrôle qui permet d'exécuter un bloc de code plusieurs fois. En Bash, elle automatise les tâches répétitives d'administration système.

**Terminologie technique** :

- **Boucle** : Structure de répétition (anglais : loop)
- **Itération** : Une exécution du bloc de code (anglais : iteration)
- **Compteur** : Variable qui suit le nombre d'itérations (anglais : counter)
- **Condition d'arrêt** : Critère de fin de boucle (anglais : exit condition)

### Types de Boucles en Bash

#### 4.1 Boucle `for` - Itération sur Collections

**Définition** : La boucle `for` parcourt une liste d'éléments prédéfinie et exécute le code pour chaque élément.

**Syntaxe générale** :

```bash
for variable in liste_elements; do
    # Actions à répéter
done
```

**Diagramme conceptuel** :

```
COLLECTION: [élément1, élément2, élément3]
     │
     ▼
┌─────────────────┐
│ FOR variable    │ ──► variable = élément1 ──► Exécuter bloc
│ IN collection   │ ──► variable = élément2 ──► Exécuter bloc
│ DO              │ ──► variable = élément3 ──► Exécuter bloc
│   bloc_code     │ ──► FIN
│ DONE            │
└─────────────────┘
```

#### Exemple Pratique : Vérification de Connectivité Serveurs

```bash
#!/bin/bash
# Script d'audit de connectivité infrastructure avec boucle for

# Vérification de connectivité sur plusieurs serveurs - automatisation avec boucle for
echo "=== AUDIT DE CONNECTIVITÉ INFRASTRUCTURE ==="

# DÉCLARATION DE TABLEAU : liste des serveurs à tester
# Syntaxe : nom_tableau=(élément1 élément2 élément3 ...)
serveurs=("web-prod-01" "web-prod-02" "api-prod-01" "db-prod-01")

# BOUCLE FOR : itère sur chaque élément du tableau
# "${serveurs[@]}" : expansion de tous les éléments du tableau
# for ... in ... do ... done : structure de boucle for
for serveur in "${serveurs[@]}"; do
    # echo -n : affiche sans saut de ligne final (pour le formatage)
    echo -n "Test connectivité $serveur : "

    # TEST DE CONNECTIVITÉ :
    # ping -c 1 : envoie 1 seul paquet ICMP
    # -W 2 : timeout de 2 secondes maximum
    # >/dev/null 2>&1 : redirige sortie standard et erreurs vers /dev/null (silencieux)
    if ping -c 1 -W 2 "$serveur" >/dev/null 2>&1; then
        echo "ACCESSIBLE"     # Code de retour 0 : serveur répond
    else
        echo "INACCESSIBLE"   # Code de retour ≠ 0 : serveur ne répond pas
    fi
done  # Fin de la boucle for

echo "Audit terminé"
```

#### 4.2 Boucle `while` - Répétition Conditionnelle

**Définition** : La boucle `while` répète un bloc de code tant qu'une condition reste vraie (true).

**Syntaxe générale** :

```bash
while [[ condition ]]; do
    # Actions à répéter
    # Modification de la condition (important !)
done
```

**Diagramme de flux** :

```
START
  │
  ▼
┌─────────────────┐
│ CONDITION       │ ──NON──► FIN
│ est-elle vraie? │
└─────────────────┘
  │ OUI
  ▼
┌─────────────────┐
│ EXÉCUTER        │
│ bloc de code    │
└─────────────────┘
  │
  │ (retour au test)
  └──────────────────┘
```

#### Exemple Pratique : Monitoring avec Retry

````bash
#!/bin/bash

# Attente de disponibilité d'un service - boucle while avec retry
echo "=== MONITORING DISPONIBILITÉ SERVICE ==="

service_url="http://api.monapp.com/health"  # Endpoint de health check
max_tentatives=10                            # Limite pour éviter boucle infinie
tentative=1                                  # Compteur initialisé à 1

echo "Surveillance du service : $service_url"

```bash
#!/bin/bash
# Script de monitoring avec retry automatique - boucle while

# Attente de disponibilité d'un service - boucle while avec retry
echo "=== MONITORING DISPONIBILITÉ SERVICE ==="

# VARIABLES DE CONFIGURATION :
service_url="http://api.monapp.com/health"  # Endpoint de health check à surveiller
max_tentatives=10                            # Limite pour éviter boucle infinie
tentative=1                                  # Compteur initialisé à 1

echo "Surveillance du service : $service_url"

# BOUCLE WHILE : continue tant que la condition est vraie
# -le : opérateur "less than or equal" (inférieur ou égal)
# [[ ]] : test conditionnel avancé Bash
while [[ $tentative -le $max_tentatives ]]; do
    echo "Tentative $tentative/$max_tentatives..."

    # TEST DE DISPONIBILITÉ HTTP :
    # curl : client HTTP en ligne de commande
    # -s : mode silencieux (pas de sortie de progression)
    # -f : fail on HTTP errors (échec si code d'erreur HTTP)
    # >/dev/null : redirige sortie vers /dev/null (silencieux)
    if curl -s -f "$service_url" >/dev/null; then
        echo "SUCCÈS: Service disponible !"
        break  # break : sortie immédiate de la boucle (termine la boucle)
    else
        echo "Service indisponible, nouvelle tentative dans 5s..."
        sleep 5              # Pause de 5 secondes entre tentatives
        ((tentative++))      # Incrémentation arithmétique : tentative = tentative + 1
    fi
done  # Fin de la boucle while

# VÉRIFICATION POST-BOUCLE : analyser le résultat final
# -gt : opérateur "greater than" (supérieur à)
if [[ $tentative -gt $max_tentatives ]]; then
    echo "ÉCHEC: Service indisponible après $max_tentatives tentatives"
    echo "Action requise : Vérifier l'état du service et logs"
    exit 1  # Code d'erreur 1 pour scripts appelants et systèmes de monitoring
else
    echo "Monitoring terminé avec succès"
fi
````

#### 4.3 Boucle `for` avec Plages Numériques

**Syntaxe des plages** : `{début..fin}` ou `{début..fin..pas}`

```bash
#!/bin/bash
# Script de rotation automatique des sauvegardes - boucle for avec plages

# Sauvegarde rotation - boucle for avec plage numérique
echo "=== ROTATION DES SAUVEGARDES ==="

# VARIABLES DE CONFIGURATION :
backup_dir="/backup"              # Répertoire de sauvegarde principal
retention_days=7                  # Nombre de jours de rétention des sauvegardes

# BOUCLE FOR AVEC PLAGE NUMÉRIQUE :
# {1..7} : génère automatiquement la séquence 1, 2, 3, 4, 5, 6, 7
# Syntaxe générale : {début..fin} ou {début..fin..pas}
for day in {1..7}; do
    # CONSTRUCTION DU NOM DE FICHIER :
    # Concaténation de chaînes avec variables
    backup_file="$backup_dir/daily_backup_day_$day.tar.gz"

    echo "Vérification sauvegarde jour $day : $backup_file"

    # TEST D'EXISTENCE DE FICHIER :
    # -f : teste si c'est un fichier régulier (pas un répertoire ou lien)
    if [[ -f "$backup_file" ]]; then
        # CALCUL DE L'ÂGE DU FICHIER :
        # $(date +%s) : timestamp Unix actuel (secondes depuis 1970)
        # $(stat -c %Y "$fichier") : timestamp de dernière modification
        # / 86400 : conversion secondes vers jours (86400 = 24h * 60min * 60s)
        # $(( )) : arithmétique entière Bash
        file_age=$(( ($(date +%s) - $(stat -c %Y "$backup_file")) / 86400 ))

        echo "  Âge du fichier : $file_age jours"

        # LOGIQUE DE RÉTENTION :
        # -gt : opérateur "greater than" (supérieur à)
        if [[ $file_age -gt $retention_days ]]; then
            echo "  SUPPRESSION : Fichier expiré (>$retention_days jours)"
            rm "$backup_file"  # Suppression du fichier obsolète
        else
            echo "  CONSERVATION : Fichier valide"
        fi
    else
        echo "  ABSENT : Aucune sauvegarde pour ce jour"
    fi
done  # Fin de la boucle for

echo "Rotation terminée"
```

#### Comparaison des Types de Boucles

| Type     | Usage Principal               | Condition d'Arrêt        | Exemple DevOps                   |
| -------- | ----------------------------- | ------------------------ | -------------------------------- |
| `for`    | Parcours d'une liste connue   | Fin de la liste          | Déploiement sur N serveurs       |
| `while`  | Répétition conditionnelle     | Condition devient fausse | Attente de disponibilité service |
| `{1..N}` | Itération sur plage numérique | Fin de la plage          | Rotation de sauvegardes          |

### Application pratique

📝 **LAB 3** - Structures répétitives : `S1_S2_S1_lab3_structures_repetitives.sh`

**Énoncé du LAB 3** :
Développez un script d'administration utilisant différents types de boucles pour automatiser la surveillance et la maintenance d'infrastructure.

- **Objectif** : Maîtriser les boucles for et while dans des contextes DevOps réalistes
- **Contexte** : Script de monitoring automatisé pour infrastructure de production
- **Instructions** : Créer une boucle for pour tester des services, une boucle while pour retry, une boucle numérique pour rotation
- **Critères d'évaluation** : 3 types de boucles fonctionnelles, logique de retry, gestion d'erreurs
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S2_S1_lab3_structures_repetitives.sh`

#### 4.4 Boucles Imbriquées - Structures Combinées

**Définition** : Les **boucles imbriquées** sont des boucles placées à l'intérieur d'autres boucles, permettant de traiter des structures de données bidimensionnelles.

**Cas d'usage DevOps** : Audit multi-environnement, déploiement multi-service, validation croisée.

```bash
#!/bin/bash
# Script d'audit multi-environnement et multi-service avec boucles imbriquées

# Audit multi-environnement et multi-service - boucles imbriquées
echo "=== AUDIT INFRASTRUCTURE COMPLÈTE ==="

# DÉCLARATION DE TABLEAUX :
# Tableaux Bash : stockent plusieurs valeurs dans une seule variable
environnements=("staging" "production")      # Environnements cibles à auditer
services=("nginx" "docker" "mysql")          # Services critiques à vérifier

# BOUCLE EXTERNE : parcourt chaque environnement
# "${environnements[@]}" : expansion de tous les éléments du tableau
for env in "${environnements[@]}"; do
    echo "Environnement : $env"
    echo "────────────────────────────"

    # BOUCLE INTERNE : pour chaque environnement, teste tous les services
    # Concept : boucles imbriquées = boucle à l'intérieur d'une autre boucle
    # Pour chaque environnement, on teste TOUS les services
    for service in "${services[@]}"; do
        # echo -n : affiche sans retour à la ligne (pour formatage en ligne)
        echo -n "  Service $service : "

        # TEST DE STATUT DE SERVICE :
        # systemctl is-active : vérifie si un service systemd est actif
        # --quiet : supprime la sortie, ne retourne que le code d'état
        # Code retour 0 = service actif, ≠ 0 = service inactif/problème
        if systemctl is-active --quiet "$service"; then
            echo "ACTIF"     # Service fonctionnel
        else
            echo "INACTIF"   # Service arrêté ou défaillant
        fi
    done  # Fin de la boucle interne (services)

    echo ""  # Ligne vide pour séparation visuelle entre environnements
done  # Fin de la boucle externe (environnements)

echo "Audit terminé"
```

**Diagramme de flux des boucles imbriquées** :

```
DÉBUT
  │
  ▼
Pour chaque ENVIRONNEMENT [staging, production]
  │
  ├─► Pour chaque SERVICE [nginx, docker, mysql]
  │     │
  │     ├─► [Service actif ?] ──OUI──► Afficher "ACTIF"
  │     │         │
  │     │         └─NON──► Afficher "INACTIF"
  │     │
  │     └─► Service suivant (boucle interne continue)
  │
  └─► Environnement suivant (boucle externe continue)
  │
  ▼
FIN
```

#### 4.5 Structures de Contrôle Combinées - Validation Complète

**Principe** : Combinaison de conditions (`if`) et boucles (`for/while`) pour créer des scripts de validation robustes.

```bash
#!/bin/bash
# Script de validation pré-déploiement avec structures de contrôle combinées

# Script de validation pré-déploiement - structures combinées
echo "=== VALIDATION PRÉ-DÉPLOIEMENT INFRASTRUCTURE ==="

# TABLEAU ASSOCIATIF : structure clé-valeur avancée
# declare -A : déclare un tableau associatif (hashmap/dictionnaire)
# Syntaxe : nom_tableau=([clé1]="valeur1" [clé2]="valeur2")
declare -A services_requis=(
    ["docker"]="Containerisation"
    ["nginx"]="Reverse proxy"
    ["mysql"]="Base de données"
)

# VARIABLE DE CONTRÔLE GLOBALE :
# Track l'état global de validation (booléen logique)
validation_ok=true

# BOUCLE FOR AVEC TABLEAU ASSOCIATIF :
# "${!services_requis[@]}" : expansion des CLÉS du tableau associatif
# Différent de "${services_requis[@]}" qui donnerait les valeurs
for service in "${!services_requis[@]}"; do
    # ACCÈS AUX VALEURS DU TABLEAU ASSOCIATIF :
    # ${tableau[clé]} : récupère la valeur associée à la clé
    description="${services_requis[$service]}"
    echo -n "Vérification $service ($description) : "

    # STRUCTURE CONDITIONNELLE IMBRIQUÉE DANS LA BOUCLE :
    # Combinaison boucle + condition pour validation individuelle
    if systemctl is-active --quiet "$service"; then
        echo "VALIDE"                          # Service opérationnel
    else
        echo "ÉCHEC"                           # Service défaillant
        validation_ok=false                    # Mise à jour état global
    fi
done  # Fin de la boucle de validation

# ANALYSE POST-BOUCLE : décision finale basée sur l'état global
echo ""
echo "=== RÉSULTAT DE LA VALIDATION ==="

# CONDITION FINALE : test de la variable booléenne globale
# == : comparaison de chaînes (pas d'assignation)
if [[ "$validation_ok" == true ]]; then
    echo "SUCCÈS: VALIDATION RÉUSSIE"
    echo "L'infrastructure est prête pour le déploiement"
    exit 0  # Code de retour 0 = succès (pour scripts appelants et CI/CD)
else
    echo "ÉCHEC: VALIDATION ÉCHOUÉE"
    echo "Corrigez les services défaillants avant de continuer"
    echo "Actions requises :"
    echo "  1. Vérifier les logs des services en échec"
    echo "  2. Redémarrer les services si nécessaire"
    echo "  3. Relancer la validation"
    exit 1  # Code de retour 1 = erreur (pour monitoring/CI/CD)
fi
```

**Avantages des structures combinées** :

| Combinaison        | Avantage Principal                    | Usage DevOps                |
| ------------------ | ------------------------------------- | --------------------------- |
| `if` dans `for`    | Validation conditionnelle par élément | Audit de services multiples |
| `while` avec `if`  | Retry intelligent avec logique        | Attente conditionnelle      |
| `for` imbriqués    | Traitement bidimensionnel             | Multi-environnement/service |
| Variables de suivi | État global après itérations          | Validation d'infrastructure |

## 5. Scripts d'Administration Système

### Définition : Administration Système par Script

L'**administration système par script** consiste à automatiser les tâches d'administration (installation, configuration, monitoring) via des scripts Bash plutôt que par des commandes manuelles.

**Terminologie technique** :

- **Automation** : Exécution automatique de tâches administratives (anglais : automation)
- **Script d'administration** : Programme automatisant des tâches système (anglais : system administration script)
- **Batch processing** : Traitement par lots d'opérations (anglais : batch processing)

### Contexte d'utilisation DevOps

Les scripts d'administration automatisent les tâches répétitives comme la vérification de services, la création de sauvegardes et l'installation de packages, libérant du temps pour les tâches à plus forte valeur ajoutée.

### Scripts d'Information Système

```bash
#!/bin/bash
# Script de rapport système automatisé pour administration DevOps

echo "=== RAPPORT SYSTÈME DEVOPS ==="

# HORODATAGE : génération d'un timestamp de rapport
# $(date) : substitution de commande, exécute date et récupère la sortie
echo "Date de génération : $(date)"

# INFORMATIONS SYSTÈME DE BASE :
# uname -a : affiche toutes les informations système (noyau, version, architecture)
echo "Système d'exploitation : $(uname -a)"

# MONITORING DE L'ESPACE DISQUE :
echo "Espace disque disponible :"
# df -h : affiche l'utilisation des systèmes de fichiers
# -h : format human-readable (Ko, Mo, Go au lieu d'octets)
# / : système de fichiers racine (le plus critique)
df -h /

# CHARGE SYSTÈME ET UPTIME :
echo "Charge système et temps de fonctionnement :"
# uptime : affiche depuis quand le système fonctionne + charge moyenne
# Charge = nombre de processus en attente d'exécution
uptime

# ÉTAT DES SERVICES SYSTÈME :
echo "Nombre de services actifs :"
# systemctl list-units : liste les unités systemd
# --type=service : filtre seulement les services (pas les mount, timer, etc.)
# --state=active : filtre seulement les services actifs
# wc -l : compte le nombre de lignes (donc le nombre de services)
systemctl list-units --type=service --state=active | wc -l
```

**Schéma conceptuel** :

```
Script d'administration
├── Collecte d'informations système
├── Vérification de services
├── Rapport de statut
└── Actions correctives basiques
```

### Sauvegarde Automatisée Simple

```bash
#!/bin/bash
# Script de sauvegarde automatisée - administration système

# CONFIGURATION DE LA SAUVEGARDE :
# $(date +%Y%m%d) : formatage de date (Année+Mois+Jour, ex: 20241115)
backup_dir="/backup/$(date +%Y%m%d)"
source_dir="/etc"  # Répertoire des configurations système critiques

# CRÉATION DU RÉPERTOIRE DE SAUVEGARDE :
# mkdir -p : crée le répertoire et tous ses parents si nécessaire
# -p : mode parents (pas d'erreur si le répertoire existe déjà)
mkdir -p "$backup_dir"

# CRÉATION DE L'ARCHIVE DE SAUVEGARDE :
# tar : outil d'archivage Unix/Linux
# -c : create (créer une archive)
# -z : gzip (compression automatique)
# -f : file (spécifier le nom du fichier de sortie)
# $(date +%H%M) : formatage heure+minute pour timestamp unique
tar -czf "$backup_dir/config-$(date +%H%M).tar.gz" "$source_dir"

echo "Sauvegarde terminée: $backup_dir"
```

### Application pratique

📝 **LAB 4 - Challenge** - Administration système complète : `S1_S2_S1_lab4_administration_complete.sh`

**Énoncé du LAB 4 Challenge (Hors séance - Bonus)** :

Ce challenge optionnel permet d'approfondir les concepts vus en séance et d'explorer des applications avancées en autonomie.

Créez un script d'administration système avancé qui combine tous les concepts pour créer un outil de maintenance et de diagnostic complet.

- **Objectif** : Développer un script professionnel d'administration utilisant tous les concepts Bash fondamentaux
- **Statut** : Activité bonus, hors des 2 heures de séance
- **Contexte** : Script de maintenance préventive pour serveurs DevOps
- **Instructions** : Collecter infos système complètes, vérifier espace disque avec alertes, tester services critiques, créer sauvegarde automatique, générer rapport formaté
- **Critères d'évaluation** : 5 informations système, vérification espace disque avec seuils, test de 3+ services, sauvegarde fonctionnelle, rapport professionnel, gestion paramètres
- **Durée estimée** : 30-45 minutes
- **Niveau** : Avancé, concepts d'excellence
- **Fichier de travail** : `S1_S2_S1_lab4_administration_complete.sh`

## 6. Récapitulatif et prochaines étapes

Cette séance a permis de découvrir les fondamentaux du scripting Bash et de créer ses premiers scripts d'administration système DevOps.

**Concepts clés acquis** :

- Structure de base des scripts Bash avec shebang et commentaires
- Manipulation des variables et paramètres de script
- Utilisation des structures de contrôle (if/else, boucles for)
- Création de scripts d'administration système basiques
- Automation de tâches répétitives d'administration

**Prochaine séance** : Automation et Monitoring - Scripts avancés pour déploiement automatisé et monitoring d'infrastructure.

## 7. Ressources complémentaires

- **Documentation Bash** : Advanced Bash-Scripting Guide (The Linux Documentation Project)
- **Standards DevOps** : The DevOps Handbook (Kim, Humble, Debois, Willis)
- **Logging Standards** : RFC 3164 - The BSD Syslog Protocol
- **Service Management** : systemd.service manual pages
- **Infrastructure as Code** : Terraform Documentation, Ansible Best Practices

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 1 : Fondamentaux du Scripting Bash Modulaire pour DevOps_
