"""
Visual Template Generator
Loads and applies layout templates to drawing generation
"""

import json
from pathlib import Path
from typing import Dict, Optional


class VisualTemplateGenerator:
    """
    Manages visual templates and applies them to drawing generation
    """
    
    def __init__(self, template_path: str = None):
        """
        Initialize with a template file
        
        Args:
            template_path: Path to JSON template file
        """
        self.template = None
        if template_path:
            self.load_template(template_path)
    
    def load_template(self, template_path: str) -> Dict:
        """
        Load a template from JSON file
        
        Args:
            template_path: Path to template file
        
        Returns:
            Template dictionary
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = json.load(f)
        
        print(f"✓ Loaded template: {self.template.get('template_name', 'Unknown')}")
        return self.template
    
    def get_page_config(self) -> Dict:
        """Get page format configuration"""
        if not self.template:
            # Default fallback
            return {
                "format": "A3_landscape",
                "width_mm": 420,
                "height_mm": 297
            }
        return self.template.get("page", {})
    
    def get_zone_config(self, zone_name: str) -> Optional[Dict]:
        """
        Get configuration for a specific zone
        
        Args:
            zone_name: Name of zone (e.g., 'left_column', 'center_column')
        
        Returns:
            Zone configuration dict or None
        """
        if not self.template:
            return None
        
        zones = self.template.get("zones", {})
        return zones.get(zone_name)
    
    def get_all_zones(self) -> Dict:
        """Get all zone configurations"""
        if not self.template:
            return {}
        return self.template.get("zones", {})
    
    def get_styling_rules(self) -> Dict:
        """Get visual styling rules"""
        if not self.template:
            return {
                "line_weights": {"thick": 1.5, "medium": 1.0, "thin": 0.5},
                "colors": {"primary": "black", "accent": "red", "fill": "lightgray"}
            }
        return self.template.get("styling", {})
    
    def get_text_hierarchy(self) -> Dict:
        """Get text size hierarchy"""
        if not self.template:
            return {
                "title": 12,
                "heading": 10,
                "body": 8,
                "small": 6
            }
        text_layout = self.template.get("text_layout", {})
        return text_layout.get("hierarchy", {})
    
    def get_drawing_conventions(self) -> Dict:
        """Get drawing conventions for panel indicators, etc."""
        if not self.template:
            return {
                "panel_indicators": {
                    "fixed": "text_F_centered",
                    "casement": "diagonal_line_from_hinge",
                    "slider": "bidirectional_arrows"
                }
            }
        return self.template.get("drawing_conventions", {})
    
    def get_element_config(self, element_type: str) -> Optional[Dict]:
        """
        Get configuration for a specific visual element
        
        Args:
            element_type: Type of element (e.g., 'elevation', 'cross_section')
        
        Returns:
            Element configuration or None
        """
        if not self.template:
            return None
        
        elements = self.template.get("visual_elements", {})
        return elements.get(element_type)
    
    def apply_to_matplotlib_layout(self, fig, layout):
        """
        Apply template styling to a matplotlib figure
        
        Args:
            fig: Matplotlib figure
            layout: DrawingLayout instance
        """
        styling = self.get_styling_rules()
        
        # Apply any global styling
        # This is a placeholder for future enhancements
        pass
    
    def get_zone_proportions(self) -> Dict:
        """
        Get zone width proportions for layout
        
        Returns:
            Dictionary with left, center, right percentages
        """
        zones = self.get_all_zones()
        
        left = zones.get('left_column', {}).get('width_percent', 30)
        center = zones.get('center_column', {}).get('width_percent', 45)
        right = zones.get('right_column', {}).get('width_percent', 25)
        
        # Normalize to sum to 100
        total = left + center + right
        if total > 0:
            left = (left / total) * 100
            center = (center / total) * 100
            right = (right / total) * 100
        
        return {
            "left": left / 100,  # Convert to ratio
            "center": center / 100,
            "right": right / 100
        }


def load_template(template_path: str) -> VisualTemplateGenerator:
    """
    Convenience function to load a template
    
    Args:
        template_path: Path to template JSON file
    
    Returns:
        VisualTemplateGenerator instance
    """
    return VisualTemplateGenerator(template_path)


def create_default_template(output_path: str):
    """
    Create a default template file
    
    Args:
        output_path: Where to save the template
    """
    default_template = {
        "template_name": "Raven_Standard_Layout",
        "page": {
            "format": "A3_landscape",
            "width_mm": 420,
            "height_mm": 297,
            "orientation": "landscape"
        },
        "zones": {
            "left_column": {
                "x_percent": 0,
                "y_percent": 0,
                "width_percent": 30,
                "height_percent": 100,
                "contains": ["cross_sections", "spec_table"]
            },
            "center_column": {
                "x_percent": 30,
                "y_percent": 0,
                "width_percent": 45,
                "height_percent": 100,
                "contains": ["elevation_view", "dimensions"]
            },
            "right_column": {
                "x_percent": 75,
                "y_percent": 0,
                "width_percent": 25,
                "height_percent": 100,
                "contains": ["title_block", "metadata", "icons"]
            }
        },
        "visual_elements": {
            "cross_section": {
                "type": "technical_profile",
                "location": "left_column_top",
                "style": "outlined_shape"
            },
            "elevation": {
                "type": "window_outline",
                "location": "center",
                "style": "frame_with_panels"
            },
            "spec_table": {
                "type": "data_table",
                "location": "left_column_bottom",
                "style": "bordered_cells"
            }
        },
        "styling": {
            "line_weights": {
                "thick": 1.5,
                "medium": 1.0,
                "thin": 0.5
            },
            "colors": {
                "primary": "black",
                "accent": "red",
                "fill": "lightgray"
            }
        },
        "text_layout": {
            "hierarchy": {
                "title": 12,
                "heading": 10,
                "body": 8,
                "small": 6
            }
        },
        "drawing_conventions": {
            "panel_indicators": {
                "fixed": "text_F_centered",
                "casement": "diagonal_line_from_hinge",
                "slider": "bidirectional_arrows",
                "awning": "horizontal_pivot_line"
            }
        }
    }
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(default_template, f, indent=2)
    
    print(f"✓ Created default template: {output_file}")
    return output_file
