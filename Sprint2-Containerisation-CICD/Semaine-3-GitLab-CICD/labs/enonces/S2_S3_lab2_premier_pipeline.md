# LAB 2 - Premier pipeline React

## Contexte

Votre équipe DevOps a développé une application React (demo-deploy-react-app) pour démontrer les concepts GitLab CI/CD. Vous devez maintenant créer et configurer le premier pipeline GitLab CI/CD pour automatiser le build, les tests et le déploiement de cette application.

## Objectif

Configurer un pipeline complet build/test/deploy pour une application React en utilisant GitLab CI/CD avec optimisations cache et artifacts.

## Prérequis

- Compte GitLab.com actif
- Application demo-deploy-react-app créée précédemment
- Connaissances de base React et npm

## Instructions détaillées

### Étape 1 : Création projet GitLab (8 minutes)

1. **Créer nouveau projet** :

   - Aller sur GitLab.com
   - Cliquer "New project" → "Create blank project"
   - Nom : `demo-deploy-react-app-cicd`
   - Visibilité : Public
   - Initialiser avec README

2. **Upload code existant** :

   - Télécharger le code demo-deploy-react-app local
   - Utiliser l'interface GitLab pour upload des fichiers
   - Ou cloner et push si Git configuré

3. **Vérifier structure** :
   ```
   demo-deploy-react-app-cicd/
   ├── package.json
   ├── public/
   ├── src/
   ├── README.md
   └── .gitignore
   ```

### Étape 2 : Configuration pipeline de base (12 minutes)

1. **Créer fichier `.gitlab-ci.yml`** à la racine :

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
    - echo "Installation des dépendances npm"
    - npm ci --cache .npm --prefer-offline
    - echo "Dépendances installées avec succès"
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
    - echo "Construction de l'application React"
    - npm run build
    - echo "Build terminé avec succès"
    - ls -la build/
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
    - echo "Exécution des tests unitaires"
    - npm test -- --coverage --watchAll=false
    - echo "Tests terminés"
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
    - echo "Déploiement vers l'environnement staging"
    - echo "URL de staging: https://staging-demo-react-app.example.com"
    - echo "Simulation déploiement staging réussi"
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
    - echo "Déploiement vers l'environnement production"
    - echo "URL de production: https://demo-react-app.example.com"
    - echo "Simulation déploiement production réussi"
  environment:
    name: production
    url: https://demo-react-app.example.com
  dependencies:
    - build_application
  only:
    - main
  when: manual
```

### Étape 3 : Optimisation et test pipeline (10 minutes)

1. **Commit et push** :

   - Committer le fichier `.gitlab-ci.yml`
   - Message : "Add GitLab CI/CD pipeline with 4 stages"
   - Pusher vers la branche main

2. **Observer exécution** :

   - Aller dans CI/CD → Pipelines
   - Cliquer sur le pipeline en cours
   - Observer chaque job en temps réel
   - Noter les durées et artifacts

3. **Analyser résultats** :
   - Vérifier que tous les jobs passent
   - Télécharger artifacts build/
   - Examiner rapport de couverture
   - Tester déploiement manuel staging

## Livrables attendus

### 1. Fichier .gitlab-ci.yml fonctionnel

Avec les caractéristiques :

- 4 stages : install, build, test, deploy
- 5 jobs configurés correctement
- Cache npm optimisé
- Artifacts pour build et coverage
- Environments staging et production

### 2. Pipeline réussi

Capturer :

- Screenshot du pipeline complet avec tous jobs verts
- Durée totale d'exécution
- Artifacts générés et téléchargés

### 3. Document analyse

Créer `pipeline_analysis.md` avec :

- Configuration utilisée et justifications
- Optimisations implémentées (cache, artifacts)
- Problèmes rencontrés et solutions
- Améliorations possibles identifiées

## Critères d'évaluation

**Total : 20 points**

- **Pipeline fonctionnel (10 points)** : 4 jobs réussissent sans erreur
- **Configuration optimisée (5 points)** : Cache et artifacts correctement configurés
- **Environments (3 points)** : Staging et production configurés avec URLs
- **Documentation (2 points)** : Analyse complète et structurée

## Durée estimée

**30 minutes** réparties :

- Création projet : 8 minutes
- Configuration pipeline : 12 minutes
- Test et optimisation : 10 minutes

## Conseils

- Tester le pipeline par étapes (commit fréquents)
- Utiliser les logs pour debugger les erreurs
- Optimiser le cache pour accélérer les builds
- Vérifier que les artifacts sont bien générés

## Ressources

- [GitLab CI/CD YAML Reference](https://docs.gitlab.com/ee/ci/yaml/)
- [React Build Documentation](https://create-react-app.dev/docs/production-build/)
- [GitLab Artifacts Documentation](https://docs.gitlab.com/ee/ci/pipelines/job_artifacts.html)
