# Scripts Docker Compose

## Pré-requis

Avant de démarrer, assurez-vous que :
- Docker Desktop est installé et démarré
- Le service Docker est en cours d'exécution

### Vérifier Docker
```bash
# Vérifier que Docker fonctionne
docker --version
docker ps

# Si Docker Desktop n'est pas démarré sur Windows
# Lancez Docker Desktop depuis le menu Démarrer
```

## Démarrage de l'application

```bash
# Construire et démarrer l'application
docker-compose up --build

# Démarrer en arrière-plan
docker-compose up -d --build

# Utiliser la version simplifiée
docker-compose -f docker-compose.simple.yml up --build
```

## Commandes utiles

```bash
# Voir les logs
docker-compose logs -f

# Arrêter l'application
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Reconstruire les images
docker-compose build --no-cache
```

## Test de l'application

```bash
# Vérifier l'état de santé
curl http://localhost:3000/health

# Ajouter une technologie
curl -X POST http://localhost:3000/technologies \
  -H "Content-Type: application/json" \
  -d '{"technology": "Docker"}'

# Récupérer les technologies
curl http://localhost:3000/technologies
```

## Volumes

- **technologies_data** : Volume Docker persistant pour stocker les données
- Monté sur `/app/data` dans le conteneur
- Les données persistent même après l'arrêt du conteneur

## Résolution de problèmes

### Erreur "unable to get image"
Si vous rencontrez l'erreur :
```
unable to get image 'persistence-demo-persistence-demo': error during connect
```

**Solutions :**
1. **Démarrer Docker Desktop :**
   - Sur Windows : Lancez Docker Desktop depuis le menu Démarrer
   - Attendez que Docker soit complètement démarré (icône Docker stable)

2. **Vérifier Docker :**
   ```bash
   docker --version
   docker ps
   ```

3. **Nettoyer et reconstruire :**
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

### Problème de version obsolète
L'avertissement `version is obsolete` est normal avec les nouvelles versions de Docker Compose. Le fichier fonctionne correctement sans l'attribut `version`.
