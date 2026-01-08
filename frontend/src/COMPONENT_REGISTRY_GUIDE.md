# Component Registry Integration Guide

## Overview

The Component Registry system provides a centralized mapping of frame series and product types to their corresponding profile sections and schematic icons. This enables dynamic loading of correct assets when users change parameters.

## Architecture

```
ComponentRegistry.js (Config)
    ↓
useComponentRegistry.js (Hook)
    ↓
ProfileDisplay.jsx (Component)
OpeningSchematic.jsx (Component)
    ↓
SmartParameterPanel.jsx / CanvasDrawingPreview.tsx (Integration)
```

## Files Created

### 1. `src/config/ComponentRegistry.js`
**Purpose:** Central registry mapping frame series and product types to assets

**Key Exports:**
- `FRAME_SERIES_MAP` - Maps series IDs (65, 86, 135, 4518) to profile paths and metadata
- `PRODUCT_TYPE_MAP` - Maps product types (FIXED, CASEMENT, etc.) to schematic info
- `getFrameSeriesConfig(seriesId)` - Get configuration for a specific series
- `getProductTypeConfig(productType)` - Get configuration for a specific product type
- `getHeadProfile(seriesId)` - Get HEAD profile asset
- `getSillProfile(seriesId)` - Get SILL profile asset
- `getJambProfile(seriesId)` - Get JAMB profile asset

**Example:**
```javascript
import { getFrameSeriesConfig, getProductTypeConfig } from '../config/ComponentRegistry'

const seriesConfig = getFrameSeriesConfig('65')
// Returns: {
//   name: 'Series 65',
//   headProfile: { path: '/assets/profiles/series65-head.svg', ... },
//   sillProfile: { path: '/assets/profiles/series65-sill.svg', ... },
//   ...
// }

const productConfig = getProductTypeConfig('CASEMENT')
// Returns: {
//   name: 'Casement Window',
//   schematicType: 'casement',
//   openingStyle: 'swing',
//   ...
// }
```

---

### 2. `src/hooks/useComponentRegistry.js`
**Purpose:** React hook for convenient access to registry data with memoization

**Key Features:**
- Memoized lookups for performance
- Returns both series and product configurations
- Provides helper properties (seriesName, productName, openingStyle, etc.)

**Usage:**
```javascript
import { useComponentRegistry } from '../hooks/useComponentRegistry'

function MyComponent({ seriesId, productType }) {
  const {
    seriesConfig,
    productConfig,
    headProfile,
    sillProfile,
    jambProfile,
    seriesName,
    productName,
    openingStyle,
    schematicType,
  } = useComponentRegistry(seriesId, productType)

  return (
    <div>
      <h1>{seriesName} - {productName}</h1>
      <p>Opening Style: {openingStyle}</p>
      {headProfile && <img src={headProfile.path} alt={headProfile.alt} />}
    </div>
  )
}
```

---

### 3. `src/components/ProfileDisplay.jsx`
**Purpose:** Component that dynamically renders profile sections based on series

**Props:**
- `seriesId` (string) - Frame series ID (default: '65')
- `profileType` (string) - 'HEAD', 'SILL', or 'JAMB' (default: 'HEAD')
- `width` (number) - Display width in pixels (default: 300)
- `height` (number) - Display height in pixels (default: 200)

**Features:**
- Automatic image loading with loading state
- Error handling and fallback UI
- Uses ComponentRegistry for asset lookup
- Responsive to series changes

**Example Integration in CanvasDrawingPreview:**
```tsx
import ProfileDisplay from '../ProfileDisplay'

export const CanvasDrawingPreview = ({ parameters }) => {
  return (
    <div>
      {/* LEFT SECTION - Frame Cross-Sections */}
      <div className="frameSection">
        <h3>HEAD SECTION</h3>
        <ProfileDisplay
          seriesId={parameters?.series}
          profileType="HEAD"
          width={250}
          height={180}
        />
      </div>

      <div className="frameSection">
        <h3>SILL SECTION</h3>
        <ProfileDisplay
          seriesId={parameters?.series}
          profileType="SILL"
          width={250}
          height={180}
        />
      </div>

      <div className="frameSection">
        <h3>JAMB SECTION</h3>
        <ProfileDisplay
          seriesId={parameters?.series}
          profileType="JAMB"
          width={250}
          height={180}
        />
      </div>
    </div>
  )
}
```

---

### 4. `src/components/OpeningSchematic.jsx`
**Purpose:** Renders schematic diagrams showing how windows/doors open

**Props:**
- `type` (string) - Opening type: 'casement', 'fixed', 'double-hung', 'sliding', 'patio-door', 'awning'
- `width` (number) - SVG width in pixels (default: 200)
- `height` (number) - SVG height in pixels (default: 150)

**Supported Types:**
- **FIXED** - Non-operating fixed pane (rectangle)
- **CASEMENT** - Side-hinged with swing arc
- **DOUBLE-HUNG** - Vertically sliding sashes
- **SLIDING** - Horizontally sliding panel
- **PATIO-DOOR** - Large sliding door
- **AWNING** - Top-hinged outward opening

**Example Integration in SmartParameterPanel:**
```jsx
import OpeningSchematic from '../OpeningSchematic'
import { getProductTypeConfig } from '../config/ComponentRegistry'

function SmartParameterPanel({ parameters, setParameters }) {
  const productConfig = getProductTypeConfig(parameters?.productType)

  return (
    <div>
      <h3>Product Type: {productConfig.name}</h3>
      
      <OpeningSchematic
        type={productConfig.schematicType}
        width={250}
        height={150}
      />

      {/* Rest of panel */}
    </div>
  )
}
```

---

## Integration Steps

