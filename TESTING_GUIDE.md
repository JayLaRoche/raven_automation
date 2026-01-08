# Testing Guide: Canvas Drawing Preview Implementation

## Pre-Testing Checklist

- [ ] Backend server installed and working
- [ ] Frontend server installed and working
- [ ] Frame PNG files available (or create test files)
- [ ] All three servers ready to start (Terminal 1, 2, 3)

---

## Test Phase 1: Backend Static Files

### Test 1.1: Verify Static Directory Creation
```bash
# Expected: Directory exists and is empty
ls -la backend/static/
# Should show: frames/ subdirectory exists

ls -la backend/static/frames/
# Should show: empty initially (or files if you ran organizer)
```

### Test 1.2: Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```

**Expected Output:**
```
✅ Database tables created/verified
✅ Static files mounted at /static
INFO:     Application startup complete
```

**If you see warnings instead:**
```
⚠️ Database connection not available (This is OK!)
✅ Using fallback mode - frames endpoint will return default data
```

---

## Test Phase 2: Frame Asset Organization

### Test 2.1: Create Test Frame PNG Files
```bash
cd backend

# Create source_frames directory if not exists
mkdir -p source_frames

# Copy your actual frame PNGs here, OR
# Create dummy test files:

# Create 1x1 pixel PNG files for testing
# (Just for verifying the system works)
```

### Test 2.2: Run Organizer Script
```bash
cd backend
python organize_frame_assets.py
```

**Expected Output:**
```
============================================================
FRAME ASSETS ORGANIZATION SCRIPT
============================================================

📁 Source directory:  C:\...\raven-shop-automation\backend\source_frames
📁 Output directory:  C:\...\raven-shop-automation\backend\static\frames

🔍 Found 6 PNG file(s)
────────────────────────────────────────────────────────────
✅ ORGANIZED: 86-head.png
   → series-86-head.png
✅ ORGANIZED: 86-sill.png
   → series-86-sill.png
✅ ORGANIZED: 86-jamb.png
   → series-86-jamb.png
...

============================================================
SUMMARY
============================================================
✅ Organized:  6 file(s)
⏭️  Skipped:    0 file(s)
❌ Errors:     0 file(s)
============================================================
```

### Test 2.3: Verify Organized Files
```bash
# Check that files were copied
ls -la backend/static/frames/

# You should see:
# series-86-head.png
# series-86-sill.png
# series-86-jamb.png
# (and any other series you organized)
```

---

## Test Phase 3: API Endpoints

### Test 3.1: Backend Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### Test 3.2: Frame Cross-Sections Endpoint
```bash
curl http://localhost:8000/api/frames/cross-sections/86
```

**Expected Response (with files):**
```json
{
  "head": "/static/frames/series-86-head.png",
  "sill": "/static/frames/series-86-sill.png",
  "jamb": "/static/frames/series-86-jamb.png"
}
```

**Expected Response (without files):**
```json
{
  "head": null,
  "sill": null,
  "jamb": null
}
```

### Test 3.3: Static File Serving
```bash
# Test if static files are accessible
curl -I http://localhost:8000/static/frames/series-86-head.png
```

**Expected Response:**
```
HTTP/1.1 200 OK
content-length: 12345
content-type: image/png
```

**Or if file missing:**
```
HTTP/1.1 404 Not Found
```

---

## Test Phase 4: Frontend Integration

### Test 4.1: Start Frontend Server
```bash
cd frontend
npm start
```

**Expected Output:**
```
webpack compiled successfully
Compiled successfully!

You can now view raven-shop-automation in the browser.

  Local:            http://localhost:3000
```

### Test 4.2: Open in Browser
```
Navigate to: http://localhost:3000
```

### Test 4.3: Open Browser Developer Console
```
Press: F12 (or Ctrl+Shift+I)
Click: Console tab

Expected: NO red error messages
Any yellow warnings are usually OK
```

---

## Test Phase 5: Canvas Drawing Preview

