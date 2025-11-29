/**
 * Type definitions for Palmar Background Removal Web App
 */

export interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  role: 'USER' | 'ADMIN' | 'SUPER_ADMIN';
  createdAt: string;
  updatedAt: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface CreditBalance {
  userId: string;
  balance: number;
  lifetimeUsed: number;
  updatedAt: string;
}

export type ImageStatus = 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';

export type BackgroundType = 'TRANSPARENT' | 'SOLID' | 'GRADIENT' | 'TEXTURE' | 'CUSTOM';

export type DownloadTier = 'SMALL' | 'HD' | 'ULTRA_HD';

export interface BackgroundConfig {
  color?: string;
  angle?: number;
  textureType?: string;
  customImageKey?: string;
}

export interface Image {
  id: string;
  userId: string;
  originalFilename: string;
  originalS3Key: string;
  processedSmallUrl?: string;
  processedHdUrl?: string;
  processedUltraHdUrl?: string;
  status: ImageStatus;
  backgroundType: BackgroundType;
  backgroundConfig?: BackgroundConfig;
  downloadTier: DownloadTier;
  mimeType?: string;
  fileSize?: number;
  processingTimeMs?: number;
  errorMessage?: string;
  createdAt: string;
  updatedAt: string;
  processedAt?: string;
}

export interface UploadImageRequest {
  file: File;
  backgroundType: BackgroundType;
  backgroundConfig?: BackgroundConfig;
  downloadTier: DownloadTier;
}

export interface ProcessingStatus {
  imageId: string;
  status: ImageStatus;
  progress?: number;
  processedUrls?: {
    small?: string;
    hd?: string;
    ultraHd?: string;
  };
  error?: string;
}

export type PlanType =
  | 'FREE'
  | 'STARTER_MONTHLY'
  | 'PROFESSIONAL_MONTHLY'
  | 'BUSINESS_MONTHLY'
  | 'ENTERPRISE_MONTHLY'
  | 'ULTRA_MONTHLY'
  | 'STARTER_LIFETIME'
  | 'PROFESSIONAL_LIFETIME'
  | 'BUSINESS_LIFETIME'
  | 'ENTERPRISE_LIFETIME';

export interface Subscription {
  id: string;
  userId: string;
  planType: PlanType;
  status: 'ACTIVE' | 'CANCELLED' | 'EXPIRED';
  creditsIncluded: number;
  startDate: string;
  endDate?: string;
  cancelledAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}
