#!/usr/bin/env python3
"""Debug: Check what's in Test_1 sheet and database"""
import os
import sys
os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("DEBUGGING Test_1 SHEET")
print("=" * 70)

try:
    from services.google_sheets_services import GoogleSheetsService
    from app.database import SessionLocal
    from app.models import Project
    
    # Check Google Sheets
    print("\n[1] Checking Google Sheets for 'Test_1'...")
    service = GoogleSheetsService()
    
    try:
        ws = service.get_worksheet('Test_1')
        records = ws.get_all_records()
        print(f"  ✓ Found 'Test_1' sheet with {len(records)} records")
        
        if records:
            print(f"  ✓ First record headers: {list(records[0].keys())[:5]}")
            print(f"  ✓ Sample data: {records[0]}")
    except Exception as e:
        print(f"  ✗ Error reading Test_1: {e}")
        print("\n  Available sheets (checking for similar names):")
        worksheets = service.spreadsheet.worksheets()
        for ws in worksheets[:20]:
            print(f"    - '{ws.title}'")
    
    # Check Database
    print("\n[2] Checking SQLite database for 'Test_1'...")
    db = SessionLocal()
    project = db.query(Project).filter(Project.po_number == 'Test_1').first()
    
    if project:
        print(f"  ✓ Found 'Test_1' in database")
        print(f"    - Project: {project.project_name}")
        print(f"    - Windows: {len(project.windows)}")
        print(f"    - Doors: {len(project.doors)}")
    else:
        print(f"  ✗ 'Test_1' not in database - needs to be synced")
        
        # List what IS in the database
        all_projects = db.query(Project).all()
        print(f"\n  Projects in database ({len(all_projects)}):")
        for p in all_projects[:5]:
            print(f"    - {p.po_number}: {p.project_name} ({len(p.windows)} windows, {len(p.doors)} doors)")
    
    db.close()
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
