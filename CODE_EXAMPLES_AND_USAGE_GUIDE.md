# Code Examples & Usage Guide

## Quick Code References

### 1. Using Presentation Mode in Parent Component

```typescript
// SalesPresentation.tsx
import { useState } from 'react'
import { CanvasDrawingPreview } from './CanvasDrawingPreview'

export function SalesPresentation() {
  // Create local state for presentation mode
  const [presentationModeLocal, setPresentationModeLocal] = useState(false)

  // Define toggle function
  const togglePresentation = () => {
    setPresentationModeLocal(!presentationModeLocal)
  }

  return (
    <div>
      {/* Pass props to child component */}
      <CanvasDrawingPreview
        presentationMode={presentationModeLocal}
        onPresentationMode={togglePresentation}
        parameters={{...}}
      />
    </div>
  )
}
```

---

### 2. Implementing Presentation Mode in Child Component

```typescript
// CanvasDrawingPreview.tsx
import { useState, useRef, useEffect } from 'react'
import styles from './CanvasDrawingPreview.module.css'

interface DrawingPreviewProps {
  presentationMode?: boolean
  onPresentationMode?: () => void
  // ... other props
}

export const CanvasDrawingPreview = ({
  presentationMode = false,
  onPresentationMode,
  // ... other props
}: DrawingPreviewProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  // Conditional render based on presentationMode prop
  return (
    <>
      {presentationMode ? (
        // Presentation Mode - Full Screen
        <div className={styles.presentationModeWrapper}>
          <div className={styles.presentationModeHeader}>
            <h2>Technical Drawing - Full Screen</h2>
            <button 
              onClick={() => onPresentationMode?.()}
              className={styles.presentationModeExitBtn}
            >
              Exit Full Screen
            </button>
          </div>
          
          <div className={styles.presentationModeContent}>
            <div className={styles.presentationModeCanvas}>
              <canvas
                ref={canvasRef}
                style={{
                  maxWidth: '95%',
                  maxHeight: '95%',
                  objectFit: 'contain'
                }}
              />
            </div>
          </div>
        </div>
      ) : (
        // Normal Mode - Split Layout
        <div className={styles.canvasContainer}>
          {/* Normal canvas rendering */}
        </div>
      )}
    </>
  )
}
```

---

### 3. Image Validation Helper

```typescript
// Helper function for image validation
const isImageValid = (image: HTMLImageElement | null): boolean => {
  if (!image) return false
  
  // All checks must pass
  return (
    image.complete &&              // Image has finished loading
    image.width > 0 &&             // CSS width is valid
    image.height > 0 &&            // CSS height is valid
    image.naturalWidth > 0 &&      // Natural width is valid
    image.naturalHeight > 0        // Natural height is valid
  )
}

// Usage in canvas drawing
if (isImageValid(frameImages.head)) {
  // Image is safe to draw
  ctx.drawImage(frameImages.head, x, y, width, height)
} else {
  // Draw placeholder instead
  drawImagePlaceholder(ctx, x, y, width, height)
}
```

---

### 4. Image Placeholder Function

```typescript
// Draw a placeholder when image is unavailable
const drawImagePlaceholder = (
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  width: number,
  height: number
) => {
  // Light grey background
  ctx.fillStyle = '#f3f4f6'
  ctx.fillRect(x, y, width, height)

  // Border
  ctx.strokeStyle = '#d1d5db'
  ctx.lineWidth = 1
  ctx.strokeRect(x, y, width, height)

  // Text message
  ctx.fillStyle = '#666666'
  ctx.font = '14px Arial'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText('No image available', x + width / 2, y + height / 2)
}
```

---

### 5. Loading Images with CORS Support

