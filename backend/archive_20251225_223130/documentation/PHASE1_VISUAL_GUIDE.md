# PHASE 1: VISUAL OUTPUT STRUCTURE

## Professional Drawing Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RAVEN SHOP DRAWING                              │
│                                                                           │
│ ┌──────────────┬─────────────────────────┬──────────────────────────┐   │
│ │              │                         │                          │   │
│ │  SPEC_1      │                         │      HEADER BLOCK        │   │
│ │  ───────     │                         │                          │   │
│ │              │                         │  RAVEN CUSTOM GLASS      │   │
│ │ Dimensions   │   ELEVATION VIEW        │  Technical Shop Drawings │   │
│ │ ──────────   │   ─────────────         │                          │   │
│ │ Width: 72"   │                         │  Professional Window &    │   │
│ │ Height: 60"  │   [Window Frame]        │  Door Drawings           │   │
│ │ Type: Dbl    │   with CAD dims         │                          │   │
│ │ Qty: 2       │                         ├──────────────────────────┤   │
│ │              │     72"                 │      TITLE BLOCK         │   │
│ │              │     ↔                   │  ──────────────────────  │   │
│ │              │  ┌─────────────────┐    │  WINDOW                  │   │
│ │              │  │                 │    │  Item: W-001             │   │
│ │              │  │   [GLASS]       │    │  ELEVATION               │   │
│ │              │  │                 │    │                          │   │
│ │              │  │                 │    ├──────────────────────────┤   │
│ │              │  │                 │    │   PROJECT INFORMATION    │   │
│ │              │  │                 │    │ ──────────────────────── │   │
│ │              │  │                 │    │ Project: Beach House     │   │
│ │              │  │                 │    │ PO#: DEMO-001            │   │
│ │              │  │                 │    │ Customer: John Doe       │   │
│ │              │  │                 │    │ Date: 12/24/2025         │   │
│ │              │  │                 │    │ Scale: 1/4" = 1'         │   │
│ │              │  │                 │    │                          │   │
│ │              │  │                 │    ├──────────────────────────┤   │
│ │              │  │                 │    │    REVISIONS             │   │
│ │              │  │                 │    │ Rev Date  Description    │   │
│ │              │  │                 │    │  -   -        -          │   │
│ │              │  │                 │    │                          │   │
│ │ ┌────────────┤  │                 │    │                          │   │
│ │ │  SPEC_2    │  │                 │    └──────────────────────────┘   │
│ │ │  ────────  │  │                 │                                    │
│ │ │            │  │                 │                                    │
│ │ │ Materials  │  │                 │                                    │
│ │ │ ─────────  │  │                 │                                    │
│ │ │ Frame: S60 │  │                 │                                    │
│ │ │ Glass: LE  │  └─────────────────┘                                    │
│ │ │ Color: Wh  │  60"                                                    │
│ │ │ Swing: Out │  ↕                                                      │
│ │ │            │                                                         │
│ │ └────────────┘                                                         │
│ │                                                                        │
│ └───────────────┴─────────────────────────┴──────────────────────────┘   │
│                                                                           │
│ LEFT (30%)    │     CENTER (45%)         │      RIGHT (25%)              │
│               │                          │                               │
│ • Spec Table  │  • Elevation Drawing     │  • Company Header             │
│ • Dimensions  │  • CAD Dimensions        │  • Drawing Title              │
│ • Materials   │  • Extension Lines       │  • Project Info               │
│               │  • Dimension Text        │  • Revision Block             │
│               │  • Frame Detail          │                               │
│               │                          │                               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Layout Grid System (8 Zones)

