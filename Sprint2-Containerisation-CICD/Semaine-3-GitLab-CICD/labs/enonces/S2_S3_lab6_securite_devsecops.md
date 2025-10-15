# LAB 6 - Sécurité DevSecOps

## Contexte

Votre équipe DevOps doit implémenter une stratégie de sécurité complète (DevSecOps) dans le pipeline GitLab CI/CD. Vous devez intégrer l'analyse de sécurité statique (SAST), dynamique (DAST), la gestion sécurisée des secrets, et assurer la conformité aux standards de sécurité.

## Objectif

Implémenter une stratégie DevSecOps complète avec SAST, DAST, gestion des secrets avancée, analyse des dépendances, et conformité sécuritaire dans GitLab CI/CD.

## Prérequis

- LAB 5 complété (tests avancés)
- Connaissances en sécurité applicative
- Accès GitLab Ultimate ou outils de sécurité open source

## Instructions détaillées

### Étape 1 : Configuration des outils de sécurité (10 minutes)

1. **Installer les dépendances de sécurité** :

```bash
# Analyse de sécurité statique
npm install --save-dev eslint-plugin-security @typescript-eslint/eslint-plugin-tslint

# Analyse des dépendances
npm install --save-dev audit-ci retire

# Tests de sécurité
npm install --save-dev helmet express-rate-limit

# Outils de scan
npm install --save-dev snyk @snyk/protect
```

2. **Configuration ESLint sécurisé** `.eslintrc.security.js` :

```javascript
module.exports = {
  extends: ['.eslintrc.js'],
  plugins: ['security'],
  rules: {
    // Règles de sécurité strictes
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'error',
    'security/detect-non-literal-fs-filename': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-pseudoRandomBytes': 'error',
    'security/detect-possible-timing-attacks': 'warn',
    'security/detect-unsafe-regex': 'error',
    'security/detect-buffer-noassert': 'error',
    'security/detect-child-process': 'error',
    'security/detect-disable-mustache-escape': 'error',
    'security/detect-no-csrf-before-method-override': 'error',
    'security/detect-non-literal-require': 'error',

    // Règles additionnelles de sécurité
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',
    'no-inline-comments': 'off',
    'no-mixed-spaces-and-tabs': 'error'
  },
  env: {
    node: true,
    browser: true
  }
};
```

3. **Configuration Snyk** `.snyk` :

```yaml
# Snyk (https://snyk.io) policy file
version: v1.0.0
ignore: {}
language-settings:
  javascript:
    # Ignorer les dépendances de développement pour les vulnérabilités de faible priorité
    ignoreDevDependencies: true
patch: {}
```

4. **Script de sécurité** `scripts/security-check.sh` :

```bash
#!/bin/bash
set -e

echo "🔒 === VÉRIFICATION DE SÉCURITÉ COMPLÈTE ==="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction de logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Vérification des secrets dans le code
log_info "🔍 Recherche de secrets dans le code"
if command -v git-secrets >/dev/null 2>&1; then
    git-secrets --scan || {
        log_error "Secrets détectés dans le code"
        exit 1
    }
else
    log_warn "git-secrets non installé, vérification manuelle"
    # Recherche basique de patterns suspects
    if grep -r -E "(password|secret|key|token).*=.*['\"][^'\"]*['\"]" src/ 2>/dev/null; then
        log_error "Patterns suspects détectés"
        exit 1
    fi
fi

# 2. Audit des dépendances npm
log_info "📦 Audit des dépendances npm"
npm audit --audit-level=high --production

# 3. Vérification avec Snyk
log_info "🐍 Analyse Snyk"
if command -v snyk >/dev/null 2>&1; then
    snyk test --severity-threshold=high || {
        log_error "Vulnérabilités critiques détectées par Snyk"
        exit 1
    }
else
    log_warn "Snyk CLI non installé"
fi

# 4. Analyse statique avec ESLint sécurisé
log_info "🔍 Analyse statique de sécurité"
npx eslint src/ --config .eslintrc.security.js --ext .js,.jsx,.ts,.tsx

# 5. Vérification des permissions des fichiers
log_info "📁 Vérification des permissions"
find . -type f -perm -002 -not -path "./node_modules/*" -not -path "./.git/*" | while read file; do
    log_warn "Fichier avec permissions d'écriture globale: $file"
done

# 6. Vérification de la configuration Docker
if [ -f "Dockerfile" ]; then
    log_info "🐳 Vérification sécurité Docker"

    # Vérification utilisateur non-root
    if ! grep -q "USER.*[^0]" Dockerfile; then
        log_error "Dockerfile utilise l'utilisateur root"
        exit 1
    fi

    # Vérification des secrets hardcodés
    if grep -i -E "(password|secret|key|token)" Dockerfile; then
        log_error "Secrets potentiels dans Dockerfile"
        exit 1
    fi
fi

log_info "✅ Vérification de sécurité terminée"
```

