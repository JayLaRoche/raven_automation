# Raven Shop Drawing Web App - Design System Implementation Guide

## Overview

This guide walks through implementing the **Raven Custom Glass** design system across the shop drawing web application to match the brand identity of ravencustomglass.com.

---

## FILES CREATED

### 1. **DESIGN_TOKENS_EXTRACTED.md**
- Comprehensive design token documentation
- Color palette with hex codes
- Typography scale and font families
- Spacing system and measurements
- Component styling specifications
- Accessibility standards

### 2. **tailwind.config.js**
- Custom Tailwind CSS configuration
- Extended color palette (Raven brand colors)
- Font families and sizes
- Spacing scale (4px base unit)
- Border radius and shadow definitions
- Transition and animation settings

### 3. **RavenComponents.tsx**
- Reusable UI components with Raven styling:
  - **Button** (multiple variants: primary, secondary, tertiary, danger, success)
  - **Input** (with error states and labels)
  - **Card** (elevated and flat options)
  - **Header** (navigation bar with logo)
  - **Footer** (with company info and links)
  - **Section** (content container with background options)
  - **Badge** (status labels and tags)
  - **Divider** (visual separators)
  - **Skeleton** (loading placeholders)

### 4. **raven-global.css**
- Global CSS styles
- HTML element resets and defaults
- Typography hierarchy
- Form element styling
- Animation keyframes
- Responsive utilities
- Print and accessibility styles

---

## IMPLEMENTATION STEPS

### Step 1: Import Global Styles

Add the global CSS to your main React entry point:

**File: `frontend/src/main.tsx` or `frontend/src/index.tsx`**

```tsx
import './styles/raven-global.css'
import App from './App.tsx'

// Rest of your app...
```

### Step 2: Update Tailwind Config

Replace your existing `tailwind.config.js` with the new configuration:

```bash
# Copy the new config
cp DESIGN_TOKENS_EXTRACTED.md to your root directory (for reference)
# Update your tailwind.config.js with the extended theme
```

### Step 3: Import Components

Use the Raven components throughout your application:

**Example: Header Component**

```tsx
import { Header, Button } from '@/components/ui/RavenComponents'

export function App() {
  return (
    <>
      <Header
        logoText="Raven's Design Sandbox"
        navLinks={[
          { id: 1, label: 'Home', href: '/' },
          { id: 2, label: 'Documentation', href: '/docs' },
          { id: 3, label: 'About', href: '/about' },
        ]}
        ctaButton="Export PDF"
      />
      <main>
        {/* Your content */}
      </main>
    </>
  )
}
```

**Example: Drawing Page with Components**

```tsx
import {
  Button,
  Input,
  Card,
  Section,
  Badge,
  Footer,
} from '@/components/ui/RavenComponents'

export function DrawingPage() {
  return (
    <>
      <Section title="Shop Drawing Parameters" subtitle="Configure your window">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Input
            label="Series"
            type="number"
            placeholder="86"
            defaultValue={86}
          />
          
          <Input
            label="Width (inches)"
            type="number"
            placeholder="36"
            defaultValue={36}
          />
          
          <Input
            label="Height (inches)"
            type="number"
            placeholder="48"
            defaultValue={48}
          />
        </div>
        
        <div className="mt-6 flex gap-4">
          <Button variant="primary">
            Export PDF
          </Button>
          
          <Button variant="secondary">
            Save Configuration
          </Button>
        </div>
      </Section>
      
      <Section background="gray" title="Drawing Preview">
        <Card elevated className="mb-6">
          {/* Your canvas component */}
        </Card>
      </Section>
      
      <Footer />
    </>
  )
}
```

### Step 4: Update SalesPresentation Component

Replace the styling in `frontend/src/components/sales/SalesPresentation.tsx`:

```tsx
import {
  Header,
  Button,
  Card,
  Section,
  Footer,
} from '@/components/ui/RavenComponents'

export function SalesPresentation() {
  return (
    <>
      <Header
        logoText="Raven's Design Sandbox"
        ctaButton="Full Screen"
      />
      
      <Section title="CAD Drawing Generator">
        <div className="grid grid-cols-3 gap-6">
          {/* Drawing controls and canvas */}
        </div>
      </Section>
      
      <Footer
        companyName="Raven Custom Glass"
        address="9960 W Cheyenne Ave, Suite 140, Las Vegas NV 89129"
        phone="(702) 577-1003"
        links={[
          {
            title: 'Product',
            items: [
              { id: 1, label: 'Doors', href: '#' },
              { id: 2, label: 'Windows', href: '#' },
              { id: 3, label: 'Pricing', href: '#' },
            ],
          },
          {
            title: 'Company',
            items: [
              { id: 1, label: 'About', href: '#' },
              { id: 2, label: 'Blog', href: '#' },
              { id: 3, label: 'Contact', href: '#' },
            ],
          },
        ]}
      />
    </>
  )
}
```

