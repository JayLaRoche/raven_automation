# Raven Shop Drawing Generator - AI Coding Instructions

## Project Overview
Raven Shop Automation is a full-stack application for generating custom shop drawings for window/door frames. **Key distinction:** This is NOT a monolithic app—it's an integrated system where the frontend (React) proxies API calls to a backend (FastAPI) that orchestrates drawing generation, database queries, and PDF exports.

## Architecture & Key Patterns

### Multi-Service Architecture
- **Frontend** (port 3000): React/Vite app—handles UI and proxies `/api` requests to backend
- **Backend** (port 8000): FastAPI server—exposes REST API, manages PostgreSQL, generates PDFs
- **Database** (port 5432): PostgreSQL with Alembic migrations, Docker container via `docker-compose.yml`
- **Static Files** (`backend/static/frames/`): Frame series images served by FastAPI

**Why this structure:** Separation of concerns allows independent scaling, clear API boundaries, and the frontend can work without database access.

### Critical Data Flow: Frame Series Display
```
React Component → axios `/api/frames/series-with-images` → 
  FastAPI router → SQL query → Check filesystem for images → 
  JSON response with image URLs → Frontend renders dropdown with images
```
**Key file:** [backend/routers/frames.py](backend/routers/frames.py#L1) implements the dual lookup (database + filesystem).

### Database & Migrations
- **ORM:** SQLAlchemy 2.1 with declarative models
- **Migrations:** Alembic in [backend/alembic](backend/alembic) directory
- **Connection:** [backend/app/database.py](backend/app/database.py) handles PostgreSQL fallback to SQLite for dev
- **Fallback mode:** If database unavailable, API returns hardcoded series list (not an error)

## Developer Workflows

### Start Full Stack
**Single command (Windows):**
```bash
./START_SERVERS.bat
```
**Manual (all terminals from root):**
```bash
# Terminal 1: Backend
cd backend && uvicorn main:app --reload

# Terminal 2: Frontend  
cd frontend && npm run dev

# Terminal 3 (optional): Database shell
docker-compose up postgres pgadmin
```
**Visit:** http://localhost:3000 (frontend automatically proxies `/api` to `:8000`)

### Database Setup
```bash
# First-time: Initialize database
docker-compose up postgres pgadmin
cd backend && python init_db.py

# Create migration
cd backend && alembic revision --autogenerate -m "description"
alembic upgrade head

# Access pgAdmin: http://localhost:5050 (admin/admin2025)
```

### Frame Asset Organization
Before running the app with frame images:
```bash
cd backend && python organize_frame_assets.py
```
This moves files matching `{NUMBER}-{SECTION}.png` to `series-{NUMBER}-{SECTION}.png` format for consistency.

### Running Tests
```bash
cd backend
pytest tests/
httpx  # Frontend HTTP client testing
```

## Project-Specific Conventions

### API Endpoint Structure
All endpoints prefixed with `/api/`:
- `/api/frames/series` → returns `{"series": ["86", "135", ...]}`
- `/api/frames/series-with-images` → returns series WITH image URLs for UI display
- `/api/frames/series/{name}` → detailed frame specs (width/height ranges, view types)
- `/api/drawings/generate` → POST, returns PDF generation status
- `/api/drawings/export/pdf` → POST, returns blob

**Pattern:** Routers in [backend/routers/](backend/routers/) separate concerns (frames, drawings, projects). Each has its own `@router.get()` decorators.

### Frontend Service Layer
[frontend/src/services/api.js](frontend/src/services/api.js) is the **single point** for backend communication:
- Uses Axios with `baseURL: http://localhost:8000`
- Vite proxy in [frontend/vite.config.js](frontend/vite.config.js) forwards dev `/api` calls to backend
- All components use `useQuery()` from `@tanstack/react-query` (TanStack Query v5)

**Pattern:** Never directly import `axios`—always use exported functions from `api.js` (e.g., `getFrameSeriesWithImages()`).

### Database Query Pattern (Backend)
```python
# Do NOT use ORM queries directly in routes—use raw SQL via `text()`
from sqlalchemy import text
query = db.execute(
    text("SELECT DISTINCT series FROM frame_cross_sections ORDER BY series")
)
results = [row[0] for row in query.fetchall()]

# Always wrap in try/except with fallback return for resilience
```

### Static File Serving
- Frame images live in `backend/static/frames/` 
- FastAPI serves them at `/static/frames/{filename}`
- **Pattern:** Routers check filesystem existence before returning URLs
- Example: Series 86 looks for `series-86-thumbnail.png`, falls back to `series-86-head.png`

### Environment Configuration
[.env.example](/.env.example) defines:
- `DATABASE_URL` → PostgreSQL connection string
- `GOOGLE_SHEETS_CREDENTIALS_PATH` → Google Sheets integration
- `GOOGLE_SHEET_ID` → Project data source
- Frontend reads `VITE_API_URL` for proxy override in production

**Always load via:** `python-dotenv` (backend) or `import.meta.env` (frontend Vite).

## Key Dependencies & Versions
- **Backend:** FastAPI 0.104, SQLAlchemy 2.1, Alembic 1.13, Pillow 12.0, PyPDF2 3.0
- **Frontend:** React 18.2, Vite 5.0, TanStack Query 5.12, Zustand 5.0 (state management), Tailwind CSS 3.3
- **Database:** PostgreSQL 15 (Alpine), Alembic for schema versioning
- **PDF Generation:** ReportLab 4.0, matplotlib 3.9 for technical drawing generation

## Critical Integration Points

### CORS Configuration
[backend/main.py](backend/main.py) allows only `http://localhost:3000` in dev. **Update for production.**

### Drawing Generation Pipeline
[backend/services/reference_shop_drawing_generator.py](backend/services/reference_shop_drawing_generator.py) orchestrates:
1. Parse form parameters from frontend
2. Query database for frame specs (dimensions, materials, series data)
3. Generate PDF using ReportLab canvas
4. Return blob to frontend for download

### Google Sheets Sync
[backend/services/google_sheets_services.py](backend/services/google_sheets_services.py) handles credential flow. Requires `GOOGLE_SHEETS_CREDENTIALS_PATH` in `.env` for production data sync.

## Common Pitfalls & Solutions

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Frontend gets 404 on `/api/*` | Vite proxy not running or backend down | Check both servers running; restart both |
| Frame images not displaying | Images not in `backend/static/frames/` or wrong naming | Run `organize_frame_assets.py` |
| Database connection refused | PostgreSQL container not started | Run `docker-compose up postgres` |
| CORS errors in browser | Frontend running on different port | Verify `CORSMiddleware` allows your port |
| Alembic migration fails | Schema conflict or missing `env.py` | Check `backend/alembic/env.py` and retry with `--autogenerate` |

## File Structure Reference
```
backend/
  main.py                    # FastAPI app, CORS, static mount
  app/database.py            # SQLAlchemy engine, session factory
  routers/frames.py          # Frame series endpoints
  routers/drawings.py        # PDF generation endpoints
  services/                  # Business logic (drawing generator, sheets sync)
  models/                    # SQLAlchemy ORM models
  alembic/                   # Database migration scripts
frontend/
  src/services/api.js        # Axios client, all API functions
  src/pages/                 # Route-level components
  src/components/            # Reusable UI components
  vite.config.js             # Vite config with /api proxy
docker-compose.yml           # PostgreSQL + pgAdmin services
.env.example                 # Configuration template
```

## When Adding Features
1. **New database table?** Create SQLAlchemy model in `backend/models/`, then `alembic revision --autogenerate`
2. **New API endpoint?** Add route in appropriate `backend/routers/file.py`, follow existing pattern (query database, fallback on error)
3. **New frontend page?** Create in `frontend/src/pages/`, use `useQuery()` with function from `api.js`
4. **New frame series?** Add PNG images to `backend/static/frames/` with naming `series-{NUMBER}-{SECTION}.png`
5. **Production deployment?** Update CORS origins, database URL, and Google Sheets credentials in `.env`
