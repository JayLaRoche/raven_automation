# RAVEN DESIGN TOKENS - Complete Reference

## 1. COLORS

### Primary Palette
```
Black         #000000  (Primary text, headings, headers)
White         #FFFFFF  (Backgrounds, content areas)
Dark Gray     #1a1a1a  (Secondary black variant)
Light Gray    #f5f5f5  (Light backgrounds)
Border Gray   #e0e0e0  (Borders, dividers)
```

### Gray Scale (9-step)
```
50%  #f9f9f9  (Lightest background)
100% #f5f5f5  (Light gray background)
200% #e0e0e0  (Subtle borders)
300% #d0d0d0  (Secondary borders)
400% #b0b0b0  (Medium gray)
500% #808080  (Neutral gray)
600% #666666  (Secondary text)
700% #4d4d4d  (Dark gray text)
800% #1a1a1a  (Very dark gray)
900% #0a0a0a  (Near black)
```

### Accent Colors
```
Gold          #d4af37  (Premium touches, hover)
Blue          #0066cc  (Links, CTAs, primary interactive)
Blue Hover    #005bb3  (Link hover state)
```

### Text Colors
```
Primary       #000000  (Main headings and text)
Secondary     #666666  (Secondary content)
Muted         #999999  (Tertiary text, metadata)
Light         #f5f5f5  (Text on dark backgrounds)
```

### Functional Colors
```
Success       #4CAF50  (Success messages, confirmations)
Warning       #FF9800  (Warnings, caution)
Error         #F44336  (Errors, danger states)
Info          #2196F3  (Informational messages)
```

---

## 2. TYPOGRAPHY

### Font Families
```
Heading:  -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif
Body:     -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif
Mono:     'Monaco', 'Menlo', 'Ubuntu Mono', monospace
```

### Font Weights
```
Light:        300
Normal:       400
Medium:       500
Semibold:     600
Bold:         700
Extrabold:    800
```

### Font Sizes & Line Heights
```
xs     12px   Line-height: 1.2   (Small labels, captions)
sm     14px   Line-height: 1.5   (Small text, secondary)
base   16px   Line-height: 1.5   (Body text, default)
lg     18px   Line-height: 1.5   (Larger body, emphasis)
xl     20px   Line-height: 1.5   (Subheadings)
2xl    24px   Line-height: 1.2   (Section titles)
3xl    30px   Line-height: 1.2   (Page headings)
4xl    36px   Line-height: 1.1   (Major headings)
5xl    48px   Line-height: 1.1   (Hero headings)
```

### Line Heights
```
Tight:        1.2   (Headings)
Normal:       1.5   (Body text)
Relaxed:      1.75  (Large text blocks)
Loose:        2     (Very loose spacing)
```

### Letter Spacing
```
Tight:        -0.02em  (Tight spacing)
Normal:       0        (Default)
Wide:         0.025em  (Wide spacing)
Wider:        0.05em   (Very wide spacing)
```

---

## 3. SPACING

### Base Unit: 4px
```
0     0
1     4px
2     8px
3     12px
4     16px   ← Standard padding/margin
5     20px
6     24px
7     28px
8     32px
10    40px
12    48px
14    56px
16    64px
20    80px
24    96px
28    112px
32    128px
```

### Common Padding/Margin
```
Component padding:      16px (space-4)
Card padding:           24px (space-6)
Section padding:        32px (space-8)
Container padding:      16px (space-4)
```

### Gap Spacing
```
Inline elements:        8px (space-2)
Component sections:     16px (space-4)
Layout columns:         24px (space-6)
Large sections:         32px (space-8)
```

---

## 4. BORDER RADIUS

```
none   0
sm     4px
md     6px      ← Primary button/input radius
lg     8px      ← Primary card radius
xl     12px
2xl    16px
full   9999px   (circle)
```

### Usage
```
Buttons:        6-8px (rounded-md to rounded-lg)
Inputs:         6px (rounded-md)
Cards:          8px (rounded-lg)
Images:         0-8px
Containers:     8-12px
```

---

## 5. SHADOWS

### Shadow Values
```
none    none
sm      0 1px 2px 0 rgba(0, 0, 0, 0.05)
md      0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
lg      0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
xl      0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)
2xl     0 25px 50px -12px rgba(0, 0, 0, 0.25)
hover   0 10px 20px -5px rgba(0, 0, 0, 0.15)
```

