# Simplon Maghreb - Formation DevOps

# Sprint 2 - Semaine 1 - Séance 3 : Volumes et Networks Docker

# 📝 LAB 3 - Application complète avec persistance et réseau

**Fichier de travail** : `S2_S1_S3_lab3_app_complete.yml`  
**Durée estimée** : 35 minutes  
**Points** : 12/30  
**Objectif** : Intégrer volumes, réseaux et communications dans une architecture production-ready

---

## Contexte

Vous devez déployer une application web complète avec monitoring pour une équipe DevOps. L'architecture doit être résiliente, observable et prête pour la production avec persistance des données et séparation des préoccupations réseau.

## Architecture cible

```
Internet → Load Balancer → [Frontend] → React App
                             ↓
                        [API Network] → Express API → [Backend] → PostgreSQL
                             ↓                           ↓
                        Redis Cache ← [Cache Network] ←  ↓
                             ↓                           ↓
                        [Monitoring] → Prometheus → [Metrics Storage]
```

**Services déployés** :

- **Frontend** : React (Nginx) + Load Balancer
- **Backend** : Express.js API REST
- **Database** : PostgreSQL avec persistance
- **Cache** : Redis pour performances
- **Monitoring** : Prometheus + Node Exporter

## Prérequis

- Docker et Docker Compose installés
- Ports 80, 3000, 5432, 6379, 9090 disponibles
- 4GB RAM disponible pour tous les services

## Instructions détaillées

### Étape 1 : Architecture réseau multi-tiers (3 points)

1. **Créer l'architecture réseau complète** :

   ```bash
   # Créer tous les réseaux nécessaires
   docker network create frontend_network --subnet=172.18.0.0/24
   docker network create api_network --subnet=172.19.0.0/24
   docker network create backend_network --subnet=172.20.0.0/24
   docker network create cache_network --subnet=172.21.0.0/24
   docker network create monitoring_network --subnet=172.22.0.0/24

   # Vérifier la création
   docker network ls | grep -E "(frontend|api|backend|cache|monitoring)_network"
   ```

2. **Documenter l'architecture complète** :

   ```bash
   cat > architecture_complete.md << 'EOF'
   # Architecture Application Complète DevOps

   ## Réseaux et isolation
   - frontend_network (172.18.0.0/24): Load Balancer ↔ React
   - api_network (172.19.0.0/24): React ↔ Express API
   - backend_network (172.20.0.0/24): Express ↔ PostgreSQL
   - cache_network (172.21.0.0/24): Express ↔ Redis
   - monitoring_network (172.22.0.0/24): All services ↔ Prometheus

   ## Services et connectivité
   - PostgreSQL: backend_network + monitoring_network
   - Redis: cache_network + monitoring_network
   - Express API: api_network + backend_network + cache_network + monitoring_network
   - React/Nginx: frontend_network + api_network + monitoring_network
   - Load Balancer: frontend_network (point d'entrée)
   - Prometheus: monitoring_network (collecte métriques)

   ## Ports exposés
   - 80: Load Balancer (entrée publique)
   - 9090: Prometheus (interface monitoring)

   ## Volumes persistants
   - postgres_data: Base de données
   - redis_data: Cache Redis
   - prometheus_data: Métriques historiques
   EOF
   ```

### Étape 2 : Persistance pour tous services (3 points)

1. **Créer tous les volumes nécessaires** :

   ```bash
   # Volumes pour la persistance des données
   docker volume create postgres_lab3_data
   docker volume create redis_lab3_data
   docker volume create prometheus_lab3_data

   # Vérifier la création
   docker volume ls | grep lab3_data

   # Inspecter les volumes
   docker volume inspect postgres_lab3_data
   docker volume inspect redis_lab3_data
   docker volume inspect prometheus_lab3_data
   ```

