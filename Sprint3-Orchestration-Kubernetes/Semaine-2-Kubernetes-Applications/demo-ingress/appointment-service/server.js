const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const Joi = require('joi');
const moment = require('moment');
const {v4: uuidv4} = require('uuid');

const app = express();
const PORT = process.env.PORT || 3003;

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
const appointmentSchema = Joi.object({
  user_id: Joi.number().positive().required(),
  campaign_id: Joi.number().positive().required(),
  time_slot_id: Joi.number().positive().required(),
  notes: Joi.string().max(500).optional()
});

// Connexion base de données
async function initDatabase() {
  try {
    pool = mysql.createPool(dbConfig);
    console.log('🗄️  Connexion à MySQL établie (Appointment Service)');
  } catch (error) {
    console.error('❌ Erreur connexion MySQL:', error);
    process.exit(1);
  }
}

// Utilitaires
function generateConfirmationCode() {
  return uuidv4().split('-')[0].toUpperCase();
}

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'Appointment Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Obtenir créneaux disponibles pour une campagne
app.get('/api/appointments/slots/:campaignId', async (req, res) => {
  try {
    const {campaignId} = req.params;
    const {date} = req.query;

    let query = `
      SELECT ts.*, 
             c.name as campaign_name,
             c.location_name,
             (ts.capacity - COUNT(a.id)) as available_spots
      FROM time_slots ts
      JOIN campaigns c ON ts.campaign_id = c.id
      LEFT JOIN appointments a ON ts.id = a.time_slot_id AND a.status IN ('booked', 'confirmed')
      WHERE ts.campaign_id = ?
    `;

    let queryParams = [campaignId];

    if (date) {
      query += ' AND DATE(ts.slot_datetime) = ?';
      queryParams.push(date);
    }

    query += `
      GROUP BY ts.id
      HAVING available_spots > 0
      ORDER BY ts.slot_datetime ASC
    `;

    const [slots] = await pool.execute(query, queryParams);

    // Grouper par date
    const slotsByDate = {};
    slots.forEach((slot) => {
      const date = moment(slot.slot_datetime).format('YYYY-MM-DD');
      if (!slotsByDate[date]) {
        slotsByDate[date] = [];
      }
      slotsByDate[date].push({
        ...slot,
        time: moment(slot.slot_datetime).format('HH:mm'),
        formatted_datetime: moment(slot.slot_datetime).format(
          'DD/MM/YYYY à HH:mm'
        )
      });
    });

    res.json({
      slots_by_date: slotsByDate,
      total_slots: slots.length
    });
  } catch (error) {
    console.error('Erreur récupération créneaux:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Réserver un rendez-vous
app.post('/api/appointments/book', async (req, res) => {
  try {
    const {error, value} = appointmentSchema.validate(req.body);
    if (error) {
      return res.status(400).json({error: error.details[0].message});
    }

    const {user_id, campaign_id, time_slot_id, notes} = value;

    // Transaction pour éviter les conflits de réservation
    const connection = await pool.getConnection();
    await connection.beginTransaction();

    try {
      // Vérifier que l'utilisateur n'a pas déjà un RDV pour cette campagne
      const [existingAppointments] = await connection.execute(
        `
        SELECT id FROM appointments 
        WHERE user_id = ? AND campaign_id = ? AND status IN ('booked', 'confirmed')
      `,
        [user_id, campaign_id]
      );

      if (existingAppointments.length > 0) {
        await connection.rollback();
        connection.release();
        return res.status(409).json({
          error: 'Vous avez déjà un rendez-vous pour cette campagne'
        });
      }

      // Vérifier que le créneau est encore disponible
      const [slotInfo] = await connection.execute(
        `
        SELECT ts.*, 
               (ts.capacity - COUNT(a.id)) as available_spots,
               c.name as campaign_name
        FROM time_slots ts
        JOIN campaigns c ON ts.campaign_id = c.id
        LEFT JOIN appointments a ON ts.id = a.time_slot_id AND a.status IN ('booked', 'confirmed')
        WHERE ts.id = ? AND ts.campaign_id = ?
        GROUP BY ts.id
      `,
        [time_slot_id, campaign_id]
      );

      if (slotInfo.length === 0) {
        await connection.rollback();
        connection.release();
        return res.status(404).json({error: 'Créneau non trouvé'});
      }

      if (slotInfo[0].available_spots <= 0) {
        await connection.rollback();
        connection.release();
        return res.status(409).json({error: 'Créneau complet'});
      }

      // Vérifier que l'utilisateur est éligible au don
      const [userProfile] = await connection.execute(
        `
        SELECT mp.eligible_to_donate, mp.last_donation_date,
               u.first_name, u.last_name
        FROM users u
        LEFT JOIN medical_profiles mp ON u.id = mp.user_id
        WHERE u.id = ?
      `,
        [user_id]
      );

      if (userProfile.length === 0) {
        await connection.rollback();
        connection.release();
        return res.status(404).json({error: 'Utilisateur non trouvé'});
      }

      if (!userProfile[0].eligible_to_donate) {
        await connection.rollback();
        connection.release();
        return res.status(403).json({
          error: "Vous n'êtes pas éligible au don de sang actuellement"
        });
      }

      // Vérifier la période d'attente entre deux dons (8 semaines pour les hommes, 12 pour les femmes)
      if (userProfile[0].last_donation_date) {
        const lastDonation = moment(userProfile[0].last_donation_date);
        const weeksAgo = moment().diff(lastDonation, 'weeks');

        if (weeksAgo < 8) {
          // Période minimale de sécurité
          await connection.rollback();
          connection.release();
          return res.status(403).json({
            error: `Vous devez attendre ${
              8 - weeksAgo
            } semaine(s) avant votre prochain don`
          });
        }
      }

      // Créer le rendez-vous
      const confirmationCode = generateConfirmationCode();
      const [result] = await connection.execute(
        `
        INSERT INTO appointments (user_id, campaign_id, time_slot_id, status, notes, confirmation_code)
        VALUES (?, ?, ?, 'booked', ?, ?)
      `,
        [user_id, campaign_id, time_slot_id, notes, confirmationCode]
      );

      await connection.commit();
      connection.release();

      res.status(201).json({
        message: 'Rendez-vous réservé avec succès',
        appointment: {
          id: result.insertId,
          confirmation_code: confirmationCode,
          campaign_name: slotInfo[0].campaign_name,
          slot_datetime: slotInfo[0].slot_datetime,
          formatted_datetime: moment(slotInfo[0].slot_datetime).format(
            'DD/MM/YYYY à HH:mm'
          )
        }
      });
    } catch (error) {
      await connection.rollback();
      connection.release();
      throw error;
    }
  } catch (error) {
    console.error('Erreur réservation RDV:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Obtenir les rendez-vous d'un utilisateur
app.get('/api/appointments/user/:userId', async (req, res) => {
  try {
    const {userId} = req.params;
    const {status = '', page = 1, limit = 10} = req.query;

    const offset = (page - 1) * limit;

    let query = `
      SELECT a.*, 
             c.name as campaign_name,
             c.location_name,
             c.address,
             c.city,
             ts.slot_datetime,
             ts.duration_minutes
      FROM appointments a
      JOIN campaigns c ON a.campaign_id = c.id
      JOIN time_slots ts ON a.time_slot_id = ts.id
      WHERE a.user_id = ?
    `;

    let queryParams = [userId];

    if (status) {
      query += ' AND a.status = ?';
      queryParams.push(status);
    }

    query += ' ORDER BY ts.slot_datetime DESC LIMIT ? OFFSET ?';
    queryParams.push(parseInt(limit), parseInt(offset));

    const [appointments] = await pool.execute(query, queryParams);

    // Formater les dates
    appointments.forEach((appointment) => {
      appointment.formatted_datetime = moment(appointment.slot_datetime).format(
        'DD/MM/YYYY à HH:mm'
      );
      appointment.is_past = moment().isAfter(appointment.slot_datetime);
      appointment.can_cancel =
        !appointment.is_past && appointment.status === 'booked';
    });

    // Compter le total
    let countQuery =
      'SELECT COUNT(*) as total FROM appointments WHERE user_id = ?';
    let countParams = [userId];

    if (status) {
      countQuery += ' AND status = ?';
      countParams.push(status);
    }

    const [countResult] = await pool.execute(countQuery, countParams);

    res.json({
      appointments,
      pagination: {
        current_page: parseInt(page),
        per_page: parseInt(limit),
        total: countResult[0].total,
        total_pages: Math.ceil(countResult[0].total / limit)
      }
    });
  } catch (error) {
    console.error('Erreur récupération RDV utilisateur:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Confirmer un rendez-vous
app.put('/api/appointments/:id/confirm', async (req, res) => {
  try {
    const {id} = req.params;
    const {confirmation_code} = req.body;

    if (!confirmation_code) {
      return res.status(400).json({error: 'Code de confirmation requis'});
    }

    const [appointments] = await pool.execute(
      `
      SELECT a.*, c.name as campaign_name, ts.slot_datetime
      FROM appointments a
      JOIN campaigns c ON a.campaign_id = c.id
      JOIN time_slots ts ON a.time_slot_id = ts.id
      WHERE a.id = ? AND a.confirmation_code = ?
    `,
      [id, confirmation_code]
    );

    if (appointments.length === 0) {
      return res
        .status(404)
        .json({error: 'Rendez-vous non trouvé ou code invalide'});
    }

    const appointment = appointments[0];

    if (appointment.status !== 'booked') {
      return res
        .status(400)
        .json({error: 'Rendez-vous déjà confirmé ou annulé'});
    }

    // Vérifier que le RDV n'est pas déjà passé
    if (moment().isAfter(appointment.slot_datetime)) {
      return res
        .status(400)
        .json({error: 'Impossible de confirmer un rendez-vous passé'});
    }

    await pool.execute(
      'UPDATE appointments SET status = "confirmed", updated_at = NOW() WHERE id = ?',
      [id]
    );

    res.json({
      message: 'Rendez-vous confirmé avec succès',
      appointment: {
        id: appointment.id,
        campaign_name: appointment.campaign_name,
        formatted_datetime: moment(appointment.slot_datetime).format(
          'DD/MM/YYYY à HH:mm'
        )
      }
    });
  } catch (error) {
    console.error('Erreur confirmation RDV:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Annuler un rendez-vous
app.delete('/api/appointments/:id/cancel', async (req, res) => {
  try {
    const {id} = req.params;
    const {user_id} = req.body;

    // Vérifier que le RDV appartient à l'utilisateur
    const [appointments] = await pool.execute(
      `
      SELECT a.*, ts.slot_datetime, c.name as campaign_name
      FROM appointments a
      JOIN time_slots ts ON a.time_slot_id = ts.id
      JOIN campaigns c ON a.campaign_id = c.id
      WHERE a.id = ? AND a.user_id = ?
    `,
      [id, user_id]
    );

    if (appointments.length === 0) {
      return res.status(404).json({error: 'Rendez-vous non trouvé'});
    }

    const appointment = appointments[0];

    if (appointment.status === 'cancelled') {
      return res.status(400).json({error: 'Rendez-vous déjà annulé'});
    }

    if (appointment.status === 'completed') {
      return res
        .status(400)
        .json({error: "Impossible d'annuler un don déjà effectué"});
    }

    // Vérifier qu'il reste assez de temps pour annuler (au moins 2h avant)
    const hoursUntilAppointment = moment(appointment.slot_datetime).diff(
      moment(),
      'hours'
    );
    if (hoursUntilAppointment < 2) {
      return res.status(400).json({
        error:
          "Impossible d'annuler moins de 2h avant le rendez-vous. Contactez le centre."
      });
    }

    await pool.execute(
      'UPDATE appointments SET status = "cancelled", updated_at = NOW() WHERE id = ?',
      [id]
    );

    res.json({
      message: 'Rendez-vous annulé avec succès',
      refund_notice:
        "Le créneau est maintenant disponible pour d'autres donneurs"
    });
  } catch (error) {
    console.error('Erreur annulation RDV:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Marquer un rendez-vous comme terminé (pour le staff médical)
app.put('/api/appointments/:id/complete', async (req, res) => {
  try {
    const {id} = req.params;
    const {
      donation_completed,
      volume_ml,
      hemoglobin_level,
      blood_pressure_systolic,
      blood_pressure_diastolic,
      temperature,
      pulse_rate,
      complications,
      notes,
      medical_staff_id
    } = req.body;

    const [appointments] = await pool.execute(
      `
      SELECT a.*, u.id as user_id
      FROM appointments a
      JOIN users u ON a.user_id = u.id
      WHERE a.id = ?
    `,
      [id]
    );

    if (appointments.length === 0) {
      return res.status(404).json({error: 'Rendez-vous non trouvé'});
    }

    const appointment = appointments[0];

    if (appointment.status !== 'confirmed') {
      return res.status(400).json({error: 'Le rendez-vous doit être confirmé'});
    }

    const connection = await pool.getConnection();
    await connection.beginTransaction();

    try {
      // Marquer le RDV comme terminé
      await connection.execute(
        'UPDATE appointments SET status = "completed", donation_completed = ?, notes = ?, updated_at = NOW() WHERE id = ?',
        [donation_completed, notes, id]
      );

      // Si le don a été effectué, créer l'entrée dans l'historique
      if (donation_completed) {
        await connection.execute(
          `
          INSERT INTO donation_history (
            user_id, appointment_id, donation_date, volume_ml, 
            hemoglobin_level, blood_pressure_systolic, blood_pressure_diastolic,
            temperature, pulse_rate, complications, notes, medical_staff_id
          ) VALUES (?, ?, CURDATE(), ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `,
          [
            appointment.user_id,
            id,
            volume_ml || 450,
            hemoglobin_level,
            blood_pressure_systolic,
            blood_pressure_diastolic,
            temperature,
            pulse_rate,
            complications,
            notes,
            medical_staff_id
          ]
        );

        // Mettre à jour la date du dernier don dans le profil médical
        await connection.execute(
          'UPDATE medical_profiles SET last_donation_date = CURDATE() WHERE user_id = ?',
          [appointment.user_id]
        );
      }

      await connection.commit();
      connection.release();

      res.json({
        message: donation_completed
          ? 'Don enregistré avec succès'
          : 'Rendez-vous marqué comme terminé',
        donation_completed
      });
    } catch (error) {
      await connection.rollback();
      connection.release();
      throw error;
    }
  } catch (error) {
    console.error('Erreur finalisation RDV:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Statistiques des rendez-vous
app.get('/api/appointments/stats/overview', async (req, res) => {
  try {
    const {start_date, end_date} = req.query;

    let dateFilter = '';
    let queryParams = [];

    if (start_date && end_date) {
      dateFilter = 'WHERE ts.slot_datetime BETWEEN ? AND ?';
      queryParams = [start_date, end_date];
    }

    const [stats] = await pool.execute(
      `
      SELECT 
        COUNT(*) as total_appointments,
        SUM(CASE WHEN a.status = 'booked' THEN 1 ELSE 0 END) as booked_appointments,
        SUM(CASE WHEN a.status = 'confirmed' THEN 1 ELSE 0 END) as confirmed_appointments,
        SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) as completed_appointments,
        SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_appointments,
        SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) as no_show_appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations
      FROM appointments a
      JOIN time_slots ts ON a.time_slot_id = ts.id
      ${dateFilter}
    `,
      queryParams
    );

    const [dailyStats] = await pool.execute(
      `
      SELECT 
        DATE(ts.slot_datetime) as date,
        COUNT(*) as appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as donations
      FROM appointments a
      JOIN time_slots ts ON a.time_slot_id = ts.id
      ${dateFilter}
      GROUP BY DATE(ts.slot_datetime)
      ORDER BY date DESC
      LIMIT 30
    `,
      queryParams
    );

    res.json({
      overview: stats[0],
      daily_stats: dailyStats
    });
  } catch (error) {
    console.error('Erreur statistiques RDV:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Démarrer le serveur
async function startServer() {
  await initDatabase();

  app.listen(PORT, () => {
    console.log(`🚀 Appointment Service démarré sur le port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
  });
}

startServer().catch((error) => {
  console.error('❌ Erreur démarrage serveur:', error);
  process.exit(1);
});
