"""
SQLAlchemy ORM Models
Database models for CAD components and products
"""

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB, BYTEA, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class FrameCrossSection(Base):
    """Frame profile cross-sections"""
    __tablename__ = "frame_cross_sections"
    
    id = Column(Integer, primary_key=True)
    series_name = Column(String(10), nullable=False)
    view_type = Column(String(50), nullable=False)
    configuration = Column(String(50), default='standard')
    image_path = Column(String(500), nullable=False)
    image_filename = Column(String(255))
    dimensions = Column(JSONB)
    anchor_points = Column(JSONB)
    line_weights = Column(JSONB)
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CADComponent(Base):
    """Reusable CAD drawing components"""
    __tablename__ = "cad_components"
    
    id = Column(Integer, primary_key=True)
    component_type = Column(String(50), nullable=False)
    component_name = Column(String(100), nullable=False)
    category = Column(String(50))
    svg_data = Column(BYTEA)
    png_data = Column(BYTEA)
    metadata = Column(JSONB)
    thumbnail = Column(BYTEA)
    tags = Column(ARRAY(Text))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ProductConfig(Base):
    """Product configurations from Google Sheets"""
    __tablename__ = "product_configs"
    
    id = Column(Integer, primary_key=True)
    item_number = Column(String(50), nullable=False)
    product_type = Column(String(50), nullable=False)
    frame_series = Column(String(10), nullable=False)
    width_inches = Column(DECIMAL(6, 2), nullable=False)
    height_inches = Column(DECIMAL(6, 2), nullable=False)
    configuration = Column(JSONB)
    specifications = Column(JSONB)
    project_id = Column(Integer, ForeignKey('projects.id'))
    sheet_row_number = Column(Integer)
    is_door = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="products")
    generated_drawings = relationship("GeneratedDrawing", back_populates="product_config")


class Project(Base):
    """Projects linked to Google Sheets"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    project_name = Column(String(200), nullable=False)
    po_number = Column(String(100))
    client_info = Column(JSONB)
    sheet_url = Column(Text)
    sheet_id = Column(String(100))
    sheet_name = Column(String(100))
    last_synced = Column(DateTime)
    sync_status = Column(String(20), default='pending')
    sync_error = Column(Text)
    item_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    products = relationship("ProductConfig", back_populates="project", cascade="all, delete-orphan")
    generated_drawings = relationship("GeneratedDrawing", back_populates="project")


class DrawingTemplate(Base):
    """Drawing layout templates"""
    __tablename__ = "drawing_templates"
    
    id = Column(Integer, primary_key=True)
    template_name = Column(String(100), nullable=False, unique=True)
    template_type = Column(String(50), nullable=False)
    page_size = Column(String(20), default='A3')
    orientation = Column(String(20), default='landscape')
    layout_config = Column(JSONB, nullable=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    generated_drawings = relationship("GeneratedDrawing", back_populates="template")


class GeneratedDrawing(Base):
    """Generated drawings tracking"""
    __tablename__ = "generated_drawings"
    
    id = Column(Integer, primary_key=True)
    product_config_id = Column(Integer, ForeignKey('product_configs.id', ondelete='CASCADE'))
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'))
    drawing_number = Column(String(50))
    file_path = Column(String(500), nullable=False)
    file_size_kb = Column(Integer)
    template_used = Column(Integer, ForeignKey('drawing_templates.id'))
    generation_params = Column(JSONB)
    preview_image = Column(BYTEA)
    generated_by = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    product_config = relationship("ProductConfig", back_populates="generated_drawings")
    project = relationship("Project", back_populates="generated_drawings")
    template = relationship("DrawingTemplate", back_populates="generated_drawings")


class UserPreference(Base):
    """Desktop application user preferences"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False, unique=True)
    default_series = Column(String(10))
    default_template = Column(Integer, ForeignKey('drawing_templates.id'))
    ui_settings = Column(JSONB)
    export_settings = Column(JSONB)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