2. **Créer la structure de données PostgreSQL** :

   ```bash
   mkdir -p database_init

   cat > database_init/init.sql << 'EOF'
   CREATE DATABASE devops_app;
   \c devops_app;

   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) UNIQUE NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       role VARCHAR(20) DEFAULT 'user',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       last_login TIMESTAMP
   );

   CREATE TABLE projects (
       id SERIAL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       description TEXT,
       status VARCHAR(20) DEFAULT 'active',
       owner_id INTEGER REFERENCES users(id),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE deployments (
       id SERIAL PRIMARY KEY,
       project_id INTEGER REFERENCES projects(id),
       version VARCHAR(50) NOT NULL,
       environment VARCHAR(20) NOT NULL,
       status VARCHAR(20) DEFAULT 'pending',
       deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Données de test
   INSERT INTO users (username, email, role) VALUES
   ('admin', 'admin@devops.local', 'admin'),
   ('dev1', 'dev1@devops.local', 'developer'),
   ('ops1', 'ops1@devops.local', 'operator'),
   ('dev2', 'dev2@devops.local', 'developer');

   INSERT INTO projects (name, description, owner_id) VALUES
   ('Frontend App', 'Application React pour le dashboard', 1),
   ('API Backend', 'API REST pour les services DevOps', 2),
   ('Monitoring Stack', 'Infrastructure de monitoring Prometheus', 3),
   ('CI/CD Pipeline', 'Pipeline automatisé de déploiement', 1);

   INSERT INTO deployments (project_id, version, environment, status) VALUES
   (1, 'v1.0.0', 'production', 'deployed'),
   (1, 'v1.1.0', 'staging', 'deployed'),
   (2, 'v2.0.0', 'production', 'deployed'),
   (2, 'v2.1.0', 'staging', 'pending'),
   (3, 'v1.0.0', 'production', 'deployed'),
   (4, 'v1.0.0', 'development', 'failed');
   EOF
   ```

3. **Déployer PostgreSQL avec persistance** :

   ```bash
   docker run -d \
     --name postgres_app \
     --network backend_network \
     --ip 172.20.0.10 \
     -e POSTGRES_DB=postgres \
     -e POSTGRES_USER=devops_user \
     -e POSTGRES_PASSWORD=DevOpsPass123 \
     -v postgres_lab3_data:/var/lib/postgresql/data \
     -v $(pwd)/database_init:/docker-entrypoint-initdb.d \
     postgres:13

   # Connecter au monitoring
   docker network connect monitoring_network postgres_app --ip 172.22.0.10

   # Attendre l'initialisation et vérifier
   sleep 15
   docker exec postgres_app psql -U devops_user -d devops_app -c "SELECT COUNT(*) FROM users;"
   ```

### Étape 3 : Déploiement de tous les services (3 points)

1. **Déployer Redis avec persistance** :

   ```bash
   docker run -d \
     --name redis_cache \
     --network cache_network \
     --ip 172.21.0.10 \
     -v redis_lab3_data:/data \
     redis:alpine redis-server --save 60 1 --loglevel warning

   # Connecter au monitoring
   docker network connect monitoring_network redis_cache --ip 172.22.0.20

   # Tester Redis
   docker exec redis_cache redis-cli ping
   ```

