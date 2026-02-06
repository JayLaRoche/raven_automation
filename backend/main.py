from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from routers import projects, drawings, frames
from app.database import engine, Base

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log configuration summary
logger.info(settings.summary())

# Create database tables (with error handling)
try:
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created/verified")
except Exception as e:
    print(f"[WARNING] Database connection not available: {str(e)}")
    print("   Using fallback mode - frames endpoint will return default data")

app = FastAPI(title="Raven Shop Drawings API")

# CORS for React frontend
# In production, settings.CORS_ORIGINS will be set to your Render frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router)
app.include_router(drawings.router)
app.include_router(frames.router)

# Mount static files for frame images FIRST
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"[OK] Created static directory: {static_dir}")

if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
    print("[OK] Static files mounted at /static (includes O-Icon_library)")
    
    # Verify O-Icon_library exists
    o_icon_dir = os.path.join(static_dir, 'O-Icon_library')
    if os.path.exists(o_icon_dir):
        print(f"[OK] O-Icon library verified at /static/O-Icon_library")
    else:
        print(f"[WARNING] O-Icon library not found at: {o_icon_dir}")

# Mount assets directory for frame cross-section images
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)
    print(f"[OK] Created assets directory: {assets_dir}")

if os.path.exists(assets_dir):
    app.mount('/assets', StaticFiles(directory=assets_dir), name='assets')
    print("[OK] Assets mounted at /assets")

# Mount frame_library directory for Series variant images
frame_library_dir = os.path.join(os.path.dirname(__file__), 'frame_library')
if os.path.exists(frame_library_dir):
    app.mount('/frame-library', StaticFiles(directory=frame_library_dir), name='frame-library')
    print("[OK] Frame library mounted at /frame-library")
else:
    print(f"[WARNING] Frame library directory not found: {frame_library_dir}")

# Startup and Shutdown Events for Frame Sync Scheduler
@app.on_event("startup")
async def startup_event():
    logger.info("[OK] Application starting...")
    logger.info("[OK] Frame sync scheduler can be activated via API endpoint")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("[OK] Shutting down application...")
    try:
        from services.frame_sync_scheduler import stop_frame_sync_scheduler
        stop_frame_sync_scheduler()
    except Exception as e:
        logger.warning(f"[WARNING] Error stopping scheduler: {str(e)}")
    logger.info("[OK] Shutdown complete")

@app.get("/")
async def root():
    return {"message": "Raven Shop Drawings API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for Render and Docker"""
    from datetime import datetime
    from app.database import SessionLocal
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "unknown",
        "environment": os.getenv("APP_ENV", "development"),
        "port": os.getenv("PORT", "8000"),
    }
    
    # Check database connectivity
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["database"] = f"disconnected: {str(e)}"
        logger.warning(f"Health check database error: {str(e)}")
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to allow external connections (required by Render)
    # Read PORT from environment (Render sets this dynamically)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")