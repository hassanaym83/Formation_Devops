# Formation DevOps - Application de démonstration

Cette application Node.js a été créée pour démontrer les concepts de containerisation avec Docker dans le cadre de la Formation DevOps de Simplon Maghreb.

## Description

Application web simple qui expose plusieurs endpoints pour gérer les inscriptions à la formation DevOps.

## Fonctionnalités

### Endpoints principaux

1. **GET /** - Page d'accueil avec informations complètes sur la formation

   - Détails de la formation (durée, sprints, technologies)
   - Formulaire d'inscription
   - Statistiques des participants

2. **POST /inscription** - Endpoint pour s'inscrire à la formation

   - Validation des données (nom et prénom requis)
   - Vérification des doublons
   - Redirection vers la liste des participants

3. **GET /participants** - Liste de tous les participants inscrits
   - Affichage des participants avec détails
   - Indication des nouveaux inscrits
   - Statistiques de la formation

### Endpoints API

- **GET /api/participants** - Données JSON des participants
- **GET /api/formation** - Informations de formation en JSON
- **GET /health** - Health check de l'application

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
