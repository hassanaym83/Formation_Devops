# LAB 2 - Build multi-stage et sécurité

## Informations générales

- **Sprint** : 2 - Containerisation et CI/CD
- **Semaine** : 1 - Docker Basics
- **Séance** : 2 - Dockerfile Creation
- **LAB** : 2/3
- **Durée estimée** : 25 minutes
- **Formateur** : Hassan ESSADIK

## Objectifs pédagogiques

- Implémenter un build multi-stage pour optimisation
- Configurer la sécurité avec utilisateur non-root
- Créer des health checks robustes
- Scanner les vulnérabilités de sécurité

## Contexte

Vous devez créer une image Docker production-ready pour une application Node.js Express, en utilisant les techniques multi-stage et en appliquant les meilleures pratiques de sécurité.

## Prérequis techniques

- Docker Desktop avec BuildKit activé
- Node.js installé localement (pour tests)
- Trivy ou outil de scan de vulnérabilités
- Connaissances de base Node.js/Express

## Instructions

### Étape 1 : Préparation de l'application Node.js (8 minutes)

Créez la structure suivante :

```
lab2-multistage/
├── src/
│   ├── app.js
│   ├── routes/
│   │   └── api.js
│   └── middleware/
│       └── security.js
├── package.json
├── Dockerfile
├── .dockerignore
├── healthcheck.js
└── docker-entrypoint.sh
```

**Fichier `package.json`** :

```json
{
  "name": "express-multistage-lab",
  "version": "1.0.0",
  "description": "LAB 2 - Multi-stage build with security",
  "main": "src/app.js",
  "scripts": {
    "start": "node src/app.js",
    "dev": "nodemon src/app.js",
    "build": "npm ci --only=production",
    "test": "jest --coverage",
    "lint": "eslint src/",
    "security-audit": "npm audit"
  },
  "dependencies": {
    "express": "^4.18.2",
    "helmet": "^7.0.0",
    "express-rate-limit": "^6.10.0",
    "morgan": "^1.10.0",
    "cors": "^2.8.5"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "eslint": "^8.45.0",
    "jest": "^29.6.2"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

**Fichier `src/app.js`** :

```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');
const cors = require('cors');
const apiRoutes = require('./routes/api');
const securityMiddleware = require('./middleware/security');

const app = express();
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'production';

// Security middleware
app.use(helmet());
app.use(cors());
app.use(securityMiddleware);

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Logging
app.use(morgan('combined'));

// Body parsing
app.use(express.json({limit: '10mb'}));
app.use(express.urlencoded({extended: true}));

// Routes
app.use('/api', apiRoutes);

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
    version: process.env.npm_package_version || '1.0.0',
    uptime: process.uptime(),
    memory: process.memoryUsage()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Express Multi-stage LAB API',
    version: '1.0.0',
    endpoints: ['/health', '/api/users', '/api/status']
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({error: 'Something went wrong!'});
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({error: 'Route not found'});
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT} in ${NODE_ENV} mode`);
});

module.exports = app;
```

**Fichier `src/routes/api.js`** :

```javascript
const express = require('express');
const router = express.Router();

// Mock users data
const users = [
  {id: 1, name: 'Hassan', role: 'DevOps Engineer'},
  {id: 2, name: 'Alice', role: 'Developer'},
  {id: 3, name: 'Bob', role: 'SRE'}
];

router.get('/users', (req, res) => {
  res.json({
    success: true,
    data: users,
    count: users.length
  });
});

router.get('/status', (req, res) => {
  res.json({
    api_status: 'operational',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
```

**Fichier `src/middleware/security.js`** :

```javascript
module.exports = (req, res, next) => {
  // Remove X-Powered-By header
  res.removeHeader('X-Powered-By');

  // Add security headers
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');

  next();
};
```

### Étape 2 : Health check script (3 minutes)

**Fichier `healthcheck.js`** :

