# CORRECTION LAB 2 : Manipulation de conteneurs et images

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab2_manipulation_conteneurs`  
**Durée correction** : 15 minutes  
**Points** : 10/30

## Solution complète et explications

### Phase 1 : Exploration Docker Hub et téléchargement d'images (2 points)

#### Solution détaillée avec commandes

```bash
# 1. Recherche sur Docker Hub
docker search postgres
# Résultat attendu: Liste avec postgres (OFFICIAL), postgres/postgres, etc.

docker search redis
# Résultat attendu: redis (OFFICIAL) en première position

docker search nginx
# Résultat attendu: nginx (OFFICIAL) avec high star count

# 2. Téléchargement des images officielles
docker pull postgres:13-alpine
# Sortie: Pulling from library/postgres
# 13-alpine: Pulling from library/postgres
# Status: Downloaded newer image for postgres:13-alpine

docker pull redis:6-alpine
# Sortie: 6-alpine: Pulling from library/redis

docker pull nginx:1.21-alpine
# Sortie: 1.21-alpine: Pulling from library/nginx

docker pull node:16-alpine
# Sortie: 16-alpine: Pulling from library/node

# 3. Vérification des images téléchargées
docker images
# Sortie attendue:
# REPOSITORY   TAG        IMAGE ID       CREATED       SIZE
# postgres     13-alpine  f0b28aaa7edf   2 weeks ago   196MB
# redis        6-alpine   f0b28aaa7edf   2 weeks ago   32.3MB
# nginx        1.21-alpine f0b28aaa7edf  2 weeks ago   22.8MB
# node         16-alpine  f0b28aaa7edf   2 weeks ago   109MB
```

#### Inspection détaillée des images

```bash
# Inspection complète PostgreSQL
docker image inspect postgres:13-alpine
# Points clés dans la sortie:
# - "Architecture": "amd64"
# - "Os": "linux"
# - "ExposedPorts": {"5432/tcp": {}}
# - "Env": ["POSTGRES_USER=postgres", "POSTGRES_DB=postgres"]

# Analyse de l'historique
docker image history nginx:1.21-alpine
# Résultat: montre les couches et leur taille
# IMAGE         CREATED       CREATED BY                                      SIZE
# 2b7d6430f78d  2 weeks ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…  0B
# <missing>     2 weeks ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT          0B
```

**Points d'évaluation** :

- 4 images officielles téléchargées (1 point)
- Inspection et historique analysés (1 point)

### Phase 2 : Analyse de la structure en couches (4 points)

#### Analyse détaillée des couches

```bash
# 1. Historique détaillé sans troncature
docker image history postgres:13-alpine --no-trunc
# Résultat: Historique complet avec commandes de construction

docker image history nginx:1.21-alpine --no-trunc
# Analyse des étapes de construction

# 2. Inspection des couches RootFS
docker image inspect nginx:1.21-alpine --format='{{.RootFS.Layers}}'
# Sortie: [sha256:abc123... sha256:def456... sha256:ghi789...]

docker image inspect postgres:13-alpine --format='{{.RootFS.Layers}}'
# Comparaison du nombre de couches

# 3. Analyse de l'utilisation d'espace
docker system df
# Sortie attendue:
# TYPE      TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images    4         0         360.1MB   360.1MB (100%)
# Containers 0        0         0B        0B
# Local Volumes 0     0         0B        0B

docker system df -v
# Détails par image avec partage de couches

# 4. Test du partage de couches Alpine
docker pull alpine:3.14
docker pull alpine:3.15

# Vérification du partage
docker system df
# La taille totale doit être < somme des tailles individuelles
```

#### Exemple d'analyse de couches

```bash
# Exploration du filesystem Alpine
docker run --rm alpine:3.14 ls -la /
# Sortie: Structure de répertoires Alpine de base

docker run --rm alpine:3.14 cat /etc/os-release
# Sortie:
# NAME="Alpine Linux"
# ID=alpine
# VERSION_ID=3.14.10
# PRETTY_NAME="Alpine Linux v3.14"

