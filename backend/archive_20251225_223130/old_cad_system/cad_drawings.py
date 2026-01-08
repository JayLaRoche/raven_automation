"""
CAD Drawing API Routes
RESTful endpoints for generating professional CAD shop drawings
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from pathlib import Path
import io

from app.models import Window, Door, Project
from app.database import get_db
from app.services.cad_drawing_generator import generate_cad_drawing
from app.services.cad_data_transformer import CADDataTransformer, CADDrawingValidator

router = APIRouter(prefix="/api/drawings/cad", tags=["CAD Drawings"])


@router.post("/window/{window_id}")
def generate_window_cad_drawing(
    window_id: int,
    db: Session = next(get_db()),
    download: bool = Query(False, description="Return as downloadable file")
):
    """
    Generate CAD drawing for a specific window
    
    Args:
        window_id: ID of the window
        download: If true, return as downloadable file
        
    Returns:
        PDF bytes or file response
    """
    # Get window from database
    window = db.query(Window).filter(Window.id == window_id).first()
    if not window:
        raise HTTPException(status_code=404, detail=f"Window {window_id} not found")
    
    # Get associated project if available
    project = None
    if hasattr(window, 'project_id'):
        project = db.query(Project).filter(Project.id == window.project_id).first()
    
    # Transform to CAD data
    cad_data = CADDataTransformer.window_to_cad_data(window, project)
    
    # Validate
    is_valid, errors = CADDrawingValidator.validate_window_data(cad_data)
    if not is_valid:
        raise HTTPException(status_code=422, detail=f"Invalid drawing data: {errors}")
    
    # Generate PDF
    pdf_bytes = generate_cad_drawing(cad_data)
    
    if download:
        filename = f"Drawing_W{window.item_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            filename=filename
        )
    else:
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf"
        )


@router.post("/door/{door_id}")
def generate_door_cad_drawing(
    door_id: int,
    db: Session = next(get_db()),
    download: bool = Query(False, description="Return as downloadable file")
):
    """
    Generate CAD drawing for a specific door
    
    Args:
        door_id: ID of the door
        download: If true, return as downloadable file
        
    Returns:
        PDF bytes or file response
    """
    # Get door from database
    door = db.query(Door).filter(Door.id == door_id).first()
    if not door:
        raise HTTPException(status_code=404, detail=f"Door {door_id} not found")
    
    # Get associated project if available
    project = None
    if hasattr(door, 'project_id'):
        project = db.query(Project).filter(Project.id == door.project_id).first()
    
    # Transform to CAD data
    cad_data = CADDataTransformer.door_to_cad_data(door, project)
    
    # Validate
    is_valid, errors = CADDrawingValidator.validate_door_data(cad_data)
    if not is_valid:
        raise HTTPException(status_code=422, detail=f"Invalid drawing data: {errors}")
    
    # Generate PDF
    pdf_bytes = generate_cad_drawing(cad_data)
    
    if download:
        filename = f"Drawing_D{door.item_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            filename=filename
        )
    else:
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf"
        )


@router.post("/project/{po_number}/all")
def generate_project_cad_drawings(
    po_number: str,
    db: Session = next(get_db()),
    as_zip: bool = Query(False, description="Return as ZIP file")
):
    """
    Generate CAD drawings for all items in a project
    
    Args:
        po_number: PO number for the project
        as_zip: If true, return all drawings as ZIP
        
    Returns:
        Multiple PDFs or ZIP file
    """
    # Get project
    project = db.query(Project).filter(Project.po_number == po_number).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {po_number} not found")
    
    # Get all windows and doors for project
    windows = db.query(Window).filter(Window.project_id == project.id).all()
    doors = db.query(Door).filter(Door.project_id == project.id).all()
    
    if not windows and not doors:
        raise HTTPException(status_code=404, detail=f"No items found for project {po_number}")
    
    # Generate all drawings
    drawings = {}
    
    for window in windows:
        cad_data = CADDataTransformer.window_to_cad_data(window, project)
        is_valid, errors = CADDrawingValidator.validate_window_data(cad_data)
        if is_valid:
            pdf_bytes = generate_cad_drawing(cad_data)
            filename = f"W{window.item_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            drawings[filename] = pdf_bytes
    
    for door in doors:
        cad_data = CADDataTransformer.door_to_cad_data(door, project)
        is_valid, errors = CADDrawingValidator.validate_door_data(cad_data)
        if is_valid:
            pdf_bytes = generate_cad_drawing(cad_data)
            filename = f"D{door.item_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            drawings[filename] = pdf_bytes
    
    if as_zip:
        import zipfile
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename, pdf_bytes in drawings.items():
                zf.writestr(filename, pdf_bytes)
        
        zip_buffer.seek(0)
        return FileResponse(
            zip_buffer,
            media_type="application/zip",
            filename=f"{po_number}_drawings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
    else:
        # Return first drawing (could be extended to handle multiple)
        if drawings:
            pdf_bytes = list(drawings.values())[0]
            return StreamingResponse(
                io.BytesIO(pdf_bytes),
                media_type="application/pdf"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate drawings")


@router.post("/custom")
def generate_custom_cad_drawing(
    data: dict,
    download: bool = Query(False, description="Return as downloadable file")
):
    """
    Generate CAD drawing from custom data (no database lookup)
    
    Args:
        data: Dictionary with drawing parameters
        download: If true, return as downloadable file
        
    Returns:
        PDF bytes or file response
    """
    # Validate data
    is_valid, errors = CADDrawingValidator.validate_window_data(data)
    if not is_valid:
        raise HTTPException(status_code=422, detail=f"Invalid drawing data: {errors}")
    
    # Generate PDF
    pdf_bytes = generate_cad_drawing(data)
    
    if download:
        filename = f"Drawing_Custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return FileResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            filename=filename
        )
    else:
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf"
        )


@router.get("/list/windows")
def list_window_drawings(
    project_id: Optional[int] = None,
    db: Session = next(get_db())
):
    """
    List available windows for drawing generation
    
    Args:
        project_id: Optional filter by project
        
    Returns:
        List of windows with drawing-relevant info
    """
    query = db.query(Window)
    
    if project_id:
        query = query.filter(Window.project_id == project_id)
    
    windows = query.all()
    
    return [
        {
            'id': w.id,
            'item_number': w.item_number,
            'room': w.room,
            'dimensions': f"{w.width_inches}\" x {w.height_inches}\"",
            'series': w.frame_series,
            'type': w.window_type,
            'color': w.frame_color
        }
        for w in windows
    ]


@router.get("/list/doors")
def list_door_drawings(
    project_id: Optional[int] = None,
    db: Session = next(get_db())
):
    """
    List available doors for drawing generation
    
    Args:
        project_id: Optional filter by project
        
    Returns:
        List of doors with drawing-relevant info
    """
    query = db.query(Door)
    
    if project_id:
        query = query.filter(Door.project_id == project_id)
    
    doors = query.all()
    
    return [
        {
            'id': d.id,
            'item_number': d.item_number,
            'room': d.room,
            'dimensions': f"{d.width_inches}\" x {d.height_inches}\"",
            'series': d.frame_series,
            'type': d.door_type,
            'color': d.frame_color
        }
        for d in doors
    ]


@router.get("/settings/frame-series")
def get_frame_series_options():
    """Get available frame series options"""
    return {
        'series': ['80', '86', '135'],
        'descriptions': {
            '80': 'Fixed Windows & Single Casement',
            '86': 'Multi-Light Casement & Small Doors',
            '135': 'Patio Doors & Large Sliders'
        }
    }


@router.get("/settings/window-types")
def get_window_type_options():
    """Get available window type options"""
    return {
        'types': [
            'FIXED',
            'SINGLE CASEMENT',
            'DOUBLE CASEMENT',
            'AWNING',
            'PIVOT',
            '2-TRACK SLIDER',
            '3-TRACK SLIDER',
            '4-TRACK SLIDER',
            'ACCORDION'
        ]
    }


@router.get("/settings/door-types")
def get_door_type_options():
    """Get available door type options"""
    return {
        'types': [
            'SWING',
            'FRENCH SWING',
            'BIFOLD',
            '2-TRACK SLIDER',
            '3-TRACK SLIDER',
            '4-TRACK SLIDER',
            'PATIO SLIDER'
        ]
    }


@router.get("/settings/glass-options")
def get_glass_options():
    """Get common glass specification options"""
    return {
        'options': [
            'Clear',
            'Clear - 1/2" Low-E',
            'Clear - 5/8" Low-E',
            'Tempered - 3/8" Low-E',
            'Tempered - 1/2" Low-E',
            'Insulated Low-E',
            'Tinted - Low-E',
            'Reflective - Low-E'
        ]
    }


@router.get("/settings/frame-colors")
def get_frame_color_options():
    """Get available frame color options"""
    return {
        'colors': [
            'Black',
            'Bronze',
            'White',
            'Silver',
            'Tan',
            'Anodized Aluminum',
            'Custom'
        ]
    }
