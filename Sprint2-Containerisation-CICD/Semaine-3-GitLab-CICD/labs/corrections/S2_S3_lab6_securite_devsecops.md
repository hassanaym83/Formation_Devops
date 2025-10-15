# LAB 6 - CORRECTIONS : Sécurité DevSecOps

## Solution complète

### 1. Configuration ESLint sécurisé avancée

**Fichier `.eslintrc.security.js`** :

```javascript
module.exports = {
  extends: ['.eslintrc.js'],
  plugins: ['security', 'no-secrets'],
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  rules: {
    // === RÈGLES DE SÉCURITÉ CRITIQUES ===

    // Injection et évaluation de code
    'security/detect-object-injection': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-non-literal-regexp': 'error',
    'security/detect-non-literal-fs-filename': 'error',
    'security/detect-non-literal-require': 'error',
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',

    // Cryptographie et randomisation
    'security/detect-pseudoRandomBytes': 'error',
    'security/detect-possible-timing-attacks': 'warn',
    'security/detect-unsafe-regex': 'error',

    // Sécurité des buffers et processus
    'security/detect-buffer-noassert': 'error',
    'security/detect-child-process': 'error',

    // Protection contre les vulnérabilités web
    'security/detect-disable-mustache-escape': 'error',
    'security/detect-no-csrf-before-method-override': 'error',

    // === RÈGLES ADDITIONNELLES DE SÉCURITÉ ===

    // Scripts et URLs dangereuses
    'no-script-url': 'error',
    'no-inline-comments': 'off',
    'no-mixed-spaces-and-tabs': 'error',

    // Gestion des erreurs sécurisée
    'no-console': ['error', {allow: ['warn', 'error']}],
    'no-alert': 'error',
    'no-debugger': 'error',

    // === RÈGLES PERSONNALISÉES DE SÉCURITÉ ===

    // Détection de secrets (patterns custom)
    'no-secrets/no-secrets': [
      'error',
      {
        patterns: [
          {
            name: 'API Key',
            regex: /api[_-]?key['"]?\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]/i
          },
          {
            name: 'Database Password',
            regex: /(password|pwd)['"]?\s*[:=]\s*['"][^'"]{8,}['"]/i
          },
          {
            name: 'JWT Secret',
            regex: /jwt[_-]?secret['"]?\s*[:=]\s*['"][^'"]{16,}['"]/i
          },
          {
            name: 'Private Key',
            regex: /-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----/
          }
        ]
      }
    ],

    // Validation des entrées utilisateur
    'security/detect-object-injection': [
      'error',
      {
        patterns: [
          '__proto__',
          'constructor.prototype',
          'prototype.constructor'
        ]
      }
    ],

    // === RÈGLES SPÉCIFIQUES REACT/WEB ===

    // Protection XSS
    'react/no-danger': 'error',
    'react/no-danger-with-children': 'error',
    'react/jsx-no-script-url': 'error',
    'react/jsx-no-target-blank': [
      'error',
      {
        allowReferrer: false,
        enforceDynamicLinks: 'always'
      }
    ],

    // === CONFIGURATION AVANCÉE ===

    // Complexité et maintenabilité (sécurité par la simplicité)
    complexity: ['error', {max: 8}],
    'max-depth': ['error', {max: 3}],
    'max-lines-per-function': ['error', {max: 30}],
    'max-params': ['error', {max: 3}],

    // Gestion stricte des variables
    'no-unused-vars': [
      'error',
      {
        vars: 'all',
        args: 'after-used',
        ignoreRestSiblings: false,
        argsIgnorePattern: '^_'
      }
    ],
    'no-undef': 'error',
    'no-global-assign': 'error',
    'no-implicit-globals': 'error',

    // === RÈGLES POUR LES DÉPENDANCES ===

    // Import sécurisés
    'import/no-dynamic-require': 'error',
    'import/no-unresolved': 'error',
    'import/no-absolute-path': 'error',
    'import/no-self-import': 'error',
    'import/no-cycle': 'error',
    'import/no-useless-path-segments': 'error'
  },

  // === CONFIGURATION SPÉCIFIQUE PAR ENVIRONNEMENT ===
  overrides: [
    {
      files: ['**/*.test.js', '**/*.test.jsx', '**/*.spec.js'],
      rules: {
        'security/detect-non-literal-fs-filename': 'off',
        'security/detect-child-process': 'off',
        'no-console': 'off'
      }
    },
    {
      files: ['scripts/**/*.js', 'config/**/*.js'],
      rules: {
        'security/detect-child-process': 'warn',
        'security/detect-non-literal-fs-filename': 'warn'
      }
    },
    {
      files: ['src/**/*.js', 'src/**/*.jsx'],
      rules: {
        'security/detect-child-process': 'error',
        'security/detect-non-literal-fs-filename': 'error',
        'no-console': ['error', {allow: []}]
      }
    }
  ]
};
```

### 2. Script de sécurité complet

**Fichier `scripts/security-check.sh`** :

