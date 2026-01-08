"""
Data Transformer Service
Converts database models and Google Sheets data into drawing generator format
"""

from typing import Dict, Optional, Any
from app.models import Window, Door, Project


class DataTransformer:
    """Transform database records into drawing generator parameters"""
    
    @staticmethod
    def window_to_drawing_data(window: Window, project: Project = None) -> Dict[str, Any]:
        """
        Convert Window database model to ProfessionalDrawingGenerator format
        
        Args:
            window: Window model instance from database
            project: Optional Project model for metadata
            
        Returns:
            Dictionary with keys expected by ProfessionalDrawingGenerator.generate_window_drawing()
        """
        
        drawing_data = {
            'item_number': window.item_number or f'W-{window.id}',
            'width_inches': float(window.width_inches or 36),
            'height_inches': float(window.height_inches or 48),
            'window_type': window.window_type or 'Standard',
            'frame_series': window.frame_series or 'Series 6000',
            'swing_direction': window.swing_direction or 'Out',
            'glass_type': window.glass_type or 'Low-E',
            'frame_color': window.frame_color or 'White',
            'quantity': int(window.quantity or 1)
        }
        
        # Optional fields
        if hasattr(window, 'room') and window.room:
            drawing_data['room'] = window.room
        if hasattr(window, 'screen') and window.screen:
            drawing_data['screen'] = window.screen
        if hasattr(window, 'hardware') and window.hardware:
            drawing_data['hardware'] = window.hardware
        
        return drawing_data
    
    @staticmethod
    def door_to_drawing_data(door: Door, project: Project = None) -> Dict[str, Any]:
        """
        Convert Door database model to ProfessionalDrawingGenerator format
        
        Args:
            door: Door model instance from database
            project: Optional Project model for metadata
            
        Returns:
            Dictionary with keys expected by ProfessionalDrawingGenerator.generate_door_drawing()
        """
        
        drawing_data = {
            'item_number': door.item_number or f'D-{door.id}',
            'width_inches': float(door.width_inches or 36),
            'height_inches': float(door.height_inches or 84),
            'window_type': door.door_type or 'Single Swing',
            'frame_series': door.frame_series or 'Series 6000',
            'swing_direction': door.swing_direction or 'Right',
            'glass_type': door.glass_type or 'Clear',
            'frame_color': door.frame_color or 'White',
            'quantity': int(door.quantity or 1)
        }
        
        if hasattr(door, 'room') and door.room:
            drawing_data['room'] = door.room
        if hasattr(door, 'hardware') and door.hardware:
            drawing_data['hardware'] = door.hardware
        
        return drawing_data
    
    @staticmethod
    def project_to_metadata(project: Project) -> Dict[str, str]:
        """
        Convert Project model to drawing metadata
        
        Args:
            project: Project model instance
            
        Returns:
            Dictionary with project metadata for drawings
        """
        return {
            'po_number': project.po_number or 'UNKNOWN',
            'project_name': project.project_name or 'Project',
            'customer_name': project.customer_name or 'Customer',
            'billing_address': project.billing_address or '',
            'shipping_address': project.shipping_address or ''
        }
    
    @staticmethod
    def batch_windows_to_drawing_data(
        windows: list, 
        project: Project = None
    ) -> tuple[list, Dict]:
        """
        Convert list of windows and project to format for batch generation
        
        Args:
            windows: List of Window model instances
            project: Project model for metadata
            
        Returns:
            Tuple of (list of drawing_data dicts, project_metadata dict)
        """
        drawing_items = [DataTransformer.window_to_drawing_data(w, project) for w in windows]
        metadata = DataTransformer.project_to_metadata(project) if project else {}
        return drawing_items, metadata
    
    @staticmethod
    def batch_doors_to_drawing_data(
        doors: list,
        project: Project = None
    ) -> tuple[list, Dict]:
        """
        Convert list of doors and project to format for batch generation
        
        Args:
            doors: List of Door model instances
            project: Project model for metadata
            
        Returns:
            Tuple of (list of drawing_data dicts, project_metadata dict)
        """
        drawing_items = [DataTransformer.door_to_drawing_data(d, project) for d in doors]
        metadata = DataTransformer.project_to_metadata(project) if project else {}
        return drawing_items, metadata
    
    @staticmethod
    def from_google_sheets_row(row: Dict[str, str], item_type: str = 'window') -> Dict[str, Any]:
        """
        Convert Google Sheets row to drawing data format
        
        Args:
            row: Dictionary representing one row from Google Sheets
            item_type: 'window' or 'door'
            
        Returns:
            Drawing data dictionary
        """
        
        # Common mappings
        width = float(row.get('Width', row.get('width', 36)))
        height = float(row.get('Height', row.get('height', 48)))
        
        drawing_data = {
            'item_number': row.get('Item', row.get('item', f'{item_type[0].upper()}-001')),
            'width_inches': width,
            'height_inches': height,
            'frame_series': row.get('Frame Series', row.get('Series', 'Series 6000')),
            'glass_type': row.get('Glass', row.get('glass_type', 'Low-E')),
            'frame_color': row.get('Color', row.get('frame_color', 'White')),
            'quantity': int(row.get('Qty', row.get('quantity', 1)))
        }
        
        if item_type.lower() == 'window':
            drawing_data['window_type'] = row.get('Type', row.get('window_type', 'Standard'))
            drawing_data['swing_direction'] = row.get('Swing', row.get('swing_direction', 'Out'))
        else:
            drawing_data['window_type'] = row.get('Type', row.get('door_type', 'Single Swing'))
            drawing_data['swing_direction'] = row.get('Swing', row.get('swing_direction', 'Right'))
        
        return drawing_data


# Convenience functions
def transform_window(window: Window, project: Project = None) -> Dict:
    """Quick transformation for single window"""
    return DataTransformer.window_to_drawing_data(window, project)


def transform_door(door: Door, project: Project = None) -> Dict:
    """Quick transformation for single door"""
    return DataTransformer.door_to_drawing_data(door, project)


def transform_project(project: Project) -> Dict:
    """Quick transformation for project metadata"""
    return DataTransformer.project_to_metadata(project)
