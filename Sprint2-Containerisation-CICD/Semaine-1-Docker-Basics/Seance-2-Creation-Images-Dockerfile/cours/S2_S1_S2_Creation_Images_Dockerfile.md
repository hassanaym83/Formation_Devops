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
# INSTRUCTION FROM: Définit l'image de base
# Alpine 3.14 = distribution Linux ultra-légère (~5MB)
# Parfaite pour la containerisation (sécurisée et rapide)
FROM alpine:3.14

# INSTRUCTION RUN: Exécute une commande pendant la construction
# apk = gestionnaire de paquets Alpine Package Keeper
# --no-cache = évite de stocker l'index des paquets (économise l'espace)
# curl = outil de transfert de données réseau
RUN apk add --no-cache curl

# INSTRUCTION COPY: Copie un fichier depuis l'hôte vers l'image
# Source: app.sh (script shell local)
# Destination: /usr/local/bin/ (répertoire standard pour exécutables)
COPY app.sh /usr/local/bin/

# INSTRUCTION CMD: Commande par défaut exécutée au démarrage du conteneur
# Format exec: ["executable", "param1", "param2"] (plus sûr que format shell)
# app.sh sera accessible depuis n'importe où grâce au PATH
CMD ["app.sh"]
```

### 1.2 Système de couches et cache

#### Fonctionnement des couches

```dockerfile
# COUCHE 1: Image de base Ubuntu 20.04 LTS
# Taille: ~72MB, système complet avec outils standard
# Cette couche est partagée entre toutes les images Ubuntu 20.04
FROM ubuntu:20.04

# COUCHE 2: Mise à jour de l'index des paquets
# apt-get update télécharge la liste des paquets disponibles
# Cette étape est cruciale avant toute installation
RUN apt-get update

# COUCHE 3: Installation de Git
# -y = accepter automatiquement les confirmations
# Chaque RUN crée une nouvelle couche dans l'image finale
RUN apt-get install -y git

# COUCHE 4: Copie du code source
# "." = répertoire courant sur l'hôte (contexte de build)
# "/app" = destination dans le conteneur
COPY . /app

# COUCHE 5: Compilation de l'application
# make build exécute le processus de compilation défini dans Makefile
# Cette couche contient les artefacts de build
RUN make build
```

Chaque instruction `RUN`, `COPY`, `ADD` crée une nouvelle couche.

#### Optimisation du cache

**Mauvaise pratique** :

```dockerfile
# PROBLÈME: Copie tout le code en premier
# Conséquence: Chaque modification de code invalide le cache
# Résultat: npm install se réexécute à chaque build (lent et coûteux)
COPY . /app          # [ERREUR] Invalidation du cache à chaque changement
RUN npm install      # [ERREUR] Cache invalidé, réinstallation complète des dépendances
```

**Bonne pratique** :

```dockerfile
# SOLUTION: Copier les fichiers de dépendances en premier
# package*.json change rarement par rapport au code source
# Cette stratégie optimise le cache Docker pour des builds plus rapides
COPY package*.json /app/  # [OK] Cache stable si dépendances inchangées
RUN npm install           # [OK] Réutilise le cache, installation rapide
COPY . /app              # [OK] Copie le code après installation des dépendances
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

### 2.1 FROM - Image de base et architecture des conteneurs

#### Contexte fondamental

**Principe architectural** :
L'instruction FROM définit l'image de base sur laquelle votre conteneur sera construit. C'est la fondation de votre application conteneurisée, comparable au système d'exploitation d'une machine virtuelle, mais en beaucoup plus léger et optimisé.

**Impact critique** : Le choix de l'image de base influence directement :

- **Taille finale** : De quelques MB à plusieurs GB
- **Sécurité** : Nombre de vulnérabilités potentielles
- **Performance** : Temps de téléchargement et démarrage
- **Compatibilité** : Support des dépendances applicatives

#### Syntaxe et variantes expliquées

```dockerfile
# FORME BASIQUE - Image standard avec version
# ubuntu:20.04 = Distribution Ubuntu version 20.04 LTS
# Avantage: Stabilité à long terme, compatibilité étendue
# Inconvénient: Taille importante (~72MB base)
FROM ubuntu:20.04

# FORME MULTI-STAGE - Image avec nom de stage
# AS builder = Nom du stage pour référence dans d'autres stages
# node:16-alpine = Version Node.js 16 sur base Alpine
# Usage: Construction en plusieurs étapes pour optimisation
FROM node:16-alpine AS builder

# IMAGE SCRATCH - Base vide pour applications compilées
# scratch = Image virtuelle complètement vide (0 byte)
# Usage: Langages compilés (Go, Rust) produisant des binaires statiques
# Avantage: Sécurité maximale, taille minimale
FROM scratch

# FORME AVEC ARGUMENT - Image de base paramétrable
# ARG = Argument de build modifiable au moment de la construction
# Usage: Flexibilité pour différents environnements (dev, prod)
ARG BASE_IMAGE=alpine:3.14
FROM $BASE_IMAGE
```

#### Choix stratégique de l'image de base

**Critères de sélection** :

1. **Taille de l'image** : Impact sur les temps de déploiement
2. **Sécurité** : Nombre de paquets et vulnérabilités
3. **Compatibilité** : Support des dépendances nécessaires
4. **Maintenance** : Fréquence des mises à jour sécurité

**Images recommandées par catégorie** :

**Alpine Linux** - Option légère et sécurisée :

```dockerfile
# ALPINE DE BASE
# Avantages: Très légère (~5MB), sécurisée, musl libc
# Inconvénients: Compatibilité limitée avec certaines bibliothèques
FROM alpine:3.14     # Base minimale pour scripts shell, Go

# ALPINE AVEC RUNTIME
# node:16-alpine = Node.js 16 + Alpine base
# Économie: ~790MB (900MB - 110MB) par rapport à node:16 standard
FROM node:16-alpine  # 110MB vs node:16 (900MB)

# PYTHON SUR ALPINE
# python:3.9-alpine = Python 3.9 + Alpine + pip
# Cas d'usage: APIs Flask/FastAPI, scripts d'automatisation
FROM python:3.9-alpine
```

**Distroless** - Sécurité maximale (Google) :

```dockerfile
# JAVA DISTROLESS
# Contenu: JVM + bibliothèques essentielles UNIQUEMENT
# Avantages: Aucun shell, aucun gestionnaire de paquets
# Sécurité: Surface d'attaque minimale
FROM gcr.io/distroless/java:11

# PYTHON DISTROLESS
# Contenu: Python runtime + bibliothèques standard
# Usage: Applications Python en production haute sécurité
FROM gcr.io/distroless/python3
```

