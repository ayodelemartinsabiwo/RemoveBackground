/**
 * Winston Logger Configuration
 * Production-grade structured logging with daily rotation
 * JSON format for easy parsing in production
 */

import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';
import path from 'path';
import env from '../config/env';

/**
 * Custom log format for development (readable)
 */
const devFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const metaStr = Object.keys(meta).length ? JSON.stringify(meta, null, 2) : '';
    return `${timestamp} [${level}]: ${message} ${metaStr}`;
  })
);

/**
 * Custom log format for production (JSON)
 */
const prodFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

/**
 * Daily rotate file transport for error logs
 */
const errorFileTransport = new DailyRotateFile({
  filename: path.join(env.LOG_DIR, 'error-%DATE%.log'),
  datePattern: 'YYYY-MM-DD',
  level: 'error',
  maxSize: '20m',
  maxFiles: '14d',
  zippedArchive: true,
});

/**
 * Daily rotate file transport for combined logs
 */
const combinedFileTransport = new DailyRotateFile({
  filename: path.join(env.LOG_DIR, 'combined-%DATE%.log'),
  datePattern: 'YYYY-MM-DD',
  maxSize: '20m',
  maxFiles: '14d',
  zippedArchive: true,
});

/**
 * Winston Logger Instance
 */
const logger = winston.createLogger({
  level: env.LOG_LEVEL,
  format: env.NODE_ENV === 'production' ? prodFormat : devFormat,
  transports: [
    // Console transport
    new winston.transports.Console({
      format: env.NODE_ENV === 'production' ? prodFormat : devFormat,
    }),
    // File transports (production only)
    ...(env.NODE_ENV === 'production'
      ? [errorFileTransport, combinedFileTransport]
      : []),
  ],
  // Don't exit on error
  exitOnError: false,
});

/**
 * Create child logger with additional context
 * @param context - Additional context to add to all log messages
 */
export function createChildLogger(context: Record<string, unknown>): winston.Logger {
  return logger.child(context);
}

/**
 * Log HTTP requests (for middleware)
 */
export function logHttpRequest(req: {
  method: string;
  url: string;
  ip?: string;
  headers: Record<string, unknown>;
}): void {
  logger.http('HTTP Request', {
    method: req.method,
    url: req.url,
    ip: req.ip,
    userAgent: req.headers['user-agent'],
  });
}

/**
 * Log errors with stack trace
 */
export function logError(error: Error, context?: Record<string, unknown>): void {
  logger.error({
    message: error.message,
    stack: error.stack,
    ...context,
  });
}

export default logger;
