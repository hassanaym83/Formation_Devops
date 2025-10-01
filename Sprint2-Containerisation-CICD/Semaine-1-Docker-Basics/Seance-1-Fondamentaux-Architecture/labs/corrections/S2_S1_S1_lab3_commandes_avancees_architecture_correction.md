# CORRECTION LAB 3 : Commandes Docker avancées et exploration de l'architecture

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab3_commandes_avancees_architecture_correction`

## Solutions détaillées

### Phase 1 : Inspection approfondie des conteneurs

**Déploiement des conteneurs** :

```bash
# Conteneurs de test
docker run -d --name web-server -p 8080:80 nginx:alpine
docker run -d --name test-db -e MYSQL_ROOT_PASSWORD=secret mysql:8.0
docker run -d --name ubuntu-container -it ubuntu:20.04 sleep infinity
```

**Inspection avec docker inspect** :

```bash
# Inspection complète
docker inspect web-server

# Informations spécifiques clés :
docker inspect web-server --format='{{.State.Status}}'           # running
docker inspect web-server --format='{{.NetworkSettings.IPAddress}}'  # Ex: 172.17.0.2
docker inspect web-server --format='{{.Config.Image}}'          # nginx:alpine
docker inspect web-server --format='{{.Config.WorkingDir}}'     # /
```

**Analyse d'image** :

```bash
# Historique des couches
docker history nginx:alpine

# Résultat attendu : environ 6-7 couches
# Couche de base Alpine + couches Nginx
```

**Configuration réseau** :

```bash
# JSON formaté de la configuration réseau
docker inspect web-server --format='{{json .NetworkSettings}}' | python -m json.tool

# Réseaux Docker
docker network ls
# bridge, host, none par défaut

# Inspection du réseau bridge
docker network inspect bridge
```

**Réponses aux questions d'analyse** :

1. **IP du conteneur web-server** : Généralement 172.17.0.x (visible dans NetworkSettings.IPAddress)
2. **Couches nginx:alpine** : Environ 6-7 couches (base Alpine + Nginx)
3. **Répertoire de travail Ubuntu** : `/` (racine)

### Phase 2 : Debugging et logs

**Analyse des logs** :

```bash
# Logs Nginx avec horodatage
docker logs -f --timestamps web-server

# Exemple de sortie :
# 2025-10-01T10:00:00.000000000Z /docker-entrypoint.sh: Configuration complete; ready for start up
```

**Génération de trafic et observation** :

```bash
# Tests d'accès
curl http://localhost:8080          # 200 OK
curl http://localhost:8080/test     # 404 Not Found

# Logs d'accès attendus :
# 172.17.0.1 - - [01/Oct/2025:10:00:00 +0000] "GET / HTTP/1.1" 200 615
# 172.17.0.1 - - [01/Oct/2025:10:00:01 +0000] "GET /test HTTP/1.1" 404 153
```

**Debugging avec exec** :

```bash
# Shell Ubuntu
docker exec -it ubuntu-container /bin/bash

# Commandes de diagnostic attendues :
ps aux          # Processus : PID 1 = sleep infinity
cat /etc/os-release  # Ubuntu 20.04.x LTS
df -h           # Utilisation filesystem
mount           # Points de montage
```

**Debugging MySQL** :

```bash
# Test de connectivité
docker exec test-db mysqladmin ping -p
# Résultat attendu : "mysqld is alive"

# Console MySQL
docker exec -it test-db mysql -p
# SHOW DATABASES; → information_schema, mysql, performance_schema, sys
# SELECT version(); → 8.0.x
```

### Phase 3 : Monitoring et statistiques

**Statistiques de performance** :

```bash
# Stats en temps réel
docker stats

# Résultats typiques :
# web-server : CPU ~0%, MEM 2-5MB
# test-db : CPU ~0-2%, MEM 200-400MB
# ubuntu-container : CPU ~0%, MEM 1-2MB
```

**Analyse des processus** :

```bash
# Processus Nginx
docker top web-server
# PID  USER  COMMAND
# 1    root  nginx: master process
# X    nginx nginx: worker process

# Processus MySQL
docker top test-db
# PID  USER  COMMAND
# 1    mysql mysqld
```

**Test de charge** :

```bash
# Génération de charge
for i in {1..100}; do curl -s http://localhost:8080 > /dev/null; done &

