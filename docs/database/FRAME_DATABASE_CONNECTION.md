# Frame Series Database Connection - Implementation Complete

## Summary
Successfully connected the frame series dropdown to your database and implemented dynamic image loading from the database.

## Changes Made

### 1. Backend API Enhancement (`backend/routers/frames.py`)
**New Endpoint Added:** `/api/frames/series-with-images`

```python
@router.get("/series-with-images")
async def get_frame_series_with_images(db: Session = Depends(get_db)):
    """
    Get list of available frame series with their image URLs
    Frontend uses this to populate dropdown with images
    """
```

**What it does:**
- Queries the database for all distinct frame series
- Checks `backend/static/frames/` directory for frame images
- Returns frame series list with image URLs
- Falls back to default series if database is empty

**Response Format:**
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
    }
  ]
}
```

### 2. Frontend API Service (`frontend/src/services/api.js`)
**New Function Added:**

```javascript
export const getFrameSeriesWithImages = async () => {
  const response = await api.get('/api/frames/series-with-images')
  return response.data
}
```

### 3. SmartParameterPanel Component (`frontend/src/components/sales/SmartParameterPanel.tsx`)
**Updated with:**

1. **New Import:**
   ```typescript
   import { getFrameSeriesWithImages } from '../../services/api'
   ```

2. **Updated Query Hook:**
   ```typescript
   const { data: frameSeriesData, isLoading: isLoadingFrameSeries } = useQuery({
     queryKey: ['frameSeriesWithImages'],
     queryFn: getFrameSeriesWithImages,
   })
   ```

3. **Enhanced Frame Series Dropdown:**
   - Displays loading state while fetching from database
   - Shows all frame series from database
   - Displays frame preview image below dropdown when selected
   - Falls back to "No preview image available" if image URL is null

4. **Image Preview Section:**
   - Shows frame thumbnail/head image when series is selected
   - Image URL comes directly from database via API
   - Gracefully handles missing images with fallback text
   - Images are served from `/static/frames/` directory

## How It Works

### Data Flow:
1. **Component Mounts** → Query triggered
2. **Frontend Calls API** → `GET /api/frames/series-with-images`
3. **Backend Queries DB** → Gets distinct series from `frame_cross_sections` table
4. **Backend Checks Static Files** → Looks for frame images in `backend/static/frames/`
5. **API Returns Data** → Series list with image URLs
6. **Component Renders** → Dropdown shows series, images load on selection

### Frame Image Location:
Images should be stored in: `backend/static/frames/`

**Supported File Naming:**
- `series-{number}-thumbnail.png` (preferred)
- `series-{number}-head.png` (fallback)
- `series-{number}-sill.png` (for cross-sections)
- `series-{number}-jamb.png` (for cross-sections)

**Example:**
- `series-86-thumbnail.png`
- `series-135-head.png`
- `series-65-sill.png`

## To Use This Feature

### 1. Start the Backend Server
```bash
cd backend
python main.py
# Server runs on http://localhost:8000
```

### 2. Start the Frontend Server
```bash
cd frontend
npm run dev
# Server runs on http://localhost:3001
```

### 3. Add Frame Images (Optional)
Place frame images in `backend/static/frames/`:
```
backend/static/frames/
├── series-86-thumbnail.png
├── series-135-head.png
├── series-65-thumbnail.png
└── ...
```

### 4. Test the Connection
1. Open http://localhost:3001 in browser
2. Navigate to frame series dropdown
3. Dropdown should populate with series from database
4. Selecting a series should display its preview image (if available)

## Database Integration Details

### Database Table:
The component queries from: `frame_cross_sections` table

**Expected Table Structure:**
```sql
CREATE TABLE frame_cross_sections (
  id INTEGER PRIMARY KEY,
  series VARCHAR(50),
  size VARCHAR(50),
  view_type VARCHAR(20),
  image_path VARCHAR(255),
  width_min DECIMAL,
  width_max DECIMAL,
  height_min DECIMAL,
  height_max DECIMAL
);
```

### Current Implementation:
- Uses distinct series from database
- Shows loading state while fetching
- Falls back to default series if database is empty or errors occur

## Error Handling

The implementation includes graceful error handling:

**If Backend is Down:**
- Component shows "Loading frame series..." indefinitely
- User can still use the form with hardcoded fallback

**If Database is Empty:**
- Returns default series list: 86, 135, 150, 65, 68, 58, 4518, Other

**If Image is Missing:**
- Shows "No preview image available" message
- Component still works, just no image displayed

## Features Implemented

✅ Database-driven frame series list
✅ Dynamic image loading from static files
✅ Loading states for better UX
✅ Error handling and fallbacks
✅ Real-time image preview on series selection
✅ Frame view selector (HEAD/SILL/JAMB) still functional
✅ Fully type-safe with TypeScript

## Next Steps

1. **Add Frame Images:** Place PNG files in `backend/static/frames/`
2. **Populate Database:** Ensure `frame_cross_sections` table has series data
3. **Test Dropdown:** Verify it populates with database series
4. **Verify Images:** Check that images load when series is selected
5. **Deploy:** Push changes to production database server

## API Endpoints Reference

**Get Frame Series with Images:**
```
GET /api/frames/series-with-images
```

**Get Series Details:**
```
GET /api/frames/series/{series_name}
```

**Get Frame Count:**
```
GET /api/frames/count
```

**Get Cross-Sections:**
```
GET /api/frames/cross-sections/{series}
```

**Get Series Thumbnail:**
```
GET /api/frames/series/{series}/image
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dropdown shows "Loading..." | Check backend is running on port 8000 |
| Series don't appear | Verify `frame_cross_sections` table has data |
| Images don't load | Check files exist in `backend/static/frames/` |
| Network errors | Ensure CORS is enabled (already configured) |
| Database connection fails | Check DATABASE_URL in `.env` file |

## Files Modified

1. `backend/routers/frames.py` - Added `/series-with-images` endpoint
2. `frontend/src/services/api.js` - Added `getFrameSeriesWithImages()` function
3. `frontend/src/components/sales/SmartParameterPanel.tsx` - Updated component to use database data

## Technical Stack

- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Frontend:** React + TypeScript + React Query
- **State Management:** Zustand
- **API Communication:** Axios
- **Styling:** Tailwind CSS

---

**Status:** ✅ COMPLETE - Ready for testing with real database and frame images
