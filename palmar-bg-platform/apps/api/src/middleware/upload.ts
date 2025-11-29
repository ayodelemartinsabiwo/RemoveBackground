/**
 * File Upload Middleware (Multer)
 * Handles multipart/form-data file uploads
 * Production-grade with validation and security
 */

import multer from 'multer';
import { NextFunction } from 'express';
import { AppError, HttpStatus } from './errorHandler';
import env from '../config/env';

/**
 * Multer memory storage
 * Files are stored in memory as Buffer objects
 */
const storage = multer.memoryStorage();

/**
 * File filter for image uploads
 * Only allows specific image types
 */
const imageFileFilter = (
  _req: Express.Request,
  file: Express.Multer.File,
  callback: multer.FileFilterCallback
): void => {
  const allowedTypes = env.ALLOWED_FILE_TYPES;
  const fileType = file.mimetype;

  if (allowedTypes.includes(fileType)) {
    callback(null, true);
  } else {
    callback(
      new AppError(
        `Invalid file type: ${fileType}. Allowed: ${allowedTypes.join(', ')}`,
        HttpStatus.BAD_REQUEST
      )
    );
  }
};

/**
 * Multer upload configuration for single image
 */
export const uploadSingleImage = multer({
  storage,
  fileFilter: imageFileFilter,
  limits: {
    fileSize: env.MAX_FILE_SIZE, // 25MB default
    files: 1, // Only 1 file per request
  },
}).single('image'); // Field name must be 'image'

/**
 * Multer upload configuration for multiple images (batch)
 */
export const uploadMultipleImages = multer({
  storage,
  fileFilter: imageFileFilter,
  limits: {
    fileSize: env.MAX_FILE_SIZE,
    files: 500, // Max 500 files per batch
  },
}).array('images', 500); // Field name must be 'images'

/**
 * Error handler for Multer errors
 */
export function handleMulterError(
  error: unknown,
  _req: Express.Request,
  _res: Express.Response,
  next: NextFunction
): void {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      next(
        new AppError(
          `File too large. Maximum size: ${env.MAX_FILE_SIZE / (1024 * 1024)}MB`,
          HttpStatus.BAD_REQUEST
        )
      );
    } else if (error.code === 'LIMIT_FILE_COUNT') {
      next(
        new AppError('Too many files uploaded', HttpStatus.BAD_REQUEST)
      );
    } else if (error.code === 'LIMIT_UNEXPECTED_FILE') {
      next(
        new AppError('Unexpected file field', HttpStatus.BAD_REQUEST)
      );
    } else {
      next(new AppError(error.message, HttpStatus.BAD_REQUEST));
    }
  } else {
    next(error);
  }
}
