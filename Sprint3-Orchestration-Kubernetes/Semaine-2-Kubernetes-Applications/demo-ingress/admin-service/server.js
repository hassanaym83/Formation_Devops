const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const Joi = require('joi');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const moment = require('moment');
const {v4: uuidv4} = require('uuid');
const multer = require('multer');

const app = express();
const PORT = process.env.PORT || 3005;

// Configuration
const JWT_SECRET = process.env.JWT_SECRET || 'admin_jwt_secret_key_very_secure';
const JWT_EXPIRES_IN = '24h';

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

// Rate limiting plus strict pour l'admin
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 50,
  message: 'Trop de requêtes depuis cette IP'
});
app.use(limiter);

// Configuration multer pour upload de fichiers
const upload = multer({
  dest: 'uploads/',
  limits: {fileSize: 10 * 1024 * 1024}, // 10MB
  fileFilter: (req, file, cb) => {
    if (
      file.mimetype.startsWith('image/') ||
      file.mimetype === 'application/pdf'
    ) {
      cb(null, true);
    } else {
      cb(new Error('Type de fichier non autorisé'));
    }
  }
});

// Schémas de validation
const adminLoginSchema = Joi.object({
  username: Joi.string().required(),
  password: Joi.string().required()
});

const adminCreateSchema = Joi.object({
  username: Joi.string().alphanum().min(3).max(30).required(),
  email: Joi.string().email().required(),
  first_name: Joi.string().max(50).required(),
  last_name: Joi.string().max(50).required(),
  role: Joi.string().valid('super_admin', 'admin', 'moderator').required(),
  permissions: Joi.array().items(Joi.string()).optional()
});

const userUpdateSchema = Joi.object({
  first_name: Joi.string().max(50).optional(),
  last_name: Joi.string().max(50).optional(),
  email: Joi.string().email().optional(),
  phone: Joi.string().max(20).optional(),
  address: Joi.string().max(200).optional(),
  city: Joi.string().max(50).optional(),
  postal_code: Joi.string().max(10).optional(),
  is_active: Joi.boolean().optional()
});

// Connexion base de données
async function initDatabase() {
  try {
    pool = mysql.createPool(dbConfig);
    console.log('🗄️  Connexion à MySQL établie (Admin Service)');
  } catch (error) {
    console.error('❌ Erreur connexion MySQL:', error);
    process.exit(1);
  }
}

// Middleware d'authentification admin
async function authenticateAdmin(req, res, next) {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({error: "Token d'accès requis"});
    }

    const decoded = jwt.verify(token, JWT_SECRET);

    const [admins] = await pool.execute(
      'SELECT * FROM admin_users WHERE id = ? AND is_active = 1',
      [decoded.userId]
    );

    if (admins.length === 0) {
      return res.status(401).json({error: 'Admin non trouvé ou désactivé'});
    }

    req.admin = admins[0];
    next();
  } catch (error) {
    res.status(401).json({error: 'Token invalide'});
  }
}

// Middleware de vérification des permissions
function requirePermission(permission) {
  return (req, res, next) => {
    if (req.admin.role === 'super_admin') {
      return next(); // Super admin a toutes les permissions
    }

    const permissions = JSON.parse(req.admin.permissions || '[]');
    if (!permissions.includes(permission)) {
      return res.status(403).json({error: 'Permission insuffisante'});
    }

    next();
  };
}