# Comparaison des tailles
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
# REPOSITORY   TAG        SIZE
# postgres     13-alpine  196MB
# node         16-alpine  109MB
# nginx        1.21-alpine 22.8MB
# redis        6-alpine   32.3MB
# alpine       3.14       5.6MB
# alpine       3.15       5.6MB
```

**Économie d'espace calculée** :

- Alpine 3.14 + 3.15 = ~5.6MB (couche de base partagée)
- Sans partage = 2 × 5.6MB = 11.2MB
- Économie = ~50% sur la couche de base

**Points d'évaluation** :

- Historique des couches analysé (1 point)
- Comparaison des tailles effectuée (1 point)
- Partage de couches démontré (1 point)
- Exploration filesystem réussie (1 point)

### Phase 3 : Gestion du cycle de vie des conteneurs (4 points)

#### Solution complète de déploiement

```bash
# 1. Déploiement PostgreSQL avec configuration complète
docker run -d \
  --name dev-postgres \
  --restart unless-stopped \
  -e POSTGRES_DB=devdb \
  -e POSTGRES_USER=devuser \
  -e POSTGRES_PASSWORD=devpass \
  -p 5432:5432 \
  postgres:13-alpine

# Vérification du démarrage
docker ps
# Doit montrer dev-postgres en état "Up"

# 2. Déploiement Redis
docker run -d \
  --name dev-redis \
  --restart unless-stopped \
  -p 6379:6379 \
  redis:6-alpine

# 3. Test de connectivité PostgreSQL
# Attendre le démarrage complet (10-15 secondes)
sleep 15

docker run --rm --link dev-postgres:postgres postgres:13-alpine \
  psql -h postgres -U devuser -d devdb -c "SELECT version();"
# Sortie attendue: version de PostgreSQL

# Test avec insertion de données
docker run --rm --link dev-postgres:postgres postgres:13-alpine \
  psql -h postgres -U devuser -d devdb -c "CREATE TABLE test (id SERIAL, name TEXT);"

docker run --rm --link dev-postgres:postgres postgres:13-alpine \
  psql -h postgres -U devuser -d devdb -c "INSERT INTO test (name) VALUES ('Docker Test');"

# 4. Test de connectivité Redis
docker run --rm --link dev-redis:redis redis:6-alpine \
  redis-cli -h redis ping
# Sortie attendue: PONG

# Test avec données
docker run --rm --link dev-redis:redis redis:6-alpine \
  redis-cli -h redis SET test-key "Docker Redis Test"

docker run --rm --link dev-redis:redis redis:6-alpine \
  redis-cli -h redis GET test-key
# Sortie: "Docker Redis Test"
```

#### Gestion complète du cycle de vie

```bash
# État initial
docker ps
# Les 2 conteneurs doivent être "Up"

# Test de pause/reprise
docker pause dev-redis
docker ps  # dev-redis doit être en état "Up (Paused)"

docker unpause dev-redis
docker ps  # dev-redis revient en état "Up"

# Test arrêt/démarrage
docker stop dev-postgres
docker ps -a  # dev-postgres en état "Exited"

docker start dev-postgres
sleep 10  # Attendre redémarrage PostgreSQL

# Vérification persistance des données
docker run --rm --link dev-postgres:postgres postgres:13-alpine \
  psql -h postgres -U devuser -d devdb -c "SELECT * FROM test;"
# Doit afficher la donnée insérée précédemment

# Test restart complet
docker restart dev-redis
docker logs dev-redis --tail 10
# Logs de redémarrage Redis
```

**Points d'évaluation** :

- PostgreSQL déployé et configuré (1 point)
- Redis déployé avec succès (1 point)
- Tests de connectivité réussis (1 point)
- Cycle de vie complet testé (1 point)

### Phase 4 : Inspection et monitoring de base (2 points)

#### Inspection détaillée des conteneurs

```bash
# 1. Métadonnées des conteneurs
docker inspect dev-postgres --format='{{.State.Status}}'
# Sortie: running

