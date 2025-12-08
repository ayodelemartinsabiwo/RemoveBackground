/**
 * Environment Configuration with Zod Validation
 * Ensures all required environment variables are present and valid
 * Zero tolerance for configuration errors
 */

import { config } from 'dotenv';
import { z } from 'zod';

// Load environment variables from .env file
config();

const envSchema = z.object({
  // Server
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).pipe(z.number().min(1).max(65535)).default('3000'),
  API_VERSION: z.string().default('v1'),

  // Database
  DATABASE_URL: z.string().url().min(1),

  // Redis
  REDIS_HOST: z.string().min(1),
  REDIS_PORT: z.string().transform(Number).pipe(z.number().min(1).max(65535)),
  REDIS_PASSWORD: z.string().optional().default(''),
  REDIS_DB: z.string().transform(Number).pipe(z.number().min(0).max(15)).default('0'),

  // JWT
  JWT_SECRET: z.string().min(32, 'JWT secret must be at least 32 characters'),
  JWT_EXPIRES_IN: z.string().default('15m'),
  REFRESH_TOKEN_SECRET: z.string().min(32, 'Refresh token secret must be at least 32 characters'),
  REFRESH_TOKEN_EXPIRES_IN: z.string().default('7d'),

  // Bcrypt
  BCRYPT_ROUNDS: z.string().transform(Number).pipe(z.number().min(10).max(15)).default('12'),

  // AWS S3
  AWS_ACCESS_KEY_ID: z.string().min(1),
  AWS_SECRET_ACCESS_KEY: z.string().min(1),
  AWS_REGION: z.string().default('us-east-1'),
  S3_BUCKET_NAME: z.string().min(1),
  S3_ENDPOINT: z.string().url().optional(),
  S3_FORCE_PATH_STYLE: z.string().transform((val) => val === 'true').default('false'),

  // CORS
  CORS_ORIGIN: z.string().transform((val) => val.split(',')),
  CORS_CREDENTIALS: z.string().transform((val) => val === 'true').default('true'),

  // Rate Limiting
  RATE_LIMIT_WINDOW_MS: z.string().transform(Number).pipe(z.number().positive()).default('900000'),
  RATE_LIMIT_MAX_REQUESTS: z.string().transform(Number).pipe(z.number().positive()).default('1000'),

  // File Upload
  MAX_FILE_SIZE: z.string().transform(Number).pipe(z.number().positive()).default('26214400'),
  ALLOWED_FILE_TYPES: z.string().transform((val) => val.split(',')),

  // Logging
  LOG_LEVEL: z.enum(['error', 'warn', 'info', 'http', 'verbose', 'debug']).default('info'),
  LOG_DIR: z.string().default('logs'),

  // Queue
  QUEUE_NAME: z.string().default('image-processing'),
  QUEUE_CONCURRENCY: z.string().transform(Number).pipe(z.number().positive()).default('10'),

  // Feature Flags
  ENABLE_EMAIL_VERIFICATION: z.string().transform((val) => val === 'true').default('false'),
  ENABLE_RATE_LIMITING: z.string().transform((val) => val === 'true').default('true'),

  // SendGrid (Optional)
  SENDGRID_API_KEY: z.string().optional(),
  SENDGRID_FROM_EMAIL: z.string().email().optional(),
  SENDGRID_FROM_NAME: z.string().optional(),
});

export type Env = z.infer<typeof envSchema>;

/**
 * Validate and parse environment variables
 * Throws error if validation fails
 */
function validateEnv(): Env {
  const parsed = envSchema.safeParse(process.env);

  if (!parsed.success) {
    console.error('❌ Invalid environment variables:', parsed.error.format());
    throw new Error('Environment validation failed. Check your .env file.');
  }

  return parsed.data;
}

// Export validated environment
export const env = validateEnv();

// Type-safe environment access
export default env;
