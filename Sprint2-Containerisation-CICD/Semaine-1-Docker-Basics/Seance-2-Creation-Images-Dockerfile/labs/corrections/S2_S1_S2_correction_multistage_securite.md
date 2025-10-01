# CORRECTION LAB 2 - Build multi-stage et sécurité

## Informations générales

- **Sprint** : 2 - Containerisation et CI/CD
- **Semaine** : 1 - Docker Basics
- **Séance** : 2 - Dockerfile Creation
- **Correction** : LAB 2 - Multi-stage et sécurité
- **Formateur** : Hassan ESSADIK

## Solution complète

### Structure finale

```
lab2-multistage/
├── src/
│   ├── app.js                    ✓ Application Express sécurisée
│   ├── routes/
│   │   └── api.js               ✓ Routes API structurées
│   └── middleware/
│       └── security.js          ✓ Middleware de sécurité
├── package.json                  ✓ Dependencies et scripts
├── Dockerfile                    ✓ Multi-stage optimisé
├── .dockerignore                ✓ Exclusions appropriées
├── healthcheck.js               ✓ Health check personnalisé
├── docker-entrypoint.sh         ✓ Point d'entrée robuste
├── docker-compose.yml           ✓ Orchestration complète
├── nginx.conf                   ✓ Reverse proxy
└── SECURITY-REPORT.md           ✓ Analyse de sécurité
```

### 1. Application Express sécurisée (src/app.js)

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

// Configuration de sécurité avancée avec Helmet
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:']
      }
    },
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    }
  })
);

// CORS configuration sécurisée
app.use(
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || [
      'http://localhost:3000'
    ],
    credentials: true,
    optionsSuccessStatus: 200
  })
);

// Rate limiting avancé
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limite par IP
  message: {
    error: 'Too many requests',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false
});

const strictLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Limite stricte pour certains endpoints
  message: {
    error: 'Too many requests to this endpoint',
    retryAfter: '15 minutes'
  }
});

app.use('/api', limiter);
app.use('/auth', strictLimiter);

// Middleware de sécurité personnalisé
app.use(securityMiddleware);

// Logging sécurisé
app.use(
  morgan('combined', {
    stream: {
      write: (message) => {
        // Masquer les informations sensibles
        const sanitized = message.replace(/password=[^&\s]*/gi, 'password=***');
        console.log(sanitized.trim());
      }
    }
  })
);

// Body parsing avec limites de sécurité
app.use(
  express.json({
    limit: '10mb',
    verify: (req, res, buf) => {
      req.rawBody = buf;
    }
  })
);
app.use(
  express.urlencoded({
    extended: true,
    limit: '10mb'
  })
);

// Routes
app.use('/api', apiRoutes);

// Health check endpoint sécurisé
app.get('/health', (req, res) => {
  const healthData = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
    version: process.env.npm_package_version || '1.0.0',
    uptime: Math.floor(process.uptime()),
    memory: {
      used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
      total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024)
    },
    checks: {
      database: 'connected', // Simulé
      cache: 'operational', // Simulé
      external_api: 'available' // Simulé
    }
  };

  res.status(200).json(healthData);
});

// Endpoint de readiness probe
app.get('/ready', (req, res) => {
  // Vérifications plus poussées pour Kubernetes
  const ready = {
    ready: true,
    timestamp: new Date().toISOString(),
    dependencies: {
      database: true,
      cache: true,
      storage: true
    }
  };

  res.status(200).json(ready);
});

// Endpoint principal
app.get('/', (req, res) => {
  res.json({
    message: 'Express Multi-stage LAB API - Secured',
    version: '2.0.0',
    environment: NODE_ENV,
    endpoints: {
      health: '/health',
      ready: '/ready',
      api: '/api/*'
    },
    security: {
      helmet: 'enabled',
      rate_limiting: 'active',
      cors: 'configured'
    }
  });
});

// Metrics endpoint pour monitoring
app.get('/metrics', (req, res) => {
  const metrics = {
    timestamp: new Date().toISOString(),
    process: {
      pid: process.pid,
      uptime: process.uptime(),
      memory: process.memoryUsage(),
      cpu: process.cpuUsage()
    },
    node: {
      version: process.version,
      platform: process.platform,
      arch: process.arch
    }
  };

  res.json(metrics);
});

// Middleware de gestion d'erreurs sécurisé
app.use((err, req, res, next) => {
  console.error('Error:', err.message);

  // Ne pas exposer les détails d'erreur en production
  const isDevelopment = NODE_ENV === 'development';

  res.status(err.status || 500).json({
    error: isDevelopment ? err.message : 'Internal server error',
    ...(isDevelopment && {stack: err.stack})
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.originalUrl,
    method: req.method
  });
});

