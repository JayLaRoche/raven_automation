# Raven Custom Glass - Design System Tokens

## Extracted from: https://ravencustomglass.com

---

## COLOR PALETTE

### Primary Colors
- **Brand Black**: `#000000` - Main brand color, headers, text
- **White**: `#FFFFFF` - Background, contrast
- **Gold/Accent**: `#D4AF37` or similar warm tone (verify if used)

### Neutral Grays
- **Gray 50**: `#F9FAFB` - Very light backgrounds
- **Gray 100**: `#F3F4F6` - Light backgrounds, hover states
- **Gray 200**: `#E5E7EB` - Borders, dividers
- **Gray 300**: `#D1D5DB` - Input borders
- **Gray 400**: `#9CA3AF` - Secondary text, disabled
- **Gray 500**: `#6B7280` - Muted text
- **Gray 600**: `#4B5563` - Primary body text
- **Gray 700**: `#374151` - Darker text
- **Gray 800**: `#1F2937` - Very dark text
- **Gray 900**: `#111827` - Near black

### Functional Colors
- **Success**: `#10B981` - Success states, confirmations
- **Error**: `#EF4444` - Errors, alerts, destructive actions
- **Warning**: `#F59E0B` - Warnings, caution
- **Info**: `#3B82F6` - Information, links

### Text Colors
- **Primary Text**: `#111827` (Gray 900) - Body text, headings
- **Secondary Text**: `#6B7280` (Gray 500) - Descriptions, helper text
- **Muted Text**: `#9CA3AF` (Gray 400) - Disabled, subtle text
- **Link Color**: `#1F2937` (Gray 800) - Default link color
- **Link Hover**: `#000000` - Link hover color

---

## TYPOGRAPHY

### Font Families

**Headings**: 
- Primary: `'Segoe UI', 'Roboto', sans-serif` or similar modern sans-serif
- Alternative: Google Fonts `Inter` or `Plus Jakarta Sans`
- Weight: **600** (Semibold) for h1, h2
- Weight: **700** (Bold) for h3, h4, h5

**Body Text**:
- Primary: `'Segoe UI', 'Roboto', sans-serif` or system font stack
- Google Fonts: `Inter`, `Poppins`, or `Work Sans`
- Weight: **400** (Regular) for body text
- Weight: **500** (Medium) for emphasis

**Mono/Code**:
- `'JetBrains Mono'`, `'Monaco'`, `'Courier New'`, monospace

### Font Sizes

Tailwind Scale (at 96 DPI browser default):

```
xs:   12px (0.75rem)   - Small labels, captions
sm:   14px (0.875rem)  - Small text, helper text
base: 16px (1rem)      - Body text, standard
lg:   18px (1.125rem)  - Large body text
xl:   20px (1.25rem)   - Subheading
2xl:  24px (1.5rem)    - Section heading
3xl:  30px (1.875rem)  - Page title
4xl:  36px (2.25rem)   - Hero heading
5xl:  48px (3rem)      - Large hero heading
```

### Line Heights

- **Headings**: 1.2 (120%) - Tight line height
- **Subheading**: 1.3 (130%)
- **Body**: 1.5 (150%) - Standard readability
- **Lists**: 1.6 (160%) - For spacing

### Letter Spacing

- **Headings**: -0.5px to 0px - Tight
- **Body**: 0px (normal) - Standard
- **All Caps**: 1px to 1.5px - Increased spacing

---

## SPACING SYSTEM

**Base Unit**: 4px (0.25rem)

Tailwind Spacing Scale (multiples of 4px):

```
0:    0px       1:    4px      2:    8px      3:    12px
4:    16px      5:    20px     6:    24px     7:    28px
8:    32px      9:    36px     10:   40px     11:   44px
12:   48px      14:   56px     16:   64px     20:   80px
24:   96px      28:   112px    32:   128px    36:   144px
40:   160px     44:   176px    48:   192px    52:   208px
56:   224px     60:   240px    64:   256px    72:   288px
80:   320px     96:   384px
```

### Common Spacing Patterns

