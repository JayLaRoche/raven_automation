# Canvas Panel - Header-Aware Sticky Positioning Fix

## Summary

Updated the canvas panel sticky positioning to respect the page header and prevent the canvas from scrolling underneath it.

## The Problem

Previously, the canvas panel used:
```css
position: sticky;
top: 20px;  /* Only 20px from viewport top */
```

This caused the canvas to stick very close to the top of the browser window, scrolling under the header content.

## The Solution

The canvas panel now uses header-aware positioning:
```css
position: sticky;
top: 100px;
/* Header height (~80px) + spacing (20px) = 100px total */

max-height: calc(100vh - 140px);
/* Viewport minus header (80px) + top spacing (20px) + bottom margin (40px) */
```

## How It Works

### Measurement

The header in `SalesPresentation.tsx` has:
- **Padding**: `py-4` = 16px top + 16px bottom = 32px
- **Content**: `text-2xl` heading (32px) + `text-sm` subtitle (14px)
- **Border**: Bottom border adds visual height
- **Total height**: Approximately **80-85px**

### Calculation

```
Header height:        ~80px
Top spacing:          20px
────────────────────────────
Sticky top offset:    100px

Viewport height:      100vh
Header + spacing:     100px
Bottom margin:        40px
────────────────────────────
Canvas max-height:    calc(100vh - 140px)
```

## Files Modified

### `frontend/src/components/sales/CanvasDrawingPreview.module.css`

**Changes:**
1. Updated `.canvasContainer` sticky positioning:
   - `top: 20px` → `top: 100px`
   - `max-height: calc(100vh - 40px)` → `max-height: calc(100vh - 140px)`
   
2. Updated `@supports not (position: sticky)` fallback:
   - `top: 20px` → `top: 100px`
   - Added `max-height: calc(100vh - 140px)`

## Expected Behavior

### Desktop (>1024px)

✅ **Canvas scrolls normally with left panel initially**
- Left panel (parameters) scrolls down
- Canvas scrolls along with it

✅ **Canvas sticks 100px from top when reaching header**
- As user scrolls content up, canvas stops scrolling
- Canvas "sticks" at exactly 100px from viewport top
- This places it 20px below the header (80px header + 20px spacing)

✅ **Other content scrolls behind sticky canvas**
- While canvas is sticky, left panel continues scrolling underneath
- Canvas remains visible and never goes under the header

✅ **At page bottom, canvas scrolls naturally**
- If user reaches end of scrollable content, canvas scrolls past naturally
- Normal document flow is maintained

### Tablet (1024px - 768px)

✅ **Sticky disabled** (single column layout)
- Canvas uses `position: relative`
- Stacks below parameters
- Normal scrolling behavior

### Mobile (<768px)

✅ **Sticky disabled** (full width, stacked)
- Canvas uses `position: relative`
- Full-width layout
- Normal scrolling behavior

## Testing Checklist

Use this checklist to verify the sticky behavior is working correctly:

- [ ] **Viewport is wider than 1024px** (desktop view active)
- [ ] **Canvas starts in normal position on page load**
  - Canvas should be below any header content
  - Should have proper spacing (20px from header)
  
- [ ] **Scroll down the left panel**
  - Watch canvas as you scroll
  - Canvas should scroll WITH the content initially
  - NOT stay fixed at top
  
- [ ] **Canvas reaches sticky point**
  - As you continue scrolling, canvas should "stick"
  - Should stick at 100px from viewport top
  - This is 20px below the 80px header
  
- [ ] **Header remains on top**
  - Header should ALWAYS be visible
  - Canvas should never overlap the header
  - z-index layering is correct (header > canvas)
  
- [ ] **Smooth scroll with internal content**
  - If canvas is taller than remaining viewport space
  - Canvas should allow internal scrolling (`overflow-y: auto`)
  - Should not affect page scroll
  
- [ ] **Mobile view (resize to <768px)**
  - Sticky disabled automatically
  - Canvas switches to `position: relative`
  - Normal stacked layout
  - Content flows naturally
  
- [ ] **No visual glitches**
  - No layout shifts or jumps
  - No flickering during scroll
  - No overlap or z-index issues
  - Scrollbars work smoothly

## How to Adjust Header Height

If the header height is different on your screen:

