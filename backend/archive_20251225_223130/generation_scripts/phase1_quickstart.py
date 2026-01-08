#!/usr/bin/env python3
"""
PHASE 1 QUICK START GUIDE
Get professional drawings in 30 seconds
"""

# ==============================================================================
# OPTION 1: SIMPLE GENERATION (Copy & Paste)
# ==============================================================================

def quick_demo():
    """Generate a professional drawing in 10 lines"""
    from services.drawing_engine import ProfessionalDrawingGenerator
    
    gen = ProfessionalDrawingGenerator('./drawings')
    
    window = {
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
    
    project = {
        'po_number': 'DEMO-001',
        'project_name': 'Sample Project',
        'customer_name': 'John Doe'
    }
    
    pdf = gen.generate_window_drawing(window, project)
    print(f"✓ Created: {pdf}")
    return pdf


# ==============================================================================
# OPTION 2: FROM GOOGLE SHEETS DATA (WITH SHEET SELECTION)
# ==============================================================================

def from_google_sheets(sheet_name: str = None):
    """Generate drawings directly from Google Sheets (optionally from specific sheet)"""
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_engine import ProfessionalDrawingGenerator
    
    # Get data from Google Sheets
    sheets = GoogleSheetsService()
    
    # If no sheet specified, list available sheets
    if sheet_name is None:
        available = sheets.get_available_sheets()
        print("Available sheets:")
        for i, s in enumerate(available, 1):
            print(f"  {i}. {s}")
        return
    
    project_data = sheets.parse_project_data(sheet_name=sheet_name)
    
    # Generate drawings
    gen = ProfessionalDrawingGenerator('./drawings')
    
    for window in project_data.get('windows', []):
        pdf = gen.generate_window_drawing(window, project_data['metadata'])
        print(f"✓ {pdf}")
    
    for door in project_data.get('doors', []):
        pdf = gen.generate_door_drawing(door, project_data['metadata'])
        print(f"✓ {pdf}")


# ==============================================================================
# OPTION 3: BATCH GENERATION
# ==============================================================================

def batch_generate(po_number: str):
    """Generate all windows and doors for a project"""
    from services.google_sheets_services import GoogleSheetsService
    from services.drawing_engine import ProfessionalDrawingGenerator
    
    sheets = GoogleSheetsService()
    project_data = sheets.parse_project_data()
    
    generator = ProfessionalDrawingGenerator('./drawings')
    generated_files = []
    
    # Windows
    for window in project_data.get('windows', []):
        try:
            pdf = generator.generate_window_drawing(
                window,
                project_data['metadata']
            )
            generated_files.append(pdf)
            print(f"✓ Window: {window['item_number']}")
        except Exception as e:
            print(f"✗ Window {window['item_number']}: {e}")
    
    # Doors
    for door in project_data.get('doors', []):
        try:
            pdf = generator.generate_door_drawing(
                door,
                project_data['metadata']
            )
            generated_files.append(pdf)
            print(f"✓ Door: {door['item_number']}")
        except Exception as e:
            print(f"✗ Door {door['item_number']}: {e}")
    
    print(f"\nGenerated {len(generated_files)} drawings")
    return generated_files


# ==============================================================================
# OPTION 4: WITH CUSTOM STYLING
# ==============================================================================

def custom_styling():
    """Example with custom output filename"""
    from services.drawing_engine import ProfessionalDrawingGenerator
    
    gen = ProfessionalDrawingGenerator('./drawings')
    
    window = {
        'item_number': 'W-CUSTOM',
        'width_inches': 36,
        'height_inches': 48,
        'window_type': 'Single Hung',
        'frame_series': 'Series 4000',
        'swing_direction': 'Vertical',
        'glass_type': 'Standard',
        'frame_color': 'Bronze',
        'quantity': 1
    }
    
    project = {
        'po_number': 'CUSTOM-001',
        'project_name': 'Custom Renovation',
        'customer_name': 'Jane Smith'
    }
    
    pdf = gen.generate_window_drawing(
        window,
        project,
        output_filename="CUSTOM-DRAWING_W-CUSTOM.pdf"
    )
    
    return pdf


# ==============================================================================
# STEP-BY-STEP: UNDERSTANDING THE OUTPUT
# ==============================================================================

"""
GENERATED PDF STRUCTURE:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌──────────────┐  ┌─────────────────────┐  ┌────────────┐ │
│  │              │  │                     │  │ RAVEN      │ │
│  │  DIMENSIONS  │  │                     │  │ CUSTOM     │ │
│  │              │  │   ELEVATION VIEW    │  │ GLASS      │ │
│  ├──────────────┤  │   with CAD Dims     │  ├────────────┤ │
│  │              │  │                     │  │ WINDOW     │ │
│  │ MATERIALS    │  │                     │  │ W-001      │ │
│  │ & SPECS      │  │                     │  │ ELEVATION  │ │
│  │              │  │                     │  ├────────────┤ │
│  │              │  │                     │  │ PROJECT    │ │
│  │              │  │                     │  │ INFO       │ │
│  │              │  │                     │  │            │ │
│  │              │  │                     │  ├────────────┤ │
│  │              │  │                     │  │ REVISIONS  │ │
│  └──────────────┘  └─────────────────────┘  └────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘

LEFT COLUMN (30%):
- Product dimensions (width, height, type, quantity)
- Material specifications (frame, glass, color, swing direction)

CENTER COLUMN (45%):
- Main elevation drawing of window/door
- CAD-style dimension annotations
- Extension lines and arrows
- Professional technical drawing format

RIGHT COLUMN (25%):
- Company header (RAVEN CUSTOM GLASS)
- Drawing title (product type + item number)
- Project information (PO, customer, date, scale)
- Revision tracking block
"""


# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

"""
PROBLEM: ModuleNotFoundError: No module named 'services.drawing_engine'

SOLUTION:
1. Make sure you're in the backend directory
2. Check that drawing_engine folder exists:
   backend/services/drawing_engine/
3. Check that __init__.py exists in drawing_engine folder

PROBLEM: PDF file is empty or corrupted

SOLUTION:
1. Check matplotlib is installed: pip install matplotlib
2. Check reportlab is installed: pip install reportlab
3. Try regenerating the drawing
4. Check disk space available

PROBLEM: Dimensions not showing up

SOLUTION:
1. Check window/door size is reasonable (not too small)
2. Verify scale parameter is appropriate
3. Try with test data: W-001 (72"x60")

PROBLEM: Text is too small or too large

SOLUTION:
1. Adjust font sizes in components.py
2. Edit fontsize parameters in draw_* methods
3. Modify text_offset values in dimensions.py
"""


# ==============================================================================
# COMMAND LINE USAGE
# ==============================================================================

if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("PHASE 1: PROFESSIONAL DRAWING GENERATOR - QUICK START")
    print("=" * 70)
    print()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'demo':
            print("[Running Demo]")
            quick_demo()
        elif command == 'batch':
            po = sys.argv[2] if len(sys.argv) > 2 else 'DEMO'
            print(f"[Batch Generating for {po}]")
            batch_generate(po)
        elif command == 'custom':
            print("[Custom Styling Example]")
            custom_styling()
        elif command == 'sheets':
            print("[Generating from Google Sheets]")
            from_google_sheets()
        else:
            print("Unknown command")
    else:
        print("USAGE:")
        print("  python phase1_quickstart.py demo      - Run quick demo")
        print("  python phase1_quickstart.py batch PO  - Generate all drawings")
        print("  python phase1_quickstart.py custom    - Custom styling example")
        print("  python phase1_quickstart.py sheets    - From Google Sheets")
        print()
        print("Or import in your code:")
        print("  from services.drawing_engine import ProfessionalDrawingGenerator")
        print("  gen = ProfessionalDrawingGenerator('./drawings')")
        print("  pdf = gen.generate_window_drawing(window_data, project_data)")
