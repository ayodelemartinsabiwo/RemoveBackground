# ======================================
# Multi-stage Dockerfile for Node.js API
# Production-optimized with minimal image size
# ======================================

# Stage 1: Dependencies
FROM node:20-alpine AS deps

# Install security updates
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
COPY apps/api/package.json ./apps/api/

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 2: Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/api/node_modules ./apps/api/node_modules

# Copy source code
COPY apps/api ./apps/api
COPY packages/database ./packages/database

# Copy TypeScript config
COPY tsconfig.json ./
COPY apps/api/tsconfig.json ./apps/api/

# Generate Prisma client
WORKDIR /app/packages/database
RUN npx prisma generate

# Build TypeScript
WORKDIR /app/apps/api
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nodejs

WORKDIR /app

# Set environment to production
ENV NODE_ENV=production

# Copy necessary files from builder
COPY --from=builder --chown=nodejs:nodejs /app/apps/api/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/apps/api/package.json ./
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/packages/database/node_modules/.prisma ./node_modules/.prisma

# Create logs directory
RUN mkdir -p /app/logs && chown nodejs:nodejs /app/logs

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start server with dumb-init
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