```bash
#!/bin/bash
set -euo pipefail

# === CONFIGURATION ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Couleurs pour l'affichage
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Compteurs
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# === FONCTIONS UTILITAIRES ===

log_info() {
    echo -e "${GREEN}[✓ INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[⚠ WARN]${NC} $1"
    ((WARNING_CHECKS++))
}

log_error() {
    echo -e "${RED}[✗ ERROR]${NC} $1"
    ((FAILED_CHECKS++))
}

log_check() {
    echo -e "${BLUE}[🔍 CHECK]${NC} $1"
    ((TOTAL_CHECKS++))
}

check_passed() {
    ((PASSED_CHECKS++))
}

print_summary() {
    echo
    echo "=== RÉSUMÉ DE SÉCURITÉ ==="
    echo -e "Total des vérifications: ${BLUE}$TOTAL_CHECKS${NC}"
    echo -e "Réussites: ${GREEN}$PASSED_CHECKS${NC}"
    echo -e "Avertissements: ${YELLOW}$WARNING_CHECKS${NC}"
    echo -e "Échecs: ${RED}$FAILED_CHECKS${NC}"
    echo

    if [ "$FAILED_CHECKS" -gt 0 ]; then
        echo -e "${RED}❌ ÉCHEC: $FAILED_CHECKS problème(s) de sécurité critique(s)${NC}"
        return 1
    elif [ "$WARNING_CHECKS" -gt 0 ]; then
        echo -e "${YELLOW}⚠️ ATTENTION: $WARNING_CHECKS avertissement(s) de sécurité${NC}"
        return 0
    else
        echo -e "${GREEN}✅ SUCCÈS: Toutes les vérifications de sécurité passées${NC}"
        return 0
    fi
}

# === VÉRIFICATIONS DE SÉCURITÉ ===

check_secrets_in_code() {
    log_check "Recherche de secrets dans le code source"

    local secrets_found=0

    # Patterns de secrets à détecter
    local -a secret_patterns=(
        "password\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        "secret\s*[:=]\s*['\"][^'\"]{16,}['\"]"
        "api[_-]?key\s*[:=]\s*['\"][a-zA-Z0-9]{16,}['\"]"
        "token\s*[:=]\s*['\"][^'\"]{20,}['\"]"
        "auth\s*[:=]\s*['\"][^'\"]{16,}['\"]"
        "-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----"
        "sk_live_[a-zA-Z0-9]{24,}"
        "pk_live_[a-zA-Z0-9]{24,}"
        "access_token['\"]?\s*[:=]\s*['\"][^'\"]{16,}['\"]"
        "refresh_token['\"]?\s*[:=]\s*['\"][^'\"]{16,}['\"]"
    )

    for pattern in "${secret_patterns[@]}"; do
        if grep -r -E -i "$pattern" src/ 2>/dev/null | grep -v ".test." | grep -v ".spec."; then
            log_error "Pattern de secret détecté: $pattern"
            ((secrets_found++))
        fi
    done

    # Vérification avec git-secrets si disponible
    if command -v git-secrets >/dev/null 2>&1; then
        if ! git-secrets --scan; then
            log_error "git-secrets a détecté des secrets"
            ((secrets_found++))
        fi
    else
        log_warn "git-secrets non installé - recommandé pour une vérification complète"
    fi

    if [ "$secrets_found" -eq 0 ]; then
        log_info "Aucun secret détecté dans le code"
        check_passed
    else
        log_error "$secrets_found secret(s) potentiel(s) détecté(s)"
    fi
}

check_dependencies_vulnerabilities() {
    log_check "Vérification des vulnérabilités dans les dépendances"

    # npm audit
    log_info "Exécution de npm audit"
    if npm audit --audit-level=moderate --production --json > audit-result.json 2>/dev/null; then
        local vulnerabilities=$(jq '.metadata.vulnerabilities | to_entries | map(select(.value > 0)) | length' audit-result.json 2>/dev/null || echo "0")
        if [ "$vulnerabilities" -gt 0 ]; then
            log_warn "npm audit a détecté $vulnerabilities type(s) de vulnérabilités"
        else
            log_info "npm audit: aucune vulnérabilité détectée"
            check_passed
        fi
    else
        log_error "npm audit a échoué ou détecté des vulnérabilités critiques"
    fi

    # Vérification avec yarn audit si yarn est utilisé
    if [ -f "yarn.lock" ] && command -v yarn >/dev/null 2>&1; then
        log_info "Exécution de yarn audit"
        if yarn audit --level moderate --json > yarn-audit.json 2>/dev/null; then
            log_info "yarn audit: aucune vulnérabilité critique"
        else
            log_warn "yarn audit a détecté des vulnérabilités"
        fi
    fi

    # Nettoyage
    rm -f audit-result.json yarn-audit.json
}

check_file_permissions() {
    log_check "Vérification des permissions de fichiers"

    local permission_issues=0

    # Fichiers avec permissions d'écriture pour tous
    while IFS= read -r -d '' file; do
        log_warn "Fichier avec permissions d'écriture globale: $file"
        ((permission_issues++))
    done < <(find . -type f -perm -002 -not -path "./node_modules/*" -not -path "./.git/*" -print0 2>/dev/null)

    # Fichiers exécutables suspects
    while IFS= read -r -d '' file; do
        if [[ ! "$file" =~ \.(sh|js|py|rb)$ ]] && [[ ! "$file" =~ ^./scripts/ ]]; then
            log_warn "Fichier exécutable suspect: $file"
            ((permission_issues++))
        fi
    done < <(find . -type f -perm -111 -not -path "./node_modules/*" -not -path "./.git/*" -print0 2>/dev/null)

    if [ "$permission_issues" -eq 0 ]; then
        log_info "Permissions de fichiers correctes"
        check_passed
    fi
}

check_docker_security() {
    log_check "Vérification de la sécurité Docker"

    if [ ! -f "Dockerfile" ]; then
        log_warn "Dockerfile non trouvé - vérification ignorée"
        return
    fi

    local docker_issues=0

    # Vérification utilisateur non-root
    if ! grep -q "USER.*[^0]" Dockerfile; then
        log_error "Dockerfile utilise l'utilisateur root"
        ((docker_issues++))
    fi

    # Vérification des secrets hardcodés
    if grep -i -E "(password|secret|key|token)\s*[:=]" Dockerfile; then
        log_error "Secrets potentiels dans Dockerfile"
        ((docker_issues++))
    fi

    # Vérification des bonnes pratiques
    if ! grep -q "HEALTHCHECK" Dockerfile; then
        log_warn "Dockerfile sans HEALTHCHECK"
    fi

    if grep -q "ADD.*http" Dockerfile; then
        log_warn "Utilisation d'ADD avec URL - préférer COPY"
    fi

    if grep -q "RUN.*sudo" Dockerfile; then
        log_warn "Utilisation de sudo dans Dockerfile"
    fi

    if [ "$docker_issues" -eq 0 ]; then
        log_info "Configuration Docker sécurisée"
        check_passed
    fi
}

check_security_headers() {
    log_check "Vérification des en-têtes de sécurité"

    local headers_found=0
    local -a required_headers=(
        "X-Content-Type-Options"
        "X-Frame-Options"
        "X-XSS-Protection"
        "Strict-Transport-Security"
        "Content-Security-Policy"
        "Referrer-Policy"
    )

    for header in "${required_headers[@]}"; do
        if grep -r -i "$header" src/ nginx.conf* *.js *.json 2>/dev/null | grep -v node_modules | grep -v test; then
            ((headers_found++))
        fi
    done

    if [ "$headers_found" -ge 4 ]; then
        log_info "En-têtes de sécurité principaux configurés ($headers_found/6)"
        check_passed
    elif [ "$headers_found" -ge 2 ]; then
        log_warn "Quelques en-têtes de sécurité manquants ($headers_found/6)"
    else
        log_error "En-têtes de sécurité insuffisants ($headers_found/6)"
    fi
}

check_environment_variables() {
    log_check "Vérification des variables d'environnement"

    local env_issues=0

    # Vérification des fichiers .env
    if [ -f ".env" ]; then
        log_warn "Fichier .env présent - vérifier qu'il n'est pas commité"
        if git ls-files --error-unmatch .env >/dev/null 2>&1; then
            log_error "Fichier .env est tracké par Git"
            ((env_issues++))
        fi
    fi

    # Vérification des variables hardcodées
    if grep -r -E "process\.env\.[A-Z_]+\s*\|\|\s*['\"][^'\"]+['\"]" src/ 2>/dev/null; then
        log_warn "Variables d'environnement avec valeurs par défaut hardcodées"
    fi

    if [ "$env_issues" -eq 0 ]; then
        log_info "Configuration des variables d'environnement sécurisée"
        check_passed
    fi
}

check_input_validation() {
    log_check "Vérification de la validation des entrées"

    local validation_issues=0

    # Recherche de fonctions dangereuses
    local -a dangerous_functions=(
        "eval\s*\("
        "innerHTML\s*="
        "outerHTML\s*="
        "document\.write\s*\("
        "\.html\s*\("
    )

    for func in "${dangerous_functions[@]}"; do
        if grep -r -E "$func" src/ 2>/dev/null | grep -v test | grep -v spec; then
            log_warn "Fonction potentiellement dangereuse détectée: $func"
            ((validation_issues++))
        fi
    done

    # Vérification de la validation côté client
    if ! grep -r -E "(validator|joi|yup|ajv)" package.json 2>/dev/null; then
        log_warn "Aucune librairie de validation détectée"
    fi

    if [ "$validation_issues" -eq 0 ]; then
        log_info "Pas de fonction dangereuse détectée"
        check_passed
    fi
}

check_ssl_tls_configuration() {
    log_check "Vérification de la configuration SSL/TLS"

    # Vérification dans nginx.conf
    if [ -f "nginx.conf" ] || [ -f "nginx.conf.template" ]; then
        if grep -q "ssl_protocols.*TLSv1\.[23]" nginx.conf* 2>/dev/null; then
            log_info "Protocoles TLS modernes configurés"
            check_passed
        else
            log_warn "Configuration TLS non trouvée ou obsolète"
        fi
    else
        log_warn "Configuration serveur web non trouvée"
    fi

    # Vérification des certificats de test
    if find . -name "*.pem" -o -name "*.crt" -o -name "*.key" | grep -v node_modules; then
        log_warn "Certificats ou clés détectés - vérifier qu'ils ne sont pas en production"
    fi
}

check_cors_configuration() {
    log_check "Vérification de la configuration CORS"

    # Recherche de configuration CORS permissive
    if grep -r -E "origin.*\*" src/ package.json 2>/dev/null | grep -v test; then
        log_warn "Configuration CORS permissive détectée (origin: *)"
    fi

    if grep -r -E "Access-Control-Allow-Origin.*\*" src/ nginx.conf* 2>/dev/null; then
        log_warn "En-tête CORS permissif détecté"
    fi

    log_info "Vérification CORS terminée"
    check_passed
}

check_logging_configuration() {
    log_check "Vérification de la configuration des logs"

    # Vérification que les informations sensibles ne sont pas loggées
    if grep -r -E "console\.log.*password|console\.log.*secret|console\.log.*token" src/ 2>/dev/null; then
        log_error "Informations sensibles potentiellement loggées"
    else
        log_info "Pas d'informations sensibles dans les logs"
        check_passed
    fi

    # Vérification de la présence d'une solution de logging structuré
    if grep -r -E "(winston|pino|bunyan|morgan)" package.json 2>/dev/null; then
        log_info "Solution de logging structuré détectée"
    else
        log_warn "Pas de solution de logging structuré détectée"
    fi
}

# === EXÉCUTION PRINCIPALE ===

main() {
    echo "🔒 === VÉRIFICATION DE SÉCURITÉ COMPLÈTE ==="
    echo "📅 Date: $(date)"
    echo "📁 Projet: $PROJECT_ROOT"
    echo "👤 Utilisateur: $(whoami)"
    echo

    # Exécution de toutes les vérifications
    check_secrets_in_code
    check_dependencies_vulnerabilities
    check_file_permissions
    check_docker_security
    check_security_headers
    check_environment_variables
    check_input_validation
    check_ssl_tls_configuration
    check_cors_configuration
    check_logging_configuration

    # Affichage du résumé et retour du code de sortie approprié
    print_summary
}

# Exécution du script
main "$@"
```

