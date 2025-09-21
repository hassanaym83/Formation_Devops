# Simplon Maghreb - Formation DevOps

# Sprint 1 - Semaine 2 - Séance 3 : Fondamentaux Python pour DevOps

## Objectifs pédagogiques

- Manipuler variables et types Python pour scripts DevOps
- Appliquer opérateurs et structures conditionnelles
- Utiliser boucles pour automation de tâches répétitives
- Créer scripts monitoring et alertes

## Objectifs techniques

Python, variables, int, float, str, bool, list, dict, if/elif/else, for, while, opérateurs, f-strings, monitoring DevOps

## Table des matières

1. [Installation et configuration Python](#1-installation-et-configuration-python)
2. [Introduction et objectifs](#2-introduction-et-objectifs)
3. [Variables et types de données](#3-variables-et-types-de-données)
4. [Opérateurs et expressions](#4-opérateurs-et-expressions)
5. [Structures conditionnelles et boucles](#5-structures-conditionnelles-et-boucles)
6. [Récapitulatif et prochaines étapes](#6-récapitulatif-et-prochaines-étapes)
7. [Ressources complémentaires](#7-ressources-complémentaires)

## 1. Installation pyenv et environnements virtuels

### 1.1 Qu'est-ce que pyenv ?

**Définition** : pyenv est un gestionnaire de versions Python qui permet d'installer et de basculer facilement entre différentes versions de Python sur un même système.

**Avantages pour DevOps** :

- **Isolation des projets** : Chaque projet peut utiliser sa propre version Python
- **Compatibilité** : Tester le code sur différentes versions Python
- **Simplicité** : Installation et gestion centralisée des versions
- **Développement** : Éviter les conflits entre projets

### 1.2 Installation de pyenv

#### **Linux (Ubuntu/Debian)**

```bash
# Installation des dépendances
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
liblzma-dev python3-openssl git

# Installation de pyenv via le script automatique
curl https://pyenv.run | bash

# Ajout au fichier de configuration shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Recharger la configuration
source ~/.bashrc
```

#### **macOS**

```bash
# Installation via Homebrew
brew install pyenv

# Configuration du shell
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Recharger la configuration
source ~/.zshrc
```

#### **Windows (avec Git Bash)**

```bash
# Installation avec pyenv-win
git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv

# Ajout aux variables d'environnement Windows
# PYENV = %USERPROFILE%\.pyenv\pyenv-win
# PATH += %USERPROFILE%\.pyenv\pyenv-win\bin
# PATH += %USERPROFILE%\.pyenv\pyenv-win\shims
```

### 1.3 Utilisation de pyenv

#### **Commandes essentielles**

```bash
# Lister les versions Python disponibles
pyenv install --list

# Installer une version Python spécifique
pyenv install 3.11.0
pyenv install 3.10.8

# Lister les versions installées
pyenv versions

# Définir la version globale par défaut
pyenv global 3.11.0

# Définir la version locale pour un projet
cd /path/to/project
pyenv local 3.10.8

# Vérifier la version active
pyenv version
python --version
```

#### **Exemple pratique DevOps**

```bash
# Projet DevOps avec Python 3.11
mkdir monitoring-app
cd monitoring-app
pyenv local 3.11.0

# Projet legacy avec Python 3.9
mkdir legacy-scripts
cd legacy-scripts
pyenv local 3.9.16

# Vérification
cd monitoring-app && python --version  # Python 3.11.0
cd ../legacy-scripts && python --version  # Python 3.9.16
```

### 1.4 Environnements virtuels avec venv

#### **Qu'est-ce qu'un environnement virtuel ?**

**Définition** : Un environnement virtuel est un environnement Python isolé qui permet d'installer des packages spécifiques à un projet sans affecter le système global.

**Avantages DevOps** :

- **Isolation des dépendances** : Éviter les conflits entre projets
- **Reproductibilité** : Environnements identiques entre développement et production
- **Sécurité** : Isolation des packages et versions
- **Portabilité** : Partage facile des configurations

#### **Création et gestion d'environnements virtuels**

```bash
# Créer un environnement virtuel
python -m venv venv_devops

# Activer l'environnement (Linux/macOS)
source venv_devops/bin/activate

# Activer l'environnement (Windows)
venv_devops\Scripts\activate

# Vérifier l'activation
which python  # Doit pointer vers le venv
python --version
pip --version

# Désactiver l'environnement
deactivate
```

#### **Comprendre pip : le gestionnaire de packages Python**

**Définition** : pip (Pip Installs Packages) est le gestionnaire de packages officiel de Python. Il permet d'installer, de mettre à jour et de désinstaller des bibliothèques Python depuis le Python Package Index (PyPI) et d'autres dépôts.

**Rôle en DevOps** :

- **Gestion des dépendances** : Installation automatique des bibliothèques nécessaires aux projets
- **Reproductibilité** : Garantir que tous les développeurs utilisent les mêmes versions de packages
- **Automation** : Intégrer l'installation de packages dans les scripts de déploiement
- **Isolation** : Gérer des versions différentes de packages selon les projets

**Commandes essentielles pip** :

```bash
# Vérifier la version de pip
pip --version

# Mettre à jour pip lui-même
pip install --upgrade pip

# Installer un package
pip install requests

# Installer une version spécifique
pip install requests==2.31.0

# Installer plusieurs packages
pip install requests pyyaml python-dotenv

# Lister les packages installés
pip list

# Afficher les informations d'un package
pip show requests

# Désinstaller un package
pip uninstall requests

# Installer depuis requirements.txt
pip install -r requirements.txt

# Générer requirements.txt
pip freeze > requirements.txt
```

**Packages essentiels pour DevOps** :

```bash
# Client HTTP pour APIs
pip install requests

# Manipulation de fichiers YAML (configurations)
pip install pyyaml

# Gestion des variables d'environnement
pip install python-dotenv

# Framework pour créer des CLI
pip install click

# Automation et orchestration
pip install ansible

# Conteneurisation
pip install docker

# Orchestration Kubernetes
pip install kubernetes

# Tests automatisés
pip install pytest

# Qualité de code
pip install black flake8
```

**Bonnes pratiques pip en DevOps** :

```bash
# Toujours utiliser un environnement virtuel
source venv/bin/activate

# Épingler les versions dans requirements.txt
echo "requests==2.31.0" >> requirements.txt
echo "pyyaml==6.0.1" >> requirements.txt

# Séparer les dépendances par environnement
# requirements.txt (production)
# requirements-dev.txt (développement)
# requirements-test.txt (tests)

# Installer en mode développement
pip install -e .

# Utiliser pip-tools pour la gestion avancée
pip install pip-tools
pip-compile requirements.in
```

#### **Workflow DevOps complet**

```bash
# 1. Créer un nouveau projet DevOps
mkdir infrastructure-automation
cd infrastructure-automation

# 2. Définir la version Python avec pyenv
pyenv local 3.11.0

# 3. Créer l'environnement virtuel
python -m venv venv

# 4. Activer l'environnement
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

# 5. Mettre à jour pip
pip install --upgrade pip

# 6. Installer les dépendances DevOps
pip install requests pyyaml python-dotenv click
pip install ansible docker-py kubernetes

# 7. Créer le fichier requirements.txt
pip freeze > requirements.txt

# 8. Structure du projet
touch main.py
mkdir scripts tests docs
```

### 1.5 Bonnes pratiques environnements virtuels

#### **Nommage et organisation**

```bash
# Structure recommandée pour projets DevOps
projects/
├── monitoring-dashboard/
│   ├── venv/                 # Environnement virtuel
│   ├── requirements.txt      # Dépendances
│   ├── .python-version      # Version pyenv
│   └── src/                 # Code source
├── deployment-scripts/
│   ├── venv/
│   ├── requirements.txt
│   └── scripts/
└── infrastructure-as-code/
    ├── venv/
    ├── requirements.txt
    └── terraform/
```

#### **Gestion des dépendances**

```bash
# Créer requirements.txt avec versions exactes
pip freeze > requirements.txt

# Installer depuis requirements.txt
pip install -r requirements.txt

# Requirements.txt pour DevOps typique
cat > requirements.txt << EOF
requests==2.31.0
pyyaml==6.0.1
python-dotenv==1.0.0
click==8.1.7
ansible==8.5.0
docker==6.1.3
kubernetes==27.2.0
pytest==7.4.2
black==23.9.1
flake8==6.1.0
EOF
```

#### **Variables d'environnement et configuration**

```bash
# Fichier .env pour configuration
cat > .env << EOF
# Configuration DevOps
ENVIRONMENT=development
API_URL=https://api.monitoring.local
DATABASE_URL=postgresql://localhost:5432/devops
DOCKER_REGISTRY=registry.company.com
K8S_NAMESPACE=production
LOG_LEVEL=INFO
EOF

# Script d'activation personnalisé
cat > activate_project.sh << EOF
#!/bin/bash
# Activation environnement DevOps
source venv/bin/activate
export $(cat .env | xargs)
echo "Environnement DevOps activé pour: $(basename $(pwd))"
echo "Python: $(python --version)"
echo "Environment: $ENVIRONMENT"
EOF

chmod +x activate_project.sh
```

### 1.6 Test de l'environnement

**Script de vérification** :

```python
# test_environment.py
import sys
import subprocess
import os

def check_python_version():
    """Vérifier la version Python"""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    return version.major >= 3 and version.minor >= 9

def check_virtual_env():
    """Vérifier si on est dans un environnement virtuel"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    print(f"Environnement virtuel: {'Oui' if in_venv else 'Non'}")
    if in_venv:
        print(f"Chemin Python: {sys.executable}")
    return in_venv

def check_pyenv():
    """Vérifier pyenv"""
    try:
        result = subprocess.run(['pyenv', 'version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Pyenv: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    print("Pyenv: Non installé")
    return False

def check_packages():
    """Vérifier les packages essentiels"""
    essential_packages = ['requests', 'pyyaml', 'python-dotenv']
    for package in essential_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"{package} installé")
        except ImportError:
            print(f"{package} manquant")

if __name__ == "__main__":
    print("=== VÉRIFICATION ENVIRONNEMENT PYTHON DEVOPS ===")
    print()
    check_python_version()
    check_virtual_env()
    check_pyenv()
    print()
    print("=== PACKAGES ===")
    check_packages()
    print()
    print("Environnement prêt pour DevOps!")
```

**Exécution** :

```bash
python test_environment.py
```

## 2. Introduction et objectifs

### Pourquoi Python en DevOps ?

Python est devenu le langage de référence en DevOps pour plusieurs raisons fondamentales :

**Simplicité et lisibilité** : La syntaxe Python privilégie la clarté, ce qui facilite la maintenance des scripts d'automation et la collaboration en équipe.

**Écosystème riche** : Une vaste bibliothèque de modules spécialisés pour l'infrastructure (paramiko, fabric, ansible), les APIs (requests, flask), et l'automation (schedule, celery).

**Portabilité** : Python fonctionne de manière identique sur Linux, Windows et macOS, simplifiant le déploiement multi-plateforme.

**Communauté active** : Documentation abondante, support communautaire et intégration native dans la plupart des outils DevOps modernes.

### Applications DevOps typiques

- **Scripts d'automation** : Déploiement, configuration, monitoring
- **Orchestration** : Coordination de services et d'infrastructures
- **Traitement de données** : Analyse de logs, métriques, reporting
- **APIs et webhooks** : Intégration de services, notifications
- **Infrastructure as Code** : Génération de configurations, templates

### Environnement de développement

Pour cette formation, nous utiliserons :

- **Python 3.9+** : Version recommandée pour la compatibilité
- **pip** : Gestionnaire de packages intégré
- **venv** : Isolation des environnements de développement
- **VS Code** : Éditeur avec support Python avancé

## 3. Variables et types de données

### 2.1 Variables en Python

#### Définition formelle

**Variable Python** : Une variable en Python est un nom symbolique qui fait référence à un objet stocké en mémoire. Contrairement aux langages typés statiquement, Python utilise un typage dynamique où le type de la variable est déterminé à l'exécution selon l'objet référencé.

**Caractéristiques techniques :**

- **Référence d'objet** : La variable ne contient pas la valeur mais une référence vers l'objet
- **Typage dynamique** : Le type peut changer pendant l'exécution
- **Gestion automatique** : Allocation et libération mémoire automatiques (garbage collector)

**Syntaxe de base :**

```python
nom_variable = valeur
```

**Règles de nommage :**

- Commence par une lettre ou underscore
- Contient lettres, chiffres et underscores uniquement
- Sensible à la casse (myVar ≠ myvar)
- Éviter les mots-clés Python (if, for, def, etc.)

**Conventions DevOps :**

```python
# Style snake_case recommandé
server_name = "web-01"
max_connections = 100
is_production = True

# Variables d'environnement
DATABASE_URL = "postgresql://localhost:5432/app"
API_TOKEN = "abc123xyz"
```

### 2.2 Types de données fondamentaux

#### Définition formelle des types de données

**Type de données** : En informatique, un type de données définit la nature des valeurs qu'une variable peut contenir et les opérations autorisées sur ces valeurs. Python implémente un système de types orienté objet où chaque valeur est un objet d'une classe spécifique.

#### Hiérarchie des types Python

**Diagramme conceptuel des types de base :**

```
 object (classe mère)
 │
 ┌─────────┼─────────┬─────────┬─────────┐
 │ │ │ │ │
 int float str bool complex
 │ │ │ │ │
 (entiers) (décimaux) (texte) (booléens) (complexes)
```

**Classification par mutabilité :**

```
Types Python
├── IMMUTABLES (non modifiables)
│ ├── int, float, bool
│ ├── str (chaînes)
│ └── tuple
└── MUTABLES (modifiables)
 ├── list (listes)
 ├── dict (dictionnaires)
 └── set (ensembles)
```

#### 2.2.1 Types numériques

**Entiers (int) :**

```python
port = 8080
timeout = 30
retry_count = 3
```

**Nombres à virgule (float) :**

```python
cpu_usage = 85.7
response_time = 0.245
disk_usage_percent = 92.3
```

#### 2.2.2 Chaînes de caractères (str)

**Déclaration :**

```python
# Guillemets simples ou doubles
hostname = "web-server-01"
log_level = 'INFO'

# Chaînes multi-lignes
config_template = """
server {
 listen 80;
 server_name example.com;
}
"""
```

**Opérations utiles :**

```python
# Exemple simple 1 : Informations de base
server_name = "web-server-01"
print(len(server_name)) # 13 caractères
```

```python
# Exemple simple 2 : Transformations
server_name = "web-server-01"
print(server_name.upper()) # WEB-SERVER-01
print(server_name.replace("-", "_")) # web_server_01
```

```python
# Exemple simple 3 : Tests de contenu
server_name = "web-server-01"
print("web" in server_name) # True
print(server_name.startswith("web")) # True
```

#### 2.2.3 Booléens (bool)

```python
is_running = True
maintenance_mode = False
ssl_enabled = True

# Valeurs considérées comme False
empty_string = ""
zero_value = 0
empty_list = []
none_value = None
```

#### 2.2.4 Collections de base

**Listes (list) :**

```python
# Création
servers = ["web-01", "web-02", "db-01"]
ports = [80, 443, 3306]

# Accès par index (commence à 0)
first_server = servers[0] # "web-01"
last_server = servers[-1] # "db-01"

# Ajout d'éléments
servers.append("cache-01")
ports.extend([6379, 11211])

# Taille
server_count = len(servers)
```

**Dictionnaires (dict) :**

```python
# Configuration serveur
server_config = {
 "hostname": "web-01",
 "ip": "192.168.1.10",
 "port": 80,
 "ssl": True
}

# Accès aux valeurs
server_ip = server_config["ip"]
server_port = server_config.get("port", 80) # Valeur par défaut

# Modification
server_config["status"] = "running"
server_config.update({"cpu_cores": 4, "ram_gb": 16})
```

## 4. Opérateurs et expressions

### 3.1 Opérateurs arithmétiques

```python
# Opérations de base
memory_total = 16384 # MB
memory_used = 8192

memory_free = memory_total - memory_used
memory_usage_percent = (memory_used / memory_total) * 100

# Division
division_entiere = memory_used // 1024 # 8 (GB)
reste = memory_used % 1024 # 0

# Puissance
storage_bytes = 2 ** 30 # 1 GB en bytes
```

### 3.2 Opérateurs de comparaison

```python
cpu_usage = 85.5
threshold = 90

# Comparaisons
is_critical = cpu_usage > threshold # False
is_warning = cpu_usage >= 80 # True
is_normal = cpu_usage < 50 # False
is_exact = cpu_usage == 85.5 # True
is_different = cpu_usage != threshold # True
```

### 3.3 Opérateurs logiques

```python
disk_usage = 95
memory_usage = 75
cpu_usage = 40

# AND - toutes les conditions vraies
system_overloaded = disk_usage > 90 and memory_usage > 80 # False

# OR - au moins une condition vraie
needs_attention = disk_usage > 90 or memory_usage > 80 or cpu_usage > 90 # True

# NOT - négation
system_healthy = not (disk_usage > 95) # False
```

### 3.4 Opérateurs sur les chaînes

```python
service_name = "web"
environment = "production"

# Concaténation
full_name = service_name + "-" + environment # "web-production"

# Formatage moderne (f-strings)
server_id = f"{service_name}-{environment}-01" # "web-production-01"
log_message = f"Service {service_name} status: running on port {port}"

# Répétition
separator = "-" * 50 # "--------------------------------------------------"
```

### 4.5 Application pratique

**LAB 1** - Variables, types et opérateurs pour DevOps : `S1_S2_S3_lab1_variables_types.py`

**Énoncé du LAB 1** :

Objectif : Maîtriser les variables, types de données et opérateurs jusqu'aux opérateurs sur les chaînes
Contexte : Script de monitoring et gestion des serveurs de production

Instructions :

1. Définir les variables serveur avec différents types de données (str, int, float, bool)
2. Manipuler les types numériques et chaînes de caractères
3. Utiliser les opérateurs arithmétiques pour des calculs DevOps (pourcentages, conversions)
4. Appliquer les opérateurs sur les chaînes pour formater les données (concaténation, f-strings)
5. Créer un système de nommage et d'identification automatique
6. Générer un rapport de monitoring formaté et professionnel

Points : 5/30
Durée estimée : 25 minutes

## 5. Structures conditionnelles et boucles

### 5.1 Structures conditionnelles

#### 5.1.1 if, elif, else - Fondamentaux

**Syntaxe de base :**

```python
if condition:
    # Code à exécuter si condition vraie
elif autre_condition:
    # Code à exécuter si autre_condition vraie
else:
    # Code à exécuter si aucune condition vraie
```

**Exemple DevOps classique :**

```python
cpu_usage = 85

if cpu_usage > 90:
    status = "CRITICAL"
    action = "Scale up immediately"
elif cpu_usage > 75:
    status = "WARNING"
    action = "Monitor closely"
elif cpu_usage > 50:
    status = "OK"
    action = "Normal operation"
else:
    status = "IDLE"
    action = "Consider scaling down"

print(f"CPU Status: {status} - {action}")
```

#### 5.1.2 Cas spéciaux et pièges courants

**Piège 1 : Comparaison avec None**

```python
# INCORRECT - Peut causer des erreurs
server_response = get_server_status()  # Peut retourner None
if server_response == "OK":
    deploy_application()

# CORRECT - Vérifier None en premier
server_response = get_server_status()
if server_response is not None and server_response == "OK":
    deploy_application()
else:
    handle_server_error()
```

**Piège 2 : Valeurs "falsy" en Python**

```python
# Valeurs considérées comme False
server_list = []        # Liste vide
server_count = 0        # Zéro
server_name = ""        # Chaîne vide
connection = None       # None

# PIÈGE - Test ambigu
if server_count:
    print("Serveurs disponibles")
# Ne s'exécute pas si server_count = 0

# CORRECT - Test explicite
if server_count > 0:
    print(f"{server_count} serveurs disponibles")
else:
    print("Aucun serveur disponible")
```

**Piège 3 : Ordre des conditions**

```python
# INCORRECT - Ordre des conditions important
memory_usage = 95

if memory_usage > 80:
    level = "WARNING"    # Sera exécuté même si > 90
elif memory_usage > 90:
    level = "CRITICAL"   # Ne sera jamais atteint !

# CORRECT - Conditions du plus spécifique au général
if memory_usage > 90:
    level = "CRITICAL"
elif memory_usage > 80:
    level = "WARNING"
else:
    level = "OK"
```

#### 5.1.3 Conditions avancées pour DevOps

**Gestion des environnements multiples :**

```python
environment = "production"
cpu_usage = 85
memory_usage = 70

# Seuils différents selon l'environnement
if environment == "production":
    cpu_threshold = 80      # Plus strict en prod
    memory_threshold = 85
elif environment == "staging":
    cpu_threshold = 90      # Plus tolérant en staging
    memory_threshold = 90
else:  # development
    cpu_threshold = 95      # Très tolérant en dev
    memory_threshold = 95

# Application des seuils
if cpu_usage > cpu_threshold:
    alert_level = "CRITICAL"
    action = f"CPU critique en {environment}"
elif memory_usage > memory_threshold:
    alert_level = "WARNING"
    action = f"Memory élevée en {environment}"
else:
    alert_level = "OK"
    action = f"Système nominal en {environment}"
```

**Validation de configuration :**

```python
config = {
    "replicas": 3,
    "memory_limit": "512Mi",
    "cpu_limit": "500m",
    "environment": "production"
}

# Validation complexe avec conditions imbriquées
def validate_config(config):
    if not isinstance(config, dict):
        return False, "Configuration doit être un dictionnaire"

    if "replicas" not in config:
        return False, "Replicas manquant"

    replicas = config["replicas"]
    env = config.get("environment", "development")

    # Validation selon l'environnement
    if env == "production":
        if replicas < 2:
            return False, "Production nécessite au moins 2 replicas"
        if not config.get("memory_limit"):
            return False, "Memory limit obligatoire en production"
    elif env == "staging":
        if replicas < 1:
            return False, "Staging nécessite au moins 1 replica"

    return True, "Configuration valide"

# Utilisation
is_valid, message = validate_config(config)
if is_valid:
    print(f"{message}")
else:
    print(f"Erreur: {message}")
```

#### 5.1.4 Conditions imbriquées complexes

**Gestion de santé de service multi-niveaux :**

```python
service_status = "running"
port_open = True
response_code = 200
ssl_enabled = True
certificate_valid = True

def get_service_health():
    if service_status == "running":
        if port_open:
            if response_code == 200:
                if ssl_enabled:
                    if certificate_valid:
                        return "HEALTHY", "Service pleinement opérationnel"
                    else:
                        return "SSL_WARNING", "Certificat SSL invalide"
                else:
                    return "SSL_DISABLED", "SSL non activé"
            elif 400 <= response_code < 500:
                return "CLIENT_ERROR", f"Erreur client: {response_code}"
            elif response_code >= 500:
                return "SERVER_ERROR", f"Erreur serveur: {response_code}"
            else:
                return "UNKNOWN_RESPONSE", f"Code inattendu: {response_code}"
        else:
            return "PORT_CLOSED", "Port inaccessible"
    elif service_status == "stopped":
        return "SERVICE_DOWN", "Service arrêté"
    elif service_status == "starting":
        return "STARTING", "Service en cours de démarrage"
    else:
        return "UNKNOWN_STATUS", f"Statut inconnu: {service_status}"

health, message = get_service_health()
print(f"État: {health} - {message}")
```

#### 5.1.5 Opérateurs logiques avancés

**Conditions complexes avec AND, OR, NOT :**

```python
# Métriques système
cpu_usage = 85
memory_usage = 75
disk_usage = 90
network_errors = 5
uptime_hours = 168  # 7 jours

# Conditions combinées sophistiquées
system_overloaded = (
    (cpu_usage > 90 and memory_usage > 85) or
    (disk_usage > 95) or
    (network_errors > 10 and uptime_hours < 24)
)

system_degraded = (
    (cpu_usage > 75 or memory_usage > 80 or disk_usage > 85) and
    not system_overloaded  # Pas critique mais attention
)

system_healthy = not (system_overloaded or system_degraded)

# Logique de décision
if system_overloaded:
    priority = "P1"
    action = "Intervention immédiate"
    notification = "Alerte équipe astreinte"
elif system_degraded:
    priority = "P2"
    action = "Surveillance renforcée"
    notification = "Notification équipe technique"
elif system_healthy:
    priority = "P4"
    action = "Monitoring standard"
    notification = "Log normal"
else:
    priority = "P3"
    action = "Vérification manuelle"
    notification = "Escalade support"

print(f"Priorité: {priority}")
print(f"Action: {action}")
print(f"Notification: {notification}")
```

#### 5.1.6 Patterns DevOps avec conditions

**Pattern: Circuit Breaker**

```python
class ServiceCircuitBreaker:
    def __init__(self, failure_threshold=5, timeout_seconds=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call_service(self):
        current_time = time.time()

        if self.state == "OPEN":
            if self.last_failure_time and \
               (current_time - self.last_failure_time) > self.timeout_seconds:
                self.state = "HALF_OPEN"
                print("Circuit breaker: HALF_OPEN - Test de reconnexion")
            else:
                print("Circuit breaker: OPEN - Service indisponible")
                return None

        if self.state == "CLOSED" or self.state == "HALF_OPEN":
            try:
                # Simuler appel service
                response = call_external_service()

                if self.state == "HALF_OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    print("Circuit breaker: CLOSED - Service rétabli")

                return response

            except ServiceException:
                self.failure_count += 1
                self.last_failure_time = current_time

                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    print("Circuit breaker: OPEN - Trop d'échecs")

                return None
```

**Pattern: Feature Flags**

```python
def deploy_feature(user_id, feature_name, environment):
    # Configuration des feature flags
    feature_config = {
        "new_authentication": {
            "production": {"enabled": True, "rollout_percentage": 10},
            "staging": {"enabled": True, "rollout_percentage": 100},
            "development": {"enabled": True, "rollout_percentage": 100}
        },
        "experimental_ui": {
            "production": {"enabled": False, "rollout_percentage": 0},
            "staging": {"enabled": True, "rollout_percentage": 50},
            "development": {"enabled": True, "rollout_percentage": 100}
        }
    }

    if feature_name not in feature_config:
        return False, "Feature inconnue"

    env_config = feature_config[feature_name].get(environment)
    if not env_config:
        return False, f"Environment {environment} non configuré"

    if not env_config["enabled"]:
        return False, f"Feature désactivée en {environment}"

    # Calcul du rollout basé sur l'ID utilisateur
    user_hash = hash(str(user_id)) % 100
    rollout_percentage = env_config["rollout_percentage"]

    if user_hash < rollout_percentage:
        return True, f"Feature activée (rollout {rollout_percentage}%)"
    else:
        return False, f"Feature non activée pour cet utilisateur"

# Exemple d'utilisation
user_id = 12345
feature_enabled, message = deploy_feature(user_id, "new_authentication", "production")

if feature_enabled:
    print(f"{message}")
    # Utiliser la nouvelle feature
else:
    print(f"{message}")
    # Utiliser l'ancienne feature
```

### 5.2 Boucles

Les boucles sont un mécanisme fondamental de programmation permettant de répéter des instructions de manière contrôlée. En DevOps, elles sont essentielles pour l'automatisation de tâches répétitives comme le déploiement sur plusieurs serveurs, le monitoring cyclique, ou le traitement de collections de données.

#### 5.2.1 Boucles for : itération contrôlée

**Principe fondamental**

La boucle `for` en Python itère sur des séquences (listes, chaînes, dictionnaires) ou des objets itérables. Elle garantit un nombre fini d'itérations basé sur la taille de la collection.

**Syntaxe de base :**

```python
for element in sequence:
    # Instructions à répéter
    pass
```

**Exemples DevOps fondamentaux :**

```python
# Exemple 1 : Déploiement sur plusieurs serveurs
servers = ["web-01.prod", "web-02.prod", "web-03.prod"]

for server in servers:
    print(f"Déploiement sur {server}")
    # Logique de déploiement ici
    print(f"Déploiement terminé sur {server}")
```

```python
# Exemple 2 : Vérification de ports avec enumerate()
required_ports = [80, 443, 8080, 9090]

for index, port in enumerate(required_ports, 1):
    print(f"Port {index}/4: {port}")
    # Vérifier si le port est ouvert
    status = "ouvert" if port in [80, 443] else "fermé"
    print(f"  Statut: {status}")
```

**Itération avec range() pour automation :**

```python
# Exemple 3 : Retry automatique avec délai
import time

def deploy_with_retry(app_name, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        print(f"Tentative {attempt}/{max_attempts} - Déploiement {app_name}")

        # Simulation déploiement
        success = attempt == 2  # Réussit au 2ème essai

        if success:
            print(f"Déploiement réussi !")
            break
        else:
            print(f"Échec tentative {attempt}")
            if attempt < max_attempts:
                print("Attente avant nouvelle tentative...")
                time.sleep(2)
    else:
        print(f"Échec définitif après {max_attempts} tentatives")

# Usage
deploy_with_retry("api-service")
```

#### 5.2.2 Boucles for avec dictionnaires et structures complexes

**Parcours de configurations :**

```python
# Configuration infrastructure complète
infrastructure = {
    "web_servers": {
        "web-01": {"cpu": 4, "ram": 8, "status": "running"},
        "web-02": {"cpu": 4, "ram": 8, "status": "stopped"},
        "web-03": {"cpu": 8, "ram": 16, "status": "running"}
    },
    "databases": {
        "db-primary": {"cpu": 8, "ram": 32, "status": "running"},
        "db-replica": {"cpu": 8, "ram": 32, "status": "running"}
    }
}

# Exemple 1 : Audit complet de l'infrastructure
print("=== AUDIT INFRASTRUCTURE ===")
for category, servers in infrastructure.items():
    print(f"\nCatégorie: {category.upper()}")

    for server_name, config in servers.items():
        print(f"  {server_name}")
        print(f"    CPU: {config['cpu']} cores")
        print(f"    RAM: {config['ram']} GB")
        print(f"    Status: {config['status']}")
```

**Patterns avancés avec zip() :**

```python
# Exemple 2 : Synchronisation de configurations
production_servers = ["prod-web-01", "prod-web-02", "prod-db-01"]
staging_servers = ["staging-web-01", "staging-web-02", "staging-db-01"]
config_files = ["nginx.conf", "app.conf", "database.conf"]

print("=== SYNCHRONISATION CONFIGS ===")
for prod, staging, config in zip(production_servers, staging_servers, config_files):
    print(f"Sync {config}")
    print(f"  Source: {prod}")
    print(f"  Target: {staging}")
    print(f"  Action: copy_config({prod}, {staging}, '{config}')")
    print()
```

#### 5.2.3 Boucles while : monitoring et attente

**Principe et usage DevOps**

La boucle `while` continue tant qu'une condition est vraie. Particulièrement utile pour :

- Monitoring continu
- Attente de conditions
- Retry avec conditions dynamiques

**Exemples pratiques :**

```python
# Exemple 1 : Monitoring de service avec timeout
import time

def wait_for_service(service_name, timeout=60):
    """Attendre qu'un service soit disponible"""
    start_time = time.time()
    attempt = 0

    while time.time() - start_time < timeout:
        attempt += 1
    print(f"Vérification {service_name} (tentative {attempt})")

        # Simulation vérification service
        service_up = attempt >= 3  # Service up après 3 tentatives

        if service_up:
            elapsed = time.time() - start_time
            print(f"Service {service_name} disponible après {elapsed:.1f}s")
            return True

    print(f"Service non disponible, attente 5s...")
        time.sleep(5)

    print(f"Timeout: Service {service_name} non disponible après {timeout}s")
    return False

# Usage
wait_for_service("api-gateway", timeout=30)
```

**Monitoring continu avec conditions multiples :**

```python
# Exemple 2 : Monitoring système continu
def monitor_system():
    """Monitoring système avec conditions d'arrêt multiples"""
    monitoring = True
    consecutive_errors = 0
    max_errors = 3

    while monitoring and consecutive_errors < max_errors:
        # Simulation métriques système
        cpu_usage = 85  # Simulation
        memory_usage = 92
        disk_usage = 78

    print(f"CPU: {cpu_usage}% | RAM: {memory_usage}% | Disk: {disk_usage}%")

        # Logique d'alerte
        if cpu_usage > 90 or memory_usage > 95:
            consecutive_errors += 1
            print(f"Alerte système ! Erreur {consecutive_errors}/{max_errors}")

            if consecutive_errors >= max_errors:
                print("ALERTE CRITIQUE: Arrêt monitoring")
                break
        else:
            consecutive_errors = 0  # Reset compteur si tout va bien
            print("Système OK")

        # Condition d'arrêt externe (simulation)
        stop_monitoring = consecutive_errors >= 2  # Simulation
        monitoring = not stop_monitoring

        time.sleep(10)  # Attente avant prochaine vérification

# Usage (attention : boucle infinie sans condition d'arrêt)
# monitor_system()
```

#### 5.2.4 Contrôle de flux : break, continue, else

**break : interruption contrôlée**

```python
# Exemple 1 : Recherche de serveur disponible
available_servers = ["web-01", "web-02", "web-03", "web-04"]
target_server = None

for server in available_servers:
    print(f"Test connexion à {server}")

    # Simulation test connexion
    is_available = server in ["web-03", "web-04"]  # web-01 et web-02 down

    if is_available:
    print(f"Connexion réussie à {server}")
        target_server = server
        break  # Arrêt dès qu'un serveur est trouvé
    else:
    print(f"{server} non disponible")

if target_server:
    print(f"Serveur sélectionné: {target_server}")
else:
    print("Aucun serveur disponible")
```

**continue : saut d'itération**

```python
# Exemple 2 : Traitement sélectif de logs
log_entries = [
    {"level": "INFO", "message": "Application started", "service": "api"},
    {"level": "DEBUG", "message": "Cache hit", "service": "cache"},
    {"level": "ERROR", "message": "Database timeout", "service": "db"},
    {"level": "DEBUG", "message": "Request processed", "service": "api"},
    {"level": "WARN", "message": "High memory usage", "service": "worker"},
    {"level": "ERROR", "message": "Connection failed", "service": "external"}
]

print("=== LOGS CRITIQUES UNIQUEMENT ===")
for entry in log_entries:
    # Ignorer les logs de debug
    if entry["level"] == "DEBUG":
        continue

    # Traiter uniquement ERROR et WARN
    if entry["level"] in ["ERROR", "WARN"]:
        print(f"[{entry['service']}] {entry['message']}")
```

**else avec boucles : exécution si pas de break**

```python
# Exemple 3 : Validation complète avec else
def validate_all_configs(config_files):
    """Valider tous les fichiers de configuration"""
    print("Validation des configurations...")

    for config_file in config_files:
        print(f"  Validation: {config_file}")

        # Simulation validation
        is_valid = config_file != "broken.conf"  # broken.conf est invalide

        if not is_valid:
            print(f"Configuration invalide: {config_file}")
            break
    else:
        # Ce bloc s'exécute SEULEMENT si aucun break n'a eu lieu
    print("Toutes les configurations sont valides")
        return True

    print("Validation échouée")
    return False

# Test avec configs valides
valid_configs = ["nginx.conf", "app.conf", "database.conf"]
validate_all_configs(valid_configs)

print()

# Test avec config invalide
invalid_configs = ["nginx.conf", "broken.conf", "database.conf"]
validate_all_configs(invalid_configs)
```

#### 5.2.5 Pièges courants et bonnes pratiques

**Piège 1 : Modification de liste pendant l'itération**

```python
# INCORRECT : Modification pendant itération
servers = ["web-01", "web-02", "down-server", "web-03"]

# Ceci peut causer des comportements imprévisibles
for server in servers:
    if "down" in server:
    servers.remove(server)  # Dangereux !

# CORRECT : Créer une nouvelle liste
servers = ["web-01", "web-02", "down-server", "web-03"]
active_servers = []

for server in servers:
    if "down" not in server:
        active_servers.append(server)

print(f"Serveurs actifs: {active_servers}")
```

**Piège 2 : Boucles infinies non intentionnelles**

```python
# INCORRECT : Condition qui ne change jamais
def wait_for_deployment():
    status = "deploying"

    while status == "deploying":
        print("Attente fin déploiement...")
    # Oubli de mise à jour de status -> boucle infinie !
        time.sleep(5)

# CORRECT : Assurer que la condition change
def wait_for_deployment_safe():
    status = "deploying"
    attempts = 0
    max_attempts = 10

    while status == "deploying" and attempts < max_attempts:
        print(f"Attente fin déploiement... ({attempts + 1}/{max_attempts})")
        attempts += 1

        # Simulation changement de statut
        if attempts >= 5:
            status = "completed"

        time.sleep(1)

    return status == "completed"
```

**Piège 3 : Performance avec range() vs listes**

```python
# MOINS EFFICACE : Création de liste complète
large_numbers = list(range(1000000))
for num in large_numbers:
    if num > 10:
        break  # Gaspillage mémoire pour 999,990 éléments non utilisés

# PLUS EFFICACE : Générateur avec range()
for num in range(1000000):
    if num > 10:
        break  # Range génère à la demande
```

#### 5.2.6 Patterns DevOps avancés avec boucles

**Pattern 1 : Retry avec backoff exponentiel**

```python
import time
import random

def deploy_with_exponential_backoff(service_name, max_retries=5):
    """Déploiement avec retry et délai croissant"""
    base_delay = 1

    for attempt in range(max_retries):
    print(f"Déploiement {service_name} (tentative {attempt + 1}/{max_retries})")

        # Simulation déploiement (30% de chance de réussite)
        success = random.random() < 0.3

        if success:
            print(f"Déploiement réussi !")
            return True

        if attempt < max_retries - 1:  # Pas d'attente après la dernière tentative
            delay = base_delay * (2 ** attempt)  # Backoff exponentiel
            print(f"Échec. Attente {delay}s avant nouvelle tentative...")
            time.sleep(delay)

    print(f"Déploiement échoué après {max_retries} tentatives")
    return False

# Usage
deploy_with_exponential_backoff("user-service")
```

**Pattern 2 : Monitoring avec circuit breaker**

```python
class ServiceMonitor:
    def __init__(self, service_name, failure_threshold=3):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.failure_count = 0
        self.circuit_open = False

    def check_service(self):
        """Vérifier un service avec circuit breaker"""
        if self.circuit_open:
            print(f"Circuit ouvert pour {self.service_name}")
            return False

        # Simulation vérification service
        is_healthy = random.random() < 0.7  # 70% de chance d'être OK

        if is_healthy:
            self.failure_count = 0  # Reset compteur
            print(f"{self.service_name} OK")
            return True
        else:
            self.failure_count += 1
            print(f"{self.service_name} KO (échecs: {self.failure_count})")

            if self.failure_count >= self.failure_threshold:
                self.circuit_open = True
                print(f"Circuit ouvert pour {self.service_name}")

            return False

# Exemple d'utilisation
def monitor_services():
    monitors = [
        ServiceMonitor("api-gateway"),
        ServiceMonitor("user-service"),
        ServiceMonitor("payment-service")
    ]

    for cycle in range(10):  # 10 cycles de monitoring
    print(f"\n=== Cycle {cycle + 1} ===")

        for monitor in monitors:
            monitor.check_service()

        time.sleep(2)

# Usage (décommenté pour test)
# monitor_services()
```

**Pattern 3 : Traitement par batch avec limitation de ressources**

```python
def process_deployments_in_batches(deployments, batch_size=3, delay_between_batches=5):
    """Traiter des déploiements par lots pour éviter la surcharge"""
    total_deployments = len(deployments)

    # Diviser en batches
    for i in range(0, total_deployments, batch_size):
        batch = deployments[i:i + batch_size]
        batch_number = (i // batch_size) + 1
        total_batches = (total_deployments + batch_size - 1) // batch_size

    print(f"\nBatch {batch_number}/{total_batches}")
    print(f"Déploiements: {', '.join(batch)}")

        # Traiter le batch
        for deployment in batch:
            print(f"  Déploiement: {deployment}")
            time.sleep(1)  # Simulation temps de déploiement
            print(f"  Terminé: {deployment}")

        # Attente entre batches (sauf pour le dernier)
        if i + batch_size < total_deployments:
            print(f"Attente {delay_between_batches}s avant prochain batch...")
            time.sleep(delay_between_batches)

    print(f"\nTous les déploiements terminés !")

# Usage
all_deployments = [
    "frontend-v2.1", "api-gateway-v1.5", "user-service-v3.0",
    "payment-service-v2.0", "notification-v1.2", "analytics-v1.8",
    "auth-service-v2.2", "file-storage-v1.1"
]

process_deployments_in_batches(all_deployments, batch_size=3)
```

### 4.2 Boucles

#### 4.2.1 Boucle for avec listes

```python
servers = ["web-01", "web-02", "db-01", "cache-01"]

# Parcours simple
for server in servers:
 print(f"Checking server: {server}")

# Avec index
for index, server in enumerate(servers):
 print(f"Server {index + 1}: {server}")

# Filtrage pendant l'itération
web_servers = []
for server in servers:
 if "web" in server:
 web_servers.append(server)
```

#### 4.2.2 Boucle for avec dictionnaires

```python
server_config = {
 "hostname": "web-01",
 "ip": "192.168.1.10",
 "port": 80,
 "ssl": True
}

# Parcours des clés
for key in server_config:
 print(f"Config key: {key}")

# Parcours des valeurs
for value in server_config.values():
 print(f"Config value: {value}")

# Parcours des paires clé-valeur
for key, value in server_config.items():
 print(f"{key}: {value}")
```

### 5.3 Application pratique

**LAB 3** - Boucles avancées pour DevOps : `S1_S2_S3_lab3_boucles.py`

**Énoncé du LAB 3** :

Objectif : Maîtriser les boucles pour l'automatisation DevOps
Contexte : Automation de tâches répétitives sur infrastructure

**Couverture** : Section 5.2 - Boucles

- 5.2.1 Boucle for avec listes
- 5.2.2 Boucle for avec dictionnaires
- 5.2.3 Boucles while et contrôle de flux

Instructions :

1. Parcourir des listes de serveurs et appliquer des opérations
2. Itérer sur des configurations dans des dictionnaires
3. Utiliser enumerate() et zip() pour des traitements avancés
4. Implémenter des boucles while pour monitoring continu
5. Gérer break et continue pour contrôler les flux

Points : 5/30
Durée estimée : 20 minutes

### 5.4 Application pratique globale

**LAB 2** - Structures conditionnelles pour DevOps : `S1_S2_S3_lab2_conditionnelles.py`

**Énoncé du LAB 2** :

Objectif : Maîtriser les structures conditionnelles pour l'automatisation DevOps
Contexte : Système d'alertes et de prise de décision automatique

**Couverture** : Section 5.1 - Structures conditionnelles

- 5.1.1 if, elif, else
- 5.1.2 Conditions imbriquées
- 5.1.3 Opérateurs logiques dans conditions
- 5.1.4 Cas spéciaux et pièges

Instructions :

1. Créer un système d'alertes basé sur les métriques serveur avec conditions
2. Implémenter des niveaux d'alerte (OK, WARNING, CRITICAL) avec elif
3. Utiliser des conditions imbriquées pour des cas complexes
4. Appliquer des opérateurs logiques pour des conditions combinées
5. Gérer les cas spéciaux et éviter les pièges courants

Points : 5/30
Durée estimée : 20 minutes

## 6. Récapitulatif et prochaines étapes

### 6.1 Concepts clés maîtrisés

**Fondements théoriques :**

- **Variables et typage dynamique** : Références d'objets, règles de nommage
- **Types primitifs** : int, float, str, bool avec leurs caractéristiques
- **Collections** : list, dict avec manipulation avancée
- **Opérateurs** : Arithmétiques, comparaison, logiques, priorité
- **Structures de contrôle** : if/elif/else, for, while, break/continue

**Applications DevOps :**

- **Monitoring système** : Collecte et analyse de métriques
- **Configuration management** : Structures de données pour l'infrastructure
- **Alerting logic** : Systèmes de décision automatisée
- **Data processing** : Traitement et transformation de données

### 6.2 Bonnes pratiques DevOps

1. **Nommage explicite** : Variables et fonctions avec des noms clairs
2. **Commentaires utiles** : Expliquer la logique métier, pas l'évident
3. **Constantes en majuscules** : `MAX_RETRIES = 5`
4. **Validation des entrées** : Vérifier les valeurs avant traitement
5. **Gestion des erreurs** : Anticiper les cas d'échec

### 6.3 Préparation Séance 4

**Progression pédagogique :**

La **Séance 4 - Fonctions et Modules** s'appuiera directement sur ces fondamentaux pour :

1. **Modularisation du code** : Transformer les scripts en fonctions réutilisables
2. **Organisation avancée** : Structurer le code en modules et packages
3. **Réutilisabilité** : Créer une bibliothèque d'utilitaires DevOps
4. **Documentation** : Bonnes pratiques de documentation technique

**Prérequis validés pour Séance 4** :

- Maîtrise des variables et types
- Compréhension des structures de données

## 7. Ressources complémentaires

### 7.1 Documentation officielle

- [Python.org - Tutorial](https://docs.python.org/3/tutorial/)
- [Python.org - Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [PEP 8 - Style Guide](https://pep8.org/)

### 7.2 Outils de développement

- [Python.org - IDLE](https://docs.python.org/3/library/idle.html)
- [VS Code Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [PyCharm Community Edition](https://www.jetbrains.com/pycharm/)

### 7.3 Communauté et support

- [Stack Overflow - Python](https://stackoverflow.com/questions/tagged/python)
- [Real Python - Tutorials](https://realpython.com/)
- [Python Developer's Guide](https://devguide.python.org/)

### 7.4 DevOps et Python

- [Python for DevOps - O'Reilly](https://www.oreilly.com/library/view/python-for-devops/9781492057680/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/)
- [Python DevOps Toolkit](https://github.com/topics/python-devops)

_Formateur : Hassan ESSADIK | Sprint 1 - Semaine 2 - Séance 3_
