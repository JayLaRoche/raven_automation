# Raven Shop Automation - Production Deployment Script
# This script builds and deploys the application using Docker Compose

param(
    [switch]$Build,
    [switch]$Stop,
    [switch]$Logs,
    [switch]$Status,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Raven Shop Automation - Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env.production exists
if (-not (Test-Path ".env.production")) {
    Write-Host "[ERROR] .env.production file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.production.example to .env.production and configure it." -ForegroundColor Yellow
    exit 1
}

# Function to check Docker
function Test-Docker {
    try {
        docker --version | Out-Null
        docker-compose --version | Out-Null
        return $true
    } catch {
        Write-Host "[ERROR] Docker or Docker Compose not found!" -ForegroundColor Red
        Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        return $false
    }
}

# Stop containers
if ($Stop) {
    Write-Host "[STEP] Stopping production containers..." -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml down
    Write-Host "[OK] Containers stopped" -ForegroundColor Green
    exit 0
}

# Show logs
if ($Logs) {
    Write-Host "[STEP] Showing container logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml logs -f
    exit 0
}

# Show status
if ($Status) {
    Write-Host "[STEP] Container status:" -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml ps
    Write-Host ""
    Write-Host "[STEP] Health check:" -ForegroundColor Yellow
    try {
        $response = Invoke-RestMethod -Uri "http://localhost/api/health" -Method Get
        Write-Host "Backend Health: " -NoNewline
        Write-Host $response.status -ForegroundColor Green
        Write-Host "Database: " -NoNewline
        Write-Host $response.database -ForegroundColor Green
    } catch {
        Write-Host "Backend not responding" -ForegroundColor Red
    }
    exit 0
}

# Clean volumes and rebuild
if ($Clean) {
    Write-Host "[WARNING] This will remove all containers, volumes, and data!" -ForegroundColor Red
    $confirm = Read-Host "Type 'yes' to continue"
    if ($confirm -eq "yes") {
        Write-Host "[STEP] Cleaning up..." -ForegroundColor Yellow
        docker-compose -f docker-compose.prod.yml down -v
        Write-Host "[OK] Cleanup complete" -ForegroundColor Green
    } else {
        Write-Host "[CANCELLED]" -ForegroundColor Yellow
    }
    exit 0
}

# Check Docker is available
if (-not (Test-Docker)) {
    exit 1
}

# Build and deploy
Write-Host "[STEP 1/5] Checking environment..." -ForegroundColor Yellow
Write-Host "[OK] .env.production found" -ForegroundColor Green
Write-Host "[OK] Docker available" -ForegroundColor Green

if ($Build) {
    Write-Host ""
    Write-Host "[STEP 2/5] Building Docker images (this may take a few minutes)..." -ForegroundColor Yellow
    docker-compose -f docker-compose.prod.yml build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Build failed!" -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Images built successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "[STEP 3/5] Stopping old containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml down
Write-Host "[OK] Old containers stopped" -ForegroundColor Green

Write-Host ""
Write-Host "[STEP 4/5] Starting production containers..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to start containers!" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Containers started" -ForegroundColor Green

Write-Host ""
Write-Host "[STEP 5/5] Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check health
$maxAttempts = 30
$attempt = 0
$healthy = $false

while ($attempt -lt $maxAttempts -and -not $healthy) {
    $attempt++
    try {
        $response = Invoke-RestMethod -Uri "http://localhost/api/health" -Method Get -TimeoutSec 2
        if ($response.status -eq "healthy") {
            $healthy = $true
            Write-Host "[OK] Application is healthy!" -ForegroundColor Green
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Cyan
            Write-Host "Deployment Complete!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Cyan
            Write-Host "Frontend: http://localhost" -ForegroundColor White
            Write-Host "API:      http://localhost/api" -ForegroundColor White
            Write-Host "Health:   http://localhost/api/health" -ForegroundColor White
            Write-Host ""
            Write-Host "View logs: .\deploy.ps1 -Logs" -ForegroundColor Yellow
            Write-Host "Check status: .\deploy.ps1 -Status" -ForegroundColor Yellow
            Write-Host "Stop: .\deploy.ps1 -Stop" -ForegroundColor Yellow
            break
        }
    } catch {
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 2
    }
}

if (-not $healthy) {
    Write-Host ""
    Write-Host "[WARNING] Health check timeout - services may still be starting" -ForegroundColor Yellow
    Write-Host "Check logs with: .\deploy.ps1 -Logs" -ForegroundColor Yellow
}
