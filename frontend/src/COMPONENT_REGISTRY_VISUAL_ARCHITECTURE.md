# Component Registry - Visual Architecture & Data Flow

## System Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                         RAVEN DRAWING SYSTEM                           │
└────────────────────────────────────────────────────────────────────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ↓                    ↓                    ↓
         ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
         │   SmartParam│    │   CanvasDrawing │   │  Elevation  │
         │   Panel     │    │   Preview      │   │   View      │
         │             │    │                │   │             │
         └──────┬──────┘    └────────┬───────┘   └─────────────┘
                │                    │
                │  setParameters()   │
                │  (series, product) │
                ↓                    ↓
        ┌───────────────────────────────────┐
        │    Parameters Context/State        │
        │  {                                 │
        │    series: '86',                   │
        │    productType: 'CASEMENT',        │
        │    width: 48,                      │
        │    height: 60                      │
        │  }                                 │
        └────────────┬──────────────────────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
        ↓                           ↓
   ┌─────────────────┐    ┌──────────────────┐
   │ ProfileDisplay  │    │ OpeningSchematic │
   │   Component     │    │   Component      │
   └────────┬────────┘    └────────┬─────────┘
            │                      │
            ↓                      ↓
   ┌─────────────────┐    ┌──────────────────┐
   │useComponentReg. │    │getProductTypeReg.│
   │   (Hook)        │    │    (Function)    │
   └────────┬────────┘    └────────┬─────────┘
            │                      │
            └──────────────┬───────┘
                          ↓
        ┌─────────────────────────────┐
        │   ComponentRegistry.js       │
        │   (Central Registry)         │
        │                             │
        │  FRAME_SERIES_MAP {         │
        │    '65': {...},             │
        │    '86': {...},             │
        │    '135': {...},            │
        │    '4518': {...}            │
        │  }                          │
        │                             │
        │  PRODUCT_TYPE_MAP {         │
        │    'FIXED': {...},          │
        │    'CASEMENT': {...},       │
        │    'DOUBLE-HUNG': {...},    │
        │    'SLIDING': {...},        │
        │    'PATIO-DOOR': {...},     │
        │    'AWNING': {...}          │
        │  }                          │
        └──────────┬──────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ↓                     ↓
  Profile Asset         Schematic Type
  /assets/profiles/     'casement' →
  series86-head.svg     Render Diagram
```

---

## Data Flow - User Changes Series from 65 → 86

```
USER ACTION: Click Series 86 in dropdown
        │
        ↓
SmartParameterPanel.handleSeriesChange('86')
        │
        ├─→ setSelectedSeries('86')
        │
        ├─→ setParameters(prev => ({ ...prev, series: '86' }))
        │
        └─→ onParametersChange() callback
                │
                ↓
        CanvasDrawingPreview receives updated prop
        {
          parameters: {
            series: '86',  ← CHANGED
            productType: 'CASEMENT',
            ...
          }
        }
                │
                ↓
        ProfileDisplay components re-render with seriesId='86'
                │
        ┌───────┼───────┐
        ↓       ↓       ↓
       HEAD   SILL    JAMB
       │       │       │
        └───────┼───────┘
                ↓
        useComponentRegistry('86', null)
                │
                ├─→ useMemo(() => 
                │     getFrameSeriesConfig('86'), ['86']
                │   )
                │
                └─→ Returns:
                    {
                      seriesConfig: {
                        name: 'Series 86',
                        headProfile: {
                          path: '/assets/profiles/series86-head.svg',
                          type: 'svg',
                          alt: 'Series 86 Head Profile'
                        },
                        sillProfile: {...},
                        jambProfile: {...},
                        ...
                      },
                      headProfile: {...},
                      sillProfile: {...},
                      jambProfile: {...}
                    }
                │
                ↓
        ProfileDisplay renders <img> tag
        <img 
          src="/assets/profiles/series86-head.svg"
          alt="Series 86 Head Profile"
        />
                │
                ↓
        Browser loads SVG from public directory
                │
                ↓
        Image renders in canvas layout
                │
                ↓
        USER SEES: Series 86 HEAD profile ✓
```

---

## Component Interaction Map

### ProfileDisplay Component

```
Input Props:
┌─────────────────────────────────┐
│ seriesId: '86'    (required)     │
│ profileType: 'HEAD' (required)   │
│ width: 300        (optional)     │
│ height: 200       (optional)     │
└────────────┬────────────────────┘
             │
             ↓
      useComponentRegistry Hook
      ├─→ Looks up series config
      ├─→ Extracts matching profile
      └─→ Returns headProfile object
             │
             ↓
      Check if asset exists
      ├─→ YES: Render <img>
      │         └─→ Load from path
      │         └─→ Show loading state
      │         └─→ Handle errors
      │
      └─→ NO: Show placeholder
                │
                ├─→ "Profile Not Available"
                ├─→ Show series & type
                └─→ Gray background
