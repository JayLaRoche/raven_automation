import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { useDrawingStore } from '../../store/drawingStore'
import { useKeyboardShortcuts } from '../../hooks/useKeyboardShortcuts'
import { useReferencePDFGeneration } from '../../hooks/useReferencePDFGeneration'
import { SmartParameterPanel } from './SmartParameterPanel'
import { CanvasDrawingPreview } from './CanvasDrawingPreview'
import { DrawingPDFViewer } from '../drawing/DrawingPDFViewer'
import { PresentationMode } from './PresentationMode'
import { QuickExport } from './QuickExport'
import styles from './SalesPresentation.module.css'

import { useToast } from '../ui/Toast'
import { generateDrawing } from '../../services/api'
import { debounce } from 'lodash-es'

export function SalesPresentation() {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { parameters, drawing, autoUpdate, presentationMode, setPresentationMode, setDrawing, setIsGenerating, selectedFrameView } = useDrawingStore()
  const { pdfUrl, isLoading: pdfLoading, error: pdfError, generatePDF } = useReferencePDFGeneration()
  const [showExportModal, setShowExportModal] = useState(false)
  const [viewMode, setViewMode] = useState<'canvas' | 'pdf'>('canvas')
  const [presentationModeLocal, setPresentationModeLocal] = useState(false)
  const toast = useToast()
  
  // Toggle presentation mode
  const togglePresentation = () => {
    setPresentationModeLocal(!presentationModeLocal)
  }
  
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
  
  if (presentationMode) {
    return (
      <PresentationMode
        drawing={drawing}
        parameters={parameters}
        onExit={() => setPresentationMode(false)}
      />
    )
  }
  
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
              <h1 className="text-2xl font-bold text-raven-black">Raven's Design Sandbox</h1>
              <p className="text-sm text-raven-text-secondary">CAD Drawing Generator</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            {/* View Mode Switcher */}
            <div className="flex items-center gap-2 bg-raven-bg-secondary p-1 rounded-lg">
              <button
                onClick={() => setViewMode('canvas')}
                className={`px-3 py-1 rounded transition-colors ${viewMode === 'canvas' ? 'bg-raven-white text-raven-black font-medium' : 'text-raven-text-secondary hover:text-raven-black'}`}
              >
                📐 Canvas
              </button>
              <button
                onClick={() => setViewMode('pdf')}
                className={`px-3 py-1 rounded transition-colors ${viewMode === 'pdf' ? 'bg-raven-white text-raven-black font-medium' : 'text-raven-text-secondary hover:text-raven-black'}`}
              >
                📄 PDF
              </button>
            </div>
            
            {/* Generate PDF Button */}
            <button
              onClick={() => {
                if (!parameters.series || !parameters.width || !parameters.height) {
                  toast.error('Please fill in required parameters')
                  return
                }
                generatePDF({
                  series: parameters.series,
                  product_type: parameters.productType || 'FIXED',
                  width: parameters.width,
                  height: parameters.height,
                  glass_type: parameters.glassType || 'Clear Low E',
                  frame_color: parameters.frameColor || 'Black',
                  configuration: parameters.configuration || 'O',
                  item_number: parameters.itemNumber || 'P001',
                  po_number: parameters.poNumber || '',
                  notes: parameters.notes || '',
                })
                setViewMode('pdf')
              }}
              disabled={pdfLoading || !parameters.series || !parameters.width}
              className="btn-primary px-4 py-2 rounded-lg disabled:opacity-60 disabled:cursor-not-allowed font-medium transition-colors"
            >
              {pdfLoading ? '⏳ Generating PDF...' : '📄 Generate PDF'}
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
      <div className={`flex-1 overflow-hidden ${styles.mainContent} ${viewMode === 'canvas' ? styles.canvasView : styles.pdfView}`}>
        {viewMode === 'pdf' ? (
          // PDF View (Full Width)
          <div className="h-full p-4 bg-raven-bg-secondary">
            <DrawingPDFViewer 
              pdfUrl={pdfUrl}
              loading={pdfLoading}
              error={pdfError}
            />
          </div>
        ) : (
          // Canvas View - 2 Column Layout with Sticky Canvas
          <div className={styles.canvasViewLayout}>
            {/* Left: Parameter Panel (30%) */}
            <div ref={leftPanelRef} className={styles.leftPanel}>
              <SmartParameterPanel />
            </div>
            
            {/* Right: Drawing Display (70%) with Sticky Canvas */}
            <div ref={rightPanelRef} className={styles.rightPanel}>
              <CanvasDrawingPreview
                selectedFrameView={selectedFrameView}
                presentationMode={presentationModeLocal}
                onPresentationMode={togglePresentation}
                parameters={{
                  series: parameters.series,
                  width: parameters.width,
                  height: parameters.height,
                  productType: parameters.productType || 'CASEMENT',
                  glassType: parameters.glassType || 'Clear Low E',
                  frameColor: parameters.frameColor || 'White',
                  configuration: parameters.configuration || 'O',
                  itemNumber: parameters.itemNumber,
                }}
              />
            </div>
          </div>
        )}
      </div>
      
      {/* Export Modal */}
      {showExportModal && (
        <div className="fixed inset-0 bg-raven-black/50 flex items-center justify-center z-50">
          <div className="bg-raven-white rounded-lg shadow-lg p-8 max-w-md w-full border border-raven-border-light">
            <h3 className="text-xl font-bold text-raven-black mb-4">Export Drawing</h3>
            
            <div className="space-y-3 mb-6">
              <button
                onClick={() => {
                  const canvas = document.querySelector('canvas')
                  if (canvas instanceof HTMLCanvasElement) {
                    const link = document.createElement('a')
                    const timestamp = new Date().toISOString().split('T')[0]
                    link.download = `${parameters.poNumber || 'drawing'}_${parameters.itemNumber || 'item'}_${timestamp}.png`
                    link.href = canvas.toDataURL()
                    link.click()
                    toast.success('PNG exported successfully!')
                    setShowExportModal(false)
                  }
                }}
                className="w-full p-4 text-left rounded-lg border border-raven-border-light hover:bg-raven-bg-secondary transition-colors hover:shadow-sm"
              >
                <div className="font-medium text-raven-black">📥 Export as PNG</div>
                <div className="text-xs text-raven-text-secondary">Fast, easy sharing</div>
              </button>
              
              <button
                onClick={() => {
                  if (!parameters.series || !parameters.width || !parameters.height) {
                    toast.error('Please fill in required parameters')
                    return
                  }
                  generatePDF({
                    series: parameters.series,
                    product_type: parameters.productType || 'FIXED',
                    width: parameters.width,
                    height: parameters.height,
                    glass_type: parameters.glassType || 'Clear Low E',
                    frame_color: parameters.frameColor || 'Black',
                    configuration: parameters.configuration || 'O',
                    item_number: parameters.itemNumber || 'P001',
                    po_number: parameters.poNumber || '',
                    notes: parameters.notes || '',
                  })
                  toast.success('PDF generated! Switch to PDF view to download.')
                  setShowExportModal(false)
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
