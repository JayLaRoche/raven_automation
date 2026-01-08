# Drawing API - Complete Integration Guide

## Overview

The Drawing API provides production-ready CAD-style shop drawing generation with professional layout, parametric dimensions, and specification tables.

**Integration Architecture:**
```
FastAPI Request
    ↓
Database Query (Project/Window/Door models)
    ↓
DataTransformer (model → drawing format)
    ↓
ProfessionalDrawingGenerator (layout + dimensions)
    ↓
PDF Output (./drawings/)
    ↓
FastAPI Response (file download/info)
```

## Key Components

### 1. Data Transformer (`app/services/data_transformer.py`)
Bridges database models to drawing generator format.

**Static Methods:**
- `window_to_drawing_data(window: Window, project: Project) → Dict`
- `door_to_drawing_data(door: Door, project: Project) → Dict`
- `project_to_metadata(project: Project) → Dict`
- `from_google_sheets_row(row: Dict, item_type: str) → Dict`

### 2. Integrated Drawing Service (`app/services/integrated_drawing_service.py`)
High-level service wrapping the drawing engine.

**Key Methods:**
- `generate_window_from_model(window, project, filename)`
- `generate_door_from_model(door, project, filename)`
- `generate_project_drawings(project, windows, doors)`
- `generate_from_google_sheets_row(row, item_type, project_data, filename)`
- `list_generated_drawings()`
- `delete_drawing(filename)`

### 3. Professional Drawing Engine (`services/drawing_engine/`)
Low-level drawing generation (phase 1 implementation).

**Modules:**
- `layout.py` - 3-column grid with 8 zones
- `dimensions.py` - CAD-style dimension lines
- `components.py` - Specification tables, headers, project info
- `main.py` - Main `ProfessionalDrawingGenerator` class

## API Endpoints

### 1. Generate Project Drawings (All Items)

```http
POST /api/drawings/project/{po_number}/generate
```

**Request:**
```bash
curl -X POST http://localhost:8000/api/drawings/project/MOD-2024-001/generate
```

**Response:**
```json
{
  "success": true,
  "po_number": "MOD-2024-001",
  "project_name": "Modern Office Building",
  "message": "Generated 5 drawing(s)",
  "windows_generated": 3,
  "doors_generated": 2,
  "files": {
    "windows": [
      "MOD-2024-001_Window-W-001_ELEV.pdf",
      "MOD-2024-001_Window-W-002_ELEV.pdf",
      "MOD-2024-001_Window-W-003_ELEV.pdf"
    ],
    "doors": [
      "MOD-2024-001_Door-D-001_ELEV.pdf",
      "MOD-2024-001_Door-D-002_ELEV.pdf"
    ]
  }
}
```

**Status Codes:**
- `200` - Success
- `404` - Project not found
- `500` - Generation error

---

### 2. Generate Window Drawing

```http
POST /api/drawings/window/{window_id}
```

**Request:**
```bash
curl -X POST http://localhost:8000/api/drawings/window/42
```

**Response:**
```json
{
  "success": true,
  "window_id": 42,
  "item_number": "W-001",
  "file": "MOD-2024-001_Window-W-001_ELEV.pdf",
  "path": "./drawings/MOD-2024-001_Window-W-001_ELEV.pdf"
}
```

**Status Codes:**
- `200` - Success
- `404` - Window not found
- `500` - Generation error

---

### 3. Generate Door Drawing

```http
POST /api/drawings/door/{door_id}
```

**Request:**
```bash
curl -X POST http://localhost:8000/api/drawings/door/15
```

**Response:**
```json
{
  "success": true,
  "door_id": 15,
  "item_number": "D-001",
  "file": "MOD-2024-001_Door-D-001_ELEV.pdf",
  "path": "./drawings/MOD-2024-001_Door-D-001_ELEV.pdf"
}
```

**Status Codes:**
- `200` - Success
- `404` - Door not found
- `500` - Generation error

---

### 4. Download Drawing PDF

```http
GET /api/drawings/download/{filename}
```

**Request:**
```bash
curl -O http://localhost:8000/api/drawings/download/MOD-2024-001_Window-W-001_ELEV.pdf
```

**Response:**
- Content-Type: `application/pdf`
- File download with proper headers

