# CORRECTION LAB 1 : Installation et premiers pas Docker

**Sprint 2 - Semaine 1 - Séance 1**  
**Référence** : `S2_S1_S1_lab1_installation_premiers_pas`  
**Durée correction** : 10 minutes  
**Points** : 8/30

## Solution complète et explications

### Phase 1 : Installation Docker Engine (3 points)

#### Ubuntu/Debian - Solution détaillée

```bash
# 1. Préparation système
sudo apt update && sudo apt upgrade -y
uname -r  # Vérifier version kernel (minimum 3.10)

# 2. Installation des prérequis
sudo apt install -y ca-certificates curl gnupg lsb-release

# 3. Ajout clé GPG et repository Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4. Installation Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 5. Configuration post-installation
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# 6. Test après reconnexion
newgrp docker
```

#### Windows - Solution avec Docker Desktop

```powershell
# 1. Vérifier prérequis Windows
# Windows 10 Pro/Enterprise ou Windows 11
Get-WindowsOptionalFeature -FeatureName Microsoft-Hyper-V -Online

# 2. Activer WSL2 si nécessaire
wsl --install
wsl --set-default-version 2

# 3. Télécharger et installer Docker Desktop
# https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

# 4. Vérification post-installation
docker version
docker system info
```

#### Commandes de vérification attendues

```bash
# Sortie attendue pour docker version
Client: Docker Engine - Community
 Version:           20.10.21
 API version:       1.41
 Go version:        go1.18.7
 Git commit:        baeda1f
 Built:             Tue Oct 25 18:01:58 2022
 OS/Arch:           linux/amd64

Server: Docker Engine - Community
 Engine:
  Version:          20.10.21
  API version:      1.41 (minimum version 1.12)
  Go version:       go1.18.7
```

**Points d'évaluation** :

- Installation sans erreur (1 point)
- Service démarré automatiquement (1 point)
- Permissions utilisateur configurées (1 point)

### Phase 2 : Tests fonctionnels avancés (3 points)

#### Solution complète avec explications

```bash
# 1. Test des images
docker pull nginx:alpine
# Sortie: Using default tag: latest
# Status: Downloaded newer image for nginx:alpine

docker pull postgres:13-alpine
docker images
# Doit montrer les 2 images téléchargées

# 2. Test conteneur web
docker run -d --name test-web -p 8080:80 nginx:alpine
# Sortie: ID du conteneur (12 caractères aléatoires)

docker ps
# Doit montrer le conteneur test-web en état "Up"

# Test accessibilité
curl http://localhost:8080
# Sortie: Code HTML de la page par défaut Nginx

# Alternative navigateur
firefox http://localhost:8080  # ou autre navigateur

# 3. Test logs et monitoring
docker logs test-web
# Sortie: Logs de démarrage Nginx + requêtes HTTP

docker stats test-web --no-stream
# Sortie: Utilisation CPU, RAM, réseau, disque

docker exec test-web ps aux
# Sortie: Processus en cours dans le conteneur

# 4. Nettoyage propre
docker stop test-web
docker rm test-web
docker rmi nginx:alpine postgres:13-alpine
docker system df  # Vérifier l'espace libéré
```

**Points d'évaluation** :

- Images téléchargées avec succès (1 point)
- Serveur nginx accessible (1 point)
- Logs et stats récupérées (1 point)

### Phase 3 : Comparaison performance VM vs Conteneur (2 points)

#### Métriques de comparaison

**Temps de démarrage** :

```bash
# Conteneur Ubuntu
time docker run --rm ubuntu:20.04 echo "Conteneur démarré"
# Résultat attendu: 0m2.847s (environ 3 secondes)

# VM Ubuntu (exemple VirtualBox)
# Temps typique: 30-60 secondes pour démarrage complet
```

**Consommation mémoire** :

```bash
# Conteneur Nginx
docker run -d --name resource-test nginx:alpine
docker stats resource-test --no-stream
# Résultat attendu:
# CONTAINER    CPU %   MEM USAGE / LIMIT     MEM %
# resource-test 0.00%   8.5MiB / 15.6GiB     0.05%

# VM Ubuntu typique: 512MB-2GB RAM minimum
```

**Portabilité** :

```bash
# Export image Docker
docker save nginx:alpine > nginx-image.tar
ls -lh nginx-image.tar
# Taille attendue: environ 9-15MB

# VM Ubuntu .ova typique: 1-5GB
```

#### Tableau comparatif attendu

| Métrique        | Machine Virtuelle | Conteneur Docker  | Gain   |
| --------------- | ----------------- | ----------------- | ------ |
| Temps démarrage | 30-60 secondes    | 2-5 secondes      | 85-90% |
| RAM minimum     | 512MB-2GB         | 8-50MB            | 90-95% |
| Taille export   | 1-5GB             | 10-50MB           | 95-98% |
| Densité/serveur | 5-10 VMs          | 50-100 conteneurs | 900%   |

