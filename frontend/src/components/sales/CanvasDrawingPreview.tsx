import { useEffect, useRef, useState } from 'react'
import styles from './CanvasDrawingPreview.module.css'
import WindowElevationView from '../WindowElevationView'
import DoorSwingPlanView from '../DoorSwingPlanView'

interface DrawingPreviewProps {
  parameters?: {
    series?: string
    width?: number
    height?: number
    productType?: string
    glassType?: string
    frameColor?: string
    configuration?: string
    itemNumber?: string
  }
  selectedFrameView?: 'head' | 'sill' | 'jamb'
  onPresentationMode?: () => void
  presentationMode?: boolean
}

interface FrameImageUrls {
  head: string | null
  sill: string | null
  jamb: string | null
}

interface FrameImages {
  head: HTMLImageElement | null
  sill: HTMLImageElement | null
  jamb: HTMLImageElement | null
}

export const CanvasDrawingPreview = ({ parameters, selectedFrameView = 'head', onPresentationMode, presentationMode = false }: DrawingPreviewProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [frameImageUrls, setFrameImageUrls] = useState<FrameImageUrls>({
    head: null,
    sill: null,
    jamb: null,
  })
  const [frameImages, setFrameImages] = useState<FrameImages>({
    head: null,
    sill: null,
    jamb: null,
  })
  const [isFullScreen, setIsFullScreen] = useState(false)
  const [showFloatingPlan, setShowFloatingPlan] = useState(false)
  const scrollContainerRef = useRef<HTMLDivElement>(null)

  // Helper function to validate image is properly loaded
  const isImageValid = (image: HTMLImageElement | null): boolean => {
    if (!image) return false
    return (
      image.complete &&
      image.width > 0 &&
      image.height > 0 &&
      image.naturalWidth > 0 &&
      image.naturalHeight > 0
    )
  }

  // Draw placeholder for invalid image
  const drawImagePlaceholder = (ctx: CanvasRenderingContext2D, x: number, y: number, width: number, height: number) => {
    ctx.fillStyle = '#f3f4f6'
    ctx.fillRect(x, y, width, height)
    ctx.strokeStyle = '#d1d5db'
    ctx.lineWidth = 1
    ctx.strokeRect(x, y, width, height)

    ctx.fillStyle = '#666666'
    ctx.font = '14px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText('No image available', x + width / 2, y + height / 2)
  }

  // Handle ESC key to exit full screen
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullScreen) {
        setIsFullScreen(false)
      }
    }

    if (isFullScreen) {
      document.addEventListener('keydown', handleKeyDown)
      return () => document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isFullScreen])

  // Handle scroll to show/hide floating plan
  useEffect(() => {
    const handleScroll = () => {
      if (scrollContainerRef.current) {
        const scrollTop = scrollContainerRef.current.scrollTop
        setShowFloatingPlan(scrollTop > 100)
      }
    }

    const container = scrollContainerRef.current
    if (container) {
      container.addEventListener('scroll', handleScroll)
      return () => container.removeEventListener('scroll', handleScroll)
    }
  }, [])

  // Construct frame cross-section image URLs directly
  useEffect(() => {
    if (!parameters?.series) {
      setFrameImageUrls({ head: null, sill: null, jamb: null })
      return
    }

    // Strip "Series" text and whitespace
    const cleanSeries = parameters.series.replace(/Series\s*/i, '').trim()

    // Construct image URLs with ABSOLUTE paths pointing to backend server
    const backendUrl = 'http://localhost:8000'
    setFrameImageUrls({
      head: `${backendUrl}/static/frames/series_${cleanSeries}_HEAD.png`,
      sill: `${backendUrl}/static/frames/series_${cleanSeries}_SILL.png`,
      jamb: `${backendUrl}/static/frames/series_${cleanSeries}_JAMB.png`,
    })
  }, [parameters?.series])

  // Preload images from URLs
  useEffect(() => {
    loadHeadImage()
    loadSillImage()
    loadJambImage()
  }, [frameImageUrls])

  const loadHeadImage = () => {
    if (!frameImageUrls.head) return
    const headImg = new Image()
    headImg.crossOrigin = 'anonymous'
    headImg.onload = () => {
      // Verify image actually loaded with dimensions
      if (headImg.complete && headImg.width > 0 && headImg.height > 0) {
        setFrameImages((prev: FrameImages) => ({ ...prev, head: headImg }))
      } else {
        console.warn('HEAD image loaded but has invalid dimensions')
        setFrameImages((prev: FrameImages) => ({ ...prev, head: null }))
      }
    }
    headImg.onerror = () => {
      console.warn(`Failed to load HEAD image: ${frameImageUrls.head}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, head: null }))
    }
    headImg.onabort = () => {
      console.warn(`HEAD image loading aborted: ${frameImageUrls.head}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, head: null }))
    }
    headImg.src = frameImageUrls.head
  }

  const loadSillImage = () => {
    if (!frameImageUrls.sill) return
    const sillImg = new Image()
    sillImg.crossOrigin = 'anonymous'
    sillImg.onload = () => {
      // Verify image actually loaded with dimensions
      if (sillImg.complete && sillImg.width > 0 && sillImg.height > 0) {
        setFrameImages((prev: FrameImages) => ({ ...prev, sill: sillImg }))
      } else {
        console.warn('SILL image loaded but has invalid dimensions')
        setFrameImages((prev: FrameImages) => ({ ...prev, sill: null }))
      }
    }
    sillImg.onerror = () => {
      console.warn(`Failed to load SILL image: ${frameImageUrls.sill}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, sill: null }))
    }
    sillImg.onabort = () => {
      console.warn(`SILL image loading aborted: ${frameImageUrls.sill}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, sill: null }))
    }
    sillImg.src = frameImageUrls.sill
  }

  const loadJambImage = () => {
    if (!frameImageUrls.jamb) return
    const jambImg = new Image()
    jambImg.crossOrigin = 'anonymous'
    jambImg.onload = () => {
      // Verify image actually loaded with dimensions
      if (jambImg.complete && jambImg.width > 0 && jambImg.height > 0) {
        setFrameImages((prev: FrameImages) => ({ ...prev, jamb: jambImg }))
      } else {
        console.warn('JAMB image loaded but has invalid dimensions')
        setFrameImages((prev: FrameImages) => ({ ...prev, jamb: null }))
      }
    }
    jambImg.onerror = () => {
      console.warn(`Failed to load JAMB image: ${frameImageUrls.jamb}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, jamb: null }))
    }
    jambImg.onabort = () => {
      console.warn(`JAMB image loading aborted: ${frameImageUrls.jamb}`)
      setFrameImages((prev: FrameImages) => ({ ...prev, jamb: null }))
    }
    jambImg.src = frameImageUrls.jamb
  }

  // Draw the canvas
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Landscape canvas - increased for better readability
    const canvasWidth = 2000
    const canvasHeight = 1100

    canvas.width = canvasWidth
    canvas.height = canvasHeight

    // White background
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, canvasWidth, canvasHeight)

    // Border
    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 2
    ctx.strokeRect(10, 10, canvasWidth - 20, canvasHeight - 20)

    // Draw sections
    drawHeader(ctx, canvasWidth, canvasHeight)
    drawMainContent(ctx, canvasWidth, canvasHeight)
    drawSpecsTable(ctx, canvasWidth, canvasHeight)
  }, [parameters, frameImages, selectedFrameView, presentationMode])

  const drawHeader = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    // Left: "Drawn from inside view"
    ctx.font = 'bold 14px Arial'
    ctx.fillStyle = '#000000'
    ctx.fillText('Drawn from inside view', 30, 35)

    // Right: Company info block
    const blockX = width - 200
    const blockY = 15
    const blockWidth = 180
    const blockHeight = 70

    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 1
    ctx.strokeRect(blockX, blockY, blockWidth, blockHeight)

    ctx.font = 'bold 12px Arial'
    ctx.fillText('▶ raven', blockX + 10, blockY + 20)

    ctx.font = '9px Arial'
    ctx.fillText('Add: 9960 W Cheyenne ave', blockX + 10, blockY + 35)
    ctx.fillText('Suite 140 Las Vegas NV 89129', blockX + 10, blockY + 47)
    ctx.fillText('Cell: 702-577-1003', blockX + 10, blockY + 59)
    ctx.fillText('Website: ravencustomglass.com', blockX + 10, blockY + 68)
  }

  const drawMainContent = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const margin = 20
    const col1X = margin
    const col1Width = (width - 60) * 0.3
    const col2X = col1X + col1Width + 15
    const col2Width = (width - 60) * 0.37
    const col3X = col2X + col2Width + 15
    const col3Width = (width - 60) * 0.28

    const contentTop = 110
    const contentHeight = height - 350 // Reduced to shift sections up and avoid line crossing

    drawFrameCrossSections(ctx, col1X, contentTop, col1Width, contentHeight)
    drawElevationAndPlan(ctx, col2X, contentTop, col2Width, contentHeight)
    drawFrameTypeAndInfo(ctx, col3X, contentTop, col3Width, contentHeight)
  }

  const drawFrameCrossSections = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number
  ) => {
    const sections = [
      { title: 'HEAD', image: frameImages.head, view: 'head' },
      { title: 'SILL', image: frameImages.sill, view: 'sill' },
      { title: 'JAMB', image: frameImages.jamb, view: 'jamb' },
    ]

    // Filter to show only selected view
    const visibleSections = sections.filter(s => s.view === selectedFrameView)
    const sectionHeight = height

    visibleSections.forEach((section, index) => {
      const sectionY = y + index * sectionHeight

      // Draw section title
      ctx.font = 'bold 14px Arial'
      ctx.fillStyle = '#000000'
      ctx.fillText(section.title, x + 5, sectionY + 20)

      // Draw section border
      ctx.strokeStyle = '#cccccc'
      ctx.lineWidth = 1
      ctx.strokeRect(x, sectionY + 28, width, sectionHeight - 33)

      // Draw section content (larger for single view)
      const contentX = x + 5
      const contentY = sectionY + 35
      const contentWidth = width - 10
      const contentHeight = sectionHeight - 45

      // Validate image before drawing
      const imageIsValid = section.image && 
                          section.image.complete && 
                          section.image.width > 0 && 
                          section.image.height > 0 &&
                          section.image.naturalWidth > 0 &&
                          section.image.naturalHeight > 0

      if (imageIsValid && section.image) {
        // Calculate scaling to fit within bounds
        const scale = Math.min(contentWidth / section.image.width, contentHeight / section.image.height)
        const scaledWidth = section.image.width * scale
        const scaledHeight = section.image.height * scale
        const offsetX = contentX + (contentWidth - scaledWidth) / 2
        const offsetY = contentY + (contentHeight - scaledHeight) / 2

        // Draw the image
        try {
          ctx.drawImage(section.image as CanvasImageSource, offsetX, offsetY, scaledWidth, scaledHeight)
        } catch (e) {
          console.error(`Error drawing ${section.title} image:`, e)
          drawPlaceholder(ctx, contentX, contentY, contentWidth, contentHeight, section.title)
        }
      } else {
        // Draw placeholder if no image
        let reason = 'no image'
        if (section.image) {
          if (!section.image.complete) reason = 'not loaded'
          else if (section.image.width === 0) reason = 'invalid width'
          else reason = 'invalid height'
        }
        console.debug(`Showing placeholder for ${section.title} (${reason})`)
        drawPlaceholder(ctx, contentX, contentY, contentWidth, contentHeight, section.title)
      }
    })
  }

  const drawPlaceholder = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number,
    label: string
  ) => {
    ctx.fillStyle = '#f0f0f0'
    ctx.fillRect(x, y, width, height)
    ctx.strokeStyle = '#ddd'
    ctx.lineWidth = 1
    ctx.strokeRect(x, y, width, height)

    ctx.fillStyle = '#999999'
    ctx.font = '11px Arial'
    ctx.textAlign = 'center'
    ctx.fillText('No Image', x + width / 2, y + height / 2 - 5)
    ctx.fillText(`(${label})`, x + width / 2, y + height / 2 + 10)
    ctx.textAlign = 'left'
  }

  const drawElevationAndPlan = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number
  ) => {
    const headerHeight = 25
    const elevationHeight = (height * 0.65) - headerHeight
    const planHeight = (height * 0.35) - headerHeight

    // Elevation Header
    ctx.font = 'bold 14px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    ctx.fillText('ELEVATION', x + 10, y + 18)

    // Elevation Box - Border only (content will be rendered by WindowElevationView SVG component)
    ctx.strokeStyle = '#cccccc'
    ctx.lineWidth = 1
    ctx.strokeRect(x, y + headerHeight, width, elevationHeight)

    // NOTE: Window drawing content is now handled by WindowElevationView SVG overlay
    // The following code is skipped to avoid double-rendering:
    // - Window frame rectangle
    // - Panel grid lines
    // - Dimension lines
    // This allows the SVG component to render cleanly within the box

    // Plan Header
    const planY = y + (height * 0.65)

    ctx.font = 'bold 14px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    ctx.fillText('PLAN', x + 10, planY + 18)

    // Plan Box
    ctx.strokeStyle = '#cccccc'
    ctx.lineWidth = 1
    ctx.strokeRect(x, planY + headerHeight, width, planHeight)

    // NOTE: Door swing plan view is now rendered by DoorSwingPlanView SVG overlay
    // The following code is skipped to avoid double-rendering:
    // - Window/door frame rectangle
    // - Person silhouette
    // This allows the SVG component to render cleanly within the box
  }

  const drawFrameTypeAndInfo = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number
  ) => {
    // FRAME TYPE header
    ctx.font = 'bold 12px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    ctx.fillText('FRAME TYPE', x + 10, y + 18)

    // Main content box
    ctx.strokeStyle = '#cccccc'
    ctx.lineWidth = 1
    ctx.strokeRect(x, y + 25, width, height - 25)

    // Frame type icons
    const iconSize = width * 0.18
    const iconStartY = y + 35
    const iconSpacing = (width - 20) / 4

    for (let i = 0; i < 4; i++) {
      const iconX = x + 10 + i * iconSpacing
      const iconY = iconStartY

      ctx.strokeStyle = '#000000'
      ctx.lineWidth = 1
      ctx.strokeRect(iconX, iconY, iconSize, iconSize)

      ctx.fillStyle = '#f9f9f9'
      ctx.fillRect(iconX, iconY, iconSize, iconSize)
    }

    // Drawing information inline below icons
    const infoStartY = iconStartY + iconSize + 15
    const infoData = [
      { label: 'Date:', value: new Date().toISOString().split('T')[0] },
      { label: 'Serial:', value: parameters?.itemNumber || 'P001' },
      { label: 'Designer:', value: 'Construction' },
      { label: 'Revision:', value: new Date().toISOString().split('T')[0] },
    ]

    // Draw info in a single row, inline
    ctx.font = '8px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    
    const colWidth = width / infoData.length
    infoData.forEach((item, index) => {
      const infoX = x + 10 + index * colWidth
      const labelY = infoStartY
      const valueY = infoStartY + 12

      ctx.font = 'bold 8px Arial'
      ctx.fillText(item.label, infoX, labelY)
      
      ctx.font = '8px Arial'
      ctx.fillText(item.value, infoX, valueY)
    })
  }

  const drawSpecsTable = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const tableY = height - 200
    const tableHeight = 190
    const margin = 20
    const tableWidth = width - 2 * margin

    ctx.font = 'bold 15px Arial'
    ctx.fillStyle = '#000000'
    ctx.fillText('SPECIFICATIONS', margin, tableY)

    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 1
    ctx.strokeRect(margin, tableY + 20, tableWidth, tableHeight - 20)

    const specs = [
      { label: 'Glass', value: parameters?.glassType || 'N/A' },
      { label: 'Frame Color', value: parameters?.frameColor || 'N/A' },
      {
        label: 'Frame Series',
        value: `${parameters?.series || 'N/A'} ${parameters?.productType || 'N/A'}`,
      },
      { label: 'Elevation Detail', value: 'Stucco setback 35mm from outside' },
      {
        label: 'Dimensions',
        value: `${parameters?.width || 0}" × ${parameters?.height || 0}"`,
      },
      { label: 'Special Notes', value: '' },
    ]

    const rowHeight = (tableHeight - 20) / specs.length
    const labelWidth = tableWidth * 0.25

    specs.forEach((spec, index) => {
      const rowY = tableY + 20 + index * rowHeight

      if (index > 0) {
        ctx.lineWidth = 0.5
        ctx.strokeStyle = '#cccccc'
        ctx.beginPath()
        ctx.moveTo(margin, rowY)
        ctx.lineTo(margin + tableWidth, rowY)
        ctx.stroke()
      }

      ctx.lineWidth = 0.5
      ctx.strokeStyle = '#cccccc'
      ctx.beginPath()
      ctx.moveTo(margin + labelWidth, rowY)
      ctx.lineTo(margin + labelWidth, rowY + rowHeight)
      ctx.stroke()

      ctx.font = 'bold 15px Arial'
      ctx.fillStyle = '#000000'
      ctx.fillText(spec.label, margin + 8, rowY + rowHeight / 2 + 5)

      ctx.font = '15px Arial'
      ctx.fillText(spec.value, margin + labelWidth + 8, rowY + rowHeight / 2 + 5)
    })
  }

  // Extract nested ternary into separate variable
  const renderMode = presentationMode ? 'presentation' : isFullScreen ? 'fullscreen' : 'normal'

  return (
    <>
      {renderMode === 'presentation' ? (
        // Presentation mode - Full screen wrapper
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
                className={styles.canvas}
                style={{
                  maxWidth: '95%',
                  maxHeight: '95%',
                  objectFit: 'contain'
                }}
              />
            </div>
          </div>
        </div>
      ) : renderMode === 'fullscreen' ? (
        // Full screen mode
        <div className="fixed inset-0 bg-black z-50 flex flex-col" ref={scrollContainerRef}>
          {/* Header */}
          <div className="flex justify-between items-center px-6 py-4 bg-gray-900 text-white">
            <h1 className="text-2xl font-bold">A4 Landscape - {parameters?.series} {parameters?.width}\" × {parameters?.height}\"</h1>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-300">Press ESC to exit</span>
              <button
                onClick={() => setIsFullScreen(false)}
                className="px-6 py-2 bg-red-600 hover:bg-red-700 rounded text-white font-semibold transition-colors"
              >
                Exit Full Screen
              </button>
            </div>
          </div>

          {/* Canvas area - centered */}
          <div className="flex-1 flex items-center justify-center overflow-auto p-4 bg-black">
            <canvas
              ref={canvasRef}
              className="bg-white shadow-2xl"
              style={{
                maxWidth: '95vw',
                maxHeight: '95vh',
                aspectRatio: '1122/794',
              }}
            />
          </div>

          {/* Footer with info */}
          <div className="px-6 py-3 bg-gray-900 text-white text-sm border-t border-gray-700">
            <p>A4 Landscape (1122×794px) | Frame Images: HEAD {frameImages.head ? '✓' : '✗'} | SILL {frameImages.sill ? '✓' : '✗'} | JAMB {frameImages.jamb ? '✓' : '✗'}</p>
          </div>

          {/* Floating Plan Panel in Fullscreen */}
          {showFloatingPlan && (
            <div className="fixed bottom-6 right-6 bg-white rounded-lg shadow-2xl border-2 border-gray-300 p-4 z-40 animate-fade-in" style={{ width: '300px', maxHeight: '320px' }}>
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-sm font-bold text-gray-900">📐 PLAN VIEW</h3>
                <button
                  onClick={() => setShowFloatingPlan(false)}
                  className="text-gray-400 hover:text-gray-600 text-lg leading-none"
                >
                  ✕
                </button>
              </div>
              
              {/* Mini Plan Canvas */}
              <div className="bg-gray-50 rounded border border-gray-200 p-2 flex items-center justify-center" style={{ height: '240px', overflow: 'hidden' }}>
                <canvas
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    aspectRatio: '1',
                  }}
                  ref={(miniCanvas) => {
                    if (miniCanvas && canvasRef.current) {
                      const ctx = miniCanvas.getContext('2d')
                      if (!ctx) return

                      const size = 220
                      miniCanvas.width = size
                      miniCanvas.height = size

                      // Draw mini plan view
                      ctx.clearRect(0, 0, size, size)
                      ctx.fillStyle = '#ffffff'
                      ctx.fillRect(0, 0, size, size)
                      ctx.strokeStyle = '#000000'
                      ctx.lineWidth = 2

                      // Draw window from plan perspective
                      const padding = 20
                      const windowSize = size - padding * 2
                      const frameDepth = 8

                      ctx.strokeRect(padding, padding, windowSize, windowSize)

                      // Inner frame
                      ctx.lineWidth = 1
                      ctx.strokeRect(padding + frameDepth, padding + frameDepth, windowSize - frameDepth * 2, windowSize - frameDepth * 2)

                      // Draw person for scale
                      const personX = padding + windowSize + 35
                      const personY = padding + 20

                      ctx.fillStyle = '#000000'
                      ctx.beginPath()
                      ctx.arc(personX, personY + 8, 5, 0, Math.PI * 2)
                      ctx.fill()

                      ctx.fillRect(personX - 3, personY + 13, 6, 12)

                      // Add label
                      ctx.font = 'bold 11px Arial'
                      ctx.fillText('PLAN', padding + 5, padding + 15)
                    }
                  }}
                />
              </div>

              <div className="mt-2 text-xs text-gray-500 text-center">
                Series: {parameters?.series || '—'} | {parameters?.width}″ × {parameters?.height}″
              </div>
            </div>
          )}
        </div>
      ) : (
        // Normal mode - Zoom to Fit layout with responsive scaling
        <div className={`flex flex-col w-full h-full relative ${styles.stickyWrapper}`}>
          {/* Controls */}
          <div className="flex justify-between items-center px-4 pt-4 w-full">
            <h2 className="text-lg font-semibold text-gray-900">Drawing Preview</h2>
            <button
              onClick={() => setIsFullScreen(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors font-semibold"
            >
              Full Screen
            </button>
          </div>

          {/* Zoom to Fit Container - Scales canvas down to fit available space */}
          <div 
            className={styles.canvasContainer}
            style={{
              width: '100%',
              height: '100%',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              overflow: 'hidden',
              backgroundColor: '#f3f4f6',
              padding: '20px',
            }}
          >
            {/* Responsive Canvas Wrapper - Removed A4 aspect ratio constraint */}
            <div style={{ 
              position: 'relative',
              maxWidth: '100%',
              maxHeight: '100%',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
              backgroundColor: 'white',
              borderRadius: '4px',
            }}>
              {/* Main Canvas - High resolution (1600×1000) scaling to fit container */}
              <canvas
                ref={canvasRef}
                width={1600}
                height={1000}
                className={styles.canvas}
                style={{
                  width: '100%',
                  height: '100%',
                  display: 'block',
                  borderRadius: '4px',
                }}
              />
              
              {/* Elevation SVG Component - Perfectly centered within ELEVATION grid box */}
              {/* Coordinates: col2X=617px (30.85%), contentTop+headerHeight=135px (12.27%), width=717.8px (35.89%), height=437.5px (39.77%) */}
              <div
                style={{
                  position: 'absolute',
                  left: '30.85%',    // Start of ELEVATION box (col2X)
                  top: '12.27%',     // Start of ELEVATION box (contentTop + headerHeight)
                  width: '35.89%',   // Width of ELEVATION box (col2Width)
                  height: '39.77%',  // Height of ELEVATION box
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  overflow: 'hidden',
                  padding: '20px',   // Prevents drawing from touching edges
                }}
              >
                <WindowElevationView
                  width={parameters?.width ? parameters.width * 25.4 : 609.6}
                  height={parameters?.height ? parameters.height * 25.4 : 1524}
                  gridCols={2}
                  gridRows={3}
                />
              </div>

              {/* Door Swing Plan SVG Component - Overlay below Elevation */}
              {/* Scales responsively with aspect ratio wrapper */}
              <div
                style={{
                  position: 'absolute',
                  left: '48.3%',
                  top: '64.8%',
                  width: '25%',
                  height: '26%',
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  padding: '15px',
                  overflow: 'hidden',
                  borderRadius: '2px',
                }}
              >
                <div
                  style={{
                    width: '100%',
                    height: '100%',
                    maxWidth: '100%',
                    maxHeight: '100%',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                  }}
                >
                  <DoorSwingPlanView
                    handing={parameters?.configuration?.toLowerCase().includes('left') ? 'left' : 'right'}
                    isOutswing={!parameters?.configuration?.toLowerCase().includes('inswing')}
                    label={parameters?.productType?.split('-')[0] ?? null}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Floating Plan Panel */}
          {showFloatingPlan && (
            <div className="fixed bottom-6 right-6 bg-white rounded-lg shadow-xl border border-gray-300 p-4 z-40 animate-fade-in" style={{ width: '280px', maxHeight: '300px' }}>
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-sm font-bold text-gray-900">📐 PLAN VIEW</h3>
                <button
                  onClick={() => setShowFloatingPlan(false)}
                  className="text-gray-400 hover:text-gray-600 text-lg leading-none"
                >
                  ✕
                </button>
              </div>
              
              {/* Mini Plan Canvas */}
              <div className="bg-gray-50 rounded border border-gray-200 p-2 flex items-center justify-center" style={{ height: '220px', overflow: 'hidden' }}>
                <canvas
                  style={{
                    maxWidth: '100%',
                    maxHeight: '100%',
                    aspectRatio: '1',
                  }}
                  ref={(miniCanvas) => {
                    if (miniCanvas && canvasRef.current) {
                      const ctx = miniCanvas.getContext('2d')
                      if (!ctx) return

                      const size = 200
                      miniCanvas.width = size
                      miniCanvas.height = size

                      // Draw mini plan view
                      ctx.clearRect(0, 0, size, size)
                      ctx.fillStyle = '#ffffff'
                      ctx.fillRect(0, 0, size, size)
                      ctx.strokeStyle = '#000000'
                      ctx.lineWidth = 2

                      // Draw window from plan perspective
                      const padding = 20
                      const windowSize = size - padding * 2
                      const frameDepth = 8

                      ctx.strokeRect(padding, padding, windowSize, windowSize)

                      // Inner frame
                      ctx.lineWidth = 1
                      ctx.strokeRect(padding + frameDepth, padding + frameDepth, windowSize - frameDepth * 2, windowSize - frameDepth * 2)

                      // Draw person for scale
                      const personX = padding + windowSize + 30
                      const personY = padding + 15

                      ctx.fillStyle = '#000000'
                      ctx.beginPath()
                      ctx.arc(personX, personY + 8, 5, 0, Math.PI * 2)
                      ctx.fill()

                      ctx.fillRect(personX - 3, personY + 13, 6, 12)

                      // Add label
                      ctx.font = 'bold 10px Arial'
                      ctx.fillText('PLAN', padding + 5, padding + 15)
                    }
                  }}
                />
              </div>

              <div className="mt-2 text-xs text-gray-500 text-center">
                Series: {parameters?.series || '—'} | {parameters?.width}″ × {parameters?.height}″
              </div>
            </div>
          )}

          {/* Debug info */}
          <div className="px-4 pb-4 text-xs text-gray-500 border-t pt-2 mt-4">
            <p>Canvas Size: 1600×1000px (Expanded format) | Frame Images: HEAD {frameImages.head ? '✓' : '✗'} | SILL {frameImages.sill ? '✓' : '✗'} | JAMB {frameImages.jamb ? '✓' : '✗'}</p>
          </div>
        </div>
      )}
    </>
  )
}

function drawDimensionLine(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  length: number,
  orientation: 'horizontal' | 'vertical',
  label: string
) {
  ctx.strokeStyle = '#000000'
  ctx.lineWidth = 1
  ctx.fillStyle = '#000000'
  ctx.font = '10px Arial'

  const arrowSize = 8

  if (orientation === 'horizontal') {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x + length, y)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x + arrowSize, y - arrowSize / 2)
    ctx.lineTo(x + arrowSize, y + arrowSize / 2)
    ctx.closePath()
    ctx.fill()

    ctx.beginPath()
    ctx.moveTo(x + length, y)
    ctx.lineTo(x + length - arrowSize, y - arrowSize / 2)
    ctx.lineTo(x + length - arrowSize, y + arrowSize / 2)
    ctx.closePath()
    ctx.fill()

    ctx.fillText(label, x + length / 2 - 15, y - 8)
  } else {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x, y + length)
    ctx.stroke()

    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x - arrowSize / 2, y + arrowSize)
    ctx.lineTo(x + arrowSize / 2, y + arrowSize)
    ctx.closePath()
    ctx.fill()

    ctx.beginPath()
    ctx.moveTo(x, y + length)
    ctx.lineTo(x - arrowSize / 2, y + length - arrowSize)
    ctx.lineTo(x + arrowSize / 2, y + length - arrowSize)
    ctx.closePath()
    ctx.fill()

    ctx.save()
    ctx.translate(x + 15, y + length / 2)
    ctx.rotate(Math.PI / 2)
    ctx.fillText(label, -15, 0)
    ctx.restore()
  }
}

function drawPersonSilhouette(ctx: CanvasRenderingContext2D, x: number, y: number) {
  ctx.strokeStyle = '#000000'
  ctx.lineWidth = 1
  ctx.fillStyle = '#ffffff'

  ctx.beginPath()
  ctx.arc(x, y + 8, 5, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()

  ctx.fillRect(x - 4, y + 13, 8, 15)
  ctx.strokeRect(x - 4, y + 13, 8, 15)

  ctx.beginPath()
  ctx.moveTo(x - 4, y + 16)
  ctx.lineTo(x - 10, y + 14)
  ctx.stroke()

  ctx.beginPath()
  ctx.moveTo(x + 4, y + 16)
  ctx.lineTo(x + 10, y + 14)
  ctx.stroke()

  ctx.beginPath()
  ctx.moveTo(x - 2, y + 28)
  ctx.lineTo(x - 3, y + 35)
  ctx.stroke()

  ctx.beginPath()
  ctx.moveTo(x + 2, y + 28)
  ctx.lineTo(x + 3, y + 35)
  ctx.stroke()
}
