"""
CAD-Style Dimension Line Generator
Creates professional dimension annotations with extension lines and arrows
Includes collision detection and smart text positioning
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
from typing import Tuple, Optional, List
from .text_bounds import DimensionTextPositioner, TextBoundsCalculator, TextBounds


class DimensionLine:
    """
    CAD-style dimension line with:
    - Extension lines (1/8" beyond dimension)
    - Dimension line with arrow ends
    - Dimension text centered above/below with smart positioning
    - Collision detection to avoid overlapping text
    """
    
    # Standard CAD dimension styles
    ARROW_SIZE = 0.15  # inches
    EXTENSION_OFFSET = 0.125  # 1/8" beyond dimension
    TEXT_OFFSET = 0.2  # Distance from dimension line to text
    MIN_TEXT_SPACING = 0.5  # Minimum spacing between dimension texts
    LINE_WIDTH = 1.0  # points
    
    def __init__(self, ax, scale: float = 1.0):
        """
        Initialize dimension line drawer
        
        Args:
            ax: Matplotlib axis
            scale: Scaling factor (inches to plot units)
        """
        self.ax = ax
        self.scale = scale
        self.dimension_positions: List[Tuple[float, float]] = []  # Track placed dimensions
    
    def _calculate_text_offset_smart(
        self,
        x1: float, x2: float,
        dimension: str,
        base_offset: float = 0.2
    ) -> float:
        """
        Calculate smart offset for dimension text based on text width
        
        Args:
            x1, x2: Start and end coordinates
            dimension: Text string
            base_offset: Base offset distance
        
        Returns:
            Adjusted offset for text placement
        """
        dimension_length = abs(x2 - x1)
        calculated_offset = DimensionTextPositioner.calculate_offset(
            dimension,
            dimension_length,
            fontsize=9
        )
        return max(base_offset, calculated_offset / self.scale if self.scale > 0 else base_offset)
    
    def draw_horizontal(
        self,
        x1: float, x2: float,
        y: float,
        dimension: str,
        above: bool = True,
        color: str = 'black',
        check_collisions: bool = True
    ):
        """
        Draw horizontal dimension line with smart text positioning
        
        Args:
            x1, x2: Start and end X coordinates
            y: Y coordinate for dimension line
            dimension: Text label (e.g., "72\"")
            above: If True, text above line; else below
            color: Line and text color
            check_collisions: Enable collision detection
        """
        # Extension lines (1/8" past start/end)
        ext_offset = self.EXTENSION_OFFSET * self.scale
        
        # Draw extension lines
        self.ax.plot(
            [x1, x1],
            [y - ext_offset, y + ext_offset],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        self.ax.plot(
            [x2, x2],
            [y - ext_offset, y + ext_offset],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Draw dimension line
        self.ax.plot(
            [x1, x2],
            [y, y],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Draw arrow ends
        arrow_size = self.ARROW_SIZE * self.scale
        
        # Left arrow
        self.ax.annotate(
            '', xy=(x1 + arrow_size, y),
            xytext=(x1, y),
            arrowprops=dict(arrowstyle='->', lw=self.LINE_WIDTH, color=color)
        )
        
        # Right arrow
        self.ax.annotate(
            '', xy=(x2 - arrow_size, y),
            xytext=(x2, y),
            arrowprops=dict(arrowstyle='->', lw=self.LINE_WIDTH, color=color)
        )
        
        # Calculate smart offset for dimension text
        text_offset = self._calculate_text_offset_smart(x1, x2, dimension)
        
        # Determine text position with collision avoidance
        text_x = (x1 + x2) / 2
        
        if check_collisions and self.dimension_positions:
            # Check if any nearby dimension conflicts
            nearby_conflicts = [
                (pos_y, 0.4) for pos_x, pos_y in self.dimension_positions
                if abs(pos_x - text_x) < abs(x2 - x1) * 0.6
            ]
            
            if nearby_conflicts and above:
                # Use DimensionTextPositioner for smart positioning
                text_y, _, is_above = DimensionTextPositioner.find_best_dimension_position(
                    x1, x2, y, dimension,
                    fontsize=9,
                    preferred_above=above,
                    nearby_dimensions=nearby_conflicts
                )
            else:
                text_y = y + text_offset * self.scale if above else y - text_offset * self.scale
        else:
            text_y = y + text_offset * self.scale if above else y - text_offset * self.scale
        
        # Track this dimension position
        self.dimension_positions.append((text_x, text_y))
        
        # Add dimension text with padding
        self.ax.text(
            text_x, text_y,
            dimension,
            ha='center', va='bottom' if above else 'top',
            fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='none', alpha=0.9),
            zorder=10  # Ensure text is above other elements
        )
    
    def draw_vertical(
        self,
        x: float,
        y1: float, y2: float,
        dimension: str,
        left: bool = True,
        color: str = 'black',
        check_collisions: bool = True
    ):
        """
        Draw vertical dimension line with smart text positioning
        
        Args:
            x: X coordinate for dimension line
            y1, y2: Start and end Y coordinates
            dimension: Text label (e.g., "60\"")
            left: If True, dimension to left; else to right
            color: Line and text color
            check_collisions: Enable collision detection
        """
        # Extension lines
        ext_offset = self.EXTENSION_OFFSET * self.scale
        
        # Draw extension lines
        self.ax.plot(
            [x - ext_offset, x + ext_offset],
            [y1, y1],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        self.ax.plot(
            [x - ext_offset, x + ext_offset],
            [y2, y2],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Draw dimension line
        self.ax.plot(
            [x, x],
            [y1, y2],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Draw arrow ends
        arrow_size = self.ARROW_SIZE * self.scale
        
        # Bottom arrow
        self.ax.annotate(
            '', xy=(x, y1 + arrow_size),
            xytext=(x, y1),
            arrowprops=dict(arrowstyle='->', lw=self.LINE_WIDTH, color=color)
        )
        
        # Top arrow
        self.ax.annotate(
            '', xy=(x, y2 - arrow_size),
            xytext=(x, y2),
            arrowprops=dict(arrowstyle='->', lw=self.LINE_WIDTH, color=color)
        )
        
        # Calculate smart offset for dimension text
        dimension_length = abs(y2 - y1)
        text_offset = DimensionTextPositioner.calculate_offset(
            dimension, dimension_length, fontsize=9
        ) / self.scale if self.scale > 0 else self.TEXT_OFFSET
        
        # Determine text position
        text_y = (y1 + y2) / 2
        text_x = x - text_offset * self.scale if left else x + text_offset * self.scale
        
        # Track position
        self.dimension_positions.append((text_x, text_y))
        
        # Add dimension text (rotated) with better padding
        self.ax.text(
            text_x, text_y,
            dimension,
            ha='right' if left else 'left',
            va='center',
            fontsize=9, fontweight='bold',
            rotation=90,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='none', alpha=0.9),
            zorder=10
        )
    
    def draw_diagonal(
        self,
        x1: float, y1: float,
        x2: float, y2: float,
        dimension: str,
        offset: float = 0.3,
        color: str = 'black'
    ):
        """
        Draw diagonal dimension line with proper spacing
        
        Args:
            x1, y1: Start point
            x2, y2: End point
            dimension: Text label
            offset: Offset distance for dimension line (with collision avoidance)
            color: Line color
        """
        # Calculate angle
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        # Calculate smart offset based on text length
        text_offset = DimensionTextPositioner.calculate_offset(
            dimension, length, fontsize=9
        ) / self.scale if self.scale > 0 else offset
        
        # Extension lines perpendicular to dimension line
        ext_offset = self.EXTENSION_OFFSET * self.scale
        perp_angle = angle + np.pi / 2
        
        # Draw extension lines
        ext_dx = ext_offset * np.cos(perp_angle)
        ext_dy = ext_offset * np.sin(perp_angle)
        
        self.ax.plot(
            [x1 - ext_dx, x1 + ext_dx],
            [y1 - ext_dy, y1 + ext_dy],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        self.ax.plot(
            [x2 - ext_dx, x2 + ext_dx],
            [y2 - ext_dy, y2 + ext_dy],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Draw dimension line parallel to the measured line
        offset_dx = text_offset * np.cos(perp_angle)
        offset_dy = text_offset * np.sin(perp_angle)
        
        self.ax.plot(
            [x1 + offset_dx, x2 + offset_dx],
            [y1 + offset_dy, y2 + offset_dy],
            color=color,
            linewidth=self.LINE_WIDTH
        )
        
        # Add text at midpoint
        mid_x = (x1 + x2) / 2 + offset_dx
        mid_y = (y1 + y2) / 2 + offset_dy
        
        self.dimension_positions.append((mid_x, mid_y))
        
        self.ax.text(
            mid_x, mid_y,
            dimension,
            ha='center', va='bottom',
            fontsize=9, fontweight='bold',
            rotation=np.degrees(angle),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='none', alpha=0.9),
            zorder=10
        )
    
    def clear_positions(self) -> None:
        """Reset tracked dimension positions for new drawing"""
        self.dimension_positions = []


def draw_window_frame_with_dimensions(
    ax,
    width: float,
    height: float,
    frame_width: float = 2.0,
    scale: float = 1.0
):
    """
    Draw a window frame with full CAD-style dimensions
    
    Args:
        ax: Matplotlib axis
        width: Window width in inches
        height: Window height in inches
        frame_width: Frame thickness in inches
        scale: Scaling factor (inches to plot units)
    """
    # Convert to plot units
    w = width * scale
    h = height * scale
    fw = frame_width * scale
    
    # Center drawing in axis
    x_center, y_center = 5, 5
    x1 = x_center - w / 2
    x2 = x_center + w / 2
    y1 = y_center - h / 2
    y2 = y_center + h / 2
    
    # Draw frame (outer rectangle)
    frame = patches.Rectangle(
        (x1, y1), w, h,
        linewidth=2, edgecolor='black', facecolor='lightblue', alpha=0.3
    )
    ax.add_patch(frame)
    
    # Draw glass area (inner rectangle with frame offset)
    glass = patches.Rectangle(
        (x1 + fw, y1 + fw), w - 2*fw, h - 2*fw,
        linewidth=1, edgecolor='blue', facecolor='none', linestyle='--'
    )
    ax.add_patch(glass)
    
    # Add dimensions
    dim_drawer = DimensionLine(ax, scale)
    
    # Overall width dimension (bottom)
    dim_drawer.draw_horizontal(x1, x2, y1 - 0.8, f'{width}"', above=False)
    
    # Overall height dimension (left side)
    dim_drawer.draw_vertical(x1 - 0.8, y1, y2, f'{height}"', left=True)
    
    return dim_drawer
