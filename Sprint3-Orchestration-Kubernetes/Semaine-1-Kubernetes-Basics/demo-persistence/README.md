# Application de Démonstration - Persistance Kubernetes

Cette application Node.js simple démontre la persistance des données avec les volumes Kubernetes.

## Fonctionnalités

- **POST /technologies** : Ajouter une nouvelle technologie
- **GET /technologies** : Récupérer toutes les technologies enregistrées
- **DELETE /technologies** : Supprimer toutes les technologies
- **GET /health** : Vérifier l'état de l'application

## Structure des données

Les technologies sont stockées dans le fichier `data/technologies.txt`, une technologie par ligne.

## Installation et démarrage

```bash
# Installer les dépendances
npm install

# Démarrer l'application
npm start

# Démarrage en mode développement (avec nodemon)
npm run dev
```

## Exemples d'utilisation

### Ajouter une technologie

```bash
curl -X POST http://localhost:3000/technologies \
  -H "Content-Type: application/json" \
  -d '{"technology": "Kubernetes"}'
```

### Récupérer toutes les technologies

```bash
curl -X GET http://localhost:3000/technologies
```

### Supprimer toutes les technologies

```bash
curl -X DELETE http://localhost:3000/technologies
```

### Vérifier l'état de l'application

```bash
curl -X GET http://localhost:3000/health
```

## Utilisation avec Kubernetes

Cette application est conçue pour démontrer :

- Les volumes persistants (PV)
- Les revendications de volumes persistants (PVC)
- Le montage de volumes dans les pods
- La persistance des données entre les redémarrages de pods

Le dossier `data/` doit être monté sur un volume persistant pour conserver les données entre les redémarrages.

## Configuration

- **Port** : 3000 (configurable via la variable d'environnement `PORT`)
- **Fichier de données** : `data/technologies.txt`
- **Interface** : Écoute sur toutes les interfaces (0.0.0.0)

## Structure du projet

```
persistence-demo/
├── app.js           # Application principale
├── package.json     # Configuration npm
├── README.md        # Documentation
└── data/           # Dossier de données (créé automatiquement)
    └── technologies.txt  # Fichier de stockage des technologies
```
