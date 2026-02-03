# Feature Implementation Summary: Window vs. Door Selector & Plan View Images

## Overview
Successfully implemented a major feature update that separates Window vs. Door selection, adds swing direction logic, and prepares infrastructure for Plan View image integration from Google Sheets.

---

## Changes Made

### 1. **SmartParameterPanel.tsx** - Split Product Selectors ✓

#### What Changed:
- **Replaced** single "Product Type" dropdown with **two separate dropdowns**:
  - **Window Unit Type**: Fixed, Casement, Double Casement, Slider, Hung, Double Hung, Accordian, Awning, Curtain Wall
  - **Door Unit Type**: Hinged Door, Double Door (French), 2 Panel Slider, 3 Track 3 Panel, 4 Track 4 Panel, 4 Panel meet in the middle

#### Mutual Exclusivity Logic:
- Selecting a Window Type clears the Door Type selection
- Selecting a Door Type clears the Window Type selection
- **Stored in**: `parameters.productType`

#### Swing Direction Control:
- **Appears conditionally** when:
  - **Window**: "Casement" is selected
  - **Door**: "Hinged Door" is selected
- Two toggle buttons: "Left" and "Right"
- **Stored in**: `parameters.configuration`

---

### 2. **planViewImages.ts** (NEW) - Mapping Utility ✓

#### Location:
`frontend/src/utils/planViewImages.ts`

#### Functionality:
- **Export**: `getPlanViewImage(productType, direction)` → Returns image URL or null
- **Export**: `hasPlanViewImage(productType, direction)` → Boolean check
- **Export**: `getConfiguredPlanViewKeys()` → Helper for debugging

#### Structure:
```typescript
const imageMap: PlanViewImageMap = {
  'Casement_Left': null,      // Placeholder - replace with Google Sheet URL
  'Casement_Right': null,
  'Hinged Door_Left': null,
  'Hinged Door_Right': null,
  'Slider': null,
  // ... more product types
}
```

#### How to Use:
1. Open your Google Sheet with Plan View images
2. Right-click each image → "Copy image link"
3. Paste the URL into the `imageMap` object, replacing `null` values
4. The utility will automatically match product type + direction to image

---

### 3. **CanvasDrawingPreview.tsx** - Plan View Image Rendering ✓

#### What Changed:
- **Added import**: `getPlanViewImage` and `hasPlanViewImage` utilities
- **Plan View Section**: Now checks for image URL before rendering
  - **If image exists**: Renders the image in the PLAN section
  - **If no image**: Falls back to existing SVG (`DoorSwingPlanView`)
  - **Image maintains aspect ratio** with `maxWidth: 90%`, `maxHeight: 90%`

#### Overlay Position:
```jsx
<div style={{
  position: 'absolute',
  left: '30.85%',    // Matches ELEVATION box
  top: '53.5%',      // Below ELEVATION in PLAN area
  width: '35.89%',   // Same width as ELEVATION
  height: '20%',     // Fits in PLAN area
}}>
  {/* Image or SVG rendered here */}
</div>
```

---

### 4. **WindowElevationView.jsx** - Door Support ✓

#### New Props:
```jsx
<WindowElevationView
  width={...}                          // In mm
  height={...}                         // In mm
  gridCols={2}
  gridRows={3}
  productType="Slider"                 // NEW: for door detection
  swingDirection="Right"               // NEW: for handle placement
/>
```

#### Door Features Implemented:

##### 1. **Thicker Threshold (Bottom Frame)**
- Automatically detected from `productType` (includes "door" or "slider")
- Threshold line weight: **20px** (vs 10px for windows)
- Visual indicator of door bottom frame

##### 2. **Slider Door Arrows**
- When `productType.includes('Slider')`:
  - **First panel**: Directional arrow pointing right (moving panel)
  - **Other panels**: "F" label (fixed panels)
- Arrow components created with `<line>` and `<polygon>` for filled head

