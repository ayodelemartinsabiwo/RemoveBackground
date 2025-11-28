/**
 * Job Queue Service (BullMQ)
 * Handles async image processing jobs
 * Production-grade with retry logic and error handling
 */

import { Queue, Worker, Job, QueueEvents } from 'bullmq';
import { BackgroundType, DownloadTier } from '@prisma/client';
import redisClient from '../config/redis';
import prisma from '../config/database';
import logger from '../utils/logger';
import env from '../config/env';

/**
 * Job data interface for image processing
 */
export interface ImageProcessingJobData {
  imageId: string;
  userId: string;
  s3Key: string;
  backgroundType: BackgroundType;
  backgroundConfig?: {
    color?: string;
    angle?: number;
    textureType?: string;
    customImageKey?: string;
  };
  downloadTier: DownloadTier;
}

/**
 * Job result interface
 */
export interface ImageProcessingJobResult {
  imageId: string;
  processedS3Keys: {
    small: string;
    hd?: string;
    ultraHd?: string;
  };
  processingTimeMs: number;
}

/**
 * Create BullMQ connection from existing Redis client
 */
const connection = {
  host: redisClient.options.host,
  port: redisClient.options.port,
  password: redisClient.options.password,
  db: redisClient.options.db,
};

/**
 * Image Processing Queue
 */
export const imageProcessingQueue = new Queue<ImageProcessingJobData>(
  env.QUEUE_NAME,
  {
    connection,
    defaultJobOptions: {
      attempts: 3, // Retry up to 3 times
      backoff: {
        type: 'exponential',
        delay: 2000, // Start with 2 second delay
      },
      removeOnComplete: {
        age: 24 * 60 * 60, // Keep completed jobs for 24 hours
        count: 1000, // Keep last 1000 completed jobs
      },
      removeOnFail: {
        age: 7 * 24 * 60 * 60, // Keep failed jobs for 7 days
      },
    },
  }
);

/**
 * Queue Events for monitoring
 */
export const queueEvents = new QueueEvents(env.QUEUE_NAME, { connection });

/**
 * Add image processing job to queue
 * @param data - Job data
 * @returns Job ID
 */
export async function addImageProcessingJob(
  data: ImageProcessingJobData
): Promise<string> {
  const job = await imageProcessingQueue.add('process-image', data, {
    jobId: data.imageId, // Use image ID as job ID for idempotency
  });

  logger.info('Image processing job added to queue', {
    jobId: job.id,
    imageId: data.imageId,
    userId: data.userId,
  });

  return job.id ?? data.imageId;
}

/**
 * Get job status
 * @param jobId - Job ID
 * @returns Job status and progress
 */
export async function getJobStatus(jobId: string) {
  const job = await imageProcessingQueue.getJob(jobId);

  if (!job) {
    return null;
  }

  const state = await job.getState();
  const progress = job.progress;

  return {
    id: job.id,
    state,
    progress,
    attemptsMade: job.attemptsMade,
    data: job.data,
    returnvalue: job.returnvalue,
    failedReason: job.failedReason,
  };
}

/**
 * Cancel a job
 * @param jobId - Job ID
 */
export async function cancelJob(jobId: string): Promise<void> {
  const job = await imageProcessingQueue.getJob(jobId);

  if (job) {
    await job.remove();
    logger.info('Job cancelled', { jobId });
  }
}

/**
 * Get queue statistics
 */
export async function getQueueStats() {
  const [waiting, active, completed, failed, delayed] = await Promise.all([
    imageProcessingQueue.getWaitingCount(),
    imageProcessingQueue.getActiveCount(),
    imageProcessingQueue.getCompletedCount(),
    imageProcessingQueue.getFailedCount(),
    imageProcessingQueue.getDelayedCount(),
  ]);

  return {
    waiting,
    active,
    completed,
    failed,
    delayed,
    total: waiting + active + completed + failed + delayed,
  };
}

/**
 * Queue event handlers for logging
 */
queueEvents.on('waiting', ({ jobId }) => {
  logger.info('Job waiting', { jobId });
});

queueEvents.on('active', ({ jobId }) => {
  logger.info('Job active', { jobId });
});

queueEvents.on('completed', ({ jobId, returnvalue }) => {
  logger.info('Job completed', { jobId, result: returnvalue });
});

queueEvents.on('failed', ({ jobId, failedReason }) => {
  logger.error('Job failed', { jobId, reason: failedReason });
});

queueEvents.on('progress', ({ jobId, data }) => {
  logger.info('Job progress', { jobId, progress: data });
});

/**
 * Worker process (will be run in separate process/container)
 * This is a placeholder - actual worker will call Python FastAPI
 */
export function createWorker() {
  const worker = new Worker<ImageProcessingJobData, ImageProcessingJobResult>(
    env.QUEUE_NAME,
    async (job: Job<ImageProcessingJobData>) => {
      const startTime = Date.now();

      logger.info('Processing image job', {
        jobId: job.id,
        imageId: job.data.imageId,
      });

      try {
        // Update database status to PROCESSING
        await prisma.image.update({
          where: { id: job.data.imageId },
          data: { processingStatus: 'PROCESSING' },
        });

        // Report progress
        await job.updateProgress(10);

        // TODO: Call Python FastAPI worker to process image
        // For now, this is a placeholder
        // In production, this will make HTTP request to worker service

        const result: ImageProcessingJobResult = {
          imageId: job.data.imageId,
          processedS3Keys: {
            small: `processed/${job.data.userId}/${job.data.imageId}/small.png`,
            hd: `processed/${job.data.userId}/${job.data.imageId}/hd.png`,
            ultraHd: `processed/${job.data.userId}/${job.data.imageId}/ultra_hd.png`,
          },
          processingTimeMs: Date.now() - startTime,
        };

        // Update database status to COMPLETED
        await prisma.image.update({
          where: { id: job.data.imageId },
          data: {
            processingStatus: 'COMPLETED',
            processedSmallUrl: result.processedS3Keys.small,
            processedHdUrl: result.processedS3Keys.hd,
            processedUltraHdUrl: result.processedS3Keys.ultraHd,
            processingTimeMs: result.processingTimeMs,
          },
        });

        await job.updateProgress(100);

        return result;
      } catch (error) {
        logger.error('Image processing failed', {
          jobId: job.id,
          imageId: job.data.imageId,
          error,
        });

        // Update database status to FAILED
        await prisma.image.update({
          where: { id: job.data.imageId },
          data: {
            processingStatus: 'FAILED',
            errorMessage: error instanceof Error ? error.message : 'Unknown error',
          },
        });

        throw error;
      }
    },
    {
      connection,
      concurrency: env.QUEUE_CONCURRENCY,
    }
  );

  worker.on('completed', (job) => {
    logger.info('Worker completed job', { jobId: job.id });
  });

  worker.on('failed', (job, err) => {
    logger.error('Worker job failed', {
      jobId: job?.id,
      error: err.message,
    });
  });

  return worker;
}

/**
 * Graceful shutdown
 */
export async function shutdownQueue(): Promise<void> {
  await imageProcessingQueue.close();
  await queueEvents.close();
  logger.info('Queue shutdown complete');
}
