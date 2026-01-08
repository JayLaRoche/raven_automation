#!/usr/bin/env python3
import os
import json
import sys

sys.path.insert(0, r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")

result_file = "generation_status.txt"

with open(result_file, "w") as f:
    f.write("=" * 80 + "\n")
    f.write("GENERATION STATUS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    # Check drawings directory
    drawings_dir = "./drawings"
    f.write(f"Drawings Directory: {os.path.abspath(drawings_dir)}\n")
    f.write(f"Exists: {os.path.exists(drawings_dir)}\n\n")
    
    if os.path.exists(drawings_dir):
        all_files = os.listdir(drawings_dir)
        pdf_files = [f for f in all_files if f.endswith('.pdf')]
        test_1_pdfs = [f for f in pdf_files if 'Test_1' in f or 'test_1' in f.lower()]
        
        f.write(f"Total Files: {len(all_files)}\n")
        f.write(f"Total PDFs: {len(pdf_files)}\n")
        f.write(f"Test_1 PDFs: {len(test_1_pdfs)}\n\n")
        
        if test_1_pdfs:
            f.write("✓ Test_1 PDFs Found:\n")
            for pdf in sorted(test_1_pdfs):
                fsize = os.path.getsize(os.path.join(drawings_dir, pdf)) / 1024
                f.write(f"  • {pdf} ({fsize:.1f} KB)\n")
        else:
            f.write("✗ No Test_1 PDFs found\n\n")
            f.write("All PDFs in directory:\n")
            for pdf in sorted(pdf_files)[:10]:
                fsize = os.path.getsize(os.path.join(drawings_dir, pdf)) / 1024
                f.write(f"  • {pdf} ({fsize:.1f} KB)\n")
    
    f.write("\n" + "=" * 80 + "\n")
    f.write("ATTEMPTING GENERATION\n")
    f.write("=" * 80 + "\n\n")
    
    try:
        f.write("[1] Loading environment...\n")
        from dotenv import load_dotenv
        load_dotenv()
        f.write("    ✓ Environment loaded\n\n")
        
        f.write("[2] Importing services...\n")
        from services.google_sheets_services import GoogleSheetsService
        from services.drawing_generator import get_drawing_generator
        f.write("    ✓ Imports successful\n\n")
        
        f.write("[3] Connecting to Google Sheets...\n")
        service = GoogleSheetsService()
        f.write("    ✓ Connected\n\n")
        
        f.write("[4] Getting Test_1 worksheet...\n")
        ws = service.get_worksheet('Test_1')
        records = ws.get_all_records()
        f.write(f"    ✓ Found {len(records)} records\n\n")
        
        f.write("[5] Parsing data...\n")
        project_data = service.parse_project_data()
        windows = len(project_data.get('windows', []))
        doors = len(project_data.get('doors', []))
        f.write(f"    ✓ Parsed {windows} windows, {doors} doors\n\n")
        
        f.write("[6] Generating PDFs...\n")
        generator = get_drawing_generator("./drawings")
        files = generator.generate_project_package(project_data, "Test_1")
        f.write(f"    ✓ Generated {len(files)} PDFs\n\n")
        
        for file in files:
            fname = os.path.basename(file)
            fsize = os.path.getsize(file) / 1024
            f.write(f"      • {fname} ({fsize:.1f} KB)\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("✓ SUCCESS\n")
        f.write("=" * 80 + "\n")
        
    except Exception as e:
        f.write(f"\n✗ ERROR: {type(e).__name__}\n")
        f.write(f"{str(e)}\n\n")
        import traceback
        f.write("Traceback:\n")
        f.write(traceback.format_exc())

print("Report written to: generation_status.txt")

# Read and display
with open(result_file, "r") as f:
    content = f.read()
    print(content)
