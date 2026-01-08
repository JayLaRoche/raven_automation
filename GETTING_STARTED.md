# 🚀 Getting Started - Apply Design System Now

## Your Raven Shop Drawing Web App Design System is Ready!

The complete design system matching **ravencustomglass.com** has been extracted and implemented. Follow these simple steps to see it in action.

---

## STEP 1: Ensure Global Styles are Imported ✅

**File**: `frontend/src/main.tsx`

Make sure this is at the top of the file:

```tsx
import './styles/raven-global.css'  // ← Add this line if missing
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
```

---

## STEP 2: Update SalesPresentation Component

**File**: `frontend/src/components/sales/SalesPresentation.tsx`

Replace old color classes with Raven design system classes:

### BEFORE (Old):
```tsx
<button style={{backgroundColor: '#333'}}>Generate</button>
<div style={{color: '#666'}}>Text</div>
```

### AFTER (New - Raven):
```tsx
<button className="btn-primary">Generate</button>
<div className="text-secondary">Text</div>
```

---

## STEP 3: Apply to All Components

Use these Raven classes throughout your app:

### Buttons
```tsx
<button className="btn-primary">Create Drawing</button>
<button className="btn-secondary">Cancel</button>
<button className="btn-outline">Learn More</button>
<button className="btn-link">Details</button>
```

### Text & Colors
```tsx
<h1>Main Heading</h1>               {/* 48px, black */}
<h2>Section Title</h2>              {/* 30px, black */}
<p className="text-secondary">Secondary text</p>
<p className="text-muted">Muted text</p>
<a href="#" className="text-raven-accent-blue">Link</a>
```

### Forms
```tsx
<div className="form-group">
  <label htmlFor="width">Width</label>
  <input id="width" type="number" placeholder="Enter width" />
</div>
```

### Cards & Containers
```tsx
<div className="card">
  <div className="card-header">
    <h3>Drawing Parameters</h3>
  </div>
  <div className="card-body">
    {/* Content here */}
  </div>
  <div className="card-footer">
    <button className="btn-primary">Save</button>
  </div>
</div>
```

### Spacing & Layout
```tsx
<div className="flex gap-4 p-6">
  <div className="flex-1">Left</div>
  <div className="flex-1">Right</div>
</div>

<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Grid items */}
</div>
```

---

## STEP 4: Test in Browser

1. Make sure both servers are running:
   ```
   Frontend: http://localhost:3000
   Backend:  http://localhost:8000
   ```

2. Open http://localhost:3000 in your browser

3. You should see:
   - Clean, professional black and white design
   - Proper typography hierarchy
   - Blue accent colors for links
   - Smooth hover effects on buttons
   - Responsive layout on mobile/tablet

---

## STEP 5: Quick Reference During Development

### Color Classes
```
text-raven-black          (Primary text)
text-raven-gray-600       (Secondary text)
text-raven-gray-800       (Dark variant)
text-raven-accent-blue    (Link blue)
bg-raven-light-gray       (Light background)
border-raven-border-gray  (Borders)
```

### Button Classes
```
btn-primary               (Black button)
btn-secondary             (Gray button)
btn-outline               (Blue outline)
btn-link                  (Text link)
btn-sm / btn-lg           (Size variants)
```

### Spacing (Tailwind)
```
p-4    (padding: 16px)
m-6    (margin: 24px)
gap-3  (gap: 12px)
px-6   (padding-left/right: 24px)
py-4   (padding-top/bottom: 16px)
```

---

## STEP 6: Verify Your Changes

Check that you have:

