/**
 * BullMQ Worker Process
 * Consumes jobs from BullMQ and delegates to Python worker
 */

import axios from 'axios';
import { createWorker } from './services/queue.service';
import { Worker, Job } from 'bullmq';
import prisma from './config/database';
import logger from './utils/logger';
import env from './config/env';
import redisClient from './config/redis';
import { ImageProcessingJobData, ImageProcessingJobResult } from './services/queue.service';

// Python worker URL
const PYTHON_WORKER_URL = process.env.PYTHON_WORKER_URL || 'http://worker:8000';

/**
 * Call Python FastAPI worker to process image
 */
async function callPythonWorker(jobData: ImageProcessingJobData): Promise<any> {
  try {
    const response = await axios.post(
      `${PYTHON_WORKER_URL}/api/process`,
      {
        image_id: jobData.imageId,
        user_id: jobData.userId,
        s3_key: jobData.s3Key,
        background_type: jobData.backgroundType,
        background_config: jobData.backgroundConfig,
        download_tier: jobData.downloadTier,
      },
      {
        timeout: 900000, // 15 minutes timeout (for initial model download)
      }
    );

    return response.data;
  } catch (error) {
    logger.error('Python worker call failed', {
      error: error instanceof Error ? error.message : 'Unknown error',
      jobData,
    });
    throw error;
  }
}

/**
 * Create and start worker
 */
async function startWorker() {
  logger.info('Starting BullMQ worker...');

  const connection = {
    host: redisClient.options.host,
    port: redisClient.options.port,
    password: redisClient.options.password,
    db: redisClient.options.db,
  };

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

        await job.updateProgress(10);

        // Call Python worker
        logger.info('Calling Python worker', {
          imageId: job.data.imageId,
          workerUrl: PYTHON_WORKER_URL,
        });

        const result = await callPythonWorker(job.data);

        await job.updateProgress(90);

        // Update database with results
        await prisma.image.update({
          where: { id: job.data.imageId },
          data: {
            processingStatus: 'COMPLETED',
            processedSmallUrl: result.processed_small_url,
            processedHdUrl: result.processed_hd_url,
            processedUltraHdUrl: result.processed_ultra_hd_url,
            processedS3Key: result.processed_s3_key,
            processingTimeMs: Date.now() - startTime,
            processedAt: new Date(),
          },
        });

        await job.updateProgress(100);

        logger.info('Job completed successfully', {
          jobId: job.id,
          imageId: job.data.imageId,
          processingTime: Date.now() - startTime,
        });

        return {
          imageId: job.data.imageId,
          processedS3Keys: {
            small: result.processed_small_url,
            hd: result.processed_hd_url,
            ultraHd: result.processed_ultra_hd_url,
          },
          processingTimeMs: Date.now() - startTime,
        };
      } catch (error) {
        logger.error('Image processing failed', {
          jobId: job.id,
          imageId: job.data.imageId,
          error: error instanceof Error ? error.message : 'Unknown error',
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
      concurrency: env.QUEUE_CONCURRENCY || 1,
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

  worker.on('error', (err) => {
    logger.error('Worker error', { error: err.message });
  });

  logger.info('✅ BullMQ worker started and listening for jobs');

  // Graceful shutdown
  process.on('SIGTERM', async () => {
    logger.info('SIGTERM received, closing worker...');
    await worker.close();
    await prisma.$disconnect();
    process.exit(0);
  });

  process.on('SIGINT', async () => {
    logger.info('SIGINT received, closing worker...');
    await worker.close();
    await prisma.$disconnect();
    process.exit(0);
  });

  return worker;
}

// Start worker
startWorker().catch((error) => {
  logger.error('Failed to start worker', { error });
  process.exit(1);
});
