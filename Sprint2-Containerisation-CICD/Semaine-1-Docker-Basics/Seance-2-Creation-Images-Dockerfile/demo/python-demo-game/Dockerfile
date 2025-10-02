FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le script du jeu dans le conteneur
COPY number_game.py .

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash gameuser && \
    chown -R gameuser:gameuser /app

# Changer vers l'utilisateur non-root
USER gameuser

# Commande par défaut pour lancer le jeu
CMD ["python", "number_game.py"]