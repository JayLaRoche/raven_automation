# RAVEN SHOP AUTOMATION - STARTUP GUIDE

**Last Updated:** January 6, 2026  
**Status:** Ready to Run ✓

---

## Quick Start (3 Steps)

### 1️⃣ Start Backend Server

**Option A: Double-click Batch File (EASIEST)**
```
Double-click: START_BACKEND.bat
```

**Option B: PowerShell**
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
[OK] Database tables created/verified
[OK] Static files mounted at /static
[OK] Assets mounted at /assets
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✓ **Backend is running!** Leave this window open.

---

### 2️⃣ Start Frontend Server

**In a NEW terminal window/tab**, double-click or run:

```
Double-click: START_FRONTEND.bat
```

OR:

```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

✓ **Frontend is running!** Leave this window open.

---

### 3️⃣ Open Browser

Visit: **http://localhost:3000**

You should see the Raven Shop Automation application!

✓ **All servers running!** Ready to develop.

---

## Verify Everything Works

### Test 1: Backend Responding
```powershell
Invoke-RestMethod "http://localhost:8000/health"
```
Should return: `@{status="healthy"}`

### Test 2: Frame Series Available
```powershell
(Invoke-RestMethod "http://localhost:8000/api/frames/series").series
```
Should show: `80, 86, 65, 135, MD100H, 68, 58, 150, 4518`

### Test 3: Frontend Accessible
Open: `http://localhost:3000`

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│  Browser: http://localhost:3000 (React Vite)    │
└────────────────────┬────────────────────────────┘
                     │
                     │ HTTP Requests
                     │ /api/* proxied to :8000
                     │
┌────────────────────▼────────────────────────────┐
│  Backend: http://localhost:8000 (FastAPI)       │
│  - /api/frames/* - Frame series endpoints       │
│  - /api/drawings/* - Drawing generation         │
│  - /static - Static frame images                │
│  - /assets - Asset files                        │
└────────────────────┬────────────────────────────┘
                     │
                     │ SQL Queries
                     │
┌────────────────────▼────────────────────────────┐
│  Database: PostgreSQL (Docker container)        │
│  - Frame data                                   │
│  - Project data                                 │
│  - Drawing metadata                             │
└─────────────────────────────────────────────────┘
```

---

## File Locations Reference

| Component | Directory | Start Command |
|-----------|-----------|---|
| **Backend** | `backend/` | `python -m uvicorn main:app --host 0.0.0.0 --port 8000` |
| **Frontend** | `frontend/` | `npm run dev` |
| **Database** | PostgreSQL (Docker) | `docker-compose up postgres -d` |
| **Frame Images** | `backend/static/frames/` | 67 PNG files present |
| **Main Config** | `backend/main.py` | FastAPI app definition |
| **Routers** | `backend/routers/` | `frames.py`, `drawings.py` |
| **React App** | `frontend/src/` | React components |

---

## Troubleshooting

### "localhost refused to connect"

**Cause:** Backend server not running or port 8000 not listening

**Fix:**
```powershell
# Check if port 8000 is listening
netstat -an | Select-String "8000" | Where-Object {$_ -match "LISTENING"}

# If not found, start backend:
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### "Cannot GET /"

**Cause:** Accessing backend without API path (e.g., http://localhost:8000)

**Fix:** Frontend should be on port 3000. Backend is on port 8000.
- Frontend: http://localhost:3000 ✓
- Backend: http://localhost:8000/health ✓

### "Port 8000 already in use"

**Cause:** Another process is using port 8000

**Fix:**
```powershell
# Find what's using port 8000
netstat -ano | findstr ":8000"

# Get the PID from the output, then kill it:
taskkill /PID [PID] /F

# Or kill all python processes:
Stop-Process -Name python -Force -ErrorAction SilentlyContinue
```

### Frame images not displaying

**Cause:** Images not in correct location

**Verify:**
```powershell
ls C:\Users\larochej3\Desktop\raven-shop-automation\backend\static\frames\
```

Should show 67 PNG files like `series-86-thumbnail.png`

### CORS errors

**Cause:** Frontend and backend not communicating

**Fix:** Ensure:
1. Backend running on http://0.0.0.0:8000 (NOT 127.0.0.1:8000)
2. Vite proxy configured in `frontend/vite.config.js`
3. CORS enabled in `backend/main.py`

---

## Environment Setup

### Python Dependencies
Installed in `backend/` - see `backend/requirements.txt`

Key packages:
- FastAPI 0.104
- SQLAlchemy 2.1
- Uvicorn 0.24
- Pillow 12.0 (image handling)

### Node Dependencies
Installed in `frontend/` - see `frontend/package.json`

Key packages:
- React 18.2
- Vite 5.0
- TanStack Query 5.12
- Tailwind CSS 3.3

### Database
PostgreSQL 15 via Docker - configured in `docker-compose.yml`

```powershell
# Start database:
docker-compose up postgres -d

# Stop database:
docker-compose down
```

---

## Development Workflow

### Making Backend Changes
1. Edit files in `backend/`
2. Backend auto-reloads (if using `--reload` flag)
3. Refresh browser to test

### Making Frontend Changes
1. Edit files in `frontend/src/`
2. Vite hot-reload (automatic refresh)
3. Changes visible immediately in browser

### Database Changes
1. Edit `backend/models/`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Apply: `alembic upgrade head`
4. Restart backend

---

## Production Deployment

Before deploying to production:

1. **Update CORS Origins**
   - Edit `backend/main.py`
   - Change `allow_origins` from `["http://localhost:3000"]` to your domain

2. **Set Database URL**
   - Create `backend/.env` file
   - Set `DATABASE_URL` to production PostgreSQL

3. **Set Environment Variables**
   - `VITE_API_URL` - production API URL
   - `GOOGLE_SHEETS_CREDENTIALS_PATH` - path to credentials file
   - Other secrets in `.env`

4. **Build Frontend**
   ```powershell
   cd frontend
   npm run build
   # Creates optimized `dist/` folder
   ```

5. **Run Backend**
   ```powershell
   # Without reload, with production gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ```

---

## Common Commands

```powershell
# Backend: Start development server
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Backend: Run tests
cd backend
pytest tests/

# Frontend: Start development server
cd frontend
npm run dev

# Frontend: Build for production
cd frontend
npm run build

# Database: Start PostgreSQL
docker-compose up postgres -d

# Database: Stop PostgreSQL
docker-compose down

# Database: Access database shell
docker-compose exec postgres psql -U postgres

# Check what's running
Get-Process python, node

# Kill all processes
Stop-Process -Name python, node -Force -ErrorAction SilentlyContinue
```

---

## Getting Help

### Check Logs

**Backend Logs:**
- Look at the terminal window running the backend
- All requests and errors logged there

**Frontend Logs:**
- Look at the terminal window running frontend
- Check browser console (F12 → Console tab)

**Database Logs:**
```powershell
docker logs raven_postgres
```

### Debug Mode

**Backend with Debug Logging:**
```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

**Frontend with Dev Tools:**
- Press F12 in browser
- Check Console, Network, and Application tabs

---

## System Requirements Checklist

- ✓ Python 3.9+ (tested on 3.13)
- ✓ Node.js 18+ (for npm)
- ✓ Docker (for PostgreSQL)
- ✓ PowerShell 5.1+
- ✓ Port 3000 available (frontend)
- ✓ Port 8000 available (backend)
- ✓ Port 5432 available (database)

---

## Status: READY FOR DEVELOPMENT ✓

All components verified and tested.

**Next Step:** Run `START_BACKEND.bat` then `START_FRONTEND.bat`

Enjoy building! 🚀

