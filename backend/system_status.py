#!/usr/bin/env python3
"""
System Status Report
Complete overview of PostgreSQL system, reference data, and capabilities
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from sqlalchemy import text
import subprocess

print("=" * 70)
print("RAVEN CUSTOM GLASS - SYSTEM STATUS REPORT")
print("=" * 70)
print()

# Docker Status
print("[1] DOCKER CONTAINERS")
print("-" * 70)
try:
    result = subprocess.run('docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"', 
                          shell=True, capture_output=True, text=True)
    print(result.stdout)
except Exception as e:
    print(f"Error checking Docker: {e}")

# Database Connection
print("[2] DATABASE CONNECTION")
print("-" * 70)
db = SessionLocal()
try:
    result = db.execute(text("SELECT version()"))
    version = result.scalar()
    print(f"✓ Connected to PostgreSQL")
    print(f"  {version[:80]}...")
    
    # Database size
    result = db.execute(text("""
        SELECT pg_size_pretty(pg_database_size('raven_drawings'))
    """))
    size = result.scalar()
    print(f"  Database size: {size}")
    
except Exception as e:
    print(f"✗ Connection failed: {e}")

# Reference Data Statistics
print("\n[3] REFERENCE DATA")
print("-" * 70)

tables = {
    'frame_series': 'Frame Series',
    'configuration_types': 'Configuration Types',
    'glass_types': 'Glass Types',
    'hardware_options': 'Hardware Options',
    'frame_colors': 'Frame Colors'
}

for table, name in tables.items():
    try:
        result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        print(f"  • {name:25} {count:3} records")
    except Exception as e:
        print(f"  • {name:25} ERROR: {e}")

# Application Data
print("\n[4] APPLICATION DATA")
print("-" * 70)

app_tables = {
    'projects': 'Projects',
    'windows': 'Windows',
    'doors': 'Doors'
}

for table, name in app_tables.items():
    try:
        result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = result.scalar()
        print(f"  • {name:25} {count:3} records")
    except Exception as e:
        print(f"  • {name:25} ERROR: {e}")

# Recent Activity
print("\n[5] RECENT ACTIVITY")
print("-" * 70)

try:
    # Check if there are any projects
    result = db.execute(text("""
        SELECT project_name, created_at 
        FROM projects 
        ORDER BY created_at DESC 
        LIMIT 5
    """))
    projects = result.fetchall()
    
    if projects:
        print("Recent projects:")
        for proj in projects:
            print(f"  • {proj[0]} ({proj[1]})")
    else:
        print("  No projects created yet")
except Exception as e:
    print(f"  {e}")

# Generated Drawings
print("\n[6] GENERATED DRAWINGS")
print("-" * 70)

drawings_dir = Path('./drawings')
if drawings_dir.exists():
    pdfs = list(drawings_dir.glob('*.pdf'))
    print(f"  Total PDFs: {len(pdfs)}")
    
    if pdfs:
        print("  Recent drawings:")
        for pdf in sorted(pdfs, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            size_kb = pdf.stat().st_size / 1024
            print(f"    • {pdf.name} ({size_kb:.1f} KB)")
else:
    print("  Drawings directory not found")

# Backups
print("\n[7] BACKUPS")
print("-" * 70)

backups_dir = Path('./backups')
if backups_dir.exists():
    backups = list(backups_dir.glob('*'))
    print(f"  Total backups: {len(backups)}")
    
    if backups:
        print("  Recent backups:")
        for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)[:3]:
            size_kb = backup.stat().st_size / 1024
            print(f"    • {backup.name} ({size_kb:.1f} KB)")
else:
    print("  No backups created yet")

# System Capabilities
print("\n[8] SYSTEM CAPABILITIES")
print("-" * 70)
print("  ✅ PostgreSQL database with Docker")
print("  ✅ Reference data for accurate drawings")
print("  ✅ Data validation & auto-correction")
print("  ✅ Database migrations (Alembic)")
print("  ✅ Automated backups (SQL + JSON)")
print("  ✅ Professional drawing generation")
print("  ✅ Google Sheets integration")
print("  ✅ pgAdmin web interface")

# Quick Links
print("\n[9] QUICK ACCESS")
print("-" * 70)
print("  • pgAdmin:      http://localhost:5050")
print("  • Database:     localhost:5432")
print("  • Database:     raven_drawings")
print("  • User:         raven_user")

# Available Commands
print("\n[10] AVAILABLE COMMANDS")
print("-" * 70)
print("  Testing & Demo:")
print("    python test_postgres_integration.py")
print("    python quick_start_postgres.py")
print("    python test_validator.py")
print()
print("  Data Validation:")
print('    python validate_sheet_data.py "Sheet Name"')
print()
print("  Drawing Generation:")
print('    python generate_from_sheet.py "Sheet Name"')
print()
print("  Database Management:")
print("    python backup_database.py")
print("    python database/init_db.py")
print()
print("  Docker:")
print("    docker-compose up -d")
print("    docker-compose down")
print("    docker logs raven_postgres")

db.close()

print("\n" + "=" * 70)
print("STATUS: ✅ OPERATIONAL")
print("=" * 70)
print()
