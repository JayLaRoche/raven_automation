"""
Main Application Window
PyQt6 main window with parameter panel and drawing preview
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                              QToolBar, QStatusBar, QMenuBar, QMenu, QMessageBox,
                              QFileDialog, QDockWidget)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QAction, QKeySequence
from pathlib import Path
import logging

from .parameter_panel import ParameterPanel
from .preview_widget import PreviewWidget
from src.database import DatabaseManager, FrameLibrary, DatabaseQueries
from src.drawing import DrawingGenerator

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window for Raven Shop Drawing Generator
    
    Layout:
    - Left: Parameter selection panel (dockable)
    - Center: Drawing preview canvas
    - Top: Menu and toolbar
    - Bottom: Status bar
    """
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.frame_library = FrameLibrary(db_manager)
        self.queries = DatabaseQueries(db_manager)
        self.drawing_generator = DrawingGenerator(db_manager)
        
        # Application settings
        self.settings = QSettings('RavenCustomGlass', 'ShopDrawing')
        
        # Current drawing state
        self.current_parameters = {}
        self.current_drawing = None
        
        self.init_ui()
        self.restore_window_state()
        
        logger.info("Main window initialized")
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Raven Shop Drawing Generator - Desktop")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Create menus
        self.create_menus()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget with preview
        self.preview = PreviewWidget()
        self.setCentralWidget(self.preview)
        
        # Create dockable parameter panel
        self.param_dock = QDockWidget("Parameters", self)
        self.param_panel = ParameterPanel(self.db_manager)
        self.param_panel.parameters_changed.connect(self.on_parameters_changed)
        self.param_dock.setWidget(self.param_panel)
        self.param_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                        Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.param_dock)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_menus(self):
        """Create application menus"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Drawing", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_drawing)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Project...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Drawing...", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self.export_drawing)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        prefs_action = QAction("&Preferences...", self)
        prefs_action.triggered.connect(self.show_preferences)
        edit_menu.addAction(prefs_action)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        
        toggle_params_action = self.param_dock.toggleViewAction()
        toggle_params_action.setText("&Parameter Panel")
        view_menu.addAction(toggle_params_action)
        
        view_menu.addSeparator()
        
        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.preview.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.preview.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        zoom_fit_action = QAction("Zoom to &Fit", self)
        zoom_fit_action.setShortcut(QKeySequence("Ctrl+0"))
        zoom_fit_action.triggered.connect(self.preview.zoom_fit)
        view_menu.addAction(zoom_fit_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        sync_sheets_action = QAction("&Sync Google Sheets...", self)
        sync_sheets_action.triggered.connect(self.sync_google_sheets)
        tools_menu.addAction(sync_sheets_action)
        
        frame_library_action = QAction("&Frame Library Manager...", self)
        frame_library_action.triggered.connect(self.show_frame_library)
        tools_menu.addAction(frame_library_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add common actions
        generate_action = QAction("Generate Drawing", self)
        generate_action.triggered.connect(self.generate_drawing)
        toolbar.addAction(generate_action)
        
        toolbar.addSeparator()
        
        export_action = QAction("Export PDF", self)
        export_action.triggered.connect(self.export_drawing)
        toolbar.addAction(export_action)
    
    def on_parameters_changed(self, parameters: dict):
        """Handle parameter changes from panel"""
        self.current_parameters = parameters
        self.statusBar().showMessage(
            f"Parameters updated: {parameters.get('product_type', 'Unknown')} "
            f"{parameters.get('width', 0)}\" × {parameters.get('height', 0)}\""
        )
        
        # Auto-regenerate drawing if enabled
        if self.settings.value('auto_regenerate', True, type=bool):
            self.generate_drawing()
    
    def generate_drawing(self):
        """Generate drawing from current parameters"""
        if not self.current_parameters:
            self.statusBar().showMessage("No parameters set")
            return
        
        try:
            self.statusBar().showMessage("Generating drawing...")
            
            # Import here to avoid circular dependency
            from src.drawing.generator import DrawingGenerator
            
            # Generate drawing using the drawing generator
            figure = self.drawing_generator.generate(self.current_parameters)
            
            self.current_drawing = figure
            self.preview.update_drawing(figure)
            
            self.statusBar().showMessage("Drawing generated successfully")
            
        except Exception as e:
            logger.error(f"Failed to generate drawing: {e}")
            QMessageBox.critical(self, "Generation Error", 
                               f"Failed to generate drawing:\n\n{str(e)}")
            self.statusBar().showMessage("Generation failed")
    
    def export_drawing(self):
        """Export current drawing to PDF"""
        if not self.current_drawing:
            QMessageBox.warning(self, "No Drawing", 
                              "Please generate a drawing first.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Drawing",
            str(Path.home() / "Documents" / "drawing.pdf"),
            "PDF Files (*.pdf);;All Files (*)"
        )
        
        if filename:
            try:
                self.statusBar().showMessage("Exporting drawing...")
                
                # Export matplotlib figure to PDF
                self.current_drawing.savefig(filename, format='pdf', dpi=300, 
                                             bbox_inches='tight')
                
                self.statusBar().showMessage(f"Exported to {filename}")
                QMessageBox.information(self, "Export Complete", 
                                      f"Drawing exported to:\n{filename}")
                
            except Exception as e:
                logger.error(f"Export failed: {e}")
                QMessageBox.critical(self, "Export Error", 
                                   f"Failed to export drawing:\n\n{str(e)}")
    
    def new_drawing(self):
        """Create new drawing"""
        self.param_panel.reset_parameters()
        self.preview.clear()
        self.current_parameters = {}
        self.current_drawing = None
        self.statusBar().showMessage("New drawing created")
    
    def open_project(self):
        """Open project dialog"""
        # TODO: Implement project selection dialog
        QMessageBox.information(self, "Open Project", 
                              "Project selection dialog not yet implemented.")
    
    def sync_google_sheets(self):
        """Sync data from Google Sheets"""
        # TODO: Implement Google Sheets sync dialog
        QMessageBox.information(self, "Sync Google Sheets", 
                              "Google Sheets sync not yet implemented.")
    
    def show_frame_library(self):
        """Show frame library manager"""
        # TODO: Implement frame library manager dialog
        QMessageBox.information(self, "Frame Library", 
                              "Frame library manager not yet implemented.")
    
    def show_preferences(self):
        """Show preferences dialog"""
        # TODO: Implement preferences dialog
        QMessageBox.information(self, "Preferences", 
                              "Preferences dialog not yet implemented.")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Raven Shop Drawing",
            "<h2>Raven Shop Drawing Generator</h2>"
            "<p>Professional CAD shop drawing generator for windows and doors</p>"
            "<p>Version 1.0.0</p>"
            "<p>© 2025 Raven Custom Glass</p>"
        )
    
    def restore_window_state(self):
        """Restore window geometry and state from settings"""
        geometry = self.settings.value('window/geometry')
        if geometry:
            self.restoreGeometry(geometry)
        
        state = self.settings.value('window/state')
        if state:
            self.restoreState(state)
    
    def save_window_state(self):
        """Save window geometry and state to settings"""
        self.settings.setValue('window/geometry', self.saveGeometry())
        self.settings.setValue('window/state', self.saveState())
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.save_window_state()
        
        # Clean up database connections
        try:
            self.db_manager.close_all_connections()
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")
        
        event.accept()
