# LAB 3 - Image personnalisée avec BuildKit

## Informations générales

- **Sprint** : 2 - Containerisation et CI/CD
- **Semaine** : 1 - Docker Basics
- **Séance** : 2 - Dockerfile Creation
- **LAB** : 3/3
- **Durée estimée** : 35 minutes
- **Formateur** : Hassan ESSADIK

## Objectifs pédagogiques

- Créer une image DevOps complète avec outils intégrés
- Maîtriser les fonctionnalités avancées de BuildKit
- Optimiser avec cache mounts et build secrets
- Préparer une image CI/CD ready

## Contexte

Vous devez développer une image Docker personnalisée contenant un ensemble d'outils DevOps (kubectl, helm, terraform, azure-cli) optimisée pour les pipelines CI/CD, en utilisant les fonctionnalités avancées de BuildKit.

## Prérequis techniques

- Docker Desktop avec BuildKit activé
- Accès internet pour téléchargement des outils
- Connaissance des outils DevOps (kubectl, helm, terraform)
- Expérience avec les secrets et les caches

## Instructions

### Étape 1 : Architecture et planification (5 minutes)

Créez la structure suivante :

```
lab3-buildkit/
├── Dockerfile
├── scripts/
│   ├── install-tools.sh
│   ├── entrypoint.sh
│   └── health-check.sh
├── configs/
│   ├── terraform.tf
│   ├── kube-config.yaml
│   └── helm-values.yaml
├── .dockerignore
├── docker-compose.yml
└── README.md
```

**Outils à intégrer** :

- kubectl (Kubernetes CLI)
- helm (Kubernetes package manager)
- terraform (Infrastructure as Code)
- azure-cli (Azure CLI)
- git, curl, jq (utilitaires)
- docker-cli (pour Docker-in-Docker scenarios)

### Étape 2 : Scripts d'installation (10 minutes)

**Fichier `scripts/install-tools.sh`** :

```bash
#!/bin/bash
set -euo pipefail

# Configuration des versions
KUBECTL_VERSION="v1.28.2"
HELM_VERSION="v3.12.3"
TERRAFORM_VERSION="1.5.7"
AZURE_CLI_VERSION="2.52.0"

echo "=== Installation des outils DevOps ==="

# Mise à jour du système
apk update && apk upgrade
apk add --no-cache \
    curl \
    wget \
    git \
    jq \
    bash \
    openssh-client \
    ca-certificates \
    python3 \
    py3-pip \
    nodejs \
    npm

# Installation kubectl
echo "Installation kubectl ${KUBECTL_VERSION}..."
curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin/

# Installation Helm
echo "Installation Helm ${HELM_VERSION}..."
wget https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz
tar -zxvf helm-${HELM_VERSION}-linux-amd64.tar.gz
mv linux-amd64/helm /usr/local/bin/
rm -rf linux-amd64 helm-${HELM_VERSION}-linux-amd64.tar.gz

# Installation Terraform
echo "Installation Terraform ${TERRAFORM_VERSION}..."
wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip
mv terraform /usr/local/bin/
rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Installation Azure CLI
echo "Installation Azure CLI ${AZURE_CLI_VERSION}..."
pip3 install azure-cli==${AZURE_CLI_VERSION}

# Installation d'outils supplémentaires
echo "Installation d'outils complémentaires..."
npm install -g @azure/static-web-apps-cli
pip3 install awscli ansible

# Vérification des installations
echo "=== Vérification des installations ==="
kubectl version --client
helm version
terraform version
az version
git --version
jq --version

echo "=== Installation terminée ==="
```

**Fichier `scripts/entrypoint.sh`** :

```bash
#!/bin/bash
set -e

# Configuration de l'environnement
export PATH="/usr/local/bin:$PATH"
export KUBECONFIG="${KUBECONFIG:-/app/configs/kube-config.yaml}"
export TF_DATA_DIR="${TF_DATA_DIR:-/app/.terraform}"

# Fonction d'aide
show_help() {
    cat << EOF
DevOps Toolbox Container
========================

Outils disponibles:
  kubectl     - Kubernetes CLI
  helm        - Kubernetes Package Manager
  terraform   - Infrastructure as Code
  az          - Azure CLI
  git         - Version Control
  jq          - JSON Processor

Utilisation:
  docker run devops-toolbox:latest kubectl get pods
  docker run devops-toolbox:latest terraform plan
  docker run devops-toolbox:latest az login

Variables d'environnement:
  KUBECONFIG  - Chemin vers le fichier kubeconfig
  TF_DATA_DIR - Répertoire de données Terraform
  AZURE_SUBSCRIPTION_ID - ID de souscription Azure

EOF
}

# Gestion des signaux
trap 'echo "Arrêt gracieux..."; exit 0' SIGTERM SIGINT

# Si aucun argument, afficher l'aide
if [ $# -eq 0 ]; then
    show_help
    exec "$@"
fi

# Exécution de la commande
echo "Exécution: $*"
exec "$@"
```

