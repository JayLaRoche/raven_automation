#!/usr/bin/env python3
"""
Database Initialization Script
Creates all tables and seeds reference data for accurate drawing generation
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.database import engine, Base
from app.models import Project, Window, Door

print("=" * 70)
print("RAVEN CUSTOM GLASS - DATABASE INITIALIZATION")
print("=" * 70)
print()

# Step 1: Create main application tables
print("[Step 1] Creating application tables (Projects, Windows, Doors)...")
try:
    Base.metadata.create_all(bind=engine)
    print("✓ Application tables created successfully")
except Exception as e:
    print(f"✗ Error creating tables: {e}")
    sys.exit(1)

# Step 2: Verify reference data
print("\n[Step 2] Verifying reference data...")
try:
    with engine.connect() as conn:
        # Check frame series
        result = conn.execute(text("SELECT COUNT(*) FROM frame_series"))
        frame_count = result.scalar()
        print(f"  • Frame Series: {frame_count} records")
        
        # Check configuration types
        result = conn.execute(text("SELECT COUNT(*) FROM configuration_types"))
        config_count = result.scalar()
        print(f"  • Configuration Types: {config_count} records")
        
        # Check glass types
        result = conn.execute(text("SELECT COUNT(*) FROM glass_types"))
        glass_count = result.scalar()
        print(f"  • Glass Types: {glass_count} records")
        
        # Check hardware options
        result = conn.execute(text("SELECT COUNT(*) FROM hardware_options"))
        hardware_count = result.scalar()
        print(f"  • Hardware Options: {hardware_count} records")
        
        # Check frame colors
        result = conn.execute(text("SELECT COUNT(*) FROM frame_colors"))
        color_count = result.scalar()
        print(f"  • Frame Colors: {color_count} records")
        
        conn.commit()
        
        total = frame_count + config_count + glass_count + hardware_count + color_count
        print(f"\n✓ Total reference records: {total}")
        
except Exception as e:
    print(f"✗ Error verifying reference data: {e}")
    print("\nNote: Reference data is loaded from SQL files in database/init/")
    print("Make sure Docker containers are running with mounted init scripts.")

# Step 3: Display connection info
print("\n[Step 3] Database Connection Info")
print(f"  • Database URL: {os.getenv('DATABASE_URL', 'Not configured')}")
print(f"  • pgAdmin URL: http://localhost:5050")
print(f"  • Database: {os.getenv('DB_NAME', 'raven_drawings')}")
print(f"  • User: {os.getenv('DB_USER', 'raven_user')}")

print("\n" + "=" * 70)
print("DATABASE INITIALIZATION COMPLETE")
print("=" * 70)
print()
print("Next steps:")
print("  1. Access pgAdmin at http://localhost:5050")
print("     Email: admin@ravencustomglass.com")
print("     Password: admin2025")
print()
print("  2. Start generating drawings:")
print("     python generate_from_sheet.py 'Sheet Name'")
print()
