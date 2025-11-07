const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const Joi = require('joi');
const moment = require('moment');

const app = express();
const PORT = process.env.PORT || 3002;

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
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: 'Trop de requêtes depuis cette IP'
});
app.use(limiter);

// Schémas de validation
const campaignSchema = Joi.object({
  name: Joi.string().min(3).max(255).required(),
  description: Joi.string().optional(),
  start_date: Joi.date().min('now').required(),
  end_date: Joi.date().min(Joi.ref('start_date')).required(),
  start_time: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$/)
    .optional(),
  end_time: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$/)
    .optional(),
  location_name: Joi.string().max(255).required(),
  address: Joi.string().optional(),
  city: Joi.string().max(100).required(),
  latitude: Joi.number().min(-90).max(90).optional(),
  longitude: Joi.number().min(-180).max(180).optional(),
  max_capacity: Joi.number().positive().max(1000).default(50),
  blood_types_needed: Joi.array()
    .items(Joi.string().valid('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
    .optional(),
  created_by: Joi.number().positive().optional()
});

// Connexion base de données
async function initDatabase() {
  try {
    pool = mysql.createPool(dbConfig);
    console.log('🗄️  Connexion à MySQL établie (Campaign Service)');
  } catch (error) {
    console.error('❌ Erreur connexion MySQL:', error);
    process.exit(1);
  }
}

