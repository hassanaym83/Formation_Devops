# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 1 - Séance 3 : Volumes et Networks Docker

# 📝 LAB 2 - Réseaux et communication multi-conteneurs

**Fichier de travail** : `S2_S1_S3_lab2_networks_communication.yml`  
**Durée estimée** : 25 minutes  
**Points** : 10/30  
**Objectif** : Maîtriser les réseaux Docker et communications inter-conteneurs

---

## Contexte

Vous devez déployer une architecture 3-tiers sécurisée pour une application web DevOps : frontend Nginx (proxy reverse), backend Node.js (API REST), et base de données PostgreSQL. L'isolation réseau est critique pour la sécurité.

## Architecture cible

```
Internet → [Frontend Network] → Nginx → [Backend Network] → Node.js → PostgreSQL
```

**Isolation** :

- PostgreSQL accessible uniquement depuis Node.js
- Node.js accessible depuis Nginx et PostgreSQL
- Nginx accessible depuis Internet et Node.js

## Prérequis

- Docker et Docker Compose installés
- Port 80 disponible sur l'hôte
- Connaissances des réseaux IP

## Instructions détaillées

### Étape 1 : Création de l'architecture réseau (2 points)

1. **Créer les réseaux personnalisés** :

   ```bash
   # Réseau frontend (Nginx ↔ Node.js)
   docker network create frontend_network --subnet=172.20.0.0/24

   # Réseau backend (Node.js ↔ PostgreSQL)
   docker network create backend_network --subnet=172.21.0.0/24

   # Vérifier la création
   docker network ls | grep -E "(frontend|backend)_network"

   # Inspecter les réseaux
   docker network inspect frontend_network
   docker network inspect backend_network
   ```

2. **Documenter l'architecture** :

   ```bash
   cat > network_architecture.md << 'EOF'
   # Architecture Réseau 3-Tiers

   ## Réseaux
   - frontend_network: 172.20.0.0/24 (Nginx ↔ Node.js)
   - backend_network: 172.21.0.0/24 (Node.js ↔ PostgreSQL)

   ## Isolation
   - PostgreSQL: backend_network uniquement
   - Node.js: frontend_network + backend_network (pont)
   - Nginx: frontend_network uniquement

   ## Flux de communication
   Internet → Nginx (80) → Node.js (3000) → PostgreSQL (5432)
   EOF
   ```

### Étape 2 : Déploiement PostgreSQL (backend uniquement) (4 points)

1. **Déployer PostgreSQL sur réseau backend** :

   ```bash
   # Créer un volume pour PostgreSQL
   docker volume create postgres_lab2_data

   # Déployer PostgreSQL
   docker run -d \
     --name postgres_backend \
     --network backend_network \
     --ip 172.21.0.10 \
     -e POSTGRES_DB=app_database \
     -e POSTGRES_USER=app_user \
     -e POSTGRES_PASSWORD=AppPass123 \
     -v postgres_lab2_data:/var/lib/postgresql/data \
     postgres:13
   ```

2. **Vérifier le déploiement** :

   ```bash
   # Vérifier le conteneur
   docker ps | grep postgres_backend

   # Vérifier l'IP assignée
   docker inspect postgres_backend | grep -A 5 "Networks"

   # Vérifier l'accessibilité depuis le réseau backend
   docker run --rm --network backend_network alpine ping -c 3 postgres_backend
   ```

3. **Créer la structure de base de données** :

   ```bash
   # Créer la table pour l'API
   docker exec postgres_backend psql -U app_user -d app_database << 'EOF'
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   INSERT INTO users (username, email) VALUES
   ('devops_admin', 'admin@devops.local'),
   ('developer_1', 'dev1@devops.local'),
   ('operator_1', 'ops1@devops.local');
   EOF

   # Vérifier les données
   docker exec postgres_backend psql -U app_user -d app_database -c "SELECT * FROM users;"
   ```

### Étape 3 : Déploiement Node.js (pont entre réseaux) (4 points)

