"""
Integration Guide: Adding CAD Drawing Generator to Main FastAPI App

This guide shows how to integrate the CAD drawing system into an existing
FastAPI application.
"""

# ============================================================================
# STEP 1: Add CAD Drawing Router to Main App
# ============================================================================
# File: app/main.py (or wherever you initialize FastAPI)

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cad_drawings  # Import the router
from app.database import engine
from app import models

# Create FastAPI app
app = FastAPI(
    title="Raven Shop Automation",
    description="Professional CAD shop drawing generation and order management",
    version="1.0.0"
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# ✅ Include CAD drawing router
app.include_router(cad_drawings.router, tags=["CAD Drawings"])

# Include other routers as needed
# app.include_router(other_router)

@app.get("/")
def read_root():
    return {
        "status": "Raven Shop Automation API",
        "version": "1.0.0",
        "endpoints": {
            "CAD Drawings": "/api/drawings/cad",
            "API Documentation": "/docs",
            "Alternative Docs": "/redoc"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""


# ============================================================================
# STEP 2: Verify Dependencies
# ============================================================================
# Add to requirements.txt:

"""
reportlab==4.0.7
"""

# Or install directly:
# pip install reportlab


# ============================================================================
# STEP 3: Test the Integration
# ============================================================================

"""
# Start the server
uvicorn app.main:app --reload

# Test endpoint (in separate terminal or using curl)
curl -X GET http://localhost:8000/docs

# This will show the Swagger UI with all available endpoints
"""


# ============================================================================
# STEP 4: Using the CAD Drawing API
# ============================================================================

"""
EXAMPLE 1: Generate a single window drawing
───────────────────────────────────────────

GET http://localhost:8000/api/drawings/cad/window/1

Response: PDF stream (inline display)


EXAMPLE 2: Download a window drawing
─────────────────────────────────────

GET http://localhost:8000/api/drawings/cad/window/1?download=true

Response: PDF file download (Drawing_W001_20240120_143022.pdf)


EXAMPLE 3: Generate all drawings for a project
────────────────────────────────────────────────

POST http://localhost:8000/api/drawings/cad/project/PO-2024-001/all

Response: Multiple PDFs (one per item)


EXAMPLE 4: Batch export as ZIP
───────────────────────────────

POST http://localhost:8000/api/drawings/cad/project/PO-2024-001/all?as_zip=true

Response: ZIP file (PO-2024-001_drawings_20240120_143022.zip)


EXAMPLE 5: Generate from custom data
──────────────────────────────────────

POST http://localhost:8000/api/drawings/cad/custom

Body:
{
    "item_id": "W-CUSTOM",
    "width_inches": 72.0,
    "height_inches": 48.0,
    "series": "80",
    "frame_color": "Black",
    "glass": "Clear - 1/2 Low-E",
    "quantity": 1,
    "config": {
        "type": "FIXED",
        "panels": 1
    }
}

Response: PDF stream
"""


# ============================================================================
# STEP 5: Database Model Compatibility
# ============================================================================

"""
The CAD drawing system expects these fields in your Window model:

Required:
  - item_number: str (e.g., 'W102')
  - width_inches: float (e.g., 72.0)
  - height_inches: float (e.g., 48.0)
  - frame_series: str (e.g., 'Series 80')

Recommended:
  - room: str (e.g., 'Living Room')
  - window_type: str (e.g., 'FIXED')
  - swing_direction: str (e.g., 'Left')
  - glass_type: str (e.g., 'Clear')
  - frame_color: str (e.g., 'Black')
  - quantity: int (e.g., 1)
  - screen_type: str (optional)
  - hardware_spec: str (optional)

Optional:
  - project_id: int (links to Project)

Example model definition:

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Window(Base):
    __tablename__ = "windows"
    
    id = Column(Integer, primary_key=True)
    item_number = Column(String)
    room = Column(String)
    width_inches = Column(Float)
    height_inches = Column(Float)
    window_type = Column(String)
    frame_series = Column(String)
    swing_direction = Column(String)
    glass_type = Column(String)
    frame_color = Column(String)
    quantity = Column(Integer, default=1)
    screen_type = Column(String, nullable=True)
    hardware_spec = Column(String, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    project = relationship("Project", back_populates="windows")
"""


# ============================================================================
# STEP 6: Environment & Configuration
# ============================================================================

"""
Optional: Create a .env file for configuration

# .env
DATABASE_URL=postgresql://user:password@localhost/raven_db
DEBUG=True
CAD_OUTPUT_DIR=./drawings
MAX_DRAWING_SIZE=10MB

Then load in your app:

from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", False)
"""


# ============================================================================
# STEP 7: Error Handling & Logging
# ============================================================================

"""
The API includes comprehensive error handling. Examples:

400 Bad Request
───────────────
{
    "detail": "Invalid drawing data: ['Width must be positive']"
}

404 Not Found
──────────────
{
    "detail": "Window 999 not found"
}

422 Unprocessable Entity
────────────────────────
{
    "detail": "Invalid drawing data: ['Invalid series: 99']"
}

To add logging:

import logging

logger = logging.getLogger(__name__)

@router.post("/window/{window_id}")
def generate_window_cad_drawing(window_id: int, db: Session):
    logger.info(f"Generating drawing for window {window_id}")
    try:
        # ... existing code ...
        logger.info(f"Drawing generated successfully")
    except Exception as e:
        logger.error(f"Failed to generate drawing: {str(e)}")
        raise
"""


# ============================================================================
# STEP 8: Production Deployment Checklist
# ============================================================================

"""
Before deploying to production:

✅ Database
   - [ ] Verify all Window/Door fields populated
   - [ ] Validate database connectivity
   - [ ] Test sample data retrieval

✅ Dependencies
   - [ ] Install reportlab (pip install reportlab)
   - [ ] Verify all imports work
   - [ ] Check Python version compatibility

✅ API Endpoints
   - [ ] Test individual window generation
   - [ ] Test batch project generation
   - [ ] Test custom data submission
   - [ ] Verify ZIP export works

✅ PDF Output
   - [ ] Verify PDF files are generated
   - [ ] Check file sizes (should be < 1MB)
   - [ ] Test PDF opens correctly
   - [ ] Validate layout and dimensions

✅ Error Handling
   - [ ] Test with missing data
   - [ ] Test with invalid series
   - [ ] Test with non-existent IDs
   - [ ] Verify error messages are helpful

✅ Performance
   - [ ] Measure generation time
   - [ ] Check memory usage
   - [ ] Test with batch of 50+ drawings
   - [ ] Verify server doesn't crash

✅ Security
   - [ ] Enable HTTPS in production
   - [ ] Implement authentication if needed
   - [ ] Validate all user inputs
   - [ ] Limit file download sizes
   - [ ] Add rate limiting if necessary

✅ Monitoring
   - [ ] Set up error logging
   - [ ] Monitor API response times
   - [ ] Track usage statistics
   - [ ] Alert on failures
"""


# ============================================================================
# STEP 9: Testing Examples (using pytest)
# ============================================================================

"""
# tests/test_cad_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_window_drawing():
    # Create test window in database first
    response = client.get("/api/drawings/cad/window/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_generate_window_download():
    response = client.get("/api/drawings/cad/window/1?download=true")
    assert response.status_code == 200
    assert "filename" in response.headers["content-disposition"]


def test_invalid_window():
    response = client.get("/api/drawings/cad/window/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_custom_drawing():
    data = {
        "width_inches": 72.0,
        "height_inches": 48.0,
        "series": "80",
        "frame_color": "Black",
        "config": {"type": "FIXED", "panels": 1}
    }
    response = client.post("/api/drawings/cad/custom", json=data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_invalid_custom_drawing():
    data = {
        "width_inches": -10,  # Invalid: negative
        "height_inches": 48.0,
        "series": "80"
    }
    response = client.post("/api/drawings/cad/custom", json=data)
    assert response.status_code == 422


# Run tests
# pytest tests/test_cad_api.py -v
"""


# ============================================================================
# STEP 10: Performance Optimization (Optional)
# ============================================================================

"""
For high-volume drawing generation:

1. Caching
───────
from functools import lru_cache

@lru_cache(maxsize=100)
def get_profile(series: str):
    return FRAME_PROFILES[series]


2. Async Generation
──────────────────
from fastapi import BackgroundTasks

@router.post("/window/{window_id}/async")
async def generate_async(window_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_and_save, window_id)
    return {"status": "generating", "window_id": window_id}


3. Database Connection Pooling
──────────────────────────────
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)


4. Batch Processing with Celery
────────────────────────────────
from celery import shared_task

@shared_task
def generate_project_drawings(po_number: str):
    # Long-running task
    project = db.query(Project).filter(...).first()
    for window in project.windows:
        generate_cad_drawing(window)


5. Disk Caching
───────────────
import hashlib
from pathlib import Path

cache_dir = Path("./drawings_cache")

def get_cached_drawing(window_id: int) -> Optional[bytes]:
    cache_file = cache_dir / f"{window_id}.pdf"
    if cache_file.exists():
        return cache_file.read_bytes()
    return None

def cache_drawing(window_id: int, pdf_bytes: bytes):
    cache_file = cache_dir / f"{window_id}.pdf"
    cache_file.write_bytes(pdf_bytes)
"""


# ============================================================================
# STEP 11: Troubleshooting
# ============================================================================

"""
Issue: ImportError: No module named 'reportlab'
────────────────────────────────────────────────
Solution: pip install reportlab

Issue: PDF files are empty or corrupt
──────────────────────────────────────
Solution: Check that all data fields are populated correctly
         Run test_cad_generator.py to verify output

Issue: Dimension callouts missing from drawing
───────────────────────────────────────────────
Solution: Verify width_inches and height_inches are positive
         Check that frame_series is valid ('80', '86', '135')

Issue: API timeout on batch generation
───────────────────────────────────────
Solution: Increase timeout in nginx/uvicorn config
         Or use ZIP export endpoint which supports multiple files
         Or implement async generation with Celery

Issue: Memory usage growing after many requests
────────────────────────────────────────────────
Solution: Ensure BytesIO buffers are properly closed
         Use garbage collection explicitly if needed
         Consider using disk caching for large batches
"""


# ============================================================================
# SUMMARY
# ============================================================================

"""
Integration Steps:
1. Add cad_drawings router to main FastAPI app
2. Ensure reportlab is installed
3. Verify database models match expected fields
4. Test individual endpoints
5. Run comprehensive tests
6. Deploy with proper error handling and logging

Key Files:
- routers/cad_drawings.py      (11 API endpoints)
- app/services/cad_drawing_generator.py  (PDF generation)
- app/services/cad_data_transformer.py   (Data conversion)
- app/services/frame_profiles.py         (Geometry definitions)

Documentation:
- CAD_DRAWING_GUIDE.md              (Technical reference)
- CAD_IMPLEMENTATION_SUMMARY.md      (Overview)
- This file (Integration guide)

Status: ✅ Ready for production integration
"""