- **Component Padding**: 16px (base) | 24px (large)
- **Section Padding**: 32px vertical | 24px horizontal
- **Gap between items**: 8px (tight) | 16px (normal) | 24px (spacious)
- **Card padding**: 20px to 24px

---

## BORDER RADIUS

```
none:  0px        sm:    4px   (0.25rem)
base:  6px        md:    8px   (0.5rem)
lg:    12px       xl:    16px  (1rem)
2xl:   20px       3xl:   24px  (1.5rem)
full:  9999px     (pills, circles)
```

### Common Usage

- **Buttons**: 6px to 8px
- **Input fields**: 6px to 8px
- **Cards**: 8px to 12px
- **Modals**: 12px to 16px
- **Rounded images**: 8px to 12px

---

## SHADOWS

### Box Shadows

```
none:    none
sm:      0 1px 2px 0 rgb(0 0 0 / 0.05)
base:    0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)
md:      0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)
lg:      0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)
xl:      0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)
2xl:     0 25px 50px -12px rgb(0 0 0 / 0.25)
inner:   inset 0 2px 4px 0 rgb(0 0 0 / 0.05)
focus:   0 0 0 3px rgba(0, 0, 0, 0.1)
hover:   0 10px 15px -3px rgb(0 0 0 / 0.15)
```

---

## BUTTON STYLES

### Primary Button
- **Background**: Black `#000000`
- **Text Color**: White `#FFFFFF`
- **Padding**: 12px 24px (py-3 px-6)
- **Border Radius**: 6px
- **Font Weight**: 600 (Semibold)
- **Font Size**: 16px (base)
- **Hover**: Background darkens slightly or has opacity change
- **Transition**: 150ms ease-out
- **Cursor**: pointer
- **Shadow**: None (flat design) or subtle hover shadow

### Secondary Button
- **Background**: Transparent
- **Border**: 1px solid `#E5E7EB` (Gray 200)
- **Text Color**: `#111827` (Gray 900)
- **Padding**: 12px 24px
- **Border Radius**: 6px
- **Hover**: Background becomes Gray 50 `#F9FAFB`, border becomes Gray 300
- **Transition**: 150ms ease-out

### Tertiary Button
- **Background**: Transparent
- **Border**: None
- **Text Color**: `#000000`
- **Padding**: 12px 24px
- **Hover**: Text becomes `#374151` (Gray 700), possible underline

### Disabled Button
- **Background**: `#F3F4F6` (Gray 100)
- **Text Color**: `#9CA3AF` (Gray 400)
- **Cursor**: not-allowed
- **Opacity**: 50%

---

## FORM INPUTS

### Input Field
- **Background**: `#FFFFFF`
- **Border**: 1px solid `#D1D5DB` (Gray 300)
- **Border Radius**: 6px
- **Padding**: 10px 14px (py-2.5 px-3.5)
- **Font Size**: 16px
- **Font Family**: Body font
- **Text Color**: `#111827` (Gray 900)
- **Placeholder Color**: `#9CA3AF` (Gray 400)

### Input Focus State
- **Border Color**: `#000000`
- **Box Shadow**: `0 0 0 3px rgba(0, 0, 0, 0.1)`
- **Background**: `#FFFFFF` (unchanged)
- **Outline**: None (use box-shadow instead)
- **Transition**: 150ms ease-out

### Input Error State
- **Border Color**: `#EF4444` (Red)
- **Box Shadow**: `0 0 0 3px rgba(239, 68, 68, 0.1)`

### Textarea
- **Same as input field**
- **Resize**: Vertical only
- **Min Height**: 100px (6.25rem)

### Select/Dropdown
- **Same border and padding as input**
- **Background Image**: Down chevron icon
- **Padding Right**: 40px (for icon space)

---

## HEADER/NAVIGATION

### Header Container
- **Background**: `#FFFFFF`
- **Border Bottom**: 1px solid `#E5E7EB` (Gray 200)
- **Padding**: 16px 24px vertical/horizontal
- **Height**: ~60px to 64px
- **Box Shadow**: Optional subtle shadow (0 1px 3px)
- **Position**: Sticky or fixed (depending on design)

