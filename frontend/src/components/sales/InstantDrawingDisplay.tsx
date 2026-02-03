import { useEffect, useState } from 'react'
import { useDrawingStore } from '../../store/drawingStore'
import { LoadingSpinner } from '../ui/LoadingSpinner'
import { Button } from '../ui/Button'

interface DrawingDisplayProps {
  onPresentationMode?: () => void
}

export function InstantDrawingDisplay({ onPresentationMode }: DrawingDisplayProps) {
  const { drawing, isGenerating, parameters } = useDrawingStore()
  const [displayedDrawing, setDisplayedDrawing] = useState(drawing)
  const [isTransitioning, setIsTransitioning] = useState(false)
  
  // Smooth fade transition when drawing changes
  useEffect(() => {
    if (drawing && drawing !== displayedDrawing && !isGenerating) {
      setIsTransitioning(true)
      setTimeout(() => {
        setDisplayedDrawing(drawing)
        setIsTransitioning(false)
      }, 300)
    }
  }, [drawing, isGenerating, displayedDrawing])
  
  const scale = 5 // pixels per inch
  const width = (parameters.width ?? 0) * scale
  const height = (parameters.height ?? 0) * scale
  const canvasWidth = 800
  const canvasHeight = 1000
  
  return (
    <div className="relative bg-white rounded-lg shadow-sm p-6 h-full flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Drawing Preview</h2>
        <Button
          variant="ghost"
          size="md"
          onClick={onPresentationMode}
        >
          👁️ Present
        </Button>
      </div>
      
      {/* Drawing Canvas */}
      <div className="flex-1 relative bg-gray-50 rounded-lg border border-gray-200 overflow-auto flex items-center justify-center">
        {/* Loading Overlay */}
        {isGenerating && (
          <div className="absolute inset-0 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center z-10">
            <LoadingSpinner size="lg" />
            <p className="text-lg font-medium text-gray-900 mt-4">Generating drawing...</p>
            <p className="text-sm text-gray-600">~3 seconds</p>
          </div>
        )}
        
        {/* Drawing Content */}
        <div
          className={`transition-opacity duration-300 ${
            isTransitioning ? 'opacity-50' : 'opacity-100'
          }`}
        >
          {displayedDrawing || drawing ? (
            <canvas
              width={canvasWidth}
              height={canvasHeight}
              className="bg-white"
              ref={(canvas) => {
                if (canvas && (displayedDrawing || drawing)) {
                  const ctx = canvas.getContext('2d')
                  if (!ctx) return
                  
                  // Clear canvas
                  ctx.clearRect(0, 0, canvas.width, canvas.height)
                  
                  // Draw background
                  ctx.fillStyle = '#ffffff'
                  ctx.fillRect(0, 0, canvas.width, canvas.height)
                  
                  // Draw frame outline
                  const startX = 50
                  const startY = 50
                  
                  // Outer frame
                  ctx.strokeStyle = '#000000'
                  ctx.lineWidth = 2
                  ctx.strokeRect(startX, startY, width, height)
                  
                  // Inner frame (glass opening)
                  const frameWidth = 10 // 2 inches * 5 px/in
                  ctx.lineWidth = 1
                  ctx.strokeRect(
                    startX + frameWidth,
                    startY + frameWidth,
                    width - frameWidth * 2,
                    height - frameWidth * 2
                  )
                  
                  // Draw grids if enabled
                  if (parameters.hasGrids) {
                    ctx.strokeStyle = '#999999'
                    ctx.lineWidth = 0.5
                    ctx.setLineDash([5, 5])
                    
                    // Horizontal grids
                    const gridHeight = height / 3
                    for (let i = 1; i < 3; i++) {
                      ctx.beginPath()
                      ctx.moveTo(startX + frameWidth, startY + gridHeight * i)
                      ctx.lineTo(startX + width - frameWidth, startY + gridHeight * i)
                      ctx.stroke()
                    }
                    
                    // Vertical grids
                    const gridWidth = width / 2
                    ctx.beginPath()
                    ctx.moveTo(startX + gridWidth, startY + frameWidth)
                    ctx.lineTo(startX + gridWidth, startY + height - frameWidth)
                    ctx.stroke()
                    
                    ctx.setLineDash([])
                  }
                  
                  // Draw dimensions
                  ctx.fillStyle = '#000000'
                  ctx.font = 'bold 14px Arial'
                  ctx.textAlign = 'center'
                  
                  // Width dimension
                  ctx.fillText(
                    `${parameters.width}"`,
                    startX + width / 2,
                    startY + height + 30
                  )
                  
                  // Height dimension
                  ctx.save()
                  ctx.translate(startX - 30, startY + height / 2)
                  ctx.rotate(-Math.PI / 2)
                  ctx.textAlign = 'center'
                  ctx.fillText(`${parameters.height}"`, 0, 0)
                  ctx.restore()
                  
                  // Title block
                  ctx.fillStyle = '#f3f4f6'
                  ctx.fillRect(startX, startY + height + 60, width, 80)
                  ctx.strokeStyle = '#000000'
                  ctx.lineWidth = 1
                  ctx.strokeRect(startX, startY + height + 60, width, 80)
                  
                  ctx.fillStyle = '#000000'
                  ctx.font = 'bold 16px Arial'
                  ctx.textAlign = 'left'
                  ctx.fillText('RAVEN CUSTOM GLASS', startX + 10, startY + height + 80)
                  
                  ctx.font = '11px Arial'
                  ctx.fillText(`Series: ${parameters.series}`, startX + 10, startY + height + 100)
                  ctx.fillText(`Product: ${parameters.productType}`, startX + 10, startY + height + 115)
                  ctx.fillText(`Item #: ${parameters.itemNumber || 'N/A'}`, startX + width / 2, startY + height + 100)
                  ctx.fillText(`Glass: ${parameters.glassType}`, startX + width / 2, startY + height + 115)
                  ctx.fillText(`Color: ${parameters.frameColor}`, startX + width / 2, startY + height + 130)
                }
              }}
            />
          ) : (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">📐</div>
              <p className="text-xl font-medium text-gray-900">No drawing yet</p>
              <p className="text-sm text-gray-600 mt-2">Configure parameters to auto-generate</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Status Bar */}
      <div className="mt-4 flex justify-between items-center text-sm text-gray-600">
        <div>
          {isGenerating ? (
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" />
              Generating...
            </span>
          ) : displayedDrawing || drawing ? (
            <span className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-600 rounded-full" />
              Ready to export
            </span>
          ) : (
            <span>Waiting for input</span>
          )}
        </div>
        <button
          onClick={() => {
            if (displayedDrawing || drawing) {
              const canvas = document.querySelector('canvas') as HTMLCanvasElement
              if (canvas) {
                const link = document.createElement('a')
                link.download = `drawing-${parameters.itemNumber || 'untitled'}.png`
                link.href = canvas.toDataURL()
                link.click()
              }
            }
          }}
          disabled={!displayedDrawing && !drawing}
          className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-300"
        >
          💾 Export PNG
        </button>
      </div>
    </div>
  )
}
