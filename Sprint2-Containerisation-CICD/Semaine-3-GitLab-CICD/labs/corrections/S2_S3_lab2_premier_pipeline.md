# LAB 2 - CORRECTIONS : Premier pipeline React

## Solution complète

### Configuration .gitlab-ci.yml finale

```yaml
# Pipeline GitLab CI/CD pour React App
image: node:18-alpine

# Définition des stages
stages:
  - install
  - build
  - test
  - deploy

# Configuration cache global
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .npm/

# Variables globales
variables:
  npm_config_cache: '$CI_PROJECT_DIR/.npm'

# Job 1: Installation dépendances
install_dependencies:
  stage: install
  script:
    - echo "🔧 Installation des dépendances npm"
    - npm ci --cache .npm --prefer-offline
    - echo "✅ Dépendances installées avec succès"
    - echo "📊 Taille node_modules:" && du -sh node_modules/
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour
  only:
    - main
    - develop
    - merge_requests

# Job 2: Build application
build_application:
  stage: build
  script:
    - echo "🏗️ Construction de l'application React"
    - npm run build
    - echo "✅ Build terminé avec succès"
    - echo "📁 Contenu du dossier build:"
    - ls -la build/
    - echo "📊 Taille du build:" && du -sh build/
  artifacts:
    paths:
      - build/
    expire_in: 1 day
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests

# Job 3: Tests application
test_application:
  stage: test
  script:
    - echo "🧪 Exécution des tests unitaires"
    - npm test -- --coverage --watchAll=false
    - echo "✅ Tests terminés"
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 1 week
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests

# Job 4: Déploiement staging
deploy_staging:
  stage: deploy
  script:
    - echo "🚀 Déploiement vers l'environnement staging"
    - echo "📁 Vérification des fichiers à déployer:"
    - ls -la build/
    - echo "🌐 URL de staging: https://staging-demo-react-app.example.com"
    - echo "✅ Simulation déploiement staging réussi"
  environment:
    name: staging
    url: https://staging-demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - develop
  when: manual

# Job 5: Déploiement production
deploy_production:
  stage: deploy
  script:
    - echo "🚀 Déploiement vers l'environnement production"
    - echo "📁 Vérification des fichiers à déployer:"
    - ls -la build/
    - echo "🌐 URL de production: https://demo-react-app.example.com"
    - echo "✅ Simulation déploiement production réussi"
  environment:
    name: production
    url: https://demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - main
  when: manual
```

## Explications détaillées

### 1. Configuration d'image et stages

**Image utilisée** : `node:18-alpine`

- **Pourquoi Alpine ?** Image plus légère (5MB vs 300MB pour Ubuntu)
- **Node 18** : Version LTS stable pour React
- **Performance** : Réduction du temps de téléchargement

**Stages définis** :

```yaml
stages:
  - install # Installation des dépendances
  - build # Construction de l'application
  - test # Tests unitaires et couverture
  - deploy # Déploiement staging/production
```

### 2. Optimisation cache

**Configuration cache globale** :

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/
    - .npm/
```

**Avantages** :

- Réduction du temps d'installation de 2-3 minutes à 30 secondes
- Utilisation du cache npm local
- Cache partagé entre les jobs du même pipeline

### 3. Variables d'environnement

```yaml
variables:
  npm_config_cache: '$CI_PROJECT_DIR/.npm'
```

**Fonction** :

- Définit le répertoire cache npm dans le projet
- Optimise les téléchargements de packages
- Améliore la reproductibilité

### 4. Configuration des jobs

#### Job Install

```yaml
install_dependencies:
  stage: install
  script:
    - npm ci --cache .npm --prefer-offline
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour
```

**Points clés** :

- `npm ci` au lieu de `npm install` (plus rapide, reproductible)
- `--prefer-offline` utilise le cache en priorité
- Artifacts partagés avec les autres jobs
- Expiration 1h (suffisant pour le pipeline)

#### Job Build

```yaml
build_application:
  stage: build
  dependencies:
    - install_dependencies
  artifacts:
    paths:
      - build/
    expire_in: 1 day
```

**Points clés** :

- Dépendance explicite sur `install_dependencies`
- Artifacts build conservés 1 jour
- Vérification du contenu généré

#### Job Test

```yaml
test_application:
  stage: test
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

**Points clés** :

- Regex pour extraire le pourcentage de couverture
- Rapport de couverture Cobertura pour GitLab
- Tests sans mode watch (`--watchAll=false`)

#### Jobs Deploy

```yaml
deploy_staging:
  environment:
    name: staging
    url: https://staging-demo-react-app.example.com
  only:
    - develop
  when: manual

deploy_production:
  environment:
    name: production
    url: https://demo-react-app.example.com
  only:
    - main
  when: manual
```

**Points clés** :

- Environments GitLab avec URLs
- Déploiement manuel (`when: manual`)
- Branches spécifiques (develop → staging, main → production)

## Problèmes courants et solutions

### 1. Erreur "npm command not found"

**Cause** : Image sans Node.js
**Solution** : Utiliser `image: node:18-alpine`

### 2. Tests qui ne passent pas

**Cause** : Tests en mode watch
**Solution** : Ajouter `--watchAll=false`

### 3. Cache inefficace

**Cause** : Mauvaise configuration des paths
**Solution** : Vérifier `node_modules/` et `.npm/` dans le cache

### 4. Artifacts non disponibles

**Cause** : Jobs sans dépendances
**Solution** : Ajouter `dependencies: [nom_job]`

## Optimisations possibles

### 1. Parallélisation

```yaml
# Exécuter build et test en parallèle après install
build_application:
  stage: build
test_application:
  stage: build # Même stage que build
```

### 2. Cache plus agressif

```yaml
cache:
  key:
    files:
      - package-lock.json # Cache basé sur le lockfile
  policy: pull-push
```

### 3. Conditions de déclenchement

```yaml
only:
  changes:
    - 'src/**/*'
    - 'public/**/*'
    - package.json
```

### 4. Notifications

```yaml
after_script:
  - echo "Pipeline terminé - Notification Slack/Teams"
```

## Métriques attendues

### Temps d'exécution

- **Install** : 30-60 secondes (avec cache)
- **Build** : 45-90 secondes
- **Test** : 15-30 secondes
- **Deploy** : 10-20 secondes
- **Total** : 2-3 minutes (sans cache : 5-7 minutes)

### Taille des artifacts

- **node_modules/** : 150-300 MB
- **build/** : 2-5 MB
- **coverage/** : 1-3 MB

### Couverture de code

- **Objectif minimum** : 70%
- **Objectif recommandé** : 85%

## Points d'attention

1. **Sécurité** : Ne jamais exposer de secrets dans les logs
2. **Performance** : Surveiller la taille du cache
3. **Coûts** : Optimiser les runners et le temps d'exécution
4. **Maintenance** : Tenir à jour les versions d'images

## Validation du lab

✅ **Pipeline complet fonctionnel**
✅ **Cache configuré et efficace**
✅ **Artifacts générés correctement**
✅ **Environments configurés**
✅ **Documentation complète**
