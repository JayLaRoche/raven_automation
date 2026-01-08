#!/usr/bin/env python3
"""
Phase 1 Test Script
Generate sample professional window drawing with Phase 1 features
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.drawing_engine import ProfessionalDrawingGenerator
from datetime import datetime


def test_phase_1_window():
    """Test Phase 1: Generate professional window drawing"""
    
    print("=" * 70)
    print("PHASE 1: PROFESSIONAL DRAWING GENERATOR TEST")
    print("=" * 70)
    print()
    
    # Test window specification
    window_data = {
        'item_number': 'W-001',
        'width_inches': 72,
        'height_inches': 60,
        'window_type': 'Double Casement',
        'frame_series': 'Series 6000',
        'swing_direction': 'Out Both',
        'glass_type': 'Low-E Tempered',
        'frame_color': 'White',
        'quantity': 2
    }
    
    # Test project data
    project_data = {
        'po_number': 'PHASE1-TEST',
        'project_name': 'Phase 1 Sample Project',
        'customer_name': 'Demo Customer'
    }
    
    print("[Test Data]")
    print(f"  Window: {window_data['item_number']}")
    print(f"  Size: {window_data['width_inches']}\" x {window_data['height_inches']}\"")
    print(f"  Type: {window_data['window_type']}")
    print(f"  Project: {project_data['po_number']}")
    print()
    
    try:
        print("[Generating Drawing...]")
        generator = ProfessionalDrawingGenerator(output_dir='./drawings')
        
        output_file = generator.generate_window_drawing(
            window_data,
            project_data,
            output_filename=f"{project_data['po_number']}_W-001_ELEV_Phase1.pdf"
        )
        
        print(f"  ✓ Drawing generated successfully")
        print(f"  ✓ Location: {os.path.abspath(output_file)}")
        print()
        
        # Check file size
        file_size = os.path.getsize(output_file) / 1024
        print(f"[Result]")
        print(f"  File: {os.path.basename(output_file)}")
        print(f"  Size: {file_size:.1f} KB")
        print()
        
        return output_file
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_phase_1_door():
    """Test Phase 1: Generate professional door drawing"""
    
    print("=" * 70)
    print("PHASE 1: DOOR DRAWING TEST")
    print("=" * 70)
    print()
    
    # Test door specification
    door_data = {
        'item_number': 'D-001',
        'width_inches': 36,
        'height_inches': 84,
        'panel_type': 'Hinged Door',
        'frame_series': 'Series 65',
        'swing_direction': 'Right Out',
        'glass_type': 'Tempered',
        'frame_color': 'Anodized Bronze',
        'quantity': 1
    }
    
    # Test project data
    project_data = {
        'po_number': 'PHASE1-TEST',
        'project_name': 'Phase 1 Sample Project',
        'customer_name': 'Demo Customer'
    }
    
    print("[Test Data]")
    print(f"  Door: {door_data['item_number']}")
    print(f"  Size: {door_data['width_inches']}\" x {door_data['height_inches']}\"")
    print(f"  Type: {door_data['panel_type']}")
    print()
    
    try:
        print("[Generating Drawing...]")
        generator = ProfessionalDrawingGenerator(output_dir='./drawings')
        
        output_file = generator.generate_door_drawing(
            door_data,
            project_data,
            output_filename=f"{project_data['po_number']}_D-001_ELEV_Phase1.pdf"
        )
        
        print(f"  ✓ Drawing generated successfully")
        print(f"  ✓ Location: {os.path.abspath(output_file)}")
        print()
        
        # Check file size
        file_size = os.path.getsize(output_file) / 1024
        print(f"[Result]")
        print(f"  File: {os.path.basename(output_file)}")
        print(f"  Size: {file_size:.1f} KB")
        print()
        
        return output_file
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all Phase 1 tests"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PROFESSIONAL DRAWING GENERATOR" + " " * 22 + "║")
    print("║" + " " * 20 + "PHASE 1 IMPLEMENTATION TEST" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Test 1: Window drawing
    window_file = test_phase_1_window()
    
    print()
    
    # Test 2: Door drawing
    door_file = test_phase_1_door()
    
    print()
    print("=" * 70)
    print("PHASE 1 TEST SUMMARY")
    print("=" * 70)
    print()
    
    if window_file:
        print("✓ Window drawing generated")
    else:
        print("✗ Window drawing failed")
    
    if door_file:
        print("✓ Door drawing generated")
    else:
        print("✗ Door drawing failed")
    
    print()
    print("=" * 70)
    print("PHASE 1 FEATURES IMPLEMENTED:")
    print("=" * 70)
    print("""
    ✓ 3-column layout (30% / 45% / 25%)
    ✓ 8-zone GridSpec layout system
    ✓ Left column: Specification tables
    ✓ Center column: Elevation view with CAD dimensions
    ✓ Right column: Company header, title, project info
    ✓ CAD-style dimension lines with arrows
    ✓ Specification tables (dimensions, materials)
    ✓ Company header block
    ✓ Drawing title block
    ✓ Project information table
    ✓ Revision block
    """)
    
    print()
    print("=" * 70)
    print("PHASE 2 FEATURES TO ADD NEXT:")
    print("=" * 70)
    print("""
    1. Cross-section detail generation (frame cross-sections)
    2. Multi-pane grid drawings (muntins, grates)
    3. Hardware specifications and details
    4. Thermal break visualization
    5. Installation notes and callouts
    6. Multiple views (plan, section, detail)
    7. Material schedules
    8. Paint/finish schedules
    """)
    
    print()


if __name__ == '__main__':
    main()