docker inspect dev-postgres --format='{{.NetworkSettings.IPAddress}}'
# Sortie: IP du conteneur (ex: 172.17.0.2)

docker inspect dev-postgres --format='{{.Config.Env}}'
# Sortie: [POSTGRES_DB=devdb POSTGRES_USER=devuser ...]

# Configuration réseau détaillée
docker inspect dev-postgres --format='{{.NetworkSettings.Ports}}'
# Sortie: map[5432/tcp:[{0.0.0.0 5432}]]

# 2. Monitoring des ressources en temps réel
docker stats dev-postgres dev-redis --no-stream
# Sortie attendue:
# CONTAINER     CPU %   MEM USAGE / LIMIT     MEM %    NET I/O       BLOCK I/O
# dev-postgres  0.15%   45.2MiB / 15.6GiB     0.28%    1.2kB / 648B  8.19MB / 16.4kB
# dev-redis     0.08%   8.5MiB / 15.6GiB      0.05%    648B / 648B   0B / 0B

# Processus dans les conteneurs
docker top dev-postgres
# Sortie: processus PostgreSQL actifs

docker top dev-redis
# Sortie: processus Redis server
```

#### Gestion avancée des logs

```bash
# 3. Analyse des logs
docker logs dev-postgres --tail 20
# Logs de démarrage PostgreSQL

docker logs dev-redis --since "5m"
# Logs Redis des 5 dernières minutes

# Logs en temps réel (lancer en arrière-plan)
docker logs -f dev-postgres &
LOGS_PID=$!

# Générer de l'activité
docker run --rm --link dev-postgres:postgres postgres:13-alpine \
  psql -h postgres -U devuser -d devdb -c "SELECT NOW();"

# Arrêter le suivi des logs
kill $LOGS_PID

# 4. Inspection du réseau
docker network ls
# Sortie: réseaux Docker disponibles

docker network inspect bridge
# Configuration du réseau bridge par défaut
```

**Points d'évaluation** :

- Métadonnées récupérées (1 point)
- Monitoring et logs configurés (1 point)

### Phase bonus : Création d'image personnalisée (2 points)

#### Solution complète avec Dockerfile

```dockerfile
# Dockerfile pour outil DevOps
FROM alpine:3.14

# Métadonnées
LABEL maintainer="hassan.essadik@simplon.ma"
LABEL description="DevOps Health Checker Tool"
LABEL version="1.0"

# Installation des outils
RUN apk add --no-cache \
    curl \
    jq \
    wget \
    netcat-openbsd \
    bash

# Création du répertoire de travail
WORKDIR /app

# Copie du script de health check
COPY check-services.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/check-services.sh

# Variable d'environnement
ENV CHECK_INTERVAL=30
ENV LOG_LEVEL=INFO

# Exposition du port pour monitoring
EXPOSE 8080

# Health check intégré
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD /usr/local/bin/check-services.sh --self-check || exit 1

# Point d'entrée
CMD ["/usr/local/bin/check-services.sh"]
```

#### Script de vérification avancé

```bash
#!/bin/bash
# check-services.sh

set -e

LOG_LEVEL=${LOG_LEVEL:-INFO}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$LOG_LEVEL] $1"
}

check_postgres() {
    log "Checking PostgreSQL connection..."
    if nc -z dev-postgres 5432; then
        log "✓ PostgreSQL is accessible"
        return 0
    else
        log "✗ PostgreSQL is not accessible"
        return 1
    fi
}

check_redis() {
    log "Checking Redis connection..."
    if nc -z dev-redis 6379; then
        log "✓ Redis is accessible"
        return 0
    else
        log "✗ Redis is not accessible"
        return 1
    fi
}

check_services() {
    log "Starting health check cycle..."

    postgres_status=0
    redis_status=0

    check_postgres || postgres_status=$?
    check_redis || redis_status=$?

    if [[ $postgres_status -eq 0 && $redis_status -eq 0 ]]; then
        log "✓ All services are healthy"
        return 0
    else
        log "✗ Some services are unhealthy"
        return 1
    fi
}

