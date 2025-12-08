# 🚀 QUICK START - Use This Every Time

## Starting the Application

### Option 1: One Command Startup (Recommended)
```powershell
cd C:\RemoveBackground\palmar-bg-platform

# Start Docker services
docker-compose -f docker-compose.dev.yml up -d postgres redis minio minio-setup worker

# Start API (in new window)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\api; npm run dev"

# Start Web (in new window)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd apps\web; npm run dev"
```

### Option 2: Manual Startup
**Terminal 1 - Docker:**
```powershell
cd C:\RemoveBackground\palmar-bg-platform
docker-compose -f docker-compose.dev.yml up -d
```

**Terminal 2 - API:**
```powershell
cd C:\RemoveBackground\palmar-bg-platform\apps\api
npm run dev
```

**Terminal 3 - Web:**
```powershell
cd C:\RemoveBackground\palmar-bg-platform\apps\web
npm run dev
```

---

## Application URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Web App** | **http://localhost:5173** | Main application |
| API | http://localhost:3001 | Backend API |
| API Health | http://localhost:3001/health | Health check |
| MinIO Admin | http://localhost:9001 | Storage admin (minioadmin/minioadmin) |

---

## Quick Health Check

```powershell
cd C:\RemoveBackground\palmar-bg-platform
.\scripts\health-check.ps1
```

**Expected output:**
```
✅ PostgreSQL: Connected
✅ Redis: Connected
✅ MinIO: Connected
✅ API Server: Responding
✅ Web Frontend: Responding
```

---

## Stopping Services

```powershell
# Stop Docker services
docker-compose -f docker-compose.dev.yml down

# Stop Node processes (API & Web)
Stop-Process -Name "node" -Force
```

---

## Common Commands

### Restart Everything
```powershell
# Stop all
docker-compose -f docker-compose.dev.yml down
Stop-Process -Name "node" -Force

# Start Docker
docker-compose -f docker-compose.dev.yml up -d

# Start API & Web
cd apps\api; npm run dev  # Terminal 1
cd apps\web; npm run dev  # Terminal 2
```

### View Logs
```powershell
# Docker logs
docker-compose -f docker-compose.dev.yml logs -f

# Specific service
docker logs palmar-postgres-dev -f
docker logs palmar-redis-dev -f
docker logs palmar-minio-dev -f
docker logs palmar-worker-dev -f
```

### Database Commands
```powershell
cd packages\database

# Generate Prisma client
npx prisma generate

# Run migrations
npx prisma migrate dev

# Open Prisma Studio
npx prisma studio
```

---

## Troubleshooting

### Port 5173 Already in Use
```powershell
# Find process using port 5173
Get-NetTCPConnection -LocalPort 5173 | Select-Object OwningProcess
Stop-Process -Id <PID> -Force
```

### Port 3001 Already in Use
```powershell
# Find process using port 3001
Get-NetTCPConnection -LocalPort 3001 | Select-Object OwningProcess
Stop-Process -Id <PID> -Force
```

### Docker Services Not Starting
```powershell
# Remove all containers and volumes
docker-compose -f docker-compose.dev.yml down -v

# Start fresh
docker-compose -f docker-compose.dev.yml up -d
```

### Web Shows Blank Page
```powershell
# Clear Vite cache
cd apps\web
Remove-Item -Recurse -Force node_modules\.vite
npm run dev
```

---

## Development Workflow

### Making Changes

**Frontend (React/TypeScript):**
1. Edit files in `apps/web/src/`
2. Save
3. Browser auto-refreshes (HMR)

**Backend (Node.js):**
1. Edit files in `apps/api/src/`
2. Save
3. Server auto-restarts (tsx watch)

**Database Schema:**
1. Edit `packages/database/prisma/schema.prisma`
2. Run: `npx prisma migrate dev --name <name>`
3. Client regenerates automatically

---

## Quick Links

- [Complete Fix Documentation](./ALL_ISSUES_RESOLVED.md)
- [Authentication Fix Details](./AUTHENTICATION_FIX_COMPLETE.md)
- [Original Implementation Guide](./IMPLEMENTATION_COMPLETE.md)

---

**Everything is working! Just run the commands above to start. 🎉**
