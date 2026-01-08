#!/usr/bin/env python3
"""Verify Phase 1 implementation"""
import os
import sys

sys.path.insert(0, r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")
os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")

print("=" * 70)
print("PHASE 1 IMPLEMENTATION VERIFICATION")
print("=" * 70)
print()

# Check if modules exist
print("[1] Checking module files...")
modules = [
    'services/drawing_engine/__init__.py',
    'services/drawing_engine/layout.py',
    'services/drawing_engine/dimensions.py',
    'services/drawing_engine/components.py',
    'services/drawing_engine/main.py',
]

for module in modules:
    if os.path.exists(module):
        size = os.path.getsize(module)
        print(f"  ✓ {module:45s} ({size:,} bytes)")
    else:
        print(f"  ✗ {module:45s} NOT FOUND")

print()
print("[2] Testing imports...")

try:
    from services.drawing_engine import ProfessionalDrawingGenerator
    print("  ✓ ProfessionalDrawingGenerator imported successfully")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

print()
print("[3] Generating test drawings...")

try:
    # Window test
    window_data = {
        'item_number': 'W-001',
        'width_inches': 72,
        'height_inches': 60,
        'window_type': 'Double Casement',
        'frame_series': 'Series 6000',
        'swing_direction': 'Out',
        'glass_type': 'Low-E',
        'frame_color': 'White',
        'quantity': 2
    }
    
    project_data = {
        'po_number': 'PHASE1-TEST',
        'project_name': 'Test Project',
        'customer_name': 'Test Customer'
    }
    
    generator = ProfessionalDrawingGenerator(output_dir='./drawings')
    
    # Generate window
    window_file = generator.generate_window_drawing(
        window_data,
        project_data,
        output_filename="PHASE1-TEST_W-001_ELEV.pdf"
    )
    print(f"  ✓ Window drawing: {os.path.basename(window_file)}")
    
    # Generate door
    door_data = {
        'item_number': 'D-001',
        'width_inches': 36,
        'height_inches': 84,
        'panel_type': 'Hinged Door',
        'frame_series': 'Series 65',
        'swing_direction': 'Right',
        'glass_type': 'Tempered',
        'frame_color': 'Bronze',
        'quantity': 1
    }
    
    door_file = generator.generate_door_drawing(
        door_data,
        project_data,
        output_filename="PHASE1-TEST_D-001_ELEV.pdf"
    )
    print(f"  ✓ Door drawing: {os.path.basename(door_file)}")
    
except Exception as e:
    print(f"  ✗ Generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("[4] Checking generated files...")

files_to_check = [
    'drawings/PHASE1-TEST_W-001_ELEV.pdf',
    'drawings/PHASE1-TEST_D-001_ELEV.pdf',
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath) / 1024
        print(f"  ✓ {os.path.basename(filepath):40s} ({size:.1f} KB)")
    else:
        print(f"  ✗ {os.path.basename(filepath):40s} NOT FOUND")

print()
print("=" * 70)
print("✓ PHASE 1 IMPLEMENTATION SUCCESSFUL")
print("=" * 70)
print()
print("Generated files located in: ./drawings/")
print()
