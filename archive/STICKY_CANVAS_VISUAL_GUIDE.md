# Sticky Canvas Panel - Visual Layout Guide

## Overall Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         HEADER                                  │
│  Raven's Design Sandbox | Canvas | PDF | Generate | Export     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     MAIN CONTENT AREA                           │
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────────────────┐  │
│  │                  │        │   CANVAS (STICKY)            │  │
│  │   LEFT PANEL     │        │   ┌────────────────────────┐ │  │
│  │                  │        │   │                        │ │  │
│  │ Parameters:      │        │   │   TECHNICAL DRAWING    │ │  │
│  │ • Series        │◄──────►│   │   (Stays visible)      │ │  │
│  │ • Width/Height  │        │   │                        │ │  │
│  │ • Product Type  │        │   │                        │ │  │
│  │ • Glass Type    │        │   └────────────────────────┘ │  │
│  │ • Frame Color   │        │                              │  │
│  │ • Config        │        │  ↑                           │  │
│  │ • Notes         │        │  └─ Sticky: top: 20px       │  │
│  │                 │        │     max-height: 100vh - 40px│  │
│  │ (SCROLLS)       │        │                              │  │
│  │                 │        │                              │  │
│  └──────────────────┘        │  Internal scrollbar if      │  │
│                              │  content exceeds viewport   │  │
│  30% width          ◄────────►  70% width                  │  │
│  overflow-y: auto            │                              │  │
│  border-right                │  overflow-y: auto           │  │
│  (separates columns)         │  (internal only)            │  │
│                              │                              │  │
│                              └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

        ↓ User scrolls left panel ↓

┌─────────────────────────────────────────────────────────────────┐
│                     MAIN CONTENT AREA                           │
│                                                                 │
│  ┌──────────────────┐        ┌──────────────────────────────┐  │
│  │                  │        │   CANVAS (STAYS AT TOP)      │  │
│  │   LEFT PANEL     │        │   ┌────────────────────────┐ │  │
│  │                  │        │   │                        │ │  │
│  │ Parameters:      │        │   │   TECHNICAL DRAWING    │ │  │
│  │ • Series  ▲      │        │   │   (Still visible!)     │ │  │
│  │ • Width/Height   │  ◄────►│   │                        │ │  │
│  │ • Product Type   │ (30%)  │   │                        │ │  │
│  │ • Glass Type     │        │   └────────────────────────┘ │  │
│  │ • Frame Color ▲  │        │                              │  │
│  │ • Config        │        │  Sticky = always visible!    │  │
│  │ • Notes         │        │  (position: sticky; top: 20px) │  │
│  │                 │        │                              │  │
│  └──────────────────┘        │   70%  (right side)          │  │
│  Scrolling down...           │                              │  │
│                              └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Desktop View (>1024px)

```
┌───────────────────────────────────────────────────────────────────┐
│ Two-Column Layout                                                 │
│                                                                   │
│ ┌──────────────────────┐  ┌────────────────────────────────────┐ │
│ │ Left Panel (30%)     │  │ Right Panel (70%)                  │ │
│ │ • Parameters scroll  │  │ • Canvas STICKY                    │ │
│ │ • border-right       │  │ • Stays on screen                  │ │
│ │ • overflow-y: auto   │  │ • position: sticky; top: 20px      │ │
│ │                      │  │ • max-height: calc(100vh - 40px)   │ │
│ │ Fully scrollable     │  │ • Internal scroll if needed        │ │
│ │                      │  │ • align-items: flex-start         │ │
│ └──────────────────────┘  └────────────────────────────────────┘ │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Tablet View (1024px - 768px)

```
┌──────────────────────────────────────────────────┐
│ Single Column Layout                             │
│                                                  │
│ ┌──────────────────────────────────────────────┐│
│ │ Parameters Panel (100% width)                 ││
│ │                                               ││
│ │ • Series                                      ││
│ │ • Width/Height                                ││
│ │ • Product Type                                ││
│ │ • Glass Type                                  ││
│ │ • Frame Color                                 ││
│ │ • Configuration                               ││
│ │                                               ││
│ │ scroll down ↓                                  ││
│ └──────────────────────────────────────────────┘│
│                                                  │
│ ┌──────────────────────────────────────────────┐│
│ │ Canvas Panel (100% width)                     ││
│ │                                               ││
│ │ • Sticky DISABLED at this breakpoint          ││
│ │ • position: relative (normal flow)            ││
│ │ • overflow-y: visible (no internal scroll)   ││
│ │ • Canvas stays with content                   ││
│ │                                               ││
│ └──────────────────────────────────────────────┘│
│                                                  │
└──────────────────────────────────────────────────┘
```

## Mobile View (<768px)

```
┌──────────────────────────┐
│ Single Column - Mobile   │
│                          │
│ Parameters (full width)  │
│ ┌──────────────────────┐│
│ │ Series               ││
│ │ Width/Height         ││
│ │ Product Type         ││
│ │ Glass Type           ││
│ │ Frame Color          ││
│ │ ...                  ││
│ └──────────────────────┘│
│                          │
│ Canvas (full width)      │
│ ┌──────────────────────┐│
│ │ Technical Drawing    ││
│ │ (scrolls normally)   ││
│ │                      ││
│ │ No sticky effect     ││
│ │                      ││
│ └──────────────────────┘│
│                          │
└──────────────────────────┘
```

## CSS Positioning Flow

### How Sticky Positioning Works

```
PARENT (.rightPanel)
│
├─ Property: overflow-y: visible  ← CRITICAL (not auto/hidden)
├─ Property: display: flex        ← Flex container
├─ Property: align-items: flex-start  ← CRITICAL (required)
│
└─ CHILD (.canvasContainer)
   │
   ├─ Property: position: sticky  ← Creates sticky context
   ├─ Property: top: 20px         ← Sticky offset
   ├─ Property: max-height: calc(100vh - 40px)
   └─ Property: overflow-y: auto  ← Internal scrolling
      │
      └─ RESULT: Canvas sticks to viewport
         within parent bounds
