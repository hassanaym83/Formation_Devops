# Utiliser l'image officielle Node.js 18 Alpine (plus légère)
FROM node:18-alpine

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install --only=production

# Copier le code source de l'application
COPY app.js .

# Exposer le port 3000
EXPOSE 3000

# Créer un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Changer vers l'utilisateur non-root
USER nodejs

# Définir la commande par défaut
CMD ["node", "app.js"]