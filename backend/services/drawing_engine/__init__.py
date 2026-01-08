"""
Professional Drawing Engine - Phase 1
Technical shop drawing generator with CAD-style dimensions and layouts
"""

from .layout import DrawingLayout
from .dimensions import DimensionLine, draw_window_frame_with_dimensions
from .components import (
    SpecificationTable,
    CompanyHeader,
    DrawingTitle,
    ProjectInfoBlock,
    RevisionBlock
)
from .main import ProfessionalDrawingGenerator

__version__ = "1.0.0"
__all__ = [
    'DrawingLayout',
    'DimensionLine',
    'draw_window_frame_with_dimensions',
    'SpecificationTable',
    'CompanyHeader',
    'DrawingTitle',
    'ProjectInfoBlock',
    'RevisionBlock',
    'ProfessionalDrawingGenerator',
]
