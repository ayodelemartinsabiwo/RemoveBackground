/**
 * Health Check Controllers
 * Monitors service health and dependencies
 * Production-grade for Kubernetes liveness/readiness probes
 */

import { Request, Response } from 'express';
import { isDatabaseHealthy } from '../config/database';
import { isRedisHealthy } from '../config/redis';
import { isS3Healthy } from '../config/s3';
import { getQueueStats } from '../services/queue.service';
import { asyncHandler, HttpStatus } from '../middleware/errorHandler';
import env from '../config/env';

/**
 * Basic health check
 * GET /health
 * Returns 200 if service is running
 */
export const healthCheck = asyncHandler(async (req: Request, res: Response) => {
  res.status(HttpStatus.OK).json({
    success: true,
    message: 'Service is healthy',
    timestamp: new Date().toISOString(),
  });
});

/**
 * Readiness probe
 * GET /ready
 * Returns 200 if service and all dependencies are ready
 * Used by Kubernetes to determine if pod can receive traffic
 */
export const readinessCheck = asyncHandler(async (req: Request, res: Response) => {
  const checks = await Promise.all([
    isDatabaseHealthy().then((healthy) => ({ database: healthy })),
    isRedisHealthy().then((healthy) => ({ redis: healthy })),
    isS3Healthy().then((healthy) => ({ s3: healthy })),
  ]);

  const results = Object.assign({}, ...checks);
  const allHealthy = Object.values(results).every((v) => v === true);

  if (allHealthy) {
    res.status(HttpStatus.OK).json({
      success: true,
      message: 'Service is ready',
      checks: results,
      timestamp: new Date().toISOString(),
    });
  } else {
    res.status(HttpStatus.SERVICE_UNAVAILABLE).json({
      success: false,
      message: 'Service is not ready',
      checks: results,
      timestamp: new Date().toISOString(),
    });
  }
});

/**
 * Liveness probe
 * GET /live
 * Returns 200 if service is alive
 * Used by Kubernetes to determine if pod should be restarted
 */
export const livenessCheck = asyncHandler(async (req: Request, res: Response) => {
  // Simple check - if we can respond, we're alive
  res.status(HttpStatus.OK).json({
    success: true,
    message: 'Service is alive',
    timestamp: new Date().toISOString(),
  });
});

/**
 * Detailed status endpoint
 * GET /status
 * Returns detailed service metrics
 * Should be protected in production
 */
export const statusCheck = asyncHandler(async (req: Request, res: Response) => {
  const [dbHealthy, redisHealthy, s3Healthy, queueStats] = await Promise.all([
    isDatabaseHealthy(),
    isRedisHealthy(),
    isS3Healthy(),
    getQueueStats(),
  ]);

  const status = {
    service: {
      name: 'palmar-bg-api',
      version: env.API_VERSION,
      environment: env.NODE_ENV,
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
    },
    dependencies: {
      database: {
        healthy: dbHealthy,
        type: 'postgresql',
      },
      redis: {
        healthy: redisHealthy,
        type: 'redis',
      },
      storage: {
        healthy: s3Healthy,
        type: 's3/minio',
      },
    },
    queue: queueStats,
    system: {
      memory: {
        used: Math.round(process.memoryUsage().heapUsed / 1024 / 1024),
        total: Math.round(process.memoryUsage().heapTotal / 1024 / 1024),
        unit: 'MB',
      },
      cpu: {
        usage: process.cpuUsage(),
      },
    },
  };

  const allHealthy = dbHealthy && redisHealthy && s3Healthy;

  res.status(allHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE).json({
    success: allHealthy,
    data: status,
  });
});
