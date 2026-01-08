#!/usr/bin/env python3
"""Complete test of PDF generation with detailed logging"""
import os
import sys
import json
from datetime import datetime

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

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
    f.write("PDF GENERATION LOG\n")
    f.write("=" * 70 + "\n\n")

log("Starting PDF generation process...")

try:
    log("[1/6] Loading environment...")
    from dotenv import load_dotenv
    load_dotenv()
    log(f"      GOOGLE_SHEET_ID: {os.getenv('GOOGLE_SHEET_ID', 'NOT SET')[:30]}...")
    log(f"      DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
    
    log("[2/6] Importing services...")
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_generator import get_drawing_generator
    
    log("[3/6] Connecting to Google Sheets...")
    service = GoogleSheetsService()
    log("      ✓ Connected to spreadsheet")
    
    log("[4/6] Reading 'Test_1' sheet...")
    try:
        ws = service.get_worksheet('Test_1')
        log(f"      ✓ Found worksheet: '{ws.title}' ({ws.row_count} rows × {ws.col_count} cols)")
        
        records = ws.get_all_records()
        log(f"      ✓ Read {len(records)} records")
        
        if len(records) > 0:
            first_keys = list(records[0].keys())[:3]
            log(f"      ✓ Headers: {first_keys}")
        
    except Exception as e:
        log(f"      ✗ Error reading Test_1: {e}")
        # List available sheets
        log("      Available sheets:")
        worksheets = service.spreadsheet.worksheets()
        for ws in worksheets[:10]:
            log(f"        - '{ws.title}'")
        raise
    
    log("[5/6] Parsing project data...")
    project_data = service.parse_project_data()
    windows = project_data.get('windows', [])
    doors = project_data.get('doors', [])
    log(f"      ✓ Found {len(windows)} windows, {len(doors)} doors")
    
    if not windows and not doors:
        log("      ⚠ No items found in sheet, creating sample...")
        project_data = {
            'metadata': {
                'po_number': 'Test_1',
                'project_name': 'Test_1 Sample Project',
                'customer_name': 'Test Customer'
            },
            'windows': [{
                'item_number': 'SAMPLE-W-001',
                'width_inches': 36,
                'height_inches': 48,
                'window_type': 'Double Hung',
                'quantity': 1
            }],
            'doors': []
        }
    
    log("[6/6] Generating PDFs...")
    generator = get_drawing_generator("./drawings")
    files = generator.generate_project_package(project_data, "Test_1")
    log(f"      ✓ Generated {len(files)} file(s)")
    
    for f in files:
        fname = os.path.basename(f)
        fsize = os.path.getsize(f) / 1024
        log(f"        • {fname} ({fsize:.1f} KB)")
    
    log("\n" + "=" * 70)
    log("✓ SUCCESS! PDFs generated successfully")
    log("=" * 70)
    
except Exception as e:
    log(f"\n✗ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    log("\nTraceback:")
    for line in traceback.format_exc().split('\n'):
        log(f"  {line}")

log(f"\nLog saved to: {os.path.abspath(output_log)}")

# Print the log
print("\n" + "=" * 70)
print("FULL LOG:")
print("=" * 70)
with open(output_log, "r") as f:
    print(f.read())
