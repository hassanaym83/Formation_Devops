# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 1 - Séance 3 : Volumes et Networks Docker

## Objectifs pédagogiques

- Maîtriser la persistance des données avec volumes Docker
- Configurer et gérer les réseaux de conteneurs
- Implémenter des communications inter-conteneurs sécurisées
- Appliquer les bonnes pratiques de stockage et réseau

## Objectifs techniques

Volumes Docker, bind mounts, networks bridge, communication inter-conteneurs, persistance données, réseaux isolés, monitoring réseau

## Table des matières

1. [Volumes et persistance des données](#1-volumes-et-persistance-des-données)
2. [Réseaux Docker](#2-réseaux-docker)
3. [Communication inter-conteneurs](#3-communication-inter-conteneurs)
4. [Bonnes pratiques production](#4-bonnes-pratiques-production)
5. [Récapitulatif et prochaines étapes](#5-récapitulatif-et-prochaines-étapes)
6. [Ressources complémentaires](#6-ressources-complémentaires)

---

## 1. Volumes et persistance des données

### 1.1 Définitions et concepts fondamentaux

#### Qu'est-ce que la persistance dans Docker ?

**Définition** : La persistance des données est la capacité de conserver les données au-delà du cycle de vie d'un conteneur. Par défaut, les données créées dans un conteneur sont temporaires et disparaissent à sa suppression.

**Problématique** : Les conteneurs sont par nature éphémères (ephemeral). Toute modification du système de fichiers d'un conteneur est perdue lors de sa suppression.

#### Types de stockage Docker

Docker propose trois mécanismes de persistance :

**1. Volumes (Recommandé)**

- Stockage géré par Docker
- Indépendant du système de fichiers hôte
- Partageable entre conteneurs
- Sauvegardable et portable

**2. Bind mounts**

- Montage direct d'un répertoire hôte
- Accès complet au système de fichiers hôte
- Dépendant de la structure de l'hôte
- Utilisé pour le développement

**3. tmpfs mounts (Linux uniquement)**

- Stockage en mémoire temporaire
- Très rapide, non persistant
- Données sensibles temporaires

#### Diagramme architectural des types de stockage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOCKER HOST                                    │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   VOLUMES       │    │  BIND MOUNTS    │    │   TMPFS         │         │
│  │                 │    │                 │    │                 │         │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │         │
│  │ │Docker Volume│ │    │ │Host Directory│ │    │ │   Memory    │ │         │
│  │ │   Storage   │ │    │ │ /host/path  │ │    │ │   Storage   │ │         │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │         │
│  │       │         │    │       │         │    │       │         │         │
│  └───────┼─────────┘    └───────┼─────────┘    └───────┼─────────┘         │
│          │                      │                      │                   │
│  ┌───────┼─────────┐    ┌───────┼─────────┐    ┌───────┼─────────┐         │
│  │   CONTAINER 1   │    │   CONTAINER 2   │    │   CONTAINER 3   │         │
│  │                 │    │                 │    │                 │         │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │         │
│  │ │/app/data    │ │    │ │/app/config  │ │    │ │/tmp/cache   │ │         │
│  │ │(Persistent) │ │    │ │(Host sync)  │ │    │ │(Temporary)  │ │         │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

LÉGENDE:
- Volumes : Gérés par Docker, indépendants du filesystem hôte
- Bind Mounts : Montage direct depuis le système hôte
- tmpfs : Stockage temporaire en mémoire (Linux uniquement)
```

#### Cas d'usage par type de stockage

**Volumes Docker - Cas d'usage production :**

- Bases de données (PostgreSQL, MongoDB, MySQL)
- Stockage de fichiers applicatifs
- Logs d'application persistants
- Données de configuration partagées

**Bind Mounts - Cas d'usage développement :**

- Code source en cours de développement
- Fichiers de configuration dynamiques
- Partage de ressources hôte
- Outils de debugging

**tmpfs - Cas d'usage performance :**

- Cache applicatif temporaire
- Données sensibles (mots de passe, tokens)
- Stockage temporaire haute performance
- Session stores

### 1.1.1 Démonstration comparative : Persistance vs Éphémère

#### Démonstration 1 : Données éphémères (comportement par défaut)

```bash
echo "=== DÉMO 1: Conteneur sans volume (données éphémères) ==="

# Créer un conteneur et écrire des données
echo "1. Création d'un conteneur avec données temporaires..."
docker run --name demo-ephemere alpine sh -c "
    echo 'Données importantes' > /tmp/fichier.txt
    echo 'Configuration app' > /tmp/config.json
    ls -la /tmp/
    echo 'Contenu fichier:' && cat /tmp/fichier.txt
"

# Arrêter et redémarrer le conteneur
echo "2. Redémarrage du conteneur..."
docker restart demo-ephemere

# Vérifier que les données sont perdues
echo "3. Vérification des données après redémarrage..."
docker exec demo-ephemere sh -c "
    echo 'Contenu du répertoire /tmp après redémarrage:'
    ls -la /tmp/
    echo 'Tentative de lecture du fichier:'
    cat /tmp/fichier.txt 2>/dev/null || echo 'FICHIER PERDU!'
"

# Nettoyage
docker rm -f demo-ephemere
```

#### Démonstration 2 : Données persistantes avec volumes

```bash
echo "=== DÉMO 2: Conteneur avec volume (données persistantes) ==="

# Créer un volume dédié
echo "1. Création d'un volume Docker..."
docker volume create demo-persist

# Créer un conteneur avec volume monté
echo "2. Création d'un conteneur avec volume persistant..."
docker run --name demo-persist -v demo-persist:/data alpine sh -c "
    echo 'Données importantes' > /data/fichier.txt
    echo 'Configuration app' > /data/config.json
    echo '{\"version\": \"1.0\", \"env\": \"prod\"}' > /data/app-config.json
    ls -la /data/
    echo 'Contenu fichier:' && cat /data/fichier.txt
"

# Arrêter et redémarrer le conteneur
echo "3. Redémarrage du conteneur..."
docker restart demo-persist

# Vérifier que les données sont conservées
echo "4. Vérification des données après redémarrage..."
docker exec demo-persist sh -c "
    echo 'Contenu du répertoire /data après redémarrage:'
    ls -la /data/
    echo 'Contenu du fichier (CONSERVÉ):'
    cat /data/fichier.txt
    echo 'Configuration JSON:'
    cat /data/app-config.json
"

# Supprimer le conteneur mais garder le volume
echo "5. Suppression du conteneur (volume conservé)..."
docker rm -f demo-persist

# Créer un nouveau conteneur avec le même volume
echo "6. Nouveau conteneur avec le même volume..."
docker run --name demo-persist-2 -v demo-persist:/data alpine sh -c "
    echo 'Données toujours présentes dans le nouveau conteneur:'
    ls -la /data/
    cat /data/fichier.txt
    echo 'Ajout de nouvelles données...'
    echo 'Nouvelle entrée' >> /data/fichier.txt
    cat /data/fichier.txt
"

# Nettoyage
docker rm -f demo-persist-2
docker volume rm demo-persist
```

#### Démonstration 3 : Comparaison des performances

```bash
echo "=== DÉMO 3: Comparaison des performances par type de stockage ==="

# Test performance bind mount
echo "1. Test bind mount (répertoire hôte)..."
mkdir -p /tmp/demo-bind
time docker run --rm -v /tmp/demo-bind:/test alpine sh -c "
    for i in \$(seq 1 1000); do
        echo 'Test data line \$i' >> /test/performance.txt
    done
"

# Test performance volume Docker
echo "2. Test volume Docker..."
docker volume create demo-perf
time docker run --rm -v demo-perf:/test alpine sh -c "
    for i in \$(seq 1 1000); do
        echo 'Test data line \$i' >> /test/performance.txt
    done
"

# Test performance tmpfs
echo "3. Test tmpfs (mémoire)..."
time docker run --rm --tmpfs /test alpine sh -c "
    for i in \$(seq 1 1000); do
        echo 'Test data line \$i' >> /test/performance.txt
    done
"

# Nettoyage
rm -rf /tmp/demo-bind
docker volume rm demo-perf
```

### 1.1.3 Troubleshooting et bonnes pratiques

#### Problèmes courants et solutions

**1. Volume non monté correctement**

```bash
# Diagnostic
docker volume ls | grep mon_volume
docker volume inspect mon_volume
docker inspect mon_conteneur | grep -A 10 "Mounts"

# Solutions
# - Vérifier que le volume existe
# - Contrôler la syntaxe de montage
# - Vérifier les permissions
```

**2. Espace disque insuffisant**

```bash
# Diagnostic complet
docker system df
docker system df -v
df -h /var/lib/docker

# Nettoyage sélectif
docker volume prune --filter "until=24h"
docker system prune --volumes
```

**3. Performances dégradées**

```bash
# Test de performance I/O
docker run --rm -v mon_volume:/test alpine sh -c "
    dd if=/dev/zero of=/test/testfile bs=1M count=100
    sync
    dd if=/test/testfile of=/dev/null bs=1M
"

# Optimisation
# - Utiliser des SSD pour les volumes critiques
# - Configurer le bon driver de stockage
# - Éviter les bind mounts pour la production
```

### 1.2 Gestion des volumes Docker

#### Commandes essentielles

```bash
# Créer un volume
docker volume create mon_volume

# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect mon_volume

# Supprimer un volume
docker volume rm mon_volume

# Nettoyer les volumes non utilisés
docker volume prune
```

#### Utilisation avec les conteneurs

```bash
# Monter un volume nommé
docker run -v mon_volume:/data nginx

# Monter un bind mount
docker run -v /host/path:/container/path nginx

# Monter en lecture seule
docker run -v mon_volume:/data:ro nginx

# Monter un tmpfs
docker run --tmpfs /tmp nginx
```

📝 **LAB 1** - Configuration volumes et persistance : `S2_S1_S3_lab1_volumes_persistance.sh`

**Énoncé du LAB 1** :

Créer une infrastructure de base de données PostgreSQL avec persistance des données et sauvegarde automatique.

- **Objectif** : Maîtriser les volumes Docker pour la persistance
- **Contexte** : Base de données pour application DevOps
- **Instructions** :

  1. Créer un volume dédié pour PostgreSQL
  2. Déployer PostgreSQL avec le volume monté
  3. Insérer des données de test
  4. Vérifier la persistance après redémarrage du conteneur
  5. Implémenter une stratégie de sauvegarde

- **Critères d'évaluation** :

  - Volume créé et configuré (2 points)
  - PostgreSQL fonctionnel avec persistance (3 points)
  - Données conservées après redémarrage (2 points)
  - Stratégie de sauvegarde documentée (1 point)

- **Durée estimée** : 20 minutes
- **Points** : 8/30
- **Fichier de travail** : `S2_S1_S3_lab1_volumes_persistance.sh`

---

## 2. Réseaux Docker

### 2.1 Architecture réseau Docker

#### Concepts fondamentaux

**Définition** : Les réseaux Docker permettent aux conteneurs de communiquer entre eux et avec l'extérieur de manière isolée et sécurisée.

#### Architecture réseau Docker

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOCKER HOST                                    │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │  BRIDGE (par    │    │   HOST NETWORK  │    │   NONE NETWORK  │         │
│  │   défaut)       │    │                 │    │                 │         │
│  │                 │    │ ┌─────────────┐ │    │ ┌─────────────┐ │         │
│  │ ┌─────────────┐ │    │ │  Container  │ │    │ │  Container  │ │         │
│  │ │  Container  │ │    │ │   (direct   │ │    │ │  (isolé)    │ │         │
│  │ │   (NAT)     │ │    │ │   host net) │ │    │ │             │ │         │
│  │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │         │
│  │       │         │    │                 │    │                 │         │
│  └───────┼─────────┘    └─────────────────┘    └─────────────────┘         │
│          │                                                                  │
│  ┌───────┼──────────────────────────────────────────────────────────────┐  │
│  │       │                    RÉSEAU HÔTE                               │  │
│  │   ┌───▼───┐                                                          │  │
│  │   │ NAT   │          ┌─────────────────┐                             │  │
│  │   │Bridge │          │   Interface     │                             │  │
│  │   └───────┘          │   Réseau Hôte   │                             │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Types de réseaux Docker - Progression pédagogique

Docker fournit **trois types de réseaux fondamentaux** installés par défaut, plus des **réseaux personnalisés** que vous pouvez créer :

##### **Niveau 1 : Réseaux par défaut (installés automatiquement)**

**1. Bridge (par défaut)**

```bash
# Réseau utilisé automatiquement si aucun n'est spécifié
docker run nginx
```

- **Usage** : Développement et applications simples
- **Isolation** : Conteneurs isolés de l'hôte mais peuvent communiquer entre eux
- **Communication externe** : Via NAT (Network Address Translation)
- **Résolution DNS** : Par adresse IP uniquement
- **Plage d'adresses** : 172.17.0.0/16 (par défaut)

**Communication hôte ↔ conteneur dans le réseau bridge :**

```bash
# Démonstration de la communication hôte-conteneur
docker run -d --name web-test -p 8080:80 nginx

# ✓ L'hôte PEUT communiquer avec le conteneur via :
# 1. Port mapping (recommandé) :
curl http://localhost:8080

# 2. Adresse IP directe du conteneur :
CONTAINER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-test)
curl http://$CONTAINER_IP

# ✓ Le conteneur PEUT communiquer avec l'hôte via :
# - L'IP de la passerelle (172.17.0.1 par défaut)
# - L'host spécial "host.docker.internal" (sur Windows/Mac)
docker exec web-test ping host.docker.internal

# Nettoyage
docker stop web-test && docker rm web-test
```

**Important** : Dans le réseau bridge par défaut, la communication bidirectionnelle hôte-conteneur est **possible** mais nécessite soit un port mapping, soit la connaissance de l'IP du conteneur.

**2. Host**

```bash
# Conteneur utilise directement le réseau de l'hôte
docker run --network=host nginx
```

- **Usage** : Applications nécessitant de hautes performances réseau
- **Isolation** : Aucune (partage le réseau de l'hôte)
- **Communication externe** : Directe (même IP que l'hôte)
- **Sécurité** : Risque plus élevé (accès direct au réseau hôte)

**Explication technique : Host vs Bridge**

**Mode Host - "Pas d'isolation réseau"**

```bash
# Le conteneur hérite de TOUTES les interfaces réseau de l'hôte
docker run --network=host alpine ip addr show
# Résultat : Même sortie que 'ip addr show' sur l'hôte !

# Pas besoin de port mapping - le conteneur écoute directement sur l'hôte
docker run --network=host nginx  # Nginx écoute sur l'IP de l'hôte:80
curl http://localhost  # Accès direct, pas de NAT
```

**Mode Bridge - "Isolation avec pont réseau"**

```bash
# Le conteneur a sa propre interface eth0 dans un réseau privé
docker run alpine ip addr show
# Résultat : Interface eth0 avec IP 172.17.x.x (différente de l'hôte)

# Port mapping nécessaire pour l'accès externe
docker run -p 8080:80 nginx  # NAT : hôte:8080 → conteneur:80
curl http://localhost:8080   # Accès via translation d'adresse
```

**Comparaison technique :**

| Aspect                      | Mode Host               | Mode Bridge               |
| --------------------------- | ----------------------- | ------------------------- |
| **Namespace réseau**        | Partagé avec l'hôte     | Isolé (nouveau namespace) |
| **Interfaces réseau**       | Toutes celles de l'hôte | eth0 dans réseau privé    |
| **Adresse IP**              | Même que l'hôte         | 172.17.x.x (par défaut)   |
| **Port binding**            | Direct sur l'hôte       | Via NAT (port mapping)    |
| **Performance**             | Maximale (pas de NAT)   | Légère surcharge (NAT)    |
| **Isolation**               | Aucune                  | Complète                  |
| **Accès aux services hôte** | Direct                  | Via passerelle 172.17.0.1 |

**Démonstration pratique - Comparaison des adresses IP :**

```bash
echo "=== COMPARAISON DES ADRESSES IP HOST vs BRIDGE ==="

# D'abord, voyons l'IP de votre machine hôte
echo "IP de la machine hôte :"
hostname -I  # Linux
# ou ipconfig | findstr "IPv4"  # Windows

# 1. Mode Bridge (par défaut) - IP DIFFÉRENTE
echo "1. Mode Bridge - Le conteneur a sa PROPRE IP :"
docker run --rm alpine sh -c "ip addr show eth0 | grep 'inet '"
# Sortie : inet 172.17.0.x/16 (IP PRIVÉE différente de l'hôte)

# 2. Mode Host - MÊME IP que l'hôte
echo "2. Mode Host - Le conteneur utilise l'IP de l'HÔTE :"
docker run --rm --network=host alpine sh -c "ip addr show | grep 'inet ' | head -3"
# Sortie : EXACTEMENT les mêmes IPs que votre machine !

# Preuve concrète avec un test nginx :
echo "3. Test pratique avec nginx :"

# Bridge : Nginx dans un réseau privé
docker run -d --name nginx-bridge -p 8080:80 nginx
echo "Bridge - nginx accessible via : http://localhost:8080"
BRIDGE_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nginx-bridge)
echo "IP privée du conteneur bridge : $BRIDGE_IP (172.17.x.x)"

# Host : Nginx directement sur l'IP de l'hôte
docker run -d --name nginx-host --network=host nginx
echo "Host - nginx accessible via : http://localhost (port 80 de l'hôte)"
echo "IP du conteneur host : IDENTIQUE à celle de votre machine"

# Vérification
echo "Vérification :"
echo "- Bridge container IP: $BRIDGE_IP"
echo "- Host container: utilise directement l'IP de votre machine"

# Nettoyage
docker stop nginx-bridge nginx-host
docker rm nginx-bridge nginx-host
```

**Résultat attendu :**

- **Conteneur Bridge** : IP = 172.17.0.2 (réseau privé Docker)
- **Conteneur Host** : IP = **Votre IP machine** (ex: 192.168.1.100, 10.0.0.5, etc.)

**Points clés à retenir :**

1. **Mode Host** = Conteneur a la **MÊME IP** que votre machine hôte
2. **Mode Bridge** = Conteneur a une **IP privée** 172.17.x.x
3. **Pas de 172.17.x.x** en mode Host !
4. **Accès direct** en mode Host (pas de port mapping nécessaire)

```bash
echo "2. Mode Host :"
docker run --rm --network=host alpine sh -c "ip addr show | grep 'inet ' | head -3"
# Sortie : Mêmes IPs que l'hôte !

# 3. Test de performance
echo "3. Test de latence :"

# Bridge (avec NAT)
time docker run --rm -p 8080:80 nginx curl http://localhost:8080

# Host (direct)
time docker run --rm --network=host nginx curl http://localhost:80
```

**Cas d'usage typiques :**

- **Mode Host** : Bases de données haute performance, monitoring réseau, applications legacy
- **Mode Bridge** : Applications web, microservices, développement, production sécurisée

**3. None**

```bash
# Conteneur sans accès réseau
docker run --network=none alpine
```

- **Usage** : Traitement de données isolé, sécurité maximale
- **Isolation** : Complète (aucun accès réseau)
- **Communication externe** : Impossible
- **Sécurité** : Maximale

##### **Niveau 2 : Réseaux personnalisés (créés manuellement)**

**4. Bridge personnalisé (recommandé pour la production)**

```bash
# Création d'un réseau bridge personnalisé
docker network create mon-app-network
docker run --network=mon-app-network --name web nginx
docker run --network=mon-app-network --name db postgres
```

- **Usage** : Applications multi-conteneurs en production
- **Isolation** : Conteneurs isolés par projet
- **Communication externe** : Via NAT configuré
- **Résolution DNS** : Automatique par nom de conteneur

##### **Niveau 3 : Réseaux avancés (orchestration)**

**5. Overlay (Docker Swarm/multi-hôtes)**

```bash
# Pour clusters Docker Swarm
docker network create --driver overlay mon-cluster-network
```

- **Usage** : Applications distribuées sur plusieurs serveurs
- **Isolation** : Entre clusters et services
- **Communication externe** : Routage inter-serveurs
- **Chiffrement** : Communication sécurisée entre nœuds

#### Tableau comparatif des réseaux

| Type                | Isolation | Performance | DNS               | Communication hôte    | Usage typique        | Complexité    |
| ------------------- | --------- | ----------- | ----------------- | --------------------- | -------------------- | ------------- |
| Bridge (défaut)     | Faible    | Moyen       | IP uniquement     | Via port mapping/IP   | Développement        | Simple        |
| Host                | Non       | Maximum     | Hôte              | Directe (même réseau) | Performance critique | Simple        |
| None                | Maximum   | N/A         | Aucun             | Impossible            | Sécurité maximale    | Simple        |
| Bridge personnalisé | Élevée    | Moyen       | Nom + IP          | Via port mapping/IP   | Production           | Intermédiaire |
| Overlay             | Élevée    | Faible      | Service discovery | Via configuration     | Multi-serveurs       | Avancé        |

#### Démonstration pratique des types de réseaux

```bash
echo "=== DÉMONSTRATION : Comparaison des types de réseaux ==="

# 1. Test du réseau bridge par défaut
echo "1. Réseau bridge par défaut :"
docker run --rm --name test-bridge alpine ip addr show eth0
docker run --rm alpine ping -c 2 test-bridge 2>/dev/null || echo "Communication par nom impossible"

# 2. Test du réseau host
echo "2. Réseau host (même IP que l'hôte) :"
docker run --rm --network=host alpine ip addr show | grep "inet " | head -3

# 3. Test du réseau none
echo "3. Réseau none (aucune interface) :"
docker run --rm --network=none alpine ip addr show || echo "Seule interface loopback disponible"

# 4. Test du réseau bridge personnalisé
echo "4. Réseau bridge personnalisé avec DNS :"
docker network create demo-network
docker run -d --name app1 --network=demo-network alpine sleep 30
docker run --rm --network=demo-network alpine ping -c 2 app1
echo "Oui Communication par nom réussie !"

# Nettoyage
docker stop app1 && docker rm app1
docker network rm demo-network
```

#### Troubleshooting : Problèmes de communication réseau courants

**Problème 1 : Impossible de communiquer avec le conteneur via son IP (curl/ping échoue)**

```bash
# Symptômes observés :
CONTAINER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-test)
echo $CONTAINER_IP  # Affiche : 172.17.0.2
curl http://$CONTAINER_IP  # ÉCHOUE : Failed to connect
ping 172.17.0.1  # ÉCHOUE : ping vers la passerelle
```

**Causes possibles et solutions :**

**1. Docker Desktop (Windows/Mac) - Isolation réseau**

```bash
# CAUSE : Docker Desktop isole les conteneurs du réseau de l'hôte
# SOLUTION : Utiliser le port mapping obligatoirement
docker run -d --name web-test -p 8080:80 nginx
curl http://localhost:8080  # ✓ FONCTIONNE

# Alternative : Accéder depuis un autre conteneur
docker run --rm alpine ping 172.17.0.2  # ✓ FONCTIONNE entre conteneurs
```

**2. Service non démarré dans le conteneur**

```bash
# DIAGNOSTIC : Vérifier que le service écoute
docker exec web-test netstat -tuln
docker exec web-test curl http://localhost  # Test depuis l'intérieur

# SOLUTION : S'assurer que l'application écoute sur 0.0.0.0:80
docker logs web-test  # Vérifier les logs de démarrage
```

**3. Firewall de l'hôte**

```bash
# DIAGNOSTIC : Tester la connectivité réseau
docker exec web-test ip route  # Vérifier les routes
docker exec web-test ping 8.8.8.8  # Test internet depuis le conteneur

# SOLUTION Linux : Configurer iptables/firewalld
sudo iptables -I DOCKER-USER -s 172.17.0.0/16 -j ACCEPT
```

**4. Configuration Docker incorrecte**

```bash
# DIAGNOSTIC : Vérifier la configuration réseau Docker
docker network inspect bridge
docker info | grep -i "bridge\|network"

# SOLUTION : Redémarrer Docker si nécessaire
sudo systemctl restart docker  # Linux
# ou redémarrer Docker Desktop (Windows/Mac)
```

**Méthode de diagnostic complète :**

```bash
#!/bin/bash
echo "=== DIAGNOSTIC RÉSEAU DOCKER ==="

# 1. Informations de base
echo "1. Conteneurs en cours :"
docker ps

# 2. Réseaux disponibles
echo "2. Réseaux Docker :"
docker network ls

# 3. Test de connectivité entre conteneurs
echo "3. Test communication entre conteneurs :"
docker run -d --name test-server nginx
CONTAINER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-server)
echo "IP du conteneur : $CONTAINER_IP"

# Test depuis un autre conteneur (devrait fonctionner)
docker run --rm alpine ping -c 2 $CONTAINER_IP && echo "✓ Ping entre conteneurs OK" || echo "✗ Ping entre conteneurs ÉCHOUÉ"

# Test depuis l'hôte (peut échouer sur Docker Desktop)
ping -c 2 $CONTAINER_IP && echo "✓ Ping depuis hôte OK" || echo "✗ Ping depuis hôte ÉCHOUÉ (normal sur Docker Desktop)"

# 4. Test avec port mapping
docker stop test-server && docker rm test-server
docker run -d --name test-server -p 8080:80 nginx
curl -s http://localhost:8080 && echo "✓ Accès via port mapping OK" || echo "✗ Accès via port mapping ÉCHOUÉ"

# Nettoyage
docker stop test-server && docker rm test-server
```

**Bonnes pratiques pour éviter ces problèmes :**

1. **Toujours utiliser le port mapping** pour l'accès depuis l'hôte
2. **Utiliser des réseaux bridge personnalisés** pour la communication entre conteneurs
3. **Tester la connectivité progressivement** : conteneur → conteneur → hôte → externe
4. **Vérifier les logs** en cas de problème de démarrage de service

### 2.2 Gestion des réseaux

#### Commandes essentielles

```bash
# Lister les réseaux
docker network ls

# Créer un réseau bridge personnalisé
docker network create mon_reseau

# Inspecter un réseau
docker network inspect mon_reseau

# Connecter un conteneur à un réseau
docker network connect mon_reseau mon_conteneur

# Déconnecter un conteneur
docker network disconnect mon_reseau mon_conteneur

# Supprimer un réseau
docker network rm mon_reseau
```

#### Configuration réseau avancée

```bash
# Créer un réseau avec sous-réseau spécifique
docker network create --subnet=172.20.0.0/16 --ip-range=172.20.240.0/20 mon_reseau_custom

# Déployer avec IP fixe
docker run --network mon_reseau_custom --ip 172.20.240.5 nginx

# Publier des ports spécifiques
docker run -p 8080:80 -p 8443:443 nginx
```

### 2.3 Application pratique - Réseaux

📝 **LAB 2** - Réseaux et communication multi-conteneurs : `S2_S1_S3_lab2_networks_communication.yml`

**Énoncé du LAB 2** :

Déployer une architecture 3-tiers avec réseau isolé : frontend Nginx, backend Node.js, base de données PostgreSQL.

- **Objectif** : Maîtriser les réseaux Docker et communications
- **Contexte** : Architecture microservices sécurisée
- **Instructions** :

  1. Créer deux réseaux : frontend et backend
  2. Déployer PostgreSQL sur le réseau backend uniquement
  3. Déployer Node.js connecté aux deux réseaux
  4. Déployer Nginx sur le réseau frontend uniquement
  5. Configurer la communication complète
  6. Vérifier l'isolation réseau

- **Critères d'évaluation** :

  - Réseaux créés et configurés (2 points)
  - Architecture 3-tiers fonctionnelle (4 points)
  - Communication entre services (2 points)
  - Isolation réseau respectée (2 points)

- **Durée estimée** : 25 minutes
- **Points** : 10/30
- **Fichier de travail** : `S2_S1_S3_lab2_networks_communication.yml`

---

## 3. Communication inter-conteneurs

### 3.1 Mécanismes de communication

#### Résolution DNS automatique

Dans un réseau bridge personnalisé, Docker fournit une résolution DNS automatique grâce à un serveur DNS intégré qui mappe automatiquement les noms de conteneurs vers leurs adresses IP.

##### Fonctionnement technique du DNS Docker

**Architecture du système DNS intégré :**

```
┌─────────────────────────────────────────────────────────────────┐
│                    RÉSEAU BRIDGE PERSONNALISÉ                  │
│                         app_network                            │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   Container A   │    │   Container B   │    │ DNS SERVER   │ │
│  │  "database"     │    │     "api"       │    │ (dockerd)    │ │
│  │  IP: 172.18.0.2 │    │  IP: 172.18.0.3 │    │ IP: 127.0.0.11│ │
│  │                 │    │                 │    │              │ │
│  │  /etc/resolv.conf│    │  /etc/resolv.conf│    │ Résolution:  │ │
│  │  nameserver     │    │  nameserver     │    │ database →   │ │
│  │  127.0.0.11     │    │  127.0.0.11     │    │ 172.18.0.2   │ │
│  └─────────────────┘    └─────────────────┘    │ api →        │ │
│           │                       │            │ 172.18.0.3   │ │
│           └───────────────────────┼────────────┘              │ │
│                                   │                           │ │
│                        ┌──────────▼──────────┐                │ │
│                        │    Requête DNS      │                │ │
│                        │  "ping database"    │                │ │
│                        │  Résolu vers:       │                │ │
│                        │  172.18.0.2         │                │ │
│                        └─────────────────────┘                │ │
└─────────────────────────────────────────────────────────────────┘
```

**Mécanisme technique détaillé :**

1. **Serveur DNS intégré (dockerd)** :

   - Docker daemon exécute un serveur DNS sur l'IP `127.0.0.11:53`
   - Chaque conteneur a automatiquement `nameserver 127.0.0.11` dans `/etc/resolv.conf`
   - Le serveur DNS maintient une table de correspondance nom ↔ IP

2. **Enregistrement automatique** :

   - Lors de la création d'un conteneur, Docker enregistre automatiquement :
     - Nom du conteneur → IP du conteneur
     - Alias du réseau → IP du conteneur (si spécifié)
   - Mise à jour en temps réel lors des changements d'IP

3. **Résolution DNS** :
   - Requête DNS depuis un conteneur : `ping database`
   - Le conteneur interroge `127.0.0.11:53`
   - Docker daemon résout le nom vers l'IP correspondante
   - Réponse renvoyée au conteneur demandeur

**Démonstration technique complète :**

```bash
echo "=== FONCTIONNEMENT TECHNIQUE DU DNS DOCKER ==="

# 1. Créer un réseau bridge personnalisé
docker network create --driver bridge app_network

# 2. Déployer des conteneurs avec noms spécifiques
docker run -d --name database --network app_network \
  -e POSTGRES_PASSWORD=demo123 \
  -e POSTGRES_DB=appdb \
  postgres:13
docker run -d --name api --network app_network nginx
docker run -d --name cache --network app_network redis:6

# 3. Vérifier la configuration DNS dans un conteneur
echo "Configuration DNS du conteneur :"
docker exec api cat /etc/resolv.conf
# Sortie attendue :
# nameserver 127.0.0.11
# options ndots:0

# 4. Tester la résolution DNS
echo "Test de résolution DNS :"
docker exec api nslookup database
# Sortie : database résolu vers l'IP 172.18.0.x

docker exec api nslookup cache
# Sortie : cache résolu vers l'IP 172.18.0.y

# 5. Vérifier les adresses IP réelles
echo "Correspondance réelle nom → IP :"
docker inspect -f '{{.Name}} → {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' database api cache

# 6. Test de communication effective
echo "Test de communication inter-conteneurs :"
docker exec api ping -c 2 database
docker exec api ping -c 2 cache
docker exec database ping -c 2 api

# 7. Analyse du trafic DNS (optionnel)
echo "Analyse des requêtes DNS :"
docker exec api sh -c "nslookup database && echo 'DNS query successful'"

# Nettoyage
docker stop database api cache
docker rm database api cache
docker network rm app_network
```

#### Approche interactive : Travailler directement dans les conteneurs

**Pour une expérience plus pratique, vous pouvez entrer directement dans les conteneurs :**

```bash
echo "=== DÉMONSTRATION INTERACTIVE ==="

# 1. Créer l'environnement
docker network create --driver bridge demo_network
docker run -d --name database --network demo_network \
  -e POSTGRES_PASSWORD=demo123 \
  -e POSTGRES_DB=testdb \
  postgres:13
docker run -d --name api --network demo_network nginx

# 2. Entrer dans le conteneur api de manière interactive
echo "Entrons dans le conteneur api pour travailler interactivement..."
docker exec -it api bash

# Une fois dans le conteneur, exécutez les commandes suivantes :
# (Ces commandes sont à taper manuellement dans le terminal du conteneur)
```

**Commandes à exécuter dans le conteneur api :**

```bash
# Installation des outils réseau (dans le conteneur)
apt update && apt install -y dnsutils iputils-ping curl

# Vérification de la configuration DNS
cat /etc/resolv.conf

# Test de résolution DNS
nslookup database
nslookup cache  # Devrait échouer (conteneur n'existe pas)

# Test de connectivité
ping -c 3 database

# Test de connexion aux services
curl -I http://database:5432  # Devrait échouer (PostgreSQL n'est pas HTTP)

# Exploration de l'environnement réseau
ip addr show
ip route show
cat /etc/hosts

# Sortir du conteneur
exit
```

**Script de nettoyage :**

```bash
# Nettoyage après la démonstration
docker stop database api
docker rm database api
docker network rm demo_network
```

**Avantages de l'approche interactive :**

- **Exploration libre** : Possibilité de tester différentes commandes
- **Apprentissage par la pratique** : Compréhension immédiate des résultats
- **Debugging en temps réel** : Résolution des problèmes au fur et à mesure
- **Flexibilité** : Adaptation aux questions des étudiants

#### Troubleshooting : Configuration PostgreSQL

**Problème courant** : Erreur `Database is uninitialized and superuser password is not specified`

**Cause** : PostgreSQL nécessite une configuration d'authentification lors du premier démarrage.

**Solutions** :

```bash
# Solution 1 : Avec mot de passe (Recommandé pour production)
docker run -d --name database --network app_network \
  -e POSTGRES_PASSWORD=monmotdepasse \
  postgres:13

# Solution 2 : Configuration complète
docker run -d --name database --network app_network \
  -e POSTGRES_PASSWORD=demo123 \
  -e POSTGRES_USER=appuser \
  -e POSTGRES_DB=appdb \
  postgres:13

# Solution 3 : Mode trust (UNIQUEMENT pour développement/tests)
docker run -d --name database --network app_network \
  -e POSTGRES_HOST_AUTH_METHOD=trust \
  postgres:13

# Test de connexion
docker exec -it database psql -U postgres -d postgres
# Ou avec utilisateur personnalisé :
docker exec -it database psql -U appuser -d appdb
```

**Variables d'environnement PostgreSQL importantes :**

- `POSTGRES_PASSWORD` : Mot de passe pour l'utilisateur postgres (requis)
- `POSTGRES_USER` : Nom d'utilisateur personnalisé (optionnel)
- `POSTGRES_DB` : Nom de la base de données à créer (optionnel)
- `POSTGRES_HOST_AUTH_METHOD=trust` : Accepte toutes connexions sans mot de passe (non sécurisé)

**Différences importantes avec le réseau bridge par défaut :**

| Aspect                 | Bridge par défaut  | Bridge personnalisé  |
| ---------------------- | ------------------ | -------------------- |
| **Serveur DNS**        | Pas de serveur DNS | Serveur DNS intégré  |
| **Résolution par nom** | IP uniquement      | Nom + IP             |
| **Communication**      | Via IP ou --link   | Via nom de conteneur |
| **Isolation**          | Faible             | Forte (par réseau)   |
| **Service Discovery**  | Manuel             | Automatique          |

**Limitations et considérations :**

- **Réseau par défaut** : Pas de résolution DNS automatique
- **Conteneurs externes** : Seuls les conteneurs du même réseau sont résolvables
- **Performance** : Légère latence supplémentaire pour la résolution DNS
- **Cache DNS** : Docker maintient un cache pour optimiser les performances

**Exemple pratique d'usage :**

```bash
# Les conteneurs peuvent se contacter par nom
docker network create app_network
docker run --name database --network app_network postgres
docker run --name api --network app_network -e DB_HOST=database node_app
```

**Dans le conteneur `api`, l'application peut directement utiliser :**

```javascript
// Code JavaScript dans le conteneur api
const dbConnection = `postgresql://user:pass@database:5432/mydb`;
// 'database' sera automatiquement résolu vers l'IP du conteneur PostgreSQL
```

#### Variables d'environnement

Communication via configuration :

```bash
# Passage d'informations de connexion
docker run --name api \
  -e DB_HOST=database \
  -e DB_PORT=5432 \
  -e DB_NAME=app_db \
  --network app_network \
  node_app
```

### 3.2 Patterns de communication

#### Service Discovery

**Pattern 1 : DNS-based**

- Utilisation des noms de conteneurs
- Résolution automatique par Docker
- Simple et efficace pour la plupart des cas

**Pattern 2 : Environment-based**

- Configuration via variables d'environnement
- Flexibilité de configuration
- Compatible avec les outils d'orchestration

#### Load Balancing

```bash
# Plusieurs instances d'un même service
docker run --name api1 --network app_network node_app
docker run --name api2 --network app_network node_app
docker run --name api3 --network app_network node_app

# Load balancer nginx
docker run --name lb --network app_network -p 80:80 nginx_lb
```

### 3.3 Application pratique - Communication complète

📝 **LAB 3** - Application complète avec persistance et réseau : `S2_S1_S3_lab3_app_complete.yml`

**Énoncé du LAB 3** :

Déployer une application web complète avec monitoring : frontend React, API REST, base de données, cache Redis, monitoring Prometheus.

- **Objectif** : Intégrer volumes, réseaux et communications
- **Contexte** : Application production-ready avec observabilité
- **Instructions** :

  1. Créer l'architecture réseau multi-tiers
  2. Configurer la persistance pour base de données et metrics
  3. Déployer tous les services avec leurs volumes
  4. Configurer la communication entre tous les composants
  5. Implémenter le monitoring avec Prometheus
  6. Tester la résilience (arrêt/redémarrage services)
  7. Valider la persistance et la communication

- **Critères d'évaluation** :

  - Architecture réseau complète (3 points)
  - Persistance configurée sur tous services (3 points)
  - Communication inter-services fonctionnelle (3 points)
  - Monitoring opérationnel (2 points)
  - Tests de résilience réussis (1 point)

- **Durée estimée** : 35 minutes
- **Points** : 12/30
- **Fichier de travail** : `S2_S1_S3_lab3_app_complete.yml`

---

## 4. Bonnes pratiques production

### 4.1 Sécurité des volumes

#### Permissions et ownership

```bash
# Créer un volume avec utilisateur spécifique
docker run --user 1001:1001 -v mon_volume:/data app

# Vérifier les permissions
docker run --rm -v mon_volume:/data alpine ls -la /data
```

#### Chiffrement des données

- Utilisation de volumes chiffrés au niveau de l'hôte
- Chiffrement en transit pour les communications
- Gestion sécurisée des secrets

### 4.2 Performance et optimisation

#### Choix du type de stockage

**Volumes** : Pour la production et données applicatives
**Bind mounts** : Pour le développement et fichiers de configuration
**tmpfs** : Pour données temporaires et cache

#### Optimisation réseau

```bash
# Réseau avec MTU optimisé
docker network create --opt com.docker.network.driver.mtu=1500 optimized_net

# Limitation de bande passante (avec tc sur l'hôte)
# Monitoring des performances réseau
```

### 4.3 Monitoring et observabilité

#### Surveillance des volumes

```bash
# Espace disque des volumes
docker system df

# Détails par volume
docker volume inspect mon_volume

# Nettoyage automatique
docker volume prune -f
```

#### Monitoring réseau

```bash
# Statistiques réseau des conteneurs
docker stats

# Inspection du trafic réseau
docker exec conteneur netstat -i

# Logs réseau
docker logs conteneur | grep -i network
```

---

## 5. Récapitulatif et prochaines étapes

### Points clés de la séance

**Volumes Docker**

- Trois types : volumes, bind mounts, tmpfs
- Volumes recommandés pour la production
- Gestion du cycle de vie indépendante des conteneurs

**Réseaux Docker**

- Isolation par défaut avec communication contrôlée
- Réseaux bridge personnalisés pour la résolution DNS
- Architecture multi-tiers avec séparation des préoccupations

**Communication inter-conteneurs**

- Service discovery via DNS automatique
- Configuration via variables d'environnement
- Patterns de haute disponibilité

### Préparation séance suivante

La **Séance 4 - Production et Optimisation** s'appuiera sur ces concepts pour :

- Optimisation avancée des conteneurs
- Sécurité renforcée en production
- Monitoring et observabilité
- Déploiement à grande échelle

### Validation des acquis

- Maîtrise des volumes pour la persistance
- Configuration de réseaux isolés et sécurisés
- Communication efficace entre microservices
- Application des bonnes pratiques de production

---

## 6. Ressources complémentaires

### Documentation officielle

- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Docker Networks](https://docs.docker.com/network/)
- [Docker Storage Best Practices](https://docs.docker.com/storage/)

### Outils et extensions

- **Portainer** : Interface graphique pour volumes et réseaux
- **Docker Desktop** : Visualisation des ressources
- **Dive** : Analyse des layers et volumes

### Lectures approfondies

- Patterns de persistance pour microservices
- Sécurité des réseaux containerisés
- Performance tuning Docker storage drivers

---

_Formateur : Hassan ESSADIK | Sprint 2 - Semaine 1 - Séance 3_
