# PDF Generation Diagnostics & Fixes

## Problem Identified
User reported "Drawing Error" when attempting to generate PDFs through the frontend.

## Root Cause Analysis

**Primary Issue Found:**
The error handling in `useReferencePDFGeneration.ts` hook was too generic, returning only HTTP status text instead of parsing the actual error message from the backend response.

**Secondary Issue:**
Buffer size checking in `reference_shop_drawing_generator.py` used `pdf_buffer.tell()` which returns the cursor position (0 after seek), not the buffer size. This caused a false "Generated PDF is empty" error even though the PDF was successfully created.

## Fixes Implemented

### 1. **Frontend Hook Enhancement** (`frontend/src/hooks/useReferencePDFGeneration.ts`)
**Lines 28-58** - Improved error handling:
- ✅ Extracts detailed error messages from backend JSON responses
- ✅ Validates PDF blob is not empty (`blob.size === 0`)
- ✅ Adds detailed console logging for debugging
- ✅ Properly logs error details including params and status

**Before:**
```typescript
if (!response.ok) {
  throw new Error(`Failed to generate drawing: ${response.statusText}`)
}
```

**After:**
```typescript
if (!response.ok) {
  let errorMessage = `Failed to generate drawing (${response.status})`
  try {
    const errorData = await response.json()
    if (errorData.detail) {
      errorMessage = errorData.detail
    }
  } catch (parseError) {
    errorMessage = response.statusText || errorMessage
  }
  console.error('[PDF Generation Error]', {...})
  throw new Error(errorMessage)
}
```

### 2. **Backend PDF Generation Fix** (`backend/services/reference_shop_drawing_generator.py`)
**Lines 114-144** - Fixed buffer size checking:
- ✅ Changed from `pdf_buffer.tell()` to `pdf_buffer.getvalue()`
- ✅ `getvalue()` returns the actual buffer content
- ✅ Properly validates PDF size: `file_size = len(pdf_data)`

**Before:**
```python
file_size = pdf_buffer.tell()  # WRONG: returns 0 after seek(0)
if file_size == 0:
    raise RuntimeError("Generated PDF is empty")
```

**After:**
```python
pdf_data = pdf_buffer.getvalue()  # CORRECT: gets actual content
file_size = len(pdf_data)
if file_size == 0:
    raise RuntimeError("Generated PDF is empty")
pdf_buffer = io.BytesIO(pdf_data)  # Create fresh buffer
return pdf_buffer
```

### 3. **Backend Endpoint Validation** (`backend/routers/drawings.py`)
**Lines 285-344** - Enhanced error handling:
- ✅ Added input parameter validation (series, item_number, width, height)
- ✅ Distinguishes between validation errors (400) and runtime errors (500)
- ✅ Provides detailed error context to frontend
- ✅ Better logging with parameters

### 4. **PDF Generator Robustness** (`backend/services/reference_shop_drawing_generator.py`)
**Lines 47-160** - Added comprehensive error handling:
- ✅ Input parameter validation at start (prevents downstream errors)
- ✅ Detailed logging at each stage
- ✅ Try-catch blocks around matplotlib figure creation, saving, and PDF generation
- ✅ Proper cleanup with `missing_ok=True` for temporary files
- ✅ Descriptive error messages for each failure point

### 5. **Drawing Function Improvements**
**`_draw_elevation_view()`** (Lines 300-357):
- ✅ Added error handling with try-except
- ✅ Safe configuration validation (handles empty/null config)
- ✅ Prevents division by zero: `max(panel_count, 1)`

**`_draw_plan_view()`** (Lines 360-408):
- ✅ Added error handling with try-except
- ✅ Removed redundant `Circle` import (used from top-level import)

## Testing Results

### Diagnostic Test Created: `test_pdf_generation.py`
Tests the PDF generation endpoint with real parameters:
- ✅ Status Code: 200 (Success)
- ✅ PDF Generated: 72,588+ bytes
- ✅ Content-Type: application/pdf

### Direct Generation Test: `debug_pdf.py`
Tests the generator directly:
- ✅ Generated PDF: 72,588 bytes
- ✅ No errors with proper parameter validation

## Error Messages Now Properly Displayed

**Example Error Flow:**
1. Frontend sends invalid parameters
2. Backend validates: `ValueError: Invalid width/height values`
3. Returns HTTP 400 with JSON: `{"detail": "Invalid parameters: Invalid width/height values"}`
4. Frontend extracts `.detail` field
5. User sees meaningful error: "Invalid parameters: Invalid width/height values"

## Build Status

✅ Frontend builds successfully (787 modules, 273-286 KB)
✅ No TypeScript errors
✅ All changes backward compatible

## User Impact

**Before Fix:**
- Generic "Drawing Error" message in red box
- No indication what went wrong
- Difficult to debug issues

**After Fix:**
- Specific, actionable error messages
- Details extracted from backend
- Clear logging in console for developers
- Proper parameter validation before drawing

## Recommendations

1. **Add Request Validation**: Use Pydantic request models to validate all inputs
2. **Implement Retry Logic**: Add exponential backoff for transient failures
3. **Add Monitoring**: Log all PDF generation requests with timestamps
4. **Cache Assets**: Pre-load frame images instead of fetching each time
5. **User Feedback**: Show progress indicators during 3-second PDF generation