1. **Créer l'application Node.js** :

   ```bash
   # Créer le répertoire de l'application
   mkdir -p nodejs_api
   cd nodejs_api

   # Créer package.json
   cat > package.json << 'EOF'
   {
     "name": "devops-api",
     "version": "1.0.0",
     "description": "API REST pour LAB DevOps",
     "main": "server.js",
     "dependencies": {
       "express": "^4.18.0",
       "pg": "^8.8.0"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   EOF

   # Créer l'API REST
   cat > server.js << 'EOF'
   const express = require('express');
   const { Pool } = require('pg');

   const app = express();
   const port = 3000;

   // Configuration PostgreSQL
   const pool = new Pool({
     user: 'app_user',
     host: 'postgres_backend',
     database: 'app_database',
     password: 'AppPass123',
     port: 5432,
   });

   app.use(express.json());

   // Endpoint de santé
   app.get('/health', (req, res) => {
     res.json({ status: 'OK', service: 'DevOps API', timestamp: new Date() });
   });

   // Liste des utilisateurs
   app.get('/api/users', async (req, res) => {
     try {
       const result = await pool.query('SELECT * FROM users ORDER BY id');
       res.json(result.rows);
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   // Créer un utilisateur
   app.post('/api/users', async (req, res) => {
     try {
       const { username, email } = req.body;
       const result = await pool.query(
         'INSERT INTO users (username, email) VALUES ($1, $2) RETURNING *',
         [username, email]
       );
       res.status(201).json(result.rows[0]);
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   app.listen(port, '0.0.0.0', () => {
     console.log(`API DevOps listening on port ${port}`);
   });
   EOF

   # Créer le Dockerfile
   cat > Dockerfile << 'EOF'
   FROM node:16-alpine
   WORKDIR /app
   COPY package.json .
   RUN npm install
   COPY server.js .
   EXPOSE 3000
   CMD ["npm", "start"]
   EOF
   ```

2. **Construire et déployer l'API** :

   ```bash
   # Construire l'image
   docker build -t devops-api:lab2 .

   # Déployer sur les deux réseaux
   docker run -d \
     --name nodejs_api \
     --network backend_network \
     --ip 172.21.0.20 \
     devops-api:lab2

   # Connecter au réseau frontend
   docker network connect frontend_network nodejs_api --ip 172.20.0.20

   # Vérifier les connexions réseau
   docker inspect nodejs_api | grep -A 20 "Networks"
   ```

3. **Tester l'API** :

   ```bash
   # Attendre que l'API soit prête
   sleep 10

   # Tester depuis le réseau backend
   docker run --rm --network backend_network curlimages/curl \
     curl -s http://172.21.0.20:3000/health

   # Tester l'accès aux données
   docker run --rm --network backend_network curlimages/curl \
     curl -s http://172.21.0.20:3000/api/users
   ```

### Étape 4 : Déploiement Nginx (frontend uniquement) (2 points)

1. **Créer la configuration Nginx** :

   ```bash
   cd ..
   mkdir nginx_config

   cat > nginx_config/nginx.conf << 'EOF'
   events {
       worker_connections 1024;
   }

   http {
       upstream api_backend {
           server 172.20.0.20:3000;
       }

       server {
           listen 80;
           server_name localhost;

           # Page d'accueil
           location / {
               return 200 '<!DOCTYPE html>
   <html>
   <head><title>DevOps LAB 2</title></head>
   <body>
   <h1>Architecture 3-Tiers DevOps</h1>
   <p>Frontend Nginx → Backend Node.js → Database PostgreSQL</p>
   <p><a href="/api/users">Voir les utilisateurs</a></p>
   <p><a href="/health">Statut de l\'API</a></p>
   </body>
   </html>';
               add_header Content-Type text/html;
           }

           # Proxy vers l'API
           location /api/ {
               proxy_pass http://api_backend;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
           }

           # Endpoint de santé
           location /health {
               proxy_pass http://api_backend;
           }
       }
   }
   EOF
   ```

2. **Déployer Nginx** :

   ```bash
   # Déployer Nginx sur le réseau frontend uniquement
   docker run -d \
     --name nginx_frontend \
     --network frontend_network \
     --ip 172.20.0.10 \
     -p 80:80 \
     -v $(pwd)/nginx_config/nginx.conf:/etc/nginx/nginx.conf:ro \
     nginx:alpine

   # Vérifier le déploiement
   docker ps | grep nginx_frontend

   # Vérifier l'isolation réseau
   docker inspect nginx_frontend | grep -A 10 "Networks"
   ```