### Usage
```
Cards (default):     shadow-sm
Cards (hover):       shadow-lg or shadow-hover
Buttons (default):   shadow-md
Buttons (hover):     shadow-lg with -2px elevation
Floating elements:   shadow-xl
Modal dialogs:       shadow-2xl
```

---

## 6. BORDER STYLES

### Border Colors
```
Gray-200      #e0e0e0   (Default, subtle)
Gray-300      #d0d0d0   (Secondary)
Gray-400      #b0b0b0   (Heavier)
Blue          #0066cc   (Focus state)
Red           #F44336   (Error state)
```

### Border Widths
```
1px   Standard border (inputs, cards)
2px   Focus/active states
3px   Strong emphasis
```

---

## 7. TRANSITIONS

### Duration
```
100ms   Fast (micro-interactions)
200ms   Standard (default interactions)
300ms   Slow (major changes)
500ms   Very slow (extended animations)
```

### Timing Functions
```
linear      cubic-bezier(0, 0, 1, 1)
ease-in     cubic-bezier(0.42, 0, 1, 1)
ease-out    cubic-bezier(0, 0, 0.58, 1)
ease-smooth cubic-bezier(0.42, 0, 0.58, 1)
bounce      cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

### Properties to Animate
```
Color:         200ms ease-smooth
Background:    200ms ease-smooth
Shadow:        200ms ease-smooth
Transform:     200ms ease-smooth (elevation)
Opacity:       200ms ease-smooth (fade)
```

---

## 8. Z-INDEX SCALE

```
auto          (default)
0             (background)
10            (buried elements)
20            (default content)
30            (lifted content)
40            (floating elements)
50            (important floating)
100           (modals, overlays)
1000          (header, sticky elements)
```

### Usage
```
Regular content:       z-0 to z-20
Dropdowns/Popovers:    z-40 to z-50
Modal backdrop:        z-100
Modal dialog:          z-100+ (50 higher)
Header/sticky:         z-1000
Notifications:         z-1000
```

---

## 9. BREAKPOINTS

```
xs    Default    (<640px)
sm    640px+     (Tablet small)
md    768px+     (Tablet)
lg    1024px+    (Laptop)
xl    1280px+    (Desktop)
2xl   1536px+    (Large desktop)
```

### Responsive Prefixes
```
sm:text-lg       → 16px on tablet, 18px on tablet+
md:grid-cols-2   → 1 column on mobile, 2 on tablet+
lg:gap-8         → 16px gap on mobile, 32px on laptop+
```

---

## 10. CONTAINER SIZES

```
sm    24rem   (384px)
md    28rem   (448px)
lg    32rem   (512px)
xl    36rem   (576px)
2xl   42rem   (672px)
3xl   48rem   (768px)
4xl   56rem   (896px)
5xl   64rem   (1024px)
6xl   72rem   (1152px)
```

---

## 11. BUTTON SPECIFICATIONS

### Primary Button
```
Background:     #000000 (black)
Text:           #FFFFFF (white)
Padding:        12px 24px (0.75rem 1.5rem)
Border Radius:  6px (0.375rem)
Font Weight:    600 (semibold)
Font Size:      16px (1rem)
Shadow:         md (default), hover (hover)
Hover State:    #1a1a1a (dark gray), shadow-lg, -2px elevation
Transition:     200ms ease-smooth
```

### Secondary Button
```
Background:     #f5f5f5 (light gray)
Text:           #000000 (black)
Border:         1px #e0e0e0
Padding:        12px 24px
Border Radius:  6px
Font Weight:    600
Hover State:    #efefef background, #d0d0d0 border
```

### Outline Button
```
Background:     transparent
Border:         2px #0066cc
Text:           #0066cc
Padding:        12px 24px
Hover State:    rgba(0, 102, 204, 0.05) background
```

### Link Button
```
Background:     transparent
Text:           #0066cc
Padding:        8px 12px
Font Weight:    500
Hover State:    #005bb3 text, underline
```

---

## 12. FORM ELEMENT SPECIFICATIONS

### Input Field
```
Border:         1px #e0e0e0
Padding:        12px 16px
Border Radius:  6px
Font Size:      16px
Background:     #FFFFFF (white)
Text Color:     #000000
Placeholder:    #999999 (muted)
Focus Border:   #0066cc
Focus Shadow:   0 0 0 3px rgba(0, 102, 204, 0.1)
```

### Label
```
Font Size:      15px (0.95rem)
Font Weight:    600 (semibold)
Color:          #000000
Margin Bottom:  8px
Required:       Append red asterisk
```

### Textarea
```
Same as Input
Min Height:     96px (6rem)
Resize:         vertical only
```

### Select
```
Same as Input
Background Image:  Dropdown SVG arrow (right-aligned)
Padding Right:     40px (account for arrow)
```

---

## 13. CARD SPECIFICATIONS

```
Background:     #FFFFFF
Border:         1px #e0e0e0
Border Radius:  8px
Padding:        24px (1.5rem)
Shadow:         sm (default)
Hover Shadow:   lg
Hover Transform: translateY(-2px)
Hover Border:   #d0d0d0

