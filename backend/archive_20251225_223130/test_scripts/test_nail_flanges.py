"""
Test script to verify nail flange diagrams in cross-sections
"""
import sys
import os
from datetime import datetime

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.drawing_engine.main import ProfessionalDrawingGenerator

# Test window data
window_data = {
    'item_number': 'W-101',
    'mark': 'A1',
    'quantity': 2,
    'width': 48,
    'height': 60,
    'configuration': 'Slider',
    'operation_type': 'Slider',
    'frame_color': 'White',
    'glass_type': 'Low-E Dual Pane',
    'screen': 'Full Screen',
    'hardware': 'Standard Lock',
    'notes': 'Test window for nail flange diagrams'
}

# Project metadata
project_data = {
    'project_name': 'Nail Flange Test Project',
    'project_number': 'TEST-NF-001',
    'client': 'Quality Control',
    'date': datetime.now().strftime('%Y-%m-%d'),
    'revision': 'A'
}

print("=" * 70)
print("TESTING NAIL FLANGE DIAGRAMS")
print("=" * 70)
print("\nGenerating window drawing with cross-sections...")
print(f"Window: {window_data['configuration']} - {window_data['width']}\" x {window_data['height']}\"")

# Generate the drawing
generator = ProfessionalDrawingGenerator()
output_path = generator.generate_window_drawing(
    window_data,
    project_data,
    output_filename='NAIL_FLANGE_TEST.pdf'
)

print(f"\n✓ Drawing generated: {output_path}")
print("\nCheck the cross-section views for:")
print("  • Red-highlighted nail flanges on vertical section (left/right)")
print("  • Red-highlighted nail flanges on horizontal section (top/bottom)")
print("  • 'Nail Fin' labels")
print("  • 30mm dimension callout")
print("  • INT/EXT orientation labels")
print("\n" + "=" * 70)

# Auto-open the PDF
os.startfile(output_path)
print(f"Opening {output_path}...")
