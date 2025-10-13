# CORRECTION LAB 1 - Découverte GitLab CI et premier pipeline

**Sprint 2 - Semaine 3 - Séance 1**  
**Référence** : `S2_S3_S1_lab1_premier_pipeline_correction`

## Solution complète

### Réponses aux questions d'analyse

1. **Quels sont les stages logiques pour cette application ?**

   - Stage 1 : **install** (installation des dépendances)
   - Stage 2 : **test** (exécution des tests unitaires)
   - Stage 3 : **build** (construction de l'application)
   - Stage 4 : **deploy** (déploiement sur GitLab Pages)

2. **Quelles images Docker conviennent pour ce projet ?**

   - Pour les tests : **node:18-alpine** (légère et rapide)
   - Pour le build : **node:18-alpine** (même environnement cohérent)

3. **Quels artifacts doivent être conservés ?**
   - **node_modules/** (après installation, pour les autres jobs)
   - **dist/** (application buildée pour le déploiement)

### Fichier .gitlab-ci.yml complet

```yaml
# Configuration GitLab CI/CD pour application Node.js
# Couvre : installation, tests, build, déploiement GitLab Pages

stages:
  - install
  - test
  - build
  - deploy

# Variables globales
variables:
  NODE_VERSION: "18"
  CACHE_KEY: "$CI_COMMIT_REF_SLUG-node"

# Cache partagé pour optimiser les performances
cache:
  key: $CACHE_KEY
  paths:
    - node_modules/

# Job 1: Installation des dépendances
install_dependencies:
  stage: install
  image: node:18-alpine
  script:
    - echo "Installation des dépendances Node.js..."
    - npm ci --prefer-offline --no-audit
    - echo "Dépendances installées avec succès"
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour
  only:
    - branches

# Job 2: Exécution des tests
run_tests:
  stage: test
  image: node:18-alpine
  dependencies:
    - install_dependencies
  script:
    - echo "Exécution des tests unitaires..."
    - npm test
    - echo "Tests terminés avec succès"
  artifacts:
    reports:
      junit: junit.xml
    when: always
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  only:
    - branches

# Job 3: Build de l'application
build_app:
  stage: build
  image: node:18-alpine
  dependencies:
    - install_dependencies
  script:
    - echo "Construction de l'application..."
    - npm run build
    - echo "Build terminé, artefacts créés dans dist/"
    - ls -la dist/
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
  only:
    - branches

# Job 4: Déploiement GitLab Pages
pages:
  stage: deploy
  image: alpine:latest
  dependencies:
    - build_app
  script:
    - echo "Préparation du déploiement GitLab Pages..."
    # GitLab Pages attend un dossier 'public'
    - mkdir -p public
    - cp -r dist/* public/
    - echo "Application prête pour GitLab Pages"
    - ls -la public/
  artifacts:
    paths:
      - public
  only:
    - main

# Job 5: Tests de smoke (vérification post-déploiement)
smoke_tests:
  stage: deploy
  image: node:18-alpine
  dependencies:
    - build_app
  script:
    - echo "Tests de fumée (smoke tests)..."
    - node -e "const calc = require('./dist/calculator.js'); console.log('Test:', calc.add(2,3) === 5 ? 'PASS' : 'FAIL');"
    - echo "Tests de fumée terminés"
  only:
    - main
```

## Explications détaillées

### Structure du pipeline

1. **Stage install**

   - Installation des dépendances npm
   - Cache des node_modules pour optimiser les executions suivantes
   - Artifacts conservés 1 heure pour les jobs suivants

2. **Stage test**

   - Récupère les dépendances du job précédent
   - Exécute les tests Jest
   - Génère des rapports de couverture
   - S'exécute sur toutes les branches

3. **Stage build**

   - Construit l'application (copie fichiers dans dist/)
   - Artifacts conservés 1 semaine
   - Prépare les fichiers pour le déploiement

4. **Stage deploy**
   - **Job pages** : Déploie sur GitLab Pages (branche main uniquement)
   - **Job smoke_tests** : Tests de vérification post-déploiement

### Optimisations appliquées

- **Cache intelligent** : node_modules mis en cache par branche
- **Artifacts ciblés** : Seuls les fichiers nécessaires sont conservés
- **Images légères** : node:18-alpine pour rapidité
- **Conditions de branche** : Déploiement uniquement sur main
- **Parallélisme** : Tests de fumée en parallèle du déploiement

### Variables importantes

```yaml
variables:
  NODE_VERSION: '18' # Version Node.js cohérente
  CACHE_KEY: '$CI_COMMIT_REF_SLUG-node' # Clé de cache par branche
```

### Artifacts stratégiques

```yaml
# node_modules (installation → test/build)
artifacts:
  paths:
    - node_modules/
  expire_in: 1 hour

# Application buildée (build → deploy)
artifacts:
  paths:
    - dist/
  expire_in: 1 week

# Site GitLab Pages (deploy)
artifacts:
  paths:
    - public
```

## Version alternative avec Docker

Pour des environnements plus complexes :

```yaml
# Version avec build Docker (alternative)
build_docker:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  variables:
    DOCKER_TLS_CERTDIR: '/certs'
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

## Debugging courant

### Erreur : "npm: command not found"

**Cause** : Image Docker sans Node.js
**Solution** : Utiliser `image: node:18-alpine`

### Erreur : "Module not found"

**Cause** : Dependencies manquantes entre jobs
**Solution** : Ajouter `dependencies: [install_dependencies]`

### Erreur : "No such file or directory: dist/"

**Cause** : Script build échoue
**Solution** : Vérifier `npm run build` et création du dossier

### GitLab Pages ne fonctionne pas

**Cause** : Dossier `public` manquant ou job mal nommé
**Solution** : Job doit s'appeler `pages` et créer dossier `public/`

## Métriques de performance

Avec cette configuration optimisée :

- **Installation** : ~30-45 secondes
- **Tests** : ~15-20 secondes
- **Build** : ~10-15 secondes
- **Deploy** : ~20-30 secondes
- **Total** : ~1 minute 30 secondes

## Bonnes pratiques appliquées

1. **Séparation des responsabilités** : Chaque job a un rôle précis
2. **Gestion des dépendances** : Artifacts entre jobs
3. **Optimisation des performances** : Cache et images légères
4. **Conditions intelligentes** : Déploiement contrôlé par branche
5. **Rapports intégrés** : Tests et couverture dans GitLab
6. **Nommage cohérent** : Variables et jobs explicites

Cette configuration constitue une base solide pour des projets Node.js plus complexes !
