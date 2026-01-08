#!/usr/bin/env python3
"""
Quick Start Guide - Integrated Drawing API
Practical examples for common use cases
"""

# ============================================================================
# SETUP
# ============================================================================

"""
1. Ensure your FastAPI server is running:
   cd backend
   uvicorn app.main:app --reload

2. This creates API at: http://localhost:8000
3. Interactive docs at: http://localhost:8000/docs
"""

# ============================================================================
# EXAMPLE 1: Check API Status
# ============================================================================

import requests

# Get service info
response = requests.get("http://localhost:8000/api/drawings/info")
print(response.json())
# Output:
# {
#   "service": "Professional CAD Drawing Generator",
#   "status": "operational",
#   "version": "1.0",
#   ...
# }


# ============================================================================
# EXAMPLE 2: Generate All Drawings for a Project
# ============================================================================

# Generate all windows and doors for project with PO# MOD-2024-001
response = requests.post(
    "http://localhost:8000/api/drawings/project/MOD-2024-001/generate"
)

result = response.json()
print(f"Generated {result['windows_generated']} windows and {result['doors_generated']} doors")
print(f"Files: {result['files']}")
# Output:
# Generated 3 windows and 2 doors
# Files: {
#   "windows": ["MOD-2024-001_Window-W-001_ELEV.pdf", ...],
#   "doors": ["MOD-2024-001_Door-D-001_ELEV.pdf", ...]
# }


# ============================================================================
# EXAMPLE 3: Generate Single Window Drawing
# ============================================================================

# Generate drawing for window with database ID 42
response = requests.post(
    "http://localhost:8000/api/drawings/window/42"
)

result = response.json()
print(f"Generated: {result['file']}")
print(f"Item: {result['item_number']}")
# Output:
# Generated: MOD-2024-001_Window-W-001_ELEV.pdf
# Item: W-001


# ============================================================================
# EXAMPLE 4: Generate Single Door Drawing
# ============================================================================

# Generate drawing for door with database ID 15
response = requests.post(
    "http://localhost:8000/api/drawings/door/15"
)

result = response.json()
print(f"Generated: {result['file']}")


# ============================================================================
# EXAMPLE 5: List All Generated Drawings
# ============================================================================

response = requests.get("http://localhost:8000/api/drawings/list/all")

data = response.json()
print(f"Total generated: {data['total']}")
print(f"Recent (last 10):")
for pdf in data['recent_drawings']:
    print(f"  - {pdf}")


# ============================================================================
# EXAMPLE 6: Download a Drawing
# ============================================================================

# Download a specific PDF
filename = "MOD-2024-001_Window-W-001_ELEV.pdf"
response = requests.get(
    f"http://localhost:8000/api/drawings/download/{filename}"
)

# Save to disk
with open(f"downloads/{filename}", "wb") as f:
    f.write(response.content)

print(f"Downloaded: {filename}")


# ============================================================================
# EXAMPLE 7: Using Python SDK (Direct Integration)
# ============================================================================

from app.database import SessionLocal
from app.models import Project, Window, Door
from app.services.integrated_drawing_service import get_drawing_service

# Initialize
db = SessionLocal()
drawing_service = get_drawing_service()

# Get project
project = db.query(Project).filter_by(po_number="MOD-2024-001").first()

if project:
    # Generate single window
    window = db.query(Window).filter_by(project_id=project.id).first()
    pdf_path = drawing_service.generate_window_from_model(window, project)
    print(f"Generated: {pdf_path}")
    
    # Generate all project drawings
    results = drawing_service.generate_project_drawings(project)
    print(f"Windows: {len(results['windows'])}")
    print(f"Doors: {len(results['doors'])}")

db.close()


# ============================================================================
# EXAMPLE 8: Error Handling
# ============================================================================

import requests
from requests.exceptions import RequestException

def safe_generate_drawing(po_number):
    """Safely generate drawings with error handling"""
    try:
        response = requests.post(
            f"http://localhost:8000/api/drawings/project/{po_number}/generate",
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'windows': data['windows_generated'],
                'doors': data['doors_generated']
            }
        elif response.status_code == 404:
            return {'success': False, 'error': f'Project {po_number} not found'}
        else:
            return {'success': False, 'error': response.json()['detail']}
            
    except RequestException as e:
        return {'success': False, 'error': f'Connection error: {e}'}

# Usage
result = safe_generate_drawing("MOD-2024-001")
if result['success']:
    print(f"Generated {result['windows']} windows, {result['doors']} doors")
else:
    print(f"Error: {result['error']}")


# ============================================================================
# EXAMPLE 9: Batch Generation with Progress
# ============================================================================

from app.database import SessionLocal
from app.models import Project
from app.services.integrated_drawing_service import get_drawing_service
import time