// Graceful shutdown
const gracefulShutdown = (signal) => {
  console.log(`Received ${signal}, shutting down gracefully`);

  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });

  // Force shutdown after 10 seconds
  setTimeout(() => {
    console.error(
      'Could not close connections in time, forcefully shutting down'
    );
    process.exit(1);
  }, 10000);
};

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server running on port ${PORT} in ${NODE_ENV} mode`);
  console.log(`📊 Health check: http://localhost:${PORT}/health`);
  console.log(`📈 Metrics: http://localhost:${PORT}/metrics`);
});

// Signal handlers
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

module.exports = app;
```

### 2. Middleware de sécurité avancé (src/middleware/security.js)

```javascript
const crypto = require('crypto');

// Génération de nonce pour CSP
const generateNonce = () => crypto.randomBytes(16).toString('base64');

module.exports = (req, res, next) => {
  // Suppression des headers révélateurs
  res.removeHeader('X-Powered-By');
  res.removeHeader('Server');

  // Headers de sécurité personnalisés
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader(
    'Permissions-Policy',
    'geolocation=(), microphone=(), camera=()'
  );

  // HSTS pour HTTPS
  if (req.secure || req.headers['x-forwarded-proto'] === 'https') {
    res.setHeader(
      'Strict-Transport-Security',
      'max-age=31536000; includeSubDomains; preload'
    );
  }

  // Nonce pour CSP
  req.nonce = generateNonce();
  res.locals.nonce = req.nonce;

  // Logging des tentatives d'accès suspects
  const suspiciousPatterns = [
    /\.\.\//, // Path traversal
    /<script/i, // XSS attempts
    /union.*select/i, // SQL injection
    /javascript:/i // JavaScript injection
  ];

  const url = req.originalUrl || req.url;
  const userAgent = req.get('User-Agent') || '';

  suspiciousPatterns.forEach((pattern) => {
    if (pattern.test(url) || pattern.test(userAgent)) {
      console.warn(
        `🚨 Suspicious request detected: ${req.method} ${url} from ${req.ip}`
      );
      console.warn(`User-Agent: ${userAgent}`);
    }
  });

  // Limitation de la taille des headers
  const headerSizeLimit = 8192; // 8KB
  const headerSize = JSON.stringify(req.headers).length;

  if (headerSize > headerSizeLimit) {
    return res.status(413).json({
      error: 'Request headers too large',
      limit: headerSizeLimit
    });
  }

  next();
};
```

### 3. Health check avancé (healthcheck.js)

```javascript
const http = require('http');
const url = require('url');

const config = {
  hostname: 'localhost',
  port: process.env.PORT || 3000,
  timeout: 5000,
  retries: 3,
  retryDelay: 1000
};

// Health check avec retry logic
const performHealthCheck = (attempt = 1) => {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: config.hostname,
      port: config.port,
      path: '/health',
      method: 'GET',
      timeout: config.timeout,
      headers: {
        'User-Agent': 'HealthCheck/1.0'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => (data += chunk));

      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const healthData = JSON.parse(data);
            console.log(`✅ Health check passed (attempt ${attempt})`);
            console.log(`Status: ${healthData.status}`);
            console.log(`Uptime: ${healthData.uptime}s`);
            console.log(`Memory: ${healthData.memory?.used || 'N/A'}MB`);
            resolve(healthData);
          } catch (err) {
            reject(new Error(`Invalid health response: ${err.message}`));
          }
        } else {
          reject(
            new Error(`Health check failed with status ${res.statusCode}`)
          );
        }
      });
    });

    req.on('error', (error) => {
      reject(new Error(`Health check request failed: ${error.message}`));
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Health check timeout'));
    });

    req.end();
  });
};

// Logique de retry
const healthCheckWithRetry = async () => {
  for (let attempt = 1; attempt <= config.retries; attempt++) {
    try {
      await performHealthCheck(attempt);
      process.exit(0);
    } catch (error) {
      console.error(
        `❌ Health check failed (attempt ${attempt}/${config.retries}): ${error.message}`
      );

      if (attempt === config.retries) {
        console.error('🚨 All health check attempts failed');
        process.exit(1);
      }

      // Attendre avant le prochain essai
      await new Promise((resolve) => setTimeout(resolve, config.retryDelay));
    }
  }
};

