# Quick Fix Script - PowerShell
# This script resolves common issues by cleaning and restarting services

Write-Host "🔧 Running quick fix..." -ForegroundColor Green
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Stop all services
Write-Host "🛑 Stopping all services..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml down
Write-Host "✅ Services stopped" -ForegroundColor Green

# Clean cache and build artifacts
Write-Host ""
Write-Host "🧹 Cleaning cache..." -ForegroundColor Cyan
if (Test-Path "apps\web\node_modules\.vite") {
    Remove-Item -Recurse -Force "apps\web\node_modules\.vite"
    Write-Host "   Removed web/.vite cache" -ForegroundColor Gray
}
if (Test-Path "apps\web\dist") {
    Remove-Item -Recurse -Force "apps\web\dist"
    Write-Host "   Removed web/dist" -ForegroundColor Gray
}
if (Test-Path "apps\api\dist") {
    Remove-Item -Recurse -Force "apps\api\dist"
    Write-Host "   Removed api/dist" -ForegroundColor Gray
}
if (Test-Path "apps\api\node_modules\.cache") {
    Remove-Item -Recurse -Force "apps\api\node_modules\.cache"
    Write-Host "   Removed api cache" -ForegroundColor Gray
}
Write-Host "✅ Cache cleaned" -ForegroundColor Green

# Reinstall dependencies
Write-Host ""
Write-Host "📦 Checking and installing dependencies..." -ForegroundColor Cyan

Write-Host "   Installing web dependencies..." -ForegroundColor Gray
Set-Location "apps\web"
npm install --silent
Set-Location $projectRoot

Write-Host "   Installing API dependencies..." -ForegroundColor Gray
Set-Location "apps\api"
npm install --silent
Set-Location $projectRoot

Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Regenerate Prisma client
Write-Host ""
Write-Host "🗄️  Regenerating database client..." -ForegroundColor Cyan
Set-Location "packages\database"
npx prisma generate --silent
Set-Location $projectRoot
Write-Host "✅ Database client regenerated" -ForegroundColor Green

# Create .env files if they don't exist
Write-Host ""
Write-Host "📝 Checking environment files..." -ForegroundColor Cyan

if (-not (Test-Path "apps\web\.env")) {
    Copy-Item "apps\web\.env.example" "apps\web\.env"
    Write-Host "   Created apps\web\.env from example" -ForegroundColor Gray
} else {
    Write-Host "   apps\web\.env already exists" -ForegroundColor Gray
}

if (-not (Test-Path "apps\api\.env")) {
    Copy-Item "apps\api\.env.example" "apps\api\.env"
    Write-Host "   Created apps\api\.env from example" -ForegroundColor Gray
} else {
    Write-Host "   apps\api\.env already exists" -ForegroundColor Gray
}

Write-Host "✅ Environment files ready" -ForegroundColor Green

# Start services
Write-Host ""
Write-Host "🚀 Starting Docker services..." -ForegroundColor Cyan
docker-compose -f docker-compose.dev.yml up -d postgres redis minio minio-setup
Write-Host "✅ Docker services started" -ForegroundColor Green

Write-Host ""
Write-Host "⏳ Waiting for services to be ready (15 seconds)..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "✅ Quick fix complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Run health check: .\scripts\health-check.ps1" -ForegroundColor Yellow
Write-Host "   2. Start API: cd apps\api && npm run dev" -ForegroundColor Yellow
Write-Host "   3. Start Web: cd apps\web && npm run dev" -ForegroundColor Yellow
Write-Host ""
