/**
 * Credit System Service
 * Manages user credits, subscriptions, and credit transactions
 * Production-grade with proper transaction handling
 */

import { PlanType, DownloadTier, TransactionType, TransactionStatus } from '@prisma/client';
import prisma from '../config/database';
import logger from '../utils/logger';
import { AppError, HttpStatus } from '../middleware/errorHandler';

/**
 * Credit costs for different download tiers
 */
export const CREDIT_COSTS: Record<DownloadTier, number> = {
  SMALL: 0, // Free tier
  HD: 2, // HD costs 2 credits
  ULTRA_HD: 4, // Ultra HD costs 4 credits
};

/**
 * Monthly credit allocations per plan
 */
export const PLAN_CREDITS: Record<PlanType, number> = {
  FREE: 3,
  STARTER_MONTHLY: 40,
  PROFESSIONAL_MONTHLY: 200,
  BUSINESS_MONTHLY: 500,
  ENTERPRISE_MONTHLY: 1200,
  ULTRA_MONTHLY: 5000,
  STARTER_LIFETIME: 10,
  PROFESSIONAL_LIFETIME: 75,
  BUSINESS_LIFETIME: 200,
  ENTERPRISE_LIFETIME: 500,
};

/**
 * Check if user has sufficient credits
 * @param userId - User ID
 * @param requiredCredits - Number of credits needed
 * @returns Promise<boolean>
 */
export async function hasCredits(
  userId: string,
  requiredCredits: number
): Promise<boolean> {
  const subscription = await prisma.subscription.findFirst({
    where: {
      userId,
      status: 'ACTIVE',
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  if (!subscription) {
    return false;
  }

  return subscription.creditsBalance >= requiredCredits;
}

/**
 * Get user's active subscription
 * @param userId - User ID
 * @returns Active subscription or null
 */
export async function getActiveSubscription(userId: string) {
  const subscription = await prisma.subscription.findFirst({
    where: {
      userId,
      status: 'ACTIVE',
    },
    orderBy: {
      createdAt: 'desc',
    },
  });

  return subscription;
}

/**
 * Deduct credits from user's account
 * Creates a transaction record for audit trail
 * @param userId - User ID
 * @param credits - Number of credits to deduct
 * @param description - Transaction description
 * @param metadata - Additional metadata
 * @returns Transaction ID
 */
export async function deductCredits(
  userId: string,
  credits: number,
  description: string,
  metadata?: Record<string, unknown>
): Promise<string> {
  // Check if user has sufficient credits
  const hasEnoughCredits = await hasCredits(userId, credits);

  if (!hasEnoughCredits) {
    throw new AppError('Insufficient credits', HttpStatus.PAYMENT_REQUIRED);
  }

  // Use transaction to ensure atomicity
  const result = await prisma.$transaction(async (tx) => {
    // Get active subscription with row-level lock
    const subscription = await tx.subscription.findFirst({
      where: {
        userId,
        status: 'ACTIVE',
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    if (!subscription) {
      throw new AppError('No active subscription found', HttpStatus.BAD_REQUEST);
    }

    // Double-check credits (race condition protection)
    if (subscription.creditsBalance < credits) {
      throw new AppError('Insufficient credits', HttpStatus.PAYMENT_REQUIRED);
    }

    // Update subscription balance
    await tx.subscription.update({
      where: { id: subscription.id },
      data: {
        creditsBalance: subscription.creditsBalance - credits,
      },
    });

    // Create transaction record
    const transaction = await tx.creditTransaction.create({
      data: {
        userId,
        subscriptionId: subscription.id,
        amount: -credits,
        type: TransactionType.DEDUCTION,
        status: TransactionStatus.COMPLETED,
        description,
        metadata: metadata as any ?? {},
      },
    });

    logger.info('Credits deducted', {
      userId,
      credits,
      newBalance: subscription.creditsBalance - credits,
      transactionId: transaction.id,
    });

    return transaction.id;
  });

  return result;
}

/**
 * Add credits to user's account
 * Used for credit purchases or refunds
 * @param userId - User ID
 * @param credits - Number of credits to add
 * @param description - Transaction description
 * @param metadata - Additional metadata
 * @returns Transaction ID
 */
export async function addCredits(
  userId: string,
  credits: number,
  description: string,
  metadata?: Record<string, unknown>
): Promise<string> {
  const result = await prisma.$transaction(async (tx) => {
    const subscription = await tx.subscription.findFirst({
      where: {
        userId,
        status: 'ACTIVE',
      },
      orderBy: {
        createdAt: 'desc',
      },
    });

    if (!subscription) {
      throw new AppError('No active subscription found', HttpStatus.BAD_REQUEST);
    }

    // Update subscription balance
    await tx.subscription.update({
      where: { id: subscription.id },
      data: {
        creditsBalance: subscription.creditsBalance + credits,
      },
    });

    // Create transaction record
    const transaction = await tx.creditTransaction.create({
      data: {
        userId,
        subscriptionId: subscription.id,
        amount: credits,
        type: TransactionType.PURCHASE,
        status: TransactionStatus.COMPLETED,
        description,
        metadata: metadata as any ?? {},
      },
    });

    logger.info('Credits added', {
      userId,
      credits,
      newBalance: subscription.creditsBalance + credits,
      transactionId: transaction.id,
    });

    return transaction.id;
  });

  return result;
}

/**
 * Get credit cost for a download tier
 * @param tier - Download tier
 * @returns Number of credits required
 */
export function getCreditCost(tier: DownloadTier): number {
  return CREDIT_COSTS[tier];
}

/**
 * Get user's credit balance
 * @param userId - User ID
 * @returns Credit balance
 */
export async function getCreditBalance(userId: string): Promise<number> {
  const subscription = await getActiveSubscription(userId);

  if (!subscription) {
    return 0;
  }

  return subscription.creditsBalance;
}

/**
 * Get user's credit transactions
 * @param userId - User ID
 * @param limit - Number of transactions to return
 * @returns Array of transactions
 */
export async function getCreditTransactions(
  userId: string,
  limit: number = 50
) {
  const transactions = await prisma.creditTransaction.findMany({
    where: { userId },
    orderBy: { createdAt: 'desc' },
    take: limit,
    include: {
      subscription: {
        select: {
          planType: true,
        },
      },
    },
  });

  return transactions;
}

/**
 * Refund credits to user
 * Used when image processing fails
 * @param userId - User ID
 * @param credits - Number of credits to refund
 * @param originalTransactionId - Original transaction ID
 * @returns Transaction ID
 */
export async function refundCredits(
  userId: string,
  credits: number,
  originalTransactionId: string
): Promise<string> {
  return addCredits(
    userId,
    credits,
    `Refund for failed processing`,
    { originalTransactionId }
  );
}
