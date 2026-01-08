# Canvas Panel Sticky Fix - Visual Testing Guide

## Quick Start Testing (2 minutes)

### Prerequisites
- Frontend running: `npm run dev` in `frontend/` directory
- Backend running: Available at `http://localhost:8000` (optional for testing sticky only)
- Browser: Chrome, Firefox, Safari, or Edge (modern version)

### Test Steps

1. **Load the page**
   ```
   Open: http://localhost:3000
   Navigate: Drawing Generator tab
   ```

2. **Ensure desktop view**
   ```
   Window width should be >1024px
   If using mobile view, expand to desktop size
   DevTools: Press F12 → Click device toggle to disable mobile view
   ```

3. **Observe initial state**
   ```
   You should see:
   ✓ Header at top with "Raven's Design Sandbox" title
   ✓ Left panel with parameters (Series, Width, Height, etc.)
   ✓ Right panel with canvas drawing
   ✓ Canvas positioned ~100px from top (below header with spacing)
   ```

4. **Test sticky behavior**
   ```
   Action: Scroll the LEFT PANEL (parameters) down
   
   What you'll see:
   ✓ Canvas scrolls WITH the left panel initially
   ✓ Canvas doesn't stay fixed at top
   ✓ As left panel scrolls, canvas follows the scroll
   ✓ Canvas reaches a point where it "sticks" at ~100px from top
   ✓ Once stuck, left panel continues scrolling underneath
   ✓ Canvas remains visible in the viewport
   ✓ Header always stays above canvas
   ```

5. **Verify no header overlap**
   ```
   Key verification:
   ✓ Header is ALWAYS fully visible
   ✓ Canvas is ALWAYS below header
   ✓ Clear 20px gap between header and canvas
   ✓ NO overlapping or hidden content
   ```

---

## Detailed Visual Checklist

### ✅ Initial Load (Page Just Opened)

```
Viewport Layout:
┌──────────────────────────────────────────────────┐
│ HEADER: Raven's Design Sandbox                   │ ← Always visible
├──────────────────────────────────────────────────┤ ← Header border
│                20px gap                          │ ← This space here
│ ┌─────────────────┐  ┌──────────────────────┐   │
│ │                 │  │ CANVAS DRAWING       │   │ ← Canvas starts at 100px
│ │ PARAMETERS      │  │ ┌────────────────┐   │   │
│ │ Series  [  ]    │  │ │ Technical      │   │   │
│ │ Width   [  ]    │  │ │ Drawing Here   │   │   │
│ │ Height  [  ]    │  │ │                │   │   │
│ │ Glass   [   ▼]  │  │ │                │   │   │
│ │                 │  │ │                │   │   │
│ └─────────────────┘  │ │                │   │   │
│                      │ │                │   │   │
│                      │ │                │   │   │
│                      │ └────────────────┘   │   │
│                      │                      │   │
│                      └──────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Expected checklist:**
- [ ] Header is at the very top
- [ ] Title "Raven's Design Sandbox" is readable
- [ ] 20px visible gap between header and canvas
- [ ] Canvas doesn't touch the header
- [ ] Parameters panel is on the left
- [ ] Canvas panel is on the right

### ✅ After Scrolling Down (User scrolls left panel)

```
User scrolls the LEFT PANEL down...

