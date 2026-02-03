# Raven Custom Glass Design System - Extracted

## Design Extraction from ravencustomglass.com

### COLOR PALETTE

**Primary Colors:**
```css
--raven-black: #000000;        /* Primary brand color - headings, text */
--raven-white: #FFFFFF;        /* Page backgrounds, text on dark */
--raven-dark-gray: #1a1a1a;    /* Secondary dark shade */
--raven-light-gray: #f5f5f5;   /* Light backgrounds, subtle sections */
--raven-border-gray: #e0e0e0;  /* Borders and dividers */
```

**Accent Colors:**
```css
--raven-accent-gold: #d4af37;  /* Premium accent/highlights (Raven brand accent) */
--raven-accent-blue: #0066cc;  /* Links, CTAs */
--raven-accent-hover: #005bb3; /* Link hover state */
```

**Text Colors:**
```css
--raven-text-primary: #000000;     /* Main text, headings */
--raven-text-secondary: #666666;   /* Secondary text, descriptions */
--raven-text-muted: #999999;       /* Tertiary text, metadata */
--raven-text-light: #f5f5f5;       /* Text on dark backgrounds */
```

**Functional Colors:**
```css
--raven-success: #4CAF50;      /* Success states */
--raven-warning: #FF9800;      /* Warning states */
--raven-error: #F44336;        /* Error states */
--raven-info: #2196F3;         /* Info messages */
```

---

### TYPOGRAPHY

**Font Families:**
```css
/* Primary Font Family: System/Web-safe stack */
--font-heading: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
--font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
--font-mono: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;

/* Alternative Premium: If using Google Fonts */
/* Recommended: Playfair Display (headings), Inter (body) - matching modern luxury brands */
```

**Font Weights:**
```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

**Type Scale (px to rem conversion):**
```css
/* Base: 16px = 1rem */
--text-xs:   0.75rem;   /* 12px - small labels, captions */
--text-sm:   0.875rem;  /* 14px - small text, secondary */
--text-base: 1rem;      /* 16px - body text, standard */
--text-lg:   1.125rem;  /* 18px - larger body, emphasis */
--text-xl:   1.25rem;   /* 20px - subheadings */
--text-2xl:  1.5rem;    /* 24px - section titles */
--text-3xl:  1.875rem;  /* 30px - page headings */
--text-4xl:  2.25rem;   /* 36px - major headings */
--text-5xl:  3rem;      /* 48px - hero headings */
```

**Line Heights:**
```css
--line-tight:   1.2;   /* Headings */
--line-normal:  1.5;   /* Body text */
--line-relaxed: 1.75;  /* Large text blocks */
--line-loose:   2;     /* Very loose spacing */
```

**Letter Spacing:**
```css
--tracking-tight:  -0.02em;
--tracking-normal: 0;
--tracking-wide:   0.025em;
--tracking-wider:  0.05em;
```

---

### SPACING SYSTEM

**Base Unit: 4px grid**
```css
--space-0:    0;
--space-1:    0.25rem;  /* 4px */
--space-2:    0.5rem;   /* 8px */
--space-3:    0.75rem;  /* 12px */
--space-4:    1rem;     /* 16px - base padding/margin */
--space-5:    1.25rem;  /* 20px */
--space-6:    1.5rem;   /* 24px */
--space-7:    1.75rem;  /* 28px */
--space-8:    2rem;     /* 32px */
--space-10:   2.5rem;   /* 40px */
--space-12:   3rem;     /* 48px */
--space-14:   3.5rem;   /* 56px */
--space-16:   4rem;     /* 64px */
--space-20:   5rem;     /* 80px */
--space-24:   6rem;     /* 96px */
```

---

### BORDER RADIUS

```css
--radius-none: 0;
--radius-sm:   0.25rem;  /* 4px */
--radius-md:   0.375rem; /* 6px */
--radius-lg:   0.5rem;   /* 8px - primary radius */
--radius-xl:   0.75rem;  /* 12px */
--radius-2xl:  1rem;     /* 16px */
--radius-full: 9999px;   /* Full circle/pill */
```

**Common Usage:**
- Buttons: 6-8px
- Cards/Containers: 8px
- Inputs: 6px
- Images: 0-8px

---

### SHADOWS

```css
--shadow-none:   none;
--shadow-sm:     0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md:     0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg:     0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl:     0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl:    0 25px 50px -12px rgba(0, 0, 0, 0.25);

