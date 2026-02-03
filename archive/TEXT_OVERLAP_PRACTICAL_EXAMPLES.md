# Text Overlap Fixes - Practical Examples

## Example 1: Basic Dimension Line with Collision Detection

### Before (Overlap Issues):
```python
# Simple dimension drawing - text overlaps with line
dim_drawer = DimensionLine(ax, scale=1.5)
dim_drawer.draw_horizontal(
    x1=10, x2=50,
    y=20,
    dimension='40"',
    above=True
)
# Problem: If another dimension is at y=20.2, they overlap
```

### After (Smart Positioning):
```python
# Dimension drawing with collision detection
from drawing_engine.dimensions import DimensionLine

dim_drawer = DimensionLine(ax, scale=1.5)

# First dimension
dim_drawer.draw_horizontal(
    x1=10, x2=50,
    y=20,
    dimension='40"',
    above=True,
    check_collisions=True  # Enable smart positioning
)

# Second dimension - automatically spaced to avoid overlap
dim_drawer.draw_horizontal(
    x1=10, x2=50,
    y=19.5,
    dimension='Width: 40"',
    above=True,
    check_collisions=True
)

# Dimension texts don't overlap - automatically offset!
```

**What Changed:**
- Text offset calculated dynamically: `0.2 + (text_width - dimension_length)/2`
- Nearby dimensions detected and positioned differently
- Text box padding increased from 0.3 to 0.4 for breathing room
- Z-order set to 10 to ensure visibility

---

## Example 2: Specification Table with Text Wrapping

### Before (Text Overflow):
```python
# Simple table - text extends beyond cells
specs = [
    ('Glass Type', 'High Performance Low-E Triple Pane with Argon Gas'),
    ('Frame Color', 'Almond'),
    ('Series', '65'),
]

table = SpecificationTable(ax)
table.draw_table(data=specs, title='SPECIFICATIONS')
# Problem: Long glass type text gets cut off or overlaps with next column
```

### After (Smart Text Handling):
```python
from drawing_engine.components import SpecificationTable
from drawing_engine.text_bounds import SpecificationTableLayouter

specs = [
    ('Glass Type', 'High Performance Low-E Triple Pane with Argon Gas'),
    ('Frame Color', 'Almond'),
    ('Series', '65'),
]

table = SpecificationTable(ax)

# Option 1: Auto-calculate column widths
table.draw_table(
    data=specs,
    title='SPECIFICATIONS',
    min_column_padding=2.0  # 2mm padding in cells
)

# Result: Column widths automatically calculated
# - Label column: 50mm
# - Value column: 100mm
# Long glass text is truncated: "High Performance Low-E Triple Pane..."

# Option 2: Manual layout control
label_width, value_width = SpecificationTableLayouter.calculate_column_widths(
    data=specs,
    total_width=160,
    min_label_width=40,
    min_value_width=40,
    char_width=1.2
)
print(f"Layout: Labels {label_width}mm, Values {value_width}mm")
```

**What Changed:**
- Column widths calculated based on content length
- Long text automatically truncated with ellipsis ("...")
- Minimum 2mm padding inside cells
- Better row height (1.0 unit) for readability
- Alternating row colors with proper z-order

---

## Example 3: Frame Section Labels Without Overlap

### Before (Label Collisions):
```python
# Frame sections - labels overlap with frame content
def _draw_frame_section(ax, x, y, width, height, label):
    bg = Rectangle((x, y - height), width, height, ...)
    ax.add_patch(bg)
    
    # Label positioned too close to content
    ax.text(x + 2, y - 5, label, fontsize=7, fontweight='bold')
    
    # Frame profile box
    outer = Rectangle((x + 5, y - height + 5), width - 10, ...)
    ax.add_patch(outer)
    
    # Problem: "HEAD" label overlaps with frame line
```