**Variants Slim** - Compromis taille/fonctionnalité :

```dockerfile
# PYTHON SLIM
# Contenu: Python + outils de base (sans développement)
# Économie: ~835MB (économie de 95% par rapport à python:3.9)
FROM python:3.9-slim    # 45MB vs python:3.9 (880MB)

# NODE.JS SLIM
# Contenu: Node.js + npm + outils système de base
# Usage: Applications de production sans outils de build
FROM node:16-slim
```

**Tableau comparatif des images** :

| Type       | Taille    | Sécurité | Compatibilité | Usage recommandé           |
| ---------- | --------- | -------- | ------------- | -------------------------- |
| Standard   | 500MB-1GB | Moyenne  | Élevée        | Développement, prototypage |
| Alpine     | 50-150MB  | Élevée   | Moyenne       | Production légère          |
| Slim       | 100-300MB | Bonne    | Élevée        | Production standard        |
| Distroless | 20-100MB  | Maximale | Limitée       | Production haute sécurité  |

### 2.2 RUN - Exécution de commandes et gestion des couches

#### Contexte technique fondamental

**Principe de fonctionnement** :
L'instruction RUN exécute des commandes pendant la phase de construction de l'image. Chaque RUN crée une nouvelle couche dans l'image finale, ce qui a un impact direct sur la taille et les performances. La maîtrise de cette instruction est cruciale pour l'optimisation.

**Impact sur l'architecture** :

- **Couches** : Chaque RUN = une couche permanente
- **Cache** : Réutilisation possible si les commandes sont identiques
- **Taille** : Accumulation des artefacts temporaires
- **Performance** : Temps de build et de téléchargement

#### Formes d'exécution expliquées

**Forme shell** - Recommandée pour scripts complexes :

```dockerfile
# FORME SHELL: Exécution via /bin/sh -c
# Avantages: Variables d'environnement, pipes, redirections
# Usage: Scripts complexes, chaînage de commandes

RUN apt-get update && apt-get install -y \
    # INSTALLATION DE PAQUETS MULTIPLES
    # \\ = Continuation de ligne pour lisibilité
    curl \
    wget \
    # NETTOYAGE DANS LA MÊMĝ COUCHE
    # rm -rf: Suppression du cache APT (peut représenter plusieurs MB)
    && rm -rf /var/lib/apt/lists/*

# AVANTAGES:
# - Chaînage avec && (arrêt si échec)
# - Variables d'environnement automatiquement substituées
# - Pipes et redirections disponibles
# - Une seule couche créée malgré plusieurs commandes
```

**Forme exec** - Recommandée pour sécurité et précision :

```dockerfile
# FORME EXEC: Exécution directe sans shell
# Avantages: Pas d'interprétation shell, sécurité renforcée
# Usage: Commandes précises, environnements sécurisés

# COMMANDE SIMPLE AVEC ARGUMENTS EXPLICITES
RUN ["apt-get", "update"]

# EXÉCUTION AVEC SHELL SPÉCIFIQUE
# /bin/bash: Shell plus riche que /bin/sh par défaut
# -c: Exécuter la commande fournie en argument
RUN ["/bin/bash", "-c", "echo hello"]

# AVANTAGES:
# - Pas d'interprétation shell (sécurité)
# - Arguments échappés automatiquement
# - Comportement prévisible
# - Pas de substitution de variables non désirée
```

#### Optimisation critique des commandes RUN

**Principe fondamental** : Minimiser le nombre de couches et l'accumulation d'artefacts temporaires.

**Mauvaise pratique** - Multiple couches problématiques :

```dockerfile
# PROBLÈME: Chaque RUN crée une couche distincte
# Conséquence: Accumulation des artefacts dans chaque couche

# COUCHE 1: Mise à jour de l'index des paquets
RUN apt-get update           # ~10MB (index des paquets)

# COUCHE 2: Installation de curl
RUN apt-get install -y curl  # ~15MB (curl + dépendances)

# COUCHE 3: Installation de wget
RUN apt-get install -y wget  # ~12MB (wget + dépendances)

# COUCHE 4: Tentative de nettoyage
RUN apt-get clean            # ~0MB (mais les caches précédents restent)

# RÉSULTAT PROBLÉMATIQUE:
# - 4 couches distinctes dans l'image finale
# - Taille totale: ~37MB au lieu de ~12MB optimisé
# - Caches temporaires préservés dans les couches intermédiaires
# - Temps de build plus long (invalidation de cache fréquente)
```

**Bonne pratique** - Optimisation en une seule couche :

```dockerfile
# SOLUTION: Chaînage de toutes les opérations dans un seul RUN
# Avantage: Une seule couche contenant uniquement le résultat final

RUN apt-get update && \
    # INSTALLATION GROUPÉE DE PAQUETS
    # -y: Accepter automatiquement les confirmations
    # Format multi-ligne pour la lisibilité
    apt-get install -y \
        curl \
        wget \
    # NETTOYAGE DANS LA MÊMĝ INSTRUCTION
    # apt-get clean: Supprime le cache des paquets téléchargés
    && apt-get clean \
    # SUPPRESSION COMPLÈTE DES MÉTADONNÉES APT
    # /var/lib/apt/lists/*: Index des paquets disponibles
    # Peut représenter plusieurs dizaines de MB
    && rm -rf /var/lib/apt/lists/*

# RÉSULTAT OPTIMISÉ:
# - 1 seule couche dans l'image finale
# - Taille: ~12MB (seulement les binaires installés)
# - Aucun cache temporaire conservé
# - Build plus efficace et cache mieux utilisé
```

**Techniques d'optimisation avancées** :

```dockerfile
# OPTIMISATION AVEC VARIABLES TEMPORAIRES
RUN set -eux; \
    # set -e: Arrêt en cas d'erreur
    # set -u: Erreur si variable non définie
    # set -x: Mode debug (affichage des commandes)
    \
    # INSTALLATION AVEC GESTION D'ERREUR
    apt-get update && \
    apt-get install -y --no-install-recommends \
        # --no-install-recommends: Évite les paquets "recommandés"
        # Réduction significative de la taille
        build-essential \
        python3-dev \
    && \
    # COMPILATION/INSTALLATION PERSONNALISÉE
    pip install --no-cache-dir some-package && \
    # NETTOYAGE COMPLET
    apt-get purge -y build-essential python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# TECHNIQUES APPLIQUÉES:
# - Suppression des outils de build après usage
# - Éviction des paquets recommandés non essentiels
# - Nettoyage complet des répertoires temporaires
# - Gestion d'erreur robuste
```