# Monitoring pendant la charge
docker stats web-server --no-stream
# CPU peut monter à 1-5% temporairement
```

**Analyse filesystem** :

```bash
# Utilisation globale Docker
docker system df

# Différences avec image de base
docker diff ubuntu-container
# A /tmp
# A /root/.bash_history
```

### Phase 4 : Exploration du système Docker

**Informations système** :

```bash
# Info système Docker
docker system info

# Éléments clés à noter :
# - Server Version
# - Storage Driver (overlay2 généralement)
# - Logging Driver (json-file par défaut)
# - Containers/Images counts
```

**Analyse des images** :

```bash
# Images avec tailles
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Tailles typiques :
# nginx:alpine ~23MB
# mysql:8.0 ~500MB
# ubuntu:20.04 ~72MB
```

**Monitoring des événements** :

```bash
# Terminal 1 : Monitoring
docker events &

# Terminal 2 : Actions
docker stop web-server    # Event : container stop
docker start web-server   # Event : container start
```

### Phase 5 : Administration avancée

**Gestion en lot** :

```bash
# Arrêt de tous les conteneurs
docker stop $(docker ps -q)

# Redémarrage sélectif
docker start web-server ubuntu-container

# Statut formaté
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
```

**Filtrage avancé** :

```bash
# Conteneurs en cours
docker ps --filter "status=running"

# Conteneurs arrêtés
docker ps -a --filter "status=exited"

# Conteneurs par nom
docker ps --filter "name=web"

# Images Nginx
docker images --filter "reference=nginx*"
```

**Export et sauvegarde** :

```bash
# Export conteneur
docker export ubuntu-container > ubuntu-backup.tar

# Sauvegarde image
docker save nginx:alpine > nginx-alpine.tar

# Vérification
ls -lh *.tar
# ubuntu-backup.tar ~72MB
# nginx-alpine.tar ~24MB
```

**Nettoyage** :

```bash
# Conteneurs arrêtés
docker container prune -f

# Images non utilisées
docker image prune

# Nettoyage complet
docker system prune --volumes

# Espace libéré affiché
```

## Tests de validation finale

### Diagnostic conteneur problématique

```bash
# Conteneur avec mauvaise configuration de port
docker run -d --name problematic-app -p 3000:8080 nginx:alpine

# Diagnostic :
docker logs problematic-app     # Nginx démarre normalement
docker inspect problematic-app --format='{{.Config.ExposedPorts}}'  # 80/tcp
# Problème : Nginx écoute sur port 80, mais on map le port 8080

# Solution :
curl http://localhost:3000      # Connection refused
docker stop problematic-app
docker rm problematic-app
docker run -d --name fixed-app -p 3000:80 nginx:alpine
curl http://localhost:3000     # Fonctionne !
```

### Analyse comparative

```bash
# Serveurs web comparatifs
docker run -d --name apache-server -p 8081:80 httpd:alpine
docker run -d --name nginx-server -p 8082:80 nginx:alpine

# Stats comparatives
docker stats apache-server nginx-server --no-stream

# Résultats typiques :
# Apache : MEM ~8-15MB, CPU ~0%
# Nginx : MEM ~2-5MB, CPU ~0%
# → Nginx plus léger en mémoire

# Test performance
time curl -s http://localhost:8081 > /dev/null  # ~0.01s
time curl -s http://localhost:8082 > /dev/null  # ~0.01s
# Performances similaires pour requêtes simples
```

## Points clés à retenir

### Commandes essentielles maîtrisées

1. **Inspection** : `docker inspect` avec templates de format
2. **Debugging** : `docker logs`, `docker exec`
3. **Monitoring** : `docker stats`, `docker top`
4. **Administration** : `docker system`, filtres avancés

### Architecture Docker comprise

1. **Isolation** : Conteneurs partagent le kernel mais sont isolés
2. **Réseaux** : Bridge par défaut, IP dynamiques
3. **Filesystem** : Couches read-only + layer modifiable
4. **Processus** : PID 1 = processus principal du conteneur

### Bonnes pratiques

1. **Monitoring régulier** avec `docker stats`
2. **Logs centralisés** avec `docker logs`
3. **Nettoyage périodique** avec `docker system prune`
4. **Inspection systématique** en cas de problème

---

**Formateur** : Hassan ESSADIK  
**Validation** : Maîtrise opérationnelle des commandes avancées Docker
