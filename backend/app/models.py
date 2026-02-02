from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Text, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Legacy fields (kept for backward compatibility)
    project_name = Column(String(255), nullable=True)  # Made nullable
    po_number = Column(String(100))
    customer_name = Column(String(255))
    billing_address = Column(Text)
    shipping_address = Column(Text)
    
    # New flexible fields (can be used instead of or alongside legacy fields)
    client_name = Column(String(255))  # Alternative to customer_name
    address = Column(Text)  # General address field
    date = Column(DateTime)  # Project date
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    windows = relationship("Window", back_populates="project", cascade="all, delete-orphan")
    doors = relationship("Door", back_populates="project", cascade="all, delete-orphan")
    units = relationship("Unit", back_populates="project", cascade="all, delete-orphan")
    drawings = relationship("Drawing", back_populates="project", cascade="all, delete-orphan")

class Window(Base):
    __tablename__ = "windows"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    item_number = Column(String(50), nullable=False)
    room = Column(String(100))
    width_inches = Column(DECIMAL(10, 2))
    height_inches = Column(DECIMAL(10, 2))
    window_type = Column(String(50))
    frame_series = Column(String(20))
    swing_direction = Column(String(20))
    quantity = Column(Integer, default=1)
    frame_color = Column(String(50))
    glass_type = Column(String(100))
    grids = Column(String(50))
    screen = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    project = relationship("Project", back_populates="windows")

class Door(Base):
    __tablename__ = "doors"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    item_number = Column(String(50), nullable=False)
    room = Column(String(100))
    width_inches = Column(DECIMAL(10, 2))
    height_inches = Column(DECIMAL(10, 2))
    door_type = Column(String(50))
    frame_series = Column(String(20))
    swing_direction = Column(String(50))
    quantity = Column(Integer, default=1)
    frame_color = Column(String(50))
    glass_type = Column(String(100))
    threshold = Column(String(50))
    sill_pan_depth = Column(DECIMAL(10, 2))
    sill_pan_length = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    project = relationship("Project", back_populates="doors")

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Unit specifications
    series = Column(String(50))
    product_type = Column(String(100))
    width = Column(DECIMAL(10, 2))
    height = Column(DECIMAL(10, 2))
    glass_type = Column(String(100))
    frame_color = Column(String(100))
    configuration = Column(String(100))
    
    # Additional details
    item_number = Column(String(100))
    has_grids = Column(Integer, default=0)  # SQLite uses 0/1 for boolean
    panel_count = Column(Integer, default=1)
    swing_orientation = Column(String(50))
    handle_side = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    project = relationship("Project", back_populates="units")
    drawings = relationship("Drawing", back_populates="unit", cascade="all, delete-orphan")

class Drawing(Base):
    __tablename__ = "drawings"
    
    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Drawing metadata
    pdf_filename = Column(String(255))
    pdf_blob = Column(LargeBinary)  # Store PDF binary data
    thumbnail_blob = Column(LargeBinary, nullable=True)  # Optional preview
    
    # Drawing specifications (snapshot of parameters at generation time)
    series = Column(String(50))
    product_type = Column(String(100))
    width = Column(DECIMAL(10, 2))
    height = Column(DECIMAL(10, 2))
    glass_type = Column(String(100))
    frame_color = Column(String(100))
    configuration = Column(String(100))
    
    # Version tracking
    version = Column(Integer, default=1)
    is_current = Column(Integer, default=1)  # SQLite boolean (0/1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    unit = relationship("Unit", back_populates="drawings")
    project = relationship("Project", back_populates="drawings")
