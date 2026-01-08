"""
Parameter Selection Panel
Left panel for window/door parameter configuration
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                              QSpinBox, QDoubleSpinBox, QLabel, QPushButton, 
                              QGroupBox, QFormLayout, QCheckBox, QLineEdit,
                              QScrollArea)
from PyQt6.QtCore import pyqtSignal, Qt
import logging

from src.database import DatabaseManager, FrameLibrary, DatabaseQueries

logger = logging.getLogger(__name__)


class ParameterPanel(QWidget):
    """
    Parameter selection panel with real-time updates
    Emits parameters_changed signal when any control changes
    """
    
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db_manager = db_manager
        self.frame_library = FrameLibrary(db_manager)
        self.queries = DatabaseQueries(db_manager)
        
        self.setup_ui()
        self.load_database_options()
        
        logger.info("Parameter panel initialized")
    
    def setup_ui(self):
        """Setup user interface"""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # === Frame Series Selection ===
        frame_group = QGroupBox("Frame Series")
        frame_layout = QFormLayout()
        
        self.series_combo = QComboBox()
        self.series_combo.currentTextChanged.connect(self.emit_parameters)
        frame_layout.addRow("Series:", self.series_combo)
        
        frame_group.setLayout(frame_layout)
        layout.addWidget(frame_group)
        
        # === Product Type ===
        product_group = QGroupBox("Product Type")
        product_layout = QFormLayout()
        
        self.product_combo = QComboBox()
        self.product_combo.currentTextChanged.connect(self.emit_parameters)
        product_layout.addRow("Type:", self.product_combo)
        
        # Configuration (X/O notation for operable units)
        self.config_edit = QLineEdit()
        self.config_edit.setPlaceholderText("e.g., XO, XX, OXO")
        self.config_edit.textChanged.connect(self.emit_parameters)
        product_layout.addRow("Config:", self.config_edit)
        
        product_group.setLayout(product_layout)
        layout.addWidget(product_group)
        
        # === Dimensions ===
        dim_group = QGroupBox("Dimensions")
        dim_layout = QFormLayout()
        
        # Width
        width_container = QHBoxLayout()
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(12.0, 300.0)
        self.width_spin.setSingleStep(0.5)
        self.width_spin.setValue(48.0)
        self.width_spin.setSuffix(' in')
        self.width_spin.setDecimals(2)
        self.width_spin.valueChanged.connect(self.emit_parameters)
        width_container.addWidget(self.width_spin)
        dim_layout.addRow("Width:", self.width_spin)
        
        # Height
        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(12.0, 300.0)
        self.height_spin.setSingleStep(0.5)
        self.height_spin.setValue(60.0)
        self.height_spin.setSuffix(' in')
        self.height_spin.setDecimals(2)
        self.height_spin.valueChanged.connect(self.emit_parameters)
        dim_layout.addRow("Height:", self.height_spin)
        
        dim_group.setLayout(dim_layout)
        layout.addWidget(dim_group)
        
        # === Specifications ===
        spec_group = QGroupBox("Specifications")
        spec_layout = QFormLayout()
        
        # Glass type
        self.glass_combo = QComboBox()
        self.glass_combo.addItems([
            'Single Pane Clear',
            'Dual Pane Clear',
            'Low-E',
            'Low-E + Argon',
            'Tempered',
            'Laminated'
        ])
        self.glass_combo.currentTextChanged.connect(self.emit_parameters)
        spec_layout.addRow("Glass:", self.glass_combo)
        
        # Frame color
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            'White',
            'Bronze',
            'Black',
            'Mill Finish',
            'Custom'
        ])
        self.color_combo.currentTextChanged.connect(self.emit_parameters)
        spec_layout.addRow("Color:", self.color_combo)
        
        # Grids
        self.grids_check = QCheckBox()
        self.grids_check.stateChanged.connect(self.emit_parameters)
        spec_layout.addRow("Grids:", self.grids_check)
        
        spec_group.setLayout(spec_layout)
        layout.addWidget(spec_group)
        
        # === Project Information ===
        project_group = QGroupBox("Project Info")
        project_layout = QFormLayout()
        
        self.item_number_edit = QLineEdit()
        self.item_number_edit.setPlaceholderText("W-001")
        self.item_number_edit.textChanged.connect(self.emit_parameters)
        project_layout.addRow("Item #:", self.item_number_edit)
        
        self.po_number_edit = QLineEdit()
        self.po_number_edit.setPlaceholderText("PO-2024-001")
        self.po_number_edit.textChanged.connect(self.emit_parameters)
        project_layout.addRow("PO #:", self.po_number_edit)
        
        project_group.setLayout(project_layout)
        layout.addWidget(project_group)
        
        # === Action Buttons ===
        button_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_parameters)
        button_layout.addWidget(self.reset_btn)
        
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.emit_parameters)
        self.generate_btn.setDefault(True)
        button_layout.addWidget(self.generate_btn)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push controls to top
        layout.addStretch()
        
        # Set content to scroll area
        scroll.setWidget(content)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def load_database_options(self):
        """Load options from PostgreSQL database"""
        try:
            # Load frame series
            series_list = self.frame_library.get_available_series()
            if series_list:
                self.series_combo.addItems(series_list)
                logger.info(f"Loaded {len(series_list)} frame series")
            else:
                # Fallback to common series
                self.series_combo.addItems(['65', '80', '86', '135', '68', 'MD100H'])
                logger.warning("No series found in database, using fallback list")
            
            # Load product types
            product_types = self.queries.get_product_types()
            if product_types:
                self.product_combo.addItems(product_types)
            else:
                # Fallback to common types
                self.product_combo.addItems([
                    'FIXED',
                    'CASEMENT',
                    'DOUBLE CASEMENT',
                    'AWNING',
                    'SLIDER 2-PANEL',
                    'SLIDER 3-PANEL',
                    'SLIDER 4-PANEL',
                    'HINGED DOOR',
                    'BIFOLD DOOR'
                ])
            
        except Exception as e:
            logger.error(f"Failed to load database options: {e}")
            # Use fallback values
            self.series_combo.addItems(['65', '80', '86', '135'])
            self.product_combo.addItems(['FIXED', 'CASEMENT', 'SLIDER', 'DOOR'])
    
    def emit_parameters(self):
        """Emit current parameters as dictionary"""
        params = {
            'series': self.series_combo.currentText(),
            'product_type': self.product_combo.currentText(),
            'configuration': self.config_edit.text(),
            'width': self.width_spin.value(),
            'height': self.height_spin.value(),
            'glass_type': self.glass_combo.currentText(),
            'frame_color': self.color_combo.currentText(),
            'has_grids': self.grids_check.isChecked(),
            'item_number': self.item_number_edit.text(),
            'po_number': self.po_number_edit.text()
        }
        
        self.parameters_changed.emit(params)
        logger.debug(f"Parameters emitted: {params}")
    
    def reset_parameters(self):
        """Reset all parameters to defaults"""
        self.series_combo.setCurrentIndex(0)
        self.product_combo.setCurrentIndex(0)
        self.config_edit.clear()
        self.width_spin.setValue(48.0)
        self.height_spin.setValue(60.0)
        self.glass_combo.setCurrentIndex(0)
        self.color_combo.setCurrentIndex(0)
        self.grids_check.setChecked(False)
        self.item_number_edit.clear()
        self.po_number_edit.clear()
        
        self.emit_parameters()
        logger.info("Parameters reset to defaults")
    
    def load_parameters(self, params: dict):
        """Load parameters from dictionary"""
        if 'series' in params:
            index = self.series_combo.findText(params['series'])
            if index >= 0:
                self.series_combo.setCurrentIndex(index)
        
        if 'product_type' in params:
            index = self.product_combo.findText(params['product_type'])
            if index >= 0:
                self.product_combo.setCurrentIndex(index)
        
        if 'configuration' in params:
            self.config_edit.setText(params['configuration'])
        
        if 'width' in params:
            self.width_spin.setValue(float(params['width']))
        
        if 'height' in params:
            self.height_spin.setValue(float(params['height']))
        
        if 'glass_type' in params:
            index = self.glass_combo.findText(params['glass_type'])
            if index >= 0:
                self.glass_combo.setCurrentIndex(index)
        
        if 'frame_color' in params:
            index = self.color_combo.findText(params['frame_color'])
            if index >= 0:
                self.color_combo.setCurrentIndex(index)
        
        if 'has_grids' in params:
            self.grids_check.setChecked(bool(params['has_grids']))
        
        if 'item_number' in params:
            self.item_number_edit.setText(params['item_number'])
        
        if 'po_number' in params:
            self.po_number_edit.setText(params['po_number'])
        
        self.emit_parameters()
