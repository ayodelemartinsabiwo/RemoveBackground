/**
 * Express Server Entry Point
 * Production-grade API server with all middleware and routes
 * Zero tolerance for errors - comprehensive error handling
 */

import express, { Application } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import morgan from 'morgan';
import env from './config/env';
import logger from './utils/logger';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';
import { globalRateLimiter } from './middleware/rateLimit';

// Import routes
import healthRoutes from './routes/health.routes';
import authRoutes from './routes/auth.routes';
import imageRoutes from './routes/image.routes';
import userRoutes from './routes/user.routes';

// Import database and services
import prisma from './config/database';
import redisClient from './config/redis';

/**
 * Fix BigInt JSON serialization
 * PostgreSQL BigInt columns cannot be serialized by default
 */
(BigInt.prototype as any).toJSON = function () {
  return this.toString();
};

/**
 * Create Express application
 */
const app: Application = express();

/**
 * Security middleware
 */
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
    crossOriginEmbedderPolicy: false, // Allow S3 presigned URLs
  })
);

/**
 * CORS configuration
 */
app.use(
  cors({
    origin: env.CORS_ORIGIN,
    credentials: env.CORS_CREDENTIALS,
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  })
);

/**
 * Body parsing middleware
 */
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

/**
 * Compression middleware
 */
app.use(compression());

/**
 * Request logging (HTTP requests)
 */
if (env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
} else {
  app.use(
    morgan('combined', {
      stream: {
        write: (message: string) => logger.http(message.trim()),
      },
    })
  );
}

/**
 * Rate limiting (disabled in test environment)
 */
if (env.ENABLE_RATE_LIMITING && env.NODE_ENV !== 'test') {
  app.use(globalRateLimiter);
  logger.info('Rate limiting enabled');
}

/**
 * Health check routes (no /api prefix for Kubernetes)
 */
app.use('/', healthRoutes);

/**
 * API routes (versioned)
 */
const API_PREFIX = `/api/${env.API_VERSION}`;

app.use(`${API_PREFIX}/auth`, authRoutes);
app.use(`${API_PREFIX}/users`, userRoutes);
app.use(`${API_PREFIX}/images`, imageRoutes);

/**
 * 404 handler (must be after all routes)
 */
app.use(notFoundHandler);

/**
 * Global error handler (must be last)
 */
app.use(errorHandler);

/**
 * Start server
 */
const PORT = env.PORT;

async function startServer(): Promise<void> {
  try {
    // Test database connection
    await prisma.$connect();
    logger.info('✅ Database connected');

    // Test Redis connection
    await redisClient.ping();
    logger.info('✅ Redis connected');

    // Start listening
    const server = app.listen(PORT, () => {
      logger.info(`🚀 Server running on port ${PORT}`);
      logger.info(`📍 Environment: ${env.NODE_ENV}`);
      logger.info(`🔗 API URL: http://localhost:${PORT}${API_PREFIX}`);
      logger.info(`💚 Health check: http://localhost:${PORT}/health`);
    });

    // Graceful shutdown
    const gracefulShutdown = async (signal: string): Promise<void> => {
      logger.info(`${signal} received. Starting graceful shutdown...`);

      server.close(async () => {
        logger.info('HTTP server closed');

        try {
          await prisma.$disconnect();
          logger.info('Database disconnected');

          await redisClient.quit();
          logger.info('Redis disconnected');

          logger.info('Graceful shutdown complete');
          process.exit(0);
        } catch (error) {
          logger.error('Error during shutdown:', error);
          process.exit(1);
        }
      });

      // Force shutdown after 30 seconds
      setTimeout(() => {
        logger.error('Forced shutdown after 30s timeout');
        process.exit(1);
      }, 30000);
    };

    // Listen for shutdown signals
    process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
    process.on('SIGINT', () => gracefulShutdown('SIGINT'));

    // Handle uncaught errors
    process.on('uncaughtException', (error: Error) => {
      logger.error('Uncaught exception:', error);
      gracefulShutdown('UNCAUGHT_EXCEPTION');
    });

    process.on('unhandledRejection', (reason: unknown) => {
      logger.error('Unhandled rejection:', reason);
      gracefulShutdown('UNHANDLED_REJECTION');
    });
  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

/**
 * Start server if not in test mode
 */
if (env.NODE_ENV !== 'test') {
  startServer();
}

export default app;
