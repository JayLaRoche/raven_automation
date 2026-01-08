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
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(projects.router)
app.include_router(drawings.router)
app.include_router(frames.router)

# Mount static files for frame images
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"[OK] Created static directory: {static_dir}")

if os.path.exists(static_dir):
    app.mount('/static', StaticFiles(directory=static_dir), name='static')
    print("[OK] Static files mounted at /static")

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
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")