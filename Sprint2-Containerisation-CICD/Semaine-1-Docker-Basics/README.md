# Semaine 1 - Docker Basics : Fondations de la Containerisation

## Menu de Navigation

### Séances de la Semaine

| Séance       | Titre                                                                  | Durée | Navigation                                                                                                                                                          |
| ------------ | ---------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Séance 1** | [Fondamentaux & Architecture](./Seance-1-Fondamentaux-Architecture/)   | 2h    | [Cours](./Seance-1-Fondamentaux-Architecture/cours/) \| [Labs](./Seance-1-Fondamentaux-Architecture/labs/) \| [Quiz](./Seance-1-Fondamentaux-Architecture/quiz/)    |
| **Séance 2** | [Création Images & Dockerfile](./Seance-2-Creation-Images-Dockerfile/) | 2h    | [Cours](./Seance-2-Creation-Images-Dockerfile/cours/) \| [Labs](./Seance-2-Creation-Images-Dockerfile/labs/) \| [Quiz](./Seance-2-Creation-Images-Dockerfile/quiz/) |
| **Séance 3** | [Images & Registries](./Seance-3-Images-Registries/)                   | 2h    | [Cours](./Seance-3-Images-Registries/cours/) \| [Labs](./Seance-3-Images-Registries/labs/) \| [Quiz](./Seance-3-Images-Registries/quiz/)                            |
| **Séance 4** | [Volumes & Networks](./Seance-4-Volumes-Networks/)                     | 2h    | [Cours](./Seance-4-Volumes-Networks/cours/) \| [Labs](./Seance-4-Volumes-Networks/labs/) \| [Quiz](./Seance-4-Volumes-Networks/quiz/)                               |
| **Séance 5** | [Docker Production](./Seance-5-Docker-Production/)                     | 2h    | [Cours](./Seance-5-Docker-Production/cours/) \| [Labs](./Seance-5-Docker-Production/labs/) \| [Quiz](./Seance-5-Docker-Production/quiz/)                            |

### Navigation Rapide

