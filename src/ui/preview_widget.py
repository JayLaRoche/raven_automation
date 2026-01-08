"""
Drawing Preview Widget
Matplotlib canvas for displaying generated CAD drawings
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import logging

logger = logging.getLogger(__name__)


class PreviewWidget(QWidget):
    """
    Widget for displaying drawing previews
    Embeds matplotlib figure with zoom controls
    """
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        logger.info("Preview widget initialized")
    
    def setup_ui(self):
        """Setup matplotlib canvas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 10), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Add toolbar for zoom controls
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Add to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Initialize with blank canvas
        self.clear()
    
    def update_drawing(self, figure: Figure):
        """
        Update canvas with new matplotlib figure
        
        Args:
            figure: Matplotlib Figure object
        """
        try:
            # Replace figure
            self.figure = figure
            
            # Update canvas
            self.canvas.figure = self.figure
            self.canvas.draw()
            
            logger.info("Drawing preview updated")
            
        except Exception as e:
            logger.error(f"Failed to update drawing: {e}")
            self.show_error(str(e))
    
    def clear(self):
        """Clear the canvas"""
        self.figure.clear()
        
        # Add centered text
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'No drawing loaded\n\nConfigure parameters and click Generate',
                ha='center', va='center', fontsize=14, color='gray',
                transform=ax.transAxes)
        ax.axis('off')
        
        self.canvas.draw()
        logger.debug("Canvas cleared")
    
    def show_error(self, message: str):
        """Display error message on canvas"""
        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, f'Error generating drawing:\n\n{message}',
                ha='center', va='center', fontsize=12, color='red',
                transform=ax.transAxes, wrap=True)
        ax.axis('off')
        
        self.canvas.draw()
        logger.warning(f"Error displayed on canvas: {message}")
    
    def zoom_in(self):
        """Zoom in to drawing"""
        self.toolbar.zoom()
    
    def zoom_out(self):
        """Zoom out from drawing"""
        self.toolbar.back()
    
    def fit_to_window(self):
        """Reset zoom to fit entire drawing"""
        self.toolbar.home()
    
    def sizeHint(self):
        """Recommended size for widget"""
        return QSize(800, 1000)