### After (Proper Spacing):
```python
def _draw_frame_section(ax, x, y, width, height, label):
    # Section background
    bg = Rectangle((x, y - height), width, height, ...)
    ax.add_patch(bg)
    
    # Label positioned in top-left corner with clearance
    label_x = x + 2
    label_y = y - 3  # Top of frame section with clearance
    
    ax.text(label_x, label_y, label, fontsize=7, fontweight='bold',
           va='top', ha='left', zorder=5)  # zorder ensures visibility
    
    # Frame profile with optimized margins
    frame_margin = 1.5  # Was 5mm - too much
    outer_width = width - 2 * frame_margin
    outer_height = height - 3
    
    outer = Rectangle((x + frame_margin, y - height + 2),
                      outer_width, outer_height - 1, ...)
    ax.add_patch(outer)
    
    # Glass opening with proper spacing
    glass_margin = 2
    glass_width = outer_width - 2 * glass_margin
    glass_height = outer_height - 2 * glass_margin - 1
    
    if glass_width > 0 and glass_height > 0:
        glass = Rectangle((x + frame_margin + glass_margin,
                          y - height + 2 + glass_margin),
                         glass_width, glass_height, ...)
        ax.add_patch(glass)
    
    # Result: "HEAD", "SILL", "JAMB" labels are visible and clear
```

**What Changed:**
- Label positioned at top with 3mm clearance
- Frame margin reduced from 5mm to 1.5mm (better proportions)
- Glass opening margin optimized to 2mm
- Z-order=5 ensures label appears above frame shapes
- Better use of available space

---

## Example 4: Elevation View with Proper Dimension Spacing

### Before (Dimension Overlaps):
```python
# Elevation view - dimension text overlaps
def _draw_elevation_view(ax, x, y, width, height):
    ax.text(x, y - 2, 'ELEVATION', fontsize=7, fontweight='bold')
    
    frame = Rectangle((x, y - height), width, height - 3, ...)
    ax.add_patch(frame)
    
    # Panel grid drawing...
    
    # Dimensions - positioned too close together
    dim_x = x + 2
    dim_y = y - height - 3  # Too close to frame
    
    ax.text(dim_x, dim_y, "W: 4'-0\"", fontsize=6)
    ax.text(dim_x, dim_y - 3, "H: 5'-0\"", fontsize=6)
    # Problem: "W:" and "H:" might overlap if frame is small
```

### After (Smart Spacing):
```python
def _draw_elevation_view(ax, x, y, width, height):
    # Title with proper alignment
    ax.text(x, y - 2, 'ELEVATION', fontsize=7, fontweight='bold',
           va='top', ha='left')
    
    frame = Rectangle((x, y - height), width, height - 3, ...)
    ax.add_patch(frame)
    
    # Panel grid with centered labels
    for i, char in enumerate(config[:4]):
        panel_x = x + 2 + i * panel_width
        panel = Rectangle((panel_x, y - height + 2), panel_width - 1, ...)
        ax.add_patch(panel)
        
        label = 'O' if char in ['O', 'V'] else 'X'
        ax.text(panel_x + panel_width/2, y - height/2, label,
               fontsize=8, fontweight='bold', ha='center',
               va='center', zorder=5)  # Ensure visibility
    
    # Dimensions with extra spacing to avoid overlap
    dim_x = x + 2
    dim_y_width = y - height - 4   # Extra spacing below frame (was -3)
    dim_y_height = y - height - 7  # Further spacing for second dimension
    
    width_ft = int(w_inch / 12)
    width_in = int(w_inch % 12)
    height_ft = int(h_inch // 12)
    height_in = int(h_inch % 12)
    
    # Width dimension with background box
    width_text = f"W: {width_ft}'-{width_in}\""
    ax.text(dim_x, dim_y_width, width_text, fontsize=6, va='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Height dimension with background box
    height_text = f"H: {height_ft}'-{height_in}\""
    ax.text(dim_x, dim_y_height, height_text, fontsize=6, va='top',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Result: Dimensions have 4-7mm spacing, no overlap
```

**What Changed:**
- Extra 1-2mm spacing below frame for dimensions
- White background boxes improve text readability
- Separate y-positions for width (dim_y_width) and height (dim_y_height)
- Better visual hierarchy with proper positioning

---

## Example 5: Complete Safe Text Positioning

