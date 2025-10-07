# Application de Gestion des Réclamations
# Démonstration des volumes Docker

# Image de base Node.js Alpine pour une taille optimisée
FROM node:18-alpine

# Métadonnées de l'image
LABEL maintainer="Formation DevOps Simplon" \
      description="Application Node.js pour démonstration volumes Docker" \
      version="1.0.0"

# Variables d'environnement
ENV NODE_ENV=production \
    PORT=3000 \
    TZ=Europe/Paris

# Création de l'utilisateur non-privilégié pour la sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S hassan -u 1001

# Répertoire de travail de l'application
WORKDIR /app

# Copie et installation des dépendances
# (copie package*.json en premier pour optimiser le cache Docker)
COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

# Copie du code source de l'application
COPY . .

# Création des répertoires nécessaires avec permissions appropriées
RUN mkdir -p /tmp/claims /persist/claims/validated /persist/claims/archived && \
    chown -R hassan:nodejs /app /tmp/claims /persist

# Exposition du port de l'application
EXPOSE 3000

# Basculement vers l'utilisateur non-privilégié
USER hassan

# Commande de démarrage de l'application
CMD ["node", "server.js"]