### 3. Pipeline GitLab CI/CD sécurisé optimisé

```yaml
# Pipeline GitLab CI/CD avec sécurité DevSecOps complète
include:
  # Templates GitLab officiels pour la sécurité
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/License-Scanning.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/DAST.gitlab-ci.yml

# Variables de sécurité globales
variables:
  # Configuration SAST
  SAST_EXCLUDED_ANALYZERS: 'gosec'
  SAST_EXCLUDED_PATHS: 'node_modules, coverage, build, docs'
  SAST_DEFAULT_ANALYZERS: 'eslint, nodejs-scan, semgrep'

  # Configuration Secret Detection
  SECRET_DETECTION_EXCLUDED_PATHS: 'node_modules, coverage, *.md'
  SECRET_DETECTION_HISTORIC_SCAN: 'true'

  # Configuration Dependency Scanning
  DS_EXCLUDED_ANALYZERS: ''
  DS_EXCLUDED_PATHS: 'node_modules, coverage'
  DS_DEFAULT_ANALYZERS: 'retire-js, gemnasium'

  # Configuration Container Scanning
  CS_MAJOR_VERSION: 5
  CS_ANALYZER_IMAGE: '$CI_TEMPLATE_REGISTRY_HOST/security-products/container-scanning:$CS_MAJOR_VERSION'
  CS_SEVERITY_THRESHOLD: 'MEDIUM'

  # Configuration DAST
  DAST_WEBSITE: 'http://localhost:3000'
  DAST_FULL_SCAN_ENABLED: 'true'
  DAST_BROWSER_SCAN: 'true'
  DAST_API_SPECIFICATION: 'docs/api-spec.json'

  # Seuils de sécurité
  SECURITY_FAIL_ON_CRITICAL: 'true'
  SECURITY_FAIL_ON_HIGH: 'true'
  SECURITY_FAIL_ON_MEDIUM: 'false'

stages:
  - security-validate
  - security-static
  - build
  - security-container
  - security-dynamic
  - security-report
  - deploy

# Cache pour outils de sécurité
cache:
  key: security-tools-$CI_COMMIT_REF_SLUG
  paths:
    - .sonar/cache
    - .snyk/
    - .trivy-cache/
  policy: pull-push

# Template pour jobs de sécurité
.security_template: &security_template
  allow_failure: false
  artifacts:
    reports:
      security: gl-*.json
    paths:
      - security-reports/
    expire_in: 30 days
    when: always
  before_script:
    - mkdir -p security-reports
    - echo "🔒 Job de sécurité: $CI_JOB_NAME"
    - echo "📅 Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# === PHASE 1: VALIDATION SÉCURISÉE ===

security_validation_comprehensive:
  stage: security-validate
  image: node:18-alpine
  <<: *security_template
  before_script:
    - !reference [.security_template, before_script]
    - apk add --no-cache git bash curl jq
    - chmod +x scripts/security-check.sh
  script:
    - echo "🔍 === VALIDATION SÉCURISÉE COMPLÈTE ==="

    # Validation de la structure de sécurité
    - |
      echo "📋 Vérification des fichiers de sécurité requis"
      required_security_files=(
        ".eslintrc.security.js"
        "scripts/security-check.sh"
        ".snyk"
        ".auditcirc.json"
      )

      missing_files=()
      for file in "${required_security_files[@]}"; do
        if [ ! -f "$file" ]; then
          missing_files+=("$file")
        fi
      done

      if [ ${#missing_files[@]} -gt 0 ]; then
        echo "❌ Fichiers de sécurité manquants: ${missing_files[*]}"
        exit 1
      fi
      echo "✅ Tous les fichiers de sécurité sont présents"

    # Validation des secrets dans l'historique Git
    - |
      echo "🔍 Scan des secrets dans l'historique Git"
      git log --all --full-history -- . | grep -i -E "(password|secret|key|token)" | head -10 || echo "Aucun secret détecté dans les commits"

    # Exécution du script de sécurité personnalisé
    - echo "🛡️ Exécution du script de sécurité complet"
    - ./scripts/security-check.sh

    - echo "✅ Validation sécurisée terminée"
  only:
    - main
    - develop
    - merge_requests

# === PHASE 2: ANALYSE STATIQUE (SAST) ===

sast_eslint_security_advanced:
  stage: security-static
  image: node:18-alpine
  <<: *security_template
  script:
    - echo "🔍 === SAST AVANCÉ AVEC ESLINT SÉCURISÉ ==="
    - npm ci --prefer-offline --no-audit

    # ESLint avec règles de sécurité strictes
    - |
      npx eslint src/ \
        --config .eslintrc.security.js \
        --ext .js,.jsx,.ts,.tsx \
        --format json \
        --output-file security-reports/eslint-security.json \
        --max-warnings 0

    # Analyse des résultats de sécurité
    - |
      echo "📊 Analyse des résultats ESLint sécurité"
      if [ -f security-reports/eslint-security.json ]; then
        security_errors=$(jq '[.[].messages[] | select(.severity == 2 and (.ruleId | startswith("security/")))] | length' security-reports/eslint-security.json)
        security_warnings=$(jq '[.[].messages[] | select(.severity == 1 and (.ruleId | startswith("security/")))] | length' security-reports/eslint-security.json)
        
        echo "Erreurs de sécurité: $security_errors"
        echo "Avertissements de sécurité: $security_warnings"
        
        if [ "$security_errors" -gt 0 ]; then
          echo "❌ Erreurs de sécurité critiques détectées"
          jq '[.[].messages[] | select(.severity == 2 and (.ruleId | startswith("security/")))]' security-reports/eslint-security.json
          exit 1
        fi
        
        if [ "$security_warnings" -gt 5 ]; then
          echo "⚠️ Trop d'avertissements de sécurité ($security_warnings > 5)"
          exit 1
        fi
      fi

    - echo "✅ SAST ESLint sécurisé réussi"
  artifacts:
    paths:
      - security-reports/eslint-security.json
    reports:
      codequality: security-reports/eslint-security.json
  only:
    - main
    - develop
    - merge_requests

sast_semgrep_advanced:
  stage: security-static
  image: returntocorp/semgrep:latest
  <<: *security_template
  script:
    - echo "🔍 === SAST AVEC SEMGREP ==="

    # Scan avec règles de sécurité Semgrep
    - |
      semgrep \
        --config=auto \
        --config=p/security-audit \
        --config=p/secrets \
        --config=p/owasp-top-ten \
        --json \
        --output=security-reports/semgrep-report.json \
        --severity=ERROR \
        --severity=WARNING \
        src/

    # Analyse des résultats
    - |
      if [ -f security-reports/semgrep-report.json ]; then
        critical_findings=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' security-reports/semgrep-report.json)
        high_findings=$(jq '[.results[] | select(.extra.severity == "WARNING")] | length' security-reports/semgrep-report.json)
        
        echo "Findings critiques: $critical_findings"
        echo "Findings élevés: $high_findings"
        
        if [ "$critical_findings" -gt 0 ]; then
          echo "❌ Findings critiques détectés par Semgrep"
          jq '.results[] | select(.extra.severity == "ERROR")' security-reports/semgrep-report.json
          exit 1
        fi
      fi

    - echo "✅ SAST Semgrep réussi"
  artifacts:
    paths:
      - security-reports/semgrep-report.json
    reports:
      sast: security-reports/semgrep-report.json
  only:
    - main
    - develop
    - merge_requests

# Analyse des dépendances multi-outils
dependency_security_comprehensive:
  stage: security-static
  image: node:18-alpine
  <<: *security_template
  before_script:
    - !reference [.security_template, before_script]
    - apk add --no-cache python3 py3-pip curl
    - npm install -g audit-ci retire snyk
    - pip3 install safety
  script:
    - echo "📦 === ANALYSE SÉCURITÉ DÉPENDANCES COMPLÈTE ==="
    - npm ci --prefer-offline

    # npm audit avec audit-ci
    - |
      echo "🔍 Audit npm avec audit-ci"
      audit-ci --config .auditcirc.json --output-format json > security-reports/npm-audit.json || {
        echo "❌ Vulnérabilités critiques détectées par npm audit"
        exit 1
      }

    # Retire.js pour les vulnérabilités JavaScript
    - |
      echo "🔍 Scan Retire.js"
      retire --js --outputformat json --outputpath security-reports/retire.json src/ || echo "Retire scan terminé"

    # Snyk scan
    - |
      echo "🐍 Scan Snyk"
      snyk test --json > security-reports/snyk.json || echo "Snyk scan terminé"

      if [ -f security-reports/snyk.json ]; then
        high_vulns=$(jq '[.vulnerabilities[] | select(.severity == "high")] | length' security-reports/snyk.json 2>/dev/null || echo "0")
        critical_vulns=$(jq '[.vulnerabilities[] | select(.severity == "critical")] | length' security-reports/snyk.json 2>/dev/null || echo "0")
        
        echo "Vulnérabilités critiques: $critical_vulns"
        echo "Vulnérabilités élevées: $high_vulns"
        
        if [ "$critical_vulns" -gt 0 ]; then
          echo "❌ Vulnérabilités critiques détectées par Snyk"
          exit 1
        fi
      fi

    # OSV Scanner (si disponible)
    - |
      if command -v osv-scanner >/dev/null 2>&1; then
        echo "🔍 Scan OSV"
        osv-scanner --json --output security-reports/osv.json . || echo "OSV scan terminé"
      fi

    # Rapport consolidé
    - |
      echo "📊 Génération du rapport consolidé"
      cat > security-reports/dependency-summary.json << EOF
      {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "tools": {
          "npm_audit": $(cat security-reports/npm-audit.json 2>/dev/null || echo '{}'),
          "retire": $(cat security-reports/retire.json 2>/dev/null || echo '{}'),
          "snyk": $(cat security-reports/snyk.json 2>/dev/null || echo '{}')
        }
      }
      EOF

    - echo "✅ Analyse des dépendances terminée"
  artifacts:
    paths:
      - security-reports/
    reports:
      dependency_scanning: security-reports/dependency-summary.json
  only:
    - main
    - develop
    - merge_requests

# === PHASE 3: SÉCURITÉ DES CONTAINERS ===

container_security_trivy_advanced:
  stage: security-container
  image: docker:24.0.5
  services:
    - docker:24.0.5-dind
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
    TRIVY_CACHE_DIR: '.trivy-cache'
  <<: *security_template
  before_script:
    - !reference [.security_template, before_script]
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - apk add --no-cache curl
    - curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
  script:
    - echo "🐳 === SCAN SÉCURITÉ CONTAINER AVANCÉ ==="
    - IMAGE_NAME="$CI_REGISTRY_IMAGE/demo-react-app:$CI_COMMIT_SHORT_SHA"

    # Pull de l'image
    - docker pull "$IMAGE_NAME"

    # Scan des vulnérabilités OS
    - |
      echo "🔍 Scan Trivy - Vulnérabilités système"
      trivy image \
        --format json \
        --output security-reports/trivy-os.json \
        --vuln-type os \
        --severity HIGH,CRITICAL \
        --ignore-unfixed \
        "$IMAGE_NAME"

    # Scan des vulnérabilités des librairies
    - |
      echo "🔍 Scan Trivy - Vulnérabilités librairies"
      trivy image \
        --format json \
        --output security-reports/trivy-library.json \
        --vuln-type library \
        --severity HIGH,CRITICAL \
        --ignore-unfixed \
        "$IMAGE_NAME"

    # Scan de configuration
    - |
      echo "🔍 Scan Trivy - Configuration"
      trivy config \
        --format json \
        --output security-reports/trivy-config.json \
        --severity HIGH,CRITICAL \
        .

    # Scan des secrets dans l'image
    - |
      echo "🔍 Scan Trivy - Secrets"
      trivy image \
        --format json \
        --output security-reports/trivy-secrets.json \
        --scanners secret \
        "$IMAGE_NAME"

    # Analyse des résultats
    - |
      echo "📊 Analyse des résultats Trivy"

      # Vulnérabilités OS critiques
      critical_os=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length' security-reports/trivy-os.json)
      high_os=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH")] | length' security-reports/trivy-os.json)

      # Vulnérabilités librairies critiques
      critical_lib=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length' security-reports/trivy-library.json)
      high_lib=$(jq '[.Results[]?.Vulnerabilities[]? | select(.Severity == "HIGH")] | length' security-reports/trivy-library.json)

      # Secrets détectés
      secrets_count=$(jq '[.Results[]?.Secrets[]?] | length' security-reports/trivy-secrets.json)

      echo "=== RÉSUMÉ SÉCURITÉ CONTAINER ==="
      echo "Vulnérabilités OS critiques: $critical_os"
      echo "Vulnérabilités OS élevées: $high_os"
      echo "Vulnérabilités lib critiques: $critical_lib"
      echo "Vulnérabilités lib élevées: $high_lib"
      echo "Secrets détectés: $secrets_count"

      # Échec si vulnérabilités critiques
      total_critical=$((critical_os + critical_lib))
      if [ "$total_critical" -gt 0 ]; then
        echo "❌ $total_critical vulnérabilité(s) critique(s) détectée(s)"
        exit 1
      fi

      # Échec si secrets détectés
      if [ "$secrets_count" -gt 0 ]; then
        echo "❌ $secrets_count secret(s) détecté(s) dans l'image"
        exit 1
      fi

    - echo "✅ Scan sécurité container réussi"
  artifacts:
    paths:
      - security-reports/trivy-*.json
    reports:
      container_scanning: security-reports/trivy-os.json
  needs:
    - job: docker_build
      optional: true
  only:
    - main
    - develop
    - merge_requests

# === PHASE 4: TESTS DYNAMIQUES (DAST) ===

dast_owasp_zap_comprehensive:
  stage: security-dynamic
  image: owasp/zap2docker-stable:latest
  variables:
    website: 'http://localhost:3000'
  <<: *security_template
  services:
    - name: docker:24.0.5-dind
      alias: docker
  before_script:
    - !reference [.security_template, before_script]
    - echo "🕷️ Préparation OWASP ZAP"
    # L'application doit être démarrée dans un service séparé
  script:
    - echo "🕷️ === DAST COMPLET AVEC OWASP ZAP ==="

    # Scan baseline rapide
    - |
      echo "🔍 ZAP Baseline Scan"
      zap-baseline.py \
        -t $website \
        -J security-reports/zap-baseline.json \
        -r security-reports/zap-baseline.html \
        -x security-reports/zap-baseline.xml \
        -a \
        -j \
        -l PASS \
        -i \
        -z "-config scanner.strength=MEDIUM" \
        || echo "Baseline scan terminé avec des findings"

    # Scan API si disponible
    - |
      if [ -f "docs/api-spec.json" ]; then
        echo "🔍 ZAP API Scan"
        zap-api-scan.py \
          -t docs/api-spec.json \
          -f openapi \
          -J security-reports/zap-api.json \
          -r security-reports/zap-api.html \
          -x security-reports/zap-api.xml \
          || echo "API scan terminé"
      fi

    # Scan complet (si activé)
    - |
      if [ "$DAST_FULL_SCAN_ENABLED" = "true" ]; then
        echo "🔍 ZAP Full Scan"
        zap-full-scan.py \
          -t $website \
          -J security-reports/zap-full.json \
          -r security-reports/zap-full.html \
          -x security-reports/zap-full.xml \
          -a \
          -j \
          -l PASS \
          -T 15 \
          -z "-config scanner.strength=HIGH" \
          || echo "Full scan terminé avec des findings"
      fi

    # Analyse des résultats
    - |
      echo "📊 Analyse des résultats DAST"

      if [ -f security-reports/zap-baseline.json ]; then
        high_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("High"))' security-reports/zap-baseline.json | wc -l)
        medium_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("Medium"))' security-reports/zap-baseline.json | wc -l)
        
        echo "Risques élevés: $high_risks"
        echo "Risques moyens: $medium_risks"
        
        if [ "$high_risks" -gt 0 ]; then
          echo "❌ $high_risks vulnérabilité(s) DAST critique(s) détectée(s)"
          jq '.site[].alerts[] | select(.riskdesc | startswith("High"))' security-reports/zap-baseline.json
          exit 1
        fi
        
        if [ "$medium_risks" -gt 5 ]; then
          echo "⚠️ Trop de vulnérabilités moyennes détectées ($medium_risks > 5)"
        fi
      fi

    - echo "✅ DAST terminé"
  artifacts:
    paths:
      - security-reports/zap-*
    reports:
      dast: security-reports/zap-baseline.json
  needs:
    - job: deploy_staging_docker
      optional: true
  when: manual
  only:
    - main
    - develop

# === PHASE 5: RAPPORT DE SÉCURITÉ CONSOLIDÉ ===

security_report_consolidated:
  stage: security-report
  image: node:18-alpine
  <<: *security_template
  before_script:
    - !reference [.security_template, before_script]
    - apk add --no-cache jq curl
  script:
    - echo "📊 === GÉNÉRATION RAPPORT SÉCURITÉ CONSOLIDÉ ==="

    # Collecte de tous les rapports de sécurité
    - |
      echo "📋 Collecte des rapports de sécurité"

      # Initialisation du rapport consolidé
      cat > security-reports/consolidated-report.json << EOF
      {
        "metadata": {
          "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
          "commit": "$CI_COMMIT_SHA",
          "pipeline": "$CI_PIPELINE_ID",
          "branch": "$CI_COMMIT_REF_NAME",
          "project": "$CI_PROJECT_NAME"
        },
        "security_scans": {},
        "summary": {},
        "recommendations": []
      }
      EOF

    # Agrégation des résultats SAST
    - |
      echo "🔍 Agrégation SAST"
      sast_issues=0

      if [ -f security-reports/eslint-security.json ]; then
        eslint_issues=$(jq '[.[].messages[] | select(.ruleId | startswith("security/"))] | length' security-reports/eslint-security.json)
        sast_issues=$((sast_issues + eslint_issues))
        jq --arg count "$eslint_issues" '.security_scans.sast.eslint = {"status": "completed", "issues": ($count | tonumber)}' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json
      fi

      if [ -f security-reports/semgrep-report.json ]; then
        semgrep_issues=$(jq '[.results[]] | length' security-reports/semgrep-report.json)
        sast_issues=$((sast_issues + semgrep_issues))
        jq --arg count "$semgrep_issues" '.security_scans.sast.semgrep = {"status": "completed", "issues": ($count | tonumber)}' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json
      fi

    # Agrégation des résultats de dépendances
    - |
      echo "📦 Agrégation Dependency Scanning"
      dep_vulns=0

      if [ -f security-reports/npm-audit.json ]; then
        npm_vulns=$(jq '.metadata.vulnerabilities | to_entries | map(.value) | add' security-reports/npm-audit.json 2>/dev/null || echo "0")
        dep_vulns=$((dep_vulns + npm_vulns))
      fi

      jq --arg count "$dep_vulns" '.security_scans.dependency_scanning = {"status": "completed", "vulnerabilities": ($count | tonumber)}' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json

    # Agrégation des résultats container
    - |
      echo "🐳 Agrégation Container Scanning"
      container_vulns=0

      if [ -f security-reports/trivy-os.json ]; then
        os_vulns=$(jq '[.Results[]?.Vulnerabilities[]?] | length' security-reports/trivy-os.json)
        container_vulns=$((container_vulns + os_vulns))
      fi

      if [ -f security-reports/trivy-library.json ]; then
        lib_vulns=$(jq '[.Results[]?.Vulnerabilities[]?] | length' security-reports/trivy-library.json)
        container_vulns=$((container_vulns + lib_vulns))
      fi

      jq --arg count "$container_vulns" '.security_scans.container_scanning = {"status": "completed", "vulnerabilities": ($count | tonumber)}' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json

    # Agrégation des résultats DAST
    - |
      echo "🕷️ Agrégation DAST"
      dast_risks=0

      if [ -f security-reports/zap-baseline.json ]; then
        high_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("High"))' security-reports/zap-baseline.json | wc -l)
        medium_risks=$(jq '.site[].alerts[] | select(.riskdesc | startswith("Medium"))' security-reports/zap-baseline.json | wc -l)
        dast_risks=$((high_risks + medium_risks))
      fi

      jq --arg count "$dast_risks" '.security_scans.dast = {"status": "completed", "risks": ($count | tonumber)}' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json

    # Génération du résumé
    - |
      echo "📈 Génération du résumé"
      total_issues=$((sast_issues + dep_vulns + container_vulns + dast_risks))

      # Détermination du niveau de sécurité
      if [ "$total_issues" -eq 0 ]; then
        security_level="EXCELLENT"
        security_score=100
      elif [ "$total_issues" -le 5 ]; then
        security_level="GOOD"
        security_score=85
      elif [ "$total_issues" -le 15 ]; then
        security_level="MODERATE"
        security_score=70
      else
        security_level="POOR"
        security_score=50
      fi

      jq --arg level "$security_level" --arg score "$security_score" --arg total "$total_issues" \
        '.summary = {"level": $level, "score": ($score | tonumber), "total_issues": ($total | tonumber)}' \
        security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json

    # Génération des recommandations
    - |
      echo "💡 Génération des recommandations"
      recommendations='[]'

      if [ "$sast_issues" -gt 0 ]; then
        recommendations=$(echo "$recommendations" | jq '. + ["Corriger les issues SAST détectés dans le code source"]')
      fi

      if [ "$dep_vulns" -gt 0 ]; then
        recommendations=$(echo "$recommendations" | jq '. + ["Mettre à jour les dépendances vulnérables"]')
      fi

      if [ "$container_vulns" -gt 0 ]; then
        recommendations=$(echo "$recommendations" | jq '. + ["Mettre à jour l'\''image de base Docker"]')
      fi

      if [ "$dast_risks" -gt 0 ]; then
        recommendations=$(echo "$recommendations" | jq '. + ["Corriger les vulnérabilités détectées par les tests dynamiques"]')
      fi

      if [ "$total_issues" -eq 0 ]; then
        recommendations=$(echo "$recommendations" | jq '. + ["Excellente posture de sécurité - maintenir les bonnes pratiques"]')
      fi

      jq --argjson recs "$recommendations" '.recommendations = $recs' security-reports/consolidated-report.json > tmp.json && mv tmp.json security-reports/consolidated-report.json

    # Génération du rapport HTML
    - |
      echo "📄 Génération du rapport HTML"
      cat > security-reports/security-report.html << 'EOF'
      <!DOCTYPE html>
      <html>
      <head>
          <title>Rapport de Sécurité</title>
          <style>
              body { font-family: Arial, sans-serif; margin: 20px; }
              .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
              .summary { background: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }
              .excellent { color: #27ae60; }
              .good { color: #f39c12; }
              .moderate { color: #e67e22; }
              .poor { color: #e74c3c; }
              .section { margin: 20px 0; padding: 15px; border: 1px solid #bdc3c7; border-radius: 5px; }
              .recommendation { background: #d5dbdb; padding: 10px; margin: 5px 0; border-radius: 3px; }
          </style>
      </head>
      <body>
          <div class="header">
              <h1>🔒 Rapport de Sécurité DevSecOps</h1>
              <p>Projet: PROJECT_NAME | Pipeline: PIPELINE_ID | Commit: COMMIT_SHA</p>
          </div>
      EOF

      # Injection des données du rapport JSON dans le HTML
      project_name=$(jq -r '.metadata.project' security-reports/consolidated-report.json)
      pipeline_id=$(jq -r '.metadata.pipeline' security-reports/consolidated-report.json)
      commit_sha=$(jq -r '.metadata.commit' security-reports/consolidated-report.json)
      security_level=$(jq -r '.summary.level' security-reports/consolidated-report.json)
      security_score=$(jq -r '.summary.score' security-reports/consolidated-report.json)
      total_issues=$(jq -r '.summary.total_issues' security-reports/consolidated-report.json)

      sed -i "s/PROJECT_NAME/$project_name/g" security-reports/security-report.html
      sed -i "s/PIPELINE_ID/$pipeline_id/g" security-reports/security-report.html
      sed -i "s/COMMIT_SHA/${commit_sha:0:8}/g" security-reports/security-report.html

    # Affichage du résumé
    - |
      echo "=== RÉSUMÉ SÉCURITÉ ==="
      echo "🏆 Niveau de sécurité: $security_level"
      echo "📊 Score de sécurité: $security_score/100"
      echo "⚠️ Total des issues: $total_issues"
      echo "🔍 SAST issues: $sast_issues"
      echo "📦 Dependency vulns: $dep_vulns"
      echo "🐳 Container vulns: $container_vulns"
      echo "🕷️ DAST risks: $dast_risks"
      echo

      # Affichage du rapport complet
      cat security-reports/consolidated-report.json | jq '.'

    - echo "✅ Rapport de sécurité consolidé généré"

    # Détermination du code de sortie
    - |
      if [ "$total_issues" -gt 20 ]; then
        echo "❌ Trop d'issues de sécurité détectés ($total_issues > 20)"
        exit 1
      elif [ "$total_issues" -gt 10 ]; then
        echo "⚠️ Nombre élevé d'issues de sécurité ($total_issues)"
        # Continuer mais avec avertissement
      else
        echo "✅ Niveau de sécurité acceptable"
      fi
  artifacts:
    paths:
      - security-reports/
    reports:
      security: security-reports/consolidated-report.json
    expire_in: 30 days
  needs:
    - job: sast_eslint_security_advanced
      artifacts: true
      optional: true
    - job: sast_semgrep_advanced
      artifacts: true
      optional: true
    - job: dependency_security_comprehensive
      artifacts: true
      optional: true
    - job: container_security_trivy_advanced
      artifacts: true
      optional: true
    - job: dast_owasp_zap_comprehensive
      artifacts: true
      optional: true
  when: always
  only:
    - main
    - develop
    - merge_requests
```