### 2.3 COPY vs ADD - Gestion des fichiers et bonnes pratiques

#### Contexte et choix technique

**Problématique** :
Docker propose deux instructions pour intégrer des fichiers dans l'image : COPY et ADD. Bien qu'apparemment similaires, elles ont des comportements distincts qui influencent la sécurité, les performances et la maintenabilité de vos images.

**Règle générale** : Toujours utiliser COPY sauf besoin spécifique d'ADD.

#### COPY - Instruction recommandée

**Principe** : Copie simple et transparente de fichiers locaux vers l'image.

```dockerfile
# COPIE SIMPLE DE RÉPERTOIRE
# src/: Répertoire source sur l'hôte (relatif au contexte de build)
# /app/: Répertoire destination dans l'image
# Comportement: Copie récursive en préservant la structure
COPY src/ /app/

# COPIE AVEC GESTION DES PERMISSIONS
# --chown: Change le propriétaire directement à la copie
# app:app: Utilisateur:Groupe de destination
# Avantage: Évite une instruction RUN supplémentaire pour chown
COPY --chown=app:app src/ /app/

# COPIE DEPUIS UN STAGE MULTI-STAGE
# --from=builder: Référence au stage "builder"
# /app/dist: Artefacts compilés du stage de build
# Usage: Récupération d'artefacts optimisés
COPY --from=builder /app/dist /app/

# COPIE SÉLECTIVE AVEC PATTERNS
# package*.json: Glob pattern pour package.json et package-lock.json
# Optimisation: Cache Docker préservé si dependencies inchangées
COPY package*.json ./
```

#### ADD - Usage spécifique et limité

**Principe** : Copie avec fonctionnalités avancées (extraction, téléchargement).

```dockerfile
# EXTRACTION AUTOMATIQUE D'ARCHIVES
# app.tar.gz: Archive compressée sur l'hôte
# /app/: Répertoire de destination
# Comportement: ADD extrait automatiquement l'archive
# Formats supportés: tar, gzip, bzip2, xz
ADD app.tar.gz /app/

# TÉLÉCHARGEMENT D'URL (NON RECOMMANDÉ)
# https://example.com/file.txt: URL distante
# Problèmes: Pas de cache, vulnérabilités, erreurs réseau
# Alternative recommandée: RUN curl/wget + COPY
ADD https://example.com/file.txt /app/
```

#### Comparaison technique détaillée

| Fonctionnalité   | COPY                       | ADD                          |
| ---------------- | -------------------------- | ---------------------------- |
| **Copie simple** | ✅ Recommandé              | ✅ Possible                  |
| **Transparence** | ✅ Comportement prévisible | ⚠️ Logique complexe          |
| **Performance**  | ✅ Rapide et efficace      | ⚠️ Plus lent (vérifications) |
| **Sécurité**     | ✅ Sécurisé                | ⚠️ Risques avec URLs         |
| **Extraction**   | ❌ Non                     | ✅ Automatique               |
| **URLs**         | ❌ Non                     | ✅ Support natif             |
| **Cache Docker** | ✅ Optimal                 | ⚠️ Peut être invalidé        |

#### Bonnes pratiques appliquées

```dockerfile
# PATTERN RECOMMANDÉ: Étapes séparées pour optimiser le cache

# 1. COPIE DES DÉPENDANCES D'ABORD
# Avantage: Cache stable si dépendances inchangées
COPY requirements.txt ./
COPY package.json package-lock.json ./

# 2. INSTALLATION DES DÉPENDANCES
# Exécuté seulement si fichiers de dépendances modifiés
RUN pip install -r requirements.txt
RUN npm ci --only=production

# 3. COPIE DU CODE APPLICATION
# Exécuté à chaque modification du code source
COPY src/ ./src/
COPY app.py ./

# 4. GESTION DES FICHIERS À EXCLURE
# .dockerignore: Liste des fichiers/répertoires à ignorer
# Contenu type:
# node_modules/
# .git/
# *.log
# .env
```

**Règles de sécurité et performance** :

- **Préférer COPY** : Plus prévisible et sécurisé
- **Utiliser .dockerignore** : Réduit la taille du contexte de build
- **Copier les fichiers nécessaires en dernier** : Optimise le cache
- **Éviter ADD avec URLs** : Utiliser RUN curl/wget pour plus de contrôle

### 2.4 WORKDIR et ENV - Configuration de l'environnement d'exécution

#### WORKDIR - Gestion du répertoire de travail

**Principe fondamental** :
WORKDIR définit le répertoire de travail pour toutes les instructions suivantes (RUN, CMD, ENTRYPOINT, COPY, ADD). C'est l'équivalent de "cd" permanent dans votre conteneur.

**Comportement et optimisations** :

```dockerfile
# DÉFINITION DU RÉPERTOIRE DE TRAVAIL
# /app: Répertoire conventionnel pour les applications
# Comportement: Création automatique si inexistant
WORKDIR /app

# ÉQUIVALENT INEFFICACE:
# RUN mkdir -p /app && cd /app
# Problème: cd n'est pas persistant entre les instructions RUN

# UTILISATION AVEC CHEMINS RELATIFS
# Toutes les instructions suivantes utilisent /app comme base

# COPIE RELATIVE: . = /app dans le conteneur
COPY package.json .      # Résultat: /app/package.json

# EXÉCUTION RELATIVE: Commande exécutée dans /app
RUN npm install          # Exécuté dans /app, crée /app/node_modules

# CONFIGURATION FINALE: CMD/ENTRYPOINT utilise également /app
CMD ["node", "server.js"] # Exécute /app/server.js
```

**Patterns avancés avec WORKDIR** :

```dockerfile
# WORKDIR MULTIPLES POUR ORGANISATION
WORKDIR /app
# ... configuration application ...

WORKDIR /app/frontend
COPY frontend/ .
RUN npm install && npm run build

WORKDIR /app/backend
COPY backend/ .
RUN pip install -r requirements.txt

# RETOUR AU RÉPERTOIRE PRINCIPAL
WORKDIR /app
CMD ["python", "backend/app.py"]
```

#### ENV - Variables d'environnement et configuration