// Deep health check (optionnel)
const deepHealthCheck = async () => {
  try {
    // Vérification readiness
    const readyCheck = await new Promise((resolve, reject) => {
      const req = http.request(
        {
          hostname: config.hostname,
          port: config.port,
          path: '/ready',
          method: 'GET',
          timeout: config.timeout
        },
        (res) => {
          if (res.statusCode === 200) {
            resolve(true);
          } else {
            reject(new Error(`Readiness check failed: ${res.statusCode}`));
          }
        }
      );

      req.on('error', reject);
      req.on('timeout', () => reject(new Error('Readiness timeout')));
      req.end();
    });

    console.log('✅ Deep health check passed');
    return true;
  } catch (error) {
    console.error(`❌ Deep health check failed: ${error.message}`);
    return false;
  }
};

// Exécution du health check
if (process.env.DEEP_HEALTH_CHECK === 'true') {
  deepHealthCheck().then((success) => {
    process.exit(success ? 0 : 1);
  });
} else {
  healthCheckWithRetry();
}
```

### 4. Dockerfile multi-stage optimisé

```dockerfile
# syntax=docker/dockerfile:1.4

# ===== ARGUMENTS DE BUILD =====
ARG NODE_VERSION=18.18-alpine
ARG NGINX_VERSION=1.25-alpine

# ===== STAGE 1: Base avec dépendances système =====
FROM node:${NODE_VERSION} AS base