```typescript
// Load image from URL with CORS support
const loadHeadImage = () => {
  if (!frameImageUrls.head) return

  const headImg = new Image()
  
  // Enable CORS for cross-origin images
  headImg.crossOrigin = 'anonymous'

  // Handle successful load
  headImg.onload = () => {
    // Validate image dimensions
    if (
      headImg.complete &&
      headImg.width > 0 &&
      headImg.height > 0 &&
      headImg.naturalWidth > 0 &&
      headImg.naturalHeight > 0
    ) {
      setFrameImages((prev) => ({ ...prev, head: headImg }))
    } else {
      console.warn('HEAD image loaded but has invalid dimensions')
      setFrameImages((prev) => ({ ...prev, head: null }))
    }
  }

  // Handle load errors
  headImg.onerror = () => {
    console.warn(`Failed to load HEAD image: ${frameImageUrls.head}`)
    setFrameImages((prev) => ({ ...prev, head: null }))
  }

  // Handle abort
  headImg.onabort = () => {
    console.warn(`HEAD image loading aborted: ${frameImageUrls.head}`)
    setFrameImages((prev) => ({ ...prev, head: null }))
  }

  // Start loading
  headImg.src = frameImageUrls.head
}
```

---

### 6. CSS for Presentation Mode

```css
/* Main wrapper - full screen overlay */
.presentationModeWrapper {
  position: fixed;              /* Covers entire screen */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;                /* Above all other elements */
  background: #ffffff;
  display: flex;
  flex-direction: column;
  overflow: hidden;              /* No scrolling */
  animation: fadeIn 0.3s ease-out;
}

/* Header bar */
.presentationModeHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #1f2937;    /* Dark grey */
  color: #ffffff;
  border-bottom: 2px solid #374151;
  flex-shrink: 0;               /* Don't shrink */
}

/* Exit button */
.presentationModeExitBtn {
  padding: 8px 16px;
  background-color: #dc2626;    /* Red */
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.presentationModeExitBtn:hover {
  background-color: #b91c1c;    /* Darker red */
}

/* Content area */
.presentationModeContent {
  flex: 1;                      /* Take remaining space */
  overflow: auto;               /* Allow scrolling if needed */
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
  padding: 24px;
}

/* Canvas container */
.presentationModeCanvas {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Canvas element */
.presentationModeCanvas canvas {
  max-width: 95%;               /* Leave padding */
  max-height: 95%;
  object-fit: contain;          /* Maintain aspect ratio */
  background: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Fade-in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

---

### 7. Error Handling Pattern

```typescript
// Complete error handling flow
const drawFrameCrossSections = (
  ctx: CanvasRenderingContext2D,
  // ... parameters
) => {
  const sections = [
    { title: 'HEAD', image: frameImages.head },
    { title: 'SILL', image: frameImages.sill },
    { title: 'JAMB', image: frameImages.jamb },
  ]

  sections.forEach((section) => {
    // Check if image is valid
    const isValid = section.image &&
                   section.image.complete &&
                   section.image.width > 0 &&
                   section.image.height > 0 &&
                   section.image.naturalWidth > 0 &&
                   section.image.naturalHeight > 0

    if (isValid && section.image) {
      try {
        // Try to draw the image
        ctx.drawImage(section.image, x, y, width, height)
      } catch (error) {
        // Handle drawing errors
        console.error(`Error drawing ${section.title} image:`, error)
        drawImagePlaceholder(ctx, x, y, width, height, section.title)
      }
    } else {
      // Draw placeholder for invalid/missing image
      drawImagePlaceholder(ctx, x, y, width, height, section.title)
    }
  })
}
```

---

### 8. useEffect with Presentation Mode

```typescript
// Effect that triggers canvas redraw
useEffect(() => {
  const canvas = canvasRef.current
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // Set canvas size
  canvas.width = 1122
  canvas.height = 794

  // Draw canvas content
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  // Draw sections with validation
  drawHeader(ctx, canvas.width, canvas.height)
  drawMainContent(ctx, canvas.width, canvas.height)
  drawSpecsTable(ctx, canvas.width, canvas.height)

  // Dependencies include presentationMode
  // So canvas redraws when entering/exiting presentation mode
}, [
  parameters,
  frameImages,
  selectedFrameView,
  presentationMode  // ← NEW: Canvas redraws in presentation mode
])
```

---

### 9. Testing Example

```typescript
// Test presentation mode toggle
describe('CanvasDrawingPreview - Presentation Mode', () => {
  test('should render presentation mode when prop is true', () => {
    render(
      <CanvasDrawingPreview
        presentationMode={true}
        onPresentationMode={() => {}}
      />
    )

    expect(screen.getByText('Technical Drawing - Full Screen')).toBeInTheDocument()
  })

  test('should call onPresentationMode when exit button clicked', () => {
    const mockCallback = jest.fn()
    render(
      <CanvasDrawingPreview
        presentationMode={true}
        onPresentationMode={mockCallback}
      />
    )

    const exitButton = screen.getByText('Exit Full Screen')
    fireEvent.click(exitButton)

    expect(mockCallback).toHaveBeenCalled()
  })

  test('should render normal mode when presentationMode is false', () => {
    render(
      <CanvasDrawingPreview
        presentationMode={false}
      />
    )

    const heading = screen.queryByText('Technical Drawing - Full Screen')
    expect(heading).not.toBeInTheDocument()
  })
})
```

---

### 10. Integration Example

```typescript
// Complete integration in a page
import { SalesPresentation } from '@/components/sales/SalesPresentation'

