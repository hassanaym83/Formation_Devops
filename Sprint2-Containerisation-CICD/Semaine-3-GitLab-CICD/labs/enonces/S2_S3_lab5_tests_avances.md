# LAB 5 - Tests Avancés et Qualité de Code

## Contexte

Votre équipe DevOps souhaite améliorer la qualité du code et implémenter une stratégie de tests complète dans le pipeline GitLab CI/CD. Vous devez intégrer les tests unitaires, les tests d'intégration, les tests E2E, l'analyse de qualité de code, et les métriques de performance.

## Objectif

Implémenter une stratégie de tests complète avec analyse de qualité de code, tests End-to-End, et métriques de performance dans GitLab CI/CD.

## Prérequis

- LAB 4 complété (intégration Docker)
- Connaissances Jest, Cypress, SonarQube
- Application React avec tests existants

## Instructions détaillées

### Étape 1 : Configuration des tests avancés (12 minutes)

1. **Installer les dépendances de test** :

```bash
# Tests E2E avec Cypress
npm install --save-dev cypress @cypress/code-coverage cypress-multi-reporters
npm install --save-dev mocha mochawesome mochawesome-merge mochawesome-report-generator

# Analyse de qualité de code
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier

# Tests de performance
npm install --save-dev lighthouse puppeteer

# Coverage et reporting
npm install --save-dev nyc babel-plugin-istanbul
```

2. **Créer la configuration Cypress** `cypress.config.js` :

```javascript
const {defineConfig} = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    video: true,
    screenshot: true,
    screenshotOnRunFailure: true,
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    setupNodeEvents(on, config) {
      // Coverage plugin
      require('@cypress/code-coverage/task')(on, config);

      // Custom tasks
      on('task', {
        log(message) {
          console.log(message);
          return null;
        }
      });

      return config;
    }
  },
  component: {
    devServer: {
      framework: 'create-react-app',
      bundler: 'webpack'
    }
  },
  reporter: 'cypress-multi-reporters',
  reporterOptions: {
    configFile: 'cypress-reporter-config.json'
  }
});
```

3. **Configuration des reporters** `cypress-reporter-config.json` :

```json
{
  "reporterEnabled": "mochawesome",
  "mochawesomeReporterOptions": {
    "reportDir": "cypress/reports/mocha",
    "quite": true,
    "overwrite": false,
    "html": false,
    "json": true,
    "timestamp": "mmddyyyy_HHMMss"
  }
}
```

4. **Créer les tests E2E** `cypress/e2e/app.cy.js` :

```javascript
describe('Demo React App E2E Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  describe('Page Load Tests', () => {
    it('should load the homepage successfully', () => {
      cy.get('body').should('be.visible');
      cy.title().should('contain', 'React App');
    });

    it('should display main content', () => {
      cy.get('[data-testid="main-content"]', {timeout: 10000}).should(
        'be.visible'
      );
      cy.get('header').should('contain.text', 'Welcome');
    });
  });

  describe('Navigation Tests', () => {
    it('should navigate between pages', () => {
      cy.get('[data-testid="nav-about"]').click();
      cy.url().should('include', '/about');
      cy.get('h1').should('contain', 'About');
    });

    it('should handle 404 pages gracefully', () => {
      cy.visit('/non-existent-page', {failOnStatusCode: false});
      cy.get('body').should('contain', '404');
    });
  });

  describe('Performance Tests', () => {
    it('should load within acceptable time', () => {
      const start = Date.now();
      cy.visit('/').then(() => {
        const loadTime = Date.now() - start;
        expect(loadTime).to.be.lessThan(3000); // 3 seconds max
      });
    });

    it('should have good Lighthouse scores', () => {
      cy.task('lighthouse', {
        url: 'http://localhost:3000',
        options: {
          formFactor: 'desktop',
          screenEmulation: {disabled: true}
        }
      }).then((results) => {
        expect(results.performance).to.be.greaterThan(80);
        expect(results.accessibility).to.be.greaterThan(90);
        expect(results.bestPractices).to.be.greaterThan(80);
        expect(results.seo).to.be.greaterThan(80);
      });
    });
  });

  describe('Responsive Design Tests', () => {
    const viewports = [
      {device: 'iphone-6', width: 375, height: 667},
      {device: 'ipad-2', width: 768, height: 1024},
      {device: 'macbook-15', width: 1440, height: 900}
    ];

    viewports.forEach(({device, width, height}) => {
      it(`should work on ${device}`, () => {
        cy.viewport(width, height);
        cy.visit('/');
        cy.get('body').should('be.visible');
        cy.get('[data-testid="main-content"]').should('be.visible');
      });
    });
  });

  describe('Accessibility Tests', () => {
    it('should have proper ARIA attributes', () => {
      cy.get('[role="main"]').should('exist');
      cy.get('[role="navigation"]').should('exist');
    });

    it('should support keyboard navigation', () => {
      cy.get('body').type('{tab}');
      cy.focused().should('have.attr', 'data-testid', 'nav-home');
    });
  });
});
```

