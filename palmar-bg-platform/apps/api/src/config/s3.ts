/**
 * AWS S3 / MinIO Client Configuration
 * Supports both AWS S3 and MinIO for local development
 * Production-grade with proper error handling
 */

import { S3Client, S3ClientConfig } from '@aws-sdk/client-s3';
import env from './env';
import logger from '../utils/logger';

/**
 * S3 Client Configuration
 * Supports both AWS S3 (production) and MinIO (development)
 */
const s3Config: S3ClientConfig = {
  region: env.AWS_REGION,
  credentials: {
    accessKeyId: env.AWS_ACCESS_KEY_ID,
    secretAccessKey: env.AWS_SECRET_ACCESS_KEY,
  },
  ...(env.S3_ENDPOINT && {
    endpoint: env.S3_ENDPOINT,
    forcePathStyle: env.S3_FORCE_PATH_STYLE, // Required for MinIO
  }),
};

/**
 * S3 Client Instance
 */
export const s3Client = new S3Client(s3Config);

/**
 * S3 Bucket Name
 */
export const S3_BUCKET = env.S3_BUCKET_NAME;

/**
 * S3 Health Check
 * Verifies bucket accessibility
 */
export async function isS3Healthy(): Promise<boolean> {
  try {
    const { HeadBucketCommand } = await import('@aws-sdk/client-s3');
    const command = new HeadBucketCommand({ Bucket: S3_BUCKET });
    await s3Client.send(command);
    return true;
  } catch (error) {
    logger.error('S3 health check failed:', error);
    return false;
  }
}

logger.info(`S3 client configured for bucket: ${S3_BUCKET}`);

export default s3Client;