```javascript
const http = require('http');

const options = {
  hostname: 'localhost',
  port: process.env.PORT || 3000,
  path: '/health',
  method: 'GET',
  timeout: 5000
};

const req = http.request(options, (res) => {
  if (res.statusCode === 200) {
    console.log('Health check passed');
    process.exit(0);
  } else {
    console.log(`Health check failed with status ${res.statusCode}`);
    process.exit(1);
  }
});

req.on('error', (error) => {
  console.log(`Health check failed: ${error.message}`);
  process.exit(1);
});

req.on('timeout', () => {
  console.log('Health check timeout');
  req.destroy();
  process.exit(1);
});

req.end();
```

**Fichier `docker-entrypoint.sh`** :

```bash
#!/bin/sh
set -e

# Function to handle shutdown gracefully
shutdown() {
    echo "Received shutdown signal, stopping application..."
    kill -TERM "$child" 2>/dev/null
    wait "$child"
    exit 0
}

# Set up signal handlers
trap shutdown TERM INT

echo "Starting Express application..."
echo "Node.js version: $(node --version)"
echo "NPM version: $(npm --version)"
echo "Environment: ${NODE_ENV:-production}"

# Start the application in background
node src/app.js &
child=$!

# Wait for the application to start
wait "$child"
```

### Étape 3 : Dockerfile multi-stage avec sécurité (10 minutes)

**Dockerfile complet** :

```dockerfile
# syntax=docker/dockerfile:1.4

# ===== STAGE 1: Base image with dependencies =====
FROM node:18-alpine AS base
RUN apk add --no-cache \
    dumb-init \
    && rm -rf /var/cache/apk/*
WORKDIR /app
COPY package*.json ./

# ===== STAGE 2: Development dependencies =====
FROM base AS dev-deps
RUN npm ci --include=dev

# ===== STAGE 3: Production dependencies =====
FROM base AS prod-deps
RUN npm ci --only=production && \
    npm cache clean --force

# ===== STAGE 4: Build and test =====
FROM dev-deps AS build
COPY . .
RUN npm run lint && \
    npm run security-audit --audit-level=moderate

# ===== STAGE 5: Security scanning =====
FROM aquasec/trivy:latest AS security
COPY --from=build /app /scan
RUN trivy fs --exit-code 0 --severity HIGH,CRITICAL /scan

# ===== STAGE 6: Final production image =====
FROM node:18-alpine AS production

# Install security updates
RUN apk upgrade --no-cache && \
    apk add --no-cache dumb-init curl && \
    rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S appuser -u 1001 -G nodejs

# Set working directory
WORKDIR /app

# Copy production dependencies
COPY --from=prod-deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=prod-deps --chown=appuser:nodejs /app/package*.json ./

# Copy application code and scripts
COPY --chown=appuser:nodejs src/ ./src/
COPY --chown=appuser:nodejs healthcheck.js ./
COPY --chown=appuser:nodejs docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

# Switch to non-root user
USER appuser

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV NPM_CONFIG_CACHE=/tmp/.npm

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD node healthcheck.js

# Expose port
EXPOSE 3000

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]
CMD ["./docker-entrypoint.sh"]
```

**Fichier `.dockerignore`** :

```dockerignore
node_modules
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.git
.gitignore
README.md
Dockerfile*
.dockerignore
coverage/
.nyc_output
.vscode/
.idea/
*.log
.env
.env.local
.env.test
```

### Étape 4 : Build et tests de sécurité (4 minutes)

**Build multi-stage** :

```bash
# Activer BuildKit
export DOCKER_BUILDKIT=1

# Build avec target spécifique pour tests
docker build --target build -t express-lab2:build .

# Build production complet
docker build -t express-lab2:latest .

# Analyse de la taille
docker images | grep express-lab2
```

**Tests de sécurité** :

```bash
# Scan de vulnérabilités avec Trivy
trivy image express-lab2:latest

# Vérification de l'utilisateur non-root
docker run --rm express-lab2:latest id

# Test des capabilities
docker run --rm express-lab2:latest cat /proc/1/status | grep Cap
```