### Test 5.1: Fill in Drawing Parameters
In the left panel (SmartParameterPanel):
- [ ] Series: `86` (or your series number)
- [ ] Width: `36` (inches)
- [ ] Height: `48` (inches)
- [ ] Product Type: `CASEMENT`
- [ ] Glass Type: `Clear Low E`
- [ ] Frame Color: `White`
- [ ] Configuration: `O` (single pane)

### Test 5.2: Verify Canvas Display
Look at the right panel (Canvas Drawing Preview):

Should see:
- [ ] White canvas with dark border
- [ ] "Drawn from inside view" text (top left)
- [ ] Company info block (top right):
  - [ ] "▶ raven"
  - [ ] "9960 W Cheyenne ave"
  - [ ] "Suite 140 Las Vegas NV 89129"
  - [ ] "Cell: 702-577-1003"
  - [ ] "Website: ravencustomglass.com"

### Test 5.3: Verify Frame Sections
In the left column of the canvas:
- [ ] HEAD label with image or gray placeholder
- [ ] SILL label with image or gray placeholder
- [ ] JAMB label with image or gray placeholder

### Test 5.4: Verify Elevation View
In the middle column:
- [ ] "ELEVATION" title
- [ ] Window frame drawing
- [ ] Panel dividers (1 divider for 'O' config)
- [ ] Dimension line at top: "36""
- [ ] Dimension line at right: "48""

### Test 5.5: Verify Plan View
Below elevation:
- [ ] "PLAN" title
- [ ] Small frame profile
- [ ] Person silhouette for scale

