#!/usr/bin/env python3
"""Test PDF drawing generation"""
import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from services.drawing_generator import get_drawing_generator

print("=" * 70)
print("PDF DRAWING GENERATION TEST")
print("=" * 70)

# Create sample project data
sample_project = {
    "metadata": {
        "po_number": "TEST-001",
        "project_name": "Demo Project - Evergreen Creek",
        "customer_name": "Test Customer",
        "billing_address": "123 Main St, Las Vegas NV",
    },
    "windows": [
        {
            "item_number": "W-001",
            "room": "Living Room",
            "width_inches": 36,
            "height_inches": 48,
            "window_type": "Double Hung",
            "frame_series": "Victory",
            "swing_direction": "Both",
            "quantity": 2,
            "frame_color": "White",
            "glass_type": "Low-E",
            "grids": "6x6",
            "screen": "Yes",
        },
        {
            "item_number": "W-002",
            "room": "Bedroom",
            "width_inches": 30,
            "height_inches": 36,
            "window_type": "Slider",
            "frame_series": "Victory",
            "swing_direction": "Both",
            "quantity": 1,
            "frame_color": "White",
            "glass_type": "Low-E",
            "grids": "None",
            "screen": "Yes",
        }
    ],
    "doors": [
        {
            "item_number": "D-001",
            "room": "Patio",
            "width_inches": 36,
            "height_inches": 84,
            "door_type": "Patio Door",
            "frame_series": "Victory",
            "swing_direction": "Right",
            "quantity": 1,
            "frame_color": "White",
            "glass_type": "Low-E",
            "threshold": "ADA",
        },
        {
            "item_number": "D-002",
            "room": "Entry",
            "width_inches": 32,
            "height_inches": 84,
            "door_type": "Entry Door",
            "frame_series": "Victory",
            "swing_direction": "Right",
            "quantity": 1,
            "frame_color": "White",
            "glass_type": "None",
            "threshold": "Standard",
        }
    ]
}

try:
    print("\n[Initializing Drawing Generator]")
    generator = get_drawing_generator("./drawings")
    print("  ✓ Generator initialized")
    
    print("\n[Generating Drawings]")
    files = generator.generate_project_package(sample_project, "TEST-001")
    
    print(f"\n[Results]")
    print(f"  ✓ Generated {len(files)} PDF drawing(s)")
    for f in files:
        print(f"    - {f}")
    
    print(f"\n{'=' * 70}")
    print("✓ ALL TESTS PASSED - PDF generation is working!")
    print(f"{'=' * 70}\n")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}")
    print(f"  {str(e)}")
    import traceback
    traceback.print_exc()