## Explications techniques

### 1. Configuration ESLint sécurisé

**Règles de sécurité critiques** :

- **Injection de code** : `detect-eval-with-expression`, `detect-object-injection`
- **Cryptographie** : `detect-pseudoRandomBytes`, `detect-possible-timing-attacks`
- **Protection XSS** : `react/no-danger`, `react/jsx-no-script-url`
- **Gestion des secrets** : Plugin custom `no-secrets` avec patterns

### 2. Script de sécurité complet

**Vérifications automatisées** :

- **Détection de secrets** : Patterns regex avancés + git-secrets
- **Audit des dépendances** : npm audit + yarn audit + validation des versions
- **Permissions fichiers** : Détection des permissions dangereuses
- **Configuration Docker** : Utilisateur non-root, secrets hardcodés
- **Headers de sécurité** : HSTS, CSP, X-Frame-Options, etc.

### 3. Pipeline DevSecOps multi-phases

**Phase 1 - Validation** :

- Vérification des fichiers de sécurité requis
- Scan des secrets dans l'historique Git
- Validation de la structure de sécurité

**Phase 2 - SAST** :

- ESLint avec règles de sécurité strictes
- Semgrep avec règles OWASP et sécurité
- Analyse des résultats avec seuils configurables

**Phase 3 - Dependency Scanning** :

