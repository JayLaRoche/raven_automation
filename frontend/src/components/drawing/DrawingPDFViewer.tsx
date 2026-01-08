import { useState, useEffect } from 'react'

interface DrawingPDFViewerProps {
  pdfUrl?: string
  loading?: boolean
  error?: string
}

export function DrawingPDFViewer({ pdfUrl, loading = false, error }: DrawingPDFViewerProps) {
  const [scale, setScale] = useState(1.0)
  const [showFullscreen, setShowFullscreen] = useState(false)

  const handleZoomIn = () => setScale(s => Math.min(2.0, s + 0.1))
  const handleZoomOut = () => setScale(s => Math.max(0.5, s - 0.1))
  const handleFitPage = () => setScale(1.0)

  if (loading) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center bg-gray-100 rounded-lg">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mb-4"></div>
        <p className="text-gray-600 text-lg">Generating shop drawing...</p>
        <p className="text-gray-500 text-sm mt-2">~3 seconds</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center bg-red-50 rounded-lg border-2 border-red-300">
        <div className="text-red-600 text-lg font-bold mb-2">⚠ Drawing Error</div>
        <p className="text-red-700 text-sm">{error}</p>
      </div>
    )
  }

  if (!pdfUrl) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <div className="text-center">
          <div className="text-5xl mb-3">📄</div>
          <p className="text-gray-600 font-medium">No drawing generated yet</p>
          <p className="text-gray-500 text-sm mt-1">Adjust parameters and generate a drawing</p>
        </div>
      </div>
    )
  }

  return (
    <div className={`flex flex-col h-full bg-white rounded-lg border border-gray-200 ${showFullscreen ? 'fixed inset-0 z-50' : ''}`}>
      {/* Toolbar */}
      <div className="flex items-center justify-between gap-2 p-3 bg-gray-100 border-b border-gray-200 flex-shrink-0">
        <div className="text-sm font-medium text-gray-700">Shop Drawing (A3 Landscape)</div>
        
        <div className="flex items-center gap-2">
          {/* Zoom Controls */}
          <button
            onClick={handleZoomOut}
            title="Zoom out"
            className="px-2 py-1 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 font-medium"
          >
            −
          </button>
          
          <input
            type="range"
            min="50"
            max="200"
            step="10"
            value={scale * 100}
            onChange={(e) => setScale(Number(e.target.value) / 100)}
            className="w-24"
            title="Zoom level"
          />
          
          <div className="text-xs font-medium text-gray-700 w-10 text-center">
            {Math.round(scale * 100)}%
          </div>
          
          <button
            onClick={handleZoomIn}
            title="Zoom in"
            className="px-2 py-1 text-sm bg-white border border-gray-300 rounded hover:bg-gray-50 font-medium"
          >
            +
          </button>
          
          <div className="w-px h-6 bg-gray-300"></div>
          
          <button
            onClick={handleFitPage}
            title="Fit to page"
            className="px-3 py-1 text-xs bg-white border border-gray-300 rounded hover:bg-gray-50"
          >
            Fit Page
          </button>
          
          <div className="w-px h-6 bg-gray-300"></div>
          
          {/* Download Button */}
          <a
            href={pdfUrl}
            download
            className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 font-medium"
            title="Download PDF"
          >
            📥 Download
          </a>
          
          {/* Fullscreen Button */}
          <button
            onClick={() => setShowFullscreen(!showFullscreen)}
            title="Toggle fullscreen"
            className="px-3 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            {showFullscreen ? '⛶ Exit' : '⛶ Full'}
          </button>
        </div>
      </div>

      {/* PDF Viewer */}
      <div className={`flex-1 overflow-auto bg-gray-50 flex items-center justify-center ${showFullscreen ? '' : 'p-4'}`}>
        <iframe
          src={`${pdfUrl}#toolbar=1&navpanes=0&scrollbar=1&zoom=${Math.round(scale * 100)}`}
          className="w-full h-full border-none"
          title="Shop Drawing PDF"
          style={{
            transform: `scale(${scale})`,
            transformOrigin: 'top center',
            // Account for transform scaling
            width: `${100 / scale}%`,
            height: `${100 / scale}%`,
          }}
        />
      </div>

      {/* Status Bar */}
      <div className="px-3 py-2 bg-gray-100 border-t border-gray-200 text-xs text-gray-600 flex-shrink-0">
        <span>A3 Landscape | 420mm × 297mm | Professional Reference Layout</span>
      </div>
    </div>
  )
}
