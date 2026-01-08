#!/usr/bin/env python3
"""
Integration Validation Script
Verifies all components are properly installed and configured
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and print result"""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}")
    return exists


def check_module_imports():
    """Check if all modules can be imported"""
    print("\n2️⃣  CHECKING IMPORTS")
    print("=" * 60)
    
    modules_to_check = [
        ("fastapi", "FastAPI"),
        ("sqlalchemy", "SQLAlchemy"),
        ("gspread", "Google Sheets"),
        ("requests", "Requests"),
        ("matplotlib", "Matplotlib"),
        ("numpy", "NumPy"),
    ]
    
    all_ok = True
    for module_name, display_name in modules_to_check:
        try:
            __import__(module_name)
            print(f"  ✓ {display_name}")
        except ImportError:
            print(f"  ✗ {display_name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok


def check_project_files():
    """Check if all required project files exist"""
    print("\n1️⃣  CHECKING PROJECT FILES")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    
    files_to_check = [
        # New integration files
        ("app/services/data_transformer.py", "Data Transformer Service"),
        ("app/services/integrated_drawing_service.py", "Integrated Drawing Service"),
        ("routers/drawings.py", "Updated Drawing Router"),
        
        # Documentation
        ("DRAWING_API.md", "API Documentation"),
        ("DRAWING_API_EXAMPLES.py", "API Examples"),
        ("integration_test_demo.py", "Integration Test"),
        ("INTEGRATION_COMPLETE.md", "Integration Summary"),
        
        # Core files
        ("app/models.py", "Database Models"),
        ("app/database.py", "Database Config"),
        ("app/main.py", "FastAPI Main"),
        ("routers/projects.py", "Projects Router"),
        
        # Drawing engine
        ("services/drawing_engine/main.py", "Drawing Generator"),
        ("services/drawing_engine/layout.py", "Layout Module"),
        ("services/drawing_engine/dimensions.py", "Dimensions Module"),
        ("services/drawing_engine/components.py", "Components Module"),
        ("services/drawing_engine/__init__.py", "Drawing Engine Init"),
        
        # Services
        ("services/google_sheets_services.py", "Google Sheets Service"),
    ]
    
    all_exist = True
    for filepath, description in files_to_check:
        full_path = base_dir / filepath
        if not check_file_exists(full_path, description):
            all_exist = False
    
    return all_exist


def check_class_definitions():
    """Check if key classes are properly defined"""
    print("\n3️⃣  CHECKING CLASS DEFINITIONS")
    print("=" * 60)
    
    all_ok = True
    
    try:
        from app.services.data_transformer import DataTransformer
        print(f"  ✓ DataTransformer class")
        
        # Check methods
        methods = [
            'window_to_drawing_data',
            'door_to_drawing_data',
            'project_to_metadata',
            'from_google_sheets_row',
            'batch_windows_to_drawing_data',
            'batch_doors_to_drawing_data'
        ]
        
        for method_name in methods:
            if hasattr(DataTransformer, method_name):
                print(f"    ✓ {method_name}()")
            else:
                print(f"    ✗ {method_name}() - MISSING")
                all_ok = False
                
    except ImportError as e:
        print(f"  ✗ DataTransformer - IMPORT ERROR: {e}")
        all_ok = False
    
    try:
        from app.services.integrated_drawing_service import IntegratedDrawingService
        print(f"  ✓ IntegratedDrawingService class")
        
        # Check methods
        methods = [
            'generate_window_from_model',
            'generate_door_from_model',
            'generate_project_drawings',
            'generate_from_google_sheets_row',
            'list_generated_drawings',
            'delete_drawing'
        ]
        
        for method_name in methods:
            if hasattr(IntegratedDrawingService, method_name):
                print(f"    ✓ {method_name}()")
            else:
                print(f"    ✗ {method_name}() - MISSING")
                all_ok = False
                
    except ImportError as e:
        print(f"  ✗ IntegratedDrawingService - IMPORT ERROR: {e}")
        all_ok = False
    
    try:
        from services.drawing_engine import ProfessionalDrawingGenerator
        print(f"  ✓ ProfessionalDrawingGenerator class")
        
        methods = [
            'generate_window_drawing',
            'generate_door_drawing'
        ]
        
        for method_name in methods:
            if hasattr(ProfessionalDrawingGenerator, method_name):
                print(f"    ✓ {method_name}()")
            else:
                print(f"    ✗ {method_name}() - MISSING")
                all_ok = False
                
    except ImportError as e:
        print(f"  ✗ ProfessionalDrawingGenerator - IMPORT ERROR: {e}")
        all_ok = False
    
    return all_ok


def check_api_endpoints():
    """Check if API endpoints are properly defined"""
    print("\n4️⃣  CHECKING API ENDPOINTS")
    print("=" * 60)
    
    all_ok = True
    
    try:
        from routers.drawings import router
        print(f"  ✓ Drawing Router imported")
        
        # Get routes
        routes = [route.path for route in router.routes]
        
        expected_endpoints = [
            "/project/{po_number}/generate",
            "/window/{window_id}",
            "/door/{door_id}",
            "/download/{filename}",
            "/list/all",
            "/info"
        ]
        
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print(f"    ✓ {endpoint}")
            else:
                print(f"    ✗ {endpoint} - MISSING")
                all_ok = False
                
    except ImportError as e:
        print(f"  ✗ Drawing Router - IMPORT ERROR: {e}")
        all_ok = False
    except Exception as e:
        print(f"  ✗ Error checking routes: {e}")
        all_ok = False
    
    return all_ok


def check_database_models():
    """Check if database models are properly defined"""
    print("\n5️⃣  CHECKING DATABASE MODELS")
    print("=" * 60)
    
    all_ok = True
    
    try:
        from app.models import Project, Window, Door
        print(f"  ✓ Project model")
        print(f"  ✓ Window model")
        print(f"  ✓ Door model")
        
        # Check Project fields
        project_fields = ['id', 'project_name', 'po_number', 'customer_name']
        
        for field in project_fields:
            if hasattr(Project, field):
                print(f"    ✓ Project.{field}")
            else:
                print(f"    ✗ Project.{field} - MISSING")
                all_ok = False
        
    except ImportError as e:
        print(f"  ✗ Database Models - IMPORT ERROR: {e}")
        all_ok = False
    
    return all_ok


def check_output_directory():
    """Check if output directory exists"""
    print("\n6️⃣  CHECKING OUTPUT DIRECTORY")
    print("=" * 60)
    
    drawings_dir = Path("./drawings")
    
    if drawings_dir.exists():
        print(f"  ✓ Output directory exists: {drawings_dir}")
        
        # Count PDFs
        pdfs = list(drawings_dir.glob("*.pdf"))
        print(f"  ✓ PDFs in directory: {len(pdfs)}")
        
        if pdfs:
            print(f"\n  Recent PDFs:")
            for pdf in sorted(pdfs, key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
                size_kb = pdf.stat().st_size / 1024
                print(f"    • {pdf.name} ({size_kb:.1f} KB)")
        
        return True
    else:
        print(f"  ✗ Output directory does not exist: {drawings_dir}")
        print(f"  💡 Creating directory...")
        drawings_dir.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Directory created")
        return True


def print_summary(results):
    """Print validation summary"""
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\n  Total Checks: {total}")
    print(f"  ✓ Passed: {passed}")
    print(f"  ✗ Failed: {failed}")
    
    if failed == 0:
        print("\n  🎉 ALL CHECKS PASSED!")
        print("\n  Your integration is complete and ready to use.")
        print("\n  Next steps:")
        print("  1. Start the API server:")
        print("     uvicorn app.main:app --reload")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Test endpoints in Swagger UI")
        print("  4. Run integration test:")
        print("     python integration_test_demo.py")
    else:
        print(f"\n  ⚠️  {failed} check(s) failed. Review the output above.")
        return False
    
    return True


def main():
    """Run all validation checks"""
    print("\n" + "=" * 60)
    print("RAVEN CUSTOM GLASS - INTEGRATION VALIDATION")
    print("=" * 60)
    print("\nValidating all components of the drawing API integration...\n")
    
    results = {}
    
    # Run checks
    results['Files'] = check_project_files()
    results['Imports'] = check_module_imports()
    results['Classes'] = check_class_definitions()
    results['Endpoints'] = check_api_endpoints()
    results['Models'] = check_database_models()
    results['Output'] = check_output_directory()
    
    # Print summary
    success = print_summary(results)
    
    # Exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
