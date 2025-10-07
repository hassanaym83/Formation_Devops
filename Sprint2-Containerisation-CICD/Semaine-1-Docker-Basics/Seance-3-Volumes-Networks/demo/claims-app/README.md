# Application de Gestion des Réclamations

## Démonstration pratique des volumes Docker

### Objectif de cette application

Cette application Node.js a été spécialement conçue pour démontrer de manière pratique et visuelle le fonctionnement des volumes Docker. Elle illustre la différence fondamentale entre les données temporaires et les données persistantes dans un environnement conteneurisé.

### Concept de démonstration

L'application implémente un workflow en deux étapes qui permet d'observer concrètement le comportement des volumes Docker :

1. **Soumission** : Les réclamations sont initialement stockées dans `/tmp/claims` (système de fichiers temporaire du conteneur)
2. **Validation** : Après validation, les réclamations sont transférées vers `/persist/claims` (volume Docker persistent)

### Architecture technique

```
┌─────────────────────────────────────────┐
│            Interface Web                │
│          (port 3000)                   │
└─────────────────┬───────────────────────┘
                  │
                  v
┌─────────────────────────────────────────┐
│           API Node.js/Express           │
└─────────┬───────────────────────┬───────┘
          │                       │
          v                       v
┌─────────────────┐    ┌─────────────────┐
│  /tmp/claims    │    │ /persist/claims │
│   (temporaire)  │    │  (volume Docker)│
│                 │    │                 │
│ • Perdu au      │    │ • Préservé au   │
│   redémarrage   │    │   redémarrage   │
│ • Données       │    │ • Données       │
│   volatiles     │    │   persistantes  │
└─────────────────┘    └─────────────────┘
```

### Fonctionnalités implémentées

#### Gestion des réclamations

- **Soumission** : Formulaire web pour créer de nouvelles réclamations
- **Validation** : Transfert des réclamations temporaires vers le stockage permanent
- **Consultation** : Affichage en temps réel des réclamations temporaires et permanentes
- **Suppression** : Nettoyage des réclamations temporaires
- **Nettoyage automatique** : Suppression des fichiers temporaires anciens (> 24h)

#### API REST complète

```
GET  /                        - Interface web interactive
GET  /api/health              - Vérification santé application
POST /api/claims              - Soumettre nouvelle réclamation
GET  /api/claims/pending      - Lister réclamations temporaires
GET  /api/claims/validated    - Lister réclamations persistantes
POST /api/claims/:file/validate - Valider réclamation (temp → persist)
DELETE /api/claims/:file      - Supprimer réclamation temporaire
POST /api/claims/cleanup      - Nettoyage automatique anciennes réclamations
```

### Utilisation pour la formation

#### Construction de l'image Docker

```bash
# Construction de l'image
docker build -t claims-app .

# Vérification de l'image créée
docker images claims-app
```

#### Démarrage sans volume (données temporaires uniquement)

```bash
# Lancement du conteneur sans volume
docker run -d -p 3000:3000 --name claims-temp claims-app

# Accès à l'application
open http://localhost:3000

# Arrêt et suppression du conteneur
docker stop claims-temp && docker rm claims-temp
```

#### Démarrage avec volume Docker (démonstration de la persistance)

```bash
# Création d'un volume Docker nommé
docker volume create claims-data

# Lancement avec volume monté
docker run -d -p 3000:3000 \
  -v claims-data:/persist \
  --name claims-persistent \
  claims-app

# Test de persistance : soumission → validation → redémarrage
# 1. Soumettre des réclamations via l'interface web
# 2. Valider quelques réclamations (transfert vers /persist)
# 3. Redémarrer le conteneur
docker restart claims-persistent

# Observer : réclamations temporaires perdues, permanentes préservées
```

#### Inspection des volumes

```bash
# Lister les volumes Docker
docker volume ls

# Inspecter le contenu du volume
docker volume inspect claims-data

# Accéder au contenu du volume
docker run --rm -v claims-data:/data alpine ls -la /data/claims/validated
```

### Scénarios d'apprentissage

#### Scénario 1 : Perte de données sans volume

1. Démarrer l'application sans volume
2. Soumettre plusieurs réclamations
3. Observer les fichiers dans `/tmp/claims`
4. Redémarrer le conteneur
5. **Constater** : toutes les données sont perdues

#### Scénario 2 : Persistance avec volume

1. Démarrer l'application avec volume Docker
2. Soumettre et valider des réclamations
3. Redémarrer le conteneur
4. **Constater** : réclamations validées préservées, temporaires perdues

#### Scénario 3 : Comparaison bind mount vs volume

```bash
# Test avec bind mount
docker run -d -p 3001:3000 \
  -v $(pwd)/data:/persist \
  --name claims-bindmount \
  claims-app

# Test avec volume Docker
docker run -d -p 3002:3000 \
  -v claims-volume:/persist \
  --name claims-volume \
  claims-app
```

### Configuration et personnalisation

#### Variables d'environnement

```bash
# Port personnalisé
docker run -e PORT=8080 -p 8080:8080 claims-app

# Mode debug
docker run -e NODE_ENV=development claims-app

# Fuseau horaire
docker run -e TZ=America/New_York claims-app
```

#### Montage de répertoires spécifiques

```bash
# Séparation des répertoires temporaires et permanents
docker run -d \
  -v /host/temp:/tmp/claims \
  -v claims-data:/persist/claims \
  -p 3000:3000 \
  claims-app
```

### Intérêt pédagogique

Cette application permet aux apprenants de :

1. **Visualiser** concrètement la différence entre données temporaires et persistantes
2. **Expérimenter** les effets du redémarrage de conteneurs sur les données
3. **Comprendre** l'importance des volumes pour la persistance
4. **Manipuler** les commandes Docker volumes de manière pratique
5. **Observer** le comportement des applications stateful en environnement conteneurisé

### Technologies utilisées

- **Backend** : Node.js 18, Express.js
- **Frontend** : HTML5, CSS3, JavaScript vanilla (sans framework pour simplicité)
- **Containerisation** : Docker avec image Alpine optimisée
- **Stockage** : Système de fichiers + volumes Docker
- **Validation** : Express-validator pour la sécurité des données
- **Sécurité** : Helmet.js, utilisateur non-privilégié, CORS

### Structure du projet

```
claims-app/
├── Dockerfile              # Configuration conteneur optimisée
├── package.json            # Dépendances Node.js
├── server.js              # Serveur Express avec API complète
├── public/
│   └── index.html         # Interface web interactive
└── README.md              # Documentation (ce fichier)
```

### Utilisation en formation

Cette application s'intègre parfaitement dans le module **Séance 4 - Volumes & Networks** du programme Docker, permettant une approche pratique et interactive de l'apprentissage des volumes Docker.
