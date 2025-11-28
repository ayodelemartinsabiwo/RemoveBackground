/**
 * Cryptography Utilities
 * Bcrypt wrapper for secure password hashing
 * Production-grade with configurable rounds from environment
 */

import bcrypt from 'bcrypt';
import env from '../config/env';

/**
 * Hash a plain text password using bcrypt
 * @param password - Plain text password to hash
 * @returns Promise<string> - Hashed password
 */
export async function hashPassword(password: string): Promise<string> {
  const saltRounds = env.BCRYPT_ROUNDS;
  const hashedPassword = await bcrypt.hash(password, saltRounds);
  return hashedPassword;
}

/**
 * Compare a plain text password with a hashed password
 * @param password - Plain text password
 * @param hashedPassword - Hashed password from database
 * @returns Promise<boolean> - True if passwords match
 */
export async function comparePassword(
  password: string,
  hashedPassword: string
): Promise<boolean> {
  const isMatch = await bcrypt.compare(password, hashedPassword);
  return isMatch;
}

/**
 * Generate a random token for email verification or password reset
 * @param length - Length of the token (default: 32)
 * @returns string - Random hex token
 */
export function generateRandomToken(length: number = 32): string {
  const crypto = require('crypto');
  return crypto.randomBytes(length).toString('hex');
}
