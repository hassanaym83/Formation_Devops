FROM node:18-alpine

# Créer un utilisateur non-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
# Use npm install with --omit=dev to avoid requiring package-lock.json (simpler for teaching/demo)
RUN npm install --omit=dev --no-audit --no-fund && npm cache clean --force

# Copier le code source
COPY . .

# Changer la propriété des fichiers vers l'utilisateur nodejs
RUN chown -R nodejs:nodejs /app
USER nodejs

# Exposer le port
EXPOSE 3002

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3002/health || exit 1

# Commande de démarrage
CMD ["node", "app.js"]