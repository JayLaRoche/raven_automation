import { useEffect, useRef, useState } from 'react'
import styles from './CanvasDrawingPreview.module.css'
import WindowElevationView from '../WindowElevationView'
import { useDrawingStore } from '../../store/drawingStore'
import { saveDrawing } from '../../services/api'

// Get API URL from environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Function to map product type and swing orientation to plan view image URL
const getPlanViewUrl = (product: string | undefined, swing: string | undefined) => {
  if (!product) return null
  const baseUrl = `${API_URL}/static/O-Icon_library`
  
  // 1. Sliding Doors & Windows (Map to the 2-panel slider image)
  if ([
    'Standard Sliding Door', 
    'Lift Slide Door', 
    'Slim Frame Interior Door',
    'Slim Frame Sliding Door',
    'Standard Sliding Window'
  ].includes(product)) {
    // If you have a specific 4-panel image, you can check swing for 4-panel config
    if (product === 'Slim Frame Sliding Door' && swing?.includes('4')) {
      return `${baseUrl}/D-4_Track_4_Panel_Slider.PNG`
    }
    return `${baseUrl}/D-2_Panel_Slider.PNG`
  }

  // 2. Casement / Hinged Doors
  if (product === 'Casement Door') {
    if (swing === 'Left Hand Inswing') return `${baseUrl}/D-Hinged_Door_IN_L.PNG`
    if (swing === 'Right Hand Inswing') return `${baseUrl}/D-Hinged_Door_IN_R.PNG`
    if (swing === 'Left Hand Outswing') return `${baseUrl}/D-Hinged_Door_OUT_L.PNG`
    if (swing === 'Right Hand Outswing') return `${baseUrl}/D-Hinged_Door_OUT_R.PNG`
  }

  // 3. Pivot Doors (Using Hinged images as visual proxy)
  if (product === 'Pivot Door') {
    if (swing === 'Pivot Left') return `${baseUrl}/D-Hinged_Door_IN_L.PNG`
    if (swing === 'Pivot Right') return `${baseUrl}/D-Hinged_Door_IN_R.PNG`
  }

  // 4. Windows
  if (product === 'Fixed Window') {
    return `${baseUrl}/W-Fixed_O.PNG`
  }
  
  if (product === 'Slim Frame Casement Window') {
    if (swing === 'Left Hand') return `${baseUrl}/W-Left_Casement_O.PNG`
    if (swing === 'Right Hand') return `${baseUrl}/W-Right_Casement_O.PNG`
    // Default to Left if undefined
    return `${baseUrl}/W-Left_Casement_O.PNG`
  }

  // Fallback / Double Cases
  if (swing === 'Double Door Inswing') return `${baseUrl}/W-Double_Casement_O.PNG`

  return null
}

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
    panelCount?: number
    swingOrientation?: string
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
  const { projectId, unitId } = useDrawingStore()
  const [isSaving, setIsSaving] = useState(false)
  const [saveMessage, setSaveMessage] = useState('')
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
  const [productImage, setProductImage] = useState<HTMLImageElement | null>(null)
  const [logoImage, setLogoImage] = useState<HTMLImageElement | null>(null)
  const [isFullScreen, setIsFullScreen] = useState(false)
  const [showFloatingPlan, setShowFloatingPlan] = useState(false)
  const scrollContainerRef = useRef<HTMLDivElement>(null)

  // Handle saving drawing to database
  const handleSaveDrawing = async () => {
    if (!unitId || !projectId) {
      alert('Cannot save: No project/unit context available')
      return
    }

    if (!canvasRef.current) {
      alert('Cannot save: No drawing generated')
      return
    }

    try {
      setIsSaving(true)
      setSaveMessage('Saving...')

      // Convert canvas to blob
      const blob = await new Promise<Blob | null>((resolve) => {
        canvasRef.current?.toBlob(resolve, 'image/png')
      })

      if (!blob) {
        throw new Error('Failed to create canvas blob')
      }

      // Convert blob to base64
      const reader = new FileReader()
      const base64Promise = new Promise<string>((resolve, reject) => {
        reader.onloadend = () => {
          const base64 = (reader.result as string).split(',')[1]
          resolve(base64)
        }
        reader.onerror = reject
        reader.readAsDataURL(blob)
      })

      const pdfBase64 = await base64Promise

      // Save to database
      const result = await saveDrawing({
        unitId,
        projectId,
        pdfBase64,
        parameters: {
          series: parameters?.series || '',
          productType: parameters?.productType || '',
          width: parameters?.width || 0,
          height: parameters?.height || 0,
          glassType: parameters?.glassType || '',
          frameColor: parameters?.frameColor || '',
          configuration: parameters?.configuration,
          hasGrids: false,
          panelCount: parameters?.panelCount,
          swingOrientation: parameters?.swingOrientation,
          handleSide: ''
        }
      })

      setSaveMessage(`✅ ${result.message}`)
      setTimeout(() => setSaveMessage(''), 3000)

    } catch (error: any) {
      console.error('Save failed:', error)
      alert(error.response?.data?.detail || 'Failed to save drawing')
    } finally {
      setIsSaving(false)
    }
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

  // Load product image based on productType
  useEffect(() => {
    if (!parameters?.productType) {
      setProductImage(null)
      return
    }

    // Convert productType to slug format (lowercase, spaces to hyphens)
    const slug = parameters.productType.toLowerCase().replace(/\s+/g, '-')
    const imageUrl = `http://localhost:8000/static/products/${slug}.jpg`

    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      setProductImage(img)
    }
    
    img.onerror = () => {
      setProductImage(null)
    }
    
    img.src = imageUrl
  }, [parameters?.productType])

  // Load company logo for header
  useEffect(() => {
    const logoUrl = '/raven-logo.PNG'
    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      setLogoImage(img)
    }
    
    img.onerror = () => {
      console.warn('Failed to load logo image')
      setLogoImage(null)
    }
    
    img.src = logoUrl
  }, [])

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
    drawHeader(ctx, canvasWidth)
    drawMainContent(ctx, canvasWidth, canvasHeight)
    drawSpecsTable(ctx, canvasWidth, canvasHeight)
  }, [parameters, frameImages, selectedFrameView, presentationMode, isFullScreen])

  const drawHeader = (ctx: CanvasRenderingContext2D, width: number) => {
    // Left: "Drawn from inside view"
    ctx.font = 'bold 19px Arial'
    ctx.fillStyle = '#000000'
    ctx.fillText('Drawn from inside view', 30, 35)

    // Right: Company logo
    if (logoImage && logoImage.complete && logoImage.naturalWidth > 0) {
      const maxLogoWidth = 180
      const maxLogoHeight = 70
      const logoAspect = logoImage.naturalWidth / logoImage.naturalHeight
      
      // Calculate scaled dimensions to fit within max bounds
      let logoWidth = maxLogoWidth
      let logoHeight = maxLogoWidth / logoAspect
      
      if (logoHeight > maxLogoHeight) {
        logoHeight = maxLogoHeight
        logoWidth = maxLogoHeight * logoAspect
      }
      
      const logoX = width - logoWidth - 20
      const logoY = 15
      
      ctx.drawImage(logoImage, logoX, logoY, logoWidth, logoHeight)
    }
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

    // Show all three sections stacked vertically with reduced size
    const visibleSections = sections
    const sectionHeight = height / 3
    const spacing = 10 // Add spacing between sections
    const reducedSectionHeight = sectionHeight * 0.7 // Reduce to 70% of original size

    visibleSections.forEach((section, index) => {
      const sectionY = y + index * sectionHeight

      // Draw section border with reduced height
      ctx.strokeStyle = '#cccccc'
      ctx.lineWidth = 1
      ctx.strokeRect(x, sectionY + spacing, width, reducedSectionHeight - spacing)

      // Draw section content with reduced dimensions
      const contentX = x + 5
      const contentY = sectionY + spacing + 5
      const contentWidth = width - 10
      const contentHeight = reducedSectionHeight - spacing - 10

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
          ctx.drawImage(section.image, offsetX, offsetY, scaledWidth, scaledHeight)
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
    ctx.font = '16px Arial'
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
    ctx.font = 'bold 19px Arial'
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

    ctx.font = 'bold 19px Arial'
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
    
    // Check if a Plan View image is available
    const planImageUrl = getPlanViewUrl(parameters?.productType, parameters?.swingOrientation)
    if (planImageUrl) {
      // Plan View Image will be rendered in the SVG overlay
      // This is handled by the <img> tag in the JSX return section
    }
  }

  const drawFrameTypeAndInfo = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width: number,
    height: number
  ) => {
    // PRODUCT REFERENCE header
    ctx.font = 'bold 17px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    ctx.fillText('PRODUCT REFERENCE', x + 10, y + 18)

    // Main content box
    ctx.strokeStyle = '#cccccc'
    ctx.lineWidth = 1
    ctx.strokeRect(x, y + 25, width, height - 25)

    // Image Drawing Area
    const imgAreaX = x + 10
    const imgAreaY = y + 30
    const imgAreaWidth = width - 20
    const imgAreaHeight = height - 80 // Leave space for text at bottom

    if (productImage && productImage.complete && productImage.naturalWidth > 0) {
      // Calculate aspect ratio to "contain" the image
      const scale = Math.min(
        imgAreaWidth / productImage.naturalWidth,
        imgAreaHeight / productImage.naturalHeight
      )
      const drawW = productImage.naturalWidth * scale
      const drawH = productImage.naturalHeight * scale
      const drawX = imgAreaX + (imgAreaWidth - drawW) / 2
      const drawY = imgAreaY + (imgAreaHeight - drawH) / 2

      ctx.drawImage(productImage, drawX, drawY, drawW, drawH)
      
      // Optional: Add a light border around the image
      ctx.strokeStyle = '#eeeeee'
      ctx.lineWidth = 1
      ctx.strokeRect(drawX, drawY, drawW, drawH)
    } else {
      // Placeholder
      ctx.fillStyle = '#f9f9f9'
      ctx.fillRect(imgAreaX, imgAreaY, imgAreaWidth, imgAreaHeight)
      ctx.fillStyle = '#999999'
      ctx.textAlign = 'center'
      ctx.font = 'italic 17px Arial'
      ctx.fillText('Product Image Not Available', imgAreaX + imgAreaWidth / 2, imgAreaY + imgAreaHeight / 2)
      ctx.textAlign = 'left' // Reset alignment
    }

    // Drawing information inline below image
    const infoStartY = imgAreaY + imgAreaHeight + 20
    const infoData = [
      { label: 'Date:', value: new Date().toISOString().split('T')[0] },
      { label: 'Serial:', value: parameters?.itemNumber || 'P001' },
      { label: 'Designer:', value: 'Construction' },
      { label: 'Revision:', value: new Date().toISOString().split('T')[0] },
    ]

    // Draw info in a single row, inline with increased font size
    ctx.font = '20px Arial'
    ctx.fillStyle = '#000000'
    ctx.textAlign = 'left'
    
    const colWidth = width / infoData.length
    infoData.forEach((item, index) => {
      const infoX = x + 5 + index * colWidth
      const labelY = infoStartY
      const valueY = infoStartY + 22 // Increased spacing for 20px font

      ctx.font = 'bold 20px Arial'
      ctx.fillText(item.label, infoX, labelY)
      
      ctx.font = '20px Arial'
      ctx.fillText(item.value, infoX, valueY)
    })
  }

  const drawSpecsTable = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    const tableY = height - 200
    const tableHeight = 190
    const margin = 20
    const tableWidth = width - 2 * margin

    ctx.font = 'bold 20px Arial'
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

      ctx.font = 'bold 20px Arial'
      ctx.fillStyle = '#000000'
      ctx.fillText(spec.label, margin + 8, rowY + rowHeight / 2 + 5)

      ctx.font = '20px Arial'
      ctx.fillText(spec.value, margin + labelWidth + 8, rowY + rowHeight / 2 + 5)
    })
  }

  // Render helper functions to reduce cognitive complexity
  const renderPresentationMode = () => (
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
        <div className="flex items-center justify-center w-full h-full">
          {renderCanvasWithOverlays()}
        </div>
      </div>
    </div>
  )

  const renderFullScreenMode = () => (
    <div className="fixed inset-0 z-[9999] bg-black flex flex-col items-center justify-center p-8" ref={scrollContainerRef}>
      {renderFloatingControls()}
      <div className="flex items-center justify-center w-full h-full">
        {renderCanvasWithOverlays()}
      </div>
      {renderInfoFooter()}
    </div>
  )

  const renderFloatingControls = () => (
    <div className="absolute top-6 right-6 flex gap-4 z-[10000]">
      {saveMessage && (
        <div className="px-4 py-2 bg-green-600 text-white rounded shadow-lg font-bold flex items-center gap-2">
          {saveMessage}
        </div>
      )}
      
      <button 
        onClick={handleSaveDrawing}
        disabled={isSaving || !projectId || !unitId}
        className={`px-6 py-2 ${
          isSaving || !projectId || !unitId
            ? 'bg-gray-500 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700'
        } text-white rounded shadow-lg font-bold flex items-center gap-2 transition-colors`}
        title={!projectId || !unitId ? 'No project/unit context' : 'Save drawing to database'}
      >
        <span>💾</span> {isSaving ? 'Saving...' : 'Save to Project'}
      </button>
      
      <button 
        onClick={() => {
          if (presentationMode && onPresentationMode) {
            onPresentationMode()
          } else {
            setIsFullScreen(false)
          }
        }}
        className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded shadow-lg font-bold flex items-center gap-2 transition-colors"
      >
        <span>✕</span> Exit
      </button>
    </div>
  )

  const renderInfoFooter = () => (
    <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-900/80 text-white text-sm px-6 py-2 rounded-full backdrop-blur-sm">
      {parameters?.series} Series | {parameters?.width}" × {parameters?.height}" | Frame Images: HEAD {frameImages.head ? '✓' : '✗'} SILL {frameImages.sill ? '✓' : '✗'} JAMB {frameImages.jamb ? '✓' : '✗'}
    </div>
  )

  const renderCanvasWithOverlays = () => (
    <div 
      style={{
        position: 'relative',
        width: '100%',
        height: 'auto',
        aspectRatio: '1600 / 1000',
        maxWidth: '95vw',
        maxHeight: presentationMode ? '90vh' : '85vh',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        backgroundColor: 'white',
        borderRadius: '4px',
      }}
    >
      <canvas
        ref={canvasRef}
        className="bg-white"
        style={{
          width: '100%',
          height: '100%',
          display: 'block',
          borderRadius: '4px',
        }}
      />
      {renderElevationOverlay()}
      {renderPlanViewOverlay()}
    </div>
  )

  const renderElevationOverlay = () => (
    <div
      style={{
        position: 'absolute',
        left: '30.85%',
        top: '12.27%',
        width: '35.89%',
        height: '39.77%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        overflow: 'hidden',
        padding: '20px',
        pointerEvents: 'none',
      }}
    >
      <WindowElevationView
        parameters={parameters}
        selectedFrameView={selectedFrameView}
      />
    </div>
  )

  const renderPlanViewOverlay = () => {
    const planImageUrl = getPlanViewUrl(parameters?.productType, parameters?.swingOrientation)
    if (!planImageUrl) return null

    return (
      <div
        style={{
          position: 'absolute',
          left: '30.85%',
          top: '56.6%',
          width: '35.89%',
          height: '21%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '10px',
          overflow: 'hidden',
          borderRadius: '2px',
          pointerEvents: 'none',
        }}
      >
        <img
          src={planImageUrl}
          alt="Plan View"
          style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
          onError={(e) => {
            console.warn('Plan view image failed to load:', e.currentTarget.src);
            e.currentTarget.style.display = 'none';
          }}
        />
      </div>
    )
  }

  // Determine which render mode to use
  const getRenderMode = () => {
    if (presentationMode || isFullScreen) return renderFullScreenMode()
    return renderNormalMode()
  }

  const renderNormalMode = () => (
    <div className={`flex flex-col w-full h-full relative ${styles.stickyWrapper}`}>
      {renderNormalControls()}
      {renderNormalCanvas()}
      {showFloatingPlan && renderFloatingPlanPanel()}
      {renderDebugInfo()}
    </div>
  )

  const renderNormalControls = () => (
    <div className="flex justify-between items-center px-4 pt-4 w-full">
      <h2 className="text-lg font-semibold text-gray-900">Drawing Preview</h2>
      <button
        onClick={() => setIsFullScreen(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors font-semibold"
      >
        Full Screen
      </button>
    </div>
  )

  const renderNormalCanvas = () => (
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
      <div style={{ 
        position: 'relative',
        maxWidth: '100%',
        maxHeight: '100%',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        backgroundColor: 'white',
        borderRadius: '4px',
      }}>
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
        {renderElevationOverlay()}
        {renderPlanViewOverlay()}
      </div>
    </div>
  )

  const renderFloatingPlanPanel = () => (
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

              ctx.clearRect(0, 0, size, size)
              ctx.fillStyle = '#ffffff'
              ctx.fillRect(0, 0, size, size)
              ctx.strokeStyle = '#000000'
              ctx.lineWidth = 2

              const padding = 20
              const windowSize = size - padding * 2
              const frameDepth = 8

              ctx.strokeRect(padding, padding, windowSize, windowSize)
              ctx.lineWidth = 1
              ctx.strokeRect(padding + frameDepth, padding + frameDepth, windowSize - frameDepth * 2, windowSize - frameDepth * 2)

              const personX = padding + windowSize + 30
              const personY = padding + 15

              ctx.fillStyle = '#000000'
              ctx.beginPath()
              ctx.arc(personX, personY + 8, 5, 0, Math.PI * 2)
              ctx.fill()

              ctx.fillRect(personX - 3, personY + 13, 6, 12)

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
  )

  const renderDebugInfo = () => (
    <div className="px-4 pb-4 text-xs text-gray-500 border-t pt-2 mt-4">
      <p>Canvas Size: 1600×1000px (Expanded format) | Frame Images: HEAD {frameImages.head ? '✓' : '✗'} | SILL {frameImages.sill ? '✓' : '✗'} | JAMB {frameImages.jamb ? '✓' : '✗'}</p>
    </div>
  )

  return <>{getRenderMode()}</>
}
