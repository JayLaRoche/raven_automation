"""
Professional Drawing Components
Specification tables, headers, and info blocks for technical drawings
Includes smart text positioning and overflow prevention
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from typing import List, Dict, Tuple
from .text_bounds import SpecificationTableLayouter, TextBoundsCalculator


class SpecificationTable:
    """Render specification tables in drawing zones"""
    
    def __init__(self, ax):
        """
        Initialize specification table drawer
        
        Args:
            ax: Matplotlib axis
        """
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_table(
        self,
        data: List[Tuple[str, str]],
        title: str = None,
        title_bg: str = '#333333',
        title_fg: str = 'white',
        min_column_padding: float = 2.0
    ):
        """
        Draw a specification table with smart text wrapping and overflow prevention
        
        Args:
            data: List of (label, value) tuples
            title: Table title
            title_bg: Title background color
            title_fg: Title text color
            min_column_padding: Minimum padding in mm for text in cells
        """
        # Calculate optimal column widths
        available_width = 9.6  # Roughly the usable width
        label_width, value_width = SpecificationTableLayouter.calculate_column_widths(
            data, available_width
        )
        
        # Draw title
        if title:
            title_box = FancyBboxPatch(
                (0.2, 8.5), 9.6, 1.2,
                boxstyle="round,pad=0.1",
                facecolor=title_bg,
                edgecolor='black',
                linewidth=1.5
            )
            self.ax.add_patch(title_box)
            
            # Truncate title if it's too long
            truncated_title = SpecificationTableLayouter.truncate_text(
                title, 9.6 - 0.4, char_width=1.1, suffix='...'
            )
            
            self.ax.text(
                5, 9.1,
                truncated_title,
                ha='center', va='center',
                fontsize=11, fontweight='bold',
                color=title_fg
            )
        
        # Draw table rows
        row_height = 1.0
        start_y = 8.5 if title else 10
        
        for i, (label, value) in enumerate(data):
            y = start_y - (i + 1) * row_height
            
            if y < 0.5:  # Don't draw beyond axis
                break
            
            # Draw row background (alternating)
            if i % 2 == 0:
                bg = patches.Rectangle(
                    (0.2, y - row_height + 0.2), 9.6, row_height - 0.2,
                    facecolor='#f5f5f5',
                    edgecolor='lightgray',
                    linewidth=0.5
                )
            else:
                bg = patches.Rectangle(
                    (0.2, y - row_height + 0.2), 9.6, row_height - 0.2,
                    facecolor='white',
                    edgecolor='lightgray',
                    linewidth=0.5
                )
            self.ax.add_patch(bg)
            
            # Process label with text wrapping and truncation
            label_x = 0.5
            label_padding = min_column_padding
            max_label_width = label_width - label_padding
            
            # Truncate label to fit width
            truncated_label = SpecificationTableLayouter.truncate_text(
                label, max_label_width, char_width=1.0, suffix='...'
            )
            
            text_y = y - row_height / 2
            
            self.ax.text(
                label_x, text_y,
                truncated_label,
                ha='left', va='center',
                fontsize=8, fontweight='bold',
                wrap=True
            )
            
            # Process value with text wrapping and truncation
            value_x = label_width + 0.3
            max_value_width = value_width - min_column_padding
            
            # Truncate value to fit width
            truncated_value = SpecificationTableLayouter.truncate_text(
                value, max_value_width, char_width=1.0, suffix='...'
            )
            
            self.ax.text(
                value_x, text_y,
                truncated_value,
                ha='left', va='center',
                fontsize=8,
                wrap=True
            )


class CompanyHeader:
    """Render company/project header block"""
    
    def __init__(self, ax):
        """
        Initialize header renderer
        
        Args:
            ax: Matplotlib axis
        """
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_header(
        self,
        company_name: str = "RAVEN CUSTOM GLASS",
        company_logo: str = None
    ):
        """
        Draw company header block
        
        Args:
            company_name: Company name to display
            company_logo: Path to logo image (optional)
        """
        # Header background
        header_box = FancyBboxPatch(
            (0.2, 2), 9.6, 8,
            boxstyle="round,pad=0.15",
            facecolor='#f0f0f0',
            edgecolor='black',
            linewidth=2
        )
        self.ax.add_patch(header_box)
        
        # Company name
        self.ax.text(
            5, 8,
            company_name,
            ha='center', va='center',
            fontsize=14, fontweight='bold',
            family='monospace'
        )
        
        # Subtitle
        self.ax.text(
            5, 6.5,
            "Technical Shop Drawings",
            ha='center', va='center',
            fontsize=10, style='italic',
            color='#666666'
        )
        
        # Contact info placeholder
        self.ax.text(
            5, 5,
            "Professional Window & Door Drawings",
            ha='center', va='center',
            fontsize=8,
            color='#888888'
        )


class DrawingTitle:
    """Render drawing title and type block"""
    
    def __init__(self, ax):
        """
        Initialize title renderer
        
        Args:
            ax: Matplotlib axis
        """
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_title(
        self,
        drawing_type: str,
        item_number: str,
        view: str = "ELEVATION"
    ):
        """
        Draw drawing title block
        
        Args:
            drawing_type: Type of product (Window, Door, etc)
            item_number: Item number/identifier
            view: View type (ELEVATION, SECTION, PLAN)
        """
        # Title box
        title_box = FancyBboxPatch(
            (0.2, 2), 9.6, 8,
            boxstyle="round,pad=0.1",
            facecolor='white',
            edgecolor='black',
            linewidth=1.5
        )
        self.ax.add_patch(title_box)
        
        # Product type
        self.ax.text(
            5, 8,
            drawing_type.upper(),
            ha='center', va='center',
            fontsize=12, fontweight='bold'
        )
        
        # Item number
        self.ax.text(
            5, 6.5,
            f"Item: {item_number}",
            ha='center', va='center',
            fontsize=10, family='monospace'
        )
        
        # View type
        self.ax.text(
            5, 5,
            view,
            ha='center', va='center',
            fontsize=10, style='italic',
            color='#333333'
        )


class ProjectInfoBlock:
    """Render project information table"""
    
    def __init__(self, ax):
        """
        Initialize project info renderer
        
        Args:
            ax: Matplotlib axis
        """
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_project_info(
        self,
        project_name: str,
        po_number: str,
        customer_name: str,
        date: str,
        scale: str = "1/4\" = 1'"
    ):
        """
        Draw project information block
        
        Args:
            project_name: Name of project
            po_number: Purchase order number
            customer_name: Customer name
            date: Drawing date
            scale: Drawing scale
        """
        # Background
        info_box = FancyBboxPatch(
            (0.2, 0.2), 9.6, 9.8,
            boxstyle="round,pad=0.1",
            facecolor='#fafafa',
            edgecolor='black',
            linewidth=1
        )
        self.ax.add_patch(info_box)
        
        # Project info data
        info_data = [
            ("Project", project_name),
            ("PO Number", po_number),
            ("Customer", customer_name),
            ("Date", date),
            ("Scale", scale),
        ]
        
        # Draw each field
        row_height = 1.8
        for i, (label, value) in enumerate(info_data):
            y = 9 - i * row_height
            
            # Label
            self.ax.text(
                0.8, y,
                label + ":",
                ha='left', va='center',
                fontsize=7, fontweight='bold'
            )
            
            # Value
            self.ax.text(
                0.8, y - 0.5,
                value,
                ha='left', va='center',
                fontsize=8,
                family='monospace',
                bbox=dict(boxstyle='round,pad=0.3', 
                         facecolor='white', edgecolor='lightgray')
            )


class RevisionBlock:
    """Render revision and sign-off block"""
    
    def __init__(self, ax):
        """
        Initialize revision block renderer
        
        Args:
            ax: Matplotlib axis
        """
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_revision_block(self, revisions: List[Dict] = None):
        """
        Draw revision and approval block
        
        Args:
            revisions: List of revision dicts with keys: rev, date, description
        """
        # Block background
        block_box = FancyBboxPatch(
            (0.2, 0.2), 9.6, 9.8,
            boxstyle="round,pad=0.05",
            facecolor='white',
            edgecolor='black',
            linewidth=1
        )
        self.ax.add_patch(block_box)
        
        # Title
        self.ax.text(
            5, 9,
            "REVISIONS",
            ha='center', va='top',
            fontsize=8, fontweight='bold'
        )
        
        # Default revision (blank)
        if revisions is None:
            revisions = [
                {"rev": "-", "date": "-", "description": "-"}
            ]
        
        # Draw revision rows
        row_height = 1.5
        for i, rev in enumerate(revisions[:6]):  # Max 6 revisions
            y = 7.5 - i * row_height
            
            # Revision line
            self.ax.text(
                1, y, rev.get('rev', '-'),
                ha='left', va='center', fontsize=7
            )
            self.ax.text(
                3, y, rev.get('date', '-'),
                ha='center', va='center', fontsize=7
            )
            self.ax.text(
                6, y, rev.get('description', '-'),
                ha='left', va='center', fontsize=6
            )
            
            # Row divider
            self.ax.plot(
                [0.3, 9.7], [y - 0.5, y - 0.5],
                color='lightgray', linewidth=0.5
            )


class ConfigurationIcons:
    """Draw window/door operation type icons with highlighting"""
    
    def __init__(self, ax):
        self.ax = ax
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.axis('off')
    
    def draw_icons(self, active_type: str = 'FIXED'):
        """
        Draw 6 operation icons in 2x3 grid, highlight active
        
        Args:
            active_type: Window/door type to highlight (e.g., 'CASEMENT', 'SLIDER')
        """
        active_type = active_type.upper()
        
        # Title
        self.ax.text(5, 9.5, 'OPERATION TYPES', ha='center', va='top',
                    fontsize=9, fontweight='bold')
        
        # Define 6 operation types with symbols and positions
        icons = [
            ('FIXED', '□', 1.5, 7),
            ('CASEMENT', '◄►', 5, 7),
            ('AWNING', '△', 8.5, 7),
            ('SLIDER', '⇄', 1.5, 3.5),
            ('BIFOLD', '⊲⊳', 5, 3.5),
            ('ACCORDION', '⩘⩗', 8.5, 3.5),
        ]
        
        for name, symbol, x, y in icons:
            # Check if this icon should be highlighted
            is_active = name in active_type or active_type in name
            
            # Draw box
            box = patches.Rectangle(
                (x-1, y-0.9), 2, 1.8,
                linewidth=2 if is_active else 1,
                edgecolor='red' if is_active else 'black',
                facecolor='yellow' if is_active else 'white',
                alpha=0.7 if is_active else 0.3
            )
            self.ax.add_patch(box)
            
            # Draw symbol
            self.ax.text(x, y + 0.2, symbol, ha='center', va='center',
                        fontsize=16 if is_active else 14, 
                        fontweight='bold' if is_active else 'normal')
            
            # Draw label
            self.ax.text(x, y - 0.6, name, ha='center', va='center',
                        fontsize=6, fontweight='bold' if is_active else 'normal')
