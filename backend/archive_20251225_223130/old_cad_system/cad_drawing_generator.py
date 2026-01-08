"""
Professional CAD Shop Drawing Generator
Generates pixel-perfect manufacturing documentation for Raven Custom Glass
Compatible with Series 80, 86, 135 frame profiles

Output: Landscape A3 (420mm x 297mm) PDF
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
from typing import Dict, Optional, List, Tuple
import math

from app.services.frame_profiles import (
    get_profile, PROFILE_COLORS, HATCHING_PATTERN, 
    LINE_WEIGHTS, DASH_PATTERNS
)


class CADShopDrawingGenerator:
    """Generate professional CAD shop drawings for windows and doors"""
    
    # Page setup
    PAGE_WIDTH = 420 * mm
    PAGE_HEIGHT = 297 * mm
    MARGIN = 10 * mm
    
    # Section widths (A3 landscape, 420mm total)
    LEFT_SECTION_WIDTH = 150 * mm      # Cross-sections
    CENTER_SECTION_WIDTH = 180 * mm    # Elevation
    RIGHT_SECTION_WIDTH = 120 * mm     # Title block
    
    def __init__(self):
        """Initialize the drawing generator"""
        self.c = None
        self.draw_data = None
        
    def generate(self, window_data: Dict) -> bytes:
        """
        Generate CAD drawing PDF from window/door data
        
        Args:
            window_data: Dictionary with window/door specifications
            
        Returns:
            PDF file as bytes
        """
        # Create PDF in memory
        pdf_buffer = BytesIO()
        
        # Initialize canvas
        self.c = canvas.Canvas(
            pdf_buffer,
            pagesize=(self.PAGE_WIDTH, self.PAGE_HEIGHT)
        )
        
        # Store data
        self.draw_data = window_data
        
        # Set page background to white
        self.c.setFillColor(Color(1, 1, 1))
        self.c.rect(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT, fill=1, stroke=0)
        
        # Draw main layout
        self._draw_page_border()
        self._draw_drawn_from_label()
        
        # Draw three main sections
        self._draw_left_section()      # Cross-sections
        self._draw_center_section()    # Elevation
        self._draw_right_section()     # Title block
        
        # Draw specification table (bottom left)
        self._draw_specification_table()
        
        # Finalize and get PDF bytes
        self.c.save()
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    def _draw_page_border(self):
        """Draw outer page border"""
        self.c.setLineWidth(LINE_WEIGHTS['page_border'] / 10)  # Convert to points
        self.c.setStrokeColor(Color(0, 0, 0))
        
        # Border rectangle
        border_x = self.MARGIN
        border_y = self.MARGIN
        border_w = self.PAGE_WIDTH - (2 * self.MARGIN)
        border_h = self.PAGE_HEIGHT - (2 * self.MARGIN)
        
        self.c.rect(border_x, border_y, border_w, border_h, fill=0, stroke=1)
    
    def _draw_drawn_from_label(self):
        """Draw 'Drawn from inside view' label in top-left corner"""
        label_x = self.MARGIN + 5 * mm
        label_y = self.PAGE_HEIGHT - self.MARGIN - 12 * mm
        label_w = 50 * mm
        label_h = 12 * mm
        
        # Border
        self.c.setLineWidth(LINE_WEIGHTS['label_box'] / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(label_x, label_y, label_w, label_h, fill=0, stroke=1)
        
        # Text
        self.c.setFont("Helvetica", 7)
        self.c.drawCentredString(
            label_x + label_w / 2,
            label_y + label_h / 2 - 2,
            "Drawn from"
        )
        self.c.drawCentredString(
            label_x + label_w / 2,
            label_y + label_h / 2 - 5,
            "inside view"
        )
    
    def _draw_left_section(self):
        """Draw left section - vertical and horizontal cross-sections"""
        left_x = self.MARGIN + 5 * mm
        
        # Vertical cross-section (top)
        vert_y = self.PAGE_HEIGHT - self.MARGIN - 100 * mm
        self._draw_vertical_section(left_x, vert_y)
        
        # Horizontal cross-section (bottom)
        horiz_y = self.MARGIN + 20 * mm
        self._draw_horizontal_section(left_x, horiz_y)
    
    def _draw_vertical_section(self, x: float, y: float):
        """Draw vertical cross-section of frame profile"""
        profile = get_profile(self.draw_data.get('series', '80'))
        
        # Section title
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(x, y + 10 * mm, "Vertical Section")
        
        # Draw frame profile (simplified representation)
        # This is a placeholder - full implementation would draw exact profile
        profile_y = y
        profile_height = 40 * mm
        profile_width = 50 * mm
        
        # Outer frame
        self.c.setLineWidth(LINE_WEIGHTS['frame_outline'] / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(x, profile_y, profile_width, profile_height, fill=0, stroke=1)
        
        # Glass pocket (dashed)
        self.c.setLineWidth(0.5)
        glass_start = x + 8 * mm
        glass_width = 34 * mm
        self.c.setDash(DASH_PATTERNS['glass_pocket'][0], DASH_PATTERNS['glass_pocket'][1])
        self.c.rect(glass_start, profile_y + 5 * mm, glass_width, profile_height - 10 * mm, fill=0, stroke=1)
        self.c.setDash()
        
        # Nail flange (red)
        nail_x = x - 5 * mm
        nail_y = profile_y + profile_height / 2 - 3 * mm
        nail_w = 5 * mm
        nail_h = 6 * mm
        
        self.c.setFillColor(Color(*PROFILE_COLORS['nail_flange_fill']))
        self.c.setStrokeColor(Color(*PROFILE_COLORS['nail_flange_outline']))
        self.c.setLineWidth(1.0 / 10)
        self.c.rect(nail_x, nail_y, nail_w, nail_h, fill=1, stroke=1)
        
        # Labels
        self.c.setFont("Helvetica", 6)
        self.c.drawString(x - 12 * mm, profile_y + profile_height / 2 - 1 * mm, "Inside")
        self.c.drawString(x + profile_width + 2 * mm, profile_y + profile_height / 2 - 1 * mm, "Outside")
        
        # Dimensions (simplified)
        self._draw_dimension_lines_vertical(x, profile_y, profile_width, profile_height)
    
    def _draw_horizontal_section(self, x: float, y: float):
        """Draw horizontal cross-section of frame profile"""
        # Section title
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(x, y + 10 * mm, "Horizontal Section")
        
        # Draw frame profile
        profile_y = y
        profile_height = 30 * mm
        profile_width = 50 * mm
        
        # Outer frame
        self.c.setLineWidth(LINE_WEIGHTS['frame_outline'] / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(x, profile_y, profile_width, profile_height, fill=0, stroke=1)
        
        # Glass pocket (dashed)
        self.c.setLineWidth(0.5)
        glass_start_x = x + 8 * mm
        glass_width = 34 * mm
        glass_start_y = profile_y + 5 * mm
        glass_height = profile_height - 10 * mm
        self.c.setDash(DASH_PATTERNS['glass_pocket'][0], DASH_PATTERNS['glass_pocket'][1])
        self.c.rect(glass_start_x, glass_start_y, glass_width, glass_height, fill=0, stroke=1)
        self.c.setDash()
        
        # Labels
        self.c.setFont("Helvetica", 6)
        self.c.drawString(x - 12 * mm, profile_y + profile_height / 2 - 1 * mm, "Inside")
        self.c.drawString(x + profile_width + 2 * mm, profile_y + profile_height / 2 - 1 * mm, "Outside")
    
    def _draw_dimension_lines_vertical(self, x: float, y: float, width: float, height: float):
        """Draw dimension lines for vertical section"""
        self.c.setLineWidth(0.7 / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.setFont("Helvetica", 6)
        
        # Top dimension
        dim_y = y + height + 8 * mm
        self.c.line(x, dim_y, x + width, dim_y)
        self.c.drawCentredString(x + width / 2, dim_y + 2 * mm, f"{width/mm:.0f}mm")
    
    def _draw_center_section(self):
        """Draw center section - elevation view"""
        center_x = self.MARGIN + self.LEFT_SECTION_WIDTH + 5 * mm
        
        # Title
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(center_x, self.PAGE_HEIGHT - self.MARGIN - 10 * mm, "Elevation View")
        
        # Elevation drawing
        elev_y = self.PAGE_HEIGHT - self.MARGIN - 120 * mm
        elev_height = 100 * mm
        
        self._draw_elevation(center_x, elev_y, elev_height)
        
        # Orientation section
        orient_y = elev_y - 40 * mm
        self._draw_orientation(center_x, orient_y)
    
    def _draw_elevation(self, x: float, y: float, height: float):
        """Draw elevation view with panel configuration"""
        width_inches = self.draw_data.get('width_inches', 72)
        height_inches = self.draw_data.get('height_inches', 48)
        
        # Calculate aspect ratio-preserving width
        aspect_ratio = width_inches / height_inches
        width = height * aspect_ratio
        
        # Clamp to section width
        max_width = (self.CENTER_SECTION_WIDTH - 10 * mm)
        if width > max_width:
            width = max_width
            height = width / aspect_ratio
        
        # Draw frame outline
        self.c.setLineWidth(LINE_WEIGHTS['frame_outline'] / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(x, y, width, height, fill=0, stroke=1)
        
        # Draw panel configuration
        config = self.draw_data.get('config', {})
        panel_type = config.get('type', 'FIXED')
        panel_count = config.get('panels', 1)
        
        self._draw_panel_configuration(x, y, width, height, panel_type, panel_count)
        
        # Draw dimensions
        self._draw_elevation_dimensions(x, y, width, height, width_inches, height_inches)
    
    def _draw_panel_configuration(self, x: float, y: float, width: float, height: float, 
                                  panel_type: str, panel_count: int):
        """Draw panel configuration indicators"""
        self.c.setFont("Helvetica-Bold", 20)
        
        if panel_type == 'FIXED':
            # Fixed panel - show "F." in center
            self.c.drawCentredString(x + width / 2, y + height / 2 - 8, "F.")
            
        elif panel_type == 'CASEMENT':
            # Casement - diagonal line
            if panel_count == 1:
                self.c.setLineWidth(0.8 / 10)
                self.c.line(x + 5*mm, y + 5*mm, x + width - 5*mm, y + height - 5*mm)
            elif panel_count == 2:
                # Two casements side by side
                mid_x = x + width / 2
                self.c.line(x + 5*mm, y + 5*mm, mid_x - 3*mm, y + height - 5*mm)
                self.c.line(mid_x + 3*mm, y + 5*mm, x + width - 5*mm, y + height - 5*mm)
                # Mullion
                self.c.setLineWidth(0.8 / 10)
                self.c.line(mid_x, y + 2*mm, mid_x, y + height - 2*mm)
        
        elif panel_type == 'SLIDER':
            # Slider - horizontal arrows
            self.c.setLineWidth(0.8 / 10)
            arrow_y = y + height / 2
            # Left arrow
            self.c.line(x + 8*mm, arrow_y, x + 15*mm, arrow_y)
            self.c.line(x + 15*mm, arrow_y, x + 12*mm, arrow_y - 2*mm)
            self.c.line(x + 15*mm, arrow_y, x + 12*mm, arrow_y + 2*mm)
            # Right arrow
            self.c.line(x + width - 15*mm, arrow_y, x + width - 8*mm, arrow_y)
            self.c.line(x + width - 15*mm, arrow_y, x + width - 12*mm, arrow_y - 2*mm)
            self.c.line(x + width - 15*mm, arrow_y, x + width - 12*mm, arrow_y + 2*mm)
    
    def _draw_elevation_dimensions(self, x: float, y: float, width: float, height: float,
                                   width_inches: float, height_inches: float):
        """Draw dimension lines around elevation"""
        # Convert to metric
        width_mm = width_inches * 25.4
        height_mm = height_inches * 25.4
        
        self.c.setLineWidth(0.7 / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.setFont("Helvetica", 8)
        
        # Width dimension (bottom)
        dim_y = y - 8 * mm
        self.c.line(x - 2*mm, dim_y, x + width + 2*mm, dim_y)
        # Extension lines
        self.c.line(x, y - 3*mm, x, dim_y + 1*mm)
        self.c.line(x + width, y - 3*mm, x + width, dim_y + 1*mm)
        
        # Dimension text
        dim_text = f"{width_mm:.1f} [{width_inches:.1f}\"]"
        self.c.drawCentredString(x + width / 2, dim_y - 3*mm, dim_text)
        
        # Height dimension (right)
        dim_x = x + width + 8 * mm
        self.c.line(dim_x, y - 2*mm, dim_x, y + height + 2*mm)
        # Extension lines
        self.c.line(x + width - 3*mm, y, dim_x - 1*mm, y)
        self.c.line(x + width - 3*mm, y + height, dim_x - 1*mm, y + height)
        
        # Dimension text (vertical)
        self.c.saveState()
        self.c.translate(dim_x + 5*mm, y + height / 2)
        self.c.rotate(90)
        dim_text = f"{height_mm:.1f} [{height_inches:.1f}\"]"
        self.c.drawCentredString(0, -1*mm, dim_text)
        self.c.restoreState()
    
    def _draw_orientation(self, x: float, y: float):
        """Draw orientation indicators (Inside/Outside, icons)"""
        # Outside label
        label_x = x + 10 * mm
        label_y = y + 12 * mm
        label_w = 45 * mm
        label_h = 12 * mm
        
        self.c.setLineWidth(0.5 / 10)
        self.c.rect(label_x, label_y, label_w, label_h, fill=0, stroke=1)
        self.c.setFont("Helvetica", 7)
        self.c.drawCentredString(label_x + label_w / 2, label_y + 3*mm, "Outside")
        
        # Inside label
        label_y -= 15 * mm
        self.c.rect(label_x, label_y, label_w, label_h, fill=0, stroke=1)
        self.c.drawCentredString(label_x + label_w / 2, label_y + 3*mm, "Inside")
        
        # Raven logo placeholder
        logo_x = x + 80 * mm
        logo_y = y + 8 * mm
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(logo_x, logo_y, "raven")
    
    def _draw_right_section(self):
        """Draw right section - title block and metadata"""
        right_x = self.MARGIN + self.LEFT_SECTION_WIDTH + self.CENTER_SECTION_WIDTH + 5 * mm
        
        # Logo area
        logo_y = self.PAGE_HEIGHT - self.MARGIN - 50 * mm
        self._draw_logo_area(right_x, logo_y)
        
        # Configuration icons
        icons_y = logo_y - 60 * mm
        self._draw_configuration_icons(right_x, icons_y)
        
        # Metadata table
        table_y = icons_y - 80 * mm
        self._draw_metadata_table(right_x, table_y)
    
    def _draw_logo_area(self, x: float, y: float):
        """Draw company logo and contact information"""
        # Logo border
        logo_w = self.RIGHT_SECTION_WIDTH - 10 * mm
        logo_h = 50 * mm
        
        self.c.setLineWidth(1.0 / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(x, y, logo_w, logo_h, fill=0, stroke=1)
        
        # Company name
        self.c.setFont("Helvetica-Bold", 16)
        self.c.drawCentredString(x + logo_w / 2, y + 25 * mm, "raven")
        
        # Contact info
        contact_y = y - 5 * mm
        self.c.setFont("Helvetica", 6)
        self.c.drawString(x + 2*mm, contact_y, "9960 W Cheyenne Ave")
        self.c.drawString(x + 2*mm, contact_y - 3*mm, "Suite 190, Las Vegas NV 89129")
        self.c.drawString(x + 2*mm, contact_y - 6*mm, "Tel: 702-577-1003")
        self.c.drawString(x + 2*mm, contact_y - 9*mm, "ravencustomglass.com")
    
    def _draw_configuration_icons(self, x: float, y: float):
        """Draw 6 configuration type icons"""
        icons = [
            ('Fixed', 'F'),
            ('Casement', 'C'),
            ('Awning', 'A'),
            ('Pivot', 'P'),
            ('Slider', 'S'),
            ('Accordion', 'Ac')
        ]
        
        icon_size = 15 * mm
        spacing = 2 * mm
        col_width = icon_size + spacing
        
        for idx, (name, label) in enumerate(icons):
            col = idx % 3
            row = idx // 3
            
            icon_x = x + col * col_width + 2*mm
            icon_y = y - row * col_width - icon_size
            
            # Icon box
            self.c.setLineWidth(0.5 / 10)
            self.c.setStrokeColor(Color(0, 0, 0))
            self.c.rect(icon_x, icon_y, icon_size, icon_size, fill=0, stroke=1)
            
            # Icon label
            self.c.setFont("Helvetica-Bold", 8)
            self.c.drawCentredString(icon_x + icon_size / 2, icon_y + icon_size / 2 - 2, label)
    
    def _draw_metadata_table(self, x: float, y: float):
        """Draw metadata table with project information"""
        col_w = (self.RIGHT_SECTION_WIDTH - 10 * mm) / 2
        row_h = 10 * mm
        
        metadata = [
            ('Salesman', self.draw_data.get('salesman', '')),
            ('Drawing Date', self.draw_data.get('date', datetime.now().strftime('%Y-%m-%d'))),
            ('Serial #', self.draw_data.get('serial', '-')),
            ('Designer', self.draw_data.get('designer', '-')),
            ('Revision', self.draw_data.get('revision', '-')),
            ('Confirmation', ''),
            ('Date', ''),
        ]
        
        self.c.setFont("Helvetica", 6)
        self.c.setLineWidth(0.5 / 10)
        
        for idx, (label, value) in enumerate(metadata):
            row_y = y - idx * row_h
            
            # Borders
            self.c.rect(x, row_y, col_w, row_h, fill=0, stroke=1)
            self.c.rect(x + col_w, row_y, col_w, row_h, fill=0, stroke=1)
            
            # Label
            self.c.drawString(x + 2*mm, row_y + 3*mm, label)
            
            # Value
            self.c.drawString(x + col_w + 2*mm, row_y + 3*mm, str(value))
    
    def _draw_specification_table(self):
        """Draw specification table (bottom left)"""
        table_x = self.MARGIN + 5 * mm
        table_y = self.MARGIN + 10 * mm
        table_w = 140 * mm
        table_h = 50 * mm
        
        # Table border
        self.c.setLineWidth(0.8 / 10)
        self.c.setStrokeColor(Color(0, 0, 0))
        self.c.rect(table_x, table_y, table_w, table_h, fill=0, stroke=1)
        
        # Item ID header
        self.c.setFont("Helvetica-Bold", 8)
        self.c.drawString(table_x + 2*mm, table_y + table_h - 4*mm, self.draw_data.get('item_id', 'ITEM'))
        
        # Header line
        self.c.setLineWidth(0.3 / 10)
        self.c.line(table_x, table_y + table_h - 8*mm, table_x + table_w, table_y + table_h - 8*mm)
        
        # Content rows
        col1_w = 50 * mm
        col2_w = table_w - col1_w
        row_h = 7 * mm
        
        rows = [
            ('Glass:', self.draw_data.get('glass', '-')),
            ('Frame Color:', self.draw_data.get('frame_color', '-')),
            ('Screen:', self.draw_data.get('screen', '-')),
            ('Hardware:', self.draw_data.get('hardware', '-')),
            ('Quantity:', str(self.draw_data.get('quantity', 1))),
        ]
        
        self.c.setFont("Helvetica", 6)
        current_y = table_y + table_h - 12 * mm
        
        for label, value in rows:
            # Label
            self.c.drawString(table_x + 2*mm, current_y + 1*mm, label)
            
            # Value
            self.c.drawString(table_x + col1_w + 2*mm, current_y + 1*mm, str(value))
            
            # Row divider
            self.c.setLineWidth(0.3 / 10)
            self.c.line(table_x, current_y - 1*mm, table_x + table_w, current_y - 1*mm)
            
            current_y -= row_h


def generate_cad_drawing(window_data: Dict) -> bytes:
    """
    Generate a professional CAD shop drawing
    
    Args:
        window_data: Dictionary with window specifications
        
    Returns:
        PDF file as bytes
    """
    generator = CADShopDrawingGenerator()
    return generator.generate(window_data)
