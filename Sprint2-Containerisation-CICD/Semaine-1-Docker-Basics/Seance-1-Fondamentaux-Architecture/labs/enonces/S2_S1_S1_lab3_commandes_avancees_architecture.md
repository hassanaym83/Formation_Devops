# LAB 3 : Commandes Docker avancées et exploration de l'architecture

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab3_commandes_avancees_architecture`  
**Durée** : 30 minutes

## Objectif du LAB

Maîtriser les commandes Docker avancées pour explorer en profondeur l'architecture et comprendre le fonctionnement interne des conteneurs dans un contexte DevOps professionnel.

## Contexte métier

En tant que DevOps, vous devez être capable de diagnostiquer, débugger et monitorer les conteneurs en production. Ce LAB vous apprend les commandes essentielles pour l'inspection, le debugging et le monitoring des conteneurs.

## Prérequis techniques

- Docker Engine installé et fonctionnel (LABs 1 et 2 complétés)
- Connaissance des commandes de base : run, stop, start, rm
- Ports 80, 8080, 3000 disponibles
- Minimum 4GB RAM

## Énoncé détaillé

### Phase 1 : Inspection approfondie des conteneurs

**Contexte** : Comprendre l'architecture interne et la configuration des conteneurs

**Instructions** :

1. **Déploiement de conteneurs de test** :

   ```bash
   # Conteneur web Nginx
   docker run -d --name web-server -p 8080:80 nginx:alpine

   # Conteneur base de données
   docker run -d --name test-db -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

   # Conteneur interactif Ubuntu
   docker run -d --name ubuntu-container -it ubuntu:20.04 sleep infinity
   ```

2. **Inspection détaillée avec docker inspect** :

   ```bash
   # Inspection complète du conteneur Nginx
   docker inspect web-server

   # Extraction d'informations spécifiques
   docker inspect web-server --format='{{.State.Status}}'
   docker inspect web-server --format='{{.NetworkSettings.IPAddress}}'
   docker inspect web-server --format='{{.Config.Image}}'
   docker inspect web-server --format='{{.Mounts}}'
   ```

3. **Analyse des métadonnées de l'image** :

   ```bash
   # Inspection de l'image source
   docker inspect nginx:alpine

   # Historique des couches
   docker history nginx:alpine

   # Informations de taille par couche
   docker history nginx:alpine --format "table {{.CreatedBy}}\t{{.Size}}"
   ```

4. **Exploration de la configuration réseau** :

   ```bash
   # Configuration réseau détaillée
   docker inspect web-server --format='{{json .NetworkSettings}}' | python -m json.tool

   # Liste des réseaux Docker
   docker network ls

   # Inspection du réseau bridge par défaut
   docker network inspect bridge
   ```

**Validation** :

- Comprendre la structure JSON d'inspection
- Identifier l'IP du conteneur et sa configuration réseau
- Analyser l'historique des couches d'une image

**Questions d'analyse** :

1. Quelle est l'adresse IP du conteneur web-server ?
2. Combien de couches compose l'image nginx:alpine ?
3. Quel est le répertoire de travail par défaut du conteneur Ubuntu ?

### Phase 2 : Debugging et logs

**Contexte** : Techniques de debugging pour diagnostiquer les problèmes de conteneurs

**Instructions** :

1. **Analyse des logs en temps réel** :

   ```bash
   # Logs du conteneur Nginx
   docker logs web-server

   # Logs en temps réel avec horodatage
   docker logs -f --timestamps web-server

   # Dernières 10 lignes de logs
   docker logs --tail 10 web-server
   ```

2. **Génération de trafic pour analyser les logs** :

   ```bash
   # Test du serveur web (dans un autre terminal)
   curl http://localhost:8080
   curl http://localhost:8080/nonexistent
   curl http://localhost:8080/

   # Observation des logs d'accès
   docker logs --tail 20 web-server
   ```

3. **Debugging avec docker exec** :

   ```bash
   # Accès shell au conteneur Ubuntu
   docker exec -it ubuntu-container /bin/bash

   # Dans le conteneur Ubuntu, explorer la structure :
   ps aux
   cat /etc/os-release
   df -h
   mount
   exit

   # Exécution de commandes ponctuelles
   docker exec ubuntu-container ps aux
   docker exec ubuntu-container cat /proc/meminfo
   docker exec web-server nginx -t
   ```

4. **Debugging du conteneur MySQL** :

   ```bash
   # Vérification du statut MySQL
   docker exec test-db mysqladmin ping -p

   # Accès à la console MySQL
   docker exec -it test-db mysql -p
   # Dans MySQL :
   SHOW DATABASES;
   SELECT version();
   \q
   ```

**Validation** :

- Accès réussi aux shells des conteneurs
- Compréhension des logs d'application
- Capacité d'exécuter des commandes de diagnostic

### Phase 3 : Monitoring et statistiques

**Contexte** : Surveillance des performances et ressources des conteneurs

**Instructions** :

1. **Monitoring des ressources en temps réel** :

   ```bash
   # Statistiques globales
   docker stats

   # Statistiques d'un conteneur spécifique
   docker stats web-server --no-stream

   # Statistiques formatées
   docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
   ```

2. **Analyse détaillée des processus** :

   ```bash
   # Processus dans le conteneur
   docker top web-server
   docker top ubuntu-container
   docker top test-db

   # Processus détaillés avec colonnes personnalisées
   docker top web-server aux
   ```

3. **Test de charge et monitoring** :

   ```bash
   # Génération de charge sur Nginx
   for i in {1..100}; do curl -s http://localhost:8080 > /dev/null; done &

   # Surveillance pendant la charge
   docker stats web-server --no-stream

   # Vérification des processus actifs
   docker top web-server
   ```

4. **Analyse de l'utilisation du système de fichiers** :

   ```bash
   # Taille des conteneurs
   docker system df

   # Utilisation détaillée par conteneur
   docker exec ubuntu-container df -h
   docker exec web-server df -h

   # Différences avec l'image de base
   docker diff ubuntu-container
   docker diff web-server
   ```

**Validation** :

- Compréhension des métriques de performance
- Capacité à identifier les processus actifs
- Analyse de l'utilisation des ressources

### Phase 4 : Exploration du système Docker

**Contexte** : Comprendre l'infrastructure Docker sous-jacente

**Instructions** :

1. **Exploration du système Docker** :

   ```bash
   # Informations générales du système Docker
   docker system info

   # Version détaillée
   docker version

   # Espace disque utilisé
   docker system df -v
   ```

2. **Analyse des images et couches** :

   ```bash
   # Liste des images avec tailles
   docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

   # Images intermédiaires (dangling)
   docker images --filter "dangling=true"

   # Historique détaillé d'une image
   docker history --no-trunc nginx:alpine
   ```

3. **Exploration des réseaux et volumes** :

   ```bash
   # Réseaux disponibles
   docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"

   # Volumes Docker
   docker volume ls

   # Conteneurs en cours d'exécution avec leurs ports
   docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
   ```

4. **Analyse des événements Docker** :

   ```bash
   # Événements en temps réel (nouveau terminal)
   docker events &

   # Dans le terminal principal, déclencher des événements
   docker stop web-server
   docker start web-server
   docker restart test-db

   # Arrêter le monitoring d'événements
   pkill -f "docker events"
   ```

**Validation** :

- Compréhension de l'infrastructure Docker
- Capacité à analyser l'utilisation des ressources
- Maîtrise du monitoring des événements système

### Phase 5 : Commandes d'administration avancées

**Contexte** : Outils d'administration pour la gestion quotidienne

**Instructions** :

1. **Gestion des conteneurs en lot** :

   ```bash
   # Arrêt de tous les conteneurs
   docker stop $(docker ps -q)

   # Redémarrage sélectif
   docker start web-server ubuntu-container

   # Statut détaillé de tous les conteneurs
   docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
   ```

2. **Filtrage et recherche avancés** :

   ```bash
   # Conteneurs par statut
   docker ps --filter "status=running"
   docker ps -a --filter "status=exited"

   # Conteneurs par nom
   docker ps --filter "name=web"

   # Images par référentiel
   docker images --filter "reference=nginx*"
   ```

3. **Export et sauvegarde** :

   ```bash
   # Export d'un conteneur vers archive tar
   docker export ubuntu-container > ubuntu-backup.tar

   # Sauvegarde d'une image
   docker save nginx:alpine > nginx-alpine.tar

   # Vérification des archives créées
   ls -lh *.tar
   ```

4. **Nettoyage et optimisation** :

   ```bash
   # Nettoyage des conteneurs arrêtés
   docker container prune -f

   # Nettoyage des images non utilisées
   docker image prune

   # Nettoyage complet du système
   docker system prune --volumes

   # Vérification de l'espace libéré
   docker system df
   ```

**Validation** :

- Maîtrise des opérations en lot
- Compréhension des filtres Docker
- Capacité d'export et de sauvegarde

## Tests de validation finale

### Diagnostic d'un conteneur problématique

```bash
# Créer un conteneur avec problème
docker run -d --name problematic-app \
  -p 3000:8080 \
  nginx:alpine \
  nginx -g 'daemon off; error_log /dev/stderr debug;'

