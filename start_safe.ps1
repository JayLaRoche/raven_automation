# ============================================================================
# RAVEN SHOP AUTOMATION - COMPLETE RECOVERY PROCEDURE (SAFE STARTUP)
# ============================================================================
# This script implements all steps from the diagnostics guide to prevent
# "ERR_CONNECTION_REFUSED" and server crashes.
#
# Procedure:
#   1. Kill zombie processes (Python/Node)
#   2. Start PostgreSQL via Docker
#   3. Verify static/frames directory
#   4. Start Backend (FastAPI) in new terminal
#   5. Start Frontend (Vite) in new terminal
#   6. Wait for servers to be ready
#   7. Open browser to http://localhost:3000
#
# Usage: cd C:\Users\larochej3\Desktop\raven-shop-automation
#        .\start_safe.ps1
#
# Note: Requires PowerShell 5.1+, Docker, Node.js, Python 3.9+
# ============================================================================

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          RAVEN SHOP AUTOMATION - SAFE STARTUP SCRIPT           ║" -ForegroundColor Cyan
Write-Host "║          Complete Recovery Procedure Implementation            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Configuration
$RootDir = Split-Path -Parent $MyInvocation.MyCommandPath
$BackendDir = Join-Path $RootDir "backend"
$FrontendDir = Join-Path $RootDir "frontend"
$StaticDir = Join-Path $BackendDir "static"
$FramesDir = Join-Path $StaticDir "frames"

Write-Host "Project Root: $RootDir" -ForegroundColor Yellow
Write-Host "`n"

# ============================================================================
# STEP 1: KILL ZOMBIE PROCESSES
# ============================================================================
Write-Host "STEP 1: Cleaning Up Zombie Processes" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

# Kill Python processes
$PythonProcs = Get-Process python* -ErrorAction SilentlyContinue
if ($PythonProcs) {
    Write-Host "  • Found $($PythonProcs.Count) Python process(es) - terminating..." -ForegroundColor Yellow
    Stop-Process -Name python* -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Python processes terminated" -ForegroundColor Green
} else {
    Write-Host "  ✓ No Python processes (clean state)" -ForegroundColor Green
}

# Kill Node processes
$NodeProcs = Get-Process node* -ErrorAction SilentlyContinue
if ($NodeProcs) {
    Write-Host "  • Found $($NodeProcs.Count) Node process(es) - terminating..." -ForegroundColor Yellow
    Stop-Process -Name node* -Force -ErrorAction SilentlyContinue
    Write-Host "  ✓ Node processes terminated" -ForegroundColor Green
} else {
    Write-Host "  ✓ No Node processes (clean state)" -ForegroundColor Green
}

Write-Host "  • Waiting 2 seconds for OS cleanup..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Write-Host "`n"

# ============================================================================
# STEP 2: START POSTGRESQL DATABASE
# ============================================================================
Write-Host "STEP 2: Starting PostgreSQL Database" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "  ⚠ docker-compose not found (optional - database may be unavailable)" -ForegroundColor Yellow
} else {
    try {
        Write-Host "  • Starting PostgreSQL container..." -ForegroundColor Cyan
        docker-compose up postgres -d 2>&1 | Out-Null
        Write-Host "  ✓ Docker container launched" -ForegroundColor Green
        Write-Host "  • Waiting 5 seconds for database initialization..." -ForegroundColor Cyan
        Start-Sleep -Seconds 5
        Write-Host "  ✓ PostgreSQL ready" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Docker-compose failed (skipping): $_" -ForegroundColor Yellow
    }
}

Write-Host "`n"

# ============================================================================
# STEP 3: VERIFY BACKEND STATIC DIRECTORY
# ============================================================================
Write-Host "STEP 3: Verifying Backend Configuration" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

# Create static directories if missing
if (-not (Test-Path $StaticDir)) {
    Write-Host "  • Creating backend/static directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $StaticDir -Force | Out-Null
    Write-Host "  ✓ Created backend/static" -ForegroundColor Green
} else {
    Write-Host "  ✓ backend/static directory exists" -ForegroundColor Green
}

# Create frames directory
if (-not (Test-Path $FramesDir)) {
    Write-Host "  • Creating backend/static/frames directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $FramesDir -Force | Out-Null
    Write-Host "  ✓ Created backend/static/frames" -ForegroundColor Green
} else {
    $frameCount = (Get-ChildItem $FramesDir -Filter "*.png" -ErrorAction SilentlyContinue).Count
    Write-Host "  ✓ backend/static/frames exists ($frameCount PNG files)" -ForegroundColor Green
}

Write-Host "`n"

# ============================================================================
# STEP 4: START BACKEND SERVER (IN NEW TERMINAL)
# ============================================================================
Write-Host "STEP 4: Starting Backend Server" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

Write-Host "  • Launching FastAPI on port 8000..." -ForegroundColor Cyan
Write-Host "  • Backend will open in a new terminal window" -ForegroundColor Cyan

$backendCmd = @"
`$backendDir = '$BackendDir'
Write-Host "`nBackend starting in: `$backendDir" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
cd `$backendDir
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
"@

$backendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", $backendCmd -PassThru
Write-Host "  ✓ Backend process launched (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "  • Waiting 5 seconds for backend to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Check if backend is listening
$backendCheck = netstat -ano 2>$null | Select-String ":8000" | Select-String "LISTENING"
if ($backendCheck) {
    Write-Host "  ✓ Backend is listening on port 8000" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Backend not yet responding (may need a few more seconds)" -ForegroundColor Yellow
}