// Utilitaires
function logAdminAction(
  admin_id,
  action,
  target_type,
  target_id,
  details = null
) {
  pool
    .execute(
      'INSERT INTO audit_logs (admin_id, action, target_type, target_id, new_values) VALUES (?, ?, ?, ?, ?)',
      [admin_id, action, target_type, target_id, JSON.stringify(details)]
    )
    .catch((error) => console.error('Erreur log audit:', error));
}

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'Admin Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Connexion admin
app.post('/api/admin/login', async (req, res) => {
  try {
    const {error, value} = adminLoginSchema.validate(req.body);
    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {username, password} = value;

    const [admins] = await pool.execute(
      'SELECT * FROM admin_users WHERE username = ? AND is_active = 1',
      [username]
    );

    if (admins.length === 0) {
      return res.status(401).json({error: 'Identifiants invalides'});
    }

    const admin = admins[0];
    const isValidPassword = await bcrypt.compare(password, admin.password_hash);

    if (!isValidPassword) {
      return res.status(401).json({error: 'Identifiants invalides'});
    }

    const token = jwt.sign({userId: admin.id, role: admin.role}, JWT_SECRET, {
      expiresIn: JWT_EXPIRES_IN
    });

    // Mettre à jour la dernière connexion
    await pool.execute(
      'UPDATE admin_users SET last_login = NOW() WHERE id = ?',
      [admin.id]
    );

    logAdminAction(admin.id, 'login', 'admin', admin.id);

    res.json({
      message: 'Connexion réussie',
      token,
      admin: {
        id: admin.id,
        username: admin.username,
        first_name: admin.first_name,
        last_name: admin.last_name,
        role: admin.role,
        permissions: admin.permissions
          ? typeof admin.permissions === 'string'
            ? JSON.parse(admin.permissions)
            : admin.permissions
          : []
      }
    });
  } catch (error) {
    console.error('Erreur connexion admin:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Dashboard administrateur
app.get('/api/admin/dashboard', authenticateAdmin, async (req, res) => {
  try {
    // Statistiques générales
    const [stats] = await pool.execute(`
      SELECT 
        (SELECT COUNT(*) FROM users) as total_users,
        (SELECT COUNT(*) FROM campaigns) as total_campaigns,
        (SELECT COUNT(*) FROM appointments WHERE DATE(created_at) = CURDATE()) as today_appointments,
        (SELECT COUNT(*) FROM donation_history WHERE DATE(donation_date) = CURDATE()) as today_donations,
        (SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURDATE()) as today_new_users,
        (SELECT COUNT(*) FROM campaigns WHERE status = 'active') as active_campaigns,
        (SELECT COUNT(*) FROM appointments WHERE status = 'booked') as pending_appointments
    `);

    // Activité récente
    const [recentActivity] = await pool.execute(`
      SELECT 
        'user_registration' as type,
        CONCAT(first_name, ' ', last_name) as description,
        created_at as timestamp
      FROM users 
      WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
      
      UNION ALL
      
      SELECT 
        'campaign_created' as type,
        name as description,
        created_at as timestamp
      FROM campaigns 
      WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
      
      UNION ALL
      
      SELECT 
        'donation_completed' as type,
        CONCAT('Don de ', volume_ml, 'ml') as description,
        created_at as timestamp
      FROM donation_history 
      WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
      
      ORDER BY timestamp DESC
      LIMIT 10
    `);

    // Alertes système
    const alerts = [];

    // Vérifier les campagnes sans créneaux
    const [campaignsWithoutSlots] = await pool.execute(`
      SELECT c.id, c.name 
      FROM campaigns c 
      LEFT JOIN time_slots ts ON c.id = ts.campaign_id 
      WHERE c.status = 'active' AND ts.id IS NULL
    `);

    if (campaignsWithoutSlots.length > 0) {
      alerts.push({
        type: 'warning',
        message: `${campaignsWithoutSlots.length} campagne(s) active(s) sans créneaux`,
        action: 'Ajouter des créneaux'
      });
    }

    // Vérifier les créneaux surbookés
    const [overbookedSlots] = await pool.execute(`
      SELECT COUNT(*) as count
      FROM time_slots ts
      JOIN (
        SELECT time_slot_id, COUNT(*) as bookings
        FROM appointments 
        WHERE status IN ('booked', 'confirmed')
        GROUP BY time_slot_id
      ) a ON ts.id = a.time_slot_id
      WHERE a.bookings > ts.capacity
    `);

    if (overbookedSlots[0].count > 0) {
      alerts.push({
        type: 'error',
        message: `${overbookedSlots[0].count} créneau(x) surbooké(s)`,
        action: 'Vérifier les réservations'
      });
    }

    res.json({
      statistics: stats[0],
      recent_activity: recentActivity,
      system_alerts: alerts
    });
  } catch (error) {
    console.error('Erreur dashboard admin:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Gestion des utilisateurs - Liste
app.get(
  '/api/admin/users',
  authenticateAdmin,
  requirePermission('manage_users'),
  async (req, res) => {
    try {
      const {page = 1, limit = 20, search = '', status = ''} = req.query;
      const offset = (page - 1) * limit;

      let query = `
      SELECT 
        u.*,
        mp.blood_group,
        mp.eligible_to_donate,
        mp.last_donation_date,
        (SELECT COUNT(*) FROM donation_history WHERE user_id = u.id) as total_donations
      FROM users u
      LEFT JOIN medical_profiles mp ON u.id = mp.user_id
      WHERE 1=1
    `;

      let queryParams = [];

      if (search) {
        query += ` AND (u.first_name LIKE ? OR u.last_name LIKE ? OR u.email LIKE ?)`;
        queryParams.push(`%${search}%`, `%${search}%`, `%${search}%`);
      }

      if (status === 'active') {
        query += ` AND u.is_active = 1`;
      } else if (status === 'inactive') {
        query += ` AND u.is_active = 0`;
      }

      query += ` ORDER BY u.created_at DESC LIMIT ? OFFSET ?`;
      queryParams.push(parseInt(limit), parseInt(offset));

      const [users] = await pool.execute(query, queryParams);

      // Compter le total
      let countQuery = 'SELECT COUNT(*) as total FROM users u WHERE 1=1';
      let countParams = [];

      if (search) {
        countQuery += ` AND (first_name LIKE ? OR last_name LIKE ? OR email LIKE ?)`;
        countParams.push(`%${search}%`, `%${search}%`, `%${search}%`);
      }

      if (status === 'active') {
        countQuery += ` AND is_active = 1`;
      } else if (status === 'inactive') {
        countQuery += ` AND is_active = 0`;
      }

      const [countResult] = await pool.execute(countQuery, countParams);

      res.json({
        users,
        pagination: {
          current_page: parseInt(page),
          per_page: parseInt(limit),
          total: countResult[0].total,
          total_pages: Math.ceil(countResult[0].total / limit)
        }
      });
    } catch (error) {
      console.error('Erreur récupération utilisateurs:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Gestion des utilisateurs - Détails
app.get(
  '/api/admin/users/:id',
  authenticateAdmin,
  requirePermission('manage_users'),
  async (req, res) => {
    try {
      const {id} = req.params;

      const [users] = await pool.execute(
        `
      SELECT 
        u.*,
        mp.*
      FROM users u
      LEFT JOIN medical_profiles mp ON u.id = mp.user_id
      WHERE u.id = ?
    `,
        [id]
      );

      if (users.length === 0) {
        return res.status(404).json({error: 'Utilisateur non trouvé'});
      }

      // Historique des dons
      const [donations] = await pool.execute(
        `
      SELECT 
        dh.*,
        c.name as campaign_name,
        c.location_name
      FROM donation_history dh
      LEFT JOIN appointments a ON dh.appointment_id = a.id
      LEFT JOIN campaigns c ON a.campaign_id = c.id
      WHERE dh.user_id = ?
      ORDER BY dh.donation_date DESC
    `,
        [id]
      );

      // Rendez-vous à venir
      const [upcomingAppointments] = await pool.execute(
        `
      SELECT 
        a.*,
        c.name as campaign_name,
        c.location_name,
        ts.slot_datetime
      FROM appointments a
      JOIN campaigns c ON a.campaign_id = c.id
      JOIN time_slots ts ON a.time_slot_id = ts.id
      WHERE a.user_id = ? AND ts.slot_datetime > NOW()
      ORDER BY ts.slot_datetime ASC
    `,
        [id]
      );

      res.json({
        user: users[0],
        donation_history: donations,
        upcoming_appointments: upcomingAppointments
      });
    } catch (error) {
      console.error('Erreur détails utilisateur:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Gestion des utilisateurs - Modification
app.put(
  '/api/admin/users/:id',
  authenticateAdmin,
  requirePermission('manage_users'),
  async (req, res) => {
    try {
      const {id} = req.params;
      const {error, value} = userUpdateSchema.validate(req.body);

      if (error) {
        return res.status(400).json({error: error.details[0].message});
      }

      const updateFields = [];
      const updateValues = [];

      Object.keys(value).forEach((key) => {
        updateFields.push(`${key} = ?`);
        updateValues.push(value[key]);
      });

      if (updateFields.length === 0) {
        return res.status(400).json({error: 'Aucune donnée à modifier'});
      }

      updateValues.push(id);

      await pool.execute(
        `UPDATE users SET ${updateFields.join(
          ', '
        )}, updated_at = NOW() WHERE id = ?`,
        updateValues
      );

      logAdminAction(req.admin.id, 'user_update', 'user', id, value);

      res.json({message: 'Utilisateur mis à jour avec succès'});
    } catch (error) {
      console.error('Erreur modification utilisateur:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Gestion des campagnes - Liste avec actions admin
app.get(
  '/api/admin/campaigns',
  authenticateAdmin,
  requirePermission('manage_campaigns'),
  async (req, res) => {
    try {
      const {page = 1, limit = 20, status = '', city = ''} = req.query;
      const offset = (page - 1) * limit;

      let query = `
      SELECT 
        c.*,
        COUNT(DISTINCT ts.id) as total_slots,
        COUNT(DISTINCT a.id) as total_appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations,
        (SELECT COUNT(*) FROM appointments aa 
         JOIN time_slots tts ON aa.time_slot_id = tts.id 
         WHERE tts.campaign_id = c.id AND aa.status IN ('booked', 'confirmed')) as active_appointments
      FROM campaigns c
      LEFT JOIN time_slots ts ON c.id = ts.campaign_id
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE 1=1
    `;

      let queryParams = [];

      if (status) {
        query += ` AND c.status = ?`;
        queryParams.push(status);
      }

      if (city) {
        query += ` AND c.city LIKE ?`;
        queryParams.push(`%${city}%`);
      }

      query += ` GROUP BY c.id ORDER BY c.created_at DESC LIMIT ? OFFSET ?`;
      queryParams.push(parseInt(limit), parseInt(offset));

      const [campaigns] = await pool.execute(query, queryParams);

      res.json({campaigns});
    } catch (error) {
      console.error('Erreur récupération campagnes admin:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Suspendre/Réactiver un utilisateur
app.put(
  '/api/admin/users/:id/toggle-status',
  authenticateAdmin,
  requirePermission('manage_users'),
  async (req, res) => {
    try {
      const {id} = req.params;

      const [users] = await pool.execute(
        'SELECT is_active FROM users WHERE id = ?',
        [id]
      );

      if (users.length === 0) {
        return res.status(404).json({error: 'Utilisateur non trouvé'});
      }

      const newStatus = !users[0].is_active;

      await pool.execute(
        'UPDATE users SET is_active = ?, updated_at = NOW() WHERE id = ?',
        [newStatus, id]
      );

      logAdminAction(
        req.admin.id,
        newStatus ? 'user_activated' : 'user_suspended',
        'user',
        id
      );

      res.json({
        message: `Utilisateur ${
          newStatus ? 'réactivé' : 'suspendu'
        } avec succès`,
        is_active: newStatus
      });
    } catch (error) {
      console.error('Erreur changement statut utilisateur:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Logs d'audit
app.get(
  '/api/admin/audit-logs',
  authenticateAdmin,
  requirePermission('view_audit'),
  async (req, res) => {
    try {
      const {page = 1, limit = 50, action = '', admin_id = ''} = req.query;
      const offset = (page - 1) * limit;

      let query = `
      SELECT 
        al.*,
        au.username,
        au.first_name,
        au.last_name
      FROM audit_logs al
      JOIN admin_users au ON al.admin_id = au.id
      WHERE 1=1
    `;

      let queryParams = [];

      if (action) {
        query += ` AND al.action = ?`;
        queryParams.push(action);
      }

      if (admin_id) {
        query += ` AND al.admin_id = ?`;
        queryParams.push(admin_id);
      }

      query += ` ORDER BY al.created_at DESC LIMIT ? OFFSET ?`;
      queryParams.push(parseInt(limit), parseInt(offset));

      const [logs] = await pool.execute(query, queryParams);

      res.json({audit_logs: logs});
    } catch (error) {
      console.error('Erreur récupération logs audit:', error);
      res.status(500).json({error: 'Erreur interne du serveur'});
    }
  }
);

// Statistiques système avancées
app.get('/api/admin/system-stats', authenticateAdmin, async (req, res) => {
  try {
    // Performance des services (simulation)
    const serviceHealth = {
      'user-service': {
        status: 'healthy',
        response_time: '45ms',
        uptime: '99.9%'
      },
      'campaign-service': {
        status: 'healthy',
        response_time: '32ms',
        uptime: '99.8%'
      },
      'appointment-service': {
        status: 'healthy',
        response_time: '28ms',
        uptime: '99.9%'
      },
      'analytics-service': {
        status: 'healthy',
        response_time: '67ms',
        uptime: '99.7%'
      }
    };

    // Statistiques base de données
    const [dbStats] = await pool.execute(`
      SELECT 
        (SELECT COUNT(*) FROM users) as total_users,
        (SELECT COUNT(*) FROM campaigns) as total_campaigns,
        (SELECT COUNT(*) FROM appointments) as total_appointments,
        (SELECT COUNT(*) FROM donation_history) as total_donations,
        (SELECT COUNT(*) FROM audit_logs) as total_audit_logs
    `);

    res.json({
      service_health: serviceHealth,
      database_stats: dbStats[0],
      system_info: {
        version: '1.0.0',
        last_backup: '2024-01-15T10:30:00Z',
        storage_used: '2.3 GB',
        active_sessions: 12
      }
    });
  } catch (error) {
    console.error('Erreur stats système:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Créer un nouvel admin (super admin uniquement)
app.post('/api/admin/create-admin', authenticateAdmin, async (req, res) => {
  try {
    if (req.admin.role !== 'super_admin') {
      return res
        .status(403)
        .json({error: 'Seul un super admin peut créer des admins'});
    }

    const {error, value} = adminCreateSchema.validate(req.body);
    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {username, email, first_name, last_name, role, permissions} = value;

    // Vérifier unicité
    const [existing] = await pool.execute(
      'SELECT id FROM admin_users WHERE username = ? OR email = ?',
      [username, email]
    );

    if (existing.length > 0) {
      return res
        .status(409)
        .json({error: "Nom d'utilisateur ou email déjà utilisé"});
    }

    // Générer mot de passe temporaire
    const tempPassword = uuidv4().split('-')[0];
    const hashedPassword = await bcrypt.hash(tempPassword, 10);

    const [result] = await pool.execute(
      `
      INSERT INTO admin_users (username, email, first_name, last_name, password_hash, role, permissions)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `,
      [
        username,
        email,
        first_name,
        last_name,
        hashedPassword,
        role,
        JSON.stringify(permissions || [])
      ]
    );

    logAdminAction(req.admin.id, 'admin_created', 'admin', result.insertId, {
      username,
      role
    });

    res.status(201).json({
      message: 'Administrateur créé avec succès',
      admin_id: result.insertId,
      temporary_password: tempPassword,
      note: 'Le mot de passe temporaire doit être changé à la première connexion'
    });
  } catch (error) {
    console.error('Erreur création admin:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Démarrer le serveur
async function startServer() {
  await initDatabase();

  app.listen(PORT, () => {
    console.log(`🚀 Admin Service démarré sur le port ${PORT}`);
    console.log(`🔐 Health check: http://localhost:${PORT}/health`);
    console.log(`👨‍💼 Login: POST http://localhost:${PORT}/api/admin/login`);
  });
}

startServer().catch((error) => {
  console.error('❌ Erreur démarrage serveur:', error);
  process.exit(1);
});
