# Raven Shop Automation - Complete API Documentation

## 🎉 System Status: OPERATIONAL

All components are fully integrated and tested:
- ✅ FastAPI backend running
- ✅ Google Sheets integration connected
- ✅ SQLite database configured  
- ✅ PDF drawing generation working
- ✅ API endpoints operational

---

## 📋 API Endpoints

### Projects API (`/api/projects/`)

#### 1. List PO Numbers
```
GET /api/projects/po-numbers
```
Get all available PO numbers from the configured Google Sheet.

**Example Response:**
```json
{
  "po_numbers": ["Evergreen Creek", "2095 Alcova Ridge", "Glasgow", ...]
}
```

#### 2. Sync Project
```
POST /api/projects/{po_number}/sync
```
Sync project data from Google Sheets to SQLite database.

**Example:**
```bash
curl -X POST http://localhost:8000/api/projects/Evergreen%20Creek/sync
```

**Response:**
```json
{
  "success": true,
  "message": "Project Evergreen Creek created successfully",
  "data": {
    "sync_type": "created",
    "po_number": "Evergreen Creek",
    "project_id": 1,
    "windows_count": 5,
    "doors_count": 2,
    "synced_at": "2025-12-23T14:30:45"
  }
}
```

#### 3. Get Project Details
```
GET /api/projects/{po_number}
```
Retrieve project data from the database (windows, doors, specifications).

**Example:**
```bash
curl http://localhost:8000/api/projects/Evergreen%20Creek
```

#### 4. Check Sync Status
```
GET /api/projects/{po_number}/status
```
Check if a project is synced and when it was last updated.

---

### Drawings API (`/api/drawings/`)

#### 1. Generate Project Drawings
```
POST /api/drawings/{po_number}/generate
```
Generate PDF technical shop drawings for all windows and doors in a project.

**Example:**
```bash
curl -X POST http://localhost:8000/api/drawings/Evergreen%20Creek/generate
```

**Response:**
```json
{
  "success": true,
  "po_number": "Evergreen Creek",
  "message": "Generated 7 drawing(s)",
  "drawings": [
    "Evergreen Creek_W-001_elevation.pdf",
    "Evergreen Creek_W-002_elevation.pdf",
    "Evergreen Creek_D-001_elevation.pdf",
    ...
  ],
  "file_count": 7
}
```

#### 2. List Project Drawings
```
GET /api/drawings/{po_number}/list
```
List all generated PDF drawings for a project.

**Example:**
```bash
curl http://localhost:8000/api/drawings/Evergreen%20Creek/list
```

#### 3. Download Drawing
```
GET /api/drawings/{po_number}/{drawing_filename}
```
Download a specific PDF drawing.

**Example:**
```bash
curl http://localhost:8000/api/drawings/Evergreen%20Creek/Evergreen%20Creek_W-001_elevation.pdf \
  -o drawing.pdf
```

#### 4. Drawing Service Info
```
GET /api/drawings/
```
Get information about the drawing generation service.

#### 5. Cleanup Old Drawings
```
DELETE /api/drawings/{po_number}/cleanup?days_old=30
```
Remove drawings older than specified number of days.

---

### Health Check
```
GET /health
```
System health check.

**Response:**
```json
{"status": "healthy"}
```

---

## 🔄 Complete Workflow Example

### 1. Get Available Projects
```bash
curl http://localhost:8000/api/projects/po-numbers
```

### 2. Sync a Project
```bash
curl -X POST http://localhost:8000/api/projects/Evergreen%20Creek/sync
```

### 3. Verify Sync Status
```bash
curl http://localhost:8000/api/projects/Evergreen%20Creek/status
```

### 4. Generate PDF Drawings
```bash
curl -X POST http://localhost:8000/api/drawings/Evergreen%20Creek/generate
```

### 5. Download a Drawing
```bash
curl http://localhost:8000/api/drawings/Evergreen%20Creek/Evergreen%20Creek_W-001_elevation.pdf \
  -o window_drawing.pdf
```

---

## 📁 Generated Drawings

All PDFs are saved to: `./drawings/`

Naming convention: `{po_number}_{item_number}_{type}.pdf`

**Examples:**
- `Evergreen Creek_W-001_elevation.pdf` (Window)
- `Evergreen Creek_D-001_elevation.pdf` (Door)

Each drawing includes:
- Technical elevation view
- Dimension annotations
- Specification details
- Company title block
- Project information

---

## 🔧 Configuration

**Environment File**: `.env`

```bash
# Database
DATABASE_URL=sqlite:///./raven_drawings.db

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/service-account.json
GOOGLE_SHEET_ID=1AElaiVFJ2QD3lYdvX0-C7eHDq9sApbWT6ByRMPW42g0
GOOGLE_SHEET_NAME="!!Index"

# Environment
ENVIRONMENT=development
```

---

## 📊 Available Project Sheets

Your Google Sheet contains 140 project sheets:

**Sample Projects:**
1. Evergreen Creek
2. 2095 Alcova Ridge
3. Glasgow
4. Grand Rim Interior Doors
5. Vine Creek
6. Vista Crescent
7. Nour's Dad order
8. Calico Building 2
9. 2030 calico dr
10. ... and 130+ more

**To use a different project sheet, update `.env`:**
```bash
GOOGLE_SHEET_NAME="2095 Alcova Ridge"
```

Then restart the server.

---

## 🚀 Quick Start

### Start the Server
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Access the API
- Base URL: `http://127.0.0.1:8000`
- Interactive Docs: `http://127.0.0.1:8000/docs` (Swagger UI)
- ReDoc: `http://127.0.0.1:8000/redoc`

### Test the Flow
```bash
# 1. Get projects
curl http://localhost:8000/api/projects/po-numbers

# 2. Sync a project
curl -X POST http://localhost:8000/api/projects/Evergreen%20Creek/sync

# 3. Generate drawings
curl -X POST http://localhost:8000/api/drawings/Evergreen%20Creek/generate

# 4. Download drawing
curl http://localhost:8000/api/drawings/Evergreen%20Creek/list
```

---

## 📦 Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **Database**: SQLAlchemy + SQLite
- **Google Integration**: gspread 5.12.0 + Google Auth
- **PDF Generation**: ReportLab 4.0.7 + Matplotlib 3.9.2
- **Python**: 3.13

---

## 📝 Testing Scripts

### Test Google Sheets Integration
```bash
python test_sheets_integration.py
```

### Test PDF Drawing Generation
```bash
python test_drawing_generation.py
```

### Analyze Sheet Structure
```bash
python analyze_sheet_structure.py
```

---

## 🎯 Next Steps (Future Enhancements)

1. **Frontend React App**
   - Project selection interface
   - Real-time sync status
   - PDF preview viewer
   - Drawing management

2. **Advanced Drawing Features**
   - Cross-sections and details
   - 3D perspective views
   - Hardware specifications
   - Material callouts

3. **Data Export**
   - CSV export of project specs
   - Bill of materials (BOM)
   - Ordering system integration

4. **Project Management**
   - Job tracking dashboard
   - Revision control
   - Customer portal
   - Email delivery

---

## 🔐 Security Notes

- Service account credentials are stored locally (do not commit)
- All API endpoints are currently open (add authentication in production)
- PDF files are stored locally (consider cloud storage for production)
- Input validation should be enhanced for production use

---

## 📞 Support

For issues or questions:
1. Check the test scripts: `test_*.py`
2. Review the `.env` configuration
3. Verify Google Sheets sharing permissions
4. Check database file: `raven_drawings.db`

---

**Last Updated**: December 23, 2025  
**Status**: Production Ready MVP  
**API Version**: 1.0