```
╔════════════════════════════════════════════════════════════════════════╗
║                         Page: 11" × 17"                                ║
║                                                                         ║
║  Grid Structure:                                                        ║
║  - Rows: 8 (flexible heights)                                          ║
║  - Cols: 3 (30%, 45%, 25% widths)                                      ║
║                                                                         ║
║  Row 1  ┌─────────────────────────────────────────────────────────┐   ║
║  (h=1)  │ Zone 1: SPEC_1         │ Zone 3: ELEVATION │ Zone 5: HEADER │   ║
║         │ (Dimensions)           │ (Part 1)          │ (Company Info) │   ║
║  Row 2  ├─────────────────────────────────────────────────────────┤   ║
║  (h=1)  │ Zone 2: SPEC_2 (Cont.) │ Zone 3: ELEVATION │ Zone 6: TITLE  │   ║
║         │ (Materials/Finish)     │ (Part 2)          │ (Product Type) │   ║
║  Row 3  │                        │                   │                │   ║
║  (h=2)  ├─────────────────────────────────────────────────────────┤   ║
║         │  (SPEC continues)      │ Zone 3 ELEVATION  │ Zone 7: PROJECT│   ║
║         │                        │ with CAD Dims     │ (continued)    │   ║
║  Row 4  │                        │                   │                │   ║
║  (h=2)  ├─────────────────────────────────────────────────────────┤   ║
║         │                        │ Zone 4: SECTION   │ Zone 7: PROJECT│   ║
║         │                        │ (Detail Cut)      │ INFO           │   ║
║  Row 5  │                        │                   │                │   ║
║  (h=1)  ├─────────────────────────────────────────────────────────┤   ║
║         │  (End SPEC)            │ Zone 4: SECTION   │ Zone 7: PROJECT│   ║
║         │                        │ (continued)       │ (continued)    │   ║
║  Row 6  │                        │                   │                │   ║
║  (h=1)  ├─────────────────────────────────────────────────────────┤   ║
║         │                        │                   │ Zone 8: REVISION│   ║
║  Row 7  │                        │                   │                │   ║
║  (h=1.5)├─────────────────────────────────────────────────────────┤   ║
║         │                        │                   │ (continued)    │   ║
║  Row 8  │                        │                   │                │   ║
║  (h=0.8)└─────────────────────────────────────────────────────────┘   ║
║                                                                         ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## Zone Details

### LEFT COLUMN (30% width)

```
┌─────────────────────┐
│   ZONE 1: SPEC_1    │  ← Dimensions Table
│  ═════════════════  │
│ Width:      72"     │
│ Height:     60"     │
│ Type:      Double   │
│ Qty:        2       │
└─────────────────────┘
        ↓
┌─────────────────────┐
│   ZONE 2: SPEC_2    │  ← Materials Table
│  ═════════════════  │
│ Frame:   Series 60  │
│ Glass:   Low-E      │
│ Color:   White      │
│ Swing:   Out Both   │
└─────────────────────┘
```

### CENTER COLUMN (45% width)

```
┌──────────────────────────────┐
│                              │
│     ZONE 3: ELEVATION        │  ← Main drawing
│   ──────────────────────     │     with full CAD
│                              │     dimensions
│         72"                  │
│         ↔                    │
│     ┌──────────────┐         │
│     │              │         │
│ 60" │   [GLASS]    │  60"    │  ← Vertical dims
│ ↕   │              │  ←      │
│     │              │         │
│     └──────────────┘         │
│         72"                  │
│         ↔                    │
│                              │
└──────────────────────────────┘
        ↓
┌──────────────────────────────┐
│                              │
│    ZONE 4: SECTION DETAIL    │  ← Cross-section
│   ─────────────────────────  │     (Phase 2)
│                              │
│    [Frame Cross-Section]     │
│                              │
│                              │
└──────────────────────────────┘
```

### RIGHT COLUMN (25% width)

```
┌──────────────────────┐
│  ZONE 5: HEADER      │  ← Company branding
│  ════════════════    │
│  RAVEN CUSTOM GLASS  │
│  Technical Drawings  │
└──────────────────────┘
        ↓
┌──────────────────────┐
│  ZONE 6: TITLE       │  ← Product info
│  ════════════════    │
│  WINDOW              │
│  Item: W-001         │
│  ELEVATION           │
└──────────────────────┘
        ↓
┌──────────────────────┐
│  ZONE 7: PROJECT     │  ← Project details
│  ════════════════    │
│  Project: House      │
│  PO#: DEMO-001       │
│  Customer: John Doe  │
│  Date: 12/24/2025    │
│  Scale: 1/4"=1'      │
└──────────────────────┘
        ↓
┌──────────────────────┐
│  ZONE 8: REVISIONS   │  ← Change log
│  ════════════════    │
│  Rev Date Desc.      │
│   -   -     -        │
└──────────────────────┘
```

---

## CAD Dimension Details

### Horizontal Dimension
```
        Extension    Dimension Text
        Lines        (centered with background)
         ↓              ↓
         │              │
         │             72"
         │              │
    ┌────┴──────────────┴────┐
    │                        │
    │    [WINDOW FRAME]      │
    │                        │
    └──→ ← Arrows at ends   │
         │ (pointing in)     │
         ↑                   ↑
      Start              End
