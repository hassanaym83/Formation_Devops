# LAB 1 - Dockerfile fondamental et optimisation

## Informations générales

- **Sprint** : 2 - Containerisation et CI/CD
- **Semaine** : 1 - Docker Basics
- **Séance** : 2 - Dockerfile Creation
- **LAB** : 1/3
- **Durée estimée** : 20 minutes
- **Formateur** : Hassan ESSADIK

## Objectifs pédagogiques

- Maîtriser la syntaxe de base d'un Dockerfile
- Optimiser le cache des couches Docker
- Analyser la taille et les performances d'une image
- Implémenter une application Flask conteneurisée

## Contexte

Vous devez containeriser une API Flask simple en optimisant le processus de build et la taille de l'image finale. Cette API servira de base pour les prochains labs.

## Prérequis techniques

- Docker Desktop installé et fonctionnel
- Éditeur de code (VS Code recommandé)
- Connaissance de base Python/Flask
- Accès internet pour téléchargement d'images

## Instructions

### Étape 1 : Préparation de l'application Flask (5 minutes)

Créez la structure suivante :

```
lab1-dockerfile/
├── app.py
├── requirements.txt
├── Dockerfile
└── .dockerignore
```

**Fichier `app.py`** :

```python
from flask import Flask, jsonify
import os
import platform
import psutil

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Flask API - LAB 1 Dockerfile",
        "status": "running",
        "python_version": platform.python_version(),
        "hostname": platform.node()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "cpu_count": psutil.cpu_count()
    })

@app.route('/env')
def env():
    return jsonify({
        "environment": os.getenv('FLASK_ENV', 'production'),
        "debug": os.getenv('FLASK_DEBUG', 'False'),
        "port": os.getenv('PORT', '5000')
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

**Fichier `requirements.txt`** :

```
Flask==2.3.3
psutil==5.9.5
gunicorn==21.2.0
```

### Étape 2 : Premier Dockerfile (non optimisé) (5 minutes)

Créez un Dockerfile basique :

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

**Tests** :

```bash
# Build de l'image
docker build -t flask-lab1:v1 .

# Analyse de la taille
docker images flask-lab1:v1

# Test de l'application
docker run -p 5000:5000 flask-lab1:v1

# Test des endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

### Étape 3 : Optimisation du cache (5 minutes)

Modifiez le Dockerfile pour optimiser le cache :

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Copie des dépendances en premier (cache stable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code application (cache souvent invalidé)
COPY app.py .

# Configuration
EXPOSE 5000
ENV FLASK_ENV=production
ENV PORT=5000

# Commande avec Gunicorn pour production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Créez `.dockerignore` :

```dockerignore
.git
.gitignore
README.md
Dockerfile
.dockerignore
__pycache__
*.pyc
.pytest_cache
.coverage
.venv
venv/
```

### Étape 4 : Test d'optimisation du cache (5 minutes)

**Test du cache** :

```bash
# Premier build (complet)
time docker build -t flask-lab1:v2 .

# Modification du code seulement (app.py)
# Ajoutez un commentaire dans app.py
echo "# Version 2" >> app.py

# Second build (cache utilisé pour requirements)
time docker build -t flask-lab1:v2 .

# Comparaison des tailles
docker images | grep flask-lab1
```

**Analyse des couches** :

```bash
# Inspection des couches
docker history flask-lab1:v2

# Analyse détaillée
docker inspect flask-lab1:v2
```

## Tests et validations

### Test fonctionnel

```bash
# Lancement du conteneur optimisé
docker run -d -p 5000:5000 --name flask-test flask-lab1:v2

# Tests complets
curl -s http://localhost:5000/ | jq
curl -s http://localhost:5000/health | jq
curl -s http://localhost:5000/env | jq

# Vérification des logs
docker logs flask-test

# Nettoyage
docker stop flask-test && docker rm flask-test
```

### Analyse des performances

```bash
# Comparaison des tailles
echo "=== COMPARAISON DES TAILLES ==="
docker images | grep flask-lab1

# Analyse du temps de build
echo "=== TEMPS DE BUILD ==="
time docker build -t flask-lab1:v3 .
```

## Livrables attendus

### 1. Fichiers sources

- [ ] `app.py` fonctionnel avec tous les endpoints
- [ ] `requirements.txt` avec versions spécifiées
- [ ] `.dockerignore` correctement configuré

### 2. Dockerfile optimisé

- [ ] Image de base appropriée (slim/alpine)
- [ ] Ordre des instructions optimisé pour le cache
- [ ] Variables d'environnement configurées
- [ ] Commande de production (Gunicorn)

### 3. Tests et analyse

- [ ] Application accessible et fonctionnelle
- [ ] Cache optimization démontrée (temps de build)
- [ ] Analyse de taille réalisée et documentée

### 4. Documentation

- [ ] Commandes utilisées documentées
- [ ] Comparaison avant/après optimisation
- [ ] Observations et conclusions

## Critères d'évaluation

**Fonctionnalité** : Application Flask accessible avec tous endpoints
**Optimisation** : Cache correctement optimisé, ordre des instructions
**Analyse** : Comparaison des tailles et temps de build

## Bonus (optionnel)

### Multi-stage build

Implémentez un Dockerfile multi-stage :

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim AS production
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Health check integration

Ajoutez un health check au Dockerfile :

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
```

## Ressources complémentaires

- [Docker Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/dev-best-practices/)
- [Flask deployment with Gunicorn](https://flask.palletsprojects.com/en/2.3.x/deploying/gunicorn/)

## Aide au dépannage

### Problèmes courants

**Port déjà utilisé** :

```bash
# Trouver le processus
netstat -ano | findstr :5000
# Ou changer le port
docker run -p 5001:5000 flask-lab1:v2
```

**Erreur de build** :

```bash
# Nettoyer le cache Docker
docker builder prune
# Rebuild from scratch
docker build --no-cache -t flask-lab1:v2 .
```

**Application non accessible** :

```bash
# Vérifier les logs
docker logs <container_id>
# Vérifier la configuration réseau
docker port <container_id>
```

---

**Note importante** : Documentez toutes vos observations et comparaisons dans un fichier `ANALYSE.md`. Cela vous servira pour les prochains labs et pour comprendre l'impact des optimisations.