- **Progression** : [Séance 1](./Seance-1-Fondamentaux-Architecture/) → [Séance 2](./Seance-2-Creation-Images-Dockerfile/) → [Séance 3](./Seance-3-Images-Registries/) → [Séance 4](./Seance-4-Volumes-Networks/) → [Séance 5](./Seance-5-Docker-Production/)
- **Structure** : [Retour Sprint 2](../README.md) | [Semaine 2 - Docker Compose](../Semaine-2-Docker-Compose/) | [Semaine 3 - GitLab CI/CD](../Semaine-3-GitLab-CICD/)
- **Évaluation** : [Labs Pratiques](#labs-pratiques) | [Standards de Qualité](#standards-de-qualité)

---

## Objectifs de la Semaine

Maîtriser Docker et la containerisation pour créer des environnements reproductibles, portables et sécurisés selon les standards DevOps modernes.

### Compétences Acquises

À l'issue de cette semaine, vous maîtriserez :

- Concepts Fondamentaux : Containerisation, isolation, images vs conteneurs
- Docker Engine : Installation, configuration, architecture
- Images Docker : Création, optimisation, sécurisation
- Gestion Avancée : Volumes, réseaux, registries
- Production Ready : Bonnes pratiques, sécurité, monitoring
- Outils DevOps : Buildkit, Multi-stage builds, scanning sécurité

## Planning des Séances

### Séance 1 : Introduction Docker

**Objectif** : Comprendre la containerisation et maîtriser Docker Engine

- Concepts : VM vs Containers, architecture Docker
- Installation : Docker Desktop, Docker Engine Linux
- Premiers pas : Commandes essentielles, lifecycle des conteneurs

### Séance 2 : Dockerfile Creation

**Objectif** : Maîtriser la création d'images optimisées et sécurisées

- Dockerfile : Syntaxe, instructions, bonnes pratiques
- Multi-stage builds : Optimisation taille et sécurité
- BuildKit : Fonctionnalités avancées et cache

### Séance 3 : Images Registries

**Objectif** : Gérer la distribution et versioning des images

- Docker Hub : Publication et automated builds
- Registries privés : Harbor, authentification, sécurité
- Stratégies : Tagging, versioning, distribution multi-environnements

### Séance 4 : Volumes Networks

**Objectif** : Gérer la persistance des données et communication

- Volumes : Types, gestion, bonnes pratiques
- Réseaux : Bridge, overlay, communication inter-conteneurs
- Bind mounts vs volumes : Cas d'usage

### Séance 5 : Docker Production

**Objectif** : Préparer des déploiements production-ready

- Optimisation : Resource limits, health checks
- Sécurité : User non-root, secrets, least privilege
- Monitoring : Logs, métriques, debugging

## Technologies et Outils

### Outils Principaux

- Docker Engine : Runtime de containerisation
- Docker Desktop : Interface développement
- Docker BuildKit : Builder avancé
- Docker Compose : Introduction

### Outils DevOps Intégrés

- Dive : Analyse d'images Docker
- Trivy : Scanner de vulnérabilités
- Hadolint : Linter pour Dockerfile
- Portainer : Interface de gestion

## Évaluation

### Répartition des Points

- LABs Pratiques : 5 séances × 30 points = 150 points
- Quiz Validation : 5 Quiz × 15 points = 75 points
- Total : 225 points (seuil : 72% = 162 points)

## Standards de Qualité

### Pédagogie

- Progression Logique : Concepts fondamentaux vers avancés
- Pratique Intensive : 80% du temps en hands-on
- Projets Réels : Cas d'usage authentiques DevOps
- Évaluation Continue : Validation par étapes

### Contenu Technique

- Standards Industrie : Docker official best practices
- Sécurité First : Intégration dès le début
- DevOps Culture : Automation, monitoring, collaboration
- Outils Modernes : Technologies actuelles du marché

## Structure des Dossiers

```
Semaine-1-Docker-Basics/
├── README.md
├── Seance-1-Introduction-Docker/
├── Seance-2-Dockerfile-Creation/
├── Seance-3-Images-Registries/
├── Seance-4-Volumes-Networks/
└── Seance-5-Docker-Production/
```

## Prérequis

### Connaissances Techniques

- Linux : Ligne de commande, processus, système de fichiers
- Réseaux : TCP/IP, ports, protocoles HTTP/HTTPS
- Développement : Bases (HTML, scripts)
- Git : Versioning et collaboration

### Outils Requis

- Ordinateur : Linux, macOS, ou Windows avec WSL2
- Docker Desktop : Version récente installée
- Éditeur : VS Code recommandé avec extensions Docker
- Terminal : Bash/Zsh ou PowerShell

## Labs Pratiques

### Répartition par Séance

| Navigation Séquentielle                                                           | Objectif Technique                          | Technologies                         |
| --------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------ |
| [Séance 1 - Fondamentaux & Architecture](./Seance-1-Fondamentaux-Architecture/)   | Docker Engine, Installation, Commandes CLI  | Docker Desktop, Ubuntu, Alpine       |
| [Séance 2 - Création Images & Dockerfile](./Seance-2-Creation-Images-Dockerfile/) | Dockerfile, Multi-stage, BuildKit           | Dockerfile, BuildKit, Optimisation   |
| [Séance 3 - Images & Registries](./Seance-3-Images-Registries/)                   | Docker Hub, Registries privés, Distribution | Docker Hub, Harbor, Authentification |
| [Séance 4 - Volumes & Networks](./Seance-4-Volumes-Networks/)                     | Persistance données, Communication          | Volumes, Bridge, Overlay Networks    |
| [Séance 5 - Docker Production](./Seance-5-Docker-Production/)                     | Sécurité, Monitoring, Bonnes pratiques      | Health checks, Resource limits       |

## Navigation

### Accès Direct aux Séances

| Séance                                                                            | Contenu Détaillé                             | Durée |
| --------------------------------------------------------------------------------- | -------------------------------------------- | ----- |
| [Séance 1 - Fondamentaux & Architecture](./Seance-1-Fondamentaux-Architecture/)   | Containerisation, Docker Engine, CLI         | 2h    |
| [Séance 2 - Création Images & Dockerfile](./Seance-2-Creation-Images-Dockerfile/) | Dockerfile, Multi-stage builds, Optimisation | 2h    |
| [Séance 3 - Images & Registries](./Seance-3-Images-Registries/)                   | Docker Hub, Registries privés, Distribution  | 2h    |
| [Séance 4 - Volumes & Networks](./Seance-4-Volumes-Networks/)                     | Volumes, Bind mounts, Réseaux Docker         | 2h    |
| [Séance 5 - Docker Production](./Seance-5-Docker-Production/)                     | Sécurité, Monitoring, Production-ready       | 2h    |

### Navigation Générale

- **Retour** : [Sprint 2 - Containerisation CI/CD](../README.md)
- **Précédent** : [Sprint 1 - Fondations DevOps](../../Sprint1-Fondations-DevOps/)
- **Suivant** : [Semaine 2 - Docker Compose](../Semaine-2-Docker-Compose/)
- **Programme** : [Menu Principal](../../README.md)
- **Début** : [Menu de Navigation](#menu-de-navigation)

---

_Formation DevOps - Sprint 2 Semaine 1 | Framework HASSAN_