self_check() {
    log "Self-check mode"
    echo "DevOps Checker is running"
    return 0
}

# Point d'entrée principal
case "${1}" in
    --self-check)
        self_check
        ;;
    --continuous)
        while true; do
            check_services
            sleep ${CHECK_INTERVAL}
        done
        ;;
    *)
        check_services
        ;;
esac
```

#### Build et test de l'image

```bash
# 1. Construction de l'image
docker build -t devops-checker:v1.0 .
# Sortie: étapes de construction Dockerfile

# Vérification de l'image créée
docker images devops-checker
# REPOSITORY       TAG   IMAGE ID     CREATED         SIZE
# devops-checker   v1.0  a1b2c3d4e5f6 2 minutes ago  15.2MB

# 2. Test avec les conteneurs existants
docker run --rm --link dev-postgres:dev-postgres --link dev-redis:dev-redis \
  devops-checker:v1.0

# Sortie attendue:
# [2023-XX-XX XX:XX:XX] [INFO] Starting health check cycle...
# [2023-XX-XX XX:XX:XX] [INFO] Checking PostgreSQL connection...
# [2023-XX-XX XX:XX:XX] [INFO] ✓ PostgreSQL is accessible
# [2023-XX-XX XX:XX:XX] [INFO] Checking Redis connection...
# [2023-XX-XX XX:XX:XX] [INFO] ✓ Redis is accessible
# [2023-XX-XX XX:XX:XX] [INFO] ✓ All services are healthy

# 3. Test en mode continu (arrière-plan)
docker run -d --name health-checker \
  --link dev-postgres:dev-postgres \
  --link dev-redis:dev-redis \
  devops-checker:v1.0 --continuous

# Vérification des logs
docker logs health-checker
sleep 60
docker logs health-checker --tail 10

# Test du health check intégré
docker inspect health-checker --format='{{.State.Health.Status}}'
# Sortie: healthy

# Nettoyage
docker stop health-checker
docker rm health-checker
```

**Points d'évaluation** :

- Image construite avec succès (1 point)
- Script fonctionnel et tests réussis (1 point)

## Problèmes courants et solutions

### Erreur de connectivité entre conteneurs

**Problème** :

```
could not translate host name "dev-postgres" to address
```

**Solution** :

```bash
# Vérifier que les conteneurs sont en cours d'exécution
docker ps

# Utiliser --link correctement ou créer un réseau
docker network create dev-network
docker network connect dev-network dev-postgres
docker network connect dev-network dev-redis
```

### PostgreSQL pas prêt

**Problème** :

```
psql: FATAL: the database system is starting up
```

**Solution** :

```bash
# Attendre le démarrage complet
docker exec dev-postgres pg_isready -U devuser -d devdb
# Répéter jusqu'à "accepting connections"

# Ou utiliser un script d'attente
wait_for_postgres() {
    until docker exec dev-postgres pg_isready -U devuser -d devdb; do
        echo "Waiting for PostgreSQL..."
        sleep 2
    done
}
```

### Port déjà utilisé

**Problème** :

```
Error starting userland proxy: listen tcp 0.0.0.0:5432: bind: address already in use
```

**Solution** :

```bash
# Identifier le processus
sudo lsof -i :5432
sudo netstat -tulpn | grep :5432

# Utiliser un autre port
docker run -d --name dev-postgres -p 5433:5432 postgres:13-alpine
```

## Optimisations et bonnes pratiques

### Dockerfile optimisé

```dockerfile
# Multi-stage build pour optimiser la taille
FROM alpine:3.14 AS builder
RUN apk add --no-cache curl

FROM alpine:3.14
RUN apk add --no-cache jq netcat-openbsd bash
COPY --from=builder /usr/bin/curl /usr/bin/curl
# Image finale plus légère
```

### Gestion des ressources

```bash
# Limitation des ressources
docker run -d \
  --name dev-postgres \
  --memory="512m" \
  --cpus="0.5" \
  -e POSTGRES_DB=devdb \
  postgres:13-alpine

