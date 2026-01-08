#!/usr/bin/env python3
"""
Generate professional shop drawings from 'updated Evergreen Creek' Google Sheets
"""

from services.google_sheets_services import GoogleSheetsService
from services.drawing_engine import ProfessionalDrawingGenerator
import os
from datetime import datetime

def parse_sheet_row(row_data, headers):
    """Parse a sheet row into drawing data format"""
    data = {}
    for i, header in enumerate(headers):
        if i < len(row_data):
            data[header.lower().strip()] = row_data[i]
    return data

def generate_drawings_from_sheet(sheet_name='updated Evergreen Creek'):
    """Generate drawings from Google Sheets data"""
    
    # Initialize services
    sheets_service = GoogleSheetsService()
    drawing_gen = ProfessionalDrawingGenerator('./drawings')
    
    print(f"📄 Reading from sheet: '{sheet_name}'")
    print("-" * 60)
    
    try:
        # Get worksheet
        worksheet = sheets_service.get_worksheet(sheet_name)
        
        if not worksheet:
            print(f"❌ Sheet '{sheet_name}' not found")
            return
        
        # Get all values from worksheet
        sheet_data = worksheet.get_all_values()
        
        if not sheet_data or len(sheet_data) < 2:
            print(f"❌ No data found in sheet '{sheet_name}'")
            return
        
        # First row is headers
        headers = sheet_data[0]
        rows = sheet_data[1:]
        
        print(f"✓ Headers: {headers}")
        print(f"✓ Found {len(rows)} items to generate")
        print("-" * 60)
        
        # Project info (from headers or defaults)
        project_data = {
            'po_number': sheet_name.replace(' ', '-')[:20],
            'project_name': sheet_name,
            'customer_name': 'Evergreen Creek'
        }
        
        generated_files = []
        errors = []
        
        # Generate drawing for each row
        for idx, row in enumerate(rows, 1):
            try:
                # Parse row data
                item_data = parse_sheet_row(row, headers)
                
                # Skip empty rows
                if not any(item_data.values()):
                    continue
                
                # Extract required fields
                item_number = item_data.get('item', f'ITEM-{idx}')
                width = float(item_data.get('width', item_data.get('width inches', 36)))
                height = float(item_data.get('height', item_data.get('height inches', 48)))
                product_type = item_data.get('type', item_data.get('product type', 'Window'))
                
                # Prepare structured data
                window_data = {
                    'item_number': str(item_number),
                    'width_inches': width,
                    'height_inches': height,
                    'window_type': item_data.get('window type', 'Standard'),
                    'frame_series': item_data.get('frame series', item_data.get('series', 'Series 6000')),
                    'swing_direction': item_data.get('swing', item_data.get('swing direction', 'Out')),
                    'glass_type': item_data.get('glass', item_data.get('glass type', 'Low-E')),
                    'frame_color': item_data.get('color', item_data.get('frame color', 'White')),
                    'quantity': int(item_data.get('qty', item_data.get('quantity', 1)))
                }
                
                # Generate filename
                product_type_short = 'Window' if 'window' in product_type.lower() else 'Door'
                filename = f"{project_data['po_number']}_{product_type_short}-{item_number}_ELEV.pdf"
                
                # Generate drawing
                if product_type_short == 'Window':
                    result = drawing_gen.generate_window_drawing(window_data, project_data, filename)
                else:
                    result = drawing_gen.generate_door_drawing(window_data, project_data, filename)
                
                print(f"✓ [{idx:2d}] {item_number:12} ({width:.0f}\"x{height:.0f}\") → {filename}")
                generated_files.append(result)
                
            except Exception as e:
                error_msg = f"Row {idx}: {str(e)}"
                print(f"✗ [{idx:2d}] ERROR: {error_msg}")
                errors.append(error_msg)
        
        print("-" * 60)
        print(f"\n✓ Successfully generated {len(generated_files)} drawings")
        if errors:
            print(f"⚠ {len(errors)} errors encountered")
        
        return generated_files
        
    except Exception as e:
        print(f"❌ Failed to read sheet: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    # Generate drawings from 'updated Evergreen Creek' sheet
    files = generate_drawings_from_sheet('updated Evergreen Creek')
    
    if files:
        print(f"\n📁 Generated files location: ./drawings/")
        print(f"📊 Total files: {len(files)}")
