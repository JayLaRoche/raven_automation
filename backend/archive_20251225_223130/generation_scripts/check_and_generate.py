#!/usr/bin/env python3
"""Check if PDFs were generated"""
import os
import glob

drawings_dir = r"c:\Users\larochej3\Desktop\raven-shop-automation\backend\drawings"

print("Checking for generated PDFs...\n")

if os.path.exists(drawings_dir):
    pdfs = glob.glob(os.path.join(drawings_dir, "*.pdf"))
    
    if pdfs:
        print(f"✓ Found {len(pdfs)} PDF file(s):\n")
        for pdf in sorted(pdfs):
            fname = os.path.basename(pdf)
            fsize = os.path.getsize(pdf) / 1024
            mtime = os.path.getmtime(pdf)
            print(f"  • {fname:50s} ({fsize:7.1f} KB)")
    else:
        print("✗ No PDFs found in drawings directory")
else:
    print(f"✗ Drawings directory not found: {drawings_dir}")

# Also try to run the generation directly
print("\n" + "=" * 70)
print("Attempting to generate PDFs now...")
print("=" * 70 + "\n")

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
import sys
sys.path.insert(0, '.')

try:
    from dotenv import load_dotenv
    load_dotenv()
    os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'
    
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_generator import get_drawing_generator
    
    service = GoogleSheetsService()
    project_data = service.parse_project_data()
    
    generator = get_drawing_generator("./drawings")
    files = generator.generate_project_package(project_data, project_data['metadata']['po_number'])
    
    print(f"\n✓ SUCCESS! Generated {len(files)} PDF(s):")
    for f in files:
        print(f"  • {os.path.basename(f)}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
