# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 3 : GitLab Fondamentaux et Collaboration

## Prérequis

- Connaissance de base de Git et des concepts de versioning
- Familiarité avec les interfaces web et les concepts DevOps
- Accès à un compte GitLab (gitlab.com ou instance locale)

## Objectifs pédagogiques

À l'issue de cette formation, l'apprenant sera capable de :

1. **Structurer** un projet GitLab avec la hiérarchie appropriée (Instance, Groups, Projects)
2. **Configurer** les permissions et rôles selon les besoins de l'équipe
3. **Mettre en œuvre** GitLab Flow comme workflow de développement collaboratif
4. **Sécuriser** les branches principales avec des règles de protection adaptées
5. **Organiser** la gestion de projet avec Issues, Labels et Milestones
6. **Déployer** des applications en utilisant les environnements GitLab

## Compétences techniques visées

- Gestion des utilisateurs et groupes GitLab
- Configuration des niveaux de permissions
- Mise en place de règles de protection des branches
- Implémentation des stratégies de merge request
- Maîtrise du GitLab Flow
- Organisation du travail collaboratif avec code reviews
- Gestion de projet intégrée
- Configuration des fonctionnalités de sécurité
- Gestion des environnements de déploiement
- Utilisation de GitLab Pages

## Plan de formation

### Progression pédagogique

La formation suit une approche **progressive** et **pratique** structurée en 5 modules :

**Module 1 : Fondamentaux GitLab** (45 minutes)

- Théorie : Structure organisationnelle et concepts de base
- Pratique : Configuration d'une organisation GitLab
- Évaluation : Exercice de mise en place d'équipe

**Module 2 : Collaboration Git Avancée** (60 minutes)

- Théorie : Workflows Git et stratégies de collaboration
- Pratique : Implémentation GitLab Flow
- Évaluation : Simulation de workflow collaboratif

**Module 3 : Protection et Sécurité** (50 minutes)

- Théorie : Sécurisation des projets et contrôles d'accès
- Pratique : Configuration de la protection des branches
- Évaluation : Audit de sécurité d'un projet

**Module 4 : Project Management** (45 minutes)

- Théorie : Gestion de projet intégrée
- Pratique : Organisation d'un backlog avec Issues et Milestones
- Évaluation : Planification de sprint

**Module 5 : Environnements et Déploiements** (40 minutes)

- Théorie : Gestion des environnements de déploiement
- Pratique : Configuration d'environnements et Review Apps
- Évaluation : Mise en place d'un pipeline de déploiement

**Durée totale** : 4h avec pauses et exercices pratiques

### Méthode pédagogique

- **Apprentissage actif** : Alternance théorie/pratique (30/70)
- **Learning by doing** : Manipulation directe de GitLab
- **Projet fil rouge** : Configuration complète d'un projet collaboratif
- **Validation continue** : Quiz et exercices pratiques

## Table des matières

