import { useQuery } from '@tanstack/react-query'
import { useDrawingStore } from '../../store/drawingStore'
import { getFrameSeriesWithImages } from '../../services/api'
import { Button } from '../ui/Button'
import { useState } from 'react'

interface FrameSeries {
  id: string
  name: string
  series: string
  image_url?: string
}

const QUICK_PRESETS = [
  {
    name: 'Standard Bedroom',
    params: { series: '86', productType: 'CASEMENT', width: 48, height: 60, glassType: 'Dual Pane Clear', frameColor: 'White' },
  },
  {
    name: 'Patio Door',
    params: { series: '135', productType: 'SLIDER 2-PANEL', width: 96, height: 108, glassType: 'Dual Pane Clear', frameColor: 'White' },
  },
  {
    name: 'Entry Door',
    params: { series: '65', productType: 'HINGED DOOR', width: 36, height: 108, glassType: 'Tempered', frameColor: 'Bronze' },
  },
]

export function SmartParameterPanel() {
  const { parameters, setParameters, autoUpdate, setAutoUpdate, selectedFrameView, setSelectedFrameView } = useDrawingStore()
  const [isSyncing, setIsSyncing] = useState(false)
  const [syncMessage, setSyncMessage] = useState<string | null>(null)
  
  // Fetch frame series with images from database
  const { data: frameSeriesData = { series: [] }, isLoading: isLoadingFrameSeries } = useQuery<{ series: FrameSeries[] }>({
    queryKey: ['frameSeriesWithImages'],
    queryFn: getFrameSeriesWithImages,
  })

  const frameSeries = frameSeriesData?.series || []
  
  // Helper to get selected series data
  const selectedSeriesData = frameSeries.find((s) => s.series === parameters.series)
  
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
  
  const handlePreset = (preset: typeof QUICK_PRESETS[0]) => {
    setParameters(preset.params)
  }
  
  const handleDimensionChange = (field: 'width' | 'height', value: number) => {
    const min = 12
    const max = 300
    const newValue = Math.max(min, Math.min(max, value))
    setParameters({ [field]: newValue })
  }
  
  const handleDimensionIncrement = (field: 'width' | 'height', increment: number) => {
    const currentValue = field === 'width' ? parameters.width : parameters.height
    handleDimensionChange(field, (currentValue ?? 36) + increment)
  }
  
  const handleSyncFrameData = async () => {
    setIsSyncing(true)
    setSyncMessage(null)
    try {
      const response = await fetch('http://localhost:8000/api/frames/sync-now', {
        method: 'POST',
      })
      const data = await response.json()
      if (data.status === 'success' || data.result?.status === 'success') {
        setSyncMessage('✓ Frame library synced successfully')
        setTimeout(() => setSyncMessage(null), 3000)
      } else {
        setSyncMessage('✗ Sync failed - check console')
      }
    } catch (error) {
      setSyncMessage('✗ Network error during sync')
    } finally {
      setIsSyncing(false)
    }
  }
  
  return (
    <div className="bg-white rounded-lg shadow-sm p-6 space-y-6 h-full overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Design Window</h2>
        <p className="text-sm text-gray-600">Configure parameters to auto-generate drawing</p>
      </div>
      
      {/* Quick Presets */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-3">Quick Presets</label>
        <div className="grid grid-cols-1 gap-2">
          {QUICK_PRESETS.map((preset) => (
            <button
              key={preset.name}
              onClick={() => handlePreset(preset)}
              className="p-3 text-left rounded-lg border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition-colors"
            >
              <div className="font-medium text-gray-900">{preset.name}</div>
              <div className="text-xs text-gray-600">
                {preset.params.width}" × {preset.params.height}" | {preset.params.series}
              </div>
            </button>
          ))}
        </div>
      </div>
      
      {/* Frame Series Selector - Dropdown with Images from Database */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="block text-sm font-semibold text-gray-700">Frame Series</label>
          <button
            onClick={handleSyncFrameData}
            disabled={isSyncing}
            className="text-xs px-2 py-1 bg-blue-50 text-blue-600 border border-blue-200 rounded hover:bg-blue-100 disabled:opacity-50"
          >
            {isSyncing ? 'Syncing...' : '↻ Sync'}
          </button>
        </div>
        {syncMessage && (
          <div className="text-xs mb-2 p-2 bg-green-50 text-green-700 border border-green-200 rounded">
            {syncMessage}
          </div>
        )}
        {isLoadingFrameSeries ? (
          <div className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">
            Loading frame series...
          </div>
        ) : (
          <div className="space-y-2">
            <select
              value={parameters.series}
              onChange={(e) => setParameters({ series: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium"
            >
              <option value="">-- Select Frame Series --</option>
              {frameSeries.map((series: FrameSeries) => (
                <option key={series.id} value={series.series}>
                  {series.name}
                </option>
              ))}
            </select>

            {/* Frame Series Detail Views - HEAD, SILL, JAMB */}
            {parameters.series && (
              <div className="border border-gray-200 rounded-lg p-3 bg-gray-50 mt-2">
                <p className="text-xs font-medium text-gray-500 mb-2">Frame Details:</p>
                <div className="grid grid-cols-3 gap-2">
                  {['HEAD', 'SILL', 'JAMB'].map((view) => {
                    // 1. clean the series name (e.g. "Series 86" -> "86")
                    const cleanSeries = parameters.series?.toString().replace(/Series\s*/i, '').trim() || '';
                    
                    // 2. Construct FULL URL pointing to the Backend Port (8000)
                    const imageUrl = `http://localhost:8000/static/frames/series_${cleanSeries}_${view}.png`;

                    return (
                      <div key={view} className="flex flex-col items-center group">
                        <div className="w-full h-20 bg-white rounded border border-gray-200 flex items-center justify-center overflow-hidden relative shadow-sm hover:border-blue-400 transition-colors">
                          <img
                            src={imageUrl}
                            alt={`${view} View`}
                            className="w-full h-full object-contain p-1"
                            crossOrigin="anonymous" 
                            onError={(e) => {
                              // Fallback if image is missing
                              e.currentTarget.style.display = 'none';
                              e.currentTarget.parentElement.classList.add('bg-gray-50');
                              e.currentTarget.parentElement.innerHTML = `<span class="text-[10px] text-gray-400 select-none">No Image</span>`;
                            }}
                          />
                        </div>
                        <span className="text-[9px] font-bold text-gray-500 uppercase mt-1">{view}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Frame View Selector - Shows HEAD/SILL/JAMB */}
      {parameters.series && (
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-3">Frame View</label>
          <div className="grid grid-cols-3 gap-2">
            {['head', 'sill', 'jamb'].map((view) => (
              <button
                key={view}
                onClick={() => setSelectedFrameView(view as 'head' | 'sill' | 'jamb')}
                className={`py-2 px-3 rounded-lg border-2 transition-all text-sm font-medium uppercase tracking-wider ${
                  selectedFrameView === view
                    ? 'border-blue-600 bg-blue-50 text-blue-900 shadow-md'
                    : 'border-gray-200 hover:border-gray-400 text-gray-700'
                }`}
              >
                {view}
              </button>
            ))}
          </div>
        </div>
      )}
      
      {/* Product Type */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">Product Type</label>
        <select
          value={parameters.productType}
          onChange={(e) => setParameters({ productType: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {productTypes.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>
      
      {/* Glass Type */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">Glass Type</label>
        <select
          value={parameters.glassType}
          onChange={(e) => setParameters({ glassType: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {glassTypes.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>
      
      {/* Frame Color */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">Frame Color</label>
        <select
          value={parameters.frameColor}
          onChange={(e) => setParameters({ frameColor: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {frameColors.map((color) => (
            <option key={color} value={color}>{color}</option>
          ))}
        </select>
      </div>
      
      {/* Project Info */}
      <div className="space-y-3">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Item Number</label>
          <input
            type="text"
            value={parameters.itemNumber}
            onChange={(e) => setParameters({ itemNumber: e.target.value })}
            placeholder="W-001"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">PO Number</label>
          <input
            type="text"
            value={parameters.poNumber}
            onChange={(e) => setParameters({ poNumber: e.target.value })}
            placeholder="PO-2024-001"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Canvas Size Divider */}
      <div className="border-t-2 border-gray-200 pt-6">
        <h3 className="text-sm font-semibold text-gray-700 mb-4">Canvas Size</h3>
      </div>
      
      {/* Dimensions - Moved to Bottom */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Width</label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleDimensionIncrement('width', -1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-lg"
            >
              −
            </button>
            <input
              type="number"
              value={parameters.width ?? 36}
              onChange={(e) => handleDimensionChange('width', Number.parseFloat(e.target.value) || 0)}
              step="0.5"
              min="12"
              max="300"
              className="flex-1 h-12 text-center text-xl font-semibold border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={() => handleDimensionIncrement('width', 1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-lg"
            >
              +
            </button>
            <span className="text-gray-600 font-medium">in</span>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Height</label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleDimensionIncrement('height', -1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-lg"
            >
              −
            </button>
            <input
              type="number"
              value={parameters.height ?? 48}
              onChange={(e) => handleDimensionChange('height', Number.parseFloat(e.target.value) || 0)}
              step="0.5"
              min="12"
              max="300"
              className="flex-1 h-12 text-center text-xl font-semibold border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={() => handleDimensionIncrement('height', 1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-lg"
            >
              +
            </button>
            <span className="text-gray-600 font-medium">in</span>
          </div>
        </div>
      </div>
      
      {/* Auto-Update Toggle */}
      <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="text-xl">⚡</span>
          <span className="font-medium text-gray-900">Auto-Generate</span>
        </div>
        <button
          onClick={() => setAutoUpdate(!autoUpdate)}
          className={`w-12 h-7 rounded-full transition-colors ${
            autoUpdate ? 'bg-green-600' : 'bg-gray-300'
          } relative flex items-center justify-start overflow-hidden`}
        >
          <div className={`w-6 h-6 bg-white rounded-full transition-transform ${
            autoUpdate ? 'translate-x-6' : 'translate-x-0'
          }`} />
        </button>
      </div>
      
      {!autoUpdate && (
        <Button
          variant="success"
          size="lg"
          className="w-full"
          onClick={() => {
            // Manual generation handled in parent
          }}
        >
          🚀 Generate Now
        </Button>
      )}
    </div>
  )
}