5. **Configuration ESLint** `.eslintrc.js` :

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
    'cypress/globals': true
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier'
  ],
  plugins: ['react', 'react-hooks', 'cypress', 'prettier'],
  parserOptions: {
    ecmaFeatures: {
      jsx: true
    },
    ecmaVersion: 12,
    sourceType: 'module'
  },
  rules: {
    'prettier/prettier': 'error',
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    'no-unused-vars': ['error', {argsIgnorePattern: '^_'}],
    'no-console': 'warn',
    'no-debugger': 'error',
    complexity: ['error', 10],
    'max-depth': ['error', 4],
    'max-lines': ['error', 300],
    'max-params': ['error', 5]
  },
  settings: {
    react: {
      version: 'detect'
    }
  }
};
```

### Étape 2 : Pipeline avec tests avancés (15 minutes)

1. **Mettre à jour `.gitlab-ci.yml`** :

```yaml
# Pipeline GitLab CI/CD avec tests avancés et qualité de code
image: node:18-alpine

# Services pour tests
services:
  - docker:24.0.5-dind
  - name: sonarqube:9.9-community
    alias: sonarqube

# Variables globales
variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_TLS_CERTDIR: ''
  SONAR_USER_HOME: '${CI_PROJECT_DIR}/.sonar'
  GIT_DEPTH: '0'
  npm_config_cache: '$CI_PROJECT_DIR/.npm'

stages:
  - validate
  - install
  - lint
  - test-unit
  - test-integration
  - test-e2e
  - quality-analysis
  - build
  - docker-build
  - deploy

# Cache optimisé
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
    - .npm/
    - .sonar/cache

# Installation des dépendances
install_dependencies:
  stage: install
  script:
    - echo "📦 Installation des dépendances"
    - npm ci --cache .npm --prefer-offline
    - echo "📊 Audit de sécurité"
    - npm audit --audit-level=high
    - echo "✅ Installation terminée"
  artifacts:
    paths:
      - node_modules/
    expire_in: 2 hours
  only:
    - main
    - develop
    - merge_requests

# Linting et formatage
lint_code:
  stage: lint
  script:
    - echo "🔍 Analyse du code avec ESLint"
    - npx eslint src/ --ext .js,.jsx,.ts,.tsx --format gitlab --output-file eslint-report.json
    - echo "🎨 Vérification du formatage avec Prettier"
    - npx prettier --check src/
    - echo "✅ Linting terminé"
  artifacts:
    reports:
      codequality: eslint-report.json
    paths:
      - eslint-report.json
    expire_in: 1 week
  dependencies:
    - install_dependencies
  allow_failure: false
  only:
    - main
    - develop
    - merge_requests

# Tests unitaires avancés
test_unit_advanced:
  stage: test-unit
  script:
    - echo "🧪 Tests unitaires avec couverture détaillée"
    - npm test -- --coverage --coverageReporters=text-lcov --coverageReporters=json --coverageReporters=html --watchAll=false --verbose
    - echo "📊 Analyse de la couverture"
    - npx nyc report --reporter=text-summary
    - echo "✅ Tests unitaires terminés"
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
      junit: coverage/junit.xml
    paths:
      - coverage/
    expire_in: 1 week
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests

# Tests d'intégration
test_integration:
  stage: test-integration
  services:
    - name: postgres:13-alpine
      alias: postgres
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
    DATABASE_URL: postgresql://testuser:testpass@postgres:5432/testdb
  script:
    - echo "🔗 Tests d'intégration"
    - echo "🗄️ Attente de la base de données"
    - sleep 10
    - echo "🧪 Exécution des tests d'intégration"
    - npm run test:integration || echo "Tests d'intégration à implémenter"
    - echo "✅ Tests d'intégration terminés"
  artifacts:
    reports:
      junit: integration-test-results.xml
    paths:
      - integration-test-results.xml
    expire_in: 1 week
  dependencies:
    - install_dependencies
  allow_failure: true
  only:
    - main
    - develop
    - merge_requests

