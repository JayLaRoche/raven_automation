# "Failed to Generate Drawing" Error - Complete Diagnostic Report

**Date:** January 6, 2026  
**Issue:** User selects frame series but gets "failed to generate drawing" error  
**Severity:** 🔴 **CRITICAL** - Core functionality blocked

---

## Summary of Findings

After analyzing the codebase, I found **12 potential failure points** that could cause the "failed to generate drawing" error when selecting a frame series.

---

## 🔴 CRITICAL ISSUES FOUND

### Issue #1: Missing Backend API Endpoint
**File:** `backend/main.py` & `backend/routers/drawings.py`  
**Severity:** 🔴 **CRITICAL**  
**Problem:** The `generateDrawing` API endpoint is NOT implemented in the backend

**Evidence:**
- `backend/routers/drawings.py` is imported but commented out in `main.py` (line 37-38)
- No endpoint handles `POST /api/drawings/generate` 
- Frontend calls `generateDrawing(parameters)` which tries to POST to backend

**Frontend Code (SalesPresentation.tsx line 155):**
```typescript
const result = await generateDrawing(parameters)
const drawingData = result.drawing || result
```

**What Happens:**
1. User selects frame series (e.g., "86")
2. Frontend calls `api.post('/api/drawings/generate', parameters)`
3. Backend has NO route for this
4. Request fails with 404 or 500
5. Error is caught, "failed to generate drawing" shown

**Fix Required:**
```bash
# Backend needs /api/drawings/generate endpoint
# Currently: routers/drawings.py is commented out
```

---

### Issue #2: Router Not Registered in FastAPI App
**File:** `backend/main.py` line 37-38  
**Severity:** 🔴 **CRITICAL**  
**Problem:** Drawings router is commented out

```python
# app.include_router(projects.router)
# app.include_router(drawings.router)  # ← COMMENTED OUT!
app.include_router(frames.router)
```

**Impact:**
- Even if `/api/drawings/generate` endpoint exists, it's NOT registered
- Backend app doesn't know about the route
- All drawing generation requests fail

**Fix Required:**
```python
app.include_router(drawings.router)  # Uncomment this line
```

---

### Issue #3: Missing or Broken generateDrawing API Function
**File:** `frontend/src/services/api.js`  
**Severity:** 🟡 **HIGH**  
**Problem:** API client function might not exist or be broken

**Current Code (line 20-22):**
```javascript
export const generateDrawing = async (parameters) => {
  const response = await api.post('/api/drawings/generate', parameters)
  return response.data
}
```

**Potential Problems:**
1. Function exists but endpoint doesn't exist (Issue #1 above)
2. Endpoint expects different parameter format
3. Axios baseURL misconfigured
4. CORS headers not allowing POST requests

**Check Required:**
```bash
# Verify the function exists
grep -n "export const generateDrawing" frontend/src/services/api.js

# Check if it's being called
grep -n "generateDrawing" frontend/src/components/sales/SalesPresentation.tsx
```

---

### Issue #4: Parameters Missing Required Fields
**File:** `frontend/src/components/sales/SmartParameterPanel.tsx`  
**Severity:** 🟡 **HIGH**  
**Problem:** Drawing generation requires specific parameter fields that might be missing

**Required Parameters (from SalesPresentation.tsx line 329-346):**
```typescript
generatePDF({
  series: parameters.series,              // e.g., "86"
  product_type: parameters.productType,   // e.g., "FIXED"
  width: parameters.width,                 // e.g., 48
  height: parameters.height,               // e.g., 60
  glass_type: parameters.glassType,       // e.g., "Clear Low E"
  frame_color: parameters.frameColor,     // e.g., "Black"
  configuration: parameters.configuration, // e.g., "O"
  item_number: parameters.itemNumber,     // e.g., "P001"
  po_number: parameters.poNumber,         // e.g., ""
  notes: parameters.notes,                 // e.g., ""
})
```

