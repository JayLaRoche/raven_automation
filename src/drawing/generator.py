"""
Drawing Generator Adapter
Bridges PyQt6 desktop app with existing matplotlib drawing system
"""

import os
from pathlib import Path
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import logging
from typing import Dict, Any, Optional

from src.database import DatabaseManager, FrameLibrary, DatabaseQueries

logger = logging.getLogger(__name__)


class DrawingGenerator:
    """
    Adapter for generating CAD shop drawings
    Reuses existing drawing_engine logic from FastAPI backend
    """
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.frame_library = FrameLibrary(db_manager)
        self.queries = DatabaseQueries(db_manager)
        
        logger.info("Drawing generator initialized")
    
    def generate(self, parameters: Dict[str, Any]) -> Figure:
        """
        Generate CAD shop drawing from parameters
        
        Args:
            parameters: Dict with keys:
                - series: Frame series (e.g., '65', '80')
                - product_type: Product type (e.g., 'FIXED', 'CASEMENT')
                - configuration: Operable config (e.g., 'XO', 'XX')
                - width: Width in inches
                - height: Height in inches
                - glass_type: Glass specification
                - frame_color: Frame color
                - has_grids: Boolean for grids
                - item_number: Item/unit number
                - po_number: Purchase order number
        
        Returns:
            Matplotlib Figure object
        """
        try:
            logger.info(f"Generating drawing for {parameters.get('item_number', 'untitled')}")
            
            # Create figure (8.5" x 11" portrait)
            fig = Figure(figsize=(8.5, 11), dpi=100)
            
            # Main drawing area (leave margins for title block)
            ax = fig.add_axes([0.1, 0.25, 0.8, 0.65])
            
            # Title block area
            title_ax = fig.add_axes([0.1, 0.05, 0.8, 0.15])
            
            # Generate main drawing
            self._draw_elevation(ax, parameters)
            
            # Generate title block
            self._draw_title_block(title_ax, parameters)
            
            logger.info("Drawing generated successfully")
            return fig
            
        except Exception as e:
            logger.error(f"Failed to generate drawing: {e}", exc_info=True)
            raise
    
    def _draw_elevation(self, ax, parameters: Dict[str, Any]):
        """
        Draw front elevation view
        
        Args:
            ax: Matplotlib axes
            parameters: Drawing parameters
        """
        width = parameters.get('width', 48.0)
        height = parameters.get('height', 60.0)
        series = parameters.get('series', '65')
        product_type = parameters.get('product_type', 'FIXED')
        
        # Load frame cross-section for dimensions
        try:
            frame_data = self.frame_library.get_cross_section(
                series=series,
                view_type='jamb',  # Use jamb for frame width
                configuration='standard'
            )
            
            # Get frame width from dimensions
            frame_width = frame_data.get('dimensions', {}).get('frame_width', 2.0)
            
        except Exception as e:
            logger.warning(f"Could not load frame data: {e}, using default width")
            frame_width = 2.0
        
        # Set up axes
        ax.set_aspect('equal')
        ax.set_xlim(-5, width + 5)
        ax.set_ylim(-5, height + 5)
        
        # Draw outer frame
        outer_rect = Rectangle(
            (0, 0), width, height,
            fill=False, edgecolor='black', linewidth=2
        )
        ax.add_patch(outer_rect)
        
        # Draw inner frame (glass opening)
        inner_x = frame_width
        inner_y = frame_width
        inner_width = width - (2 * frame_width)
        inner_height = height - (2 * frame_width)
        
        inner_rect = Rectangle(
            (inner_x, inner_y), inner_width, inner_height,
            fill=False, edgecolor='black', linewidth=1
        )
        ax.add_patch(inner_rect)
        
        # Draw operable divisions if applicable
        config = parameters.get('configuration', '').upper()
        if config and product_type in ['SLIDER 2-PANEL', 'SLIDER 3-PANEL', 'SLIDER 4-PANEL',
                                        'DOUBLE CASEMENT', 'BIFOLD DOOR']:
            self._draw_divisions(ax, config, inner_x, inner_y, inner_width, inner_height)
        
        # Draw grids if requested
        if parameters.get('has_grids', False):
            self._draw_grids(ax, inner_x, inner_y, inner_width, inner_height)
        
        # Add dimensions
        self._add_dimensions(ax, width, height)
        
        # Add labels
        ax.text(width / 2, -3, f"{product_type} - {series} SERIES",
                ha='center', va='top', fontsize=10, weight='bold')
        
        # Remove axes
        ax.axis('off')
    
    def _draw_divisions(self, ax, config: str, x: float, y: float, 
                        width: float, height: float):
        """
        Draw operable panel divisions
        
        Args:
            ax: Matplotlib axes
            config: Configuration string (e.g., 'XO', 'OXO')
            x, y: Starting position
            width, height: Opening dimensions
        """
        num_panels = len(config)
        if num_panels < 2:
            return
        
        panel_width = width / num_panels
        
        # Draw vertical divisions
        for i in range(1, num_panels):
            division_x = x + (i * panel_width)
            line = Line2D(
                [division_x, division_x],
                [y, y + height],
                color='black', linewidth=1.5
            )
            ax.add_line(line)
        
        # Draw operable indicators (arrows or X's)
        for i, char in enumerate(config):
            panel_x = x + (i * panel_width) + (panel_width / 2)
            panel_y = y + (height / 2)
            
            if char == 'O':
                # Draw arrow for operable
                ax.annotate('', xy=(panel_x + 1, panel_y), 
                           xytext=(panel_x - 1, panel_y),
                           arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
            elif char == 'X':
                # Draw X for fixed
                ax.plot([panel_x - 1, panel_x + 1], [panel_y - 1, panel_y + 1],
                       'k-', linewidth=1)
                ax.plot([panel_x - 1, panel_x + 1], [panel_y + 1, panel_y - 1],
                       'k-', linewidth=1)
    
    def _draw_grids(self, ax, x: float, y: float, width: float, height: float):
        """
        Draw grid pattern on glass
        
        Args:
            ax: Matplotlib axes
            x, y: Starting position
            width, height: Glass dimensions
        """
        # Draw horizontal grids (3 divisions)
        for i in range(1, 3):
            grid_y = y + (i * height / 3)
            line = Line2D(
                [x, x + width],
                [grid_y, grid_y],
                color='gray', linewidth=0.5, linestyle='--'
            )
            ax.add_line(line)
        
        # Draw vertical grids (2 divisions)
        for i in range(1, 2):
            grid_x = x + (i * width / 2)
            line = Line2D(
                [grid_x, grid_x],
                [y, y + height],
                color='gray', linewidth=0.5, linestyle='--'
            )
            ax.add_line(line)
    
    def _add_dimensions(self, ax, width: float, height: float):
        """
        Add dimension lines and text
        
        Args:
            ax: Matplotlib axes
            width: Overall width
            height: Overall height
        """
        # Width dimension (bottom)
        dim_y = -2
        ax.plot([0, width], [dim_y, dim_y], 'k-', linewidth=0.5)
        ax.plot([0, 0], [dim_y - 0.3, dim_y + 0.3], 'k-', linewidth=0.5)
        ax.plot([width, width], [dim_y - 0.3, dim_y + 0.3], 'k-', linewidth=0.5)
        ax.text(width / 2, dim_y - 0.8, f'{width:.2f}"', 
                ha='center', va='top', fontsize=8)
        
        # Height dimension (right)
        dim_x = width + 2
        ax.plot([dim_x, dim_x], [0, height], 'k-', linewidth=0.5)
        ax.plot([dim_x - 0.3, dim_x + 0.3], [0, 0], 'k-', linewidth=0.5)
        ax.plot([dim_x - 0.3, dim_x + 0.3], [height, height], 'k-', linewidth=0.5)
        ax.text(dim_x + 0.8, height / 2, f'{height:.2f}"', 
                ha='left', va='center', fontsize=8, rotation=90)
    
    def _draw_title_block(self, ax, parameters: Dict[str, Any]):
        """
        Draw title block with project information
        
        Args:
            ax: Matplotlib axes for title block
            parameters: Drawing parameters
        """
        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        # Company name
        ax.text(0.5, 0.85, 'RAVEN CUSTOM GLASS',
                ha='center', va='center', fontsize=14, weight='bold')
        
        # Drawing information
        info_left_x = 0.05
        info_y_start = 0.65
        info_y_step = 0.12
        
        # Item number
        ax.text(info_left_x, info_y_start, f"Item #: {parameters.get('item_number', 'N/A')}",
                ha='left', va='center', fontsize=10)
        
        # PO number
        ax.text(info_left_x, info_y_start - info_y_step, 
                f"PO #: {parameters.get('po_number', 'N/A')}",
                ha='left', va='center', fontsize=10)
        
        # Specifications (right column)
        spec_x = 0.55
        
        # Series
        ax.text(spec_x, info_y_start, 
                f"Series: {parameters.get('series', 'N/A')}",
                ha='left', va='center', fontsize=9)
        
        # Glass type
        ax.text(spec_x, info_y_start - info_y_step,
                f"Glass: {parameters.get('glass_type', 'N/A')}",
                ha='left', va='center', fontsize=9)
        
        # Frame color
        ax.text(spec_x, info_y_start - (2 * info_y_step),
                f"Color: {parameters.get('frame_color', 'N/A')}",
                ha='left', va='center', fontsize=9)
        
        # Border
        border = Rectangle(
            (0.02, 0.02), 0.96, 0.96,
            fill=False, edgecolor='black', linewidth=2
        )
        ax.add_patch(border)
