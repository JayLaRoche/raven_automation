#!/usr/bin/env python3
"""
CAD Drawing Generator - Quick Start Guide
Ready-to-run examples for testing the system
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.services.cad_drawing_generator import generate_cad_drawing
from app.services.cad_data_transformer import CADDataTransformer


def open_pdf(file_path):
    """
    Open a PDF file with the default viewer
    
    Args:
        file_path: Path to the PDF file
    """
    try:
        if sys.platform == 'win32':
            os.startfile(str(file_path))
        elif sys.platform == 'darwin':
            os.system(f'open "{file_path}"')
        else:
            os.system(f'xdg-open "{file_path}"')
    except Exception as e:
        print(f"Note: Could not open PDF automatically: {e}")


def example_1_basic_window():
    """
    Example 1: Generate a simple fixed window drawing
    This demonstrates the most basic use case
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Fixed Window (72\" × 48\")")
    print("="*70)
    
    # Window specification
    window_data = {
        'item_id': 'W101',
        'room': 'Master Bedroom',
        'width_inches': 72.0,
        'height_inches': 48.0,
        'series': '80',
        'frame_color': 'Black',
        'glass': 'Clear - 1/2" Low-E',
        'screen': 'No Screen',
        'hardware': 'Standard',
        'quantity': 1,
        'config': {
            'type': 'FIXED',
            'panels': 1
        }
    }
    
    # Generate PDF
    pdf_bytes = generate_cad_drawing(window_data)
    
    # Save to file
    output_path = backend_dir / 'example_output' / 'W101_fixed.pdf'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print(f"   Dimensions: {window_data['width_inches']}\" × {window_data['height_inches']}\"")
    print(f"   Series: {window_data['series']}")
    print(f"   Opening PDF...")
    open_pdf(output_path)
    
    return output_path


def example_2_casement_window():
    """
    Example 2: Double casement window
    Shows how the system handles multiple-panel windows
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Double Casement Window (36\" × 48\")")
    print("="*70)
    
    window_data = {
        'item_id': 'W102',
        'room': 'Kitchen',
        'width_inches': 36.0,
        'height_inches': 48.0,
        'series': '86',
        'frame_color': 'Bronze',
        'glass': 'Clear - 1/2" Low-E',
        'screen': 'Retractable Screen',
        'hardware': 'Casement Hinges with Screen',
        'quantity': 2,
        'config': {
            'type': 'CASEMENT',
            'panels': 2,
            'swing_direction': 'Left/Right'
        }
    }
    
    pdf_bytes = generate_cad_drawing(window_data)
    
    output_path = backend_dir / 'example_output' / 'W102_casement.pdf'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print(f"   Configuration: {window_data['config']['type']} ({window_data['config']['panels']} panels)")
    print(f"   Series: {window_data['series']}")
    
    return output_path


def example_3_sliding_door():
    """
    Example 3: 4-panel sliding patio door
    Demonstrates the largest frame series (135) and multi-panel configuration
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: 4-Panel Sliding Patio Door (144\" × 96\")")
    print("="*70)
    
    door_data = {
        'item_id': 'D201',
        'room': 'Patio/Deck',
        'width_inches': 144.0,
        'height_inches': 96.0,
        'series': '135',
        'frame_color': 'Anodized Aluminum',
        'glass': 'Tempered - 3/8" Low-E',
        'screen': 'Sliding Screen',
        'hardware': 'Heavy-Duty Sliding Rollers',
        'quantity': 1,
        'config': {
            'type': 'SLIDER',
            'panels': 4,
            'swing_direction': 'N/A'
        }
    }
    
    pdf_bytes = generate_cad_drawing(door_data)
    
    output_path = backend_dir / 'example_output' / 'D201_slider.pdf'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print(f"   Configuration: {door_data['config']['type']} ({door_data['config']['panels']} panels)")
    print(f"   Series: {door_data['series']}")
    print(f"   Opening PDF...")
    open_pdf(output_path)
    
    return output_path


