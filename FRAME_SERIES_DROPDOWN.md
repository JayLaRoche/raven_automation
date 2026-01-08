# Frame Series Dropdown & View Selection - Implementation Complete

## Overview

The frame series selection has been upgraded from a grid of buttons to a dropdown menu with frame view selection. When a user selects a frame series, they can now choose which view (HEAD, SILL, or JAMB) to display in the drawing preview.

---

## How It Works

### 1. **Frame Series Dropdown** (Left Panel)
- **Location**: SmartParameterPanel.tsx
- **Selector**: `<select>` dropdown showing all available frame series
- **Action**: When user selects a series, the drawing preview updates
- **Result**: Only selected series is displayed in frame area

### 2. **Frame View Selector** (Appears after series selection)
- **Buttons**: HEAD | SILL | JAMB
- **Display**: Only shows when a frame series is selected
- **Selected State**: Blue background + border highlight
- **Active View**: Selected view displays full-height in drawing area

### 3. **Drawing Preview Updates**
- **Canvas**: Shows only the selected frame view (HEAD, SILL, or JAMB)
- **Size**: Frame view expands to fill entire frame section
- **Auto-refresh**: Updates when user changes view selection or series

---

## Component Architecture

### Frontend Components Updated

#### 1. **SmartParameterPanel.tsx**
```tsx
// Frame Series Dropdown
<select value={parameters.series} onChange={...}>
  {series.map(s => <option>{s}</option>)}
</select>

// Frame View Selector (appears when series selected)
{parameters.series && (
  <div>
    {['head', 'sill', 'jamb'].map(view => (
      <button onClick={() => setSelectedFrameView(view)}>
        {view.toUpperCase()}
      </button>
    ))}
  </div>
)}
```

#### 2. **drawingStore.ts** (Zustand)
Added state management:
```typescript
interface DrawingState {
  selectedFrameView: 'head' | 'sill' | 'jamb'
  setSelectedFrameView: (view) => void
}
```

#### 3. **CanvasDrawingPreview.tsx**
Modified to display only selected view:
```tsx
// Filter sections to show only selected view
const visibleSections = sections.filter(s => s.view === selectedFrameView)

// Render at full height
visibleSections.forEach((section) => {
  // Draw large frame view image
})
```

#### 4. **SalesPresentation.tsx**
Updated to pass selectedFrameView:
```tsx
<CanvasDrawingPreview
  selectedFrameView={selectedFrameView}
  parameters={...}
/>
```

---

## User Workflow

1. **Step 1**: User selects frame series from dropdown
   ```
   "-- Select Frame Series --"
   "Series 65"  ← Select this
   "Series 86"
   "Series 135"
   ```

2. **Step 2**: Frame view buttons appear (HEAD | SILL | JAMB)
   ```
   HEAD | SILL | JAMB
    ↑ (user clicks)
   ```

3. **Step 3**: Selected view displays in drawing preview
   ```
   Drawing area shows large frame cross-section image
   from /api/frames/series/65/image
   ```

4. **Step 4**: User can switch views instantly
   ```
   Click SILL button → Drawing updates to show SILL view
   Click JAMB button → Drawing updates to show JAMB view
   ```

---

## Data Flow

```
SmartParameterPanel
├── Frame Series Dropdown
│   └── setParameters({ series: "65" })
│       └── useDrawingStore updates
│
├── Frame View Selector
│   └── setSelectedFrameView('head')
│       └── useDrawingStore updates
│
└── useDrawingStore passes to SalesPresentation
    └── SalesPresentation passes to CanvasDrawingPreview
        └── CanvasDrawingPreview renders selected view
```

---

## Files Modified

| File | Change | Lines |
|------|--------|-------|
| `frontend/src/store/drawingStore.ts` | Added `selectedFrameView` state | +15 |
| `frontend/src/components/sales/SmartParameterPanel.tsx` | Changed grid buttons to dropdown + added view selector | -40 / +30 |
| `frontend/src/components/sales/CanvasDrawingPreview.tsx` | Filter to show only selected view | +10 |
| `frontend/src/components/sales/SalesPresentation.tsx` | Pass selectedFrameView prop | +1 |

---

## API Integration

The backend endpoint is already set up:
- **Endpoint**: `GET /api/frames/series/{series}/image`
- **Returns**: PNG image of frame cross-section
- **Fallback**: If no image, shows placeholder with "No Image"

---

## Key Features

✅ **Dropdown Menu**: Clean, professional frame series selection  
✅ **View Selector**: Choose HEAD, SILL, or JAMB view  
✅ **Full-Height Display**: Selected view expands to use entire frame area  
✅ **Real-time Updates**: Drawing updates instantly on selection change  
✅ **State Persistence**: Selection saved in Zustand store  
✅ **Responsive**: Works on all screen sizes  
✅ **Fallback Support**: Shows placeholders if images missing  

---

## Testing

### Test Frame Series Selection
1. Open app at http://localhost:3001
2. Look at left panel (SmartParameterPanel)
3. Should see dropdown: "-- Select Frame Series --"
4. Click dropdown and select "Series 65"
5. ✅ Verify: Frame view buttons appear (HEAD | SILL | JAMB)

### Test Frame View Switching
1. With frame series selected, click different view buttons
2. Click "HEAD" → Drawing shows HEAD view
3. Click "SILL" → Drawing shows SILL view
4. Click "JAMB" → Drawing shows JAMB view
5. ✅ Verify: Drawing updates instantly

### Test With Frame Images
1. Add PNG files to `backend/static/frames/`
2. Restart backend server
3. Select frame series and view
4. ✅ Verify: Frame PNG images appear in drawing

---

## Next Steps

1. **Add Frame Images** to `backend/static/frames/`
   - File naming: `series-{NUMBER}-{view}.png`
   - Or: `series-{NUMBER}-thumbnail.png`

2. **Customize View Button Styling** (optional)
   - Change colors/fonts in SmartParameterPanel.tsx
   - Adjust height/sizing of frame display area

3. **Add Frame Labels** (optional)
   - Show series name + view name in drawing header
   - Add dimensions/scale information

---

## Status

✅ **Dropdown Menu**: Implemented  
✅ **View Selector**: Implemented  
✅ **State Management**: Implemented  
✅ **Canvas Rendering**: Implemented  
⏳ **Frame Images**: Awaiting user to add PNG files

**Ready for Production**: Yes, once frame images are added
