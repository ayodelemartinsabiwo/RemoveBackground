/**
 * Authentication Routes
 * Defines all authentication-related endpoints
 */

import { Router } from 'express';
import {
  register,
  login,
  refresh,
  logout,
  getProfile,
  registerSchema,
  loginSchema,
  refreshTokenSchema,
} from '../controllers/auth.controller';
import { authenticate } from '../middleware/auth';
import { validateBody } from '../middleware/validation';

const router = Router();

/**
 * POST /api/v1/auth/register
 * Register a new user account
 */
router.post('/register', validateBody(registerSchema), register);

/**
 * POST /api/v1/auth/login
 * Login with email and password
 */
router.post('/login', validateBody(loginSchema), login);

/**
 * POST /api/v1/auth/refresh
 * Refresh access token using refresh token
 */
router.post('/refresh', validateBody(refreshTokenSchema), refresh);

/**
 * POST /api/v1/auth/logout
 * Logout and revoke refresh token (requires authentication)
 */
router.post('/logout', authenticate, logout);

/**
 * GET /api/v1/auth/me
 * Get current user profile (requires authentication)
 */
router.get('/me', authenticate, getProfile);

export default router;
