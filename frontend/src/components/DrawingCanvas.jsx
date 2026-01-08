import { useEffect, useRef } from 'react'

export default function DrawingCanvas({ drawing, parameters }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    if (!drawing || !canvasRef.current) {
      return
    }

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw background
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Draw frame outline
    const scale = 5 // pixels per inch
    const width = (parameters?.width ?? 36) * scale
    const height = (parameters?.height ?? 48) * scale
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
    if (parameters?.hasGrids) {
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
    ctx.font = '12px Arial'
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

    ctx.font = '12px Arial'
    ctx.fillText(
      `Series: ${parameters.series}`,
      startX + 10,
      startY + height + 100
    )
    ctx.fillText(
      `Product: ${parameters.productType}`,
      startX + 10,
      startY + height + 115
    )
    ctx.fillText(
      `Item #: ${parameters.itemNumber || 'N/A'}`,
      startX + width / 2,
      startY + height + 100
    )
    ctx.fillText(
      `Glass: ${parameters.glassType}`,
      startX + width / 2,
      startY + height + 115
    )
    ctx.fillText(
      `Color: ${parameters.frameColor}`,
      startX + width / 2,
      startY + height + 130
    )

  }, [drawing, parameters])

  const handleExport = () => {
    if (!canvasRef.current) return

    const link = document.createElement('a')
    link.download = `drawing-${parameters.itemNumber || 'untitled'}.png`
    link.href = canvasRef.current.toDataURL()
    link.click()
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Drawing Preview</h2>
        <button
          onClick={handleExport}
          disabled={!drawing}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Export PNG
        </button>
      </div>

      <div className="border border-gray-300 rounded overflow-auto bg-gray-50">
        {drawing ? (
          <canvas
            ref={canvasRef}
            width={800}
            height={1000}
            className="mx-auto"
          />
        ) : (
          <div className="h-96 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <p className="text-lg mb-2">No drawing generated</p>
              <p className="text-sm">
                Configure parameters and click "Generate Drawing"
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
