import { useState } from 'react'
import SmartParameterPanel from '../components/SmartParameterPanel'
import DrawingCanvas from '../components/DrawingCanvas'
import { generateDrawing } from '../services/api'

export default function DrawingGenerator() {
  const [parameters, setParameters] = useState({
    series: '65',
    productType: 'FIXED',
    width: 48,
    height: 60,
    glassType: 'Dual Pane Clear',
    frameColor: 'White',
    hasGrids: false,
    itemNumber: '',
    poNumber: '',
  })

  const [drawing, setDrawing] = useState(null)

  const handleGenerate = async () => {
    try {
      const result = await generateDrawing(parameters)
      // The API returns {success, drawing, status}
      // We need to pass drawing data to DrawingCanvas
      if (result?.drawing) {
        setDrawing(result.drawing)
      } else {
        setDrawing(result)
      }
      console.log('Drawing generated:', result)
    } catch (error) {
      console.error('Failed to generate drawing:', error)
      alert('Error generating drawing: ' + error.message)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Parameter Panel - Left Side */}
        <div className="lg:col-span-1">
          <SmartParameterPanel
            parameters={parameters}
            setParameters={setParameters}
            onParametersChange={handleGenerate}
          />
        </div>

        {/* Drawing Canvas - Right Side */}
        <div className="lg:col-span-2">
          <DrawingCanvas drawing={drawing} parameters={parameters} />
        </div>
      </div>
    </div>
  )
}