┌──────────────────────────────────────────────────┐
│ HEADER: Still visible at top                     │ ← Never hidden
├──────────────────────────────────────────────────┤
│                20px gap                          │ ← Still here
│ ┌─────────────────┐  ┌──────────────────────┐   │
│ │ PARAMETERS      │  │ CANVAS               │   │ ← Sticks at 100px!
│ │ • Glass Type    │  │ ┌────────────────┐   │   │
│ │ • Frame Color   │  │ │ Drawing        │   │   │
│ │ • Configuration │  │ │ (STICKY!)      │   │   │
│ │ • Notes         │  │ │                │   │   │
│ │   [           ] │  │ │ Stays visible  │   │   │
│ │                 │  │ │ while params   │   │   │
│ │ scroll down ↓   │  │ │ scroll under   │   │   │
│ │                 │  │ │                │   │   │
│ │ • Item Number   │  │ │                │   │   │
│ │ • PO Number     │  │ │                │   │   │
│ │                 │  │ │                │   │   │
│ └─────────────────┘  │ │                │   │   │
│ ↓ (more params)     │ │                │   │   │
│                      │ └────────────────┘   │   │
│                      │                      │   │
│                      └──────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Expected checklist:**
- [ ] Header is still at top (not scrolled away)
- [ ] Canvas stayed at ~100px from top (didn't scroll with params)
- [ ] Canvas is now "stuck" in place
- [ ] Parameters scrolled underneath canvas
- [ ] 20px gap still visible between header and canvas
- [ ] Canvas appears to be sticky (fixed relative to viewport)

### ✅ Scrolling More (Continue scrolling down)

```
User keeps scrolling the left panel...

┌──────────────────────────────────────────────────┐
│ HEADER: Still visible                            │ ← Always on top
├──────────────────────────────────────────────────┤
│                20px gap                          │
│ ┌─────────────────┐  ┌──────────────────────┐   │
│ │ PARAMETERS      │  │ CANVAS               │   │ ← Still sticky!
│ │ (scrolling...)  │  │ ┌────────────────┐   │   │
│ │                 │  │ │ Drawing        │   │   │
│ │ • Item #1       │  │ │ (Remains visible) │ │   │
│ │ • Item #2       │  │ │                │   │   │
│ │ • Item #3       │  │ │ No jumping or  │   │   │
│ │ • Item #4       │  │ │ unexpected     │   │   │
│ │   [...]         │  │ │ movement       │   │   │
│ │ • Item #20      │  │ │                │   │   │
│ │   [...]         │  │ │                │   │   │
│ │ • Item #50      │  │ │                │   │   │
│ │   [...]         │  │ │ Canvas height  │   │   │
│ │ (end of list)   │  │ │ lets you see   │   │   │
│ │                 │  │ │ the drawing    │   │   │
│ └─────────────────┘  │ └────────────────┘   │   │
│                      │                      │   │
│                      └──────────────────────┘   │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Expected checklist:**
- [ ] Canvas never moves from 100px position
- [ ] Parameters scroll completely past canvas
- [ ] Canvas content is fully visible
- [ ] No layout jumping or shifting
- [ ] Scrolling is smooth (no jank)
- [ ] Header remains visible throughout

### ✅ Bottom of Parameters (User scrolls all the way down)

```
User reaches bottom of parameters list...

┌──────────────────────────────────────────────────┐
│ HEADER: Still there                              │
├──────────────────────────────────────────────────┤
│                20px gap                          │
│ ┌─────────────────┐  ┌──────────────────────┐   │
│ │ PARAMETERS      │  │ CANVAS               │   │
│ │                 │  │ ┌────────────────┐   │   │
│ │ • Last item     │  │ │ Drawing        │   │   │
│ │   [value]       │  │ │                │   │   │
│ │                 │  │ │ (100% viewport │   │   │
│ │ (end of list)   │  │ │  visible)      │   │   │
│ │                 │  │ │                │   │   │
│ │ [No more items] │  │ │                │   │   │
│ │                 │  │ │                │   │   │
│ └─────────────────┘  │ │                │   │   │
│ ↑ Can't scroll more  │ │                │   │   │
│                      │ │                │   │   │
│                      │ │                │   │   │
│                      │ └────────────────┘   │   │
│                      │                      │   │
│                      └──────────────────────┘   │
└──────────────────────────────────────────────────┘
```

**Expected checklist:**
- [ ] Parameters list has reached end
- [ ] Canvas is still visible and at correct position
- [ ] Canvas didn't scroll past or get hidden
- [ ] No over-scrolling or bouncing

---

## Troubleshooting During Testing

### Issue: Canvas scrolls to top with parameters

**Expected:** Canvas should scroll WITH params, then STICK

**If this happens:** 
- Check browser console (F12) for errors
- Check that browser supports `position: sticky` (Chrome 56+)
- Verify `CanvasDrawingPreview.module.css` was updated correctly
- Check CSS file for typos in `top: 100px` value

### Issue: Canvas at very top (not below header)

**Problem:** Canvas is at 20px instead of 100px

**If this happens:**
- Check if CSS wasn't saved properly
- Verify `top: 100px` in the CSS file
- Clear browser cache: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
- Refresh page: Ctrl+F5

### Issue: Canvas overlaps header

**Problem:** Canvas is going under the header text

**If this happens:**
- Check actual header height on your system
- Header might be taller than 80px
- Use DevTools to measure: Inspect header → Check computed height
- If header is different, update `top` value accordingly
- Formula: `top: actual_header_height + 20px`

### Issue: Canvas content is cut off at bottom

**Problem:** Canvas can't display full drawing

**If this happens:**
- Check `max-height: calc(100vh - 140px)` value
- Try increasing to `calc(100vh - 120px)` or `calc(100vh - 100px)`
- This gives canvas more vertical space
- Note: Make sure header still stays visible

### Issue: Sticky doesn't work in Firefox/Safari

**Problem:** Canvas doesn't stick (older browser)

**Expected:** Modern browsers should work fine

**If issue persists:**
- Update browser to latest version
- Some versions have bugs in sticky positioning
- Fallback uses `position: fixed` which should work

---

## Responsive Testing

### Tablet View (1024px - 768px)

```
Expected behavior:
1. Resize browser to 1024px wide
2. Layout changes to single column
3. Canvas below parameters
4. NO sticky effect
5. Normal scrolling

Visual:
┌──────────────────────────┐
│ HEADER                   │
├──────────────────────────┤
│ PARAMETERS (100% width)  │
│ • Series                 │
│ • Width/Height           │
│ • Glass Type             │
│ scroll down ↓            │
└──────────────────────────┘
                            
┌──────────────────────────┐
│ CANVAS (100% width)      │
│ ┌────────────────────┐   │
│ │ Drawing Here       │   │
│ │                    │   │
│ │ (normal scrolling) │   │
│ │                    │   │
│ └────────────────────┘   │
└──────────────────────────┘
```

**Test checklist:**
- [ ] Window is 768-1024px wide
- [ ] Layout is single column
- [ ] Parameters stack above canvas
- [ ] Sticky is disabled
- [ ] Normal scrolling behavior

### Mobile View (<768px)

```
Expected behavior:
1. Resize browser to <768px
2. Full-width stacked layout
3. Canvas below parameters
4. NO sticky effect
5. Normal scrolling

Visual:
┌──────────────┐
│ HEADER       │
├──────────────┤
│ PARAMETERS   │
│ (full width) │
│              │
│ Series  [ ]  │
│ Width   [ ]  │
│              │
│ scroll ↓     │
└──────────────┘

┌──────────────┐
│ CANVAS       │
│ (full width) │
│              │
│ ┌──────────┐ │
│ │ Drawing  │ │
│ │          │ │
│ └──────────┘ │
│              │
└──────────────┘
```

**Test checklist:**
- [ ] Window is <768px wide
- [ ] Full-width layout
- [ ] Parameters and canvas stack vertically
- [ ] No sticky effects
- [ ] Smooth natural scrolling

---

## Success Criteria

### ✅ All Good If:

1. **Desktop (>1024px)**
   - ✓ Canvas sticks at ~100px from top
   - ✓ Header stays visible above
   - ✓ 20px gap between header and canvas
   - ✓ Parameters scroll under canvas
   - ✓ No visual overlap or glitches

2. **Tablet/Mobile (<1024px)**
   - ✓ Sticky is disabled
   - ✓ Canvas stacks below parameters
   - ✓ Normal scrolling throughout
   - ✓ No unexpected behavior

3. **Overall**
   - ✓ Smooth scrolling (no jank)
   - ✓ No console errors
   - ✓ Works in multiple browsers
   - ✓ Responsive design intact

### ❌ Something's Wrong If:

1. Canvas scrolls to top (should stick at 100px)
2. Canvas overlaps header
3. Canvas content is cut off
4. Layout breaks on resize
5. Smooth scrolling is janky
6. Console shows CSS errors

---

## Verification Steps

### Step 1: Visual Inspection (30 seconds)
```
✓ Load page
✓ Look at canvas position relative to header
✓ Verify 20px gap exists
✓ Check header is fully visible
```

### Step 2: Scroll Test (1 minute)
```
✓ Scroll left panel down slowly
✓ Watch canvas stick at 100px position
✓ Verify smooth sticking behavior
✓ Confirm parameters scroll underneath
```

### Step 3: Responsive Test (1 minute)
```
✓ Resize to tablet (1024px)
✓ Verify sticky is disabled
✓ Resize to mobile (<768px)
✓ Verify normal stacking
```

### Step 4: Browser Test (2 minutes)
```
✓ Test in Chrome
✓ Test in Firefox
✓ Test in Safari/Edge (if available)
✓ Verify all show same behavior
```

**Total time: ~5 minutes for complete verification**

---

## Final Sign-Off

When you can confirm all of the following, the fix is working correctly:

```
✅ Desktop: Canvas sticks 100px from top (below header)
✅ Desktop: Parameters scroll under sticky canvas
✅ Desktop: 20px gap between header and canvas
✅ Tablet: Sticky disabled, single column layout
✅ Mobile: Sticky disabled, full-width stacked
✅ All browsers: Smooth scrolling, no errors
✅ All browsers: No visual glitches or overlap
```

If all of these check out, the Canvas Header-Aware Sticky Fix is complete and working! 🎉
