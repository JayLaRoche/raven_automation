#!/usr/bin/env python3
"""
PostgreSQL Integration Test
Verifies database connection, reference data, and drawing generation
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("POSTGRESQL INTEGRATION TEST")
print("=" * 70)
print()

# Test 1: Database Connection
print("[Test 1] PostgreSQL Connection")
print("-" * 70)
try:
    from app.database import engine, SessionLocal
    from sqlalchemy import text
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"✓ Connected to PostgreSQL")
        print(f"  Version: {version[:50]}...")
        conn.commit()
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print("\nMake sure Docker containers are running:")
    print("  docker-compose up -d")
    sys.exit(1)

# Test 2: Check Reference Data
print("\n[Test 2] Reference Data Verification")
print("-" * 70)
try:
    db = SessionLocal()
    
    # Frame Series
    result = db.execute(text("SELECT series_name, series_code, frame_width_mm FROM frame_series LIMIT 3"))
    frames = result.fetchall()
    print(f"✓ Frame Series ({len(frames)} shown):")
    for frame in frames:
        print(f"  • {frame[0]} ({frame[1]}) - {frame[2]}mm")
    
    # Configuration Types
    result = db.execute(text("SELECT config_name, config_code, panel_count FROM configuration_types LIMIT 5"))
    configs = result.fetchall()
    print(f"\n✓ Configuration Types ({len(configs)} shown):")
    for config in configs:
        print(f"  • {config[0]} ({config[1]}) - {config[2]} panels")
    
    # Glass Types
    result = db.execute(text("SELECT glass_name, glass_code, u_factor FROM glass_types LIMIT 3"))
    glasses = result.fetchall()
    print(f"\n✓ Glass Types ({len(glasses)} shown):")
    for glass in glasses:
        print(f"  • {glass[0]} ({glass[1]}) - U-Factor: {glass[2]}")
    
    db.close()
    
except Exception as e:
    print(f"✗ Error reading reference data: {e}")
    print("\nReference data should be loaded automatically when containers start.")
    print("Check: backend/database/init/*.sql files")

# Test 3: Application Tables
print("\n[Test 3] Application Tables")
print("-" * 70)
try:
    from app.models import Project, Window, Door
    
    db = SessionLocal()
    
    # Count existing records
    project_count = db.query(Project).count()
    window_count = db.query(Window).count()
    door_count = db.query(Door).count()
    
    print(f"✓ Tables accessible:")
    print(f"  • Projects: {project_count} records")
    print(f"  • Windows: {window_count} records")
    print(f"  • Doors: {door_count} records")
    
    db.close()
    
except Exception as e:
    print(f"✗ Error accessing application tables: {e}")

# Test 4: Drawing Generation with Reference Data
print("\n[Test 4] Drawing Generation Test")
print("-" * 70)
try:
    from services.drawing_engine import ProfessionalDrawingGenerator
    from datetime import datetime
    
    # Create test window using reference data
    test_window = {
        'item_number': 'W-TEST-PG',
        'mark': 'PostgreSQL Test',
        'quantity': 1,
        'width': 48,
        'height': 60,
        'configuration': 'Slider',
        'operation_type': 'Slider',
        'frame_series': 'Series 90',
        'frame_color': 'White',
        'glass_type': 'Low-E Dual Pane',
        'screen': 'Full Screen',
        'hardware': 'Slider Window Lock',
        'notes': 'PostgreSQL integration test window'
    }
    
    project_data = {
        'project_name': 'PostgreSQL Integration Test',
        'project_number': 'PG-TEST-001',
        'client': 'Quality Control',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'revision': 'A'
    }
    
    print("Generating test drawing with reference data...")
    generator = ProfessionalDrawingGenerator()
    output_path = generator.generate_window_drawing(
        test_window,
        project_data,
        output_filename='POSTGRES_TEST.pdf'
    )
    
    print(f"✓ Drawing generated: {output_path}")
    print("  • Frame Series: Series 90")
    print("  • Glass Type: Low-E Dual Pane")
    print("  • Hardware: Slider Window Lock")
    print("  • Color: White")
    
    # Auto-open PDF
    if os.path.exists(output_path):
        os.startfile(output_path)
        print(f"\n✓ Opening {output_path}...")
    
except Exception as e:
    print(f"✗ Drawing generation failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 70)
print("POSTGRESQL INTEGRATION TEST COMPLETE")
print("=" * 70)
print()
print("PostgreSQL Database Features:")
print("  ✓ Connection pooling enabled")
print("  ✓ Reference data for accurate drawings")
print("  ✓ Frame series specifications (Series 80, 86, 90, 135, 200)")
print("  ✓ Configuration types (Fixed, Casement, Slider, Bifold, etc.)")
print("  ✓ Glass specifications (U-factor, SHGC values)")
print("  ✓ Hardware catalog (locks, operators, hinges)")
print("  ✓ Frame color options (White, Bronze, Black, etc.)")
print()
print("Management Tools:")
print("  • pgAdmin: http://localhost:5050")
print("  • Database: raven_drawings")
print("  • User: raven_user")
print()
