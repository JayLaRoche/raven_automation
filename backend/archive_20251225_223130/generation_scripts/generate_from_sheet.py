#!/usr/bin/env python3
"""
Quick script to generate drawings from any sheet
Usage: python generate_from_sheet.py "Sheet Name"
"""

import sys
import os

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

from dotenv import load_dotenv
from services.google_sheets_services import GoogleSheetsService
from services.drawing_engine import ProfessionalDrawingGenerator

load_dotenv()

if len(sys.argv) < 2:
    print("📄 AVAILABLE SHEETS:")
    print("=" * 60)
    sheets = GoogleSheetsService()
    available = sheets.get_available_sheets()
    for i, sheet in enumerate(available, 1):
        print(f"  {i:3}. {sheet}")
    print("=" * 60)
    print("\nUsage: python generate_from_sheet.py \"Sheet Name\"")
    print("\nExample:")
    print("  python generate_from_sheet.py \"updated Evergreen Creek\"")
    print("  python generate_from_sheet.py \"Test_1\"")
    sys.exit(0)

sheet_name = sys.argv[1]

print("=" * 70)
print(f"GENERATING DRAWINGS FROM '{sheet_name}'")
print("=" * 70)

try:
    sheets_service = GoogleSheetsService()
    gen = ProfessionalDrawingGenerator('./drawings')
    
    print(f"\n[1] Reading sheet...")
    worksheet = sheets_service.get_worksheet(sheet_name)
    sheet_data = worksheet.get_all_values()
    
    if not sheet_data or len(sheet_data) < 2:
        print(f"❌ No data in sheet '{sheet_name}'")
        sys.exit(1)
    
    headers = sheet_data[0]
    rows = sheet_data[1:]
    
    print(f"    ✓ Found {len(rows)} items")
    
    print(f"\n[2] Generating drawings...")
    project_data = {
        'po_number': sheet_name.replace(' ', '-')[:20],
        'project_name': sheet_name,
        'customer_name': sheet_name
    }
    
    generated = 0
    for idx, row in enumerate(rows, 1):
        try:
            if not any(row):
                continue
            
            item_data = {
                'item_number': row[0] if len(row) > 0 else f'ITEM-{idx}',
                'width_inches': float(row[1]) if len(row) > 1 and row[1] else 36,
                'height_inches': float(row[2]) if len(row) > 2 and row[2] else 48,
                'window_type': row[3] if len(row) > 3 else 'Standard',
                'frame_series': row[4] if len(row) > 4 else 'Series 6000',
                'swing_direction': row[5] if len(row) > 5 else 'Out',
                'glass_type': row[6] if len(row) > 6 else 'Low-E',
                'frame_color': row[7] if len(row) > 7 else 'White',
                'quantity': int(row[8]) if len(row) > 8 and row[8] else 1
            }
            
            filename = f"{project_data['po_number']}_Window-{item_data['item_number']}_ELEV.pdf"
            gen.generate_window_drawing(item_data, project_data, filename)
            
            print(f"    ✓ [{idx:3}] {item_data['item_number']:12}")
            generated += 1
            
        except Exception as e:
            pass
    
    print(f"\n✅ SUCCESS! Generated {generated} drawings")
    print(f"📁 Location: ./drawings/")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