**Principe d'utilisation** :
ENG définit des variables d'environnement persistantes pour le conteneur. Ces variables sont disponibles pendant le build ET pendant l'exécution du conteneur.

**Définition et utilisation des variables** :

```dockerfile
# DÉFINITION DE VARIABLES D'APPLICATION
# NODE_ENV: Configuration de l'environnement Node.js
# Impact: Comportement des frameworks (logs, optimisations)
ENV NODE_ENV=production

# PORT: Port d'écoute de l'application
# Usage: Configuration réseau standardisée
ENV PORT=3000

# MODIFICATION DU PATH SYSTÈME
# /app/bin: Ajout d'un répertoire au PATH
# $PATH: Référence à la variable PATH existante
ENV PATH="/app/bin:$PATH"

# VARIABLES DE CONFIGURATION APPLICATIVE
ENV DATABASE_URL="postgresql://localhost:5432/myapp"
ENV LOG_LEVEL="info"
ENV MAX_CONNECTIONS="100"
```

**Utilisation des variables dans les instructions** :

```dockerfile
# UTILISATION DANS RUN
# $NODE_ENV: Substitution de variable pendant le build
RUN echo "Environment: $NODE_ENV"

# UTILISATION DANS EXPOSE
# $PORT: Port dynamique basé sur la variable
EXPOSE $PORT

# UTILISATION DANS CMD/ENTRYPOINT
# Variables disponibles à l'exécution
CMD ["node", "server.js"]
# Le processus Node.js aura accès à process.env.NODE_ENV
```

**Patterns de configuration avancés** :

```dockerfile
# CONFIGURATION PAR ENVIRONNEMENT
# Variables avec valeurs par défaut raisonnables
ENV NODE_ENV=production
ENV PORT=3000
ENV WORKERS=1
ENV MEMORY_LIMIT=512m

# CONFIGURATION DE SÉCURITÉ
# Variables pour certificats et authentification
ENV SSL_CERT_PATH="/etc/ssl/certs/app.crt"
ENV SSL_KEY_PATH="/etc/ssl/private/app.key"
ENV JWT_SECRET=""

# VARIABLES DE DEBUGGING ET MONITORING
ENV DEBUG="*"
ENV LOG_FORMAT="json"
ENV METRICS_ENABLED="true"

# UTILISATION CONDITIONELLE
RUN if [ "$NODE_ENV" = "development" ]; then \
        npm install --include=dev; \
    else \
        npm install --only=production; \
    fi
```

**Bonnes pratiques pour ENV** :

- **Valeurs par défaut sensibles** : Permettre l'exécution sans configuration
- **Pas de secrets** : Utiliser des volumes ou secrets Docker
- **Documentation** : Commenter l'usage de chaque variable
- **Standardisation** : Suivre les conventions (PORT, NODE_ENV, etc.)

---

## 3. Instructions avancées

### 3.1 ENTRYPOINT vs CMD - Gestion des commandes d'exécution

#### Contexte technique et cas d'usage

**Problématique** :
La gestion des commandes d'exécution dans Docker nécessite une compréhension précise des différences entre CMD et ENTRYPOINT. Ces instructions déterminent comment votre conteneur se comporte au démarrage et comment il réagit aux arguments fournis par l'utilisateur.

#### Différences fondamentales expliquées

**CMD - Commande par défaut modifiable** :

```dockerfile
# INSTRUCTION CMD: Définit la commande par défaut du conteneur
# Comportement: Peut être complètement remplacée par l'utilisateur
# Cas d'usage: Applications avec comportement par défaut flexible

CMD ["node", "app.js"]

# EXÉCUTION ET COMPORTEMENT:
# docker run myapp
# → Exécute: node app.js (commande par défaut)

# docker run myapp python script.py
# → Exécute: python script.py (CMD complètement remplacée)
# → La commande "node app.js" est ignorée
```

**ENTRYPOINT - Point d'entrée fixe** :

```dockerfile
# INSTRUCTION ENTRYPOINT: Définit le point d'entrée immuable
# Comportement: Ne peut pas être remplacé, les arguments sont ajoutés
# Cas d'usage: Applications avec comportement strict et prévisible

ENTRYPOINT ["node"]
CMD ["app.js"]

# EXÉCUTION ET COMPORTEMENT:
# docker run myapp
# → Exécute: node app.js (ENTRYPOINT + CMD)

# docker run myapp script.js
# → Exécute: node script.js (ENTRYPOINT + argument utilisateur)
# → L'argument "script.js" remplace CMD mais pas ENTRYPOINT
```

**Tableau comparatif des comportements** :

| Aspect         | CMD                  | ENTRYPOINT + CMD              |
| -------------- | -------------------- | ----------------------------- |
| Flexibilité    | Totale (remplaçable) | Contrôlée (arguments ajoutés) |
| Sécurité       | Moyenne              | Élevée (comportement garanti) |
| Cas d'usage    | Scripts polyvalents  | Applications spécialisées     |
| Prédictibilité | Variable             | Constante                     |

#### Patterns d'usage professionnels

**Pattern 1: Script wrapper - Initialisation complexe** :

```dockerfile
# CONTEXTE: Applications nécessitant une initialisation complexe
# Exemple: Configuration dynamique, migration de base de données, vérifications

# COPIE DU SCRIPT D'INITIALISATION
# entrypoint.sh: Script bash pour la logique de démarrage
COPY entrypoint.sh /usr/local/bin/

# CONFIGURATION DES PERMISSIONS
RUN chmod +x /usr/local/bin/entrypoint.sh

# POINT D'ENTRÉE FIXE
# Le script entrypoint.sh sera TOUJOURS exécuté en premier
ENTRYPOINT ["entrypoint.sh"]

# COMMANDE PAR DÉFAUT
# "app" sera passé comme argument au script entrypoint.sh
CMD ["app"]

# EXEMPLE DE SCRIPT entrypoint.sh:
# #!/bin/bash
# echo "Initialisation de l'application..."
# # Vérification de la base de données
# if ! pg_isready -h $DB_HOST; then
#   echo "Erreur: Base de données non accessible"
#   exit 1
# fi
# # Exécution de la commande passée en argument
# exec "$@"
```

**Pattern 2: Application avec arguments - Outil CLI** :

