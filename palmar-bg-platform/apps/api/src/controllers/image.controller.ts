/**
 * Image Controllers
 * Handle HTTP requests for image operations
 * Production-grade with proper error handling
 */

import { Request, Response } from 'express';
import { z } from 'zod';
import { BackgroundType, DownloadTier } from '@prisma/client';
import {
  uploadAndProcessImage,
  downloadProcessedImage,
  getUserImages,
  getImageDetails,
  deleteImage,
} from '../services/image.service';
import { asyncHandler, AppError, HttpStatus } from '../middleware/errorHandler';

/**
 * Validation Schemas
 */
export const uploadImageSchema = z.object({
  backgroundType: z
    .nativeEnum(BackgroundType)
    .optional()
    .default(BackgroundType.TRANSPARENT),
  backgroundColor: z.string().regex(/^#[0-9A-F]{6}$/i).optional(),
  backgroundAngle: z.number().min(0).max(360).optional(),
  backgroundTexture: z.string().optional(),
});

export const downloadImageSchema = z.object({
  tier: z.nativeEnum(DownloadTier),
});

export const listImagesSchema = z.object({
  limit: z.string().transform(Number).pipe(z.number().min(1).max(100)).optional(),
  offset: z.string().transform(Number).pipe(z.number().min(0)).optional(),
});

export const imageIdSchema = z.object({
  id: z.string().uuid('Invalid image ID'),
});

/**
 * Upload and process image
 * POST /api/v1/images/upload
 * Requires authentication
 * Multipart form data with 'image' field
 */
export const uploadImage = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new AppError('User not authenticated', HttpStatus.UNAUTHORIZED);
  }

  if (!req.file) {
    throw new AppError('No image file provided', HttpStatus.BAD_REQUEST);
  }

  // Parse background configuration from body
  const backgroundType = (req.body.backgroundType as BackgroundType) ?? BackgroundType.TRANSPARENT;
  const backgroundConfig: Record<string, unknown> = {};

  if (req.body.backgroundColor) {
    backgroundConfig.color = req.body.backgroundColor;
  }
  if (req.body.backgroundAngle) {
    backgroundConfig.angle = parseInt(req.body.backgroundAngle, 10);
  }
  if (req.body.backgroundTexture) {
    backgroundConfig.textureType = req.body.backgroundTexture;
  }

  const image = await uploadAndProcessImage({
    userId: req.user.id,
    file: req.file,
    backgroundType,
    backgroundConfig,
  });

  // Return image directly for consistency
  res.status(HttpStatus.CREATED).json({
    success: true,
    data: { image }, // Keep { image } wrapper for backward compatibility with frontend
    message: 'Image uploaded and queued for processing',
  });
});

/**
 * Download processed image
 * GET /api/v1/images/:id/download?tier=HD
 * Requires authentication
 */
export const downloadImage = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new AppError('User not authenticated', HttpStatus.UNAUTHORIZED);
  }

  const id = req.params.id!;
  const { tier } = req.query as { tier: DownloadTier };

  const downloadUrl = await downloadProcessedImage(id, req.user.id, tier);

  res.status(HttpStatus.OK).json({
    success: true,
    data: { downloadUrl },
    message: 'Download URL generated',
  });
});

/**
 * Get user's images
 * GET /api/v1/images?limit=50&offset=0
 * Requires authentication
 */
export const listImages = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new AppError('User not authenticated', HttpStatus.UNAUTHORIZED);
  }

  const limit = req.query.limit! ? parseInt(req.query.limit! as string, 10) : 50;
  const offset = req.query.offset! ? parseInt(req.query.offset! as string, 10) : 0;

  const result = await getUserImages(req.user.id, limit, offset);

  res.status(HttpStatus.OK).json({
    success: true,
    data: result,
  });
});

/**
 * Get single image details
 * GET /api/v1/images/:id
 * Requires authentication
 */
export const getImage = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new AppError('User not authenticated', HttpStatus.UNAUTHORIZED);
  }

  const id = req.params.id!;

  const image = await getImageDetails(id, req.user.id);

  // Return image directly, not wrapped in { image }
  // Frontend expects response.data.data to be the image object
  res.status(HttpStatus.OK).json({
    success: true,
    data: image,
  });
});

/**
 * Delete image
 * DELETE /api/v1/images/:id
 * Requires authentication
 */
export const removeImage = asyncHandler(async (req: Request, res: Response) => {
  if (!req.user) {
    throw new AppError('User not authenticated', HttpStatus.UNAUTHORIZED);
  }

  const id = req.params.id!;

  await deleteImage(id, req.user.id);

  res.status(HttpStatus.OK).json({
    success: true,
    message: 'Image deleted successfully',
  });
});
