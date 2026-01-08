#!/usr/bin/env python3
"""
Test Reference Data Validator
Demonstrates validation with sample data
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.services.reference_data_validator import ReferenceDataValidator

print("=" * 70)
print("REFERENCE DATA VALIDATOR - TEST")
print("=" * 70)
print()

# Initialize validator
db = SessionLocal()
validator = ReferenceDataValidator(db)

# Test Data - Some valid, some invalid
test_windows = [
    {
        'item_number': 'W-001',
        'width': 48,
        'height': 60,
        'configuration': 'Slider 4-Panel',  # Valid
        'frame_series': 'Series 90',        # Valid
        'glass_type': 'Low-E Dual Pane',    # Valid
        'hardware': 'Slider Window Lock',   # Valid
        'frame_color': 'White'              # Valid
    },
    {
        'item_number': 'W-002',
        'width': 36,
        'height': 48,
        'configuration': 'Casement Window', # Invalid (should be 'Single Casement')
        'frame_series': 'Series 85',        # Invalid (should be 86)
        'glass_type': 'Low E Glass',        # Invalid (should be 'Low-E Dual Pane')
        'hardware': 'Lock',                 # Invalid (too generic)
        'frame_color': 'White'              # Valid
    },
    {
        'item_number': 'W-003',
        'width': 72,
        'height': 60,
        'configuration': 'Fixed',           # Valid
        'frame_series': 'Series 80',        # Valid
        'glass_type': 'Tempered',           # Invalid (should be 'Tempered Clear')
        'hardware': 'None',                 # Invalid
        'frame_color': 'Bronze'             # Valid
    }
]

print("[Test 1] Validating Sample Windows")
print("-" * 70)

for i, window in enumerate(test_windows, 1):
    print(f"\nWindow {i}: {window['item_number']}")
    print(f"  Configuration: {window['configuration']}")
    print(f"  Frame Series: {window['frame_series']}")
    print(f"  Glass: {window['glass_type']}")
    print(f"  Hardware: {window['hardware']}")
    print(f"  Color: {window['frame_color']}")
    
    is_valid, errors = validator.validate_window(window)
    
    if is_valid:
        print("  ✅ Valid")
    else:
        print("  ❌ Invalid:")
        for error in errors:
            print(f"     • {error}")

# Test Auto-Correction
print("\n" + "=" * 70)
print("[Test 2] Auto-Correction")
print("-" * 70)

invalid_window = test_windows[1]  # The one with errors
print(f"\nOriginal: {invalid_window['item_number']}")
print(f"  Configuration: {invalid_window['configuration']}")
print(f"  Frame Series: {invalid_window['frame_series']}")
print(f"  Glass: {invalid_window['glass_type']}")
print(f"  Hardware: {invalid_window['hardware']}")

corrected = validator.auto_correct(invalid_window)
print(f"\nCorrected:")
print(f"  Configuration: {corrected['configuration']}")
print(f"  Frame Series: {corrected['frame_series']}")
print(f"  Glass: {corrected['glass_type']}")
print(f"  Hardware: {corrected['hardware']}")

# Validate corrected version
is_valid, errors = validator.validate_window(corrected)
print(f"\n✅ Corrected version is valid: {is_valid}")

# Test Default Values
print("\n" + "=" * 70)
print("[Test 3] Default Values by Configuration")
print("-" * 70)

configurations = ['Slider 4-Panel', 'Single Casement', 'Fixed', 'Sliding Door 2-Panel']
for config in configurations:
    defaults = validator.get_default_values(config)
    print(f"\n{config}:")
    print(f"  Frame Series: {defaults.get('frame_series')}")
    print(f"  Glass Type: {defaults.get('glass_type')}")
    print(f"  Hardware: {defaults.get('hardware', 'N/A')}")
    print(f"  Color: {defaults.get('frame_color')}")

# Show Available Reference Data
print("\n" + "=" * 70)
print("[Test 4] Available Reference Data")
print("-" * 70)

summary = validator.get_reference_summary()

print("\nFrame Series:")
for series in summary['frame_series']:
    print(f"  • {series}")

print("\nConfigurations:")
for config in summary['configurations']:
    print(f"  • {config}")

print("\nGlass Types:")
for glass in summary['glass_types']:
    print(f"  • {glass}")

print("\nFrame Colors:")
for color in summary['colors']:
    print(f"  • {color}")

print("\nHardware (first 10):")
for hardware in summary['hardware'][:10]:
    print(f"  • {hardware}")

db.close()

print("\n" + "=" * 70)
print("VALIDATION TEST COMPLETE")
print("=" * 70)
print()
print("Key Features Demonstrated:")
print("  ✅ Validation against reference tables")
print("  ✅ Auto-correction with closest matches")
print("  ✅ Default value suggestions")
print("  ✅ Reference data lookup")
print()
print("Usage in production:")
print("  1. Validate before generating drawings")
print("  2. Auto-correct invalid values")
print("  3. Suggest defaults for missing data")
print("  4. Ensure drawing accuracy")
print()