```dockerfile
# CONTEXTE: Outils en ligne de commande avec options variées
# Exemple: Utilitaires DevOps, CLIs d'administration

# POINT D'ENTRÉE: Exécutable principal
# ./myapp sera TOUJOURS l'exécutable de base
ENTRYPOINT ["./myapp"]

# COMMANDE PAR DÉFAUT: Aide utilisateur
# --help sera exécuté si aucun argument fourni
CMD ["--help"]

# EXEMPLES D'UTILISATION:
# docker run mycli
# → Exécute: ./myapp --help (affiche l'aide)

# docker run mycli --version
# → Exécute: ./myapp --version (affiche la version)

# docker run mycli deploy --env prod
# → Exécute: ./myapp deploy --env prod (commande de déploiement)
```

**Pattern 3: Combinaison flexible** :

```dockerfile
# CONTEXTE: Applications avec modes d'exécution multiples
# Exemple: Serveurs web avec modes development/production

# SCRIPT DE GESTION DES MODES
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh

# CONFIGURATION FLEXIBLE
ENTRYPOINT ["start.sh"]
CMD ["server", "--mode=production"]

# EXEMPLES D'UTILISATION:
# docker run myapp
# → Exécute: start.sh server --mode=production

# docker run myapp worker
# → Exécute: start.sh worker

# docker run myapp migrate
# → Exécute: start.sh migrate
```

### 3.2 USER et sécurité - Principe du moindre privilège

#### Contexte de sécurité critique

**Problématique de sécurité** :
Par défaut, les conteneurs Docker s'exécutent avec l'utilisateur root (UID 0), ce qui représente un risque de sécurité majeur. En cas de compromission du conteneur, l'attaquant obtient des privilèges root, permettant l'échappement vers l'hôte ou l'accès à d'autres conteneurs.

**Principe de sécurité** : Toujours exécuter les applications avec des privilèges minimaux.

#### Création d'utilisateur non-root sécurisé

**Méthode 1: Création complète avec groupe** :

```dockerfile
# CRÉATION DU GROUPE D'APPLICATION
# addgroup: Commande Alpine/Debian pour créer un groupe
# -g 1001: GID (Group ID) spécifique pour la cohérence
# -S: Groupe système (pas d'accès shell par défaut)
# appgroup: Nom du groupe pour l'application
RUN addgroup -g 1001 -S appgroup && \
    # CRÉATION DE L'UTILISATEUR D'APPLICATION
    # adduser: Commande pour créer un utilisateur
    # -u 1001: UID (User ID) correspondant au GID
    # -S: Utilisateur système (pas de répertoire home interactif)
    # -G appgroup: Ajout au groupe créé précédemment
    adduser -u 1001 -S appuser -G appgroup

# BASCULEMENT VERS L'UTILISATEUR NON-ROOT
# USER: Instruction pour définir l'utilisateur d'exécution
# Toutes les instructions suivantes s'exécuteront avec cet utilisateur
USER appuser

# ALTERNATIVE AVEC IDENTIFIANTS NUMÉRIQUES
# Plus sécurisé car indépendant des noms d'utilisateurs
# Format: UID:GID
USER 1001:1001
```

**Méthode 2: Exemple complet avec bonnes pratiques** :

```dockerfile
# IMAGE DE BASE ALPINE (légère et sécurisée)
FROM alpine:3.14

# CRÉATION D'UN UTILISATEUR SIMPLE
# adduser: Commande Alpine optimisée
# -D: Pas de mot de passe requis
# -s /bin/sh: Shell par défaut (minimal)
RUN adduser -D -s /bin/sh appuser

# CONFIGURATION DU RÉPERTOIRE DE TRAVAIL
# Important: Créer le répertoire AVANT de changer d'utilisateur
WORKDIR /app

# COPIE AVEC CHANGEMENT DE PROPRIÉTAIRE
# --chown: Assigne la propriété directement lors de la copie
# Format: utilisateur:groupe
# Avantage: Évite une instruction RUN supplémentaire
COPY --chown=appuser:appuser . .

# BASCULEMENT DÉFINITIF VERS L'UTILISATEUR SÉCURISÉ
# À partir d'ici, tout s'exécute avec les privilèges appuser
USER appuser

# COMMANDE D'EXÉCUTION
# L'application s'exécute SANS privilèges root
CMD ["./app"]
```

**Avantages de sécurité** :

- **Isolation renforcee** : Limitation des dommages en cas de compromission
- **Conformité** : Respect des standards de sécurité industriels
- **Audit** : Traçabilité des actions par utilisateur
- **Production-ready** : Pratique obligatoire en environnement professionnel

### 3.3 VOLUME et EXPOSE - Gestion des données et réseau

#### VOLUME - Persistance et partage de données

**Contexte technique** :
Les conteneurs Docker sont éphémères par nature. L'instruction VOLUME permet de déclarer des points de montage pour la persistance des données au-delà du cycle de vie du conteneur.

**Déclaration de volumes dans Dockerfile** :

```dockerfile
# VOLUMES MULTIPLES
# Syntaxe tableau JSON pour plusieurs volumes
# Chaque chemin sera un point de montage indépendant
VOLUME ["/data", "/logs"]

# AVANTAGES:
# - /data: Répertoire pour les données applicatives persistantes
# - /logs: Répertoire pour les logs d'application
# - Isolation: Chaque volume peut avoir une stratégie de sauvegarde différente

# VOLUME UNIQUE
# Syntaxe simple pour un seul point de montage
# Cas d'usage: Base de données, stockage centralisé
VOLUME /var/lib/mysql

# EXEMPLE CONCRET: Application web avec logs
VOLUME ["/app/uploads", "/var/log/nginx"]
```

**Note importante sur l'utilisation** :

```dockerfile
# ATTENTION: VOLUME dans Dockerfile crée des volumes ANONYMES
# Problème: Difficulté de gestion et de nettoyage
# Solution recommandée: Utiliser -v ou --mount avec docker run

# Exemple d'utilisation recommandée:
# docker run -v /host/data:/app/data myapp
# docker run --mount type=bind,source=/host/data,target=/app/data myapp
```

#### EXPOSE - Documentation des ports réseau

**Contexte réseau** :
L'instruction EXPOSE documente les ports que votre application utilise. C'est une information cruciale pour les administrateurs et les outils d'orchestration, mais elle ne publie PAS automatiquement les ports.

**Déclaration des ports d'application** :

