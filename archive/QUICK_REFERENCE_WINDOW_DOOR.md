# Quick Reference: Window/Door Selector Implementation

## 🎯 What Was Implemented

### 1. Split Product Type Selector ✓
- **Before**: Single "Product Type" dropdown
- **After**: Two separate dropdowns (Window Types / Door Types)
- **Behavior**: Mutually exclusive selection

### 2. Swing Direction Control ✓
- **Shows for**: Casement (windows) and Hinged Door (doors)
- **Options**: Left / Right buttons
- **Storage**: `parameters.configuration`

### 3. Plan View Image Integration ✓
- **New utility**: `src/utils/planViewImages.ts`
- **Function**: `getPlanViewImage(productType, direction)`
- **Purpose**: Map product selections to Google Sheet images

### 4. Enhanced Elevation View ✓
- **Door threshold**: Thicker bottom frame for doors
- **Slider arrows**: Directional indicators for moving panels
- **Fixed labels**: "F" markers on fixed panels
- **Door handles**: Positioned based on swing direction

---

## 📋 Quick Steps to Configure

### Step 1: Add Google Sheet Image URLs
Edit: `frontend/src/utils/planViewImages.ts`

```typescript
const imageMap = {
  'Casement_Left': 'https://YOUR_GOOGLE_SHEET_IMAGE_URL_HERE',
  'Casement_Right': 'https://YOUR_GOOGLE_SHEET_IMAGE_URL_HERE',
  // Add more URLs...
}
```

### Step 2: Test
1. Run the app: `npm run dev` (from frontend folder)
2. Select a Window Type (e.g., "Casement")
3. Toggle "Swing Direction"
4. View should update in ELEVATION section
5. Plan View should show image (if configured) or SVG fallback

### Step 3: Deploy
- All files are ready for production
- No database changes needed
- Images served directly from Google Sheets

---

## 📂 Files Modified

```
frontend/src/
├── components/
│   ├── sales/
│   │   ├── SmartParameterPanel.tsx      ← Window/Door split
│   │   └── CanvasDrawingPreview.tsx     ← Plan View image rendering
│   └── WindowElevationView.jsx          ← Door features (arrows, handles, threshold)
└── utils/
    └── planViewImages.ts                ← NEW: Image URL mapping
```

---

## 🧪 Testing Scenarios

| Scenario | Expected Result |
|----------|-----------------|
| Select "Casement" | Swing Direction toggle appears |
| Select "Hinged Door" | Swing Direction toggle appears |
| Select "Fixed" window | Swing Direction toggle hides |
| Switch Window→Door type | Previous selection clears |
| Slider door shown | Arrows visible on first panel, "F" on fixed |
| Hinged door shown | Handle on left/right based on swing direction |
| Image URL configured | Plan View shows image instead of SVG |
| Image URL null/missing | Falls back to SVG (DoorSwingPlanView) |

---

## 🔗 Component Relationships

```
SmartParameterPanel
    │
    ├─→ Updates: parameters.productType (e.g., "Casement", "Hinged Door")
    └─→ Updates: parameters.configuration (e.g., "Left", "Right")
           │
           └─→ Passed to CanvasDrawingPreview
               │
               ├─→ WindowElevationView (sees productType + swingDirection)
               │   └─→ Renders door features (threshold, arrows, handles)
               │
               └─→ Plan View Image Lookup (uses planViewImages.ts)
                   └─→ Renders image or falls back to DoorSwingPlanView SVG
```

---

## 🚀 Next Features (Optional)

- [ ] Add more grid configurations (3-panel, 4-panel sliders)
- [ ] Custom icons for each product type
- [ ] Animated slider arrows
- [ ] Door swing animation in preview
- [ ] Material thickness visualization

---

## 💡 Tips

1. **Google Sheet Image Links**: Make sure images are publicly viewable
2. **Fallback Behavior**: If image fails, SVG renders automatically
3. **Storage**: Swing direction in `configuration` field (flexible for other uses)
4. **Extensible**: Easy to add more product types by updating arrays in SmartParameterPanel

---

## 📞 Support

- **Image mapping issues?** Check `planViewImages.ts` - ensure URLs are valid
- **Selection not clearing?** Check `setParameters()` calls in SmartParameterPanel
- **Door features not showing?** Check `productType` string matching in WindowElevationView
