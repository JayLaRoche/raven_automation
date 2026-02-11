"""Reference Layout Shop Drawing Generator - CLIENT-SIDE CAPTURE
Generates professional shop drawings using client-side canvas capture
Output: A4 Landscape PDF (297mm x 210mm)

This version accepts a Base64-encoded image from the frontend canvas
and embeds it directly into a PDF, ensuring 100% match with what the user sees.
"""

import io
import base64
import logging
from typing import Dict, Optional
import os
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle, Circle

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.utils import ImageReader

logger = logging.getLogger(__name__)


class ReferenceShopDrawingGenerator:
    """
    Generate professional A4 LANDSCAPE shop drawings using client-side capture
    
    Dimensions: 297mm × 210mm (A4 Landscape)
    """
    
    def __init__(self, db_connection=None, parameters: Dict = None):
        """Initialize drawing generator"""
        self.db = db_connection
        self.params = parameters or {}
        
        # A4 LANDSCAPE dimensions (CORRECTED)
        self.page_width_mm = 297
        self.page_height_mm = 210
        self.page_width_in = 11.69
        self.page_height_in = 8.27
        
        # Margins and layout
        self.margin_mm = 8
        self.dpi = 300
    
    def generate_pdf(self) -> io.BytesIO:
        """Generate PDF from client-side captured canvas image"""
        logger.info("Generating PDF from canvas snapshot with params: %s", self.params)
        
        try:
            # Check for imageSnapshot parameter
            image_snapshot = self.params.get('imageSnapshot')
            if not image_snapshot:
                raise ValueError("Missing imageSnapshot parameter - frontend must capture canvas")
            
            # Decode Base64 image
            # Format: "data:image/png;base64,iVBORw0KG..."
            logger.debug("Decoding Base64 image (length: %d)", len(image_snapshot))
            
            if ',' in image_snapshot:
                # Strip the data URL prefix
                image_data_base64 = image_snapshot.split(',')[1]
            else:
                # Already raw Base64
                image_data_base64 = image_snapshot
            
            try:
                image_bytes = base64.b64decode(image_data_base64)
                logger.debug("Decoded image bytes: %d", len(image_bytes))
            except Exception as decode_error:
                logger.error("Failed to decode Base64 image: %s", str(decode_error))
                raise ValueError(f"Invalid Base64 image data: {str(decode_error)}")
            
            # Create PDF buffer
            pdf_buffer = io.BytesIO()
            page_width, page_height = landscape(A4)  # 842 x 595 points
            
            logger.debug("Creating PDF canvas (%.1f x %.1f points)", page_width, page_height)
            c = rl_canvas.Canvas(pdf_buffer, pagesize=landscape(A4))
            
            # Create ImageReader from bytes
            try:
                img_buffer = io.BytesIO(image_bytes)
                img = ImageReader(img_buffer)
                logger.debug("Image loaded successfully")
            except Exception as img_error:
                logger.error("Failed to load image: %s", str(img_error))
                raise ValueError(f"Invalid image format: {str(img_error)}")
            
            # Draw image to fill the page (maintaining aspect ratio)
            # A4 Landscape is 842 x 595 points
            try:
                c.drawImage(img, 0, 0, 
                           width=page_width, 
                           height=page_height, 
                           preserveAspectRatio=True,
                           anchor='c')  # Center anchor
                logger.debug("Image drawn to canvas")
            except Exception as draw_error:
                logger.error("Failed to draw image: %s", str(draw_error))
                raise RuntimeError(f"Failed to embed image in PDF: {str(draw_error)}")
            
            # Finalize PDF
            c.save()
            pdf_buffer.seek(0)
            
            # Validate PDF size
            pdf_data = pdf_buffer.getvalue()
            file_size = len(pdf_data)
            
            if file_size == 0:
                raise RuntimeError("Generated PDF is empty")
            
            logger.info("PDF generated successfully (%d bytes)", file_size)
            return io.BytesIO(pdf_data)
            
        except ValueError as e:
            logger.warning("Validation error in PDF generation: %s", str(e))
            raise
        except Exception as e:
            logger.error("Error generating shop drawing: %s", str(e), exc_info=True)
            raise RuntimeError(f"PDF generation failed: {str(e)}")
        """Draw entire A4 landscape layout"""
        
        w = self.page_width_mm  # 297
        h = self.page_height_mm  # 210
        m = self.margin_mm
        
        # Page border
        border = Rectangle((0, 0), w, h, linewidth=1, edgecolor='black', 
                          facecolor='white', zorder=0)
        ax.add_patch(border)
        
        # 1. HEADER (top ~28mm)
        header_y = h - 28
        self._draw_header(ax, header_y, w)
        
        # 2. MAIN CONTENT AREA
        main_y_top = header_y - 5
        main_y_bottom = 45  # Leave room for specs table
        main_height = main_y_top - main_y_bottom
        
        # Three columns
        col_width = (w - 2*m - 4) / 3
        
        # Column 1: Frames
        col1_x = m
        self._draw_column1_frames(ax, col1_x, main_y_bottom, col_width, main_height)
        
        # Column 2: Elevation & Plan
        col2_x = col1_x + col_width + 2
        self._draw_column2_elevation_plan(ax, col2_x, main_y_bottom, col_width, main_height)
        
        # Column 3: Icons & Info
        col3_x = col2_x + col_width + 2
        self._draw_column3_info(ax, col3_x, main_y_bottom, col_width, main_height)
        
        # 3. SPECIFICATIONS TABLE (bottom ~40mm)
        self._draw_specifications_table(ax, m, 0, w - 2*m, 40)
    
    def _draw_header(self, ax, y, width):
        """Draw header section"""
        
        # Header background
        header = Rectangle((0, y), width, 28, linewidth=0.5, 
                          edgecolor='black', facecolor='#F5F5F5')
        ax.add_patch(header)
        
        # Left: "Drawn from inside view"
        ax.text(8, y + 14, 'Drawn from inside view', 
               fontsize=8, fontweight='bold', va='center')
        
        # Right: Company info
        company_x = width - 50
        ax.text(company_x, y + 20, 'RAVEN', fontsize=10, fontweight='bold', va='top')
        ax.text(company_x, y + 16, 'Custom Glass', fontsize=7, va='top')
        ax.text(company_x, y + 12, 'Sales & Service', fontsize=6, va='top', style='italic')
        
        # Separator line
        ax.plot([0, width], [y - 0.5, y - 0.5], 'k-', linewidth=1)
    
    def _draw_column1_frames(self, ax, x, y_bottom, width, height):
        """Draw frame cross-sections: HEAD, SILL, JAMB"""
        
        # Column background
        col = Rectangle((x, y_bottom), width, height, linewidth=0.5,
                       edgecolor='#CCCCCC', facecolor='white')
        ax.add_patch(col)
        
        y_top = y_bottom + height
        section_height = (height - 8) / 3
        
        # Three sections
        head_y = y_top - section_height
        self._draw_frame_section(ax, x + 5, head_y - 5, width - 10, 
                                section_height - 5, "HEAD")
        
        sill_y = head_y - section_height
        self._draw_frame_section(ax, x + 5, sill_y - 5, width - 10,
                                section_height - 5, "SILL")
        
        jamb_y = sill_y - section_height
        self._draw_frame_section(ax, x + 5, jamb_y - 5, width - 10,
                                section_height - 5, "JAMB")
    
    def _draw_frame_section(self, ax, x, y, width, height, label):
        """
        Draw a single frame cross-section with improved label positioning
        Labels positioned to avoid overlapping with frame content
        
        Args:
            ax: Matplotlib axis
            x, y: Position
            width, height: Dimensions
            label: Label text (HEAD, SILL, JAMB)
        """
        
        # Section background
        bg = Rectangle((x, y - height), width, height, linewidth=0.5,
                      edgecolor='black', facecolor='#FAFAFA')
        ax.add_patch(bg)
        
        # Label positioned in top-left corner with padding to avoid overlap
        label_x = x + 2
        label_y = y - 3  # Top of frame section with clearance
        
        ax.text(label_x, label_y, label, fontsize=7, fontweight='bold', 
               va='top', ha='left', zorder=5)
        
        # Frame profile
        frame_margin = 1.5
        outer_width = width - 2 * frame_margin
        outer_height = height - 3
        
        outer = Rectangle((x + frame_margin, y - height + 2), outer_width, outer_height - 1,
                         linewidth=1, edgecolor='black', facecolor='#CCCCCC')
        ax.add_patch(outer)
        
        # Glass opening with proper margins
        glass_margin = 2
        glass_width = outer_width - 2 * glass_margin
        glass_height = outer_height - 2 * glass_margin - 1
        
        if glass_width > 0 and glass_height > 0:
            glass = Rectangle((x + frame_margin + glass_margin, y - height + 2 + glass_margin),
                             glass_width, glass_height,
                             linewidth=0.5, edgecolor='blue', facecolor='#E8F4FF')
            ax.add_patch(glass)
    
    def _draw_column2_elevation_plan(self, ax, x, y_bottom, width, height):
        """Draw elevation view and plan view"""
        
        # Column background
        col = Rectangle((x, y_bottom), width, height, linewidth=0.5,
                       edgecolor='#CCCCCC', facecolor='white')
        ax.add_patch(col)
        
        y_top = y_bottom + height
        mid_y = y_bottom + height / 2
        
        # Elevation (top half)
        self._draw_elevation_view(ax, x + 2, mid_y + 2, width - 4, height/2 - 4)
        
        # Plan (bottom half)
        self._draw_plan_view(ax, x + 2, y_bottom + 2, width - 4, height/2 - 4)
    
    def _draw_elevation_view(self, ax, x, y, width, height):
        """
        Draw elevation view with improved dimension text positioning
        """
        
        try:
            # Title with padding to avoid overlap
            ax.text(x, y - 2, 'ELEVATION', fontsize=7, fontweight='bold', va='top', ha='left')
            
            # Frame
            frame = Rectangle((x, y - height), width, height - 3, linewidth=0.5,
                             edgecolor='black', facecolor='white')
            ax.add_patch(frame)
            
            # Panel grid
            w_inch = float(self.params.get('width', 48))
            h_inch = float(self.params.get('height', 60))
            config = str(self.params.get('configuration', 'XX')).upper().strip()
            
            # Validate configuration
            if not config or len(config) == 0:
                config = 'XX'
            
            # Limit to 4 panels max
            config = config[:4]
            
            # Calculate panel width safely
            panel_count = len(config) if config else 2
            panel_width = (width - 4) / max(panel_count, 1)
            
            for i, char in enumerate(config):
                panel_x = x + 2 + i * panel_width
                
                panel = Rectangle((panel_x, y - height + 2), panel_width - 1, height - 5,
                                linewidth=0.5, edgecolor='black', facecolor='#E8F4FF')
                ax.add_patch(panel)
                
                # Panel label centered in panel
                label = 'O' if char in ['O', 'V'] else 'X'
                ax.text(panel_x + panel_width/2, y - height/2, label,
                       fontsize=8, fontweight='bold', ha='center', va='center', zorder=5)
            
            # Dimensions positioned below frame with extra spacing to avoid overlap
            dim_x = x + 2
            dim_y_width = y - height - 4  # Extra spacing below frame
            dim_y_height = y - height - 7  # Further spacing for second dimension
            
            width_ft = int(w_inch / 12)
            width_in = int(w_inch % 12)
            height_ft = int(h_inch // 12)
            height_in = int(h_inch % 12)
            
            # Width dimension with padding
            width_text = f"W: {width_ft}'-{width_in}\""
            ax.text(dim_x, dim_y_width, width_text, fontsize=6, va='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            # Height dimension with padding
            height_text = f"H: {height_ft}'-{height_in}\""
            ax.text(dim_x, dim_y_height, height_text, fontsize=6, va='top',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
                   
        except Exception as e:
            logger.error(f"Error in _draw_elevation_view: {str(e)}", exc_info=True)
            raise
    
    
    def _draw_plan_view(self, ax, x, y, width, height):
        """
        Draw plan view with improved element spacing
        """
        try:
            # Title with padding
            ax.text(x, y - 2, 'PLAN', fontsize=7, fontweight='bold', va='top', ha='left')
            
            # Frame
            frame = Rectangle((x, y - height), width, height - 3, linewidth=0.5,
                             edgecolor='black', facecolor='white')
            ax.add_patch(frame)
            
            # Plan rectangle with proper margins
            plan_margin = 3
            plan_width = width - 2*plan_margin
            plan_height = height - 7  # More space for label at bottom
            
            if plan_width > 0 and plan_height > 0:
                plan_rect = Rectangle((x + plan_margin, y - height + 3), plan_width, plan_height - 2,
                                     linewidth=0.5, edgecolor='black', facecolor='#FFFACD')
                ax.add_patch(plan_rect)
                
                # Person silhouette for scale - positioned to avoid overlap
                person_x = x + plan_margin + plan_width/4
                person_y = y - height + plan_height/2.5
                
                # Simple stick figure (smaller to avoid overlap)
                head_radius = 1.0
                
                # Head (using Circle from matplotlib.patches, already imported)
                head = Circle((person_x, person_y), head_radius, color='black', zorder=5)
                ax.add_patch(head)
                
                # Body
                ax.plot([person_x, person_x], [person_y - head_radius, person_y - 2.5], 
                       'k-', linewidth=0.8, zorder=5)
                
                # Arms
                ax.plot([person_x - 1.2, person_x + 1.2], [person_y - 1.5, person_y - 1.5], 
                       'k-', linewidth=0.8, zorder=5)
                
                # Legs
                ax.plot([person_x, person_x - 0.5], [person_y - 2.5, person_y - 3.8], 
                       'k-', linewidth=0.8, zorder=5)
                ax.plot([person_x, person_x + 0.5], [person_y - 2.5, person_y - 3.8], 
                       'k-', linewidth=0.8, zorder=5)
            
            # Scale label at bottom with padding
            scale_y = y - height + 0.8
            ax.text(x + width/2, scale_y, 'SCALE', 
                   fontsize=5, ha='center', style='italic', va='top',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
                   
            # Attempt to load a plan-view icon from static/plan_views based on product/config
            try:
                product = (self.params.get('productType') or '').strip()
                swing = (self.params.get('swingOrientation') or self.params.get('configuration') or '').strip()
                static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'plan_views'))

                def candidate_names(prod, swing_val):
                    prod_lower = (prod or '').lower()
                    swing_lower = (swing_val or '').lower()
                    names = []
                    # Sliding
                    if 'slid' in prod_lower or 'slider' in prod_lower:
                        names += ['slider_2panel.png', 'D-2_Panel_Slider.PNG']
                    # Casement / Hinged
                    if 'casement' in prod_lower or 'hinged' in prod_lower or 'door' in prod_lower:
                        if 'left' in swing_lower:
                            names += ['casement_left.png', 'D-Hinged_Door_IN_L.PNG']
                        if 'right' in swing_lower:
                            names += ['casement_right.png', 'D-Hinged_Door_IN_R.PNG']
                        # Outswing variants
                        if 'outswing' in swing_lower or 'out' in swing_lower:
                            names += ['casement_out_left.png', 'D-Hinged_Door_OUT_L.PNG', 'casement_out_right.png', 'D-Hinged_Door_OUT_R.PNG']
                    # Fixed window
                    if 'fixed' in prod_lower:
                        names += ['window_fixed.png', 'W-Fixed_O.PNG']
                    # Fallbacks
                    names += ['plan_slider.png', 'plan_casement.png', 'plan_default.png']
                    return names

                found = None
                for fname in candidate_names(product, swing):
                    candidate = os.path.join(static_dir, fname)
                    if os.path.exists(candidate):
                        found = candidate
                        break

                if found:
                    try:
                        img = mpimg.imread(found)
                        # Compute extent for imshow: left, right, bottom, top
                        left = x + plan_margin
                        bottom = y - height + 3
                        right = left + plan_width
                        top = bottom + plan_height - 2
                        ax.imshow(img, extent=(left, right, bottom, top), aspect='auto', zorder=10)
                    except Exception as img_err:
                        logger.warning(f"Failed to render plan view image '{found}': {img_err}")
            except Exception:
                # Non-fatal - continue without plan icon
                pass
        except Exception as e:
            logger.error(f"Error in _draw_plan_view: {str(e)}", exc_info=True)
            raise
    
    def _draw_column3_info(self, ax, x, y_bottom, width, height):
        """Draw frame icons, info table, and drawing details"""
        
        # Column background
        col = Rectangle((x, y_bottom), width, height, linewidth=0.5,
                       edgecolor='#CCCCCC', facecolor='white')
        ax.add_patch(col)
        
        # Icons (top half)
        self._draw_frame_icons(ax, x + 2, y_bottom + height * 0.5 + 2, 
                              width - 4, height * 0.5 - 4)
        
        # Info table (bottom half)
        self._draw_drawing_info_table(ax, x + 2, y_bottom + 2,
                                     width - 4, height * 0.5 - 4)
    
    def _draw_frame_icons(self, ax, x, y, width, height):
        """Draw 3x2 grid of frame type icons"""
        
        ax.text(x, y - 2, 'FRAME TYPES', fontsize=6, fontweight='bold')
        
        types = [
            ('FIXED', '⬚'),
            ('CASEMENT', '⬌'),
            ('SLIDER', '⬌⬌'),
            ('AWNING', '⌢'),
            ('HOPPER', '⌣'),
            ('PROJECTED', '⬍'),
        ]
        
        cols = 3
        rows = 2
        icon_width = (width - 2) / cols
        icon_height = (height - 6) / rows
        
        product_type = self.params.get('product_type', 'FIXED')
        
        for i, (type_name, icon_char) in enumerate(types):
            row = i // cols
            col = i % cols
            
            icon_x = x + 1 + col * icon_width
            icon_y = y - 6 - row * icon_height
            
            is_selected = type_name == product_type
            bg_color = '#C8E6C9' if is_selected else '#F0F0F0'
            bg = Rectangle((icon_x, icon_y - icon_height), icon_width - 1, icon_height - 1,
                          linewidth=0.5 if is_selected else 0.3,
                          edgecolor='darkgreen' if is_selected else '#AAAAAA',
                          facecolor=bg_color)
            ax.add_patch(bg)
            
            ax.text(icon_x + icon_width/2 - 1, icon_y - icon_height/2,
                   icon_char, fontsize=6, ha='center', va='center')
            
            ax.text(icon_x + icon_width/2 - 1, icon_y - icon_height + 1,
                   type_name, fontsize=4, ha='center', va='top')
    
    def _draw_drawing_info_table(self, ax, x, y, width, height):
        """
        Draw drawing information table with improved text spacing
        """
        
        ax.text(x, y - 1, 'DRAWING INFO', fontsize=6, fontweight='bold', va='top',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        rows = [
            ('Date', self.params.get('date_created', '---')[:10]),  # Limit date to 10 chars
            ('Serial', self.params.get('item_number', 'TBD')[:12]),  # Limit serial
            ('Designer', 'Sales System'),
            ('Revision', '-'),
        ]
        
        row_height = (height - 4) / len(rows)
        col_width = width / 2
        
        for i, (label, value) in enumerate(rows):
            row_y = y - 4 - i * row_height
            
            # Row background
            bg = Rectangle((x, row_y - row_height), width, row_height - 0.5,
                          linewidth=0.3, edgecolor='#CCCCCC',
                          facecolor='#FAFAFA' if i % 2 else 'white', zorder=1)
            ax.add_patch(bg)
            
            # Label (left)
            label_display = label
            if len(label) > 10:
                label_display = label[:8] + '..'
            
            ax.text(x + 0.5, row_y - 1.3, label_display, fontsize=5, fontweight='bold', 
                   va='top', ha='left', zorder=2)
            
            # Value (right)
            value_display = value
            if len(value) > 12:
                value_display = value[:10] + '..'
            
            ax.text(x + col_width + 0.3, row_y - 1.3, value_display, fontsize=5, 
                   va='top', ha='left', zorder=2)
    
    def _draw_specifications_table(self, ax, x, y, width, height):
        """
        Draw specifications table at bottom with proper text wrapping and overflow prevention
        """
        
        # Background
        table_bg = Rectangle((x, y), width, height, linewidth=0.5,
                           edgecolor='black', facecolor='white')
        ax.add_patch(table_bg)
        
        # Title with padding
        ax.text(x + 2, y + height - 3, 'SPECIFICATIONS', fontsize=7, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
        
        # Specs rows with improved text handling
        specs = [
            ('Glass:', self.params.get('glass_type', '5mm Clear')),
            ('Frame Color:', self.params.get('frame_color', 'White')),
            ('Series:', self.params.get('series', '65')),
            ('Elevation:', self.params.get('configuration', 'XO')),
            ('Dimensions:', f"{self.params.get('width', 48)}\" × {self.params.get('height', 60)}\""),
            ('Notes:', self.params.get('notes', '-')),
        ]
        
        row_height = (height - 6) / len(specs)
        col_width = width / 2  # Two columns: label and value
        
        for i, (label, value) in enumerate(specs):
            row_y = y + height - 6 - i * row_height
            
            # Row separator
            ax.plot([x, x + width], [row_y - row_height, row_y - row_height],
                   'k-', linewidth=0.3)
            
            # Label (left column)
            label_x = x + 1
            label_display = label
            if len(label) > 12:
                label_display = label[:10] + '..'  # Truncate long labels
            
            ax.text(label_x, row_y - 1.5, label_display, fontsize=5, fontweight='bold', 
                   va='top', ha='left')
            
            # Value (right column) with wrapping for long values
            value_x = x + col_width + 0.3
            max_value_width = col_width - 1  # Leave margin
            
            # Simple text wrapping for long values
            value_display = value
            if len(value) > 25:
                value_display = value[:22] + '..'  # Truncate very long values
            
            ax.text(value_x, row_y - 1.5, value_display, fontsize=5, 
                   va='top', ha='left')