2. **Créer l'API Express.js avancée** :

   ```bash
   mkdir -p express_api
   cd express_api

   cat > package.json << 'EOF'
   {
     "name": "devops-api-complete",
     "version": "2.0.0",
     "description": "API DevOps avec cache Redis et métriques",
     "main": "server.js",
     "dependencies": {
       "express": "^4.18.0",
       "pg": "^8.8.0",
       "redis": "^4.3.0",
       "prom-client": "^14.0.0",
       "cors": "^2.8.5"
     },
     "scripts": {
       "start": "node server.js"
     }
   }
   EOF

   cat > server.js << 'EOF'
   const express = require('express');
   const { Pool } = require('pg');
   const redis = require('redis');
   const client = require('prom-client');
   const cors = require('cors');

   const app = express();
   const port = 3000;

   // Métriques Prometheus
   const collectDefaultMetrics = client.collectDefaultMetrics;
   collectDefaultMetrics({ timeout: 5000 });

   const httpRequestsTotal = new client.Counter({
     name: 'http_requests_total',
     help: 'Total number of HTTP requests',
     labelNames: ['method', 'route', 'status']
   });

   const httpRequestDuration = new client.Histogram({
     name: 'http_request_duration_seconds',
     help: 'HTTP request duration in seconds',
     labelNames: ['method', 'route']
   });

   // Configuration PostgreSQL
   const pool = new Pool({
     user: 'devops_user',
     host: 'postgres_app',
     database: 'devops_app',
     password: 'DevOpsPass123',
     port: 5432,
   });

   // Configuration Redis
   const redisClient = redis.createClient({
     host: 'redis_cache',
     port: 6379
   });

   redisClient.connect();

   app.use(cors());
   app.use(express.json());

   // Middleware pour métriques
   app.use((req, res, next) => {
     const startTime = Date.now();

     res.on('finish', () => {
       const duration = (Date.now() - startTime) / 1000;
       httpRequestsTotal.inc({
         method: req.method,
         route: req.route?.path || req.path,
         status: res.statusCode
       });
       httpRequestDuration.observe({
         method: req.method,
         route: req.route?.path || req.path
       }, duration);
     });

     next();
   });

   // Endpoints
   app.get('/health', (req, res) => {
     res.json({
       status: 'OK',
       service: 'DevOps API Complete',
       version: '2.0.0',
       timestamp: new Date(),
       uptime: process.uptime()
     });
   });

   app.get('/metrics', async (req, res) => {
     res.set('Content-Type', client.register.contentType);
     res.end(await client.register.metrics());
   });

   app.get('/api/users', async (req, res) => {
     try {
       const cached = await redisClient.get('users');
       if (cached) {
         return res.json({ data: JSON.parse(cached), source: 'cache' });
       }

       const result = await pool.query('SELECT id, username, email, role, created_at FROM users ORDER BY id');
       await redisClient.setEx('users', 300, JSON.stringify(result.rows));
       res.json({ data: result.rows, source: 'database' });
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   app.get('/api/projects', async (req, res) => {
     try {
       const result = await pool.query(`
         SELECT p.*, u.username as owner_name
         FROM projects p
         LEFT JOIN users u ON p.owner_id = u.id
         ORDER BY p.id
       `);
       res.json(result.rows);
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   app.get('/api/deployments', async (req, res) => {
     try {
       const result = await pool.query(`
         SELECT d.*, p.name as project_name
         FROM deployments d
         LEFT JOIN projects p ON d.project_id = p.id
         ORDER BY d.deployed_at DESC
       `);
       res.json(result.rows);
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   app.get('/api/stats', async (req, res) => {
     try {
       const users = await pool.query('SELECT COUNT(*) FROM users');
       const projects = await pool.query('SELECT COUNT(*) FROM projects');
       const deployments = await pool.query('SELECT COUNT(*) FROM deployments');
       const recent = await pool.query('SELECT COUNT(*) FROM deployments WHERE deployed_at > NOW() - INTERVAL \'24 hours\'');

       res.json({
         users: parseInt(users.rows[0].count),
         projects: parseInt(projects.rows[0].count),
         deployments: parseInt(deployments.rows[0].count),
         recent_deployments: parseInt(recent.rows[0].count)
       });
     } catch (err) {
       res.status(500).json({ error: err.message });
     }
   });

   app.listen(port, '0.0.0.0', () => {
     console.log(`DevOps API Complete listening on port ${port}`);
   });
   EOF

   cat > Dockerfile << 'EOF'
   FROM node:16-alpine
   WORKDIR /app
   COPY package.json .
   RUN npm install
   COPY server.js .
   EXPOSE 3000
   CMD ["npm", "start"]
   EOF

   # Construire l'image
   docker build -t devops-api-complete:lab3 .
   cd ..
   ```