**Fichier `scripts/health-check.sh`** :

```bash
#!/bin/bash
set -e

# Vérification de la santé des outils
check_tool() {
    local tool=$1
    local version_cmd=$2

    if command -v "$tool" >/dev/null 2>&1; then
        echo "✓ $tool: $(eval $version_cmd)"
        return 0
    else
        echo "✗ $tool: Non disponible"
        return 1
    fi
}

echo "=== Health Check DevOps Tools ==="

# Vérification des outils principaux
check_tool "kubectl" "kubectl version --client --short"
check_tool "helm" "helm version --short"
check_tool "terraform" "terraform version"
check_tool "az" "az --version | head -1"
check_tool "git" "git --version"
check_tool "jq" "jq --version"

# Vérification des répertoires
echo -e "\n=== Vérification des répertoires ==="
[ -d "/app" ] && echo "✓ /app existe" || echo "✗ /app manquant"
[ -d "/app/configs" ] && echo "✓ /app/configs existe" || echo "✗ /app/configs manquant"

# Vérification des permissions
echo -e "\n=== Vérification des permissions ==="
[ -r "/app/configs" ] && echo "✓ Lecture configs OK" || echo "✗ Problème lecture configs"

echo -e "\n=== Health Check terminé ==="
```

### Étape 3 : Dockerfile avec BuildKit avancé (15 minutes)

**Dockerfile complet** :

