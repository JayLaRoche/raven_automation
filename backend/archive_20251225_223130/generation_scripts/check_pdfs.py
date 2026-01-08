#!/usr/bin/env python3
"""Check generated PDFs"""
import os
import glob
from datetime import datetime

drawings_dir = r"c:\Users\larochej3\Desktop\raven-shop-automation\backend\drawings"

print("=" * 70)
print("CHECKING GENERATED PDFs FROM Test_1")
print("=" * 70)
print()

if os.path.exists(drawings_dir):
    pdfs = sorted(glob.glob(os.path.join(drawings_dir, "Test_1*.pdf")))
    
    if pdfs:
        print(f"✓ Found {len(pdfs)} PDF file(s):\n")
        for pdf in pdfs:
            fname = os.path.basename(pdf)
            fsize = os.path.getsize(pdf) / 1024  # KB
            mtime = datetime.fromtimestamp(os.path.getmtime(pdf)).strftime("%Y-%m-%d %H:%M:%S")
            print(f"  • {fname:55s} {fsize:8.1f} KB  ({mtime})")
        print()
    else:
        print("✗ No PDFs found matching 'Test_1*.pdf'\n")
        print("  All PDFs in drawings directory:")
        all_pdfs = glob.glob(os.path.join(drawings_dir, "*.pdf"))
        if all_pdfs:
            for pdf in sorted(all_pdfs)[-5:]:
                fname = os.path.basename(pdf)
                fsize = os.path.getsize(pdf) / 1024
                print(f"    - {fname} ({fsize:.1f} KB)")
        else:
            print("    - (none)")
else:
    print(f"✗ Drawings directory not found: {drawings_dir}\n")

# Try to trigger generation if no PDFs exist
if not pdfs or len(pdfs) == 0:
    print("=" * 70)
    print("ATTEMPTING TO GENERATE PDFs")
    print("=" * 70)
    print()
    
    try:
        import sys
        sys.path.insert(0, r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
        
        from dotenv import load_dotenv
        from services.google_sheets_services import GoogleSheetsService
        from services.drawing_generator import get_drawing_generator
        
        load_dotenv()
        
        print("[1] Connecting to Google Sheets...")
        service = GoogleSheetsService()
        
        print("[2] Getting Test_1 sheet...")
        ws = service.get_worksheet('Test_1')
        records = ws.get_all_records()
        print(f"    Found {len(records)} records")
        
        print("[3] Parsing project data...")
        project_data = service.parse_project_data()
        print(f"    Windows: {len(project_data.get('windows', []))}")
        print(f"    Doors: {len(project_data.get('doors', []))}")
        
        print("[4] Generating PDFs...")
        generator = get_drawing_generator("./drawings")
        files = generator.generate_project_package(project_data, "Test_1")
        
        print(f"\n✓ SUCCESS! Generated {len(files)} PDF(s):")
        for f in files:
            fname = os.path.basename(f)
            fsize = os.path.getsize(f) / 1024
            print(f"  • {fname} ({fsize:.1f} KB)")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