## Tests et validations

### Test fonctionnel complet

```bash
# Lancement avec health check
docker run -d -p 3000:3000 --name express-test express-lab2:latest

# Attendre le démarrage (health check)
sleep 10

# Tests des endpoints
curl -s http://localhost:3000/ | jq
curl -s http://localhost:3000/health | jq
curl -s http://localhost:3000/api/users | jq
curl -s http://localhost:3000/api/status | jq

# Vérification du health check
docker inspect express-test | jq '.[0].State.Health'

# Test de performance
ab -n 1000 -c 10 http://localhost:3000/

# Nettoyage
docker stop express-test && docker rm express-test
```

### Analyse de sécurité

```bash
# Vérification de l'utilisateur
docker run --rm express-lab2:latest whoami

# Vérification des processus
docker run --rm express-lab2:latest ps aux

# Scan avec Docker Scout (si disponible)
docker scout cves express-lab2:latest
```

## Livrables attendus

### 1. Multi-stage build fonctionnel

- [ ] Dockerfile avec au moins 3 stages distincts
- [ ] Optimisation de taille démontrée
- [ ] Dependencies séparées (dev/prod)
- [ ] Build reproductible

### 2. Sécurité configurée

- [ ] Utilisateur non-root configuré et testé
- [ ] Image de base mise à jour (security patches)
- [ ] Headers de sécurité dans l'application
- [ ] Scan de vulnérabilités réalisé

### 3. Health checks opérationnels

- [ ] Health check intégré au Dockerfile
- [ ] Script de health check personnalisé
- [ ] Tests de health check validés
- [ ] Gestion des signaux (graceful shutdown)

### 4. Scan de vulnérabilités réalisé

- [ ] Scan avec Trivy ou équivalent
- [ ] Rapport de vulnérabilités documenté
- [ ] Actions correctives identifiées
- [ ] Niveau de sécurité acceptable

## Critères d'évaluation

**Multi-stage** : Build optimisé avec stages séparés
**Sécurité** : Non-root user, patches, headers sécurisés
**Health checks** : Health checks fonctionnels et testés
**Vulnérabilités** : Scan réalisé et documenté

## Bonus (optionnel)

### Optimisation avancée

Implémentez des optimisations supplémentaires :

```dockerfile
# Cache mount pour npm
RUN --mount=type=cache,target=/tmp/.npm \
    npm ci --only=production

# Utilisation de distroless
FROM gcr.io/distroless/nodejs18-debian11 AS distroless
COPY --from=production /app /app
WORKDIR /app
EXPOSE 3000
CMD ["src/app.js"]
```

### Monitoring intégré

Ajoutez des métriques Prometheus :

```javascript
// Dans app.js
const client = require('prom-client');
const register = new client.Registry();

// Métriques personnalisées
const httpDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['route', 'method', 'status_code']
});

register.registerMetric(httpDuration);

app.get('/metrics', (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(register.metrics());
});
```

## Ressources complémentaires

- [Multi-stage builds](https://docs.docker.com/develop/dev-best-practices/)
- [Docker security best practices](https://docs.docker.com/engine/security/security/)
- [Trivy vulnerability scanner](https://trivy.dev/)
- [Node.js security best practices](https://nodejs.org/en/docs/guides/security/)

## Aide au dépannage

### Problèmes de build

```bash
# Debug du build multi-stage
docker build --target build -t debug .

# Inspection des layers
docker history express-lab2:latest

# Debug de sécurité
docker run --rm -it express-lab2:latest sh
```

### Problèmes de permissions

```bash
# Vérification des permissions
docker run --rm express-lab2:latest ls -la /app

# Debug utilisateur
docker run --rm express-lab2:latest id
```

---

**Note importante** : Ce LAB prépare aux déploiements production. Documentez toutes les vulnérabilités trouvées et les mesures de mitigation appliquées.
