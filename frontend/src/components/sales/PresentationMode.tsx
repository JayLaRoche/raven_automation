import { DrawingParams } from '../../store/drawingStore'

interface PresentationModeProps {
  drawing: any
  parameters: DrawingParams
  onExit: () => void
}

export function PresentationMode({ drawing, parameters, onExit }: PresentationModeProps) {
  const scale = 5
  const width = (parameters.width ?? 0) * scale
  const height = (parameters.height ?? 0) * scale
  
  return (
    <div className="w-full h-screen bg-black flex items-center justify-center relative overflow-hidden">
      {/* Full-Screen Drawing */}
      <div className="flex items-center justify-center w-full h-full">
        <canvas
          width={1200}
          height={1400}
          className="max-w-full max-h-full object-contain"
          ref={(canvas) => {
            if (canvas && drawing) {
              const ctx = canvas.getContext('2d')
              if (!ctx) return
              
              // Clear canvas
              ctx.clearRect(0, 0, canvas.width, canvas.height)
              
              // Draw background
              ctx.fillStyle = '#ffffff'
              ctx.fillRect(0, 0, canvas.width, canvas.height)
              
              // Draw frame outline
              const startX = 100
              const startY = 100
              
              // Outer frame
              ctx.strokeStyle = '#000000'
              ctx.lineWidth = 3
              ctx.strokeRect(startX, startY, width, height)
              
              // Inner frame (glass opening)
              const frameWidth = 10
              ctx.lineWidth = 2
              ctx.strokeRect(
                startX + frameWidth,
                startY + frameWidth,
                width - frameWidth * 2,
                height - frameWidth * 2
              )
              
              // Draw grids if enabled
              if (parameters.hasGrids) {
                ctx.strokeStyle = '#999999'
                ctx.lineWidth = 1
                ctx.setLineDash([5, 5])
                
                const gridHeight = height / 3
                for (let i = 1; i < 3; i++) {
                  ctx.beginPath()
                  ctx.moveTo(startX + frameWidth, startY + gridHeight * i)
                  ctx.lineTo(startX + width - frameWidth, startY + gridHeight * i)
                  ctx.stroke()
                }
                
                const gridWidth = width / 2
                ctx.beginPath()
                ctx.moveTo(startX + gridWidth, startY + frameWidth)
                ctx.lineTo(startX + gridWidth, startY + height - frameWidth)
                ctx.stroke()
                
                ctx.setLineDash([])
              }
              
              // Draw dimensions
              ctx.fillStyle = '#000000'
              ctx.font = 'bold 24px Arial'
              ctx.textAlign = 'center'
              
              ctx.fillText(
                `${parameters.width}"`,
                startX + width / 2,
                startY + height + 50
              )
              
              ctx.save()
              ctx.translate(startX - 50, startY + height / 2)
              ctx.rotate(-Math.PI / 2)
              ctx.textAlign = 'center'
              ctx.fillText(`${parameters.height}"`, 0, 0)
              ctx.restore()
              
              // Title block (larger for presentation)
              ctx.fillStyle = '#f3f4f6'
              ctx.fillRect(startX, startY + height + 80, width, 120)
              ctx.strokeStyle = '#000000'
              ctx.lineWidth = 2
              ctx.strokeRect(startX, startY + height + 80, width, 120)
              
              ctx.fillStyle = '#000000'
              ctx.font = 'bold 28px Arial'
              ctx.textAlign = 'left'
              ctx.fillText('RAVEN CUSTOM GLASS', startX + 15, startY + height + 120)
              
              ctx.font = '16px Arial'
              ctx.fillText(`Series: ${parameters.series}`, startX + 15, startY + height + 150)
              ctx.fillText(`Product: ${parameters.productType}`, startX + 15, startY + height + 175)
              ctx.fillText(`Item #: ${parameters.itemNumber || 'N/A'}`, startX + width / 2 + 15, startY + height + 150)
              ctx.fillText(`Glass: ${parameters.glassType}`, startX + width / 2 + 15, startY + height + 175)
            }
          }}
        />
      </div>
      
      {/* Exit Button */}
      <button
        onClick={onExit}
        className="absolute top-8 right-8 px-6 py-3 bg-white text-black rounded-lg font-bold hover:bg-gray-200 text-lg"
      >
        ✕ Exit
      </button>
      
      {/* Keyboard Hint */}
      <div className="absolute bottom-8 left-8 text-white text-sm opacity-70">
        Press <kbd className="bg-white/20 px-2 py-1 rounded">Cmd+P</kbd> or click Exit to return
      </div>
    </div>
  )
}