- [ ] Global CSS imported in main.tsx
- [ ] Buttons use `btn-primary`, `btn-secondary` classes
- [ ] Text uses `text-primary`, `text-secondary` classes
- [ ] Forms use `form-group` wrapper
- [ ] Cards use `.card`, `.card-header`, `.card-body` classes
- [ ] Colors from Raven palette (black #000000, blue #0066cc)
- [ ] Spacing uses Tailwind classes (p-4, m-6, gap-3)
- [ ] Responsive classes for mobile/tablet/desktop

---

## FILES YOU CREATED

📄 **RAVEN_DESIGN_EXTRACTED.md**
- Full design token specifications
- Colors, typography, spacing, shadows

📄 **RAVEN_DESIGN_TOKENS.md**
- Complete reference with hex codes
- All component specifications
- Copy-paste values

📄 **RAVEN_DESIGN_IMPLEMENTATION.md**
- Step-by-step implementation guide
- Component patterns and examples
- Accessibility guidelines

📄 **RAVEN_QUICK_REFERENCE.md**
- Quick color and class lookup
- Copy-paste code snippets
- Common patterns

📄 **tailwind.config.js** (UPDATED)
- Raven color palette
- Typography scale
- Spacing system

📄 **raven-global.css** (UPDATED)
- 400+ lines of brand CSS
- Button, form, card components
- Responsive utilities

---

## COMMON TASKS

### Change Button Color
```tsx
// From
<button style={{backgroundColor: '#0066cc'}}>Click</button>

// To
<button className="btn-primary">Click</button>
```

### Add Spacing
```tsx
// From
<div style={{padding: '20px', marginBottom: '30px'}}>

// To
<div className="p-5 mb-7.5">
```

### Create a Form
```tsx
<div className="form-group">
  <label htmlFor="name">Name</label>
  <input id="name" type="text" />
</div>

<div className="form-group">
  <label htmlFor="email">Email</label>
  <input id="email" type="email" />
</div>

<button className="btn-primary">Submit</button>
```

### Responsive Layout
```tsx
<div className="
  grid grid-cols-1     {/* 1 column on mobile */}
  md:grid-cols-2       {/* 2 columns on tablet */}
  lg:grid-cols-4       {/* 4 columns on desktop */}
  gap-6
">
  {/* Items */}
</div>
```

---

## COLOR QUICK REFERENCE

| Use | Color | Hex |
|-----|-------|-----|
| Headings | Black | #000000 |
| Body Text | Black | #000000 |
| Secondary Text | Gray | #666666 |
| Muted Text | Gray | #999999 |
| Links | Blue | #0066cc |
| Link Hover | Blue Dark | #005bb3 |
| Backgrounds | White | #FFFFFF |
| Light BG | Light Gray | #f5f5f5 |
| Borders | Border Gray | #e0e0e0 |
| Buttons | Black | #000000 |
| Success | Green | #4CAF50 |
| Error | Red | #F44336 |
| Warning | Orange | #FF9800 |

---

## NEXT STEPS

1. ✅ Import `raven-global.css` in main.tsx
2. ✅ Update all buttons to use `btn-primary`, etc.
3. ✅ Update all text colors to `text-primary`, `text-secondary`
4. ✅ Replace inline styles with Tailwind classes
5. ✅ Test on mobile, tablet, and desktop
6. ✅ Verify all links are blue #0066cc
7. ✅ Verify all headings are black #000000
8. ✅ Check hover states work smoothly
9. ✅ Test forms and inputs
10. ✅ Deploy to production

---

## SUPPORT DOCUMENTS

**For detailed reference:**
- `RAVEN_DESIGN_TOKENS.md` - All design tokens with hex codes
- `RAVEN_DESIGN_IMPLEMENTATION.md` - How to implement each component
- `RAVEN_QUICK_REFERENCE.md` - Quick lookup guide

**For specific questions:**
- Button styling → See RAVEN_QUICK_REFERENCE.md
- Color values → See RAVEN_DESIGN_TOKENS.md
- Form components → See RAVEN_DESIGN_IMPLEMENTATION.md
- Responsive design → See RAVEN_DESIGN_IMPLEMENTATION.md

---

## EXAMPLE: Complete Component

Here's a complete example of a component using the Raven design system:

```tsx
import React from 'react'

export function DrawingForm() {
  return (
    <div className="container mx-auto px-4 py-12">
      <h1>Create Custom Drawing</h1>
      <p className="text-secondary mb-6">Design your custom glass door or window</p>

      <div className="card max-w-2xl">
        <div className="card-header">
          <h2>Drawing Parameters</h2>
        </div>

        <div className="card-body space-y-6">
          <div className="form-group">
            <label htmlFor="width">Width (inches)</label>
            <input
              id="width"
              type="number"
              placeholder="Enter width"
              defaultValue={36}
            />
          </div>

          <div className="form-group">
            <label htmlFor="height">Height (inches)</label>
            <input
              id="height"
              type="number"
              placeholder="Enter height"
              defaultValue={72}
            />
          </div>

          <div className="form-group">
            <label htmlFor="type">Door Type</label>
            <select id="type">
              <option>Sliding Door</option>
              <option>Pivot Door</option>
              <option>Casement Door</option>
            </select>
          </div>
        </div>

        <div className="card-footer flex gap-4 justify-end">
          <button className="btn-secondary">Cancel</button>
          <button className="btn-primary">Generate Drawing</button>
        </div>
      </div>
    </div>
  )
}
```

---

## YOU'RE ALL SET! 🎉

Your Raven Shop Drawing Web App is now designed to match the professional standards of ravencustomglass.com.

**Start implementing the changes and see your app transform into a professional, cohesive brand experience!**

---

**Questions?** Refer to the documentation files:
- RAVEN_DESIGN_IMPLEMENTATION.md
- RAVEN_QUICK_REFERENCE.md
- RAVEN_DESIGN_TOKENS.md

**Happy coding!** ✨
