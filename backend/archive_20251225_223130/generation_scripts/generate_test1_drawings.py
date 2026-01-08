#!/usr/bin/env python3
"""Generate drawings from Test_1 sheet"""
import sys
sys.path.insert(0, '.')
import os

# Set the sheet name before loading env
os.environ['GOOGLE_SHEET_NAME'] = 'Test_1'

from dotenv import load_dotenv
load_dotenv()

from services.google_sheets_services import get_sheets_service
from services.drawing_generator import get_drawing_generator

print("=" * 70)
print("GENERATING DRAWINGS FROM Test_1 SHEET")
print("=" * 70)

try:
    sheets_service = get_sheets_service()
    print("\n[Reading from Test_1 sheet...]")
    project_data = sheets_service.parse_project_data()
    
    if not project_data.get('windows') and not project_data.get('doors'):
        print("No data found in Test_1 sheet")
        sys.exit(1)
    
    po_number = project_data['metadata'].get('po_number', 'TEST_1')
    print(f"Project: {po_number}")
    print(f"Windows: {len(project_data.get('windows', []))}")
    print(f"Doors: {len(project_data.get('doors', []))}")
    
    print("\n[Generating PDFs...]")
    generator = get_drawing_generator()
    drawing_files = generator.generate_project_package(project_data, po_number)
    
    print(f"\nGenerated {len(drawing_files)} drawing(s):")
    for f in drawing_files:
        print(f"  - {os.path.basename(f)}")
    
    print("\n" + "=" * 70)
    print("SUCCESS - Drawings generated from Test_1 sheet!")
    print("=" * 70)
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
