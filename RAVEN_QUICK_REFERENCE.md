# Raven Design System - Quick Reference

## COLOR PALETTE

```
NEUTRALS:
  Black:          #000000
  Dark Gray:      #1a1a1a
  Gray:           #666666
  Light Gray:     #f5f5f5
  Border Gray:    #e0e0e0
  White:          #FFFFFF

ACCENTS:
  Premium Gold:   #d4af37
  Link Blue:      #0066cc
  Link Hover:     #005bb3

FUNCTIONAL:
  Success:        #4CAF50
  Warning:        #FF9800
  Error:          #F44336
  Info:           #2196F3
```

## TAILWIND CLASSES

```
// Colors
text-raven-black          text-raven-accent-blue
bg-raven-light-gray       border-raven-border-gray

// Buttons
btn-primary               btn-secondary
btn-outline               btn-link
btn-sm                    btn-lg

// Forms
form-group                (wrapper for label + input)

// Cards
card                      card-header
card-body                 card-footer

// Text
text-primary              text-secondary
text-muted                text-light

// Spacing (Tailwind classes)
p-4   m-6   gap-3   px-6   py-4

// Borders & Shadows
shadow-sm                 shadow-lg
border-subtle

// Transitions
transition-default        transition-fast
transition-slow
```

## COMPONENT PATTERNS

### Button
```tsx
<button className="btn-primary">Primary Action</button>
<button className="btn-secondary">Secondary</button>
<button className="btn-outline">Outline</button>
<button className="btn-link">Link Button</button>
```

### Form Input
```tsx
<div className="form-group">
  <label htmlFor="input-id">Label Text</label>
  <input id="input-id" type="text" placeholder="..." />
</div>
```

### Card
```tsx
<div className="card">
  <div className="card-header">
    <h3>Title</h3>
  </div>
  <div className="card-body">Content</div>
  <div className="card-footer">Footer</div>
</div>
```

### Text Hierarchy
```tsx
<h1>Heading 1 (48px)</h1>      {/* Page title */}
<h2>Heading 2 (30px)</h2>      {/* Section */}
<h3>Heading 3 (24px)</h3>      {/* Subsection */}
<p>Body text (16px)</p>
<small>Small text (14px)</small>
```

## RESPONSIVE BREAKPOINTS

```
Mobile:    < 640px      (default)
Tablet:    ≥ 640px      (sm:)
Medium:    ≥ 768px      (md:)
Laptop:    ≥ 1024px     (lg:)
Desktop:   ≥ 1280px     (xl:)

Example:
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
```

## SPACING SCALE (4px base)

```
space-0:   0
space-1:   4px
space-2:   8px
space-3:   12px
space-4:   16px
space-6:   24px
space-8:   32px
space-10:  40px
space-12:  48px

Usage: p-4, m-6, gap-3, px-6, py-4
```

## FONT SIZING

```
text-xs:   12px
text-sm:   14px
text-base: 16px      (default)
text-lg:   18px
text-xl:   20px
text-2xl:  24px
text-3xl:  30px
text-4xl:  36px
text-5xl:  48px
```

## SHADOWS

```
shadow-sm:   subtle shadow
shadow-md:   medium shadow
shadow-lg:   large shadow (hover state)
shadow-xl:   extra large
shadow-hover: elevation on hover
```

## BORDER RADIUS

```
rounded-none:  0
rounded-sm:    4px
rounded-md:    6px
rounded-lg:    8px
rounded-xl:    12px
rounded-2xl:   16px
rounded-full:  circle
```

## QUICK IMPLEMENTATION STEPS

1. Import in main.tsx:
   ```tsx
   import './styles/raven-global.css'
   ```

2. Use Raven classes:
   ```tsx
   <button className="btn-primary">Click</button>
   <div className="card">
     <p className="text-secondary">Content</p>
   </div>
   ```

3. For custom colors, use CSS variables:
   ```tsx
   <div style={{color: 'var(--raven-accent-blue)'}}>Blue text</div>
   ```

4. Use Tailwind for layout:
   ```tsx
   <div className="flex gap-4 p-6">
     <div className="flex-1">Left</div>
     <div className="flex-1">Right</div>
   </div>
   ```

## TYPOGRAPHY RULES

- **Headings**: Bold, tight line-height (1.2)
- **Body**: Regular weight, relaxed line-height (1.6)
- **Labels**: Medium weight (500)
- **Small text**: Gray secondary color
- **Links**: Blue, underline on hover

## ACCESSIBILITY CHECKLIST

✓ All buttons and links have focus states (automatic)
✓ Form labels associated with inputs (use htmlFor)
✓ Color contrast ratio ≥ 4.5:1 (black/white guaranteed)
✓ Keyboard navigation support (built-in)
✓ Semantic HTML elements
✓ ARIA attributes where needed

## HOVER STATES (Automatic)

```
Buttons:      Elevate 2px, darken
Cards:        Elevate, darken border
Links:        Color change, underline
Inputs:       Blue border, blue shadow on focus
```

## CSS VARIABLES

```css
/* Colors */
--raven-black
--raven-white
--raven-accent-blue
--raven-accent-gold
--raven-text-primary
--raven-text-secondary

/* Spacing */
--space-4     (16px)
--space-6     (24px)
--space-8     (32px)

/* Effects */
--shadow-md
--shadow-hover
--transition-default
--radius-lg

Usage: color: var(--raven-accent-blue);
```

## GOTCHAS

❌ Don't use bg-blue-500 - use text-raven-accent-blue
❌ Don't create custom shadows - use shadow-md, shadow-lg
❌ Don't use arbitrary colors - stick to Raven palette
❌ Don't remove raven-global.css import
✓ DO use semantic HTML
✓ DO use Tailwind spacing classes
✓ DO combine btn-primary with btn-sm/btn-lg
✓ DO wrap form inputs with form-group

---

**For detailed documentation, see: RAVEN_DESIGN_IMPLEMENTATION.md**
