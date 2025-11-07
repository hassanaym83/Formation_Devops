const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const Joi = require('joi');
const moment = require('moment');
const cron = require('node-cron');

const app = express();
const PORT = process.env.PORT || 3004;

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
  max: 200, // Plus de requêtes pour les analytics
  message: 'Trop de requêtes depuis cette IP'
});
app.use(limiter);

// Schémas de validation
const dateRangeSchema = Joi.object({
  start_date: Joi.date().optional(),
  end_date: Joi.date()
    .optional()
    .when('start_date', {
      is: Joi.exist(),
      then: Joi.date().min(Joi.ref('start_date'))
    })
});

// Connexion base de données
async function initDatabase() {
  try {
    pool = mysql.createPool(dbConfig);
    console.log('🗄️  Connexion à MySQL établie (Analytics Service)');
  } catch (error) {
    console.error('❌ Erreur connexion MySQL:', error);
    process.exit(1);
  }
}

// Utilitaires
function formatDateRange(start_date, end_date) {
  const start = start_date ? moment(start_date) : moment().subtract(30, 'days');
  const end = end_date ? moment(end_date) : moment();

  return {
    start: start.format('YYYY-MM-DD'),
    end: end.format('YYYY-MM-DD'),
    formatted_range: `${start.format('DD/MM/YYYY')} - ${end.format(
      'DD/MM/YYYY'
    )}`
  };
}

// Routes

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'Analytics Service',
    status: 'OK',
    timestamp: new Date().toISOString(),
    port: PORT
  });
});

