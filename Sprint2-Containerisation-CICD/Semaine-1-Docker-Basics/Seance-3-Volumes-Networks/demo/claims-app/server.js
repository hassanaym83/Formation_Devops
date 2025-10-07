const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');
const fs = require('fs').promises;
const {v4: uuidv4} = require('uuid');
const {body, validationResult} = require('express-validator');

const app = express();
const PORT = process.env.PORT || 3000;

// Répertoires pour les données (relatifs au projet)
const TEMP_DIR = path.join(__dirname, 'tmp', 'claims');
const PERSIST_DIR = path.join(__dirname, 'persist', 'claims');
const VALIDATED_DIR = path.join(PERSIST_DIR, 'validated');
const ARCHIVED_DIR = path.join(PERSIST_DIR, 'archived');

// Middleware de sécurité et logging
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({limit: '10mb'}));
app.use(express.urlencoded({extended: true}));

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Initialisation des répertoires
async function initializeDirectories() {
  const directories = [TEMP_DIR, PERSIST_DIR, VALIDATED_DIR, ARCHIVED_DIR];

  for (const dir of directories) {
    try {
      await fs.access(dir);
      console.log(`Répertoire existant: ${dir}`);
    } catch (error) {
      try {
        await fs.mkdir(dir, {recursive: true});
        console.log(`Répertoire créé: ${dir}`);
      } catch (createError) {
        console.error(
          `Erreur création répertoire ${dir}:`,
          createError.message
        );
      }
    }
  }
}

// Utilitaires pour gestion des fichiers
function generateClaimFilename(reclamateur, date = new Date()) {
  const sanitizedName = reclamateur
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '_')
    .replace(/_+/g, '_');

  const timestamp = date
    .toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .split('.')[0];

  return `${sanitizedName}_${timestamp}.json`;
}

async function saveClaimToFile(claim, directory) {
  const filename = generateClaimFilename(
    claim.reclamateur,
    new Date(claim.date_soumission)
  );
  const filepath = path.join(directory, filename);

  try {
    await fs.writeFile(filepath, JSON.stringify(claim, null, 2), 'utf8');
    return {success: true, filename, filepath};
  } catch (error) {
    console.error('Erreur sauvegarde:', error);
    return {success: false, error: error.message};
  }
}

async function readClaimsFromDirectory(directory) {
  try {
    const files = await fs.readdir(directory);
    const jsonFiles = files.filter((file) => file.endsWith('.json'));

    const claims = [];
    for (const file of jsonFiles) {
      try {
        const content = await fs.readFile(path.join(directory, file), 'utf8');
        const claim = JSON.parse(content);
        claim.filename = file;
        claims.push(claim);
      } catch (parseError) {
        console.error(`Erreur lecture fichier ${file}:`, parseError.message);
      }
    }

    return claims.sort(
      (a, b) => new Date(b.date_soumission) - new Date(a.date_soumission)
    );
  } catch (error) {
    console.error('Erreur lecture répertoire:', error);
    return [];
  }
}

// Routes API

// Page d'accueil
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Santé de l'application
app.get('/api/health', async (req, res) => {
  try {
    // Vérification des répertoires
    const tempExists = await fs
      .access(TEMP_DIR)
      .then(() => true)
      .catch(() => false);
    const persistExists = await fs
      .access(PERSIST_DIR)
      .then(() => true)
      .catch(() => false);

    // Statistiques
    const tempClaims = await readClaimsFromDirectory(TEMP_DIR);
    const validatedClaims = await readClaimsFromDirectory(VALIDATED_DIR);

    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      directories: {
        temp: {exists: tempExists, path: TEMP_DIR},
        persist: {exists: persistExists, path: PERSIST_DIR}
      },
      statistics: {
        claims_pending: tempClaims.length,
        claims_validated: validatedClaims.length,
        total_claims: tempClaims.length + validatedClaims.length
      },
      version: process.env.npm_package_version || '1.0.0'
    });
  } catch (error) {
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

// Soumettre une nouvelle réclamation
app.post(
  '/api/claims',
  [
    body('reclamateur')
      .trim()
      .isLength({min: 2, max: 100})
      .withMessage('Nom requis (2-100 caractères)'),
    body('email').isEmail().withMessage('Email valide requis'),
    body('sujet')
      .trim()
      .isLength({min: 5, max: 200})
      .withMessage('Sujet requis (5-200 caractères)'),
    body('description')
      .trim()
      .isLength({min: 10, max: 2000})
      .withMessage('Description requise (10-2000 caractères)'),
    body('priorite')
      .isIn(['basse', 'moyenne', 'haute', 'urgente'])
      .withMessage('Priorité invalide')
  ],
  async (req, res) => {
    try {
      // Validation des données
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          success: false,
          message: 'Données invalides',
          errors: errors.array()
        });
      }

      const {
        reclamateur,
        email,
        sujet,
        description,
        priorite = 'moyenne'
      } = req.body;

      // Création de l'objet réclamation
      const claim = {
        id: uuidv4(),
        reclamateur: reclamateur.trim(),
        email: email.trim().toLowerCase(),
        sujet: sujet.trim(),
        description: description.trim(),
        priorite,
        statut: 'en_attente',
        date_soumission: new Date().toISOString(),
        date_modification: new Date().toISOString()
      };

      // Sauvegarde dans le répertoire temporaire
      const result = await saveClaimToFile(claim, TEMP_DIR);

      if (result.success) {
        console.log(`Nouvelle réclamation: ${result.filename}`);
        res.status(201).json({
          success: true,
          message: 'Réclamation enregistrée avec succès',
          data: {
            id: claim.id,
            filename: result.filename,
            statut: claim.statut,
            date_soumission: claim.date_soumission
          }
        });
      } else {
        res.status(500).json({
          success: false,
          message: "Erreur lors de l'enregistrement",
          error: result.error
        });
      }
    } catch (error) {
      console.error('Erreur soumission réclamation:', error);
      res.status(500).json({
        success: false,
        message: 'Erreur serveur interne',
        error: error.message
      });
    }
  }
);