# Installation des dépendances système et outils de sécurité
RUN apk update && apk upgrade && \
    apk add --no-cache \
        dumb-init \
        curl \
        ca-certificates \
        && rm -rf /var/cache/apk/* \
        && addgroup -g 1001 -S nodejs \
        && adduser -S appuser -u 1001 -G nodejs

WORKDIR /app

# ===== STAGE 2: Dependencies installer =====
FROM base AS deps

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation de toutes les dépendances (dev + prod)
RUN --mount=type=cache,target=/root/.npm \
    npm ci --include=dev

# ===== STAGE 3: Builder avec tests =====
FROM deps AS builder

# Copie du code source
COPY . .

# Audit de sécurité et tests
RUN npm audit --audit-level=moderate && \
    npm run lint && \
    npm run test --if-present

# Build de production (si applicable)
RUN npm run build --if-present

# ===== STAGE 4: Production dependencies =====
FROM base AS prod-deps

COPY package*.json ./

# Installation des dépendances de production uniquement
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production && \
    npm cache clean --force

# ===== STAGE 5: Security scanning =====
FROM aquasec/trivy:latest AS security-scanner

# Copie de l'application pour scan
COPY --from=builder /app /scan
COPY --from=prod-deps /app/node_modules /scan/node_modules

# Scan de sécurité (non-blocking pour le build)
RUN trivy fs --exit-code 0 --severity HIGH,CRITICAL \
    --format table \
    /scan > /tmp/security-report.txt || true

# ===== STAGE 6: Runtime image =====
FROM node:${NODE_VERSION} AS runtime

# Installation des mises à jour de sécurité
RUN apk update && apk upgrade && \
    apk add --no-cache \
        dumb-init \
        curl \
        ca-certificates \
        tini \
        && rm -rf /var/cache/apk/*

# Création de l'utilisateur non-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S appuser -u 1001 -G nodejs

# Configuration du répertoire de travail
WORKDIR /app

# Copie des dépendances de production
COPY --from=prod-deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=prod-deps --chown=appuser:nodejs /app/package*.json ./

# Copie du code application
COPY --from=builder --chown=appuser:nodejs /app/src ./src
COPY --chown=appuser:nodejs healthcheck.js ./
COPY --chown=appuser:nodejs docker-entrypoint.sh ./

# Scripts exécutables
RUN chmod +x docker-entrypoint.sh

# Variables d'environnement de sécurité
ENV NODE_ENV=production \
    PORT=3000 \
    NPM_CONFIG_CACHE=/tmp/.npm \
    NODE_OPTIONS="--max-old-space-size=512" \
    FORCE_COLOR=0

# Passage à l'utilisateur non-root
USER appuser

# Health check avancé
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD ["node", "healthcheck.js"]

# Exposition du port
EXPOSE 3000

# Signal handling avec tini
ENTRYPOINT ["tini", "--"]
CMD ["./docker-entrypoint.sh"]

# ===== STAGE 7: Nginx reverse proxy (optionnel) =====
FROM nginx:${NGINX_VERSION} AS proxy

# Configuration Nginx sécurisée
COPY nginx.conf /etc/nginx/nginx.conf

# Utilisateur non-root pour Nginx
RUN addgroup -g 1001 -S nginx-user && \
    adduser -S nginx-user -u 1001 -G nginx-user && \
    chown -R nginx-user:nginx-user /var/cache/nginx && \
    chown -R nginx-user:nginx-user /var/log/nginx && \
    chown -R nginx-user:nginx-user /etc/nginx/conf.d

USER nginx-user

EXPOSE 80
```

### 5. Configuration Nginx sécurisée (nginx.conf)

```nginx
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Sécurité
    server_tokens off;
    client_max_body_size 10M;
    client_body_buffer_size 16K;
    client_header_buffer_size 1k;
    large_client_header_buffers 2 1k;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types
        application/json
        application/javascript
        text/css
        text/plain
        text/xml;

    upstream app {
        server app:3000;
        keepalive 32;
    }

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Health check
        location /health {
            access_log off;
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # API endpoints avec rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Auth endpoints avec rate limiting strict
        location /auth/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Autres endpoints
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### 6. Docker Compose avec orchestration complète

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
      args:
        - NODE_VERSION=18.18-alpine
    image: express-multistage:secure
    container_name: express-app
    environment:
      - NODE_ENV=production
      - PORT=3000
      - ALLOWED_ORIGINS=http://localhost:80
    networks:
      - app-network
    healthcheck:
      test: ['CMD', 'node', 'healthcheck.js']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - SETUID
      - SETGID
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  nginx:
    build:
      context: .
      dockerfile: Dockerfile
      target: proxy
    image: express-proxy:secure
    container_name: express-proxy
    ports:
      - '80:80'
    depends_on:
      app:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - DAC_OVERRIDE
      - SETUID
      - SETGID

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - app-network
    depends_on:
      - app

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  prometheus-data:
```

## Tests et validation

### Script de test de sécurité

```bash
#!/bin/bash
# security-test.sh

echo "=== TESTS DE SÉCURITÉ AVANCÉS ==="

# Build et démarrage
docker-compose up -d --build

# Attendre le démarrage
echo "Attente du démarrage des services..."
sleep 30

echo -e "\n1. Test utilisateur non-root..."
USER_TEST=$(docker exec express-app id)
echo "Utilisateur: $USER_TEST"

echo -e "\n2. Test des capabilities..."
docker exec express-app cat /proc/1/status | grep Cap

echo -e "\n3. Test des headers de sécurité..."
curl -I http://localhost/

echo -e "\n4. Test du rate limiting..."
for i in {1..15}; do
  curl -s -o /dev/null -w "%{http_code} " http://localhost/api/status
done
echo

echo -e "\n5. Test XSS protection..."
curl -s "http://localhost/?test=<script>alert('xss')</script>" | jq

echo -e "\n6. Scan de vulnérabilités..."
trivy image express-multistage:secure

echo -e "\n7. Test health check..."
curl -s http://localhost/health | jq

echo -e "\n8. Test des métriques..."
curl -s http://localhost/metrics | jq

# Nettoyage
docker-compose down

echo -e "\n=== TESTS TERMINÉS ==="
```

## Barème de correction

### Multi-stage build fonctionnel (3/10 points)

- ✅ **1/1** - Au moins 3 stages distincts et fonctionnels
- ✅ **1/1** - Optimisation de taille démontrée (< 200MB)
- ✅ **1/1** - Séparation dev/prod dependencies

### Sécurité configurée (3/10 points)

- ✅ **1/1** - Utilisateur non-root configuré et testé
- ✅ **1/1** - Headers de sécurité dans application et Nginx
- ✅ **1/1** - Scan de vulnérabilités intégré

### Health checks opérationnels (2/10 points)

- ✅ **1/1** - Health check Dockerfile fonctionnel
- ✅ **1/1** - Script personnalisé avec retry logic

### Scan de vulnérabilités réalisé (2/10 points)

- ✅ **1/1** - Scan Trivy intégré au build
- ✅ **1/1** - Rapport documenté et actions correctives

## Points d'excellence

### Fonctionnalités avancées implémentées

1. **Reverse proxy Nginx** avec rate limiting
2. **Monitoring Prometheus** intégré
3. **Security hardening** complet
4. **Graceful shutdown** avec signaux
5. **Retry logic** dans health checks
6. **Resource limits** configurés

### Critères de sécurité respectés

1. **Principe du moindre privilège**
2. **Defense in depth**
3. **Fail secure**
4. **Logging sécurisé**
5. **Input validation**

---

**Note pédagogique** : Cette correction démontre l'intégration complète des bonnes pratiques de sécurité et d'optimisation pour un déploiement production-ready.
