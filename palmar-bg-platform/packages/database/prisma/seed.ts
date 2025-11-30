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
  await prisma.download.deleteMany();
  await prisma.image.deleteMany();
  await prisma.creditTransaction.deleteMany();
  await prisma.subscription.deleteMany();
  await prisma.user.deleteMany();

  // Create test users
  console.log('Creating test users...');

  const testPassword = await hashPassword('password123');

  const freeUser = await prisma.user.create({
    data: {
      email: 'free@test.com',
      passwordHash: testPassword,
      firstName: 'Free',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscription: {
        create: {
          planType: PlanType.FREE,
          status: 'ACTIVE',
          startDate: new Date(),
          creditsIncluded: 3,
          nextBillingDate: null,
        },
      },
    },
  });

  const starterUser = await prisma.user.create({
    data: {
      email: 'starter@test.com',
      passwordHash: testPassword,
      firstName: 'Starter',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscription: {
        create: {
          planType: PlanType.STARTER_MONTHLY,
          status: 'ACTIVE',
          startDate: new Date(),
          creditsIncluded: 40,
          amount: 9.0,
          currency: 'USD',
          nextBillingDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 days
        },
      },
    },
  });

  const proUser = await prisma.user.create({
    data: {
      email: 'pro@test.com',
      passwordHash: testPassword,
      firstName: 'Professional',
      lastName: 'User',
      role: Role.USER,
      emailVerified: true,
      subscription: {
        create: {
          planType: PlanType.PROFESSIONAL_MONTHLY,
          status: 'ACTIVE',
          startDate: new Date(),
          creditsIncluded: 120,
          amount: 19.0,
          currency: 'USD',
          nextBillingDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        },
      },
    },
  });

  const adminUser = await prisma.user.create({
    data: {
      email: 'admin@palmar.com',
      passwordHash: testPassword,
      firstName: 'Admin',
      lastName: 'User',
      role: Role.ADMIN,
      emailVerified: true,
      subscription: {
        create: {
          planType: PlanType.ENTERPRISE_MONTHLY,
          status: 'ACTIVE',
          startDate: new Date(),
          creditsIncluded: 850,
          amount: 99.0,
          currency: 'USD',
          nextBillingDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
        },
      },
    },
  });

  console.log('✅ Created test users');

  // Grant initial credits
  console.log('Granting initial credits...');

  await prisma.creditTransaction.create({
    data: {
      userId: freeUser.id,
      amount: 3,
      type: 'GRANT',
      description: 'Welcome bonus - FREE plan',
      balanceAfter: 3,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: starterUser.id,
      amount: 40,
      type: 'PURCHASE',
      description: 'Monthly credits - STARTER plan',
      balanceAfter: 40,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: proUser.id,
      amount: 120,
      type: 'PURCHASE',
      description: 'Monthly credits - PROFESSIONAL plan',
      balanceAfter: 120,
    },
  });

  await prisma.creditTransaction.create({
    data: {
      userId: adminUser.id,
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
      userId: proUser.id,
      originalUrl: 's3://palmar-bg-images/sample/portrait-original.jpg',
      processedSmallUrl: 's3://palmar-bg-images/sample/portrait-512.png',
      processedHdUrl: 's3://palmar-bg-images/sample/portrait-1920.png',
      processedUltraHdUrl: 's3://palmar-bg-images/sample/portrait-3840.png',
      fileSize: 2457600, // ~2.4MB
      width: 1920,
      height: 2560,
      mimeType: 'image/jpeg',
      status: 'COMPLETED',
      backgroundType: 'TRANSPARENT',
      creditsUsed: 1,
      processingTime: 4.5,
    },
  });

  await prisma.image.create({
    data: {
      userId: proUser.id,
      originalUrl: 's3://palmar-bg-images/sample/product-original.jpg',
      processedSmallUrl: 's3://palmar-bg-images/sample/product-512.png',
      processedHdUrl: 's3://palmar-bg-images/sample/product-1920.png',
      fileSize: 1843200, // ~1.8MB
      width: 1500,
      height: 1500,
      mimeType: 'image/jpeg',
      status: 'COMPLETED',
      backgroundType: 'SOLID',
      solidColor: '#FFFFFF',
      creditsUsed: 1,
      processingTime: 3.2,
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