# Monitoring des limites
docker stats dev-postgres --no-stream
```

### Script de déploiement automatisé

```bash
#!/bin/bash
# deploy-dev-stack.sh

set -e

echo "Déploiement de la stack de développement..."

# Nettoyage préalable
docker stop dev-postgres dev-redis 2>/dev/null || true
docker rm dev-postgres dev-redis 2>/dev/null || true

# Déploiement PostgreSQL
docker run -d \
  --name dev-postgres \
  --restart unless-stopped \
  -e POSTGRES_DB=devdb \
  -e POSTGRES_USER=devuser \
  -e POSTGRES_PASSWORD=devpass \
  -p 5432:5432 \
  postgres:13-alpine

# Déploiement Redis
docker run -d \
  --name dev-redis \
  --restart unless-stopped \
  -p 6379:6379 \
  redis:6-alpine

# Attente et validation
echo "Attente du démarrage des services..."
sleep 15

# Tests de connectivité
if docker run --rm --link dev-postgres:postgres postgres:13-alpine \
   psql -h postgres -U devuser -d devdb -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✓ PostgreSQL opérationnel"
else
    echo "✗ PostgreSQL échec"
    exit 1
fi

if docker run --rm --link dev-redis:redis redis:6-alpine \
   redis-cli -h redis ping > /dev/null 2>&1; then
    echo "✓ Redis opérationnel"
else
    echo "✗ Redis échec"
    exit 1
fi

echo "Stack de développement déployée avec succès!"
```

## Tests de validation finale

### Script de validation automatisé

```bash
#!/bin/bash
# validate-lab2.sh

echo "=== Validation LAB 2 - Manipulation conteneurs ==="

# Test 1: Images téléchargées
EXPECTED_IMAGES=("postgres:13-alpine" "redis:6-alpine" "nginx:1.21-alpine" "node:16-alpine")
for image in "${EXPECTED_IMAGES[@]}"; do
    if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "$image"; then
        echo "✓ Image $image présente"
    else
        echo "✗ Image $image manquante"
    fi
done

# Test 2: Conteneurs en cours d'exécution
if docker ps --format "{{.Names}}" | grep -q "dev-postgres"; then
    echo "✓ PostgreSQL container en cours d'exécution"
else
    echo "✗ PostgreSQL container non trouvé"
fi

if docker ps --format "{{.Names}}" | grep -q "dev-redis"; then
    echo "✓ Redis container en cours d'exécution"
else
    echo "✗ Redis container non trouvé"
fi

# Test 3: Connectivité des services
if docker run --rm --link dev-postgres:postgres postgres:13-alpine \
   psql -h postgres -U devuser -d devdb -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✓ PostgreSQL connectivité OK"
else
    echo "✗ PostgreSQL connectivité échec"
fi

if docker run --rm --link dev-redis:redis redis:6-alpine \
   redis-cli -h redis ping | grep -q "PONG"; then
    echo "✓ Redis connectivité OK"
else
    echo "✗ Redis connectivité échec"
fi

# Test 4: Image personnalisée (si créée)
if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "devops-checker:v1.0"; then
    echo "✓ Image personnalisée créée"
else
    echo "⚠ Image personnalisée non trouvée (bonus)"
fi

echo "=== Validation terminée ==="
```

## Nettoyage final

```bash
#!/bin/bash
# cleanup-lab2.sh

echo "Nettoyage LAB 2..."

# Arrêt des conteneurs
docker stop dev-postgres dev-redis health-checker 2>/dev/null || true

# Suppression des conteneurs
docker rm dev-postgres dev-redis health-checker 2>/dev/null || true

# Suppression des images (optionnel)
read -p "Supprimer les images téléchargées? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker rmi postgres:13-alpine redis:6-alpine nginx:1.21-alpine node:16-alpine devops-checker:v1.0 2>/dev/null || true
fi

# Nettoyage système
docker system prune -f

echo "Nettoyage terminé!"
```

---

**Correction réalisée par** : Hassan ESSADIK  
**Durée de correction** : 15 minutes  
**Validation** : Manipulation avancée des conteneurs et images maîtrisée
