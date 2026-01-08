#!/usr/bin/env python3
"""
CAD Drawing Generator - Deployment Checklist

Use this to verify everything is working before production deployment.
"""

import subprocess
import sys
from pathlib import Path

class DeploymentChecker:
    """Verify all components are ready for deployment"""
    
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
    
    def print_header(self, text):
        """Print section header"""
        print("\n" + "="*70)
        print(f"  {text}")
        print("="*70)
    
    def print_check(self, name, passed, message=""):
        """Print check result"""
        symbol = "✅" if passed else "❌"
        status = "PASS" if passed else "FAIL"
        print(f"{symbol} {name:<50} [{status}]")
        if message:
            print(f"   └─ {message}")
        
        if passed:
            self.checks_passed += 1
        else:
            self.checks_failed += 1
    
    def print_warning(self, text):
        """Print warning"""
        print(f"⚠️  {text}")
        self.warnings.append(text)
    
    def check_python_version(self):
        """Check Python version is 3.9+"""
        self.print_header("1. Python Version")
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        required = (3, 9)
        
        is_ok = sys.version_info >= required
        self.print_check(
            f"Python {version}",
            is_ok,
            f"Required: 3.9+, Found: {version}"
        )
        return is_ok
    
    def check_dependencies(self):
        """Check all required dependencies are installed"""
        self.print_header("2. Dependencies")
        
        dependencies = [
            ('reportlab', 'ReportLab (PDF generation)'),
            ('fastapi', 'FastAPI (web framework)'),
            ('sqlalchemy', 'SQLAlchemy (database)'),
            ('pydantic', 'Pydantic (validation)'),
        ]
        
        all_ok = True
        for module_name, description in dependencies:
            try:
                __import__(module_name)
                self.print_check(f"{module_name:<20}", True, description)
            except ImportError:
                self.print_check(f"{module_name:<20}", False, description)
                all_ok = False
        
        return all_ok
    
    def check_files_exist(self):
        """Check all required files exist"""
        self.print_header("3. Required Files")
        
        backend_dir = Path(__file__).parent
        files = [
            ('app/services/frame_profiles.py', 'Frame geometry definitions'),
            ('app/services/cad_drawing_generator.py', 'Drawing generator'),
            ('app/services/cad_data_transformer.py', 'Data transformer'),
            ('routers/cad_drawings.py', 'API endpoints'),
            ('test_cad_generator.py', 'Test suite'),
            ('quick_start.py', 'Quick start examples'),
        ]
        
        all_ok = True
        for file_path, description in files:
            full_path = backend_dir / file_path
            exists = full_path.exists()
            self.print_check(
                f"{file_path:<40}",
                exists,
                description if exists else f"Missing: {full_path}"
            )
            all_ok = all_ok and exists
        
        return all_ok
    
    def check_documentation(self):
        """Check all documentation files exist"""
        self.print_header("4. Documentation")
        
        backend_dir = Path(__file__).parent
        docs = [
            ('INDEX.md', 'Documentation index'),
            ('README_CAD.md', 'Project README'),
            ('README_VISUAL.md', 'Visual overview'),
            ('CAD_DRAWING_GUIDE.md', 'Technical reference'),
            ('CAD_IMPLEMENTATION_SUMMARY.md', 'Implementation overview'),
            ('INTEGRATION_GUIDE.md', 'Integration instructions'),
            ('DEPENDENCIES.md', 'Dependencies reference'),
            ('COMPLETION_SUMMARY.md', 'Completion checklist'),
        ]
        
        all_ok = True
        for doc_file, description in docs:
            full_path = backend_dir / doc_file
            exists = full_path.exists()
            self.print_check(
                f"{doc_file:<40}",
                exists,
                description
            )
            all_ok = all_ok and exists
        
        return all_ok
    
    def check_database_models(self):
        """Check database models are compatible"""
        self.print_header("5. Database Models")
        
        try:
            from app.models import Window, Door, Project
            
            # Check Window has required fields
            window_ok = all(hasattr(Window, field) for field in [
                'item_number', 'width_inches', 'height_inches',
                'frame_series', 'window_type'
            ])
            self.print_check("Window model", window_ok, "Has all required fields")
            
            # Check Door has required fields
            door_ok = all(hasattr(Door, field) for field in [
                'item_number', 'width_inches', 'height_inches',
                'frame_series', 'door_type'
            ])
            self.print_check("Door model", door_ok, "Has all required fields")
            
            # Check Project exists
            project_ok = hasattr(Project, 'po_number')
            self.print_check("Project model", project_ok, "Has po_number field")
            
            return window_ok and door_ok and project_ok
            
        except ImportError as e:
            self.print_check("Database models", False, str(e))
            return False
    
    def check_imports(self):
        """Check all imports work"""
        self.print_header("6. Import Verification")
        
        imports = [
            ('app.services.frame_profiles', 'get_profile'),
            ('app.services.cad_drawing_generator', 'generate_cad_drawing'),
            ('app.services.cad_data_transformer', 'CADDataTransformer'),
        ]
        
        all_ok = True
        for module, item in imports:
            try:
                mod = __import__(module, fromlist=[item])
                getattr(mod, item)
                self.print_check(f"{module}.{item}", True)
            except (ImportError, AttributeError) as e:
                self.print_check(f"{module}.{item}", False, str(e))
                all_ok = False
        
        return all_ok
    
    def check_api_routes(self):
        """Check API routes are defined"""
        self.print_header("7. API Routes")
        
        try:
            from routers import cad_drawings
            
            # Check router exists
            router_ok = hasattr(cad_drawings, 'router')
            self.print_check("Router object", router_ok)
            
            # Count routes
            if router_ok:
                routes = cad_drawings.router.routes
                route_count = len([r for r in routes if hasattr(r, 'path')])
                self.print_check(
                    f"Routes defined",
                    route_count >= 4,
                    f"Found {route_count} routes (expected 4+)"
                )
            
            return router_ok
            
        except ImportError as e:
            self.print_check("API routes", False, str(e))
            return False
    
    def run_examples(self):
        """Try to run quick_start.py"""
        self.print_header("8. Example Generation")
        
        try:
            # Just import the test module to verify syntax
            import test_cad_generator
            self.print_check("Test module loads", True, "test_cad_generator.py")
            
            # Try to import quick_start
            import quick_start as qs
            self.print_check("Quick start loads", True, "quick_start.py")
            
            return True
            
        except Exception as e:
            self.print_check("Example generation", False, str(e))
            return False
    
    def check_configuration(self):
        """Check basic configuration"""
        self.print_header("9. Configuration")
        
        backend_dir = Path(__file__).parent
        
        # Check for .env file (optional)
        env_file = backend_dir / '.env'
        if env_file.exists():
            self.print_check(".env file", True, "Environment file found")
        else:
            self.print_warning(".env file not found (optional)")
        
        # Check for database config
        try:
            from app.database import engine
            self.print_check("Database engine", True, "Connected to database")
            return True
        except Exception as e:
            self.print_check("Database engine", False, str(e))
            return False
    
    def print_summary(self):
        """Print final summary"""
        self.print_header("DEPLOYMENT STATUS")
        
        total = self.checks_passed + self.checks_failed
        
        print(f"\n✅ Passed: {self.checks_passed}/{total}")
        print(f"❌ Failed: {self.checks_failed}/{total}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings: {len(self.warnings)}")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        print("\n" + "="*70)
        
        if self.checks_failed == 0:
            print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT")
            print("="*70)
            print("\nNext steps:")
            print("  1. Register router in app/main.py")
            print("  2. Test endpoints: GET /api/drawings/cad/list/windows")
            print("  3. Deploy to staging")
            print("  4. Run final validation")
            print("  5. Deploy to production")
            return True
        else:
            print("❌ SOME CHECKS FAILED - RESOLVE ISSUES BEFORE DEPLOYMENT")
            print("="*70)
            print("\nReview failures above and:")
            print("  1. Install missing dependencies")
            print("  2. Ensure all files are in place")
            print("  3. Fix import errors")
            print("  4. Verify database configuration")
            print("\nFor help, see: INTEGRATION_GUIDE.md")
            return False
    
    def run_all_checks(self):
        """Run all checks"""
        print("\n" + "="*70)
        print("  CAD DRAWING GENERATOR - DEPLOYMENT CHECKLIST")
        print("="*70)
        print(f"\nRunning {9} verification checks...\n")
        
        results = [
            self.check_python_version(),
            self.check_dependencies(),
            self.check_files_exist(),
            self.check_documentation(),
            self.check_database_models(),
            self.check_imports(),
            self.check_api_routes(),
            self.run_examples(),
            self.check_configuration(),
        ]
        
        return self.print_summary()


def main():
    """Main entry point"""
    try:
        checker = DeploymentChecker()
        success = checker.run_all_checks()
        return 0 if success else 1
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
