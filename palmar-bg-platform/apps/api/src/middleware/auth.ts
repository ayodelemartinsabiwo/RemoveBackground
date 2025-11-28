/**
 * Authentication Middleware
 * Protects routes by verifying JWT access tokens
 * Adds authenticated user to request object
 */

import { Request, Response, NextFunction } from 'express';
import { Role } from '@prisma/client';
import { verifyAccessToken, DecodedToken } from '../utils/jwt';
import { AppError, HttpStatus } from './errorHandler';
import { getUserById } from '../services/auth.service';

/**
 * Extend Express Request to include authenticated user
 */
declare global {
  namespace Express {
    interface Request {
      user?: {
        id: string;
        email: string;
        role: Role;
      };
    }
  }
}

/**
 * Authenticate JWT middleware
 * Verifies access token and attaches user to request
 * Usage: app.get('/protected', authenticate, controller)
 */
export async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    // Get token from Authorization header
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      throw new AppError('No authorization token provided', HttpStatus.UNAUTHORIZED);
    }

    // Extract token (format: "Bearer <token>")
    const parts = authHeader.split(' ');

    if (parts.length !== 2 || parts[0] !== 'Bearer') {
      throw new AppError('Invalid token format', HttpStatus.UNAUTHORIZED);
    }

    const token = parts[1];

    // Verify token
    const decoded = verifyAccessToken(token);

    if (!decoded) {
      throw new AppError('Invalid or expired token', HttpStatus.UNAUTHORIZED);
    }

    // Verify user still exists
    const user = await getUserById(decoded.userId);

    if (!user) {
      throw new AppError('User not found', HttpStatus.UNAUTHORIZED);
    }

    // Attach user to request
    req.user = {
      id: user.id,
      email: user.email,
      role: user.role,
    };

    next();
  } catch (error) {
    next(error);
  }
}

/**
 * Require specific role middleware
 * Must be used AFTER authenticate middleware
 * Usage: app.get('/admin', authenticate, requireRole('ADMIN'), controller)
 */
export function requireRole(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user) {
      throw new AppError('Authentication required', HttpStatus.UNAUTHORIZED);
    }

    if (!roles.includes(req.user.role)) {
      throw new AppError('Insufficient permissions', HttpStatus.FORBIDDEN);
    }

    next();
  };
}

/**
 * Optional authentication middleware
 * Attaches user if token is valid, but doesn't throw error if missing
 * Useful for routes that work differently for authenticated users
 * Usage: app.get('/public', optionalAuth, controller)
 */
export async function optionalAuth(
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
      return next();
    }

    const parts = authHeader.split(' ');

    if (parts.length !== 2 || parts[0] !== 'Bearer') {
      return next();
    }

    const token = parts[1];
    const decoded = verifyAccessToken(token);

    if (!decoded) {
      return next();
    }

    const user = await getUserById(decoded.userId);

    if (user) {
      req.user = {
        id: user.id,
        email: user.email,
        role: user.role,
      };
    }

    next();
  } catch (error) {
    // Ignore errors for optional auth
    next();
  }
}
