# Dossier de démonstration - Applications pour Docker# Formation DevOps - Application de démonstration

Ce dossier contient des applications de démonstration utilisées dans la formation DevOps pour illustrer les concepts de containerisation avec Docker.Cette application Node.js a été créée pour démontrer les concepts de containerisation avec Docker dans le cadre de la Formation DevOps de Simplon Maghreb.

## Applications disponibles## Description

### 1. Application Node.js (demo/)Application web simple qui expose plusieurs endpoints pour gérer les inscriptions à la formation DevOps.

- **Type**: Application web Express.js

- **Port**: 3000## Fonctionnalités

- **Fonctionnalités**: Inscription de participants, interface web responsive

- **Dockerfile**: Prêt pour la containerisation### Endpoints principaux

- **Usage**: Démonstration des concepts Docker de base

1. **GET /** - Page d'accueil avec informations complètes sur la formation

### 2. Jeu Python (python-demo-game/)

- **Type**: Application interactive en ligne de commande - Détails de la formation (durée, sprints, technologies)

- **Fonctionnalités**: Jeu de devinette avec système de scores - Formulaire d'inscription

- **Dockerfile**: Image Python optimisée avec utilisateur non-root - Statistiques des participants

- **Usage**: Pratique des commandes Docker avancées et persistance des données

2. **POST /inscription** - Endpoint pour s'inscrire à la formation

## Utilisation dans la formation

- Validation des données (nom et prénom requis)

Ces applications sont conçues pour accompagner les séances pratiques: - Vérification des doublons

- Redirection vers la liste des participants

- **Séance 1**: Découverte de Docker avec l'application Node.js

- **Séance 2**: Création d'images et Dockerfile avec les deux applications3. **GET /participants** - Liste de tous les participants inscrits

- **Séances suivantes**: Concepts avancés (volumes, réseaux, composition) - Affichage des participants avec détails

  - Indication des nouveaux inscrits

## Instructions de déploiement - Statistiques de la formation

Chaque application contient sa propre documentation dans son README.md respectif avec les commandes Docker nécessaires.### Endpoints API

---- **GET /api/participants** - Données JSON des participants

_Formation DevOps - Simplon Maghreb_- **GET /api/formation** - Informations de formation en JSON

_Auteur: Hassan ESSADIK_- **GET /health** - Health check de l'application

## Structure du projet

```
demo/
├── package.json          # Dépendances et scripts
├── app.js                # Application Express principale
├── README.md             # Documentation
└── Dockerfile            # Configuration Docker (à créer)
```

## Installation et démarrage

### Prérequis

- Node.js 16+
- npm

### Installation des dépendances

```bash
cd demo
npm install
```

### Démarrage de l'application

```bash
# Mode production
npm start

# Mode développement (avec nodemon)
npm run dev
```

L'application sera accessible sur http://localhost:3000

## Technologies utilisées

- **Node.js** - Runtime JavaScript
- **Express.js** - Framework web
- **Body-parser** - Parsing des données de formulaire
- **HTML/CSS** - Interface utilisateur responsive

## Données

L'application utilise une base de données en mémoire avec quelques participants pré-inscrits :

- Hassan ESSADIK (Formateur)
- Sophie MARTIN
- Ahmed BENALI

## Containerisation avec Docker

Cette application est conçue pour être containerisée avec Docker. Les caractéristiques importantes :

- **Port** : 3000 (configurable via variable d'environnement PORT)
- **Bind address** : 0.0.0.0 (nécessaire pour Docker)
- **Health check** : Endpoint /health disponible
- **Logs** : Messages de démarrage informatifs

## Formation DevOps - Contexte pédagogique

Cette application sert d'exemple pratique pour :

### Sprint 2 - Containerisation et CI/CD

- **Séance 2** : Création d'images avec Dockerfile
- **Séance 3** : Docker Compose et orchestration
- **Séance 4** : Production et optimisation

### Concepts abordés

- Création de Dockerfile optimisé
- Multi-stage builds
- Variables d'environnement
- Health checks
- Volumes et persistance
- Réseaux Docker
- Sécurité des conteneurs

## Auteur

**Hassan ESSADIK**  
Formateur DevOps - Simplon Maghreb  
Formation DevOps 2025

---

_Cette application fait partie du programme de formation DevOps de Simplon Maghreb et est utilisée à des fins pédagogiques pour enseigner les concepts de containerisation et de déploiement._
