#!/usr/bin/env python3
import subprocess
import sys
import os

os.chdir(r"c:\Users\larochej3\Desktop\raven-shop-automation\backend")

script_path = r"c:\Users\larochej3\multipleWindow3dScene\test_generate_from_test1.py"

print("=" * 70)
print("RUNNING: Generate PDF from Test_1 Sheet")
print("=" * 70)
print()

try:
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    print(f"\nExit Code: {result.returncode}")
    
    if result.returncode == 0:
        print("\n✓ Script completed successfully")
    else:
        print("\n✗ Script failed with errors (see above)")
        
except subprocess.TimeoutExpired:
    print("✗ Script timed out after 30 seconds")
except Exception as e:
    print(f"✗ Error running script: {e}")
