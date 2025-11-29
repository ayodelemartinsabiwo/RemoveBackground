/**
 * Authentication Service
 * Business logic for user registration, login, and token management
 * Production-grade with proper error handling and security
 */

import { User, Role, PlanType } from '@prisma/client';
import prisma from '../config/database';
import redisClient from '../config/redis';
import logger from '../utils/logger';
import { hashPassword, comparePassword } from '../utils/crypto';
import { signAccessToken, signRefreshToken, verifyRefreshToken } from '../utils/jwt';

/**
 * Registration Input
 */
export interface RegisterInput {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

/**
 * Login Input
 */
export interface LoginInput {
  email: string;
  password: string;
}

/**
 * Authentication Response
 */
export interface AuthResponse {
  user: {
    id: string;
    email: string;
    firstName: string | null;
    lastName: string | null;
    role: Role;
  };
  accessToken: string;
  refreshToken: string;
}

/**
 * Register a new user
 * Creates user account with FREE plan (3 credits/month)
 * @param input - Registration data
 * @returns AuthResponse - User data with tokens
 * @throws Error if email already exists
 */
export async function registerUser(input: RegisterInput): Promise<AuthResponse> {
  const { email, password, firstName, lastName } = input;

  // Check if user already exists
  const existingUser = await prisma.user.findUnique({
    where: { email },
  });

  if (existingUser) {
    throw new Error('Email already registered');
  }

  // Hash password
  const passwordHash = await hashPassword(password);

  // Create user with FREE subscription
  const user = await prisma.user.create({
    data: {
      email,
      passwordHash,
      firstName: firstName ?? null,
      lastName: lastName ?? null,
      role: Role.USER,
      emailVerified: false,
      twoFactorEnabled: false,
      subscriptions: {
        create: {
          planType: PlanType.FREE,
          creditsBalance: 3,
          status: 'ACTIVE',
          autoRenew: false,
          currentPeriodStart: new Date(),
          currentPeriodEnd: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
        },
      },
    },
    include: {
      subscriptions: true,
    },
  });

  logger.info('User registered successfully', {
    userId: user.id,
    email: user.email,
  });

  // Generate tokens
  const accessToken = signAccessToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  const refreshToken = signRefreshToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  // Store refresh token in Redis (7 days expiry)
  await redisClient.setex(
    `refresh_token:${user.id}`,
    7 * 24 * 60 * 60,
    refreshToken
  );

  return {
    user: {
      id: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
      role: user.role,
    },
    accessToken,
    refreshToken,
  };
}

/**
 * Login an existing user
 * Verifies credentials and generates new tokens
 * @param input - Login credentials
 * @returns AuthResponse - User data with tokens
 * @throws Error if credentials are invalid
 */
export async function loginUser(input: LoginInput): Promise<AuthResponse> {
  const { email, password } = input;

  // Find user by email
  const user = await prisma.user.findUnique({
    where: { email },
    include: {
      subscriptions: {
        where: { status: 'ACTIVE' },
        orderBy: { createdAt: 'desc' },
        take: 1,
      },
    },
  });

  if (!user) {
    throw new Error('Invalid email or password');
  }

  // Check if user has password (not OAuth-only account)
  if (!user.passwordHash) {
    throw new Error('Please login with Google');
  }

  // Verify password
  const isPasswordValid = await comparePassword(password, user.passwordHash);

  if (!isPasswordValid) {
    throw new Error('Invalid email or password');
  }

  // Update last login timestamp
  await prisma.user.update({
    where: { id: user.id },
    data: { lastLoginAt: new Date() },
  });

  logger.info('User logged in successfully', {
    userId: user.id,
    email: user.email,
  });

  // Generate tokens
  const accessToken = signAccessToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  const refreshToken = signRefreshToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  // Store refresh token in Redis (7 days expiry)
  await redisClient.setex(
    `refresh_token:${user.id}`,
    7 * 24 * 60 * 60,
    refreshToken
  );

  return {
    user: {
      id: user.id,
      email: user.email,
      firstName: user.firstName,
      lastName: user.lastName,
      role: user.role,
    },
    accessToken,
    refreshToken,
  };
}

/**
 * Refresh access token using refresh token
 * Implements token rotation for enhanced security
 * @param refreshToken - Current refresh token
 * @returns Object with new access and refresh tokens
 * @throws Error if refresh token is invalid or expired
 */
export async function refreshAccessToken(refreshToken: string): Promise<{
  accessToken: string;
  refreshToken: string;
}> {
  // Verify refresh token
  const decoded = verifyRefreshToken(refreshToken);

  if (!decoded) {
    throw new Error('Invalid or expired refresh token');
  }

  // Check if token exists in Redis
  const storedToken = await redisClient.get(`refresh_token:${decoded.userId}`);

  if (!storedToken || storedToken !== refreshToken) {
    throw new Error('Refresh token has been revoked');
  }

  // Find user
  const user = await prisma.user.findUnique({
    where: { id: decoded.userId },
  });

  if (!user) {
    throw new Error('User not found');
  }

  // Generate new tokens (token rotation)
  const newAccessToken = signAccessToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  const newRefreshToken = signRefreshToken({
    userId: user.id,
    email: user.email,
    role: user.role,
  });

  // Replace old refresh token with new one in Redis
  await redisClient.setex(
    `refresh_token:${user.id}`,
    7 * 24 * 60 * 60,
    newRefreshToken
  );

  logger.info('Access token refreshed', {
    userId: user.id,
    email: user.email,
  });

  return {
    accessToken: newAccessToken,
    refreshToken: newRefreshToken,
  };
}

/**
 * Logout user by revoking refresh token
 * @param userId - User ID to logout
 */
export async function logoutUser(userId: string): Promise<void> {
  // Remove refresh token from Redis
  await redisClient.del(`refresh_token:${userId}`);

  logger.info('User logged out', { userId });
}

/**
 * Get user by ID
 * @param userId - User ID
 * @returns User object or null
 */
export async function getUserById(userId: string): Promise<User | null> {
  const user = await prisma.user.findUnique({
    where: { id: userId },
  });

  return user;
}
