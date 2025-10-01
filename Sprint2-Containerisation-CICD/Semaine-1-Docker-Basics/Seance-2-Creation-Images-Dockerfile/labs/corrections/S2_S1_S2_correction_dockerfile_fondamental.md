# CORRECTION LAB 1 - Dockerfile fondamental et optimisation

## Informations générales

- **Sprint** : 2 - Containerisation et CI/CD
- **Semaine** : 1 - Docker Basics
- **Séance** : 2 - Dockerfile Creation
- **Correction** : LAB 1 - Dockerfile fondamental
- **Formateur** : Hassan ESSADIK

## Solution complète

### Structure finale

```
lab1-dockerfile/
├── app.py                 ✓ Application Flask complète
├── requirements.txt       ✓ Dépendances spécifiées
├── Dockerfile            ✓ Optimisé pour cache
├── .dockerignore         ✓ Fichiers exclus
├── docker-compose.yml    ✓ Orchestration simple
└── ANALYSE.md           ✓ Documentation des résultats
```

### 1. Application Flask (app.py)

```python
from flask import Flask, jsonify
import os
import platform
import psutil
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint principal avec informations système"""
    return jsonify({
        "message": "Flask API - LAB 1 Dockerfile Optimisé",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "architecture": platform.architecture()[0]
    })

@app.route('/health')
def health():
    """Health check endpoint pour monitoring"""
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "memory_usage": f"{memory.percent}%",
                "memory_available": f"{memory.available // (1024**2)}MB",
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "disk_usage": f"{disk.percent}%"
            },
            "process": {
                "pid": os.getpid(),
                "memory_rss": f"{psutil.Process().memory_info().rss // (1024**2)}MB"
            }
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/env')
def env():
    """Endpoint pour variables d'environnement"""
    return jsonify({
        "environment": os.getenv('FLASK_ENV', 'production'),
        "debug": os.getenv('FLASK_DEBUG', 'False'),
        "port": os.getenv('PORT', '5000'),
        "worker_class": os.getenv('WORKER_CLASS', 'sync'),
        "workers": os.getenv('WORKERS', '1'),
        "timezone": os.getenv('TZ', 'UTC')
    })

@app.route('/api/status')
def api_status():
    """Status de l'API avec métriques"""
    return jsonify({
        "api": "Flask LAB1",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "environment": "/env",
            "metrics": "/api/status"
        },
        "uptime": psutil.boot_time()
    })

@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    return jsonify({
        "error": "Route not found",
        "message": "The requested resource was not found on this server",
        "available_routes": ["/", "/health", "/env", "/api/status"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Gestionnaire d'erreur 500"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on the server"
    }), 500

if __name__ == '__main__':
    # Configuration pour le développement
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
```

### 2. Dependencies (requirements.txt)

```txt
# Framework web
Flask==2.3.3

# Monitoring système
psutil==5.9.5

# Serveur WSGI pour production
gunicorn==21.2.0

# Utilitaires
python-dotenv==1.0.0
```

### 3. Dockerfile optimisé

```dockerfile
# Utilisation d'une image de base légère
FROM python:3.11-slim AS base

# Métadonnées
LABEL maintainer="hassan.essadik@simplon.ma"
LABEL version="1.0.0"
LABEL description="Flask API optimisée - LAB 1"

# Variables d'environnement pour optimisation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installation des dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# ===== OPTIMISATION DU CACHE =====
# Copie des dépendances en premier (couche stable)
COPY requirements.txt .

# Installation des dépendances Python (mise en cache si requirements.txt inchangé)
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code application (couche fréquemment modifiée)
COPY app.py .

# Configuration de l'environnement
ENV FLASK_ENV=production \
    PORT=5000 \
    WORKERS=2 \
    WORKER_CLASS=sync \
    TIMEOUT=30

# Création d'un utilisateur non-root pour la sécurité
RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

# Exposition du port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Commande par défaut avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
```

### 4. Exclusions (.dockerignore)

```dockerignore
# Git
.git
.gitignore

# Documentation
README.md
ANALYSE.md
*.md

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
venv/
env/
.venv/
.env

# Logs
*.log
logs/

# Docker
Dockerfile*
.dockerignore
docker-compose*.yml

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
```

### 5. Orchestration (docker-compose.yml)

```yaml
version: '3.8'

services:
  flask-app:
    build:
      context: .
      dockerfile: Dockerfile
    image: flask-lab1:optimized
    container_name: flask-lab1
    ports:
      - '5000:5000'
    environment:
      - FLASK_ENV=production
      - PORT=5000
      - WORKERS=2
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:5000/health']
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
    networks:
      - flask-network

  # Service de monitoring (optionnel)
  monitoring:
    image: prom/prometheus:latest
    container_name: flask-monitoring
    ports:
      - '9090:9090'
    networks:
      - flask-network
    depends_on:
      - flask-app

networks:
  flask-network:
    driver: bridge
```

## Démonstration de l'optimisation

### Tests de performance du cache

