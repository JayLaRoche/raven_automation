# Reference Layout PDF - Quick Start Guide

## 🚀 Quick Test (2 minutes)

### Step 1: Start Servers
```bash
# Backend (if not running)
cd C:\Users\larochej3\Desktop\raven-shop-automation\backend
python -m uvicorn main:app --reload --port 8000

# Frontend (if not running)
cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend
npm run dev
```

Both servers should be running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Step 2: Open App
Visit: **http://localhost:3000** in your browser

### Step 3: Generate PDF

1. **Fill in Parameters** (left panel):
   - Frame Series: Select "65" or "86"
   - Product Type: Select "CASEMENT"
   - Width: Enter "48"
   - Height: Enter "60"
   - Glass Type: Select "Clear Low E Dual Pane"
   - Frame Color: Select "Black"

2. **Generate PDF**:
   - Click green **"📄 Generate PDF"** button in header
   - Wait for PDF to generate (~3 seconds)
   - App automatically switches to PDF view

3. **View & Download**:
   - PDF displays in full-screen viewer
   - Use zoom controls (-, +, Fit)
   - Click **"📥 Download"** to save locally
   - Filename: `P001_drawing.pdf` (or uses your item number)

### Step 4: Verify Layout

Check that PDF matches reference exactly:

✅ **Header Section**
- "Drawn from inside view" text in top left
- Raven company info block in top right with:
  - ▶ raven logo
  - Address: 9960 W Cheyenne ave
  - Suite 140, Las Vegas NV 89129
  - Phone: 702-577-1003
  - Website: ravencustomglass.com

✅ **Three-Column Layout**
- **Left (30%):** Frame cross-sections (HEAD, SILL, JAMB) with labels and placeholders
- **Center (37%):** Elevation view (top) with panel grid, Plan view (bottom) with person silhouette
- **Right (28%):** Frame type icons (highlighted for CASEMENT), Drawing info table

✅ **Bottom Section**
- Specifications table with 6 rows:
  - Glass: Clear Low E Dual Pane
  - Frame Color: Black
  - Frame Series: Series 65 CASEMENT
  - Elevation Detail: (from notes)
  - Dimensions: 48" × 60"
  - Special Notes: N/A

✅ **Professional Quality**
- Crisp black text on white background
- Proper line weights (bold outer frame, thin details)
- Dimension arrows and labels correctly positioned
- All information readable at various zoom levels

## 📋 Parameter Examples

### Example 1: Standard Window
```json
{
  "series": "65",
  "product_type": "CASEMENT",
  "width": 48.0,
  "height": 60.0,
  "glass_type": "Clear Low E Dual Pane",
  "frame_color": "Black",
  "configuration": "XO",
  "item_number": "WIN-001",
  "po_number": "PO-2025-001",
  "notes": "Stucco setback 35mm from outside"
}
```

### Example 2: Fixed Window
```json
{
  "series": "86",
  "product_type": "FIXED",
  "width": 72.0,
  "height": 48.0,
  "glass_type": "Clear Low E Triple Pane",
  "frame_color": "Bronze",
  "configuration": "O",
  "item_number": "WIN-002",
  "po_number": "PO-2025-001",
  "notes": "Brick opening, no setback"
}
```

### Example 3: Slider Door
```json
{
  "series": "135",
  "product_type": "SLIDER",
  "width": 60.0,
  "height": 84.0,
  "glass_type": "Clear Low E Dual Pane",
  "frame_color": "White",
  "configuration": "XO",
  "item_number": "DOOR-001",
  "po_number": "PO-2025-002",
  "notes": "Patio door, no sill pan required"
}
```

## 🔄 Switching Between Views

### Canvas View (Fast Preview)
- Click **"📐 Canvas"** button in header
- Shows real-time parameter adjustments
- PNG export available
- Quicker for iterations

### PDF View (Professional Output)
- Click **"📄 PDF"** button in header
- Shows reference layout drawing
- Zoom, pan, download controls
- Print-ready quality
- Exact match to fabrication drawings