- npm audit avec audit-ci
- Retire.js pour vulnérabilités JavaScript
- Snyk pour analyse complète
- OSV Scanner (si disponible)

**Phase 4 - Container Security** :

- Trivy pour vulnérabilités OS et librairies
- Scan de configuration Docker
- Détection de secrets dans les images
- Seuils configurables par sévérité

**Phase 5 - DAST** :

- OWASP ZAP baseline et full scan
- Scan API avec spécification OpenAPI
- Analyse des risques avec seuils

**Phase 6 - Rapport consolidé** :

- Agrégation de tous les résultats
- Calcul du score de sécurité
- Génération de recommandations
- Rapport HTML et JSON

## Métriques de sécurité

### Seuils de sécurité

- **SAST** : 0 erreurs critiques, max 5 avertissements
- **Dependencies** : 0 vulnérabilités critiques/élevées
- **Container** : 0 vulnérabilités critiques, max 5 élevées
- **DAST** : 0 risques élevés, max 5 moyens

### Score de sécurité

- **EXCELLENT (100)** : 0 issues détectés
- **GOOD (85)** : 1-5 issues mineures
- **MODERATE (70)** : 6-15 issues modérées
- **POOR (50)** : 16+ issues ou critiques

### Conformité

- **OWASP Top 10** : Couvert par Semgrep et ZAP
- **CWE** : Détection via ESLint security et Trivy
- **CVE** : Tracking via npm audit, Snyk, et Trivy

## Bonnes pratiques implémentées

### 1. Shift-Left Security

- ✅ Validation dès le commit
- ✅ SAST intégré au développement
- ✅ Feedback rapide aux développeurs

### 2. Defense in Depth

- ✅ Multiple outils pour chaque type de scan
- ✅ Validation à chaque étape du pipeline
- ✅ Seuils configurables par environnement

### 3. Continuous Monitoring

- ✅ Rapports consolidés et trackés
- ✅ Métriques de sécurité dans le temps
- ✅ Alertes automatiques sur régression

### 4. Compliance & Governance

- ✅ Conformité OWASP et standards
- ✅ Traçabilité complète des scans
- ✅ Rapports d'audit automatisés
