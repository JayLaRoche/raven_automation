#!/usr/bin/env python3
"""
Database Backup Script
Creates backups of PostgreSQL database and exports reference data to JSON
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import json
import subprocess

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from sqlalchemy import text

print("=" * 70)
print("DATABASE BACKUP SYSTEM")
print("=" * 70)
print()

# Create backup directory
backup_dir = Path('backups')
backup_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Step 1: PostgreSQL Dump
print("[Step 1] PostgreSQL Database Dump")
print("-" * 70)

db_name = os.getenv('DB_NAME', 'raven_drawings')
db_user = os.getenv('DB_USER', 'raven_user')
container_name = 'raven_postgres'

sql_backup_file = backup_dir / f'postgres_backup_{timestamp}.sql'

try:
    # Use docker exec to run pg_dump
    cmd = f'docker exec {container_name} pg_dump -U {db_user} {db_name}'
    
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        sql_backup_file.write_text(result.stdout)
        size_mb = sql_backup_file.stat().st_size / (1024 * 1024)
        print(f"✓ SQL backup created: {sql_backup_file}")
        print(f"  Size: {size_mb:.2f} MB")
    else:
        print(f"✗ Backup failed: {result.stderr}")
except Exception as e:
    print(f"✗ Error creating SQL backup: {e}")

# Step 2: Export Reference Data to JSON
print("\n[Step 2] Exporting Reference Data to JSON")
print("-" * 70)

db = SessionLocal()

try:
    reference_data = {}
    
    # Frame Series
    result = db.execute(text("""
        SELECT series_name, series_code, frame_width_mm, sash_width_mm, 
               nail_fin_width_mm, nail_fin_height_mm, thermal_break, 
               glass_pocket_depth_mm, description
        FROM frame_series
        ORDER BY series_code
    """))
    reference_data['frame_series'] = [
        {
            'series_name': row[0],
            'series_code': row[1],
            'frame_width_mm': float(row[2]) if row[2] else None,
            'sash_width_mm': float(row[3]) if row[3] else None,
            'nail_fin_width_mm': float(row[4]) if row[4] else None,
            'nail_fin_height_mm': float(row[5]) if row[5] else None,
            'thermal_break': row[6],
            'glass_pocket_depth_mm': float(row[7]) if row[7] else None,
            'description': row[8]
        }
        for row in result
    ]
    
    # Configuration Types
    result = db.execute(text("""
        SELECT config_name, config_code, panel_count, operable_panels,
               panel_indicator_style, requires_mullions, requires_hardware, description
        FROM configuration_types
        ORDER BY config_name
    """))
    reference_data['configuration_types'] = [
        {
            'config_name': row[0],
            'config_code': row[1],
            'panel_count': row[2],
            'operable_panels': row[3],
            'panel_indicator_style': row[4],
            'requires_mullions': row[5],
            'requires_hardware': row[6],
            'description': row[7]
        }
        for row in result
    ]
    
    # Glass Types
    result = db.execute(text("""
        SELECT glass_name, glass_code, thickness_mm, u_factor, shgc, description
        FROM glass_types
        ORDER BY glass_name
    """))
    reference_data['glass_types'] = [
        {
            'glass_name': row[0],
            'glass_code': row[1],
            'thickness_mm': float(row[2]) if row[2] else None,
            'u_factor': float(row[3]) if row[3] else None,
            'shgc': float(row[4]) if row[4] else None,
            'description': row[5]
        }
        for row in result
    ]
    
    # Hardware Options
    result = db.execute(text("""
        SELECT hardware_name, hardware_type, manufacturer, model_number,
               finish, applicable_configs, description
        FROM hardware_options
        ORDER BY hardware_type, hardware_name
    """))
    reference_data['hardware_options'] = [
        {
            'hardware_name': row[0],
            'hardware_type': row[1],
            'manufacturer': row[2],
            'model_number': row[3],
            'finish': row[4],
            'applicable_configs': row[5],
            'description': row[6]
        }
        for row in result
    ]
    
    # Frame Colors
    result = db.execute(text("""
        SELECT color_name, color_code, hex_value, rgb_value, finish_type
        FROM frame_colors
        ORDER BY color_name
    """))
    reference_data['frame_colors'] = [
        {
            'color_name': row[0],
            'color_code': row[1],
            'hex_value': row[2],
            'rgb_value': row[3],
            'finish_type': row[4]
        }
        for row in result
    ]
    
    # Save to JSON
    json_backup_file = backup_dir / f'reference_data_{timestamp}.json'
    json_backup_file.write_text(json.dumps(reference_data, indent=2))
    
    # Summary
    print("✓ Reference data exported:")
    print(f"  • Frame Series: {len(reference_data['frame_series'])} records")
    print(f"  • Configuration Types: {len(reference_data['configuration_types'])} records")
    print(f"  • Glass Types: {len(reference_data['glass_types'])} records")
    print(f"  • Hardware Options: {len(reference_data['hardware_options'])} records")
    print(f"  • Frame Colors: {len(reference_data['frame_colors'])} records")
    print(f"\n  Saved to: {json_backup_file}")
    
except Exception as e:
    print(f"✗ Error exporting reference data: {e}")
finally:
    db.close()

# Step 3: Backup Summary
print("\n" + "=" * 70)
print("BACKUP SUMMARY")
print("=" * 70)
print()

backups = sorted(backup_dir.glob('*'))
print(f"Backup directory: {backup_dir.absolute()}")
print(f"Total backups: {len(backups)}")
print()

# Show recent backups
print("Recent backups:")
for backup in backups[-5:]:
    size_mb = backup.stat().st_size / (1024 * 1024)
    print(f"  • {backup.name} ({size_mb:.2f} MB)")

print()
print("=" * 70)
print("BACKUP COMMANDS")
print("=" * 70)
print()
print("Create backup:")
print("  python backup_database.py")
print()
print("Restore from SQL dump:")
print(f"  Get-Content backups\\postgres_backup_TIMESTAMP.sql | docker exec -i {container_name} psql -U {db_user} -d {db_name}")
print()
print("Import reference data from JSON:")
print("  python restore_reference_data.py backups/reference_data_TIMESTAMP.json")
print()