```dockerfile
# syntax=docker/dockerfile:1.4

# ===== ARGUMENTS DE BUILD =====
ARG ALPINE_VERSION=3.18
ARG KUBECTL_VERSION=v1.28.2
ARG HELM_VERSION=v3.12.3
ARG TERRAFORM_VERSION=1.5.7
ARG AZURE_CLI_VERSION=2.52.0

# ===== STAGE 1: Base Alpine avec cache =====
FROM alpine:${ALPINE_VERSION} AS base

# Installation des packages de base avec cache mount
RUN --mount=type=cache,target=/var/cache/apk \
    --mount=type=cache,target=/var/lib/apk \
    apk update && \
    apk add --no-cache \
        bash \
        curl \
        wget \
        git \
        jq \
        openssh-client \
        ca-certificates \
        python3 \
        py3-pip \
        nodejs \
        npm \
        unzip \
        tar \
        gzip

# ===== STAGE 2: Installation des outils avec secrets =====
FROM base AS tools-installer

# Utilisation de secrets pour les clés API (si nécessaire)
RUN --mount=type=secret,id=github_token,required=false \
    --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/root/.cache/pip \
    if [ -f /run/secrets/github_token ]; then \
        export GITHUB_TOKEN=$(cat /run/secrets/github_token); \
        echo "GitHub token configuré"; \
    fi

# Installation kubectl avec cache
ARG KUBECTL_VERSION
RUN --mount=type=cache,target=/tmp/downloads \
    if [ ! -f /tmp/downloads/kubectl-${KUBECTL_VERSION} ]; then \
        curl -L "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
        -o /tmp/downloads/kubectl-${KUBECTL_VERSION}; \
    fi && \
    cp /tmp/downloads/kubectl-${KUBECTL_VERSION} /usr/local/bin/kubectl && \
    chmod +x /usr/local/bin/kubectl

# Installation Helm avec cache
ARG HELM_VERSION
RUN --mount=type=cache,target=/tmp/downloads \
    if [ ! -f /tmp/downloads/helm-${HELM_VERSION}.tar.gz ]; then \
        wget https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz \
        -O /tmp/downloads/helm-${HELM_VERSION}.tar.gz; \
    fi && \
    tar -C /tmp -zxf /tmp/downloads/helm-${HELM_VERSION}.tar.gz && \
    mv /tmp/linux-amd64/helm /usr/local/bin/ && \
    rm -rf /tmp/linux-amd64

# Installation Terraform avec cache
ARG TERRAFORM_VERSION
RUN --mount=type=cache,target=/tmp/downloads \
    if [ ! -f /tmp/downloads/terraform-${TERRAFORM_VERSION}.zip ]; then \
        wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
        -O /tmp/downloads/terraform-${TERRAFORM_VERSION}.zip; \
    fi && \
    unzip /tmp/downloads/terraform-${TERRAFORM_VERSION}.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/terraform

# Installation Azure CLI avec cache pip
ARG AZURE_CLI_VERSION
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir azure-cli==${AZURE_CLI_VERSION}

# Installation d'outils complémentaires
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/root/.cache/pip \
    npm install -g @azure/static-web-apps-cli && \
    pip3 install --no-cache-dir awscli ansible

# ===== STAGE 3: Validation et tests =====
FROM tools-installer AS validator

# Copie des scripts de test
COPY scripts/health-check.sh /tmp/
RUN chmod +x /tmp/health-check.sh && /tmp/health-check.sh

# ===== STAGE 4: Image finale production =====
FROM alpine:${ALPINE_VERSION} AS production

# Métadonnées
LABEL maintainer="hassan.essadik@simplon.ma"
LABEL version="1.0.0"
LABEL description="DevOps Toolbox with kubectl, helm, terraform, azure-cli"
LABEL org.opencontainers.image.source="https://github.com/simplon-devops/toolbox"

# Installation des runtime dependencies uniquement
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
        bash \
        curl \
        git \
        jq \
        openssh-client \
        ca-certificates \
        python3 \
        py3-pip \
        nodejs \
        npm

# Création de l'utilisateur non-root
RUN addgroup -g 1001 -S devops && \
    adduser -u 1001 -S devops -G devops -h /app

# Copie des outils depuis le stage précédent
COPY --from=tools-installer /usr/local/bin/kubectl /usr/local/bin/
COPY --from=tools-installer /usr/local/bin/helm /usr/local/bin/
COPY --from=tools-installer /usr/local/bin/terraform /usr/local/bin/
COPY --from=tools-installer /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=tools-installer /usr/local/bin/az /usr/local/bin/

# Copie des scripts
COPY --chown=devops:devops scripts/ /app/scripts/
RUN chmod +x /app/scripts/*.sh

# Copie des configurations
COPY --chown=devops:devops configs/ /app/configs/

# Configuration de l'environnement
ENV PATH="/usr/local/bin:$PATH"
ENV KUBECONFIG="/app/configs/kube-config.yaml"
ENV TF_DATA_DIR="/app/.terraform"
ENV ANSIBLE_CONFIG="/app/configs/ansible.cfg"

# Répertoires de travail
WORKDIR /app
RUN chown -R devops:devops /app

# Passage à l'utilisateur non-root
USER devops

# Health check avancé
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD ["/app/scripts/health-check.sh"]

# Point d'entrée
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["--help"]
```

### Étape 4 : Fichiers de configuration (5 minutes)

**Fichier `configs/terraform.tf`** :

```hcl
# Configuration Terraform par défaut
terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

# Provider Azure
provider "azurerm" {
  features {}
}

# Provider Kubernetes
provider "kubernetes" {
  config_path = var.kubeconfig_path
}

variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "/app/configs/kube-config.yaml"
}
```

**Fichier `configs/helm-values.yaml`** :

```yaml
# Valeurs par défaut pour Helm
global:
  imageRegistry: ''
  imagePullSecrets: []

# Configuration du monitoring
monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true

# Configuration de sécurité
security:
  runAsNonRoot: true
  runAsUser: 1001
  fsGroup: 1001

# Configuration des ressources
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

**Fichier `docker-compose.yml`** :

```yaml
version: '3.8'

services:
  devops-toolbox:
    build:
      context: .
      dockerfile: Dockerfile
      secrets:
        - github_token
      args:
        - KUBECTL_VERSION=v1.28.2
        - HELM_VERSION=v3.12.3
        - TERRAFORM_VERSION=1.5.7
    image: devops-toolbox:latest
    container_name: devops-tools
    volumes:
      - ./workdir:/app/workspace
      - ~/.kube:/app/.kube:ro
      - ~/.azure:/app/.azure:ro
    environment:
      - KUBECONFIG=/app/.kube/config
      - AZURE_CONFIG_DIR=/app/.azure
    networks:
      - devops-net

  # Service de test
  test-runner:
    image: devops-toolbox:latest
    depends_on:
      - devops-toolbox
    command: /app/scripts/health-check.sh
    networks:
      - devops-net