**Points d'évaluation** :

- Mesures effectuées et documentées (1 point)
- Analyse comparative réalisée (1 point)

## Problèmes courants et solutions

### Erreur de permissions

**Problème** :

```
permission denied while trying to connect to the Docker daemon socket
```

**Solution** :

```bash
sudo usermod -aG docker $USER
newgrp docker
# Ou redémarrer la session
```

### Service Docker non démarré

**Problème** :

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution** :

```bash
sudo systemctl start docker
sudo systemctl enable docker
systemctl status docker
```

### Port déjà utilisé

**Problème** :

```
Error starting userland proxy: listen tcp 0.0.0.0:8080: bind: address already in use
```

**Solution** :

```bash
# Identifier le processus
sudo netstat -tulpn | grep :8080
sudo lsof -i :8080

# Utiliser un autre port
docker run -d -p 8081:80 nginx:alpine
```

### Problème de réseau Windows

**Problème** : Nginx non accessible depuis Windows

**Solution** :

```bash
# Vérifier IP Docker Desktop
docker inspect test-web | grep IPAddress

# Tester depuis WSL2
curl http://172.17.0.2:80

# Utiliser localhost avec port mapping
docker run -d -p 127.0.0.1:8080:80 nginx:alpine
```

## Optimisations et bonnes pratiques

### Configuration daemon.json

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ]
}
```

### Script d'installation automatisé

```bash
#!/bin/bash
# install-docker.sh

set -e

echo "Installation Docker Engine - Script automatisé"

# Détection OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
fi

case $OS in
    "Ubuntu"|"Debian GNU/Linux")
        echo "Installation sur $OS $VER"

        # Prérequis
        sudo apt update
        sudo apt install -y ca-certificates curl gnupg lsb-release

        # Repository Docker
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        # Installation
        sudo apt update
        sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        ;;
    "CentOS Linux"|"Red Hat Enterprise Linux")
        echo "Installation sur $OS $VER"

        sudo yum install -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        ;;
    *)
        echo "OS non supporté: $OS"
        exit 1
        ;;
esac

# Configuration post-installation
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

echo "Installation terminée. Redémarrez votre session pour utiliser Docker sans sudo."
echo "Test: docker run hello-world"
```

## Tests de validation finale

### Script de validation automatisé

```bash
#!/bin/bash
# validate-docker-install.sh

echo "=== Validation installation Docker ==="

# Test 1: Docker daemon
if docker version > /dev/null 2>&1; then
    echo "✓ Docker daemon accessible"
else
    echo "✗ Docker daemon non accessible"
    exit 1
fi

# Test 2: Pull image
if docker pull hello-world > /dev/null 2>&1; then
    echo "✓ Pull d'image fonctionnel"
else
    echo "✗ Problème de pull d'image"
    exit 1
fi

# Test 3: Run conteneur
if docker run --rm hello-world > /dev/null 2>&1; then
    echo "✓ Exécution de conteneur fonctionnelle"
else
    echo "✗ Problème d'exécution de conteneur"
    exit 1
fi

# Test 4: Permissions utilisateur
if groups $USER | grep -q docker; then
    echo "✓ Utilisateur dans le groupe docker"
else
    echo "⚠ Utilisateur pas dans le groupe docker (sudo requis)"
fi

# Test 5: Storage driver
DRIVER=$(docker system info | grep "Storage Driver" | awk '{print $3}')
if [[ "$DRIVER" == "overlay2" ]]; then
    echo "✓ Storage driver optimal (overlay2)"
else
    echo "⚠ Storage driver: $DRIVER (overlay2 recommandé)"
fi

echo "=== Validation terminée ==="
```

## Ressources pour aller plus loin

### Documentation avancée

- **Docker Best Practices** : https://docs.docker.com/develop/dev-best-practices/
- **Production Deployment** : https://docs.docker.com/engine/security/
- **Performance Tuning** : https://docs.docker.com/config/containers/resource_constraints/

### Outils complémentaires

```bash
# Installation d'outils DevOps
docker pull portainer/portainer-ce  # Interface graphique
docker pull aquasec/trivy          # Security scanning
docker pull wagoodman/dive         # Analyse des couches
```

### Prochaines étapes

1. **Dockerfile** : Création d'images personnalisées
2. **Docker Compose** : Orchestration multi-conteneurs
3. **Volumes** : Persistance des données
4. **Networks** : Communication inter-conteneurs
5. **Security** : Sécurisation des déploiements

---

**Correction réalisée par** : Hassan ESSADIK  
**Durée de correction** : 10 minutes  
**Validation** : Installation Docker opérationnelle pour développement
