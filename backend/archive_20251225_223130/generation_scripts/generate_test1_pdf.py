#!/usr/bin/env python3
"""Generate PDF drawings from Test_1 sheet"""
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
import os

load_dotenv()

# Override sheet name
os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'

from services.google_sheets_services import GoogleSheetsService
from services.drawing_generator import get_drawing_generator

print("=" * 70)
print("GENERATING PDF FROM Test_1 SHEET")
print("=" * 70)

try:
    # Get the sheet data
    print("\n[Reading Google Sheet: Test_1]")
    service = GoogleSheetsService()
    
    # Get the Test_1 sheet
    ws = service.get_worksheet('Test_1')
    print(f"  ✓ Found sheet: '{ws.title}'")
    print(f"  ✓ Dimensions: {ws.row_count} rows × {ws.col_count} cols")
    
    # Get all records
    records = ws.get_all_records()
    print(f"  ✓ Read {len(records)} records")
    
    # Create sample project structure from first few records
    windows = []
    doors = []
    
    for i, row in enumerate(records[:5]):  # Take first 5 records
        item_type = row.get('TYPE OF PRODUCT', '').strip().lower()
        
        item = {
            'item_number': row.get('ITEM #', f'ITEM-{i+1}').strip(),
            'room': row.get('room', f'Room {i+1}').strip(),
            'width_inches': float(row.get('Width (inches)', 36)) if row.get('Width (inches)') else 36,
            'height_inches': float(row.get('Height (inches)', 48)) if row.get('Height (inches)') else 48,
            'window_type': row.get('TYPE OF PRODUCT', 'Unknown').strip(),
            'frame_series': row.get('Frame Series', 'Standard').strip(),
            'swing_direction': row.get('Swing Direction', 'Both').strip(),
            'quantity': int(row.get('quantity:', 1)) if row.get('quantity:') else 1,
            'frame_color': row.get('Frame color', 'White').strip(),
            'glass_type': row.get('Glass', 'Standard').strip(),
        }
        
        if 'window' in item_type:
            windows.append(item)
        elif 'door' in item_type:
            doors.append(item)
    
    print(f"\n[Parsed Data]")
    print(f"  Windows found: {len(windows)}")
    print(f"  Doors found: {len(doors)}")
    
    # Create project structure
    project_data = {
        "metadata": {
            "po_number": "Test_1",
            "project_name": "Test_1 Project",
            "customer_name": "Test Customer",
        },
        "windows": windows,
        "doors": doors
    }
    
    # Generate drawings
    print(f"\n[Generating PDFs]")
    generator = get_drawing_generator("./drawings")
    files = generator.generate_project_package(project_data, "Test_1")
    
    print(f"\n[Success]")
    print(f"  ✓ Generated {len(files)} PDF(s):")
    for f in files:
        print(f"    - {os.path.basename(f)}")
    
    print(f"\n{'=' * 70}")
    print("✓ PDF GENERATION COMPLETE!")
    print(f"{'=' * 70}\n")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}")
    print(f"  {str(e)}")
    import traceback
    traceback.print_exc()
