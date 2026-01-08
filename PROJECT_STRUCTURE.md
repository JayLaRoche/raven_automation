# Raven Shop Drawing - Project Structure

## 📂 Directory Organization

```
raven-shop-automation/
│
├── 🎨 frontend/                      # React web application
│   ├── src/
│   │   ├── components/
│   │   │   ├── DrawingCanvas.jsx     # HTML5 Canvas drawing renderer
│   │   │   ├── Header.jsx            # Navigation header
│   │   │   └── ParameterPanel.jsx    # Parameter selection form
│   │   ├── pages/
│   │   │   ├── DrawingGenerator.jsx  # Main drawing app
│   │   │   └── ProjectList.jsx       # Projects list view
│   │   ├── services/
│   │   │   └── api.js                # Axios HTTP client
│   │   ├── App.jsx                   # Main router
│   │   ├── main.jsx                  # React entry point
│   │   └── index.css                 # TailwindCSS styles
│   ├── public/                       # Static assets
│   ├── index.html                    # HTML entry point
│   ├── package.json                  # npm dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind CSS config
│   ├── postcss.config.js             # PostCSS config
│   ├── .env                          # Environment variables
│   └── README.md                     # Frontend documentation
│
├── 🔧 backend/                       # FastAPI backend (existing)
│   ├── app/                          # Application code
│   ├── alembic/                      # Database migrations
│   ├── main.py                       # FastAPI entry point
│   ├── requirements.txt              # Python dependencies
│   └── ...
│
├── 🗄️ database/                      # Database files
│   └── schema.sql                    # PostgreSQL schema
│
├── 🗂️ scripts/                       # Utility scripts
│   ├── upload_frames_from_sheets.py # Google Sheets sync
│   ├── test_database.py             # Database verification
│   └── setup_database.py            # Database initialization
│
├── 📚 docs/                          # Documentation
│   └── ...
│
├── 📦 archive_desktop_app_*/         # Archived PyQt6 files (OLD)
│   └── [Timestamped archive of desktop app]
│
├── ⚙️ Configuration Files (Root)
│   ├── SETUP_GUIDE.md               # Quick start guide
│   ├── PROJECT_STRUCTURE.md         # This file
│   ├── README.md                    # Project overview
│   ├── API_DOCUMENTATION.md         # API reference
│   └── archive_desktop_files.ps1    # Archive script
│
└── 🚀 Development Files
    ├── package.json                 # Frontend dependencies
    ├── requirements.txt             # Backend dependencies
    └── .env                         # Environment config
```

## 🚀 Quick Start

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Start Frontend (Development)

```bash
cd frontend
npm run dev
```

**Access at**: `http://localhost:3000`

### 3. Start Backend (Development)

```bash
cd backend
uvicorn main:app --reload
```

**Access at**: `http://localhost:8000`

### 4. Backend API Endpoints (Already configured in Vite)

The frontend is configured to proxy API requests to `http://localhost:8000`:
- `GET /api/frames/series` - Get frame series list
- `POST /api/drawings/generate` - Generate drawing
- `GET /api/projects` - Get projects list
- `POST /api/drawings/export/pdf` - Export as PDF

## 📊 Component Architecture

### Frontend Stack
- **React 18** - UI framework
- **Vite 5** - Build tool & dev server (port 3000)
- **TailwindCSS 3** - Styling
- **React Query** - Data fetching
- **Axios** - HTTP client
- **React Router** - Navigation

### Backend Stack
- **FastAPI** - API framework (port 8000)
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Google Sheets API** - Data sync

### Database
- **raven_cad** PostgreSQL database
- 7 tables: frame_cross_sections, cad_components, product_configs, projects, drawing_templates, generated_drawings, user_preferences
- 2 views: v_frame_series_complete, v_project_status
- 29+ frame cross-sections synced from Google Sheets

## 📁 Key Files

### Frontend
- `frontend/src/App.jsx` - Main router (routes: /, /projects)
- `frontend/src/pages/DrawingGenerator.jsx` - Main app (combines ParameterPanel + DrawingCanvas)
- `frontend/src/components/ParameterPanel.jsx` - Parameter selection UI (9 controls)
- `frontend/src/components/DrawingCanvas.jsx` - Canvas renderer (800x1000px)
- `frontend/src/services/api.js` - API client (4 endpoints)

### Backend
- `backend/main.py` - FastAPI entry point
- `backend/app/` - Application modules
- `database/schema.sql` - Database schema (PostgreSQL)

### Database
- `database/schema.sql` - Table definitions, migrations, seed data

### Scripts
- `scripts/upload_frames_from_sheets.py` - Google Sheets → PostgreSQL sync
- `scripts/test_database.py` - Database verification
- `scripts/setup_database.py` - Database initialization

## 🎯 Development Workflow

### Adding a New Feature

1. **Frontend Component**: Create in `frontend/src/components/`
2. **API Endpoint**: Add route in `backend/app/routers/`
3. **Database Query**: Update `backend/app/services/`
4. **Test**: Use dev server at localhost:3000

### Updating Database Schema

1. Edit `database/schema.sql`
2. Run migrations via Alembic
3. Sync Google Sheets: `python scripts/upload_frames_from_sheets.py`

## 🔐 Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```
DATABASE_URL=postgresql://raven_user:raven_password_2025@localhost:5432/raven_cad
GOOGLE_SHEETS_CREDENTIALS=./credentials/service-account.json
```

## 📝 Important Notes

- **Database**: PostgreSQL must be running on localhost:5432
- **Google Sheets**: Service account JSON in `backend/credentials/`
- **Port 3000**: Frontend dev server (Vite)
- **Port 8000**: Backend API (FastAPI)
- **Proxy**: Frontend proxies `/api/*` to backend

## 🗂️ Desktop App Archive

Old PyQt6 desktop application files are archived in:
```
archive_desktop_app_20251226_072055/
```

To recreate: `.\archive_desktop_files.ps1` (run in project root)

## 📚 Documentation Files

- `SETUP_GUIDE.md` - Step-by-step setup instructions
- `README.md` - Project overview
- `API_DOCUMENTATION.md` - API reference
- `PROJECT_STRUCTURE.md` - This file (directory structure)

## ✅ Checklist

- ✅ Frontend React app created
- ✅ Frontend dependencies installed
- ✅ Database schema created
- ✅ Google Sheets sync working
- ✅ Desktop app archived
- ⏳ Backend API endpoints (4 routes needed)
- ⏳ Test end-to-end flow
- ⏳ Deploy to production

## 🚀 Next Steps

1. **Ensure backend is running**: `cd backend && uvicorn main:app --reload`
2. **Add API endpoints** to `backend/app/routers/`
3. **Test frontend**: `cd frontend && npm run dev`
4. **Build for production**: `cd frontend && npm run build`

---

**Version**: 1.0.0  
**Last Updated**: December 26, 2025  
**Status**: ✅ Frontend Ready | ⏳ Backend Integration Pending
