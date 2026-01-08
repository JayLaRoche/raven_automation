"""
Test CAD drawing generator with sample data
Quick verification that the system generates PDFs correctly
"""

import os
from pathlib import Path
from app.services.cad_drawing_generator import generate_cad_drawing
from app.services.cad_data_transformer import CADDataTransformer


def test_single_fixed_window():
    """Generate a test drawing for a fixed window"""
    test_data = {
        'item_id': 'W102',
        'room': 'Living Room',
        'width_inches': 72.0,
        'height_inches': 48.0,
        'width_mm': 1828.8,
        'height_mm': 1219.2,
        'series': '80',
        'frame_color': 'Black',
        'glass': 'Clear - 1/2" Low-E',
        'screen': 'No Screen',
        'hardware': 'Standard',
        'quantity': 1,
        'salesman': 'John Smith',
        'designer': 'Jane Doe',
        'po_number': 'PO-2024-001',
        'customer_name': 'Acme Corp',
        'date': '2024-01-15',
        'config': {
            'type': 'FIXED',
            'panels': 1,
            'swing_direction': 'N/A'
        }
    }
    
    # Generate PDF
    pdf_bytes = generate_cad_drawing(test_data)
    
    # Save to test output directory
    output_dir = Path('test_output')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'test_W102_fixed.pdf'
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"✓ Generated test drawing: {output_file}")
    print(f"  File size: {len(pdf_bytes)} bytes")
    return output_file


def test_double_casement_window():
    """Generate a test drawing for a double casement window"""
    test_data = {
        'item_id': 'W100a',
        'room': 'Bedroom',
        'width_inches': 36.0,
        'height_inches': 48.0,
        'width_mm': 914.4,
        'height_mm': 1219.2,
        'series': '86',
        'frame_color': 'Bronze',
        'glass': 'Clear - 1/2" Low-E',
        'screen': 'Retractable Screen',
        'hardware': 'Casement Hinges',
        'quantity': 2,
        'salesman': 'Mike Johnson',
        'designer': 'Sarah Williams',
        'po_number': 'PO-2024-002',
        'customer_name': 'Smith Residence',
        'date': '2024-01-16',
        'config': {
            'type': 'CASEMENT',
            'panels': 2,
            'swing_direction': 'Left/Right'
        }
    }
    
    pdf_bytes = generate_cad_drawing(test_data)
    
    output_dir = Path('test_output')
    output_file = output_dir / 'test_W100a_casement.pdf'
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"✓ Generated test drawing: {output_file}")
    print(f"  File size: {len(pdf_bytes)} bytes")
    return output_file


def test_sliding_door():
    """Generate a test drawing for a sliding door"""
    test_data = {
        'item_id': 'D200',
        'room': 'Patio',
        'width_inches': 144.0,
        'height_inches': 96.0,
        'width_mm': 3657.6,
        'height_mm': 2438.4,
        'series': '135',
        'frame_color': 'Anodized Aluminum',
        'glass': 'Tempered - 3/8" Low-E',
        'screen': 'Sliding Screen',
        'hardware': 'Sliding Rollers',
        'quantity': 1,
        'salesman': 'Tom Brown',
        'designer': 'David Lee',
        'po_number': 'PO-2024-003',
        'customer_name': 'Jones Residence',
        'date': '2024-01-17',
        'config': {
            'type': 'SLIDER',
            'panels': 4,
            'swing_direction': 'N/A'
        }
    }
    
    pdf_bytes = generate_cad_drawing(test_data)
    
    output_dir = Path('test_output')
    output_file = output_dir / 'test_D200_slider.pdf'
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"✓ Generated test drawing: {output_file}")
    print(f"  File size: {len(pdf_bytes)} bytes")
    return output_file


def test_data_transformer():
    """Test the data transformer with sample models"""
    # Create a mock window object (would be from database)
    class MockWindow:
        item_number = 'W-001'
        room = 'Kitchen'
        width_inches = 48.0
        height_inches = 36.0
        window_type = 'FIXED'
        frame_series = 'Series 80'
        swing_direction = 'N/A'
        glass_type = 'Clear'
        frame_color = 'Black'
        quantity = 1
        screen_type = 'No Screen'
        hardware_spec = 'Standard'
    
    # Create a mock project object
    class MockProject:
        po_number = 'PO-2024-TEST'
        customer_name = 'Test Customer'
        salesman = 'Test Sales'
        designer = 'Test Designer'
    
    window = MockWindow()
    project = MockProject()
    
    # Transform to CAD data
    cad_data = CADDataTransformer.window_to_cad_data(window, project)
    
    print(f"\n✓ Data transformation successful")
    print(f"  Item ID: {cad_data['item_id']}")
    print(f"  Dimensions: {cad_data['width_inches']}\" x {cad_data['height_inches']}\"")
    print(f"  Frame Series: {cad_data['series']}")
    print(f"  Config: {cad_data['config']}")
    
    return cad_data


if __name__ == '__main__':
    print("=" * 60)
    print("CAD Drawing Generator Test Suite")
    print("=" * 60)
    
    # Test data transformation
    print("\n[1] Testing Data Transformer...")
    test_data_transformer()
    
    # Generate test drawings
    print("\n[2] Generating Test Drawings...")
    test_single_fixed_window()
    test_double_casement_window()
    test_sliding_door()
    
    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)
