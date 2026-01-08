#!/usr/bin/env python3
"""List all available sheets"""
from services.google_sheets_services import GoogleSheetsService

print("Listing all available sheets...")
try:
    service = GoogleSheetsService()
    
    # List all worksheets
    worksheets = service.spreadsheet.worksheets()
    
    print(f"\nFound {len(worksheets)} worksheets:\n")
    for i, ws in enumerate(worksheets, 1):
        print(f"{i:3d}. '{ws.title}' ({ws.row_count} rows × {ws.col_count} cols)")
        
        # Show first row (headers) for sheets that contain "Test"
        if 'test' in ws.title.lower():
            try:
                records = ws.get_all_records()
                if records:
                    print(f"      Headers: {list(records[0].keys())[:5]}...")
            except:
                pass
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
