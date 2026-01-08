#!/usr/bin/env python3
"""Direct execution with file output"""
import sys
import os

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
sys.path.insert(0, '.')

output_file = "generation_result.txt"

with open(output_file, "w") as f:
    f.write("=" * 70 + "\n")
    f.write("GENERATING DRAWINGS FROM Test_1 SHEET\n")
    f.write("=" * 70 + "\n\n")
    
    try:
        f.write("[Step 1] Importing services...\n")
        from dotenv import load_dotenv
        load_dotenv()
        os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'
        
        from services.google_sheets_services import GoogleSheetsService
        from services.drawing_generator import get_drawing_generator
        f.write("  ✓ Imports successful\n")
        
        f.write("\n[Step 2] Connecting to Google Sheets...\n")
        service = GoogleSheetsService()
        f.write("  ✓ Connected\n")
        
        f.write("\n[Step 3] Getting Test_1 worksheet...\n")
        ws = service.get_worksheet('Test_1')
        f.write(f"  ✓ Found '{ws.title}' ({ws.row_count}x{ws.col_count})\n")
        
        f.write("\n[Step 4] Reading records...\n")
        records = ws.get_all_records()
        f.write(f"  ✓ Read {len(records)} records\n")
        
        f.write("\n[Step 5] Parsing project data...\n")
        project_data = service.parse_project_data()
        windows = len(project_data.get('windows', []))
        doors = len(project_data.get('doors', []))
        f.write(f"  ✓ Found {windows} windows, {doors} doors\n")
        
        po_number = project_data['metadata']['po_number']
        
        f.write(f"\n[Step 6] Generating PDFs for {po_number}...\n")
        generator = get_drawing_generator("./drawings")
        files = generator.generate_project_package(project_data, po_number)
        
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"✓ SUCCESS! Generated {len(files)} PDFs:\n")
        f.write("=" * 70 + "\n\n")
        
        for file in files:
            fname = os.path.basename(file)
            fsize = os.path.getsize(file) / 1024
            f.write(f"  • {fname:50s} ({fsize:7.1f} KB)\n")
        
        f.write(f"\nLocation: {os.path.abspath('./drawings')}\n")
        
    except Exception as e:
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"✗ ERROR: {type(e).__name__}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"{str(e)}\n\n")
        
        import traceback
        f.write("Traceback:\n")
        f.write(traceback.format_exc())

print(f"Results written to: c:\\Users\\larochej3\\Desktop\\raven-shop-automation\\backend\\{output_file}")
