# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 1 - Séance 2 : Création d'Images avec Dockerfile

## Objectifs pédagogiques

- Maîtriser la syntaxe complète Dockerfile et ses instructions
- Optimiser la taille et sécurité des images Docker
- Implémenter des builds multi-stage pour la production
- Utiliser BuildKit et les fonctionnalités avancées

## Objectifs techniques

Dockerfile syntax, instructions avancées, multi-stage builds, BuildKit, image optimization, security best practices, layer caching, build automation

## Table des matières

1. [Fondamentaux Dockerfile](#1-fondamentaux-dockerfile)
2. [Instructions essentielles](#2-instructions-essentielles)
3. [Instructions avancées](#3-instructions-avancées)
4. [Multi-stage builds](#4-multi-stage-builds)
5. [Optimisation et sécurité](#5-optimisation-et-sécurité)
6. [BuildKit et fonctionnalités avancées](#6-buildkit-et-fonctionnalités-avancées)
7. [Récapitulatif et bonnes pratiques](#7-récapitulatif-et-bonnes-pratiques)

---

## 1. Fondamentaux Dockerfile

### 1.1 Qu'est-ce qu'un Dockerfile

#### Définition

Un **Dockerfile** est un fichier texte contenant une série d'instructions qui permettent à Docker de construire automatiquement une image. C'est le blueprint de votre conteneur.

**Principes fondamentaux** :

- Chaque instruction crée une nouvelle couche (layer)
- Les couches sont mises en cache pour optimiser les builds
- L'ordre des instructions influence les performances
- Les instructions sont exécutées séquentiellement

#### Structure de base

```dockerfile
# Commentaire
FROM image_de_base:tag
INSTRUCTION arguments
INSTRUCTION arguments
...
```

**Exemple simple** :

```dockerfile
FROM alpine:3.14
RUN apk add --no-cache curl
COPY app.sh /usr/local/bin/
CMD ["app.sh"]
```

### 1.2 Système de couches et cache

#### Fonctionnement des couches

```dockerfile
FROM ubuntu:20.04          # Couche 1: Image de base
RUN apt-get update         # Couche 2: Mise à jour des packages
RUN apt-get install -y git # Couche 3: Installation Git
COPY . /app               # Couche 4: Copie des fichiers
RUN make build            # Couche 5: Compilation
```

Chaque instruction `RUN`, `COPY`, `ADD` crée une nouvelle couche.

#### Optimisation du cache

**Mauvaise pratique** :

```dockerfile
COPY . /app          # Se réexécute à chaque changement de code
RUN npm install      # Cache invalidé à chaque fois
```

**Bonne pratique** :

```dockerfile
COPY package*.json /app/  # Cache préservé si package.json unchanged
RUN npm install           # Réutilise le cache si dépendances inchangées
COPY . /app              # Copie le code après installation
```

### 1.3 Application pratique - Premier Dockerfile

**LAB 1** - Dockerfile fondamental et optimisation : `S2_S1_S2_lab1_dockerfile_fondamental.md`

**Énoncé du LAB 1** :

Créer une image Python optimisée avec application Flask et bonnes pratiques.

- **Objectif** : Maîtriser les bases Dockerfile avec optimisation
- **Contexte** : API Flask simple avec dépendances et cache optimization
- **Instructions** :

  1. Créer une application Flask basique
  2. Écrire un Dockerfile optimisé pour le cache
  3. Tester les performances de build
  4. Analyser la taille de l'image

- **Critères d'évaluation** :

  - Dockerfile syntaxiquement correct
  - Application Flask fonctionnelle
  - Optimisation du cache démontrée
  - Analyse de taille réalisée

- **Durée estimée** : 20 minutes
- **Fichier de travail** : `S2_S1_S2_lab1_dockerfile_fondamental.md`
- **Correction** : `S2_S1_S2_correction_dockerfile_fondamental.md`

---

## 2. Instructions essentielles

### 2.1 FROM - Image de base

#### Syntaxe et variantes

```dockerfile
# Forme basique
FROM ubuntu:20.04

# Avec nom de stage (pour multi-stage)
FROM node:16-alpine AS builder

# Image scratch (vide)
FROM scratch

# Avec argument
ARG BASE_IMAGE=alpine:3.14
FROM $BASE_IMAGE
```

#### Choix de l'image de base

**Images recommandées** :

**Alpine Linux** (légère et sécurisée) :

```dockerfile
FROM alpine:3.14     # ~5MB
FROM node:16-alpine  # ~110MB vs node:16 (~900MB)
FROM python:3.9-alpine
```

**Distroless** (Google, ultra-sécurisée) :

```dockerfile
FROM gcr.io/distroless/java:11
FROM gcr.io/distroless/python3
```

**Slim variants** :

```dockerfile
FROM python:3.9-slim    # ~45MB vs python:3.9 (~880MB)
FROM node:16-slim
```

### 2.2 RUN - Exécution de commandes

#### Formes exec vs shell

**Forme shell** (recommandée pour scripts) :

```dockerfile
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*
```

**Forme exec** (recommandée pour sécurité) :

```dockerfile
RUN ["apt-get", "update"]
RUN ["/bin/bash", "-c", "echo hello"]
```

#### Optimisation des commandes RUN

**Mauvaise pratique** (multiple couches) :

```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get clean
```

**Bonne pratique** (une seule couche) :

```dockerfile
RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 2.3 COPY vs ADD

#### COPY (recommandé)

```dockerfile
# Copie simple
COPY src/ /app/

# Copie avec permissions
COPY --chown=app:app src/ /app/

# Copie depuis un stage (multi-stage)
COPY --from=builder /app/dist /app/
```

#### ADD (usage spécifique)

```dockerfile
# Extraction automatique d'archives
ADD app.tar.gz /app/

# Téléchargement d'URL (non recommandé)
ADD https://example.com/file.txt /app/
```

**Bonnes pratiques** :

- Préférer `COPY` à `ADD` sauf cas spécifiques
- Utiliser `.dockerignore` pour exclure des fichiers
- Copier les fichiers nécessaires à la fin

### 2.4 WORKDIR et ENV

#### WORKDIR (répertoire de travail)

```dockerfile
WORKDIR /app
# Équivalent à: RUN mkdir -p /app && cd /app

# Chemins relatifs s'appliquent à WORKDIR
COPY package.json .      # Copie vers /app/package.json
RUN npm install          # Exécuté dans /app
```

#### ENV (variables d'environnement)

```dockerfile
# Définition de variables
ENV NODE_ENV=production
ENV PORT=3000
ENV PATH="/app/bin:$PATH"

# Utilisation dans d'autres instructions
RUN echo "Environment: $NODE_ENV"
EXPOSE $PORT
```

---

## 3. Instructions avancées

### 3.1 ENTRYPOINT vs CMD

#### Différences fondamentales

**CMD** : Commande par défaut, peut être remplacée

```dockerfile
CMD ["node", "app.js"]
# docker run myapp → node app.js
# docker run myapp python script.py → python script.py
```

**ENTRYPOINT** : Point d'entrée fixe, arguments ajoutés

```dockerfile
ENTRYPOINT ["node"]
CMD ["app.js"]
# docker run myapp → node app.js
# docker run myapp script.js → node script.js
```

#### Patterns d'usage

**Script wrapper pattern** :

```dockerfile
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]
CMD ["app"]
```

**Application avec arguments** :

```dockerfile
ENTRYPOINT ["./myapp"]
CMD ["--help"]
```

### 3.2 USER et sécurité

#### Utilisateur non-root

```dockerfile
# Création d'un utilisateur
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Changement d'utilisateur
USER appuser

# Alternative avec numéro
USER 1001:1001
```

**Exemple complet** :

```dockerfile
FROM alpine:3.14
RUN adduser -D -s /bin/sh appuser
WORKDIR /app
COPY --chown=appuser:appuser . .
USER appuser
CMD ["./app"]
```

### 3.3 VOLUME et EXPOSE

#### VOLUME (points de montage)

```dockerfile
# Déclaration de volumes
VOLUME ["/data", "/logs"]

# Volume unique
VOLUME /var/lib/mysql
```

**Note** : VOLUME dans Dockerfile crée des volumes anonymes. Préférer `-v` lors du `docker run`.

#### EXPOSE (documentation des ports)

```dockerfile
# Port simple
EXPOSE 80

# Multiples ports
EXPOSE 80 443

# Avec protocole
EXPOSE 53/udp
EXPOSE 8080/tcp
```

**Important** : EXPOSE ne publie pas les ports, c'est documentaire. Utiliser `-p` avec `docker run`.

### 3.4 Application pratique - Instructions avancées

**LAB 2** - Build multi-stage et sécurité : `S2_S1_S2_lab2_multistage_securite.md`

**Énoncé du LAB 2** :

Implémenter un build multi-stage pour application Node.js avec sécurité renforcée.

- **Objectif** : Maîtriser multi-stage builds et sécurité
- **Contexte** : Application Node.js production-ready avec optimisation
- **Instructions** :

  1. Créer un Dockerfile multi-stage (build + production)
  2. Configurer utilisateur non-root
  3. Implémenter health checks
  4. Scanner les vulnérabilités

- **Critères d'évaluation** :

  - Multi-stage build fonctionnel
  - Sécurité configurée (utilisateur non-root)
  - Health checks opérationnels
  - Scan de vulnérabilités réalisé

- **Durée estimée** : 25 minutes
- **Fichier de travail** : `S2_S1_S2_lab2_multistage_securite.md`
- **Correction** : `S2_S1_S2_correction_multistage_securite.md`

---

## 4. Multi-stage builds

### 4.1 Concept et avantages

#### Problématique

**Build monolithique** :

```dockerfile
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install        # Inclut devDependencies
COPY . .
RUN npm run build      # Outils de build inclus dans l'image finale
EXPOSE 3000
CMD ["npm", "start"]
# Résultat: Image ~1GB avec outils de build
```

#### Solution multi-stage

```dockerfile
# Stage 1: Build
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:16-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
EXPOSE 3000
CMD ["node", "dist/server.js"]
# Résultat: Image ~150MB sans outils de build
```

### 4.2 Patterns avancés

#### Build avec compilation

```dockerfile
# Stage 1: Dependencies
FROM node:16 AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --frozen-lockfile

# Stage 2: Build
FROM node:16 AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:16-alpine AS runner
WORKDIR /app
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
CMD ["npm", "start"]
```

#### Stage avec outils spécialisés

```dockerfile
# Étape de test
FROM base AS testing
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run test
RUN npm run lint

# Étape de sécurité
FROM aquasec/trivy:latest AS security
COPY --from=builder /app /scan
RUN trivy fs --exit-code 1 /scan

# Production finale
FROM base AS production
COPY --from=builder /app/dist ./
# Seulement si tests et sécurité passent
```

### 4.3 Optimisation de taille

#### Comparaison des tailles

```dockerfile
# Image complète de développement
FROM node:16
# ... toutes les étapes
# Taille finale: ~950MB

# Multi-stage optimisé
FROM node:16-alpine AS production
# ... étapes optimisées
# Taille finale: ~85MB

# Distroless (production)
FROM gcr.io/distroless/nodejs18-debian11
# Taille finale: ~65MB
```

#### Techniques d'optimisation

**Nettoyage dans la même couche** :

```dockerfile
RUN apt-get update && \
    apt-get install -y build-essential && \
    npm install && \
    npm run build && \
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    npm cache clean --force
```

**Exclusion de fichiers** (.dockerignore) :

```dockerignore
node_modules
npm-debug.log
Dockerfile*
.dockerignore
.git
.gitignore
README.md
.env
.nyc_output
coverage
.pytest_cache
```

---

## 5. Optimisation et sécurité

### 5.1 Bonnes pratiques de sécurité

#### Utilisateur non-root obligatoire

```dockerfile
# Mauvaise pratique (root par défaut)
FROM alpine:3.14
COPY app /usr/local/bin/
CMD ["app"]

# Bonne pratique
FROM alpine:3.14
RUN adduser -D -s /bin/sh appuser
COPY --chown=appuser:appuser app /usr/local/bin/
USER appuser
CMD ["app"]
```

#### Gestion des secrets

**Mauvaise pratique** :

```dockerfile
# JAMAIS de secrets dans l'image
ENV API_KEY=secret123
RUN echo "password123" > /app/config
```

**Bonne pratique** :

```dockerfile
# Utiliser des build secrets (BuildKit)
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    curl -H "Authorization: $API_KEY" ...

# Ou variables d'environnement au runtime
ENV API_KEY=""
```

#### Scan de vulnérabilités

```bash
# Avec Trivy
trivy image myapp:latest

# Avec Docker Scout
docker scout cves myapp:latest

# Intégration dans Dockerfile
FROM aquasec/trivy:latest AS security-scan
COPY --from=builder /app /scan
RUN trivy fs --exit-code 1 /scan
```

### 5.2 Optimisation des performances

#### Cache des couches

```dockerfile
# Optimisé pour le cache
FROM python:3.9-slim
WORKDIR /app

# Étape 1: Dépendances (cache stable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 2: Code application (cache souvent invalidé)
COPY . .

# Étape 3: Configuration runtime
EXPOSE 8000
CMD ["python", "app.py"]
```

#### Réduction des métadonnées

```dockerfile
# Labels informatifs mais pas essentiels
LABEL maintainer="hassan.essadik@simplon.ma"
LABEL version="1.0.0"
LABEL description="API Flask optimisée"

# Suppression des métadonnées build
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*
```

### 5.3 Health checks avancés

#### HEALTHCHECK dans Dockerfile

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/
COPY app/ /usr/share/nginx/html/

# Health check simple
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Health check avancé
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1
```

#### Script de health check personnalisé

```dockerfile
COPY health-check.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/health-check.sh

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/usr/local/bin/health-check.sh"]
```

**health-check.sh** :

```bash
#!/bin/sh
# Vérification complète de l'application

# Test HTTP
if ! curl -f http://localhost:8080/health > /dev/null 2>&1; then
    echo "HTTP health check failed"
    exit 1
fi

# Test base de données
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "Database connection failed"
    exit 1
fi

echo "All health checks passed"
exit 0
```

---

## 6. BuildKit et fonctionnalités avancées

### 6.1 Activation de BuildKit

#### Configuration

```bash
# Variable d'environnement
export DOCKER_BUILDKIT=1

# Dans daemon.json
{
  "features": {
    "buildkit": true
  }
}

# Syntaxe dans Dockerfile
# syntax=docker/dockerfile:1.4
```

### 6.2 Fonctionnalités BuildKit

#### Build secrets

```dockerfile
# syntax=docker/dockerfile:1.4
FROM alpine
RUN --mount=type=secret,id=aws_access_key \
    AWS_ACCESS_KEY_ID=$(cat /run/secrets/aws_access_key) && \
    aws s3 cp s3://bucket/file /app/
```

```bash
# Build avec secret
echo "secret_value" | docker build --secret id=aws_access_key,src=- .
```

#### Cache mounts

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:16
WORKDIR /app

# Cache npm
RUN --mount=type=cache,target=/root/.npm \
    npm install

# Cache apt
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && apt-get install -y python3
```

#### SSH mounts

```dockerfile
# syntax=docker/dockerfile:1.4
FROM alpine
RUN apk add --no-cache openssh-client git
RUN --mount=type=ssh \
    git clone git@github.com:user/private-repo.git /app
```

### 6.3 Build multi-plateforme

```bash
# Build pour multiple architectures
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest .

# Création d'un builder
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```

### 6.4 Application pratique - BuildKit avancé

**LAB 3** - Image personnalisée avec BuildKit : `S2_S1_S2_lab3_buildkit_avance.md`

**Énoncé du LAB 3** :

Développer une image DevOps complète avec outils intégrés, optimisation BuildKit et préparation CI/CD.

- **Objectif** : Maîtriser BuildKit et optimisation avancée
- **Contexte** : Image DevOps avec multiple outils et CI/CD ready
- **Instructions** :

  1. Créer une image avec outils DevOps (kubectl, helm, terraform)
  2. Utiliser BuildKit cache mounts et secrets
  3. Implémenter multi-stage avec optimisation
  4. Préparer pour intégration CI/CD

- **Critères d'évaluation** :

  - Image DevOps complète avec outils
  - BuildKit features utilisées (cache, secrets)
  - Multi-stage optimisé
  - CI/CD ready

- **Durée estimée** : 35 minutes
- **Fichier de travail** : `S2_S1_S2_lab3_buildkit_avance.md`
- **Correction** : `S2_S1_S2_correction_buildkit_avance.md`

---

## 7. Récapitulatif et bonnes pratiques

### Points clés de la séance

**Maîtrise Dockerfile** :

- Instructions essentielles et avancées
- Multi-stage builds pour optimisation
- Sécurité et utilisateurs non-root
- BuildKit pour fonctionnalités avancées

**Optimisation** :

- Cache des couches efficace
- Réduction de taille des images
- Health checks intégrés
- Performance de build

**Sécurité** :

- Utilisateur non-root obligatoire
- Gestion des secrets sécurisée
- Scan de vulnérabilités
- Images de base minimalistes

### Préparation séance suivante

La **Séance 3 - Images Registries** s'appuiera sur ces bases pour :

- Publier et distribuer les images créées
- Configurer des registries privés
- Implémenter des stratégies de versioning
- Automatiser la distribution multi-environnements

### Validation des acquis

- Dockerfile multi-stage fonctionnel
- Images optimisées (taille < 100MB pour applications simples)
- Sécurité de base implémentée
- BuildKit features utilisées

---

_Formateur : Hassan ESSADIK | Sprint 2 - Semaine 1 - Séance 2_
