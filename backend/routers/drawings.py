"""
Drawing generation routes
API endpoints for generating and retrieving technical shop drawings
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
import os
import io
from typing import List, Dict
from pydantic import BaseModel

from app.database import get_db
from app.models import Project, Window, Door
from services.google_sheets_services import get_sheets_service
from app.services.integrated_drawing_service import get_drawing_service
from services.reference_shop_drawing_generator import ReferenceShopDrawingGenerator

router = APIRouter(prefix="/api/drawings", tags=["drawings"])


class DrawingParameters(BaseModel):
    """Parameters for generating a shop drawing"""
    series: str = "65"
    product_type: str = "FIXED"
    width: float = 48.0
    height: float = 60.0
    glass_type: str = "Clear Low E Dual Pane"
    frame_color: str = "Black"
    configuration: str = "O"  # X/O notation
    item_number: str = "P001"
    po_number: str = ""
    notes: str = ""
    special_notes: str = ""


@router.post("/project/{po_number}/generate")
async def generate_project_drawings(po_number: str, db: Session = Depends(get_db)):
    """
    Generate technical shop drawings for all items in a project
    
    Args:
        po_number: Purchase order number to generate drawings for
        
    Returns:
        List of generated drawing file paths
    """
    try:
        # Get project and items from database
        project = db.query(Project).filter_by(po_number=po_number).first()
        
        if not project:
            raise ValueError(f"Project with PO number '{po_number}' not found")
        
        # Get drawing service
        drawing_service = get_drawing_service()
        
        # Generate all drawings for project
        results = drawing_service.generate_project_drawings(project)
        
        total_generated = len(results['windows']) + len(results['doors'])
        
        if total_generated == 0:
            raise ValueError(f"No items found in project {po_number}")
        
        return {
            "success": True,
            "po_number": po_number,
            "project_name": project.project_name,
            "message": f"Generated {total_generated} drawing(s)",
            "windows_generated": len(results['windows']),
            "doors_generated": len(results['doors']),
            "files": {
                "windows": [os.path.basename(f) for f in results['windows']],
                "doors": [os.path.basename(f) for f in results['doors']]
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drawing generation failed: {str(e)}")


@router.post("/window/{window_id}")
async def generate_window_drawing(window_id: int, db: Session = Depends(get_db)):
    """
    Generate a drawing for a specific window
    
    Args:
        window_id: Database ID of the window
        
    Returns:
        Generated PDF file info
    """
    try:
        # Get window and project from database
        window = db.query(Window).filter_by(id=window_id).first()
        
        if not window:
            raise ValueError(f"Window with ID {window_id} not found")
        
        project = db.query(Project).filter_by(id=window.project_id).first()
        
        # Generate drawing
        drawing_service = get_drawing_service()
        pdf_path = drawing_service.generate_window_from_model(window, project)
        
        return {
            "success": True,
            "window_id": window_id,
            "item_number": window.item_number,
            "file": os.path.basename(pdf_path),
            "path": pdf_path
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drawing generation failed: {str(e)}")


@router.post("/door/{door_id}")
async def generate_door_drawing(door_id: int, db: Session = Depends(get_db)):
    """
    Generate a drawing for a specific door
    
    Args:
        door_id: Database ID of the door
        
    Returns:
        Generated PDF file info
    """
    try:
        # Get door and project from database
        door = db.query(Door).filter_by(id=door_id).first()
        
        if not door:
            raise ValueError(f"Door with ID {door_id} not found")
        
        project = db.query(Project).filter_by(id=door.project_id).first()
        
        # Generate drawing
        drawing_service = get_drawing_service()
        pdf_path = drawing_service.generate_door_from_model(door, project)
        
        return {
            "success": True,
            "door_id": door_id,
            "item_number": door.item_number,
            "file": os.path.basename(pdf_path),
            "path": pdf_path
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drawing generation failed: {str(e)}")


@router.get("/download/{filename}")
async def download_drawing(filename: str):
    """
    Download a specific drawing PDF
    
    Args:
        filename: Name of the drawing file
        
    Returns:
        PDF file for download
    """
    drawings_dir = "./drawings"
    filepath = os.path.join(drawings_dir, filename)
    
    # Security: Ensure file is in drawings directory
    if not os.path.abspath(filepath).startswith(os.path.abspath(drawings_dir)):
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Drawing not found")
    
    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=filename
    )


@router.get("/list/all")
async def list_all_drawings():
    """
    List all generated drawings
    
    Returns:
        List of all PDF files in drawings directory
    """
    try:
        drawing_service = get_drawing_service()
        drawings = drawing_service.list_generated_drawings()
        
        return {
            "total": len(drawings['all']),
            "recent_count": len(drawings['recent']),
            "all_drawings": drawings['all'],
            "recent_drawings": drawings['recent']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_drawing(drawing_params: dict):
    """
    Generate a drawing from parameters (for web app)
    
    Args:
        drawing_params: Dictionary containing drawing parameters:
            - series: Frame series name
            - productType: Type of product
            - width: Width in inches
            - height: Height in inches
            - glassType: Type of glass
            - frameColor: Color of frame
            - hasGrids: Whether to include grids
            - itemNumber: Item number
            - poNumber: PO number
    
    Returns:
        Drawing data for frontend rendering
    """
    try:
        # Return the parameters back to frontend
        # Frontend will render using HTML5 Canvas
        return {
            "success": True,
            "drawing": drawing_params,
            "status": "ready_for_rendering"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prepare drawing: {str(e)}")


@router.get("/info")
async def drawing_service_info():
    """
    Get info about the drawing service

    Returns:
        Service status and capabilities
    """
    drawings_dir = "./drawings"

    # Count total drawings
    total_drawings = 0
    if os.path.exists(drawings_dir):
        total_drawings = len([f for f in os.listdir(drawings_dir) if f.endswith('.pdf')])

    return {
        "service": "Professional CAD Drawing Generator",
        "status": "operational",
        "version": "1.0",
        "capabilities": [
            "Generate window elevation drawings with CAD dimensions",
            "Generate door elevation drawings with CAD dimensions",
            "Support for professional 3-column layout",
            "Specification tables and project metadata",
            "Batch project drawing generation",
            "PDF download and file management"
        ],
        "output_directory": drawings_dir,
        "total_drawings_generated": total_drawings,
        "api_endpoints": {
            "generate": "POST /api/drawings/generate",
            "generate_reference": "POST /api/drawings/generate-pdf",
            "generate_project": "POST /api/drawings/project/{po_number}/generate",
            "generate_window": "POST /api/drawings/window/{window_id}",
            "generate_door": "POST /api/drawings/door/{door_id}",
            "list_all": "GET /api/drawings/list/all",
            "download": "GET /api/drawings/download/{filename}",
            "info": "GET /api/drawings/info"
        }
    }


@router.post("/generate-pdf")
async def generate_reference_pdf(params: DrawingParameters):
    """
    Generate A3 landscape shop drawing in PDF format with exact reference layout
    
    Returns:
        PDF document matching Raven's reference layout exactly
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"PDF generation request: series={params.series}, item={params.item_number}")
        
        # Validate input parameters
        if not params.series:
            raise ValueError("Series is required")
        if not params.item_number:
            raise ValueError("Item number is required")
        if params.width is None or params.width <= 0:
            raise ValueError(f"Invalid width: {params.width}")
        if params.height is None or params.height <= 0:
            raise ValueError(f"Invalid height: {params.height}")
        
        # Create drawing generator
        generator = ReferenceShopDrawingGenerator(
            db_connection=None,  # Database optional
            parameters=params.dict()
        )
        
        # Generate PDF
        logger.debug("Starting PDF generation")
        pdf_buffer = generator.generate_pdf()
        
        if not pdf_buffer or pdf_buffer.tell() == 0:
            raise RuntimeError("PDF buffer is empty")
        
        logger.info(f"PDF generated successfully: {pdf_buffer.tell()} bytes")
        
        # Return as streaming PDF response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={params.item_number}_drawing.pdf"
            }
        )
        
    except ValueError as e:
        logger.warning(f"Validation error in PDF generation: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid parameters: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
        error_msg = str(e)
        if "PDF generation failed:" in error_msg:
            # Use the detailed message from the generator
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate drawing: {error_msg}"
            )
