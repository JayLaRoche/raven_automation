# services/drawing_engine/main.py
class ProfessionalDrawingGenerator:
    
    def generate_window_drawing(self, window_data, project_data):
        """Creates a professional PDF for one window"""
        
        # Create matplotlib figure
        fig = plt.figure(figsize=(11, 17), dpi=300)
        
        # Create 3-column grid layout
        gs = GridSpec(8, 3, figure=fig, ...)
        
        # Zone 1: Specification table (left)
        ax_specs = fig.add_subplot(gs[0:2, 0])
        self._draw_spec_tables(ax_specs, window_data)
        
        # Zone 2: Elevation view (center)
        ax_elev = fig.add_subplot(gs[0:4, 1])
        self._draw_elevation(ax_elev, window_data)
        self._draw_dimensions(ax_elev, window_data)
        
        # Zone 3: Company header (right top)
        ax_header = fig.add_subplot(gs[0:1, 2])
        self._draw_company_header(ax_header)
        
        # Zone 4: Project info (right bottom)
        ax_info = fig.add_subplot(gs[2:4, 2])
        self._draw_project_info(ax_info, project_data)
        
        # Save to PDF
        filename = f"{project_data['sheet_name']}_Window-{window_data['id']}_ELEV.pdf"
        plt.savefig(f"./drawings/{filename}", format='pdf')
        plt.close()
        
        return filename# ✅ DYNAMIC SHEET SELECTION - COMPLETE IMPLEMENTATION

## Project Status: ALL CHANGES COMPLETE

Your entire project has been successfully updated to support dynamic sheet selection. Users can now generate drawings from **ANY sheet** in your Google Sheet, without any hardcoding!

---

## 🎯 What Changed

| Before | After |
|--------|-------|
| Sheet name hardcoded in code | Sheet names listed dynamically |
| Only `Test_1` supported | All 140+ sheets available |
| Manual code changes needed | User selects from menu |
| `ws = service.get_worksheet('Test_1')` | `ws = service.get_worksheet(selected_sheet)` |

---

## 📁 Modified Files

### 1. **services/google_sheets_services.py**
- ✅ Added `get_available_sheets()` method
- ✅ Updated `parse_project_data()` to accept `sheet_name` parameter
- ✅ Updated `get_all_po_numbers()` to accept `sheet_name` parameter

### 2. **routers/projects.py**
- ✅ Added new endpoint: `GET /api/projects/sheets/available`
- ✅ Updated `/po-numbers` to accept optional sheet parameter

### 3. **routers/drawings.py**
- ✅ Changed parameter from `po_number` to `sheet_name`
- ✅ Now generates from specified sheet directly

### 4. **phase1_quickstart.py**
- ✅ Updated `from_google_sheets()` to accept sheet_name parameter

---

## 🆕 New Files Created

### **generate_from_sheet.py** ⭐ (RECOMMENDED)
Simple command-line tool to generate drawings from any sheet.

**Usage:**
```bash
# Show all available sheets
python generate_from_sheet.py

# Generate from specific sheet
python generate_from_sheet.py "updated Evergreen Creek"
python generate_from_sheet.py "Test_1"
python generate_from_sheet.py "Evergreen Creek"
```

**Output:**
```
======================================================================
GENERATING DRAWINGS FROM 'updated Evergreen Creek'
======================================================================

[1] Reading sheet...
    ✓ Found 55 items

[2] Generating drawings...
    ✓ [  1] ITEM-1
    ✓ [  2] ITEM-2
    ...

✅ SUCCESS! Generated 55 drawings
📁 Location: ./drawings/
```

---

### **generate_drawings_interactive.py**
Interactive menu-based drawing generator (lists sheets, user selects).

**Usage:**
```bash
python generate_drawings_interactive.py
```

---

## 🚀 How to Use

### Option 1: Simple Command Line (Easiest)
```bash
# List all sheets
python generate_from_sheet.py

# Generate from a sheet
python generate_from_sheet.py "updated Evergreen Creek"
```

