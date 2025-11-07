const express = require('express');
const mysql = require('mysql2/promise');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const Joi = require('joi');

const app = express();
const PORT = process.env.PORT || 3001;

// Configuration base de données
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 3306,
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || 'password',
  database: process.env.DB_NAME || 'dondesang',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

let pool;

// Middlewares
app.use(helmet());
app.use(cors());
app.use(express.json({limit: '10mb'}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limite à 100 requêtes par IP
  message: 'Trop de requêtes depuis cette IP'
});
app.use(limiter);

// Schémas de validation Joi
const userRegistrationSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(6).required(),
  first_name: Joi.string().min(2).max(100).required(),
  last_name: Joi.string().min(2).max(100).required(),
  phone: Joi.string()
    .pattern(/^[+]?[\d\s-()]+$/)
    .optional(),
  birth_date: Joi.date().max('now').required(),
  blood_type: Joi.string()
    .valid('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    .optional(),
  gender: Joi.string().valid('M', 'F', 'Other').optional(),
  address: Joi.string().max(255).optional(),
  city: Joi.string().max(100).optional(),
  postal_code: Joi.string().max(20).optional()
});

const medicalProfileSchema = Joi.object({
  weight: Joi.number().positive().max(300).optional(),
  height: Joi.number().positive().max(250).optional(),
  medical_conditions: Joi.string().optional(),
  medications: Joi.string().optional(),
  allergies: Joi.string().optional(),
  eligible_to_donate: Joi.boolean().optional()
});

// Connexion base de données
async function initDatabase() {
  try {
    pool = mysql.createPool(dbConfig);
    console.log('🗄️  Connexion à MySQL établie (User Service)');
  } catch (error) {
    console.error('❌ Erreur connexion MySQL:', error);
    process.exit(1);
  }
}

// Middleware d'authentification
async function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({error: "Token d'accès requis"});
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret_key');
    req.userId = decoded.userId;
    next();
  } catch (error) {
    return res.status(403).json({error: 'Token invalide'});
  }
}

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'User Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

