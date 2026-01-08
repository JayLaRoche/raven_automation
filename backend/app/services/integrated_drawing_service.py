"""
Integrated Drawing Service
Wrapper around ProfessionalDrawingGenerator with database integration
"""

import os
from typing import Dict, Optional, List, Tuple
from pathlib import Path
from datetime import datetime

from services.drawing_engine import ProfessionalDrawingGenerator
from app.services.data_transformer import DataTransformer
from app.models import Window, Door, Project


class IntegratedDrawingService:
    """
    Complete drawing generation service integrating:
    - Professional drawing engine (Phase 1)
    - Database models
    - Data transformation
    - File management
    """
    
    def __init__(self, output_dir: str = "./drawings"):
        """
        Initialize the drawing service
        
        Args:
            output_dir: Directory to save generated PDFs
        """
        self.output_dir = output_dir
        self.generator = ProfessionalDrawingGenerator(output_dir)
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_window_from_model(
        self,
        window: Window,
        project: Project = None,
        filename: str = None
    ) -> str:
        """
        Generate drawing from Window database model
        
        Args:
            window: Window model instance
            project: Optional Project model for metadata
            filename: Optional custom filename
            
        Returns:
            Path to generated PDF file
        """
        # Transform data
        window_data = DataTransformer.window_to_drawing_data(window, project)
        project_data = DataTransformer.project_to_metadata(project) if project else {
            'po_number': 'UNKNOWN',
            'project_name': 'Project',
            'customer_name': 'Customer'
        }
        
        # Generate filename if not provided
        if filename is None:
            po = project_data['po_number'].replace(' ', '-')[:15]
            item = window_data['item_number']
            filename = f"{po}_Window-{item}_ELEV.pdf"
        
        # Generate drawing
        pdf_path = self.generator.generate_window_drawing(
            window_data,
            project_data,
            filename
        )
        
        return pdf_path
    
    def generate_door_from_model(
        self,
        door: Door,
        project: Project = None,
        filename: str = None
    ) -> str:
        """
        Generate drawing from Door database model
        
        Args:
            door: Door model instance
            project: Optional Project model for metadata
            filename: Optional custom filename
            
        Returns:
            Path to generated PDF file
        """
        # Transform data
        door_data = DataTransformer.door_to_drawing_data(door, project)
        project_data = DataTransformer.project_to_metadata(project) if project else {
            'po_number': 'UNKNOWN',
            'project_name': 'Project',
            'customer_name': 'Customer'
        }
        
        # Generate filename if not provided
        if filename is None:
            po = project_data['po_number'].replace(' ', '-')[:15]
            item = door_data['item_number']
            filename = f"{po}_Door-{item}_ELEV.pdf"
        
        # Generate drawing
        pdf_path = self.generator.generate_door_drawing(
            door_data,
            project_data,
            filename
        )
        
        return pdf_path
    
    def generate_project_drawings(
        self,
        project: Project,
        windows: List[Window] = None,
        doors: List[Door] = None
    ) -> Dict[str, List[str]]:
        """
        Generate all drawings for a project
        
        Args:
            project: Project model instance
            windows: List of Window models (if None, uses project.windows)
            doors: List of Door models (if None, uses project.doors)
            
        Returns:
            Dictionary with 'windows' and 'doors' lists of PDF paths
        """
        result = {'windows': [], 'doors': []}
        
        # Use provided lists or get from project
        windows = windows or (project.windows if hasattr(project, 'windows') else [])
        doors = doors or (project.doors if hasattr(project, 'doors') else [])
        
        # Generate window drawings
        for window in windows:
            try:
                pdf_path = self.generate_window_from_model(window, project)
                result['windows'].append(pdf_path)
            except Exception as e:
                print(f"Error generating window {window.item_number}: {e}")
        
        # Generate door drawings
        for door in doors:
            try:
                pdf_path = self.generate_door_from_model(door, project)
                result['doors'].append(pdf_path)
            except Exception as e:
                print(f"Error generating door {door.item_number}: {e}")
        
        return result
    
    def generate_from_google_sheets_row(
        self,
        row: Dict,
        item_type: str = 'window',
        project_data: Dict = None,
        filename: str = None
    ) -> str:
        """
        Generate drawing directly from Google Sheets row data
        
        Args:
            row: Dictionary representing Google Sheets row
            item_type: 'window' or 'door'
            project_data: Optional project metadata dictionary
            filename: Optional custom filename
            
        Returns:
            Path to generated PDF file
        """
        # Transform data
        item_data = DataTransformer.from_google_sheets_row(row, item_type)
        
        if project_data is None:
            project_data = {
                'po_number': 'SHEETS',
                'project_name': 'Google Sheets',
                'customer_name': 'Customer'
            }
        
        # Generate filename if not provided
        if filename is None:
            po = project_data['po_number'].replace(' ', '-')[:15]
            item = item_data['item_number']
            item_type_short = 'Window' if item_type.lower() == 'window' else 'Door'
            filename = f"{po}_{item_type_short}-{item}_ELEV.pdf"
        
        # Generate drawing
        if item_type.lower() == 'window':
            pdf_path = self.generator.generate_window_drawing(
                item_data,
                project_data,
                filename
            )
        else:
            pdf_path = self.generator.generate_door_drawing(
                item_data,
                project_data,
                filename
            )
        
        return pdf_path
    
    def list_generated_drawings(self) -> Dict[str, List[str]]:
        """
        List all PDF files in the output directory
        
        Returns:
            Dictionary with 'all' (all PDFs) and 'recent' (last 10)
        """
        pdf_dir = Path(self.output_dir)
        
        if not pdf_dir.exists():
            return {'all': [], 'recent': []}
        
        all_pdfs = sorted(
            pdf_dir.glob('*.pdf'),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        return {
            'all': [str(p) for p in all_pdfs],
            'recent': [str(p) for p in all_pdfs[:10]]
        }
    
    def delete_drawing(self, filename: str) -> bool:
        """
        Delete a generated drawing file
        
        Args:
            filename: Name of PDF file to delete
            
        Returns:
            True if deleted, False if not found
        """
        pdf_path = Path(self.output_dir) / filename
        
        if pdf_path.exists():
            pdf_path.unlink()
            return True
        
        return False


# Global service instance
_drawing_service: Optional[IntegratedDrawingService] = None


def get_drawing_service(output_dir: str = "./drawings") -> IntegratedDrawingService:
    """
    Get or create the global drawing service instance
    
    Args:
        output_dir: Directory for PDF output (only used on first call)
        
    Returns:
        IntegratedDrawingService instance
    """
    global _drawing_service
    
    if _drawing_service is None:
        _drawing_service = IntegratedDrawingService(output_dir)
    
    return _drawing_service
