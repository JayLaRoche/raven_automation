# Component Registry - Quick Reference

## Quick Start

### 1. Import the Registry
```javascript
import { getFrameSeriesConfig, getProductTypeConfig } from '../config/ComponentRegistry'
```

### 2. Use the Hook (Recommended)
```javascript
import { useComponentRegistry } from '../hooks/useComponentRegistry'

function MyComponent({ seriesId, productType }) {
  const {
    seriesName,
    productName,
    headProfile,
    sillProfile,
    jambProfile,
    schematicType,
  } = useComponentRegistry(seriesId, productType)
  // Use the data...
}
```

### 3. Use ProfileDisplay Component
```javascript
import ProfileDisplay from '../components/ProfileDisplay'

<ProfileDisplay seriesId="65" profileType="HEAD" width={300} height={200} />
```

### 4. Use OpeningSchematic Component
```javascript
import OpeningSchematic from '../components/OpeningSchematic'

<OpeningSchematic type="casement" width={250} height={150} />
```

---

## Available Frame Series

- **65** - Series 65 (thermal-break, weather-seal)
- **86** - Series 86 (heavy-duty variant)
- **135** - Series 135 (commercial-grade)
- **4518** - Series 4518 (slim-profile)

**Dynamic lookup:**
```javascript
const config = getFrameSeriesConfig('65')
console.log(config.name) // "Series 65"
console.log(config.headProfile.path) // "/assets/profiles/series65-head.svg"
```

---

## Available Product Types

- **FIXED** - Non-operating fixed pane
- **CASEMENT** - Side-hinged swinging window
- **DOUBLE-HUNG** - Vertically sliding window
- **SLIDING** - Horizontally sliding window
- **PATIO-DOOR** - Sliding or hinged patio door
- **AWNING** - Top-hinged outward opening window

**Dynamic lookup:**
```javascript
const config = getProductTypeConfig('CASEMENT')
console.log(config.name) // "Casement Window"
console.log(config.schematicType) // "casement"
console.log(config.openingStyle) // "swing"
```

---

## ProfileDisplay Component

Displays frame profile sections (HEAD, SILL, JAMB) with automatic loading states.

**Props:**
```tsx
<ProfileDisplay
  seriesId="65"           // Required: Frame series ID
  profileType="HEAD"      // Required: 'HEAD', 'SILL', or 'JAMB'
  width={300}            // Optional: Width in pixels (default: 300)
  height={200}           // Optional: Height in pixels (default: 200)
/>
```

**Features:**
- ✅ Automatic image loading detection
- ✅ Error handling with fallback UI
- ✅ Loading state display
- ✅ Responsive sizing
- ✅ Reacts to series changes

**Example:**
```jsx
function FrameDetails({ series }) {
  return (
    <>
      <ProfileDisplay seriesId={series} profileType="HEAD" width={280} height={200} />
      <ProfileDisplay seriesId={series} profileType="SILL" width={280} height={200} />
      <ProfileDisplay seriesId={series} profileType="JAMB" width={280} height={200} />
    </>
  )
}
```

---

## OpeningSchematic Component

Renders visual diagrams showing how windows/doors open.

**Props:**
```tsx
<OpeningSchematic
  type="casement"    // Required: Type of opening
  width={200}       // Optional: Width in pixels (default: 200)
  height={150}      // Optional: Height in pixels (default: 150)
/>
```

**Supported Types:**
- `fixed` / `FIXED` - Static rectangle
- `casement` / `CASEMENT` - Swing arc with hinge
- `double-hung` / `DOUBLE-HUNG` - Vertical sliders
- `sliding` / `SLIDING` - Horizontal slider
- `patio-door` / `PATIO-DOOR` - Large sliding door
- `awning` / `AWNING` - Top-hinged outward

**Example:**
```jsx
function ProductSelector({ selectedProduct }) {
  const productConfig = getProductTypeConfig(selectedProduct)
  return (
    <OpeningSchematic
      type={productConfig.schematicType}
      width={250}
      height={150}
    />
  )
}
```

---

## Complete Integration Example

