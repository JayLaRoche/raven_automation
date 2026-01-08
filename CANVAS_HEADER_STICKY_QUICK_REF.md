# Canvas Panel Header-Aware Sticky Fix - Quick Reference

## What Changed ✅

The canvas panel now respects the page header and sticks **below** it instead of overlapping.

### Before
```css
.canvasContainer {
  position: sticky;
  top: 20px;  /* Only 20px from top - scrolls under header! */
  max-height: calc(100vh - 40px);
}
```

### After
```css
.canvasContainer {
  position: sticky;
  top: 100px;  /* Header (80px) + spacing (20px) */
  max-height: calc(100vh - 140px);  /* Account for header height */
}
```

## How To Test

1. **Start the app**: `npm run dev` in frontend folder
2. **Navigate to**: Drawing Generator → Sales Presentation
3. **Scroll the left panel** (parameters list)
4. **Watch the canvas**:
   - ✅ Should scroll WITH the page initially
   - ✅ Should stop at ~100px from top
   - ✅ Should stick there while you scroll more
   - ✅ Header should always be visible above it
   - ✅ NO overlapping or jumping

## The Math

```
Header height:               ~80px
Desired spacing below:        20px
Sticky top offset:           100px
───────────────────────────────────
Viewport height:            100vh
Less header:                 80px
Less spacing:                20px
Less bottom margin:          40px
Canvas max-height:  calc(100vh - 140px)
```

## Files Modified

**`frontend/src/components/sales/CanvasDrawingPreview.module.css`**

Changes in 2 places:

1. **Main rule** (lines 4-18)
   - `top: 20px` → `top: 100px`
   - `max-height: calc(100vh - 40px)` → `max-height: calc(100vh - 140px)`

2. **Fallback rule for older browsers** (lines 156-163)
   - `top: 20px` → `top: 100px`
   - Added `max-height: calc(100vh - 140px)`

## Responsive Behavior

| Viewport | Behavior |
|----------|----------|
| >1024px | Sticky (100px offset) |
| 1024-768px | Relative (no sticky) |
| <768px | Relative (no sticky) |

## If Header Height is Different

Measure your header:
1. Open DevTools (F12)
2. Inspect the header
3. Note the height (let's say it's 75px)

Update the CSS:
```css
.canvasContainer {
  position: sticky;
  top: 95px;  /* 75px header + 20px spacing */
  max-height: calc(100vh - 135px);  /* 100vh - (75 + 20 + 40) */
}
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `frontend/src/components/sales/CanvasDrawingPreview.module.css` | Canvas styles (MODIFIED) |
| `frontend/src/components/sales/CanvasDrawingPreview.tsx` | Canvas component (no changes) |
| `frontend/src/components/sales/SalesPresentation.tsx` | Parent layout with header |
| `CANVAS_HEADER_STICKY_FIX.md` | Detailed documentation |

## Expected Viewport Layout

```
┌─────────────────────────────────────────────┐  80px
│ HEADER (Raven's Design Sandbox)             │
├─────────────────────────────────────────────┤
│ ┌──────────────┐ ┌─────────────────────────┐│
│ │              │ │   ← STICKY AREA STARTS  ││  100px from top
│ │ PARAMETERS   │ │   (20px below header)   ││  of viewport
│ │              │ │   CANVAS PANEL (sticky) ││
│ │ • Series     │ │   ┌─────────────────┐   ││
│ │ • Width      │ │   │  Drawing        │   ││
│ │ • Height     │ │   │                 │   ││
│ │              │ │   │  (stays visible │   ││
│ │ scroll ↓     │ │   │  while scrolling)│  ││
│ │              │ │   │                 │   ││
│ │ • Glass Type │ │   │                 │   ││
│ │ • Frame Color│ │   └─────────────────┘   ││
│ │              │ │   (max 95% viewport)   ││
│ └──────────────┘ └─────────────────────────┘│
│ (parameters scroll) (canvas sticks & scrolls)
└─────────────────────────────────────────────┘
```

## Browser Support

- ✅ Chrome 56+
- ✅ Firefox 59+
- ✅ Safari 13+
- ✅ Edge 16+
- ✅ All modern mobile browsers
- ⚠️ Older browsers use fixed positioning fallback

## Summary

| Aspect | Details |
|--------|---------|
| **Change Type** | CSS positioning update |
| **Files Changed** | 1 (CanvasDrawingPreview.module.css) |
| **Breaking Changes** | None |
| **Browser Compatibility** | Full |
| **Mobile Responsive** | Yes |
| **Performance Impact** | None (pure CSS) |

---

For full details, see [`CANVAS_HEADER_STICKY_FIX.md`](CANVAS_HEADER_STICKY_FIX.md)
