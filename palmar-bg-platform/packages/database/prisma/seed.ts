/**
 * Database Seed Script
 * Run with: npx prisma db seed
 */
import { PrismaClient, Role, PlanType } from '@prisma/client';
import { hashPassword } from './seed-utils';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Clear existing data (for development only)
  console.log('Clearing existing data...');
  await prisma.image.deleteMany();
  await prisma.creditTransaction.deleteMany();
  await prisma.subscription.deleteMany();
  await prisma.user.deleteMany();

  // Create test users
  console.log('Creating test users...');

  const testPassword = await hashPassword('password123');
  const now = new Date();
  const thirtyDaysFromNow = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);

  // FREE User
  const freeUser = await prisma.user.create({
    data: {
      email: 'free@test.com',
      passwordHash: testPassword,
      firstName: 'Free',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscriptions: {
        create: {
          planType: PlanType.FREE,
          status: 'ACTIVE',
          creditsBalance: 3,
          creditsTotal: 3,
          billingCycle: 'lifetime',
          currentPeriodStart: now,
          currentPeriodEnd: null,
          autoRenew: false,
        },
      },
    },
  });

  // STARTER User
  const starterUser = await prisma.user.create({
    data: {
      email: 'starter@test.com',
      passwordHash: testPassword,
      firstName: 'Starter',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscriptions: {
        create: {
          planType: PlanType.STARTER_MONTHLY,
          status: 'ACTIVE',
          creditsBalance: 40,
          creditsTotal: 40,
          billingCycle: 'monthly',
          currentPeriodStart: now,
          currentPeriodEnd: thirtyDaysFromNow,
          autoRenew: true,
        },
      },
    },
  });

  // PROFESSIONAL User
  const proUser = await prisma.user.create({
    data: {
      email: 'pro@test.com',
      passwordHash: testPassword,
      firstName: 'Professional',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscriptions: {
        create: {
          planType: PlanType.PROFESSIONAL_MONTHLY,
          status: 'ACTIVE',
          creditsBalance: 120,
          creditsTotal: 120,
          billingCycle: 'monthly',
          currentPeriodStart: now,
          currentPeriodEnd: thirtyDaysFromNow,
          autoRenew: true,
        },
      },
    },
  });

  // ADMIN/ENTERPRISE User
  const adminUser = await prisma.user.create({
    data: {
      email: 'admin@palmar.com',
      passwordHash: testPassword,
      firstName: 'Admin',
      lastName: 'User',
      role: Role.ADMIN,
      emailVerified: true,
      subscriptions: {
        create: {
          planType: PlanType.ENTERPRISE_MONTHLY,
          status: 'ACTIVE',
          creditsBalance: 850,
          creditsTotal: 850,
          billingCycle: 'monthly',
          currentPeriodStart: now,
          currentPeriodEnd: thirtyDaysFromNow,
          autoRenew: true,
        },
      },
    },
  });

  console.log('✅ Created test users');

  // Grant initial credits via transactions
  console.log('Granting initial credits...');

  // Get the subscription IDs
  const freeSubscription = await prisma.subscription.findFirst({
    where: { userId: freeUser.id },
  });
  const starterSubscription = await prisma.subscription.findFirst({
    where: { userId: starterUser.id },
  });
  const proSubscription = await prisma.subscription.findFirst({
    where: { userId: proUser.id },
  });
  const adminSubscription = await prisma.subscription.findFirst({
    where: { userId: adminUser.id },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: freeUser.id,
      subscriptionId: freeSubscription!.id,
      amount: 3,
      type: 'BONUS',
      description: 'Welcome bonus - FREE plan',
      balanceAfter: 3,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: starterUser.id,
      subscriptionId: starterSubscription!.id,
      amount: 40,
      type: 'PURCHASE',
      description: 'Monthly credits - STARTER plan',
      balanceAfter: 40,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: proUser.id,
      subscriptionId: proSubscription!.id,
      amount: 120,
      type: 'PURCHASE',
      description: 'Monthly credits - PROFESSIONAL plan',
      balanceAfter: 120,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: adminUser.id,
      subscriptionId: adminSubscription!.id,
      amount: 850,
      type: 'PURCHASE',
      description: 'Monthly credits - ENTERPRISE plan',
      balanceAfter: 850,
    },
  });

  console.log('✅ Granted initial credits');

  // Create sample images for demonstration
  console.log('Creating sample images...');

  await prisma.image.create({
    data: {
      user: { connect: { id: proUser.id } },
      originalS3Key: 'sample/portrait-original.jpg',
      originalFilename: 'portrait.jpg',
      processedS3Key: 'processed/portrait-transparent.png',
      processedSmallUrl: 's3://palmar-bg-images/sample/portrait-512.png',
      processedHdUrl: 's3://palmar-bg-images/sample/portrait-1920.png',
      processedUltraHdUrl: 's3://palmar-bg-images/sample/portrait-3840.png',
      originalFileSize: BigInt(2457600),
      processedFileSize: BigInt(1843200),
      originalWidth: 1920,
      originalHeight: 2560,
      mimeType: 'image/jpeg',
      outputFormat: 'png',
      processingStatus: 'COMPLETED',
      backgroundType: 'TRANSPARENT',
      creditsUsed: 1,
      processingTimeMs: 4500,
      processedAt: new Date(),
    },
  });

  await prisma.image.create({
    data: {
      user: { connect: { id: proUser.id } },
      originalS3Key: 'sample/product-original.jpg',
      originalFilename: 'product.jpg',
      processedS3Key: 'processed/product-white-bg.png',
      processedSmallUrl: 's3://palmar-bg-images/sample/product-512.png',
      processedHdUrl: 's3://palmar-bg-images/sample/product-1920.png',
      originalFileSize: BigInt(1843200),
      processedFileSize: BigInt(1245000),
      originalWidth: 1500,
      originalHeight: 1500,
      mimeType: 'image/jpeg',
      outputFormat: 'png',
      processingStatus: 'COMPLETED',
      backgroundType: 'SOLID',
      backgroundConfig: { solidColor: '#FFFFFF' },
      creditsUsed: 1,
      processingTimeMs: 3200,
      processedAt: new Date(),
    },
  });

  console.log('✅ Created sample images');

  // Summary
  console.log('\n📊 Seed Summary:');
  console.log('Users created:');
  console.log('  - free@test.com (password: password123) - FREE plan, 3 credits');
  console.log('  - starter@test.com (password: password123) - STARTER plan, 40 credits');
  console.log('  - pro@test.com (password: password123) - PROFESSIONAL plan, 120 credits');
  console.log('  - admin@palmar.com (password: password123) - ENTERPRISE plan, 850 credits');
  console.log('\n✅ Database seeded successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
