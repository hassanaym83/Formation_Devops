const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware pour logger les requêtes
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Endpoint racine "/"
app.get('/', (req, res) => {
  const message = `image3 app Node.js pour démonstration Kubernetes__
📅 Démarrée le: ${new Date().toISOString()}
🌐 Endpoint: GET /
✅ Status: Fonctionnel
🐳 Container ID: ${process.env.HOSTNAME || 'local'}`;

  console.log('✅ Endpoint "/" appelé avec succès');
  res.status(200).send(message);
});

// Endpoint "404" qui provoque une erreur
app.get('/404', (req, res) => {
  const errorMessage = `❌ Erreur simulée - Endpoint /404
📅 Heure: ${new Date().toISOString()}
🚨 Cette route provoque intentionnellement une erreur
💀 L'application va se terminer avec exit(1)`;

  console.error('💀 Endpoint "/404" appelé - Arrêt de l\'application');
  res.status(500).send(errorMessage);

  // Arrêt de l'application avec code d'erreur
  setTimeout(() => {
    console.error('💀 Application terminée avec exit(1)');
    process.exit(1);
  }, 1000);
});

// Endpoint pour vérifier la santé (optionnel pour Kubernetes)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Gestion des erreurs 404 pour toutes les autres routes
app.use('*', (req, res) => {
  res.status(404).send(`🔍 Route non trouvée: ${req.originalUrl}
📋 Routes disponibles:
  - GET / (accueil)
  - GET /404 (erreur simulée)
  - GET /health (santé de l'app)`);
});

// Gestion propre de l'arrêt
process.on('SIGTERM', () => {
  console.log('🛑 Signal SIGTERM reçu - Arrêt propre du serveur');
  server.close(() => {
    console.log('✅ Serveur fermé proprement');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('🛑 Signal SIGINT reçu - Arrêt propre du serveur');
  server.close(() => {
    console.log('✅ Serveur fermé proprement');
    process.exit(0);
  });
});

// Démarrage du serveur
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Application demo-pod-app démarrée`);
  console.log(`🌐 Serveur en écoute sur http://0.0.0.0:${PORT}`);
  console.log(`📋 Endpoints disponibles:`);
  console.log(`   - GET / (accueil)`);
  console.log(`   - GET /404 (erreur simulée avec exit(1))`);
  console.log(`   - GET /health (santé de l'application)`);
  console.log(`🐳 Prêt pour Kubernetes !`);
});