/* Hover elevation */
--shadow-hover:  0 10px 20px -5px rgba(0, 0, 0, 0.15);
```

---

### COMPONENT STYLES

#### Button Component

**Primary Button:**
```css
background-color: #000000;
color: #FFFFFF;
padding: 0.75rem 1.5rem;        /* 12px 24px */
border-radius: 6px;
border: none;
font-weight: 600;
font-size: 1rem;
cursor: pointer;
transition: all 200ms ease-in-out;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

/* Hover State */
background-color: #1a1a1a;
box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.15);
transform: translateY(-2px);
```

**Secondary Button:**
```css
background-color: #f5f5f5;
color: #000000;
border: 1px solid #e0e0e0;
padding: 0.75rem 1.5rem;
border-radius: 6px;
font-weight: 600;
font-size: 1rem;
transition: all 200ms ease-in-out;

/* Hover State */
background-color: #efefef;
border-color: #d0d0d0;
```

**Link/Tertiary Button:**
```css
background: transparent;
color: #0066cc;
padding: 0.5rem 1rem;
border: none;
cursor: pointer;
text-decoration: none;
transition: color 200ms ease-in-out;
font-weight: 500;

/* Hover State */
color: #005bb3;
text-decoration: underline;
```

#### Input Fields

```css
width: 100%;
padding: 0.75rem 1rem;
border: 1px solid #e0e0e0;
border-radius: 6px;
background-color: #ffffff;
color: #000000;
font-size: 1rem;
font-family: inherit;
transition: all 200ms ease-in-out;

/* Focus State */
outline: none;
border-color: #0066cc;
box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
background-color: #ffffff;

/* Disabled State */
background-color: #f5f5f5;
color: #999999;
cursor: not-allowed;
opacity: 0.6;

/* Placeholder */
placeholder-color: #999999;
```

#### Card Component

```css
background-color: #ffffff;
border: 1px solid #e0e0e0;
border-radius: 8px;
padding: 1.5rem;          /* 24px */
box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
transition: all 200ms ease-in-out;

/* Hover State */
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
transform: translateY(-2px);
border-color: #d0d0d0;
```

#### Header/Navigation

```css
background-color: #ffffff;
border-bottom: 1px solid #e0e0e0;
padding: 1rem 0;
position: sticky;
top: 0;
z-index: 1000;

/* Navigation Links */
color: #000000;
text-decoration: none;
padding: 0.5rem 1rem;
font-weight: 500;
transition: color 200ms ease-in-out;

/* Active/Hover State */
color: #0066cc;
border-bottom: 2px solid #0066cc;
```

---

### TRANSITIONS & ANIMATIONS

```css
/* Timing Functions */
--ease-linear:      cubic-bezier(0, 0, 1, 1);
--ease-in:          cubic-bezier(0.42, 0, 1, 1);
--ease-out:         cubic-bezier(0, 0, 0.58, 1);
--ease-in-out:      cubic-bezier(0.42, 0, 0.58, 1);
--ease-bounce:      cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Durations */
--duration-100:  100ms;
--duration-200:  200ms;
--duration-300:  300ms;
--duration-500:  500ms;
--duration-700:  700ms;
--duration-1000: 1000ms;

/* Standard Transitions */
--transition-fast:     all 100ms var(--ease-in-out);
--transition-default:  all 200ms var(--ease-in-out);
--transition-slow:     all 300ms var(--ease-in-out);
```

---

### BREAKPOINTS

```css
--breakpoint-xs: 320px;   /* Mobile */
--breakpoint-sm: 640px;   /* Tablet Small */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Laptop */
--breakpoint-xl: 1280px;  /* Desktop */
--breakpoint-2xl: 1536px; /* Large Desktop */
```

---

### CONTAINER SIZES

```css
--container-sm:  24rem;   /* 384px */
--container-md:  28rem;   /* 448px */
--container-lg:  32rem;   /* 512px */
--container-xl:  36rem;   /* 576px */
--container-2xl: 42rem;   /* 672px */
--container-3xl: 48rem;   /* 768px */
--container-4xl: 56rem;   /* 896px */
--container-5xl: 64rem;   /* 1024px */
--container-6xl: 72rem;   /* 1152px */
```

---

## BRAND VOICE & TONE

- **Professional**: Clean, modern, sophisticated
- **Accessible**: Clear hierarchy, readable typography
- **Minimal**: Less is more, white space is important
- **Premium**: Quality materials, attention to detail
- **Trustworthy**: Solid, dependable, reliable

## IMPLEMENTATION STATUS

✅ Colors extracted and defined
✅ Typography system created
✅ Spacing system documented
✅ Component styles specified
✅ Transitions and animations defined
✅ Ready for Tailwind CSS implementation

