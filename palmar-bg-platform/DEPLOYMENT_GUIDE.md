# Palmar Professional - Deployment Guide

Complete guide for deploying the Palmar Professional platform in development and production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Database Management](#database-management)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Docker**: 24.0+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 2.20+ (usually included with Docker Desktop)
- **Git**: For cloning the repository
- **(Optional) Node.js 20+**: For local development without Docker
- **(Optional) Python 3.11+**: For local development without Docker

### System Requirements

**Minimum** (Development):
- 8GB RAM
- 4 CPU cores
- 20GB disk space

**Recommended** (Production):
- 16GB+ RAM
- 8+ CPU cores
- 100GB+ SSD storage
- Dedicated GPU (for faster AI processing)

---

## Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd palmar-bg-platform
```

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your preferences (default values work for local dev)
nano .env
```

### 3. Start Development Stack

```bash
# Start all services with hot reload
docker-compose -f docker-compose.dev.yml up

# Or start in background
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec api npx prisma migrate deploy

# Seed test data
docker-compose -f docker-compose.dev.yml exec api npx prisma db seed
```

### 5. Verify Services

- **Frontend**: http://localhost:3000
- **API**: http://localhost:3001/health
- **Worker**: http://localhost:8000/health
- **MinIO Console**: http://localhost:9001 (minioadmin / minioadmin)

### 6. Test Accounts

After seeding:

| Email | Password | Plan | Credits |
|-------|----------|------|---------|
| free@test.com | password123 | FREE | 3 |
| starter@test.com | password123 | STARTER | 40 |
| pro@test.com | password123 | PROFESSIONAL | 120 |
| admin@palmar.com | password123 | ENTERPRISE | 850 |

### 7. Stop Services

```bash
# Stop all services
docker-compose -f docker-compose.dev.yml down

# Stop and remove volumes (CAUTION: deletes all data)
docker-compose -f docker-compose.dev.yml down -v
```

---

## Production Deployment

### 1. Server Setup

**Recommended**: Ubuntu 22.04 LTS or similar Linux distribution

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Enable Docker on boot
sudo systemctl enable docker
sudo systemctl start docker
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone <repository-url> palmar
cd palmar
```

### 3. Production Environment Variables

```bash
# Copy template
sudo cp .env.example .env

# Edit with production values
sudo nano .env
```

**Critical Settings**:

```bash
# Database
DATABASE_URL=postgresql://prod_user:STRONG_PASSWORD@postgres:5432/palmar_bg

# Redis
REDIS_PASSWORD=STRONG_REDIS_PASSWORD

# JWT Secrets (generate with: openssl rand -base64 32)
JWT_SECRET=<generated-secret-key>
JWT_REFRESH_SECRET=<generated-refresh-key>

# S3/MinIO
S3_ENDPOINT=https://s3.your-domain.com
S3_ACCESS_KEY=<production-access-key>
S3_SECRET_KEY=<production-secret-key>
S3_BUCKET=palmar-bg-production

# API
NODE_ENV=production
API_BASE_URL=https://api.your-domain.com

# Frontend
VITE_API_BASE_URL=https://api.your-domain.com/api
```

### 4. Build Images

```bash
# Build all services
sudo docker-compose build

# Or build specific service
sudo docker-compose build api
```

### 5. Start Production Stack

```bash
# Start services
sudo docker-compose up -d

# Check status
sudo docker-compose ps

# View logs
sudo docker-compose logs -f
```

### 6. Run Database Migrations

```bash
# Run migrations (DO NOT seed in production)
sudo docker-compose exec api npx prisma migrate deploy
```

### 7. Set Up Reverse Proxy (Nginx)

**Install Nginx**:

```bash
sudo apt install nginx certbot python3-certbot-nginx
```

**Configure Nginx** (`/etc/nginx/sites-available/palmar`):

```nginx
# Frontend
server {
    listen 80;
    server_name app.your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# API
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;

        # Rate limiting
        limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
        limit_req zone=api_limit burst=20 nodelay;
    }
}

# MinIO/S3
server {
    listen 80;
    server_name s3.your-domain.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Large file uploads
        client_max_body_size 25M;
    }
}
```

**Enable site**:

```bash
sudo ln -s /etc/nginx/sites-available/palmar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Get SSL certificates**:

```bash
sudo certbot --nginx -d app.your-domain.com -d api.your-domain.com -d s3.your-domain.com
```

### 8. Set Up Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 9. Set Up Automatic Backups

**Database Backup Script** (`/opt/palmar/scripts/backup-db.sh`):