### Step 1: Update SmartParameterPanel
Add product type selection and display schematic:

```jsx
import { useState } from 'react'
import OpeningSchematic from './OpeningSchematic'
import { PRODUCT_TYPE_MAP, getProductTypeConfig } from '../config/ComponentRegistry'

export default function SmartParameterPanel({ parameters, setParameters }) {
  const [selectedProductType, setSelectedProductType] = useState(parameters?.productType || 'FIXED')

  const handleProductTypeChange = (productType) => {
    setSelectedProductType(productType)
    setParameters(prev => ({ ...prev, productType }))
  }

  const productConfig = getProductTypeConfig(selectedProductType)

  return (
    <div>
      {/* ... existing code ... */}

      {/* Product Type Selection */}
      <div className="parameterGroup">
        <label>Product Type:</label>
        <select value={selectedProductType} onChange={(e) => handleProductTypeChange(e.target.value)}>
          {Object.entries(PRODUCT_TYPE_MAP).map(([key, config]) => (
            <option key={key} value={key}>
              {config.name}
            </option>
          ))}
        </select>
      </div>

      {/* Schematic Display */}
      <div className="schematicContainer">
        <h4>Opening Schematic:</h4>
        <OpeningSchematic
          type={productConfig.schematicType}
          width={280}
          height={160}
        />
      </div>
    </div>
  )
}
```

### Step 2: Update CanvasDrawingPreview
Import and use ProfileDisplay for frame sections:

```tsx
import ProfileDisplay from '../ProfileDisplay'

export const CanvasDrawingPreview = ({ parameters, selectedFrameView = 'head' }) => {
  // ... existing code ...

  return (
    <>
      {/* LEFT COLUMN - Frame Cross-Sections */}
      <div className="leftPanel">
        <div className="sectionContainer">
          <h3>HEAD SECTION</h3>
          <ProfileDisplay
            seriesId={parameters?.series}
            profileType="HEAD"
            width={280}
            height={200}
          />
        </div>

        <div className="sectionContainer">
          <h3>SILL SECTION</h3>
          <ProfileDisplay
            seriesId={parameters?.series}
            profileType="SILL"
            width={280}
            height={200}
          />
        </div>

        <div className="sectionContainer">
          <h3>JAMB SECTION</h3>
          <ProfileDisplay
            seriesId={parameters?.series}
            profileType="JAMB"
            width={280}
            height={200}
          />
        </div>
      </div>

      {/* RIGHT COLUMN - Canvas (existing) */}
      <div className="rightPanel">
        {/* ... existing canvas code ... */}
      </div>
    </>
  )
}
```

### Step 3: Ensure Parameters Flow Correctly
Verify that `parameters` object includes:
```javascript
{
  series: '65',           // Frame series ID
  productType: 'CASEMENT', // Product type
  width: 48,              // Window width in inches
  height: 60,             // Window height in inches
  // ... other properties
}
```

---

## How It Works - Example Flow

1. **User selects Series in dropdown** → SmartParameterPanel updates `parameters.series` to '65'
2. **ComponentRegistry looks up** → `getFrameSeriesConfig('65')` returns profile paths
3. **ProfileDisplay re-renders** with new `seriesId` prop
4. **ProfileDisplay fetches** `/assets/profiles/series65-head.svg` and displays it
5. **Image dynamically updates** in the canvas

---

## Adding New Frame Series

To add a new frame series:

1. Open `src/config/ComponentRegistry.js`
2. Add entry to `FRAME_SERIES_MAP`:

```javascript
export const FRAME_SERIES_MAP = {
  // ... existing series ...
  'NEW_SERIES_ID': {
    name: 'Series NEW_NAME',
    headProfile: {
      path: '/assets/profiles/seriesNEW-head.svg',
      type: 'svg',
      alt: 'Series NEW Head Profile',
    },
    sillProfile: {
      path: '/assets/profiles/seriesNEW-sill.svg',
      type: 'svg',
      alt: 'Series NEW Sill Profile',
    },
    jambProfile: {
      path: '/assets/profiles/seriesNEW-jamb.svg',
      type: 'svg',
      alt: 'Series NEW Jamb Profile',
    },
    nailFlange: true,
    material: 'Aluminum',
    features: ['thermal-break', 'weather-seal'],
  },
}
```

3. Place SVG files in `/public/assets/profiles/` directory

---

## Adding New Product Types

To add a new product type:

1. Open `src/config/ComponentRegistry.js`
2. Add entry to `PRODUCT_TYPE_MAP`:

```javascript
export const PRODUCT_TYPE_MAP = {
  // ... existing types ...
  'NEW_TYPE': {
    name: 'New Product Type Name',
    schematicType: 'new-type', // Must match case in OpeningSchematic.jsx
    icon: 'new-type-icon',
    description: 'Description here',
    openingStyle: 'swing', // or 'slide' or 'none'
  },
}
```

3. Add matching schematic rendering in `src/components/OpeningSchematic.jsx`:

```jsx
if (type === 'new-type' || type === 'NEW_TYPE') {
  return (
    <svg {...svgProps}>
      {/* Your SVG drawing code */}
    </svg>
  )
}
```

---

## Performance Optimization

The system uses React's `useMemo` hook to prevent unnecessary re-renders:
- Registry lookups are cached based on seriesId and productType
- Only re-compute when dependencies change
- Images are lazy-loaded with loading states

---

## Next Steps

1. ✅ Create asset files (`/public/assets/profiles/*.svg`)
2. ✅ Update ComponentRegistry with actual file paths
3. ✅ Integrate ProfileDisplay into CanvasDrawingPreview
4. ✅ Integrate OpeningSchematic into SmartParameterPanel
5. ✅ Test series/product type switching
6. ✅ Add more product types as needed
