/**
 * Health Check Routes
 * Kubernetes-compatible health endpoints
 */

import { Router } from 'express';
import {
  healthCheck,
  readinessCheck,
  livenessCheck,
  statusCheck,
} from '../controllers/health.controller';

const router = Router();

/**
 * GET /health
 * Basic health check
 */
router.get('/health', healthCheck);

/**
 * GET /ready
 * Readiness probe (checks dependencies)
 */
router.get('/ready', readinessCheck);

/**
 * GET /live
 * Liveness probe (checks if service is alive)
 */
router.get('/live', livenessCheck);

/**
 * GET /status
 * Detailed status (should be protected in production)
 */
router.get('/status', statusCheck);

export default router;
