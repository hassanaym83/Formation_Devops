const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration axios pour forcer IPv4 (résoudre localhost en 127.0.0.1)
axios.defaults.family = 4; // Force IPv4

// Configuration
const VALIDATION_SERVICE_URL =
  process.env.VALIDATION_SERVICE_URL || 'http://localhost:3001';
const DATABASE_SERVICE_URL =
  process.env.DATABASE_SERVICE_URL || 'http://database-service:3002';

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(express.static('views'));

// Logging middleware
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${req.method} ${req.path} - Frontend Service`);
  next();
});

// Routes

// Page d'accueil
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Health check
app.get('/health', (req, res) => {
  res.json({
    service: 'frontend-service',
    status: 'healthy',
    timestamp: new Date().toISOString(),
    pod: process.env.HOSTNAME || 'localhost',
    communication: {
      validation_service: VALIDATION_SERVICE_URL,
      database_service: DATABASE_SERVICE_URL
    }
  });
});

// Page de démonstration des communications
app.get('/demo', async (req, res) => {
  const results = {
    service: 'frontend-service',
    timestamp: new Date().toISOString(),
    communications: {}
  };

  try {
    // Test communication intra-pod (validation service)
    console.log('Testing intra-pod communication...');
    const validationResponse = await axios.get(
      `${VALIDATION_SERVICE_URL}/health`,
      {timeout: 5000}
    );
    results.communications.intra_pod = {
      target: 'validation-service',
      url: VALIDATION_SERVICE_URL,
      status: 'success',
      response: validationResponse.data
    };
  } catch (error) {
    results.communications.intra_pod = {
      target: 'validation-service',
      url: VALIDATION_SERVICE_URL,
      status: 'error',
      error: error.message
    };
  }

  try {
    // Test communication inter-pod (database service)
    console.log('Testing inter-pod communication...');
    const databaseResponse = await axios.get(`${DATABASE_SERVICE_URL}/health`, {
      timeout: 5000
    });
    results.communications.inter_pod = {
      target: 'database-service',
      url: DATABASE_SERVICE_URL,
      status: 'success',
      response: databaseResponse.data
    };
  } catch (error) {
    results.communications.inter_pod = {
      target: 'database-service',
      url: DATABASE_SERVICE_URL,
      status: 'error',
      error: error.message
    };
  }

  res.json(results);
});

// Validation d'utilisateur (intra + inter pod)
app.post('/validate-user', async (req, res) => {
  const {name, email, phone} = req.body;

  console.log('Starting user validation process...');

  try {
    // Étape 1: Validation via service intra-pod
    console.log('Step 1: Validating via intra-pod service...');
    const validationResponse = await axios.post(
      `${VALIDATION_SERVICE_URL}/validate`,
      {
        name,
        email,
        phone
      },
      {timeout: 5000}
    );

    if (!validationResponse.data.isValid) {
      return res.status(400).json({
        success: false,
        step: 'validation',
        communication: 'intra-pod',
        errors: validationResponse.data.errors
      });
    }

    // Étape 2: Sauvegarde via service inter-pod
    console.log('Step 2: Saving via inter-pod service...');
    const saveResponse = await axios.post(
      `${DATABASE_SERVICE_URL}/users`,
      {
        name,
        email,
        phone
      },
      {timeout: 5000}
    );

    res.json({
      success: true,
      message: 'User validated and saved successfully',
      user: saveResponse.data,
      communication_flow: [
        {
          step: 1,
          type: 'intra-pod',
          service: 'validation-service',
          url: VALIDATION_SERVICE_URL,
          result: 'success'
        },
        {
          step: 2,
          type: 'inter-pod',
          service: 'database-service',
          url: DATABASE_SERVICE_URL,
          result: 'success'
        }
      ]
    });
  } catch (error) {
    console.error('Error in validation process:', error.message);
    res.status(500).json({
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Liste des utilisateurs (via database service)
app.get('/users', async (req, res) => {
  try {
    console.log('Fetching users via inter-pod communication...');
    const response = await axios.get(`${DATABASE_SERVICE_URL}/users`, {
      timeout: 5000
    });

    res.json({
      communication: 'inter-pod',
      target: 'database-service',
      data: response.data
    });
  } catch (error) {
    console.error('Error fetching users:', error.message);
    res.status(500).json({
      error: 'Failed to fetch users',
      communication: 'inter-pod',
      target: 'database-service',
      details: error.message
    });
  }
});

// Créer un utilisateur (via database service)
app.post('/users', async (req, res) => {
  try {
    console.log('Creating user via inter-pod communication...');
    const response = await axios.post(
      `${DATABASE_SERVICE_URL}/users`,
      req.body,
      {timeout: 5000}
    );

    res.json({
      communication: 'inter-pod',
      target: 'database-service',
      data: response.data
    });
  } catch (error) {
    console.error('Error creating user:', error.message);
    res.status(500).json({
      error: 'Failed to create user',
      communication: 'inter-pod',
      target: 'database-service',
      details: error.message
    });
  }
});

// Test de connectivité aux services
app.get('/connectivity', async (req, res) => {
  const results = {
    service: 'frontend-service',
    timestamp: new Date().toISOString(),
    tests: []
  };

  // Test validation service (intra-pod)
  try {
    const start = Date.now();
    await axios.get(`${VALIDATION_SERVICE_URL}/health`, {timeout: 3000});
    const duration = Date.now() - start;

    results.tests.push({
      target: 'validation-service',
      type: 'intra-pod',
      url: VALIDATION_SERVICE_URL,
      status: 'success',
      duration_ms: duration
    });
  } catch (error) {
    results.tests.push({
      target: 'validation-service',
      type: 'intra-pod',
      url: VALIDATION_SERVICE_URL,
      status: 'error',
      error: error.message
    });
  }

  // Test database service (inter-pod)
  try {
    const start = Date.now();
    await axios.get(`${DATABASE_SERVICE_URL}/health`, {timeout: 3000});
    const duration = Date.now() - start;

    results.tests.push({
      target: 'database-service',
      type: 'inter-pod',
      url: DATABASE_SERVICE_URL,
      status: 'success',
      duration_ms: duration
    });
  } catch (error) {
    results.tests.push({
      target: 'database-service',
      type: 'inter-pod',
      url: DATABASE_SERVICE_URL,
      status: 'error',
      error: error.message
    });
  }

  res.json(results);
});

// Error handler
app.use((error, req, res, next) => {
  console.error('Frontend Service Error:', error);
  res.status(500).json({
    service: 'frontend-service',
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    service: 'frontend-service',
    error: 'Route not found',
    path: req.path,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Frontend Service running on port ${PORT}`);
  console.log(`📡 Validation Service URL: ${VALIDATION_SERVICE_URL}`);
  console.log(`🗄️  Database Service URL: ${DATABASE_SERVICE_URL}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`🎯 Demo page: http://localhost:${PORT}/demo`);
});

module.exports = app;
