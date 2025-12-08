/**
 * User Routes
 * Handles user-related operations like credits, profile, etc.
 */

import { Router, Request, Response, NextFunction } from 'express';
import { authenticate } from '../middleware/auth';
import prisma from '../config/database';
import logger from '../utils/logger';

const router = Router();

/**
 * GET /api/v1/users/credits
 * Get user's current credit balance
 */
router.get(
  '/credits',
  authenticate,
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = (req as any).user.id;

      // Get user with subscription (which contains credits)
      const user = await prisma.user.findUnique({
        where: { id: userId },
        select: {
          id: true,
          email: true,
          role: true,
          subscriptions: {
            where: {
              status: 'ACTIVE',
            },
            orderBy: {
              createdAt: 'desc',
            },
            take: 1,
            select: {
              creditsBalance: true,
              creditsTotal: true,
              planType: true,
            },
          },
        },
      });

      if (!user) {
        res.status(404).json({
          success: false,
          message: 'User not found',
        });
        return;
      }

      // Get credits from active subscription or default to 0
      const credits = user.subscriptions[0]?.creditsBalance ?? 0;

      logger.info('User credits fetched', {
        userId: user.id,
        credits,
      });

      res.status(200).json({
        success: true,
        data: {
          credits: Number(credits),
          email: user.email,
          role: user.role,
          planType: user.subscriptions[0]?.planType || 'FREE',
        },
      });
    } catch (error) {
      logger.error('Failed to fetch user credits', { error });
      next(error);
    }
  }
);

/**
 * GET /api/v1/users/profile
 * Get user profile information
 */
router.get(
  '/profile',
  authenticate,
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = (req as any).user.id;

      const user = await prisma.user.findUnique({
        where: { id: userId },
        select: {
          id: true,
          email: true,
          role: true,
          emailVerified: true,
          createdAt: true,
          subscriptions: {
            where: {
              status: 'ACTIVE',
            },
            orderBy: {
              createdAt: 'desc',
            },
            take: 1,
            select: {
              creditsBalance: true,
              creditsTotal: true,
              planType: true,
            },
          },
        },
      });

      if (!user) {
        res.status(404).json({
          success: false,
          message: 'User not found',
        });
        return;
      }

      // Count user's images
      const totalImages = await prisma.image.count({
        where: { userId, isDeleted: false },
      });

      const credits = user.subscriptions[0]?.creditsBalance ?? 0;

      res.status(200).json({
        success: true,
        data: {
          id: user.id,
          email: user.email,
          credits: Number(credits),
          role: user.role,
          emailVerified: user.emailVerified,
          totalImages,
          memberSince: user.createdAt,
          planType: user.subscriptions[0]?.planType || 'FREE',
        },
      });
    } catch (error) {
      logger.error('Failed to fetch user profile', { error });
      next(error);
    }
  }
);

/**
 * GET /api/v1/users/stats
 * Get user statistics (images processed, credits used, etc.)
 */
router.get(
  '/stats',
  authenticate,
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const userId = (req as any).user.id;

      // Get image statistics
      const [totalImages, completedImages, failedImages, totalCreditsUsed] = await Promise.all([
        prisma.image.count({
          where: { userId, isDeleted: false },
        }),
        prisma.image.count({
          where: { userId, isDeleted: false, processingStatus: 'COMPLETED' },
        }),
        prisma.image.count({
          where: { userId, isDeleted: false, processingStatus: 'FAILED' },
        }),
        prisma.image.aggregate({
          where: { userId, isDeleted: false },
          _sum: {
            creditsUsed: true,
          },
        }),
      ]);

      res.status(200).json({
        success: true,
        data: {
          totalImages,
          completedImages,
          failedImages,
          processingImages: totalImages - completedImages - failedImages,
          totalCreditsUsed: Number(totalCreditsUsed._sum.creditsUsed || 0),
        },
      });
    } catch (error) {
      logger.error('Failed to fetch user stats', { error });
      next(error);
    }
  }
);

export default router;
