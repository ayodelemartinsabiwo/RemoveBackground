/**
 * Authentication Controllers
 * Handle HTTP requests for authentication endpoints
 * Production-grade with proper error handling
 */

import { Request, Response } from 'express';
import { z } from 'zod';
import {
  registerUser,
  loginUser,
  refreshAccessToken,
  logoutUser,
} from '../services/auth.service';
import { asyncHandler, HttpStatus } from '../middleware/errorHandler';

/**
 * Validation Schemas
 */
export const registerSchema = z.object({
  email: z.string().email('Invalid email format').toLowerCase(),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .max(100, 'Password too long')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      'Password must contain uppercase, lowercase, and number'
    ),
  firstName: z.string().min(1).max(50).optional(),
  lastName: z.string().min(1).max(50).optional(),
});

export const loginSchema = z.object({
  email: z.string().email('Invalid email format').toLowerCase(),
  password: z.string().min(1, 'Password is required'),
});

export const refreshTokenSchema = z.object({
  refreshToken: z.string().min(1, 'Refresh token is required'),
});

/**
 * Register new user
 * POST /api/v1/auth/register
 */
export const register = asyncHandler(async (req: Request, res: Response) => {
  const input = req.body as z.infer<typeof registerSchema>;

  const result = await registerUser(input);

  res.status(HttpStatus.CREATED).json({
    success: true,
    data: result,
    message: 'User registered successfully',
  });
});

/**
 * Login existing user
 * POST /api/v1/auth/login
 */
export const login = asyncHandler(async (req: Request, res: Response) => {
  const input = req.body as z.infer<typeof loginSchema>;

  const result = await loginUser(input);

  res.status(HttpStatus.OK).json({
    success: true,
    data: result,
    message: 'Login successful',
  });
});

/**
 * Refresh access token
 * POST /api/v1/auth/refresh
 */
export const refresh = asyncHandler(async (req: Request, res: Response) => {
  const { refreshToken } = req.body as z.infer<typeof refreshTokenSchema>;

  const result = await refreshAccessToken(refreshToken);

  res.status(HttpStatus.OK).json({
    success: true,
    data: result,
    message: 'Token refreshed successfully',
  });
});

/**
 * Logout user
 * POST /api/v1/auth/logout
 * Requires authentication
 */
export const logout = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new Error('User not authenticated');
  }

  await logoutUser(req.user.id);

  res.status(HttpStatus.OK).json({
    success: true,
    message: 'Logout successful',
  });
});

/**
 * Get current user profile
 * GET /api/v1/auth/me
 * Requires authentication
 */
export const getProfile = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new Error('User not authenticated');
  }

  res.status(HttpStatus.OK).json({
    success: true,
    data: {
      user: req.user,
    },
  });
});
