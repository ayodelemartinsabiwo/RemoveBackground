# Start All Services - PowerShell Script
# This script starts all required services for the Palmar Background Remover Platform

Write-Host "🚀 Starting Palmar Background Remover Platform..." -ForegroundColor Green
Write-Host ""

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Cyan
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Navigate to project root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Start Docker services
Write-Host ""
Write-Host "📦 Starting Docker services (PostgreSQL, Redis, MinIO)..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml up -d postgres redis minio minio-setup

# Wait for services to be ready
Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Check PostgreSQL
Write-Host "🔍 Checking PostgreSQL..." -ForegroundColor Cyan
$retries = 0
$maxRetries = 30
while ($retries -lt $maxRetries) {
    try {
        docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U postgres 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ PostgreSQL is ready" -ForegroundColor Green
            break
        }
    } catch {}

    if ($retries -eq $maxRetries - 1) {
        Write-Host "❌ PostgreSQL failed to start" -ForegroundColor Red
        exit 1
    }

    Write-Host "   Waiting for PostgreSQL... ($retries/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    $retries++
}

# Check Redis
Write-Host "🔍 Checking Redis..." -ForegroundColor Cyan
$retries = 0
while ($retries -lt $maxRetries) {
    try {
        docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Redis is ready" -ForegroundColor Green
            break
        }
    } catch {}

    if ($retries -eq $maxRetries - 1) {
        Write-Host "❌ Redis failed to start" -ForegroundColor Red
        exit 1
    }

    Write-Host "   Waiting for Redis... ($retries/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    $retries++
}

# Check MinIO
Write-Host "🔍 Checking MinIO..." -ForegroundColor Cyan
$retries = 0
while ($retries -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ MinIO is ready" -ForegroundColor Green
            break
        }
    } catch {}

    if ($retries -eq $maxRetries - 1) {
        Write-Host "❌ MinIO failed to start" -ForegroundColor Red
        exit 1
    }

    Write-Host "   Waiting for MinIO... ($retries/$maxRetries)" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    $retries++
}

# Setup database
Write-Host ""
Write-Host "🗄️  Setting up database..." -ForegroundColor Cyan
Set-Location "$projectRoot\packages\database"
npx prisma generate
npx prisma migrate dev --name init
Set-Location $projectRoot
Write-Host "✅ Database setup complete" -ForegroundColor Green

Write-Host ""
Write-Host "✅ All Docker services started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service URLs:" -ForegroundColor Cyan
Write-Host "   PostgreSQL:   localhost:5432" -ForegroundColor White
Write-Host "   Redis:        localhost:6379" -ForegroundColor White
Write-Host "   MinIO API:    http://localhost:9000" -ForegroundColor White
Write-Host "   MinIO Admin:  http://localhost:9001 (minioadmin/minioadmin)" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Open a new terminal and run: cd apps\api && npm run dev" -ForegroundColor Yellow
Write-Host "   2. Open another terminal and run: cd apps\web && npm run dev" -ForegroundColor Yellow
Write-Host "   3. Open browser at: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "🛑 To stop all services: docker-compose -f docker-compose.dev.yml down" -ForegroundColor Red
Write-Host ""
