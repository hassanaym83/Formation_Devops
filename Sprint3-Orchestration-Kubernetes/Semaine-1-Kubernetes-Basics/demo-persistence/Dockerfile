# Dockerfile pour l'application de démonstration de persistance
FROM node:18-alpine

# Métadonnées
LABEL maintainer="Formation DevOps"
LABEL description="Application de démonstration pour la persistance Kubernetes"
LABEL version="1.0.0"

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration npm
COPY package*.json ./

# Installer les dépendances
RUN npm ci --only=production && npm cache clean --force

# Créer un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copier le code source
COPY --chown=nodejs:nodejs . .

# Créer le dossier data avec les bonnes permissions
RUN mkdir -p /app/data && \
    chown -R nodejs:nodejs /app/data

# Changer vers l'utilisateur non-root
USER nodejs

# Exposer le port
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=production
ENV PORT=3000

# Point de montage pour le volume persistant
VOLUME ["/app/data"]

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Commande de démarrage
CMD ["npm", "start"]