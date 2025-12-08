# Health Check Script - PowerShell
# This script checks the health of all services

Write-Host "🏥 Running health checks..." -ForegroundColor Green
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

$allHealthy = $true

# Check PostgreSQL
Write-Host "1️⃣  PostgreSQL:" -ForegroundColor Cyan
try {
    docker-compose -f docker-compose.dev.yml exec -T postgres pg_isready -U postgres 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Connected" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "   ❌ Not responding" -ForegroundColor Red
    $allHealthy = $false
}

# Check Redis
Write-Host "2️⃣  Redis:" -ForegroundColor Cyan
try {
    docker-compose -f docker-compose.dev.yml exec -T redis redis-cli ping 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Connected" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "   ❌ Not responding" -ForegroundColor Red
    $allHealthy = $false
}

# Check MinIO
Write-Host "3️⃣  MinIO:" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:9000/minio/health/live" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Connected" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "   ❌ Not responding" -ForegroundColor Red
    $allHealthy = $false
}

# Check API Server
Write-Host "4️⃣  API Server:" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/api/v1/health" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Responding" -ForegroundColor Green
        $data = $response.Content | ConvertFrom-Json
        Write-Host "      Status: $($data.status)" -ForegroundColor Gray
    } else {
        Write-Host "   ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "   ❌ Not responding (Is it running? Run: cd apps\api && npm run dev)" -ForegroundColor Red
    $allHealthy = $false
}

# Check Web Frontend
Write-Host "5️⃣  Web Frontend:" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Responding" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Not responding" -ForegroundColor Red
        $allHealthy = $false
    }
} catch {
    Write-Host "   ❌ Not responding (Is it running? Run: cd apps\web && npm run dev)" -ForegroundColor Red
    $allHealthy = $false
}

Write-Host ""
if ($allHealthy) {
    Write-Host "✅ All services are healthy!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some services are not healthy. Check the output above." -ForegroundColor Yellow
}
Write-Host ""
