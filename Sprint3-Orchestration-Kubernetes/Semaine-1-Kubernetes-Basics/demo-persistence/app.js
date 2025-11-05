const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'data', 'technologies.txt');
const DATA_DIR = path.join(__dirname, 'data');

// Middleware pour parser JSON
app.use(express.json());

// Créer le dossier data s'il n'existe pas
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, {recursive: true});
  console.log('Dossier data créé');
}

// Créer le fichier technologies.txt s'il n'existe pas
if (!fs.existsSync(DATA_FILE)) {
  fs.writeFileSync(DATA_FILE, '');
  console.log('Fichier technologies.txt créé');
}

// Endpoint pour ajouter une technologie (POST)
app.post('/technologies', (req, res) => {
  try {
    const {technology} = req.body;

    if (!technology) {
      return res.status(400).json({
        error: 'Le champ "technology" est requis'
      });
    }

    // Lire le contenu existant
    let existingTechnologies = [];
    if (fs.existsSync(DATA_FILE)) {
      const content = fs.readFileSync(DATA_FILE, 'utf8');
      if (content.trim()) {
        existingTechnologies = content.trim().split('\n');
      }
    }

    // Vérifier si la technologie existe déjà
    if (existingTechnologies.includes(technology)) {
      return res.status(409).json({
        error: 'Cette technologie existe déjà'
      });
    }

    // Ajouter la nouvelle technologie
    existingTechnologies.push(technology);

    // Écrire dans le fichier
    fs.writeFileSync(DATA_FILE, existingTechnologies.join('\n') + '\n');

    console.log(`Technologie ajoutée: ${technology}`);

    res.status(201).json({
      message: 'Technologie ajoutée avec succès',
      technology: technology,
      total: existingTechnologies.length
    });
  } catch (error) {
    console.error("Erreur lors de l'ajout:", error);
    res.status(500).json({
      error: 'Erreur interne du serveur'
    });
  }
});

// Endpoint pour récupérer toutes les technologies (GET)
app.get('/technologies', (req, res) => {
  try {
    let technologies = [];

    if (fs.existsSync(DATA_FILE)) {
      const content = fs.readFileSync(DATA_FILE, 'utf8');
      if (content.trim()) {
        technologies = content.trim().split('\n');
      }
    }

    console.log(`Nombre de technologies récupérées: ${technologies.length}`);

    res.json({
      technologies: technologies,
      count: technologies.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Erreur lors de la lecture:', error);
    res.status(500).json({
      error: 'Erreur interne du serveur'
    });
  }
});

// Endpoint pour supprimer toutes les technologies (DELETE)
app.delete('/technologies', (req, res) => {
  try {
    if (fs.existsSync(DATA_FILE)) {
      fs.writeFileSync(DATA_FILE, '');
      console.log('Toutes les technologies ont été supprimées');
    }

    res.json({
      message: 'Toutes les technologies ont été supprimées'
    });
  } catch (error) {
    console.error('Erreur lors de la suppression:', error);
    res.status(500).json({
      error: 'Erreur interne du serveur'
    });
  }
});

// Endpoint de santé
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    dataFile: fs.existsSync(DATA_FILE) ? 'exists' : 'missing'
  });
});

// Endpoint racine
app.get('/', (req, res) => {
  res.json({
    message: 'API de démonstration de persistance Kubernetes',
    endpoints: {
      'POST /technologies': 'Ajouter une technologie',
      'GET /technologies': 'Récupérer toutes les technologies',
      'DELETE /technologies': 'Supprimer toutes les technologies',
      'GET /health': "Vérifier l'état de l'application"
    },
    example: {
      post: {
        url: '/technologies',
        body: {technology: 'Kubernetes'}
      }
    }
  });
});

app.get('/error', () => {
  process.exit(1);
});

// Gestionnaire d'erreur global
app.use((err, req, res, next) => {
  console.error('Erreur non gérée:', err);
  res.status(500).json({
    error: 'Erreur interne du serveur'
  });
});

// Démarrer le serveur
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
  console.log(`Fichier de données: ${DATA_FILE}`);
  console.log(`Endpoints disponibles:`);
  console.log(`   POST http://localhost:${PORT}/technologies`);
  console.log(`   GET  http://localhost:${PORT}/technologies`);
  console.log(`   DELETE http://localhost:${PORT}/technologies`);
  console.log(`   GET  http://localhost:${PORT}/health`);
});
