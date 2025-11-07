import axios from 'axios';

// Configuration des URLs de base pour chaque service
const API_URLS = {
  ADMIN_SERVICE:
    process.env.REACT_APP_ADMIN_SERVICE_URL || 'http://localhost:3005',
  USER_SERVICE:
    process.env.REACT_APP_USER_SERVICE_URL || 'http://localhost:3001',
  CAMPAIGN_SERVICE:
    process.env.REACT_APP_CAMPAIGN_SERVICE_URL || 'http://localhost:3002',
  APPOINTMENT_SERVICE:
    process.env.REACT_APP_APPOINTMENT_SERVICE_URL || 'http://localhost:3003',
  ANALYTICS_SERVICE:
    process.env.REACT_APP_ANALYTICS_SERVICE_URL || 'http://localhost:3004'
};

// Création des instances Axios pour chaque service
const createServiceClient = (baseURL, isAdminAuth = false) => {
  const client = axios.create({
    baseURL,
    timeout: 15000,
    headers: {
      'Content-Type': 'application/json'
    }
  });

  // Intercepteur pour ajouter le token d'authentification admin
  client.interceptors.request.use(
    (config) => {
      const tokenKey = isAdminAuth ? 'adminToken' : 'token';
      const token = localStorage.getItem(tokenKey);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Intercepteur pour gérer les erreurs
  client.interceptors.response.use(
    (response) => response.data,
    (error) => {
      if (error.response?.status === 401 && isAdminAuth) {
        // Token admin expiré
        localStorage.removeItem('adminToken');
        localStorage.removeItem('adminUser');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// Clients pour chaque service
const adminService = createServiceClient(API_URLS.ADMIN_SERVICE, true);
const userService = createServiceClient(API_URLS.USER_SERVICE);
const campaignService = createServiceClient(API_URLS.CAMPAIGN_SERVICE);
const appointmentService = createServiceClient(API_URLS.APPOINTMENT_SERVICE);
const analyticsService = createServiceClient(API_URLS.ANALYTICS_SERVICE);

// API Administration (Admin Service)
export const adminAPI = {
  // Authentification admin
  login: (username, password) =>
    adminService.post('/api/admin/login', {username, password}),

  // Dashboard admin
  getDashboard: () => adminService.get('/api/admin/dashboard'),

  // Gestion des utilisateurs
  getUsers: (page = 1, limit = 20, search = '', status = '') => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    });
    if (search) params.append('search', search);
    if (status) params.append('status', status);
    return adminService.get(`/api/admin/users?${params}`);
  },

  getUserById: (id) => adminService.get(`/api/admin/users/${id}`),

  updateUser: (id, userData) =>
    adminService.put(`/api/admin/users/${id}`, userData),

  toggleUserStatus: (id) =>
    adminService.put(`/api/admin/users/${id}/toggle-status`),

  // Gestion des campagnes
  getAdminCampaigns: (page = 1, limit = 20, status = '', city = '') => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    });
    if (status) params.append('status', status);
    if (city) params.append('city', city);
    return adminService.get(`/api/admin/campaigns?${params}`);
  },

  // Logs d'audit
  getAuditLogs: (page = 1, limit = 50, action = '', adminId = '') => {
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    });
    if (action) params.append('action', action);
    if (adminId) params.append('admin_id', adminId);
    return adminService.get(`/api/admin/audit-logs?${params}`);
  },

  // Statistiques système
  getSystemStats: () => adminService.get('/api/admin/system-stats'),

  // Créer un nouvel admin
  createAdmin: (adminData) =>
    adminService.post('/api/admin/create-admin', adminData)
};

// API Analytics (Analytics Service) - accès admin
export const adminAnalyticsAPI = {
  getDashboard: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/dashboard?${params}`);
  },

  getUserAnalytics: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/users?${params}`);
  },

  getCampaignAnalytics: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/campaigns?${params}`);
  },

  getSchedulingAnalytics: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/scheduling?${params}`);
  },

  getPredictions: () => analyticsService.get('/api/analytics/predictions'),

  exportData: (type = 'full', startDate = null, endDate = null) => {
    const params = new URLSearchParams({type});
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/export?${params}`);
  }
};

// API Campagnes (Campaign Service) - accès admin
export const adminCampaignAPI = {
  getCampaigns: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach((key) => {
      if (filters[key]) params.append(key, filters[key]);
    });
    return campaignService.get(`/api/campaigns?${params}`);
  },

  getCampaignById: (id) => campaignService.get(`/api/campaigns/${id}`),

  createCampaign: (campaignData) =>
    campaignService.post('/api/campaigns', campaignData),

  updateCampaign: (id, campaignData) =>
    campaignService.put(`/api/campaigns/${id}`, campaignData),

  deleteCampaign: (id) => campaignService.delete(`/api/campaigns/${id}`),

  getCampaignStats: (id) => campaignService.get(`/api/campaigns/${id}/stats`)
};

// API Rendez-vous (Appointment Service) - accès admin
export const adminAppointmentAPI = {
  getAppointments: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach((key) => {
      if (filters[key]) params.append(key, filters[key]);
    });
    return appointmentService.get(`/api/appointments?${params}`);
  },

  getAppointmentById: (id) => appointmentService.get(`/api/appointments/${id}`),

  completeAppointment: (id, completionData) =>
    appointmentService.put(`/api/appointments/${id}/complete`, completionData),

  getAppointmentStats: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return appointmentService.get(`/api/appointments/stats/overview?${params}`);
  }
};

// Utilitaires
export const apiUtils = {
  // Gestion des erreurs
  handleError: (error) => {
    if (error.response) {
      return error.response.data.error || 'Erreur du serveur';
    } else if (error.request) {
      return 'Impossible de contacter le serveur';
    } else {
      return 'Erreur inattendue';
    }
  },

  // Formatage des dates pour les API
  formatDate: (date) => {
    if (!date) return null;
    return new Date(date).toISOString().split('T')[0];
  },

  // Formatage des dates et heures
  formatDateTime: (date) => {
    if (!date) return null;
    return new Date(date).toISOString();
  },

  // Validation des réponses
  validateResponse: (response) => {
    if (!response || typeof response !== 'object') {
      throw new Error('Réponse invalide du serveur');
    }
    return response;
  },

  // Formatage des nombres
  formatNumber: (num) => {
    if (typeof num !== 'number') return num;
    return new Intl.NumberFormat('fr-FR').format(num);
  },

  // Formatage des pourcentages
  formatPercentage: (num, decimals = 1) => {
    if (typeof num !== 'number') return num;
    return `${num.toFixed(decimals)}%`;
  }
};

export default {
  adminAPI,
  adminAnalyticsAPI,
  adminCampaignAPI,
  adminAppointmentAPI,
  apiUtils
};