##### 3. **Hinged Door Handle**
- When `productType.includes('Hinged Door')`:
  - Small black rectangle (8×60px) positioned based on `swingDirection`
  - **Left swing**: Handle on left edge
  - **Right swing**: Handle on right edge

##### 4. **Grid Adjustments**
- Vertical lines now stop at threshold (don't cross bottom frame for doors)

---

## File Changes Summary

| File | Change Type | Key Updates |
|------|-------------|------------|
| `SmartParameterPanel.tsx` | Modified | Split product selectors, added swing direction toggle |
| `CanvasDrawingPreview.tsx` | Modified | Added Plan View image rendering logic, updated props passing |
| `WindowElevationView.jsx` | Modified | Added door rendering (threshold, arrows, handles), new props |
| `planViewImages.ts` | Created | New utility for Google Sheets image mapping |

---

## How to Add Google Sheets Images

### Step 1: Prepare Your Images
1. Open your Google Sheet with Plan View images
2. Right-click each image
3. Select "Copy image link"

### Step 2: Update planViewImages.ts
```typescript
const imageMap: PlanViewImageMap = {
  'Casement_Left': 'https://lh3.googleusercontent.com/...',  // Paste link here
  'Casement_Right': 'https://lh3.googleusercontent.com/...',
  'Hinged Door_Left': 'https://lh3.googleusercontent.com/...',
  'Hinged Door_Right': 'https://lh3.googleusercontent.com/...',
  '2 Panel Slider': 'https://lh3.googleusercontent.com/...',
  // ... etc
}
```

### Step 3: Test
- Select a product type with a configured image
- The image will render in the PLAN section
- If image fails to load, SVG fallback activates

---

## Technical Details

### Data Flow
```
SmartParameterPanel
  ↓ (User selects Window/Door Type)
  ↓ setParameters({ productType: '...' })
  ↓
CanvasDrawingPreview
  ↓ (receives parameters)
  ↓ getPlanViewImage(productType, configuration)
  ↓
WindowElevationView
  ↓ (props: productType, swingDirection)
  ↓ (renders door features conditionally)
```

### State Management Notes
- `parameters.productType`: Stores selected window or door type
- `parameters.configuration`: Stores swing direction ("Left" or "Right")
- These merge into Zustand store via `setParameters()`

### Fallback Behavior
- **If image URL is null**: Renders `DoorSwingPlanView` SVG (existing behavior)
- **If image fails to load**: Console warning + fallback to SVG
- **If product type is not configured**: Uses SVG

---

## Testing Checklist

- [ ] Select "Casement" → Swing Direction toggle appears
- [ ] Select "Hinged Door" → Swing Direction toggle appears
- [ ] Select other types → Swing Direction toggle hidden
- [ ] Switch from Window to Door type → Previous selection clears
- [ ] WindowElevationView shows thicker bottom frame for door types
- [ ] Slider doors show arrows and "F" labels
- [ ] Hinged doors show handle on correct side based on swing direction
- [ ] Plan View image renders when URL is configured
- [ ] Plan View fallback to SVG when image URL is null/missing

---

## Next Steps

1. **Add Google Sheet Image Links**
   - Update `planViewImages.ts` with actual image URLs from your Google Sheet
   - Test rendering in the PLAN section

2. **Optional Enhancements**
   - Add more grid layouts (3-panel sliders, 4-panel configurations)
   - Create custom door/window icons for each type
   - Add animation to slider arrows

3. **Production Deployment**
   - Ensure Google Sheet image URLs are publicly accessible
   - Test image loading from production environment
   - Update CORS if images are served from different domain

---

## Files Modified
- ✓ `frontend/src/components/sales/SmartParameterPanel.tsx`
- ✓ `frontend/src/components/sales/CanvasDrawingPreview.tsx`
- ✓ `frontend/src/components/WindowElevationView.jsx`
- ✓ `frontend/src/utils/planViewImages.ts` (NEW)

All code compiles without errors. Ready for testing!
