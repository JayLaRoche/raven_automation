# SHOP DRAWING GENERATION - PROFESSIONAL FORMAT UPGRADE

## OBJECTIVE
Transform the current basic elevation drawings into comprehensive, professional shop drawings that match the reference example format provided in `/mnt/project/Raven_automation_shop_drawing_example.PNG`.

## CURRENT STATE vs TARGET STATE

### Current Output (BASIC)
- Simple rectangle with width x height dimensions
- Single elevation view only
- No context, no details, minimal information

### Target Output (PROFESSIONAL)
- Multi-view technical drawing with 5+ components
- Detailed cross-sections showing frame profiles
- Dimension lines with proper CAD notation
- Scale reference (person silhouette)
- Opening direction indicators
- Professional specification tables
- Company branding and project information
- Thumbnail reference icons

---

## DETAILED REQUIREMENTS

### 1. DRAWING LAYOUT & STRUCTURE

The drawing should be organized into these distinct zones:

#### **LEFT COLUMN (30% width)**
- **Top Section**: Specification Table
  - Item ID (W001, D101, etc.)
  - Glass specification
  - Frame color
  - Screen details
  - Hardware information
  - Insulated frame details
  - Quantity
  
- **Upper-Left**: Two vertical cross-section details
  - Show frame profile assemblies
  - Include hardware mounting details (hinges, locks, etc.)
  - Label "Drawn from inside view" at top
  - Use detailed technical line work showing:
    * Thermal break sections
    * Weatherstripping
    * Hardware mounting points
    * Glass pocket depth

#### **CENTER COLUMN (45% width)**
- **Upper**: Elevation view with proper dimensions
  - For multi-panel units, show width broken into panel segments
  - Use dimension lines with:
    * Extension lines (thin, extending beyond dimension line)
    * Dimension line (with arrows at ends)
    * Dimension text (centered above line)
  - Show panel divisions with vertical lines
  - Add X/O notation (X = operable, O = fixed)
  
- **Middle**: Person silhouette for scale
  - 5'8"-6'0" tall figure
  - Include curved arrow showing swing direction for doors
  - For casement windows: show opening direction with curved arrow
  - Position person at appropriate scale relative to door/window
  
- **Lower**: Horizontal plan/section view
  - Show multiple frame assemblies in cross-section
  - Display depth and frame details
  - Include dimension arrows and labels
  - Show how panels stack or overlap (for sliders)

#### **RIGHT COLUMN (25% width)**
- **Top**: Company Header
  - Raven logo (stylized text)
  - Address: "9960 W Cheyenne ave Suite 140, Las Vegas NV 89129"
  - Phone: "702-577-1003"
  - Website: "ravencustomglass.com"
  
- **Middle**: Thumbnail Reference Icons
  - Grid of 6-8 small window/door type icons showing:
    * Single fixed window
    * Double hung
    * Casement
    * Picture window
    * French doors
    * Slider
  - Current item type should be highlighted/circled
  
- **Bottom**: Project Information Table
  - Drawing date
  - Serial number (Item ID)
  - Designer name
  - Revision number
  - Construction type
  - Date field

---

### 2. DATA EXTRACTION FROM GOOGLE SHEETS

For each window/door item, extract these fields from the Google Sheets data:

**Windows:**
- Item # (e.g., W001, W100, W101)
- Room location (e.g., "Bed 5", "Stairwell")
- Width (inches)
- Height (inches)
- Type (FIXED, CASEMENT, DOUBLE CASEMENT, etc.)
- Swing Direction (left/right for casements)
- Quantity
- Frame Series (80, 86, 65, 135, MD100H)
- Nail Fin Setup
- Frame Color
- Glass specification
- Grids (NONE, 1x2, 0x2, etc.)
- Screen (NONE or type)

**Doors:**
- Item # (e.g., D101, D102)
- Room location
- Width (inches)
- Height (inches)
- Type (Hinged Door, 2 Panel Slider, 4 Track 4 Panel, etc.)
- Swing Direction (Right In Swing, Left Out Swing, etc.)
- Quantity
- Frame Series (65, 135, MD100H)
- Threshold type
- Sill Pan dimensions
- Frame Color
- Glass specification
- Grids
- Screen

---