### Étape 2 : Pipeline de sécurité GitLab (18 minutes)

1. **Créer `.gitlab-ci-security.yml`** :

```yaml
# Pipeline GitLab CI/CD avec sécurité DevSecOps
include:
  # Templates GitLab pour la sécurité
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/DAST.gitlab-ci.yml

# Variables de sécurité
variables:
  # SAST
  SAST_EXCLUDED_ANALYZERS: 'gosec'
  SAST_EXCLUDED_PATHS: 'node_modules, coverage, build'

  # Secret Detection
  SECRET_DETECTION_EXCLUDED_PATHS: 'node_modules, coverage'

  # Dependency Scanning
  DS_EXCLUDED_ANALYZERS: 'retire-js'
  DS_EXCLUDED_PATHS: 'node_modules'

  # Container Scanning
  CS_MAJOR_VERSION: 4
  CS_ANALYZER_IMAGE: '$CI_TEMPLATE_REGISTRY_HOST/security-products/container-scanning:$CS_MAJOR_VERSION'

  # DAST
  DAST_WEBSITE: 'http://localhost:3000'
  DAST_FULL_SCAN_ENABLED: 'true'

stages:
  - validate
  - security-static
  - build
  - security-dynamic
  - deploy

# Template pour jobs de sécurité
.security_job_template: &security_job
  allow_failure: false
  artifacts:
    reports:
      security: gl-*.json
    expire_in: 1 week

# Validation sécurisée du code
security_code_validation:
  stage: validate
  image: node:18-alpine
  before_script:
    - apk add --no-cache git bash curl
    - chmod +x scripts/security-check.sh
  script:
    - echo "🔒 === VALIDATION SÉCURISÉE DU CODE ==="
    - echo "🔍 Recherche de secrets hardcodés"
    - |
      # Recherche de patterns de secrets
      secret_patterns=(
        "password\s*=\s*['\"][^'\"]*['\"]"
        "secret\s*=\s*['\"][^'\"]*['\"]"
        "api_?key\s*=\s*['\"][^'\"]*['\"]"
        "token\s*=\s*['\"][^'\"]*['\"]"
        "auth\s*=\s*['\"][^'\"]*['\"]"
        "-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----"
      )

      for pattern in "${secret_patterns[@]}"; do
        if grep -r -E "$pattern" src/ 2>/dev/null; then
          echo "❌ Pattern suspect détecté: $pattern"
          exit 1
        fi
      done
      echo "✅ Aucun secret hardcodé détecté"

    - echo "🔧 Vérification de la configuration sécurisée"
    - |
      # Vérification des en-têtes de sécurité dans le code
      required_headers=(
        "X-Content-Type-Options"
        "X-Frame-Options"
        "X-XSS-Protection"
        "Strict-Transport-Security"
      )

      for header in "${required_headers[@]}"; do
        if ! grep -r "$header" src/ nginx.conf* 2>/dev/null; then
          echo "⚠️ En-tête de sécurité manquant: $header"
        fi
      done

    - echo "🛡️ Exécution du script de sécurité personnalisé"
    - ./scripts/security-check.sh
    - echo "✅ Validation sécurisée terminée"
  only:
    - main
    - develop
    - merge_requests

# SAST personnalisé avec ESLint sécurisé
sast_eslint_security:
  stage: security-static
  image: node:18-alpine
  <<: *security_job
  script:
    - echo "🔍 === ANALYSE SAST AVEC ESLINT SÉCURISÉ ==="
    - npm ci --prefer-offline
    - |
      npx eslint src/ \
        --config .eslintrc.security.js \
        --ext .js,.jsx,.ts,.tsx \
        --format json \
        --output-file eslint-security-report.json
    - echo "📊 Analyse des résultats"
    - |
      if [ -f eslint-security-report.json ]; then
        security_issues=$(jq '[.[].messages[] | select(.ruleId | startswith("security/"))] | length' eslint-security-report.json)
        echo "Issues de sécurité détectés: $security_issues"
        if [ "$security_issues" -gt 0 ]; then
          echo "❌ Issues de sécurité critiques détectés"
          jq '[.[].messages[] | select(.ruleId | startswith("security/"))]' eslint-security-report.json
          exit 1
        fi
      fi
    - echo "✅ SAST ESLint réussi"
  artifacts:
    paths:
      - eslint-security-report.json
    reports:
      codequality: eslint-security-report.json
  only:
    - main
    - develop
    - merge_requests

# Analyse des dépendances avec multiples outils
dependency_security_scan:
  stage: security-static
  image: node:18-alpine
  <<: *security_job
  before_script:
    - apk add --no-cache python3 py3-pip
    - npm install -g audit-ci retire snyk
  script:
    - echo "📦 === ANALYSE DE SÉCURITÉ DES DÉPENDANCES ==="
    - npm ci --prefer-offline

    - echo "🔍 Audit npm avec audit-ci"
    - audit-ci --config .auditcirc.json

    - echo "🔍 Analyse avec Retire.js"
    - retire --js --outputformat json --outputpath retire-report.json src/ || echo "Retire scan terminé"

    - echo "🐍 Analyse avec Snyk"
    - snyk test --json > snyk-report.json || echo "Snyk scan terminé"

    - echo "📊 Consolidation des rapports"
    - |
      # Création d'un rapport consolidé
      cat > dependency-security-report.json << EOF
      {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "tools": {
          "npm_audit": "$(npm audit --json | jq -c .)",
          "retire": "$(cat retire-report.json 2>/dev/null || echo '{}')",
          "snyk": "$(cat snyk-report.json 2>/dev/null || echo '{}')"
        }
      }
      EOF

    - echo "✅ Analyse des dépendances terminée"
  artifacts:
    paths:
      - dependency-security-report.json
      - retire-report.json
      - snyk-report.json
    reports:
      dependency_scanning: dependency-security-report.json
  only:
    - main
    - develop
    - merge_requests

# Scan de sécurité des containers
container_security_scan:
  stage: security-static
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  <<: *security_job
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    # Installation de Trivy
    - apk add --no-cache curl
    - |
      curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
  script:
    - echo "🐳 === SCAN DE SÉCURITÉ DES CONTAINERS ==="
    - IMAGE_NAME="$CI_REGISTRY_IMAGE/demo-react-app:$CI_COMMIT_SHORT_SHA"
    - echo "🔍 Scan de l'image: $IMAGE_NAME"

    - echo "📥 Pull de l'image"
    - docker pull "$IMAGE_NAME"

    - echo "🔍 Scan Trivy - Vulnérabilités OS"
    - |
      trivy image \
        --format json \
        --output trivy-os-report.json \
        --vuln-type os \
        --severity HIGH,CRITICAL \
        "$IMAGE_NAME"

    - echo "🔍 Scan Trivy - Vulnérabilités librairies"
    - |
      trivy image \
        --format json \
        --output trivy-lib-report.json \
        --vuln-type library \
        --severity HIGH,CRITICAL \
        "$IMAGE_NAME"

    - echo "🔍 Scan de configuration"
    - |
      trivy config \
        --format json \
        --output trivy-config-report.json \
        .

    - echo "📊 Analyse des résultats"
    - |
      # Compter les vulnérabilités critiques
      critical_vulns=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length' trivy-os-report.json)
      high_vulns=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH")] | length' trivy-lib-report.json)

      echo "Vulnérabilités critiques: $critical_vulns"
      echo "Vulnérabilités élevées: $high_vulns"

      if [ "$critical_vulns" -gt 0 ]; then
        echo "❌ Vulnérabilités critiques détectées"
        exit 1
      fi

    - echo "✅ Scan de sécurité des containers terminé"
  artifacts:
    paths:
      - trivy-*-report.json
    reports:
      container_scanning: trivy-os-report.json
  needs:
    - job: docker_build
      optional: true
  only:
    - main
    - develop
    - merge_requests

# Tests de sécurité applicative
security_application_tests:
  stage: security-static
  image: node:18-alpine
  <<: *security_job
  script:
    - echo "🛡️ === TESTS DE SÉCURITÉ APPLICATIVE ==="
    - npm ci --prefer-offline

    - echo "🔍 Tests de sécurité des API"
    - |
      # Création de tests de sécurité basiques
      cat > security-tests.js << 'EOF'
      const http = require('http');
      const assert = require('assert');

      // Test des en-têtes de sécurité
      function testSecurityHeaders(url) {
        return new Promise((resolve, reject) => {
          http.get(url, (res) => {
            const headers = res.headers;
            const requiredHeaders = [
              'x-content-type-options',
              'x-frame-options',
              'x-xss-protection'
            ];
            
            const missing = requiredHeaders.filter(h => !headers[h]);
            if (missing.length > 0) {
              reject(new Error(`En-têtes manquants: ${missing.join(', ')}`));
            } else {
              resolve('Headers OK');
            }
          }).on('error', reject);
        });
      }

      // Test des endpoints sensibles
      function testSensitiveEndpoints(baseUrl) {
        const sensitiveEndpoints = [
          '/admin',
          '/.env',
          '/config',
          '/secret',
          '/.git'
        ];
        
        return Promise.all(sensitiveEndpoints.map(endpoint => {
          return new Promise((resolve) => {
            http.get(baseUrl + endpoint, (res) => {
              if (res.statusCode === 200) {
                resolve(`DANGER: ${endpoint} accessible`);
              } else {
                resolve(`OK: ${endpoint} protégé`);
              }
            }).on('error', () => resolve(`OK: ${endpoint} non accessible`));
          });
        }));
      }

      module.exports = { testSecurityHeaders, testSensitiveEndpoints };
      EOF

    - echo "🧪 Exécution des tests de sécurité"
    - node -e "
      const { testSensitiveEndpoints } = require('./security-tests.js');
      testSensitiveEndpoints('http://localhost:3000')
      .then(results => {
      results.forEach(r => console.log(r));
      const dangers = results.filter(r => r.startsWith('DANGER'));
      if (dangers.length > 0) {
      console.log('❌ Endpoints sensibles exposés');
      process.exit(1);
      }
      console.log('✅ Tests de sécurité réussis');
      })
      .catch(err => {
      console.log('ℹ️ Tests de sécurité partiels:', err.message);
      });
      "

    - echo "✅ Tests de sécurité applicative terminés"
  only:
    - main
    - develop
    - merge_requests

# DAST avec OWASP ZAP
dast_owasp_zap:
  stage: security-dynamic
  image: owasp/zap2docker-stable:latest
  variables:
    website: 'http://localhost:3000'
  <<: *security_job
  before_script:
    - echo "🚀 Démarrage de l'application pour DAST"
    # L'application doit être démarrée dans un autre service ou job
  script:
    - echo "🕷️ === ANALYSE DAST AVEC OWASP ZAP ==="
    - |
      # Scan baseline OWASP ZAP
      zap-baseline.py -t $website \
        -J zap-baseline-report.json \
        -r zap-baseline-report.html \
        -x zap-baseline-report.xml \
        -a \
        -j \
        -l PASS \
        -i \
        || echo "DAST scan terminé avec warnings"

    - echo "🕷️ Scan complet OWASP ZAP"
    - |
      zap-full-scan.py -t $website \
        -J zap-full-report.json \
        -r zap-full-report.html \
        -x zap-full-report.xml \
        -a \
        -j \
        -l PASS \
        -T 10 \
        || echo "DAST full scan terminé avec warnings"

    - echo "📊 Analyse des résultats DAST"
    - |
      if [ -f zap-baseline-report.json ]; then
        high_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("High"))' zap-baseline-report.json | wc -l)
        medium_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("Medium"))' zap-baseline-report.json | wc -l)
        
        echo "Risques élevés: $high_risks"
        echo "Risques moyens: $medium_risks"
        
        if [ "$high_risks" -gt 0 ]; then
          echo "❌ Vulnérabilités DAST critiques détectées"
          exit 1
        fi
      fi

    - echo "✅ Analyse DAST terminée"
  artifacts:
    paths:
      - zap-*-report.*
    reports:
      dast: zap-baseline-report.json
  needs:
    - job: deploy_staging_docker
      optional: true
  when: manual
  only:
    - main
    - develop

# Rapport de sécurité consolidé
security_report:
  stage: security-dynamic
  image: node:18-alpine
  script:
    - echo "📊 === GÉNÉRATION DU RAPPORT DE SÉCURITÉ CONSOLIDÉ ==="
    - apk add --no-cache jq
    - |
      # Création du rapport consolidé
      cat > security-consolidated-report.json << EOF
      {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "commit": "$CI_COMMIT_SHA",
        "pipeline": "$CI_PIPELINE_ID",
        "branch": "$CI_COMMIT_REF_NAME",
        "security_scans": {
          "sast": {
            "eslint_security": "$(test -f eslint-security-report.json && echo 'completed' || echo 'skipped')",
            "gitlab_sast": "$(test -f gl-sast-report.json && echo 'completed' || echo 'skipped')"
          },
          "dependency_scanning": {
            "npm_audit": "completed",
            "snyk": "$(test -f snyk-report.json && echo 'completed' || echo 'skipped')",
            "retire": "$(test -f retire-report.json && echo 'completed' || echo 'skipped')"
          },
          "container_scanning": {
            "trivy": "$(test -f trivy-os-report.json && echo 'completed' || echo 'skipped')"
          },
          "dast": {
            "owasp_zap": "$(test -f zap-baseline-report.json && echo 'completed' || echo 'skipped')"
          },
          "secret_detection": {
            "gitlab": "$(test -f gl-secret-detection-report.json && echo 'completed' || echo 'skipped')"
          }
        }
      }
      EOF

    - echo "📈 Métriques de sécurité"
    - |
      echo "=== RÉSUMÉ SÉCURITÉ ==="
      echo "🔍 SAST: Analyse statique du code"
      echo "📦 Dependency Scanning: Analyse des dépendances"
      echo "🐳 Container Scanning: Scan des images Docker"
      echo "🕷️ DAST: Tests dynamiques"
      echo "🔒 Secret Detection: Détection de secrets"

      cat security-consolidated-report.json | jq '.'

    - echo "✅ Rapport de sécurité consolidé généré"
  artifacts:
    paths:
      - security-consolidated-report.json
    reports:
      security: security-consolidated-report.json
    expire_in: 30 days
  needs:
    - job: sast_eslint_security
      artifacts: true
      optional: true
    - job: dependency_security_scan
      artifacts: true
      optional: true
    - job: container_security_scan
      artifacts: true
      optional: true
    - job: dast_owasp_zap
      artifacts: true
      optional: true
  when: always
  only:
    - main
    - develop
    - merge_requests
```

