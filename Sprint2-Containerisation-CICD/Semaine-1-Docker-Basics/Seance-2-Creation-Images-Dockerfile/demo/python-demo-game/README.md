# Jeu de Devinette Python - Formation DevOps

## Description

Application Python interactive de devinette de nombres, développée pour démontrer la containerisation avec Docker dans le cadre de la formation DevOps.

## Fonctionnalités

- Génération aléatoire de nombres entre 1 et 99
- Système de score basé sur le nombre de tentatives
- Podium des 3 meilleurs scores avec persistance
- Interface en ligne de commande intuitive
- Gestion complète des erreurs utilisateur
- Statistiques globales des parties jouées

## Prérequis

- Python 3.11 ou supérieur
- Docker (pour la containerisation)

## Utilisation Locale

### Installation

```bash
# Cloner ou télécharger les fichiers
# Aucune dépendance externe requise
```

### Lancement

```bash
python number_game.py
```

## Utilisation avec Docker

### Construction de l'image

```bash
docker build -t python-number-game .
```

### Lancement du conteneur

```bash
# Mode interactif avec terminal
docker run -it python-number-game

# Avec persistance des scores (volume)
docker run -it -v $(pwd)/scores:/app python-number-game
```

### Commandes Docker avancées

```bash
# Lancement avec nom de conteneur
docker run -it --name game-session python-number-game

# Arrêt propre du conteneur
docker stop game-session

# Redémarrage
docker restart game-session

# Suppression du conteneur
docker rm game-session
```

## Architecture de l'Application

### Structure des fichiers

```
python-demo-game/
├── number_game.py    # Script principal du jeu
├── Dockerfile        # Configuration Docker
├── README.md         # Documentation
└── scores.json       # Fichier de scores (généré automatiquement)
```

### Classes et méthodes principales

- `NumberGuessingGame`: Classe principale du jeu
  - `play_round()`: Gestion d'une partie
  - `load_scores()`/`save_scores()`: Persistance des données
  - `display_podium()`: Affichage du classement
  - `run()`: Boucle principale

## Règles du Jeu

1. L'ordinateur génère un nombre secret entre 1 et 99
2. Le joueur doit deviner ce nombre
3. Le système indique si le nombre est plus grand ou plus petit
4. Le score correspond au nombre de tentatives
5. Moins de tentatives = meilleur score

## Système de Notation

- **1 tentative**: INCROYABLE ! Réussi du premier coup !
- **2-3 tentatives**: EXCELLENT ! Très peu de tentatives !
- **4-6 tentatives**: BIEN JOUÉ ! Bon score !
- **7-10 tentatives**: Pas mal ! Vous pouvez faire mieux !
- **11+ tentatives**: Il y a de la place pour l'amélioration !

## Podium et Statistiques

Le jeu maintient automatiquement:

- Classement des 3 meilleurs scores
- Nombre total de parties jouées
- Moyenne des tentatives
- Record absolu

## Contexte Pédagogique

Cette application fait partie du programme de formation DevOps et sert à:

- Comprendre la containerisation Python avec Docker
- Pratiquer les commandes Docker de base
- Illustrer la persistance des données dans les conteneurs
- Démontrer les bonnes pratiques de sécurité (utilisateur non-root)

## Commandes de Démonstration Docker

### Inspection et débogage

```bash
# Inspecter l'image construite
docker inspect python-number-game

# Vérifier les processus dans le conteneur
docker exec -it game-session ps aux

# Accéder au shell du conteneur
docker exec -it game-session /bin/bash

# Consulter les logs
docker logs game-session
```

### Gestion des volumes

```bash
# Créer un volume pour la persistance
docker volume create game-scores

# Lancer avec volume nommé
docker run -it -v game-scores:/app python-number-game

# Inspecter le volume
docker volume inspect game-scores
```

## Auteur

Hassan ESSADIK - Formation DevOps Simplon Maghreb

## Licence

Projet éducatif - Formation DevOps