```

### OpeningSchematic Component

```
Input Props:
┌──────────────────────────────────┐
│ type: 'casement' (required)      │
│ width: 200       (optional)      │
│ height: 150      (optional)      │
└────────────┬─────────────────────┘
             │
             ↓
      Check type against supported types
      ├─→ 'fixed' → Render rectangle SVG
      ├─→ 'casement' → Render swing diagram
      ├─→ 'double-hung' → Render vertical sliders
      ├─→ 'sliding' → Render horizontal slider
      ├─→ 'patio-door' → Render large door
      ├─→ 'awning' → Render top-hinged
      │
      └─→ Unknown → Show error placeholder
             │
             ↓
      Render SVG with dimensions
      └─→ Return complete SVG element
```

---

## Registry Lookup Flow

```
useComponentRegistry('86', 'CASEMENT')
        │
        ├─→ useMemo for getFrameSeriesConfig
        │       │
        │       ↓
        │   Check FRAME_SERIES_MAP['86']
        │       │
        │       ├─→ Found: Return config object
        │       │           {
        │       │             name: 'Series 86',
        │       │             headProfile: {...},
        │       │             sillProfile: {...},
        │       │             jambProfile: {...},
        │       │             nailFlange: true,
        │       │             material: 'Aluminum',
        │       │             features: [...]
        │       │           }
        │       │
        │       └─→ Not Found: Return default
        │                       {
        │                         name: 'Series 86',
        │                         headProfile: {
        │                           path: null,
        │                           type: 'svg'
        │                         },
        │                         ...
        │                       }
        │
        ├─→ useMemo for getProductTypeConfig
        │       │
        │       ↓
        │   Check PRODUCT_TYPE_MAP['CASEMENT']
        │       │
        │       ├─→ Found: Return config object
        │       │           {
        │       │             name: 'Casement Window',
        │       │             schematicType: 'casement',
        │       │             openingStyle: 'swing',
        │       │             icon: 'casement-swing-icon',
        │       │             description: '...'
        │       │           }
        │       │
        │       └─→ Not Found: Return default
        │
        ├─→ Extract individual profiles
        │   getHeadProfile('86') → headProfile object
        │   getSillProfile('86') → sillProfile object
        │   getJambProfile('86') → jambProfile object
        │
        └─→ Return merged object with all data
            {
              seriesId: '86',
              productType: 'CASEMENT',
              seriesConfig: {...},
              productConfig: {...},
              headProfile: {...},
              sillProfile: {...},
              jambProfile: {...},
              seriesName: 'Series 86',
              productName: 'Casement Window',
              openingStyle: 'swing',
              schematicType: 'casement'
            }
```

---

## File Import Hierarchy

```
SmartParameterPanel.jsx (or integration point)
├─→ import { getProductTypeConfig } from '../config/ComponentRegistry'
├─→ import { PRODUCT_TYPE_MAP } from '../config/ComponentRegistry'
├─→ import OpeningSchematic from './OpeningSchematic'
└─→ Usage:
    const config = getProductTypeConfig(type)
    <OpeningSchematic type={config.schematicType} />

CanvasDrawingPreview.tsx (or integration point)
├─→ import ProfileDisplay from '../ProfileDisplay'
└─→ Usage:
    <ProfileDisplay seriesId={parameters.series} profileType="HEAD" />

ProfileDisplay.jsx
├─→ import { useComponentRegistry } from '../hooks/useComponentRegistry'
└─→ Usage:
    const { headProfile } = useComponentRegistry(seriesId, null)

useComponentRegistry.js
├─→ import { getFrameSeriesConfig, ... } from '../config/ComponentRegistry'
└─→ Wraps registry calls with useMemo

OpeningSchematic.jsx
└─→ No dependencies (pure React component)

ComponentRegistry.js
└─→ No dependencies (pure JavaScript objects & functions)
```

---

## State Flow Example

```
┌─────────────────────────────────────────────────────────┐
│  Initial Page Load                                      │
│  parameters = {                                         │
│    series: '65',                                        │
│    productType: 'FIXED'                                 │
│  }                                                      │
└──────────────────────────┬────────────────────────────┘
                           │
                    ┌──────┴───────┐
                    ↓              ↓
            ProfileDisplay    OpeningSchematic
            (Series 65)       (FIXED type)
                    │              │
                    ↓              ↓
            65 Head Profile   Rectangle Diagram