// Utilitaire de calcul de distance (formule haversine)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Rayon de la Terre en km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c; // Distance en km
}

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'Campaign Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Obtenir toutes les campagnes avec filtres
app.get('/api/campaigns', async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      status = '',
      city = '',
      blood_type = '',
      start_date = '',
      end_date = ''
    } = req.query;

    const offset = (page - 1) * limit;

    let query = `
      SELECT c.*, 
             COUNT(a.id) as current_registrations,
             (c.max_capacity - COUNT(a.id)) as available_spots
      FROM campaigns c
      LEFT JOIN appointments a ON c.id = a.campaign_id AND a.status IN ('booked', 'confirmed')
    `;

    let whereConditions = [];
    let queryParams = [];

    if (status) {
      whereConditions.push('c.status = ?');
      queryParams.push(status);
    }

    if (city) {
      whereConditions.push('c.city LIKE ?');
      queryParams.push(`%${city}%`);
    }

    if (start_date) {
      whereConditions.push('c.start_date >= ?');
      queryParams.push(start_date);
    }

    if (end_date) {
      whereConditions.push('c.end_date <= ?');
      queryParams.push(end_date);
    }

    if (blood_type) {
      whereConditions.push(
        'JSON_CONTAINS(c.blood_types_needed, JSON_QUOTE(?))'
      );
      queryParams.push(blood_type);
    }

    if (whereConditions.length > 0) {
      query += ' WHERE ' + whereConditions.join(' AND ');
    }

    query += ' GROUP BY c.id ORDER BY c.start_date ASC LIMIT ? OFFSET ?';
    queryParams.push(parseInt(limit), parseInt(offset));

    const [campaigns] = await pool.execute(query, queryParams);

    // Compter le total
    let countQuery = 'SELECT COUNT(*) as total FROM campaigns c';
    let countParams = [];

    if (whereConditions.length > 0) {
      countQuery += ' WHERE ' + whereConditions.join(' AND ');
      countParams = queryParams.slice(0, -2); // Enlever limit et offset
    }

    const [countResult] = await pool.execute(countQuery, countParams);
    const total = countResult[0].total;

    // Parser les blood_types_needed JSON
    campaigns.forEach((campaign) => {
      if (campaign.blood_types_needed) {
        try {
          campaign.blood_types_needed = JSON.parse(campaign.blood_types_needed);
        } catch (e) {
          campaign.blood_types_needed = [];
        }
      }
    });

    res.json({
      campaigns,
      pagination: {
        current_page: parseInt(page),
        per_page: parseInt(limit),
        total,
        total_pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('Erreur récupération campagnes:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir campagnes actives
app.get('/api/campaigns/active', async (req, res) => {
  try {
    const [campaigns] = await pool.execute(`
      SELECT c.*, 
             COUNT(a.id) as current_registrations,
             (c.max_capacity - COUNT(a.id)) as available_spots
      FROM campaigns c
      LEFT JOIN appointments a ON c.id = a.campaign_id AND a.status IN ('booked', 'confirmed')
      WHERE c.status = 'active' 
        AND c.start_date <= CURDATE() 
        AND c.end_date >= CURDATE()
      GROUP BY c.id
      ORDER BY c.start_date ASC
    `);

    campaigns.forEach((campaign) => {
      if (campaign.blood_types_needed) {
        try {
          campaign.blood_types_needed = JSON.parse(campaign.blood_types_needed);
        } catch (e) {
          campaign.blood_types_needed = [];
        }
      }
    });

    res.json({campaigns});
  } catch (error) {
    console.error('Erreur récupération campagnes actives:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir campagnes à proximité
app.get('/api/campaigns/nearby/:lat/:lng', async (req, res) => {
  try {
    const {lat, lng} = req.params;
    const {radius = 50} = req.query; // Rayon en km

    const latitude = parseFloat(lat);
    const longitude = parseFloat(lng);

    if (isNaN(latitude) || isNaN(longitude)) {
      return res.status(400).json({error: 'Coordonnées invalides'});
    }

    const [campaigns] = await pool.execute(`
      SELECT c.*, 
             COUNT(a.id) as current_registrations,
             (c.max_capacity - COUNT(a.id)) as available_spots
      FROM campaigns c
      LEFT JOIN appointments a ON c.id = a.campaign_id AND a.status IN ('booked', 'confirmed')
      WHERE c.status IN ('planned', 'active')
        AND c.latitude IS NOT NULL 
        AND c.longitude IS NOT NULL
      GROUP BY c.id
    `);

    // Calculer la distance et filtrer
    const nearbyCampaigns = campaigns
      .map((campaign) => {
        const distance = calculateDistance(
          latitude,
          longitude,
          campaign.latitude,
          campaign.longitude
        );
        return {...campaign, distance: Math.round(distance * 100) / 100};
      })
      .filter((campaign) => campaign.distance <= radius)
      .sort((a, b) => a.distance - b.distance);

    // Parser JSON
    nearbyCampaigns.forEach((campaign) => {
      if (campaign.blood_types_needed) {
        try {
          campaign.blood_types_needed = JSON.parse(campaign.blood_types_needed);
        } catch (e) {
          campaign.blood_types_needed = [];
        }
      }
    });

    res.json({campaigns: nearbyCampaigns});
  } catch (error) {
    console.error('Erreur recherche campagnes proches:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir une campagne spécifique
app.get('/api/campaigns/:id', async (req, res) => {
  try {
    const campaignId = req.params.id;

    const [campaigns] = await pool.execute(
      `
      SELECT c.*, 
             COUNT(a.id) as current_registrations,
             (c.max_capacity - COUNT(a.id)) as available_spots,
             au.first_name as creator_first_name,
             au.last_name as creator_last_name
      FROM campaigns c
      LEFT JOIN appointments a ON c.id = a.campaign_id AND a.status IN ('booked', 'confirmed')
      LEFT JOIN admin_users au ON c.created_by = au.id
      WHERE c.id = ?
      GROUP BY c.id
    `,
      [campaignId]
    );

    if (campaigns.length === 0) {
      return res.status(404).json({error: 'Campagne non trouvée'});
    }

    const campaign = campaigns[0];

    // Parser JSON
    if (campaign.blood_types_needed) {
      try {
        campaign.blood_types_needed = JSON.parse(campaign.blood_types_needed);
      } catch (e) {
        campaign.blood_types_needed = [];
      }
    }

    // Obtenir les créneaux horaires
    const [timeSlots] = await pool.execute(
      `
      SELECT * FROM time_slots 
      WHERE campaign_id = ? 
      ORDER BY slot_datetime ASC
    `,
      [campaignId]
    );

    res.json({
      campaign: {
        ...campaign,
        time_slots: timeSlots
      }
    });
  } catch (error) {
    console.error('Erreur récupération campagne:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Créer une nouvelle campagne
app.post('/api/campaigns', async (req, res) => {
  try {
    const {error, value} = campaignSchema.validate(req.body);
    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {
      name,
      description,
      start_date,
      end_date,
      start_time,
      end_time,
      location_name,
      address,
      city,
      latitude,
      longitude,
      max_capacity,
      blood_types_needed,
      created_by
    } = value;

    // Convertir le tableau blood_types_needed en JSON
    const bloodTypesJson = blood_types_needed
      ? JSON.stringify(blood_types_needed)
      : null;

    const [result] = await pool.execute(
      `
      INSERT INTO campaigns (
        name, description, start_date, end_date, start_time, end_time,
        location_name, address, city, latitude, longitude, max_capacity,
        blood_types_needed, created_by, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'planned')
    `,
      [
        name,
        description,
        start_date,
        end_date,
        start_time || '08:00:00',
        end_time || '18:00:00',
        location_name,
        address,
        city,
        latitude,
        longitude,
        max_capacity,
        bloodTypesJson,
        created_by
      ]
    );

    // Créer des créneaux horaires automatiquement
    if (start_time && end_time) {
      const startDateTime = moment(`${start_date} ${start_time}`);
      const endDateTime = moment(`${start_date} ${end_time}`);

      const timeSlots = [];
      let currentSlot = startDateTime.clone();

      while (currentSlot.isBefore(endDateTime)) {
        timeSlots.push([
          result.insertId,
          currentSlot.format('YYYY-MM-DD HH:mm:ss'),
          5 // Capacité par défaut de 5 personnes par créneau
        ]);
        currentSlot.add(1, 'hour'); // Créneaux d'1 heure
      }

      if (timeSlots.length > 0) {
        await pool.execute(
          `
          INSERT INTO time_slots (campaign_id, slot_datetime, capacity, available_spots) 
          VALUES ${timeSlots.map(() => '(?, ?, ?, ?)').join(', ')}
        `,
          timeSlots
            .flat()
            .map((val, i) => (i % 3 === 2 ? [val, val] : val))
            .flat()
        );
      }
    }

    res.status(201).json({
      message: 'Campagne créée avec succès',
      campaignId: result.insertId
    });
  } catch (error) {
    console.error('Erreur création campagne:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Mettre à jour une campagne
app.put('/api/campaigns/:id', async (req, res) => {
  try {
    const campaignId = req.params.id;
    const {error, value} = campaignSchema.validate(req.body);

    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {
      name,
      description,
      start_date,
      end_date,
      start_time,
      end_time,
      location_name,
      address,
      city,
      latitude,
      longitude,
      max_capacity,
      blood_types_needed,
      status
    } = value;

    // Vérifier que la campagne existe
    const [existing] = await pool.execute(
      'SELECT id FROM campaigns WHERE id = ?',
      [campaignId]
    );
    if (existing.length === 0) {
      return res.status(404).json({error: 'Campagne non trouvée'});
    }

    const bloodTypesJson = blood_types_needed
      ? JSON.stringify(blood_types_needed)
      : null;

    await pool.execute(
      `
      UPDATE campaigns SET 
        name = ?, description = ?, start_date = ?, end_date = ?, 
        start_time = ?, end_time = ?, location_name = ?, address = ?, 
        city = ?, latitude = ?, longitude = ?, max_capacity = ?,
        blood_types_needed = ?, status = ?, updated_at = NOW()
      WHERE id = ?
    `,
      [
        name,
        description,
        start_date,
        end_date,
        start_time,
        end_time,
        location_name,
        address,
        city,
        latitude,
        longitude,
        max_capacity,
        bloodTypesJson,
        status || 'planned',
        campaignId
      ]
    );

    res.json({message: 'Campagne mise à jour avec succès'});
  } catch (error) {
    console.error('Erreur mise à jour campagne:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Supprimer une campagne
app.delete('/api/campaigns/:id', async (req, res) => {
  try {
    const campaignId = req.params.id;

    // Vérifier s'il y a des rendez-vous confirmés
    const [appointments] = await pool.execute(
      'SELECT COUNT(*) as count FROM appointments WHERE campaign_id = ? AND status IN ("confirmed", "completed")',
      [campaignId]
    );

    if (appointments[0].count > 0) {
      return res.status(400).json({
        error:
          'Impossible de supprimer une campagne avec des rendez-vous confirmés'
      });
    }

    // Supprimer la campagne (les créneaux et RDV seront supprimés en cascade)
    const [result] = await pool.execute('DELETE FROM campaigns WHERE id = ?', [
      campaignId
    ]);

    if (result.affectedRows === 0) {
      return res.status(404).json({error: 'Campagne non trouvée'});
    }

    res.json({message: 'Campagne supprimée avec succès'});
  } catch (error) {
    console.error('Erreur suppression campagne:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Statistiques des campagnes
app.get('/api/campaigns/stats/overview', async (req, res) => {
  try {
    const [stats] = await pool.execute(`
      SELECT 
        COUNT(*) as total_campaigns,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_campaigns,
        SUM(CASE WHEN status = 'planned' THEN 1 ELSE 0 END) as planned_campaigns,
        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_campaigns,
        SUM(max_capacity) as total_capacity,
        COUNT(DISTINCT city) as cities_covered
      FROM campaigns
    `);

    const [recentActivity] = await pool.execute(`
      SELECT c.name, c.city, c.start_date, COUNT(a.id) as registrations
      FROM campaigns c
      LEFT JOIN appointments a ON c.id = a.campaign_id
      WHERE c.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
      GROUP BY c.id
      ORDER BY c.created_at DESC
      LIMIT 5
    `);

    res.json({
      overview: stats[0],
      recent_activity: recentActivity
    });
  } catch (error) {
    console.error('Erreur statistiques campagnes:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Démarrer le serveur
async function startServer() {
  await initDatabase();

  app.listen(PORT, () => {
    console.log(`🚀 Campaign Service démarré sur le port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
  });
}

startServer().catch((error) => {
  console.error('❌ Erreur démarrage serveur:', error);
  process.exit(1);
});
