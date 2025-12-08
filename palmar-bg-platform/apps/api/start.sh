#!/bin/sh
set -e

echo "Generating Prisma Client..."
npx prisma@5.8.0 generate --schema=/app/node_modules/@palmar/database/prisma/schema.prisma

echo "Starting development server..."
npm run dev