# Diagnostiquer le problème
docker logs problematic-app
docker inspect problematic-app --format='{{.Config.ExposedPorts}}'
docker exec problematic-app netstat -tlnp
```

### Analyse de performance comparative

```bash
# Comparer les performances de deux serveurs web
docker run -d --name apache-server -p 8081:80 httpd:alpine
docker run -d --name nginx-server -p 8082:80 nginx:alpine

# Monitoring comparatif
docker stats apache-server nginx-server --no-stream

# Test de charge comparatif
time curl -s http://localhost:8081 > /dev/null
time curl -s http://localhost:8082 > /dev/null
```

## Nettoyage final

```bash
# Arrêt et suppression de tous les conteneurs de test
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Suppression des archives
rm -f *.tar

# Nettoyage système
docker system prune -f
```

## Ressources et aide

**Commandes de référence** :

- `docker inspect` : Informations détaillées
- `docker logs` : Debugging et monitoring
- `docker exec` : Accès shell et commandes
- `docker stats` : Métriques de performance
- `docker top` : Processus des conteneurs
- `docker events` : Événements système

**Documentation** :

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/)
- [Docker Logging](https://docs.docker.com/config/containers/logging/)
- [Docker Monitoring](https://docs.docker.com/config/containers/resource_constraints/)

## Livrables attendus

1. **Rapport d'inspection** :

   - Configuration réseau de 3 conteneurs
   - Analyse des couches d'images utilisées
   - Métriques de performance observées

2. **Script de diagnostic** :

   - Commandes d'inspection automatisées
   - Procédure de debugging standard
   - Monitoring des ressources

3. **Documentation des bonnes pratiques** :
   - Commandes essentielles mémorisées
   - Techniques de debugging
   - Méthodes de monitoring

---

**Aide formateur** : Hassan ESSADIK  
**Durée recommandée** : 30 minutes  
**Validation finale** : Maîtrise des commandes avancées et compréhension de l'architecture Docker
