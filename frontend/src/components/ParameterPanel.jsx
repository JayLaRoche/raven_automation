import { useQuery } from '@tanstack/react-query'
import { getFrameSeries } from '../services/api'

export default function ParameterPanel({ parameters, setParameters, onGenerate }) {
  const { data: frameSeries } = useQuery({
    queryKey: ['frameSeries'],
    queryFn: getFrameSeries,
  })

  const productTypes = [
    'FIXED',
    'CASEMENT',
    'DOUBLE CASEMENT',
    'AWNING',
    'SLIDER 2-PANEL',
    'SLIDER 3-PANEL',
    'SLIDER 4-PANEL',
    'HINGED DOOR',
    'BIFOLD DOOR',
  ]

  const glassTypes = [
    'Single Pane Clear',
    'Dual Pane Clear',
    'Low-E',
    'Low-E + Argon',
    'Tempered',
    'Laminated',
  ]

  const frameColors = ['White', 'Bronze', 'Black', 'Mill Finish', 'Custom']

  const handleChange = (field, value) => {
    setParameters((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-6">Parameters</h2>

      {/* Frame Series */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Frame Series
        </label>
        <select
          value={parameters.series}
          onChange={(e) => handleChange('series', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {frameSeries?.series && frameSeries.series.map((series) => (
            <option key={series} value={series}>
              {series}
            </option>
          ))}
        </select>
      </div>

      {/* Product Type */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Product Type
        </label>
        <select
          value={parameters.productType}
          onChange={(e) => handleChange('productType', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {productTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      {/* Dimensions */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Width (inches)
        </label>
        <input
          type="number"
          value={parameters.width}
          onChange={(e) => handleChange('width', parseFloat(e.target.value))}
          step="0.5"
          min="12"
          max="300"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Height (inches)
        </label>
        <input
          type="number"
          value={parameters.height}
          onChange={(e) => handleChange('height', parseFloat(e.target.value))}
          step="0.5"
          min="12"
          max="300"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Glass Type */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Glass Type
        </label>
        <select
          value={parameters.glassType}
          onChange={(e) => handleChange('glassType', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {glassTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      {/* Frame Color */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Frame Color
        </label>
        <select
          value={parameters.frameColor}
          onChange={(e) => handleChange('frameColor', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {frameColors.map((color) => (
            <option key={color} value={color}>
              {color}
            </option>
          ))}
        </select>
      </div>

      {/* Grids */}
      <div className="mb-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={parameters.hasGrids}
            onChange={(e) => handleChange('hasGrids', e.target.checked)}
            className="mr-2 h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
          />
          <span className="text-sm font-medium text-gray-700">Include Grids</span>
        </label>
      </div>

      {/* Project Info */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Item Number
        </label>
        <input
          type="text"
          value={parameters.itemNumber}
          onChange={(e) => handleChange('itemNumber', e.target.value)}
          placeholder="W-001"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          PO Number
        </label>
        <input
          type="text"
          value={parameters.poNumber}
          onChange={(e) => handleChange('poNumber', e.target.value)}
          placeholder="PO-2024-001"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      {/* Generate Button */}
      <button
        onClick={onGenerate}
        className="w-full bg-primary text-white px-4 py-2 rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
      >
        Generate Drawing
      </button>
    </div>
  )
}
