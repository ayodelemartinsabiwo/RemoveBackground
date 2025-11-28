/**
 * S3 Storage Service
 * Handles file uploads, downloads, and deletion
 * Supports presigned URLs for secure client-side uploads
 */

import {
  PutObjectCommand,
  GetObjectCommand,
  DeleteObjectCommand,
  HeadObjectCommand,
} from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { s3Client, S3_BUCKET } from '../config/s3';
import logger from '../utils/logger';
import { Readable } from 'stream';

/**
 * File upload options
 */
export interface UploadOptions {
  buffer: Buffer;
  key: string;
  contentType: string;
  metadata?: Record<string, string>;
}

/**
 * Upload file to S3
 * @param options - Upload configuration
 * @returns Promise<string> - S3 object key
 */
export async function uploadFile(options: UploadOptions): Promise<string> {
  const { buffer, key, contentType, metadata = {} } = options;

  try {
    const command = new PutObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
      Body: buffer,
      ContentType: contentType,
      Metadata: metadata,
    });

    await s3Client.send(command);

    logger.info('File uploaded to S3', { key, size: buffer.length });

    return key;
  } catch (error) {
    logger.error('S3 upload failed', { key, error });
    throw new Error('Failed to upload file to storage');
  }
}

/**
 * Generate presigned upload URL
 * Allows client to upload directly to S3
 * @param key - S3 object key
 * @param contentType - File MIME type
 * @param expiresIn - URL expiration in seconds (default: 5 minutes)
 * @returns Promise<string> - Presigned URL
 */
export async function generatePresignedUploadUrl(
  key: string,
  contentType: string,
  expiresIn: number = 300
): Promise<string> {
  try {
    const command = new PutObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
      ContentType: contentType,
    });

    const url = await getSignedUrl(s3Client, command, { expiresIn });

    logger.info('Presigned upload URL generated', { key, expiresIn });

    return url;
  } catch (error) {
    logger.error('Failed to generate presigned upload URL', { key, error });
    throw new Error('Failed to generate upload URL');
  }
}

/**
 * Generate presigned download URL
 * Allows client to download directly from S3
 * @param key - S3 object key
 * @param expiresIn - URL expiration in seconds (default: 1 hour)
 * @returns Promise<string> - Presigned URL
 */
export async function generatePresignedDownloadUrl(
  key: string,
  expiresIn: number = 3600
): Promise<string> {
  try {
    const command = new GetObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
    });

    const url = await getSignedUrl(s3Client, command, { expiresIn });

    logger.info('Presigned download URL generated', { key, expiresIn });

    return url;
  } catch (error) {
    logger.error('Failed to generate presigned download URL', { key, error });
    throw new Error('Failed to generate download URL');
  }
}

/**
 * Download file from S3
 * @param key - S3 object key
 * @returns Promise<Buffer> - File buffer
 */
export async function downloadFile(key: string): Promise<Buffer> {
  try {
    const command = new GetObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
    });

    const response = await s3Client.send(command);

    if (!response.Body) {
      throw new Error('Empty response body');
    }

    // Convert stream to buffer
    const stream = response.Body as Readable;
    const chunks: Buffer[] = [];

    for await (const chunk of stream) {
      chunks.push(chunk);
    }

    const buffer = Buffer.concat(chunks);

    logger.info('File downloaded from S3', { key, size: buffer.length });

    return buffer;
  } catch (error) {
    logger.error('S3 download failed', { key, error });
    throw new Error('Failed to download file from storage');
  }
}

/**
 * Delete file from S3
 * @param key - S3 object key
 */
export async function deleteFile(key: string): Promise<void> {
  try {
    const command = new DeleteObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
    });

    await s3Client.send(command);

    logger.info('File deleted from S3', { key });
  } catch (error) {
    logger.error('S3 deletion failed', { key, error });
    throw new Error('Failed to delete file from storage');
  }
}

/**
 * Check if file exists in S3
 * @param key - S3 object key
 * @returns Promise<boolean> - True if file exists
 */
export async function fileExists(key: string): Promise<boolean> {
  try {
    const command = new HeadObjectCommand({
      Bucket: S3_BUCKET,
      Key: key,
    });

    await s3Client.send(command);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Generate S3 key for image uploads
 * Format: images/{userId}/{timestamp}_{originalName}
 */
export function generateImageKey(
  userId: string,
  originalName: string
): string {
  const timestamp = Date.now();
  const sanitizedName = originalName.replace(/[^a-zA-Z0-9.-]/g, '_');
  return `images/${userId}/${timestamp}_${sanitizedName}`;
}

/**
 * Generate S3 key for processed images
 * Format: processed/{userId}/{imageId}/{tier}_{timestamp}.png
 */
export function generateProcessedImageKey(
  userId: string,
  imageId: string,
  tier: string
): string {
  const timestamp = Date.now();
  return `processed/${userId}/${imageId}/${tier}_${timestamp}.png`;
}