---

## COLOR USAGE GUIDE

### Using Tailwind Color Classes

All colors use the `raven-` prefix:

```tsx
// Text colors
className="text-raven-black"
className="text-raven-gray-600"
className="text-raven-gray-900"

// Background colors
className="bg-raven-white"
className="bg-raven-gray-50"
className="bg-raven-gray-100"

// Border colors
className="border-raven-gray-200"
className="border-raven-gray-300"

// State colors
className="bg-raven-success"   // Green
className="bg-raven-error"     // Red
className="bg-raven-warning"   // Yellow
className="bg-raven-info"      // Blue
```

### Color Decision Matrix

| Use Case | Color | Class |
|----------|-------|-------|
| Primary text | Gray 900 | `text-raven-gray-900` |
| Secondary text | Gray 500 | `text-raven-gray-500` |
| Muted/Disabled | Gray 400 | `text-raven-gray-400` |
| Headers | Black | `text-raven-black` |
| Links | Black | `text-raven-black` |
| Link hover | Gray 700 | `hover:text-raven-gray-700` |
| Backgrounds | White | `bg-raven-white` |
| Alt backgrounds | Gray 50 | `bg-raven-gray-50` |
| Borders | Gray 200 | `border-raven-gray-200` |
| Hover borders | Gray 300 | `hover:border-raven-gray-300` |
| Buttons | Black bg | `bg-raven-black text-raven-white` |
| Success states | Green | `bg-raven-success` |
| Error states | Red | `bg-raven-error` |
| Warnings | Yellow | `bg-raven-warning` |

---

## TYPOGRAPHY USAGE GUIDE

### Heading Hierarchy

```tsx
// H1 - Page titles, main headlines
<h1>Shop Drawing Generator</h1>
// Result: 36px, bold, -1px letter spacing

// H2 - Section titles
<h2>Configuration</h2>
// Result: 30px, bold, -0.5px letter spacing

// H3 - Subsection titles
<h3>Window Specifications</h3>
// Result: 24px, semibold

// H4 - Card titles
<h4>Drawing Information</h4>
// Result: 20px, semibold

// Body text - Standard content
<p>This is the main content text...</p>
// Result: 16px, regular, 1.5 line height

// Small text - Captions, helper text
<span className="text-sm text-raven-gray-500">
  Helper text or caption
</span>
// Result: 14px, gray 500
```

### Font Weight Usage

```tsx
// Regular weight (400) - body text
<p className="font-normal">Regular body text</p>

// Medium weight (500) - emphasis
<p className="font-medium">Important text</p>

// Semibold (600) - subheadings, button text
<h4 className="font-semibold">Section Title</h4>

// Bold (700) - main headings
<h1 className="font-bold">Page Title</h1>
```

---

## SPACING GUIDE

### Padding Examples

```tsx
// Small components
className="px-3 py-2"      // 12px horizontal, 8px vertical

// Standard components
className="px-4 py-3"      // 16px horizontal, 12px vertical

// Large components
className="px-6 py-4"      // 24px horizontal, 16px vertical

// Card padding
<Card className="p-6">     // 24px padding all sides

// Section padding
<Section className="px-6 py-12">  // 24px horizontal, 48px vertical
```

### Gap Examples

```tsx
// Tight spacing (small components)
<div className="gap-2">    // 8px gap

// Normal spacing (most use)
<div className="gap-4">    // 16px gap

// Spacious spacing (large sections)
<div className="gap-6">    // 24px gap
```

---

## BUTTON VARIANTS GUIDE

### Primary Button
Use for main actions (submit, save, export)

```tsx
<Button variant="primary">
  Export PDF
</Button>
```
Styling: Black background, white text, shadow on hover

### Secondary Button
Use for alternative actions (cancel, reset, options)

```tsx
<Button variant="secondary">
  Cancel
</Button>
```
Styling: Transparent background, black border, hover fills with gray

### Tertiary Button
Use for less important actions (help, learn more, skip)

```tsx
<Button variant="tertiary">
  Learn More
</Button>
```
Styling: Transparent, text only, hover underline

### Danger Button
Use for destructive actions (delete, remove, reset all)

