# Séance 2 : Création d'Images avec Dockerfile

**Sprint 2 - Semaine 1 - Docker Basics**  
**Durée** : 80 minutes  
**Type** : Cours magistral avec travaux pratiques

## Vue d'ensemble

Cette séance approfondit la création d'images Docker personnalisées avec Dockerfile, couvrant la syntaxe complète, les optimisations de performance, et les bonnes pratiques de sécurité pour un environnement de production.

## Objectifs pédagogiques

- Maîtriser la syntaxe complète Dockerfile et ses instructions
- Optimiser la taille et sécurité des images Docker
- Implémenter des builds multi-stage pour la production
- Utiliser BuildKit et les fonctionnalités avancées

## Objectifs techniques

Dockerfile instructions, image optimization, multi-stage builds, BuildKit, security best practices, image scanning, layer caching

## Programme détaillé

### 1. Fondamentaux Dockerfile (20 minutes)

- Syntaxe et instructions essentielles
- Système de couches et optimisation
- Variables d'environnement et arguments

### 2. Instructions avancées (25 minutes)

- COPY vs ADD, ENTRYPOINT vs CMD
- USER, WORKDIR, VOLUME
- HEALTHCHECK et LABEL

### 3. Optimisation et sécurité (35 minutes)

- Multi-stage builds
- Réduction de la taille des images
- Bonnes pratiques de sécurité
- Image scanning et vulnérabilités

## Travaux pratiques

### LAB 1 : Dockerfile fondamental et optimisation (8 points - 20 minutes)

Créer une image Python optimisée avec application Flask et bonnes pratiques.

**Énoncé** : Développer une image Docker pour une API Python Flask avec optimisation de taille et sécurité de base.

**Objectifs** :

- Dockerfile multi-étapes pour API Flask
- Optimisation taille et sécurité
- Tests de fonctionnement et performance

### LAB 2 : Build multi-stage et sécurité (10 points - 25 minutes)

Implémenter un build multi-stage pour application Node.js avec sécurité renforcée.

**Énoncé** : Créer une image Node.js production-ready avec build multi-stage, utilisateur non-root, et scanning de sécurité.

**Objectifs** :

- Build multi-stage Node.js avec optimisation
- Configuration sécurité et utilisateur non-root
- Tests de vulnérabilités et performance

### LAB 3 : Image personnalisée avec BuildKit (12 points - 35 minutes)

Développer une image complexe avec BuildKit, cache optimization et CI/CD ready.

**Énoncé** : Construire une image DevOps complète avec outils intégrés, optimisation BuildKit et préparation CI/CD.

**Objectifs** :

- Image DevOps avec multiple outils
- BuildKit et optimisations avancées
- Intégration CI/CD et automation

## Évaluation

- **LAB 1** : 8 points (Dockerfile optimisé, application fonctionnelle)
- **LAB 2** : 10 points (Multi-stage, sécurité, tests)
- **LAB 3** : 12 points (BuildKit, optimisation, CI/CD)
- **Total** : 30 points

## Prérequis

- Séance 1 complétée (installation Docker, manipulation conteneurs)
- Connaissances de base Linux et ligne de commande
- Notions de développement (Python, Node.js)

## Ressources

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/multi-stage-builds/)

---

**Formateur** : Hassan ESSADIK  
**Sprint 2 - Semaine 1 - Séance 2**
