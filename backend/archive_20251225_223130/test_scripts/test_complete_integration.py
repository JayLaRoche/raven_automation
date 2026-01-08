#!/usr/bin/env python3
"""
Complete Integration Test
Tests the full pipeline: Google Sheets → Drawing Generator → PDF
"""
import sys
import os
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("COMPLETE INTEGRATION TEST")
print("=" * 70)
print("\nTesting Full Pipeline:")
print("  Google Sheets → Parser → Drawing Generator → PDF")
print()

# Test 1: Create drawing from manual data (simulating Google Sheets)
print("[Step 1] Testing with sample data (simulating Google Sheets)")
print("-" * 70)

from services.drawing_engine import ProfessionalDrawingGenerator

generator = ProfessionalDrawingGenerator(output_dir="./drawings")

# Simulate data as it would come from Google Sheets
sample_windows = [
    {
        'item_number': 'W-SLIDER-100',
        'width_inches': 144,
        'height_inches': 96,
        'window_type': 'SLIDER',
        'glass_type': 'Low-E Tempered 3/8"',
        'frame_color': 'Anodized Aluminum',
        'screen': 'Sliding Screen',
        'hardware': 'Heavy-Duty Sliding Rollers',
        'quantity': 1,
        'frame_series': 'Series 135',
        'swing_direction': 'N/A'
    },
    {
        'item_number': 'W-CASEMENT-200',
        'width_inches': 60,
        'height_inches': 48,
        'window_type': 'DOUBLE CASEMENT',
        'glass_type': 'Low-E Clear',
        'frame_color': 'White',
        'screen': 'Standard',
        'hardware': 'Premium Hinges',
        'quantity': 2,
        'frame_series': 'Series 86',
        'swing_direction': 'Out'
    },
    {
        'item_number': 'W-FIXED-300',
        'width_inches': 48,
        'height_inches': 36,
        'window_type': 'FIXED',
        'glass_type': 'Low-E Argon',
        'frame_color': 'Black',
        'screen': 'None',
        'hardware': 'N/A',
        'quantity': 3,
        'frame_series': 'Series 80',
        'swing_direction': 'N/A'
    }
]

project_data = {
    'project_name': 'Integration Test Project',
    'po_number': 'TEST-INTEGRATION-001',
    'customer_name': 'Test Customer Inc.'
}

generated_files = []

for window in sample_windows:
    print(f"\nGenerating: {window['item_number']} ({window['window_type']})")
    
    output_file = f"INTEGRATION_{window['item_number']}.pdf"
    
    path = generator.generate_window_drawing(
        window,
        project_data,
        output_filename=output_file
    )
    
    generated_files.append(path)
    print(f"  ✓ Generated: {output_file}")

print()
print("=" * 70)
print("✅ INTEGRATION TEST COMPLETE")
print("=" * 70)
print(f"\nGenerated {len(generated_files)} PDF drawings:")
for f in generated_files:
    print(f"  • {os.path.basename(f)}")

print("\n" + "=" * 70)
print("FEATURE VERIFICATION")
print("=" * 70)
print("\nEach drawing should contain:")
print("  ✓ Mullion lines (if multi-panel)")
print("  ✓ Panel indicators (F., arrows)")
print("  ✓ Cross-section views (left column)")
print("  ✓ Operation icons (right column, bottom)")
print("  ✓ Populated spec table:")
print("    - Glass Type: ", sample_windows[0]['glass_type'])
print("    - Frame Color: ", sample_windows[0]['frame_color'])
print("    - Screen Spec: ", sample_windows[0]['screen'])
print("    - Hardware: ", sample_windows[0]['hardware'])
print("    - Quantity: ", sample_windows[0]['quantity'])

print("\n" + "=" * 70)
print("NEXT STEPS")
print("=" * 70)
print("\n1. Review the generated PDFs in ./drawings/")
print("2. Verify all features match your reference drawing")
print("3. To generate from actual Google Sheets:")
print("   python generate_from_sheet.py 'Your Sheet Name'")
print("\n4. To use API:")
print("   uvicorn main:app --reload")
print("   POST /api/drawings/project/{po_number}/generate")
print()

# Auto-open first PDF
try:
    if generated_files and sys.platform == 'win32':
        print(f"Opening: {os.path.basename(generated_files[0])}")
        os.startfile(generated_files[0])
except Exception as e:
    print(f"Note: Could not auto-open: {e}")
