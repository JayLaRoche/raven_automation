# SHOP DRAWING LAYOUT - VISUAL REFERENCE GUIDE

## DRAWING CANVAS DIMENSIONS
- Paper Size: 11" x 8.5" (Landscape orientation)
- DPI: 300 (for print quality)
- Margins: 0.5" on all sides
- Working Area: 10" x 7.5"

---

## LAYOUT GRID (3 COLUMNS × 3 ROWS)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RAVEN CUSTOM GLASS                              │
│                      Professional Shop Drawing                          │
├──────────────────┬────────────────────────┬─────────────────────────────┤
│                  │                        │                             │
│  SPECIFICATION   │   ELEVATION VIEW       │    COMPANY HEADER           │
│     TABLE        │    (Front View)        │    ┌──────────────┐         │
│                  │                        │    │  ╔═══════╗   │         │
│  ┌────────────┐  │   ┌────────────────┐   │    │  ║ raven ║   │         │
│  │ Item: W001 │  │   │                │   │    │  ╚═══════╝   │         │
│  │ Glass: XXX │  │   │  72.0" x 60.0" │   │    │  Logo        │         │
│  │ Color: XXX │  │   │                │   │    └──────────────┘         │
│  │ Series: 86 │  │   │     [X] [X]    │   │                             │
│  └────────────┘  │   │                │   │  Address & Contact:         │
│                  │   └────────────────┘   │  9960 W Cheyenne Ave        │
│                  │   <----dimension--->   │  Suite 140                  │
│                  │        lines           │  Las Vegas, NV 89129        │
├──────────────────┤                        │  Phone: 702-577-1003        │
│                  ├────────────────────────┤─────────────────────────────┤
│  CROSS-SECTION   │                        │                             │
│    DETAILS       │    PERSON SCALE        │    THUMBNAIL ICONS          │
│   (Frame         │    & SWING ARROW       │                             │
│    Profile)      │                        │  ┌───┬───┬───┐              │
│                  │       ▄▄▄              │  │   │   │   │              │
│  ╔═══════════╗   │      ▐███▌   ↺         │  │ █ │▐█▌│   │              │
│  ║  ▒▒▒║▒▒▒  ║   │      ▐███▌             │  └───┴───┴───┘              │
│  ║█████║█████║   │       ████              │  ┌───┬───┬───┐              │
│  ║  ▒▒▒║▒▒▒  ║   │       ▐█▌               │  │▐█▌│ = │███│              │
│  ║     ║     ║   │        ▌▌               │  │▐█▌│ = │███│              │
│  ╚═══════════╝   │        ▌▌               │  └───┴───┴───┘              │
│                  │       ▐ ▌               │                             │
│  (Top view)      │      ▐   ▌              │  Window/Door Types          │
│                  │                         │                             │
├──────────────────┼─────────────────────────┼─────────────────────────────┤
│                  │                         │                             │
│  CROSS-SECTION   │   PLAN VIEW             │   PROJECT INFO              │
│  (Lower Detail)  │   (Horizontal Section)  │   ┌──────────────────┐      │
│                  │                         │   │ Drawing Date:    │      │
│  ╔═══════════╗   │   ┌─────┐ ┌─────┐       │   │ 2025-10-25       │      │
│  ║  ▒▒▒║▒▒▒  ║   │   ├─────┤ ├─────┤       │   ├──────────────────┤      │
│  ║█████║█████║   │   └─────┘ └─────┘       │   │ Serial Number:   │      │
│  ║  ▒▒▒║▒▒▒  ║   │   <---dimensions--->    │   │ P001             │      │
│  ╚═══════════╝   │                         │   ├──────────────────┤      │
│                  │   (Shows frame depth    │   │ Designer:        │      │
│  "Drawn from     │    and panel tracks)    │   │ Construction     │      │
│   inside view"   │                         │   ├──────────────────┤      │
│                  │                         │   │ Revision: 1      │      │
└──────────────────┴─────────────────────────┴───┴──────────────────┘      │
                                                  Date: 2025-10-25         │
                                                  └──────────────────┘      │
```

---

## DETAILED ZONE SPECIFICATIONS

### LEFT COLUMN (30% width)

**Zone 1A - Specification Table (Top)**
```
┌────────────────────┐
│ Item#    : W001    │  ← Item ID from Google Sheets
├────────────────────┤
│ Glass    : Series  │  ← Frame series specification
│            86 Low  │
│            E Clear │
├────────────────────┤
│ Frame    : Black   │  ← Frame color
│ Color              │
├────────────────────┤
│ Screen   : None    │  ← Screen specification
│ Size               │
├────────────────────┤
│ Hardware : Std     │  ← Hardware type
├────────────────────┤
│ Insulated: Yes     │  ← Insulated frame (Y/N)
│ Frame              │
├────────────────────┤
│ Quantity : 1       │  ← Quantity from sheet
└────────────────────┘
```

**Zone 1B - Cross Section Details (Middle & Bottom)**
```
"Drawn from inside view"  ← Label at top

╔══════════════╗
║ ▒▒▒  ║  ▒▒▒  ║  ← Frame profile (exterior)
║█████ ║ █████ ║  ← Thermal break (dark)
║ ▒▒▒  ║  ▒▒▒  ║  ← Frame profile (interior)
║   ●  ║       ║  ← Hardware (hinge/lock)
╚══════════════╝

(Vertical cross-section showing full frame detail)

╔══════════════╗
║ ▒▒▒  ║  ▒▒▒  ║  ← Top view cross-section
║█████ ║ █████ ║
║ ▒▒▒  ║  ▒▒▒  ║
╚══════════════╝

(Horizontal cross-section showing frame depth)
```

---

### CENTER COLUMN (45% width)

**Zone 2A - Elevation View (Top)**
```
         <------------ 72.0" ------------>
         |                                |
    ┌────┴────────────────────────────┴────┐  ↑
    │                                      │  │
    │    ┌───────────┐  ┌───────────┐     │  │
    │    │           │  │           │     │  │ 60.0"
    │    │     X     │  │     X     │     │  │
    │    │           │  │           │     │  │
    │    └───────────┘  └───────────┘     │  │
    │                                      │  ↓
    └──────────────────────────────────────┘
         <---- 36.0" --->  <---- 36.0" --->
            Panel 1            Panel 2

    X = Operable panel (casement)
    O = Fixed panel
```

**Zone 2B - Person & Swing Arrow (Middle)**
```
                     ╭─────────────╮
                    ╱               ╲  ← Swing arc
                   ╱                 ╲    (90° curved arrow)
                  ╱                   ╲
                 ▼                     
        
         ▄▄▄         ← Head
        ▐███▌        ← Body
        ▐███▌
         ████
         ▐█▌         ← Legs
          ▌▌
          ▌▌
         ▐ ▌

    (Person silhouette: 5'8" - 6'0" tall)
    (Positioned to show scale relative to window/door)
```

**Zone 2C - Plan View (Bottom)**
```
    (Looking down from above - shows frame depth)

    ┌─────┐     ┌─────┐
    ├─────┤  ◄  ├─────┤  ← Panel overlap
    └─────┘     └─────┘
    
    ◄───►       ◄───►
    Frame       Frame
    depth       depth
    
    (Shows how panels sit in tracks for sliders,
     or shows frame depth for hinged units)
```

---

### RIGHT COLUMN (25% width)

**Zone 3A - Company Header (Top)**
```
┌─────────────────────────┐
│                         │
│      ╔═══════════╗      │
│      ║  r a v e n ║      │
│      ╚═══════════╝      │
│                         │
│  9960 W Cheyenne Ave    │
│  Suite 140              │
│  Las Vegas, NV 89129    │
│                         │
│  Cell: 702-577-1003     │
│                         │
│  Website:               │
│  ravencustomglass.com   │
│                         │
└─────────────────────────┘
```

**Zone 3B - Thumbnail Icons (Middle)**
```
┌───┬───┬───┐
│   │   │   │  ← Fixed window
│ █ │▐█▌│   │  ← Casement, Double Hung
└───┴───┴───┘
┌───┬───┬───┐
│▐█▌│ = │███│  ← Slider, French Door, 
│▐█▌│ = │███│     Multi-panel Slider
└───┴───┴───┘

(Highlight current item type)
```

**Zone 3C - Project Information (Bottom)**
```
┌────────────────────┐
│ Drawing Date:      │
│ 2025-10-25         │
├────────────────────┤
│ Serial Number:     │
│ P001               │
├────────────────────┤
│ Designer:          │
│ [Name]             │
├────────────────────┤
│ Revision: 1        │
├────────────────────┤
│ Construction:      │
│ [Type]             │
├────────────────────┤
│ Date:              │
│ 2025-10-25         │
└────────────────────┘
```

---

## DIMENSION LINE DETAIL

Standard CAD dimension notation:

```
    Extension Line (thin, extends 1/8" past dimension line)
        ↓
        |
        |
    <───┼───>  Dimension Line (with filled arrow heads)
        |
        |
      36.0"    ← Dimension text (centered, 1/8" above line)
```

**Key Measurements:**
- Extension line stroke: 0.5pt
- Dimension line stroke: 0.5pt
- Arrow head: Filled triangle, 1/8" long
- Text size: 8-10pt
- Gap between dimension line and text: 1/8"

---

## SWING ARROW DETAIL

For doors and casement windows:

```
        Hinge Point
            |
            |
            ●  ← Pivot point
           ╱ ╲
          ╱   ╲ 
         ╱     ╲  ← Curved arc showing swing path
        ╱       ╲
       ╱         ▼  ← Arrow head showing open position
      ╱
     ╱
    
    (Arc typically 60-90 degrees)
    (Arrow shows final position when fully open)
```

---

## CROSS-SECTION SYMBOLS

**Frame Profile Elements:**
```
╔════════════╗
║ ▒▒▒ ║ ▒▒▒  ║  ← Light gray fill (frame aluminum)
║█████║█████ ║  ← Dark fill (thermal break)
║ ▒▒▒ ║ ▒▒▒  ║  ← Light gray fill (frame aluminum)
║  ●  ║      ║  ← Solid circle (hardware mounting)
║  ─  ║  ─   ║  ← Horizontal line (weatherstripping)
╚════════════╝

Legend:
▒▒▒ = Aluminum frame sections
███ = Thermal break material
● = Hardware (hinges, locks)
─ = Weatherstripping/seals
```

---

## PERSON SILHOUETTE PROPORTIONS

Based on average 5'8" (68 inches) person:

```
     Head: 8-9" diameter circle
     ─●─  Shoulders: 18" wide
      │   Torso: 22-24" tall
     ─┴─  Waist: 14-16" wide
      │   Legs: 30-32" tall
     ─┴─  Stance: 12" apart
```

Scale this proportionally for different reference heights.

---

## COLOR PALETTE

**Line Colors:**
- Primary lines: #000000 (Black)
- Dimension text: #000000 (Black)
- Dimension lines: #000000 (Black)
- Extension lines: #000000 (Black)

**Fill Colors:**
- Frame profiles: #CCCCCC (Light gray)
- Thermal break: #666666 (Dark gray)
- Glass areas: #E8F4F8 (Very light blue) or #FFFFFF (White)
- Person silhouette: #000000 (Solid black)
- Background: #FFFFFF (White)

**Line Weights:**
- Object outlines: 1.0pt (thick)
- Cross-section details: 0.75pt (medium)
- Dimension lines: 0.5pt (thin)
- Extension lines: 0.5pt (thin)
- Hidden/dashed lines: 0.5pt dashed

---

## GRID SYSTEM COORDINATES

Using matplotlib with normalized coordinates (0-100 scale):

**Left Column:**
- X: 0-30
- Specification Table Y: 65-100
- Cross-sections Y: 0-65

**Center Column:**
- X: 32-77
- Elevation View Y: 70-100
- Person/Swing Y: 35-70
- Plan View Y: 0-35

**Right Column:**
- X: 79-100
- Company Header Y: 75-100
- Thumbnails Y: 40-75
- Project Info Y: 0-40

---

## TYPOGRAPHY GUIDE

**Font Family:** Arial (or Helvetica as fallback)

**Font Sizes:**
- Company Logo: 16-18pt, Bold
- Section Headers: 10-11pt, Bold
- Dimension Text: 8-9pt, Regular
- Table Text: 8pt, Regular
- Labels: 7-8pt, Regular

**Text Alignment:**
- Dimension text: Center-aligned
- Table labels: Left-aligned
- Header text: Center-aligned
- Project info: Left-aligned

---

## TESTING CHECKLIST

Use this to verify each generated drawing:

**Layout & Structure:**
- [ ] All three columns present and properly sized
- [ ] Specification table complete
- [ ] Cross-section details visible
- [ ] Elevation view properly scaled
- [ ] Person silhouette present
- [ ] Plan view shows appropriate detail
- [ ] Company header formatted correctly
- [ ] Thumbnail icons displayed
- [ ] Project info table complete

**Dimensions:**
- [ ] Overall dimensions shown
- [ ] Panel dimensions shown (if multi-panel)
- [ ] Extension lines extend properly
- [ ] Dimension lines have arrows
- [ ] Text centered above dimension lines
- [ ] All measurements accurate to Google Sheets data

**Technical Details:**
- [ ] Cross-sections match specified frame series
- [ ] Hardware shown in appropriate locations
- [ ] Thermal breaks visible in cross-sections
- [ ] Panel configuration (X/O) clearly marked
- [ ] Swing direction indicated (if applicable)

**Data Accuracy:**
- [ ] Item ID matches Google Sheets
- [ ] Room location correct
- [ ] Width and height accurate
- [ ] Frame series correct
- [ ] Glass specification matches
- [ ] Frame color correct
- [ ] All table fields populated

**Visual Quality:**
- [ ] Line weights differentiated
- [ ] Text legible at print size (300 DPI)
- [ ] Colors consistent with palette
- [ ] No overlapping text or lines
- [ ] Professional appearance overall

---

## QUICK START TEMPLATE

Minimal working example to get started:

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Create figure
fig = plt.figure(figsize=(11, 8.5), dpi=300)
gs = GridSpec(3, 3, figure=fig, 
              width_ratios=[3, 4.5, 2.5],
              height_ratios=[2, 3, 2],
              hspace=0.05, wspace=0.05)

# Create axes for each zone
ax1 = fig.add_subplot(gs[0, 0])  # Spec table
ax2 = fig.add_subplot(gs[1:, 0]) # Cross-sections
ax3 = fig.add_subplot(gs[0, 1])  # Elevation
ax4 = fig.add_subplot(gs[1, 1])  # Person
ax5 = fig.add_subplot(gs[2, 1])  # Plan
ax6 = fig.add_subplot(gs[0, 2])  # Header
ax7 = fig.add_subplot(gs[1, 2])  # Thumbnails
ax8 = fig.add_subplot(gs[2, 2])  # Project info

# Turn off axes for all
for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

# Add content to each zone
ax1.text(50, 50, 'Specification Table', ha='center')
ax2.text(50, 50, 'Cross Sections', ha='center')
ax3.text(50, 50, 'Elevation View', ha='center')
ax4.text(50, 50, 'Person & Swing', ha='center')
ax5.text(50, 50, 'Plan View', ha='center')
ax6.text(50, 50, 'Company Header', ha='center')
ax7.text(50, 50, 'Thumbnails', ha='center')
ax8.text(50, 50, 'Project Info', ha='center')

plt.savefig('test_layout.pdf', dpi=300, bbox_inches='tight')
plt.close()
```

Start with this template and progressively add detail to each zone.

---

**Document Version:** 1.0  
**Companion to:** shop_drawing_improvement_prompt.md  
**Purpose:** Visual reference guide for implementation  
**Last Updated:** December 24, 2024
