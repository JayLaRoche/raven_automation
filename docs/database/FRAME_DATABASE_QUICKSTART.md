# Frame Series Database Integration - Quick Start Guide

## What Was Built

Your frame series dropdown now pulls real data from your PostgreSQL database and displays frame preview images dynamically.

## 3-Step Setup

### Step 1: Start Backend
```bash
cd backend
python main.py
```
Expected output: API running on `http://localhost:8000`

### Step 2: Start Frontend
```bash
cd frontend
npm run dev
```
Expected output: Frontend running on `http://localhost:3001`

### Step 3: Open in Browser
Navigate to `http://localhost:3001`

## Test the Feature

1. **Open the Sales Presentation page**
2. **Look at left panel** - "Frame Series" dropdown
3. **Dropdown should show:**
   - Loading state initially
   - List of all series from your database
   - "Series 86", "Series 135", etc.

4. **Select a series** (e.g., "Series 86")
5. **Below the dropdown** - Frame preview image should appear
   - If image exists: Shows `/static/frames/series-86-thumbnail.png`
   - If no image: Shows "No preview image available"

## Add Frame Images

To display frame previews, add PNG images to:
```
backend/static/frames/
```

**Example filenames:**
- `series-86-thumbnail.png`
- `series-135-head.png`
- `series-65-sill.png`

Images will automatically appear in the dropdown when selected!

## Verify Database Connection

**Check backend is reading database:**

```bash
# Test the API endpoint directly
curl http://localhost:8000/api/frames/series-with-images

# Expected response:
# {
#   "series": [
#     {"id": "86", "name": "Series 86", "series": "86", "image_url": null},
#     {"id": "135", "name": "Series 135", "series": "135", "image_url": null},
#     ...
#   ]
# }
```

## How Frame Images Work

When you select a frame series:
1. Component finds that series in the data
2. Gets its `image_url` property
3. Displays the image from that URL
4. Backend serves it from `/static/frames/` directory

**Image Discovery Process:**
- Backend checks for `series-{number}-thumbnail.png` first
- Falls back to `series-{number}-head.png` if thumbnail not found
- Returns `null` if neither exists

## Troubleshooting

### "Dropdown shows 'Loading...'  forever"
**Solution:** Make sure backend is running on port 8000
```bash
cd backend
python main.py  # Check output for "Uvicorn running on"
```

### "Dropdown shows no options"
**Solution:** Check database has data in `frame_cross_sections` table
```sql
SELECT DISTINCT series FROM frame_cross_sections ORDER BY series;
```

### "Images don't appear"
**Solution:** Add frame images to `backend/static/frames/`
```bash
# Copy your PNG files to:
backend/static/frames/series-86-thumbnail.png
backend/static/frames/series-135-thumbnail.png
# etc...
```

### "Images show broken icon"
**Solution:** Restart backend server to ensure static files are mounted
```bash
# Kill current backend process
# Restart: python main.py
```

## Code Location Reference

| File | Purpose |
|------|---------|
| `backend/routers/frames.py` | New endpoint `/api/frames/series-with-images` |
| `frontend/src/services/api.js` | New function `getFrameSeriesWithImages()` |
| `frontend/src/components/sales/SmartParameterPanel.tsx` | Updated dropdown component |

## Full Documentation

See `FRAME_DATABASE_CONNECTION.md` for complete technical details.

## API Response Example

```json
{
  "series": [
    {
      "id": "86",
      "name": "Series 86",
      "series": "86",
      "image_url": "/static/frames/series-86-thumbnail.png"
    },
    {
      "id": "135",
      "name": "Series 135",
      "series": "135",
      "image_url": "/static/frames/series-135-head.png"
    },
    {
      "id": "65",
      "name": "Series 65",
      "series": "65",
      "image_url": null
    }
  ]
}
```

## Next Steps

1. ✅ Code implementation complete
2. ⏳ **Add frame PNG images** to `backend/static/frames/`
3. ⏳ **Populate database** (if not already done)
4. ⏳ **Test in browser** at http://localhost:3001
5. ⏳ **Verify images load** when selecting series

---

Ready to test? Start with Step 1 above! 🚀