```dockerfile
# PORT SIMPLE - Application web standard
# Port 80: Standard HTTP
# Utilisation: Serveurs web, APIs REST
EXPOSE 80

# PORTS MULTIPLES - Application complexe
# Port 80: Interface web
# Port 443: Interface web sécurisée (HTTPS)
# Cas d'usage: Serveurs web complets avec SSL
EXPOSE 80 443

# PORTS AVEC PROTOCOLE SPÉCIFIQUE
# Port 53/UDP: Serveur DNS
# UDP: Protocol User Datagram Protocol (sans connexion)
EXPOSE 53/udp

# Port 8080/TCP: Interface d'administration
# TCP: Transmission Control Protocol (avec connexion)
EXPOSE 8080/tcp

# EXEMPLE COMPLET: Serveur d'application
EXPOSE 3000      # API principale
EXPOSE 3001      # Interface d'administration
EXPOSE 9090      # Métriques Prometheus
```

**Utilisation pratique et publication des ports** :

```bash
# IMPORTANT: EXPOSE ne publie PAS les ports automatiquement
# C'est une instruction DOCUMENTAIRE uniquement

# PUBLICATION RÉELLE DES PORTS:
# -p: Map port hôte:port conteneur
docker run -p 8080:80 myapp

# -P: Publie TOUS les ports EXPOSE avec des ports aléatoires
docker run -P myapp

# VÉRIFICATION DES PORTS:
# Inspecter les ports déclarés dans l'image
docker inspect myapp | grep ExposedPorts

# Vérifier les ports publiés d'un conteneur en cours
docker port mycontainer
```

**Bonnes pratiques de documentation** :

- **Toujours documenter** les ports utilisés par l'application
- **Spécifier le protocole** si différent de TCP
- **Commenter** l'usage de chaque port dans le Dockerfile
- **Coordonner** avec l'équipe d'infrastructure pour éviter les conflits

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

**Contexte professionnel** :
Dans un environnement de production, les images Docker doivent être à la fois fonctionnelles et optimisées. Le défi principal est de pouvoir construire une application avec tous les outils nécessaires (compilateurs, gestionnaires de paquets, outils de build) tout en produisant une image finale légère pour le déploiement.

**Build monolithique** - Approche traditionnelle problématique :

```dockerfile
# IMAGE DE BASE COMPLÈTE (problématique)
# node:16 contient tous les outils de développement (npm, yarn, build tools)
# Taille de base: environ 900MB
FROM node:16

# RÉPERTOIRE DE TRAVAIL
WORKDIR /app

# COPIE DES DÉPENDANCES
# package*.json contient les dépendances de production ET de développement
COPY package*.json ./

# INSTALLATION COMPLÈTE
# npm install télécharge TOUTES les dépendances (prod + dev + outils de build)
# Exemple: webpack, babel, typescript, jest, etc.
RUN npm install        # [PROBLÈME] Inclut devDependencies inutiles en production

# COPIE DU CODE SOURCE
COPY . .

# COMPILATION/BUILD
# npm run build utilise les outils de développement pour créer l'application
# Génère les fichiers de production dans /dist ou /build
RUN npm run build      # [PROBLÈME] Outils de build restent dans l'image finale

# CONFIGURATION RÉSEAU
EXPOSE 3000

# COMMANDE DE DÉMARRAGE
# L'application démarre mais l'image contient des centaines de MB inutiles
CMD ["npm", "start"]

# RÉSULTAT PROBLÉMATIQUE:
# - Taille finale: ~1GB (900MB base + dépendances + outils de build)
# - Vulnérabilités: Outils de développement exposés en production
# - Performances: Téléchargement et déploiement lents
# - Sécurité: Surface d'attaque importante
```

#### Solution multi-stage

**Principe fondamental** :
Le multi-stage build permet de séparer les phases de construction et de production. Les outils de build restent dans les stages intermédiaires et seuls les artefacts nécessaires sont copiés dans l'image finale.

**Dockerfile multi-stage optimisé** :

```dockerfile
# ===============================================
# STAGE 1: CONSTRUCTION (Builder Stage)
# ===============================================
# Cette étape contient tous les outils nécessaires au build
# Elle sera supprimée dans l'image finale
FROM node:16 AS builder

# CONFIGURATION DU RÉPERTOIRE DE TRAVAIL
WORKDIR /app

# COPIE DES FICHIERS DE DÉPENDANCES
# Optimisation: copier d'abord les fichiers de dépendances pour le cache
COPY package*.json ./

# INSTALLATION OPTIMISÉE DES DÉPENDANCES
# npm ci: Installation propre basée sur package-lock.json
# --only=production: Exclut les devDependencies (mais on en a besoin pour le build...)
# Note: En réalité, on a besoin des devDependencies pour construire
RUN npm ci --frozen-lockfile  # Installation complète pour le build

# COPIE DU CODE SOURCE
# Le code source est copié après les dépendances pour optimiser le cache
COPY . .

# PHASE DE CONSTRUCTION
# npm run build génère les fichiers de production (généralement dans /dist)
# Utilise webpack, babel, typescript, etc. (présents dans node_modules)
RUN npm run build

# À la fin de ce stage: nous avons /app/dist avec l'application compilée

# ===============================================
# STAGE 2: PRODUCTION (Runtime Stage)
# ===============================================
# Cette étape crée l'image finale optimisée
# Utilise une image de base plus légère
FROM node:16-alpine AS production

# CONFIGURATION DU RÉPERTOIRE DE TRAVAIL
WORKDIR /app

# COPIE SÉLECTIVE DEPUIS LE STAGE BUILDER
# --from=builder: Copie depuis le stage précédent
# Nous copions SEULEMENT les fichiers nécessaires à l'exécution
COPY --from=builder /app/dist ./dist              # Application compilée
COPY --from=builder /app/node_modules ./node_modules  # Dépendances runtime
COPY package.json .                                # Métadonnées de l'application

# CONFIGURATION RÉSEAU
EXPOSE 3000

# COMMANDE DE DÉMARRAGE OPTIMISÉE
# Exécute directement le fichier compilé (plus rapide que npm start)
CMD ["node", "dist/server.js"]

# RÉSULTAT OPTIMISÉ:
# - Taille finale: ~150MB (base alpine + runtime + application)
# - Sécurité: Aucun outil de développement
# - Performance: Image légère, démarrage rapide
# - Maintenance: Séparation claire build/runtime
```

**Avantages de cette approche** :

- **Réduction de taille** : 85% de réduction (1GB → 150MB)
- **Sécurité renforcée** : Aucun outil de développement en production
- **Performance** : Déploiement et démarrage plus rapides
- **Maintenabilité** : Séparation claire des responsabilités

### 4.2 Patterns avancés

