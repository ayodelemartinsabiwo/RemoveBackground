/**
 * Swagger/OpenAPI Configuration
 */
import swaggerJsdoc from 'swagger-jsdoc';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Palmar Professional API',
      version: '1.0.0',
      description: 'AI-powered background removal API with credit-based pricing',
      contact: {
        name: 'Palmar Professional',
        email: 'support@palmar.com',
      },
      license: {
        name: 'Proprietary',
      },
    },
    servers: [
      {
        url: 'http://localhost:3001',
        description: 'Development server',
      },
      {
        url: 'https://api.palmar.com',
        description: 'Production server',
      },
    ],
    components: {
      securitySchemes: {
        BearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
          description: 'JWT token from /auth/login or /auth/register',
        },
      },
      schemas: {
        User: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            email: { type: 'string', format: 'email' },
            firstName: { type: 'string', nullable: true },
            lastName: { type: 'string', nullable: true },
            role: { type: 'string', enum: ['USER', 'ADMIN', 'SUPER_ADMIN'] },
            emailVerified: { type: 'boolean' },
            createdAt: { type: 'string', format: 'date-time' },
            updatedAt: { type: 'string', format: 'date-time' },
          },
        },
        Image: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            userId: { type: 'string', format: 'uuid' },
            originalUrl: { type: 'string' },
            processedSmallUrl: { type: 'string', nullable: true },
            processedHdUrl: { type: 'string', nullable: true },
            processedUltraHdUrl: { type: 'string', nullable: true },
            fileSize: { type: 'integer' },
            width: { type: 'integer' },
            height: { type: 'integer' },
            mimeType: { type: 'string' },
            status: { type: 'string', enum: ['PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'] },
            backgroundType: { type: 'string', enum: ['TRANSPARENT', 'SOLID', 'GRADIENT', 'TEXTURE', 'CUSTOM'] },
            solidColor: { type: 'string', nullable: true },
            creditsUsed: { type: 'integer' },
            processingTime: { type: 'number', nullable: true },
            createdAt: { type: 'string', format: 'date-time' },
            updatedAt: { type: 'string', format: 'date-time' },
          },
        },
        Subscription: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            userId: { type: 'string', format: 'uuid' },
            planType: { type: 'string' },
            status: { type: 'string', enum: ['ACTIVE', 'CANCELED', 'EXPIRED', 'PAST_DUE'] },
            startDate: { type: 'string', format: 'date-time' },
            endDate: { type: 'string', format: 'date-time', nullable: true },
            creditsIncluded: { type: 'integer' },
            amount: { type: 'number', nullable: true },
            currency: { type: 'string', nullable: true },
            nextBillingDate: { type: 'string', format: 'date-time', nullable: true },
          },
        },
        Error: {
          type: 'object',
          properties: {
            success: { type: 'boolean', example: false },
            message: { type: 'string' },
            statusCode: { type: 'integer' },
          },
        },
      },
    },
    tags: [
      {
        name: 'Authentication',
        description: 'User registration, login, and token management',
      },
      {
        name: 'Images',
        description: 'Image upload, processing, and download',
      },
      {
        name: 'Users',
        description: 'User profile and credit management',
      },
      {
        name: 'Health',
        description: 'Service health and status checks',
      },
    ],
  },
  apis: ['./src/routes/*.ts', './src/controllers/*.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
