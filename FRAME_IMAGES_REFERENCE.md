# Frame Images & Full Screen - Quick Reference

## What Changed

### ✅ Frame Image Display
- Canvas now displays HEAD/SILL/JAMB frame images
- Images load from: `GET /api/frames/cross-sections/{series}`
- Images automatically scale to fit their sections
- Gray placeholder boxes shown if images missing

### ✅ Full Screen Mode
- Click blue "Full Screen" button to expand
- Canvas fills entire viewport
- Black background for better contrast
- Red "Exit Full Screen" button to return
- Header shows drawing info: "A4 Landscape - 86 36\" × 48\""
- Footer shows frame image status

### ✅ A4 Landscape Layout
- Canvas: 1122×794px at 96 DPI (matches PDF)
- Company header with Raven branding
- 3-column layout: frame sections | elevation/plan | info
- Elevation with dimension lines
- Plan view with person silhouette
- Specs table with 6 rows of data

### ✅ Real-Time Updates
- Series change: Images reload from API
- Width/Height change: Dimension lines update
- Configuration change: Panel grid updates
- All changes instant (no refresh needed)

---

## Component Structure

```
CanvasDrawingPreview
├── State
│   ├── frameImageUrls (URLs from API)
│   ├── frameImages (loaded HTMLImageElement objects)
│   └── isFullScreen (toggle state)
│
├── Effects
│   ├── Fetch URLs from API (on series change)
│   ├── Load images (on URL change)
│   └── Draw canvas (on parameter change)
│
├── Image Loaders
│   ├── loadHeadImage()
│   ├── loadSillImage()
│   └── loadJambImage()
│
├── Drawing Functions
│   ├── drawHeader() - Company branding
│   ├── drawMainContent() - 3 columns
│   ├── drawFrameCrossSections() - Frame images ✨
│   ├── drawPlaceholder() - Gray boxes
│   ├── drawElevationAndPlan() - Views + dimensions
│   ├── drawFrameTypeAndInfo() - Right column
│   ├── drawSpecsTable() - Bottom info
│   ├── drawDimensionLine() - Arrows + labels
│   └── drawPersonSilhouette() - Scale reference
│
└── Render
    ├── Normal Mode
    │   ├── Controls (Full Screen button)
    │   ├── Canvas (centered)
    │   └── Debug info
    │
    └── Full Screen Mode
        ├── Header (black bg, white text)
        ├── Canvas (centered, large)
        └── Footer (status info)
```

---

## Image Loading Flow

```
API Request
  ↓
GET /api/frames/cross-sections/86
  ↓
Response: {"head": "/static/frames/series-86-head.png", ...}
  ↓
Create Image() objects
  ↓
Load each image asynchronously
  ↓
onload → Update state
  ↓
Canvas re-renders
  ↓
drawImage() renders images in sections
```

---

## Status Indicators

### In Normal Mode (Bottom)
```
Canvas Size: 1122×794px (A4 Landscape at 96 DPI) | 
Frame Images: HEAD ✓ | SILL ✓ | JAMB ✓
```

### In Full Screen Mode (Footer)
```
A4 Landscape (1122×794px) | Frame Images: HEAD ✓ | SILL ✓ | JAMB ✓
```

### Legend
- ✓ = Image loaded successfully
- ✗ = Image not available (showing placeholder)

---

## File Locations

### Frame PNG Files
```
backend/static/frames/
├── series-86-head.png
├── series-86-sill.png
├── series-86-jamb.png
├── series-135-head.png
└── ...
```

### Component
```
frontend/src/components/sales/CanvasDrawingPreview.tsx
```

---

## Testing Quick Start

```bash
# 1. Organize frame images
cd backend
python organize_frame_assets.py

# 2. Start backend
uvicorn main:app --reload

# 3. Start frontend (new terminal)
cd frontend
npm start

# 4. Test
Open http://localhost:3000
- Series: 86
- Width: 36
- Height: 48
- Click "Full Screen"
```

---

## API Response Format

```
GET /api/frames/cross-sections/{series}

Success (200):
{
  "head": "/static/frames/series-86-head.png",
  "sill": "/static/frames/series-86-sill.png",
  "jamb": "/static/frames/series-86-jamb.png"
}

With missing files:
{
  "head": "/static/frames/series-86-head.png",
  "sill": null,
  "jamb": null
}
```

---

## Canvas Dimensions

| Format | Value |
|--------|-------|
| Physical | 297mm × 210mm (A4 Landscape) |
| Points | 842 × 595 (at 72 DPI - PDF standard) |
| Pixels | 1122 × 794 (at 96 DPI - browser standard) |
| File | CanvasDrawingPreview.tsx (620+ lines) |

---

## Features Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Frame images display | ✅ | HEAD/SILL/JAMB loaded from API |
| Image scaling | ✅ | Auto-fits to section boxes |
| Placeholder fallback | ✅ | Gray box if image missing |
| Full screen mode | ✅ | Black bg, full viewport |
| Real-time updates | ✅ | Series/width/height/config |
| A4 Landscape | ✅ | Matches PDF (842×595 points) |
| Company branding | ✅ | Header with contact info |
| Elevation view | ✅ | With dimension lines |
| Plan view | ✅ | With person silhouette |
| Specs table | ✅ | 6 rows dynamic data |
| Debug status | ✅ | Shows image load state |

---

## Troubleshooting

**Q: Images show as gray boxes**
A: Frame PNG files not found. Run `organize_frame_assets.py` and restart backend.

**Q: Full screen button doesn't work**
A: Click the blue "Full Screen" button at top right of canvas panel.

**Q: Series change doesn't load new images**
A: Ensure files exist: `backend/static/frames/series-{series}-head.png`

**Q: Canvas looks too small**
A: Use full screen mode for better view.

**Q: Images don't scale properly**
A: Images should have aspect ratio. Check PNG dimensions.

---

**Version:** 1.0
**Status:** ✅ Production Ready
**Last Updated:** 2024
