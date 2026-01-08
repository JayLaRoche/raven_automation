from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from services.google_sheets_services import get_sheets_service
from services.sync_services import SyncService

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/sheets/available")
async def list_available_sheets():
    """Get all available sheet names from Google Sheets"""
    try:
        sheets_service = get_sheets_service()
        sheets = sheets_service.get_available_sheets()
        return {"sheets": sheets, "count": len(sheets)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/po-numbers")
async def list_po_numbers(sheet_name: str = None):
    """Get all available PO numbers from Google Sheets (optionally from specific sheet)"""
    try:
        sheets_service = get_sheets_service()
        po_numbers = sheets_service.get_all_po_numbers(sheet_name)
        return {"po_numbers": po_numbers, "sheet": sheet_name or "default"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{po_number}/sync")
async def sync_project(po_number: str, db: Session = Depends(get_db)):
    """
    Sync project data from Google Sheets to database
    This pulls the latest data and stores it locally
    """
    try:
        sheets_service = get_sheets_service()
        sync_service = SyncService(db, sheets_service)
        
        result = sync_service.sync_project(po_number)
        
        return {
            "success": True,
            "message": f"Project {po_number} {result['sync_type']} successfully",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")


@router.get("/{po_number}")
async def get_project(po_number: str, db: Session = Depends(get_db)):
    """
    Get project data from database
    If not found, returns 404 with instruction to sync
    """
    try:
        sheets_service = get_sheets_service()
        sync_service = SyncService(db, sheets_service)
        
        project_data = sync_service.get_project_from_db(po_number)
        return project_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=404, 
            detail=f"{str(e)} Use POST /api/projects/{po_number}/sync to sync from Google Sheets."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{po_number}/status")
async def check_sync_status(po_number: str, db: Session = Depends(get_db)):
    """
    Check if a project is synced and when it was last updated
    Useful for showing sync status in UI
    """
    from app.models import Project
    
    project = db.query(Project).filter(Project.po_number == po_number).first()
    
    if not project:
        return {
            "synced": False,
            "po_number": po_number,
            "message": "Project not synced yet"
        }
    
    return {
        "synced": True,
        "po_number": po_number,
        "project_id": project.id,
        "last_synced": project.updated_at.isoformat() if project.updated_at else None,
        "windows_count": len(project.windows),
        "doors_count": len(project.doors)
    }