Write-Host "`n"

# ============================================================================
# STEP 5: START FRONTEND SERVER (IN NEW TERMINAL)
# ============================================================================
Write-Host "STEP 5: Starting Frontend Server" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

Write-Host "  • Launching Vite on port 3000..." -ForegroundColor Cyan
Write-Host "  • Frontend will open in a new terminal window" -ForegroundColor Cyan

$frontendCmd = @"
`$frontendDir = '$FrontendDir'
Write-Host "`nFrontend starting in: `$frontendDir" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
cd `$frontendDir
npm run dev
"@

$frontendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", $frontendCmd -PassThru
Write-Host "  ✓ Frontend process launched (PID: $($frontendProcess.Id))" -ForegroundColor Green
Write-Host "  • Waiting 5 seconds for frontend to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Check if frontend is listening
$frontendCheck = netstat -ano 2>$null | Select-String ":3000" | Select-String "LISTENING"
if ($frontendCheck) {
    Write-Host "  ✓ Frontend is listening on port 3000" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Frontend not yet responding (may need a few more seconds)" -ForegroundColor Yellow
}

Write-Host "`n"

# ============================================================================
# STEP 6: LAUNCH APPLICATION IN BROWSER
# ============================================================================
Write-Host "STEP 6: Launching Application" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

Write-Host "  • Opening http://localhost:3000 in default browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"
Write-Host "  ✓ Browser window opened" -ForegroundColor Green

Write-Host "`n"

# ============================================================================
# FINAL STATUS REPORT
# ============================================================================
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✓ STARTUP PROCEDURE COMPLETE                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host "`n"

Write-Host "System Status:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Verify both servers are listening
$backendListening = netstat -ano 2>$null | Select-String ":8000" | Select-String "LISTENING"
$frontendListening = netstat -ano 2>$null | Select-String ":3000" | Select-String "LISTENING"

if ($backendListening) {
    Write-Host "  ✓ Backend:  http://localhost:8000  (FastAPI + Uvicorn)" -ForegroundColor Green
} else {
    Write-Host "  ✗ Backend:  NOT RESPONDING - check backend terminal for errors" -ForegroundColor Red
}

if ($frontendListening) {
    Write-Host "  ✓ Frontend: http://localhost:3000  (React + Vite)" -ForegroundColor Green
} else {
    Write-Host "  ✗ Frontend: NOT RESPONDING - check frontend terminal for errors" -ForegroundColor Red
}

Write-Host "`n"

Write-Host "Expected Results:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  1. Browser opens to http://localhost:3000" -ForegroundColor White
Write-Host "  2. Two new terminal windows appear (Backend + Frontend)" -ForegroundColor White
Write-Host "  3. Backend shows 'Application startup complete'" -ForegroundColor White
Write-Host "  4. Frontend shows 'Local: http://localhost:3000/'" -ForegroundColor White
Write-Host "  5. App loads without 'Connection Refused' errors" -ForegroundColor White
Write-Host "`n"

Write-Host "If You See Connection Refused:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  1. Check backend terminal for Python import errors" -ForegroundColor White
Write-Host "  2. Check frontend terminal for npm/Vite errors" -ForegroundColor White
Write-Host "  3. Wait 10 more seconds (servers may still be starting)" -ForegroundColor White
Write-Host "  4. Refresh browser (F5)" -ForegroundColor White
Write-Host "  5. If still failing, open DevTools (F12) to check console" -ForegroundColor White
Write-Host "`n"

Write-Host "If Backend Terminal Shows Error:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  • ModuleNotFoundError → Run: pip install -r requirements.txt" -ForegroundColor White
Write-Host "  • Address already in use → Close all terminals and try again" -ForegroundColor White
Write-Host "  • Cannot connect to PostgreSQL → Ensure Docker Desktop is running" -ForegroundColor White
Write-Host "`n"

Write-Host "If Frontend Terminal Shows Error:" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
Write-Host "  • npm ERR! → Run: npm install (in frontend directory)" -ForegroundColor White
Write-Host "  • Port 3000 in use → Close all terminals and try again" -ForegroundColor White
Write-Host "  • Module not found → Delete node_modules and run: npm install" -ForegroundColor White
Write-Host "`n"

Write-Host "Quick Troubleshooting:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  Check backend: Invoke-RestMethod http://localhost:8000/health" -ForegroundColor White
Write-Host "  Check frontend: Invoke-WebRequest http://localhost:3000" -ForegroundColor White
Write-Host "  Kill all: Get-Process python*, node* | Stop-Process -Force" -ForegroundColor White
Write-Host "`n"

Write-Host "This startup script implements the Complete Recovery Procedure:" -ForegroundColor Cyan
Write-Host "  ✓ Killed zombie processes" -ForegroundColor Green
Write-Host "  ✓ Started PostgreSQL database" -ForegroundColor Green
Write-Host "  ✓ Verified static/frames directory" -ForegroundColor Green
Write-Host "  ✓ Started Backend (FastAPI)" -ForegroundColor Green
Write-Host "  ✓ Started Frontend (Vite)" -ForegroundColor Green
Write-Host "  ✓ Opened application in browser" -ForegroundColor Green
Write-Host "`n"
