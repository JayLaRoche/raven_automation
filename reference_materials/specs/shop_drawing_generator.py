"""
Professional Shop Drawing Generator for Raven Custom Glass
==========================================================

This module generates professional 2D shop drawings for windows and doors
matching the Raven Custom Glass standard format.

Author: Jeremiah
Client: Raven Custom Glass (Zion)
Project: Automated Shop Drawing System
Date: December 24, 2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Arc, Circle, Polygon
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from datetime import datetime
import numpy as np
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

# Company Information
COMPANY_NAME = "Kingdom & CO LLC (Raven Windows & Doors)"
COMPANY_ADDRESS = "9960 W Cheyenne Ave\nSuite 140, Las Vegas NV 89129"
COMPANY_PHONE = "702-577-1003"
COMPANY_WEBSITE = "ravencustomglass.com"

# Drawing Configuration
FIGURE_SIZE = (11, 8.5)  # inches (landscape)
DPI = 300  # print quality
MARGINS = 0.5  # inches

# Color Palette
COLORS = {
    'black': '#000000',
    'dark_gray': '#666666',
    'light_gray': '#CCCCCC',
    'glass_tint': '#E8F4F8',
    'white': '#FFFFFF',
}

# Line Weights (points)
LINE_WEIGHTS = {
    'thick': 1.0,      # Object outlines
    'medium': 0.75,    # Cross-section details
    'thin': 0.5,       # Dimensions, extensions
}

# Typography
FONTS = {
    'logo': {'family': 'Arial', 'size': 16, 'weight': 'bold'},
    'header': {'family': 'Arial', 'size': 11, 'weight': 'bold'},
    'body': {'family': 'Arial', 'size': 9, 'weight': 'normal'},
    'dimension': {'family': 'Arial', 'size': 8, 'weight': 'normal'},
    'table': {'family': 'Arial', 'size': 8, 'weight': 'normal'},
}

# =============================================================================
# DATA STRUCTURES
# =============================================================================

class WindowDoorItem:
    """Data structure for window/door specifications"""
    
    def __init__(self, data: Dict):
        """Initialize from Google Sheets row data"""
        self.item_id = data.get('item_id', '')
        self.room = data.get('room', '')
        self.width = float(data.get('width', 0))
        self.height = float(data.get('height', 0))
        self.type = data.get('type', '')
        self.swing_direction = data.get('swing_direction', '')
        self.quantity = int(data.get('quantity', 1))
        self.series = data.get('series', '')
        self.nail_fin = data.get('nail_fin', '')
        self.frame_color = data.get('frame_color', '')
        self.glass = data.get('glass', '')
        self.grids = data.get('grids', 'NONE')
        self.screen = data.get('screen', 'NONE')
        self.po_number = data.get('po_number', '')
        self.project_name = data.get('project_name', '')
        
    def is_door(self) -> bool:
        """Check if item is a door"""
        return self.item_id.startswith('D')
    
    def is_window(self) -> bool:
        """Check if item is a window"""
        return self.item_id.startswith('W')
    
    def get_panel_count(self) -> int:
        """Determine number of panels from type"""
        if 'DOUBLE' in self.type.upper():
            return 2
        elif '4 PANEL' in self.type.upper():
            return 4
        elif '3 PANEL' in self.type.upper():
            return 3
        elif '2 PANEL' in self.type.upper():
            return 2
        else:
            return 1
    
    def get_panel_width(self) -> float:
        """Calculate individual panel width"""
        return self.width / self.get_panel_count()


# =============================================================================
# DRAWING LAYOUT & GRID SETUP
# =============================================================================

def create_drawing_layout() -> Tuple[plt.Figure, Dict[str, plt.Axes]]:
    """
    Create the main drawing layout with 3 columns x 3 rows grid.
    
    Returns:
        fig: Matplotlib figure
        axes: Dictionary of named axes for each zone
    """
    fig = plt.figure(figsize=FIGURE_SIZE, dpi=DPI)
    
    # Create grid: 3 columns (30%, 45%, 25%) x 3 rows (2, 3, 2)
    gs = GridSpec(3, 3, figure=fig,
                  width_ratios=[3, 4.5, 2.5],
                  height_ratios=[2, 3, 2],
                  hspace=0.05, wspace=0.05)
    
    # Create axes for each zone
    axes = {
        'spec_table': fig.add_subplot(gs[0, 0]),      # Top-left
        'cross_section': fig.add_subplot(gs[1:, 0]),  # Mid/Bottom-left
        'elevation': fig.add_subplot(gs[0, 1]),       # Top-center
        'person': fig.add_subplot(gs[1, 1]),          # Mid-center
        'plan': fig.add_subplot(gs[2, 1]),            # Bottom-center
        'header': fig.add_subplot(gs[0, 2]),          # Top-right
        'thumbnails': fig.add_subplot(gs[1, 2]),      # Mid-right
        'project_info': fig.add_subplot(gs[2, 2]),    # Bottom-right
    }
    
    # Configure all axes
    for ax in axes.values():
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
    
    return fig, axes


# =============================================================================
# DIMENSION LINE HELPERS
# =============================================================================

def draw_dimension_line(ax: plt.Axes, 
                       x1: float, y1: float, 
                       x2: float, y2: float,
                       text: str,
                       offset: float = 2,
                       text_offset: float = 1):
    """
    Draw a dimension line with arrows and text (CAD style).
    
    Args:
        ax: Matplotlib axes
        x1, y1: Start point
        x2, y2: End point
        text: Dimension text (e.g., "36.0\"")
        offset: Distance from measured object to dimension line
        text_offset: Distance from dimension line to text
    """
    # Extension lines (vertical)
    ax.plot([x1, x1], [y1, y1 - offset], 'k-', lw=LINE_WEIGHTS['thin'])
    ax.plot([x2, x2], [y2, y2 - offset], 'k-', lw=LINE_WEIGHTS['thin'])
    
    # Dimension line with arrows
    arrow = FancyArrowPatch(
        (x1, y1 - offset), (x2, y2 - offset),
        arrowstyle='<->',
        mutation_scale=10,
        lw=LINE_WEIGHTS['thin'],
        color=COLORS['black']
    )
    ax.add_patch(arrow)
    
    # Dimension text (centered, above line)
    mid_x = (x1 + x2) / 2
    ax.text(mid_x, y1 - offset + text_offset, text,
           ha='center', va='bottom',
           fontsize=FONTS['dimension']['size'],
           fontfamily=FONTS['dimension']['family'])


def draw_vertical_dimension(ax: plt.Axes,
                           x: float, y1: float, y2: float,
                           text: str,
                           offset: float = 2,
                           text_offset: float = 1,
                           side: str = 'right'):
    """
    Draw a vertical dimension line.
    
    Args:
        side: 'right' or 'left' - which side to place the dimension
    """
    x_pos = x + offset if side == 'right' else x - offset
    
    # Extension lines (horizontal)
    ax.plot([x, x_pos], [y1, y1], 'k-', lw=LINE_WEIGHTS['thin'])
    ax.plot([x, x_pos], [y2, y2], 'k-', lw=LINE_WEIGHTS['thin'])
    
    # Dimension line with arrows
    arrow = FancyArrowPatch(
        (x_pos, y1), (x_pos, y2),
        arrowstyle='<->',
        mutation_scale=10,
        lw=LINE_WEIGHTS['thin'],
        color=COLORS['black']
    )
    ax.add_patch(arrow)
    
    # Dimension text (rotated 90 degrees)
    mid_y = (y1 + y2) / 2
    text_x = x_pos + text_offset if side == 'right' else x_pos - text_offset
    ax.text(text_x, mid_y, text,
           ha='left' if side == 'right' else 'right',
           va='center',
           rotation=90 if side == 'right' else -90,
           fontsize=FONTS['dimension']['size'],
           fontfamily=FONTS['dimension']['family'])


# =============================================================================
# CROSS-SECTION DRAWING
# =============================================================================

def draw_frame_cross_section(ax: plt.Axes,
                             series: str,
                             x: float, y: float,
                             width: float, height: float,
                             show_hardware: bool = True):
    """
    Draw a frame cross-section detail based on series type.
    
    Args:
        series: Frame series ('65', '80', '86', '135', etc.)
        x, y: Bottom-left corner position
        width, height: Cross-section dimensions
        show_hardware: Whether to show hinge/lock details
    """
    # Outer frame rectangle
    frame = Rectangle((x, y), width, height,
                     linewidth=LINE_WEIGHTS['medium'],
                     edgecolor=COLORS['black'],
                     facecolor=COLORS['light_gray'])
    ax.add_patch(frame)
    
    # Thermal break (vertical line through center)
    thermal_x = x + width / 2
    ax.plot([thermal_x, thermal_x], [y, y + height],
           'k-', lw=LINE_WEIGHTS['medium'], color=COLORS['dark_gray'])
    
    # Series-specific details
    if series == '65':  # Hinged door
        if show_hardware:
            # Hinge detail (circle)
            hinge_y = y + height * 0.3
            hinge = Circle((thermal_x, hinge_y), width * 0.15,
                          color=COLORS['black'])
            ax.add_patch(hinge)
            
    elif series == '86':  # Casement window
        # Casement hardware location
        hardware_y = y + height * 0.5
        ax.plot([x + width * 0.2, x + width * 0.8], 
               [hardware_y, hardware_y],
               'k-', lw=LINE_WEIGHTS['thin'])
        
    elif series == '80':  # Fixed window
        # Simplified frame (no hardware)
        pass
    
    elif series in ['135', 'MD100H']:  # Slider systems
        # Track indicators
        track_spacing = width * 0.2
        for i in range(2):
            track_x = x + (i + 1) * track_spacing
            ax.plot([track_x, track_x], [y, y + height * 0.3],
                   'k--', lw=LINE_WEIGHTS['thin'])
    
    # Weatherstripping (dashed lines at edges)
    ax.plot([x + width * 0.1, x + width * 0.1], [y, y + height],
           'k--', lw=LINE_WEIGHTS['thin'])
    ax.plot([x + width * 0.9, x + width * 0.9], [y, y + height],
           'k--', lw=LINE_WEIGHTS['thin'])


# =============================================================================
# PERSON SILHOUETTE & SWING ARROW
# =============================================================================

def draw_person_silhouette(ax: plt.Axes,
                          x: float, y: float,
                          height: float = 68,
                          unit: str = 'inches'):
    """
    Draw a person silhouette for scale reference.
    
    Args:
        x, y: Bottom-center position
        height: Person height (default 68 inches = 5'8")
        unit: 'inches' or 'normalized'
    """
    scale = 1.0 if unit == 'normalized' else height / 68
    
    # Head (circle)
    head_y = y + 60 * scale
    head = Circle((x, head_y), 4 * scale, color=COLORS['black'])
    ax.add_patch(head)
    
    # Body (rectangle)
    body = Rectangle((x - 4*scale, y + 35*scale),
                    8*scale, 25*scale,
                    facecolor=COLORS['black'],
                    edgecolor='none')
    ax.add_patch(body)
    
    # Arms (horizontal line)
    arm_y = y + 50 * scale
    ax.plot([x - 10*scale, x + 10*scale],
           [arm_y, arm_y],
           'k-', lw=2*scale, color=COLORS['black'])
    
    # Legs (two vertical lines)
    leg_spacing = 3 * scale
    ax.plot([x - leg_spacing, x - leg_spacing],
           [y, y + 35*scale],
           'k-', lw=2*scale, color=COLORS['black'])
    ax.plot([x + leg_spacing, x + leg_spacing],
           [y, y + 35*scale],
           'k-', lw=2*scale, color=COLORS['black'])


def draw_swing_arrow(ax: plt.Axes,
                    hinge_x: float, hinge_y: float,
                    radius: float,
                    angle: float = 90,
                    direction: str = 'right'):
    """
    Draw a curved arrow showing door/window swing direction.
    
    Args:
        hinge_x, hinge_y: Hinge point location
        radius: Arc radius
        angle: Swing angle in degrees (typically 90)
        direction: 'right', 'left', 'up', 'down'
    """
    # Determine start and end angles based on direction
    angle_map = {
        'right': (0, angle),
        'left': (180 - angle, 180),
        'up': (90 - angle/2, 90 + angle/2),
        'down': (270 - angle/2, 270 + angle/2),
    }
    
    theta1, theta2 = angle_map.get(direction, (0, angle))
    
    # Draw arc
    arc = Arc((hinge_x, hinge_y), 2*radius, 2*radius,
             angle=0, theta1=theta1, theta2=theta2,
             linewidth=LINE_WEIGHTS['medium'],
             color=COLORS['black'])
    ax.add_patch(arc)
    
    # Calculate arrow head position
    end_angle_rad = np.radians(theta2)
    end_x = hinge_x + radius * np.cos(end_angle_rad)
    end_y = hinge_y + radius * np.sin(end_angle_rad)
    
    # Draw arrow head
    arrow_length = 3
    arrow_start_x = end_x - arrow_length * np.cos(end_angle_rad)
    arrow_start_y = end_y - arrow_length * np.sin(end_angle_rad)
    
    arrow = FancyArrowPatch(
        (arrow_start_x, arrow_start_y), (end_x, end_y),
        arrowstyle='->',
        mutation_scale=15,
        lw=LINE_WEIGHTS['medium'],
        color=COLORS['black']
    )
    ax.add_patch(arrow)


# =============================================================================
# ELEVATION VIEW
# =============================================================================

def draw_elevation_view(ax: plt.Axes, item: WindowDoorItem):
    """
    Draw the front elevation view with dimensions.
    
    Args:
        ax: Matplotlib axes
        item: WindowDoorItem instance
    """
    # Calculate drawing area (with padding)
    padding = 10
    draw_width = 80
    draw_height = 80
    
    # Scale to fit within drawing area
    scale_x = draw_width / item.width
    scale_y = draw_height / item.height
    scale = min(scale_x, scale_y) * 0.8  # 80% of available space
    
    # Calculate scaled dimensions
    scaled_width = item.width * scale
    scaled_height = item.height * scale
    
    # Center the drawing
    start_x = (100 - scaled_width) / 2
    start_y = (100 - scaled_height) / 2
    
    # Draw main frame outline
    frame = Rectangle((start_x, start_y), scaled_width, scaled_height,
                     linewidth=LINE_WEIGHTS['thick'],
                     edgecolor=COLORS['black'],
                     facecolor='none')
    ax.add_patch(frame)
    
    # Draw panel divisions
    panel_count = item.get_panel_count()
    if panel_count > 1:
        panel_width = scaled_width / panel_count
        for i in range(1, panel_count):
            x = start_x + i * panel_width
            ax.plot([x, x], [start_y, start_y + scaled_height],
                   'k-', lw=LINE_WEIGHTS['medium'])
        
        # Add panel dimensions
        for i in range(panel_count):
            panel_x = start_x + i * panel_width
            draw_dimension_line(ax, 
                              panel_x, start_y - 5,
                              panel_x + panel_width, start_y - 5,
                              f"{item.get_panel_width():.1f}\"",
                              offset=0)
    
    # Add overall dimensions
    draw_dimension_line(ax,
                       start_x, start_y - 10,
                       start_x + scaled_width, start_y - 10,
                       f"{item.width:.1f}\"")
    
    draw_vertical_dimension(ax,
                           start_x + scaled_width + 5, start_y,
                           start_y + scaled_height,
                           f"{item.height:.1f}\"",
                           side='right')
    
    # Add X/O notation for panel types
    if 'CASEMENT' in item.type.upper():
        # Add 'X' markers for operable panels
        for i in range(panel_count):
            panel_x = start_x + (i + 0.5) * (scaled_width / panel_count)
            panel_y = start_y + scaled_height / 2
            ax.text(panel_x, panel_y, 'X',
                   ha='center', va='center',
                   fontsize=FONTS['header']['size'],
                   fontweight='bold')
    elif 'FIXED' in item.type.upper():
        # Add 'O' marker for fixed panel
        ax.text(start_x + scaled_width/2, start_y + scaled_height/2, 'O',
               ha='center', va='center',
               fontsize=FONTS['header']['size'],
               fontweight='bold')


# =============================================================================
# SPECIFICATION TABLE
# =============================================================================

def draw_specification_table(ax: plt.Axes, item: WindowDoorItem):
    """
    Draw the specification table in the left column.
    
    Args:
        ax: Matplotlib axes
        item: WindowDoorItem instance
    """
    # Table position and sizing
    x_start = 5
    y_start = 85
    row_height = 12
    col_width = 90
    
    # Table data
    specs = [
        ('Item#', item.item_id),
        ('Glass', f"Series {item.series}\n{item.glass}"),
        ('Frame Color', item.frame_color),
        ('Screen Size', item.screen),
        ('Hardware', 'Standard'),  # Could be dynamic
        ('Insulated Frame', 'Yes' if item.series in ['80', '86', '65'] else 'No'),
        ('Quantity', str(item.quantity)),
    ]
    
    y = y_start
    for label, value in specs:
        # Draw cell border
        cell = Rectangle((x_start, y - row_height), col_width, row_height,
                        linewidth=LINE_WEIGHTS['thin'],
                        edgecolor=COLORS['black'],
                        facecolor='none')
        ax.add_patch(cell)
        
        # Add text
        ax.text(x_start + 2, y - row_height/2, f"{label}: {value}",
               va='center', ha='left',
               fontsize=FONTS['table']['size'],
               fontfamily=FONTS['table']['family'])
        
        y -= row_height


# =============================================================================
# COMPANY HEADER
# =============================================================================

def draw_company_header(ax: plt.Axes):
    """Draw company header in the right column."""
    # Logo (stylized text)
    ax.text(50, 85, 'raven',
           ha='center', va='center',
           fontsize=FONTS['logo']['size'],
           fontweight=FONTS['logo']['weight'],
           fontfamily='Arial Black' if 'Arial Black' in plt.rcParams['font.sans-serif'] else 'Arial')
    
    # Draw box around logo
    logo_box = Rectangle((20, 80), 60, 10,
                         linewidth=LINE_WEIGHTS['medium'],
                         edgecolor=COLORS['black'],
                         facecolor='none')
    ax.add_patch(logo_box)
    
    # Company info
    info_y = 70
    for line in COMPANY_ADDRESS.split('\n'):
        ax.text(50, info_y, line,
               ha='center', va='top',
               fontsize=FONTS['body']['size'])
        info_y -= 5
    
    ax.text(50, info_y - 5, f"Cell: {COMPANY_PHONE}",
           ha='center', va='top',
           fontsize=FONTS['body']['size'])
    
    ax.text(50, info_y - 10, f"Website:\n{COMPANY_WEBSITE}",
           ha='center', va='top',
           fontsize=FONTS['body']['size'])


# =============================================================================
# PROJECT INFORMATION TABLE
# =============================================================================

def draw_project_info_table(ax: plt.Axes, item: WindowDoorItem):
    """Draw project information table in the right column."""
    x_start = 5
    y_start = 95
    row_height = 15
    col_width = 90
    
    # Project data
    today = datetime.now().strftime('%Y-%m-%d')
    info = [
        ('Drawing date', today),
        ('Serial number', item.item_id),
        ('Designer', 'Raven Custom Glass'),
        ('Revision', '1'),
        ('Construction', 'New'),
        ('Date', today),
    ]
    
    y = y_start
    for label, value in info:
        # Draw cell border
        cell = Rectangle((x_start, y - row_height), col_width, row_height,
                        linewidth=LINE_WEIGHTS['thin'],
                        edgecolor=COLORS['black'],
                        facecolor='none')
        ax.add_patch(cell)
        
        # Add label
        ax.text(x_start + 2, y - 5, label,
               va='top', ha='left',
               fontsize=FONTS['table']['size'],
               fontweight='bold')
        
        # Add value
        ax.text(x_start + 2, y - row_height + 2, value,
               va='bottom', ha='left',
               fontsize=FONTS['table']['size'])
        
        y -= row_height


# =============================================================================
# MAIN GENERATION FUNCTION
# =============================================================================

def generate_shop_drawing(item: WindowDoorItem, output_path: str):
    """
    Generate a complete professional shop drawing.
    
    Args:
        item: WindowDoorItem instance with all specifications
        output_path: Path to save PDF file
    """
    # Create layout
    fig, axes = create_drawing_layout()
    
    # Draw each component
    draw_specification_table(axes['spec_table'], item)
    
    # Cross-section (placeholder - implement based on series)
    axes['cross_section'].text(50, 80, 'Drawn from inside view',
                               ha='center', fontsize=8)
    draw_frame_cross_section(axes['cross_section'], item.series,
                            30, 30, 40, 30, show_hardware=True)
    
    # Elevation view
    draw_elevation_view(axes['elevation'], item)
    
    # Person and swing arrow
    if item.is_door() or 'CASEMENT' in item.type.upper():
        draw_person_silhouette(axes['person'], 30, 20, height=68)
        if 'right' in item.swing_direction.lower():
            draw_swing_arrow(axes['person'], 50, 40, 20, angle=90, direction='right')
        elif 'left' in item.swing_direction.lower():
            draw_swing_arrow(axes['person'], 50, 40, 20, angle=90, direction='left')
    
    # Plan view (placeholder)
    axes['plan'].text(50, 50, 'Plan View\n(Horizontal Section)',
                     ha='center', va='center')
    
    # Company header
    draw_company_header(axes['header'])
    
    # Thumbnails (placeholder)
    axes['thumbnails'].text(50, 50, 'Thumbnail Icons',
                           ha='center', va='center')
    
    # Project info
    draw_project_info_table(axes['project_info'], item)
    
    # Save to PDF
    plt.savefig(output_path, dpi=DPI, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✓ Shop drawing generated: {output_path}")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    # Example data (simulating Google Sheets input)
    example_data = {
        'item_id': 'W001',
        'room': 'Bed 5',
        'width': 72,
        'height': 60,
        'type': 'DOUBLE CASEMENT',
        'swing_direction': 'NA',
        'quantity': 1,
        'series': '86',
        'nail_fin': 'Stucco setback 35mm from outside',
        'frame_color': 'Black',
        'glass': 'Clear Low E',
        'grids': 'NONE',
        'screen': 'NONE',
        'po_number': 'STARFALL',
        'project_name': 'Demo Project',
    }
    
    # Create item instance
    item = WindowDoorItem(example_data)
    
    # Generate drawing
    generate_shop_drawing(item, 'example_shop_drawing.pdf')
    print("\n✓ Example drawing generated successfully!")
    print("Check 'example_shop_drawing.pdf' to see the output.")
