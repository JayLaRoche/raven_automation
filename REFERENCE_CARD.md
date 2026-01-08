# RAVEN DESIGN SYSTEM - REFERENCE CARD

Quick visual reference for the Raven Shop Drawing Web App design system.

---

## 🎨 COLOR PALETTE

```
PRIMARY          ACCENTS           FUNCTIONAL
████ #000000     ████ #0066cc      ✓ #4CAF50 Success
████ #FFFFFF     ████ #d4af37      ✗ #F44336 Error
                                    ⚠ #FF9800 Warning
GRAYS (9-step)                       ⓘ #2196F3 Info
████ #f9f9f9     Lightest
████ #f5f5f5     
████ #e0e0e0     Borders
████ #d0d0d0     
████ #b0b0b0     
████ #808080     
████ #666666     Secondary text
████ #4d4d4d     
████ #1a1a1a     Dark variant
```

---

## 📏 TYPOGRAPHY SCALE

```
h1   48px   Bold    █████████████████  Major page headings
h2   30px   Bold    ██████████████     Section titles
h3   24px   Bold    ███████████        Subsection titles
h4   20px   Bold    ██████████         Minor headings
lg   18px   Regular ████████           Large body text
base 16px   Regular ████               Standard body text
sm   14px   Regular ███                Small text
xs   12px   Regular ██                 Tiny labels
```

---

## 🎨 BUTTON STYLES

```
PRIMARY BUTTON
┌─────────────────────────────┐
│ Generate Drawing            │  ← Black background
│ (hover: #1a1a1a, -2px up)   │  ← White text
└─────────────────────────────┘  ← 6px radius, shadow

SECONDARY BUTTON
┌─────────────────────────────┐
│ Cancel                      │  ← Light gray background
│ (hover: #efefef)            │  ← Black text, border
└─────────────────────────────┘

OUTLINE BUTTON
┌─────────────────────────────┐
│ Learn More                  │  ← Transparent, blue border
│ (hover: light blue bg)      │  ← Blue text
└─────────────────────────────┘

LINK BUTTON
Learn More → Blue text, underline on hover
```

---

## 📐 SPACING SCALE (4px base unit)

```
4px   space-1   ▮                      (label spacing)
8px   space-2   ▮▮                     (small gaps)
12px  space-3   ▮▮▮                    (form gaps)
16px  space-4   ▮▮▮▮                   (standard padding)
20px  space-5   ▮▮▮▮▮                  (larger spacing)
24px  space-6   ▮▮▮▮▮▮                 (card padding)
32px  space-8   ▮▮▮▮▮▮▮▮               (section padding)
48px  space-12  ▮▮▮▮▮▮▮▮▮▮▮▮           (large sections)
```

---

## 🎯 RESPONSIVE BREAKPOINTS

```
Mobile          Tablet          Laptop          Desktop
< 640px         640-768px       768-1024px      1024px+

┌──────┐  ┌────────────┐  ┌──────────────┐  ┌────────────────┐
│      │  │            │  │              │  │                │
│ ONE  │  │   TWO COLS │  │  THREE COLS  │  │   FOUR COLS    │
│ COL  │  │            │  │              │  │                │
└──────┘  └────────────┘  └──────────────┘  └────────────────┘
```

---

## 📝 FORM ELEMENTS

```
INPUT FIELD
┌─────────────────────────────────────┐
│ Enter your name                      │  ← Light gray border
│                                      │  ← Focus: blue border + shadow
└─────────────────────────────────────┘

LABEL
Name * ← Required indicator in red

SELECT BOX
┌─────────────────────────┐
│ Choose an option     ▼  │  ← Dropdown arrow
└─────────────────────────┘

TEXTAREA
┌─────────────────────────┐
│ Enter your message...    │
│                          │
│                          │
└─────────────────────────┘
```

---

## 🎴 CARD COMPONENT

```
┌─────────────────────────────────────┐
│ Card Header                         │  ← Border bottom
├─────────────────────────────────────┤
│ Card Body Content                   │
│ This is the main content area       │
│                                     │
├─────────────────────────────────────┤
│  [Cancel Button]  [Save Button]    │  ← Card Footer
└─────────────────────────────────────┘
   ▲
   └─ White background, 1px gray border, 8px radius
```

---

## 🏠 HEADER & FOOTER

```
HEADER
═════════════════════════════════════
│ Raven   │ Link  Link  Link  [Button] │  ← White bg, sticky
═════════════════════════════════════

FOOTER
═════════════════════════════════════
│ Contact Info                        │
│ (702) 577-1003                      │  ← Black background
│ 9960 W Cheyenne Ave, Suite 140      │  ← Gold links
│ Las Vegas NV 89129                  │
═════════════════════════════════════
```

---

## 🔄 TRANSITIONS

```
Fast (100ms)     ■═══════════════════
Standard (200ms) ■════════════════════
Slow (300ms)     ■═════════════════════

Used for:
• Color changes    200ms ease-smooth
• Shadow elevation 200ms ease-smooth
• Scale/transform  200ms ease-smooth
• Opacity/fade     200ms ease-smooth
```

