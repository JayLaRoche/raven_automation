# Plan View Schematic - Quick Visual Reference

## Component Overview

```
┌─────────────────────────────────────────┐
│     Drawing Canvas (1122×794px)         │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ ELEVATION (top section)          │  │
│  │ [WindowElevationView SVG]         │  │
│  │ Shows front elevation view        │  │
│  │ with grid lines & dimensions     │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ PLAN (bottom section)            │  │
│  │ [PlanViewSchematic SVG] ← NEW!   │  │
│  │ Shows top-down orientation       │  │
│  │ with swing arcs & human figure   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Opening Type Examples

### FIXED
```
PLAN VIEW (top-down)
┌─────────────────┐
│                 │  ← Static window
│  [FIXED]        │  (no opening)
│                 │
└─────────────────┘
```

### SWING-LEFT (Casement Left)
```
PLAN VIEW (top-down)
┌─────────────────┐   ┌─────  ← Swing arc
│                 │   │
│  ⌐─────────────┘ ▶  Hinge (left side)
│                     ↓ Direction arrow
└─────────────────┐
                    [INSIDE] 🚶
```

### SWING-RIGHT (Casement Right)
```
PLAN VIEW (top-down)
┌─────────────────┐      
│                 │   ─────┐  ← Swing arc
│ ┌──────────────⌐│  ◀ Hinge (right side)
│                 │      ↓ Direction arrow
└─────────────────┘
                   [INSIDE] 🚶
```

### SLIDER (Horizontal Sliding)
```
PLAN VIEW (top-down)
┌──────────┬──────┐
│ FIXED    │SLIDE │  ← Dividing line
│          │      │  
└──────────┴──────┘  ──────────►  (slide direction arrow)
                     
                     [INSIDE] 🚶
```

### DOUBLE-HUNG (Vertical Sliding)
```
PLAN VIEW (top-down)
┌─────────────────┐
│                 │  ⬆ (top sash moves up)
├─────────────────┤  
│                 │  ⬇ (bottom sash moves down)
└─────────────────┘

[INSIDE] 🚶
```

## Canvas Positioning

### Coordinate System
```
Canvas: 1122×794px (A4 Landscape)

┌──────────────────────────────────────┐
│                                      │
│  ┌──────────────────────────────┐  │
│  │                              │  │ 
│  │    ELEVATION                 │  │ y=110px
│  │    left: 48.3%, top: 13.8%   │  │ height: 350px (44%)
│  │    width: 25%, height: 44%   │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │    PLAN                      │  │ y=515px
│  │    left: 48.3%, top: 64.8%   │  │ height: 206px (26%)
│  │    width: 25%, height: 26%   │  │
│  │    ← PlanViewSchematic SVG   │  │
│  └──────────────────────────────┘  │
│                                      │
└──────────────────────────────────────┘
```

### Responsive Scaling
- **Canvas Width:** 100% of container
- **PLAN Box:** Always 25% of canvas width
- **SVG ViewBox:** 0 0 240 120 (internal coordinates)
- **Aspect Ratio:** Maintains 2:1 ratio (240:120)

## Data Flow

```
SmartParameterPanel
  │
  ├─ productType: "CASEMENT" ───┐
  │                              │
  ├─ width: 24 (inches) ────────┤
  │                              │
  └─ height: 36 (inches) ────────┤
                                 │
                                 ▼
                    CanvasDrawingPreview
                                 │
                                 ├─ Convert width: 24in → 609.6mm
                                 │  (24 × 25.4)
                                 │
                                 └─ Lowercase type: "casement"
                                    │
                                    ▼
                          PlanViewSchematic
                                    │
                                    ├─ type.toLowerCase() 
                                    │  → matches "swing-left" or "swing-right"
                                    │
                                    └─ Renders SVG with swing arc
```

## SVG Structure

### Container Hierarchy
```html
<PlanViewSchematic width={609.6} type="casement">
  <div style={{ display: 'flex', ... }}>
    {/* Flex wrapper for centering */}
    <svg viewBox="0 0 240 120" preserveAspectRatio="xMidYMid meet">
      
      <g>                    {/* Window frame & hinge */}
        <rect ... />         {/* Window outline */}
        <rect ... />         {/* Hinge indicator */}
        <line ... />         {/* Sash line */}
        <path ... />         {/* Swing arc (dashed) */}
        <polygon ... />      {/* Direction arrow */}
      </g>

      <text>INSIDE</text>     {/* Position label */}
      
      <g>                    {/* Stick figure (person icon) */}
        <circle ... />       {/* Head */}
        <line ... />         {/* Body */}
        <line ... />         {/* Arms */}
      </g>

    </svg>
  </div>
</PlanViewSchematic>
```

## Props Reference

### PlanViewSchematic Component
```javascript
<PlanViewSchematic
  width={609.6}           // Number in millimeters
  type="casement"         // String: 'fixed', 'casement', 'slider', 'double-hung'
/>
```

### Type Values (Case-Insensitive)
- `'fixed'` / `'FIXED'` → Static window
- `'swing-left'` / `'casement-left'` → Left swing
- `'swing-right'` / `'casement-right'` → Right swing  
- `'slider'` / `'sliding'` → Horizontal slide
- `'double-hung'` / `'double_hung'` → Vertical slide
- Default fallback: `'fixed'`

## Styling Notes

### Appearance
- **Lines:** Black (stroke: #000000)
- **Glass:** White fill with black outline
- **Hinges:** Solid black fill
- **Arcs:** Dashed line (4px dash, 4px gap)
- **Arrows:** Solid black triangles
- **Figure:** Outline style (no fill)
- **Text:** Italic gray (#666)

### Dimensions
- **Window Frame:** 140×30px (internal coords)
- **Hinge Width:** 6px
- **Arrow Size:** Variable (5-15px)
- **Person Icon:** Scaled 0.8x (original ~25px)

## Integration Checklist

- ✅ Component created: `PlanViewSchematic.jsx`
- ✅ Import added to `CanvasDrawingPreview.tsx`
- ✅ Overlay div positioned correctly (48.3%, 64.8%)
- ✅ Props wired from canvas parameters
- ✅ All opening types supported
- ✅ Responsive sizing implemented
- ✅ No compilation errors
- ✅ PropTypes validation added
- ✅ Default props set
- ✅ Ready for production

## Testing Steps

1. **Navigate to Drawing Generator page**
2. **Change Product Type dropdown:**
   - FIXED → Verify static rectangle
   - CASEMENT → Verify swing arc appears
   - SLIDER → Verify sliding arrow appears
   - DOUBLE-HUNG → Verify dual arrows appear
3. **Change Width value (e.g., 24" → 36"):**
   - SVG should scale proportionally
4. **Verify human figure visible in all modes**
5. **Check INSIDE label displays correctly**
6. **Confirm no overlapping with other elements**

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Plan view not visible | CSS overflow hidden on parent | Remove `overflow: hidden` or adjust positioning |
| SVG distorted | ViewBox aspect ratio mismatch | Check `preserveAspectRatio="xMidYMid meet"` |
| Person icon overlapping window | Incorrect x/y coordinates | Verify renderPersonIcon(185, 50) positioning |
| Type not matching | Case sensitivity | Use `type.toLowerCase()` in switch statement |
| Layout breaking | Flex container issues | Verify `display: flex` and `align-items: center` |

---

**Quick Start:** The Plan View Schematic is now integrated into the canvas overlay system. Change the product type dropdown and the schematic will automatically update! 🎨
