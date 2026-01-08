"""
Professional 2D Technical Drawing Layout Engine
Implements 3-column grid layout with 8 zones for shop drawings
"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
import numpy as np
from typing import Tuple, Dict, List


class DrawingLayout:
    """
    Manages professional 3-column layout for technical drawings
    
    Layout structure:
    - Left Column (30%): Specification tables
    - Center Column (45%): Elevation/section drawings
    - Right Column (25%): Headers, project info
    
    8 Zones:
    - Zone 1 (L-Top): Spec table - window/door specs
    - Zone 2 (L-Bottom): Spec table - materials/finish
    - Zone 3 (C-Top): Main elevation drawing
    - Zone 4 (C-Bottom): Cross-section details
    - Zone 5 (R-Top): Company header block
    - Zone 6 (R-Mid-Top): Drawing title/type
    - Zone 7 (R-Mid-Bot): Project information
    - Zone 8 (R-Bottom): Revision/sign-off block
    """
    
    def __init__(self, figsize: Tuple[float, float] = (11, 17)):
        """Initialize drawing layout with standard letter size (landscape)"""
        self.figsize = figsize
        self.fig = None
        self.gs = None
        self.zones = {}
        self._column_widths = [0.30, 0.45, 0.25]  # 30%, 45%, 25%
        
    def create_layout(self) -> Tuple[plt.Figure, Dict]:
        """
        Create 8-zone grid layout
        
        Returns:
            Tuple of (figure, zones_dict)
            zones_dict keys: 'spec_1', 'spec_2', 'elevation', 'section', 
                           'header', 'title', 'project_info', 'revision'
        """
        self.fig, axes_dict = plt.subplots(
            figsize=self.figsize,
            nrows=1, ncols=1
        )
        
        # Remove the single axis
        plt.close(self.fig)
        self.fig = plt.figure(figsize=self.figsize)
        
        # Create main GridSpec with 3 columns
        self.gs = gridspec.GridSpec(
            nrows=8,
            ncols=3,
            figure=self.fig,
            width_ratios=self._column_widths,
            height_ratios=[1, 1, 2, 2, 1, 1, 1.5, 0.8],
            hspace=0.3,
            wspace=0.2,
            left=0.05,
            right=0.95,
            top=0.95,
            bottom=0.05
        )
        
        # Zone 1: Left column, top - Spec table (window/door specs)
        self.zones['spec_1'] = self.fig.add_subplot(
            self.gs[0:2, 0]
        )
        
        # Zone 2: Left column, bottom - Material specs
        self.zones['spec_2'] = self.fig.add_subplot(
            self.gs[2:5, 0]
        )
        
        # Zone 3: Center column, top - Main elevation
        self.zones['elevation'] = self.fig.add_subplot(
            self.gs[0:4, 1]
        )
        
        # Zone 4: Center column, bottom - Cross-section
        self.zones['section'] = self.fig.add_subplot(
            self.gs[4:7, 1]
        )
        
        # Zone 5: Right column, top - Company header
        self.zones['header'] = self.fig.add_subplot(
            self.gs[0:1, 2]
        )
        
        # Zone 6: Right column, upper-mid - Drawing title
        self.zones['title'] = self.fig.add_subplot(
            self.gs[1:2, 2]
        )
        
        # Zone 7: Right column, middle - Project info
        self.zones['project_info'] = self.fig.add_subplot(
            self.gs[2:6, 2]
        )
        
        # Zone 8: Right column, bottom - Revision block
        self.zones['revision'] = self.fig.add_subplot(
            self.gs[6:8, 2]
        )
        
        # Configure all zones
        for zone_name, ax in self.zones.items():
            self._configure_zone(ax, zone_name)
        
        return self.fig, self.zones
    
    def _configure_zone(self, ax, zone_name: str):
        """Configure axis for specific zone"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Add subtle border for debugging/layout verification
        rect = Rectangle((0, 0), 10, 10, fill=False, 
                         edgecolor='lightgray', linewidth=0.5)
        ax.add_patch(rect)
    
    def get_zone(self, zone_name: str):
        """Get axis for specific zone"""
        if zone_name not in self.zones:
            raise ValueError(f"Unknown zone: {zone_name}. Valid zones: {list(self.zones.keys())}")
        return self.zones[zone_name]
    
    def save(self, filepath: str, dpi: int = 300):
        """Save figure to file"""
        self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"Drawing saved to: {filepath}")
    
    def show(self):
        """Display figure"""
        plt.show()
