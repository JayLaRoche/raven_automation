# Quick Reference: Canvas Drawing Preview Setup

## 🚀 5-Minute Setup

### Terminal 1: Organize Frame Images
```bash
cd backend
python organize_frame_assets.py
```

Expected output:
```
✅ ORGANIZED: 86-head.png → series-86-head.png
✅ ORGANIZED: 86-sill.png → series-86-sill.png
✅ ORGANIZED: 86-jamb.png → series-86-jamb.png
```

### Terminal 2: Start Backend
```bash
cd backend
uvicorn main:app --reload
```

Watch for:
```
✅ Static files mounted at /static
INFO:     Application startup complete
```

### Terminal 3: Start Frontend
```bash
cd frontend
npm start
```

---

## 📋 File Frame PNG Naming

### Required Format
```
series-{NUMBER}-{SECTION}.png

Examples:
- series-86-head.png
- series-86-sill.png
- series-86-jamb.png
- series-135-head.png
- series-135-sill.png
- series-135-jamb.png
```

### Also Accepts
```
{NUMBER}-{SECTION}.png

Examples:
- 86-head.png
- 86-sill.png
- 135-jamb.png

(Organizer script converts automatically)
```

### Valid Sections
- HEAD (top of frame)
- SILL (bottom of frame)
- JAMB (side of frame)

---

## 🧪 Quick Tests

### Test 1: Backend is serving static files
```bash
curl http://localhost:8000/static/frames/series-86-head.png
# Should return PNG file (binary data), NOT 404
```

### Test 2: API endpoint returns URLs
```bash
curl http://localhost:8000/api/frames/cross-sections/86
# Output:
# {"head":"/static/frames/series-86-head.png","sill":null,"jamb":null}
```

### Test 3: Canvas in browser
1. Open http://localhost:3000
2. Select Series: `86`
3. Should see frame image in HEAD section
4. Check bottom text: "Loaded Images: HEAD ✓"

---

## 🔧 Troubleshooting

| Symptom | Fix |
|---------|-----|
| "No Image" placeholder | Check `backend/static/frames/` has files |
| Files not organizing | Ensure source files in `backend/source_frames/` |
| Backend won't start | Run `pip install fastapi` |
| Canvas blank | Check browser console (F12) for errors |
| Images not loading | Restart backend with `Ctrl+C` |

---

## 📁 Directory Layout

```
raven-shop-automation/
├── backend/
│   ├── organize_frame_assets.py    ← Run this first
│   ├── main.py                      ← Runs with uvicorn
│   ├── static/
│   │   └── frames/                  ← Frame PNGs go here (created by organizer)
│   │       ├── series-86-head.png
│   │       ├── series-86-sill.png
│   │       └── ...
│   └── source_frames/               ← Put PNG files here (staging)
│       ├── 86-head.png
│       └── ...
│
└── frontend/
    └── src/
        └── components/sales/
            ├── CanvasDrawingPreview.tsx   ← Canvas component
            └── SalesPresentation.tsx      ← Uses canvas
```

---

## 💡 Common Commands

```bash
# Run organizer
python backend/organize_frame_assets.py

# Start backend
cd backend && uvicorn main:app --reload

# Start frontend
cd frontend && npm start

# Test API
curl http://localhost:8000/api/frames/cross-sections/86

# Check static files
ls -la backend/static/frames/

# View backend logs
# Watch Terminal 2 output
```

---

## 🎯 What You Should See

### In Canvas Preview:
- [ ] A4 Landscape layout (white page)
- [ ] Company header ("Drawn from inside view")
- [ ] Three frame sections (HEAD/SILL/JAMB) with images
- [ ] Elevation drawing with dimension lines
- [ ] Plan view with person silhouette
- [ ] Specs table with parameter values
- [ ] Status: "Canvas Size: 1122×794px"
- [ ] Status: "Loaded Images: HEAD ✓ | SILL ✓ | JAMB ✓"

### In Browser Console (F12):
- [ ] NO errors about CanvasDrawingPreview
- [ ] NO 404 errors for frame images
- [ ] No CORS errors

---

## ✅ Success Criteria

✅ All 3 servers running (backend, frontend, organizing complete)
✅ Frame PNGs in `backend/static/frames/`
✅ Canvas shows frame images
✅ No console errors
✅ PDF export still works

---

## 🚨 Emergency Troubleshooting

**If canvas is blank:**
1. Check browser console: F12 → Console tab
2. Look for red errors
3. Restart backend: `Ctrl+C` then `uvicorn main:app --reload`
4. Refresh browser: `Ctrl+F5`

**If images don't load:**
1. Verify files exist: `ls backend/static/frames/`
2. Check file names are lowercase: `series-86-head.png`
3. Run organizer again: `python organize_frame_assets.py`
4. Restart backend

**If API returns null URLs:**
1. Check files exist with correct names
2. Verify no typos in series number
3. Files must be in `backend/static/frames/` NOT elsewhere

---

## 📞 API Reference

### Get Frame Images
```
GET /api/frames/cross-sections/{series}
Response: {"head": "/static/frames/...", "sill": "...", "jamb": "..."}
```

### Access Frame Image
```
GET /static/frames/{filename}
Response: PNG binary data
```

### Canvas Component
```tsx
<CanvasDrawingPreview 
  parameters={{
    series: "86",
    width: 36,
    height: 48,
    productType: "CASEMENT",
    glassType: "Clear Low E",
    frameColor: "White"
  }}
  onPresentationMode={() => {}}
/>
```

---

**Last Updated:** 2024 | **Version:** 1.0
