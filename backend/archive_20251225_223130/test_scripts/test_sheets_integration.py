#!/usr/bin/env python3
"""Test Google Sheets API Integration"""
import sys
import os

sys.path.insert(0, '.')

from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("GOOGLE SHEETS API INTEGRATION CHECK")
print("=" * 70)

# Check environment variables
creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
sheet_id = os.getenv("GOOGLE_SHEET_ID")
sheet_name = os.getenv("GOOGLE_SHEET_NAME")

print(f"\n[Config]")
print(f"  Credentials Path: {creds_path}")
print(f"  Credentials Exists: {os.path.exists(creds_path)}")
print(f"  Sheet ID: {sheet_id}")
print(f"  Sheet Name: {sheet_name}")

# Try to import and instantiate the service
print(f"\n[Testing Service Import]")
try:
    from services.google_sheets_services import GoogleSheetsService, get_sheets_service
    print("  ✓ GoogleSheetsService imported successfully")
    
    # Try to instantiate via singleton
    print(f"\n[Testing Service Initialization]")
    service = get_sheets_service()
    print("  ✓ Service instantiated via singleton successfully")
    
    # Try to get PO numbers
    print(f"\n[Testing Google Sheets Connection]")
    po_numbers = service.get_all_po_numbers()
    print(f"  ✓ Successfully connected to Google Sheets!")
    print(f"  ✓ Found {len(po_numbers)} PO numbers:")
    for po in po_numbers:
        print(f"    - {po}")
    
    print(f"\n[Testing Data Parsing]")
    if po_numbers:
        first_po = po_numbers[0]
        project_data = service.parse_project_data(first_po)
        print(f"  ✓ Successfully parsed project data for {first_po}")
        print(f"    - Windows: {len(project_data['windows'])}")
        print(f"    - Doors: {len(project_data['doors'])}")
    
    print(f"\n{'=' * 70}")
    print("✓ ALL CHECKS PASSED - Google Sheets API integration is working!")
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
