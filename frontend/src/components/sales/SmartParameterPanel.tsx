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
    name: 'Standard Sliding Window',
    params: { series: '86', productType: 'Standard Sliding Window', width: 48, height: 60, glassType: 'Dual Pane Clear', frameColor: 'White' },
  },
  {
    name: 'Pivot Door',
    params: { series: '135', productType: 'Pivot Door', width: 36, height: 96, glassType: 'Dual Pane Clear', frameColor: 'Bronze' },
  },
  {
    name: 'Slim Frame Sliding Door',
    params: { series: '65', productType: 'Slim Frame Sliding Door', width: 96, height: 108, glassType: 'Low-E', frameColor: 'Black' },
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
  
  const windowTypes = [
    'Standard Sliding Window',
    'Folding Window',
    'Fold Up Window',
    'Slim Frame Casement Window',
    'Fixed Window',
  ]

  const doorTypes = [
    'Standard Sliding Door',
    'Casement Door',
    'Lift Slide Door',
    'Accordion Door',
    'Slim Frame Interior Door',
    'Slim Frame Sliding Door',
    'Pivot Door',
  ]

  const swingDirections = ['Left', 'Right']
  const swingTypes = ['Inswing', 'Outswing']
  
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
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/frames/sync-now`, {
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
    <div className="bg-white rounded-lg shadow-sm p-6 space-y-6 h-full overflow-y-auto border border-gray-200">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-1">Design Parameters</h2>
        <p className="text-sm text-gray-600">Configure your window or door specifications</p>
      </div>
      
      {/* Quick Presets */}
      <div className="space-y-3">
        <label className="block text-sm font-semibold text-gray-900 mb-2">Quick Presets</label>
        <div className="grid grid-cols-1 gap-2">
          {QUICK_PRESETS.map((preset) => (
            <button
              key={preset.name}
              onClick={() => handlePreset(preset)}
              className="p-3 text-left rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all font-medium"
            >
              <div className="font-semibold text-gray-900">{preset.name}</div>
              <div className="text-xs text-gray-600 mt-1">
                {preset.params.width}" × {preset.params.height}" | Series {preset.params.series}
              </div>
            </button>
          ))}
        </div>
      </div>
      
      {/* Frame Series Selector - Dropdown with Images from Database */}
      <div className="space-y-3">
        <div className="flex justify-between items-center mb-2">
          <label className="block text-sm font-semibold text-gray-900">Frame Series</label>
          <button
            onClick={handleSyncFrameData}
            disabled={isSyncing}
            className="text-xs px-3 py-1.5 bg-blue-50 text-blue-600 border-2 border-blue-200 rounded-lg hover:bg-blue-100 disabled:opacity-50 font-medium transition-all"
          >
            {isSyncing ? 'Syncing...' : '↻ Sync'}
          </button>
        </div>
        {syncMessage && (
          <div className="text-xs mb-2 p-2.5 bg-green-50 text-green-700 border-2 border-green-200 rounded-lg font-medium">
            {syncMessage}
          </div>
        )}
        {isLoadingFrameSeries ? (
          <div className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg bg-gray-50 text-gray-500 font-medium">
            Loading frame series...
          </div>
        ) : (
          <div className="space-y-3">
            <select
              value={parameters.series}
              onChange={(e) => setParameters({ series: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
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
                    
                    // 2. Construct FULL URL with hyphen format (matches backend naming convention)
                    const imageUrl = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/static/frames/series-${cleanSeries}-${view.toLowerCase()}.png`;

                    return (
                      <div key={view} className="flex flex-col items-center group">
                        <div className="w-full h-14 bg-white rounded border border-gray-200 flex items-center justify-center overflow-hidden relative shadow-sm hover:border-blue-400 transition-colors">
                          <img
                            src={imageUrl}
                            alt={`${view} View`}
                            className="w-full h-full object-contain p-1"
                            crossOrigin="anonymous" 
                            onError={(e) => {
                              // Fallback if image is missing - null-safe approach
                              const imgElement = e.currentTarget;
                              const parentElement = imgElement.parentElement;
                              
                              if (parentElement) {
                                imgElement.style.display = 'none';
                                parentElement.classList.add('bg-gray-50');
                                
                                // Create fallback text element
                                const fallbackText = document.createElement('span');
                                fallbackText.className = 'text-[10px] text-gray-400 select-none';
                                fallbackText.textContent = 'No Image';
                                parentElement.appendChild(fallbackText);
                              }
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
      
      {/* Product Type - Split into Window and Door */}
      <div className="space-y-3 border-t-2 border-gray-200 pt-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">Product Type</h3>
        <div>
          <label htmlFor="window-type-select" className="block text-sm font-semibold text-gray-900 mb-2">Window Unit Type</label>
          <select
            id="window-type-select"
            value={parameters.productType && !doorTypes.includes(parameters.productType) ? parameters.productType : ''}
            onChange={(e) => {
              if (e.target.value) {
                setParameters({ 
                  productType: e.target.value, 
                  configuration: '', 
                  panelCount: 1,
                  swingOrientation: '',
                  handleSide: ''
                })
              }
            }}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
          >
            <option value="">-- Select Window Type --</option>
            {windowTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="door-type-select" className="block text-sm font-semibold text-gray-900 mb-2">Door Unit Type</label>
          <select
            id="door-type-select"
            value={parameters.productType && doorTypes.includes(parameters.productType) ? parameters.productType : ''}
            onChange={(e) => {
              if (e.target.value) {
                setParameters({ 
                  productType: e.target.value, 
                  configuration: '', 
                  panelCount: 1,
                  swingOrientation: '',
                  handleSide: ''
                })
              }
            }}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
          >
            <option value="">-- Select Door Type --</option>
            {doorTypes.map((type) => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>

        {/* Double Casement Option - Only for Casement Door */}
        {parameters.productType === 'Casement Door' && (
          <div>
            <label htmlFor="casement-type-selector" className="block text-sm font-semibold text-gray-900 mb-2">Casement Configuration</label>
            <div id="casement-type-selector" className="flex gap-2" role="group" aria-label="Casement type selection">
              {['Single Casement', 'Double Casement'].map((casementType) => {
                const isSelected = parameters.configuration === casementType;
                const buttonClass = isSelected
                  ? 'border-gray-900 bg-gray-900 text-white shadow-md'
                  : 'border-gray-200 hover:border-gray-400 text-gray-700 bg-white';
                
                return (
                  <button
                    key={casementType}
                    onClick={() => {
                      setParameters({ 
                        configuration: casementType,
                        panelCount: casementType === 'Double Casement' ? 2 : 1
                      });
                    }}
                    className={`flex-1 py-3 px-3 rounded-lg border-2 transition-all font-semibold ${buttonClass}`}
                    aria-pressed={isSelected}
                    type="button"
                  >
                    {casementType}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Handle Side Selector - For Casement Door, Slim Frame Interior Door, Pivot Door */}
        {['Casement Door', 'Slim Frame Interior Door', 'Pivot Door'].includes(parameters.productType || '') && (
          <div>
            <label htmlFor="handle-side-selector" className="block text-sm font-semibold text-gray-900 mb-2">Handle Side</label>
            <div id="handle-side-selector" className="flex gap-2">
              {['Left', 'Right'].map((side) => {
                const isSelected = parameters.handleSide === side;
                const buttonClass = isSelected
                  ? 'border-gray-900 bg-gray-900 text-white shadow-md'
                  : 'border-gray-200 hover:border-gray-400 text-gray-700 bg-white';
                
                return (
                  <button
                    key={side}
                    onClick={() => {
                      setParameters({ handleSide: side });
                    }}
                    className={`flex-1 py-3 px-3 rounded-lg border-2 transition-all font-semibold ${buttonClass}`}
                    type="button"
                  >
                    {side}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Swing Direction - Only for Casement and Hinged Door */}
        {(parameters.productType === 'Casement' || parameters.productType === 'Hinged Door') && (
          <div className="space-y-3">
            {/* Handing (Left/Right) */}
            <div>
              <label htmlFor="handing-selector" className="block text-sm font-semibold text-gray-700 mb-2">Handing</label>
              <div id="handing-selector" className="flex gap-2" role="group" aria-label="Handing selection">
                {swingDirections.map((direction) => {
                  const isSelected = parameters.configuration?.includes(direction);
                  const currentSwing = parameters.configuration?.includes('Inswing') ? 'Inswing' : 
                                      parameters.configuration?.includes('Outswing') ? 'Outswing' : '';
                  const buttonClass = isSelected
                    ? 'border-blue-600 bg-blue-50 text-blue-900 shadow-md'
                    : 'border-gray-200 hover:border-gray-400 text-gray-700';
                  
                  return (
                    <button
                      key={direction}
                      onClick={() => {
                        const newConfig = currentSwing ? `${direction} ${currentSwing}` : direction;
                        setParameters({ configuration: newConfig });
                      }}
                      className={`flex-1 py-2 px-3 rounded-lg border-2 transition-all font-medium ${buttonClass}`}
                      aria-pressed={isSelected}
                      type="button"
                    >
                      {direction}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Swing Type (Inswing/Outswing) - Only for Hinged Door */}
            {parameters.productType === 'Hinged Door' && (
              <div>
                <label htmlFor="swing-type-selector" className="block text-sm font-semibold text-gray-700 mb-2">Swing Type</label>
                <div id="swing-type-selector" className="flex gap-2" role="group" aria-label="Swing type selection">
                  {swingTypes.map((swingType) => {
                    const isSelected = parameters.configuration?.includes(swingType);
                    const currentHanding = parameters.configuration?.includes('Left') ? 'Left' : 
                                          parameters.configuration?.includes('Right') ? 'Right' : '';
                    const buttonClass = isSelected
                      ? 'border-blue-600 bg-blue-50 text-blue-900 shadow-md'
                      : 'border-gray-200 hover:border-gray-400 text-gray-700';
                    
                    return (
                      <button
                        key={swingType}
                        onClick={() => {
                          const newConfig = currentHanding ? `${currentHanding} ${swingType}` : swingType;
                          setParameters({ configuration: newConfig });
                        }}
                        className={`flex-1 py-2 px-3 rounded-lg border-2 transition-all font-medium ${buttonClass}`}
                        aria-pressed={isSelected}
                        type="button"
                      >
                        {swingType}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      
      {/* Swing / Orientation Selector - Button Based */}
      {parameters.productType && parameters.productType !== 'Fixed Window' && (
        <div>
          <label className="block text-sm font-semibold text-gray-900 mb-2">Swing / Orientation</label>
          
          {/* Sliding Products - Left/Right Active */}
          {['Standard Sliding Door', 'Lift Slide Door', 'Accordion Door', 'Slim Frame Interior Door', 'Slim Frame Sliding Door', 'Standard Sliding Window'].includes(parameters.productType) && (
            <div className="flex gap-2">
              <button
                onClick={() => setParameters({ swingOrientation: 'XO (Left Active)' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'XO (Left Active)'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Left Active
              </button>
              <button
                onClick={() => setParameters({ swingOrientation: 'OX (Right Active)' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'OX (Right Active)'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Right Active
              </button>
            </div>
          )}
          
          {/* Casement Door - Left/Right Hand with Swing Type */}
          {parameters.productType === 'Casement Door' && (
            <div className="space-y-2">
              <div className="flex gap-2">
                <button
                  onClick={() => setParameters({ swingOrientation: 'Left Hand Inswing' })}
                  className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                    parameters.swingOrientation === 'Left Hand Inswing'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Left Inswing
                </button>
                <button
                  onClick={() => setParameters({ swingOrientation: 'Right Hand Inswing' })}
                  className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                    parameters.swingOrientation === 'Right Hand Inswing'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Right Inswing
                </button>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setParameters({ swingOrientation: 'Left Hand Outswing' })}
                  className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                    parameters.swingOrientation === 'Left Hand Outswing'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Left Outswing
                </button>
                <button
                  onClick={() => setParameters({ swingOrientation: 'Right Hand Outswing' })}
                  className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                    parameters.swingOrientation === 'Right Hand Outswing'
                      ? 'bg-gray-900 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Right Outswing
                </button>
              </div>
            </div>
          )}
          
          {/* Pivot Door - Left/Right */}
          {parameters.productType === 'Pivot Door' && (
            <div className="flex gap-2">
              <button
                onClick={() => setParameters({ swingOrientation: 'Pivot Left' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'Pivot Left'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Pivot Left
              </button>
              <button
                onClick={() => setParameters({ swingOrientation: 'Pivot Right' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'Pivot Right'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Pivot Right
              </button>
            </div>
          )}
          
          {/* Casement Window - Left/Right Hand */}
          {parameters.productType === 'Slim Frame Casement Window' && (
            <div className="flex gap-2">
              <button
                onClick={() => setParameters({ swingOrientation: 'Left Hand' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'Left Hand'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Left Hand
              </button>
              <button
                onClick={() => setParameters({ swingOrientation: 'Right Hand' })}
                className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                  parameters.swingOrientation === 'Right Hand'
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Right Hand
              </button>
            </div>
          )}
        </div>
      )}
      
      {/* Glass Type */}
      <div>
        <label htmlFor="glass-type-select" className="block text-sm font-semibold text-gray-900 mb-2">Glass Type</label>
        <select
          id="glass-type-select"
          value={parameters.glassType}
          onChange={(e) => setParameters({ glassType: e.target.value })}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
        >
          {glassTypes.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>
      
      {/* Frame Color */}
      <div>
        <label htmlFor="frame-color-select" className="block text-sm font-semibold text-gray-900 mb-2">Frame Color</label>
        <select
          id="frame-color-select"
          value={parameters.frameColor}
          onChange={(e) => setParameters({ frameColor: e.target.value })}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
        >
          {frameColors.map((color) => (
            <option key={color} value={color}>{color}</option>
          ))}
        </select>
      </div>
      
      {/* Project Info */}
      <div className="space-y-3 border-t-2 border-gray-200 pt-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-3">Project Information</h3>
        <div>
          <label htmlFor="item-number-input" className="block text-sm font-semibold text-gray-900 mb-2">Item Number</label>
          <input
            id="item-number-input"
            type="text"
            value={parameters.itemNumber}
            onChange={(e) => setParameters({ itemNumber: e.target.value })}
            placeholder="W-001"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 transition-all"
          />
        </div>
        
        <div>
          <label htmlFor="po-number-input" className="block text-sm font-semibold text-gray-900 mb-2">PO Number</label>
          <input
            id="po-number-input"
            type="text"
            value={parameters.poNumber}
            onChange={(e) => setParameters({ poNumber: e.target.value })}
            placeholder="PO-2024-001"
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 transition-all"
          />
        </div>
      </div>

      {/* Sliding Door Configuration - Replaces Panel Count */}
      {parameters.productType === 'Standard Sliding Door' && (
        <div className="mb-4">
          <label htmlFor="sliding-config-select" className="block text-sm font-semibold text-gray-900 mb-2">
            Sliding Configuration
          </label>
          <select
            id="sliding-config-select"
            value={parameters.configuration || ''}
            onChange={(e) => {
              const config = e.target.value;
              let count = 2; // default
              if (config.includes('3 Panel')) count = 3;
              if (config.includes('4 Panel') || config.includes('4 Track')) count = 4;

              setParameters({ 
                configuration: config,
                panelCount: count 
              });
            }}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 font-medium transition-all"
          >
            <option value="">-- Select Configuration --</option>
            <option value="2 Panel Slider">2 Panel Slider</option>
            <option value="3 Track 3 Panel">3 Track 3 Panel</option>
            <option value="4 Track 4 Panel">4 Track 4 Panel</option>
            <option value="4 Panel meet in the middle">4 Panel meet in the middle</option>
          </select>
        </div>
      )}

      {/* Canvas Size Divider */}
      <div className="border-t-2 border-gray-200 pt-6">
        <h3 className="text-sm font-semibold text-gray-900 mb-4">Dimensions</h3>
      </div>
      
      {/* Dimensions - Moved to Bottom */}
      <div className="space-y-4">
        <div>
          <label htmlFor="width-input" className="block text-sm font-semibold text-gray-900 mb-2">Width (inches)</label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleDimensionIncrement('width', -1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-xl transition-colors"
              type="button"
            >
              −
            </button>
            <input
              id="width-input"
              type="number"
              value={parameters.width ?? 0}
              onChange={(e) => handleDimensionChange('width', Number.parseFloat(e.target.value) || 0)}
              step="0.5"
              min="12"
              max="300"
              className="flex-1 h-12 text-center text-xl font-semibold border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 transition-all"
            />
            <button
              onClick={() => handleDimensionIncrement('width', 1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-xl transition-colors"
              type="button"
            >
              +
            </button>
            <span className="text-gray-600 font-medium min-w-[24px]">in</span>
          </div>
        </div>
        
        <div>
          <label htmlFor="height-input" className="block text-sm font-semibold text-gray-900 mb-2">Height (inches)</label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleDimensionIncrement('height', -1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-xl transition-colors"
              type="button"
            >
              −
            </button>
            <input
              id="height-input"
              type="number"
              value={parameters.height ?? 0}
              onChange={(e) => handleDimensionChange('height', Number.parseFloat(e.target.value) || 0)}
              step="0.5"
              min="12"
              max="300"
              className="flex-1 h-12 text-center text-xl font-semibold border-2 border-gray-200 rounded-lg focus:outline-none focus:border-gray-900 focus:ring-0 transition-all"
            />
            <button
              onClick={() => handleDimensionIncrement('height', 1)}
              className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 font-bold text-xl transition-colors"
              type="button"
            >
              +
            </button>
            <span className="text-gray-600 font-medium min-w-[24px]">in</span>
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

