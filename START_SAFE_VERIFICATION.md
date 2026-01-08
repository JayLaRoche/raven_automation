# START_SAFE.PS1 - Recovery Script Verification

**Date:** January 2026  
**Status:** ✓ VERIFIED AND READY TO USE

---

## What `start_safe.ps1` Does

This PowerShell recovery script ensures clean startup of the Raven Shop Automation backend server:

1. **Kills Stray Processes** - Terminates Python/Node processes preventing port conflicts
2. **Verifies Directories** - Ensures `backend/static/frames/` and required directories exist
3. **Syntax Validation** - Checks `main.py` and `routers/drawings.py` for Python syntax errors
4. **Docker Check** - Ensures PostgreSQL container is running (starts if needed)
5. **Starts Backend** - Launches FastAPI server with auto-reload on port 8000

---

## Verification Results

### ✓ Directory Structure
- `backend/static/` - **EXISTS**
- `backend/static/frames/` - **EXISTS**
- Frame images - **67 PNG files present** (series-* thumbnails and components)

### ✓ Python Syntax
- `backend/main.py` - **VALID** (no syntax errors)
- `backend/routers/drawings.py` - **VALID** (no syntax errors)

### ✓ Import Testing
- Application imports - **ALL OK**
- Database initialization - **SUCCESSFUL**
- Static file mounts - **CONFIGURED**
- Asset mounts - **CONFIGURED**

### ✓ System Requirements
- Docker - **INSTALLED** (v2.40.3)
- Docker Compose - **AVAILABLE**
- Python - **CONFIGURED**
- PostgreSQL - **Ready** (via docker-compose)

---

## How to Use

### From Windows PowerShell:
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation
.\start_safe.ps1
```

### Expected Output
```
================================================================
  RAVEN SHOP AUTOMATION - SAFE STARTUP
================================================================

PHASE 1: Terminating Stray Processes
  ✓ No Python processes running
  ✓ No Node processes running
  ⏳ Waiting for cleanup (3 seconds)...

PHASE 2: Verifying Directory Structure
  ✓ Static directory OK: C:\Users\larochej3\Desktop\raven-shop-automation\backend\static
  ✓ Frames directory OK: C:\Users\larochej3\Desktop\raven-shop-automation\backend\static\frames
  ✓ Frame images present: 67 files

PHASE 3: Syntax Validation
  Checking main.py...
  ✓ main.py syntax valid
  Checking drawings.py...
  ✓ drawings.py syntax valid
  Checking imports...
  ✓ All imports successful

PHASE 4: Docker & PostgreSQL Check
  ✓ Docker available: Docker version 27.x.x
  ✓ PostgreSQL container running

PHASE 5: Starting Backend Server
================================================================
Starting FastAPI Backend on http://0.0.0.0:8000
================================================================

INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

## What Gets Fixed

| Issue | Root Cause | How start_safe.ps1 Fixes It |
|-------|-----------|------|
| Address already in use | Python/Node process still running from previous crash | Kills all python* and node* processes |
| Frame images not found | Directory structure incomplete or missing | Creates `static/frames/` if missing |
| Syntax errors prevent startup | Python file has invalid syntax | Validates both main.py and drawings.py |
| Port 8000 won't bind | Lingering process on port 8000 | Kill process + 3-second wait before restart |
| PostgreSQL unavailable | Database container not running | Automatically starts postgres via docker-compose |
| Broken imports | Missing dependencies or import errors | Tests actual import of FastAPI app |

---

## Frontend Configuration

While `start_safe.ps1` only starts the backend, the frontend is automatically configured to work with it:

1. **Vite Proxy** - `frontend/vite.config.js` forwards `/api` requests to `http://localhost:8000`
2. **Port 3000** - Start frontend separately with `npm run dev`
3. **Automatic Proxying** - No need to manually change API URLs

---

## Troubleshooting

### If "Address already in use" still occurs:
```powershell
# Find what's on port 8000
netstat -ano | findstr ":8000"

# Kill by PID (e.g., PID 1234)
taskkill /PID 1234 /F
```

### If Docker isn't running:
- Install Docker Desktop: https://www.docker.com/products/docker-desktop
- Ensure Docker daemon is running before executing the script

### If PostgreSQL won't start:
```powershell
# Check Docker containers
docker ps -a

# Start manually
docker-compose up postgres -d
```

### If syntax errors still appear:
1. Check `backend/main.py` for Python syntax
2. Run: `python -m py_compile backend/main.py`
3. Fix any reported errors before retrying

---

## Files Modified/Created

- ✓ `start_safe.ps1` - Safe startup recovery script (simplified for PowerShell 5.1+)
- ✓ `backend/static/frames/` - Verified 67 frame images present
- ✓ All Python syntax - Validated and passing

---

## Next Steps

1. **First Time Running:**
   ```powershell
   .\start_safe.ps1
   # Waits for "Application startup complete" message
   ```

2. **In Another Terminal - Start Frontend:**
   ```powershell
   cd frontend
   npm install  # First time only
   npm run dev
   # Visit http://localhost:3000
   ```

3. **Verify Integration:**
   - Open http://localhost:3000
   - Test frame series dropdown (should show images)
   - Generate a test drawing

---

## Script Architecture

The script uses PowerShell 5.1+ compatible commands:
- `Get-Process` / `Stop-Process` - Kill processes
- `Test-Path` / `New-Item` - Verify/create directories
- `python -m py_compile` - Syntax validation
- `docker` / `docker-compose` - Container management

All output uses color-coded feedback:
- 🟢 Green = Success
- 🟡 Yellow = Warning (non-blocking)
- 🔴 Red = Error (blocking)
- 🔵 Cyan = Information

---

**Status: READY FOR PRODUCTION USE** ✓
