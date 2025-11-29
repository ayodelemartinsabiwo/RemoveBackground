/**
 * Image Service
 * Handles image upload, processing, and download logic
 * Production-grade with proper validation and error handling
 */

import { BackgroundType, DownloadTier, ProcessingStatus } from '@prisma/client';
import prisma from '../config/database';
import logger from '../utils/logger';
import { uploadFile, generateImageKey, generatePresignedDownloadUrl } from './s3.service';
import { addImageProcessingJob } from './queue.service';
import { deductCredits, getCreditCost, refundCredits } from './credit.service';
import { AppError, HttpStatus } from '../middleware/errorHandler';

/**
 * Image upload input
 */
export interface UploadImageInput {
  userId: string;
  file: Express.Multer.File;
  backgroundType?: BackgroundType;
  backgroundConfig?: {
    color?: string;
    angle?: number;
    textureType?: string;
    customImageKey?: string;
  };
}

/**
 * Upload and process image
 * @param input - Upload configuration
 * @returns Image record
 */
export async function uploadAndProcessImage(input: UploadImageInput) {
  const { userId, file, backgroundType = 'TRANSPARENT', backgroundConfig } = input;

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(file.mimetype)) {
    throw new AppError(
      'Invalid file type. Supported: JPEG, PNG, WebP',
      HttpStatus.BAD_REQUEST
    );
  }

  // Validate file size (25MB max)
  const maxSize = 25 * 1024 * 1024; // 25MB
  if (file.size > maxSize) {
    throw new AppError('File too large. Maximum size: 25MB', HttpStatus.BAD_REQUEST);
  }

  // Generate S3 key
  const s3Key = generateImageKey(userId, file.originalname);

  // Upload to S3
  await uploadFile({
    buffer: file.buffer,
    key: s3Key,
    contentType: file.mimetype,
    metadata: {
      userId,
      originalName: file.originalname,
    },
  });

  logger.info('Original image uploaded to S3', {
    userId,
    s3Key,
    size: file.size,
  });

  // Create image record in database
  const image = await prisma.image.create({
    data: {
      userId,
      originalFilename: file.originalname,
      originalS3Key: s3Key,
      fileSize: file.size,
      mimeType: file.mimetype,
      backgroundType,
      backgroundConfig: backgroundConfig ?? {},
      processingStatus: ProcessingStatus.PENDING,
    },
  });

  // Add processing job to queue
  await addImageProcessingJob({
    imageId: image.id,
    userId,
    s3Key,
    backgroundType,
    backgroundConfig,
    downloadTier: DownloadTier.SMALL, // Default processing
  });

  logger.info('Image processing job queued', {
    imageId: image.id,
    userId,
  });

  return image;
}

/**
 * Download processed image
 * Deducts credits based on download tier
 * @param imageId - Image ID
 * @param userId - User ID
 * @param tier - Download tier
 * @returns Presigned download URL
 */
export async function downloadProcessedImage(
  imageId: string,
  userId: string,
  tier: DownloadTier
): Promise<string> {
  // Get image record
  const image = await prisma.image.findUnique({
    where: { id: imageId },
  });

  if (!image) {
    throw new AppError('Image not found', HttpStatus.NOT_FOUND);
  }

  // Verify ownership
  if (image.userId !== userId) {
    throw new AppError('Unauthorized access', HttpStatus.FORBIDDEN);
  }

  // Check if processing is complete
  if (image.processingStatus !== ProcessingStatus.COMPLETED) {
    throw new AppError(
      `Image is ${image.processingStatus.toLowerCase()}`,
      HttpStatus.BAD_REQUEST
    );
  }

  // Get credit cost
  const creditCost = getCreditCost(tier);

  // Deduct credits if not free tier
  let transactionId: string | undefined;
  if (creditCost > 0) {
    transactionId = await deductCredits(
      userId,
      creditCost,
      `Download ${tier} image`,
      { imageId, tier }
    );
  }

  // Get S3 key based on tier
  let s3Key: string | null = null;
  switch (tier) {
    case DownloadTier.SMALL:
      s3Key = image.processedSmallUrl;
      break;
    case DownloadTier.HD:
      s3Key = image.processedHdUrl;
      break;
    case DownloadTier.ULTRA_HD:
      s3Key = image.processedUltraHdUrl;
      break;
  }

  if (!s3Key) {
    // Refund credits if tier not available
    if (transactionId) {
      await refundCredits(userId, creditCost, transactionId);
    }
    throw new AppError(
      `${tier} version not available`,
      HttpStatus.NOT_FOUND
    );
  }

  // Update download record
  await prisma.image.update({
    where: { id: imageId },
    data: {
      downloadTier: tier,
      creditsUsed: creditCost,
      lastDownloadedAt: new Date(),
    },
  });

  // Generate presigned download URL (1 hour expiry)
  const downloadUrl = await generatePresignedDownloadUrl(s3Key, 3600);

  logger.info('Image download URL generated', {
    imageId,
    userId,
    tier,
    creditsUsed: creditCost,
  });

  return downloadUrl;
}

/**
 * Get user's images
 * @param userId - User ID
 * @param limit - Number of images to return
 * @param offset - Pagination offset
 */
export async function getUserImages(
  userId: string,
  limit: number = 50,
  offset: number = 0
) {
  const images = await prisma.image.findMany({
    where: { userId },
    orderBy: { createdAt: 'desc' },
    take: limit,
    skip: offset,
  });

  const total = await prisma.image.count({
    where: { userId },
  });

  return {
    images,
    total,
    limit,
    offset,
  };
}

/**
 * Get single image details
 * @param imageId - Image ID
 * @param userId - User ID
 */
export async function getImageDetails(imageId: string, userId: string) {
  const image = await prisma.image.findUnique({
    where: { id: imageId },
  });

  if (!image) {
    throw new AppError('Image not found', HttpStatus.NOT_FOUND);
  }

  // Verify ownership
  if (image.userId !== userId) {
    throw new AppError('Unauthorized access', HttpStatus.FORBIDDEN);
  }

  return image;
}

/**
 * Delete image
 * @param imageId - Image ID
 * @param userId - User ID
 */
export async function deleteImage(imageId: string, userId: string): Promise<void> {
  const image = await prisma.image.findUnique({
    where: { id: imageId },
  });

  if (!image) {
    throw new AppError('Image not found', HttpStatus.NOT_FOUND);
  }

  // Verify ownership
  if (image.userId !== userId) {
    throw new AppError('Unauthorized access', HttpStatus.FORBIDDEN);
  }

  // Delete from database (S3 cleanup can be done async)
  await prisma.image.delete({
    where: { id: imageId },
  });

  logger.info('Image deleted', { imageId, userId });
}
