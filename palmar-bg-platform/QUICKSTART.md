# Quick Start Guide - Palmar Professional

Get up and running with the Palmar Professional platform in under 5 minutes!

## 🚀 30-Second Start

```bash
# 1. Clone and navigate
git clone <repository-url> && cd palmar-bg-platform

# 2. Copy environment variables
cp .env.example .env

# 3. Start everything
docker-compose -f docker-compose.dev.yml up -d

# 4. Initialize database
docker-compose -f docker-compose.dev.yml exec api npx prisma migrate deploy
docker-compose -f docker-compose.dev.yml exec api npx prisma db seed

# 5. Open browser
# Frontend: http://localhost:3000
# API: http://localhost:3001/health
```

## 📦 What You Get

After running the quick start, you'll have:

- ✅ **Frontend**: React app at http://localhost:3000
- ✅ **API**: Node.js REST API at http://localhost:3001
- ✅ **Worker**: Python AI worker at http://localhost:8000
- ✅ **Database**: PostgreSQL with test data
- ✅ **Queue**: Redis for job processing
- ✅ **Storage**: MinIO (S3-compatible) at http://localhost:9001

## 🔐 Test Accounts

Login with these accounts:

| Email | Password | Credits |
|-------|----------|---------|
| free@test.com | password123 | 3 |
| pro@test.com | password123 | 120 |
| admin@palmar.com | password123 | 850 |

## 🎯 Try It Out

### 1. Create Account or Login

Go to http://localhost:3000 and:
- Click "Get Started" to register
- Or use a test account above

### 2. Upload an Image

1. Click "Try It Free" or go to Editor
2. Drag and drop an image (JPG/PNG/WEBP, max 10MB)
3. Wait 3-8 seconds for AI processing
4. See the background removed!

### 3. Customize Background

- Choose "Transparent" for PNG with no background
- Choose "Solid Color" and pick a color
- Click "Apply Background"

### 4. Download Result

- Click "Download Image" to save processed image
- Check your dashboard to see all images

## 🛠️ Development Commands

```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down

# Restart a service
docker-compose -f docker-compose.dev.yml restart api

# Access database
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d palmar_bg

# Open Prisma Studio
cd packages/database && npx prisma studio

# Check service status
docker-compose -f docker-compose.dev.yml ps
```

## 📚 Next Steps

- **Full Documentation**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **API Docs**: http://localhost:3001/api-docs (coming soon)
- **Architecture**: See [PHASE_2_PROGRESS.md](./PHASE_2_PROGRESS.md)

## ❌ Troubleshooting

**Services won't start?**
```bash
# Check Docker is running
docker ps

# Check logs for errors
docker-compose -f docker-compose.dev.yml logs
```

**Database errors?**
```bash
# Reset database (CAUTION: deletes all data)
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
docker-compose -f docker-compose.dev.yml exec api npx prisma migrate deploy
docker-compose -f docker-compose.dev.yml exec api npx prisma db seed
```

**Port already in use?**
```bash
# Change ports in docker-compose.dev.yml
# For example: "3000:80" → "3002:80"
```

## 🆘 Need Help?

- Check the [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions
- View logs: `docker-compose -f docker-compose.dev.yml logs -f`
- Contact: support@palmar.com

---

**Happy background removing!** 🎨