Card Header:
  Margin Bottom:   16px
  Padding Bottom:  16px
  Border Bottom:   1px #e0e0e0

Card Body:
  Margin:  0

Card Footer:
  Margin Top:      16px
  Padding Top:     16px
  Border Top:      1px #e0e0e0
```

---

## 14. HEADER SPECIFICATIONS

```
Background:     #FFFFFF
Border Bottom:  1px #e0e0e0
Padding:        16px 0
Position:       sticky, top: 0
Z-Index:        1000
Shadow:         sm

Navigation Links:
  Color:            #000000
  Font Weight:      500
  Padding:          8px 16px
  Border Bottom:    2px transparent
  Hover Border:     2px #0066cc
  Hover Color:      #0066cc
```

---

## 15. ACCESSIBILITY

### Focus States
```
Outline:       2px solid #0066cc
Outline Offset: 2px
Border Radius:  varies by element
```

### Color Contrast
```
Black text on white:      21:1 ✓✓ (AAA)
Black text on gray:       ≥4.5:1 ✓✓ (AA)
Blue text:                ≥4.5:1 ✓ (AA)
```

### Motion
```
Default:       200ms ease-smooth
Prefers Reduced Motion:  100ms or disable animations
```

---

## 16. RESPONSIVE TYPOGRAPHY

### Mobile (<640px)
```
h1: 30px
h2: 24px
h3: 20px
p:  16px
```

### Tablet (640px-1024px)
```
h1: 36px
h2: 28px
h3: 24px
p:  16px
```

### Desktop (1024px+)
```
h1: 48px
h2: 30px
h3: 24px
p:  16px
```

---

## 17. ANIMATION KEYFRAMES

### Fade In
```
0%    { opacity: 0 }
100%  { opacity: 1 }
Duration: 300ms
```

### Slide Up
```
0%    { opacity: 0; transform: translateY(10px) }
100%  { opacity: 1; transform: translateY(0) }
Duration: 300ms
```

### Slide Down
```
0%    { opacity: 0; transform: translateY(-10px) }
100%  { opacity: 1; transform: translateY(0) }
Duration: 300ms
```

### Pulse
```
0%, 100%  { opacity: 1 }
50%       { opacity: 0.7 }
Duration: 2000ms (infinite)
```

---

## 18. IMPLEMENTATION CHECKLIST

- [x] Color palette defined
- [x] Typography scale created
- [x] Spacing system established
- [x] Border radius tokens
- [x] Shadow definitions
- [x] Button specifications
- [x] Form element styles
- [x] Card component specs
- [x] Header/navigation specs
- [x] Responsive breakpoints
- [x] Accessibility standards
- [x] Animation keyframes

---

## 19. FILE REFERENCES

```
tailwind.config.js          ← Color and sizing config
raven-global.css            ← Global brand styles
RAVEN_DESIGN_EXTRACTED.md   ← Full specifications
RAVEN_DESIGN_IMPLEMENTATION.md ← How to use
RAVEN_QUICK_REFERENCE.md    ← Quick lookup
```

---

## 20. QUICK COPY-PASTE COLORS

```css
/* Primary */
color: #000000;                    /* Black */
background-color: #FFFFFF;         /* White */

/* Accents */
color: #0066cc;                    /* Blue */
color: #d4af37;                    /* Gold */

/* Grays */
color: #666666;                    /* Secondary text */
border-color: #e0e0e0;            /* Borders */
background-color: #f5f5f5;        /* Light background */

/* Functional */
color: #4CAF50;                    /* Success */
color: #F44336;                    /* Error */
color: #FF9800;                    /* Warning */
```

---

**Last Updated**: December 2024
**Source**: https://ravencustomglass.com
**Design System Version**: 1.0