networks:
  devops-net:
    driver: bridge

secrets:
  github_token:
    file: ./secrets/github_token.txt
```

**Fichier `.dockerignore`** :

```dockerignore
.git
.gitignore
README.md
.vscode/
.idea/
*.log
.env*
node_modules/
.terraform/
.terraform.lock.hcl
*.tfstate
*.tfstate.backup
.kube/
.azure/
secrets/
workdir/
```

## Tests et validations

### Test du build avec BuildKit

```bash
# Activation de BuildKit
export DOCKER_BUILDKIT=1

# Build avec cache et secrets
echo "EXEMPLE_TOKEN_GITHUB_FORMATION" > secrets/github_token.txt
docker build \
  --secret id=github_token,src=secrets/github_token.txt \
  --build-arg KUBECTL_VERSION=v1.28.2 \
  -t devops-toolbox:latest .

# Test des couches
docker history devops-toolbox:latest

# Analyse de la taille
docker images devops-toolbox:latest
```

### Tests fonctionnels

```bash
# Test des outils principaux
docker run --rm devops-toolbox:latest kubectl version --client
docker run --rm devops-toolbox:latest helm version
docker run --rm devops-toolbox:latest terraform version
docker run --rm devops-toolbox:latest az --version

# Test avec montage de volumes
docker run --rm \
  -v $(pwd)/workdir:/app/workspace \
  devops-toolbox:latest \
  kubectl get nodes --kubeconfig=/app/workspace/config

# Test du health check
docker run --rm devops-toolbox:latest /app/scripts/health-check.sh
```

### Tests CI/CD

```bash
# Test avec Docker Compose
docker-compose up --build test-runner

# Simulation pipeline CI/CD
docker run --rm \
  -v $(pwd)/ci-scripts:/scripts \
  devops-toolbox:latest \
  bash /scripts/deploy.sh
```

## Livrables attendus

### 1. Image DevOps complète

- [ ] Tous les outils intégrés et fonctionnels
- [ ] Scripts d'installation robustes
- [ ] Configuration par défaut fournie
- [ ] Documentation des outils

### 2. BuildKit features utilisées

- [ ] Cache mounts implémentés et testés
- [ ] Build secrets configurés
- [ ] Multi-stage build optimisé
- [ ] Parallélisation des téléchargements

### 3. Multi-stage optimisé

- [ ] Séparation claire des responsabilités
- [ ] Optimisation de la taille finale
- [ ] Validation intégrée
- [ ] Production-ready

### 4. CI/CD ready

- [ ] Docker Compose configuré
- [ ] Scripts d'automatisation
- [ ] Intégration secrets
- [ ] Tests automatisés

## Critères d'évaluation

**Outils DevOps** : Intégration complète des outils requis
**BuildKit** : Utilisation avancée cache et secrets
**Optimisation** : Multi-stage efficace et optimisé
**CI/CD** : Préparation pour pipelines automatisés

## Bonus (optionnel)

### Monitoring intégré

Ajoutez Prometheus et Grafana :

```dockerfile
# Stage monitoring
FROM prom/prometheus:latest AS monitoring
COPY prometheus.yml /etc/prometheus/

# Intégration dans l'image finale
COPY --from=monitoring /bin/prometheus /usr/local/bin/
```

### Auto-update des outils

Script de mise à jour automatique :

```bash
#!/bin/bash
# auto-update.sh
check_and_update() {
    local tool=$1
    local current_version=$2
    local latest_version=$(get_latest_version $tool)

    if [ "$current_version" != "$latest_version" ]; then
        echo "Mise à jour disponible pour $tool: $latest_version"
        update_tool $tool $latest_version
    fi
}
```

## Ressources complémentaires

- [BuildKit features](https://docs.docker.com/buildx/working-with-buildx/)
- [Multi-stage builds best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes tools](https://kubernetes.io/docs/tasks/tools/)
- [Terraform CLI](https://www.terraform.io/docs/cli/index.html)

---

**Note importante** : Cette image sera utilisée dans les prochains sprints pour les déploiements et l'orchestration. Assurez-vous qu'elle soit robuste et bien documentée.