// Lister les réclamations en attente (temporaires)
app.get('/api/claims/pending', async (req, res) => {
  try {
    const claims = await readClaimsFromDirectory(TEMP_DIR);

    res.json({
      success: true,
      message: `${claims.length} réclamation(s) en attente`,
      data: claims,
      metadata: {
        count: claims.length,
        directory: 'temporaire',
        path: TEMP_DIR
      }
    });
  } catch (error) {
    console.error('Erreur lecture réclamations temporaires:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lecture réclamations',
      error: error.message
    });
  }
});

// Lister les réclamations validées (permanentes)
app.get('/api/claims/validated', async (req, res) => {
  try {
    const claims = await readClaimsFromDirectory(VALIDATED_DIR);

    res.json({
      success: true,
      message: `${claims.length} réclamation(s) validée(s)`,
      data: claims,
      metadata: {
        count: claims.length,
        directory: 'permanente',
        path: VALIDATED_DIR
      }
    });
  } catch (error) {
    console.error('Erreur lecture réclamations validées:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur lecture réclamations',
      error: error.message
    });
  }
});

// Valider une réclamation (transfert temporaire → permanent)
app.post('/api/claims/:filename/validate', async (req, res) => {
  try {
    const {filename} = req.params;
    const {comment = ''} = req.body;

    // Lecture du fichier temporaire
    const tempFilePath = path.join(TEMP_DIR, filename);

    try {
      const content = await fs.readFile(tempFilePath, 'utf8');
      const claim = JSON.parse(content);

      // Mise à jour du statut
      claim.statut = 'validee';
      claim.date_validation = new Date().toISOString();
      claim.date_modification = new Date().toISOString();
      if (comment) {
        claim.commentaire_validation = comment;
      }

      // Sauvegarde dans le répertoire permanent
      const saveResult = await saveClaimToFile(claim, VALIDATED_DIR);

      if (saveResult.success) {
        // Suppression du fichier temporaire
        await fs.unlink(tempFilePath);

        console.log(
          `Réclamation validée: ${filename} → ${saveResult.filename}`
        );
        res.json({
          success: true,
          message: 'Réclamation validée et transférée',
          data: {
            id: claim.id,
            old_filename: filename,
            new_filename: saveResult.filename,
            statut: claim.statut,
            date_validation: claim.date_validation
          }
        });
      } else {
        res.status(500).json({
          success: false,
          message: 'Erreur lors de la validation',
          error: saveResult.error
        });
      }
    } catch (fileError) {
      res.status(404).json({
        success: false,
        message: 'Réclamation non trouvée',
        error: fileError.message
      });
    }
  } catch (error) {
    console.error('Erreur validation réclamation:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur serveur interne',
      error: error.message
    });
  }
});

// Archiver une réclamation validée
app.post('/api/claims/:filename/archive', async (req, res) => {
  try {
    const {filename} = req.params;
    const {comment = ''} = req.body;

    // Lecture du fichier validé
    const validatedFilePath = path.join(VALIDATED_DIR, filename);

    try {
      const content = await fs.readFile(validatedFilePath, 'utf8');
      const claim = JSON.parse(content);

      // Mise à jour du statut
      claim.statut = 'archivee';
      claim.date_archivage = new Date().toISOString();
      claim.date_modification = new Date().toISOString();
      if (comment) {
        claim.commentaire_archivage = comment;
      }

      // Sauvegarde dans le répertoire d'archives
      const saveResult = await saveClaimToFile(claim, ARCHIVED_DIR);

      if (saveResult.success) {
        // Suppression du fichier validé
        await fs.unlink(validatedFilePath);

        console.log(
          `Réclamation archivée: ${filename} → ${saveResult.filename}`
        );
        res.json({
          success: true,
          message: 'Réclamation archivée avec succès',
          data: {
            id: claim.id,
            old_filename: filename,
            new_filename: saveResult.filename,
            statut: claim.statut,
            date_archivage: claim.date_archivage
          }
        });
      } else {
        res.status(500).json({
          success: false,
          message: "Erreur lors de l'archivage",
          error: saveResult.error
        });
      }
    } catch (fileError) {
      res.status(404).json({
        success: false,
        message: 'Réclamation validée non trouvée',
        error: fileError.message
      });
    }
  } catch (error) {
    console.error('Erreur archivage réclamation:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur serveur interne',
      error: error.message
    });
  }
});