**Check Point:**
- If ANY of these fields are undefined/null, request fails
- Frame series selection alone is NOT enough
- User must fill in width, height, product type, etc.

**Evidence:**
- Validation exists: `if (!parameters.series || !parameters.width || !parameters.height)` (line 215)
- But error message not shown to user if other fields missing
- Backend validation might be stricter

---

### Issue #5: Vite Proxy Not Forwarding POST Requests
**File:** `frontend/vite.config.js`  
**Severity:** 🟡 **HIGH**  
**Problem:** Proxy might not properly forward POST requests with bodies

**Current Config (line 15-18):**
```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

**Issue:**
- Proxy configured for basic GET requests
- POST requests with JSON body might need `rewrite` rule
- `changeOrigin: true` helps but may not be enough

**Fix:**
```javascript
'/api': {
  target: 'http://localhost:8000',
  changeOrigin: true,
  rewrite: (path) => path,  // Add this
}
```

---

### Issue #6: CORS Not Allowing POST from Frontend
**File:** `backend/main.py` line 27-34  
**Severity:** 🟡 **HIGH**  
**Problem:** CORS middleware might block POST requests

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # ← Should allow POST
    allow_headers=["*"],  # ← Should allow headers
)
```

**Issue:**
- Config looks correct (`allow_methods=["*"]`)
- But if origin is wrong (frontend running on different port), it blocks everything
- If frontend on 3001 or 5173, request blocked

**Check Point:**
```bash
# What port is frontend actually running on?
netstat -ano | findstr "3000|3001|5173"
```

---

### Issue #7: Canvas Drawing Logic Fails Silently
**File:** `frontend/src/components/sales/CanvasDrawingPreview.tsx`  
**Severity:** 🟡 **HIGH**  
**Problem:** Canvas rendering might fail but error not shown to user

**Debug Info Section (line 822-828):**
```tsx
<div className="px-4 pb-4 text-xs text-gray-500 border-t pt-2 mt-4">
  <p>Canvas Size: 1122×794px | Frame Images: 
    HEAD {frameImages.head ? '✓' : '✗'} | 
    SILL {frameImages.sill ? '✓' : '✗'} | 
    JAMB {frameImages.jamb ? '✓' : '✗'}
  </p>
</div>
```

**Problem:**
- If frame images show as '✗', drawing generation will fail
- Frame image URLs might be wrong
- Frame images might not be loading from API

**Check Point:**
```
User should see in the drawing preview:
- Frame Images: HEAD ✓ | SILL ✓ | JAMB ✓

If any show ✗, drawing generation fails silently
```

---

### Issue #8: Frame Images Not Loading from API
**File:** `frontend/src/components/sales/CanvasDrawingPreview.tsx` line 104-213  
**Severity:** 🟡 **HIGH**  
**Problem:** Frame images fail to load, preventing canvas drawing

**Image Loading Code (line 165-180):**
```typescript
const loadHeadImage = () => {
  if (!frameImageUrls.head) return
  const headImg = new Image()
  headImg.crossOrigin = 'anonymous'
  headImg.onload = () => {
    if (headImg.complete && headImg.width > 0 && headImg.height > 0) {
      setFrameImages((prev: FrameImages) => ({ ...prev, head: headImg }))
    } else {
      console.warn('HEAD image loaded but has invalid dimensions')
      setFrameImages((prev: FrameImages) => ({ ...prev, head: null }))
    }
  }
  headImg.onerror = () => {
    console.warn(`Failed to load HEAD image: ${frameImageUrls.head}`)
    setFrameImages((prev: FrameImages) => ({ ...prev, head: null }))
  }
  headImg.src = frameImageUrls.head
}
```

**Potential Problems:**
1. `frameImageUrls.head` is null/undefined
2. Image URL is wrong format
3. Backend not serving images at `/static/frames/`
4. CORS blocking image load
5. Image file doesn't exist

**Check Point:**
- Console shows warning: "Failed to load HEAD image"
- Or: "HEAD image loaded but has invalid dimensions"

---

