/**
 * Image Routes
 * Defines all image-related endpoints
 */

import { Router } from 'express';
import {
  uploadImage,
  downloadImage,
  listImages,
  getImage,
  removeImage,
  uploadImageSchema,
  downloadImageSchema,
  listImagesSchema,
  imageIdSchema,
} from '../controllers/image.controller';
import { authenticate } from '../middleware/auth';
import { validateQuery, validateParams } from '../middleware/validation';
import { uploadSingleImage, handleMulterError } from '../middleware/upload';

const router = Router();

// All image routes require authentication
router.use(authenticate);

/**
 * POST /api/v1/images/upload
 * Upload and process an image
 * Multipart form data with 'image' field
 */
router.post('/upload', uploadSingleImage, handleMulterError, uploadImage);

/**
 * GET /api/v1/images
 * Get user's images with pagination
 */
router.get('/', validateQuery(listImagesSchema), listImages);

/**
 * GET /api/v1/images/:id
 * Get single image details
 */
router.get('/:id', validateParams(imageIdSchema), getImage);

/**
 * GET /api/v1/images/:id/download
 * Download processed image (deducts credits)
 */
router.get(
  '/:id/download',
  validateParams(imageIdSchema),
  validateQuery(downloadImageSchema),
  downloadImage
);

/**
 * DELETE /api/v1/images/:id
 * Delete an image
 */
router.delete('/:id', validateParams(imageIdSchema), removeImage);

export default router;