**Status Codes:**
- `200` - Success
- `403` - Access denied (path traversal attempt)
- `404` - File not found

---

### 5. List All Generated Drawings

```http
GET /api/drawings/list/all
```

**Request:**
```bash
curl http://localhost:8000/api/drawings/list/all
```

**Response:**
```json
{
  "total": 127,
  "recent_count": 10,
  "all_drawings": [
    "./drawings/MOD-2024-001_Window-W-001_ELEV.pdf",
    "./drawings/MOD-2024-001_Window-W-002_ELEV.pdf",
    "./drawings/DEMO-001_Window-W-001_ELEV.pdf",
    "..."
  ],
  "recent_drawings": [
    "./drawings/MOD-2024-001_Window-W-001_ELEV.pdf",
    "./drawings/MOD-2024-001_Window-W-002_ELEV.pdf",
    "..."
  ]
}
```

**Status Codes:**
- `200` - Success
- `500` - Service error

---

### 6. Service Information

```http
GET /api/drawings/info
```

**Request:**
```bash
curl http://localhost:8000/api/drawings/info
```

**Response:**
```json
{
  "service": "Professional CAD Drawing Generator",
  "status": "operational",
  "version": "1.0",
  "capabilities": [
    "Generate window elevation drawings with CAD dimensions",
    "Generate door elevation drawings with CAD dimensions",
    "Support for professional 3-column layout",
    "Specification tables and project metadata",
    "Batch project drawing generation",
    "PDF download and file management"
  ],
  "output_directory": "./drawings",
  "total_drawings_generated": 127,
  "api_endpoints": {
    "generate_project": "POST /api/drawings/project/{po_number}/generate",
    "generate_window": "POST /api/drawings/window/{window_id}",
    "generate_door": "POST /api/drawings/door/{door_id}",
    "list_all": "GET /api/drawings/list/all",
    "download": "GET /api/drawings/download/{filename}",
    "info": "GET /api/drawings/info"
  }
}
```

---

## Usage Workflow

### Scenario 1: Generate All Drawings for a Project

1. **Query project by PO number:**
   ```python
   GET /api/projects/MOD-2024-001
   ```

2. **Generate all drawings:**
   ```python
   POST /api/drawings/project/MOD-2024-001/generate
   ```

3. **List generated files:**
   ```python
   GET /api/drawings/list/all
   ```

4. **Download individual drawing:**
   ```python
   GET /api/drawings/download/{filename}
   ```

### Scenario 2: Generate Single Window Drawing

1. **Query window by ID:**
   ```python
   GET /api/projects/MOD-2024-001/windows/42
   ```

2. **Generate drawing:**
   ```python
   POST /api/drawings/window/42
   ```

3. **Download result:**
   ```python
   GET /api/drawings/download/{filename}
   ```

### Scenario 3: Generate from Google Sheets

Using existing Google Sheets integration:

```python
from services.google_sheets_services import get_sheets_service
from app.services.integrated_drawing_service import get_drawing_service

# Get sheet data
sheets_service = get_sheets_service()
worksheet = sheets_service.get_worksheet("updated Evergreen Creek")
rows = worksheet.get_all_records()

# Generate drawings
drawing_service = get_drawing_service()
for row in rows:
    pdf_path = drawing_service.generate_from_google_sheets_row(
        row,
        item_type='window',
        project_data={'po_number': 'SHEETS-001', ...}
    )
```

---

## Database Integration

### Models

```python
class Project(Base):
    id: int
    project_name: str
    po_number: str (unique)
    customer_name: str
    billing_address: str
    shipping_address: str
    windows: List[Window] (relationship)
    doors: List[Door] (relationship)

class Window(Base):
    id: int
    project_id: int (FK)
    item_number: str
    room: str
    width_inches: float
    height_inches: float
    window_type: str
    frame_series: str
    swing_direction: str
    glass_type: str
    frame_color: str
    quantity: int

class Door(Base):
    id: int
    project_id: int (FK)
    item_number: str
    room: str
    width_inches: float
    height_inches: float
    window_type: str
    frame_series: str
    swing_direction: str
    glass_type: str
    frame_color: str
    quantity: int
```

---

## Drawing Output Format

Each generated PDF includes:

### Layout (3-Column, 8-Zone Design)

