/**
 * Prisma Database Client Configuration
 * Singleton pattern to prevent multiple instances
 * Production-grade connection pooling
 */

import { PrismaClient } from '@prisma/client';
import env from './env';

// Prevent multiple instances in development (hot reload)
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

/**
 * Prisma Client with logging configuration
 */
export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log:
      env.NODE_ENV === 'development'
        ? ['query', 'error', 'warn']
        : ['error'],
    errorFormat: 'pretty',
  });

if (env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

/**
 * Graceful shutdown handler
 * Ensures all database connections are closed properly
 */
export async function disconnectDatabase(): Promise<void> {
  await prisma.$disconnect();
}

/**
 * Database health check
 * Returns true if database is accessible
 */
export async function isDatabaseHealthy(): Promise<boolean> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    return true;
  } catch (error) {
    console.error('Database health check failed:', error);
    return false;
  }
}

export default prisma;
