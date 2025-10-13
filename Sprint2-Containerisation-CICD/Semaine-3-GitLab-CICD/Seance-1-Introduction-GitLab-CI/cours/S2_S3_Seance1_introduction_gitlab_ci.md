# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 3 - Séance 1 : Introduction GitLab CI/CD

## Objectifs pédagogiques

- Comprendre les concepts fondamentaux de l'intégration et du déploiement continus
- Maîtriser la création et configuration des premiers pipelines GitLab CI/CD
- Intégrer les acquis Docker Compose dans des workflows automatisés
- Configurer les GitLab Runners et comprendre l'exécution des jobs

## Objectifs techniques

GitLab CI/CD, pipelines YAML, GitLab Runners, jobs et stages, artifacts, Docker intégration, variables d'environnement, triggers, scheduling

## Table des matières

1. [Introduction CI/CD et GitLab](#1-introduction-cicd-et-gitlab)
2. [Premier pipeline GitLab CI/CD](#2-premier-pipeline-gitlab-cicd)
3. [Jobs, stages et artifacts](#3-jobs-stages-et-artifacts)
4. [GitLab Runners et exécuteurs](#4-gitlab-runners-et-exécuteurs)
5. [Variables et secrets](#5-variables-et-secrets)
6. [Intégration Docker et rappels Compose](#6-intégration-docker-et-rappels-compose)
7. [Triggers et automatisation](#7-triggers-et-automatisation)
8. [Récapitulatif et prochaines étapes](#8-récapitulatif-et-prochaines-étapes)
9. [Ressources complémentaires](#9-ressources-complémentaires)

---

## 1. Introduction CI/CD et GitLab

### 1.1 Définitions et concepts

**Intégration Continue (CI)** : Pratique de développement où les développeurs intègrent leur code dans un dépôt partagé plusieurs fois par jour, chaque intégration étant vérifiée par un build automatisé.

**Déploiement Continu (CD)** : Extension de l'intégration continue qui automatise le déploiement des applications vers les environnements de production.

```mermaid
graph LR
    A[Code Commit] --> B[Build automatique]
    B --> C[Tests automatisés]
    C --> D[Déploiement staging]
    D --> E[Tests d'intégration]
    E --> F[Déploiement production]
```

### 1.2 GitLab CI/CD vs autres solutions

**Avantages GitLab CI/CD** :

- Intégration native avec GitLab (pas d'outil externe)
- Configuration as Code avec fichier `.gitlab-ci.yml`
- Runners flexibles (Docker, Kubernetes, Shell)
- Environments et review apps intégrés
- Registry Docker inclus

**Comparaison avec autres outils** :

- **Jenkins** : Plus complexe, nécessite maintenance serveur
- **GitHub Actions** : Limité à GitHub, moins flexible
- **Azure DevOps** : Écosystème Microsoft, moins universel
- **CircleCI** : Service externe, coûts selon usage

### 1.3 Architecture GitLab CI/CD

```mermaid
C4Context
    title Architecture GitLab CI/CD - Vue d'ensemble

    Person(dev, "Développeur", "Pousse le code vers GitLab")

    System_Boundary(gitlab, "GitLab Platform") {
        Container(repo, "Repository", "Git", "Code source + .gitlab-ci.yml")
        Container(ci, "CI/CD Engine", "GitLab CI", "Orchestrateur de pipelines")
        Container(registry, "Container Registry", "Docker", "Images Docker")
    }

    System_Boundary(runners, "GitLab Runners") {
        Container(runner1, "Runner Docker", "Docker", "Exécution en containers")
        Container(runner2, "Runner Shell", "Shell", "Exécution directe")
        Container(runner3, "Runner K8s", "Kubernetes", "Exécution pods")
    }

    System_Ext(deploy, "Environnements", "Staging/Production")

    Rel(dev, repo, "git push")
    Rel(repo, ci, "déclenche pipeline")
    Rel(ci, runner1, "exécute jobs")
    Rel(ci, runner2, "exécute jobs")
    Rel(ci, runner3, "exécute jobs")
    Rel(runner1, registry, "push images")
    Rel(runner1, deploy, "déploie")
```

**Composants principaux** :

#### **1. GitLab Instance (Plateforme centrale)**

La **GitLab Instance** est le cerveau de l'écosystème CI/CD. Elle peut être :

- **GitLab.com (SaaS)** : Service hébergé par GitLab Inc.

  - Avantages : Maintenance automatique, mise à jour continue
  - Limites : 2000 minutes CI/CD gratuites par mois
  - URL : `https://gitlab.com`

- **GitLab Self-hosted** : Instance privée sur vos serveurs
  - Avantages : Contrôle total, données privées
  - Responsabilités : Maintenance, sauvegardes, sécurité
  - Versions : Community Edition (CE) ou Enterprise Edition (EE)

```yaml
# Exemple configuration GitLab instance
# /etc/gitlab/gitlab.rb (self-hosted)
external_url 'https://gitlab.monentreprise.com'
gitlab_rails['gitlab_shell_ssh_port'] = 22
gitlab_rails['time_zone'] = 'Europe/Paris'
```

#### **2. Repository Git (Code source et configuration)**

Le **Repository** contient non seulement le code source mais aussi la définition des pipelines :

- **Code applicatif** : Sources, tests, documentation
- **Fichier .gitlab-ci.yml** : Configuration des pipelines CI/CD
- **Autres fichiers** : Dockerfile, docker-compose.yml, etc.

```bash
# Structure type d'un repository
mon-projet/
├── src/                    # Code source
├── tests/                  # Tests automatisés
├── .gitlab-ci.yml         # Configuration CI/CD
├── Dockerfile             # Image Docker
├── docker-compose.yml     # Orchestration locale
└── README.md              # Documentation
```

#### **3. CI/CD Engine (Orchestrateur intelligent)**

Le **CI/CD Engine** analyse le fichier `.gitlab-ci.yml` et orchestre l'exécution :

```mermaid
sequenceDiagram
    participant Dev as Développeur
    participant Repo as Repository
    participant Engine as CI/CD Engine
    participant Runner as GitLab Runner
    participant Deploy as Environment

    Dev->>Repo: git push
    Repo->>Engine: Webhook déclenché
    Engine->>Engine: Parse .gitlab-ci.yml
    Engine->>Runner: Alloue job "build"
    Runner->>Runner: Exécute script build
    Runner->>Engine: Résultat build
    Engine->>Runner: Alloue job "test"
    Runner->>Runner: Exécute tests
    Runner->>Engine: Résultat tests
    Engine->>Runner: Alloue job "deploy"
    Runner->>Deploy: Déploie application
    Deploy->>Engine: Confirmation déploiement
```

**Fonctionnalités du CI/CD Engine** :

- **Parsing YAML** : Validation et interprétation du fichier `.gitlab-ci.yml`
- **Planification** : Organisation séquentielle des stages et parallélisation des jobs
- **Allocation** : Distribution des jobs vers les runners disponibles
- **Monitoring** : Suivi en temps réel de l'exécution
- **Gestion d'état** : Persistence des artifacts entre jobs
- **Notifications** : Alertes en cas de succès/échec

#### **4. GitLab Runners (Agents d'exécution)**

Les **GitLab Runners** sont des agents autonomes qui exécutent les jobs :

```mermaid
graph TB
    subgraph "Types de Runners"
        A[Shared Runners] --> A1["GitLab.com<br/>Partagés entre projets"]
        B[Group Runners] --> B1["Niveau groupe<br/>Projets du groupe"]
        C[Project Runners] --> C1["Projet spécifique<br/>Contrôle total"]
    end

    subgraph "Déploiement Runners"
        D[Cloud] --> D1["AWS, GCP, Azure<br/>Auto-scaling"]
        E[On-Premise] --> E1["Serveurs internes<br/>Contrôle sécurité"]
        F[Docker] --> F1["Containers isolés<br/>Environments propres"]
    end

    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#e8f5e8
```

**Configuration d'un Runner personnalisé** :

```bash
# Installation sur Ubuntu/Debian
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner

# Enregistrement du runner
sudo gitlab-runner register \
  --url "https://gitlab.com/" \
  --registration-token "VOTRE_TOKEN_PROJET" \
  --description "docker-runner-production" \
  --executor "docker" \
  --docker-image "alpine:latest" \
  --docker-volumes "/var/run/docker.sock:/var/run/docker.sock"
```

#### **5. Executors (Environnements d'exécution)**

Les **Executors** définissent **comment** les jobs sont exécutés :

```mermaid
graph LR
    subgraph "Docker Executor"
        A[Image Docker] --> A1[Container isolé]
        A1 --> A2[Environment reproductible]
        A2 --> A3[Cleanup automatique]
    end

    subgraph "Shell Executor"
        B[Système hôte] --> B1[Accès direct OS]
        B1 --> B2[Performances natives]
        B2 --> B3[Persistence entre jobs]
    end

    subgraph "Kubernetes Executor"
        C[Pod K8s] --> C1[Isolation maximale]
        C1 --> C2[Auto-scaling]
        C2 --> C3[Resource limits]
    end

    style A fill:#e1f5fe
    style B fill:#f1f8e9
    style C fill:#fce4ec
```

**Exemple comparatif des executors** :

```yaml
# Docker Executor (Recommandé)
job_docker:
  image: node:18-alpine
  services:
    - postgres:13
    - redis:6
  script:
    - npm ci
    - npm test
    - npm run build

# Shell Executor
job_shell:
  tags:
    - shell-runner
  script:
    - source ~/.nvm/nvm.sh
    - nvm use 18
    - npm ci && npm test

# Kubernetes Executor
job_k8s:
  image: node:18-alpine
  tags:
    - kubernetes
  variables:
    KUBERNETES_MEMORY_LIMIT: '1Gi'
    KUBERNETES_CPU_LIMIT: '500m'
  script:
    - npm ci && npm test
```

#### **6. Container Registry (Stockage d'images)**

GitLab inclut un **Container Registry** intégré pour stocker les images Docker :

```bash
# Variables automatiques GitLab
$CI_REGISTRY          # registry.gitlab.com
$CI_REGISTRY_IMAGE    # registry.gitlab.com/groupe/projet
$CI_REGISTRY_USER     # gitlab-ci-token
$CI_REGISTRY_PASSWORD # Token automatique

# Exemple d'utilisation
docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

#### **7. Workflow complet d'exécution**

```mermaid
flowchart TD
    A[Developer: git push] --> B[GitLab Repo]
    B --> C{CI/CD Engine}
    C --> D[Parse .gitlab-ci.yml]
    D --> E[Create Pipeline]
    E --> F[Queue Jobs]

    F --> G[Runner 1: Build]
    F --> H[Runner 2: Test Unit]
    F --> I[Runner 3: Test Integration]

    G --> J[Store Artifacts]
    H --> J
    I --> J

    J --> K[Stage Deploy]
    K --> L[Runner 4: Deploy Staging]
    L --> M[Environment Ready]

    M --> N{Manual Approval?}
    N -->|Yes| O[Deploy Production]
    N -->|No| P[Auto Deploy]

    style C fill:#fff3e0
    style E fill:#e8f5e8
    style J fill:#e3f2fd
    style M fill:#f3e5f5
```

**Exemple pratique - Pipeline simple** :

```yaml
# .gitlab-ci.yml - Workflow complet
stages:
  - build
  - test
  - deploy

variables:
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

# Stage Build
build_app:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    # GitLab CI/CD Engine parse cette configuration
    - echo "Building application..."
    - docker build -t $IMAGE_NAME:$IMAGE_TAG .
    # Runner exécute ces commandes dans un container Docker
    - docker push $IMAGE_NAME:$IMAGE_TAG
  # Artifacts stockés par l'Engine pour le stage suivant
  artifacts:
    reports:
      dotenv: build.env

# Stage Test (parallèle)
test_unit:
  stage: test
  image: $IMAGE_NAME:$IMAGE_TAG
  script:
    - echo "Running unit tests..."
    - npm test

test_integration:
  stage: test
  image: $IMAGE_NAME:$IMAGE_TAG
  services:
    - postgres:13
  script:
    - echo "Running integration tests..."
    - npm run test:integration

# Stage Deploy
deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to staging..."
    - kubectl apply -f k8s/staging/
  environment:
    name: staging
    url: https://staging.monapp.com
  only:
    - main
```

### 1.4 Application pratique

---

## 2. Premier pipeline GitLab CI/CD

### 2.1 Structure fichier .gitlab-ci.yml

**Fichier de configuration basique** :

```yaml
# Fichier .gitlab-ci.yml à la racine du projet
# Définit les stages (étapes) du pipeline
stages:
  - build
  - test
  - deploy

# Variables globales
variables:
  NODE_VERSION: '18'
  APP_NAME: 'mon-app'

# Job de build
build_job:
  stage: build
  image: node:${NODE_VERSION}-alpine
  script:
    - echo "Installation des dépendances"
    - npm ci
    - echo "Build de l'application"
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

# Job de test
test_job:
  stage: test
  image: node:${NODE_VERSION}-alpine
  script:
    - echo "Exécution des tests"
    - npm ci
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'

# Job de déploiement
deploy_job:
  stage: deploy
  script:
    - echo "Déploiement de l'application"
    - cp -r dist/* /var/www/html/
  only:
    - main
```

### 2.2 Syntaxe YAML essentielle

**Éléments de base** :

```yaml
# Variables d'environnement
variables:
  DATABASE_URL: 'postgresql://localhost/myapp'
  CACHE_ENABLED: 'true'

# Image Docker par défaut
image: ubuntu:20.04

# Scripts exécutés avant tous les jobs
before_script:
  - apt-get update -qq
  - apt-get install -y git

# Job avec configuration avancée
mon_job:
  stage: test
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m pytest tests/
  after_script:
    - echo "Nettoyage post-job"
  only:
    - branches
  except:
    - main
  when: manual
  allow_failure: true
```

### 2.3 Pipeline d'exemple complet

**Configuration de base** :

```yaml
# Variables et image par défaut
stages:
  - prepare
  - build
  - test
  - deploy

variables:
  NODE_VERSION: '18'
  APP_NAME: 'mon-app'

image: node:${NODE_VERSION}-alpine
```

**Template réutilisable** :

```yaml
# Template pour jobs Node.js
.node_template: &node_config
  image: node:18-alpine
  before_script:
    - npm ci --cache .npm --prefer-offline
```

**Stage de préparation** :

```yaml
# Installation des dépendances
prepare:
  <<: *node_config
  stage: prepare
  script:
    - echo "Préparation de l'environnement"
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 day
```

**Stages de build parallèles** :

```yaml
# Build frontend
build_frontend:
  <<: *node_config
  stage: build
  script:
    - npm run build:frontend
  artifacts:
    paths:
      - frontend/dist/
    expire_in: 1 day

# Build backend
build_backend:
  <<: *node_config
  stage: build
  script:
    - npm run build:backend
  artifacts:
    paths:
      - backend/dist/
    expire_in: 1 day
```

**Tests automatisés** :

```yaml
# Tests unitaires
unit_tests:
  <<: *node_config
  stage: test
  script:
    - npm run test:unit
  artifacts:
    reports:
      junit: test-results.xml
      coverage: coverage/

# Tests d'intégration
integration_tests:
  <<: *node_config
  stage: test
  services:
    - postgres:13
  variables:
    POSTGRES_DB: testdb
  script:
    - npm run test:integration
```

**Déploiements conditionnels** :

```yaml
# Déploiement staging
deploy_staging:
  stage: deploy
  script:
    - echo "Déploiement vers staging"
    - rsync -avz dist/ staging:/var/www/
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Déploiement production (manuel)
deploy_production:
  stage: deploy
  script:
    - echo "Déploiement vers production"
    - rsync -avz dist/ production:/var/www/
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

### 2.3 Application pratique

📝 **LAB 1** - Découverte GitLab CI et premier pipeline : `S2_S3_S1_lab1_premier_pipeline`

**Énoncé du LAB 1** :
Créez votre premier pipeline GitLab CI/CD pour une application web simple avec build et test automatisés.

- **Objectif** : Comprendre la structure YAML et exécution des pipelines
- **Contexte** : Application Node.js avec tests Jest, déploiement sur GitLab Pages
- **Instructions** :
  1. Analyser la structure d'un projet existant
  2. Créer fichier `.gitlab-ci.yml` avec stages basiques
  3. Configurer jobs de build et test
  4. Observer l'exécution dans l'interface GitLab
- **Critères d'évaluation** : Pipeline fonctionnel, syntaxe YAML correcte, jobs exécutés (8 points)
- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S2_S3_S1_lab1_premier_pipeline`

---

## 3. Jobs, stages et artifacts

### 3.1 Concepts fondamentaux

#### **Définition des Jobs**

Un **Job** est l'unité atomique d'exécution dans GitLab CI/CD. Il représente une tâche spécifique qui s'exécute dans un environnement isolé.

**Caractéristiques d'un Job** :

- **Isolation** : Chaque job s'exécute indépendamment
- **Environnement** : Container Docker ou shell système
- **Script** : Séquence de commandes à exécuter
- **Résultat** : Succès (exit code 0) ou échec (exit code ≠ 0)

```mermaid
graph TB
    subgraph "Anatomie d'un Job"
        A[Job Definition] --> B[Environment Setup]
        B --> C[Script Execution]
        C --> D[Artifacts Collection]
        D --> E[Job Result]
    end

    subgraph "Job Lifecycle"
        F[Queued] --> G[Running]
        G --> H[Success]
        G --> I[Failed]
        G --> J[Canceled]
    end

    style A fill:#e3f2fd
    style C fill:#e8f5e8
    style D fill:#fff3e0
```

#### **Définition des Stages**

Un **Stage** (étape) est un regroupement logique de jobs qui s'exécutent selon des règles définies :

- **Exécution séquentielle** : Les stages s'exécutent dans l'ordre défini
- **Parallélisation interne** : Tous les jobs d'un même stage s'exécutent en parallèle
- **Dépendance** : Un stage ne démarre que si le précédent réussit

```mermaid
sequenceDiagram
    participant Pipeline as Pipeline
    participant Stage1 as Stage: Build
    participant Stage2 as Stage: Test
    participant Stage3 as Stage: Deploy

    Pipeline->>Stage1: Démarre stage build
    Stage1->>Stage1: Job1 + Job2 (parallèle)
    Stage1->>Pipeline: Tous jobs réussis

    Pipeline->>Stage2: Démarre stage test
    Stage2->>Stage2: Job3 + Job4 + Job5 (parallèle)
    Stage2->>Pipeline: Tous jobs réussis

    Pipeline->>Stage3: Démarre stage deploy
    Stage3->>Stage3: Job6 (séquentiel)
    Stage3->>Pipeline: Pipeline terminé
```

#### **Définition des Artifacts**

Les **Artifacts** sont des fichiers produits par un job et conservés pour utilisation ultérieure :

- **Persistance** : Fichiers sauvegardés entre jobs
- **Partage** : Transmission de données entre stages
- **Téléchargement** : Récupération manuelle possible
- **Expiration** : Durée de vie configurable

**Types d'Artifacts** :

- **Build artifacts** : Binaires compilés, bundles JS/CSS
- **Test reports** : Résultats de tests, couverture de code
- **Documentation** : Rapports générés, diagrammes
- **Deployment packages** : Archives de déploiement

### 3.2 Organisation stratégique des stages

```mermaid
flowchart TD
    subgraph "Pipeline Stratégique"
        A[prepare] --> B[validate]
        B --> C[build]
        C --> D[test]
        D --> E[security]
        E --> F[package]
        F --> G[deploy]
    end

    subgraph "Parallelisation par Stage"
        H[test_unit]
        I[test_integration]
        J[test_e2e]
        K[test_performance]
        L[lint_code]
        M[security_scan]
    end

    D --> H
    D --> I
    D --> J
    E --> K
    E --> L
    E --> M

    style A fill:#e1f5fe
    style C fill:#f3e5f5
    style D fill:#e8f5e8
    style E fill:#fff3e0
    style G fill:#ffebee
```

#### **Stratégie de nommage des stages**

**Progression logique recommandée** :

```yaml
stages:
  - prepare # Préparation environnement et dépendances
  - validate # Validation syntaxe, format, lint
  - build # Compilation, transpilation, bundling
  - test # Tests automatisés (unit, integration, e2e)
  - security # Analyses sécurité et vulnérabilités
  - package # Création artifacts finaux, images Docker
  - deploy # Déploiement environnements (staging, prod)
  - notify # Notifications et reporting final
```

#### **Principes de parallélisation**

**Jobs parallèles efficaces** :

```mermaid
gantt
    title Timeline d'exécution Pipeline
    dateFormat X
    axisFormat %M:%S

    section Build Stage
    Compile Frontend    :done, frontend, 0, 2m
    Compile Backend     :done, backend, 0, 3m
    Build Docker Image  :done, docker, 0, 4m

    section Test Stage
    Unit Tests          :active, unit, after frontend, 1m
    Integration Tests   :active, integration, after backend, 2m
    E2E Tests          :active, e2e, after docker, 5m
    Security Scan      :active, security, after docker, 3m

    section Deploy Stage
    Deploy Staging     :deploy, after e2e, 2m
```

**Exemple d'organisation optimisée** :

```yaml
# Stage TEST - Tous jobs en parallèle
test_unit:
  stage: test
  script: npm run test:unit
  # Rapide: 2-3 minutes

test_integration:
  stage: test
  script: npm run test:integration
  # Moyen: 5-8 minutes

test_e2e:
  stage: test
  script: npm run test:e2e
  # Long: 15-20 minutes

lint_javascript:
  stage: test
  script: npm run lint:js
  # Très rapide: 30 secondes

lint_css:
  stage: test
  script: npm run lint:css
  # Très rapide: 30 secondes
```

### 3.3 Gestion avancée des artifacts

```mermaid
sequenceDiagram
    participant Build as Build Job
    participant Storage as Artifact Storage
    participant Test as Test Job
    participant Deploy as Deploy Job
    participant User as Utilisateur

    Build->>Build: Compile application
    Build->>Storage: Upload dist/ + reports/
    Note over Storage: Stockage sécurisé<br/>avec métadonnées

    Storage->>Test: Download dist/ pour tests
    Test->>Test: Exécute tests sur build
    Test->>Storage: Upload test-results.xml

    Storage->>Deploy: Download dist/ pour déploiement
    Deploy->>Deploy: Déploie en production

    User->>Storage: Télécharge rapports
    Storage->>User: Fournit artifacts
```

#### **Configuration académique des artifacts**

**Structure recommandée** :

```yaml
build_application:
  stage: build
  script:
    - echo "Compilation de l'application"
    - npm run build
    - echo "Génération des rapports"
    - npm run generate:reports
  artifacts:
    # Chemins à conserver
    paths:
      - dist/ # Application buildée
      - reports/ # Rapports générés
      - docs/generated/ # Documentation
    # Rapports spéciaux GitLab
    reports:
      junit: reports/junit.xml # Tests unitaires
      coverage: reports/coverage.xml # Couverture code
      codequality: reports/quality.json # Qualité code
      performance: reports/perf.json # Performance
    # Métadonnées de gestion
    name: 'build-$CI_COMMIT_SHORT_SHA' # Nom unique
    expire_in: 1 week # Durée conservation
    when: always # Conserver même si échec
    # Exposition publique
    expose_as: 'Application Build' # Nom interface GitLab
```

#### **Bonnes pratiques artifacts**

**Optimisation du stockage** :

```yaml
# Artifacts conditionnels
test_job:
  script:
    - npm test
  artifacts:
    paths:
      - test-results/
    # Ne conserver QUE si tests réussissent
    when: on_success
    # Nettoyage automatique
    expire_in: 3 days

# Artifacts par environnement
.artifacts_template: &artifacts_config
  artifacts:
    paths:
      - dist/
    expire_in: 2 weeks

build_staging:
  <<: *artifacts_config
  script:
    - npm run build:staging

build_production:
  <<: *artifacts_config
  script:
    - npm run build:production
  artifacts:
    # Production : conservation plus longue
    expire_in: 1 month
```

### 3.4 Optimisation du cache intelligent

#### **Théorie du cache GitLab**

Le **cache** GitLab CI/CD permet de persister des fichiers entre pipelines pour accélérer l'exécution :

**Différence Cache vs Artifacts** :

| Aspect        | Cache                        | Artifacts                   |
| ------------- | ---------------------------- | --------------------------- |
| **Usage**     | Optimisation performance     | Partage de données          |
| **Scope**     | Entre pipelines              | Entre jobs du même pipeline |
| **Fiabilité** | Best effort (peut être vide) | Garanti                     |
| **Durée**     | Indéfinie (jusqu'à éviction) | Configurable (expire_in)    |

```mermaid
graph LR
    subgraph "Cache Strategy"
        A[node_modules/] --> B[Cache Hit]
        A --> C[Cache Miss]
        B --> D[npm ci rapide]
        C --> E[npm ci complet]
        E --> F[Populate Cache]
    end

    subgraph "Cache Scope"
        G[Per Branch] --> G1[feature/login]
        G --> G2[main]
        H[Global] --> H1[Shared across branches]
        I[Per Job] --> I1[Job-specific cache]
    end
```

#### **Configuration cache avancée**

```yaml
# Variables pour optimisation cache
variables:
  npm_config_cache: '$CI_PROJECT_DIR/.npm'
  CYPRESS_CACHE_FOLDER: '$CI_PROJECT_DIR/cache/Cypress'

# Cache global intelligent
cache:
  # Clé dynamique basée sur branche et fichiers
  key:
    files:
      - package-lock.json
      - composer.lock
    prefix: $CI_COMMIT_REF_SLUG
  paths:
    - node_modules/
    - vendor/
    - .npm/
    - cache/
  # Politique de cache
  policy: pull-push # pull (download), push (upload), pull-push (both)

# Cache spécialisé par job
test_frontend:
  cache:
    key: frontend-$CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
      - .npm/
    policy: pull # Seulement télécharger
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:frontend

build_assets:
  cache:
    key: assets-$CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
      - .npm/
    policy: pull-push # Télécharger et sauvegarder
  script:
    - npm ci --cache .npm
    - npm run build
```

### 3.2 Artifacts et cache

```mermaid
sequenceDiagram
    participant Dev as Développeur
    participant Repo as Repository
    participant Job1 as Job Build
    participant Job2 as Job Test
    participant Job3 as Job Deploy
    participant Cache as Cache System
    participant Artifacts as Artifacts Store

    Dev->>Repo: git push
    Repo->>Job1: Déclenche pipeline

    Job1->>Cache: Récupère node_modules/
    Job1->>Job1: npm ci && npm run build
    Job1->>Artifacts: Stocke dist/
    Job1->>Cache: Met à jour cache

    Artifacts->>Job2: Récupère dist/
    Job2->>Job2: npm test
    Job2->>Artifacts: Stocke test-results.xml

    Artifacts->>Job3: Récupère dist/
    Job3->>Job3: Déploie application
```

**Artifacts (résultats de build)** :

```yaml
build_app:
  stage: build
  script:
    - npm run build
  artifacts:
    # Fichiers à conserver
    paths:
      - dist/
      - reports/
    # Rapports de test
    reports:
      junit: test-results.xml
      coverage: coverage/lcov.info
    # Durée de conservation
    expire_in: 1 week
    # Quand conserver
    when: always # always, on_success, on_failure
```

**Cache (optimisation)** :

```yaml
# Cache global
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .npm/

# Cache spécifique par job
test_job:
  cache:
    key: test-${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull-push # pull, push, pull-push
```

### 3.3 Application pratique

📝 **LAB 2** - Configuration avancée jobs et artifacts : `S2_S3_S1_lab2_jobs_artifacts`

**Énoncé du LAB 2** :
Configurez un pipeline complexe avec stages optimisés, artifacts partagés et cache intelligent.

- **Objectif** : Maîtriser l'organisation des jobs et optimisation des performances
- **Contexte** : Application infrastructure avec frontend React et API Node.js
- **Instructions** :
  1. Organiser 6 stages avec jobs parallèles appropriés
  2. Configurer artifacts pour partage entre jobs
  3. Optimiser avec cache intelligent
  4. Ajouter rapports de tests et métriques
- **Critères d'évaluation** : Organisation logique, artifacts fonctionnels, optimisations cache (10 points)
- **Durée estimée** : 25 minutes
- **Fichier de travail** : `S2_S3_S1_lab2_jobs_artifacts`

---

## 4. GitLab Runners et exécuteurs

### 4.1 Concepts fondamentaux des Runners

#### **Définition académique**

Un **GitLab Runner** est un agent logiciel autonome responsable de l'exécution des jobs définis dans les pipelines CI/CD. Il fonctionne selon une architecture distribuée client-serveur.

**Architecture conceptuelle** :

```mermaid
C4Container
    title Architecture GitLab Runner - Vue détaillée

    Container_Boundary(gitlab, "GitLab Instance") {
        Container(coordinator, "Coordinator", "Go", "Orchestrateur central des jobs")
        Container(api, "API", "Ruby on Rails", "Interface de communication")
    }

    Container_Boundary(runner_system, "Runner System") {
        Container(runner_manager, "Runner Manager", "Go", "Gestionnaire principal")
        Container(executor, "Executor", "Multiple", "Environnement d'exécution")
        Container(cache_manager, "Cache Manager", "Go", "Gestion cache local")
    }

    Container_Boundary(execution_env, "Execution Environment") {
        Container(container, "Docker Container", "Docker", "Environnement isolé")
        Container(shell, "Shell Environment", "OS", "Système hôte")
        Container(k8s_pod, "Kubernetes Pod", "K8s", "Pod éphémère")
    }

    Rel(coordinator, runner_manager, "Polling jobs", "HTTP/JSON")
    Rel(runner_manager, executor, "Execute job")
    Rel(executor, container, "Spawn environment")
    Rel(executor, shell, "Direct execution")
    Rel(executor, k8s_pod, "Create pod")
    Rel(runner_manager, cache_manager, "Manage cache")
```

#### **Taxonomie des Runners**

**Classification par portée** :

```mermaid
graph TB
    subgraph "Hiérarchie GitLab Runners"
        A[Instance Runners] --> A1["Niveau GitLab<br/>Tous projets de l'instance"]
        B[Group Runners] --> B1["Niveau groupe<br/>Projets du groupe"]
        C[Project Runners] --> C1["Niveau projet<br/>Projet spécifique"]
    end

    subgraph "Niveau d'isolation"
        D[Shared] --> D1["Partagé<br/>Plusieurs projets"]
        E[Dedicated] --> E1["Dédié<br/>Usage exclusif"]
        F[Spot] --> F1["Temporaire<br/>Auto-scaling"]
    end

    subgraph "Modèle de coût"
        G[Free] --> G1["GitLab.com<br/>2000 min/mois"]
        H[Paid] --> H1["GitLab Premium<br/>10000 min/mois"]
        I[Self-hosted] --> I1["Infrastructure propre<br/>Coût matériel"]
    end

    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#e8f5e8
```

**Caractéristiques comparatives** :

| Type                 | Sécurité | Performance | Coût           | Maintenance | Usage recommandé    |
| -------------------- | -------- | ----------- | -------------- | ----------- | ------------------- |
| **Instance Runners** | Faible   | Variable    | Gratuit/Limité | Aucune      | Projets open-source |
| **Group Runners**    | Moyenne  | Bonne       | Modéré         | Partagée    | Équipes organisées  |
| **Project Runners**  | Élevée   | Optimale    | Élevé          | Complète    | Projets critiques   |

### 4.2 Exécuteurs - Environnements d'exécution

#### **Théorie des Executors**

Un **Executor** définit l'environnement technique dans lequel les scripts de job s'exécutent. Chaque executor offre des compromis différents entre isolation, performance et complexité.

```mermaid
graph TB
    subgraph "Executor Decision Matrix"
        A[Requirements Analysis] --> B{Isolation Level?}
        B -->|High| C[Docker/Kubernetes]
        B -->|Medium| D[VirtualBox/Parallels]
        B -->|Low| E[Shell/SSH]

        C --> F{Scalability?}
        F -->|High| G[Kubernetes Executor]
        F -->|Medium| H[Docker Executor]

        D --> I{OS Compatibility?}
        I -->|Multi-OS| J[VirtualBox Executor]

        E --> K{Performance?}
        K -->|Critical| L[Shell Executor]
        K -->|Remote| M[SSH Executor]
    end

    style G fill:#e1f5fe
    style H fill:#f1f8e9
    style L fill:#fce4ec
```

#### **Docker Executor (Recommandé)**

**Avantages académiques** :

- **Isolation hermétique** : Chaque job dans container séparé
- **Reproductibilité** : Même environnement sur tous runners
- **Flexibilité** : Images spécialisées par technologie
- **Nettoyage automatique** : Pas de pollution entre jobs

```mermaid
sequenceDiagram
    participant Runner as Runner Manager
    participant Docker as Docker Engine
    participant Registry as Container Registry
    participant Container as Job Container

    Runner->>Docker: Request container creation
    Docker->>Registry: Pull image (if not cached)
    Registry->>Docker: Image layers
    Docker->>Container: Create & start container
    Container->>Container: Execute job script
    Container->>Runner: Job results & artifacts
    Runner->>Docker: Destroy container
    Docker->>Docker: Cleanup resources
```

**Configuration académique** :

```toml
# /etc/gitlab-runner/config.toml
[[runners]]
  name = "docker-runner-production"
  url = "https://gitlab.com/"
  token = "REGISTRATION_TOKEN"
  executor = "docker"

  [runners.docker]
    # Image par défaut
    image = "alpine:latest"

    # Sécurité et isolation
    privileged = false
    security_opt = ["no-new-privileges:true"]

    # Ressources
    memory = "2g"
    cpus = "1.0"

    # Volumes et cache
    volumes = [
      "/cache",
      "/var/run/docker.sock:/var/run/docker.sock:ro"
    ]

    # Réseau
    network_mode = "bridge"

    # Services additionnels
    services_limit = 3

    # Optimisations
    pull_policy = "if-not-present"
    shm_size = 128000000  # 128MB shared memory
```

#### **Shell Executor**

**Cas d'usage légitimes** :

- **Accès système** : Commandes nécessitant privilèges root
- **Outils natifs** : Logiciels installés sur le système hôte
- **Performance critique** : Éviter overhead de containerisation
- **Intégration legacy** : Systèmes existants non-dockerisés

**Considérations sécuritaires** :

```mermaid
graph TD
    subgraph "Shell Executor Risks"
        A[Job Execution] --> B[Direct System Access]
        B --> C[File System Pollution]
        B --> D[Process Interference]
        B --> E[Security Vulnerabilities]

        C --> F[Cleanup Required]
        D --> G[Job Isolation Issues]
        E --> H[Privilege Escalation]
    end

    subgraph "Mitigation Strategies"
        I[Dedicated User] --> J[Limited Permissions]
        K[Sandboxing] --> L[chroot/namespaces]
        M[Monitoring] --> N[Audit Logs]
    end

    style E fill:#ffebee
    style H fill:#ffebee
```

#### **Kubernetes Executor**

**Paradigme Cloud-Native** :

```mermaid
graph TB
    subgraph "Kubernetes Executor Workflow"
        A[Job Request] --> B[Pod Template]
        B --> C[Resource Allocation]
        C --> D[Pod Creation]
        D --> E[Container Execution]
        E --> F[Artifacts Collection]
        F --> G[Pod Termination]
        G --> H[Resource Cleanup]
    end

    subgraph "K8s Features"
        I[Auto-scaling] --> I1[HPA based on load]
        J[Resource Limits] --> J1[CPU/Memory constraints]
        K[Network Policies] --> K1[Traffic isolation]
        L[Persistent Volumes] --> L1[Cache storage]
    end

    style D fill:#e8f5e8
    style G fill:#fff3e0
```

**Configuration Kubernetes avancée** :

```toml
[[runners]]
  name = "kubernetes-runner"
  url = "https://gitlab.com/"
  token = "TOKEN"
  executor = "kubernetes"

  [runners.kubernetes]
    # Connexion cluster
    host = "https://k8s-cluster.example.com"
    namespace = "gitlab-runner"

    # Resources par défaut
    cpu_limit = "1"
    memory_limit = "2Gi"
    service_cpu_limit = "500m"
    service_memory_limit = "1Gi"

    # Images
    image = "alpine:latest"
    helper_image = "gitlab/gitlab-runner-helper:x86_64-latest"

    # Volumes
    [[runners.kubernetes.volumes.pvc]]
      name = "cache-pvc"
      mount_path = "/cache"

    # Sécurité
    service_account = "gitlab-runner"
    pod_security_context.run_as_non_root = true
    pod_security_context.run_as_user = 1000
```

### 4.3 Installation et configuration professionnelle

#### **Installation sécurisée sur Ubuntu/Debian**

```bash
# Méthode officielle recommandée
# 1. Ajout du repository GitLab
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash

# 2. Installation du package
sudo apt-get update
sudo apt-get install gitlab-runner

# 3. Vérification de l'installation
gitlab-runner --version
sudo gitlab-runner status

# 4. Configuration utilisateur sécurisé
sudo usermod -aG docker gitlab-runner
sudo systemctl enable gitlab-runner
sudo systemctl start gitlab-runner
```

#### **Enregistrement sécurisé**

```bash
# Enregistrement interactif (recommandé)
sudo gitlab-runner register

# Enregistrement automatisé (CI/CD)
sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.com/" \
  --registration-token "$REGISTRATION_TOKEN" \
  --description "production-docker-runner" \
  --tag-list "docker,production,linux" \
  --executor "docker" \
  --docker-image "alpine:latest" \
  --docker-privileged=false \
  --docker-volumes "/cache" \
  --docker-network-mode "bridge"
```

#### **Sécurisation post-installation**

```bash
# Configuration firewall
sudo ufw allow from gitlab.com to any port 443
sudo ufw allow from gitlab.com to any port 80

# Limitation des ressources systemd
sudo mkdir -p /etc/systemd/system/gitlab-runner.service.d
cat <<EOF | sudo tee /etc/systemd/system/gitlab-runner.service.d/limits.conf
[Service]
LimitNOFILE=65536
LimitNPROC=4096
MemoryLimit=8G
CPUQuota=400%
EOF

sudo systemctl daemon-reload
sudo systemctl restart gitlab-runner
```

### 4.4 Monitoring et observabilité

#### **Métriques Runner essentielles**

```mermaid
graph LR
    subgraph "Runner Health Metrics"
        A[Job Success Rate] --> A1[>95% target]
        B[Queue Wait Time] --> B1[<5min average]
        C[Job Duration] --> C1[Trend analysis]
        D[Resource Usage] --> D1[CPU/Memory/Disk]
    end

    subgraph "Infrastructure Metrics"
        E[Runner Availability] --> E1[99.5% uptime]
        F[Cache Hit Rate] --> F1[>80% efficiency]
        G[Network Latency] --> G1[<100ms to GitLab]
        H[Docker Registry] --> H1[Pull success rate]
    end
```

**Configuration Prometheus monitoring** :

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'gitlab-runner'
    static_configs:
      - targets: ['localhost:9252']
    scrape_interval: 30s
    metrics_path: /metrics
```

```bash
# Activation métriques GitLab Runner
sudo gitlab-runner run \
  --listen-address "0.0.0.0:9252" \
  --metrics-server "0.0.0.0:9252"
```

## 5. Variables et secrets

### 5.1 Théorie des variables dans CI/CD

#### **Définition académique**

Les **variables d'environnement** dans GitLab CI/CD sont des paires clé-valeur qui permettent de configurer dynamiquement le comportement des jobs sans modifier le code. Elles constituent un mécanisme d'**injection de configuration** essentiel pour la **portabilité** et la **sécurité** des pipelines.

**Taxonomie des variables** :

```mermaid
graph TB
    subgraph "Classification des Variables"
        A[Variables GitLab CI/CD] --> B[Variables Prédéfinies]
        A --> C[Variables Personnalisées]
        A --> D[Variables de Fichier]

        B --> B1[Variables Système]
        B --> B2[Variables Pipeline]
        B --> B3[Variables Runner]

        C --> C1[Variables Projet]
        C --> C2[Variables Groupe]
        C --> C3[Variables Instance]

        D --> D1[Secrets]
        D --> D2[Certificats]
        D --> D3[Configurations]
    end

    subgraph "Portée et Visibilité"
        E[Global] --> E1[Tout le pipeline]
        F[Job] --> F1[Job spécifique]
        G[Stage] --> G1[Stage donné]
        H[Environment] --> H1[Environnement cible]
    end

    style B fill:#e3f2fd
    style C fill:#f3e5f5
    style D fill:#ffebee
```

#### **Hiérarchie de priorité**

GitLab CI/CD applique une **hiérarchie de résolution** des variables :

```mermaid
flowchart TD
    A[Variable Resolution Hierarchy] --> B[1. Job Variables]
    B --> C[2. Pipeline Variables]
    C --> D[3. Project Variables]
    D --> E[4. Group Variables]
    E --> F[5. Instance Variables]
    F --> G[6. Runner Variables]
    G --> H[7. Predefined Variables]

    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

### 5.2 Variables prédéfinies GitLab

#### **Variables système essentielles**

GitLab fournit automatiquement un ensemble riche de variables contextuelles :

```yaml
# Démonstration variables prédéfinies
print_variables:
  script:
    # Informations projet
    - echo "=== PROJET ==="
    - echo "Projet: $CI_PROJECT_NAME"
    - echo "Namespace: $CI_PROJECT_NAMESPACE"
    - echo "URL: $CI_PROJECT_URL"
    - echo "ID: $CI_PROJECT_ID"

    # Informations commit/branche
    - echo "=== CODE SOURCE ==="
    - echo "Branche: $CI_COMMIT_REF_NAME"
    - echo "Commit SHA: $CI_COMMIT_SHA"
    - echo "Commit court: $CI_COMMIT_SHORT_SHA"
    - echo "Message: $CI_COMMIT_MESSAGE"
    - echo "Auteur: $CI_COMMIT_AUTHOR"

    # Informations pipeline
    - echo "=== PIPELINE ==="
    - echo "Pipeline ID: $CI_PIPELINE_ID"
    - echo "Source: $CI_PIPELINE_SOURCE"
    - echo "URL: $CI_PIPELINE_URL"

    # Informations job
    - echo "=== JOB ==="
    - echo "Job: $CI_JOB_NAME"
    - echo "Stage: $CI_JOB_STAGE"
    - echo "ID: $CI_JOB_ID"
    - echo "URL: $CI_JOB_URL"
    - echo "Started: $CI_JOB_STARTED_AT"

    # Informations runner
    - echo "=== RUNNER ==="
    - echo "Runner: $CI_RUNNER_DESCRIPTION"
    - echo "Tags: $CI_RUNNER_TAGS"
    - echo "Executor: $CI_RUNNER_EXECUTOR"
```

#### **Variables conditionelles avancées**

```yaml
# Variables dynamiques basées sur contexte
dynamic_variables:
  variables:
    # Environnement basé sur branche
    DEPLOY_ENV: $([[ "$CI_COMMIT_REF_NAME" == "main" ]] && echo "production" || echo "staging")

    # Version basée sur tag ou commit
    APP_VERSION: ${CI_COMMIT_TAG:-$CI_COMMIT_SHORT_SHA}

    # URL d'API selon environnement
    API_URL: $([[ "$DEPLOY_ENV" == "production" ]] && echo "https://api.prod.com" || echo "https://api.staging.com")

  script:
    - echo "Déploiement vers $DEPLOY_ENV"
    - echo "Version: $APP_VERSION"
    - echo "API: $API_URL"
```

### 5.3 Gestion sécurisée des secrets

#### **Architecture de sécurité GitLab**

```mermaid
sequenceDiagram
    participant Dev as Développeur
    participant GitLab as GitLab Instance
    participant Runner as GitLab Runner
    participant Job as Job Container

    Dev->>GitLab: Configure secret variable
    Note over GitLab: Encrypted storage<br/>AES-256

    GitLab->>Runner: Job assignment
    GitLab->>Runner: Inject variables (encrypted)

    Runner->>Job: Start container
    Runner->>Job: Set environment variables
    Note over Job: Variables available<br/>in memory only

    Job->>Job: Execute script
    Note over Job: Logs masked<br/>if variable marked

    Job->>Runner: Job completion
    Runner->>GitLab: Results (no secrets)
```

#### **Types de variables sécurisées**

**Configuration interface GitLab** :

```mermaid
graph TB
    subgraph "GitLab Variable Settings"
        A[Settings → CI/CD → Variables] --> B[Add Variable]
        B --> C[Key/Value Definition]
        C --> D[Security Options]

        D --> E[Protected: Branch restrictions]
        D --> F[Masked: Hidden in logs]
        D --> G[Expanded: Variable substitution]
        D --> H[Environment: Scope limitation]
    end

    subgraph "Security Levels"
        I[Public] --> I1[Visible in logs]
        J[Masked] --> J1[Hidden with *** in logs]
        K[Protected] --> K1[Only protected branches]
        L[File] --> L1[Mounted as file]
    end

    style K fill:#e8f5e8
    style J fill:#fff3e0
    style L fill:#ffebee
```

#### **Bonnes pratiques secrets**

```yaml
# Job avec gestion sécurisée des secrets
secure_deployment:
  stage: deploy
  variables:
    # Variables publiques
    DEPLOY_ENV: 'production'
    APP_NAME: 'mon-application'

  script:
    # Vérification présence secrets requis
    - |
      if [ -z "$API_TOKEN" ]; then
        echo "ERREUR: API_TOKEN manquant"
        exit 1
      fi

      if [ -z "$DATABASE_PASSWORD" ]; then
        echo "ERREUR: DATABASE_PASSWORD manquant"
        exit 1
      fi

    # Utilisation sécurisée (éviter echo direct)
    - echo "Connexion API..."
    - curl -H "Authorization: Bearer $API_TOKEN" "$API_ENDPOINT/deploy"

    # Configuration base de données
    - echo "Configuration database..."
    - export DATABASE_URL="postgresql://user:$DATABASE_PASSWORD@db:5432/myapp"

    # Nettoyage variables sensibles
    - unset API_TOKEN
    - unset DATABASE_PASSWORD

  # Restriction aux branches protégées
  only:
    - main
    - /^release\/.*$/
```

### 5.4 Variables d'environnement et templates

#### **Stratégie multi-environnement**

```mermaid
graph LR
    subgraph "Environment Strategy"
        A[Code Repository] --> B[Pipeline Variables]
        B --> C{Branch Detection}

        C -->|main| D[Production Variables]
        C -->|develop| E[Staging Variables]
        C -->|feature/*| F[Development Variables]

        D --> G[Production Environment]
        E --> H[Staging Environment]
        F --> I[Dev Environment]
    end

    subgraph "Variable Inheritance"
        J[Global Variables] --> K[Group Variables]
        K --> L[Project Variables]
        L --> M[Pipeline Variables]
        M --> N[Job Variables]
    end
```

#### **Template réutilisable avec variables**

```yaml
# Template de déploiement réutilisable
.deploy_template: &deploy_config
  stage: deploy
  image: alpine:latest
  before_script:
    # Validation variables requises
    - |
      REQUIRED_VARS="DEPLOY_ENV APP_VERSION API_ENDPOINT"
      for var in $REQUIRED_VARS; do
        if [ -z "${!var}" ]; then
          echo "ERREUR: Variable $var requise"
          exit 1
        fi
      done

    # Configuration dynamique
    - echo "Préparation déploiement $APP_VERSION vers $DEPLOY_ENV"
    - apk add --no-cache curl jq

  script:
    # Script générique de déploiement
    - |
      echo "Déploiement vers $DEPLOY_ENV..."
      curl -X POST "$API_ENDPOINT/deploy" \
        -H "Authorization: Bearer $DEPLOY_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
          \"environment\": \"$DEPLOY_ENV\",
          \"version\": \"$APP_VERSION\",
          \"health_check\": \"$HEALTH_CHECK_URL\"
        }"

    # Vérification déploiement
    - |
      echo "Vérification santé application..."
      for i in {1..30}; do
        if curl -f "$HEALTH_CHECK_URL"; then
          echo "✓ Application déployée avec succès"
          exit 0
        fi
        echo "Tentative $i/30..."
        sleep 10
      done
      echo "✗ Échec vérification santé"
      exit 1

# Déploiement staging
deploy_staging:
  <<: *deploy_config
  variables:
    DEPLOY_ENV: 'staging'
    API_ENDPOINT: 'https://api.staging.monapp.com'
    HEALTH_CHECK_URL: 'https://staging.monapp.com/health'
  environment:
    name: staging
    url: https://staging.monapp.com
  only:
    - develop

# Déploiement production
deploy_production:
  <<: *deploy_config
  variables:
    DEPLOY_ENV: 'production'
    API_ENDPOINT: 'https://api.monapp.com'
    HEALTH_CHECK_URL: 'https://monapp.com/health'
  environment:
    name: production
    url: https://monapp.com
  when: manual
  only:
    - main

# Variables globales
variables:
  APP_VERSION: ${CI_COMMIT_TAG:-$CI_COMMIT_SHORT_SHA}
  DOCKER_REGISTRY: $CI_REGISTRY
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$APP_VERSION
```

### 5.5 Variables de fichier et montage sécurisé

#### **Concept des File Variables**

Les **variables de fichier** permettent de stocker des contenus volumineux ou binaires (certificats, clés, configurations) :

```mermaid
graph TB
    subgraph "File Variable Workflow"
        A[GitLab Variable] --> B[File Type Selection]
        B --> C[Content Upload]
        C --> D[Encrypted Storage]

        D --> E[Pipeline Execution]
        E --> F[Temporary File Creation]
        F --> G[Variable Points to Path]
        G --> H[Job Access File]
        H --> I[Automatic Cleanup]
    end

    style D fill:#ffebee
    style F fill:#e8f5e8
    style I fill:#fff3e0
```

#### **Utilisation pratique des variables de fichier**

```yaml
# Configuration avec certificats SSL
ssl_deployment:
  stage: deploy
  script:
    # SSL_CERT_FILE et SSL_KEY_FILE sont des variables de fichier
    # GitLab les monte automatiquement comme fichiers temporaires

    - echo "Configuration SSL..."
    - ls -la "$SSL_CERT_FILE" "$SSL_KEY_FILE"

    # Copie vers destination finale
    - cp "$SSL_CERT_FILE" /etc/ssl/certs/app.crt
    - cp "$SSL_KEY_FILE" /etc/ssl/private/app.key

    # Configuration serveur web
    - |
      cat > /etc/nginx/ssl.conf << EOF
      ssl_certificate /etc/ssl/certs/app.crt;
      ssl_certificate_key /etc/ssl/private/app.key;
      EOF

    # Vérification certificat
    - openssl x509 -in "$SSL_CERT_FILE" -text -noout

  # Configuration Docker avec montage volumes
  services:
    - nginx:alpine

# Configuration avec fichier JSON complexe
config_deployment:
  script:
    # APP_CONFIG_FILE contient une configuration JSON complexe
    - echo "Chargement configuration..."
    - cat "$APP_CONFIG_FILE" | jq '.'

    # Validation schema
    - jsonschema -i "$APP_CONFIG_FILE" config-schema.json

    # Déploiement avec configuration
    - kubectl create configmap app-config --from-file="$APP_CONFIG_FILE"
```

## 6. Intégration Docker et rappels Compose

### 6.1 Théorie de l'intégration Docker dans CI/CD

#### **Évolution conceptuelle**

La transition de **Docker Compose** (orchestration locale) vers **GitLab CI/CD** (orchestration distribuée) représente une évolution fondamentale dans la gestion des environnements de développement.

```mermaid
journey
    title Evolution des pratiques DevOps
    section Phase 1: Développement Local
      Docker run manuel         : 2: Dev
      Gestion manuelle des deps : 1: Dev
      Tests locaux seulement     : 2: Dev
    section Phase 2: Docker Compose
      Orchestration locale       : 4: Dev
      Environnements reproductibles : 4: Dev
      Workflows standardisés     : 3: Dev
    section Phase 3: GitLab CI/CD
      Automatisation complète    : 5: Pipeline
      Tests sur chaque commit    : 5: Pipeline
      Déploiement automatisé     : 5: Pipeline
      Monitoring intégré         : 4: Pipeline
```

#### **Paradigmes d'intégration Docker**

```mermaid
C4Container
    title Intégration Docker GitLab CI/CD - Architecture

    Container_Boundary(dev, "Environnement Développement") {
        Container(compose, "Docker Compose", "YAML", "Orchestration locale")
        Container(local_registry, "Registry Local", "Docker", "Cache images")
    }

    Container_Boundary(cicd, "GitLab CI/CD") {
        Container(pipeline, "Pipeline Engine", "GitLab", "Orchestrateur CI/CD")
        Container(docker_runner, "Docker Runner", "Docker", "Exécution jobs")
        Container(registry, "GitLab Registry", "Docker", "Images applicatives")
    }

    Container_Boundary(deploy, "Environnements Cibles") {
        Container(staging, "Staging", "Docker/K8s", "Tests intégration")
        Container(production, "Production", "Docker/K8s", "Applications live")
    }

    Rel(compose, pipeline, "Migration workflow")
    Rel(docker_runner, registry, "Push/Pull images")
    Rel(pipeline, staging, "Deploy automatique")
    Rel(pipeline, production, "Deploy contrôlé")
```

### 6.2 Migration Docker Compose vers GitLab CI

#### **Analyse comparative des approches**

**Docker Compose (Semaine 2)** - Orchestration locale :

```yaml
# docker-compose.yml (Semaine 2)
version: '3.8'
services:
  # Service web principal
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - '3000:3000'
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
      - redis
    volumes:
      - ./src:/app/src
      - node_modules:/app/node_modules

  # Base de données
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # Cache Redis
  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
  node_modules:
```

**GitLab CI/CD (Semaine 3)** - Orchestration distribuée :

```yaml
# .gitlab-ci.yml (Semaine 3)
stages:
  - build
  - test
  - package
  - deploy

variables:
  DOCKER_REGISTRY: $CI_REGISTRY
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  POSTGRES_DB: myapp_test
  POSTGRES_USER: testuser
  POSTGRES_PASSWORD: testpass

# Construction de l'image applicative
build_image:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  variables:
    DOCKER_BUILDKIT: 1
  script:
    # Build avec cache multi-stage
    - docker build
      --cache-from $IMAGE_NAME:latest
      --tag $IMAGE_NAME:$CI_COMMIT_SHA
      --tag $IMAGE_NAME:latest
      .
    # Push vers registry GitLab
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
    - docker push $IMAGE_NAME:latest

# Tests avec services similaires à Compose
test_integration:
  stage: test
  image: $IMAGE_NAME:$CI_COMMIT_SHA
  services:
    # Reproduction de l'environnement docker-compose
    - name: postgres:13
      alias: db
      variables:
        POSTGRES_DB: $POSTGRES_DB
        POSTGRES_USER: $POSTGRES_USER
        POSTGRES_PASSWORD: $POSTGRES_PASSWORD
    - name: redis:6-alpine
      alias: redis
  variables:
    DATABASE_URL: postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_DB
    REDIS_URL: redis://redis:6379
  script:
    # Attente des services (équivalent depends_on)
    - dockerize -wait tcp://db:5432 -wait tcp://redis:6379 -timeout 60s
    # Exécution des tests d'intégration
    - npm run test:integration
    - npm run test:e2e
```

#### **Stratégies de migration**

```mermaid
flowchart TD
    subgraph "Stratégie de Migration"
        A[Analyse docker-compose.yml] --> B[Identification Services]
        B --> C[Mapping vers GitLab CI]
        C --> D[Configuration Pipeline]

        D --> E[Phase 1: Build Images]
        E --> F[Phase 2: Services Tests]
        F --> G[Phase 3: Déploiement]
        G --> H[Phase 4: Monitoring]
    end

    subgraph "Éléments à Migrer"
        I[Services] --> I1[Images Docker]
        J[Volumes] --> J1[Artifacts/Cache]
        K[Networks] --> K1[Services GitLab]
        L[Environment] --> L1[Variables CI/CD]
    end

    style E fill:#e8f5e8
    style F fill:#fff3e0
    style G fill:#f3e5f5
```

### 6.3 Build et gestion d'images Docker

#### **Architecture de build multi-stage**

```dockerfile
# Dockerfile optimisé pour CI/CD
# Stage 1: Base de développement
FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=development
COPY . .

# Stage 2: Build de production
FROM development AS builder
ENV NODE_ENV=production
RUN npm run build
RUN npm prune --production

# Stage 3: Image finale optimisée
FROM node:18-alpine AS production
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
WORKDIR /app
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]
```

#### **Pipeline de build Docker avancé**

```yaml
# Configuration registry et cache
variables:
  DOCKER_REGISTRY: $CI_REGISTRY
  IMAGE_NAME: $CI_REGISTRY_IMAGE
  CACHE_IMAGE: $CI_REGISTRY_IMAGE/cache
  BUILDKIT_PROGRESS: plain
  DOCKER_BUILDKIT: 1

# Build avec cache intelligent
build_docker_advanced:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    # Connexion au registry GitLab
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY

    # Configuration BuildKit pour cache avancé
    - export DOCKER_CLI_EXPERIMENTAL=enabled
    - docker buildx create --use --driver docker-container

  script:
    # Build multi-plateforme avec cache
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --cache-from type=registry,ref=$CACHE_IMAGE:latest \
        --cache-to type=registry,ref=$CACHE_IMAGE:latest,mode=max \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        --build-arg NODE_ENV=production \
        --tag $IMAGE_NAME:$CI_COMMIT_SHA \
        --tag $IMAGE_NAME:latest \
        --push \
        .

    # Test de sécurité de l'image
    - docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
      aquasec/trivy:latest image --exit-code 1 --severity HIGH,CRITICAL \
      $IMAGE_NAME:$CI_COMMIT_SHA

  artifacts:
    reports:
      # Rapport de scan sécurité
      container_scanning: trivy-report.json
    expire_in: 1 week
```

### 6.4 Services et tests d'intégration

#### **Configuration services complexes**

```yaml
# Test avec stack complète (équivalent docker-compose)
test_full_stack:
  stage: test
  image: $IMAGE_NAME:$CI_COMMIT_SHA
  services:
    # Base de données principale
    - name: postgres:13
      alias: primary_db
      variables:
        POSTGRES_DB: myapp
        POSTGRES_USER: app_user
        POSTGRES_PASSWORD: secure_password

    # Base de données analytique
    - name: postgres:13
      alias: analytics_db
      variables:
        POSTGRES_DB: analytics
        POSTGRES_USER: analytics_user
        POSTGRES_PASSWORD: analytics_password

    # Cache Redis avec persistance
    - name: redis:6-alpine
      alias: cache
      command: ['redis-server', '--appendonly', 'yes']

    # Message broker RabbitMQ
    - name: rabbitmq:3-management-alpine
      alias: messagequeue
      variables:
        RABBITMQ_DEFAULT_USER: mquser
        RABBITMQ_DEFAULT_PASS: mqpassword

    # Service de search Elasticsearch
    - name: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
      alias: search
      variables:
        discovery.type: single-node
        ES_JAVA_OPTS: '-Xms512m -Xmx512m'

  variables:
    # Configuration services
    DATABASE_URL: postgresql://app_user:secure_password@primary_db:5432/myapp
    ANALYTICS_DB_URL: postgresql://analytics_user:analytics_password@analytics_db:5432/analytics
    REDIS_URL: redis://cache:6379
    RABBITMQ_URL: amqp://mquser:mqpassword@messagequeue:5672
    ELASTICSEARCH_URL: http://search:9200

    # Configuration application
    NODE_ENV: test
    LOG_LEVEL: debug

  before_script:
    # Attente de tous les services
    - apt-get update && apt-get install -y netcat-openbsd curl
    - |
      echo "Attente des services..."
      # PostgreSQL primaire
      while ! nc -z primary_db 5432; do sleep 1; done
      echo "✓ PostgreSQL primaire prêt"

      # PostgreSQL analytique  
      while ! nc -z analytics_db 5432; do sleep 1; done
      echo "✓ PostgreSQL analytique prêt"

      # Redis
      while ! nc -z cache 6379; do sleep 1; done
      echo "✓ Redis prêt"

      # RabbitMQ
      while ! nc -z messagequeue 5672; do sleep 1; done
      echo "✓ RabbitMQ prêt"

      # Elasticsearch
      while ! curl -s http://search:9200/_cluster/health; do sleep 1; done
      echo "✓ Elasticsearch prêt"

    # Initialisation des bases de données
    - npm run db:migrate
    - npm run db:seed:test

  script:
    # Suite complète de tests
    - echo "=== Tests unitaires ==="
    - npm run test:unit

    - echo "=== Tests d'intégration ==="
    - npm run test:integration

    - echo "=== Tests de performance ==="
    - npm run test:performance

    - echo "=== Tests end-to-end ==="
    - npm run test:e2e

  artifacts:
    reports:
      junit:
        - test-results/unit.xml
        - test-results/integration.xml
        - test-results/e2e.xml
      coverage: coverage/lcov.info
    paths:
      - coverage/
      - test-results/
      - screenshots/
    expire_in: 1 week
```

### 6.5 Déploiement avec Docker Compose

#### **Stratégie de déploiement hybride**

```yaml
# Déploiement utilisant Docker Compose pour orchestration
deploy_with_compose:
  stage: deploy
  image: docker/compose:1.29.2
  services:
    - docker:20.10.16-dind
  variables:
    IMAGE_TAG: $CI_COMMIT_SHA
    COMPOSE_PROJECT_NAME: $CI_PROJECT_NAME-$CI_ENVIRONMENT_SLUG

  before_script:
    # Génération docker-compose.prod.yml dynamique
    - |
      cat > docker-compose.prod.yml << EOF
      version: '3.8'
      services:
        web:
          image: $IMAGE_NAME:$IMAGE_TAG
          ports:
            - '80:3000'
          environment:
            - NODE_ENV=production
            - DATABASE_URL=\${DATABASE_URL}
            - REDIS_URL=\${REDIS_URL}
          depends_on:
            - db
            - redis
          restart: unless-stopped
          healthcheck:
            test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
            interval: 30s
            timeout: 10s
            retries: 3
            
        db:
          image: postgres:13
          environment:
            POSTGRES_DB: \${POSTGRES_DB}
            POSTGRES_USER: \${POSTGRES_USER}
            POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
          volumes:
            - postgres_data:/var/lib/postgresql/data
          restart: unless-stopped
          
        redis:
          image: redis:6-alpine
          command: redis-server --appendonly yes
          volumes:
            - redis_data:/data
          restart: unless-stopped
            
      volumes:
        postgres_data:
        redis_data:
      EOF

  script:
    # Déploiement avec Docker Compose
    - echo "Déploiement vers $CI_ENVIRONMENT_NAME..."
    - docker-compose -f docker-compose.prod.yml pull
    - docker-compose -f docker-compose.prod.yml up -d

    # Vérification santé des services
    - |
      echo "Vérification des services..."
      sleep 30

      # Test santé application
      for i in {1..10}; do
        if docker-compose -f docker-compose.prod.yml exec -T web curl -f http://localhost:3000/health; then
          echo "✓ Application healthy"
          break
        fi
        echo "Tentative $i/10..."
        sleep 10
      done

    # Nettoyage images anciennes
    - docker image prune -f

  environment:
    name: $CI_ENVIRONMENT_NAME
    url: http://$CI_ENVIRONMENT_SLUG.$KUBE_INGRESS_BASE_DOMAIN

  only:
    - main
    - develop
```

### 6.3 Application pratique

📝 **LAB 3** - Intégration Docker et migration Compose : `S2_S3_S1_lab3_docker_migration`

**Énoncé du LAB 3** :
Migrez une application Docker Compose vers un pipeline GitLab CI/CD avec build et déploiement automatisés.

- **Objectif** : Transformer setup Docker Compose en pipeline automatisé
- **Contexte** : Application microservices de la Semaine 2 (monitoring) avec frontend/backend/databases
- **Instructions** :
  1. Analyser docker-compose.yml existant de Semaine 2
  2. Créer pipeline GitLab avec build d'images
  3. Configurer services pour tests d'intégration
  4. Implémenter déploiement automatisé avec Compose
- **Critères d'évaluation** : Migration réussie, images buildées, déploiement fonctionnel (12 points)
- **Durée estimée** : 35 minutes
- **Fichier de travail** : `S2_S3_S1_lab3_docker_migration`

---

## 7. Triggers et automatisation

### 7.1 Théorie des déclencheurs de pipeline

#### **Définition académique**

Les **triggers** (déclencheurs) constituent le mécanisme fondamental qui détermine **quand** et **comment** les pipelines GitLab CI/CD s'exécutent. Ils implémentent une logique conditionnelle sophistiquée basée sur des **événements** et des **règles métier**.

**Classification des déclencheurs** :

```mermaid
graph TB
    subgraph "Types de Triggers"
        A[Event-Based Triggers] --> A1[Push Events]
        A --> A2[Merge Request Events]
        A --> A3[Tag Events]
        A --> A4[Schedule Events]

        B[Condition-Based Triggers] --> B1[Branch Patterns]
        B --> B2[File Changes]
        B --> B3[Variable Conditions]
        B --> B4[Manual Triggers]

        C[External Triggers] --> C1[API Triggers]
        C --> C2[Webhook Triggers]
        C --> C3[Pipeline Triggers]
        C --> C4[Chat Commands]
    end

    subgraph "Trigger Evaluation"
        D[Event Detection] --> E[Rule Processing]
        E --> F[Condition Matching]
        F --> G[Pipeline Execution]
    end

    style A1 fill:#e8f5e8
    style B1 fill:#fff3e0
    style C1 fill:#f3e5f5
```

#### **Workflow de déclenchement intelligent**

```mermaid
sequenceDiagram
    participant Dev as Développeur
    participant Git as Git Repository
    participant GitLab as GitLab Engine
    participant Rules as Rules Engine
    participant Pipeline as Pipeline Executor

    Dev->>Git: git push feature/auth
    Git->>GitLab: Webhook push event
    GitLab->>Rules: Évalue conditions

    Rules->>Rules: Check branch pattern
    Rules->>Rules: Check file changes
    Rules->>Rules: Check variables
    Rules->>Rules: Check schedule

    alt Conditions met
        Rules->>Pipeline: Create pipeline
        Pipeline->>Pipeline: Execute jobs
        Pipeline->>Dev: Notification résultat
    else Conditions not met
        Rules->>Dev: Pipeline skipped
    end
```

### 7.2 Déclencheurs basés sur les branches

#### **Stratégies Git Flow et CI/CD**

```mermaid
gitGraph
    commit id: "Initial"

    branch develop
    checkout develop
    commit id: "Feature base"

    branch feature/authentication
    checkout feature/authentication
    commit id: "Add login form"
    commit id: "Add validation"
    commit id: "Add tests"

    checkout develop
    merge feature/authentication
    commit id: "Merge auth feature"

    checkout main
    merge develop
    commit id: "Release v1.0.0"
    commit tag: "v1.0.0"

    branch hotfix/security
    checkout hotfix/security
    commit id: "Security patch"

    checkout main
    merge hotfix/security
    commit id: "Hotfix v1.0.1"
    commit tag: "v1.0.1"
```

#### **Configuration avancée des triggers branch**

```yaml
# Workflow global avec règles sophistiquées
workflow:
  rules:
    # Exécution sur toutes les branches sauf drafts
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
    # Exécution sur merge requests
    - if: $CI_MERGE_REQUEST_IID
    # Exécution sur tags
    - if: $CI_COMMIT_TAG

# Job avec règles conditionnelles complexes
build_feature:
  stage: build
  script:
    - echo "Build feature branch"
    - npm run build:development
  rules:
    # Feature branches uniquement
    - if: $CI_COMMIT_BRANCH =~ /^feature\//
      changes:
        - 'src/**/*'
        - 'package.json'
        - 'Dockerfile'

build_staging:
  stage: build
  script:
    - echo "Build staging"
    - npm run build:staging
  rules:
    # Branche develop uniquement
    - if: $CI_COMMIT_BRANCH == "develop"

build_production:
  stage: build
  script:
    - echo "Build production"
    - npm run build:production
  rules:
    # Branche main OU tags de release
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG =~ /^v[0-9]+\.[0-9]+\.[0-9]+$/

# Déploiement avec approvals
deploy_production:
  stage: deploy
  script:
    - echo "Déploiement production"
    - ./deploy.sh production
  environment:
    name: production
    url: https://monapp.com
  rules:
    # Production: uniquement main avec validation manuelle
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
      allow_failure: false
    # Ou tags avec déploiement automatique
    - if: $CI_COMMIT_TAG =~ /^v[0-9]+\.[0-9]+\.[0-9]+$/
      when: on_success
```

#### **Matrices de déclenchement**

```mermaid
stateDiagram-v2
    [*] --> EventDetection

    EventDetection --> BranchAnalysis: git push
    EventDetection --> MRAnalysis: merge request
    EventDetection --> TagAnalysis: tag push
    EventDetection --> ScheduleAnalysis: cron trigger

    BranchAnalysis --> FeaturePipeline: feature/*
    BranchAnalysis --> DevelopPipeline: develop
    BranchAnalysis --> MainPipeline: main
    BranchAnalysis --> HotfixPipeline: hotfix/*

    FeaturePipeline --> BuildTest: build + test only
    DevelopPipeline --> BuildTestDeploy: + deploy staging
    MainPipeline --> FullPipeline: + deploy production
    HotfixPipeline --> FastTrack: emergency deploy

    MRAnalysis --> ReviewPipeline: validation + review
    TagAnalysis --> ReleasePipeline: release deployment
    ScheduleAnalysis --> MaintenancePipeline: cleanup + reports

    BuildTest --> [*]
    BuildTestDeploy --> [*]
    FullPipeline --> [*]
    FastTrack --> [*]
    ReviewPipeline --> [*]
    ReleasePipeline --> [*]
    MaintenancePipeline --> [*]
```

### 7.3 Scheduled pipelines - Automatisation temporelle

#### **Théorie des pipelines programmés**

Les **scheduled pipelines** permettent d'exécuter des tâches de maintenance, monitoring et reporting de façon périodique, indépendamment des événements de code.

**Cas d'usage académiques** :

```mermaid
graph TB
    subgraph "Categories Scheduled Pipelines"
        A[Maintenance] --> A1[Cleanup Docker images]
        A --> A2[Database backups]
        A --> A3[Log rotation]

        B[Quality Assurance] --> B1[Nightly builds]
        B --> B2[Performance tests]
        B --> B3[Security scans]

        C[Monitoring] --> C1[Health checks]
        C --> C2[Dependency updates]
        C --> C3[License compliance]

        D[Reporting] --> D1[Usage statistics]
        D --> D2[Cost analysis]
        D --> D3[Compliance reports]
    end

    style A fill:#e8f5e8
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e3f2fd
```

#### **Configuration Cron expressions**

```yaml
# Pipeline de maintenance nocturne
nightly_maintenance:
  stage: maintenance
  image: alpine:latest
  script:
    - echo "=== MAINTENANCE NOCTURNE ==="
    - echo "Début: $(date)"

    # Nettoyage images Docker anciennes
    - docker system prune -af --filter "until=72h"

    # Backup base de données
    - pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
    - aws s3 cp backup_$(date +%Y%m%d).sql s3://backups/

    # Rotation des logs
    - find /var/log -name "*.log" -mtime +7 -delete

    # Rapport de santé système
    - ./scripts/health_report.sh

    - echo "Fin: $(date)"
  rules:
    # Exécution uniquement sur schedule
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        MAINTENANCE_TYPE: 'nightly'

# Tests de performance hebdomadaires
weekly_performance:
  stage: test
  image: loadtest/artillery:latest
  script:
    - echo "=== TESTS PERFORMANCE HEBDOMADAIRES ==="

    # Tests de charge
    - artillery run --target https://monapp.com performance/load-test.yml

    # Tests de stress
    - artillery run --target https://monapp.com performance/stress-test.yml

    # Analyse résultats
    - ./scripts/analyze_performance.sh

  artifacts:
    reports:
      performance: performance-report.json
    paths:
      - performance-results/
    expire_in: 4 weeks
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        SCHEDULE_TYPE: 'performance'

# Audit de sécurité mensuel
monthly_security_audit:
  stage: security
  image: aquasec/trivy:latest
  script:
    - echo "=== AUDIT SÉCURITÉ MENSUEL ==="

    # Scan de vulnérabilités
    - trivy filesystem --format json --output security-report.json .

    # Audit des dépendances
    - npm audit --json > npm-audit.json

    # Scan des secrets
    - truffleHog --regex --entropy=False .

    # Génération rapport consolidé
    - ./scripts/security_report.sh

  artifacts:
    reports:
      container_scanning: security-report.json
    paths:
      - security-audit/
    expire_in: 6 months
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables:
        SCHEDULE_TYPE: 'security'
```

### 7.4 Pipeline triggers - Orchestration inter-projets

#### **Architecture microservices et pipelines**

```mermaid
C4Container
    title Orchestration Pipelines Multi-Projets

    Container_Boundary(frontend, "Frontend Project") {
        Container(frontend_pipeline, "Frontend Pipeline", "GitLab CI", "Build React app")
    }

    Container_Boundary(backend, "Backend Project") {
        Container(api_pipeline, "API Pipeline", "GitLab CI", "Build Node.js API")
    }

    Container_Boundary(deployment, "Deployment Project") {
        Container(deploy_pipeline, "Deploy Pipeline", "GitLab CI", "Orchestration K8s")
        Container(e2e_pipeline, "E2E Pipeline", "GitLab CI", "Tests intégration")
    }

    Container_Boundary(monitoring, "Monitoring Project") {
        Container(monitor_pipeline, "Monitor Pipeline", "GitLab CI", "Dashboards & Alerts")
    }

    Rel(frontend_pipeline, deploy_pipeline, "Trigger deployment")
    Rel(api_pipeline, deploy_pipeline, "Trigger deployment")
    Rel(deploy_pipeline, e2e_pipeline, "Trigger E2E tests")
    Rel(deploy_pipeline, monitor_pipeline, "Update monitoring")
```

#### **Configuration triggers avancés**

```yaml
# Projet Frontend - Déclenche déploiement
trigger_deployment:
  stage: trigger
  image: alpine:latest
  script:
    - echo "Frontend build réussi, déclenchement déploiement"
  trigger:
    project: devops/deployment-orchestrator
    branch: main
    strategy: depend # Attend le résultat du pipeline déclenché
    variables:
      TRIGGER_SOURCE: 'frontend'
      FRONTEND_VERSION: $CI_COMMIT_SHA
      DEPLOY_ENV: 'staging'
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"
    - if: $CI_COMMIT_BRANCH == "main"
      variables:
        DEPLOY_ENV: 'production'

# Projet Backend - Trigger conditionnel
trigger_if_api_changed:
  stage: trigger
  variables:
    API_VERSION: $CI_COMMIT_SHA
  trigger:
    project: devops/deployment-orchestrator
    variables:
      TRIGGER_SOURCE: 'backend'
      API_VERSION: $API_VERSION
      DEPLOY_ENV: $DEPLOY_TARGET
  rules:
    # Seulement si l'API a changé
    - if: $CI_COMMIT_BRANCH =~ /^(main|develop)$/
      changes:
        - 'api/**/*'
        - 'src/controllers/**/*'
        - 'src/models/**/*'
        - 'package.json'

# Projet Deployment - Orchestrateur principal
deployment_orchestration:
  stage: deploy
  image: kubectl:latest
  variables:
    FRONTEND_IMAGE: $CI_REGISTRY/frontend:${FRONTEND_VERSION:-latest}
    BACKEND_IMAGE: $CI_REGISTRY/backend:${API_VERSION:-latest}
  script:
    - echo "=== ORCHESTRATION DÉPLOIEMENT ==="
    - echo "Source: $TRIGGER_SOURCE"
    - echo "Frontend: $FRONTEND_VERSION"
    - echo "Backend: $API_VERSION"
    - echo "Environment: $DEPLOY_ENV"

    # Mise à jour des manifests K8s
    - envsubst < k8s/frontend-deployment.yml | kubectl apply -f -
    - envsubst < k8s/backend-deployment.yml | kubectl apply -f -

    # Attente du déploiement
    - kubectl rollout status deployment/frontend-app
    - kubectl rollout status deployment/backend-api

    # Déclenchement tests E2E
    - |
      if [ "$DEPLOY_ENV" = "staging" ]; then
        echo "Déclenchement tests E2E"
      fi
  trigger:
    # Tests E2E post-déploiement
    project: qa/e2e-tests
    variables:
      TEST_ENV: $DEPLOY_ENV
      FRONTEND_URL: https://$DEPLOY_ENV.monapp.com
      API_URL: https://api-$DEPLOY_ENV.monapp.com
  environment:
    name: $DEPLOY_ENV
    url: https://$DEPLOY_ENV.monapp.com
```

### 7.5 Automatisation avancée et intelligence

#### **Pipelines adaptatifs**

```yaml
# Pipeline intelligent basé sur l'analyse des changements
smart_pipeline:
  stage: analyze
  image: alpine/git:latest
  script:
    # Analyse des fichiers modifiés
    - |
      echo "=== ANALYSE INTELLIGENTE ==="

      # Détection des changements
      if git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA | grep -q "^frontend/"; then
        echo "FRONTEND_CHANGED=true" >> smart.env
      fi

      if git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA | grep -q "^api/"; then
        echo "API_CHANGED=true" >> smart.env
      fi

      if git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA | grep -q "^database/"; then
        echo "DB_CHANGED=true" >> smart.env
      fi

      # Analyse impact
      CHANGED_LINES=$(git diff --numstat $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA | awk '{sum+=$1+$2} END {print sum}')
      if [ "$CHANGED_LINES" -gt 1000 ]; then
        echo "MAJOR_CHANGES=true" >> smart.env
        echo "EXTENDED_TESTS=true" >> smart.env
      fi

      # Configuration dynamique
      cat smart.env

  artifacts:
    reports:
      dotenv: smart.env

# Jobs conditionnels basés sur l'analyse
test_frontend:
  stage: test
  script:
    - npm run test:frontend
  rules:
    - if: $FRONTEND_CHANGED == "true"

test_api:
  stage: test
  script:
    - npm run test:api
  rules:
    - if: $API_CHANGED == "true"

migration_test:
  stage: test
  script:
    - npm run test:migration
  rules:
    - if: $DB_CHANGED == "true"

extended_test_suite:
  stage: test
  script:
    - npm run test:complete
    - npm run test:performance
    - npm run test:security
  rules:
    - if: $MAJOR_CHANGES == "true"
  timeout: 2h

# Auto-rollback en cas d'échec
auto_rollback:
  stage: rollback
  script:
    - echo "Échec détecté, rollback automatique"
    - kubectl rollout undo deployment/app
  rules:
    - if: $CI_PIPELINE_SOURCE == "pipeline"
      when: on_failure
  environment:
    name: production
    action: rollback
```

#### **Notifications et observabilité**

```yaml
# Notifications intelligentes
notification_pipeline:
  stage: notify
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    # Collecte des métriques pipeline
    - |
      PIPELINE_DURATION=$(($(date +%s) - $(date -d "$CI_PIPELINE_CREATED_AT" +%s)))
      PIPELINE_STATUS=$([ "$CI_PIPELINE_STATUS" = "success" ] && echo "Succès" || echo "Échec")

      # Calcul des métriques
      JOBS_TOTAL=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/pipelines/$CI_PIPELINE_ID/jobs" | jq length)

      JOBS_FAILED=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/pipelines/$CI_PIPELINE_ID/jobs" | \
        jq '[.[] | select(.status=="failed")] | length')

      # Notification Slack conditionnelle
      if [ "$CI_COMMIT_BRANCH" = "main" ] || [ "$JOBS_FAILED" -gt 0 ]; then
        curl -X POST -H 'Content-type: application/json' \
          --data "{
            \"text\": \"$PIPELINE_STATUS Pipeline $CI_PROJECT_NAME\",
            \"attachments\": [{
              \"color\": \"$([ "$CI_PIPELINE_STATUS" = "success" ] && echo "good" || echo "danger")\",
              \"fields\": [
                {\"title\": \"Branche\", \"value\": \"$CI_COMMIT_REF_NAME\", \"short\": true},
                {\"title\": \"Commit\", \"value\": \"$CI_COMMIT_SHORT_SHA\", \"short\": true},
                {\"title\": \"Durée\", \"value\": \"${PIPELINE_DURATION}s\", \"short\": true},
                {\"title\": \"Jobs échoués\", \"value\": \"$JOBS_FAILED/$JOBS_TOTAL\", \"short\": true}
              ],
              \"actions\": [{
                \"type\": \"button\",
                \"text\": \"Voir Pipeline\",
                \"url\": \"$CI_PIPELINE_URL\"
              }]
            }]
          }" \
          $SLACK_WEBHOOK_URL
      fi
  rules:
    - when: always
```

## 8. Récapitulatif et prochaines étapes

### 8.1 Concepts maîtrisés

- Architecture et principes CI/CD avec GitLab
- Création et configuration de pipelines YAML
- Jobs, stages, artifacts et optimisations cache
- GitLab Runners et différents exécuteurs
- Variables d'environnement et gestion des secrets
- Intégration Docker et migration depuis Compose
- Triggers et automatisation des déploiements

### 8.2 Transition Semaine 2 → Semaine 3

```mermaid
journey
    title Evolution DevOps: Docker Compose vers GitLab CI/CD
    section Semaine 2 - Docker Compose
      Orchestration locale    : 3: Développeur
      Déploiement manuel      : 2: Développeur
      Tests ponctuels         : 2: Développeur
      Configuration statique  : 3: Développeur
    section Transition
      Analyse besoins         : 4: DevOps
      Migration progressive   : 3: DevOps
      Formation équipe        : 4: DevOps
    section Semaine 3 - GitLab CI/CD
      Automatisation complète : 5: Pipeline
      Tests continus          : 5: Pipeline
      Déploiement automatisé  : 5: Pipeline
      Monitoring intégré      : 4: Pipeline
```

```mermaid
graph LR
    subgraph "Semaine 2: Docker Compose"
        A[docker-compose.yml] --> B[Orchestration Manuelle]
        B --> C[docker-compose up]
        C --> D[Tests Locaux]
    end

    subgraph "Migration"
        E[Analyse Infrastructure]
        F[Conversion Workflows]
    end

    subgraph "Semaine 3: GitLab CI/CD"
        G[.gitlab-ci.yml] --> H[Pipeline Automatisé]
        H --> I[Tests + Build + Deploy]
        I --> J[Déploiement Continu]
    end

    A --> E
    E --> F
    F --> G

    style A fill:#ffecb3
    style G fill:#c8e6c9
    style H fill:#e1f5fe
```

**Évolution des compétences** :

- De l'orchestration manuelle → automatisation CI/CD
- De docker-compose.yml → .gitlab-ci.yml
- De déploiements ponctuels → pipelines continus

### 8.3 Prochaines étapes

La **Séance 2** approfondira les **Pipelines Avancés** avec :

- Matrices de tests et parallélisation
- Cache distribué et optimisations
- Déploiements conditionnels et environments
- Review apps et monitoring

## 9. Ressources complémentaires

### 9.1 Documentation officielle

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab Runners Documentation](https://docs.gitlab.com/runner/)

### 9.2 Outils et intégrations

- Docker Hub et GitLab Container Registry
- Kubernetes pour déploiements avancés
- Prometheus/Grafana pour monitoring
- SonarQube pour qualité de code

### 9.3 Bonnes pratiques

- Pipeline as Code avec versioning
- Environments séparés (dev/staging/prod)
- Secrets management sécurisé
- Monitoring et observabilité
- Documentation des pipelines

---

_Formateur : Hassan ESSADIK | Sprint 2 - Semaine 3 - Séance 1_
