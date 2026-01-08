"""
PDF Drawing Generator Service
Generates technical shop drawings for windows and doors using ReportLab and Matplotlib
"""
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from io import BytesIO
import math

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, gray
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


class DrawingGenerator:
    """Generate technical shop drawings for windows and doors"""
    
    def __init__(self, output_dir: str = "./drawings"):
        self.output_dir = output_dir
        self.company_name = "Kingdom & CO LLC (Raven Windows & Doors)"
        self.company_address = "9960 W Cheyenne ave Suite 140, Las Vegas NV 89129"
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_window_drawing(
        self, 
        item_data: Dict,
        project_name: str,
        po_number: str
    ) -> str:
        """
        Generate a technical drawing for a window
        
        Args:
            item_data: Window specifications (width_inches, height_inches, type, etc.)
            project_name: Project/customer name
            po_number: Purchase order number
            
        Returns:
            Path to generated PDF file
        """
        width = float(item_data.get('width_inches', 36))
        height = float(item_data.get('height_inches', 48))
        
        filename = f"{po_number}_{item_data.get('item_number', 'window')}_elevation.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create figure with matplotlib
        fig, ax = plt.subplots(figsize=(11, 8.5))
        fig.suptitle('WINDOW ELEVATION', fontsize=16, fontweight='bold')
        
        # Draw window frame
        self._draw_window_frame(ax, width, height, item_data)
        
        # Add dimensions
        self._add_dimensions(ax, width, height)
        
        # Add title block
        self._add_title_block(
            fig, 
            project_name=project_name,
            po_number=po_number,
            item_number=item_data.get('item_number', 'N/A'),
            drawing_type='Window Elevation'
        )
        
        # Save to PDF
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(filepath, format='pdf', dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return filepath
    
    def generate_door_drawing(
        self,
        item_data: Dict,
        project_name: str,
        po_number: str
    ) -> str:
        """
        Generate a technical drawing for a door
        
        Args:
            item_data: Door specifications
            project_name: Project/customer name
            po_number: Purchase order number
            
        Returns:
            Path to generated PDF file
        """
        width = float(item_data.get('width_inches', 36))
        height = float(item_data.get('height_inches', 84))
        
        filename = f"{po_number}_{item_data.get('item_number', 'door')}_elevation.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(11, 14))
        fig.suptitle('DOOR ELEVATION', fontsize=16, fontweight='bold')
        
        # Draw door frame
        self._draw_door_frame(ax, width, height, item_data)
        
        # Add dimensions
        self._add_dimensions(ax, width, height)
        
        # Add title block
        self._add_title_block(
            fig,
            project_name=project_name,
            po_number=po_number,
            item_number=item_data.get('item_number', 'N/A'),
            drawing_type='Door Elevation'
        )
        
        # Save to PDF
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(filepath, format='pdf', dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return filepath
    
    def _draw_window_frame(self, ax, width: float, height: float, item_data: Dict):
        """Draw window frame with glass and muntins"""
        scale = 100 / max(width, height)  # Scale to fit nicely
        
        # Frame
        frame_thickness = 2
        rect = patches.Rectangle(
            (0, 0), width * scale, height * scale,
            linewidth=2, edgecolor='black', facecolor='lightblue', alpha=0.3
        )
        ax.add_patch(rect)
        
        # Glass panes (simple grid based on type)
        glass_color = 'lightcyan'
        num_cols = 2
        num_rows = 2
        
        pane_width = (width * scale - frame_thickness * 2) / num_cols
        pane_height = (height * scale - frame_thickness * 2) / num_rows
        
        for row in range(num_rows):
            for col in range(num_cols):
                x = frame_thickness + col * pane_width
                y = frame_thickness + row * pane_height
                pane = patches.Rectangle(
                    (x, y), pane_width, pane_height,
                    linewidth=1, edgecolor='blue', facecolor=glass_color, alpha=0.5
                )
                ax.add_patch(pane)
        
        # Set axis limits with margin
        margin = 20
        ax.set_xlim(-margin, (width * scale) + margin)
        ax.set_ylim(-margin, (height * scale) + margin)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _draw_door_frame(self, ax, width: float, height: float, item_data: Dict):
        """Draw door frame with panel and hardware"""
        scale = 100 / max(width, height)
        
        # Frame
        frame_thickness = 1.75
        rect = patches.Rectangle(
            (0, 0), width * scale, height * scale,
            linewidth=2.5, edgecolor='darkred', facecolor='lightyellow', alpha=0.2
        )
        ax.add_patch(rect)
        
        # Door panel
        panel_x = frame_thickness
        panel_y = frame_thickness
        panel_width = (width * scale) - (frame_thickness * 2)
        panel_height = (height * scale) - (frame_thickness * 2)
        
        panel = patches.Rectangle(
            (panel_x, panel_y), panel_width, panel_height,
            linewidth=1.5, edgecolor='brown', facecolor='tan', alpha=0.4
        )
        ax.add_patch(panel)
        
        # Stile and rail (cross members)
        stile_width = 1.5
        rail_height = 1.5
        
        # Vertical stile
        stile_x = (width * scale) / 2 - stile_width / 2
        stile = patches.Rectangle(
            (stile_x, panel_y), stile_width, panel_height,
            linewidth=0.5, edgecolor='black', facecolor='wheat', alpha=0.5
        )
        ax.add_patch(stile)
        
        # Horizontal rails
        rail_y = (height * scale) / 3
        rail = patches.Rectangle(
            (panel_x, rail_y), panel_width, rail_height,
            linewidth=0.5, edgecolor='black', facecolor='wheat', alpha=0.5
        )
        ax.add_patch(rail)
        
        # Handle
        handle_x = stile_x + stile_width + 2
        handle_y = (height * scale) / 2 - 2
        handle = patches.Circle((handle_x, handle_y), 1, edgecolor='gold', facecolor='gold', alpha=0.7)
        ax.add_patch(handle)
        
        # Set axis limits
        margin = 30
        ax.set_xlim(-margin, (width * scale) + margin)
        ax.set_ylim(-margin, (height * scale) + margin)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _add_dimensions(self, ax, width: float, height: float):
        """Add dimension annotations to drawing"""
        scale = 100 / max(width, height)
        
        # Width dimension (bottom)
        dim_y = -5
        ax.annotate('', xy=(width * scale, dim_y), xytext=(0, dim_y),
                   arrowprops=dict(arrowstyle='<->', color='red', lw=1))
        mid_x = (width * scale) / 2
        ax.text(mid_x, dim_y - 3, f'{width:.1f}"', 
               ha='center', va='top', fontsize=10, color='red', fontweight='bold')
        
        # Height dimension (left)
        dim_x = -8
        ax.annotate('', xy=(dim_x, height * scale), xytext=(dim_x, 0),
                   arrowprops=dict(arrowstyle='<->', color='red', lw=1))
        mid_y = (height * scale) / 2
        ax.text(dim_x - 3, mid_y, f'{height:.1f}"',
               ha='right', va='center', fontsize=10, color='red', fontweight='bold', rotation=90)
    
    def _add_title_block(
        self,
        fig,
        project_name: str,
        po_number: str,
        item_number: str,
        drawing_type: str
    ):
        """Add title block with project and drawing info"""
        ax = fig.add_axes([0.05, 0.01, 0.9, 0.08])
        ax.axis('off')
        
        # Title block background
        rect = patches.Rectangle(
            (0, 0), 1, 1, transform=ax.transAxes,
            edgecolor='black', facecolor='lightgray', linewidth=2
        )
        ax.add_patch(rect)
        
        # Title block text
        info_text = f"""
{self.company_name}
{self.company_address}

Project: {project_name} | PO: {po_number} | Item: {item_number}
Drawing: {drawing_type} | Date: {datetime.now().strftime('%m/%d/%Y')}
        """.strip()
        
        ax.text(0.5, 0.5, info_text,
               transform=ax.transAxes, fontsize=9,
               ha='center', va='center',
               family='monospace',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    def generate_project_package(
        self,
        project_data: Dict,
        po_number: str
    ) -> List[str]:
        """
        Generate all drawings for a project
        
        Args:
            project_data: Project dict with 'windows' and 'doors' lists
            po_number: Purchase order number
            
        Returns:
            List of paths to generated PDF files
        """
        project_name = project_data.get('metadata', {}).get('project_name', po_number)
        generated_files = []
        
        # Generate window drawings
        for window in project_data.get('windows', []):
            try:
                filepath = self.generate_window_drawing(window, project_name, po_number)
                generated_files.append(filepath)
                print(f"✓ Generated: {os.path.basename(filepath)}")
            except Exception as e:
                print(f"✗ Error generating window drawing: {e}")
        
        # Generate door drawings
        for door in project_data.get('doors', []):
            try:
                filepath = self.generate_door_drawing(door, project_name, po_number)
                generated_files.append(filepath)
                print(f"✓ Generated: {os.path.basename(filepath)}")
            except Exception as e:
                print(f"✗ Error generating door drawing: {e}")
        
        return generated_files
    
    def cleanup_old_drawings(self, days_old: int = 30):
        """Remove drawings older than specified days"""
        import time
        cutoff_time = time.time() - (days_old * 86400)
        
        removed_count = 0
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath) and filepath.endswith('.pdf'):
                if os.path.getmtime(filepath) < cutoff_time:
                    try:
                        os.remove(filepath)
                        removed_count += 1
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")
        
        return removed_count


def get_drawing_generator(output_dir: str = "./drawings") -> DrawingGenerator:
    """Factory function for DrawingGenerator singleton"""
    return DrawingGenerator(output_dir)
