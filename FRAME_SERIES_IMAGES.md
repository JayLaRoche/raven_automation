# Frame Series Images - Implementation Guide

## Location of Frame Series Selection

The frame series selection list is located in:

**File**: [`frontend/src/components/sales/SmartParameterPanel.tsx`](frontend/src/components/sales/SmartParameterPanel.tsx)

**Lines**: ~104-119 (in the "Frame Series" section)

The component displays a 3-column grid of frame series buttons that users can click to select a series.

---

## How PNG Images Appear in Drawing Windows

### 1. **SmartParameterPanel Component** (Left Panel)
The frame series selector has been updated to display PNG images:
- Shows a thumbnail image (16px height) of each frame cross-section
- Falls back to emoji icons if image is not found
- Image is loaded from backend API endpoint

### 2. **Backend API Endpoint**
**Endpoint**: `GET /api/frames/series/{series}/image`

This endpoint:
- Looks for frame thumbnail images in `backend/static/frames/`
- Returns PNG image file for display
- Falls back to "head" cross-section if thumbnail not found
- Returns 404 if no image exists (frontend shows icon)

### 3. **Adding PNG Images**

To add frame series images to your app:

#### Step 1: Create Static Directory
```bash
mkdir -p backend/static/frames
```

#### Step 2: Add Frame Images
Place PNG images in `backend/static/frames/`:

```
backend/static/frames/
├── series-86-thumbnail.png      (Preferred)
├── series-86-head.png           (Fallback)
├── series-135-thumbnail.png
├── series-135-head.png
├── series-65-thumbnail.png
├── series-65-head.png
└── ... (one for each series)
```

#### Step 3: Image Specifications
- **Format**: PNG with transparent background
- **Dimensions**: Recommended 100px width × 60px height
- **Content**: Show frame cross-section (HEAD, SILL, JAMB views)
- **File Naming**: `series-{NUMBER}-{view}.png`

---

## Code Examples

### Frontend Component (SmartParameterPanel.tsx)

```tsx
function FrameSeriesButton({ series, isSelected, onClick }) {
  const [imageError, setImageError] = useState(false)
  const imageUrl = `/api/frames/series/${series}/image`
  
  return (
    <button onClick={onClick} className={...}>
      {!imageError ? (
        <img
          src={imageUrl}
          alt={`Frame Series ${series}`}
          onError={() => setImageError(true)}
          className="w-full h-16 object-contain mb-2 bg-white rounded"
        />
      ) : (
        <div>📋 {series}</div>
      )}
    </button>
  )
}
```

### Backend Endpoint (routers/frames.py)

```python
@router.get("/series/{series}/image")
async def get_series_thumbnail(series: str):
    """Get thumbnail image for frame series"""
    static_dir = 'backend/static/frames'
    file_path = f"{static_dir}/series-{series}-thumbnail.png"
    
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        raise HTTPException(status_code=404)
```

---

## Where Frame Images Display

1. **SmartParameterPanel** (Left side of app)
   - 3-column grid of frame series
   - Each button shows frame thumbnail
   - Click to select series for drawing generation

2. **Drawing Windows**
   - Canvas preview updates based on selected series
   - Shows actual frame cross-section dimensions
   - Referenced in dimension calculations

---

## Testing

### Test Without Images
App works with emoji fallbacks if no images provided.

### Test With Images
1. Add PNG files to `backend/static/frames/`
2. Restart backend server
3. Open app and check SmartParameterPanel
4. Images should appear in frame series buttons

---

## Current Status

✅ **Frontend Component**: Updated to load PNG images  
✅ **Backend Endpoint**: Added `/api/frames/series/{series}/image`  
⏳ **PNG Images**: Need to be added by user

---

## Next Steps

1. Gather or create frame cross-section PNG images
2. Place in `backend/static/frames/` directory
3. Name files as `series-{NUMBER}-{view}.png`
4. Restart backend server
5. View images in SmartParameterPanel
