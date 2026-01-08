#!/usr/bin/env python3
"""
Generate Single Drawing
Creates just 1 professional CAD drawing from Google Sheets
"""

from services.google_sheets_services import get_sheets_service
from app.services.integrated_drawing_service import get_drawing_service
from app.services.data_transformer import DataTransformer

# Get services
sheets_service = get_sheets_service()
drawing_service = get_drawing_service()

# Get the first available sheet
try:
    sheets = sheets_service.get_available_sheets()
    
    if not sheets:
        print("❌ No sheets available")
        exit(1)
    
    sheet_name = sheets[0]  # Use first sheet
    print(f"📋 Using sheet: {sheet_name}")
    
    # Get data from sheet
    worksheet = sheets_service.get_worksheet(sheet_name)
    rows = worksheet.get_all_records()
    
    if not rows:
        print("❌ No data in sheet")
        exit(1)
    
    # Get first row only
    row = rows[0]
    print(f"📊 Using row: {row.get('Item', 'N/A')}")
    
    # Project metadata
    project_data = {
        'po_number': sheet_name[:20],
        'project_name': sheet_name,
        'customer_name': 'Customer'
    }
    
    # Generate 1 drawing
    print("🎨 Generating drawing...")
    pdf_path = drawing_service.generate_from_google_sheets_row(
        row,
        'window',
        project_data=project_data
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"📄 Generated: {pdf_path}")
    print(f"📁 Location: ./drawings/")
    
    # Display PDF (temporary debugging method)
    import os
    import subprocess
    import time
    
    time.sleep(1)  # Wait for file to be written
    
    if os.path.exists(pdf_path):
        print("🖥️  Opening PDF viewer...")
        try:
            # Windows
            os.startfile(pdf_path)
        except AttributeError:
            # macOS/Linux
            subprocess.run(['open', pdf_path])
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