**Left Column (30%):**
- Specification Table
- Item details (type, materials, colors)
- Glass and hardware specs
- Quantity information

**Center Column (45%):**
- Elevation View
- CAD-style dimension lines
- Extension lines and arrows
- Dimensional annotations (height, width, depths)
- Grid reference system

**Right Column (25%):**
- Company header and logo area
- Drawing title
- Item number and description
- Project information
- Revision block

### Dimensions

- **Format:** 11"×17" landscape (tabloid)
- **Resolution:** 300 DPI (print-ready)
- **Font:** Professional sans-serif (Helvetica)
- **Color:** Professional grayscale with accent colors

---

## Error Handling

### Common Error Scenarios

**1. Project Not Found**
```json
{
  "detail": "Project with PO number 'INVALID' not found"
}
```
Status: 404

**2. Window/Door Not Found**
```json
{
  "detail": "Window with ID 999 not found"
}
```
Status: 404

**3. Generation Failed**
```json
{
  "detail": "Drawing generation failed: [error message]"
}
```
Status: 500

**4. File Access Denied**
```json
{
  "detail": "Access denied"
}
```
Status: 403

**5. Drawing Not Found**
```json
{
  "detail": "Drawing not found"
}
```
Status: 404

---

## Advanced Usage

### Batch Generation with Error Handling

```python
from app.database import SessionLocal
from app.models import Project, Window
from app.services.integrated_drawing_service import get_drawing_service

db = SessionLocal()
drawing_service = get_drawing_service()

project = db.query(Project).filter_by(po_number="MOD-2024-001").first()
windows = db.query(Window).filter_by(project_id=project.id).all()

results = {
    'successful': [],
    'failed': []
}

for window in windows:
    try:
        pdf_path = drawing_service.generate_window_from_model(window, project)
        results['successful'].append(pdf_path)
    except Exception as e:
        results['failed'].append({
            'item': window.item_number,
            'error': str(e)
        })

print(f"Generated: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")
```

### Custom Filenames

```python
pdf_path = drawing_service.generate_window_from_model(
    window,
    project,
    filename="Custom_Window_Name.pdf"  # Optional
)
```

### Google Sheets Direct Generation

```python
# Generate without database
window_data = DataTransformer.from_google_sheets_row(
    {'Width': '36', 'Height': '48', 'Frame Series': 'Heritage 200', ...},
    'window'
)

pdf_path = drawing_service.generate_from_google_sheets_row(
    row,
    'window',
    project_data={'po_number': 'SHEETS-001'}
)
```

---

## Configuration

### Output Directory

Change output directory when initializing service:

```python
drawing_service = get_drawing_service(output_dir="/custom/path/drawings")
```

### Drawing Engine Parameters

Available in `services/drawing_engine/main.py`:

- Page size: 11×17 inches
- DPI: 300 (print-ready)
- Margins: Adjustable in layout.py
- Column ratios: 0.30 | 0.45 | 0.25

---

## Performance Considerations

- **Single Drawing Generation:** ~2-3 seconds
- **Batch (10 items):** ~20-30 seconds
- **Memory:** ~100MB per batch operation
- **Disk:** ~500KB per PDF

For large batches (50+), generation is sequential to avoid memory issues.

---

## Testing

Run the integration test demo:

```bash
python integration_test_demo.py
```

This creates sample data and tests:
1. Database creation
2. Data transformation
3. Single drawing generation
4. Batch generation
5. File listing

---

## Troubleshooting

### PDFs not generating
1. Check output directory exists: `./drawings/`
2. Verify database has valid project/window/door records
3. Check file permissions on output directory

### File not found on download
1. Verify filename using `/api/drawings/list/all`
2. Check drawings directory exists

### Memory issues on large batches
1. Generate in smaller batches (< 50 items)
2. Clear old drawings periodically

### Import errors
1. Ensure `services/drawing_engine/` directory exists
2. Verify `__init__.py` in module directories
3. Check Python path includes project root

---

## Next Steps

1. **Frontend Integration:** Build React UI for drawing management
2. **Archive System:** Persist drawing references in database
3. **Advanced Features:** Cross-sections, multi-views, hardware specs
4. **Branding:** Custom logo and company info integration
5. **Scheduling:** Generate on-demand or scheduled batch operations