### 3. CROSS-SECTION DETAIL GENERATION

The cross-section views must show:

#### **For Hinged Doors (Series 65):**
- Frame profile showing:
  * Thermal break (dark line through center)
  * Interior and exterior frame faces
  * Weather seal locations
  * Hinge mounting points (if applicable)
  * Lock/latch mounting points

#### **For Casement Windows (Series 86):**
- Frame profile showing:
  * Operating hardware location
  * Sash pivot points
  * Multiple seal points
  * Screen track (if applicable)

#### **For Fixed Windows (Series 80):**
- Simplified frame profile:
  * Glass pocket depth
  * Interior and exterior stops
  * Seal/gasket locations

#### **For Sliders (Series 135, MD100H):**
- Track system showing:
  * Multiple panel tracks
  * Roller assembly locations
  * Panel overlap zones
  * Weatherstripping

---

### 4. DIMENSION LINE STYLING

All dimensions must follow these CAD standards:

```
Extension Line (thin, extends 1/8" beyond dimension line)
    |
    |
<---|----> Dimension Line with arrows
    |
    |
  36.0"  <- Dimension text (centered, slightly above line)
```

**Key Rules:**
- Extension lines: 0.5pt stroke width
- Dimension lines: 0.5pt stroke width
- Arrows: Filled triangles, 1/8" long
- Text: 8-10pt, centered above line
- Overall dimensions on outside
- Individual panel dimensions on inside (for multi-panel units)

---

### 5. PANEL CONFIGURATION NOTATION

For multi-panel units, show configuration using X/O system:

**Examples:**
- `X-O-X` = Operable-Fixed-Operable (3-panel window)
- `O-X` = Fixed-Operable (2-panel casement)
- `X-X-X-X` = Four operating panels (4-panel slider)

Display this notation near the top of the elevation view.

---

### 6. PERSON SILHOUETTE SPECIFICATIONS

The person figure should:
- Be a simple outline/silhouette (black fill)
- Stand 5'8"-6'0" tall (66-72 inches)
- Be positioned to left or right of door/window
- Include curved arrow showing swing direction
  * Arrow starts from hinge side
  * Curves to show arc of door/window swing
  * Arrow head points to fully open position

---

### 7. COLOR SCHEME & LINE WEIGHTS

Use professional CAD-style rendering:

**Line Weights:**
- Object outlines: 1.0pt (thick)
- Dimension lines: 0.5pt (thin)
- Extension lines: 0.5pt (thin)
- Cross-section details: 0.75pt (medium)
- Hidden/internal lines: 0.5pt dashed