1. **Measure the actual header height** in your browser:
   - Open DevTools (F12)
   - Inspect the header element
   - Check the `height` property in computed styles
   - Or: Right-click header → "Inspect" → Check dimensions

2. **Calculate new sticky offset**:
   ```
   New offset = actual_header_height + 20px_spacing
   
   Example:
   - If header is 60px: offset = 60 + 20 = 80px
   - If header is 90px: offset = 90 + 20 = 110px
   - If header is 100px: offset = 100 + 20 = 120px
   ```

3. **Update the CSS**:
   ```css
   /* In CanvasDrawingPreview.module.css */
   .canvasContainer {
     position: sticky;
     top: 100px;  /* ← Change this to your calculated value */
     max-height: calc(100vh - 140px);  /* ← And adjust this too */
   }
   
   /* max-height formula: 100vh - (header_height + 20px spacing + 40px bottom) */
   /* Example: 100vh - (80 + 20 + 40) = 100vh - 140px */
   ```

## Dynamic Header Height Detection (Advanced)

If you want to detect the header height automatically:

```tsx
import { useEffect, useState } from 'react'

export function CanvasDrawingPreview() {
  const [headerHeight, setHeaderHeight] = useState(80)
  
  useEffect(() => {
    // Find the header element and measure it
    const header = document.querySelector('header')
    if (header) {
      setHeaderHeight(header.offsetHeight)
    }
    
    // Recalculate on window resize
    const handleResize = () => {
      const newHeight = header?.offsetHeight || 80
      setHeaderHeight(newHeight)
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  
  return (
    <div 
      className={styles.canvasContainer}
      style={{
        top: `${headerHeight + 20}px`,
        maxHeight: `calc(100vh - ${headerHeight + 60}px)`
      }}
    >
      {/* Canvas content */}
    </div>
  )
}
```

## Browser Support

The sticky positioning works in:
- ✅ Chrome 56+ (2017)
- ✅ Firefox 59+ (2018)
- ✅ Safari 13+ (2019)
- ✅ Edge 16+ (2017)
- ✅ All modern mobile browsers

Older browsers fall back to `position: fixed` with the same header offset.

## Related Files

- `frontend/src/components/sales/CanvasDrawingPreview.tsx` - Component using CSS classes
- `frontend/src/components/sales/SalesPresentation.tsx` - Parent layout with header
- `frontend/src/components/sales/SalesPresentation.module.css` - Parent container config

## Troubleshooting

### Issue: Canvas still scrolls under header

**Solution**: Verify the header height
1. Measure the actual header height in DevTools
2. Update `top` value: `header_height + 20`
3. Update `max-height` value: `100vh - (header_height + 60)`

### Issue: Canvas sticks too far from header

**Solution**: Adjust the spacing (currently 20px)
- In CSS: Change `top: 100px` to `top: 90px` (less spacing)
- Current: 80px header + 20px spacing = 100px
- New: 80px header + 10px spacing = 90px

### Issue: Canvas content is cut off

**Solution**: Increase the `max-height` value
- Current: `calc(100vh - 140px)`
- Try: `calc(100vh - 120px)` or `calc(100vh - 100px)`
- But ensure header remains fully visible

### Issue: Sticky not working

**Solution**: Verify parent container configuration
- Parent (`.rightPanel`) must have `overflow-y: visible`
- Parent must have `align-items: flex-start`
- No ancestor should have `overflow: hidden`

Check [SalesPresentation.module.css](frontend/src/components/sales/SalesPresentation.module.css#L23-L32) for:
```css
.rightPanel {
  overflow-y: visible;  /* ✅ Correct */
  display: flex;
  flex-direction: column;
  align-items: flex-start;  /* ✅ Correct */
}
```

## Summary of Changes

| Component | Change | Reason |
|-----------|--------|--------|
| `.canvasContainer` | `top: 20px` → `top: 100px` | Respect 80px header + 20px spacing |
| `.canvasContainer` | `max-height: calc(100vh - 40px)` → `calc(100vh - 140px)` | Account for header height in calculation |
| Fallback (fixed) | `top: 20px` → `top: 100px` | Keep parity with sticky positioning |
| Fallback (fixed) | Added `max-height` property | Ensure consistent sizing in both modes |

All changes are backward compatible and include responsive breakpoints.
