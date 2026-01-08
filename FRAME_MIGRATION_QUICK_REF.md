# Frame Images - Quick Reference Guide

## What Was Done

✅ **Task 1**: Created `import_frames.ps1` - Migrates images from frame library  
✅ **Task 2**: Updated `CanvasDrawingPreview.tsx` - Loads images with correct URLs

---

## Quick Start

### Run the Migration Script

```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation
.\import_frames.ps1
```

**Result**: 19 frame images copied from `backend/frame_library/` to `backend/static/frames/` with proper naming.

---

## Naming Convention

### Source → Destination

| From | To | Example |
|------|----|----|
| `Series_86_a.PNG` | `series_86_HEAD.png` | Top profile |
| `Series_86_b.PNG` | `series_86_SILL.png` | Bottom sill |
| `Series_86_c.PNG` | `series_86_JAMB.png` | Side jamb |
| `Series_86_d.PNG` | ⊘ SKIPPED | Non-standard |

### Format Rules

```
series_{NUMBER}_{VIEW}.png

↓ lowercase
series_

↓ number as-is
86

↓ uppercase view type
HEAD, SILL, or JAMB

↓ lowercase extension
.png
```

---

## Frontend Logic

**File**: `frontend/src/components/sales/CanvasDrawingPreview.tsx` (Lines 105-122)

```typescript
// Input from dropdown: "Series 86"
const cleanSeries = parameters.series.replace(/Series\s*/i, '').trim()  // "86"

// Construct URLs
setFrameImageUrls({
  head: `/static/frames/series_86_HEAD.png`,
  sill: `/static/frames/series_86_SILL.png`,
  jamb: `/static/frames/series_86_JAMB.png`,
})

// Load images with CORS support
headImg.crossOrigin = 'anonymous'
```

---

## Available Images

| Series | Views | Status |
|--------|-------|--------|
| 58 | HEAD, SILL, JAMB | ✅ Complete |
| 65 | HEAD, SILL, JAMB | ✅ Complete |
| 68 | HEAD, SILL, JAMB | ✅ Complete |
| 86 | HEAD, SILL | ⚠️ JAMB missing |
| 135 | HEAD, SILL, JAMB | ✅ Complete |
| 150 | HEAD, SILL, JAMB | ✅ Complete |
| 4518 | HEAD, SILL | ⚠️ JAMB missing |

---

## Testing

Navigate to: `http://localhost:3000/generator`

1. Open dropdown → Select "Series 86"
2. Open DevTools (F12) → Network tab
3. Should see image requests: `series_86_HEAD.png`, `series_86_SILL.png`
4. Canvas displays frame cross-sections
5. Console: No errors

---

## Adding New Images

1. Copy images to: `backend/frame_library/`
2. Use naming: `Series_{NUMBER}_{LETTER}.PNG` (a=HEAD, b=SILL, c=JAMB)
3. Run: `.\import_frames.ps1`
4. Restart backend: `uvicorn main:app --reload`
5. New series appears in dropdown

---

## Files Modified

- ✅ `import_frames.ps1` - Migration script updated to support frame_library
- ✅ `CanvasDrawingPreview.tsx` - URL construction and CORS configured
- ✅ Files created for documentation and tracking

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Images not loading | Restart backend server |
| CORS errors | Already configured with `crossOrigin='anonymous'` |
| File not found | Check filename format matches exactly |
| Blank canvas | Check browser console for image load errors |

---

## Summary

✅ **Status**: Production Ready  
✅ **19 images** available across 7 series  
✅ **Proper naming** with underscores and uppercase views  
✅ **CORS configured** for canvas access  
✅ **Error handling** for failed loads  
✅ **Migration script** ready for future additions  

The application is ready to load and display frame cross-sections in the Drawing Generator!