## ⚡ Keyboard Shortcuts

While in Canvas view:
- **Cmd+G** or **Ctrl+G**: Generate drawing
- **Cmd+E** or **Ctrl+E**: Open export dialog
- **Cmd+P** or **Ctrl+P**: Toggle presentation mode

## 🐛 Troubleshooting

### PDF Not Appearing
1. Check browser console (F12)
2. Verify backend is running (http://localhost:8000)
3. Try refreshing browser (Cmd+R or Ctrl+R)
4. Check network tab for failed requests

### PDF Generation Error
1. Ensure all required parameters filled
2. Check series number is valid (65, 80, 86, 135, etc.)
3. Width and height must be positive numbers
4. Try with default parameters first

### PDF Looks Blurry
1. The display might need zoom adjustment
2. Download and open in native PDF reader for full quality
3. Print quality is always 300 DPI (sharp)

### Layout Not Matching Reference
1. Check page size (should be A3 Landscape)
2. Verify browser PDF viewer is showing full page
3. Compare with reference file pixel-by-pixel
4. Report discrepancies with screenshot

## 📊 Testing Checklist

- [ ] PDF generates without errors
- [ ] Layout matches reference (3 columns)
- [ ] Header with company info displays correctly
- [ ] Frame series labels show (HEAD, SILL, JAMB)
- [ ] Elevation view shows panel grid correctly
- [ ] Plan view shows person silhouette
- [ ] Drawing info table shows current date
- [ ] Specifications table shows all parameters
- [ ] Dimension lines and arrows display correctly
- [ ] All text is readable and properly sized
- [ ] PDF can be downloaded successfully
- [ ] Downloaded PDF opens in PDF reader
- [ ] Zoom controls work in viewer
- [ ] Print preview shows correct layout

## 🎯 Success Criteria

Your implementation is complete when:

1. ✅ PDF is generated in ~3 seconds
2. ✅ Layout matches reference exactly (side-by-side comparison)
3. ✅ All 6 sections present and correctly positioned
4. ✅ No layout warnings or errors in console
5. ✅ PDF is downloadable and opens correctly
6. ✅ Print preview shows proper page size (A3 Landscape)
7. ✅ Can switch between Canvas and PDF views seamlessly
8. ✅ Parameters update drawing immediately

## 📞 API Testing (Advanced)

### Direct API Call (cURL)

```bash
# Generate PDF via API
curl -X POST http://localhost:8000/api/drawings/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "series": "65",
    "product_type": "CASEMENT",
    "width": 48,
    "height": 60,
    "glass_type": "Clear Low E Dual Pane",
    "frame_color": "Black",
    "configuration": "XO",
    "item_number": "P001",
    "po_number": "PO-2025-001",
    "notes": "Stucco setback 35mm"
  }' --output drawing.pdf

# Open the downloaded PDF
open drawing.pdf  # macOS
xdg-open drawing.pdf  # Linux
start drawing.pdf  # Windows
```

### Python API Test

```python
import requests
import json

url = "http://localhost:8000/api/drawings/generate-pdf"
params = {
    "series": "65",
    "product_type": "CASEMENT",
    "width": 48.0,
    "height": 60.0,
    "glass_type": "Clear Low E Dual Pane",
    "frame_color": "Black",
    "configuration": "XO",
    "item_number": "P001",
    "po_number": "PO-2025-001",
    "notes": "Stucco setback 35mm from outside"
}

response = requests.post(url, json=params)

if response.status_code == 200:
    with open('drawing.pdf', 'wb') as f:
        f.write(response.content)
    print("✅ PDF generated successfully!")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

## 📝 Notes

- Frame cross-section images are placeholders when database unavailable
- Actual frame images can be loaded from database once CAD library is imported
- Layout proportions and grid structure are exact per specification
- All text styling and positioning matches reference
- PDF is optimized for web delivery and printing

---

**Ready to test?** Start with Step 1 above!