---

## ♿ ACCESSIBILITY

```
FOCUS STATES
┌─────────────────────────────────────┐
│ ◀─ 2px blue outline, 2px offset     │  
│ All interactive elements             │
└─────────────────────────────────────┘

KEYBOARD NAVIGATION
Tab     → Move to next element
Shift+Tab → Move to previous element
Enter   → Activate button/link
Space   → Toggle checkbox

COLOR CONTRAST
Black on White    21:1  ✓✓ AAA (Excellent)
Gray on White     4.5:1 ✓  AA (Good)
Blue text         4.5:1 ✓  AA (Good)
```

---

## 📊 COMMON CLASS NAMES

```
BUTTONS
.btn-primary        ← Black button, white text
.btn-secondary      ← Gray button, dark text
.btn-outline        ← Transparent, blue border
.btn-link           ← Text link style
.btn-sm / .btn-lg   ← Size variants

TEXT
.text-primary       ← Black text
.text-secondary     ← Gray text
.text-muted         ← Very gray text
.text-raven-accent-blue ← Blue text

BACKGROUNDS
.bg-raven-light-gray    ← Light background
.bg-raven-dark-gray     ← Dark background

SPACING
.p-4   .m-6   .gap-3   .px-6   .py-4

COMPONENTS
.card .card-header .card-body .card-footer
.form-group
```

---

## 🎬 HOVER EFFECTS

```
Button
┌──────────────┐      ┌──────────────┐
│ Click        │  →   │ Click ▲      │  ← Dark, elevated 2px
└──────────────┘      └──────────────┘

Card
┌──────────────────────────────┐      ┌──────────────────────────┐
│ Content                      │  →   │ Content                │  ← Shadow, -2px
└──────────────────────────────┘      └──────────────────────────┘

Link
Click me  →  Click me (colored & underlined)

Input
[Input field] → [Input field] (blue border, blue shadow)
```

---

## 📱 MOBILE-FIRST APPROACH

```
Start small (mobile), then add:

<div className="
  text-base              /* 16px on mobile */
  md:text-lg             /* 18px on tablet+ */
  lg:text-xl             /* 20px on desktop+ */
  grid grid-cols-1       /* 1 column on mobile */
  md:grid-cols-2         /* 2 columns on tablet+ */
  lg:grid-cols-4         /* 4 columns on desktop+ */
">
  Content
</div>
```

---

## 🎁 SHADOW LEVELS

```
None     ▁▁▁▁▁▁▁▁▁▁▁▁▁
Small    ▂▂▂▂▂▂▂▂▂▂▂▂▂
Medium   ▃▃▃▃▃▃▃▃▃▃▃▃▃
Large    ▄▄▄▄▄▄▄▄▄▄▄▄▄
XL       ▅▅▅▅▅▅▅▅▅▅▅▅▅
Hover    ▆▆▆▆▆▆▆▆▆▆▆▆▆
```

---

## 🎨 BORDER RADIUS

```
none   ▭▭▭▭▭▭▭▭▭▭▭▭▭  (0px)
sm     ⬜⬜⬜⬜⬜⬜⬜⬜⬜  (4px)
md     ⬜⬜⬜⬜⬜⬜⬜⬜⬜  (6px) ← Primary
lg     ⬜⬜⬜⬜⬜⬜⬜⬜⬜  (8px)
xl     ⬜⬜⬜⬜⬜⬜⬜⬜⬜  (12px)
full   ⭕⭕⭕⭕⭕⭕⭕⭕⭕  (circle)
```

---

## ✨ QUICK COPY-PASTE

**Black Button**:
```tsx
<button className="btn-primary">Click</button>
```

**Form Group**:
```tsx
<div className="form-group">
  <label htmlFor="name">Name</label>
  <input id="name" type="text" />
</div>
```

**Card**:
```tsx
<div className="card">
  <div className="card-header"><h3>Title</h3></div>
  <div className="card-body">Content</div>
</div>
```

**Responsive Grid**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Items */}
</div>
```

---

## 🎯 IMPLEMENTATION CHECKLIST

- [ ] Import raven-global.css in main.tsx
- [ ] Use .btn-primary for main buttons
- [ ] Use .text-secondary for secondary text
- [ ] Wrap forms in .form-group
- [ ] Use .card for containers
- [ ] Use Tailwind spacing classes (p-4, m-6, gap-3)
- [ ] Test responsive on mobile/tablet/desktop
- [ ] Verify focus states work
- [ ] Check color contrast
- [ ] Test on real devices

---

## 📚 FOR MORE INFORMATION

- **Quick Lookup**: RAVEN_QUICK_REFERENCE.md
- **Implementation Guide**: RAVEN_DESIGN_IMPLEMENTATION.md
- **Complete Spec**: RAVEN_DESIGN_TOKENS.md
- **Getting Started**: GETTING_STARTED.md

---

**Print this card for quick reference while coding!** 🖨️

---

Design System Version: 1.0  
Last Updated: December 27, 2024  
Status: ✅ Ready to Use
