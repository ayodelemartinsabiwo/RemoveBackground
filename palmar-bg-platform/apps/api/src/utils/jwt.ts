/**
 * JWT Utilities
 * Sign and verify JSON Web Tokens for authentication
 * Supports both access tokens (short-lived) and refresh tokens (long-lived)
 */

import jwt, { JwtPayload, SignOptions, VerifyOptions } from 'jsonwebtoken';
import env from '../config/env';

/**
 * JWT Payload Interface
 */
export interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

/**
 * Decoded JWT with standard claims
 */
export interface DecodedToken extends TokenPayload, JwtPayload {}

/**
 * Sign an access token (short-lived)
 * @param payload - User information to encode in token
 * @returns string - Signed JWT access token
 */
export function signAccessToken(payload: TokenPayload): string {
  const options: SignOptions = {
    expiresIn: env.JWT_EXPIRES_IN as any,
    issuer: 'palmar-bg-api',
    audience: 'palmar-bg-web',
  };

  return jwt.sign(payload, env.JWT_SECRET, options);
}

/**
 * Sign a refresh token (long-lived)
 * @param payload - User information to encode in token
 * @returns string - Signed JWT refresh token
 */
export function signRefreshToken(payload: TokenPayload): string {
  const options: SignOptions = {
    expiresIn: env.REFRESH_TOKEN_EXPIRES_IN as any,
    issuer: 'palmar-bg-api',
    audience: 'palmar-bg-web',
  };

  return jwt.sign(payload, env.REFRESH_TOKEN_SECRET, options);
}

/**
 * Verify an access token
 * @param token - JWT access token to verify
 * @returns DecodedToken | null - Decoded token payload or null if invalid
 */
export function verifyAccessToken(token: string): TokenPayload | null {
  try {
    const options: VerifyOptions = {
      issuer: 'palmar-bg-api',
      audience: 'palmar-bg-web',
    };

    const decoded = jwt.verify(token, env.JWT_SECRET, options) as TokenPayload;
    return decoded;
  } catch (error) {
    // Token invalid, expired, or malformed
    return null;
  }
}

/**
 * Verify a refresh token
 * @param token - JWT refresh token to verify
 * @returns DecodedToken | null - Decoded token payload or null if invalid
 */
export function verifyRefreshToken(token: string): TokenPayload | null {
  try {
    const options: VerifyOptions = {
      issuer: 'palmar-bg-api',
      audience: 'palmar-bg-web',
    };

    const decoded = jwt.verify(
      token,
      env.REFRESH_TOKEN_SECRET,
      options
    ) as TokenPayload;
    return decoded;
  } catch (error) {
    // Token invalid, expired, or malformed
    return null;
  }
}

/**
 * Decode a token without verifying (for debugging)
 * WARNING: Do not use for authentication - use verify functions
 * @param token - JWT token to decode
 * @returns DecodedToken | null - Decoded token payload or null if malformed
 */
export function decodeToken(token: string): DecodedToken | null {
  try {
    const decoded = jwt.decode(token) as DecodedToken;
    return decoded;
  } catch (error) {
    return null;
  }
}
