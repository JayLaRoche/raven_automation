"""
Professional Technical Drawing Generator - Phase 1
Orchestrates layout, dimensions, and components into complete shop drawings
"""
import os
from datetime import datetime
from typing import Dict, Optional

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .layout import DrawingLayout
from .dimensions import DimensionLine, draw_window_frame_with_dimensions
from .components import (
    SpecificationTable,
    CompanyHeader,
    DrawingTitle,
    ProjectInfoBlock,
    RevisionBlock,
    ConfigurationIcons
)


class ProfessionalDrawingGenerator:
    """
    Generate professional 2D technical shop drawings with:
    - 3-column layout (spec, elevation, project info)
    - 8-zone grid system
    - CAD-style dimensions
    - Specification tables
    - Company/project headers
    
    Phase 1 Implementation:
    - Basic window/door elevation
    - Specification tables
    - Dimension annotations
    - Project information blocks
    """
    
    def __init__(self, output_dir: str = "./drawings"):
        """
        Initialize drawing generator
        
        Args:
            output_dir: Directory to save generated PDFs
        """
        self.output_dir = output_dir
        self.layout = None
        self.zones = None
        
        # Create output directory if needed
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_window_drawing(
        self,
        item_data: Dict,
        project_data: Dict,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate professional window drawing
        
        Args:
            item_data: Window specification dict with keys:
                - item_number: Identifier (e.g., "W-001")
                - width_inches: Width in inches
                - height_inches: Height in inches
                - window_type: Type (e.g., "Double Casement")
                - frame_series: Frame series (e.g., "Series 6000")
                - swing_direction: Swing direction
                - glass_type: Glass type
                - quantity: Quantity
            
            project_data: Project info dict with keys:
                - po_number: PO number
                - project_name: Project name
                - customer_name: Customer name
            
            output_filename: Custom output filename (optional)
        
        Returns:
            Path to generated PDF file
        """
        # Create layout
        self.layout = DrawingLayout(figsize=(11, 17))
        self.fig, self.zones = self.layout.create_layout()
        
        po_number = project_data.get('po_number', 'UNKNOWN')
        item_number = item_data.get('item_number', 'W-001')
        
        # 1. Fill Left Column - Specification Tables
        self._draw_spec_tables(item_data)
        
        # 2. Fill Center Column - Elevation with Dimensions
        self._draw_elevation(item_data)
        
        # 3. Fill Right Column - Headers and Project Info
        self._draw_right_column(item_data, project_data)
        
        # Save figure
        if output_filename is None:
            output_filename = f"{po_number}_Window-{item_number}_ELEV.pdf"
        
        output_path = os.path.join(self.output_dir, output_filename)
        self.layout.save(output_path)
        
        return output_path
    
    def generate_door_drawing(
        self,
        item_data: Dict,
        project_data: Dict,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate professional door drawing
        
        Args:
            item_data: Door specification dict
            project_data: Project info dict
            output_filename: Custom output filename
        
        Returns:
            Path to generated PDF file
        """
        # Create layout
        self.layout = DrawingLayout(figsize=(11, 17))
        self.fig, self.zones = self.layout.create_layout()
        
        po_number = project_data.get('po_number', 'UNKNOWN')
        item_number = item_data.get('item_number', 'D-001')
        
        # 1. Fill Left Column - Specification Tables
        self._draw_spec_tables(item_data, is_door=True)
        
        # 2. Fill Center Column - Elevation with Dimensions
        self._draw_elevation(item_data, is_door=True)
        
        # 3. Fill Right Column - Headers and Project Info
        self._draw_right_column(item_data, project_data, is_door=True)
        
        # Save figure
        if output_filename is None:
            output_filename = f"{po_number}_Door-{item_number}_ELEV.pdf"
        
        output_path = os.path.join(self.output_dir, output_filename)
        self.layout.save(output_path)
        
        return output_path
    
    def _draw_spec_tables(self, item_data: Dict, is_door: bool = False):
        """
        Draw specification tables in left column
        
        Zone 1 (top): Product type and dimensions  
        Zone 2 (bottom): Cross-section views
        """
        # Zone 1: Dimensions and type specs
        spec_1 = SpecificationTable(self.zones['spec_1'])
        
        specs_data = [
            ("Glass:", item_data.get('glass_type', 'Standard')),
            ("Frame Color:", item_data.get('frame_color', 'White')),
            ("Screen Spec:", item_data.get('screen', 'None')),
            ("Hardware:", item_data.get('hardware', 'Standard')),
            ("Quantity:", str(item_data.get('quantity', 1))),
        ]
        
        spec_1.draw_table(
            specs_data,
            title=item_data.get('item_number', 'ITEM')
        )
        
        # Zone 2: Cross-sections
        self._draw_cross_sections(item_data, is_door)
    
    def _draw_cross_sections(self, item_data: Dict, is_door: bool = False):
        """Draw vertical and horizontal frame cross-sections with nail flanges"""
        ax = self.zones['spec_2']
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'FRAME SECTIONS', ha='center', va='top',
               fontsize=9, fontweight='bold')
        
        # === VERTICAL SECTION (Top half) ===
        v_y_base = 5
        v_y_top = 8.5
        v_x_center = 2.5
        
        # Main frame profile
        frame_width = 1.2
        v_section = Rectangle((v_x_center - frame_width/2, v_y_base), 
                             frame_width, v_y_top - v_y_base,
                             linewidth=1.5, edgecolor='black', facecolor='lightgray', alpha=0.3)
        ax.add_patch(v_section)
        
        # NAIL FLANGE - Left side (exterior)
        nail_flange_width = 0.8
        nail_flange_thickness = 0.15
        left_flange = Rectangle(
            (v_x_center - frame_width/2 - nail_flange_width, v_y_base + 0.5),
            nail_flange_width, nail_flange_thickness,
            linewidth=1.2, edgecolor='red', facecolor='red', alpha=0.4
        )
        ax.add_patch(left_flange)
        
        # NAIL FLANGE - Right side (exterior)
        right_flange = Rectangle(
            (v_x_center + frame_width/2, v_y_base + 0.5),
            nail_flange_width, nail_flange_thickness,
            linewidth=1.2, edgecolor='red', facecolor='red', alpha=0.4
        )
        ax.add_patch(right_flange)
        
        # Nail flange labels
        ax.text(v_x_center - frame_width/2 - nail_flange_width/2, v_y_base + 0.35, 
               'Nail Fin', ha='center', fontsize=5, color='red', fontweight='bold')
        
        # Interior/Exterior labels
        ax.text(0.5, v_y_base + 1.5, 'INT', ha='center', fontsize=6, style='italic')
        ax.text(4.5, v_y_base + 1.5, 'EXT', ha='center', fontsize=6, style='italic')
        
        # Frame detail lines (glass pocket, thermal break)
        ax.plot([v_x_center - 0.3, v_x_center - 0.3], [v_y_base, v_y_top], 
               'k--', linewidth=0.5, alpha=0.5, label='Glass')
        ax.plot([v_x_center + 0.3, v_x_center + 0.3], [v_y_base, v_y_top], 
               'k--', linewidth=0.5, alpha=0.5)
        
        # Section label
        ax.text(2.5, 4.5, 'VERTICAL SECTION', ha='center', fontsize=7, fontweight='bold')
        
        # === HORIZONTAL SECTION (Bottom half) ===
        h_y_base = 0.5
        h_y_top = 3
        h_x_start = 1
        h_x_end = 9
        h_y_center = (h_y_base + h_y_top) / 2
        
        # Main frame profile (sill/header)
        frame_height = 0.8
        h_section = Rectangle((h_x_start + 1, h_y_center - frame_height/2), 
                             h_x_end - h_x_start - 2, frame_height,
                             linewidth=1.5, edgecolor='black', facecolor='lightgray', alpha=0.3)
        ax.add_patch(h_section)
        
        # NAIL FLANGE - Top (exterior)
        top_flange = Rectangle(
            (h_x_start + 1.5, h_y_center + frame_height/2),
            h_x_end - h_x_start - 3, nail_flange_thickness,
            linewidth=1.2, edgecolor='red', facecolor='red', alpha=0.4
        )
        ax.add_patch(top_flange)
        
        # NAIL FLANGE - Bottom (exterior)
        bottom_flange = Rectangle(
            (h_x_start + 1.5, h_y_center - frame_height/2 - nail_flange_thickness),
            h_x_end - h_x_start - 3, nail_flange_thickness,
            linewidth=1.2, edgecolor='red', facecolor='red', alpha=0.4
        )
        ax.add_patch(bottom_flange)
        
        # Frame detail lines
        ax.plot([h_x_start + 2, h_x_end - 2], [h_y_center - 0.2, h_y_center - 0.2], 
               'k--', linewidth=0.5, alpha=0.5)
        ax.plot([h_x_start + 2, h_x_end - 2], [h_y_center + 0.2, h_y_center + 0.2], 
               'k--', linewidth=0.5, alpha=0.5)
        
        # Section label
        ax.text(5, 0.2, 'HORIZONTAL SECTION', ha='center', fontsize=7, fontweight='bold')
        
        # Dimension callout for nail flange width
        dim_y = h_y_center + frame_height/2 + nail_flange_thickness + 0.3
        ax.annotate('', xy=(h_x_start + 1.5, dim_y), xytext=(h_x_start + 1.5 + 0.8, dim_y),
                   arrowprops=dict(arrowstyle='<->', lw=0.6, color='red'))
        ax.text(h_x_start + 1.9, dim_y + 0.15, '30mm', ha='center', fontsize=6, color='red')
    
    def _draw_elevation(self, item_data: Dict, is_door: bool = False):
        """
        Draw elevation view with mullions, panel indicators, and CAD-style dimensions
        
        Zone 3 & 4: Main elevation and section views
        """
        ax = self.zones['elevation']
        ax.clear()
        
        # Get dimensions
        width = float(item_data.get('width_inches', 36))
        height = float(item_data.get('height_inches', 48))
        window_type = str(item_data.get('window_type', 'Fixed')).upper()
        
        # Scale to fit in zone (leave room for dimensions)
        scale = min(6 / width, 6 / height, 0.08)
        scaled_width = width * scale
        scaled_height = height * scale
        
        # Center the drawing
        offset_x = (10 - scaled_width) / 2
        offset_y = (10 - scaled_height) / 2 + 0.5
        
        # Draw outer frame
        frame = Rectangle(
            (offset_x, offset_y), scaled_width, scaled_height,
            linewidth=2, edgecolor='black', facecolor='none'
        )
        ax.add_patch(frame)
        
        # Detect panel configuration and draw mullions
        if 'SLIDER' in window_type or 'PATIO' in window_type or 'SLIDING' in window_type:
            # 4-panel slider configuration
            panel_width = scaled_width / 4
            
            # Draw vertical mullions
            for i in range(1, 4):
                x = offset_x + i * panel_width
                ax.plot([x, x], [offset_y, offset_y + scaled_height], 'k-', linewidth=1.5)
            
            # Draw horizontal mid-rail
            mid_y = offset_y + scaled_height / 2
            ax.plot([offset_x, offset_x + scaled_width], [mid_y, mid_y], 'k-', linewidth=1.5)
            
            # Add panel indicators (F. for Fixed panels in top row)
            for i in range(4):
                x_center = offset_x + (i + 0.5) * panel_width
                # Top panels typically fixed
                ax.text(x_center, offset_y + scaled_height * 0.75, 'F.',
                       ha='center', va='center', fontsize=8, fontweight='bold')
                # Bottom panels show arrows for sliding
                if i < 2:
                    ax.annotate('', xy=(x_center + 0.2, offset_y + scaled_height * 0.25),
                               xytext=(x_center - 0.2, offset_y + scaled_height * 0.25),
                               arrowprops=dict(arrowstyle='->', lw=1))
                    
        elif 'CASEMENT' in window_type:
            # Casement window - split vertically
            mid_x = offset_x + scaled_width / 2
            ax.plot([mid_x, mid_x], [offset_y, offset_y + scaled_height], 'k-', linewidth=1.5)
            
            # Add diagonal lines showing swing direction
            ax.plot([offset_x, mid_x], [offset_y, offset_y + scaled_height], 
                   'k--', linewidth=0.8, alpha=0.6)
            ax.plot([mid_x, offset_x + scaled_width], [offset_y, offset_y + scaled_height], 
                   'k--', linewidth=0.8, alpha=0.6)
                   
        elif 'AWNING' in window_type or 'HOPPER' in window_type:
            # Horizontal pivot
            mid_y = offset_y + scaled_height / 2
            ax.plot([offset_x, offset_x + scaled_width], [mid_y, mid_y], 'k-', linewidth=1.5)
            ax.plot([offset_x, offset_x + scaled_width], [offset_y, offset_y + scaled_height],
                   'k--', linewidth=0.8, alpha=0.6)
                   
        else:  # FIXED
            # Single pane - just add "F." indicator
            ax.text(offset_x + scaled_width/2, offset_y + scaled_height/2, 'F.',
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Add dimension lines
        dim = DimensionLine(ax)
        # Width dimension (bottom)
        dim.draw_horizontal(offset_x, offset_x + scaled_width, offset_y - 0.8, 
                          f'{width:.0f}"', above=False)
        # Height dimension (left side)
        dim.draw_vertical(offset_x - 0.8, offset_y, offset_y + scaled_height, 
                         f'{height:.0f}"', left=True)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Add title
        ax.text(
            5, 0.3,
            "ELEVATION VIEW",
            ha='center', va='bottom',
            fontsize=10, fontweight='bold',
            style='italic'
        )
    
    def _draw_right_column(self, item_data: Dict, project_data: Dict, is_door: bool = False):
        """
        Draw company header, title, and project info in right column
        
        Zone 5: Company header
        Zone 6: Drawing title
        Zone 7: Project information
        Zone 8: Revision block
        """
        # Zone 5: Company Header
        header = CompanyHeader(self.zones['header'])
        header.draw_header()
        
        # Zone 6: Drawing Title
        title_block = DrawingTitle(self.zones['title'])
        drawing_type = "DOOR" if is_door else "WINDOW"
        title_block.draw_title(
            drawing_type=drawing_type,
            item_number=item_data.get('item_number', 'UNKNOWN'),
            view="ELEVATION"
        )
        
        # Zone 7: Project Info
        width = item_data.get('width_inches', 36)
        project_info = ProjectInfoBlock(self.zones['project_info'])
        project_info.draw_project_info(
            project_name=project_data.get('project_name', 'Project'),
            po_number=project_data.get('po_number', 'PO-XXX'),
            customer_name=project_data.get('customer_name', 'Customer'),
            date=datetime.now().strftime("%m/%d/%Y"),
            scale="1/4\" = 1'" if width < 48 else "1/8\" = 1'\""
        )
        
        # Zone 8: Operation Icons
        window_type = item_data.get('window_type', 'FIXED')
        icons = ConfigurationIcons(self.zones['revision'])
        icons.draw_icons(active_type=window_type)


def demo_generate_window():
    """
    Demo: Generate sample window drawing
    Test data: W001 (72"x60" Double Casement)
    """
    # Sample window data
    window_data = {
        'item_number': 'W-001',
        'width_inches': 72,
        'height_inches': 60,
        'window_type': 'Double Casement',
        'frame_series': 'Series 6000',
        'swing_direction': 'Out',
        'glass_type': 'Low-E Tempered',
        'frame_color': 'White',
        'quantity': 2
    }
    
    # Sample project data
    project_data = {
        'po_number': 'DEMO-001',
        'project_name': 'Sample Residence',
        'customer_name': 'Demo Customer'
    }
    
    # Generate drawing
    generator = ProfessionalDrawingGenerator(output_dir='./drawings')
    output_file = generator.generate_window_drawing(window_data, project_data)
    
    print(f"✓ Sample drawing generated: {output_file}")
    return output_file


if __name__ == '__main__':
    demo_generate_window()