```bash
#!/bin/bash
# test-optimization.sh

echo "=== DÉMONSTRATION OPTIMISATION CACHE ==="

# Premier build complet
echo "1. Premier build (complet)..."
time docker build -t flask-lab1:v1 .

# Modification du code seulement
echo -e "\n2. Modification du code application..."
echo "# Version modifiée $(date)" >> app.py

# Second build avec cache
echo -e "\n3. Second build (avec cache)..."
time docker build -t flask-lab1:v2 .

# Restauration du fichier
git checkout app.py 2>/dev/null || true

echo -e "\n=== ANALYSE DES RÉSULTATS ==="
docker images | grep flask-lab1
```

### Script de test complet

```bash
#!/bin/bash
# comprehensive-test.sh

echo "=== TESTS COMPLETS FLASK LAB 1 ==="

# Build de l'image
docker build -t flask-lab1:test .

# Démarrage du conteneur
docker run -d -p 5000:5000 --name flask-test flask-lab1:test

# Attendre le démarrage
sleep 5

echo "1. Test endpoint principal..."
curl -s http://localhost:5000/ | jq

echo -e "\n2. Test health check..."
curl -s http://localhost:5000/health | jq

echo -e "\n3. Test variables d'environnement..."
curl -s http://localhost:5000/env | jq

echo -e "\n4. Test status API..."
curl -s http://localhost:5000/api/status | jq

echo -e "\n5. Test endpoint inexistant..."
curl -s http://localhost:5000/nonexistent | jq

echo -e "\n6. Vérification des logs..."
docker logs flask-test | tail -10

echo -e "\n7. Health check Docker..."
docker inspect flask-test | jq '.[0].State.Health'

# Nettoyage
docker stop flask-test && docker rm flask-test

echo -e "\n=== TESTS TERMINÉS ==="
```

## Analyse des résultats (ANALYSE.md)

````markdown
# Analyse des optimisations - LAB 1

## Comparaison des tailles d'images

| Version              | Taille | Optimisation                |
| -------------------- | ------ | --------------------------- |
| python:3.11          | ~880MB | Image de base non optimisée |
| python:3.11-slim     | ~45MB  | Image de base optimisée     |
| flask-lab1:v1        | ~120MB | Première version            |
| flask-lab1:optimized | ~85MB  | Version finale optimisée    |

## Performance du cache

### Premier build (complet)

- Temps: ~2m30s
- Toutes les couches construites

### Second build (code modifié)

- Temps: ~15s
- Cache utilisé pour requirements.txt
- Seule la couche application reconstruite

## Optimisations appliquées

### 1. Image de base

- **Avant**: `python:3.11` (880MB)
- **Après**: `python:3.11-slim` (45MB)
- **Gain**: 95% de réduction

### 2. Ordre des instructions

```dockerfile
# AVANT (non optimisé)
COPY . .
RUN pip install -r requirements.txt

# APRÈS (optimisé)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
```
````

### 3. Variables d'environnement Python

```dockerfile
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1
```

### 4. Nettoyage système

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Sécurité appliquée

1. **Utilisateur non-root**
2. **Health check intégré**
3. **Exclusion de fichiers sensibles** (.dockerignore)
4. **Variables d'environnement sécurisées**

## Recommandations

1. **Cache optimization**: Toujours copier les dépendances avant le code
2. **Multi-stage**: Pour des applications plus complexes
3. **Distroless**: Pour une sécurité maximale
4. **Monitoring**: Intégrer des métriques dès le début

````

## Barème de correction

### Fonctionnalité (3/8 points)

- ✅ **3/3** - Application Flask complète avec tous endpoints
- ✅ **Bonus** - Gestion d'erreurs et logging

### Optimisation (3/8 points)

- ✅ **2/2** - Ordre des instructions optimisé
- ✅ **1/1** - Variables d'environnement configurées
- ✅ **Bonus** - Image de base slim utilisée

### Analyse (2/8 points)

- ✅ **1/1** - Comparaison avant/après documentée
- ✅ **1/1** - Tests de cache réalisés
- ✅ **Bonus** - Scripts d'automatisation

## Points d'attention pour l'évaluation

### Erreurs courantes à éviter

1. **Cache non optimisé**
```dockerfile
# ❌ MAUVAIS
COPY . .
RUN pip install -r requirements.txt

# ✅ CORRECT
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
````

2. **Image de base inappropriée**

```dockerfile
# ❌ TROP LOURD
FROM python:3.11

# ✅ OPTIMISÉ
FROM python:3.11-slim
```

3. **Manque de nettoyage**

```dockerfile
# ❌ CACHE NON NETTOYÉ
RUN apt-get update
RUN apt-get install curl

# ✅ NETTOYAGE INTÉGRÉ
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
```

### Critères d'excellence

1. **Health check fonctionnel**
2. **Logs structurés**
3. **Gestion d'erreurs robuste**
4. **Documentation complète**
5. **Tests automatisés**

---

**Note pédagogique** : Cette correction démontre l'importance de l'optimisation du cache et de la sélection de l'image de base pour les performances et la taille finale.
