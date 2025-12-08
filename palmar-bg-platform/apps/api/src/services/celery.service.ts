/**
 * Celery Service
 * Handles triggering Celery tasks in Python worker for image processing
 */

import axios from 'axios';
import logger from '../utils/logger';
import { AppError, HttpStatus } from '../middleware/errorHandler';

const PYTHON_WORKER_URL = process.env.PYTHON_WORKER_URL || 'http://localhost:8000';

/**
 * Trigger image processing task in Celery
 */
export async function triggerImageProcessing(data: {
  imageId: string;
  userId: string;
  s3Key: string;
  backgroundType?: string;
  backgroundConfig?: any;
}): Promise<{ taskId: string; imageId: string }> {
  try {
    logger.info('Triggering Celery image processing task', {
      imageId: data.imageId,
      userId: data.userId,
    });

    const response = await axios.post(
      `${PYTHON_WORKER_URL}/api/celery/trigger`,
      {
        image_id: data.imageId,
        user_id: data.userId,
        s3_key: data.s3Key,
        background_type: data.backgroundType || 'TRANSPARENT',
        background_config: data.backgroundConfig || null,
      },
      {
        timeout: 5000, // 5 second timeout for queuing
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.data.success) {
      throw new Error(response.data.message || 'Failed to queue task');
    }

    logger.info('Celery task queued successfully', {
      taskId: response.data.task_id,
      imageId: response.data.image_id,
    });

    return {
      taskId: response.data.task_id,
      imageId: response.data.image_id,
    };
  } catch (error) {
    logger.error('Failed to trigger Celery task', {
      imageId: data.imageId,
      error: error instanceof Error ? error.message : 'Unknown error',
    });

    // If worker is unavailable, throw service unavailable error
    if (axios.isAxiosError(error) && !error.response) {
      throw new AppError(
        'Image processing service is unavailable. Please try again later.',
        HttpStatus.SERVICE_UNAVAILABLE
      );
    }

    throw new AppError(
      'Failed to queue image processing task',
      HttpStatus.INTERNAL_SERVER_ERROR
    );
  }
}

/**
 * Get Celery task status
 */
export async function getTaskStatus(taskId: string): Promise<{
  taskId: string;
  status: string;
  result?: any;
  error?: string;
}> {
  try {
    const response = await axios.get(
      `${PYTHON_WORKER_URL}/api/celery/status/${taskId}`,
      { timeout: 3000 }
    );

    return {
      taskId: response.data.task_id,
      status: response.data.status,
      result: response.data.result,
      error: response.data.error,
    };
  } catch (error) {
    logger.error('Failed to get task status', {
      taskId,
      error: error instanceof Error ? error.message : 'Unknown error',
    });

    throw new AppError(
      'Failed to get task status',
      HttpStatus.INTERNAL_SERVER_ERROR
    );
  }
}

/**
 * Check Celery worker health
 */
export async function checkCeleryHealth(): Promise<{
  status: string;
  message?: string;
}> {
  try {
    const response = await axios.get(`${PYTHON_WORKER_URL}/api/celery/health`, {
      timeout: 5000,
    });

    return {
      status: response.data.status,
      message: response.data.message,
    };
  } catch (error) {
    logger.error('Celery health check failed', {
      error: error instanceof Error ? error.message : 'Unknown error',
    });

    return {
      status: 'unavailable',
      message: 'Worker is not responding',
    };
  }
}