def example_4_with_metadata():
    """
    Example 4: Window with complete project metadata
    Shows how project-level information is displayed
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Window with Project Metadata")
    print("="*70)
    
    window_data = {
        'item_id': 'W103',
        'room': 'Living Room',
        'width_inches': 60.0,
        'height_inches': 54.0,
        'series': '80',
        'frame_color': 'White',
        'glass': 'Clear - Insulated Low-E',
        'screen': 'Fixed Screen',
        'hardware': 'Standard Hardware',
        'quantity': 3,
        'config': {
            'type': 'FIXED',
            'panels': 1
        },
        # Project metadata
        'salesman': 'John Smith',
        'designer': 'Jane Doe',
        'po_number': 'PO-2024-0142',
        'customer_name': 'Smith Residence',
        'date': '2024-01-20',
        'serial': 'SN-2024-0142-01'
    }
    
    pdf_bytes = generate_cad_drawing(window_data)
    
    output_path = backend_dir / 'example_output' / 'W103_with_metadata.pdf'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    
    print(f"✅ Generated: {output_path}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print(f"   Project: {window_data['po_number']}")
    print(f"   Customer: {window_data['customer_name']}")
    print(f"   Salesman: {window_data['salesman']}")
    print(f"   Designer: {window_data['designer']}")
    print(f"   Opening PDF...")
    open_pdf(output_path)
    
    return output_path


def example_5_batch_generation():
    """
    Example 5: Batch generate multiple drawings
    Demonstrates how to generate drawings for multiple items
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Batch Generation (3 items)")
    print("="*70)
    
    items = [
        {
            'item_id': 'W201',
            'width_inches': 48.0,
            'height_inches': 36.0,
            'series': '80',
            'frame_color': 'Black',
            'glass': 'Clear',
            'quantity': 1,
            'config': {'type': 'FIXED', 'panels': 1}
        },
        {
            'item_id': 'W202',
            'width_inches': 36.0,
            'height_inches': 48.0,
            'series': '86',
            'frame_color': 'Bronze',
            'glass': 'Low-E',
            'quantity': 2,
            'config': {'type': 'CASEMENT', 'panels': 2, 'swing_direction': 'Left/Right'}
        },
        {
            'item_id': 'D201',
            'width_inches': 120.0,
            'height_inches': 84.0,
            'series': '135',
            'frame_color': 'Aluminum',
            'glass': 'Tempered',
            'quantity': 1,
            'config': {'type': 'SLIDER', 'panels': 3, 'swing_direction': 'N/A'}
        }
    ]
    
    output_dir = backend_dir / 'example_output' / 'batch'
    output_dir.mkdir(exist_ok=True, parents=True)
    
    total_bytes = 0
    
    for item_data in items:
        pdf_bytes = generate_cad_drawing(item_data)
        
        filename = f"{item_data['item_id']}.pdf"
        output_path = output_dir / filename
        output_path.write_bytes(pdf_bytes)
        
        total_bytes += len(pdf_bytes)
        print(f"  ✓ {filename:<20} ({len(pdf_bytes):>7,} bytes)")
    
    print(f"\n✅ Batch complete!")
    print(f"   Total items: {len(items)}")
    print(f"   Total size: {total_bytes:,} bytes")
    print(f"   Output directory: {output_dir}")
    print(f"   Opening output folder...")
    
    # Open the output directory
    try:
        if sys.platform == 'win32':
            os.startfile(str(output_dir))
        elif sys.platform == 'darwin':
            os.system(f'open "{output_dir}"')
        else:
            os.system(f'xdg-open "{output_dir}"')
    except Exception as e:
        print(f"   Note: Could not open folder: {e}")
    
    return output_dir


def example_6_data_transformer():
    """
    Example 6: Data transformation demonstration
    Shows how the transformer converts database models to CAD data
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Data Transformation (Mock Database Model)")
    print("="*70)
    
    # Simulate a database model
    class MockWindow:
        item_number = 'W-DB-001'
        room = 'Office'
        width_inches = 48.0
        height_inches = 42.0
        window_type = 'LEFT CASEMENT'
        frame_series = 'Series 86'
        swing_direction = 'Left'
        glass_type = 'Low-E Clear'
        frame_color = 'Bronze'
        quantity = 1
        screen_type = 'Retractable'
        hardware_spec = 'Premium Hinges'
    
    class MockProject:
        po_number = 'PO-2024-9999'
        customer_name = 'Database Test Corp'
        salesman = 'Test Salesman'
        designer = 'Test Designer'
    
    # Transform the mock model
    window = MockWindow()
    project = MockProject()
    
    cad_data = CADDataTransformer.window_to_cad_data(window, project)
    
    print("\nInput (Database Model):")
    print(f"  Window Type: {window.window_type}")
    print(f"  Frame Series: {window.frame_series}")
    print(f"  Dimensions: {window.width_inches}\" × {window.height_inches}\"")
    
    print("\nTransformed Output (CAD Data):")
    print(f"  Item ID: {cad_data['item_id']}")
    print(f"  Dimensions: {cad_data['width_mm']:.1f}mm × {cad_data['height_mm']:.1f}mm")
    print(f"  Series: {cad_data['series']}")
    print(f"  Configuration: {cad_data['config']['type']} ({cad_data['config']['panels']} panel(s))")
    print(f"  Swing Direction: {cad_data['config']['swing_direction']}")
    
    # Generate drawing from transformed data
    pdf_bytes = generate_cad_drawing(cad_data)
    
    output_path = backend_dir / 'example_output' / 'W_transformed.pdf'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_bytes(pdf_bytes)
    
    print(f"\n✅ Generated from transformed data: {output_path}")
    print(f"   Size: {len(pdf_bytes):,} bytes")
    print(f"   Opening PDF...")
    open_pdf(output_path)
    
    return output_path, cad_data


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("CAD DRAWING GENERATOR - QUICK START EXAMPLES")
    print("="*70)
    
    try:
        # Run examples
        example_1_basic_window()
        example_2_casement_window()
        example_3_sliding_door()
        example_4_with_metadata()
        example_5_batch_generation()
        example_6_data_transformer()
        
        # Summary
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        output_dir = backend_dir / 'example_output'
        print(f"\n📁 Output Files Location: {output_dir}")
        print(f"\n📋 Generated Files:")
        
        if output_dir.exists():
            pdf_files = list(output_dir.rglob('*.pdf'))
            total_size = sum(f.stat().st_size for f in pdf_files)
            
            for pdf_file in sorted(pdf_files):
                rel_path = pdf_file.relative_to(output_dir)
                size = pdf_file.stat().st_size
                print(f"   • {str(rel_path):<35} ({size:>7,} bytes)")
            
            print(f"\n   Total: {len(pdf_files)} PDF files ({total_size:,} bytes)")
            
            # Open the first PDF
            if pdf_files:
                first_pdf = sorted(pdf_files)[0]
                print(f"\n🔍 Opening first PDF: {first_pdf.name}")
                open_pdf(first_pdf)
        
        print("\n📖 Next Steps:")
        print("   1. Review generated PDFs in example_output/")
        print("   2. Compare with reference PDFs (W102, W100a/b, D200)")
        print("   3. Integrate into FastAPI app (see INTEGRATION_GUIDE.md)")
        print("   4. Test API endpoints (see CAD_DRAWING_GUIDE.md)")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