def generate_all_projects():
    """Generate drawings for all projects in database"""
    db = SessionLocal()
    drawing_service = get_drawing_service()
    
    projects = db.query(Project).all()
    print(f"Found {len(projects)} projects to process...")
    
    results = {
        'total_projects': len(projects),
        'total_windows': 0,
        'total_doors': 0,
        'errors': []
    }
    
    for project in projects:
        try:
            print(f"Processing: {project.project_name}...", end=" ")
            start = time.time()
            
            result = drawing_service.generate_project_drawings(project)
            
            elapsed = time.time() - start
            results['total_windows'] += len(result['windows'])
            results['total_doors'] += len(result['doors'])
            
            print(f"✓ {len(result['windows'])}W + {len(result['doors'])}D ({elapsed:.1f}s)")
            
        except Exception as e:
            results['errors'].append({
                'project': project.project_name,
                'error': str(e)
            })
            print(f"✗ Error: {e}")
    
    db.close()
    return results

# Usage
# results = generate_all_projects()
# print(f"\nTotal: {results['total_windows']} windows, {results['total_doors']} doors")


# ============================================================================
# EXAMPLE 10: Direct Google Sheets Integration
# ============================================================================

from services.google_sheets_services import get_sheets_service
from app.services.integrated_drawing_service import get_drawing_service
from app.services.data_transformer import DataTransformer

def generate_from_google_sheet(sheet_name):
    """Generate drawings directly from Google Sheets"""
    
    sheets_service = get_sheets_service()
    drawing_service = get_drawing_service()
    
    # Get worksheet
    worksheet = sheets_service.get_worksheet(sheet_name)
    rows = worksheet.get_all_records()
    
    print(f"Generating from sheet: {sheet_name}")
    print(f"Found {len(rows)} items...")
    
    generated = []
    errors = []
    
    # Default project metadata
    project_data = {
        'po_number': f'SHEETS-{sheet_name[:10]}',
        'project_name': sheet_name,
        'customer_name': 'Customer'
    }
    
    for i, row in enumerate(rows):
        try:
            # Generate window drawing
            pdf_path = drawing_service.generate_from_google_sheets_row(
                row,
                item_type='window',
                project_data=project_data
            )
            generated.append(pdf_path)
            print(f"  ✓ Item {i+1}: {pdf_path}")
            
        except Exception as e:
            errors.append({'row': i+1, 'error': str(e)})
            print(f"  ✗ Item {i+1}: {e}")
    
    return {
        'generated': len(generated),
        'errors': len(errors),
        'files': generated
    }

# Usage
# result = generate_from_google_sheet("updated Evergreen Creek")
# print(f"Generated {result['generated']} drawings, {result['errors']} errors")


# ============================================================================
# COMMON WORKFLOW PATTERNS
# ============================================================================

# PATTERN 1: Generate and Download
def generate_and_download(po_number, save_dir="./downloads"):
    """Generate all drawings for a project and download them"""
    import os
    from pathlib import Path
    
    # Create output directory
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate
    response = requests.post(
        f"http://localhost:8000/api/drawings/project/{po_number}/generate"
    )
    
    if response.status_code != 200:
        print(f"Error: {response.json()['detail']}")
        return None
    
    data = response.json()
    files = data['files']['windows'] + data['files']['doors']
    
    # Download each file
    for filename in files:
        response = requests.get(
            f"http://localhost:8000/api/drawings/download/{filename}"
        )
        
        filepath = os.path.join(save_dir, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        print(f"Downloaded: {filename}")
    
    return files


# PATTERN 2: Check Generation Status
def check_project_status(po_number):
    """Check if a project has generated drawings"""
    response = requests.get("http://localhost:8000/api/drawings/list/all")
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    project_drawings = [
        f for f in data['all_drawings']
        if po_number in f
    ]
    
    return {
        'po_number': po_number,
        'has_drawings': len(project_drawings) > 0,
        'count': len(project_drawings),
        'files': project_drawings
    }


# PATTERN 3: Generate with Retry
def generate_with_retry(po_number, max_retries=3):
    """Generate drawings with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"http://localhost:8000/api/drawings/project/{po_number}/generate",
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 404:
                print(f"Project {po_number} not found")
                return None
            
            else:
                print(f"Error (attempt {attempt+1}): {response.status_code}")
                
        except requests.Timeout:
            print(f"Timeout (attempt {attempt+1}), retrying...")
            continue
    
    return None


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Drawing API - Quick Start Examples")
    print("====================================\n")
    
    # Test 1: Check API status
    print("TEST 1: Checking API status...")
    try:
        response = requests.get("http://localhost:8000/api/drawings/info")
        if response.status_code == 200:
            print("✓ API is operational\n")
        else:
            print("✗ API not responding\n")
    except requests.ConnectionError:
        print("✗ Cannot connect to API. Is the server running?\n")
    
    # Test 2: Check status pattern
    print("TEST 2: Checking project status...")
    status = check_project_status("MOD-2024-001")
    if status:
        print(f"✓ Found {status['count']} drawings for {status['po_number']}\n")
    
    # Test 3: List drawings
    print("TEST 3: Listing generated drawings...")
    try:
        response = requests.get("http://localhost:8000/api/drawings/list/all")
        data = response.json()
        print(f"✓ Total generated: {data['total']}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
    
    print("Examples are ready to use!")
    print("See comments above for each usage pattern.")
