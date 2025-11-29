/**
 * Request Validation Middleware
 * Validates request body, query, and params using Zod schemas
 * Production-grade with detailed error messages
 */

import { Request, Response, NextFunction } from 'express';
import { ZodSchema, ZodError } from 'zod';
import { AppError, HttpStatus } from './errorHandler';

/**
 * Validate request body
 * Usage: app.post('/route', validateBody(schema), controller)
 */
export function validateBody(schema: ZodSchema) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        next(error);
      } else {
        next(new AppError('Validation failed', HttpStatus.BAD_REQUEST));
      }
    }
  };
}

/**
 * Validate request query parameters
 * Usage: app.get('/route', validateQuery(schema), controller)
 */
export function validateQuery(schema: ZodSchema) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    try {
      req.query = schema.parse(req.query);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        next(error);
      } else {
        next(new AppError('Query validation failed', HttpStatus.BAD_REQUEST));
      }
    }
  };
}

/**
 * Validate request params
 * Usage: app.get('/route/:id', validateParams(schema), controller)
 */
export function validateParams(schema: ZodSchema) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    try {
      req.params = schema.parse(req.params);
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        next(error);
      } else {
        next(new AppError('Params validation failed', HttpStatus.BAD_REQUEST));
      }
    }
  };
}
