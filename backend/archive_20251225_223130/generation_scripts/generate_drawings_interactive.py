#!/usr/bin/env python3
"""
Interactive Drawing Generator
Allow users to select a sheet and generate drawings from it
"""

import os
import sys

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

output_log = "generation_log.txt"

def log(msg):
    """Write to log file and print"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(output_log, "a") as f:
        f.write(line + "\n")

# Clear log
with open(output_log, "w") as f:
    f.write("=" * 70 + "\n")
    f.write("PDF GENERATION LOG - INTERACTIVE SHEET SELECTION\n")
    f.write("=" * 70 + "\n\n")

log("Starting interactive drawing generation...")

try:
    log("[1/7] Loading environment...")
    from dotenv import load_dotenv
    load_dotenv()
    
    log("[2/7] Importing services...")
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_engine import ProfessionalDrawingGenerator
    
    log("[3/7] Connecting to Google Sheets...")
    sheets_service = GoogleSheetsService()
    log("      ✓ Connected to spreadsheet")
    
    log("[4/7] Listing available sheets...")
    available_sheets = sheets_service.get_available_sheets()
    log(f"      ✓ Found {len(available_sheets)} sheets:")
    
    for i, sheet in enumerate(available_sheets, 1):
        log(f"         {i}. {sheet}")
    
    # User selection
    log("\n[5/7] Prompting user for sheet selection...")
    print("\n" + "=" * 70)
    print("AVAILABLE SHEETS")
    print("=" * 70)
    for i, sheet in enumerate(available_sheets, 1):
        print(f"{i}. {sheet}")
    print()
    
    while True:
        try:
            choice = input("Enter sheet number (1-{}): ".format(len(available_sheets)))
            sheet_index = int(choice) - 1
            if 0 <= sheet_index < len(available_sheets):
                selected_sheet = available_sheets[sheet_index]
                log(f"      ✓ User selected: '{selected_sheet}'")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    log(f"\n[6/7] Reading data from '{selected_sheet}'...")
    worksheet = sheets_service.get_worksheet(selected_sheet)
    sheet_data = worksheet.get_all_values()
    
    if not sheet_data or len(sheet_data) < 2:
        log(f"❌ No data found in sheet '{selected_sheet}'")
        sys.exit(1)
    
    headers = sheet_data[0]
    rows = sheet_data[1:]
    
    log(f"      ✓ Headers: {headers[:5]}...")
    log(f"      ✓ Found {len(rows)} data rows")
    
    log("[7/7] Generating drawings...")
    drawing_gen = ProfessionalDrawingGenerator('./drawings')
    
    # Project info
    project_data = {
        'po_number': selected_sheet.replace(' ', '-')[:20],
        'project_name': selected_sheet,
        'customer_name': selected_sheet
    }
    
    generated_files = []
    errors = []
    
    # Parse and generate
    for idx, row in enumerate(rows, 1):
        try:
            if not any(row):
                continue
            
            # Build item data from row (adapt to your sheet structure)
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
            result = drawing_gen.generate_window_drawing(item_data, project_data, filename)
            
            log(f"      ✓ [{idx}] {item_data['item_number']:12} → {filename}")
            generated_files.append(result)
            
        except Exception as e:
            error_msg = f"Row {idx}: {str(e)[:50]}"
            log(f"      ✗ {error_msg}")
            errors.append(error_msg)
    
    log("\n" + "=" * 70)
    log(f"✓ GENERATION COMPLETE")
    log(f"  Files generated: {len(generated_files)}")
    if errors:
        log(f"  Errors: {len(errors)}")
    log(f"  Output location: ./drawings/")
    log("=" * 70)
    
except Exception as e:
    log(f"\n✗ ERROR: {e}")
    import traceback
    log(traceback.format_exc())
    sys.exit(1)

log(f"\nLog saved to: {os.path.abspath(output_log)}")

# Print summary
print("\n" + "=" * 70)
print("GENERATION COMPLETE")
print("=" * 70)
with open(output_log, "r") as f:
    print(f.read())