```bash
#!/bin/bash
BACKUP_DIR="/opt/palmar/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/palmar_db_$DATE.sql"

mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U postgres palmar_bg > $BACKUP_FILE

gzip $BACKUP_FILE

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

**Cron job** (`crontab -e`):

```cron
# Daily backup at 2 AM
0 2 * * * /opt/palmar/scripts/backup-db.sh >> /var/log/palmar-backup.log 2>&1
```

---

## Database Management

### Migrations

```bash
# Production: Apply migrations
docker-compose exec api npx prisma migrate deploy

# Development: Create new migration
docker-compose -f docker-compose.dev.yml exec api npx prisma migrate dev --name <migration_name>

# View migration status
docker-compose exec api npx prisma migrate status
```

### Database Studio (Development Only)

```bash
cd packages/database
npx prisma studio
```

Access at: http://localhost:5555

### Reset Database (Development Only)

```bash
docker-compose -f docker-compose.dev.yml exec api npx prisma migrate reset
```

### Restore from Backup

```bash
# Stop services
docker-compose down

# Restore database
gunzip -c /opt/palmar/backups/palmar_db_20251130_020000.sql.gz | \
  docker-compose exec -T postgres psql -U postgres -d palmar_bg

# Start services
docker-compose up -d
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# API health
curl http://localhost:3001/health

# Worker health
curl http://localhost:8000/health

# Redis
docker-compose exec redis redis-cli ping

# PostgreSQL
docker-compose exec postgres pg_isready
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f celery
docker-compose logs -f worker

# Last 100 lines
docker-compose logs --tail=100 api
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df

# Clean up unused images
docker system prune -a
```

### Update Deployment

```bash
# Pull latest code
cd /opt/palmar
sudo git pull

# Rebuild and restart
sudo docker-compose build
sudo docker-compose up -d

# Run migrations
sudo docker-compose exec api npx prisma migrate deploy
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
docker-compose restart celery
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs <service-name>

# Check container status
docker-compose ps

# Recreate container
docker-compose up -d --force-recreate <service-name>
```

### Database Connection Issues

```bash
# Verify PostgreSQL is running
docker-compose exec postgres pg_isready

# Check connection string
docker-compose exec api printenv DATABASE_URL

# Test connection
docker-compose exec postgres psql -U postgres -d palmar_bg -c "SELECT 1;"
```

### Redis Connection Issues

```bash
# Test Redis
docker-compose exec redis redis-cli ping

# Check connections
docker-compose exec redis redis-cli INFO clients
```

### MinIO/S3 Issues

```bash
# Check MinIO logs
docker-compose logs minio

# Access MinIO console
# http://localhost:9001

# Create bucket manually
docker-compose exec minio-setup mc mb myminio/palmar-bg-images
```

### Image Processing Fails

```bash
# Check Celery worker logs
docker-compose logs celery

# Check model files
docker-compose exec celery ls -la ~/.u2net/

# Check disk space
df -h

# Check memory
free -h
```

### Frontend Build Fails

```bash
# Rebuild with no cache
docker-compose build --no-cache web

# Check build logs
docker-compose logs web
```

### High Memory Usage

```bash
# Check resource limits in docker-compose.yml
# Restart Celery with reduced concurrency
docker-compose exec celery celery -A app.celery_app control pool_shrink 1
```

---

## Performance Optimization

### Database

```bash
# Create indexes for slow queries
# Run EXPLAIN ANALYZE on slow queries
docker-compose exec postgres psql -U postgres -d palmar_bg

# Vacuum database
VACUUM ANALYZE;
```

### Redis

```bash
# Check memory usage
docker-compose exec redis redis-cli INFO memory

# Set max memory policy
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Celery

- Adjust concurrency in docker-compose.yml
- Use separate queues for different task types
- Monitor queue length: `docker-compose exec celery celery -A app.celery_app inspect active`

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong JWT secrets
- [ ] Enable HTTPS with valid SSL certificates
- [ ] Configure firewall (UFW/iptables)
- [ ] Set up fail2ban for SSH protection
- [ ] Enable Redis authentication
- [ ] Restrict PostgreSQL network access
- [ ] Regular security updates (`apt update && apt upgrade`)
- [ ] Monitor logs for suspicious activity
- [ ] Set up automated backups
- [ ] Test disaster recovery procedures

---

## Support

For issues or questions:
- Check logs first
- Review error messages
- Consult documentation
- Contact support: support@palmar.com

---

**Last Updated**: 2025-11-30
**Version**: 2.0.0
