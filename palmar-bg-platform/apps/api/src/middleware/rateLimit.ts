/**
 * Rate Limiting Middleware
 * Protects API from abuse using Redis-backed rate limiting
 * Production-grade with per-user and global limits
 */

import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import redisClient from '../config/redis';
import env from '../config/env';
import { AppError, HttpStatus } from './errorHandler';

/**
 * Global rate limiter
 * Applies to all requests
 * 1000 requests per 15 minutes (default)
 */
export const globalRateLimiter = rateLimit({
  windowMs: env.RATE_LIMIT_WINDOW_MS, // 15 minutes default
  max: env.RATE_LIMIT_MAX_REQUESTS, // 1000 requests default
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false, // Disable X-RateLimit-* headers
  store: new RedisStore({
    // @ts-expect-error - RedisStore expects ioredis client
    sendCommand: (...args: string[]) => redisClient.call(...args),
    prefix: 'rl:global:',
  }),
  handler: (_req, _res) => {
    throw new AppError(
      'Too many requests. Please try again later.',
      HttpStatus.TOO_MANY_REQUESTS
    );
  },
  skip: (_req) => {
    // Skip rate limiting in test environment
    return env.NODE_ENV === 'test';
  },
});

/**
 * Auth endpoints rate limiter
 * More strict to prevent brute force attacks
 * 10 requests per 15 minutes
 */
export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // 10 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    // @ts-expect-error - RedisStore expects ioredis client
    sendCommand: (...args: string[]) => redisClient.call(...args),
    prefix: 'rl:auth:',
  }),
  handler: (_req, _res) => {
    throw new AppError(
      'Too many authentication attempts. Please try again in 15 minutes.',
      HttpStatus.TOO_MANY_REQUESTS
    );
  },
  skip: (_req) => env.NODE_ENV === 'test',
  keyGenerator: (req) => {
    // Rate limit by IP and email combination for auth endpoints
    const email = req.body.email || 'unknown';
    return `${req.ip ?? 'unknown'}-${email}`;
  },
});

/**
 * Upload endpoints rate limiter
 * Moderate limits to prevent spam
 * 50 uploads per hour
 */
export const uploadRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 50, // 50 uploads per hour
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    // @ts-expect-error - RedisStore expects ioredis client
    sendCommand: (...args: string[]) => redisClient.call(...args),
    prefix: 'rl:upload:',
  }),
  handler: (_req, _res) => {
    throw new AppError(
      'Upload limit reached. Please try again later.',
      HttpStatus.TOO_MANY_REQUESTS
    );
  },
  skip: (_req) => env.NODE_ENV === 'test',
  keyGenerator: (req) => {
    // Rate limit by user ID if authenticated, otherwise by IP
    return (req.user?.id ?? req.ip) as string;
  },
});

/**
 * Download endpoints rate limiter
 * Prevent excessive downloads
 * 200 downloads per hour
 */
export const downloadRateLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 200, // 200 downloads per hour
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    // @ts-expect-error - RedisStore expects ioredis client
    sendCommand: (...args: string[]) => redisClient.call(...args),
    prefix: 'rl:download:',
  }),
  handler: (_req, _res) => {
    throw new AppError(
      'Download limit reached. Please try again later.',
      HttpStatus.TOO_MANY_REQUESTS
    );
  },
  skip: (_req) => env.NODE_ENV === 'test',
  keyGenerator: (req) => {
    return (req.user?.id ?? req.ip) as string;
  },
});
