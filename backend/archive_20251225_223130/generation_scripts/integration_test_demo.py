#!/usr/bin/env python3
"""
Integration Test Demo
Shows complete workflow: Database → Transformer → Generator → PDF
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.models import Project, Window, Door
from app.database import SessionLocal, Base, engine
from app.services.data_transformer import DataTransformer
from app.services.integrated_drawing_service import get_drawing_service
from services.google_sheets_services import get_sheets_service


def create_sample_project_in_db():
    """Create sample project with windows and doors in database"""
    print("\n" + "="*60)
    print("CREATING SAMPLE PROJECT IN DATABASE")
    print("="*60)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample project
        project = Project(
            project_name="Modern Office Building",
            po_number="MOD-2024-001",
            customer_name="Acme Corp",
            billing_address="123 Main St, Suite 100, Springfield, IL 62701",
            shipping_address="456 Oak Ave, Warehouse 5, Springfield, IL 62702"
        )
        db.add(project)
        db.flush()  # Get the ID
        
        print(f"✓ Created Project: {project.project_name}")
        print(f"  PO Number: {project.po_number}")
        
        # Create sample windows
        windows_data = [
            {
                "item_number": "W-001",
                "room": "Office A",
                "width_inches": 36.0,
                "height_inches": 48.0,
                "window_type": "Aluminum Casement",
                "frame_series": "Heritage 200",
                "swing_direction": "Inward",
                "glass_type": "Clear 6/6",
                "frame_color": "White",
                "quantity": 1
            },
            {
                "item_number": "W-002",
                "room": "Conference Room",
                "width_inches": 72.0,
                "height_inches": 48.0,
                "window_type": "Aluminum Fixed",
                "frame_series": "Heritage 200",
                "swing_direction": "Fixed",
                "glass_type": "Clear 1/1",
                "frame_color": "Bronze",
                "quantity": 3
            }
        ]
        
        for window_data in windows_data:
            window = Window(
                project_id=project.id,
                **window_data
            )
            db.add(window)
            print(f"  ✓ Window {window.item_number}: {window.width_inches}\"×{window.height_inches}\"")
        
        # Create sample doors
        doors_data = [
            {
                "item_number": "D-001",
                "room": "Main Entrance",
                "width_inches": 48.0,
                "height_inches": 84.0,
                "window_type": "Aluminum Storefront",
                "frame_series": "Heritage 250",
                "swing_direction": "Outward",
                "glass_type": "Clear 6/6",
                "frame_color": "Anodized",
                "quantity": 1
            }
        ]
        
        for door_data in doors_data:
            door = Door(
                project_id=project.id,
                **door_data
            )
            db.add(door)
            print(f"  ✓ Door {door.item_number}: {door.width_inches}\"×{door.height_inches}\"")
        
        db.commit()
        print(f"\n✓ Database populated successfully!")
        
        return project.id
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        db.close()


def test_data_transformation(project_id: int):
    """Test the data transformation layer"""
    print("\n" + "="*60)
    print("TESTING DATA TRANSFORMATION LAYER")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        project = db.query(Project).filter_by(id=project_id).first()
        window = db.query(Window).filter_by(project_id=project_id).first()
        door = db.query(Door).filter_by(project_id=project_id).first()
        
        # Transform window
        window_data = DataTransformer.window_to_drawing_data(window, project)
        print("\n✓ Window Transformation:")
        for key, value in window_data.items():
            print(f"  {key}: {value}")
        
        # Transform door
        door_data = DataTransformer.door_to_drawing_data(door, project)
        print("\n✓ Door Transformation:")
        for key, value in door_data.items():
            print(f"  {key}: {value}")
        
        # Transform project metadata
        metadata = DataTransformer.project_to_metadata(project)
        print("\n✓ Project Metadata:")
        for key, value in metadata.items():
            print(f"  {key}: {value}")
        
        return window_data, door_data, metadata
        
    finally:
        db.close()


def test_drawing_generation(window_data, door_data, metadata):
    """Test the integrated drawing generation"""
    print("\n" + "="*60)
    print("TESTING INTEGRATED DRAWING GENERATION")
    print("="*60)
    
    drawing_service = get_drawing_service()
    
    # Generate window drawing
    print("\n✓ Generating Window Drawing...")
    window_pdf = drawing_service.generator.generate_window_drawing(
        window_data,
        metadata,
        f"{metadata['po_number']}_Window-{window_data['item_number']}_ELEV.pdf"
    )
    print(f"  ✓ Generated: {window_pdf}")
    print(f"  ✓ File exists: {Path(window_pdf).exists()}")
    print(f"  ✓ File size: {Path(window_pdf).stat().st_size} bytes")
    
    # Generate door drawing
    print("\n✓ Generating Door Drawing...")
    door_pdf = drawing_service.generator.generate_door_drawing(
        door_data,
        metadata,
        f"{metadata['po_number']}_Door-{door_data['item_number']}_ELEV.pdf"
    )
    print(f"  ✓ Generated: {door_pdf}")
    print(f"  ✓ File exists: {Path(door_pdf).exists()}")
    print(f"  ✓ File size: {Path(door_pdf).stat().st_size} bytes")
    
    return window_pdf, door_pdf


def test_batch_generation(project_id: int):
    """Test batch project generation"""
    print("\n" + "="*60)
    print("TESTING BATCH PROJECT GENERATION")
    print("="*60)
    
    db = SessionLocal()
    drawing_service = get_drawing_service()
    
    try:
        project = db.query(Project).filter_by(id=project_id).first()
        
        print(f"\n✓ Generating all drawings for: {project.project_name}")
        results = drawing_service.generate_project_drawings(project)
        
        print(f"\n✓ Generation Complete:")
        print(f"  Windows generated: {len(results['windows'])}")
        for pdf in results['windows']:
            print(f"    • {Path(pdf).name}")
        
        print(f"  Doors generated: {len(results['doors'])}")
        for pdf in results['doors']:
            print(f"    • {Path(pdf).name}")
        
    finally:
        db.close()


def list_generated_files():
    """List all generated drawings"""
    print("\n" + "="*60)
    print("GENERATED DRAWINGS DIRECTORY")
    print("="*60)
    
    drawing_service = get_drawing_service()
    drawings = drawing_service.list_generated_drawings()
    
    print(f"\n✓ Total drawings generated: {len(drawings['all'])}")
    print(f"✓ Recent drawings (last 10):")
    for pdf in drawings['recent']:
        path = Path(pdf)
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  • {path.name} ({size_mb:.2f} MB)")


def main():
    """Run complete integration test"""
    print("\n" + "="*70)
    print("RAVEN CUSTOM GLASS - INTEGRATION TEST DEMO")
    print("Complete Workflow: Database → Transformer → Generator → PDF")
    print("="*70)
    
    try:
        # Step 1: Create sample data
        project_id = create_sample_project_in_db()
        
        # Step 2: Test transformation
        window_data, door_data, metadata = test_data_transformation(project_id)
        
        # Step 3: Test single drawing generation
        window_pdf, door_pdf = test_drawing_generation(window_data, door_data, metadata)
        
        # Step 4: Test batch generation
        test_batch_generation(project_id)
        
        # Step 5: List all files
        list_generated_files()
        
        print("\n" + "="*70)
        print("✓ INTEGRATION TEST COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nNext Steps:")
        print("1. Start FastAPI server: uvicorn app.main:app --reload")
        print("2. API will be available at: http://localhost:8000/docs")
        print("3. Test endpoints:")
        print("   - POST /api/drawings/project/MOD-2024-001/generate")
        print("   - GET /api/drawings/list/all")
        print("   - GET /api/drawings/download/{filename}")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
