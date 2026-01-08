#!/usr/bin/env python
"""
Initialize database with sample frame data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from sqlalchemy import text

def init_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    db = SessionLocal()
    
    try:
        # Create frame_cross_sections table if it doesn't exist
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS frame_cross_sections (
                id SERIAL PRIMARY KEY,
                series VARCHAR(20) NOT NULL,
                size VARCHAR(50),
                view_type VARCHAR(50),
                image_path VARCHAR(255),
                width_min DECIMAL(10, 2),
                width_max DECIMAL(10, 2),
                height_min DECIMAL(10, 2),
                height_max DECIMAL(10, 2)
            )
        """))
        
        # Check if data already exists
        existing = db.execute(text("SELECT COUNT(*) FROM frame_cross_sections")).scalar()
        
        if existing == 0:
            # Add sample frame series
            sample_frames = [
                ("135", "Standard", "head", "", 12, 300, 12, 300),
                ("150", "Standard", "head", "", 12, 300, 12, 300),
                ("58", "Standard", "head", "", 12, 300, 12, 300),
                ("65", "Standard", "head", "", 12, 300, 12, 300),
                ("68", "Standard", "head", "", 12, 300, 12, 300),
                ("86", "Standard", "head", "", 12, 300, 12, 300),
                ("4518", "Standard", "head", "", 12, 300, 12, 300),
                ("Other", "Standard", "head", "", 12, 300, 12, 300),
            ]
            
            for series, size, view_type, image_path, w_min, w_max, h_min, h_max in sample_frames:
                db.execute(text("""
                    INSERT INTO frame_cross_sections (series, size, view_type, image_path, width_min, width_max, height_min, height_max)
                    VALUES (:series, :size, :view_type, :image_path, :w_min, :w_max, :h_min, :h_max)
                """), {
                    "series": series,
                    "size": size,
                    "view_type": view_type,
                    "image_path": image_path,
                    "w_min": w_min,
                    "w_max": w_max,
                    "h_min": h_min,
                    "h_max": h_max
                })
            
            db.commit()
            print("✅ Sample frame data added to database")
        else:
            print(f"✅ Frame data already exists ({existing} records)")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
