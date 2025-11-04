FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# Use --omit=dev to avoid installing dev dependencies in production images
RUN npm install --omit=dev --no-audit --no-fund

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Change ownership of the app directory
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "const http = require('http'); \
  const options = { hostname: 'localhost', port: 3001, path: '/health', timeout: 5000 }; \
  const req = http.request(options, (res) => { \
    if (res.statusCode === 200) process.exit(0); else process.exit(1); \
  }); \
  req.on('error', () => process.exit(1)); \
  req.on('timeout', () => process.exit(1)); \
  req.end();"

# Start application
CMD ["npm", "start"]