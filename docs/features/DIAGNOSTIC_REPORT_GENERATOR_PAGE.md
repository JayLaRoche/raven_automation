# Drawing Generator Page Diagnostic Report

**Date**: January 6, 2026  
**Issue**: `/generator` route returns blank page  
**Severity**: CRITICAL

---

## Executive Summary

The Drawing Generator page (`/generator` route) is **non-functional** due to multiple cascading errors in the `SalesPresentation` and `CanvasDrawingPreview` components. The main issue is that `CanvasDrawingPreview.tsx` is trying to call a variable as a function, causing a runtime crash that silently breaks the entire page.

---

## Root Cause Analysis

### Critical Error #1: Variable/Function Name Collision (BLOCKING)
**Location**: [frontend/src/components/sales/CanvasDrawingPreview.tsx](frontend/src/components/sales/CanvasDrawingPreview.tsx#L328)  
**Line**: 328  
**Severity**: 🔴 CRITICAL - Prevents Component from Rendering

```typescript
// Line 313: isImageValid is defined as a VARIABLE (boolean)
const isImageValid = section.image && 
                    section.image.complete && 
                    section.image.width > 0 && 
                    section.image.height > 0 &&
                    section.image.naturalWidth > 0 &&
                    section.image.naturalHeight > 0

// Line 328: THEN TRIES TO CALL IT AS A FUNCTION
if (section.image && isImageValid(section.image)) {  // ERROR: isImageValid is boolean, not function!
  ctx.drawImage(section.image, offsetX, offsetY, scaledWidth, scaledHeight)
}
```

**Problem**: Earlier in the code (line 50), `isImageValid` is defined as a **helper function**. But at line 313, it's being redeclared as a **boolean variable**. Then at line 328, it tries to **call the boolean as a function**, causing:
```
TypeError: This expression is not callable. Type 'Boolean' has no call signatures.
```

**Impact**: Throws uncaught error → React component crashes → blank page

---

## Complete Issue Inventory

### Frontend Issues

| ID | Component | File | Line | Issue | Severity | Status |
|----|-----------|------|------|-------|----------|--------|
| F1 | CanvasDrawingPreview | `CanvasDrawingPreview.tsx` | 313-328 | Variable shadows function, then calls as function | 🔴 CRITICAL | ❌ NOT FIXED |
| F2 | CanvasDrawingPreview | `CanvasDrawingPreview.tsx` | 583-741 | `styles` object referenced but CSS module import removed | 🔴 CRITICAL | ❌ NOT FIXED |
| F3 | SalesPresentation | `SalesPresentation.tsx` | 740 | `styles.mainContent` but CSS import exists | 🟡 HIGH | ❌ PARTIAL |
| F4 | SmartParameterPanel | `SmartParameterPanel.jsx` | 166, 236 | Non-interactive div with onClick, negated condition | 🟡 MEDIUM | ❌ NOT FIXED |
| F5 | DrawingGenerator | `DrawingGenerator.jsx` | 2 | Unused import `useQuery` | 🟢 LOW | ✅ FIXED |

### Backend Issues (Non-Critical)

| ID | File | Line | Issue | Impact |
|----|------|------|-------|--------|
| B1 | `main.py` | 48, 58 | f-strings with no replacement fields | Lint warning only |
| B2 | `generate_assets.py` | 96-145 | f-strings with no replacement fields | Lint warning only |
| B3 | `generate_assets.py` | 72 | Bare `except:` clause | Best practice violation |

---

## Detailed Issue Breakdown

### F1: CanvasDrawingPreview Function/Variable Collision (BLOCKING)

**File**: `frontend/src/components/sales/CanvasDrawingPreview.tsx`  
**Lines**: 50 (function definition), 313-328 (variable shadow + function call)

**Current Code**:
```typescript
// Line 50: isImageValid defined as a FUNCTION
const isImageValid = (image: HTMLImageElement | null): boolean => {
  if (!image) return false
  return image.complete && image.width > 0 && ...
}

// Line 313-320: isImageValid REDEFINED as a VARIABLE
const isImageValid = section.image && 
                    section.image.complete && 
                    section.image.width > 0 && 
                    section.image.height > 0 &&
                    section.image.naturalWidth > 0 &&
                    section.image.naturalHeight > 0

// Line 328: Tries to CALL it as a function
if (section.image && isImageValid(section.image)) {  // ❌ TypeError
  ctx.drawImage(section.image, ...)
}
```

**Fix Strategy**:
1. Rename the variable to avoid shadowing: `const imageIsValid = section.image && ...`
2. Keep the function call: `isImageValid(section.image)`
3. OR: Replace variable with direct inline check

**Solution** (Option A - Rename variable):
```typescript
// Line 313-320: Rename to avoid shadow
const imageIsValid = section.image && 
                    section.image.complete && 
                    section.image.width > 0 && 
                    section.image.height > 0 &&
                    section.image.naturalWidth > 0 &&
                    section.image.naturalHeight > 0

// Line 328: Use renamed variable OR call function
if (imageIsValid) {  // Use the variable
  ctx.drawImage(section.image, offsetX, offsetY, scaledWidth, scaledHeight)
}
```

---

### F2: Missing CSS Module in CanvasDrawingPreview (BLOCKING)

**File**: `frontend/src/components/sales/CanvasDrawingPreview.tsx`  
**Lines**: 583, 584, 588, 594, 595, 598, 718, 732, 738, 741

**Problem**: Component tries to use `styles.*` classes but CSS module import was removed:

```typescript
// Missing at top:
import styles from './CanvasDrawingPreview.module.css'

// But used throughout:
<div className={styles.presentationModeWrapper}>  // Line 583
<div className={styles.presentationModeHeader}>   // Line 584
// ... etc
<div className={`flex flex-col w-full relative ${styles.stickyWrapper}`}>  // Line 718
```

**Fix**: Restore the CSS module import at top of file:
```typescript
import { useEffect, useRef, useState } from 'react'
import styles from './CanvasDrawingPreview.module.css'  // ADD THIS LINE
```

**Verification**: CSS file exists at `frontend/src/components/sales/CanvasDrawingPreview.module.css` ✓

---

### F3: SalesPresentation CSS References (CASCADING)

**File**: `frontend/src/components/sales/SalesPresentation.tsx`  
**Lines**: 740, 732, 738

**Problem**: Uses `styles.mainContent`, `styles.canvasViewLayout`, `styles.leftPanel`, `styles.rightPanel` but CSS import exists.

**Current Import**: Line 13 has `import styles from './SalesPresentation.module.css'` ✓

**Issue**: Might be resolved by fixing F1 + F2, but verify CSS selectors exist in module.

---

### F4: SmartParameterPanel Accessibility Issues

**File**: `frontend/src/components/SmartParameterPanel.jsx`  
**Lines**: 166 (non-interactive div), 236 (negated condition)

**Issues**:
1. **Line 166**: Non-interactive div with onClick handler needs `role="button"` and keyboard support
2. **Line 236**: `!imgData.exists` creates double negative, prefer `imgData.exists === false`
3. **Line 6**: Missing prop validation for TypeScript/ESLint

**Impact**: Accessibility warning, not rendering blocker

---

## Dependency Chain Analysis

For `/generator` route to work:

```
/generator route
    ↓
<SalesPresentation /> component
    ↓
├─ useDrawingStore() hook
├─ useKeyboardShortcuts() hook
├─ useReferencePDFGeneration() hook
├─ <SmartParameterPanel /> → uses drawingStore
├─ <CanvasDrawingPreview /> ← **CRASHES HERE** (F1 error)
├─ <DrawingPDFViewer /> 
├─ <PresentationMode />
└─ <QuickExport />
```

**Blocking Step**: `<CanvasDrawingPreview />` initialization throws error → kills entire SalesPresentation → blank page

---

## Browser Console Errors Expected

When navigating to `/generator`, browser console should show:

```
TypeError: This expression is not callable. Type 'Boolean' has no call signatures.
    at CanvasDrawingPreview.tsx:328
    at draw (CanvasDrawingPreview.tsx:...)
    at requestAnimationFrame (...)
```

Plus secondary errors:

```
ReferenceError: Cannot find name 'styles'
    at CanvasDrawingPreview.tsx:583
```

---

## Fix Priority Order

### Phase 1: CRITICAL (Unblock Page)
1. **Fix F1**: Rename `isImageValid` variable → `imageIsValid` (line 313)
2. **Fix F2**: Restore CSS import in CanvasDrawingPreview.tsx

### Phase 2: MAJOR (Fix Remaining Errors)
3. **Fix F3**: Verify SalesPresentation.tsx CSS selectors
4. **Fix F4**: Fix SmartParameterPanel accessibility

### Phase 3: MINOR (Code Quality)
5. Fix backend f-string warnings
6. Fix bare except clause

---

## Testing Checklist

After fixes applied:

- [ ] Navigate to `http://localhost:3000/generator` → Page loads without blank
- [ ] "Dashboard" button works → navigates to `/`
- [ ] "Drawing Generator" button works → navigates to `/generator`
- [ ] Left panel (SmartParameterPanel) renders with frame series dropdown
- [ ] Right panel (CanvasDrawingPreview) renders with canvas
- [ ] Frame images load from `/static/frames/series_*.png`
- [ ] Canvas draws frame cross-sections without errors
- [ ] No TypeScript/Console errors in dev tools
- [ ] Keyboard shortcuts work (Cmd+Enter = generate, etc)
- [ ] PDF generation button functional
- [ ] Presentation mode button works

---

## Environment Notes

- **Frontend**: Vite 5.4.21, React 18.2, TypeScript 5.x
- **CSS Modules**: Configured in Vite, type definitions in `vite-env.d.ts`
- **Dev Server**: Running on `http://localhost:3000`
- **Backend**: FastAPI on `http://localhost:8000`
- **Test Frame Series**: 86, 65, 68, 135, 150, 4518, 58

---

## Files Requiring Changes

1. `frontend/src/components/sales/CanvasDrawingPreview.tsx` — Lines 313, 1 (add import)
2. `frontend/src/components/SmartParameterPanel.jsx` — Lines 166, 236
3. `frontend/src/components/dashboard/ProjectCard.tsx` — Line 21 (best practice)
4. `backend/main.py` — Lines 48, 58 (lint warnings)
5. `backend/generate_assets.py` — Lines 72, 96-145 (lint warnings)

---

## Related Documentation

- [APP_REORGANIZATION_COMPLETE.md](APP_REORGANIZATION_COMPLETE.md)
- [PRESENTATION_MODE_COMPLETE.md](PRESENTATION_MODE_COMPLETE.md)
- [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)

---

**Report Generated**: January 6, 2026  
**Status**: 🔴 CRITICAL ISSUES PRESENT - Page Non-Functional
