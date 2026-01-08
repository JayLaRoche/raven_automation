"""
Data transformation for CAD drawing generation
Converts database models and Google Sheets data to CAD drawing parameters
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from app.models import Window, Door, Project


class CADDataTransformer:
    """Transform database models and sheets data to CAD drawing format"""
    
    @staticmethod
    def window_to_cad_data(window: Window, project: Optional[Project] = None) -> Dict[str, Any]:
        """
        Convert Window model to CAD drawing data
        
        Args:
            window: Window model instance
            project: Optional Project instance for context
            
        Returns:
            Dictionary with CAD drawing parameters
        """
        return {
            'item_id': window.item_number,
            'room': window.room,
            'width_inches': float(window.width_inches),
            'height_inches': float(window.height_inches),
            'width_mm': float(window.width_inches) * 25.4,
            'height_mm': float(window.height_inches) * 25.4,
            'series': CADDataTransformer._parse_frame_series(window.frame_series),
            'frame_color': window.frame_color or 'Black',
            'glass': window.glass_type or 'Clear',
            'screen': window.screen_type or 'No Screen',
            'hardware': window.hardware_spec or 'Standard',
            'quantity': window.quantity or 1,
            'salesman': project.salesman if project else '',
            'designer': project.designer if project else '',
            'po_number': project.po_number if project else '',
            'customer_name': project.customer_name if project else '',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'config': CADDataTransformer._parse_window_config(window)
        }
    
    @staticmethod
    def door_to_cad_data(door: Door, project: Optional[Project] = None) -> Dict[str, Any]:
        """
        Convert Door model to CAD drawing data
        
        Args:
            door: Door model instance
            project: Optional Project instance for context
            
        Returns:
            Dictionary with CAD drawing parameters
        """
        return {
            'item_id': door.item_number,
            'room': door.room,
            'width_inches': float(door.width_inches),
            'height_inches': float(door.height_inches),
            'width_mm': float(door.width_inches) * 25.4,
            'height_mm': float(door.height_inches) * 25.4,
            'series': CADDataTransformer._parse_frame_series(door.frame_series),
            'frame_color': door.frame_color or 'Black',
            'glass': door.glass_type or 'Clear',
            'screen': door.screen_type or 'No Screen',
            'hardware': door.hardware_spec or 'Standard',
            'quantity': door.quantity or 1,
            'salesman': project.salesman if project else '',
            'designer': project.designer if project else '',
            'po_number': project.po_number if project else '',
            'customer_name': project.customer_name if project else '',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'config': CADDataTransformer._parse_door_config(door)
        }
    
    @staticmethod
    def _parse_frame_series(series_spec: Optional[str]) -> str:
        """
        Extract frame series number from specification
        
        Args:
            series_spec: Series specification string (e.g. 'Series 80', '80')
            
        Returns:
            Series number as string ('80', '86', '135')
        """
        if not series_spec:
            return '80'
        
        # Remove 'Series' prefix if present
        series_str = series_spec.replace('Series ', '').strip()
        
        # Validate against known series
        valid_series = ['80', '86', '135']
        if series_str in valid_series:
            return series_str
        
        # Default to 80 if unknown
        return '80'
    
    @staticmethod
    def _parse_window_config(window: Window) -> Dict[str, Any]:
        """
        Parse window type to determine configuration
        
        Args:
            window: Window model
            
        Returns:
            Configuration dictionary with type and panel count
        """
        window_type = (window.window_type or '').upper().strip()
        
        config = {
            'type': 'FIXED',
            'panels': 1,
            'swing_direction': window.swing_direction or 'N/A'
        }
        
        # Detect window type
        if 'FIXED' in window_type:
            config['type'] = 'FIXED'
            config['panels'] = 1
            
        elif 'CASEMENT' in window_type:
            config['type'] = 'CASEMENT'
            # Count how many casements mentioned
            if 'DOUBLE' in window_type or 'PAIR' in window_type:
                config['panels'] = 2
            else:
                config['panels'] = 1
            config['swing_direction'] = window.swing_direction or 'Left'
            
        elif 'AWNING' in window_type:
            config['type'] = 'AWNING'
            if 'DOUBLE' in window_type:
                config['panels'] = 2
            else:
                config['panels'] = 1
                
        elif 'PIVOT' in window_type:
            config['type'] = 'PIVOT'
            config['panels'] = 1
            
        elif 'SLIDER' in window_type or 'SLIDING' in window_type:
            config['type'] = 'SLIDER'
            # Extract panel count (e.g., '2-TRACK' -> 2, '4-TRACK' -> 4)
            if '4' in window_type:
                config['panels'] = 4
            elif '3' in window_type:
                config['panels'] = 3
            else:
                config['panels'] = 2
                
        elif 'ACCORDION' in window_type:
            config['type'] = 'ACCORDION'
            config['panels'] = 3  # Default to 3 panels
            
        return config
    
    @staticmethod
    def _parse_door_config(door: Door) -> Dict[str, Any]:
        """
        Parse door type to determine configuration
        
        Args:
            door: Door model
            
        Returns:
            Configuration dictionary with type and panel count
        """
        door_type = (door.door_type or '').upper().strip()
        
        config = {
            'type': 'SLIDER',
            'panels': 1,
            'swing_direction': door.swing_direction or 'N/A'
        }
        
        # Detect door type
        if 'FRENCH' in door_type:
            config['type'] = 'CASEMENT'
            config['panels'] = 2
            
        elif 'SWING' in door_type or 'SWINGING' in door_type:
            config['type'] = 'SWING'
            config['panels'] = 1
            config['swing_direction'] = door.swing_direction or 'In'
            
        elif 'SLIDER' in door_type or 'SLIDING' in door_type:
            config['type'] = 'SLIDER'
            if '4' in door_type:
                config['panels'] = 4
            elif '3' in door_type:
                config['panels'] = 3
            else:
                config['panels'] = 2
                
        elif 'BIFOLD' in door_type:
            config['type'] = 'BIFOLD'
            config['panels'] = 2
            
        return config
    
    @staticmethod
    def from_google_sheets_row(row_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform Google Sheets row directly to CAD drawing data
        
        Args:
            row_data: Dictionary from Google Sheets row
            
        Returns:
            CAD drawing parameters
        """
        return {
            'item_id': row_data.get('Item', ''),
            'room': row_data.get('Room', ''),
            'width_inches': float(row_data.get('Width', 0)),
            'height_inches': float(row_data.get('Height', 0)),
            'width_mm': float(row_data.get('Width', 0)) * 25.4,
            'height_mm': float(row_data.get('Height', 0)) * 25.4,
            'series': CADDataTransformer._parse_frame_series(row_data.get('Frame Series')),
            'frame_color': row_data.get('Frame Color', 'Black'),
            'glass': row_data.get('Glass', 'Clear'),
            'screen': row_data.get('Screen', 'No Screen'),
            'hardware': row_data.get('Hardware', 'Standard'),
            'quantity': int(row_data.get('Qty', 1)),
            'window_type': row_data.get('Type', 'FIXED'),
            'swing_direction': row_data.get('Swing', 'N/A'),
            'salesman': row_data.get('Salesman', ''),
            'designer': row_data.get('Designer', ''),
            'po_number': row_data.get('PO#', ''),
            'customer_name': row_data.get('Customer', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
        }
    
    @staticmethod
    def batch_transform_windows(windows: List[Window], project: Optional[Project] = None) -> List[Dict[str, Any]]:
        """
        Transform multiple windows to CAD data
        
        Args:
            windows: List of Window models
            project: Optional Project instance
            
        Returns:
            List of CAD drawing parameters
        """
        return [CADDataTransformer.window_to_cad_data(w, project) for w in windows]
    
    @staticmethod
    def batch_transform_doors(doors: List[Door], project: Optional[Project] = None) -> List[Dict[str, Any]]:
        """
        Transform multiple doors to CAD data
        
        Args:
            doors: List of Door models
            project: Optional Project instance
            
        Returns:
            List of CAD drawing parameters
        """
        return [CADDataTransformer.door_to_cad_data(d, project) for d in doors]
    
    @staticmethod
    def merge_with_project_metadata(cad_data: Dict[str, Any], project: Project) -> Dict[str, Any]:
        """
        Merge CAD data with project-level metadata
        
        Args:
            cad_data: CAD drawing data dictionary
            project: Project model instance
            
        Returns:
            Enhanced CAD drawing data
        """
        enhanced = cad_data.copy()
        enhanced.update({
            'po_number': project.po_number,
            'customer_name': project.customer_name,
            'salesman': getattr(project, 'salesman', ''),
            'designer': getattr(project, 'designer', ''),
            'billing_address': project.billing_address,
            'shipping_address': project.shipping_address,
        })
        return enhanced


class CADDrawingValidator:
    """Validate CAD drawing data for accuracy and completeness"""
    
    @staticmethod
    def validate_window_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate window CAD data
        
        Args:
            data: CAD drawing data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        required_fields = ['width_inches', 'height_inches', 'series']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate dimensions
        if data.get('width_inches', 0) <= 0:
            errors.append("Width must be positive")
        if data.get('height_inches', 0) <= 0:
            errors.append("Height must be positive")
        
        # Validate series
        valid_series = ['80', '86', '135']
        if data.get('series') not in valid_series:
            errors.append(f"Invalid series: {data.get('series')}")
        
        # Validate configuration
        config = data.get('config', {})
        valid_types = ['FIXED', 'CASEMENT', 'AWNING', 'PIVOT', 'SLIDER', 'ACCORDION']
        if config.get('type') not in valid_types:
            errors.append(f"Invalid configuration type: {config.get('type')}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_door_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Validate door CAD data
        
        Args:
            data: CAD drawing data
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Similar to window validation
        required_fields = ['width_inches', 'height_inches', 'series']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Missing required field: {field}")
        
        if data.get('width_inches', 0) <= 0:
            errors.append("Width must be positive")
        if data.get('height_inches', 0) <= 0:
            errors.append("Height must be positive")
        
        valid_series = ['80', '86', '135']
        if data.get('series') not in valid_series:
            errors.append(f"Invalid series: {data.get('series')}")
        
        return len(errors) == 0, errors