# Tests End-to-End
test_e2e:
  stage: test-e2e
  image: cypress/included:13.6.0
  variables:
    CYPRESS_CACHE_FOLDER: '$CI_PROJECT_DIR/cache/Cypress'
  before_script:
    - echo "🚀 Préparation des tests E2E"
    - npm ci --cache .npm
    - echo "🌐 Démarrage de l'application en arrière-plan"
    - npm start &
    - sleep 30
    - echo "🔍 Vérification que l'app est démarrée"
    - curl -f http://localhost:3000 || (echo "❌ App non démarrée" && exit 1)
  script:
    - echo "🎭 Exécution des tests E2E avec Cypress"
    - npx cypress run --browser chrome --headless --reporter mochawesome
    - echo "📊 Génération du rapport E2E"
    - npx mochawesome-merge cypress/reports/mocha/*.json > cypress/reports/report.json
    - npx marge cypress/reports/report.json --reportDir cypress/reports/html
    - echo "✅ Tests E2E terminés"
  artifacts:
    when: always
    paths:
      - cypress/screenshots/
      - cypress/videos/
      - cypress/reports/
    reports:
      junit: cypress/reports/junit/*.xml
    expire_in: 1 week
  dependencies:
    - install_dependencies
  cache:
    key: cypress-cache
    paths:
      - cache/Cypress/
  only:
    - main
    - develop
    - merge_requests

# Analyse de qualité avec SonarQube
quality_analysis:
  stage: quality-analysis
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - echo "📊 Analyse de qualité avec SonarQube"
    - |
      sonar-scanner \
        -Dsonar.projectKey=${CI_PROJECT_NAME} \
        -Dsonar.sources=src/ \
        -Dsonar.tests=src/ \
        -Dsonar.test.inclusions="**/*.test.js,**/*.test.jsx,**/*.spec.js" \
        -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info \
        -Dsonar.eslint.reportPaths=eslint-report.json \
        -Dsonar.coverage.exclusions="**/*.test.js,**/*.spec.js,**/node_modules/**" \
        -Dsonar.host.url=http://sonarqube:9000 \
        -Dsonar.login=admin \
        -Dsonar.password=admin
    - echo "✅ Analyse de qualité terminée"
  dependencies:
    - test_unit_advanced
    - lint_code
  cache:
    key: sonar-cache
    paths:
      - .sonar/cache
  allow_failure: true
  only:
    - main
    - develop
    - merge_requests

# Build avec métriques
build_with_metrics:
  stage: build
  script:
    - echo "🏗️ Build avec analyse des métriques"
    - npm run build
    - echo "📊 Analyse de la taille du bundle"
    - npx bundlesize
    - echo "🔍 Analyse des dépendances"
    - npx depcheck
    - echo "📈 Génération du rapport de build"
    - du -sh build/*
    - find build/ -name "*.js" -exec ls -lh {} \; | sort -k5 -hr | head -10
    - echo "✅ Build avec métriques terminé"
  artifacts:
    paths:
      - build/
      - build-metrics.json
    reports:
      performance: build-metrics.json
    expire_in: 1 day
  dependencies:
    - install_dependencies
  only:
    - main
    - develop
    - merge_requests
```

### Étape 3 : Configuration des métriques (3 minutes)

1. **Ajouter scripts package.json** :

```json
{
  "scripts": {
    "test:integration": "jest --config=jest.integration.config.js",
    "test:e2e": "cypress run",
    "test:e2e:open": "cypress open",
    "lint": "eslint src/ --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src/ --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write src/",
    "quality": "npm run lint && npm run test -- --coverage",
    "analyze": "npm run build && npx bundlesize"
  }
}
```

2. **Configuration bundlesize** dans `package.json` :

```json
{
  "bundlesize": [
    {
      "path": "build/static/js/*.js",
      "maxSize": "500 kB",
      "compression": "gzip"
    },
    {
      "path": "build/static/css/*.css",
      "maxSize": "50 kB",
      "compression": "gzip"
    }
  ]
}
```

## Livrables attendus

### 1. Configuration de tests complète

- Tests E2E avec Cypress fonctionnels
- Configuration ESLint et Prettier
- Tests d'intégration avec base de données
- Métriques de performance et bundle

### 2. Pipeline avec qualité de code

- Analyse SonarQube intégrée
- Rapports de couverture détaillés
- Tests automatisés à tous les niveaux
- Métriques de qualité et performance

### 3. Documentation qualité

Créer `quality_strategy.md` avec :

- Stratégie de tests complète
- Métriques de qualité utilisées
- Seuils de qualité définis
- Processus d'amélioration continue

## Critères d'évaluation

**Total : 25 points**

- **Tests E2E fonctionnels (8 points)** : Cypress configuré et tests qui passent
- **Qualité de code (8 points)** : ESLint, Prettier, SonarQube configurés
- **Pipeline complet (6 points)** : Tous les stages de test fonctionnent
- **Documentation (3 points)** : Stratégie de qualité bien documentée

## Durée estimée

**30 minutes** réparties :

- Configuration tests : 12 minutes
- Pipeline avancé : 15 minutes
- Métriques et validation : 3 minutes

## Conseils

- Commencer par configurer Cypress sur un test simple
- Ajuster les seuils de qualité progressivement
- Utiliser les rapports pour identifier les points d'amélioration
- Automatiser la correction des problèmes de formatage

## Ressources

- [Cypress Documentation](https://docs.cypress.io/)
- [ESLint Configuration](https://eslint.org/docs/user-guide/configuring/)
- [SonarQube Integration](https://docs.sonarqube.org/latest/analysis/gitlab-integration/)
