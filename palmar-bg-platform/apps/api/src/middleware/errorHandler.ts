/**
 * Global Error Handling Middleware
 * Catches all errors and returns proper HTTP responses
 * Production-grade with structured logging
 */

import { Request, Response, NextFunction } from 'express';
import { Prisma } from '@prisma/client';
import { ZodError } from 'zod';
import logger from '../utils/logger';
import env from '../config/env';

/**
 * Custom Application Error
 */
export class AppError extends Error {
  public statusCode: number;
  public isOperational: boolean;

  constructor(message: string, statusCode: number = 500) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

/**
 * HTTP Status Codes
 */
export const HttpStatus = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const;

/**
 * Error response structure
 */
interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    details?: unknown;
    stack?: string;
  };
}

/**
 * Handle Prisma errors
 */
function handlePrismaError(error: Prisma.PrismaClientKnownRequestError): {
  statusCode: number;
  message: string;
} {
  switch (error.code) {
    case 'P2002':
      // Unique constraint violation
      const field = (error.meta?.target as string[])?.join(', ') ?? 'field';
      return {
        statusCode: HttpStatus.CONFLICT,
        message: `${field} already exists`,
      };

    case 'P2025':
      // Record not found
      return {
        statusCode: HttpStatus.NOT_FOUND,
        message: 'Record not found',
      };

    case 'P2003':
      // Foreign key constraint violation
      return {
        statusCode: HttpStatus.BAD_REQUEST,
        message: 'Referenced record does not exist',
      };

    case 'P2014':
      // Invalid relation
      return {
        statusCode: HttpStatus.BAD_REQUEST,
        message: 'Invalid relation in query',
      };

    default:
      return {
        statusCode: HttpStatus.INTERNAL_SERVER_ERROR,
        message: 'Database error occurred',
      };
  }
}

/**
 * Handle Zod validation errors
 */
function handleZodError(error: ZodError): {
  statusCode: number;
  message: string;
  details: unknown;
} {
  const errors = error.errors.map((err) => ({
    field: err.path.join('.'),
    message: err.message,
  }));

  return {
    statusCode: HttpStatus.UNPROCESSABLE_ENTITY,
    message: 'Validation failed',
    details: errors,
  };
}

/**
 * Global error handler middleware
 * Must be registered AFTER all routes
 */
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  let statusCode = HttpStatus.INTERNAL_SERVER_ERROR;
  let message = 'Internal server error';
  let details: unknown = undefined;

  // Log error
  logger.error('Error occurred', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    ip: req.ip,
  });

  // Handle known error types
  if (error instanceof AppError) {
    statusCode = error.statusCode;
    message = error.message;
  } else if (error instanceof Prisma.PrismaClientKnownRequestError) {
    const prismaError = handlePrismaError(error);
    statusCode = prismaError.statusCode;
    message = prismaError.message;
  } else if (error instanceof ZodError) {
    const zodError = handleZodError(error);
    statusCode = zodError.statusCode;
    message = zodError.message;
    details = zodError.details;
  } else if (error.name === 'JsonWebTokenError') {
    statusCode = HttpStatus.UNAUTHORIZED;
    message = 'Invalid token';
  } else if (error.name === 'TokenExpiredError') {
    statusCode = HttpStatus.UNAUTHORIZED;
    message = 'Token expired';
  } else if (error.name === 'MulterError') {
    statusCode = HttpStatus.BAD_REQUEST;
    message = error.message;
  }

  // Build error response
  const errorResponse: ErrorResponse = {
    success: false,
    error: {
      message,
      ...(details && { details }),
      // Only include stack trace in development
      ...(env.NODE_ENV === 'development' && { stack: error.stack }),
    },
  };

  res.status(statusCode).json(errorResponse);
}

/**
 * Handle 404 Not Found errors
 * Must be registered BEFORE error handler middleware
 */
export function notFoundHandler(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const error = new AppError(
    `Route ${req.method} ${req.url} not found`,
    HttpStatus.NOT_FOUND
  );
  next(error);
}

/**
 * Async handler wrapper
 * Catches errors from async route handlers
 */
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
) {
  return (req: Request, res: Response, next: NextFunction): void => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}
