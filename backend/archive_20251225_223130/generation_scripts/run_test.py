#!/usr/bin/env python3
"""Generate PDF from Test_1 sheet"""
import sys
import os
sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv
load_dotenv()

os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'

try:
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_generator import get_drawing_generator
    
    print("=" * 70)
    print("GENERATING DRAWINGS FROM Test_1 SHEET")
    print("=" * 70)
    
    print("\n[Connecting to Google Sheets...]")
    service = GoogleSheetsService()
    
    print("[Parsing project data...]")
    project_data = service.parse_project_data()
    
    windows = project_data.get('windows', [])
    doors = project_data.get('doors', [])
    
    print(f"✓ Found {len(windows)} windows, {len(doors)} doors")
    
    if not windows and not doors:
        print("⚠ No items found, creating sample...")
        project_data = {
            "metadata": {
                "po_number": "TEST-1",
                "project_name": "Test Project",
                "customer_name": "Test"
            },
            "windows": [{
                "item_number": "W-001",
                "width_inches": 36,
                "height_inches": 48,
                "window_type": "Double Hung",
                "quantity": 1
            }],
            "doors": []
        }
    
    print("\n[Generating PDFs...]")
    generator = get_drawing_generator("./drawings")
    files = generator.generate_project_package(project_data, project_data['metadata']['po_number'])
    
    print(f"\n✓ SUCCESS! Generated {len(files)} PDF(s):")
    for f in files:
        print(f"  • {os.path.basename(f)}")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