┌─────────────────────────────────────────────────────────┐
│  User Changes: Series 65 → 86                           │
│  parameters = {                                         │
│    series: '86',  ← CHANGED                            │
│    productType: 'FIXED'                                 │
│  }                                                      │
└──────────────────────────┬────────────────────────────┘
                           │
                    ┌──────┴───────┐
                    ↓              ↓
            ProfileDisplay    OpeningSchematic
            (Series 86)       (FIXED type)
                    │              │
                    ↓              ↓
            86 Head Profile   Rectangle Diagram
                                  (unchanged)


┌─────────────────────────────────────────────────────────┐
│  User Changes: Product FIXED → CASEMENT                 │
│  parameters = {                                         │
│    series: '86',                                        │
│    productType: 'CASEMENT'  ← CHANGED                  │
│  }                                                      │
└──────────────────────────┬────────────────────────────┘
                           │
                    ┌──────┴───────┐
                    ↓              ↓
            ProfileDisplay    OpeningSchematic
            (Series 86)       (CASEMENT type)
                    │              │
                    ↓              ↓
            86 Head Profile   Swing Arc Diagram
                                  (changed)
```

---

## Asset Resolution Example

### When ProfileDisplay requests HEAD profile for Series 86:

```
ProfileDisplay Props:
  seriesId = '86'
  profileType = 'HEAD'
        │
        ↓
useComponentRegistry('86', null)
        │
        ├─→ Lookup FRAME_SERIES_MAP['86']
        │
        ├─→ Return seriesConfig = {
        │     name: 'Series 86',
        │     headProfile: {
        │       path: '/assets/profiles/series86-head.svg',
        │       type: 'svg',
        │       alt: 'Series 86 Head Profile'
        │     },
        │     ...
        │   }
        │
        ├─→ Extract headProfile from config
        │
        └─→ Return {
             headProfile: {
               path: '/assets/profiles/series86-head.svg',
               type: 'svg',
               alt: 'Series 86 Head Profile'
             },
             ...
           }
        │
        ↓
ProfileDisplay checks: headProfile.path exists?
        │
        ├─→ YES: Render <img src="/assets/profiles/series86-head.svg" />
        │         Image loads from public directory
        │         Shows in browser
        │
        └─→ NO: Show fallback message
```

---

## Memoization Benefits

```
Without Memoization (Re-render 1000 times/sec):
┌────────────────────────────────────────────────┐
│ Each re-render calls:                          │
│ • getFrameSeriesConfig('86')  → Recalculate   │
│ • getProductTypeConfig('CASEMENT')  → Recalc  │
│ • getHeadProfile('86')  → Recalculate         │
│ COST: O(n) × number of renders                │
└────────────────────────────────────────────────┘

With Memoization (with useMemo):
┌────────────────────────────────────────────────┐
│ First render:                                  │
│ • getFrameSeriesConfig('86') → Recalculate    │
│ • getProductTypeConfig('CASEMENT') → Recalc   │
│ • getHeadProfile('86') → Recalculate          │
│                                                │
│ Subsequent renders (if deps unchanged):       │
│ • Return memoized value  → O(1)               │
│ • No recalculation                            │
│                                                │
│ When dependencies change:                     │
│ • Invalidate cache, recalculate once          │
│ • Memoize new result                          │
│                                                │
│ RESULT: Excellent performance ✓               │
└────────────────────────────────────────────────┘
```

---

## Testing Scenarios

```
Scenario 1: First Load
═════════════════════════════════════════════════
→ System loads with default series '65'
→ ComponentRegistry returns Series 65 config
→ ProfileDisplay renders Series 65 profiles
✓ Expected: Series 65 profiles visible

Scenario 2: Series Dropdown Change
═════════════════════════════════════════════════
→ User selects Series 86 from dropdown
→ Parameters update: series = '86'
→ ProfileDisplay re-renders with new seriesId
→ Registry lookup returns Series 86 config
→ Image src changes to series86-*.svg
✓ Expected: Series 86 profiles visible

Scenario 3: Product Type Change
═════════════════════════════════════════════════
→ User selects CASEMENT from product dropdown
→ Parameters update: productType = 'CASEMENT'
→ OpeningSchematic re-renders with new type
→ Schematic diagram changes to swing arc
✓ Expected: Casement swing diagram visible

Scenario 4: Missing Asset
═════════════════════════════════════════════════
→ Profile asset file doesn't exist in /assets/profiles/
→ ProfileDisplay onError handler triggered
→ Fallback UI displays: "Failed to Load"
✓ Expected: Error message with helpful info

Scenario 5: Multiple Series Changes
═════════════════════════════════════════════════
→ User rapidly changes: 65 → 86 → 135 → 86
→ Registry caches calculations
→ Images update each time
→ No performance degradation
✓ Expected: All profiles update correctly
```

This visual architecture makes it clear how the Component Registry system works and integrates with the rest of the application!