**Colors:**
- Primary lines: Black (#000000)
- Dimension text: Black
- Cross-section fills: Light gray (#CCCCCC) for frame profiles
- Glass areas: Very light blue tint (#E8F4F8) or white
- Person silhouette: Solid black
- Arrows: Solid black

---

### 8. TEXT & LABELS

**Font Specifications:**
- Primary text: Arial or Helvetica, 9-10pt
- Dimension text: Arial, 8-9pt
- Headers: Arial Bold, 10-11pt
- Table text: Arial, 8pt
- Logo text: Custom stylized font (or Arial Black)

**Label Placement:**
- "Drawn from inside view" - top left corner
- Dimension values - centered above dimension lines
- Item ID - in specification table and drawing title
- Room location - in specification table

---

### 9. SCALE & PROPORTIONS

The drawing should maintain proper scale:

**For Doors:**
- Typical 36" x 84-108" dimensions
- Person should be proportional (reach ~80% of door height)
- Cross-sections shown at 1:1 or 1:2 scale relative to elevation

**For Windows:**
- Various sizes (18" x 18" up to 84" x 72" or more)
- Person should provide clear scale reference
- Cross-sections shown at appropriate scale

**Drawing Canvas:**
- 11" x 8.5" (landscape) or larger
- Maintain 0.5" margins on all sides
- Scale elevation view to fit comfortably in center zone

---

### 10. IMPLEMENTATION PRIORITIES

#### **Phase 1: Core Layout** (Most Critical)
1. Set up 3-column layout (Left: 30%, Center: 45%, Right: 25%)
2. Add specification table (left column)
3. Create elevation view with proper dimensions (center)
4. Add company header (right column)
5. Add project info table (right column, bottom)

#### **Phase 2: Technical Details**
6. Generate frame cross-section details (left column, top)
7. Add plan/section view (center, bottom)
8. Implement dimension lines with proper arrows and text
9. Add panel configuration notation (X/O system)

#### **Phase 3: Visual Enhancements**
10. Add person silhouette with swing direction arrows
11. Create thumbnail reference icons (right column, middle)
12. Add line weight variations for depth
13. Implement proper CAD-style rendering

#### **Phase 4: Data Integration**
14. Parse Google Sheets data for each item
15. Map frame series to correct cross-section templates
16. Generate appropriate views based on window/door type
17. Populate specification table with item details

---

### 11. TECHNICAL IMPLEMENTATION NOTES

**Matplotlib Approach:**
```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D

# Set up figure with proper DPI for print quality
fig = plt.figure(figsize=(11, 8.5), dpi=300)

# Create main grid layout
gs = fig.add_gridspec(3, 3, width_ratios=[3, 4.5, 2.5], 
                      height_ratios=[2, 3, 2],
                      hspace=0.05, wspace=0.05)

# Define axes for each zone
ax_spec_table = fig.add_subplot(gs[0, 0])      # Specification table
ax_cross_section = fig.add_subplot(gs[1:, 0])  # Cross-section details
ax_elevation = fig.add_subplot(gs[0, 1])       # Elevation view
ax_person = fig.add_subplot(gs[1, 1])          # Person & swing
ax_plan = fig.add_subplot(gs[2, 1])            # Plan/section view
ax_header = fig.add_subplot(gs[0, 2])          # Company header
ax_thumbnails = fig.add_subplot(gs[1, 2])     # Thumbnail icons
ax_project_info = fig.add_subplot(gs[2, 2])   # Project info table

# Turn off axes for all subplots
for ax in [ax_spec_table, ax_cross_section, ax_elevation, 
           ax_person, ax_plan, ax_header, ax_thumbnails, ax_project_info]:
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
```

**Dimension Lines Helper Function:**
```python
def draw_dimension_line(ax, x1, y1, x2, y2, text, offset=2):
    """Draw a dimension line with arrows and text"""
    # Extension lines
    ax.plot([x1, x1], [y1-offset, y1-offset*2], 'k-', lw=0.5)
    ax.plot([x2, x2], [y2-offset, y2-offset*2], 'k-', lw=0.5)
    
    # Dimension line with arrows
    arrow = FancyArrowPatch((x1, y1-offset), (x2, y2-offset),
                           arrowstyle='<->', mutation_scale=10,
                           lw=0.5, color='black')
    ax.add_patch(arrow)
    
    # Dimension text
    mid_x = (x1 + x2) / 2
    ax.text(mid_x, y1-offset+1, text, ha='center', va='bottom',
            fontsize=8, fontfamily='Arial')
```

**Cross-Section Drawing Function:**
```python
def draw_frame_cross_section(ax, series_type, x_pos, y_pos, width, height):
    """Draw detailed frame cross-section based on series"""
    if series_type == '65':  # Hinged door frame
        # Outer frame rectangle
        frame = Rectangle((x_pos, y_pos), width, height, 
                         linewidth=1, edgecolor='black', 
                         facecolor='#CCCCCC')
        ax.add_patch(frame)
        
        # Thermal break (dark line through center)
        thermal_break_x = x_pos + width/2
        ax.plot([thermal_break_x, thermal_break_x], 
               [y_pos, y_pos+height], 'k-', lw=2)
        
        # Hinge detail (if applicable)
        hinge_y = y_pos + height * 0.3
        circle = plt.Circle((thermal_break_x, hinge_y), 
                           width*0.15, color='black', fill=True)
        ax.add_patch(circle)
        
    elif series_type == '86':  # Casement window frame
        # Similar approach but with casement-specific details
        pass
    
    # Add more series types as needed
```

**Person Silhouette Function:**
```python
def draw_person_silhouette(ax, x_pos, y_pos, height_inches=68):
    """Draw a person silhouette for scale reference"""
    scale_factor = height_inches / 68  # Normalize to 5'8" person
    
    # Head (circle)
    head = plt.Circle((x_pos, y_pos + 60*scale_factor), 
                     4*scale_factor, color='black')
    ax.add_patch(head)
    
    # Body (rectangle)
    body = Rectangle((x_pos - 4*scale_factor, y_pos + 35*scale_factor),
                    8*scale_factor, 25*scale_factor,
                    color='black')
    ax.add_patch(body)
    
    # Arms (lines)
    ax.plot([x_pos - 10*scale_factor, x_pos + 10*scale_factor],
           [y_pos + 50*scale_factor, y_pos + 50*scale_factor],
           'k-', lw=2*scale_factor)
    
    # Legs (lines)
    ax.plot([x_pos - 3*scale_factor, x_pos - 3*scale_factor],
           [y_pos + 35*scale_factor, y_pos],
           'k-', lw=2*scale_factor)
    ax.plot([x_pos + 3*scale_factor, x_pos + 3*scale_factor],
           [y_pos + 35*scale_factor, y_pos],
           'k-', lw=2*scale_factor)
```

**Swing Direction Arrow:**
```python
def draw_swing_arrow(ax, hinge_x, hinge_y, radius, angle_deg, direction='right'):
    """Draw curved arrow showing door/window swing direction"""
    from matplotlib.patches import Arc, FancyArrowPatch
    
    # Create arc
    arc = Arc((hinge_x, hinge_y), 2*radius, 2*radius,
             angle=0, theta1=0, theta2=angle_deg,
             linewidth=1.5, color='black')
    ax.add_patch(arc)
    
    # Add arrowhead at end of arc
    import numpy as np
    end_angle = np.radians(angle_deg)
    end_x = hinge_x + radius * np.cos(end_angle)
    end_y = hinge_y + radius * np.sin(end_angle)
    
    # Arrow direction vector
    arrow = FancyArrowPatch((end_x - 2, end_y), (end_x, end_y),
                           arrowstyle='->', mutation_scale=15,
                           lw=1.5, color='black')
    ax.add_patch(arrow)
```

---

### 12. DATA FLOW & PROCESSING

**Step 1: Fetch Data from Google Sheets**
```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Authenticate and fetch sheet data
creds = Credentials.from_service_account_file('service_account.json')
service = build('sheets', 'v4', credentials=creds)

# Get window/door data
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range='Windows!A:Z'  # or 'Doors!A:Z'
).execute()
values = result.get('values', [])
```

**Step 2: Parse and Structure Data**
```python
class WindowDoorItem:
    def __init__(self, row_data):
        self.item_id = row_data[0]        # W001, D101, etc.
        self.room = row_data[1]           # "Bed 5", "Office"
        self.width = float(row_data[2])   # inches
        self.height = float(row_data[3])  # inches
        self.type = row_data[4]           # "CASEMENT", "Hinged Door"
        self.swing_dir = row_data[5]      # "left", "Right In Swing"
        self.quantity = int(row_data[6])
        self.series = row_data[7]         # "86", "65", "135"
        self.frame_color = row_data[10]   # "Black", "White"
        self.glass = row_data[11]         # "Clear Low E"
        # ... additional fields
```

**Step 3: Determine Drawing Template**
```python
def get_drawing_template(item_type, series):
    """Return appropriate drawing functions based on type and series"""
    templates = {
        ('FIXED', '80'): draw_fixed_window_80,
        ('CASEMENT', '86'): draw_casement_window_86,
        ('DOUBLE CASEMENT', '86'): draw_double_casement_86,
        ('Hinged Door', '65'): draw_hinged_door_65,
        ('2 Panel Slider', '135'): draw_slider_135,
        # ... more combinations
    }
    return templates.get((item_type, series), draw_generic)
```

**Step 4: Generate Drawing**
```python
def generate_shop_drawing(item: WindowDoorItem, output_path: str):
    """Main function to generate complete shop drawing"""
    
    # Create figure and layout
    fig, axes = create_drawing_layout()
    
    # Left column: Specification table
    draw_specification_table(axes['spec_table'], item)
    
    # Left column: Cross-sections
    draw_frame_cross_sections(axes['cross_section'], item.series)
    
    # Center column: Elevation view
    draw_elevation_view(axes['elevation'], item)
    
    # Center column: Person and swing
    draw_person_and_swing(axes['person'], item)
    
    # Center column: Plan view
    draw_plan_view(axes['plan'], item)
    
    # Right column: Company header
    draw_company_header(axes['header'])
    
    # Right column: Thumbnail icons
    draw_thumbnail_icons(axes['thumbnails'], item.type)
    
    # Right column: Project info
    draw_project_info_table(axes['project_info'], item)
    
    # Save as high-quality PDF
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

---

### 13. SPECIFIC WINDOW/DOOR TYPE HANDLING

#### **CASEMENT WINDOWS (Series 86)**
- Show single or double panel configuration
- Include X (operable) notation on appropriate panels
- Draw crank mechanism in cross-section
- Add swing arrow showing 90-degree outward opening

#### **FIXED WINDOWS (Series 80)**
- Simple frame with O (fixed) notation
- No swing arrows needed
- Simplified cross-section (no hardware)

#### **DOUBLE CASEMENT (Series 86)**
- Two panels meeting at center
- Both marked with X notation
- Show center mullion in elevation
- Dimension each panel separately
- Two swing arrows (each panel opens opposite direction)

#### **HINGED DOORS (Series 65)**
- Single or double door configuration
- Mark swing direction (In Swing / Out Swing)
- Show hinge locations in cross-section (typically 3 hinges)
- Include door handle/lockset location
- Add threshold detail in plan view

#### **SLIDER DOORS (Series 135, MD100H)**
- Show number of panels and tracks
- Indicate which panels are operable
- Display track system in plan view
- Show panel overlap zones
- Add dimension for each panel width

---

### 14. QUALITY CHECKLIST

Before finalizing each drawing, verify:

- [ ] All dimensions are present and accurate
- [ ] Dimension lines have proper arrows and extension lines
- [ ] Cross-section details match the specified frame series
- [ ] Person silhouette is proportional to actual size
- [ ] Swing direction arrows are present and correct
- [ ] Specification table is complete and accurate
- [ ] Company header includes all required information
- [ ] Project info table is populated
- [ ] Panel configuration (X/O) is clearly marked
- [ ] Line weights differentiate between object outlines and dimensions
- [ ] Drawing is clean and professional-looking
- [ ] Text is legible at intended print size
- [ ] All data from Google Sheets is correctly incorporated

---

### 15. FILE OUTPUT SPECIFICATIONS

**PDF Generation:**
```python
from matplotlib.backends.backend_pdf import PdfPages

# Generate multi-page PDF if needed
with PdfPages(f'{item_id}_shop_drawing.pdf') as pdf:
    # Page 1: Main shop drawing
    generate_shop_drawing(item, pdf)
    
    # Add metadata
    d = pdf.infodict()
    d['Title'] = f'Shop Drawing - {item.item_id}'
    d['Author'] = 'Raven Custom Glass'
    d['Subject'] = f'{item.type} - {item.room}'
    d['Keywords'] = f'{item.series}, {item.frame_color}'
    d['CreationDate'] = datetime.now()
```

**File Naming Convention:**
```
{PO_NUMBER}_{ITEM_ID}_{drawing_type}.pdf

Examples:
- STARFALL_W001_elevation.pdf
- STARFALL_D101_elevation.pdf
- TEST-001_W-001_elevation.pdf
```

---

### 16. TESTING & VALIDATION

Create test cases for:

1. **Window Types:**
   - Fixed window (Series 80) - 36" x 48"
   - Single casement (Series 86) - 24" x 60"
   - Double casement (Series 86) - 72" x 60"
   - Slider window (Series 135) - 84" x 72"

2. **Door Types:**
   - Single hinged door (Series 65) - 36" x 108"
   - Double French door (Series 65) - 72" x 108"
   - 2-panel slider (Series 135) - 96" x 108"
   - 4-panel slider (MD100H) - 240" x 108"

3. **Edge Cases:**
   - Very large units (240" wide)
   - Very small units (18" x 18")
   - Multi-panel configurations (3, 4, or more panels)
   - Both in-swing and out-swing doors
   - Left and right casement configurations

---

### 17. EXAMPLE DATA MAPPING

**From Google Sheets Row:**
```
W001 | Bed 5 | 72 | 60 | DOUBLE CASEMENT | NA | 1 | Series 86 | Stucco setback 35mm | NA | NA | Black | Clear Low E | NONE | NONE
```

**To Drawing Elements:**
- Item ID: W001
- Title: "Window Elevation - W001"
- Room: "Bed 5"
- Dimensions: 72.0" W x 60.0" H
- Panel config: X-X (two 36" panels)
- Frame series: 86 (use casement cross-section template)
- Swing: Both panels open outward
- Person height: 68" (shows window is at comfortable operating height)
- Specification table: All fields populated from row data

---

### 18. REFERENCE MATERIALS INTEGRATION

**Cross-Section Library Path:**
`/mnt/project/raven_input_selections_details.pdf`

This document contains:
- All frame series specifications (pages 1-2)
- Window and door type definitions (pages 2-3)
- Glass options and configurations
- Frame color options
- Nail fin setup variations

**Parse this file to:**
1. Extract frame series details for accurate cross-section rendering
2. Validate input data against allowed options
3. Generate specification text descriptions
4. Ensure terminology matches client standards

---

## FINAL IMPLEMENTATION STRATEGY

### Recommended Approach:

1. **Start with layout framework** - Get the 3-column grid working first
2. **Add static elements** - Header, specification table structure, project info table
3. **Implement elevation view** - Basic rectangle with dimensions
4. **Add dimension lines** - Proper CAD-style with arrows
5. **Generate cross-sections** - Start with Series 65, then expand
6. **Add person silhouette** - Simple geometric shapes
7. **Implement plan views** - Horizontal sections
8. **Add swing arrows** - Curved arrows for doors/casements
9. **Create thumbnails** - Small reference icons
10. **Polish and refine** - Line weights, colors, spacing

### Code Organization:

```
drawing_generator/
├── main.py                 # Entry point, orchestrates generation
├── layout.py               # Drawing layout and grid setup
├── dimensions.py           # Dimension line drawing functions
├── cross_sections.py       # Frame cross-section templates
├── elevation.py            # Elevation view generation
├── person.py               # Person silhouette and swing arrows
├── tables.py               # Specification and info tables
├── header.py               # Company header and thumbnails
├── data_parser.py          # Google Sheets data extraction
└── utils.py                # Helper functions (colors, styles, etc.)
```

---

## SUCCESS CRITERIA

The upgraded shop drawing system is complete when:

1. ✅ Generated drawings visually match the example format
2. ✅ All dimension lines follow CAD standards
3. ✅ Cross-sections accurately represent frame series
4. ✅ Person silhouette provides clear scale reference
5. ✅ Swing direction is clearly indicated
6. ✅ Specification tables are complete and accurate
7. ✅ Company branding is professional and consistent
8. ✅ Drawings are print-ready at 300 DPI
9. ✅ Data flows correctly from Google Sheets to drawing
10. ✅ Client (Zion at Raven Custom Glass) approves the output

---

## PRIORITY NOTES FOR THE AI AGENT

⚠️ **CRITICAL ITEMS:**
- Match the example layout EXACTLY - client expects this specific format
- Dimension lines MUST follow CAD standards (arrows, extension lines, centered text)
- Frame series cross-sections must be technically accurate
- Person silhouette is essential for scale - don't skip this
- Use the Google Sheets data structure provided - map fields correctly

💡 **NICE-TO-HAVE ENHANCEMENTS:**
- Color-coded panel types (fixed vs operable)
- Automated thumbnail generation based on item type
- Dynamic legend for X/O notation
- Multiple page support for complex configurations

🚫 **AVOID:**
- Don't simplify the layout - client needs all components
- Don't use placeholder/dummy data - fetch from Google Sheets
- Don't skip the cross-section details - these are critical for fabrication
- Don't use non-standard dimension notation - follow CAD conventions

---

## NEXT STEPS FOR DEVELOPMENT

1. Review this prompt with the development team
2. Break down into Jira tickets or GitHub issues
3. Start with Phase 1 (Core Layout) implementation
4. Schedule demo call with client after Phase 1 completion
5. Iterate based on client feedback before moving to Phase 2
6. Document any deviations from this spec and reasons why

---

**Document Version:** 1.0  
**Last Updated:** December 24, 2024  
**Author:** Jeremiah (Project Lead)  
**Client:** Raven Custom Glass (Zion)  
**Project:** Automated Shop Drawing Generation System