app.get('/api/users/health', (req, res) => {
  res.json({
    service: 'User Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Inscription utilisateur
app.post('/api/users/register', async (req, res) => {
  try {
    const {error, value} = userRegistrationSchema.validate(req.body);
    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {
      email,
      password,
      first_name,
      last_name,
      phone,
      birth_date,
      blood_type,
      gender,
      address,
      city,
      postal_code
    } = value;

    // Vérifier si l'email existe déjà
    const [existingUser] = await pool.execute(
      'SELECT id FROM users WHERE email = ?',
      [email]
    );

    if (existingUser.length > 0) {
      return res.status(409).json({error: 'Email déjà utilisé'});
    }

    // Hasher le mot de passe
    const password_hash = await bcrypt.hash(password, 10);

    // Insérer l'utilisateur
    const [result] = await pool.execute(
      `INSERT INTO users (email, password_hash, first_name, last_name, phone, birth_date, blood_type, gender, address, city, postal_code)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        email,
        password_hash,
        first_name,
        last_name,
        phone,
        birth_date,
        blood_type,
        gender,
        address,
        city,
        postal_code
      ]
    );

    // Créer le profil médical par défaut
    await pool.execute('INSERT INTO medical_profiles (user_id) VALUES (?)', [
      result.insertId
    ]);

    // Générer le token JWT pour connexion automatique
    const token = jwt.sign(
      {userId: result.insertId, email: email},
      process.env.JWT_SECRET || 'secret_key',
      {expiresIn: '24h'}
    );

    res.status(201).json({
      message: 'Utilisateur créé avec succès',
      token,
      user: {
        id: result.insertId,
        email: email,
        first_name: first_name,
        last_name: last_name
      }
    });
  } catch (error) {
    console.error('Erreur inscription:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir profil utilisateur authentifié
app.get('/api/users/profile', authenticateToken, async (req, res) => {
  try {
    const userId = req.userId;

    const [users] = await pool.execute(
      `SELECT u.id, u.email, u.first_name, u.last_name, u.phone, u.birth_date, 
              u.blood_type, u.gender, u.address, u.city, u.postal_code, u.created_at,
              mp.weight, mp.height, mp.medical_conditions, mp.medications, mp.allergies,
              mp.eligible_to_donate, mp.last_donation_date
       FROM users u
       LEFT JOIN medical_profiles mp ON u.id = mp.user_id
       WHERE u.id = ?`,
      [userId]
    );

    if (users.length === 0) {
      return res.status(404).json({error: 'Utilisateur non trouvé'});
    }

    res.json(users[0]);
  } catch (error) {
    console.error('Erreur récupération profil:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Connexion utilisateur
app.post('/api/users/login', async (req, res) => {
  try {
    const {email, password} = req.body;

    if (!email || !password) {
      return res.status(400).json({error: 'Email et mot de passe requis'});
    }

    // Récupérer l'utilisateur
    const [users] = await pool.execute(
      'SELECT id, email, password_hash, first_name, last_name FROM users WHERE email = ?',
      [email]
    );

    if (users.length === 0) {
      return res.status(401).json({error: 'Identifiants invalides'});
    }

    const user = users[0];

    // Vérifier le mot de passe
    const isValidPassword = await bcrypt.compare(password, user.password_hash);
    if (!isValidPassword) {
      return res.status(401).json({error: 'Identifiants invalides'});
    }

    // Générer le token JWT
    const token = jwt.sign(
      {userId: user.id, email: user.email},
      process.env.JWT_SECRET || 'secret_key',
      {expiresIn: '24h'}
    );

    res.json({
      message: 'Connexion réussie',
      token,
      user: {
        id: user.id,
        email: user.email,
        first_name: user.first_name,
        last_name: user.last_name
      }
    });
  } catch (error) {
    console.error('Erreur connexion:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir profil utilisateur
app.get('/api/users/profile/:id', authenticateToken, async (req, res) => {
  try {
    const userId = req.params.id;

    // Vérifier que l'utilisateur accède à son propre profil ou est admin
    if (req.userId !== parseInt(userId)) {
      return res.status(403).json({error: 'Accès non autorisé'});
    }

    const [users] = await pool.execute(
      `SELECT u.id, u.email, u.first_name, u.last_name, u.phone, u.birth_date, 
              u.blood_type, u.gender, u.address, u.city, u.postal_code, u.created_at,
              mp.weight, mp.height, mp.medical_conditions, mp.medications, mp.allergies,
              mp.eligible_to_donate, mp.last_donation_date
       FROM users u
       LEFT JOIN medical_profiles mp ON u.id = mp.user_id
       WHERE u.id = ?`,
      [userId]
    );

    if (users.length === 0) {
      return res.status(404).json({error: 'Utilisateur non trouvé'});
    }

    res.json({user: users[0]});
  } catch (error) {
    console.error('Erreur récupération profil:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Mettre à jour profil utilisateur
app.put('/api/users/profile/:id', authenticateToken, async (req, res) => {
  try {
    const userId = req.params.id;

    if (req.userId !== parseInt(userId)) {
      return res.status(403).json({error: 'Accès non autorisé'});
    }

    const {first_name, last_name, phone, address, city, postal_code} = req.body;

    await pool.execute(
      `UPDATE users SET first_name = ?, last_name = ?, phone = ?, address = ?, city = ?, postal_code = ?, updated_at = NOW()
       WHERE id = ?`,
      [first_name, last_name, phone, address, city, postal_code, userId]
    );

    res.json({message: 'Profil mis à jour avec succès'});
  } catch (error) {
    console.error('Erreur mise à jour profil:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir profil médical
app.get(
  '/api/users/:id/medical-profile',
  authenticateToken,
  async (req, res) => {
    try {
      const userId = req.params.id;

      if (req.userId !== parseInt(userId)) {
        return res.status(403).json({error: 'Accès non autorisé'});
      }

      const [profiles] = await pool.execute(
        'SELECT * FROM medical_profiles WHERE user_id = ?',
        [userId]
      );

      if (profiles.length === 0) {
        return res.status(404).json({error: 'Profil médical non trouvé'});
      }

      res.json({medical_profile: profiles[0]});
    } catch (error) {
      console.error('Erreur récupération profil médical:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Mettre à jour profil médical
app.put(
  '/api/users/:id/medical-profile',
  authenticateToken,
  async (req, res) => {
    try {
      const userId = req.params.id;

      if (req.userId !== parseInt(userId)) {
        return res.status(403).json({error: 'Accès non autorisé'});
      }

      const {error, value} = medicalProfileSchema.validate(req.body);
      if (error) {
        return res.status(400).json({error: error.details[0].message});
      }

      const {
        weight,
        height,
        medical_conditions,
        medications,
        allergies,
        eligible_to_donate
      } = value;

      await pool.execute(
        `UPDATE medical_profiles 
       SET weight = ?, height = ?, medical_conditions = ?, medications = ?, allergies = ?, eligible_to_donate = ?, updated_at = NOW()
       WHERE user_id = ?`,
        [
          weight,
          height,
          medical_conditions,
          medications,
          allergies,
          eligible_to_donate,
          userId
        ]
      );

      res.json({message: 'Profil médical mis à jour avec succès'});
    } catch (error) {
      console.error('Erreur mise à jour profil médical:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Obtenir historique des dons
app.get(
  '/api/users/:id/donation-history',
  authenticateToken,
  async (req, res) => {
    try {
      const userId = req.params.id;

      if (req.userId !== parseInt(userId)) {
        return res.status(403).json({error: 'Accès non autorisé'});
      }

      const [donations] = await pool.execute(
        `SELECT dh.*, c.name as campaign_name, c.location_name
       FROM donation_history dh
       LEFT JOIN appointments a ON dh.appointment_id = a.id
       LEFT JOIN campaigns c ON a.campaign_id = c.id
       WHERE dh.user_id = ?
       ORDER BY dh.donation_date DESC`,
        [userId]
      );

      res.json({donations});
    } catch (error) {
      console.error('Erreur récupération historique:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Liste des utilisateurs (pour admin)
app.get('/api/users', async (req, res) => {
  try {
    const {page = 1, limit = 10, search = ''} = req.query;
    const offset = (page - 1) * limit;

    let query = `
      SELECT u.id, u.email, u.first_name, u.last_name, u.phone, u.blood_type, 
             u.city, u.created_at, mp.eligible_to_donate,
             COUNT(dh.id) as total_donations
      FROM users u
      LEFT JOIN medical_profiles mp ON u.id = mp.user_id
      LEFT JOIN donation_history dh ON u.id = dh.user_id
    `;

    let queryParams = [];

    if (search) {
      query += ` WHERE u.first_name LIKE ? OR u.last_name LIKE ? OR u.email LIKE ?`;
      queryParams = [`%${search}%`, `%${search}%`, `%${search}%`];
    }

    query += ` GROUP BY u.id ORDER BY u.created_at DESC LIMIT ? OFFSET ?`;
    queryParams.push(parseInt(limit), parseInt(offset));

    const [users] = await pool.execute(query, queryParams);

    // Compter le total
    let countQuery = 'SELECT COUNT(*) as total FROM users';
    let countParams = [];

    if (search) {
      countQuery += ` WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?`;
      countParams = [`%${search}%`, `%${search}%`, `%${search}%`];
    }

    const [countResult] = await pool.execute(countQuery, countParams);
    const total = countResult[0].total;

    res.json({
      users,
      pagination: {
        current_page: parseInt(page),
        per_page: parseInt(limit),
        total,
        total_pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('Erreur récupération utilisateurs:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Démarrer le serveur
async function startServer() {
  await initDatabase();

  app.listen(PORT, () => {
    console.log(`🚀 User Service démarré sur le port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
  });
}

startServer().catch((error) => {
  console.error('❌ Erreur démarrage serveur:', error);
  process.exit(1);
});