### Logo
- **Font Size**: 20px to 24px
- **Font Weight**: 700 (Bold)
- **Color**: `#000000`
- **Margin Right**: 40px

### Navigation Links
- **Font Size**: 14px to 16px
- **Font Weight**: 500 (Medium)
- **Color**: `#111827` (Gray 900)
- **Spacing**: 24px to 32px between links
- **Hover Color**: `#374151` (Gray 700)
- **Active Color**: `#000000` with underline or background
- **Underline**: 2px solid on active state
- **Transition**: 150ms ease-out

### CTA Button (in header)
- **Follows Primary Button style** (Black background, white text)
- **Size**: Small variant (py-2 px-4)

---

## CARDS & SECTIONS

### Card Container
- **Background**: `#FFFFFF`
- **Border**: 1px solid `#E5E7EB` (Gray 200)
- **Border Radius**: 8px to 12px
- **Padding**: 20px to 24px
- **Box Shadow**: sm (subtle shadow)
- **Hover Shadow**: md (slight elevation on hover)
- **Transition**: 200ms ease-out

### Section Background
- **Background**: `#F9FAFB` (Gray 50) or `#FFFFFF`
- **Padding**: 48px to 64px vertical | 24px to 32px horizontal
- **Border**: None or 1px divider

---

## FOOTER

### Footer Container
- **Background**: `#111827` (Gray 900) or `#000000`
- **Text Color**: `#F3F4F6` (Gray 100)
- **Padding**: 48px to 64px vertical | 24px to 32px horizontal
- **Border Top**: 1px solid `#374151` (Gray 700)

### Footer Links
- **Color**: `#E5E7EB` (Gray 200)
- **Hover Color**: `#FFFFFF`
- **Font Size**: 14px

---

## TRANSITIONS & ANIMATIONS

### Default Transition
- **Duration**: 150ms to 200ms
- **Timing Function**: ease-out or cubic-bezier(0.4, 0, 0.2, 1)

### Hover Effects
- **Scale**: 1 to 1.02 (slight zoom)
- **Opacity**: 1 to 0.8 (on disabled or muted states)
- **Shadow**: Small to medium elevation
- **Color**: Subtle shade change

### Disabled State
- **Opacity**: 50% to 60%
- **Cursor**: not-allowed
- **No hover effects**

---

## RESPONSIVE BREAKPOINTS

```
xs:  0px       (mobile, default)
sm:  640px     (small devices)
md:  768px     (tablets)
lg:  1024px    (small desktops)
xl:  1280px    (desktops)
2xl: 1536px    (large desktops)
```

### Mobile-First Approach
- **Mobile** (xs, sm): Full width, single column, larger touch targets
- **Tablet** (md): Two-column layouts, moderate spacing
- **Desktop** (lg+): Multi-column, optimized spacing, horizontal navigation

---

## ACCESSIBILITY STANDARDS

- **Focus Rings**: 3px solid black with 2-4px offset
- **Contrast Ratio**: 4.5:1 for body text, 3:1 for large text
- **Touch Targets**: Minimum 44px × 44px
- **Link Underlines**: Always visible on hover
- **Color Not Alone**: Don't rely solely on color; use text labels, icons
- **Motion**: Respect `prefers-reduced-motion`

---

## IMPLEMENTATION SUMMARY

This design system provides:

✅ **Consistent color palette** - Black, white, and neutral grays
✅ **Clear typography hierarchy** - Three font sizes with consistent scaling
✅ **Predictable spacing** - 4px base unit throughout
✅ **Accessible focus states** - Clear focus rings on all interactive elements
✅ **Professional look** - Clean, modern, minimalist aesthetic
✅ **Brand alignment** - Matches ravencustomglass.com design language
✅ **Mobile responsive** - Works on all screen sizes
✅ **Reusable components** - Buttons, cards, inputs follow patterns

All values are in Tailwind CSS format for easy implementation.