#### Build avec compilation - Pattern 3 stages

**Contexte d'utilisation** :
Ce pattern est adapté aux applications complexes nécessitant une séparation claire entre la gestion des dépendances, la compilation et l'exécution. Particulièrement utile pour les applications Next.js, React, ou autres frameworks modernes.

**Architecture 3-stages expliquée** :

```dockerfile
# ===============================================
# STAGE 1: GESTION DES DÉPENDANCES
# ===============================================
# Objectif: Installer et optimiser les dépendances
# Avantage: Cache stable si package.json ne change pas
FROM node:16 AS deps
WORKDIR /app

# COPIE DES FICHIERS DE DÉPENDANCES UNIQUEMENT
# Cette stratégie optimise le cache Docker
COPY package*.json ./

# INSTALLATION DÉTERMINISTE
# --frozen-lockfile: Utilise exactement les versions dans package-lock.json
# Garantit la reproductibilité des builds
RUN npm ci --frozen-lockfile

# Résultat: /app/node_modules avec toutes les dépendances

# ===============================================
# STAGE 2: COMPILATION ET BUILD
# ===============================================
# Objectif: Compiler l'application avec les outils de build
# Utilise les dépendances du stage précédent
FROM node:16 AS builder
WORKDIR /app

# RÉCUPÉRATION DES DÉPENDANCES
# --from=deps: Copie depuis le stage "deps"
# Évite la re-installation des dépendances
COPY --from=deps /app/node_modules ./node_modules

# COPIE DU CODE SOURCE
# Fait après les dépendances pour optimiser le cache
COPY . .

# PHASE DE COMPILATION
# npm run build exécute le processus de build défini dans package.json
# Utilise webpack, babel, typescript, etc. (présents dans node_modules)
RUN npm run build

# Résultat: Application compilée (généralement dans /app/.next ou /app/dist)

# ===============================================
# STAGE 3: ENVIRONNEMENT DE PRODUCTION
# ===============================================
# Objectif: Créer l'image finale optimisée pour la production
# Utilise une base légère et des bonnes pratiques de sécurité
FROM node:16-alpine AS runner
WORKDIR /app

# CRÉATION D'UTILISATEUR NON-ROOT (Sécurité)
# addgroup: Crée un groupe système avec GID 1001
# -S: Groupe système (pas utilisateur interactif)
RUN addgroup -g 1001 -S nodejs

# adduser: Crée un utilisateur système
# -S: Utilisateur système
# -u 1001: UID spécifique
RUN adduser -S nextjs -u 1001

# COPIE DES ARTEFACTS DE PRODUCTION
# --chown: Assigne la propriété au bon utilisateur
# Copie SEULEMENT les fichiers nécessaires à l'exécution
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# SÉCURITÉ: Basculer vers l'utilisateur non-root
USER nextjs

# CONFIGURATION RÉSEAU
EXPOSE 3000

# COMMANDE DE DÉMARRAGE
CMD ["npm", "start"]
```

**Avantages de ce pattern** :

- **Cache optimisé** : Chaque stage peut être mis en cache indépendamment
- **Sécurité** : Utilisateur non-root, surface d'attaque minimale
- **Performance** : Image finale très légère
- **Maintenabilité** : Responsabilités clairement séparées

#### Stage avec outils spécialisés - Pipeline CI/CD intégré

**Contexte professionnel** :
Dans un environnement DevOps moderne, il est essentiel d'intégrer les tests et la sécurité directement dans le processus de build. Ce pattern permet de créer un pipeline complet : build → test → sécurité → production.

**Pipeline multi-stage avec validation** :

```dockerfile
# ===============================================
# STAGE: TESTS ET QUALITÉ CODE
# ===============================================
# Objectif: Exécuter tous les tests avant la production
# Échec des tests = arrêt du build
FROM base AS testing

# RÉCUPÉRATION DES DÉPENDANCES DE DÉVELOPPEMENT
# Les dépendances incluent les frameworks de test (Jest, Mocha, etc.)
COPY --from=deps /app/node_modules ./node_modules

# COPIE DU CODE SOURCE COMPLET
# Inclut les fichiers de test (__tests__, *.spec.js, etc.)
COPY . .

# EXÉCUTION DES TESTS UNITAIRES
# npm run test exécute la suite de tests définie dans package.json
# En cas d'échec, le build s'arrête ici
RUN npm run test

# ANALYSE DE LA QUALITÉ DU CODE
# npm run lint exécute ESLint, Prettier, ou autres outils de linting
# Vérifie la conformité aux standards de code
RUN npm run lint

# Résultat: Validation que le code respecte les standards qualité

# ===============================================
# STAGE: ANALYSE DE SÉCURITÉ
# ===============================================
# Objectif: Scanner les vulnérabilités avant la production
# Utilise Trivy (outil de scan de sécurité open-source)
FROM aquasec/trivy:latest AS security

# COPIE DE L'APPLICATION À SCANNER
# --from=builder: Récupère l'application compilée
COPY --from=builder /app /scan

# SCAN DE SÉCURITÉ COMPLET
# trivy fs: Scan du système de fichiers
# --exit-code 1: Arrêter le build si vulnérabilités critiques détectées
# /scan: Répertoire à scanner
RUN trivy fs --exit-code 1 /scan

# Résultat: Certification que l'application est sécurisée

# ===============================================
# STAGE: PRODUCTION FINALE
# ===============================================
# Objectif: Image finale seulement si tous les tests passent
# Cette étape ne s'exécute QUE si tests et sécurité sont OK
FROM base AS production

# COPIE DES ARTEFACTS VALIDÉS
# --from=builder: Application testée et validée
COPY --from=builder /app/dist ./

# CONFIGURATION DE PRODUCTION
EXPOSE 3000
CMD ["node", "server.js"]

# Note importante: Cette image ne sera créée que si:
# 1. Les tests unitaires passent (stage testing)
# 2. Le linting est conforme (stage testing)
# 3. Aucune vulnérabilité critique (stage security)
```

**Avantages de cette approche** :

- **Qualité garantie** : Aucune image produite sans validation
- **Sécurité intégrée** : Scan automatique des vulnérabilités
- **Échec rapide** : Arrêt précoce en cas de problème
- **Traçabilité** : Chaque stage documente une validation spécifique

### 4.3 Optimisation de taille - Comparaison des stratégies

#### Analyse comparative des tailles d'images

**Contexte d'évaluation** :
L'optimisation de la taille des images Docker est cruciale pour les performances de déploiement, les coûts de stockage et la sécurité. Voici une comparaison détaillée des différentes approches.

