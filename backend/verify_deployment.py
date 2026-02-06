"""Run this during Render build to verify deployment readiness"""
import os
import sys

def verify_deployment():
    """Check that all required directories and files exist"""
    print("=" * 60)
    print("DEPLOYMENT VERIFICATION")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # Check required files
    required_files = [
        "main.py",
        "requirements.txt",
        "init_db.py",
        "app/__init__.py",
        "app/config.py",
        "app/database.py",
        "app/models.py",
        "routers/__init__.py",
        "routers/frames.py",
        "routers/drawings.py",
        "routers/projects.py",
    ]
    
    for f in required_files:
        if os.path.exists(f):
            print(f"  [OK] {f}")
        else:
            errors.append(f"Missing required file: {f}")
            print(f"  [FAIL] {f}")
    
    # Check/create required directories
    required_dirs = [
        "data",
        "static",
        "static/frames",
        "outputs",
        "logs",
    ]
    
    for d in required_dirs:
        if os.path.exists(d):
            print(f"  [OK] {d}/")
        else:
            os.makedirs(d, exist_ok=True)
            print(f"  [CREATED] {d}/")
    
    # Check optional directories
    optional_dirs = [
        "static/O-Icon_library",
        "static/products",
        "assets/frames",
        "frame_library",
    ]
    
    for d in optional_dirs:
        if os.path.exists(d):
            file_count = len([f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))])
            print(f"  [OK] {d}/ ({file_count} files)")
        else:
            warnings.append(f"Optional directory missing: {d}")
            print(f"  [WARN] {d}/ (not found)")
    
    # Check environment
    print("\n  Environment:")
    print(f"    APP_ENV: {os.getenv('APP_ENV', 'not set')}")
    print(f"    PORT: {os.getenv('PORT', 'not set (will use 8000)')}")
    print(f"    DATABASE_URL: {'set' if os.getenv('DATABASE_URL') else 'not set'}")
    print(f"    CORS_ORIGINS: {os.getenv('CORS_ORIGINS', 'not set')}")
    print(f"    Python: {sys.version}")
    print(f"    CWD: {os.getcwd()}")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN: {w}")
        sys.exit(1)
    else:
        print(f"PASS: 0 errors, {len(warnings)} warning(s)")
        for w in warnings:
            print(f"  WARN: {w}")
    print("=" * 60)

if __name__ == "__main__":
    verify_deployment()
