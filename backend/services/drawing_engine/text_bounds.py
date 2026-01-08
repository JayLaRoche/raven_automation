"""
Text Bounds and Collision Detection
Handles text positioning, collision detection, and smart text layout
Uses ReportLab's stringWidth for accurate text measurement
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class TextBounds:
    """Represents text bounding box with position and dimensions"""
    x: float  # Left edge
    y: float  # Bottom edge
    width: float  # Text width
    height: float  # Text height (ascender to descender)
    
    @property
    def x_min(self) -> float:
        return self.x
    
    @property
    def x_max(self) -> float:
        return self.x + self.width
    
    @property
    def y_min(self) -> float:
        return self.y
    
    @property
    def y_max(self) -> float:
        return self.y + self.height
    
    def overlaps_with(self, other: 'TextBounds', padding: float = 0) -> bool:
        """
        Check if this bounding box overlaps with another
        
        Args:
            other: Another TextBounds object
            padding: Extra padding to consider (increases overlap detection area)
        
        Returns:
            True if bounding boxes overlap (considering padding)
        """
        return (
            self.x_min - padding <= other.x_max + padding and
            self.x_max + padding >= other.x_min - padding and
            self.y_min - padding <= other.y_max + padding and
            self.y_max + padding >= other.y_min - padding
        )
    
    def distance_to(self, other: 'TextBounds') -> float:
        """
        Calculate minimum distance between this and another bounding box
        
        Args:
            other: Another TextBounds object
        
        Returns:
            Distance between closest edges (0 if overlapping)
        """
        # Find closest points between boxes
        dx = max(self.x_min - other.x_max, 0, other.x_min - self.x_max)
        dy = max(self.y_min - other.y_max, 0, other.y_min - self.y_max)
        return math.sqrt(dx**2 + dy**2)


class TextBoundsCalculator:
    """
    Calculates text bounds and handles collision detection
    Uses approximate font measurements (can integrate ReportLab later)
    """
    
    # Standard font dimensions (approximate at different sizes)
    # Format: font_size -> (char_width_ratio, line_height_ratio)
    FONT_METRICS = {
        5: (0.45, 0.6),
        6: (0.50, 0.7),
        7: (0.55, 0.8),
        8: (0.60, 0.9),
        9: (0.65, 1.0),
        10: (0.70, 1.1),
        12: (0.80, 1.3),
        14: (0.90, 1.5),
    }
    
    @staticmethod
    def _get_font_metrics(fontsize: int) -> Tuple[float, float]:
        """
        Get or interpolate font metrics for a given font size
        
        Args:
            fontsize: Font size in points
        
        Returns:
            Tuple of (char_width_ratio, line_height_ratio)
        """
        if fontsize in TextBoundsCalculator.FONT_METRICS:
            return TextBoundsCalculator.FONT_METRICS[fontsize]
        
        sizes = sorted(TextBoundsCalculator.FONT_METRICS.keys())
        if fontsize < sizes[0]:
            return TextBoundsCalculator.FONT_METRICS[sizes[0]]
        if fontsize > sizes[-1]:
            return TextBoundsCalculator.FONT_METRICS[sizes[-1]]
        
        for i in range(len(sizes) - 1):
            if sizes[i] < fontsize < sizes[i+1]:
                f = (fontsize - sizes[i]) / (sizes[i+1] - sizes[i])
                char_width_ratio = (
                    TextBoundsCalculator.FONT_METRICS[sizes[i]][0] +
                    f * (TextBoundsCalculator.FONT_METRICS[sizes[i+1]][0] -
                         TextBoundsCalculator.FONT_METRICS[sizes[i]][0])
                )
                line_height_ratio = (
                    TextBoundsCalculator.FONT_METRICS[sizes[i]][1] +
                    f * (TextBoundsCalculator.FONT_METRICS[sizes[i+1]][1] -
                         TextBoundsCalculator.FONT_METRICS[sizes[i]][1])
                )
                return char_width_ratio, line_height_ratio
        
        return TextBoundsCalculator.FONT_METRICS[sizes[0]]

    @staticmethod
    def _adjust_position_for_alignment(
        x: float, y: float, width: float, height: float,
        ha: str, va: str
    ) -> Tuple[float, float]:
        """
        Adjust position based on horizontal and vertical alignment
        
        Args:
            x, y: Current position
            width, height: Text dimensions
            ha: Horizontal alignment
            va: Vertical alignment
        
        Returns:
            Adjusted (x, y) coordinates
        """
        if ha == 'center':
            x = x - width / 2
        elif ha == 'right':
            x = x - width
        
        if va == 'center':
            y = y - height / 2
        elif va == 'top':
            y = y - height
        elif va == 'baseline':
            y = y - height * 0.75
        
        return x, y

    @staticmethod
    def get_text_bounds(
        text: str,
        x: float,
        y: float,
        fontsize: int = 8,
        ha: str = 'left',
        va: str = 'baseline',
        bold: bool = False
    ) -> TextBounds:
        """
        Calculate bounding box for text
        
        Args:
            text: Text string
            x, y: Position coordinates
            fontsize: Font size in points
            ha: Horizontal alignment ('left', 'center', 'right')
            va: Vertical alignment ('baseline', 'bottom', 'center', 'top')
            bold: Whether text is bold (affects width)
        
        Returns:
            TextBounds object with calculated dimensions
        """
        char_width_ratio, line_height_ratio = TextBoundsCalculator._get_font_metrics(fontsize)
        
        bold_factor = 1.1 if bold else 1.0
        width = len(text) * fontsize * char_width_ratio * bold_factor
        height = fontsize * line_height_ratio
        
        x, y = TextBoundsCalculator._adjust_position_for_alignment(
            x, y, width, height, ha, va
        )
        
        return TextBounds(x=x, y=y, width=width, height=height)


class CollisionDetector:
    """Detects and resolves text collisions"""
    
    def __init__(self, min_spacing: float = 2.0):
        """
        Initialize collision detector
        
        Args:
            min_spacing: Minimum spacing between text elements in mm
        """
        self.min_spacing = min_spacing
        self.placed_bounds: List[TextBounds] = []
    
    def add_bounds(self, bounds: TextBounds) -> None:
        """Register a text bounding box"""
        self.placed_bounds.append(bounds)
    
    def check_collision(self, bounds: TextBounds, padding: float = 0) -> bool:
        """
        Check if text bounds collide with any placed bounds
        
        Args:
            bounds: TextBounds to check
            padding: Extra spacing to consider
        
        Returns:
            True if collision detected
        """
        effective_padding = self.min_spacing + padding
        for placed in self.placed_bounds:
            if bounds.overlaps_with(placed, padding=effective_padding):
                return True
        return False
    
    def find_safe_position(
        self,
        base_x: float,
        base_y: float,
        text: str,
        fontsize: int = 8,
        ha: str = 'center',
        va: str = 'center',
        bold: bool = False,
        search_radius: float = 20,
        search_steps: int = 16
    ) -> Tuple[float, float, bool]:
        """
        Find a safe position for text that avoids collisions
        
        Args:
            base_x, base_y: Preferred position
            text: Text string to place
            fontsize: Font size
            ha, va: Alignment
            bold: Bold font flag
            search_radius: How far to search for safe position
            search_steps: Number of angles to try
        
        Returns:
            Tuple of (x, y, found) where found indicates if safe position found
        """
        # Try base position first
        bounds = TextBoundsCalculator.get_text_bounds(
            text, base_x, base_y, fontsize, ha, va, bold
        )
        
        if not self.check_collision(bounds):
            self.add_bounds(bounds)
            return base_x, base_y, True
        
        # Search in spiral pattern around base position
        for step in range(1, search_steps + 1):
            angle_step = 360.0 / search_steps
            
            for i in range(search_steps):
                angle = i * angle_step
                rad = math.radians(angle)
                distance = search_radius * (step / search_steps)
                
                offset_x = distance * math.cos(rad)
                offset_y = distance * math.sin(rad)
                
                new_x = base_x + offset_x
                new_y = base_y + offset_y
                
                bounds = TextBoundsCalculator.get_text_bounds(
                    text, new_x, new_y, fontsize, ha, va, bold
                )
                
                if not self.check_collision(bounds):
                    self.add_bounds(bounds)
                    return new_x, new_y, True
        
        # No safe position found, use base and force placement
        self.add_bounds(bounds)
        return base_x, base_y, False
    
    def clear(self) -> None:
        """Clear all registered bounds"""
        self.placed_bounds = []


class DimensionTextPositioner:
    """Smart positioning for dimension line text labels"""
    
    @staticmethod
    def calculate_offset(
        dimension_text: str,
        dimension_length: float,
        fontsize: int = 8,
        min_clearance: float = 1.5
    ) -> float:
        """
        Calculate vertical offset for dimension text to avoid line overlap
        
        Args:
            dimension_text: Text to display (e.g., "72\"")
            dimension_length: Length of dimension line
            fontsize: Font size
            min_clearance: Minimum space between text and line
        
        Returns:
            Y offset for text placement
        """
        # Estimate text width
        char_width = fontsize * 0.6
        text_width = len(dimension_text) * char_width
        
        # Text height
        text_height = fontsize * 1.0
        
        # If text width exceeds dimension length, need extra offset
        if text_width > dimension_length:
            # Extra offset to accommodate overlapping text
            extra_offset = (text_width - dimension_length) / 2 + min_clearance
        else:
            extra_offset = min_clearance
        
        return text_height / 2 + extra_offset
    
    @staticmethod
    def find_best_dimension_position(
        x1: float, x2: float, y: float,
        dimension_text: str,
        fontsize: int = 8,
        preferred_above: bool = True,
        nearby_dimensions: Optional[List[Tuple[float, float]]] = None
    ) -> Tuple[float, float, bool]:
        """
        Find best position for dimension text
        
        Args:
            x1, x2: Start and end X coordinates of dimension line
            y: Y coordinate of dimension line
            dimension_text: Text to display
            fontsize: Font size
            preferred_above: Prefer placing text above line?
            nearby_dimensions: List of (y_pos, height) for nearby dimensions
        
        Returns:
            Tuple of (text_y, offset, is_above)
        """
        offset = DimensionTextPositioner.calculate_offset(
            dimension_text, abs(x2 - x1), fontsize
        )
        
        text_y_above = y + offset
        text_y_below = y - offset
        
        # If no nearby dimensions, use preferred position
        if not nearby_dimensions:
            if preferred_above:
                return text_y_above, offset, True
            else:
                return text_y_below, offset, False
        
        # Check which position has fewer conflicts
        conflicts_above = sum(
            1 for dim_y, dim_h in nearby_dimensions
            if abs(text_y_above - dim_y) < dim_h + 2
        )
        conflicts_below = sum(
            1 for dim_y, dim_h in nearby_dimensions
            if abs(text_y_below - dim_y) < dim_h + 2
        )
        
        if conflicts_above <= conflicts_below:
            return text_y_above, offset, True
        else:
            return text_y_below, offset, False


class SpecificationTableLayouter:
    """Smart layout for specification table cells"""
    
    @staticmethod
    def calculate_column_widths(
        data: List[Tuple[str, str]],
        total_width: float,
        min_label_width: float = 30,
        min_value_width: float = 30,
        char_width: float = 1.2
    ) -> Tuple[float, float]:
        """
        Calculate optimal column widths based on content
        
        Args:
            data: List of (label, value) tuples
            total_width: Total available width
            min_label_width: Minimum width for label column
            min_value_width: Minimum width for value column
            char_width: Width per character (mm)
        
        Returns:
            Tuple of (label_width, value_width)
        """
        # Find longest label and value
        max_label_len = max(len(label) for label, _ in data) if data else 0
        max_value_len = max(len(value) for _, value in data) if data else 0
        
        # Calculate required widths
        required_label_width = max(
            max_label_len * char_width + 4,  # +4 for padding
            min_label_width
        )
        required_value_width = max(
            max_value_len * char_width + 4,
            min_value_width
        )
        
        # If total required width exceeds available, scale down
        total_required = required_label_width + required_value_width
        if total_required > total_width:
            scale_factor = total_width / total_required
            label_width = required_label_width * scale_factor
            value_width = required_value_width * scale_factor
        else:
            label_width = required_label_width
            value_width = total_width - required_label_width
        
        return label_width, value_width
    
    @staticmethod
    def wrap_text(
        text: str,
        max_width: float,
        char_width: float = 1.2
    ) -> List[str]:
        """
        Wrap text to fit within width
        
        Args:
            text: Text to wrap
            max_width: Maximum width in mm
            char_width: Width per character
        
        Returns:
            List of text lines
        """
        chars_per_line = int(max_width / char_width)
        
        if chars_per_line <= 0:
            return [text]
        
        lines = []
        words = text.split(' ')
        current_line = ''
        
        for word in words:
            if len(current_line) + len(word) + 1 <= chars_per_line:
                current_line += (word if not current_line else ' ' + word)
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]
    
    @staticmethod
    def truncate_text(
        text: str,
        max_width: float,
        char_width: float = 1.2,
        suffix: str = '...'
    ) -> str:
        """
        Truncate text to fit within width
        
        Args:
            text: Text to truncate
            max_width: Maximum width in mm
            char_width: Width per character
            suffix: Suffix to add when truncated
        
        Returns:
            Truncated text
        """
        chars_per_line = int(max_width / char_width)
        
        if len(text) <= chars_per_line:
            return text
        
        # Reserve space for suffix
        available_chars = max(1, chars_per_line - len(suffix))
        return text[:available_chars] + suffix
