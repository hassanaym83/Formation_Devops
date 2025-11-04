const express = require('express');
const {v4: uuidv4} = require('uuid');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3002;

// In-memory database
let users = [
  {
    id: '1',
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+1234567890',
    created_at: new Date().toISOString()
  },
  {
    id: '2',
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    phone: '+0987654321',
    created_at: new Date().toISOString()
  }
];

// Statistics
let stats = {
  requests: 0,
  users_created: 0,
  users_updated: 0,
  users_deleted: 0,
  start_time: new Date().toISOString()
};

// Middleware
app.use(cors());
app.use(express.json());

// Logging middleware
app.use((req, res, next) => {
  stats.requests++;
  const timestamp = new Date().toISOString();
  console.log(
    `[${timestamp}] ${req.method} ${req.path} - Database Service (INTER-POD)`
  );
  next();
});

// Routes

// Health check
app.get('/health', (req, res) => {
  console.log('Health check requested - responding from database service');
  res.json({
    service: 'database-service',
    status: 'healthy',
    timestamp: new Date().toISOString(),
    pod: process.env.HOSTNAME || 'localhost',
    communication_type: 'inter-pod',
    accessible_from: 'any pod via Service DNS',
    database: {
      users_count: users.length,
      total_requests: stats.requests
    }
  });
});

// Get all users
app.get('/users', (req, res) => {
  console.log(`Fetching all users - count: ${users.length}`);

  const response = {
    service: 'database-service',
    communication_type: 'inter-pod',
    data: users,
    count: users.length,
    timestamp: new Date().toISOString()
  };

  res.json(response.data); // Return only users array for simplicity
});

// Get user by ID
app.get('/users/:id', (req, res) => {
  const {id} = req.params;
  console.log(`Fetching user by ID: ${id}`);

  const user = users.find((u) => u.id === id);

  if (!user) {
    console.log(`User not found: ${id}`);
    return res.status(404).json({
      service: 'database-service',
      error: 'User not found',
      id,
      timestamp: new Date().toISOString()
    });
  }

  console.log(`User found: ${user.name}`);
  res.json(user);
});

// Create new user
app.post('/users', (req, res) => {
  const {name, email, phone} = req.body;

  console.log('Creating new user:', {name, email, phone});

  // Validation
  if (!name || !email || !phone) {
    console.log('Missing required fields');
    return res.status(400).json({
      service: 'database-service',
      error: 'Missing required fields',
      required: ['name', 'email', 'phone'],
      timestamp: new Date().toISOString()
    });
  }

  // Check if email already exists
  const existingUser = users.find((u) => u.email === email);
  if (existingUser) {
    console.log(`Email already exists: ${email}`);
    return res.status(409).json({
      service: 'database-service',
      error: 'Email already exists',
      email,
      timestamp: new Date().toISOString()
    });
  }

  // Create new user
  const newUser = {
    id: uuidv4(),
    name,
    email,
    phone,
    created_at: new Date().toISOString()
  };

  users.push(newUser);
  stats.users_created++;

  console.log(`✅ User created successfully: ${newUser.id} - ${newUser.name}`);

  res.status(201).json({
    service: 'database-service',
    message: 'User created successfully',
    user: newUser,
    communication_type: 'inter-pod',
    timestamp: new Date().toISOString()
  });
});

// Update user
app.put('/users/:id', (req, res) => {
  const {id} = req.params;
  const {name, email, phone} = req.body;

  console.log(`Updating user: ${id}`, {name, email, phone});

  const userIndex = users.findIndex((u) => u.id === id);

  if (userIndex === -1) {
    console.log(`User not found for update: ${id}`);
    return res.status(404).json({
      service: 'database-service',
      error: 'User not found',
      id,
      timestamp: new Date().toISOString()
    });
  }

  // Check if new email conflicts with other users
  if (email && email !== users[userIndex].email) {
    const emailConflict = users.find((u) => u.email === email && u.id !== id);
    if (emailConflict) {
      console.log(`Email conflict during update: ${email}`);
      return res.status(409).json({
        service: 'database-service',
        error: 'Email already exists',
        email,
        timestamp: new Date().toISOString()
      });
    }
  }

  // Update user
  const updatedUser = {
    ...users[userIndex],
    ...(name && {name}),
    ...(email && {email}),
    ...(phone && {phone}),
    updated_at: new Date().toISOString()
  };

  users[userIndex] = updatedUser;
  stats.users_updated++;

  console.log(`✅ User updated successfully: ${id} - ${updatedUser.name}`);

  res.json({
    service: 'database-service',
    message: 'User updated successfully',
    user: updatedUser,
    communication_type: 'inter-pod',
    timestamp: new Date().toISOString()
  });
});

// Delete user
app.delete('/users/:id', (req, res) => {
  const {id} = req.params;

  console.log(`Deleting user: ${id}`);

  const userIndex = users.findIndex((u) => u.id === id);

  if (userIndex === -1) {
    console.log(`User not found for deletion: ${id}`);
    return res.status(404).json({
      service: 'database-service',
      error: 'User not found',
      id,
      timestamp: new Date().toISOString()
    });
  }

  const deletedUser = users[userIndex];
  users.splice(userIndex, 1);
  stats.users_deleted++;

  console.log(`✅ User deleted successfully: ${id} - ${deletedUser.name}`);

  res.json({
    service: 'database-service',
    message: 'User deleted successfully',
    deleted_user: deletedUser,
    communication_type: 'inter-pod',
    timestamp: new Date().toISOString()
  });
});