export function SalesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white border-b">
        <h1 className="text-3xl font-bold p-4">Shop Drawing Generator</h1>
      </header>

      {/* Main content with presentation mode support */}
      <main className="flex-1">
        <SalesPresentation />
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white p-4 mt-8">
        <p>&copy; 2025 Raven Custom Glass. All rights reserved.</p>
      </footer>
    </div>
  )
}
```

---

## Common Patterns

### Pattern 1: Simple Toggle Button

```typescript
const [isPresenting, setIsPresenting] = useState(false)

return (
  <>
    <button onClick={() => setIsPresenting(!isPresenting)}>
      {isPresenting ? 'Exit' : 'Full Screen'}
    </button>
    {isPresenting && <FullScreenComponent />}
  </>
)
```

### Pattern 2: Callback from Child

```typescript
// Parent
const [mode, setMode] = useState('normal')

<Child onModeChange={(newMode) => setMode(newMode)} />

// Child
<button onClick={() => onModeChange('presentation')}>
  Full Screen
</button>
```

### Pattern 3: Context for Global State

```typescript
// app-context.tsx
const PresentationContext = createContext(false)

export function PresentationProvider({ children }) {
  const [presentationMode, setPresentationMode] = useState(false)

  return (
    <PresentationContext.Provider value={{ presentationMode, setPresentationMode }}>
      {children}
    </PresentationContext.Provider>
  )
}

// component.tsx
const { presentationMode, setPresentationMode } = useContext(PresentationContext)
```

---

## Debugging Tips

### Check Presentation Mode is Active
```typescript
// In browser console
// Find the wrapper element
document.querySelector('[class*="presentationMode"]')

// Check if styles are applied
window.getComputedStyle(element).position
// Should return: "fixed"

// Check z-index
window.getComputedStyle(element).zIndex
// Should return: "9999"
```

### Debug Image Loading
```typescript
// In browser console
// Check if images are loaded
console.log(frameImages.head?.complete)  // Should be true
console.log(frameImages.head?.width)     // Should be > 0
console.log(frameImages.head?.naturalWidth)  // Should be > 0

// Check CORS headers
fetch('/api/frames/cross-sections/86', { mode: 'cors' })
  .then(r => r.json())
  .then(console.log)
```

### Check Canvas Size
```typescript
// In browser console
const canvas = document.querySelector('canvas')
console.log(canvas.width)     // Should be 1122
console.log(canvas.height)    // Should be 794
console.log(canvas.style.maxWidth)  // Should be "95%"
```

---

## Performance Optimization Tips

1. **Debounce Canvas Redraws**
```typescript
const redrawCanvas = useCallback(
  debounce(() => {
    // Draw canvas
  }, 300),
  []
)
```

2. **Memoize Image Validation**
```typescript
const imageValidation = useMemo(
  () => ({
    head: isImageValid(frameImages.head),
    sill: isImageValid(frameImages.sill),
    jamb: isImageValid(frameImages.jamb),
  }),
  [frameImages]
)
```

3. **Cache Canvas Context**
```typescript
const ctxRef = useRef<CanvasRenderingContext2D | null>(null)

useEffect(() => {
  if (!canvasRef.current) return
  ctxRef.current = canvasRef.current.getContext('2d')
}, [])
```

---

## Summary

These code examples provide complete, ready-to-use implementations for:
- ✅ Component integration
- ✅ Image validation
- ✅ Error handling
- ✅ CSS styling
- ✅ Testing
- ✅ Debugging

Copy and adapt as needed for your specific use case.