```

### Scroll Behavior Diagram

```
Viewport (Browser Window)
┌─────────────────────────────────┐
│                                 │
│  ▲ 20px margin (top: 20px)      │
│  ▼                              │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │   STICKY CANVAS AREA      │  │
│  │   (position: sticky)      │  │
│  │                           │  │
│  │   ← Stays here when       │  │
│  │      scrolling            │  │
│  │                           │  │
│  └───────────────────────────┘  │
│  ▲ 20px margin (bottom)         │
│                                 │
└─────────────────────────────────┘

When scrolling DOWN:
┌─────────────────────────────────┐
│ [Parameters scroll under here] ← │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │   STICKY CANVAS AREA        │ │
│ │   (Remains visible!)        │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│ [More parameters below] ↓       │
│                                 │
└─────────────────────────────────┘
```

## Component Hierarchy

```
<SalesPresentation>
├─ Header (controls)
└─ <MainContent> (className="mainContent")
   │
   ├─ Canvas View (active)
   │  └─ <div className={styles.canvasViewLayout}>
   │     │
   │     ├─ <div className={styles.leftPanel}>
   │     │  └─ <SmartParameterPanel /> (scrolls)
   │     │
   │     └─ <div className={styles.rightPanel}>
   │        └─ <CanvasDrawingPreview>
   │           └─ <div className={styles.canvasContainer}>
   │              ├─ (STICKY ELEMENT!)
   │              ├─ top: 20px
   │              ├─ max-height: calc(100vh - 40px)
   │              └─ <div className={styles.canvasContent}>
   │                 └─ <canvas ref={canvasRef} />
   │
   └─ PDF View (hidden)
      └─ <DrawingPDFViewer />
```

## Scrolling Scenarios

### Scenario 1: Desktop - Scroll Left Panel
```
User scrolls parameters (left panel) down:
├─ Left panel: ↓ scrolls DOWN
├─ Right panel: ← does NOT scroll (overflow-y: visible)
└─ Canvas: ↓ STICKY (stays at top: 20px)
   
Result: Canvas always visible while viewing parameters
```

### Scenario 2: Desktop - Canvas Taller Than Viewport
```
Canvas content exceeds viewport height:
├─ Canvas container has overflow-y: auto
├─ User can scroll within the canvas area
└─ Canvas still sticks to top: 20px
   
Result: Internal scrollbar appears for canvas only
```

### Scenario 3: Tablet (≤1024px) - Switch to Single Column
```
Layout changes:
├─ grid-template-columns: 1fr (single column)
├─ .canvasContainer: position: relative (sticky disabled)
├─ Both panels scroll normally
└─ Canvas scrolls away with content
   
Result: More natural mobile-like experience
```

### Scenario 4: Mobile (≤768px) - Full Width Stack
```
Layout changes:
├─ grid-template-columns: 1fr
├─ Full width panels
├─ Parameters scroll past
├─ Canvas scrolls past
└─ Normal vertical scrolling
   
Result: Touch-friendly, no sticky complications
```

## CSS Module Class Names

```
CanvasDrawingPreview.module.css:
├─ .stickyWrapper        - Main component wrapper
├─ .canvasContainer      - STICKY element (position: sticky)
├─ .canvasContent        - Content wrapper (flex container)
├─ .canvas               - Canvas element with styling
└─ .debugInfo            - Debug information display

SalesPresentation.module.css:
├─ .canvasViewLayout     - Main grid container
├─ .leftPanel            - Parameters (30% width, scrolls)
├─ .rightPanel           - Canvas area (70% width, contains sticky)
├─ .mainContent          - Outer wrapper
├─ .canvasView           - Canvas view styles
└─ .pdfView              - PDF view styles
```

## Z-Index Stacking

```
z-index: 50    ← Floating Plan Panel (floating)
z-index: 40    ← Floating Plan Label
z-index: 10    ← Canvas Container (sticky)
z-index: 0     ← Parameters Panel (default)
```

## Key Takeaway

The sticky effect works by:
1. ✅ Parent has `overflow-y: visible` (no scroll container)
2. ✅ Parent has `align-items: flex-start` (sticky positioning context)
3. ✅ Child has `position: sticky; top: 20px` (sticky behavior)
4. ✅ Child has `max-height: calc(100vh - 40px)` (respect viewport)

This combination creates the perfect Wayfair-style panel effect!

---

**Visual Guide Version**: 1.0
**Created**: January 6, 2026