// Dashboard général - Vue d'ensemble
app.get('/api/analytics/dashboard', async (req, res) => {
  try {
    const {start_date, end_date} = req.query;
    const dateRange = formatDateRange(start_date, end_date);

    // KPIs principaux
    const [kpis] = await pool.execute(
      `
      SELECT 
        (SELECT COUNT(*) FROM users WHERE created_at BETWEEN ? AND ?) as new_users,
        (SELECT COUNT(*) FROM campaigns WHERE created_at BETWEEN ? AND ?) as new_campaigns,
        (SELECT COUNT(*) FROM appointments a JOIN time_slots ts ON a.time_slot_id = ts.id 
         WHERE ts.slot_datetime BETWEEN ? AND ?) as total_appointments,
        (SELECT COUNT(*) FROM donation_history WHERE donation_date BETWEEN ? AND ?) as total_donations,
        (SELECT SUM(volume_ml) FROM donation_history WHERE donation_date BETWEEN ? AND ?) as total_volume_ml,
        (SELECT COUNT(*) FROM users) as total_users_ever,
        (SELECT COUNT(*) FROM campaigns WHERE status = 'active') as active_campaigns,
        (SELECT AVG(volume_ml) FROM donation_history WHERE donation_date BETWEEN ? AND ?) as avg_volume_per_donation
    `,
      [
        dateRange.start,
        dateRange.end, // new_users
        dateRange.start,
        dateRange.end, // new_campaigns
        dateRange.start,
        dateRange.end, // total_appointments
        dateRange.start,
        dateRange.end, // total_donations
        dateRange.start,
        dateRange.end, // total_volume_ml
        dateRange.start,
        dateRange.end // avg_volume_per_donation
      ]
    );

    // Évolution quotidienne des dons
    const [dailyTrend] = await pool.execute(
      `
      SELECT 
        DATE(donation_date) as date,
        COUNT(*) as donations,
        SUM(volume_ml) as total_volume,
        COUNT(DISTINCT user_id) as unique_donors
      FROM donation_history 
      WHERE donation_date BETWEEN ? AND ?
      GROUP BY DATE(donation_date)
      ORDER BY date
    `,
      [dateRange.start, dateRange.end]
    );

    // Répartition par groupe sanguin
    const [bloodGroupStats] = await pool.execute(
      `
      SELECT 
        mp.blood_group,
        COUNT(dh.id) as donations,
        SUM(dh.volume_ml) as total_volume,
        COUNT(DISTINCT dh.user_id) as unique_donors
      FROM donation_history dh
      JOIN medical_profiles mp ON dh.user_id = mp.user_id
      WHERE dh.donation_date BETWEEN ? AND ?
      GROUP BY mp.blood_group
      ORDER BY donations DESC
    `,
      [dateRange.start, dateRange.end]
    );

    // Taux de conversion (réservation → don effectif)
    const [conversionStats] = await pool.execute(
      `
      SELECT 
        COUNT(*) as total_appointments,
        SUM(CASE WHEN donation_completed = 1 THEN 1 ELSE 0 END) as completed_donations,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_appointments,
        SUM(CASE WHEN status = 'no_show' THEN 1 ELSE 0 END) as no_show_appointments,
        ROUND(SUM(CASE WHEN donation_completed = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as conversion_rate
      FROM appointments a
      JOIN time_slots ts ON a.time_slot_id = ts.id
      WHERE ts.slot_datetime BETWEEN ? AND ?
    `,
      [dateRange.start, dateRange.end]
    );

    res.json({
      period: dateRange,
      kpis: {
        ...kpis[0],
        conversion_rate: conversionStats[0].conversion_rate || 0
      },
      trends: {
        daily_donations: dailyTrend,
        blood_groups: bloodGroupStats,
        conversion_stats: conversionStats[0]
      }
    });
  } catch (error) {
    console.error('Erreur dashboard analytics:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Statistiques des utilisateurs et donneurs
app.get('/api/analytics/users', async (req, res) => {
  try {
    const {start_date, end_date} = req.query;
    const dateRange = formatDateRange(start_date, end_date);

    // Profil des utilisateurs
    const [userProfiles] = await pool.execute(
      `
      SELECT 
        mp.blood_group,
        mp.gender,
        COUNT(u.id) as user_count,
        COUNT(dh.id) as total_donations,
        SUM(CASE WHEN dh.donation_date BETWEEN ? AND ? THEN 1 ELSE 0 END) as recent_donations
      FROM users u
      JOIN medical_profiles mp ON u.id = mp.user_id
      LEFT JOIN donation_history dh ON u.id = dh.user_id
      GROUP BY mp.blood_group, mp.gender
      ORDER BY user_count DESC
    `,
      [dateRange.start, dateRange.end]
    );

    // Nouveaux utilisateurs par mois
    const [monthlyNewUsers] = await pool.execute(`
      SELECT 
        DATE_FORMAT(created_at, '%Y-%m') as month,
        COUNT(*) as new_users
      FROM users 
      WHERE created_at >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
      GROUP BY DATE_FORMAT(created_at, '%Y-%m')
      ORDER BY month
    `);

    // Top donneurs (utilisateurs les plus actifs)
    const [topDonors] = await pool.execute(
      `
      SELECT 
        u.first_name,
        u.last_name,
        u.email,
        mp.blood_group,
        COUNT(dh.id) as total_donations,
        SUM(dh.volume_ml) as total_volume_ml,
        MAX(dh.donation_date) as last_donation_date,
        SUM(CASE WHEN dh.donation_date BETWEEN ? AND ? THEN 1 ELSE 0 END) as recent_donations
      FROM users u
      JOIN medical_profiles mp ON u.id = mp.user_id
      JOIN donation_history dh ON u.id = dh.user_id
      GROUP BY u.id
      HAVING total_donations >= 1
      ORDER BY total_donations DESC, last_donation_date DESC
      LIMIT 20
    `,
      [dateRange.start, dateRange.end]
    );

    // Répartition géographique
    const [geographicStats] = await pool.execute(`
      SELECT 
        city,
        COUNT(DISTINCT u.id) as users,
        COUNT(dh.id) as total_donations
      FROM users u
      LEFT JOIN donation_history dh ON u.id = dh.user_id
      WHERE u.city IS NOT NULL
      GROUP BY city
      HAVING users > 0
      ORDER BY users DESC
      LIMIT 15
    `);

    res.json({
      period: dateRange,
      user_demographics: userProfiles,
      monthly_registration: monthlyNewUsers,
      top_donors: topDonors,
      geographic_distribution: geographicStats
    });
  } catch (error) {
    console.error('Erreur analytics utilisateurs:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Statistiques des campagnes
app.get('/api/analytics/campaigns', async (req, res) => {
  try {
    const {start_date, end_date} = req.query;
    const dateRange = formatDateRange(start_date, end_date);

    // Performance des campagnes
    const [campaignPerformance] = await pool.execute(
      `
      SELECT 
        c.id,
        c.name,
        c.location_name,
        c.city,
        c.start_date,
        c.end_date,
        c.target_donors,
        COUNT(DISTINCT ts.id) as total_slots,
        COUNT(DISTINCT a.id) as total_appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations,
        SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_appointments,
        ROUND(SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(a.id), 0), 2) as success_rate,
        ROUND(COUNT(DISTINCT a.id) * 100.0 / NULLIF(c.target_donors, 0), 2) as target_achievement
      FROM campaigns c
      LEFT JOIN time_slots ts ON c.id = ts.campaign_id
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE c.start_date BETWEEN ? AND ?
      GROUP BY c.id
      ORDER BY successful_donations DESC
    `,
      [dateRange.start, dateRange.end]
    );

    // Campagnes par statut
    const [campaignsByStatus] = await pool.execute(
      `
      SELECT 
        status,
        COUNT(*) as count,
        AVG(target_donors) as avg_target
      FROM campaigns 
      WHERE created_at BETWEEN ? AND ?
      GROUP BY status
    `,
      [dateRange.start, dateRange.end]
    );

    // Efficacité par localisation
    const [locationEfficiency] = await pool.execute(
      `
      SELECT 
        c.city,
        COUNT(DISTINCT c.id) as campaigns,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as total_donations,
        COUNT(DISTINCT a.user_id) as unique_donors,
        ROUND(AVG(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) * 100, 2) as avg_success_rate
      FROM campaigns c
      LEFT JOIN time_slots ts ON c.id = ts.campaign_id
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE c.start_date BETWEEN ? AND ?
      GROUP BY c.city
      HAVING campaigns > 0
      ORDER BY total_donations DESC
      LIMIT 10
    `,
      [dateRange.start, dateRange.end]
    );

    res.json({
      period: dateRange,
      campaign_performance: campaignPerformance,
      campaigns_by_status: campaignsByStatus,
      location_efficiency: locationEfficiency
    });
  } catch (error) {
    console.error('Erreur analytics campagnes:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Analyse des créneaux et de la planification
app.get('/api/analytics/scheduling', async (req, res) => {
  try {
    const {start_date, end_date} = req.query;
    const dateRange = formatDateRange(start_date, end_date);

    // Analyse par jour de la semaine
    const [weekdayAnalysis] = await pool.execute(
      `
      SELECT 
        DAYNAME(ts.slot_datetime) as day_name,
        DAYOFWEEK(ts.slot_datetime) as day_number,
        COUNT(a.id) as appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations,
        AVG(ts.capacity) as avg_slot_capacity,
        ROUND(COUNT(a.id) * 100.0 / SUM(ts.capacity), 2) as utilization_rate
      FROM time_slots ts
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE ts.slot_datetime BETWEEN ? AND ?
      GROUP BY DAYOFWEEK(ts.slot_datetime), DAYNAME(ts.slot_datetime)
      ORDER BY day_number
    `,
      [dateRange.start, dateRange.end]
    );

    // Analyse par heure de la journée
    const [hourlyAnalysis] = await pool.execute(
      `
      SELECT 
        HOUR(ts.slot_datetime) as hour,
        COUNT(a.id) as appointments,
        SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations,
        SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) as no_shows,
        ROUND(AVG(ts.capacity), 2) as avg_capacity
      FROM time_slots ts
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE ts.slot_datetime BETWEEN ? AND ?
      GROUP BY HOUR(ts.slot_datetime)
      ORDER BY hour
    `,
      [dateRange.start, dateRange.end]
    );

    // Taux d'occupation des créneaux
    const [slotUtilization] = await pool.execute(
      `
      SELECT 
        c.name as campaign_name,
        c.city,
        DATE(ts.slot_datetime) as date,
        COUNT(ts.id) as total_slots,
        SUM(ts.capacity) as total_capacity,
        COUNT(a.id) as total_bookings,
        ROUND(COUNT(a.id) * 100.0 / SUM(ts.capacity), 2) as utilization_rate
      FROM campaigns c
      JOIN time_slots ts ON c.id = ts.campaign_id
      LEFT JOIN appointments a ON ts.id = a.time_slot_id
      WHERE ts.slot_datetime BETWEEN ? AND ?
      GROUP BY c.id, DATE(ts.slot_datetime)
      HAVING total_slots > 0
      ORDER BY utilization_rate DESC
      LIMIT 20
    `,
      [dateRange.start, dateRange.end]
    );

    res.json({
      period: dateRange,
      weekday_patterns: weekdayAnalysis,
      hourly_patterns: hourlyAnalysis,
      slot_utilization: slotUtilization
    });
  } catch (error) {
    console.error('Erreur analytics planning:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Prédictions et tendances
app.get('/api/analytics/predictions', async (req, res) => {
  try {
    // Tendances des 6 derniers mois
    const [monthlyTrends] = await pool.execute(`
      SELECT 
        DATE_FORMAT(donation_date, '%Y-%m') as month,
        COUNT(*) as donations,
        SUM(volume_ml) as total_volume,
        COUNT(DISTINCT user_id) as unique_donors,
        AVG(hemoglobin_level) as avg_hemoglobin
      FROM donation_history 
      WHERE donation_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
      GROUP BY DATE_FORMAT(donation_date, '%Y-%m')
      ORDER BY month
    `);

    // Prédiction basique basée sur la moyenne mobile
    if (monthlyTrends.length >= 3) {
      const recentMonths = monthlyTrends.slice(-3);
      const avgDonations =
        recentMonths.reduce((sum, month) => sum + month.donations, 0) / 3;
      const avgVolume =
        recentMonths.reduce((sum, month) => sum + month.total_volume, 0) / 3;

      const nextMonth = moment().add(1, 'month').format('YYYY-MM');

      var predictions = {
        next_month: {
          month: nextMonth,
          predicted_donations: Math.round(avgDonations),
          predicted_volume: Math.round(avgVolume),
          confidence: 'medium'
        }
      };
    }

    // Analyse de saisonnalité
    const [seasonalAnalysis] = await pool.execute(`
      SELECT 
        MONTH(donation_date) as month,
        MONTHNAME(donation_date) as month_name,
        COUNT(*) as total_donations,
        AVG(COUNT(*)) OVER() as yearly_average,
        ROUND((COUNT(*) - AVG(COUNT(*)) OVER()) * 100.0 / AVG(COUNT(*)) OVER(), 2) as deviation_percent
      FROM donation_history 
      WHERE donation_date >= DATE_SUB(CURDATE(), INTERVAL 2 YEAR)
      GROUP BY MONTH(donation_date), MONTHNAME(donation_date)
      ORDER BY month
    `);

    // Besoins en sang par groupe sanguin
    const [bloodGroupNeeds] = await pool.execute(`
      SELECT 
        mp.blood_group,
        COUNT(dh.id) as recent_donations,
        -- Estimation basique des besoins (O- et O+ plus demandés)
        CASE 
          WHEN mp.blood_group = 'O-' THEN COUNT(dh.id) * 1.5
          WHEN mp.blood_group = 'O+' THEN COUNT(dh.id) * 1.3
          WHEN mp.blood_group IN ('A-', 'B-', 'AB-') THEN COUNT(dh.id) * 1.2
          ELSE COUNT(dh.id)
        END as estimated_monthly_need,
        CASE 
          WHEN mp.blood_group = 'O-' THEN 'Critique'
          WHEN mp.blood_group = 'O+' THEN 'Élevé'
          WHEN mp.blood_group IN ('A-', 'B-', 'AB-') THEN 'Modéré'
          ELSE 'Standard'
        END as priority_level
      FROM donation_history dh
      JOIN medical_profiles mp ON dh.user_id = mp.user_id
      WHERE dh.donation_date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
      GROUP BY mp.blood_group
      ORDER BY estimated_monthly_need DESC
    `);

    res.json({
      monthly_trends: monthlyTrends,
      predictions: predictions || null,
      seasonal_patterns: seasonalAnalysis,
      blood_group_needs: bloodGroupNeeds
    });
  } catch (error) {
    console.error('Erreur analytics prédictions:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Export de données pour rapports
app.get('/api/analytics/export', async (req, res) => {
  try {
    const {type = 'full', start_date, end_date, format = 'json'} = req.query;
    const dateRange = formatDateRange(start_date, end_date);

    let data = {};

    switch (type) {
      case 'donations':
        const [donations] = await pool.execute(
          `
          SELECT 
            dh.*,
            u.first_name, u.last_name, u.email,
            mp.blood_group, mp.gender,
            c.name as campaign_name, c.location_name
          FROM donation_history dh
          JOIN users u ON dh.user_id = u.id
          JOIN medical_profiles mp ON u.id = mp.user_id
          LEFT JOIN appointments a ON dh.appointment_id = a.id
          LEFT JOIN campaigns c ON a.campaign_id = c.id
          WHERE dh.donation_date BETWEEN ? AND ?
          ORDER BY dh.donation_date DESC
        `,
          [dateRange.start, dateRange.end]
        );
        data = {donations};
        break;

      case 'campaigns':
        const [campaigns] = await pool.execute(
          `
          SELECT 
            c.*,
            COUNT(DISTINCT ts.id) as total_slots,
            COUNT(DISTINCT a.id) as total_appointments,
            SUM(CASE WHEN a.donation_completed = 1 THEN 1 ELSE 0 END) as successful_donations
          FROM campaigns c
          LEFT JOIN time_slots ts ON c.id = ts.campaign_id
          LEFT JOIN appointments a ON ts.id = a.time_slot_id
          WHERE c.start_date BETWEEN ? AND ?
          GROUP BY c.id
          ORDER BY c.start_date DESC
        `,
          [dateRange.start, dateRange.end]
        );
        data = {campaigns};
        break;

      default:
        // Export complet
        const [fullExport] = await pool.execute(
          `
          SELECT 
            'donation' as type,
            dh.donation_date as date,
            u.first_name, u.last_name,
            mp.blood_group,
            dh.volume_ml,
            c.name as campaign_name,
            c.city
          FROM donation_history dh
          JOIN users u ON dh.user_id = u.id
          JOIN medical_profiles mp ON u.id = mp.user_id
          LEFT JOIN appointments a ON dh.appointment_id = a.id
          LEFT JOIN campaigns c ON a.campaign_id = c.id
          WHERE dh.donation_date BETWEEN ? AND ?
          ORDER BY dh.donation_date DESC
        `,
          [dateRange.start, dateRange.end]
        );
        data = {export_data: fullExport};
    }

    res.json({
      export_info: {
        type,
        period: dateRange,
        exported_at: moment().toISOString(),
        total_records: Array.isArray(data[Object.keys(data)[0]])
          ? data[Object.keys(data)[0]].length
          : 0
      },
      ...data
    });
  } catch (error) {
    console.error('Erreur export analytics:', error);
    res.status(500).json({error: 'Erreur interne du serveur'});
  }
});

// Tâche automatique - Mise à jour des statistiques (optionnel)
cron.schedule('0 1 * * *', async () => {
  try {
    console.log('🔄 Exécution des tâches analytiques quotidiennes...');

    // Ici on pourrait calculer et stocker des statistiques pré-calculées
    // pour améliorer les performances des requêtes fréquentes

    console.log('✅ Tâches analytiques terminées');
  } catch (error) {
    console.error('❌ Erreur dans les tâches automatiques:', error);
  }
});

// Démarrer le serveur
async function startServer() {
  await initDatabase();

  app.listen(PORT, () => {
    console.log(`🚀 Analytics Service démarré sur le port ${PORT}`);
    console.log(`📊 Health check: http://localhost:${PORT}/health`);
    console.log(
      `📈 Dashboard: http://localhost:${PORT}/api/analytics/dashboard`
    );
  });
}

startServer().catch((error) => {
  console.error('❌ Erreur démarrage serveur:', error);
  process.exit(1);
});