### Étape 5 : Tests de communication et isolation (2 points)

1. **Tester la communication complète** :

   ```bash
   # Test depuis l'extérieur (navigateur simulé)
   curl -s http://localhost/health
   curl -s http://localhost/api/users

   # Test de création d'utilisateur
   curl -X POST http://localhost/api/users \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "email": "test@devops.local"}'

   # Vérifier la création
   curl -s http://localhost/api/users
   ```

2. **Vérifier l'isolation réseau** :

   ```bash
   # PostgreSQL NE DOIT PAS être accessible depuis frontend
   docker run --rm --network frontend_network alpine \
     sh -c "ping -c 1 postgres_backend || echo 'ISOLATION OK: PostgreSQL non accessible depuis frontend'"

   # PostgreSQL accessible depuis backend network
   docker run --rm --network backend_network alpine \
     ping -c 1 postgres_backend

   # Nginx NE DOIT PAS être accessible depuis backend
   docker run --rm --network backend_network alpine \
     sh -c "ping -c 1 nginx_frontend || echo 'ISOLATION OK: Nginx non accessible depuis backend'"

   # Node.js accessible depuis les deux réseaux
   docker run --rm --network frontend_network alpine ping -c 1 172.20.0.20
   docker run --rm --network backend_network alpine ping -c 1 172.21.0.20
   ```

## Validation et critères d'évaluation

### Vérifications attendues

1. **Réseaux créés et configurés (2 points)** :

   ```bash
   # Vérifier l'existence des réseaux
   docker network ls | grep -E "(frontend|backend)_network"

   # Vérifier les sous-réseaux
   docker network inspect frontend_network | grep Subnet
   docker network inspect backend_network | grep Subnet
   ```

2. **Architecture 3-tiers fonctionnelle (4 points)** :

   ```bash
   # Tous les services actifs
   docker ps | grep -E "(postgres_backend|nodejs_api|nginx_frontend)"

   # Test de connectivité bout en bout
   curl -s http://localhost/api/users | jq length
   ```

3. **Communication entre services (2 points)** :

   ```bash
   # API peut accéder à PostgreSQL
   docker exec nodejs_api sh -c "curl -s http://postgres_backend:5432 || echo 'DB accessible'"

   # Nginx peut accéder à l'API
   docker exec nginx_frontend sh -c "curl -s http://172.20.0.20:3000/health"
   ```

4. **Isolation réseau respectée (2 points)** :

   ```bash
   # Tests d'isolation (doivent échouer)
   docker run --rm --network frontend_network alpine \
     sh -c "! ping -c 1 postgres_backend"

   docker run --rm --network backend_network alpine \
     sh -c "! ping -c 1 nginx_frontend"
   ```

## Livrables attendus

- [ ] Fichier `S2_S1_S3_lab2_networks_communication.yml` (Docker Compose)
- [ ] Réseaux frontend et backend configurés
- [ ] Architecture 3-tiers déployée et fonctionnelle
- [ ] Tests d'isolation réseau validés
- [ ] Documentation `network_architecture.md`

## Bonus - Docker Compose

Convertir le déploiement en fichier Docker Compose :

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    container_name: postgres_backend
    networks:
      backend:
        ipv4_address: 172.21.0.10
    environment:
      POSTGRES_DB: app_database
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: AppPass123
    volumes:
      - postgres_lab2_data:/var/lib/postgresql/data

  api:
    build: ./nodejs_api
    container_name: nodejs_api
    networks:
      frontend:
        ipv4_address: 172.20.0.20
      backend:
        ipv4_address: 172.21.0.20
    depends_on:
      - postgres

  nginx:
    image: nginx:alpine
    container_name: nginx_frontend
    networks:
      frontend:
        ipv4_address: 172.20.0.10
    ports:
      - '80:80'
    volumes:
      - ./nginx_config/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api

networks:
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/24

volumes:
  postgres_lab2_data:
```

---

**Sprint 2 - Semaine 1 - Séance 3 - LAB 2**  
_Formateur : Hassan ESSADIK_
