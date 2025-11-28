/**
 * Redis Client Configuration
 * Production-grade with reconnection logic and error handling
 */

import Redis, { RedisOptions } from 'ioredis';
import env from './env';
import logger from '../utils/logger';

/**
 * Redis connection options
 */
const redisOptions: RedisOptions = {
  host: env.REDIS_HOST,
  port: env.REDIS_PORT,
  password: env.REDIS_PASSWORD,
  db: env.REDIS_DB,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  enableOfflineQueue: true,
  retryStrategy: (times: number): number | null => {
    const delay = Math.min(times * 50, 2000);
    if (times > 10) {
      logger.error('Redis connection failed after 10 retries');
      return null; // Stop retrying
    }
    return delay;
  },
  reconnectOnError: (err: Error): boolean => {
    const targetError = 'READONLY';
    if (err.message.includes(targetError)) {
      // Only reconnect when the error contains "READONLY"
      return true;
    }
    return false;
  },
};

/**
 * Create Redis client instance
 */
export const redisClient = new Redis(redisOptions);

/**
 * Redis event handlers
 */
redisClient.on('connect', () => {
  logger.info('Redis client connecting...');
});

redisClient.on('ready', () => {
  logger.info('✅ Redis client ready');
});

redisClient.on('error', (err: Error) => {
  logger.error('❌ Redis client error:', err);
});

redisClient.on('close', () => {
  logger.warn('Redis client connection closed');
});

redisClient.on('reconnecting', () => {
  logger.info('Redis client reconnecting...');
});

/**
 * Redis health check
 */
export async function isRedisHealthy(): Promise<boolean> {
  try {
    const response = await redisClient.ping();
    return response === 'PONG';
  } catch (error) {
    logger.error('Redis health check failed:', error);
    return false;
  }
}

/**
 * Graceful shutdown
 */
export async function disconnectRedis(): Promise<void> {
  await redisClient.quit();
  logger.info('Redis client disconnected');
}

export default redisClient;