1. [Module 1 : Fondamentaux GitLab](#module-1--fondamentaux-gitlab)
2. [Module 2 : Collaboration Git Avancée](#module-2--collaboration-git-avancée)
3. [Module 3 : Protection et Sécurité](#module-3--protection-et-sécurité)
4. [Module 4 : Project Management](#module-4--project-management)
5. [Module 5 : Environnements et Déploiements](#module-5--environnements-et-déploiements)
6. [Synthèse et évaluation finale](#synthèse-et-évaluation-finale)

---

## Module 1 : Fondamentaux GitLab

### Objectifs du module

- Comprendre l'architecture GitLab et ses composants
- Distinguer les différents niveaux hiérarchiques
- Maîtriser le système de permissions
- Configurer une organisation GitLab complète

### 1.1 Structure organisationnelle GitLab

#### Concepts fondamentaux

GitLab utilise une structure hiérarchique à 4 niveaux pour organiser les projets et utilisateurs :

```mermaid
graph TB
    subgraph "GitLab Instance"
        A[GitLab Instance] --> B[Group Level 1]
        A --> C[Group Level 1]
        A --> D[User Namespace]

        B --> E[Subgroup Level 2]
        B --> F[Project A]
        B --> G[Project B]

        E --> H[Project C]
        E --> I[Project D]

        C --> J[Project E]

        D --> K[Personal Project]
    end

    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style E fill:#fff3e0
    style F fill:#e8f5e8
```

**Définitions et concepts** :

1. **GitLab Instance** : Installation complète de GitLab (gitlab.com ou self-hosted)
2. **Group** : Collection de projets et d'utilisateurs avec permissions partagées
3. **Subgroup** : Groupe imbriqué permettant une organisation hiérarchique
4. **Project** : Repository Git individuel avec ses propres paramètres
5. **User Namespace** : Espace personnel de l'utilisateur pour ses projets

#### Namespaces et organisation

**Le concept de Namespace**

Un namespace est un identifiant unique qui structure l'URL d'accès aux projets GitLab.

**Format standardisé** :

```
https://gitlab.com/[namespace]/[project-name]
```

**Exemples d'organisation** :

```
Projets personnels :
https://gitlab.com/john.doe/mon-projet-perso

Projets d'entreprise :
https://gitlab.com/mon-entreprise/site-web
https://gitlab.com/mon-entreprise/api-backend

Organisation par équipe :
https://gitlab.com/entreprise/equipe-frontend/app-react
https://gitlab.com/entreprise/equipe-backend/microservice-auth
```

#### Niveaux de visibilité

GitLab propose 3 niveaux de visibilité pour contrôler l'accès aux projets :

```mermaid
graph LR
    subgraph "Visibility Levels"
        A[Private] --> A1["Membres seulement<br/>Accès restreint<br/>Projets sensibles"]
        B[Internal] --> B1["Instance seulement<br/>Utilisateurs connectés<br/>Projets internes"]
        C[Public] --> C1["Tout le monde<br/>Lecture publique<br/>Open source"]
    end

    style A fill:#ffebee
    style B fill:#fff3e0
    style C fill:#e8f5e8
```

**Critères de choix** :

- **Private** : Projets confidentiels, code propriétaire, données sensibles
- **Internal** : Projets d'entreprise, collaboration interne, documentation
- **Public** : Projets open source, portfolios, démonstrations

### 1.2 Gestion des utilisateurs et rôles

#### Types d'utilisateurs GitLab

GitLab distingue plusieurs catégories d'utilisateurs selon leur fonction :

```mermaid
graph TB
    subgraph "User Types"
        A[Regular User] --> A1["Utilisateur standard<br/>Développeur/Contributor<br/>Accès selon permissions"]

        B[Admin User] --> B1["Super utilisateur<br/>Configuration instance<br/>Gestion utilisateurs"]

        C[Service Account] --> C1["Compte automatisé<br/>Intégrations API<br/>Scripts/Automation"]

        D[External User] --> D1["Utilisateur externe<br/>Accès limité<br/>Partenaires/Clients"]
    end

    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

#### Système de permissions GitLab

GitLab utilise un système de rôles numérotés avec des permissions croissantes.

**Hiérarchie des rôles** :

````mermaid
graph LR
    subgraph "Permission Hierarchy"
        A["Guest (10)"] --> B["Reporter (20)"]
        B --> C["Developer (30)"]
        C --> D["Maintainer (40)"]
        D --> E["Owner (50)"]
    end

    subgraph "Progression des droits"
        F[Lecture seule] --> G[Création contenu]
        G --> H[Modification code]
        H --> I[Administration projet]
        I --> J[Contrôle total]
    end

    style A fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#e3f2fd
```#### Matrice des permissions détaillée

La matrice suivante présente les permissions spécifiques à chaque rôle :

| Permission                   | Guest | Reporter | Developer | Maintainer | Owner |
| ---------------------------- | ----- | -------- | --------- | ---------- | ----- |
| **Repository**               |
| Clone repository             | Oui   | Oui      | Oui       | Oui        | Oui   |
| Pull code                    | Oui   | Oui      | Oui       | Oui        | Oui   |
| Download artifacts           | Oui   | Oui      | Oui       | Oui        | Oui   |
| Push to non-protected branch | Non   | Non      | Oui       | Oui        | Oui   |
| Push to protected branch     | Non   | Non      | Non       | Oui        | Oui   |
| Remove non-protected branch  | Non   | Non      | Oui       | Oui        | Oui   |
| **Issues & Merge Requests**  |
| View issues/MR               | Oui   | Oui      | Oui       | Oui        | Oui   |
| Create issues/MR             | Oui   | Oui      | Oui       | Oui        | Oui   |
| Comment on issues/MR         | Oui   | Oui      | Oui       | Oui        | Oui   |
| Close/reopen issues/MR       | Non   | Oui      | Oui       | Oui        | Oui   |
| Assign issues/MR             | Non   | Oui      | Oui       | Oui        | Oui   |
| Manage labels/milestones     | Non   | Non      | Oui       | Oui        | Oui   |
| **CI/CD**                    |
| View pipelines               | Oui   | Oui      | Oui       | Oui        | Oui   |
| Run pipelines                | Non   | Non      | Oui       | Oui        | Oui   |
| Manage CI/CD variables       | Non   | Non      | Non       | Oui        | Oui   |
| Manage runners               | Non   | Non      | Non       | Oui        | Oui   |
| **Administration**           |
| Manage project settings      | Non   | Non      | Non       | Oui        | Oui   |
| Manage team members          | Non   | Non      | Non       | Oui        | Oui   |
| Delete project               | Non   | Non      | Non       | Non        | Oui   |

**Points clés à retenir** :
- La progression des rôles suit une logique métier claire
- Chaque niveau hérite des permissions du niveau inférieur
- Les rôles critiques (Maintainer, Owner) ont des responsabilités importantes

### 1.3 Authentification et tokens

#### Types de tokens GitLab

GitLab propose plusieurs mécanismes d'authentification pour différents cas d'usage :

```yaml
# Personal Access Tokens
# Utilisation: API calls, Git over HTTPS
personal_token_example:
  scope: ['api', 'read_user', 'read_repository']
  expiration: '2024-12-31'
  usage: |
    git clone https://oauth2:glpat-xxxxxxxxxxxxxxxxxxxx@gitlab.com/user/repo.git
    curl --header "PRIVATE-TOKEN: glpat-xxxxxxxxxxxxxxxxxxxx" \
         "https://gitlab.com/api/v4/projects"

# Deploy Tokens
# Utilisation: CI/CD, déploiements automatisés
deploy_token_example:
  username: 'deploy-token-user'
  scope: ['read_registry', 'read_repository']
  usage: |
    docker login registry.gitlab.com -u deploy-token-user -p gldt-xxxxxxxxxxxxxxxxxxxx

# Project Access Tokens (GitLab 13.0+)
# Utilisation: Automation spécifique au projet
project_token_example:
  scope: ['api', 'read_api']
  role: 'Developer'
  usage: |
    curl --header "PRIVATE-TOKEN: glpat-project-xxxxxxxxxxxxxxxxxxxx" \
         "https://gitlab.com/api/v4/projects/123/issues"
````

### 1.4 Exercice pratique : Configuration d'une organisation

**Contexte pédagogique** : Vous devez configurer GitLab pour l'entreprise fictive "TechCorp" avec 3 équipes de développement.

#### Cahier des charges

**Structure organisationnelle souhaitée** :

```
TechCorp (Group principal)
├── Frontend Team (Subgroup)
│   ├── Application Web React
│   └── Application Mobile React Native
├── Backend Team (Subgroup)
│   ├── API Gateway
│   └── Service Utilisateurs
└── DevOps Team (Subgroup)
    ├── Infrastructure as Code
    └── Monitoring et Logs
```

**Équipes et rôles** :

- **John Doe** : CTO (Owner du group principal)
- **Jane Smith** : Tech Lead (Maintainer global)
- **Alice Frontend** : Lead Frontend (Maintainer équipe Frontend)
- **Bob Backend** : Lead Backend (Maintainer équipe Backend)
- **Charlie DevOps** : Lead DevOps (Maintainer équipe DevOps)
- **Dave Junior** : Développeur junior (Developer)
- **Eve Stagiaire** : Stagiaire (Reporter)

#### Étapes de configuration

**Étape 1 : Création de la structure**

1. Créer le group principal "techcorp" (visibilité Private)
2. Créer les 3 subgroups (visibilité Internal)
3. Créer les projets dans chaque subgroup

**Étape 2 : Attribution des rôles**

1. Assigner John Doe comme Owner du group principal
2. Assigner les leads comme Maintainers de leurs équipes respectives
3. Assigner les développeurs selon leur niveau

**Étape 3 : Configuration de la visibilité**

1. Projets sensibles (infrastructure) : Private
2. Projets internes (APIs) : Internal
3. Projets de démonstration : Public (si applicable)

#### Questions de validation

1. **Quel niveau de permission minimum faut-il pour créer une merge request ?**
2. **Alice peut-elle modifier les settings du projet "API Gateway" ?**
3. **Eve peut-elle voir les pipelines CI/CD des projets ?**
4. **Qui peut supprimer le group principal "techcorp" ?**

---

## Module 2 : Collaboration Git Avancée

### Objectifs du module

- Comprendre et appliquer GitLab Flow comme méthodologie de travail
- Maîtriser les différentes stratégies de merge
- Configurer des processus de code review efficaces
- Implémenter CODEOWNERS et règles d'approbation

### 2.1 Méthodologies de travail Git

#### Comparaison des workflows Git

Avant d'adopter GitLab Flow, il est important de comprendre les alternatives existantes :

**1. Git Flow (Complexe)**

- Branches multiples : main, develop, feature, release, hotfix
- Adapté aux projets avec cycles de release longs
- Complexité élevée pour les équipes débutantes

**2. GitHub Flow (Simple)**

- Branches : main, feature uniquement
- Déploiement direct depuis main
- Simplicité maximale mais limitation pour environnements multiples

**3. GitLab Flow (Équilibré)**

- Branches : main, feature, environment (optionnel)
- Intégration CI/CD native
- Équilibre simplicité/flexibilité

#### Principes fondamentaux de GitLab Flow

GitLab Flow suit des principes clairs pour la collaboration :

```mermaid
gitgraph
    commit id: "Initial"
    branch feature/login
    checkout feature/login
    commit id: "Add login form"
    commit id: "Add validation"
    checkout main
    merge feature/login
    commit id: "Deploy to staging"
    branch production
    checkout production
    merge main
    commit id: "v1.0 Release"
    checkout main
    branch feature/dashboard
    checkout feature/dashboard
    commit id: "Add dashboard"
    checkout main
    merge feature/dashboard
    checkout production
    merge main
    commit id: "v1.1 Release"
```

**Règles de base** :

1. **Une fonctionnalité = une branche** (feature branch)
2. **Main toujours déployable** (tests passants obligatoires)
3. **Merge requests obligatoires** (pas de push direct sur main)
4. **Environment branches optionnelles** (staging, production)
5. **CI/CD intégré** à chaque étape
   merge main
   commit id: "v1.1 Release"

````

**Principes du GitLab Flow** :

1. **Feature branches** : Une branche par fonctionnalité
2. **Main branch** : Toujours déployable
3. **Environment branches** : production, staging (optionnel)
4. **Merge requests** : Obligatoires pour main
5. **CI/CD intégré** : Tests automatiques

**Comparaison des workflows** :

| Aspect               | Git Flow                                | GitHub Flow     | GitLab Flow                |
| -------------------- | --------------------------------------- | --------------- | -------------------------- |
| **Complexité**       | Élevée                                  | Faible          | Modérée                    |
| **Branches**         | main, develop, feature, release, hotfix | main, feature   | main, feature, environment |
| **Releases**         | Branches dédiées                        | Tags sur main   | Environment branches       |
| **CI/CD**            | Externe                                 | Intégré         | Intégré natif              |
| **Learning curve**   | Difficile                               | Facile          | Modérée                    |
| **Usage recommandé** | Projets complexes                       | Projets simples | La plupart des projets     |

#### **Feature Branching Strategy**

**Convention de nommage des branches** :

```bash
# Format recommandé
feature/JIRA-123-user-authentication
feature/add-payment-gateway
feature/improve-performance

# Autres types
bugfix/fix-login-error
hotfix/security-patch-2024-01
release/v2.0.0
experimental/new-ui-design

# Éviter
feature1
new-stuff
john-changes
temp-branch
````

**Workflow feature branch détaillé** :

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Feature as Feature Branch
    participant Main as Main Branch
    participant CI as CI/CD Pipeline
    participant Review as Code Review

    Dev->>Feature: 1. Create feature branch
    Dev->>Feature: 2. Implement feature
    Dev->>Feature: 3. Commit changes
    Feature->>CI: 4. Push triggers CI
    CI->>CI: 5. Run tests
    Dev->>Review: 6. Create Merge Request
    Review->>Review: 7. Code review process
    Review->>Main: 8. Approve & merge
    Main->>CI: 9. Deploy to staging
```

### 2.2 Merge Request Strategies

#### **Types de merge dans GitLab**

```mermaid
graph TB
    subgraph "Merge Strategies"
        A[Merge Commit] --> A1["Preserve history<br/>Keep branch context<br/>Complex graph"]

        B[Squash and Merge] --> B1["Clean history<br/>Single commit<br/>Simple graph"]

        C[Rebase and Merge] --> C1["Linear history<br/>Replay commits<br/>Fast-forward"]

        D[Fast-forward] --> D1["Direct pointer move<br/>No merge commit<br/>Conditions apply"]
    end

    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

#### **Configuration des merge requests**

**Paramètres projet recommandés** :

```yaml
# Project Settings → Merge requests
merge_request_settings:
  # Stratégie de merge
  merge_method: 'merge_commit' # ou "rebase_merge", "ff"

  # Protections
  only_allow_merge_if_pipeline_succeeds: true
  only_allow_merge_if_all_discussions_are_resolved: true
  remove_source_branch_after_merge: true

  # Squash commits
  squash_option: 'default_off' # "always", "never", "default_on"

  # Merge suggestions
  merge_commit_template: |
    Merge branch '%{source_branch}' into '%{target_branch}'

    %{title}

    %{description}

    Closes %{issues}

  squash_commit_template: |
    %{title}

    %{description}
```

#### **Processus de code review**

**Template de Merge Request** :

```markdown
## Description

Brief description of changes

## Type of change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No merge conflicts
```

### 2.3 Code Owners et approbations

#### **Fichier CODEOWNERS**

Le fichier `.gitlab/CODEOWNERS` définit qui doit approuver les modifications :

```bash
# .gitlab/CODEOWNERS

# Global owners (fallback)
* @tech-lead @senior-dev

# Frontend code
/frontend/ @frontend-team @ui-designer
*.vue @frontend-team
*.scss @frontend-team @ui-designer

# Backend code
/backend/ @backend-team
*.py @backend-team
/backend/auth/ @backend-team @security-team

# Infrastructure
/docker/ @devops-team
/k8s/ @devops-team @platform-team
Dockerfile @devops-team
*.yml @devops-team

# Database
/migrations/ @backend-team @dba
/database/ @dba

# Documentation
/docs/ @tech-writer @tech-lead
README.md @tech-lead
*.md @tech-writer

# Security sensitive
/security/ @security-team @tech-lead
/auth/ @security-team @backend-team

# Configuration
.gitlab-ci.yml @devops-team @tech-lead
package.json @frontend-team @tech-lead
requirements.txt @backend-team @tech-lead
```

#### **Règles d'approbation avancées**

```yaml
# Project Settings → Merge request approvals
approval_rules:
  # Règle générale
  - name: 'General approval'
    approvals_required: 1
    users: ['@tech-lead']
    groups: ['@senior-developers']

  # Règle sécurité
  - name: 'Security approval'
    approvals_required: 2
    protected_branches: ['main', 'production']
    rule_type: 'security'
    source_files: ['**/*auth*', '**/security/**', '**/*password*']
    users: ['@security-lead', '@tech-lead']

  # Règle base de données
  - name: 'Database approval'
    approvals_required: 1
    source_files: ['**/migrations/**', '**/*migration*', '**/schema.sql']
    users: ['@dba', '@backend-lead']
```

### 2.4 Application pratique

#### **Lab : Configuration d'un workflow GitLab Flow**

**Objectif** : Configurer un projet avec GitLab Flow complet

**Étapes** :

1. **Configuration des branches** :

   ```bash
   # Branches principales
   main          # Code stable
   staging       # Tests d'intégration
   production    # Code en production

   # Branches de travail
   feature/user-auth
   bugfix/login-error
   hotfix/security-patch
   ```

2. **Protection des branches** :

   ```yaml
   # main branch protection
   main_protection:
     push_access_level: 'maintainer'
     merge_access_level: 'developer'
     unprotect_access_level: 'maintainer'
     allow_force_push: false
     code_owner_approval_required: true

   # production branch protection
   production_protection:
     push_access_level: 'maintainer'
     merge_access_level: 'maintainer'
     unprotect_access_level: 'owner'
     allow_force_push: false
     code_owner_approval_required: true
   ```

3. **Merge request template** :

   ```markdown
   <!-- .gitlab/merge_request_templates/Default.md -->

   ## Objectif

   ## Changements - [ ]

   ## Tests

   - [ ] Tests unitaires
   - [ ] Tests d'intégration
   - [ ] Tests manuels

   ## Checklist

   - [ ] Code review auto-effectué
   - [ ] Documentation mise à jour
   - [ ] Breaking changes documentés

   /assign @reviewer
   /label ~"needs review"
   ```

---

## Module 3 : Protection et Sécurité

### 3.1 Protection des branches

#### **Configuration des branches protégées**

La protection des branches est essentielle pour maintenir la qualité du code :

```mermaid
graph TB
    subgraph "Branch Protection Layers"
        A[Push Protection] --> A1["Block direct push<br/>Allow merge requests<br/>Role-based access"]

        B[Merge Protection] --> B1["Pipeline must succeed<br/>Approval required<br/>Discussions resolved"]

        C[Force Push Protection] --> C1["Prevent history rewrite<br/>Protect commit history<br/>Maintain audit trail"]

        D[Delete Protection] --> D1["Prevent branch deletion<br/>Lock important branches<br/>Admin only unprotect"]
    end

    style A fill:#ffebee
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

#### **Configuration avancée de protection**

```yaml
# Project Settings → Repository → Protected branches
branch_protection_config:
  main:
    push_access:
      access_level: 'maintainer'
      users: []
      groups: []
    merge_access:
      access_level: 'developer'
      users: ['@tech-lead']
      groups: ['@senior-developers']
    unprotect_access:
      access_level: 'maintainer'
    settings:
      allow_force_push: false
      code_owner_approval_required: true

  production:
    push_access:
      access_level: 'no_access' # Personne ne peut push directement
    merge_access:
      access_level: 'maintainer'
      users: ['@release-manager']
    unprotect_access:
      access_level: 'owner'
    settings:
      allow_force_push: false
      code_owner_approval_required: true

  'release/*':
    push_access:
      access_level: 'maintainer'
    merge_access:
      access_level: 'maintainer'
    settings:
      allow_force_push: false
```

#### **Push Rules avancées (GitLab Premium)**

```yaml
# Project Settings → Repository → Push Rules
push_rules:
  # Restrictions sur les commits
  commit_message_regex: "^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"
  commit_message_negative_regex: "(password|secret|key)"

  # Restrictions sur les branches
  branch_name_regex: "^(feature|bugfix|hotfix|release)\/[a-z0-9-]+"

  # Restrictions sur les auteurs
  author_email_regex: "@company\.com$"

  # Restrictions sur les fichiers
  prohibited_file_names: "*.exe,*.dll,*.so"
  max_file_size: 100  # MB

  # Sécurité
  deny_delete_tag: true
  member_check: true
  prevent_secrets: true
```

### 3.2 Sécurité et scanning

#### **Security Scanning intégré**

GitLab propose plusieurs types de scanning automatique :

```mermaid
graph TB
    subgraph "GitLab Security Scanning"
        A[SAST] --> A1["Static Application Security Testing<br/>Code source analysis<br/>Vulnerability detection"]

        B[DAST] --> B1["Dynamic Application Security Testing<br/>Running application test<br/>Web vulnerability scan"]

        C[Dependency Scanning] --> C1["Third-party dependencies<br/>Known vulnerabilities<br/>License compliance"]

        D[Container Scanning] --> D1["Docker image analysis<br/>OS vulnerabilities<br/>Base image security"]

        E[Secret Detection] --> E1["Hardcoded secrets<br/>API keys detection<br/>Password exposure"]
    end

    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffebee
```

#### **Configuration SAST dans GitLab CI**

```yaml
# .gitlab-ci.yml - Security scanning
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

stages:
  - build
  - test
  - security
  - deploy

# Custom SAST configuration
sast:
  stage: security
  variables:
    SAST_EXCLUDED_PATHS: 'spec, test, tests, tmp'
    SAST_EXCLUDED_ANALYZERS: 'bandit,brakeman'
  artifacts:
    reports:
      sast: gl-sast-report.json
  only:
    - merge_requests
    - main
    - develop

# Secret detection
secret_detection:
  stage: security
  variables:
    SECRET_DETECTION_EXCLUDED_PATHS: 'tests/,docs/'
  artifacts:
    reports:
      secret_detection: gl-secret-detection-report.json

# Dependency scanning
dependency_scanning:
  stage: security
  variables:
    DS_EXCLUDED_PATHS: 'spec,test,tests,tmp'
  artifacts:
    reports:
      dependency_scanning: gl-dependency-scanning-report.json

# Container scanning
container_scanning:
  stage: security
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      container_scanning: gl-container-scanning-report.json
```

### 3.3 Access control et authentification

#### **Two-Factor Authentication (2FA)**

```mermaid
sequenceDiagram
    participant User as Utilisateur
    participant GitLab as GitLab
    participant Auth as Authenticator
    participant Mobile as Mobile App

    User->>GitLab: Username + Password
    GitLab->>User: Request 2FA token
    User->>Auth: Open authenticator
    Auth->>Mobile: Generate TOTP
    Mobile->>User: Display 6-digit code
    User->>GitLab: Enter 2FA code
    GitLab->>GitLab: Verify TOTP
    GitLab->>User: Access granted
```

**Configuration 2FA obligatoire** :

```yaml
# Group Settings → General → Permissions
two_factor_settings:
  require_two_factor_authentication: true
  two_factor_grace_period: 48 # hours

# Pour forcer 2FA sur tous les projets du groupe
group_security_policy:
  enforce_two_factor_authentication: true
  two_factor_grace_period_expired_action: 'block'
```

#### **Integration SAML/SSO**

```yaml
# Admin Area → Settings → Sign-in restrictions
saml_configuration:
  enabled: true
  auto_sign_in_with_provider: 'saml'

  # SAML settings
  assertion_consumer_service_url: 'https://gitlab.company.com/users/auth/saml/callback'
  issuer: 'https://gitlab.company.com'

  # Attribute mapping
  attribute_statements:
    email: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'
    first_name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname'
    last_name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname'
    name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'
    username: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'

  # Group mapping
  group_saml:
    enabled: true
    auto_link_saml_user: true
    external_groups: ['external-contractors']
```

### 3.4 Audit et monitoring

#### **Audit Events**

GitLab enregistre automatiquement les événements critiques :

```yaml
# Types d'événements audités
audit_events:
  user_events:
    - user_created
    - user_deleted
    - user_email_changed
    - password_changed
    - two_factor_enabled

  project_events:
    - project_created
    - project_deleted
    - project_visibility_changed
    - member_added
    - member_removed
    - member_role_changed

  security_events:
    - failed_login
    - successful_login
    - token_created
    - token_revoked
    - ssh_key_added
    - ssh_key_removed

  repository_events:
    - repository_created
    - repository_deleted
    - push_events
    - merge_request_created
    - merge_request_merged
```

#### **Monitoring et alertes**

```yaml
# Configuration monitoring sécurité
security_monitoring:
  # Alertes push suspects
  suspicious_push_detection:
    enabled: true
    thresholds:
      files_changed: 100
      lines_added: 10000
      large_files: 50MB

  # Alertes connexion
  login_monitoring:
    enabled: true
    alerts:
      - multiple_failed_attempts: 5
      - unusual_location: true
      - new_device: true

  # Monitoring CI/CD
  pipeline_security:
    secrets_detection: true
    approval_bypass_alerts: true
    runner_security_alerts: true
```

---

## Module 4 : Project Management

### 4.1 Issues et Epic Management

#### **Types d'issues GitLab**

```mermaid
graph TB
    subgraph "Issue Hierarchy"
        A[Epic] --> A1["High-level goal<br/>Multiple milestones<br/>Cross-team initiative"]

        B[Issue] --> B1["Individual task<br/>Bug report<br/>Feature request"]

        C[Task] --> C1["Checklist item<br/>Sub-issue<br/>Action item"]

        D[Incident] --> D1["Production issue<br/>Urgent resolution<br/>On-call response"]
    end

    A --> B
    B --> C

    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#ffebee
```

#### **Templates d'issues**

Créez des templates pour standardiser la création d'issues :

```markdown
<!-- .gitlab/issue_templates/Bug_Report.md -->

## Bug Report

### Description

Brief description of the bug

### Steps to Reproduce

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

### Expected Behavior

Clear description of what you expected to happen.

### Actual Behavior

Clear description of what actually happened.

### Environment

- OS: [e.g. macOS, Windows, Linux]
- Browser: [e.g. Chrome, Safari, Firefox]
- Version: [e.g. 1.2.3]

### Screenshots

If applicable, add screenshots to help explain your problem.

### Additional Context

Add any other context about the problem here.

/label ~bug ~needs-investigation
/assign @bug-triager
```

```markdown
<!-- .gitlab/issue_templates/Feature_Request.md -->

## Feature Request

### Feature Summary

Brief description of the feature

### Problem Statement

What problem does this feature solve?

### Proposed Solution

Detailed description of the proposed solution

### Alternative Solutions

Describe any alternative solutions considered

### User Stories

- As a [user type], I want [goal] so that [benefit]

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Technical Considerations

Any technical constraints or considerations

### Design Mockups

Add mockups or wireframes if available

/label ~feature ~needs-design
/milestone %"Next Release"
```

### 4.2 Labels et organisation

#### **Stratégie de labeling**

```mermaid
graph LR
    subgraph "Label Categories"
        A[Type] --> A1["~bug<br/>~feature<br/>~enhancement<br/>~documentation"]

        B[Priority] --> B1["~priority::critical<br/>~priority::high<br/>~priority::medium<br/>~priority::low"]

        C[Status] --> C1["~status::todo<br/>~status::doing<br/>~status::review<br/>~status::done"]

        D[Team] --> D1["~team::frontend<br/>~team::backend<br/>~team::devops<br/>~team::design"]

        E[Epic] --> E1["~epic::user-auth<br/>~epic::payment<br/>~epic::mobile-app"]
    end

    style A fill:#e3f2fd
    style B fill:#ffebee
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#f3e5f5
```

#### **Configuration de labels avancée**

```yaml
# Labels recommandés pour un projet
project_labels:
  # Types (couleur: bleue)
  type_labels:
    - {name: '~bug', color: '#d73a4a', description: "Something isn't working"}
    - {name: '~feature', color: '#0052cc', description: 'New functionality'}
    - {
        name: '~enhancement',
        color: '#a2eeef',
        description: 'Improvement to existing feature'
      }
    - {
        name: '~documentation',
        color: '#0075ca',
        description: 'Documentation related'
      }

  # Priorités (couleur: rouge dégradé)
  priority_labels:
    - {
        name: '~priority::critical',
        color: '#d73a4a',
        description: 'Critical priority'
      }
    - {name: '~priority::high', color: '#ff6b6b', description: 'High priority'}
    - {
        name: '~priority::medium',
        color: '#ffcc02',
        description: 'Medium priority'
      }
    - {name: '~priority::low', color: '#28a745', description: 'Low priority'}

  # Statuts (couleur: verte dégradé)
  status_labels:
    - {name: '~status::todo', color: '#fbca04', description: 'Ready to start'}
    - {
        name: '~status::doing',
        color: '#0052cc',
        description: 'Work in progress'
      }
    - {name: '~status::review', color: '#f9d71c', description: 'Under review'}
    - {name: '~status::done', color: '#28a745', description: 'Completed'}

  # Équipes (couleur: violette)
  team_labels:
    - {name: '~team::frontend', color: '#8b5cf6', description: 'Frontend team'}
    - {name: '~team::backend', color: '#6366f1', description: 'Backend team'}
    - {name: '~team::devops', color: '#ec4899', description: 'DevOps team'}
    - {name: '~team::design', color: '#f59e0b', description: 'Design team'}
```

### 4.3 Milestones et planification

#### **Stratégie de milestones**

```mermaid
gantt
    title Project Roadmap
    dateFormat YYYY-MM-DD
    axisFormat %m/%d

    section Version 1.0
    Core Features     :done, v1-core, 2024-01-01, 2024-02-15
    Testing Phase     :done, v1-test, 2024-02-15, 2024-03-01
    Release v1.0      :milestone, v1-release, 2024-03-01, 0d

    section Version 1.1
    API Improvements  :active, v11-api, 2024-03-01, 2024-03-20
    UI Enhancements   :v11-ui, 2024-03-10, 2024-03-25
    Security Updates  :v11-sec, 2024-03-15, 2024-03-30
    Release v1.1      :milestone, v11-release, 2024-03-30, 0d

    section Version 2.0
    Mobile App        :v2-mobile, 2024-03-30, 2024-05-15
    Advanced Features :v2-advanced, 2024-04-15, 2024-06-01
    Release v2.0      :milestone, v2-release, 2024-06-01, 0d
```

#### **Configuration de milestones**

```yaml
# Project milestones configuration
milestones:
  'v1.0 - Core Platform':
    description: |
      Initial release with core functionality:
      - User authentication
      - Basic CRUD operations
      - Admin dashboard
    due_date: '2024-03-01'
    start_date: '2024-01-01'

  'v1.1 - Performance & UX':
    description: |
      Performance improvements and UX enhancements:
      - API optimization
      - UI/UX improvements
      - Bug fixes
    due_date: '2024-03-30'
    start_date: '2024-03-01'

  'v2.0 - Mobile & Advanced':
    description: |
      Mobile application and advanced features:
      - Mobile app (iOS/Android)
      - Advanced analytics
      - Integration APIs
    due_date: '2024-06-01'
    start_date: '2024-03-30'
```

### 4.4 Issue Boards et Kanban

#### **Configuration d'Issue Board**

```mermaid
graph LR
    subgraph "Kanban Board"
        A[Backlog] --> B[Todo]
        B --> C[Doing]
        C --> D[Review]
        D --> E[Done]
        D --> F[Blocked]
        F --> C
    end

    subgraph "Label Mapping"
        G[~status::todo] --> B
        H[~status::doing] --> C
        I[~status::review] --> D
        J[~status::done] --> E
        K[~blocked] --> F
    end
```

**Configuration board personnalisé** :

```yaml
# Issue Board configuration
issue_boards:
  'Development Board':
    lists:
      - label: 'Open' # Issues without status labels
      - label: '~status::todo'
      - label: '~status::doing'
      - label: '~status::review'
      - label: '~status::done'
      - label: 'Closed' # Closed issues

  'Team Boards':
    frontend_board:
      assignee: '@frontend-team'
      labels: ['~team::frontend']
      milestone: 'Current Sprint'

    backend_board:
      assignee: '@backend-team'
      labels: ['~team::backend']
      milestone: 'Current Sprint'
```

### 4.5 Application pratique

#### **Lab : Configuration complète project management**

**Objectif** : Configurer un système complet de gestion de projet

1. **Créer les templates** :

   ```bash
   .gitlab/
   ├── issue_templates/
   │   ├── Bug_Report.md
   │   ├── Feature_Request.md
   │   └── Task.md
   └── merge_request_templates/
       └── Default.md
   ```

2. **Configurer les labels** :

   ```yaml
   # Via API ou interface
   labels:
     - "~bug" (rouge)
     - "~feature" (bleu)
     - "~priority::high" (rouge foncé)
     - "~priority::medium" (orange)
     - "~priority::low" (vert)
     - "~status::todo" (jaune)
     - "~status::doing" (bleu)
     - "~status::done" (vert)
   ```

3. **Créer les milestones** :

   ```
   Sprint 1 (2 semaines)
   Sprint 2 (2 semaines)
   Release v1.0 (1 mois)
   ```

4. **Configurer l'Issue Board** :
   - Colonnes par statut
   - Filtres par équipe
   - Assignation automatique

---

## Module 5 : Environnements et Déploiements

### 5.1 Environment Management

#### **Concept des environments GitLab**

Les environments GitLab permettent de tracker et contrôler les déploiements :

```mermaid
graph TB
    subgraph "Environment Tiers"
        A[Development] --> A1["Feature testing<br/>Developer access<br/>Frequent deployments"]

        B[Staging] --> B1["Integration testing<br/>QA team access<br/>Release candidates"]

        C[Production] --> C1["Live application<br/>End users<br/>Restricted access"]

        D[Review Apps] --> D1["MR previews<br/>Feature demos<br/>Temporary"]
    end

    style A fill:#fff3e0
    style B fill:#e8f5e8
    style C fill:#ffebee
    style D fill:#e3f2fd
```

#### **Configuration des environments**

```yaml
# .gitlab-ci.yml - Environments configuration
stages:
  - build
  - test
  - deploy_review
  - deploy_staging
  - deploy_production

# Review Apps - Environment dynamique
deploy_review:
  stage: deploy_review
  script:
    - echo "Deploying review app..."
    - docker build -t review-app:$CI_COMMIT_SHORT_SHA .
    - docker run -d --name review-$CI_COMMIT_SHORT_SHA \
      -p 800$CI_PIPELINE_ID:80 review-app:$CI_COMMIT_SHORT_SHA
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: http://review-$CI_COMMIT_SHORT_SHA.example.com
    on_stop: stop_review
    auto_stop_in: 1 week
  only:
    - merge_requests
  except:
    - main

# Arrêt Review App
stop_review:
  stage: deploy_review
  script:
    - docker stop review-$CI_COMMIT_SHORT_SHA
    - docker rm review-$CI_COMMIT_SHORT_SHA
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
  only:
    - merge_requests

# Staging Environment
deploy_staging:
  stage: deploy_staging
  script:
    - echo "Deploying to staging..."
    - kubectl apply -f k8s/staging/
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: staging
    url: https://staging.example.com
    deployment_tier: staging
  only:
    - develop
    - main

# Production Environment
deploy_production:
  stage: deploy_production
  script:
    - echo "Deploying to production..."
    - kubectl apply -f k8s/production/
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  environment:
    name: production
    url: https://example.com
    deployment_tier: production
  only:
    - main
  when: manual
  allow_failure: false
```

### 5.2 Environment Protection

#### **Règles de protection d'environment**

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Pipeline as CI Pipeline
    participant Approval as Approval Gate
    participant Prod as Production

    Dev->>Pipeline: Trigger deployment
    Pipeline->>Approval: Request approval
    Note over Approval: Protected Environment<br/>Requires manual approval
    Approval->>Approval: Validate deployment
    Approval->>Prod: Approve deployment
    Prod->>Prod: Deploy application
    Prod->>Dev: Deployment successful
```

#### **Configuration protection avancée**

```yaml
# Project Settings → CI/CD → Environments
environment_protection:
  production:
    protected: true
    deploy_access_levels:
      - access_level: 'maintainer'
        users: ['@release-manager', '@tech-lead']
        groups: ['@senior-developers']

    approval_rules:
      - required_approvals: 2
        users: ['@tech-lead', '@product-owner']
        groups: ['@approvers']
        group_inheritance: false

    deployment_approval_settings:
      prevent_approval_by_author: true
      prevent_approval_by_commit_author: true
      require_password_to_approve: false

  staging:
    protected: true
    deploy_access_levels:
      - access_level: 'developer'
        groups: ['@development-team']

    approval_rules:
      - required_approvals: 1
        groups: ['@qa-team']
```

### 5.3 GitLab Pages

#### **Configuration GitLab Pages**

GitLab Pages permet d'héberger des sites statiques directement depuis vos repositories :

```yaml
# .gitlab-ci.yml - GitLab Pages
stages:
  - build
  - deploy

# Build du site statique
build_site:
  stage: build
  image: node:18-alpine
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

# Déploiement GitLab Pages
pages:
  stage: deploy
  script:
    - mkdir public
    - cp -r dist/* public/
  artifacts:
    paths:
      - public
  only:
    - main
  environment:
    name: pages
    url: https://$CI_PROJECT_NAMESPACE.gitlab.io/$CI_PROJECT_NAME
```

#### **Pages avec domaine personnalisé**

```yaml
# Configuration domaine personnalisé
pages_custom_domain:
  stage: deploy
  script:
    - mkdir public
    - cp -r dist/* public/
    # Configuration DNS
    - echo "blog.example.com" > public/CNAME
  artifacts:
    paths:
      - public
  environment:
    name: pages
    url: https://blog.example.com
  only:
    - main
```

#### **Pages avec authentification**

```yaml
# Pages privées (GitLab Premium)
pages_private:
  stage: deploy
  script:
    - mkdir public
    - cp -r dist/* public/
  artifacts:
    paths:
      - public
  environment:
    name: pages
    url: https://$CI_PROJECT_NAMESPACE.gitlab.io/$CI_PROJECT_NAME
  variables:
    PAGES_ACCESS_CONTROL: 'true'
  only:
    - main
```

### 5.4 Review Apps avancées

#### **Review Apps avec Docker Compose**

```yaml
# .gitlab-ci.yml - Review Apps avancées
.review_app_template: &review_app
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  before_script:
    - apk add --no-cache curl
    - docker info

deploy_review:
  <<: *review_app
  stage: deploy_review
  script:
    # Build images
    - docker build -t $CI_REGISTRY_IMAGE/app:$CI_COMMIT_SHORT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE/nginx:$CI_COMMIT_SHORT_SHA nginx/

    # Create network
    - docker network create review-$CI_COMMIT_SHORT_SHA || true

    # Deploy database
    - |
      docker run -d \
        --name review-db-$CI_COMMIT_SHORT_SHA \
        --network review-$CI_COMMIT_SHORT_SHA \
        -e POSTGRES_DB=reviewapp \
        -e POSTGRES_USER=app \
        -e POSTGRES_PASSWORD=secret \
        postgres:13-alpine

    # Deploy application
    - |
      docker run -d \
        --name review-app-$CI_COMMIT_SHORT_SHA \
        --network review-$CI_COMMIT_SHORT_SHA \
        -e DATABASE_URL=postgresql://app:secret@review-db-$CI_COMMIT_SHORT_SHA:5432/reviewapp \
        -e RAILS_ENV=production \
        $CI_REGISTRY_IMAGE/app:$CI_COMMIT_SHORT_SHA

    # Deploy nginx
    - |
      docker run -d \
        --name review-nginx-$CI_COMMIT_SHORT_SHA \
        --network review-$CI_COMMIT_SHORT_SHA \
        -p 80$CI_PIPELINE_ID:80 \
        $CI_REGISTRY_IMAGE/nginx:$CI_COMMIT_SHORT_SHA

    # Health check
    - sleep 30
    - curl -f http://localhost:80$CI_PIPELINE_ID || exit 1

  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: http://review-$CI_COMMIT_SHORT_SHA.staging.example.com
    on_stop: stop_review
    auto_stop_in: 1 week
  only:
    - merge_requests
  except:
    - main

stop_review:
  <<: *review_app
  stage: deploy_review
  script:
    - docker stop review-nginx-$CI_COMMIT_SHORT_SHA || true
    - docker stop review-app-$CI_COMMIT_SHORT_SHA || true
    - docker stop review-db-$CI_COMMIT_SHORT_SHA || true
    - docker rm review-nginx-$CI_COMMIT_SHORT_SHA || true
    - docker rm review-app-$CI_COMMIT_SHORT_SHA || true
    - docker rm review-db-$CI_COMMIT_SHORT_SHA || true
    - docker network rm review-$CI_COMMIT_SHORT_SHA || true
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
  allow_failure: true
  only:
    - merge_requests
```

### 5.5 Monitoring et observabilité

#### **Integration monitoring dans environments**

```yaml
# Monitoring d'environment
deploy_production_with_monitoring:
  stage: deploy_production
  script:
    - kubectl apply -f k8s/production/
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

    # Attendre le déploiement
    - kubectl rollout status deployment/app

    # Vérifications santé
    - kubectl get pods -l app=myapp
    - curl -f https://example.com/health

    # Notifier monitoring
    - |
      curl -X POST https://monitoring.example.com/api/deployments \
        -H "Authorization: Bearer $MONITORING_TOKEN" \
        -d "{
          \"environment\": \"production\",
          \"version\": \"$CI_COMMIT_SHA\",
          \"timestamp\": \"$(date -Iseconds)\",
          \"url\": \"https://example.com\"
        }"

  environment:
    name: production
    url: https://example.com
    deployment_tier: production
  after_script:
    # Métriques de déploiement
    - echo "DEPLOYMENT_TIME=$(date +%s)" >> deploy.env
    - echo "DEPLOYMENT_SHA=$CI_COMMIT_SHA" >> deploy.env
  artifacts:
    reports:
      dotenv: deploy.env
  only:
    - main
  when: manual
```

---

## Synthèse et Bonnes Pratiques

### Architecture GitLab complète

```mermaid
C4Container
    title GitLab Complete Architecture

    Person(dev, "Developer", "Team member")
    Person(pm, "Product Manager", "Project management")
    Person(admin, "Admin", "GitLab administration")

    System_Boundary(gitlab, "GitLab Platform") {
        Container(repo, "Repository", "Git", "Source code + GitLab Flow")
        Container(issues, "Issues & Boards", "Project Management", "Tasks, bugs, features")
        Container(mr, "Merge Requests", "Code Review", "Approval workflow")
        Container(ci, "CI/CD Pipelines", "Automation", "Build, test, deploy")
        Container(env, "Environments", "Deployment", "Review, staging, production")
        Container(sec, "Security Scanning", "DevSecOps", "SAST, DAST, Dependencies")
        Container(pages, "GitLab Pages", "Static Sites", "Documentation, demos")
        Container(reg, "Container Registry", "Docker Images", "Application artifacts")
    }

    System_Ext(k8s, "Kubernetes", "Container orchestration")
    System_Ext(mon, "Monitoring", "Observability platform")

    Rel(dev, repo, "Push code")
    Rel(dev, issues, "Create issues")
    Rel(dev, mr, "Create MR")
    Rel(pm, issues, "Manage project")
    Rel(admin, gitlab, "Configure")

    Rel(repo, ci, "Trigger pipeline")
    Rel(ci, sec, "Security scan")
    Rel(ci, reg, "Store images")
    Rel(ci, env, "Deploy apps")
    Rel(env, k8s, "Deploy to cluster")
    Rel(env, mon, "Send metrics")
    Rel(mr, env, "Create review app")
```

### Checklist configuration projet

#### **Setup initial**

- [ ] Structure organizationnelle (Groups/Projects)
- [ ] Membres et permissions configurés
- [ ] Visibility levels appropriés
- [ ] Integration SSO/SAML (si nécessaire)

#### **Repository et code**

- [ ] Branches protégées configurées
- [ ] Merge request templates créés
- [ ] CODEOWNERS file configuré
- [ ] Push rules définies (Premium)

#### **Workflow collaboration**

- [ ] GitLab Flow implémenté
- [ ] Approval rules configurées
- [ ] Labels organisés et cohérents
- [ ] Issue templates créés

#### **Project management**

- [ ] Milestones planifiés
- [ ] Issue boards configurés
- [ ] Epic hierarchy définie (Premium)
- [ ] Integration tools externes

#### **CI/CD et sécurité**

- [ ] Pipelines CI/CD configurés
- [ ] Security scanning activé
- [ ] Variables et secrets sécurisés
- [ ] Runners appropriés configurés

#### **Environments**

- [ ] Environment protection configurée
- [ ] Review apps automatiques
- [ ] Deployment approvals
- [ ] Monitoring intégré

#### **Documentation**

- [ ] README complet
- [ ] Documentation technique
- [ ] GitLab Pages configuré
- [ ] Runbooks de déploiement

### Ressources complémentaires

#### **Documentation officielle**

- [GitLab Documentation](https://docs.gitlab.com/)
- [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)
- [Security Scanning](https://docs.gitlab.com/ee/user/application_security/)
- [Environment Protection](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

#### **Outils et intégrations**

- [GitLab API](https://docs.gitlab.com/ee/api/)
- [GitLab CLI (glab)](https://gitlab.com/gitlab-org/cli)
- [Terraform GitLab Provider](https://registry.terraform.io/providers/gitlabhq/gitlab/latest)

#### **Communauté**

- [GitLab Forum](https://forum.gitlab.com/)
- [GitLab Discord](https://discord.gg/gitlab)
- [GitLab Meetups](https://about.gitlab.com/events/)

---

**Formation complétée**

Ce cours annexe couvre tous les aspects fondamentaux de GitLab nécessaires pour une utilisation professionnelle efficace. Il complète parfaitement le cours principal axé sur CI/CD en ajoutant les dimensions collaboration, sécurité et gestion de projet.