**Comparaison technique des approches** :

```dockerfile
# ===============================================
# APPROCHE 1: IMAGE COMPLÈTE DE DÉVELOPPEMENT
# ===============================================
# Inconvenients: Taille maximale, vulnérabilités, lenteur
FROM node:16
# Contenu:
# - Système de base Debian complet
# - Node.js + npm + yarn
# - Outils de développement (gcc, make, python)
# - Dépendances de développement
# - Outils de build (webpack, babel, typescript)
# Taille finale: ~950MB
# Vulnérabilités: Élevées (nombreux paquets)
# Temps de déploiement: Lent (téléchargement volumineux)

# ===============================================
# APPROCHE 2: MULTI-STAGE OPTIMISÉ
# ===============================================
# Avantages: Taille réduite, sécurité améliorée
FROM node:16-alpine AS production
# Contenu:
# - Alpine Linux (base minimale)
# - Node.js runtime uniquement
# - Dépendances de production uniquement
# - Application compilée
# Taille finale: ~85MB
# Vulnérabilités: Réduites (moins de paquets)
# Temps de déploiement: Rapide

# ===============================================
# APPROCHE 3: DISTROLESS (PRODUCTION ULTIME)
# ===============================================
# Avantages: Sécurité maximale, taille minimale
FROM gcr.io/distroless/nodejs18-debian11
# Contenu:
# - Système minimal (pas de shell, pas d'utilitaires)
# - Runtime Node.js uniquement
# - Application et dépendances strictement nécessaires
# Taille finale: ~65MB
# Vulnérabilités: Minimales (surface d'attaque réduite)
# Sécurité: Maximale (pas d'accès shell)
```

**Métriques de performance** :

| Approche      | Taille | Vulnérabilités | Déploiement | Sécurité | Debugging |
| ------------- | ------ | -------------- | ----------- | -------- | --------- |
| Développement | 950MB  | Élevées        | Lent        | Faible   | Facile    |
| Multi-stage   | 85MB   | Moyennes       | Rapide      | Bonne    | Moyen     |
| Distroless    | 65MB   | Minimales      | Très rapide | Maximale | Difficile |

#### Techniques d'optimisation avancées

**Contexte technique** :
L'optimisation des images Docker nécessite une compréhension approfondie des couches et de la gestion des artefacts temporaires. Voici les techniques professionnelles pour minimiser la taille tout en préservant les fonctionnalités.

**1. Nettoyage dans la même couche** - Pattern critique :

```dockerfile
# TECHNIQUE: Tout dans une seule instruction RUN
# Principe: Éviter l'accumulation d'artefacts temporaires dans des couches séparées
# Chaque RUN crée une couche permanente dans l'image finale

RUN apt-get update && \
    # INSTALLATION DES OUTILS DE BUILD TEMPORAIRES
    # Ces outils sont nécessaires pour la compilation mais pas pour l'exécution
    apt-get install -y build-essential && \
    \
    # INSTALLATION DES DÉPENDANCES NODEJS
    # npm install télécharge et compile les dépendances natives
    npm install && \
    \
    # COMPILATION DE L'APPLICATION
    # npm run build génère les fichiers de production
    npm run build && \
    \
    # NETTOYAGE CRITIQUE: Suppression des outils temporaires
    # apt-get purge: Supprime les paquets et leurs fichiers de configuration
    apt-get purge -y build-essential && \
    \
    # NETTOYAGE SYSTÈME APPROFONDI
    # autoremove: Supprime les dépendances orphelines
    apt-get autoremove -y && \
    \
    # SUPPRESSION DU CACHE APT
    # /var/lib/apt/lists/*: Cache des listes de paquets (peut être volumineux)
    rm -rf /var/lib/apt/lists/* && \
    \
    # NETTOYAGE DU CACHE NPM
    # npm cache: Supprime le cache npm (économise des MB)
    npm cache clean --force

# RÉSULTAT: Une seule couche contenant uniquement les artefacts nécessaires
# GAIN: Peut économiser plusieurs centaines de MB
```

**2. Exclusion de fichiers** - Configuration .dockerignore optimisée :

```dockerignore
# ===============================================
# FICHIERS DE DÉVELOPPEMENT
# ===============================================
# Ces fichiers ne doivent jamais être dans l'image de production

# Dépendances locales (seront installées via npm install)
node_modules

# Logs de développement
npm-debug.log
yarn-error.log
yarn-debug.log

# ===============================================
# FICHIERS DE CONFIGURATION DOCKER
# ===============================================
# Éviter la récursion et les conflits

Dockerfile*          # Tous les Dockerfiles
.dockerignore        # Ce fichier lui-même
docker-compose*.yml  # Fichiers de composition

# ===============================================
# SYSTÈME DE CONTRÔLE DE VERSION
# ===============================================
# Historique git inutile en production

.git                 # Dossier git complet
.gitignore          # Règles git
.gitmodules         # Sous-modules git

# ===============================================
# FICHIERS DE DOCUMENTATION
# ===============================================
# Documentation non nécessaire à l'exécution

README.md           # Documentation projet
CHANGELOG.md        # Historique des changes
LICENSE            # Fichier de licence
*.md               # Tous les fichiers markdown

# ===============================================
# ENVIRONNEMENT ET SECRETS
# ===============================================
# Fichiers sensibles ou spécifiques à l'environnement

.env               # Variables d'environnement locales
.env.local         # Configuration locale
.env.*.local       # Configurations d'environnement

# ===============================================
# ARTEFACTS DE TEST ET COUVERTURE
# ===============================================
# Résultats de tests non nécessaires en production

.nyc_output        # Couverture de code NYC
coverage           # Rapports de couverture
.pytest_cache      # Cache pytest (Python)
__pycache__        # Cache Python
*.pyc              # Fichiers Python compilés

# ===============================================
# OUTILS DE DÉVELOPPEMENT
# ===============================================
# Configuration des outils de développement

.vscode            # Configuration VS Code
.idea              # Configuration IntelliJ
.DS_Store          # Fichiers système MacOS
Thumbs.db          # Fichiers système Windows
```

**Impact de ces optimisations** :

- **Réduction de taille** : 40-60% d'économie sur l'image finale
- **Sécurité** : Moins de fichiers = surface d'attaque réduite
- **Performance** : Transfert réseau plus rapide
- **Coûts** : Réduction des coûts de stockage et bande passante

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