```

### Vertical Dimension
```
Extension Lines  Dimension
      ↓          Text (rotated)
      │              │
      │              │
    ──┤──────────    60"
      │        │      ↓
      │        │    (scaled
      │ [FRAME]│     text
      │        │     area)
      │        │      ↑
    ──┤──────────
      │              │
      │              │
      ↑              ↑
     Top           Bottom
```

### Key Features
- ✓ Extension lines extend 1/8" beyond frame edges
- ✓ Dimension lines with arrow endpoints
- ✓ Text centered and readable
- ✓ White background for clarity
- ✓ Professional spacing

---

## Specification Table Format

```
┌─────────────────────────────────────────┐
│           DIMENSIONS                    │  ← Bold header
├─────────────────────────────────────────┤
│ Width:              72"                 │  ← Alternating rows
├─────────────────────────────────────────┤
│ Height:             60"                 │
├─────────────────────────────────────────┤
│ Type:               Double Casement     │
├─────────────────────────────────────────┤
│ Quantity:           2                   │
└─────────────────────────────────────────┘

Color scheme:
- Header: Dark (e.g., #333333) with white text
- Row 1: Light gray background (#f5f5f5)
- Row 2: White background
- Row 3: Light gray background
- etc. (alternating)
```

---

## Text Hierarchy

```
Company Name (Zone 5)
├── Font: Monospace, Bold, 14pt
├── Location: Header block
└── Example: "RAVEN CUSTOM GLASS"

Product Type (Zone 6)
├── Font: Bold, 12pt
├── Location: Title block
└── Example: "WINDOW"

Item Number (Zone 6)
├── Font: Normal, 10pt
├── Location: Title block
└── Example: "Item: W-001"

Dimension Text
├── Font: Bold, 9pt
├── Background: White with rounded corners
├── Location: Above/beside dimension line
└── Example: "72""

Table Headers
├── Font: Bold, 8pt
├── Background: Colored (#333 or similar)
├── Color: White text
└── Location: Top of each specification table

Table Data
├── Font: Normal, 8pt
├── Color: Black on white/light gray background
└── Example: "Series 6000", "Low-E Tempered"
```

---

## Color Scheme

```
Primary Colors:
┌──────────────────────────────┐
│ Dark Gray    (#333333)       │  ← Headers
│ Light Gray   (#f5f5f5)       │  ← Table backgrounds
│ White        (#ffffff)       │  ← Text backgrounds
│ Black        (#000000)       │  ← Lines and text
│ Blue         (#0066cc)       │  ← Frame outlines
└──────────────────────────────┘

Apply to:
- Headers: Dark background with white text
- Specification tables: Alternating gray/white rows
- Borders: Black lines, 1-2pt width
- Text backgrounds: White with rounded corners
```

---

## PDF Output Specifications

```
Page Size:     11" × 17" (landscape letter)
DPI:           300 (high quality print)
Format:        PDF (standard)
Colors:        Black & white with light gray
Fonts:         Standard (Arial, Courier)
File Size:     ~50-100 KB per drawing

Output Naming:
{PO_NUMBER}_{TYPE}-{ITEM}_{VIEW}.pdf

Examples:
DEMO-001_Window-W-001_ELEV.pdf
DEMO-001_Door-D-001_ELEV.pdf
PROJ-2025_Window-W-005_SECTION.pdf
```

---

## Responsive Scaling

The drawing automatically scales based on product size:

```
For small windows (< 24" width):
└─ Scale: 1/4" = 1'   (4:1 ratio)
   Elevation size: fits easily in center zone

For medium windows (24" - 72" width):
└─ Scale: 1/8" = 1'   (8:1 ratio)
   Elevation size: fills most of center zone

For large windows (> 72" width):
└─ Scale: 1/12" = 1'  (12:1 ratio)
   Elevation size: scaled to fit with dimensions visible

Height scaling automatically matches width scaling
to maintain aspect ratio.
```

---

## Next Phase: Enhanced Features

Phase 2 will add:
```
┌─ Zone 4 Enhancement: Cross-section details
│  ├─ Frame profile drawings
│  ├─ Thermal break visualization
│  └─ Glazing assembly details
│
├─ Multi-pane grid support
│  ├─ Muntin drawing
│  ├─ Grid patterns
│  └─ Multiple lite configurations
│
├─ Hardware specifications
│  ├─ Hardware schedule
│  ├─ Installation details
│  └─ Hardware callouts
│
└─ Advanced layout options
   ├─ Multiple views per page
   ├─ Material schedules
   ├─ Installation notes
   └─ Sign-off blocks
```

---

**Professional Drawing Generator - Phase 1**  
**Status: Complete and Production Ready**  
**Date: December 24, 2025**