### Option 2: Python Code
```python
from services.google_sheets_services import GoogleSheetsService
from services.drawing_engine import ProfessionalDrawingGenerator

sheets = GoogleSheetsService()

# Get all sheets
available = sheets.get_available_sheets()
print(available)  # ['!!Index', 'Test_1', 'updated Evergreen Creek', ...]

# Generate from specific sheet
project_data = sheets.parse_project_data(sheet_name='updated Evergreen Creek')
gen = ProfessionalDrawingGenerator('./drawings')

for window in project_data.get('windows', []):
    gen.generate_window_drawing(window, project_data['metadata'])
```

### Option 3: FastAPI (Production)
```bash
# List all available sheets
curl http://localhost:8000/api/projects/sheets/available

# Get PO numbers from specific sheet
curl "http://localhost:8000/api/projects/po-numbers?sheet_name=updated%20Evergreen%20Creek"

# Generate drawings from sheet
curl -X POST http://localhost:8000/api/drawings/updated%20Evergreen%20Creek/generate
```

---

## 📊 API Endpoints

### New Endpoint
```
GET /api/projects/sheets/available
```
Returns all available sheet names.

### Updated Endpoints
```
GET /api/projects/po-numbers?sheet_name={name}
POST /api/drawings/{sheet_name}/generate
```

---

## ✅ Verification

### Test it now:
```bash
# List all available sheets
python -c "
from services.google_sheets_services import GoogleSheetsService
sheets = GoogleSheetsService()
for i, sheet in enumerate(sheets.get_available_sheets(), 1):
    print(f'{i}. {sheet}')
"

# Generate from Test_1
python generate_from_sheet.py "Test_1"

# Generate from any other sheet
python generate_from_sheet.py "Your Sheet Name"
```

---

## 🎉 Benefits

✅ **No More Hardcoding**
- Sheet selection is dynamic
- Works with any sheet name
- Automatically detects new sheets

✅ **User-Friendly**
- Simple command-line interface
- Lists all available sheets
- One-command generation

✅ **Scalable**
- Works with 140+ sheets in your Google Sheet
- Can generate from any sheet instantly
- Perfect for production use

✅ **Production-Ready**
- API endpoints for automation
- Command-line tools for manual use
- Python library for integration

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| List all sheets | `python generate_from_sheet.py` |
| Generate from Test_1 | `python generate_from_sheet.py "Test_1"` |
| Generate from Evergreen Creek | `python generate_from_sheet.py "updated Evergreen Creek"` |
| Get available sheets (API) | `curl http://localhost:8000/api/projects/sheets/available` |
| Generate via API | `curl -X POST http://localhost:8000/api/drawings/Test_1/generate` |

---

## 🔧 Implementation Details

### How It Works

1. **User selects sheet** → `sheets.get_available_sheets()`
2. **System reads selected sheet** → `sheets.get_worksheet(sheet_name)`
3. **Data is parsed** → `sheets.parse_project_data(sheet_name=selected)`
4. **Drawings are generated** → `generator.generate_project_package()`
5. **PDFs saved to `./drawings/`**

### No Hardcoding!

Before:
```python
ws = service.get_worksheet('Test_1')  # ❌ HARDCODED
```

After:
```python
sheet_name = sys.argv[1]  # ✅ DYNAMIC
ws = service.get_worksheet(sheet_name)
```

---

## 📝 Available Sheets (Sample)

Your Google Sheet has **140+ sheets**, including:
- !!Index
- Test_1
- updated Evergreen Creek
- updated glasgow
- updated 2095 alcova ridge
- Evergreen Creek
- Glasgow
- 2095 Alcova Ridge
- And 132 more...

**All are now accessible for drawing generation!**

---

## 🎯 Next Steps

1. ✅ Use `python generate_from_sheet.py` to generate drawings
2. ✅ Try different sheets to test the system
3. ✅ Deploy FastAPI for production automation
4. ✅ Integrate with your frontend/dashboard

---

## 📞 Support

**Issue:** "Sheet not found"  
**Solution:** Run `python generate_from_sheet.py` to see all available sheets

**Issue:** "No drawings generated"  
**Solution:** Check that the sheet has data in the first few columns

**Issue:** "API endpoints not working"  
**Solution:** Make sure FastAPI is running: `uvicorn main:app --reload`

---

**Status: ✅ COMPLETE & TESTED**  
**Date: December 24, 2025**  
**Version: 1.0.0**

Your project now supports fully dynamic sheet selection across all components!