```tsx
<Button variant="danger">
  Delete Configuration
</Button>
```
Styling: Red background, white text, shadow

### Success Button
Use for confirmatory actions (complete, confirm, enable)

```tsx
<Button variant="success">
  Confirm Drawing
</Button>
```
Styling: Green background, white text, shadow

---

## FORM INPUT USAGE

### Basic Text Input

```tsx
<Input
  label="Window Width"
  type="text"
  placeholder="Enter width in inches"
  defaultValue="36"
/>
```

### Input with Error

```tsx
<Input
  label="Series Number"
  type="number"
  error="Series must be between 50 and 200"
/>
```

### Disabled Input

```tsx
<Input
  label="Locked Field"
  type="text"
  disabled
  value="This cannot be changed"
/>
```

---

## CARD COMPONENT USAGE

### Simple Card

```tsx
<Card>
  <h3>Specifications</h3>
  <p>Details here...</p>
</Card>
```

### Elevated Card (with hover effect)

```tsx
<Card elevated>
  <h3>Interactive Card</h3>
  <p>This card has hover effect and shadow</p>
</Card>
```

---

## FORM LAYOUT BEST PRACTICES

### Single Column Form

```tsx
<form className="space-y-6 max-w-md">
  <Input label="Name" type="text" />
  <Input label="Email" type="email" />
  <Input label="Message" type="textarea" />
  <Button variant="primary">Submit</Button>
</form>
```

### Two Column Form

```tsx
<form className="space-y-6">
  <div className="grid grid-cols-2 gap-4">
    <Input label="First Name" type="text" />
    <Input label="Last Name" type="text" />
  </div>
  <Input label="Email" type="email" />
  <Button variant="primary">Submit</Button>
</form>
```

### Three Column Form (Drawing Parameters)

```tsx
<form className="grid grid-cols-3 gap-4">
  <Input label="Series" type="number" />
  <Input label="Width" type="number" />
  <Input label="Height" type="number" />
  <Button variant="primary" className="col-span-3">
    Generate Drawing
  </Button>
</form>
```

---

## RESPONSIVE DESIGN

All components are mobile-first and responsive:

```tsx
// Stack on mobile, grid on tablet+
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card>Item 1</Card>
  <Card>Item 2</Card>
  <Card>Item 3</Card>
</div>

// Hide on mobile, show on tablet+
<nav className="hidden md:flex gap-8">
  {/* Navigation links */}
</nav>

// Text sizes responsive
<h1 className="text-2xl md:text-3xl lg:text-4xl">
  Responsive Heading
</h1>
```

---

## ACCESSIBILITY CHECKLIST

✅ **Focus States** - All interactive elements have visible focus rings
✅ **Color Contrast** - Text meets WCAG AA standards (4.5:1)
✅ **Touch Targets** - Buttons/inputs are 44px minimum
✅ **Labels** - All form inputs have associated labels
✅ **Semantic HTML** - Using proper heading hierarchy
✅ **Keyboard Navigation** - All interactive elements keyboard accessible
✅ **ARIA** - Using ARIA attributes where needed
✅ **Motion** - Respects `prefers-reduced-motion`

---

## TESTING & VERIFICATION

### Visual Consistency Check

1. Open ravencustomglass.com in one browser tab
2. Open your app in another tab
3. Compare side-by-side:
   - [ ] Colors match exactly
   - [ ] Font sizes are proportional
   - [ ] Spacing feels consistent
   - [ ] Button styles match
   - [ ] Border radius matches
   - [ ] Shadows match

### Responsive Testing

- [ ] Test on mobile (320px)
- [ ] Test on tablet (768px)
- [ ] Test on desktop (1024px+)
- [ ] Test navigation responsiveness
- [ ] Test form inputs on touch devices

### Browser Compatibility

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

---

## NEXT STEPS

1. **Import the global CSS** in your main React file
2. **Replace buttons** in existing components with `Button` component
3. **Refactor forms** to use `Input` and `Card` components
4. **Update page layout** to use `Section` and `Header`/`Footer`
5. **Test** on all screen sizes and browsers
6. **Verify** colors and typography match reference site

---

## SUPPORT

For questions about specific design tokens or component usage, refer to:
- **DESIGN_TOKENS_EXTRACTED.md** - Complete design specification
- **RavenComponents.tsx** - Component source code and props
- **raven-global.css** - Global styling reference
- **tailwind.config.js** - Tailwind configuration values

Your shop drawing app will now match the professional, clean aesthetic of ravencustomglass.com! 🎨
