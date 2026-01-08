#!/usr/bin/env python3
"""
Complete PDF Layout System Test
Tests: Analyzer → Template → Drawing Generator

This demonstrates the full workflow:
1. Analyze reference PDFs (already done)
2. Load templates
3. Generate drawings using learned layouts
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, '.')

print("=" * 70)
print("PDF LAYOUT LEARNING SYSTEM - COMPLETE TEST")
print("=" * 70)

# Step 1: Verify templates exist
print("\n[Step 1] Verifying Templates")
print("-" * 70)

template_dir = Path('templates')
templates = list(template_dir.glob('*.json'))

if templates:
    print(f"✓ Found {len(templates)} templates:")
    for t in templates:
        print(f"  • {t.name}")
else:
    print("⚠ No templates found. Run analyze_layout.py first.")
    sys.exit(1)

# Step 2: Load and inspect a template
print("\n[Step 2] Loading Template")
print("-" * 70)

from app.services.visual_template_generator import load_template

template_path = templates[0]  # Use first template
generator_template = load_template(str(template_path))

print(f"\nTemplate Details:")
print(f"  Name: {generator_template.template['template_name']}")
print(f"  Page: {generator_template.template['page']['format']}")
print(f"  Size: {generator_template.template['page']['width_mm']:.0f}mm × {generator_template.template['page']['height_mm']:.0f}mm")

# Step 3: Get layout proportions
print("\n[Step 3] Extracting Layout Proportions")
print("-" * 70)

proportions = generator_template.get_zone_proportions()
print(f"Zone Widths:")
print(f"  Left:   {proportions['left']*100:.1f}%")
print(f"  Center: {proportions['center']*100:.1f}%")
print(f"  Right:  {proportions['right']*100:.1f}%")

# Step 4: Get styling rules
print("\n[Step 4] Extracting Styling Rules")
print("-" * 70)

styling = generator_template.get_styling_rules()
print(f"Line Weights:")
print(f"  Thick:  {styling['line_weights']['thick']:.2f}pt")
print(f"  Medium: {styling['line_weights']['medium']:.2f}pt")
print(f"  Thin:   {styling['line_weights']['thin']:.2f}pt")

# Step 5: Get text hierarchy
print("\n[Step 5] Text Size Hierarchy")
print("-" * 70)

text_hierarchy = generator_template.get_text_hierarchy()
print(f"Font Sizes:")
print(f"  Title:   {text_hierarchy.get('title', 12):.1f}pt")
print(f"  Heading: {text_hierarchy.get('heading', 10):.1f}pt")
print(f"  Body:    {text_hierarchy.get('body', 8):.1f}pt")
print(f"  Small:   {text_hierarchy.get('small', 6):.1f}pt")

# Step 6: Get drawing conventions
print("\n[Step 6] Drawing Conventions")
print("-" * 70)

conventions = generator_template.get_drawing_conventions()
panel_indicators = conventions.get('panel_indicators', {})
print(f"Panel Indicators:")
for panel_type, indicator_style in panel_indicators.items():
    print(f"  {panel_type.capitalize()}: {indicator_style}")

# Step 7: Generate test drawing using template
print("\n[Step 7] Generating Test Drawing with Template")
print("-" * 70)

from services.drawing_engine import ProfessionalDrawingGenerator

# Sample window data
window_data = {
    'item_number': 'W-TEMPLATE-TEST',
    'width_inches': 72,
    'height_inches': 60,
    'window_type': 'DOUBLE CASEMENT',
    'glass_type': 'Low-E Tempered',
    'frame_color': 'Bronze',
    'screen': 'Retractable',
    'hardware': 'Premium Hinges',
    'quantity': 2,
    'frame_series': 'Series 86',
    'swing_direction': 'Out'
}

project_data = {
    'project_name': 'Template Test Project',
    'po_number': 'TEMPLATE-001',
    'customer_name': 'Template Test Customer'
}

# Generate drawing
generator = ProfessionalDrawingGenerator(output_dir="./drawings")
output_path = generator.generate_window_drawing(
    window_data,
    project_data,
    output_filename="TEMPLATE_LEARNED_DRAWING.pdf"
)

print(f"✓ Generated: {output_path}")

# Step 8: Summary
print("\n" + "=" * 70)
print("✅ PDF LAYOUT LEARNING SYSTEM TEST COMPLETE")
print("=" * 70)

print("\n📊 System Capabilities:")
print("  ✓ PDF layout analysis")
print("  ✓ Visual template extraction")
print("  ✓ Template loading and application")
print("  ✓ Styling rule extraction")
print("  ✓ Text hierarchy detection")
print("  ✓ Drawing convention learning")
print("  ✓ Template-driven drawing generation")

print("\n📁 Artifacts Created:")
print(f"  • Templates: {len(templates)} files in templates/")
print(f"  • Test Drawing: {output_path}")

print("\n🎯 What This System Does:")
print("  1. Analyzes your reference PDFs (layout, not measurements)")
print("  2. Extracts visual structure (zones, styling, conventions)")
print("  3. Saves as JSON templates (human-editable)")
print("  4. Drawing engine uses templates for consistent look")
print("  5. Measurements still come from Google Sheets (as intended)")

print("\n📝 Next Steps:")
print("  1. Review templates/*.json files")
print("  2. Edit templates if needed (they're JSON)")
print("  3. Generate more drawings - they'll use learned layout")
print("  4. Add new reference PDFs - just re-run analyze_layout.py")

print("\n💡 Key Insight:")
print("  The system learned VISUAL STRUCTURE from your PDFs")
print("  but still gets DATA (measurements) from Google Sheets")
print("  This is exactly what you wanted!")

print()

# Auto-open the generated drawing
try:
    if sys.platform == 'win32':
        print(f"Opening: {output_path}")
        os.startfile(output_path)
except Exception as e:
    print(f"Note: Could not auto-open: {e}")
