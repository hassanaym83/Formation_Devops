# LAB 2 : Manipulation de conteneurs et images

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab2_manipulation_conteneurs`  
**Durée** : 25 minutes

## Objectif du LAB

Explorer l'architecture Docker en manipulant images et conteneurs pour créer un environnement de développement pour équipe DevOps.

## Contexte métier

L'équipe DevOps doit standardiser l'environnement de développement avec une stack complète : base de données, cache Redis, serveur web. Vous devez maîtriser la gestion des images et conteneurs pour orchestrer ces services.

## Prérequis techniques

- Docker Engine installé et fonctionnel (LAB 1 complété)
- Connexion internet pour télécharger images
- 8GB RAM recommandé pour stack complète
- Ports 80, 5432, 6379 disponibles

## Énoncé détaillé

### Phase 1 : Exploration Docker Hub et téléchargement d'images

**Contexte** : Sélection des images officielles pour environnement DevOps

**Instructions** :

1. **Recherche sur Docker Hub** :

   ```bash
   docker search postgres
   docker search redis
   docker search nginx
   ```

2. **Téléchargement images officielles** :

   ```bash
   docker pull postgres:13-alpine
   docker pull redis:6-alpine
   docker pull nginx:1.21-alpine
   docker pull node:16-alpine
   ```

3. **Exploration des images** :
   ```bash
   docker images
   docker image inspect postgres:13-alpine
   docker image history nginx:1.21-alpine
   ```

**Validation** :

- 4 images téléchargées avec succès
- Inspection montre les métadonnées complètes
- Historique révèle la structure en couches

**Livrables** :

- Liste des images avec leurs tailles
- Analyse de la structure d'une image au choix

### Phase 2 : Analyse de la structure en couches

**Contexte** : Compréhension du système de couches Docker

**Instructions** :

1. **Analyse détaillée des couches** :

   ```bash
   docker image history postgres:13-alpine --no-trunc
   docker image inspect nginx:1.21-alpine --format='{{.RootFS.Layers}}'
   ```

2. **Comparaison des tailles** :

   ```bash
   docker system df
   docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
   ```

3. **Test de partage de couches** :

   ```bash
   docker pull alpine:3.14
   docker pull alpine:3.15
   docker system df -v
   ```

4. **Exploration du système de fichiers** :
   ```bash
   docker run --rm alpine:3.14 ls -la /
   docker run --rm alpine:3.14 cat /etc/os-release
   ```

**Validation** :

- Historique des couches affiché pour 2 images minimum
- Comparaison des tailles documentée
- Partage de couches démontré
- Exploration filesystem réussie

**Livrables** :

- Schéma de structure en couches d'une image
- Calcul de l'espace économisé par partage de couches

### Phase 3 : Gestion du cycle de vie des conteneurs

**Contexte** : Orchestration manuelle de services pour stack DevOps

**Instructions** :

1. **Déploiement PostgreSQL** :

   ```bash
   docker run -d \
     --name dev-postgres \
     -e POSTGRES_DB=devdb \
     -e POSTGRES_USER=devuser \
     -e POSTGRES_PASSWORD=devpass \
     -p 5432:5432 \
     postgres:13-alpine
   ```

2. **Déploiement Redis** :

   ```bash
   docker run -d \
     --name dev-redis \
     -p 6379:6379 \
     redis:6-alpine
   ```

3. **Test de connectivité** :

   ```bash
   docker run --rm --link dev-postgres:postgres postgres:13-alpine \
     psql -h postgres -U devuser -d devdb -c "SELECT version();"

   docker run --rm --link dev-redis:redis redis:6-alpine \
     redis-cli -h redis ping
   ```

4. **Gestion du cycle de vie** :
   ```bash
   docker ps
   docker pause dev-redis
   docker ps
   docker unpause dev-redis
   docker stop dev-postgres
   docker start dev-postgres
   docker restart dev-redis
   ```

**Validation** :

- PostgreSQL et Redis déployés avec succès
- Tests de connectivité réussis
- Tous les états du cycle de vie testés
- Services redémarrés sans perte de données

**Livrables** :

- Log des commandes de déploiement
- Preuve de connectivité aux bases de données

### Phase 4 : Inspection et monitoring de base

**Contexte** : Surveillance des conteneurs en production

**Instructions** :

1. **Inspection détaillée** :

   ```bash
   docker inspect dev-postgres --format='{{.State.Status}}'
   docker inspect dev-postgres --format='{{.NetworkSettings.IPAddress}}'
   docker inspect dev-postgres --format='{{.Config.Env}}'
   ```

2. **Monitoring en temps réel** :

   ```bash
   docker stats dev-postgres dev-redis --no-stream
   docker top dev-postgres
   docker top dev-redis
   ```

3. **Gestion des logs** :

   ```bash
   docker logs dev-postgres --tail 20
   docker logs dev-redis --since "5m"
   docker logs -f dev-postgres &
   # Générer activité puis arrêter le suivi
   ```

4. **Inspection du réseau** :
   ```bash
   docker network ls
   docker network inspect bridge
   ```

**Validation** :

- Métadonnées des conteneurs récupérées
- Monitoring des ressources effectué
- Logs consultés avec différents filtres
- Configuration réseau inspectée

**Livrables** :

- Rapport de monitoring des ressources
- Analyse des logs système

## Phase bonus : Création d'image personnalisée

**Contexte** : Création d'un outil DevOps personnalisé

**Instructions** :

1. **Créer un Dockerfile** :

   ```dockerfile
   FROM alpine:3.14
   RUN apk add --no-cache curl jq wget
   COPY check-services.sh /usr/local/bin/
   RUN chmod +x /usr/local/bin/check-services.sh
   CMD ["/usr/local/bin/check-services.sh"]
   ```

2. **Script de vérification** :

   ```bash
   #!/bin/sh
   echo "Checking services..."
   curl -s http://dev-redis:6379 || echo "Redis not accessible"
   echo "Health check completed"
   ```

3. **Build et test** :
   ```bash
   docker build -t devops-checker:v1.0 .
   docker run --rm --link dev-redis:dev-redis devops-checker:v1.0
   ```

**Validation** :

- Image personnalisée construite avec succès
- Script de vérification fonctionnel
- Test d'exécution réussi

## Nettoyage final

```bash
docker stop dev-postgres dev-redis
docker rm dev-postgres dev-redis
docker rmi postgres:13-alpine redis:6-alpine nginx:1.21-alpine node:16-alpine
docker system prune -f
```

## Ressources et aide

**Documentation** :

- [Docker Hub Official Images](https://hub.docker.com/)
- [Docker Container Management](https://docs.docker.com/engine/reference/commandline/container/)

**Dépannage** :

- Port déjà utilisé : `docker ps` et `netstat -tulpn`
- Problème de connectivité : vérifier les liens et réseaux
- Erreur de permissions : vérifier les variables d'environnement

## Livrables attendus

1. **Rapport d'analyse des images** :

   - Structure en couches détaillée
   - Comparaison des tailles
   - Optimisations identifiées

2. **Documentation de déploiement** :

   - Commandes utilisées
   - Configuration des services
   - Tests de validation

3. **Rapport de monitoring** :
   - Métriques de performance
   - Analyse des logs
   - Recommandations d'optimisation

---

**Aide formateur** : Hassan ESSADIK  
**Durée recommandée** : 25 minutes  
**Prochaine étape** : LAB 3 - Application multi-conteneurs avec communication
