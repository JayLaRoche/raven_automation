# Raven Shop Drawing Web App - Design System Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the Raven Custom Glass design system (extracted from ravencustomglass.com) into the web application.

---

## Design System Summary

The Raven design system is built on clean, minimal, professional aesthetics with:
- **Primary Colors**: Pure black (#000000) and white (#FFFFFF)
- **Gray Palette**: 9-step scale for depth and hierarchy  
- **Accent Colors**: Gold (#d4af37) and blue (#0066cc) for premium touches
- **Typography**: System font stack for modern, accessible reading
- **Spacing**: 4px base unit for consistent rhythm
- **Shadows**: Subtle depth with hover elevation effects
- **Transitions**: 200ms default easing for smooth interactions

---

## File Structure

```
frontend/src/
├── styles/
│   └── raven-global.css          [CREATED] Global brand styles
├── components/
│   ├── ui/
│   │   └── RavenComponents.tsx    [AVAILABLE] UI component library
│   └── sales/
│       └── SalesPresentation.tsx  [UPDATED] Main app component
└── main.tsx                        [IMPORT] raven-global.css here
```

---

## 1. SETUP INSTRUCTIONS

### 1.1 Import Global Styles

In `frontend/src/main.tsx`, ensure the global CSS is imported at the top:

```tsx
import './styles/raven-global.css'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
```

**Status**: ✅ Required - do this first

### 1.2 Verify Tailwind Configuration

Check that `tailwind.config.js` in the project root includes the Raven color palette:

```javascript
colors: {
  raven: {
    black: '#000000',
    white: '#FFFFFF',
    'gray-50': '#f9f9f9',
    // ... full palette
    'accent-gold': '#d4af37',
    'accent-blue': '#0066cc',
  },
}
```

**Status**: ✅ Already configured

---

## 2. COMPONENT STYLING GUIDELINES

### 2.1 Typography Hierarchy

Use these classes for text hierarchy:

```tsx
// Headings
<h1>Major Page Heading</h1>           {/* 48px, bold */}
<h2>Section Heading</h2>              {/* 30px, bold */}
<h3>Subsection Heading</h3>           {/* 24px, bold */}
<h4>Minor Heading</h4>                {/* 20px, bold */}

// Body Text
<p>Regular paragraph text</p>         {/* 16px, regular */}
<small>Smaller supporting text</small>{/* 14px */}

// Classes
<p className="text-primary">Primary text</p>
<p className="text-secondary">Secondary text</p>
<p className="text-muted">Muted text</p>
```

### 2.2 Button Usage

Implement buttons with consistent styling:

```tsx
// Primary Button (black background)
<button className="btn-primary">
  Generate Drawing
</button>

// Secondary Button (light gray background)
<button className="btn-secondary">
  Cancel
</button>

// Outline Button (transparent, blue border)
<button className="btn-outline">
  Learn More
</button>

// Link Button (text only)
<button className="btn-link">
  View Details
</button>

// Size variants
<button className="btn-primary btn-sm">Small</button>
<button className="btn-primary btn-lg">Large</button>
```

**CSS Classes Available**:
- `.btn-primary` - Black button, white text, shadow
- `.btn-secondary` - Light gray button, dark text, border
- `.btn-outline` - Transparent, blue border and text
- `.btn-link` - Transparent, blue text only
- `.btn-sm` - Smaller padding and font
- `.btn-lg` - Larger padding and font

### 2.3 Form Inputs

Style form fields consistently:

```tsx
<div className="form-group">
  <label htmlFor="name">Full Name</label>
  <input
    id="name"
    type="text"
    placeholder="Enter your name"
  />
</div>

<div className="form-group">
  <label htmlFor="email">Email Address</label>
  <input
    id="email"
    type="email"
    placeholder="your@email.com"
  />
</div>

<div className="form-group">
  <label htmlFor="message">Message</label>
  <textarea
    id="message"
    placeholder="Enter your message..."
  ></textarea>
</div>
```

**Default Styling**:
- Border: Light gray, 1px
- Padding: 0.75rem 1rem
- Border radius: 6px
- Focus: Blue outline, subtle blue shadow
- Placeholder: Muted gray text

### 2.4 Card Components

Use cards for grouped content:

```tsx
<div className="card">
  <div className="card-header">
    <h3>Drawing Details</h3>
  </div>
  
  <div className="card-body">
    <p>Your drawing parameters and options go here.</p>
  </div>
  
  <div className="card-footer">
    <button className="btn-primary">Save Drawing</button>
  </div>
</div>
```

**Card Features**:
- White background with subtle border
- Subtle shadow that elevates on hover
- Header: Top border, spaced content
- Body: Main content area
- Footer: Bottom border, action buttons

### 2.5 Layout & Spacing

Use the spacing system for consistent rhythm:

```tsx
{/* Spacing classes */}
<div className="p-4">Padding: 1rem</div>
<div className="m-6">Margin: 1.5rem</div>
<div className="gap-4">Gap: 1rem (flex/grid)</div>

{/* Common patterns */}
<div className="flex gap-3">
  <input type="text" />
  <button>Submit</button>
</div>

<div className="grid grid-cols-2 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

**Spacing Values** (4px base unit):
- `space-1`: 4px
- `space-2`: 8px
- `space-3`: 12px
- `space-4`: 16px
- `space-6`: 24px
- `space-8`: 32px
- `space-12`: 48px

---

## 3. COLOR USAGE

### 3.1 Color Palette

```css
/* Primary */
--raven-black: #000000      /* Headers, primary text */
--raven-white: #FFFFFF      /* Backgrounds, content areas */

/* Grays (9-step scale) */
--raven-gray-50: #f9f9f9    /* Lightest background */
--raven-gray-100: #f5f5f5   /* Light gray background */
--raven-gray-200: #e0e0e0   /* Borders, dividers */
--raven-gray-300: #d0d0d0   /* Secondary borders */
--raven-gray-600: #666666   /* Secondary text */
--raven-gray-800: #1a1a1a   /* Dark variant of black */

/* Accents */
--raven-accent-gold: #d4af37      /* Premium touches */
--raven-accent-blue: #0066cc      /* Links, CTAs */
--raven-accent-blue-hover: #005bb3 /* Link hover state */

/* Functional */
--raven-success: #4CAF50    /* Success messages */
--raven-warning: #FF9800    /* Warnings */
--raven-error: #F44336      /* Errors */
--raven-info: #2196F3       /* Information */
```

### 3.2 Color Usage in Components

```tsx
{/* Text colors */}
<p className="text-raven-black">Primary text</p>
<p className="text-raven-gray-600">Secondary text</p>
<p className="text-raven-gray-800">Dark text variant</p>

{/* Backgrounds */}
<div className="bg-raven-white">White background</div>
<div className="bg-raven-gray-100">Light gray background</div>
<div className="bg-raven-gray-50">Lightest background</div>

{/* Borders */}
<div className="border border-raven-gray-200">Subtle border</div>
<div className="border-raven-gray-300">Darker border</div>

{/* Accents */}
<a href="#" className="text-raven-accent-blue">Link text</a>
<span className="text-raven-accent-gold">Premium text</span>

{/* Functional colors */}
<p className="text-raven-success">Success message</p>
<p className="text-raven-error">Error message</p>
```

---

## 4. RESPONSIVE DESIGN

The design system includes responsive breakpoints:

```tsx
{/* Mobile-first approach */}
<div className="
  text-base        /* 16px on mobile */
  md:text-lg       /* 18px on tablet */
  lg:text-xl       /* 20px on desktop */
">
  Responsive text
</div>

<div className="
  grid grid-cols-1  /* 1 column on mobile */
  md:grid-cols-2    /* 2 columns on tablet */
  lg:grid-cols-4    /* 4 columns on desktop */
  gap-4
">
  {/* Grid items */}
</div>
```

**Breakpoints**:
- Mobile: < 640px
- Tablet (sm): ≥ 640px
- Tablet (md): ≥ 768px
- Laptop (lg): ≥ 1024px
- Desktop (xl): ≥ 1280px

---

## 5. TRANSITIONS & INTERACTIONS

### 5.1 Hover Effects

```tsx
{/* Button hover with elevation */}
<button className="btn-primary">
  Create Drawing
</button>
{/* Automatically elevates on hover */}

{/* Card hover */}
<div className="card">
  {/* Automatically elevates with shadow on hover */}
</div>

{/* Link hover */}
<a href="#" className="text-raven-accent-blue">
  Link
</a>
{/* Automatically changes color and underlines on hover */}
```

### 5.2 Custom Transitions

```tsx
{/* Apply transition classes */}
<div className="transition-default">
  Content with 200ms transition
</div>

<div className="transition-fast">
  Content with 100ms transition
</div>

<div className="transition-slow">
  Content with 300ms transition
</div>
```

---

## 6. ACCESSIBILITY

The design system includes accessibility features:

### 6.1 Focus States

All interactive elements have visible focus states:

```tsx
{/* Automatically styled for keyboard navigation */}
<button>Click me</button>     {/* Blue focus ring */}
<a href="#">Link</a>           {/* Blue focus ring */}
<input type="text" />          {/* Blue focus box-shadow */}
```

### 6.2 Semantic HTML

Use proper semantic elements:

```tsx
{/* Good */}
<header>
  <nav>Navigation</nav>
</header>
<main>
  <section>Content</section>
</main>
<footer>Footer</footer>

{/* Label form inputs */}
<label htmlFor="email">Email</label>
<input id="email" type="email" />
```

### 6.3 ARIA Attributes

```tsx
{/* Use ARIA for complex components */}
<div role="button" aria-pressed="false">
  Interactive element
</div>

<div role="alert">
  Important message
</div>
```

---

## 7. IMPLEMENTATION CHECKLIST

- [ ] **Import raven-global.css** in `main.tsx`
- [ ] **Verify Tailwind config** has Raven color palette
- [ ] **Update SalesPresentation.tsx** to use Raven components
- [ ] **Replace colors** from old palette to new Raven palette
- [ ] **Update buttons** to use `.btn-primary`, `.btn-secondary` classes
- [ ] **Style forms** with `.form-group` and standard input styling
- [ ] **Apply cards** to grouped content areas
- [ ] **Update typography** to match Raven hierarchy
- [ ] **Test responsive design** at mobile, tablet, desktop breakpoints
- [ ] **Verify focus states** for accessibility
- [ ] **Check color contrast** for WCAG AA compliance
- [ ] **Test on real devices** (phone, tablet, laptop)

---

## 8. TROUBLESHOOTING

### Problem: Colors not showing

**Solution**: Ensure `raven-global.css` is imported in `main.tsx` before other styles.

### Problem: Buttons not styled correctly

**Solution**: Use class names like `btn-primary`, `btn-secondary`, etc. Don't use Tailwind bg classes on buttons.

### Problem: Form inputs look wrong

**Solution**: Remove any custom input styles - the global CSS handles all input styling.

### Problem: Spacing is inconsistent

**Solution**: Use Tailwind spacing classes (`p-4`, `m-6`, `gap-3`, etc.) based on the 4px grid.

### Problem: Colors look slightly different

**Solution**: Clear browser cache (Ctrl+Shift+Delete) and rebuild the app (`npm run dev`).

---

## 9. NEXT STEPS

1. **Apply to Current Components**
   - Update `SalesPresentation.tsx` to use Raven styling
   - Replace all custom styles with design system classes

2. **Create Brand Components**
   - Header component with navigation
   - Footer component with contact info
   - Sidebar for parameters
   - Preview panel for drawings

3. **Implement Features**
   - Drawing parameter controls
   - Drawing preview and generation
   - PDF export functionality
   - Presentation mode

4. **Testing**
   - Visual regression testing
   - Responsive design testing
   - Accessibility testing with WAVE or Axe
   - Browser compatibility testing

5. **Deployment**
   - Build optimized production version
   - Set up deployment pipeline
   - Configure CDN and caching
   - Monitor performance metrics

---

## 10. COLOR HEX REFERENCE

```
Primary:
  Black:          #000000
  White:          #FFFFFF
  Dark Gray:      #1a1a1a
  Light Gray:     #f5f5f5
  Border Gray:    #e0e0e0

Accents:
  Gold:           #d4af37
  Blue:           #0066cc
  Blue Hover:     #005bb3

Text:
  Primary:        #000000
  Secondary:      #666666
  Muted:          #999999
  Light:          #f5f5f5

Functional:
  Success:        #4CAF50
  Warning:        #FF9800
  Error:          #F44336
  Info:           #2196F3
```

---

## 11. FONTS

- **Heading Font**: System font stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue'`)
- **Body Font**: Same system font stack for consistency
- **Monospace**: `Monaco`, `Menlo`, `Ubuntu Mono`

---

## Final Status

✅ **Design System Complete**
✅ **Tailwind Config Updated**
✅ **Global Styles Created**
✅ **Component Guidelines Documented**
✅ **Ready for Implementation**

Your Raven Shop Drawing web app is now ready to be styled with the official Raven Custom Glass design system!
