import axios from 'axios';

// Configuration des URLs de base pour chaque service
const API_URLS = {
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
const createServiceClient = (baseURL) => {
  const client = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json'
    }
  });

  // Intercepteur pour ajouter le token d'authentification
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
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
      if (error.response?.status === 401) {
        // Token expiré, déconnecter l'utilisateur
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );

  return client;
};

// Clients pour chaque service
const userService = createServiceClient(API_URLS.USER_SERVICE);
const campaignService = createServiceClient(API_URLS.CAMPAIGN_SERVICE);
const appointmentService = createServiceClient(API_URLS.APPOINTMENT_SERVICE);
const analyticsService = createServiceClient(API_URLS.ANALYTICS_SERVICE);

// API Authentification (User Service)
export const authAPI = {
  login: (email, password) =>
    userService.post('/api/users/login', {email, password}),

  register: (userData) => userService.post('/api/users/register', userData),

  getProfile: () => userService.get('/api/users/profile'),

  updateProfile: (userData) => userService.put('/api/users/profile', userData),

  getMedicalProfile: (userId) =>
    userService.get(`/api/users/${userId}/medical-profile`),

  updateMedicalProfile: (userId, medicalData) =>
    userService.put(`/api/users/${userId}/medical-profile`, medicalData),

  getDonationHistory: (userId, page = 1) =>
    userService.get(`/api/users/${userId}/donation-history?page=${page}`)
};

// API Campagnes (Campaign Service)
export const campaignAPI = {
  getCampaigns: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach((key) => {
      if (filters[key]) params.append(key, filters[key]);
    });
    return campaignService.get(`/api/campaigns?${params}`);
  },

  getCampaignById: (id) => campaignService.get(`/api/campaigns/${id}`),

  searchNearby: (latitude, longitude, radius = 20) =>
    campaignService.get(
      `/api/campaigns/nearby?lat=${latitude}&lng=${longitude}&radius=${radius}`
    ),

  getCampaignStats: (id) => campaignService.get(`/api/campaigns/${id}/stats`)
};

// API Rendez-vous (Appointment Service)
export const appointmentAPI = {
  getAvailableSlots: (campaignId, date = null) => {
    const params = date ? `?date=${date}` : '';
    return appointmentService.get(
      `/api/appointments/slots/${campaignId}${params}`
    );
  },

  bookAppointment: (bookingData) =>
    appointmentService.post('/api/appointments/book', bookingData),

  getUserAppointments: (page = 1, status = '') => {
    const params = new URLSearchParams({page: page.toString()});
    if (status) params.append('status', status);

    const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
    return appointmentService.get(`/api/appointments/user/${userId}?${params}`);
  },

  confirmAppointment: (appointmentId, confirmationCode) =>
    appointmentService.put(`/api/appointments/${appointmentId}/confirm`, {
      confirmation_code: confirmationCode
    }),

  cancelAppointment: (appointmentId) => {
    const userId = JSON.parse(localStorage.getItem('user') || '{}').id;
    return appointmentService.delete(
      `/api/appointments/${appointmentId}/cancel`,
      {
        data: {user_id: userId}
      }
    );
  }
};

// API Analytics (Analytics Service)
export const analyticsAPI = {
  getDashboard: (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return analyticsService.get(`/api/analytics/dashboard?${params}`);
  },

  getUserStats: (startDate = null, endDate = null) => {
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

  // Validation des réponses
  validateResponse: (response) => {
    if (!response || typeof response !== 'object') {
      throw new Error('Réponse invalide du serveur');
    }
    return response;
  }
};

export default {
  authAPI,
  campaignAPI,
  appointmentAPI,
  analyticsAPI,
  apiUtils
};