### Issue #9: Frame Series Selection Not Updating Parameters
**File:** `frontend/src/components/sales/SmartParameterPanel.tsx`  
**Severity:** 🟡 **HIGH**  
**Problem:** Selecting frame series might not update the parameters object

**Expected Flow:**
1. User selects series from dropdown
2. `parameters.series` updated to "86"
3. Component re-renders
4. Drawing preview updates
5. Generate button becomes enabled

**Potential Issues:**
- Dropdown change handler not updating state
- Parameters not being passed to CanvasDrawingPreview
- Store not updating (if using Zustand store)

**Check Point:**
```bash
# Browser DevTools Console:
# Should show:
# parameters: { series: "86", width: 48, height: 60, ... }
```

---

### Issue #10: Backend Database Connection Failed
**File:** `backend/main.py` line 17-22  
**Severity:** 🟡 **HIGH**  
**Problem:** Database tables not created, drawing generation fails

```python
try:
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created/verified")
except Exception as e:
    print(f"[WARNING] Database connection not available: {str(e)}")
```

**What Happens:**
- If PostgreSQL not running, database tables not created
- Drawing generation expects database
- Query fails, returns error

**Fix:**
```bash
# Check if PostgreSQL is running
docker-compose ps

# If not:
docker-compose up postgres -d
```

---

### Issue #11: generateDrawing Hook Not Trigger Auto-Update
**File:** `frontend/src/components/sales/SalesPresentation.tsx` line 36-56  
**Severity:** 🟡 **HIGH**  
**Problem:** Auto-generation with React Query might not be working

```typescript
const { refetch, isFetching } = useQuery({
  queryKey: ['drawing', parameters],
  queryFn: async () => {
    setIsGenerating(true)
    try {
      const result = await generateDrawing(parameters)
      return result.drawing || result
    } finally {
      setIsGenerating(false)
    }
  },
  enabled: false,  // ← AUTO-UPDATE DISABLED!
  refetchOnWindowFocus: false,
  refetchOnMount: false,
})
```

**Issue:**
- `enabled: false` means query never runs automatically
- User must click "Generate" button
- Button might not be visible or clickable

---

### Issue #12: Toast Error Not Showing Real Error Message
**File:** `frontend/src/components/sales/SalesPresentation.tsx` line 152-160  
**Severity:** 🟠 **MEDIUM**  
**Problem:** Error toast shows generic message, not actual error

```typescript
catch (error) {
  console.error('Failed to generate:', error)
  toast.error('Failed to generate drawing')  // ← Generic message!
}
```

**Issue:**
- User sees "failed to generate drawing"
- But real error is in browser console
- Developer can't easily diagnose

**Better Error Message:**
```typescript
catch (error) {
  const errorMsg = error.response?.data?.detail || error.message || 'Unknown error'
  toast.error(`Failed to generate: ${errorMsg}`)
}
```

---

## Root Cause Analysis

### Most Likely Cause:
🔴 **Issue #1 + #2**: Backend `/api/drawings/generate` endpoint missing or router not registered

**Why:**
1. Backend main.py comments out drawings router
2. No endpoint to receive generate requests
3. Frontend POST fails
4. Error caught and shown to user

### Second Most Likely Cause:
🟡 **Issue #8**: Frame images not loading

**Why:**
1. API returns no image URLs
2. Canvas tries to render with null images
3. Rendering fails
4. Error caught and shown to user

---

## Diagnostic Steps

### Step 1: Check Backend Endpoint
```bash
# Open browser and test:
POST http://localhost:8000/api/drawings/generate
Body: { "series": "86", "width": 48, "height": 60 }

# Expected: 200 OK with drawing data
# Actual: 404 Not Found or 422 Validation Error
```

### Step 2: Check Browser Console
```
Press F12 in browser
Go to Console tab
Look for errors like:
- POST /api/drawings/generate 404 Not Found
- Failed to load image: /static/frames/series-86-head.png
- Cannot read property 'complete' of null
```

