#!/usr/bin/env python3
"""
Test New Drawing Features
Tests mullions, cross-sections, icons, and populated spec tables
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.drawing_engine import ProfessionalDrawingGenerator


def test_slider_window():
    """Test 4-panel slider with mullions"""
    print("=" * 70)
    print("TEST 1: 4-PANEL SLIDER WINDOW")
    print("=" * 70)
    
    generator = ProfessionalDrawingGenerator(output_dir="./drawings")
    
    window_data = {
        'item_number': 'W-SLIDER-001',
        'width_inches': 144,
        'height_inches': 96,
        'window_type': 'SLIDER',
        'frame_series': 'Series 6000',
        'swing_direction': 'N/A',
        'glass_type': 'Low-E Tempered',
        'frame_color': 'Bronze',
        'screen': 'Retractable',
        'hardware': 'Heavy-Duty Rollers',
        'quantity': 1,
    }
    
    project_data = {
        'project_name': 'Feature Test Project',
        'po_number': 'TEST-NEW-FEATURES',
        'customer_name': 'Test Customer',
    }
    
    output_path = generator.generate_window_drawing(
        window_data,
        project_data,
        output_filename='TEST_Slider_with_Mullions.pdf'
    )
    
    print(f"\n✅ Generated: {output_path}")
    
    # Auto-open PDF
    try:
        import subprocess
        if sys.platform == 'win32':
            os.startfile(output_path)
        elif sys.platform == 'darwin':
            subprocess.call(['open', output_path])
        else:
            subprocess.call(['xdg-open', output_path])
    except Exception as e:
        print(f"Note: Could not auto-open PDF: {e}")


def test_casement_window():
    """Test casement with diagonal swing lines"""
    print("\n" + "=" * 70)
    print("TEST 2: DOUBLE CASEMENT WINDOW")
    print("=" * 70)
    
    generator = ProfessionalDrawingGenerator(output_dir="./drawings")
    
    window_data = {
        'item_number': 'W-CASEMENT-001',
        'width_inches': 60,
        'height_inches': 48,
        'window_type': 'DOUBLE CASEMENT',
        'frame_series': 'Series 6000',
        'swing_direction': 'Out',
        'glass_type': 'Low-E Clear',
        'frame_color': 'White',
        'screen': 'Standard',
        'hardware': 'Premium Hinges',
        'quantity': 2,
    }
    
    project_data = {
        'project_name': 'Feature Test Project',
        'po_number': 'TEST-NEW-FEATURES',
        'customer_name': 'Test Customer',
    }
    
    output_path = generator.generate_window_drawing(
        window_data,
        project_data,
        output_filename='TEST_Casement_with_Swing.pdf'
    )
    
    print(f"\n✅ Generated: {output_path}")
    
    # Auto-open PDF
    try:
        if sys.platform == 'win32':
            os.startfile(output_path)
    except:
        pass


def test_fixed_window():
    """Test fixed window with F. indicator"""
    print("\n" + "=" * 70)
    print("TEST 3: FIXED WINDOW")
    print("=" * 70)
    
    generator = ProfessionalDrawingGenerator(output_dir="./drawings")
    
    window_data = {
        'item_number': 'W-FIXED-001',
        'width_inches': 48,
        'height_inches': 36,
        'window_type': 'FIXED',
        'frame_series': 'Series 6000',
        'swing_direction': 'N/A',
        'glass_type': 'Low-E Argon',
        'frame_color': 'Black',
        'screen': 'None',
        'hardware': 'N/A',
        'quantity': 3,
    }
    
    project_data = {
        'project_name': 'Feature Test Project',
        'po_number': 'TEST-NEW-FEATURES',
        'customer_name': 'Test Customer',
    }
    
    output_path = generator.generate_window_drawing(
        window_data,
        project_data,
        output_filename='TEST_Fixed_with_Indicator.pdf'
    )
    
    print(f"\n✅ Generated: {output_path}")
    
    # Auto-open PDF
    try:
        if sys.platform == 'win32':
            os.startfile(output_path)
    except:
        pass


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("TESTING NEW DRAWING FEATURES")
    print("=" * 70)
    print("\nFeatures being tested:")
    print("  ✓ Mullion grid lines (sliders)")
    print("  ✓ Panel indicators (F. for Fixed)")
    print("  ✓ Swing direction lines (casements)")
    print("  ✓ Cross-section views")
    print("  ✓ Operation type icons")
    print("  ✓ Populated specification tables")
    print()
    
    test_slider_window()
    test_casement_window()
    test_fixed_window()
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 70)
    print("\nCheck the ./drawings/ folder for:")
    print("  • TEST_Slider_with_Mullions.pdf")
    print("  • TEST_Casement_with_Swing.pdf")
    print("  • TEST_Fixed_with_Indicator.pdf")
    print()