// Supprimer une réclamation (temporaire ou validée)
app.delete('/api/claims/:filename', async (req, res) => {
  try {
    const {filename} = req.params;
    const {type = 'temp'} = req.query; // 'temp' ou 'validated'

    let filePath;
    let description;

    if (type === 'validated') {
      filePath = path.join(VALIDATED_DIR, filename);
      description = 'réclamation validée';
    } else {
      filePath = path.join(TEMP_DIR, filename);
      description = 'réclamation temporaire';
    }

    await fs.unlink(filePath);

    console.log(`Réclamation supprimée: ${filename} (${description})`);
    res.json({
      success: true,
      message: `${
        description.charAt(0).toUpperCase() + description.slice(1)
      } supprimée`,
      data: {filename, type}
    });
  } catch (error) {
    if (error.code === 'ENOENT') {
      res.status(404).json({
        success: false,
        message: 'Réclamation non trouvée'
      });
    } else {
      res.status(500).json({
        success: false,
        message: 'Erreur suppression',
        error: error.message
      });
    }
  }
});

// Nettoyage des fichiers temporaires (ancien de plus de 24h)
app.post('/api/claims/cleanup', async (req, res) => {
  try {
    const files = await fs.readdir(TEMP_DIR);
    const jsonFiles = files.filter((file) => file.endsWith('.json'));

    let cleanedCount = 0;
    const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;

    for (const file of jsonFiles) {
      const filePath = path.join(TEMP_DIR, file);
      try {
        const stats = await fs.stat(filePath);
        if (stats.mtime.getTime() < oneDayAgo) {
          await fs.unlink(filePath);
          cleanedCount++;
          console.log(`Fichier nettoyé: ${file}`);
        }
      } catch (statError) {
        console.error(`Erreur nettoyage ${file}:`, statError.message);
      }
    }

    res.json({
      success: true,
      message: `Nettoyage terminé: ${cleanedCount} fichier(s) supprimé(s)`,
      data: {cleaned_count: cleanedCount, total_files: jsonFiles.length}
    });
  } catch (error) {
    console.error('Erreur nettoyage:', error);
    res.status(500).json({
      success: false,
      message: 'Erreur nettoyage',
      error: error.message
    });
  }
});

// Gestion des erreurs 404
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint non trouvé',
    path: req.originalUrl
  });
});

// Middleware de gestion d'erreurs globales
app.use((error, req, res, next) => {
  console.error('Erreur globale:', error);
  res.status(500).json({
    success: false,
    message: 'Erreur serveur interne',
    error:
      process.env.NODE_ENV === 'development' ? error.message : 'Erreur interne'
  });
});

// Démarrage du serveur
async function startServer() {
  try {
    await initializeDirectories();

    app.listen(PORT, '0.0.0.0', () => {
      console.log('='.repeat(60));
      console.log('APPLICATION DE GESTION DES RÉCLAMATIONS');
      console.log('='.repeat(60));
      console.log(`Serveur démarré sur: http://localhost:${PORT}`);
      console.log(`Démarrage: ${new Date().toLocaleString()}`);
      console.log(`Données temporaires: ${TEMP_DIR}`);
      console.log(`Données permanentes: ${PERSIST_DIR}`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log('='.repeat(60));
      console.log('API Endpoints disponibles:');
      console.log('   GET  /                     - Interface web');
      console.log('   GET  /api/health           - Santé application');
      console.log('   POST /api/claims           - Soumettre réclamation');
      console.log('   GET  /api/claims/pending   - Réclamations temporaires');
      console.log('   GET  /api/claims/validated - Réclamations permanentes');
      console.log('   POST /api/claims/:file/validate - Valider réclamation');
      console.log('   POST /api/claims/:file/archive - Archiver réclamation');
      console.log('   DELETE /api/claims/:file   - Supprimer réclamation');
      console.log('   POST /api/claims/cleanup   - Nettoyage automatique');
      console.log('='.repeat(60));
    });
  } catch (error) {
    console.error('Erreur démarrage serveur:', error);
    process.exit(1);
  }
}

// Gestion propre de l'arrêt
process.on('SIGTERM', () => {
  console.log('\nArrêt gracieux du serveur...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('\nArrêt du serveur (Ctrl+C)...');
  process.exit(0);
});

startServer();