```jsx
import { useState } from 'react'
import { useComponentRegistry } from '../hooks/useComponentRegistry'
import ProfileDisplay from '../components/ProfileDisplay'
import OpeningSchematic from '../components/OpeningSchematic'
import { FRAME_SERIES_MAP, PRODUCT_TYPE_MAP } from '../config/ComponentRegistry'

export default function DrawingPanel() {
  const [series, setSeries] = useState('65')
  const [productType, setProductType] = useState('CASEMENT')

  const registry = useComponentRegistry(series, productType)

  return (
    <div className="drawingPanel">
      {/* Controls */}
      <div className="controls">
        <div>
          <label>Frame Series:</label>
          <select value={series} onChange={(e) => setSeries(e.target.value)}>
            {Object.keys(FRAME_SERIES_MAP).map(id => (
              <option key={id} value={id}>
                {FRAME_SERIES_MAP[id].name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label>Product Type:</label>
          <select value={productType} onChange={(e) => setProductType(e.target.value)}>
            {Object.entries(PRODUCT_TYPE_MAP).map(([key, config]) => (
              <option key={key} value={key}>
                {config.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Display */}
      <div className="displayArea">
        <section>
          <h3>{registry.seriesName}</h3>
          
          <div className="profiles">
            <div>
              <h4>HEAD</h4>
              <ProfileDisplay seriesId={series} profileType="HEAD" width={280} height={180} />
            </div>
            <div>
              <h4>SILL</h4>
              <ProfileDisplay seriesId={series} profileType="SILL" width={280} height={180} />
            </div>
            <div>
              <h4>JAMB</h4>
              <ProfileDisplay seriesId={series} profileType="JAMB" width={280} height={180} />
            </div>
          </div>
        </section>

        <section>
          <h3>{registry.productName}</h3>
          <p>Opening Style: {registry.openingStyle}</p>
          <OpeningSchematic type={registry.schematicType} width={300} height={200} />
        </section>
      </div>
    </div>
  )
}
```

---

## File Locations

```
frontend/src/
├── config/
│   └── ComponentRegistry.js          ← Central registry
├── hooks/
│   └── useComponentRegistry.js       ← React hook
├── components/
│   ├── ProfileDisplay.jsx           ← Profile section display
│   ├── OpeningSchematic.jsx         ← Schematic diagrams
│   └── sales/
│       └── CanvasDrawingPreview.tsx ← Use ProfileDisplay here
└── COMPONENT_REGISTRY_GUIDE.md      ← Full guide
```

---

## Common Tasks

### Display HEAD profile for selected series
```jsx
<ProfileDisplay 
  seriesId={parameters.series} 
  profileType="HEAD" 
  width={250} 
  height={180} 
/>
```

### Show schematic for selected product
```jsx
const config = getProductTypeConfig(parameters.productType)
<OpeningSchematic type={config.schematicType} width={250} height={150} />
```

### Get all profile assets for a series
```jsx
const { headProfile, sillProfile, jambProfile } = useComponentRegistry(seriesId, null)
```

### Get opening style for a product
```jsx
const { openingStyle } = useComponentRegistry(null, productType)
// 'swing', 'slide', or 'none'
```

---

## Troubleshooting

### Profile images not loading?
- Check that asset paths in ComponentRegistry match actual file locations
- Verify SVG files are in `/public/assets/profiles/` directory
- Check browser console for 404 errors

### Schematic not rendering for my product type?
- Ensure product type is in PRODUCT_TYPE_MAP with matching schematicType key
- Check that OpeningSchematic.jsx has matching case-insensitive condition
- Example: `type === 'new-type' || type === 'NEW_TYPE'`

### Registry data not updating when series changes?
- Verify component is receiving updated `seriesId` prop
- Check that useComponentRegistry dependencies are correct
- ProfileDisplay should automatically re-render on seriesId change

---

## API Reference

### ComponentRegistry.js

```javascript
// Get full config for a series
getFrameSeriesConfig(seriesId: string) → object

// Get full config for a product type
getProductTypeConfig(productType: string) → object

// Get specific profile assets
getHeadProfile(seriesId: string) → object | null
getSillProfile(seriesId: string) → object | null
getJambProfile(seriesId: string) → object | null

// Check features
hasNailFlange(seriesId: string) → boolean

// Get available options
getAvailableFrameSeries() → string[]
getAvailableProductTypes() → string[]
```

### useComponentRegistry Hook

```javascript
const {
  seriesId,                    // Input series ID
  productType,                 // Input product type
  seriesConfig,               // Full series configuration
  productConfig,              // Full product configuration
  headProfile,                // HEAD profile asset
  sillProfile,                // SILL profile asset
  jambProfile,                // JAMB profile asset
  seriesName,                 // Friendly series name
  productName,                // Friendly product name
  openingStyle,               // 'swing', 'slide', or 'none'
  schematicType,              // Schematic diagram type
} = useComponentRegistry(seriesId, productType)
```

---

## Version History

- **v1.0** - Initial implementation with 4 frame series, 6 product types
  - ProfileDisplay component for frame sections
  - OpeningSchematic component with 6 diagram types
  - useComponentRegistry hook for easy access
  - Complete integration guide and examples