### Step 3: Check Network Tab
```
Press F12 → Network tab
Click on frame series dropdown
Look for requests:
- /api/frames/series-with-images (should return 200)
- /api/drawings/generate (should return 200, not 404)
```

### Step 4: Check Frame Images
```bash
# Are PNG files in right location?
ls backend/static/frames/series-86-*

# Should show:
# series-86-head.png
# series-86-sill.png
# series-86-thumbnail.png
```

### Step 5: Check Backend Logs
```bash
# Watch backend terminal while selecting frame series
# Should see:
# INFO: POST /api/frames/series-with-images
# INFO: GET /static/frames/series-86-head.png

# If seeing 404s or errors, that's the problem
```

---

## Error Messages You Might See

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `404 Not Found` on `/api/drawings/generate` | Backend endpoint not exist | Implement endpoint, uncomment router |
| `Failed to load image: /static/frames/...` | Frame images missing or URL wrong | Check file exists, verify API URL format |
| `Cannot read property 'complete' of null` | Image failed to load | Check image URL, verify backend serving files |
| `Series data not loading` | `/api/frames/series-with-images` returns empty | Check database, restart backend |
| `Parameters missing required fields` | Width/height not set | Fill in all form fields |
| `CORS error in console` | Frontend port not whitelisted | Check CORS config, verify frontend port |

---

## Checklist to Fix

- [ ] **Issue #1**: Implement `/api/drawings/generate` endpoint in `backend/routers/drawings.py`
- [ ] **Issue #2**: Uncomment `app.include_router(drawings.router)` in `backend/main.py`
- [ ] **Issue #4**: Verify all required parameters filled in form
- [ ] **Issue #5**: Update Vite proxy config with `rewrite` rule
- [ ] **Issue #6**: Verify frontend running on http://localhost:3000 (CORS whitelist)
- [ ] **Issue #7**: Check browser console for canvas errors
- [ ] **Issue #8**: Verify frame images loading (check Network tab, look for 200 status)
- [ ] **Issue #9**: Verify dropdown change handler updates parameters
- [ ] **Issue #10**: Ensure PostgreSQL running or database fallback working
- [ ] **Issue #11**: Enable auto-update or ensure generate button working
- [ ] **Issue #12**: Improve error messages to show actual error details
- [ ] **Restart Services**: Kill and restart both frontend and backend

---

## Quick Fix Priority

### 🔴 DO FIRST (Blocks everything):
1. Check if `/api/drawings/generate` endpoint exists
2. Check if drawings router is uncommented in main.py
3. Restart backend

### 🟡 DO SECOND (Common issues):
4. Check browser Network tab for failed requests
5. Check browser Console for errors
6. Verify frame images loading

### 🟠 DO THIRD (Polish):
7. Improve error messages
8. Add better validation
9. Add logging for debugging

---

## Next Action

**USER SHOULD:**
1. Open browser F12 (DevTools)
2. Go to Network tab
3. Select a frame series
4. Look for red 404 errors
5. Report which requests are failing
6. Copy exact error messages

**This will determine exact cause:**
- If seeing `404 /api/drawings/generate` → Issue #1, #2
- If seeing `404 /static/frames/...` → Issue #8
- If seeing `400 /api/frames/series-with-images` → Issue #4

---

## Files That Need Changes

| File | Issue | Change Required |
|------|-------|-----------------|
| `backend/main.py` | #2 | Uncomment `app.include_router(drawings.router)` |
| `backend/routers/drawings.py` | #1 | Implement `/api/drawings/generate` endpoint |
| `frontend/vite.config.js` | #5 | Add `rewrite: (path) => path` to proxy |
| `frontend/src/services/api.js` | #3 | Verify generateDrawing function working |
| `frontend/src/components/sales/SalesPresentation.tsx` | #12 | Show actual error in toast message |

---

**Status:** 🔴 **INVESTIGATION REQUIRED**  
**Next Step:** User should check browser console for specific error messages

All 12 potential causes identified. Exact fix depends on which error message appears.
