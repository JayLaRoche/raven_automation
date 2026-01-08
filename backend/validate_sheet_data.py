#!/usr/bin/env python3
"""
Validate Google Sheets Data
Checks if all values in Google Sheets match reference data
Suggests corrections for invalid values
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.services.reference_data_validator import ReferenceDataValidator
from services.google_sheets_services import GoogleSheetsService

print("=" * 70)
print("GOOGLE SHEETS DATA VALIDATION")
print("=" * 70)
print()

# Initialize services
db = SessionLocal()
validator = ReferenceDataValidator(db)
sheets_service = GoogleSheetsService()

# Get available sheets
print("[Step 1] Available Google Sheets")
print("-" * 70)
sheets = sheets_service.get_available_sheets()
print(f"Found {len(sheets)} sheets:")
for i, sheet in enumerate(sheets[:10], 1):
    print(f"  {i}. {sheet}")
if len(sheets) > 10:
    print(f"  ... and {len(sheets) - 10} more")
print()

# Select sheet to validate
if len(sys.argv) > 1:
    sheet_name = sys.argv[1]
else:
    sheet_name = sheets[0] if sheets else "Test_1"

print(f"[Step 2] Validating Sheet: '{sheet_name}'")
print("-" * 70)

try:
    # Parse sheet data
    project_data = sheets_service.parse_project_sheet(sheet_name)
    
    windows = project_data.get('windows', [])
    doors = project_data.get('doors', [])
    
    print(f"Found: {len(windows)} windows, {len(doors)} doors")
    print()
    
    # Validate each window
    print("[Step 3] Validating Windows")
    print("-" * 70)
    
    total_errors = 0
    corrected_items = []
    
    for i, window in enumerate(windows, 1):
        is_valid, errors = validator.validate_window(window)
        
        if not is_valid:
            print(f"\n❌ Window {i}: {window.get('item_number', 'Unknown')}")
            for error in errors:
                print(f"   • {error}")
                total_errors += 1
            
            # Show auto-corrected version
            corrected = validator.auto_correct(window)
            corrected_items.append((window, corrected))
    
    # Validate each door
    if doors:
        print("\n[Step 4] Validating Doors")
        print("-" * 70)
        
        for i, door in enumerate(doors, 1):
            is_valid, errors = validator.validate_door(door)
            
            if not is_valid:
                print(f"\n❌ Door {i}: {door.get('item_number', 'Unknown')}")
                for error in errors:
                    print(f"   • {error}")
                    total_errors += 1
                
                corrected = validator.auto_correct(door)
                corrected_items.append((door, corrected))
    
    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    
    if total_errors == 0:
        print("\n✅ All data is valid! No errors found.")
    else:
        print(f"\n⚠️  Found {total_errors} validation errors")
        print(f"   {len(corrected_items)} items need correction")
        
        if corrected_items:
            print("\n[Auto-Corrections Available]")
            print("-" * 70)
            for original, corrected in corrected_items[:5]:
                print(f"\nItem: {original.get('item_number', 'Unknown')}")
                
                # Show what changed
                for key in ['frame_series', 'glass_type', 'hardware', 'frame_color', 'configuration']:
                    if key in original and key in corrected and original[key] != corrected[key]:
                        print(f"  {key}: '{original[key]}' → '{corrected[key]}'")
            
            if len(corrected_items) > 5:
                print(f"\n... and {len(corrected_items) - 5} more items")
    
    # Show available reference data
    print("\n[Available Reference Data]")
    print("-" * 70)
    summary = validator.get_reference_summary()
    
    print("\nFrame Series:")
    for series in summary['frame_series'][:5]:
        print(f"  • {series}")
    
    print("\nGlass Types:")
    for glass in summary['glass_types'][:5]:
        print(f"  • {glass}")
    
    print("\nFrame Colors:")
    for color in summary['colors']:
        print(f"  • {color}")
    
    print("\nConfigurations:")
    for config in summary['configurations'][:8]:
        print(f"  • {config}")
    
except Exception as e:
    print(f"❌ Error validating sheet: {e}")
    import traceback
    traceback.print_exc()

finally:
    db.close()

print("\n" + "=" * 70)
print("USAGE")
print("=" * 70)
print("\nValidate specific sheet:")
print('  python validate_sheet_data.py "Sheet Name"')
print()
print("View reference data:")
print("  python quick_start_postgres.py")
print()
print("Update reference data:")
print("  Access pgAdmin at http://localhost:5050")
print()
