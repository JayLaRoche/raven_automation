#!/usr/bin/env python3
"""Direct execution of PDF generation from Test_1"""
import sys
import os

# Set working directory
os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Override sheet name
os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'

print("=" * 70)
print("GENERATING DRAWINGS FROM Test_1 SHEET")
print("=" * 70)
print()

try:
    print("[Step 1] Importing services...")
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_generator import get_drawing_generator
    print("  ✓ Imports successful")
    
    print("\n[Step 2] Connecting to Google Sheets...")
    service = GoogleSheetsService()
    print("  ✓ Connected to spreadsheet")
    
    print("\n[Step 3] Getting Test_1 worksheet...")
    ws = service.get_worksheet('Test_1')
    print(f"  ✓ Found worksheet '{ws.title}' ({ws.row_count}x{ws.col_count})")
    
    print("\n[Step 4] Reading data from Test_1...")
    records = ws.get_all_records()
    print(f"  ✓ Read {len(records)} records")
    
    if len(records) == 0:
        print("  ⚠ No records found, using sample data instead...")
        project_data = {
            "metadata": {
                "po_number": "TEST-1",
                "project_name": "Test_1 Sample",
                "customer_name": "Sample Customer"
            },
            "windows": [{
                "item_number": "W-001",
                "width_inches": 36,
                "height_inches": 48,
                "window_type": "Double Hung",
                "frame_series": "Standard",
                "quantity": 1
            }],
            "doors": []
        }
    else:
        print("\n[Step 5] Parsing project data...")
        project_data = service.parse_project_data()
        windows = project_data.get('windows', [])
        doors = project_data.get('doors', [])
        print(f"  ✓ Parsed {len(windows)} windows, {len(doors)} doors")
    
    po_number = project_data['metadata']['po_number']
    
    print(f"\n[Step 6] Generating PDFs for {po_number}...")
    generator = get_drawing_generator("./drawings")
    files = generator.generate_project_package(project_data, po_number)
    
    print(f"\n{'=' * 70}")
    print(f"✓ SUCCESS!")
    print(f"{'=' * 70}")
    print(f"Generated {len(files)} PDF file(s):\n")
    for f in files:
        fname = os.path.basename(f)
        fsize = os.path.getsize(f) / 1024  # KB
        print(f"  ✓ {fname:50s} ({fsize:7.1f} KB)")
    
    print(f"\nLocation: {os.path.abspath('./drawings')}")
    print()

except Exception as e:
    print(f"\n{'=' * 70}")
    print(f"✗ ERROR: {type(e).__name__}")
    print(f"{'=' * 70}")
    print(f"\n{str(e)}\n")
    
    import traceback
    print("Traceback:")
    traceback.print_exc()
    
    sys.exit(1)