### Test 5.6: Verify Frame Type & Info
In right column:
- [ ] "FRAME TYPE" title
- [ ] 4 small icon boxes (empty is OK)
- [ ] Info table:
  - [ ] Drawing date: (today's date)
  - [ ] Serial number: (parameter value or 'P001')
  - [ ] Designer: Construction
  - [ ] Revision: (today's date)

### Test 5.7: Verify Specs Table
At the bottom:
- [ ] "SPECIFICATIONS" title
- [ ] Table with 6 rows:
  1. Glass | Clear Low E (or your value)
  2. Frame Color | White (or your value)
  3. Frame Series | Series 86 CASEMENT
  4. Elevation Detail | Stucco setback 35mm from outside
  5. Dimensions | 36" × 48"
  6. Special Notes | (empty)

### Test 5.8: Verify Debug Info
At the very bottom:
- [ ] "Canvas Size: 1122×794px (A4 Landscape at 96 DPI)"
- [ ] "Loaded Images: HEAD ✓ | SILL ✓ | JAMB ✓" (if files exist)
- [ ] Or: "Loaded Images: HEAD ✗ | SILL ✗ | JAMB ✗" (if files missing)

### Test 5.9: Test Parameter Changes
Change one parameter at a time and verify canvas updates:

1. **Change Series** (86 → 135):
   - Specs table updates (Series 135)
   - Images try to load from `/api/frames/cross-sections/135`
   - Placeholder shows if series-135 files don't exist

2. **Change Width** (36 → 42):
   - Dimension line changes (42")
   - Specs table updates (42" × 48")

3. **Change Height** (48 → 60):
   - Dimension line changes (60")
   - Specs table updates (42" × 60")

4. **Change Configuration** (O → CO):
   - Elevation window updates (2 panels instead of 1)

5. **Change Glass Type** (Clear Low E → Tinted):
   - Specs table updates

Each change should update canvas instantly without errors.

---

## Test Phase 6: Browser Console Verification

### Test 6.1: Check for Errors
Press: F12 → Console tab

**Should see NO red messages like:**
```
❌ Failed to load /api/frames/cross-sections/86
❌ Cannot read properties of undefined
❌ CORS error
```

**Yellow warnings are usually OK**

### Test 6.2: Check for Image Load Warnings
You might see:
```
⚠️ Failed to load image: /static/frames/series-86-head.png
```

This is OK if frame files don't exist yet. Canvas will show placeholder.

### Test 6.3: Check Backend Logs
Look at Terminal running backend (uvicorn):

You should see requests like:
```
INFO:     GET /api/frames/cross-sections/86 HTTP/1.1" 200
INFO:     GET /static/frames/series-86-head.png HTTP/1.1" 200 or 404
```

---

## Test Phase 7: PDF Export (Verify Backward Compatibility)

### Test 7.1: Export PDF
1. Click "Export" button
2. Select "Reference Shop Drawing"
3. PDF should download

### Test 7.2: Verify PDF
- [ ] PDF opens successfully
- [ ] Layout matches canvas exactly
- [ ] Same A4 Landscape orientation
- [ ] File size ~75KB (acceptable)

---

## Test Phase 8: Full Screen Mode

### Test 8.1: Present Drawing
1. In Canvas Drawing Preview panel
2. Click "Full Screen" button
3. Canvas should expand to full browser window

### Test 8.2: Exit Full Screen
1. Click anywhere on canvas or
2. Press ESC key
3. Should return to normal 2-column layout

---

## Troubleshooting During Testing

### Canvas is Blank (White Box Only)
**Possible Causes:**
1. Frontend not connected to backend
2. API endpoint not responding
3. Canvas rendering function errored

**Solutions:**
```bash
# 1. Check backend is running
curl http://localhost:8000/health
# Should return: {"status": "healthy"}

# 2. Check console for errors
# F12 → Console tab

# 3. Restart both servers
# Backend: Ctrl+C then uvicorn main:app --reload
# Frontend: Ctrl+C then npm start
```

### Frame Images Show as Gray Boxes
**This is NORMAL if you haven't provided frame PNGs yet**

To see actual images:
1. Provide frame PNG files
2. Copy to `backend/source_frames/`
3. Run `python organize_frame_assets.py`
4. Restart backend
5. Refresh browser

### Console Shows Image Load Errors
**Expected messages:**
```
⚠️ Failed to load image: /static/frames/series-86-head.png
```

**Means:** Frame PNG files not found. This is OK, canvas shows placeholder.

**To fix:** Run organizer script with actual PNG files.

### "Cannot read properties of undefined" Error
**Check:**
1. Are all drawing parameters set?
2. Is series number filled in?
3. Refresh page (Ctrl+F5)
4. Restart both servers

### API Returns 404 on Static Files
**Check:**
```bash
# 1. Files exist
ls backend/static/frames/

# 2. File names are correct (lowercase)
# Should be: series-86-head.png (not series-86-HEAD.png)

# 3. Backend restarted after organizing
```

---

## Success Criteria Checklist

If all these pass, your implementation is working correctly:

- [ ] Backend server starts with "✅ Static files mounted"
- [ ] Organizer script runs without errors
- [ ] Frame files appear in `backend/static/frames/`
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Frame endpoint returns image URLs (or nulls)
- [ ] Frontend loads at localhost:3000
- [ ] No red errors in browser console
- [ ] Canvas displays full A4 layout
- [ ] Specs table shows correct parameters
- [ ] Dimension lines show correct sizes
- [ ] Parameter changes update canvas instantly
- [ ] PDF export still works
- [ ] Full screen mode works

**If all are checked:** ✅ Implementation is complete and working!

---

## Quick Failure Recovery

| Issue | Quick Fix |
|-------|-----------|
| Canvas blank | Restart backend: `Ctrl+C` → `uvicorn main:app --reload` |
| Images show as gray | Run organizer: `python organize_frame_assets.py` |
| Endpoint 404 | Check file names are lowercase |
| Console errors | Press F12, look for red messages, check backend logs |
| API returns nulls | Verify files in `backend/static/frames/` |
| Parameter change doesn't update | Refresh page: `Ctrl+F5` |
| Backend won't start | Check for port conflicts: `lsof -i :8000` |
| Frontend won't load | Check port 3000 is available: `lsof -i :3000` |

---

## Performance Testing (Optional)

### Test Canvas Render Time
1. Right-click on canvas
2. Select "Inspect" (or press F12 + click canvas)
3. Open Performance tab
4. Record a short session
5. Change a parameter
6. Stop recording
7. Look for render time (should be <50ms)

### Test Image Load Time
1. F12 → Network tab
2. Change series number
3. Look for `/api/frames/cross-sections/XXX` request
4. Should be <10ms
5. Image files should load within 100ms

---

**Testing Complete!** When all tests pass, your implementation is production-ready.
