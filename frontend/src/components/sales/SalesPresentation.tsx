import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { jsPDF } from 'jspdf'
import html2canvas from 'html2canvas'
import { useDrawingStore } from '../../store/drawingStore'
import { useKeyboardShortcuts } from '../../hooks/useKeyboardShortcuts'
import { SmartParameterPanel } from './SmartParameterPanel'
import { CanvasDrawingPreview } from './CanvasDrawingPreview'
import { QuickExport } from './QuickExport'
import styles from './SalesPresentation.module.css'

import { useToast } from '../ui/Toast'
import { generateDrawing } from '../../services/api'
import { debounce } from 'lodash-es'

interface LocationState {
  initialDrawingData?: {
    series: string
    productType: string
    width: number
    height: number
    glassType: string
    frameColor: string
    configuration?: string
  }
}

export function SalesPresentation() {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const location = useLocation() as { state: LocationState | null }
  const { parameters, drawing, autoUpdate, presentationMode, setPresentationMode, setDrawing, setIsGenerating, setParameters, selectedFrameView } = useDrawingStore()
  const [showExportModal, setShowExportModal] = useState(false)
  
  const toast = useToast()
  
  // Initialize parameters from location state if available (from "Add Unit" workflow)
  useEffect(() => {
    const incomingData = location.state?.initialDrawingData
    if (incomingData) {
      // Map the incoming data to the store's parameter format
      setParameters({
        series: incomingData.series,
        productType: incomingData.productType,
        width: incomingData.width,
        height: incomingData.height,
        glassType: incomingData.glassType,
        frameColor: incomingData.frameColor,
        configuration: incomingData.configuration,
      })
      
      // Clear the location state to prevent re-initialization on component updates
      window.history.replaceState({}, document.title)
      
      // Show success message
      toast.success('Unit parameters loaded - ready to design!')
      // Show success message
      toast.success('Unit parameters loaded - ready to design!')
    }
  }, [location.state, setParameters, toast])
  
  // Refs for synchronized scrolling
  const leftPanelRef = useRef<HTMLDivElement>(null)
  const rightPanelRef = useRef<HTMLDivElement>(null)
  const isSyncingRef = useRef(false)
  const scrollAnimationFrameRef = useRef<number | null>(null)
  
  // Handle auto-generation with React Query
  const { refetch, isFetching } = useQuery({
    queryKey: ['drawing', parameters],
    queryFn: async () => {
      setIsGenerating(true)
      try {
        const result = await generateDrawing(parameters)
        return result.drawing || result
      } finally {
        setIsGenerating(false)
      }
    },
    enabled: false,
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  })
  
  // Trigger drawing generation when parameters change (if autoUpdate is enabled)
  useEffect(() => {
    if (autoUpdate) {
      refetch()
    }
  }, [parameters, autoUpdate, refetch])

  // Update store when drawing changes from API
  useEffect(() => {
    if (!isFetching && drawing) {
      setDrawing(drawing)
    }
  }, [isFetching, drawing, setDrawing])
  
  // Debounced auto-generation
  const debouncedGenerate = debounce(async () => {
    if (parameters.series && parameters.width && parameters.height) {
      setIsGenerating(true)
      try {
        const result = await generateDrawing(parameters)
        const drawingData = result.drawing || result
        setDrawing(drawingData)
      } catch (error) {
        console.error('Failed to generate:', error)
        toast.error('Failed to generate drawing')
      } finally {
        setIsGenerating(false)
      }
    }
  }, 800)
  
  // Auto-generate when parameters change
  useEffect(() => {
    if (autoUpdate) {
      debouncedGenerate()
    }
  }, [parameters, autoUpdate])
  
  // Synchronized scrolling between left and right panels using requestAnimationFrame
  useEffect(() => {
    const leftPanel = leftPanelRef.current
    const rightPanel = rightPanelRef.current
    
    if (!leftPanel || !rightPanel) return
    
    // Debounced scroll handler to prevent excessive updates
    const debouncedSyncScroll = debounce((sourcePanel: HTMLDivElement, targetPanel: HTMLDivElement) => {
      // Calculate scroll ratio to maintain proportional scrolling
      const scrollHeight = sourcePanel.scrollHeight - sourcePanel.clientHeight
      if (scrollHeight === 0) return // Prevent division by zero
      
      const scrollRatio = sourcePanel.scrollTop / scrollHeight
      const targetScrollHeight = targetPanel.scrollHeight - targetPanel.clientHeight
      targetPanel.scrollTop = scrollRatio * targetScrollHeight
    }, 16, { leading: true, trailing: true }) // ~60fps (16ms)
    
    const handleLeftScroll = () => {
      isSyncingRef.current = true
      if (scrollAnimationFrameRef.current) {
        cancelAnimationFrame(scrollAnimationFrameRef.current)
      }
      scrollAnimationFrameRef.current = requestAnimationFrame(() => {
        debouncedSyncScroll(leftPanel, rightPanel)
        isSyncingRef.current = false
      })
    }
    
    const handleRightScroll = () => {
      isSyncingRef.current = true
      if (scrollAnimationFrameRef.current) {
        cancelAnimationFrame(scrollAnimationFrameRef.current)
      }
      scrollAnimationFrameRef.current = requestAnimationFrame(() => {
        debouncedSyncScroll(rightPanel, leftPanel)
        isSyncingRef.current = false
      })
    }
    
    // Add scroll event listeners
    leftPanel.addEventListener('scroll', handleLeftScroll, { passive: true })
    rightPanel.addEventListener('scroll', handleRightScroll, { passive: true })
    
    // Cleanup
    return () => {
      leftPanel.removeEventListener('scroll', handleLeftScroll)
      rightPanel.removeEventListener('scroll', handleRightScroll)
      if (scrollAnimationFrameRef.current) {
        cancelAnimationFrame(scrollAnimationFrameRef.current)
      }
    }
  }, [])
  
  // Manual generation (skips debounce)
  const generateNow = async () => {
    if (!parameters.series || !parameters.width || !parameters.height) {
      toast.error('Please fill in required parameters')
      return
    }
    setIsGenerating(true)
    try {
      const result = await generateDrawing(parameters)
      const drawingData = result.drawing || result
      setDrawing(drawingData)
      toast.success('Drawing generated!')
    } catch (error) {
      console.error('Failed to generate:', error)
      toast.error('Failed to generate drawing')
    } finally {
      setIsGenerating(false)
    }
  }
  
  useKeyboardShortcuts({
    onGenerateNow: () => { generateNow() },
    onExportPDF: () => setShowExportModal(true),
    onPresentationMode: () => setPresentationMode(!presentationMode),
  })
  
  return (
    <>
      {/* Header */}
      <header className="bg-raven-white border-b border-raven-border-light shadow-sm">
        <div className="px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            {projectId && (
              <button
                onClick={() => navigate('/')}
                className="text-raven-text-secondary hover:text-raven-black transition-colors"
                title="Back to Projects"
              >
                ← Back
              </button>
            )}
            <div>
              {/* Replaced Text with Logo Image */}
              <img 
                src="/raven-logo.PNG" 
                alt="Raven Design Studio" 
                className="h-10 w-auto object-contain" 
              />
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Generate PDF Button */}
            <button
              onClick={async () => {
                try {
                  toast.success('Generating PDF...')
                  
                  // 1. Find the canvas container (includes canvas + SVG overlays)
                  const canvas = document.querySelector('canvas')
                  if (!canvas) {
                    toast.error('No drawing found to export')
                    return
                  }
                  
                  // 2. Get the parent container that includes the elevation SVG overlay
                  const drawingContainer = canvas.parentElement
                  if (!drawingContainer) {
                    toast.error('Drawing container not found')
                    return
                  }
                  
                  // 3. Capture the entire container (canvas + SVG overlays) using html2canvas
                  const capturedCanvas = await html2canvas(drawingContainer, {
                    backgroundColor: '#ffffff',
                    scale: 2, // Higher quality
                    useCORS: true,
                    logging: false,
                  })
                  
                  // 4. Create PDF (Landscape, Millimeters, A3 size)
                  const pdf = new jsPDF({
                    orientation: 'landscape',
                    unit: 'mm',
                    format: 'a3'
                  })

                  // 5. Convert captured canvas to image data
                  const imgData = capturedCanvas.toDataURL('image/png', 1)

                  // 6. Calculate dimensions (A3 is 420mm x 297mm)
                  const pdfWidth = 420
                  const pdfHeight = 297
                  const margin = 10
                  
                  // 7. Add image to PDF with margins
                  pdf.addImage(imgData, 'PNG', margin, margin, pdfWidth - (margin * 2), pdfHeight - (margin * 2))

                  // 8. Generate filename and save
                  const filename = `${parameters.itemNumber || 'drawing'}_${parameters.series || 'custom'}.pdf`
                  pdf.save(filename)
                  
                  toast.success('PDF generated with elevation view!')
                } catch (err) {
                  console.error("PDF generation error:", err)
                  toast.error("Failed to generate PDF. Please try again.")
                }
              }}
              disabled={!drawing}
              className="btn-primary px-4 py-2 rounded-lg disabled:opacity-60 disabled:cursor-not-allowed font-medium transition-colors"
            >
              📄 Generate PDF
            </button>
            
            <button
              onClick={() => setPresentationMode(true)}
              className="btn-secondary px-4 py-2 rounded-lg font-medium transition-colors"
            >
              👁️ Presentation
            </button>
            <QuickExport drawing={drawing} parameters={parameters} />
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <div className={`flex-1 overflow-hidden ${styles.mainContent} ${styles.canvasView}`}>
        {/* Canvas View - 2 Column Layout with Sticky Canvas */}
        <div className={styles.canvasViewLayout}>
            {/* Left: Parameter Panel (30%) */}
            <div ref={leftPanelRef} className={styles.leftPanel}>
              <SmartParameterPanel />
            </div>
            
            {/* Right: Drawing Display (70%) with Sticky Canvas */}
            <div ref={rightPanelRef} className={styles.rightPanel}>
              <CanvasDrawingPreview
                selectedFrameView={selectedFrameView}
                presentationMode={presentationMode}
                onPresentationMode={() => setPresentationMode(!presentationMode)}
                parameters={{
                  series: parameters.series,
                  width: parameters.width,
                  height: parameters.height,
                  productType: parameters.productType || 'CASEMENT',
                  glassType: parameters.glassType || 'Clear Low E',
                  frameColor: parameters.frameColor || 'White',
                  configuration: parameters.configuration || 'O',
                  itemNumber: parameters.itemNumber,
                  panelCount: parameters.panelCount || 1,
                }}
              />
            </div>
          </div>
      </div>
      
      {/* Export Modal */}
      {showExportModal && (
        <div className="fixed inset-0 bg-raven-black/50 flex items-center justify-center z-50">
          <div className="bg-raven-white rounded-lg shadow-lg p-8 max-w-md w-full border border-raven-border-light">
            <h3 className="text-xl font-bold text-raven-black mb-4">Export Drawing</h3>
            
            <div className="space-y-3 mb-6">
              <button
                onClick={async () => {
                  try {
                    // Capture the full drawing container (canvas + SVG overlays)
                    const container = document.getElementById('drawing-preview-container') || document.querySelector('canvas')?.parentElement
                    if (!container) {
                      toast.error('Drawing container not found')
                      return
                    }

                    const captured = await html2canvas(container as HTMLElement, {
                      backgroundColor: '#ffffff',
                      scale: 2,
                      useCORS: true,
                      logging: false,
                    })

                    const dataUrl = captured.toDataURL('image/png', 1)
                    const link = document.createElement('a')
                    const timestamp = new Date().toISOString().split('T')[0]
                    link.download = `${parameters.poNumber || 'drawing'}_${parameters.itemNumber || 'item'}_${timestamp}.png`
                    link.href = dataUrl
                    link.click()
                    toast.success('PNG exported successfully!')
                    setShowExportModal(false)
                  } catch (err) {
                    console.error('PNG export error:', err)
                    toast.error('Failed to export PNG')
                  }
                }}
                className="w-full p-4 text-left rounded-lg border border-raven-border-light hover:bg-raven-bg-secondary transition-colors hover:shadow-sm"
              >
                <div className="font-medium text-raven-black">📥 Export as PNG</div>
                <div className="text-xs text-raven-text-secondary">Fast, easy sharing</div>
              </button>
              
              <button
                onClick={async () => {
                  try {
                    const canvas = document.querySelector('canvas')
                    if (!canvas) {
                      toast.error('No drawing found to export')
                      return
                    }
                    
                    // Get the container with canvas + SVG overlays
                    const drawingContainer = canvas.parentElement
                    if (!drawingContainer) {
                      toast.error('Drawing container not found')
                      return
                    }
                    
                    // Capture complete drawing (canvas + elevation SVG)
                    const capturedCanvas = await html2canvas(drawingContainer, {
                      backgroundColor: '#ffffff',
                      scale: 2,
                      useCORS: true,
                      logging: false,
                    })
                    
                    // Create PDF from captured image
                    const pdf = new jsPDF({
                      orientation: 'landscape',
                      unit: 'mm',
                      format: 'a3'
                    })

                    const imgData = capturedCanvas.toDataURL('image/png', 1)

                    // A3 dimensions with margins
                    const pdfWidth = 420
                    const pdfHeight = 297
                    const margin = 10
                    
                    pdf.addImage(imgData, 'PNG', margin, margin, pdfWidth - (margin * 2), pdfHeight - (margin * 2))

                    // Save with descriptive filename
                    const filename = `${parameters.itemNumber || 'drawing'}_${parameters.series || 'custom'}.pdf`
                    pdf.save(filename)
                    
                    toast.success('PDF exported successfully!')
                    setShowExportModal(false)
                  } catch (err) {
                    console.error('PDF export error:', err)
                    toast.error('Failed to export PDF')
                  }
                }}
                className="w-full p-4 text-left rounded-lg border border-raven-border-light hover:bg-raven-bg-secondary transition-colors hover:shadow-sm"
              >
                <div className="font-medium text-raven-black">📄 Export as PDF</div>
                <div className="text-xs text-raven-text-secondary">Professional reference layout (A3 Landscape)</div>
              </button>
            </div>
            
            <button
              onClick={() => setShowExportModal(false)}
              className="w-full btn-secondary px-4 py-2 rounded-lg font-medium"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </>
  )
}
