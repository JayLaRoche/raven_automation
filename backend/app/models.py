from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(255), nullable=False)
    po_number = Column(String(100))
    customer_name = Column(String(255))
    billing_address = Column(Text)
    shipping_address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    windows = relationship("Window", back_populates="project", cascade="all, delete-orphan")
    doors = relationship("Door", back_populates="project", cascade="all, delete-orphan")

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