### Finding Safe Position for Text:
```python
from drawing_engine.text_bounds import (
    CollisionDetector,
    TextBoundsCalculator
)

# Create collision detector
detector = CollisionDetector(min_spacing=2.0)

# Register some existing text elements
existing_texts = [
    ('72"', 100, 50, 9),
    ('60"', 80, 50, 9),
]

for text, x, y, size in existing_texts:
    bounds = TextBoundsCalculator.get_text_bounds(text, x, y, fontsize=size)
    detector.add_bounds(bounds)

# Try to place new text
new_text = '48"'
base_x, base_y = 90, 50

# Find safe position
safe_x, safe_y, found = detector.find_safe_position(
    base_x=base_x,
    base_y=base_y,
    text=new_text,
    fontsize=9,
    search_radius=20,
    search_steps=16
)

if found:
    print(f"Safe position found: ({safe_x}, {safe_y})")
    ax.text(safe_x, safe_y, new_text, ha='center', va='center')
else:
    print("No safe position - using base position with force placement")
    ax.text(base_x, base_y, new_text, ha='center', va='center')
```

**How It Works:**
1. Registers existing text bounds
2. Checks base position (90, 50) - probably conflicts
3. Searches spiral pattern up to 20mm away
4. Tries 16 directions per search radius step
5. Returns first safe position or falls back to base

---

## Example 6: Complete Drawing with All Fixes

### Real-world Complete Example:
```python
import matplotlib.pyplot as plt
from drawing_engine.dimensions import DimensionLine
from drawing_engine.components import SpecificationTable
from drawing_engine.reference_shop_drawing_generator import ReferenceShopDrawingGenerator

# Create figure
fig = plt.figure(figsize=(11.69, 8.27), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 297)
ax.set_ylim(0, 210)
ax.axis('off')

# Initialize generators
generator = ReferenceShopDrawingGenerator(
    parameters={
        'width': 48,
        'height': 60,
        'series': '65',
        'glass_type': 'Low-E Clear Dual Pane',
        'frame_color': 'White',
        'configuration': 'XO',
    }
)

# Draw complete layout with all collision detection
generator._draw_complete_layout(ax)

# Result: Professional drawing with:
# ✓ No overlapping dimension text
# ✓ Frame labels clearly visible
# ✓ Specification table text fits properly
# ✓ Elevation/plan dimensions properly spaced
# ✓ White backgrounds for text clarity
# ✓ Proper z-order layering
```

---

## Testing Scenarios

### Test 1: Multiple Nearby Dimensions
```python
dim = DimensionLine(ax, scale=1.5)

# Create multiple dimensions at similar heights
for i in range(4):
    dim.draw_horizontal(
        x1=10, x2=50,
        y=20 - i*0.3,
        dimension=f'{35+i*2}"',
        above=(i % 2 == 0),
        check_collisions=True
    )

# Expected: Each dimension text positioned to avoid others
```

### Test 2: Long Text Specifications
```python
specs = [
    ('Long Label', 'Very long value that normally would overflow'),
    ('Short', 'Ok'),
    ('Another Long One', 'Yet another long specification value'),
]

table = SpecificationTable(ax)
table.draw_table(specs, min_column_padding=2.0)

# Expected: All text properly truncated and visible
```

### Test 3: Crowded Frame Section
```python
# Small frame section with all elements
_draw_frame_section(ax, x=50, y=100, width=20, height=15, label='HEAD')

# Expected: Label visible, frame and glass clearly rendered
```

---

## Performance Tips

1. **Batch Collision Detection**
   ```python
   detector = CollisionDetector(min_spacing=2.0)
   
   # Add all existing bounds first
   for text in existing_texts:
       bounds = TextBoundsCalculator.get_text_bounds(...)
       detector.add_bounds(bounds)
   
   # Then find positions for new texts
   for text in new_texts:
       x, y, found = detector.find_safe_position(...)
   ```

2. **Reduce Search Parameters for Speed**
   ```python
   x, y, found = detector.find_safe_position(
       base_x=100, base_y=50,
       text='Label',
       search_radius=10,   # Reduce from 20
       search_steps=8      # Reduce from 16
   )
   ```

3. **Disable Collision Detection When Not Needed**
   ```python
   # For simple drawings with few dimensions
   dim.draw_horizontal(..., check_collisions=False)
   ```

---

## Summary of Improvements

| Issue | Before | After |
|-------|--------|-------|
| Dimension text overlap | Overlapping | Smart positioning |
| Table text overflow | Cut off | Truncated with padding |
| Frame labels | Overlapping content | Clear with zorder |
| Spacing between elements | Inconsistent | 2-4mm minimum |
| Text readability | Low | High (white backgrounds) |
| Visual hierarchy | Flat | Proper z-order layering |

All examples demonstrate how the text overlap fixes work in practice!
