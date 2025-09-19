# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 2 - Séance 2 : Bash Scripting Intermédiaire

## Objectifs pédagogiques

- Développer des scripts Bash avec fonctions et modularité
- Implémenter la gestion d'erreurs et les bonnes pratiques
- Créer des outils d'administration système réutilisables
- Automatiser des tâches de maintenance et de surveillance basiques

## Objectifs techniques

Fonctions Bash, gestion erreurs, paramètres, validation entrées, scripts modulaires, automation maintenance, surveillance basique

## Table des matières

1. [Fonctions Bash et Modularité](#1-fonctions-bash-et-modularité)
2. [Gestion d'Erreurs et Validation](#2-gestion-derreurs-et-validation)
3. [Scripts d'Administration Réutilisables](#3-scripts-dadministration-réutilisables)
4. [Automation de Maintenance](#4-automation-de-maintenance)

## 1. Fonctions Bash et Modularité

### Définition : Fonction Bash

Une **fonction Bash** est un bloc de code réutilisable qui encapsule une série de commandes sous un nom unique. Elle peut recevoir des paramètres et retourner des valeurs.

**Terminologie technique** :

- **Fonction** : Bloc de code réutilisable avec un nom (anglais : function)
- **Paramètre local** : Variable accessible uniquement dans la fonction (anglais : local parameter)
- **Valeur de retour** : Code de sortie d'une fonction (anglais : return value)

### Contexte d'utilisation DevOps

Les fonctions permettent de créer des scripts modulaires et maintenables, évitent la duplication de code et facilitent les tests unitaires des scripts d'administration.

### Création et Utilisation de Fonctions

```bash
#!/bin/bash

# Fonction simple d'information
afficher_info_systeme() {
 echo "=== Informations Système ==="
 echo "Date: $(date)"
 echo "Utilisateur: $(whoami)"
 echo "Système: $(uname -s)"
}

# Fonction avec paramètres
verifier_service() {
 local service_name="$1"

 if systemctl is-active "$service_name" >/dev/null 2>&1; then
 echo " Service $service_name est actif"
 return 0
 else
 echo " Service $service_name est inactif"
 return 1
 fi
}
```

### Exemple d'orchestration avec fonction main

```bash
#!/bin/bash

# Fonction d'information système
obtenir_info_systeme() {
    echo "=== Informations Système ==="
    echo "Hostname: $(hostname)"
    echo "Uptime: $(uptime -p)"
    echo "Charge: $(uptime | awk -F'load average:' '{print $2}')"
}

# Fonction de vérification des services
verifier_services() {
    local services=("sshd" "nginx" "mysql")
    echo "=== Vérification Services ==="

    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service"; then
            echo "Service $service: ACTIF"
        else
            echo "Service $service: INACTIF"
        fi
    done
}

# Fonction de maintenance
effectuer_maintenance() {
    echo "=== Maintenance Système ==="
    echo "Nettoyage des logs anciens..."
    find /var/log -name "*.log" -mtime +30 -type f
    echo "Vérification de l'espace disque..."
    df -h | grep -E '^/dev/'
}

# Fonction principale - orchestration
main() {
    echo "Début du script de monitoring - $(date)"
    echo "======================================="

    obtenir_info_systeme
    echo
    verifier_services
    echo
    effectuer_maintenance

    echo "======================================="
    echo "Fin du script - $(date)"
}

# Exécution du script principal
main "$@"
```

**Schéma conceptuel** :

```
Script modulaire
├── Fonction 1: Information système
├── Fonction 2: Vérification services
├── Fonction 3: Maintenance
└── Main: Orchestration des fonctions
```

### Utilisation des Variables Locales

#### Définition : Variables Locales vs Globales

Les **variables locales** sont confinées à la portée d'une fonction et n'affectent pas l'environnement global du script.

**Terminologie technique** :

- **Variable locale** : Variable accessible uniquement dans la fonction (anglais : local variable)
- **Portée** : Zone du code où une variable est accessible (anglais : scope)
- **Encapsulation** : Isolation des données dans une fonction (anglais : encapsulation)
- **Pollution globale** : Modification involontaire de variables externes (anglais : global pollution)

#### Comparaison Variables Locales vs Globales

| Aspect                | Variables Globales       | Variables Locales             |
| --------------------- | ------------------------ | ----------------------------- |
| **Déclaration**       | `variable="valeur"`      | `local variable="valeur"`     |
| **Portée**            | Tout le script           | Fonction uniquement           |
| **Persistance**       | Jusqu'à la fin du script | Jusqu'à la fin de la fonction |
| **Isolation**         | Aucune                   | Complète                      |
| **Risque de conflit** | Élevé                    | Aucun                         |

#### Exemple démonstratif : Problème sans variables locales

```bash
#!/bin/bash

# Variable globale
username="admin"

fonction_problematique() {
    # PROBLÈME : Modification involontaire de la variable globale
    username="$1"  # Écrase la variable globale !
    echo "Utilisateur dans fonction: $username"
}

echo "Avant fonction: $username"
fonction_problematique "invité"
echo "Après fonction: $username"  # Résultat inattendu : "invité"
```

#### Solution avec variables locales

```bash
#!/bin/bash

# Variable globale préservée
username="admin"

fonction_correcte() {
    # SOLUTION : Variable locale protège la globale
    local username="$1"  # Crée une variable locale distincte
    echo "Utilisateur dans fonction: $username"
}

echo "Avant fonction: $username"    # Affiche: admin
fonction_correcte "invité"           # Affiche: invité
echo "Après fonction: $username"    # Affiche toujours: admin
```

#### Bonnes pratiques : Déclaration et utilisation

```bash
#!/bin/bash

calculer_espace_disque() {
    # Déclaration des paramètres en variables locales
    local partition="$1"
    local seuil_alerte="${2:-80}"  # Valeur par défaut: 80

    # Variable locale pour calcul intermédiaire
    local usage=$(df "$partition" | tail -1 | awk '{print $5}' | cut -d'%' -f1)

    # Logique de traitement
    if [[ $usage -gt $seuil_alerte ]]; then
        echo "Attention: Partition $partition à ${usage}%"
        return 1
    else
        echo "Partition $partition: ${usage}% (OK)"
        return 0
    fi
}
```

#### Avantages des variables locales en DevOps

**1. Réutilisabilité sécurisée**

```bash
# Fonction réutilisable sans effet de bord
deploy_service() {
    local service_name="$1"
    local version="$2"
    local config_file="/tmp/deploy_${service_name}.conf"

    # Variables locales garantissent l'isolation
    echo "Déploiement $service_name version $version"
    # Aucun risque de conflit avec d'autres fonctions
}
```

**2. Débogage facilité**

```bash
# Variables locales simplifient le débogage
monitor_process() {
    local process_name="$1"
    local pid=$(pgrep "$process_name")  # Variable locale claire
    local memory_usage=$(ps -o rss= -p "$pid")

    echo "DEBUG: process=$process_name, pid=$pid, memory=$memory_usage"
    # Chaque variable a une portée bien définie
}
```

**3. Maintenance simplifiée**

```bash
# Modification d'une fonction sans impact externe
backup_database() {
    local db_name="$1"
    local backup_dir="$2"

    # Ajout de nouvelles variables locales sans risque
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="${backup_dir}/${db_name}_${timestamp}.sql"

    mysqldump "$db_name" > "$backup_file"
}
```

#### Règles d'utilisation recommandées

**1. Toujours déclarer les paramètres en local**

```bash
ma_fonction() {
    local param1="$1"  # CORRECT
    local param2="$2"  # CORRECT
    # Ne jamais utiliser directement $1, $2 dans le code
}
```

**2. Variables de calcul en local**

```bash
calculer_statistiques() {
    local fichier="$1"

    # Variables intermédiaires toujours en local
    local nb_lignes=$(wc -l < "$fichier")
    local taille=$(stat -c%s "$fichier")
    local moyenne=$((taille / nb_lignes))

    echo "Statistiques: $nb_lignes lignes, $taille octets, $moyenne octets/ligne"
}
```

**3. Configuration temporaire en local**

```bash
configure_environment() {
    local env_type="$1"

    # Configuration locale à la fonction
    local log_level="DEBUG"
    local max_connections=100

    case "$env_type" in
        "production")
            log_level="ERROR"
            max_connections=1000
            ;;
    esac

    echo "Configuration: log=$log_level, connections=$max_connections"
}
```

### Application pratique

📝 **LAB 1** - Fonctions modulaires : `S1_S2_S2_lab1_fonctions_modulaires.sh`

**Énoncé du LAB 1** :
Créez un script avec fonctions modulaires pour l'administration système.

- **Objectif** : Développer un script avec 4 fonctions réutilisables pour vérifications système
- **Contexte** : Outil de diagnostic rapide pour serveurs DevOps
- **Instructions** : Créer fonctions pour info système, vérification services, espace disque, processus
- **Critères d'évaluation** : 4 fonctions avec paramètres locaux, gestion des erreurs, retours explicites
- **Durée estimée** : 15 minutes
- **Fichier de travail** : `S1_S2_S2_lab1_fonctions_modulaires.sh`

## 2. Gestion d'Erreurs et Validation

### Définition : Gestion d'Erreurs

La **gestion d'erreurs** consiste à prévoir, détecter et traiter les situations d'échec dans un script, permettant un comportement contrôlé et informatif en cas de problème.

**Terminologie technique** :

- **Code de retour** : Valeur numérique indiquant le succès (0) ou l'échec (non-0) (anglais : exit code)
- **Validation d'entrée** : Vérification de la validité des paramètres (anglais : input validation)
- **Gestion gracieuse** : Traitement élégant des erreurs sans crash (anglais : graceful handling)
- **Signal handling** : Capture et traitement des signaux système (anglais : signal handling)
- **Error propagation** : Transmission des erreurs entre fonctions (anglais : error propagation)

### Contexte d'utilisation DevOps

Une gestion d'erreurs robuste est essentielle pour des scripts d'automatisation fiables, évitant les pannes en cascade et permettant un débogage efficace.

### Bash vs Try/Catch/Finally : Comparaison des Paradigmes

**Important** : Bash ne possède pas de structures try/catch/finally comme les langages orientés objet (Java, Python, C#). Cependant, Bash offre des mécanismes équivalents :

**Équivalences conceptuelles** :

| Concept OOP      | Équivalent Bash             | Syntaxe                     |
| ---------------- | --------------------------- | --------------------------- |
| try {...}        | Exécution avec vérification | `if command; then`          |
| catch(Exception) | Test du code de retour      | `else` ou `if [ $? -ne 0 ]` |
| finally {...}    | Fonction trap               | `trap "cleanup" EXIT`       |

### Variable Spéciale `$?` : Code de Retour

La variable **`$?`** est une **variable automatique** fondamentale qui contient le **code de retour** (exit status) de la **dernière commande exécutée**.

#### Principe de fonctionnement

**Valeurs possibles** :

- **`0`** = Succès (commande réussie)
- **`1-255`** = Échec (différents types d'erreurs)

#### Codes de retour courants

| Code  | Signification                        |
| ----- | ------------------------------------ |
| `0`   | Succès                               |
| `1`   | Erreur générale                      |
| `2`   | Utilisation incorrecte               |
| `126` | Commande trouvée mais non exécutable |
| `127` | Commande introuvable                 |
| `130` | Script terminé par Ctrl+C            |

#### Exemples de base

```bash
# Commande réussie
ls /home
echo $?  # Affiche : 0 (succès)

# Commande échouée
ls /dossier_inexistant
echo $?  # Affiche : 2 (erreur : dossier introuvable)
```

#### Piège important à éviter

```bash
# INCORRECT : $? est écrasé
ls /dossier_inexistant
echo "Quelque chose"  # $? devient 0 (echo a réussi)
echo $?  # Affiche : 0 (et non l'erreur de ls)

# CORRECT : Sauvegarde immédiate
ls /dossier_inexistant
exit_code=$?  # Sauvegarde immédiate
echo "Traitement..."
echo "Code de retour du ls : $exit_code"
```

### Redirection des Flux : Comprendre `>&2`

La syntaxe **`>&2`** est une **redirection** fondamentale pour diriger les messages d'erreur vers le flux approprié.

#### Les flux standards Unix/Linux

**Descripteurs de fichiers** :

| Numéro | Nom        | Description     | Usage                       |
| ------ | ---------- | --------------- | --------------------------- |
| `0`    | **stdin**  | Entrée standard | Clavier, fichiers d'entrée  |
| `1`    | **stdout** | Sortie standard | Affichage normal, résultats |
| `2`    | **stderr** | Erreur standard | Messages d'erreur, alertes  |

#### Syntaxe de redirection

**Éléments de `>&2`** :

- **`>`** = Opérateur de redirection
- **`&2`** = Référence au descripteur de fichier 2 (stderr)
- **`>&2`** = "Rediriger vers stderr"

#### Comparaison pratique

```bash
# Sortie normale (stdout)
echo "Traitement réussi"

# Sortie d'erreur (stderr)
echo "Erreur: Paramètres manquants" >&2

# Démonstration de la différence
echo "Message normal"                    # Vers stdout (1)
echo "Message d'erreur" >&2            # Vers stderr (2)
```

#### Avantages de la séparation des flux

```bash
# Exemple concret : Fonction avec gestion des flux
backup_file() {
    local source="$1"
    local destination="$2"

    # Validation avec message d'erreur approprié
    if [[ ! -f "$source" ]]; then
        echo "Erreur: Fichier source inexistant: $source" >&2
        return 1
    fi

    # Opération avec message de succès normal
    if cp "$source" "$destination"; then
        echo "Sauvegarde réussie: $source -> $destination"
        return 0
    else
        echo "Erreur: Échec de la copie" >&2
        return 2
    fi
}
```

#### Utilisation pratique des redirections

```bash
# Redirection vers fichiers différents
./script.sh > resultats.txt 2> erreurs.txt

# Redirection combinée
./script.sh > output.log 2>&1   # Tout vers output.log

# Suppression des erreurs
./script.sh 2>/dev/null         # Ignorer les erreurs

# Séparation automatique
./script.sh | grep "SUCCESS"    # Seuls les résultats normaux
```

#### Pourquoi utiliser `>&2` pour les erreurs

**Avantages** :

1. **Séparation logique** : Erreurs vs résultats normaux
2. **Filtrage possible** : Traitement différencié des flux
3. **Standards Unix** : Respect des conventions système
4. **Debugging** : Isolation des messages d'erreur
5. **Automation** : Scripts plus robustes en production

### Mécanismes de Base : Codes de Retour

```bash
#!/bin/bash

# Vérification simple avec codes de retour
backup_database() {
    local db_name="$1"
    local backup_dir="$2"

    # Validation des paramètres
    if [[ -z "$db_name" ]] || [[ -z "$backup_dir" ]]; then
        echo "Erreur: Paramètres manquants (db_name, backup_dir)" >&2
        return 1
    fi

    # Tentative de sauvegarde
    if mysqldump "$db_name" > "$backup_dir/${db_name}_$(date +%Y%m%d).sql"; then
        echo "Sauvegarde réussie : $db_name"
        return 0
    else
        echo "Erreur: Échec de la sauvegarde de $db_name" >&2
        return 2
    fi
}

# Utilisation avec gestion d'erreur
if backup_database "production" "/backup"; then
    echo "Processus terminé avec succès"
else
    error_code=$?
    echo "Erreur détectée (code: $error_code)"
    exit $error_code
fi
```

### Gestion Avancée : Scripts Robustes

#### Définition : Robustesse d'un Script

Un **script robuste** est un script qui peut gérer les erreurs de manière élégante et continuer à fonctionner ou s'arrêter proprement sans endommager le système.

**Terminologie technique** :

- **Robustesse** : Capacité à fonctionner malgré les erreurs (anglais : robustness)
- **Gestion gracieuse** : Arrêt propre en cas d'erreur (anglais : graceful handling)
- **Script défensif** : Script qui anticipe les problèmes (anglais : defensive scripting)

#### Principe 1 : Arrêt en cas d'erreur avec `set -e`

**Problème sans `set -e`** :

```bash
#!/bin/bash
# Script DANGEREUX - continue malgré les erreurs

echo "Début du script"
cd /repertoire/inexistant    # ERREUR mais le script continue !
rm -rf *                     # CATASTROPHE : supprime tout le répertoire courant !
echo "Script terminé"        # Ce message s'affiche quand même
```

**Solution avec `set -e`** :

```bash
#!/bin/bash
set -e  # Arrêt immédiat si une commande échoue

echo "Début du script"
cd /repertoire/inexistant    # ERREUR → le script s'arrête ici
rm -rf *                     # Cette ligne ne s'exécute JAMAIS
echo "Script terminé"        # Ce message ne s'affiche jamais
```

#### Principe 2 : Validation des Variables avec `set -u`

**Problème sans `set -u`** :

```bash
#!/bin/bash
# Variables non définies = chaînes vides (dangereux)

echo "Suppression du répertoire: $BACKUP_DIR"
rm -rf $BACKUP_DIR/*    # Si BACKUP_DIR vide → rm -rf /*  (CATASTROPHE!)
```

**Solution avec `set -u`** :

```bash
#!/bin/bash
set -u  # Erreur si variable non définie

echo "Suppression du répertoire: $BACKUP_DIR"  # ERREUR si BACKUP_DIR non définie
rm -rf $BACKUP_DIR/*    # Cette ligne ne s'exécute pas si erreur au-dessus
```

#### Principe 3 : Nettoyage Automatique Simple

**Concept du nettoyage automatique** :

```bash
#!/bin/bash
set -e  # Arrêt en cas d'erreur

# Fonction de nettoyage simple
nettoyer() {
    echo "Nettoyage en cours..."

    # Suppression des fichiers temporaires créés
    if [ -f "/tmp/mon_fichier_temp" ]; then
        rm -f "/tmp/mon_fichier_temp"
        echo "Fichier temporaire supprimé"
    fi

    echo "Nettoyage terminé"
}

# Installer le nettoyage automatique
trap nettoyer EXIT

# Votre script principal
echo "Création d'un fichier temporaire..."
touch "/tmp/mon_fichier_temp"

echo "Simulation de travail..."
sleep 2

echo "Script terminé"
# La fonction nettoyer() s'exécute automatiquement ici
```

#### Application DevOps : Script de Sauvegarde Robuste

```bash
#!/bin/bash
# Script de sauvegarde robuste et simple

# Configuration robuste
set -e  # Arrêt en cas d'erreur
set -u  # Erreur si variable non définie

# Variables obligatoires
SOURCE_DIR="$1"
BACKUP_DIR="$2"

# Validation simple des paramètres
if [ $# -ne 2 ]; then
    echo "Usage: $0 <repertoire_source> <repertoire_sauvegarde>" >&2
    exit 1
fi

# Validation de l'existence du répertoire source
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Erreur: Le répertoire source n'existe pas: $SOURCE_DIR" >&2
    exit 1
fi

# Fonction de nettoyage
cleanup() {
    echo "Nettoyage en cours..."
    # Suppression du fichier temporaire s'il existe
    [ -f "/tmp/backup_in_progress" ] && rm -f "/tmp/backup_in_progress"
    echo "Nettoyage terminé"
}

# Installation du nettoyage automatique
trap cleanup EXIT

# Script principal
echo "Début de la sauvegarde de $SOURCE_DIR vers $BACKUP_DIR"

# Création du marqueur de sauvegarde en cours
touch "/tmp/backup_in_progress"

# Création du répertoire de sauvegarde s'il n'existe pas
mkdir -p "$BACKUP_DIR"

# Sauvegarde avec validation
if cp -r "$SOURCE_DIR"/* "$BACKUP_DIR"/; then
    echo "Sauvegarde réussie !"
else
    echo "Erreur lors de la sauvegarde" >&2
    exit 1
fi

echo "Sauvegarde terminée avec succès"
# cleanup() s'exécute automatiquement
```

#### Amélioration : Gestion des Cas d'Erreur Spécifiques

```bash
#!/bin/bash
set -e
set -u

# Fonction pour vérifier l'espace disque
verifier_espace_disque() {
    local repertoire="$1"
    local espace_libre=$(df "$repertoire" | tail -1 | awk '{print $4}')

    # Vérification simple : au moins 1GB libre (1000000 KB)
    if [ "$espace_libre" -lt 1000000 ]; then
        echo "Erreur: Espace disque insuffisant dans $repertoire" >&2
        return 1
    fi

    echo "Espace disque suffisant: ${espace_libre}KB libres"
    return 0
}

# Fonction pour vérifier les permissions
verifier_permissions() {
    local repertoire="$1"

    if [ ! -w "$repertoire" ]; then
        echo "Erreur: Pas de permission d'écriture sur $repertoire" >&2
        return 1
    fi

    echo "Permissions d'écriture: OK"
    return 0
}

# Script principal avec validations
echo "=== Vérifications préliminaires ==="
verifier_espace_disque "$BACKUP_DIR"
verifier_permissions "$BACKUP_DIR"
echo "Toutes les vérifications sont réussies"
```

### Validation Robuste des Paramètres

#### Explication détaillée : `trap "cleanup" EXIT`

**Fonctionnement** :

1. **`trap cleanup EXIT`** = À la fin du script, exécute automatiquement la fonction `cleanup`
2. **`trap cleanup INT TERM`** = En cas d'interruption (Ctrl+C) ou signal kill, exécute `cleanup`
3. **Déclenchement automatique** : Aucune intervention manuelle nécessaire

**Cas d'usage** :

```bash
# Exemple simple de trap
#!/bin/bash

# Simulation de ressources à nettoyer
TEMP_FILE="/tmp/deploy_$$.tmp"
SERVICE_PID=""

cleanup_simple() {
    echo "Nettoyage automatique..."
    [[ -f "$TEMP_FILE" ]] && rm -f "$TEMP_FILE"
    [[ -n "$SERVICE_PID" ]] && kill "$SERVICE_PID" 2>/dev/null || true
    echo "Ressources libérées"
}

# Installation du piège - OBLIGATOIRE avant utilisation des ressources
trap cleanup_simple EXIT

# Utilisation normale - cleanup sera automatique
echo "Création de fichier temporaire..."
touch "$TEMP_FILE"

echo "Démarrage service (simulation)..."
sleep 30 &  # Processus en arrière-plan
SERVICE_PID=$!

# Si erreur ici, ou Ctrl+C, ou fin normale → cleanup automatique !
echo "Traitement terminé"
```

**Points critiques** :

- **Ordre important** : `trap` doit être défini **AVANT** la création des ressources
- **EXIT toujours déclenché** : Même en cas de succès
- **Préservation de $?** : Utiliser `local exit_code=$?` pour conserver le code d'erreur original

#### Scénarios de déclenchement

| Situation                  | Signal | Résultat             |
| -------------------------- | ------ | -------------------- |
| Script termine normalement | `EXIT` | `cleanup()` exécutée |
| Erreur avec `set -e`       | `EXIT` | `cleanup()` exécutée |
| Utilisateur fait Ctrl+C    | `INT`  | `cleanup()` exécutée |
| Commande `kill script_pid` | `TERM` | `cleanup()` exécutée |
| `exit 1` explicite         | `EXIT` | `cleanup()` exécutée |

# Fonction avec gestion d'erreur sophistiquée

```bash
# Fonction de déploiement d'application avec gestion complète d'erreurs
# Paramètres:
#   $1 - nom de l'application à déployer
#   $2 - version de l'application à installer
deploy_application() {
    # Récupération des paramètres d'entrée dans des variables locales
    local app_name="$1"    # Nom de l'application (ex: "nginx", "apache")
    local version="$2"     # Version à déployer (ex: "1.2.3", "latest")

    # Affichage du début de déploiement pour traçabilité
    echo "Déploiement de $app_name version $version"

    # Création d'un répertoire temporaire sécurisé et unique
    # mktemp -d garantit un nom unique et des permissions restrictives (700)
    TEMP_DIR=$(mktemp -d)
    echo "Répertoire temporaire : $TEMP_DIR"

    # Bloc principal de déploiement avec gestion d'erreurs centralisée
    # L'utilisation de { } permet de capturer toutes les erreurs en un point
    {
        # ÉTAPE 1: Téléchargement du package d'application
        echo "Étape 1: Téléchargement..."
        # wget -q : téléchargement silencieux (pas de barre de progression)
        # -O : spécifie le nom du fichier de sortie
        # || : si wget échoue, exécuter le bloc d'erreur
        wget -q "https://releases.example.com/${app_name}-${version}.tar.gz" -O "$TEMP_DIR/app.tar.gz" || {
            echo "Erreur: Téléchargement échoué" >&2  # Erreur vers stderr
            return 3  # Code d'erreur spécifique pour le téléchargement
        }

        # ÉTAPE 2: Extraction de l'archive téléchargée
        echo "Étape 2: Extraction..."
        # tar -xzf : extraction (-x) d'archive gzip (-z) depuis fichier (-f)
        # -C : spécifie le répertoire de destination
        tar -xzf "$TEMP_DIR/app.tar.gz" -C "$TEMP_DIR" || {
            echo "Erreur: Extraction échouée" >&2
            return 4  # Code d'erreur spécifique pour l'extraction
        }

        # ÉTAPE 3: Installation dans le répertoire de destination
        echo "Étape 3: Installation..."
        # cp -r : copie récursive de tous les fichiers extraits
        # Destination: /opt/$app_name/ (répertoire standard pour applications)
        cp -r "$TEMP_DIR"/* "/opt/$app_name/" || {
            echo "Erreur: Installation échouée" >&2
            return 5  # Code d'erreur spécifique pour l'installation
        }

        # Message de succès si toutes les étapes ont réussi
        echo "Déploiement réussi !"

    } || {
        # BLOC DE GESTION D'ERREURS CENTRALISÉE
        # Exécuté si n'importe quelle étape du bloc principal échoue

        # Capture du code d'erreur de l'étape qui a échoué
        local error_code=$?
        echo "Échec du déploiement (code: $error_code)" >&2

        # PROCÉDURE DE ROLLBACK AUTOMATIQUE
        echo "Tentative de rollback..."
        # Arrêt du service de l'application si il était démarré
        # 2>/dev/null : supprime les messages d'erreur stderr
        # || true : continue même si systemctl échoue (service peut ne pas exister)
        systemctl stop "$app_name" 2>/dev/null || true

        # Retourner le code d'erreur original pour diagnostic
        return $error_code
    }
}
```

### Validation Robuste des Paramètres

```bash
#!/bin/bash

# Fonction de validation complète des paramètres de configuration serveur
# Paramètres:
#   $1 - nom du serveur (ex: "web01.example.com")
#   $2 - port du service (ex: "80", "443", "8080")
#   $3 - chemin du certificat SSL (optionnel, ex: "/etc/ssl/cert.pem")
validate_server_config() {
    # Récupération des paramètres dans des variables locales explicites
    local server_name="$1"   # Nom/FQDN du serveur à valider
    local port="$2"          # Port réseau (1-65535)
    local ssl_cert="$3"      # Chemin vers certificat SSL (optionnel)

    # Compteur d'erreurs pour accumuler les problèmes de validation
    local errors=0

    # VALIDATION 1: Nom de serveur obligatoire et format valide
    if [[ -z "$server_name" ]]; then
        # Test si la variable est vide ou non définie
        echo "Erreur: Nom de serveur requis" >&2
        ((errors++))  # Incrémentation atomique du compteur
    elif [[ ! "$server_name" =~ ^[a-zA-Z0-9.-]+$ ]]; then
        # Expression régulière pour valider le format FQDN
        # ^[a-zA-Z0-9.-]+$ = début^, caractères autorisés, fin$
        echo "Erreur: Nom de serveur invalide ($server_name)" >&2
        ((errors++))
    fi

    # VALIDATION 2: Port obligatoire et dans la plage valide
    if [[ -z "$port" ]]; then
        # Vérification que le port est fourni
        echo "Erreur: Port requis" >&2
        ((errors++))
    elif [[ ! "$port" =~ ^[0-9]+$ ]] || [[ "$port" -lt 1 ]] || [[ "$port" -gt 65535 ]]; then
        # Triple validation du port:
        # 1. ^[0-9]+$ = que des chiffres
        # 2. -lt 1 = pas de port 0 ou négatif
        # 3. -gt 65535 = respect limite TCP/UDP
        echo "Erreur: Port invalide ($port), doit être entre 1-65535" >&2
        ((errors++))
    fi

    # VALIDATION 3: Certificat SSL (optionnel mais si fourni, doit être valide)
    if [[ -n "$ssl_cert" ]]; then
        # -n teste si la variable n'est pas vide
        if [[ ! -f "$ssl_cert" ]]; then
            # -f teste l'existence du fichier régulier
            echo "Erreur: Certificat SSL introuvable ($ssl_cert)" >&2
            ((errors++))
        elif ! openssl x509 -in "$ssl_cert" -noout -checkend 86400 2>/dev/null; then
            # Vérification expiration certificat avec OpenSSL:
            # -checkend 86400 = vérifier expiration dans 24h (86400 secondes)
            # -noout = pas d'affichage du certificat
            # 2>/dev/null = supprimer les erreurs stderr
            echo "Avertissement: Certificat SSL expire dans moins de 24h" >&2
            # Note: pas d'incrémentation errors car c'est un avertissement
        fi
    fi

    # Retour du nombre total d'erreurs trouvées
    # 0 = validation réussie, >0 = nombre d'erreurs
    return $errors
}

# Fonction de monitoring avancé avec classification des erreurs
# Surveille l'état des services système et détermine la criticité
monitor_services() {
    # Liste des services à surveiller (tableau indexé)
    local services=("nginx" "mysql" "redis")  # Services web typiques
    local failed_services=()  # Tableau dynamique pour services en échec
    local critical_failure=false  # Flag pour services critiques

    echo "=== Monitoring des Services ==="

    # Boucle de vérification pour chaque service
    for service in "${services[@]}"; do
        # systemctl is-active --quiet : vérification silencieuse du statut
        # --quiet = pas de sortie texte, juste code de retour
        if systemctl is-active --quiet "$service"; then
            echo "Service $service: ACTIF"
        else
            # Service inactif ou en erreur
            echo "Service $service: INACTIF" >&2  # Message vers stderr
            failed_services+=("$service")  # Ajout au tableau des échecs

            # CLASSIFICATION DE CRITICITÉ: Services essentiels vs secondaires
            if [[ "$service" == "nginx" ]] || [[ "$service" == "mysql" ]]; then
                # nginx = serveur web, mysql = base de données
                # Ces services sont considérés comme CRITIQUES
                critical_failure=true
            fi
            # redis = cache, considéré comme non-critique dans cet exemple
        fi
    done

    # ANALYSE DES RÉSULTATS ET ACTIONS CORRECTIVES
    if [[ ${#failed_services[@]} -gt 0 ]]; then
        # ${#array[@]} = nombre d'éléments dans le tableau
        echo "Services en échec: ${failed_services[*]}" >&2
        # ${array[*]} = tous les éléments séparés par espaces

        if [[ "$critical_failure" == true ]]; then
            # GESTION DES PANNES CRITIQUES
            echo "ALERTE CRITIQUE: Service critique en panne !" >&2

            # Notification système via syslog pour alertes automatisées
            # logger envoie vers /var/log/syslog pour monitoring externe
            logger "CRITICAL: Service failure detected: ${failed_services[*]}"

            return 2  # Code d'erreur critique (conventions: 2 = erreur grave)
        else
            # GESTION DES PANNES NON-CRITIQUES
            echo "Avertissement: Services non-critiques en panne" >&2
            return 1  # Code d'avertissement (conventions: 1 = avertissement)
        fi
    fi

    # Tous les services fonctionnent normalement
    echo "Tous les services sont opérationnels"
    return 0  # Succès complet (conventions: 0 = succès)
}
```

### Application pratique

📝 **LAB 2** - Scripts d'administration système : `S1_S2_S2_lab2_scripts_administration.sh`

**Énoncé du LAB 2** :
Créez des scripts Bash pour l'administration système et le monitoring de base.

- **Objectif** : Développer des scripts de maintenance et surveillance système
- **Contexte** : Administration quotidienne avec surveillance CPU, mémoire, disque et processus
- **Instructions** : Scripts surveillance, nettoyage logs, sauvegarde configuration, rapport système
- **Critères d'évaluation** : Scripts fonctionnels, gestion d'erreurs, logs lisibles, automatisation basique
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S2_S2_lab2_scripts_administration.sh`

## 3. Scripts Modulaires et Organisation

### Définition : Scripts Modulaires

Les **scripts modulaires** consistent à décomposer un script complexe en **unités fonctionnelles** distinctes et réutilisables, permettant une meilleure lisibilité, maintenance et évolutivité du code.

**Terminologie technique** :

- **Modularité** : Principe de décomposition en modules indépendants (anglais : modularity)
- **Source/Include** : Mécanisme d'inclusion de fichiers externes (anglais : source/include)
- **Namespace** : Espace de noms pour éviter les conflits de variables (anglais : namespace)
- **Librairie** : Collection de fonctions réutilisables (anglais : library)
- **Séparation des responsabilités** : Principe d'une fonction = une responsabilité (anglais : separation of concerns)

### Contexte d'utilisation DevOps

La modularité est essentielle en DevOps pour créer des **bibliothèques d'automatisation** réutilisables, standardiser les opérations récurrentes et faciliter la collaboration en équipe sur les scripts d'infrastructure.

### Schéma Conceptuel : Architecture Modulaire

```
┌─────────────────────────────────────────────────────────────┐
│                    SCRIPT PRINCIPAL                        │
│                     (main.sh)                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
│ CONFIGURATION│ │LIBRAIRIES│ │  MODULES   │
│  (config/)   │ │ (lib/)   │ │ (modules/) │
├──────────────┤ ├──────────┤ ├────────────┤
│• common.conf │ │• utils.sh│ │• docker.sh │
│• env.conf    │ │• logs.sh │ │• k8s.sh    │
│• secrets.env │ │• net.sh  │ │• aws.sh    │
└──────────────┘ └──────────┘ └────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
              ┌───────▼───────┐
              │   EXÉCUTION   │
              │   UNIFIÉE     │
              └───────────────┘
```

### Principe de Séparation des Responsabilités

**Exemple simple : Structure de base**

```bash
#!/bin/bash
# main.sh - Script principal orchestrateur

# Import des modules (séparation des responsabilités)
source "$(dirname "$0")/lib/logger.sh"
source "$(dirname "$0")/lib/validator.sh"
source "$(dirname "$0")/config/app.conf"

# Fonction principale (orchestration simple)
main() {
    log_info "Début déploiement application"

    # Validation des prérequis
    validate_environment || exit 1

    # Déploiement
    deploy_application

    log_success "Déploiement terminé"
}

# Point d'entrée unique
main "$@"
```

### Librairie de Fonctions Utilitaires

**Exemple : lib/logger.sh**

```bash
#!/bin/bash
# lib/logger.sh - Module de logging standardisé

# Configuration des couleurs pour lisibilité
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Fonction de log info (simple et claire)
log_info() {
    local message="$1"
    echo -e "[$(date '+%H:%M:%S')] INFO: $message"
}

# Fonction de log erreur (avec couleur)
log_error() {
    local message="$1"
    echo -e "[$(date '+%H:%M:%S')] ${RED}ERROR: $message${NC}" >&2
}

# Fonction de log succès (visuelle)
log_success() {
    local message="$1"
    echo -e "[$(date '+%H:%M:%S')] ${GREEN}SUCCESS: $message${NC}"
}
```

### Configuration Centralisée

**Exemple académique : config/app.conf**

```bash
#!/bin/bash
# config/app.conf - Configuration centralisée

# Variables d'environnement (séparation config/code)
APP_NAME="web-app"
APP_VERSION="1.2.0"
DEPLOY_ENV="production"

# Chemins standardisés
APP_DIR="/opt/${APP_NAME}"
LOG_DIR="/var/log/${APP_NAME}"
BACKUP_DIR="/backup/${APP_NAME}"

# Paramètres de déploiement
MAX_RETRY=3
TIMEOUT=30
```

### Diagramme de Flux : Modularité en Action

```
DÉBUT
  │
  ▼
┌────────────────┐
│ CHARGEMENT     │◄── source lib/logger.sh
│ MODULES        │◄── source lib/validator.sh
└────────┬───────┘◄── source config/app.conf
         │
         ▼
┌────────────────┐
│ VALIDATION     │◄── validate_environment()
│ ENVIRONNEMENT  │◄── check_dependencies()
└────────┬───────┘
         │
    ┌────▼────┐
    │SUCCESS? │
    └────┬────┘
         │ OUI
         ▼
┌────────────────┐
│ EXÉCUTION      │◄── deploy_application()
│ DÉPLOIEMENT    │◄── log_info(), log_success()
└────────┬───────┘
         │
         ▼
       FIN
```

### Application pratique

📝 **LAB 3** - Scripts modulaires et organisation : `S1_S2_S2_lab3_scripts_modulaires.sh`

**Énoncé du LAB 3** :
Développez une architecture de scripts modulaires avec bibliothèques réutilisables.

- **Objectif** : Créer une structure modulaire avec fonctions communes et configuration partagée
- **Contexte** : Organisation de scripts DevOps pour maintenance, déploiement et monitoring
- **Instructions** : Structure modulaire, fonctions utilitaires, configuration centralisée, documentation
- **Critères d'évaluation** : Architecture claire, réutilisabilité, configuration centralisée, documentation complète
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S2_S2_lab3_scripts_modulaires.sh`

## 4. Automatisation et Maintenance

### Définition : Automatisation Système

L'**automatisation système** consiste à créer des scripts qui exécutent automatiquement des tâches récurrentes d'administration et de maintenance.

**Terminologie technique** :

- **Tâches automatisées** : Opérations programmées et répétitives (anglais : automated tasks)
- **Maintenance préventive** : Maintenance programmée pour éviter les pannes (anglais : preventive maintenance)
- **Script de déploiement** : Script pour automatiser la mise en production (anglais : deployment script)

### Contexte d'utilisation DevOps

L'automatisation réduit les erreurs humaines, garantit la cohérence des opérations et libère du temps pour des tâches à plus forte valeur ajoutée.

### Script de Maintenance : Définition vs Automatisation

#### Problématique : Fonction de base vs Vraie automatisation

**Important** : Une fonction de maintenance seule ne garantit PAS l'automatisation. Elle définit **ce qui doit être fait** mais pas **quand** ni **comment** l'automatiser.

**Exemple de fonction basique** :

```bash
# ATTENTION : Cette fonction n'est PAS automatique !
perform_system_maintenance() {
    local maintenance_type="$1"

    log_info "Début de la maintenance: $maintenance_type"

    case "$maintenance_type" in
        "daily")
            clean_temp_files      # Peut échouer silencieusement
            rotate_logs          # S'exécute même si précédent échoué
            check_disk_space     # Pas de validation des prérequis
            ;;
        "weekly")
            update_system_packages
            backup_configurations
            verify_services
            ;;
    esac

    log_info "Maintenance terminée avec succès"  # Message trompeur si erreurs
}
```

**Problèmes identifiés** :

1. **Exécution manuelle** : Fonction attend d'être appelée
2. **Pas de gestion d'erreurs** : Continue même si étapes échouent
3. **Pas de planification** : Aucun mécanisme de répétition automatique
4. **Pas de surveillance** : Aucun logging ou alertes d'échec

#### Solution : Automatisation robuste avec planification

```bash
#!/bin/bash
# Script : /usr/local/bin/automated_maintenance.sh

# Fonction de maintenance avec gestion d'erreurs complète
perform_system_maintenance() {
    local maintenance_type="$1"
    local errors=0
    local start_time=$(date +%s)
    local log_file="/var/log/maintenance_$(date +%Y%m%d).log"

    {
        echo "=== Début maintenance $maintenance_type - $(date) ==="

        case "$maintenance_type" in
            "daily")
                run_with_check "clean_temp_files" || ((errors++))
                run_with_check "rotate_logs" || ((errors++))
                run_with_check "check_disk_space" || ((errors++))
                ;;
            "weekly")
                run_with_check "update_system_packages" || ((errors++))
                run_with_check "backup_configurations" || ((errors++))
                run_with_check "verify_services" || ((errors++))
                ;;
            *)
                echo "ERREUR: Type de maintenance inconnu: $maintenance_type" >&2
                return 1
                ;;
        esac

        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        if [[ $errors -eq 0 ]]; then
            echo "=== Maintenance réussie - Durée: ${duration}s ==="
            return 0
        else
            echo "=== Maintenance terminée avec $errors erreurs - Durée: ${duration}s ===" >&2
            send_alert "Maintenance $maintenance_type: $errors erreurs détectées"
            return 1
        fi

    } | tee -a "$log_file"
}

# Fonction d'exécution avec vérification
run_with_check() {
    local func_name="$1"
    echo "Exécution: $func_name"

    if $func_name; then
        echo "SUCCESS: $func_name terminé"
        return 0
    else
        echo "ERROR: $func_name échoué" >&2
        return 1
    fi
}

# Fonction d'alerte pour surveillance
send_alert() {
    local message="$1"
    echo "ALERTE: $message" >&2
    logger "MAINTENANCE_ALERT: $message"
    # Notification système pour monitoring externe
}

# Point d'entrée automatique
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    perform_system_maintenance "$1"
fi
```

#### Mécanismes de planification automatique

**1. Automatisation avec crontab** :

```bash
# Installation dans le crontab système
# Fichier : /etc/crontab
0 2 * * * root /usr/local/bin/automated_maintenance.sh daily
0 3 * * 0 root /usr/local/bin/automated_maintenance.sh weekly

# Vérification de l'installation
crontab -l | grep automated_maintenance
```

**2. Automatisation moderne avec systemd** :

**Fichier service** : `/etc/systemd/system/daily-maintenance.service`

```ini
[Unit]
Description=Maintenance quotidienne automatisée
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/automated_maintenance.sh daily
User=root
StandardOutput=journal
StandardError=journal
```

**Fichier timer** : `/etc/systemd/system/daily-maintenance.timer`

```ini
[Unit]
Description=Timer maintenance quotidienne
Requires=daily-maintenance.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

**Activation** :

```bash
sudo systemctl enable daily-maintenance.timer
sudo systemctl start daily-maintenance.timer
sudo systemctl status daily-maintenance.timer
```

**3. Script auto-installant** :

```bash
# Fonction d'auto-installation dans cron
install_automation() {
    local script_path="$(realpath "$0")"

    echo "Installation de l'automatisation..."

    # Vérifier si déjà installé
    if crontab -l 2>/dev/null | grep -q "$script_path"; then
        echo "Automatisation déjà installée"
        return 0
    fi

    # Installer les tâches cron
    (
        crontab -l 2>/dev/null
        echo "# Maintenance automatique"
        echo "0 2 * * * $script_path daily"
        echo "0 3 * * 0 $script_path weekly"
    ) | crontab -

    echo "Automatisation installée avec succès"
    echo "Maintenance quotidienne : 02h00"
    echo "Maintenance hebdomadaire : 03h00 le dimanche"
}

# Usage : ./script.sh --install
if [[ "$1" == "--install" ]]; then
    install_automation
    exit 0
fi
```

#### Surveillance et monitoring

```bash
# Fonction de vérification de l'automatisation
verify_automation() {
    echo "=== Vérification Automatisation ==="

    # Vérifier présence dans cron
    if crontab -l 2>/dev/null | grep -q "automated_maintenance"; then
        echo "Crontab : CONFIGURÉ"
    else
        echo "Crontab : MANQUANT" >&2
    fi

    # Vérifier logs récents
    local last_log=$(ls -t /var/log/maintenance_*.log 2>/dev/null | head -1)
    if [[ -f "$last_log" ]]; then
        echo "Dernière exécution : $(stat -c %y "$last_log")"
        if grep -q "SUCCESS" "$last_log"; then
            echo "Statut dernière maintenance : SUCCÈS"
        else
            echo "Statut dernière maintenance : ERREURS DÉTECTÉES" >&2
        fi
    else
        echo "Aucun log de maintenance trouvé" >&2
    fi
}
```

**Workflow complet d'automatisation** :

```
Installation → Planification → Exécution → Surveillance → Alertes
     ↓              ↓            ↓           ↓           ↓
--install      cron/systemd   Scripts    Logs/Status  Notifications
```

### Automatisation de Déploiement Simple

```bash
deploy_application() {
 local app_name="$1"
 local version="$2"

 echo "Déploiement de $app_name version $version"

 # Sauvegarde de la version actuelle
 backup_current_version "$app_name"

 # Déploiement de la nouvelle version
 if install_new_version "$app_name" "$version"; then
 restart_application "$app_name"
 verify_deployment "$app_name"
 echo "Déploiement réussi"
 else
 rollback_application "$app_name"
 echo "Échec du déploiement - rollback effectué"
 return 1
 fi
}
```

### Application pratique

📝 **LAB 4** - Automatisation et maintenance : `S1_S2_S2_lab4_automatisation_maintenance.sh`

**Énoncé du LAB 4** :
Créez des scripts d'automatisation pour la maintenance système et le déploiement simple.

- **Objectif** : Développer des scripts d'automatisation pour tâches récurrentes et déploiement basique
- **Contexte** : Automatisation maintenance quotidienne, sauvegarde et déploiement d'applications simples
- **Instructions** : Scripts automatisés, planification tâches, sauvegarde/restauration, déploiement simple
- **Critères d'évaluation** : Automatisation fonctionnelle, gestion d'erreurs, logs détaillés, processus fiables
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S1_S2_S2_lab4_automatisation_maintenance.sh`

## 5. Récapitulatif et prochaines étapes

Cette séance a permis de progresser vers l'automatisation avec Bash intermédiaire : gestion d'erreurs, fonctions, scripts modulaires et maintenance automatisée.

**Concepts clés acquis** :

- Gestion avancée des erreurs avec try/catch et validation
- Fonctions Bash structurées avec paramètres et valeurs de retour
- Organisation modulaire des scripts avec bibliothèques communes
- Automatisation des tâches de maintenance et déploiement simple

**Prochaine séance** : Fondamentaux Python - Installation environnement et syntaxe de base pour outils DevOps.

## 6. Ressources complémentaires

- **Bash Scripting** : Advanced Bash-Scripting Guide (Mendel Cooper)
- **Error Handling** : Bash Error Handling Best Practices
- **Script Organization** : Shell Style Guide (Google)
- **Automation** : System Administration Scripts Collection
- **DevOps Basics** : The DevOps Handbook (Kim, Humble, Debois, Willis)

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 2_