3. **Déployer l'API avec toutes les connexions** :

   ```bash
   docker run -d \
     --name express_api \
     --network api_network \
     --ip 172.19.0.20 \
     devops-api-complete:lab3

   # Connecter à tous les réseaux nécessaires
   docker network connect backend_network express_api --ip 172.20.0.20
   docker network connect cache_network express_api --ip 172.21.0.20
   docker network connect monitoring_network express_api --ip 172.22.0.30

   # Attendre et tester
   sleep 10
   docker run --rm --network api_network curlimages/curl \
     curl -s http://172.19.0.20:3000/health
   ```

### Étape 4 : Frontend et Load Balancer (3 points)

1. **Créer l'application React simple** :

   ```bash
   mkdir -p react_frontend

   cat > react_frontend/index.html << 'EOF'
   <!DOCTYPE html>
   <html lang="fr">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>DevOps Dashboard</title>
       <style>
           body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
           .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
           .card { background: white; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; }
           .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
           .stat { text-align: center; padding: 20px; background: #007bff; color: white; border-radius: 8px; }
           .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
           .btn:hover { background: #0056b3; }
           #output { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 4px; padding: 15px; margin: 10px 0; max-height: 400px; overflow-y: auto; }
           .error { color: #dc3545; }
           .success { color: #28a745; }
       </style>
   </head>
   <body>
       <div class="container">
           <h1>🚀 DevOps Dashboard - LAB 3</h1>
           <div class="card">
               <h2>Statistiques de la plateforme</h2>
               <div id="stats" class="stats">
                   <div class="stat">
                       <h3 id="users-count">-</h3>
                       <p>Utilisateurs</p>
                   </div>
                   <div class="stat">
                       <h3 id="projects-count">-</h3>
                       <p>Projets</p>
                   </div>
                   <div class="stat">
                       <h3 id="deployments-count">-</h3>
                       <p>Déploiements</p>
                   </div>
                   <div class="stat">
                       <h3 id="recent-count">-</h3>
                       <p>Récents (24h)</p>
                   </div>
               </div>
           </div>

           <div class="card">
               <h2>Actions disponibles</h2>
               <button class="btn" onclick="loadUsers()">Charger Utilisateurs</button>
               <button class="btn" onclick="loadProjects()">Charger Projets</button>
               <button class="btn" onclick="loadDeployments()">Charger Déploiements</button>
               <button class="btn" onclick="checkHealth()">Vérifier Santé API</button>
               <button class="btn" onclick="loadStats()">Actualiser Stats</button>
           </div>

           <div class="card">
               <h2>Résultats</h2>
               <div id="output">Cliquez sur une action pour voir les résultats...</div>
           </div>
       </div>

       <script>
           const API_BASE = '/api';

           function displayResult(data, title) {
               const output = document.getElementById('output');
               output.innerHTML = `<h3>${title}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
           }

           function displayError(error, title) {
               const output = document.getElementById('output');
               output.innerHTML = `<h3 class="error">${title}</h3><p class="error">${error}</p>`;
           }

           async function apiCall(endpoint, title) {
               try {
                   const response = await fetch(endpoint);
                   if (!response.ok) throw new Error(`HTTP ${response.status}`);
                   const data = await response.json();
                   displayResult(data, title);
                   return data;
               } catch (error) {
                   displayError(error.message, `Erreur - ${title}`);
                   throw error;
               }
           }

           function loadUsers() {
               apiCall('/api/users', 'Utilisateurs');
           }

           function loadProjects() {
               apiCall('/api/projects', 'Projets');
           }

           function loadDeployments() {
               apiCall('/api/deployments', 'Déploiements');
           }

           function checkHealth() {
               apiCall('/health', 'État de santé API');
           }

           async function loadStats() {
               try {
                   const stats = await apiCall('/api/stats', 'Statistiques actualisées');
                   document.getElementById('users-count').textContent = stats.users;
                   document.getElementById('projects-count').textContent = stats.projects;
                   document.getElementById('deployments-count').textContent = stats.deployments;
                   document.getElementById('recent-count').textContent = stats.recent_deployments;
               } catch (error) {
                   console.error('Erreur lors du chargement des stats:', error);
               }
           }

           // Charger les stats au démarrage
           window.addEventListener('DOMContentLoaded', loadStats);
       </script>
   </body>
   </html>
   EOF
   ```

2. **Créer le Load Balancer Nginx** :

   ```bash
   mkdir -p nginx_complete

   cat > nginx_complete/nginx.conf << 'EOF'
   events {
       worker_connections 1024;
   }

   http {
       upstream api_servers {
           server 172.19.0.20:3000;
           # Pour la haute disponibilité, ajouter d'autres instances
           # server 172.19.0.21:3000;
       }

       upstream frontend_servers {
           server 172.18.0.20:80;
       }

       # Configuration de log
       log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                       '$status $body_bytes_sent "$http_referer" '
                       '"$http_user_agent" "$http_x_forwarded_for"';

       server {
           listen 80;
           server_name localhost;
           access_log /var/log/nginx/access.log main;

           # Servir les fichiers statiques
           location / {
               proxy_pass http://frontend_servers;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           }

           # Proxy vers l'API
           location /api/ {
               proxy_pass http://api_servers;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

               # Headers pour WebSocket si nécessaire
               proxy_http_version 1.1;
               proxy_set_header Upgrade $http_upgrade;
               proxy_set_header Connection "upgrade";
           }

           # Health check et métriques
           location /health {
               proxy_pass http://api_servers;
           }

           location /metrics {
               proxy_pass http://api_servers;
           }

           # Status Nginx
           location /nginx_status {
               stub_status on;
               access_log off;
               allow 172.18.0.0/24;
               deny all;
           }
       }
   }
   EOF
   ```

3. **Déployer Frontend et Load Balancer** :

   ```bash
   # Déployer le serveur web frontend
   docker run -d \
     --name react_frontend \
     --network frontend_network \
     --ip 172.18.0.20 \
     -v $(pwd)/react_frontend:/usr/share/nginx/html:ro \
     nginx:alpine

   # Connecter au monitoring
   docker network connect monitoring_network react_frontend --ip 172.22.0.40

   # Connecter au réseau API pour communication
   docker network connect api_network react_frontend --ip 172.19.0.30

   # Déployer le Load Balancer principal
   docker run -d \
     --name nginx_loadbalancer \
     --network frontend_network \
     --ip 172.18.0.10 \
     -p 80:80 \
     -v $(pwd)/nginx_complete/nginx.conf:/etc/nginx/nginx.conf:ro \
     nginx:alpine

   # Connecter le LB aux réseaux nécessaires
   docker network connect api_network nginx_loadbalancer --ip 172.19.0.10
   docker network connect monitoring_network nginx_loadbalancer --ip 172.22.0.50
   ```

### Étape 5 : Monitoring avec Prometheus (2 points)

1. **Configurer Prometheus** :

   ```bash
   mkdir -p prometheus_config

   cat > prometheus_config/prometheus.yml << 'EOF'
   global:
     scrape_interval: 15s
     evaluation_interval: 15s

   scrape_configs:
     - job_name: 'devops-api'
       static_configs:
         - targets: ['172.22.0.30:3000']
       metrics_path: /metrics
       scrape_interval: 10s

     - job_name: 'nginx-frontend'
       static_configs:
         - targets: ['172.22.0.40:80']
       metrics_path: /nginx_status
       scrape_interval: 15s

     - job_name: 'nginx-loadbalancer'
       static_configs:
         - targets: ['172.22.0.50:80']
       metrics_path: /nginx_status
       scrape_interval: 15s

     - job_name: 'postgres-exporter'
       static_configs:
         - targets: ['172.22.0.10:5432']
       scrape_interval: 30s

     - job_name: 'redis-exporter'
       static_configs:
         - targets: ['172.22.0.20:6379']
       scrape_interval: 30s
   EOF
   ```

2. **Déployer Prometheus** :
   ```bash
   docker run -d \
     --name prometheus_monitoring \
     --network monitoring_network \
     --ip 172.22.0.100 \
     -p 9090:9090 \
     -v prometheus_lab3_data:/prometheus \
     -v $(pwd)/prometheus_config/prometheus.yml:/etc/prometheus/prometheus.yml:ro \
     prom/prometheus:latest \
     --config.file=/etc/prometheus/prometheus.yml \
     --storage.tsdb.path=/prometheus \
     --web.console.libraries=/etc/prometheus/console_libraries \
     --web.console.templates=/etc/prometheus/consoles \
     --web.enable-lifecycle
   ```

### Étape 6 : Tests de résilience et validation (1 point)

1. **Tests de communication complète** :

   ```bash
   # Test de l'application complète depuis l'extérieur
   echo "=== Test Load Balancer ==="
   curl -s http://localhost/health | jq

   echo "=== Test API via Load Balancer ==="
   curl -s http://localhost/api/stats | jq

   echo "=== Test Cache Redis ==="
   curl -s http://localhost/api/users | jq '.source'
   curl -s http://localhost/api/users | jq '.source'  # Doit être 'cache'
   ```

2. **Tests de résilience** :

   ```bash
   echo "=== Test de résilience - Arrêt/Redémarrage de l'API ==="

   # Tester avant arrêt
   curl -s http://localhost/api/stats

   # Arrêter l'API
   docker stop express_api

   # Tester pendant l'arrêt (doit échouer)
   curl -s http://localhost/api/stats || echo "API indisponible (attendu)"

   # Redémarrer l'API
   docker start express_api
   sleep 10

   # Tester après redémarrage
   curl -s http://localhost/api/stats | jq

   echo "=== Test de persistance PostgreSQL ==="

   # Arrêter PostgreSQL
   docker stop postgres_app

   # Redémarrer PostgreSQL
   docker start postgres_app
   sleep 15

   # Vérifier que les données sont toujours là
   docker exec postgres_app psql -U devops_user -d devops_app -c "SELECT COUNT(*) FROM users;"

   echo "=== Test de persistance Redis ==="

   # Ajouter des données dans le cache
   docker exec redis_cache redis-cli SET test_key "test_value"

   # Arrêter et redémarrer Redis
   docker stop redis_cache
   docker start redis_cache
   sleep 5

   # Vérifier la persistance
   docker exec redis_cache redis-cli GET test_key
   ```

3. **Validation du monitoring** :

   ```bash
   echo "=== Validation Prometheus ==="

   # Vérifier que Prometheus collecte les métriques
   curl -s http://localhost:9090/api/v1/query?query=up | jq '.data.result[] | {job: .metric.job, value: .value[1]}'

   # Vérifier les métriques de l'API
   curl -s http://localhost:9090/api/v1/query?query=http_requests_total | jq '.data.result | length'

   echo "Accédez à http://localhost:9090 pour l'interface Prometheus"
   echo "Accédez à http://localhost pour l'application complète"
   ```

## Validation et critères d'évaluation

### Vérifications attendues

1. **Architecture réseau complète (3 points)** :

   ```bash
   # 5 réseaux créés
   docker network ls | grep -E "(frontend|api|backend|cache|monitoring)_network" | wc -l

   # Connectivité entre services validée
   docker run --rm --network api_network curlimages/curl curl -s http://172.19.0.20:3000/health
   ```

2. **Persistance configurée sur tous services (3 points)** :

   ```bash
   # 3 volumes créés et utilisés
   docker volume ls | grep lab3_data | wc -l

   # PostgreSQL avec données persistantes
   docker exec postgres_app psql -U devops_user -d devops_app -c "SELECT COUNT(*) FROM users;"

   # Redis avec persistance
   docker exec redis_cache redis-cli CONFIG GET save
   ```

3. **Communication inter-services fonctionnelle (3 points)** :

   ```bash
   # API peut accéder à PostgreSQL et Redis
   curl -s http://localhost/api/users | jq '.source' # doit retourner 'database' puis 'cache'

   # Frontend peut accéder à l'API
   curl -s http://localhost/api/stats
   ```

4. **Monitoring opérationnel (2 points)** :

   ```bash
   # Prometheus collecte les métriques
   curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets | length'

   # Métriques applicatives disponibles
   curl -s http://localhost/metrics | grep http_requests_total
   ```

5. **Tests de résilience réussis (1 point)** :
   ```bash
   # Redémarrage des services sans perte de données
   # Volumes persistants fonctionnels
   # Communication rétablie après incidents
   ```

## Livrables attendus

- [ ] Fichier `S2_S1_S3_lab3_app_complete.yml` (Docker Compose final)
- [ ] Architecture réseau 5-tiers déployée
- [ ] 5 services fonctionnels avec persistance
- [ ] Monitoring Prometheus opérationnel
- [ ] Tests de résilience documentés
- [ ] Application accessible via http://localhost
- [ ] Monitoring accessible via http://localhost:9090

## Docker Compose final

Créer le fichier `S2_S1_S3_lab3_app_complete.yml` consolidant tout le déploiement :

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: postgres_app
    networks:
      backend_network:
        ipv4_address: 172.20.0.10
      monitoring_network:
        ipv4_address: 172.22.0.10
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: devops_user
      POSTGRES_PASSWORD: DevOpsPass123
    volumes:
      - postgres_lab3_data:/var/lib/postgresql/data
      - ./database_init:/docker-entrypoint-initdb.d
    restart: unless-stopped

  redis:
    image: redis:alpine
    container_name: redis_cache
    networks:
      cache_network:
        ipv4_address: 172.21.0.10
      monitoring_network:
        ipv4_address: 172.22.0.20
    volumes:
      - redis_lab3_data:/data
    command: redis-server --save 60 1 --loglevel warning
    restart: unless-stopped

  api:
    build: ./express_api
    container_name: express_api
    networks:
      api_network:
        ipv4_address: 172.19.0.20
      backend_network:
        ipv4_address: 172.20.0.20
      cache_network:
        ipv4_address: 172.21.0.20
      monitoring_network:
        ipv4_address: 172.22.0.30
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    container_name: react_frontend
    networks:
      frontend_network:
        ipv4_address: 172.18.0.20
      api_network:
        ipv4_address: 172.19.0.30
      monitoring_network:
        ipv4_address: 172.22.0.40
    volumes:
      - ./react_frontend:/usr/share/nginx/html:ro
    depends_on:
      - api
    restart: unless-stopped

  loadbalancer:
    image: nginx:alpine
    container_name: nginx_loadbalancer
    networks:
      frontend_network:
        ipv4_address: 172.18.0.10
      api_network:
        ipv4_address: 172.19.0.10
      monitoring_network:
        ipv4_address: 172.22.0.50
    ports:
      - '80:80'
    volumes:
      - ./nginx_complete/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - api
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus_monitoring
    networks:
      monitoring_network:
        ipv4_address: 172.22.0.100
    ports:
      - '9090:9090'
    volumes:
      - prometheus_lab3_data:/prometheus
      - ./prometheus_config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    restart: unless-stopped

networks:
  frontend_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.18.0.0/24
  api_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.19.0.0/24
  backend_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
  cache_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/24
  monitoring_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.22.0.0/24

volumes:
  postgres_lab3_data:
  redis_lab3_data:
  prometheus_lab3_data:
```

---

**Sprint 2 - Semaine 1 - Séance 3 - LAB 3**  
_Formateur : Hassan ESSADIK_
