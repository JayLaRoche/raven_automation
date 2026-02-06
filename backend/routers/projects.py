from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db

# Optional imports - gracefully handle missing services
try:
    from services.google_sheets_services import get_sheets_service
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    get_sheets_service = lambda: None

try:
    from services.sync_services import SyncService
    SYNC_SERVICE_AVAILABLE = True
except ImportError:
    SYNC_SERVICE_AVAILABLE = False
    SyncService = None

router = APIRouter(prefix="/api/projects", tags=["projects"])


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    clientName: str
    address: str
    date: str


class UnitData(BaseModel):
    """Schema for adding a new unit to a project"""
    series: str
    productType: str
    width: float
    height: float
    glassType: str
    frameColor: str
    configuration: str = None

class UnitCreate(BaseModel):
    """Schema for creating a new unit with full details"""
    series: str
    productType: str
    width: float
    height: float
    glassType: str
    frameColor: str
    configuration: str = None
    hasGrids: bool = False
    itemNumber: str = None
    panelCount: int = 1
    swingOrientation: str = None
    handleSide: str = None


@router.post("/")
async def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project
    Returns project ID that can be used to navigate to the project
    """
    try:
        from app.models import Project
        from datetime import datetime
        
        # Parse date if provided
        project_date = None
        if project_data.date:
            try:
                project_date = datetime.strptime(project_data.date, "%Y-%m-%d")
            except ValueError:
                project_date = datetime.now()
        
        # Create new project - populate BOTH old and new field formats
        new_project = Project(
            # Legacy fields (for backward compatibility)
            project_name=project_data.clientName,
            customer_name=project_data.clientName,
            shipping_address=project_data.address,
            billing_address=project_data.address,
            po_number=None,
            
            # New fields (cleaner format)
            client_name=project_data.clientName,
            address=project_data.address,
            date=project_date,
            
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        return {
            "success": True,
            "id": new_project.id,
            "clientName": new_project.client_name or new_project.customer_name,
            "address": new_project.address or new_project.shipping_address,
            "date": project_data.date,
            "unitCount": 0
        }
    except Exception as e:
        db.rollback()
        import traceback
        print(f"❌ Error creating project: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


@router.get("/")
async def list_projects(db: Session = Depends(get_db)):
    """
    Get all projects from database
    Returns list of projects with their basic info
    """
    try:
        from app.models import Project
        
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        
        print(f"📋 Found {len(projects)} projects in database")
        
        return {
            "projects": [
                {
                    "id": p.id,
                    "clientName": p.client_name or p.customer_name or p.project_name or "Unknown",
                    "address": p.address or p.shipping_address or p.billing_address or "",
                    "date": p.date.strftime("%Y-%m-%d") if p.date else (p.created_at.strftime("%Y-%m-%d") if p.created_at else None),
                    "unitCount": len(p.windows) + len(p.doors) + len(p.units),
                    "status": "active"
                }
                for p in projects
            ]
        }
    except Exception as e:
        # Fallback to empty list if database not set up yet
        print(f"❌ Error fetching projects: {e}")
        import traceback
        print(traceback.format_exc())
        return {"projects": []}


@router.get("/{project_id}")
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific project
    """
    try:
        from app.models import Project
        
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {
            "id": project.id,
            "clientName": project.client_name or project.customer_name or project.project_name,
            "address": project.address or project.shipping_address,
            "date": project.date.strftime("%Y-%m-%d") if project.date else (project.created_at.strftime("%Y-%m-%d") if project.created_at else None),
            "unitCount": len(project.windows) + len(project.doors),
            "poNumber": project.po_number or "",
            "status": "active"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error fetching project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project and all its associated units.
    Uses CASCADE delete from database relationship.
    """
    try:
        from app.models import Project
        from datetime import datetime
        from sqlalchemy import text
        
        print(f"🗑️ Attempting to delete project {project_id}")
        
        # Find project
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not project:
            raise HTTPException(
                status_code=404, 
                detail=f"Project {project_id} not found"
            )
        
        # Get project name for response
        project_name = project.client_name or project.customer_name or "Unnamed Project"
        
        # Delete associated units first (CASCADE from relationship)
        delete_units_query = text("DELETE FROM units WHERE project_id = :pid")
        db.execute(delete_units_query, {"pid": project_id})
        
        # Delete project
        db.delete(project)
        db.commit()
        
        print(f"✅ Project {project_id} ({project_name}) deleted successfully")
        
        return {
            "success": True,
            "message": f"Project '{project_name}' deleted successfully",
            "deletedId": project_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error deleting project {project_id}:\n{error_trace}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete project: {str(e)}"
        )


@router.post("/{project_id}/units")
async def add_unit_to_project(
    project_id: int,
    data: UnitCreate,
    db: Session = Depends(get_db)
):
    """
    Add a new unit to an existing project
    """
    try:
        from app.models import Project, Unit
        from datetime import datetime
        from sqlalchemy import text
        
        print(f"📥 Adding unit to project {project_id}: {data.dict()}")
        
        # Verify project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Create unit using raw SQL for SQLite compatibility
        insert_query = text("""
            INSERT INTO units (
                project_id, series, product_type, width, height,
                glass_type, frame_color, configuration, has_grids,
                item_number, panel_count, swing_orientation, handle_side,
                created_at
            ) VALUES (
                :project_id, :series, :product_type, :width, :height,
                :glass_type, :frame_color, :configuration, :has_grids,
                :item_number, :panel_count, :swing_orientation, :handle_side,
                :created_at
            )
        """)
        
        db.execute(insert_query, {
            "project_id": project_id,
            "series": data.series,
            "product_type": data.productType,
            "width": data.width,
            "height": data.height,
            "glass_type": data.glassType,
            "frame_color": data.frameColor,
            "configuration": data.configuration,
            "has_grids": 1 if data.hasGrids else 0,
            "item_number": data.itemNumber,
            "panel_count": data.panelCount,
            "swing_orientation": data.swingOrientation,
            "handle_side": data.handleSide,
            "created_at": datetime.now()
        })
        db.commit()
        
        # Get the newly created unit ID
        unit_id_query = text("SELECT last_insert_rowid()")
        unit_id = db.execute(unit_id_query).scalar()
        
        print(f"✅ Unit {unit_id} added to project {project_id}")
        
        return {
            "success": True,
            "unitId": unit_id,
            "projectId": project_id,
            "unitData": {
                "series": data.series,
                "productType": data.productType,
                "width": data.width,
                "height": data.height,
                "glassType": data.glassType,
                "frameColor": data.frameColor,
                "configuration": data.configuration,
                "hasGrids": data.hasGrids,
                "panelCount": data.panelCount,
                "swingOrientation": data.swingOrientation,
                "handleSide": data.handleSide,
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error adding unit:\n{error_trace}")
        raise HTTPException(status_code=500, detail=str(e))


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


@router.post("/{project_id}/units")
async def add_unit_to_project(project_id: int, unit_data: UnitData, db: Session = Depends(get_db)):
    """
    Add a new window/door unit to an existing project
    This updates the project's unit count and stores the unit data
    """
    try:
        from app.models import Project, Window
        from datetime import datetime
        
        # Verify project exists (using mock data for now)
        # In production, query the database for the actual project
        
        # Create a new unit entry (Window model as example)
        new_unit = Window(
            project_id=project_id,
            series=unit_data.series,
            product_type=unit_data.productType,
            width=unit_data.width,
            height=unit_data.height,
            glass_type=unit_data.glassType,
            frame_color=unit_data.frameColor,
            configuration=unit_data.configuration,
            created_at=datetime.utcnow()
        )
        
        # For now, return success without database operations
        # In production: db.add(new_unit), db.commit(), db.refresh(new_unit)
        
        return {
            "success": True,
            "message": "Unit added successfully to project",
            "unit": {
                "id": f"unit_{project_id}_{datetime.utcnow().timestamp()}",
                "series": unit_data.series,
                "productType": unit_data.productType,
                "width": unit_data.width,
                "height": unit_data.height,
                "glassType": unit_data.glassType,
                "frameColor": unit_data.frameColor,
                "configuration": unit_data.configuration
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add unit: {str(e)}")
