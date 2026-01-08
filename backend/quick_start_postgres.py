#!/usr/bin/env python3
"""
Quick Start - PostgreSQL Drawing System
Complete workflow for generating drawings with reference data
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from sqlalchemy import text
from services.drawing_engine import ProfessionalDrawingGenerator
from datetime import datetime

print("=" * 70)
print("RAVEN CUSTOM GLASS - POSTGRESQL DRAWING SYSTEM")
print("=" * 70)
print()

# Show available reference data
print("📊 AVAILABLE REFERENCE DATA:")
print("-" * 70)

db = SessionLocal()

# Frame Series
print("\n[Frame Series]")
frames = db.execute(text("""
    SELECT series_name, series_code, frame_width_mm 
    FROM frame_series 
    ORDER BY series_code
""")).fetchall()
for frame in frames:
    print(f"  • {frame[0]:15} ({frame[1]:3}) - {frame[2]:6.2f}mm")

# Configuration Types
print("\n[Window/Door Configurations]")
configs = db.execute(text("""
    SELECT config_name, config_code, panel_count 
    FROM configuration_types 
    ORDER BY panel_count, config_name
""")).fetchall()
for config in configs:
    print(f"  • {config[0]:25} ({config[1]:4}) - {config[2]} panels")

# Glass Types
print("\n[Glass Options]")
glasses = db.execute(text("""
    SELECT glass_name, glass_code, u_factor 
    FROM glass_types 
    ORDER BY u_factor DESC
""")).fetchall()
for glass in glasses:
    print(f"  • {glass[0]:25} ({glass[1]:3}) - U={glass[2]:.3f}")

# Hardware
print("\n[Hardware Options]")
hardware = db.execute(text("""
    SELECT hardware_name, hardware_type 
    FROM hardware_options 
    ORDER BY hardware_type, hardware_name 
    LIMIT 8
""")).fetchall()
for hw in hardware:
    print(f"  • {hw[0]:30} [{hw[1]}]")

# Colors
print("\n[Frame Colors]")
colors = db.execute(text("""
    SELECT color_name, color_code, finish_type 
    FROM frame_colors 
    ORDER BY color_name
""")).fetchall()
for color in colors:
    print(f"  • {color[0]:15} ({color[1]:3}) - {color[2]}")

db.close()

# Generate sample drawing
print("\n" + "=" * 70)
print("📐 GENERATING SAMPLE DRAWING")
print("=" * 70)
print()

window_data = {
    'item_number': 'W-DEMO-001',
    'mark': 'Demo Window',
    'quantity': 1,
    'width': 60,
    'height': 48,
    'configuration': 'Slider 4-Panel',
    'operation_type': 'Slider',
    'frame_series': 'Series 90',
    'frame_color': 'White',
    'glass_type': 'Low-E Dual Pane',
    'screen': 'Full Screen',
    'hardware': 'Slider Window Lock',
    'notes': 'PostgreSQL reference data demo'
}

project_data = {
    'project_name': 'PostgreSQL Demo Project',
    'project_number': 'PG-DEMO-2025',
    'client': 'Raven Custom Glass',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'revision': 'A'
}

print("Window Specifications:")
print(f"  • Configuration: {window_data['configuration']}")
print(f"  • Dimensions: {window_data['width']}\" × {window_data['height']}\"")
print(f"  • Frame Series: {window_data['frame_series']}")
print(f"  • Glass: {window_data['glass_type']}")
print(f"  • Hardware: {window_data['hardware']}")
print(f"  • Color: {window_data['frame_color']}")
print()

print("Generating professional shop drawing...")
generator = ProfessionalDrawingGenerator()
output_path = generator.generate_window_drawing(
    window_data,
    project_data,
    output_filename='POSTGRES_DEMO.pdf'
)

print(f"\n✓ Drawing generated: {output_path}")
print()

# Auto-open
if os.path.exists(output_path):
    os.startfile(output_path)
    print(f"Opening {output_path}...")

print("\n" + "=" * 70)
print("QUICK START TIPS")
print("=" * 70)
print()
print("1. Access pgAdmin:")
print("   http://localhost:5050")
print("   Email: admin@ravencustomglass.com")
print("   Password: admin2025")
print()
print("2. View reference data:")
print("   SELECT * FROM frame_series;")
print("   SELECT * FROM configuration_types;")
print("   SELECT * FROM glass_types;")
print()
print("3. Generate drawings from Google Sheets:")
print("   python generate_from_sheet.py 'Sheet Name'")
print()
print("4. Check Docker containers:")
print("   docker ps")
print("   docker-compose logs -f postgres")
print()
