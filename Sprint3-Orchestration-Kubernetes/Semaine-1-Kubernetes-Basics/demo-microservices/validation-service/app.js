const express = require('express');
const validator = require('validator');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Logging middleware
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(
    `[${timestamp}] ${req.method} ${req.path} - Validation Service (INTRA-POD)`
  );
  next();
});

// Validation rules
const VALIDATION_RULES = {
  name: {
    minLength: 2,
    maxLength: 50,
    pattern: /^[a-zA-ZÀ-ÿ\s\-']+$/,
    description: 'Nom doit contenir 2-50 caractères, lettres uniquement'
  },
  email: {
    description: 'Email doit être valide (exemple@domaine.com)'
  },
  phone: {
    minLength: 10,
    maxLength: 15,
    pattern: /^[\d\s\-\+\(\)]+$/,
    description: 'Téléphone doit contenir 10-15 chiffres'
  }
};

// Routes

// Health check
app.get('/health', (req, res) => {
  console.log('Health check requested - responding from validation service');
  res.json({
    service: 'validation-service',
    status: 'healthy',
    timestamp: new Date().toISOString(),
    pod: process.env.HOSTNAME || 'localhost',
    communication_type: 'intra-pod',
    accessible_from: 'frontend-service via localhost'
  });
});

// Get validation rules
app.get('/rules', (req, res) => {
  console.log('Validation rules requested');
  res.json({
    service: 'validation-service',
    rules: VALIDATION_RULES,
    timestamp: new Date().toISOString()
  });
});

// Validate user data
app.post('/validate', (req, res) => {
  const {name, email, phone} = req.body;

  console.log('Validation request received:', {name, email, phone});

  const errors = [];
  const validationResult = {
    service: 'validation-service',
    timestamp: new Date().toISOString(),
    communication_type: 'intra-pod',
    input: {name, email, phone},
    validation: {}
  };

  // Validate name
  if (!name) {
    errors.push('Nom est requis');
    validationResult.validation.name = {valid: false, error: 'Nom est requis'};
  } else if (
    name.length < VALIDATION_RULES.name.minLength ||
    name.length > VALIDATION_RULES.name.maxLength
  ) {
    errors.push(
      `Nom doit contenir entre ${VALIDATION_RULES.name.minLength} et ${VALIDATION_RULES.name.maxLength} caractères`
    );
    validationResult.validation.name = {
      valid: false,
      error: 'Longueur invalide'
    };
  } else if (!VALIDATION_RULES.name.pattern.test(name)) {
    errors.push('Nom contient des caractères invalides');
    validationResult.validation.name = {
      valid: false,
      error: 'Caractères invalides'
    };
  } else {
    validationResult.validation.name = {valid: true};
    console.log(`✅ Name validation passed: ${name}`);
  }

  // Validate email
  if (!email) {
    errors.push('Email est requis');
    validationResult.validation.email = {
      valid: false,
      error: 'Email est requis'
    };
  } else if (!validator.isEmail(email)) {
    errors.push('Format email invalide');
    validationResult.validation.email = {
      valid: false,
      error: 'Format invalide'
    };
  } else {
    validationResult.validation.email = {valid: true};
    console.log(`✅ Email validation passed: ${email}`);
  }

  // Validate phone
  if (!phone) {
    errors.push('Téléphone est requis');
    validationResult.validation.phone = {
      valid: false,
      error: 'Téléphone est requis'
    };
  } else if (
    phone.length < VALIDATION_RULES.phone.minLength ||
    phone.length > VALIDATION_RULES.phone.maxLength
  ) {
    errors.push(
      `Téléphone doit contenir entre ${VALIDATION_RULES.phone.minLength} et ${VALIDATION_RULES.phone.maxLength} caractères`
    );
    validationResult.validation.phone = {
      valid: false,
      error: 'Longueur invalide'
    };
  } else if (!VALIDATION_RULES.phone.pattern.test(phone)) {
    errors.push('Format téléphone invalide');
    validationResult.validation.phone = {
      valid: false,
      error: 'Format invalide'
    };
  } else {
    validationResult.validation.phone = {valid: true};
    console.log(`✅ Phone validation passed: ${phone}`);
  }

  // Final result
  const isValid = errors.length === 0;
  validationResult.isValid = isValid;
  validationResult.errors = errors;

  if (isValid) {
    console.log('🎉 All validations passed successfully');
    validationResult.message = 'Validation réussie';
    res.json(validationResult);
  } else {
    console.log('❌ Validation failed:', errors);
    validationResult.message = 'Validation échouée';
    res.status(400).json(validationResult);
  }
});

// Validate specific field
app.post('/validate/:field', (req, res) => {
  const field = req.params.field;
  const {value} = req.body;

  console.log(`Validating single field: ${field} = ${value}`);

  if (!VALIDATION_RULES[field]) {
    return res.status(400).json({
      service: 'validation-service',
      error: `Field '${field}' not supported`,
      supported_fields: Object.keys(VALIDATION_RULES),
      timestamp: new Date().toISOString()
    });
  }

  let isValid = false;
  let error = null;

  switch (field) {
    case 'name':
      if (!value) {
        error = 'Nom est requis';
      } else if (
        value.length < VALIDATION_RULES.name.minLength ||
        value.length > VALIDATION_RULES.name.maxLength
      ) {
        error = 'Longueur invalide';
      } else if (!VALIDATION_RULES.name.pattern.test(value)) {
        error = 'Caractères invalides';
      } else {
        isValid = true;
      }
      break;
    case 'email':
      if (!value) {
        error = 'Email est requis';
      } else if (!validator.isEmail(value)) {
        error = 'Format email invalide';
      } else {
        isValid = true;
      }
      break;
    case 'phone':
      if (!value) {
        error = 'Téléphone est requis';
      } else if (
        value.length < VALIDATION_RULES.phone.minLength ||
        value.length > VALIDATION_RULES.phone.maxLength
      ) {
        error = 'Longueur invalide';
      } else if (!VALIDATION_RULES.phone.pattern.test(value)) {
        error = 'Format invalide';
      } else {
        isValid = true;
      }
      break;
  }

  const result = {
    service: 'validation-service',
    field,
    value,
    isValid,
    error,
    rule: VALIDATION_RULES[field],
    timestamp: new Date().toISOString()
  };

  console.log(
    `Field validation result: ${field} = ${isValid ? 'VALID' : 'INVALID'}`
  );

  res.json(result);
});

// Get validation statistics
app.get('/stats', (req, res) => {
  // Simple in-memory stats (in production, use proper storage)
  const stats = {
    service: 'validation-service',
    uptime_seconds: process.uptime(),
    memory_usage: process.memoryUsage(),
    timestamp: new Date().toISOString(),
    node_version: process.version,
    platform: process.platform,
    environment: process.env.NODE_ENV || 'development'
  };

  console.log('Statistics requested');
  res.json(stats);
});

// Error handler
app.use((error, req, res, next) => {
  console.error('Validation Service Error:', error);
  res.status(500).json({
    service: 'validation-service',
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  console.log(`404 - Route not found: ${req.method} ${req.path}`);
  res.status(404).json({
    service: 'validation-service',
    error: 'Route not found',
    path: req.path,
    method: req.method,
    available_routes: [
      'GET /health',
      'GET /rules',
      'POST /validate',
      'POST /validate/:field',
      'GET /stats'
    ],
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🔍 Validation Service running on port ${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`📋 Validation rules: http://localhost:${PORT}/rules`);
  console.log(`🎯 Communication type: INTRA-POD (accessible via localhost)`);
});

module.exports = app;
