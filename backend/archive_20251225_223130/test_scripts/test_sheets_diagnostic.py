#!/usr/bin/env python3
"""Test Google Sheets API Integration - Diagnostic Version"""
import sys
import os

sys.path.insert(0, '.')

from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("GOOGLE SHEETS API INTEGRATION - DIAGNOSTIC")
print("=" * 70)

# Check environment variables
creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
sheet_id = os.getenv("GOOGLE_SHEET_ID")
sheet_name = os.getenv("GOOGLE_SHEET_NAME")

print(f"\n[Config]")
print(f"  Credentials Path: {creds_path}")
print(f"  Credentials Exists: {os.path.exists(creds_path)}")
print(f"  Sheet ID: {sheet_id}")
print(f"  Sheet Name (from .env): {sheet_name}")

# Try to import and instantiate the service
print(f"\n[Testing Service Import]")
try:
    from services.google_sheets_services import GoogleSheetsService, get_sheets_service
    print("  ✓ GoogleSheetsService imported successfully")
    
    # Try to instantiate via singleton
    print(f"\n[Testing Service Initialization]")
    service = get_sheets_service()
    print("  ✓ Service instantiated via singleton successfully")
    
    # List all available worksheets
    print(f"\n[Available Worksheets in Spreadsheet]")
    spreadsheet = service.spreadsheet
    worksheets = spreadsheet.worksheets()
    
    print(f"  Found {len(worksheets)} worksheet(s):")
    for i, ws in enumerate(worksheets, 1):
        print(f"    {i}. '{ws.title}' (ID: {ws.id}, {ws.row_count} rows x {ws.col_count} cols)")
    
    # Try to use the first worksheet
    if worksheets:
        first_sheet = worksheets[0]
        print(f"\n[Testing Data Reading from '{first_sheet.title}']")
        
        try:
            records = first_sheet.get_all_records()
            print(f"  ✓ Read {len(records)} records")
            
            if records:
                print(f"\n  First record columns:")
                first = records[0]
                for key in list(first.keys())[:5]:  # Show first 5 columns
                    print(f"    - {key}: {first[key]}")
        except Exception as e:
            print(f"  ✗ Error reading data: {e}")
    
    print(f"\n{'=' * 70}")
    print("⚠️  NEXT STEP: Update GOOGLE_SHEET_NAME in .env to one of the worksheet names above")
    print(f"{'=' * 70}\n")
    
except ImportError as e:
    print(f"  ✗ Import Error: {str(e)}")
    import traceback
    traceback.print_exc()
except ValueError as e:
    print(f"  ✗ Configuration Error: {str(e)}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"  ✗ Error: {type(e).__name__}")
    print(f"     {str(e)}")
    import traceback
    traceback.print_exc()