### Étape 3 : Configuration avancée et tests (2 minutes)

1. **Configuration audit-ci** `.auditcirc.json` :

```json
{
  "low": true,
  "moderate": true,
  "high": false,
  "critical": false,
  "report-type": "full",
  "allowlist": [],
  "skip-dev": false,
  "show-found": true,
  "show-not-found": false,
  "retry": {
    "count": 5,
    "factor": 2,
    "minTimeout": 1000,
    "maxTimeout": 60000,
    "randomize": true
  }
}
```

2. **Intégration avec le pipeline principal** dans `.gitlab-ci.yml` :

```yaml
# Ajout à .gitlab-ci.yml existant
include:
  - local: '.gitlab-ci-security.yml'

# Nouveaux stages
stages:
  - validate
  - security-static
  - install
  - lint
  - test-unit
  - test-integration
  - test-e2e
  - quality-analysis
  - build
  - docker-build
  - security-dynamic
  - deploy
```

## Livrables attendus

### 1. Configuration sécurisée complète

- ESLint avec règles de sécurité strictes
- Scripts de vérification de sécurité automatisés
- Configuration Snyk et outils de scan

### 2. Pipeline DevSecOps intégré

- SAST avec multiples outils (ESLint, GitLab)
- Dependency scanning (npm audit, Snyk, Retire.js)
- Container scanning avec Trivy
- DAST avec OWASP ZAP
- Secret detection GitLab

### 3. Rapports de sécurité

- Rapport consolidé de tous les scans
- Métriques de sécurité trackées
- Seuils de sécurité configurés
- Processus de remediation

## Critères d'évaluation

**Total : 25 points**

- **SAST configuré (6 points)** : ESLint sécurisé + GitLab SAST
- **Dependency scanning (6 points)** : Multiple outils, seuils configurés
- **Container security (5 points)** : Trivy scan fonctionnel
- **DAST intégré (4 points)** : OWASP ZAP avec résultats
- **Rapports consolidés (4 points)** : Métriques et suivi sécurité

## Durée estimée

**30 minutes** réparties :

- Configuration outils : 10 minutes
- Pipeline sécurité : 18 minutes
- Tests et validation : 2 minutes

## Conseils

- Commencer par SAST et dependency scanning (plus rapides)
- Configurer des seuils de sécurité adaptés à votre contexte
- Automatiser la remediation des vulnérabilités simples
- Intégrer la sécurité dès le développement (shift-left)

## Ressources

- [GitLab Security Templates](https://docs.gitlab.com/ee/user/application_security/)
- [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
- [ESLint Security Plugin](https://github.com/nodesecurity/eslint-plugin-security)
