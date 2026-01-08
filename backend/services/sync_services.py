from sqlalchemy.orm import Session
from typing import Dict, List
from app.models import Project, Window, Door
from .google_sheets_services import GoogleSheetsService
from datetime import datetime


class SyncService:
    """Service for syncing Google Sheets data to PostgreSQL"""
    
    def __init__(self, db: Session, sheets_service: GoogleSheetsService):
        self.db = db
        self.sheets_service = sheets_service
    
    def sync_project(self, po_number: str) -> Dict:
        """
        Sync a project from Google Sheets to the database
        Returns summary of sync operation
        """
        # Fetch data from Google Sheets
        sheets_data = self.sheets_service.parse_project_data(po_number)
        
        if not sheets_data:
            raise ValueError(f"Project with PO '{po_number}' not found in Google Sheets")
        
        # Check if project exists in database
        project = self.db.query(Project).filter(
            Project.po_number == po_number
        ).first()
        
        if project:
            # Update existing project
            project.billing_address = sheets_data['billing_address']
            project.shipping_address = sheets_data['shipping_address']
            project.updated_at = datetime.utcnow()
            
            # Clear old windows and doors (will cascade delete)
            self.db.query(Window).filter(Window.project_id == project.id).delete()
            self.db.query(Door).filter(Door.project_id == project.id).delete()
            
            sync_type = "updated"
        else:
            # Create new project
            project = Project(
                po_number=po_number,
                project_name=po_number,  # Use PO as name for now
                billing_address=sheets_data['billing_address'],
                shipping_address=sheets_data['shipping_address'],
            )
            self.db.add(project)
            self.db.flush()  # Get the project.id
            
            sync_type = "created"
        
        # Add windows
        windows_added = 0
        for window_data in sheets_data['windows']:
            window = Window(
                project_id=project.id,
                **window_data
            )
            self.db.add(window)
            windows_added += 1
        
        # Add doors
        doors_added = 0
        for door_data in sheets_data['doors']:
            door = Door(
                project_id=project.id,
                **door_data
            )
            self.db.add(door)
            doors_added += 1
        
        # Commit all changes
        self.db.commit()
        self.db.refresh(project)
        
        return {
            "sync_type": sync_type,
            "po_number": po_number,
            "project_id": project.id,
            "windows_count": windows_added,
            "doors_count": doors_added,
            "synced_at": project.updated_at.isoformat()
        }
    
    def get_project_from_db(self, po_number: str) -> Dict:
        """Get project data from database"""
        project = self.db.query(Project).filter(
            Project.po_number == po_number
        ).first()
        
        if not project:
            raise ValueError(f"Project '{po_number}' not found in database. Please sync first.")
        
        return {
            "metadata": {
                "id": project.id,
                "po_number": project.po_number,
                "project_name": project.project_name,
                "billing_address": project.billing_address,
                "shipping_address": project.shipping_address,
                "last_synced": project.updated_at.isoformat() if project.updated_at else None,
            },
            "windows": [
                {
                    "id": w.id,
                    "item_number": w.item_number,
                    "room": w.room,
                    "width_inches": float(w.width_inches) if w.width_inches else None,
                    "height_inches": float(w.height_inches) if w.height_inches else None,
                    "window_type": w.window_type,
                    "frame_series": w.frame_series,
                    "swing_direction": w.swing_direction,
                    "quantity": w.quantity,
                    "frame_color": w.frame_color,
                    "glass_type": w.glass_type,
                    "grids": w.grids,
                    "screen": w.screen,
                }
                for w in project.windows
            ],
            "doors": [
                {
                    "id": d.id,
                    "item_number": d.item_number,
                    "room": d.room,
                    "width_inches": float(d.width_inches) if d.width_inches else None,
                    "height_inches": float(d.height_inches) if d.height_inches else None,
                    "door_type": d.door_type,
                    "frame_series": d.frame_series,
                    "swing_direction": d.swing_direction,
                    "quantity": d.quantity,
                    "frame_color": d.frame_color,
                    "glass_type": d.glass_type,
                    "threshold": d.threshold,
                    "sill_pan_depth": float(d.sill_pan_depth) if d.sill_pan_depth else None,
                    "sill_pan_length": float(d.sill_pan_length) if d.sill_pan_length else None,
                }
                for d in project.doors
            ]
        }
        