// Clear all users
app.delete('/users', (req, res) => {
  const deletedCount = users.length;
  console.log(`Clearing all users - count: ${deletedCount}`);

  users = [];
  stats.users_deleted += deletedCount;

  console.log(`✅ All users cleared`);

  res.json({
    service: 'database-service',
    message: 'All users deleted successfully',
    deleted_count: deletedCount,
    communication_type: 'inter-pod',
    timestamp: new Date().toISOString()
  });
});

// Get database statistics
app.get('/stats', (req, res) => {
  console.log('Statistics requested');

  const currentStats = {
    service: 'database-service',
    communication_type: 'inter-pod',
    database: {
      users_count: users.length,
      total_users_created: stats.users_created,
      total_users_updated: stats.users_updated,
      total_users_deleted: stats.users_deleted
    },
    server: {
      uptime_seconds: process.uptime(),
      total_requests: stats.requests,
      start_time: stats.start_time,
      memory_usage: process.memoryUsage(),
      node_version: process.version,
      platform: process.platform
    },
    timestamp: new Date().toISOString()
  };

  res.json(currentStats);
});

// Search users
app.get('/search', (req, res) => {
  const {q, field} = req.query;

  console.log(`Searching users: query="${q}", field="${field}"`);

  if (!q) {
    return res.status(400).json({
      service: 'database-service',
      error: 'Query parameter "q" is required',
      example: '/search?q=john&field=name',
      timestamp: new Date().toISOString()
    });
  }

  let filteredUsers = users;

  if (field) {
    filteredUsers = users.filter((user) => {
      if (user[field]) {
        return user[field].toLowerCase().includes(q.toLowerCase());
      }
      return false;
    });
  } else {
    filteredUsers = users.filter((user) => {
      return (
        user.name.toLowerCase().includes(q.toLowerCase()) ||
        user.email.toLowerCase().includes(q.toLowerCase()) ||
        user.phone.includes(q)
      );
    });
  }

  console.log(`Search results: ${filteredUsers.length} users found`);

  res.json({
    service: 'database-service',
    query: q,
    field: field || 'all',
    results: filteredUsers,
    count: filteredUsers.length,
    total_users: users.length,
    timestamp: new Date().toISOString()
  });
});

// Bulk operations
app.post('/users/bulk', (req, res) => {
  const {users: newUsers} = req.body;

  console.log(`Bulk user creation: ${newUsers?.length || 0} users`);

  if (!Array.isArray(newUsers) || newUsers.length === 0) {
    return res.status(400).json({
      service: 'database-service',
      error: 'Array of users is required',
      example: {
        users: [{name: 'John', email: 'john@example.com', phone: '123456789'}]
      },
      timestamp: new Date().toISOString()
    });
  }

  const results = {
    created: [],
    errors: []
  };

  newUsers.forEach((userData, index) => {
    const {name, email, phone} = userData;

    if (!name || !email || !phone) {
      results.errors.push({
        index,
        user: userData,
        error: 'Missing required fields'
      });
      return;
    }

    const existingUser = users.find((u) => u.email === email);
    if (existingUser) {
      results.errors.push({
        index,
        user: userData,
        error: 'Email already exists'
      });
      return;
    }

    const newUser = {
      id: uuidv4(),
      name,
      email,
      phone,
      created_at: new Date().toISOString()
    };

    users.push(newUser);
    results.created.push(newUser);
    stats.users_created++;
  });

  console.log(
    `✅ Bulk operation completed: ${results.created.length} created, ${results.errors.length} errors`
  );

  res.status(201).json({
    service: 'database-service',
    message: 'Bulk operation completed',
    results,
    summary: {
      total_requested: newUsers.length,
      created: results.created.length,
      errors: results.errors.length
    },
    timestamp: new Date().toISOString()
  });
});

// Error handler
app.use((error, req, res, next) => {
  console.error('Database Service Error:', error);
  res.status(500).json({
    service: 'database-service',
    error: 'Internal server error',
    timestamp: new Date().toISOString()
  });
});

// 404 handler
app.use((req, res) => {
  console.log(`404 - Route not found: ${req.method} ${req.path}`);
  res.status(404).json({
    service: 'database-service',
    error: 'Route not found',
    path: req.path,
    method: req.method,
    available_routes: [
      'GET /health',
      'GET /users',
      'GET /users/:id',
      'POST /users',
      'PUT /users/:id',
      'DELETE /users/:id',
      'DELETE /users',
      'GET /stats',
      'GET /search',
      'POST /users/bulk'
    ],
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`🗄️  Database Service running on port ${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
  console.log(`👥 Users API: http://localhost:${PORT}/users`);
  console.log(`📊 Statistics: http://localhost:${PORT}/stats`);
  console.log(`🎯 Communication type: INTER-POD (accessible via Service DNS)`);
  console.log(`📚 Initial users loaded: ${users.length}`);
});

module.exports = app;
