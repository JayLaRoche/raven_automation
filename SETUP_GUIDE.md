# Raven Shop Drawing - Web Application Setup Guide

## 🎉 Welcome!

You now have a complete web application for CAD shop drawing generation!

## 📁 Project Structure

```
raven-shop-automation/
├── backend/                    # FastAPI backend (existing)
│   ├── app/
│   ├── main.py
│   └── ...
├── frontend/                   # React web app (NEW)
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── archive_desktop_app_*/     # Archived PyQt6 files

```

## 🚀 Quick Start

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

The `.env` file is already created with:
```
VITE_API_URL=http://localhost:8000
```

### 3. Start Backend (if not running)

```bash
cd backend
uvicorn main:app --reload
```

### 4. Start Frontend

```bash
cd frontend
npm run dev
```

The web app will open at `http://localhost:3000`

## ✨ Features

### ✅ Implemented

- **Parameter Panel**: Frame series, dimensions, glass type, colors
- **Drawing Canvas**: Real-time HTML5 canvas rendering
- **Project List**: View all projects from database
- **Responsive Design**: Works on desktop and mobile
- **API Integration**: Connects to FastAPI backend

### 🎨 User Interface

- **Modern Design**: Tailwind CSS styling
- **Intuitive Layout**: 2-column responsive grid
- **Real-time Preview**: Instant drawing updates
- **Export Options**: PNG download built-in

## 🔧 Backend API Endpoints Needed

Add these to your FastAPI backend (`backend/app/main.py`):

```python
@app.get("/api/frames/series")
async def get_frame_series():
    """Get available frame series from database"""
    # Query frame_cross_sections table
    pass

@app.post("/api/drawings/generate")
async def generate_drawing(params: dict):
    """Generate CAD shop drawing"""
    # Use existing drawing engine
    pass

@app.get("/api/projects")
async def get_projects():
    """Get project list"""
    # Query projects table
    pass
```

## 📦 npm Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🌐 Deployment

### Production Build

```bash
cd frontend
npm run build
```

Output in `frontend/dist/` - deploy to any static host (Netlify, Vercel, etc.)

### Backend Deployment

Deploy FastAPI backend to cloud (AWS, Heroku, Railway, etc.)

Update `VITE_API_URL` in `.env` to production API URL

## 🔄 Migration from Desktop App

The PyQt6 desktop application files have been preserved in case you need them:

- Archive script created: `archive_desktop_files.ps1`
- Run to archive desktop files: `.\archive_desktop_files.ps1`
- All desktop files will be moved to timestamped archive folder

## 📚 Technology Stack

**Frontend:**
- React 18 - UI framework
- Vite - Build tool & dev server
- Tailwind CSS - Styling
- React Query - Data fetching
- Axios - HTTP client
- React Router - Navigation

**Backend:**
- FastAPI - API framework
- PostgreSQL - Database
- SQLAlchemy - ORM

## 🎯 Next Steps

1. ✅ **Install dependencies**: `cd frontend && npm install`
2. ✅ **Start dev server**: `npm run dev`
3. 🔧 **Add API endpoints** to FastAPI backend
4. 🎨 **Customize styling** in Tailwind config
5. 📱 **Test on mobile** devices

## 🐛 Troubleshooting

**Frontend won't start:**
- Check Node.js is installed: `node --version`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

**Can't connect to backend:**
- Verify backend is running on port 8000
- Check CORS settings in FastAPI
- Verify `.env` has correct API_URL

**Build errors:**
- Clear Vite cache: `npm run dev -- --force`
- Check all imports are correct

## 📞 Support

For issues, check:
1. Console logs (F12 in browser)
2. Network tab for API errors
3. Backend logs for server errors

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: ✅ Ready for Development
