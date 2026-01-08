import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getFrameSeriesWithImages } from '../services/api'
import './SmartParameterPanel.css'

export default function SmartParameterPanel({ parameters, setParameters, onParametersChange }) {
  const [selectedSeries, setSelectedSeries] = useState(parameters?.series || '65')
  const [selectedView, setSelectedView] = useState('HEAD')
  const [viewMode, setViewMode] = useState('single') // 'single' or 'compare'
  const [imageLoadErrors, setImageLoadErrors] = useState({})

  // Fetch all series with images
  const { data: framesData, isLoading } = useQuery({
    queryKey: ['framesWithImages'],
    queryFn: getFrameSeriesWithImages,
    staleTime: 1000 * 60 * 5, // Cache for 5 minutes
  })

  // Get current series data
  const currentSeries = framesData?.series?.find(s => s.id === selectedSeries)
  const availableImages = currentSeries?.images || {}

  // Get available view types (only those with images)
  const availableViewTypes = Object.entries(availableImages)
    .filter(([_, img]) => img.exists)
    .map(([key, _]) => key)

  // If selected view doesn't exist, switch to first available
  useEffect(() => {
    if (selectedView && availableImages[selectedView] && !availableImages[selectedView].exists) {
      const firstAvailable = availableViewTypes[0] || 'HEAD'
      setSelectedView(firstAvailable)
    }
  }, [selectedSeries, availableImages, selectedView, availableViewTypes])

  // Update parent parameters when series changes
  useEffect(() => {
    setParameters(prev => ({ ...prev, series: selectedSeries }))
    if (onParametersChange) {
      onParametersChange({ ...parameters, series: selectedSeries })
    }
  }, [selectedSeries])

  const handleImageError = (seriesId, viewType) => {
    setImageLoadErrors(prev => ({
      ...prev,
      [`${seriesId}-${viewType}`]: true
    }))
  }

  const renderPlaceholderImage = (seriesName) => (
    <div className="placeholder-image">
      <div className="placeholder-content">
        <div className="placeholder-text">{seriesName}</div>
        <div className="placeholder-subtext">Frame Cross-Section</div>
      </div>
    </div>
  )

  const getImageUrl = (series, viewType) => {
    if (!availableImages[viewType]) return null
    return availableImages[viewType].url
  }

  const renderSingleImageView = () => {
    const imageUrl = getImageUrl(selectedSeries, selectedView)
    const viewTypeInfo = availableImages[selectedView] || {}

    return (
      <div className="single-image-view">
        <div className="image-header">
          <h3 className="image-title">
            {currentSeries?.name || 'Series'} - {viewTypeInfo.view_type || 'View'}
          </h3>
          <div className="image-stats">
            <span className="stat-item">
              {currentSeries?.image_stats?.required_available || 0} / {currentSeries?.image_stats?.required_total || 0} required
            </span>
          </div>
        </div>

        <div className="image-container single">
          {imageUrl && !imageLoadErrors[`${selectedSeries}-${selectedView}`] ? (
            <img
              src={imageUrl}
              alt={`${currentSeries?.name} ${viewTypeInfo.view_type}`}
              className="frame-image"
              onError={() => handleImageError(selectedSeries, selectedView)}
            />
          ) : (
            renderPlaceholderImage(currentSeries?.name || 'Series')
          )}
        </div>

        <div className="image-footer">
          <p className="image-description">
            {viewTypeInfo.description || 'Frame cross-section view'}
          </p>
        </div>
      </div>
    )
  }

  const renderComparisonView = () => {
    const requiredViews = ['HEAD', 'SILL', 'JAMB']

    return (
      <div className="comparison-view">
        <div className="comparison-grid">
          {requiredViews.map(viewType => {
            const imageUrl = getImageUrl(selectedSeries, viewType)
            const viewTypeInfo = availableImages[viewType] || {}
            const hasError = imageLoadErrors[`${selectedSeries}-${viewType}`]

            return (
              <div key={viewType} className="comparison-item">
                <div className="comparison-header">
                  <h4 className="comparison-title">{viewTypeInfo.view_type || viewType.toUpperCase()}</h4>
                </div>

                <div className="image-container comparison">
                  {imageUrl && !hasError ? (
                    <img
                      src={imageUrl}
                      alt={`${currentSeries?.name} ${viewTypeInfo.view_type}`}
                      className="frame-image"
                      onError={() => handleImageError(selectedSeries, viewType)}
                    />
                  ) : (
                    renderPlaceholderImage(`${viewTypeInfo.view_type || viewType.toUpperCase()}`)
                  )}
                </div>

                <div className="comparison-footer">
                  <span className="view-label">{viewTypeInfo.view_label || viewType[0].toUpperCase()}</span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="parameter-panel loading">
        <div className="loading-spinner">Loading frame data...</div>
      </div>
    )
  }

  return (
    <div className="parameter-panel">
      {/* Series Gallery/Selector */}
      <div className="series-section">
        <h2 className="section-title">Frame Series</h2>

        <div className="gallery-grid">
          {framesData?.series?.map(series => {
            const isSelected = series.id === selectedSeries
            const stats = series.image_stats || {}
            const completionPercentage = stats.completion_percentage || 0

            return (
            <button
              key={series.id}
              className={`gallery-item ${isSelected ? 'active' : ''}`}
              onClick={() => setSelectedSeries(series.id)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  setSelectedSeries(series.id)
                }
              }}
              type="button"
              aria-pressed={isSelected}
            >
                <div className="gallery-image">
                  {series.images?.HEAD?.url && !imageLoadErrors[`${series.id}-HEAD`] ? (
                    <img
                      src={series.images.HEAD.url}
                      alt={series.name}
                      className="series-thumbnail"
                      onError={() => handleImageError(series.id, 'HEAD')}
                    />
                  ) : (
                    renderPlaceholderImage(series.name)
                  )}
                </div>

                <div className="gallery-content">
                  <h3 className="gallery-title">{series.name}</h3>
                  <p className="gallery-type">{series.type}</p>

                  {/* Badge Row */}
                  <div className="badge-row">
                    {Object.entries(series.images || {}).map(([viewType, imgData]) => {
                      if (!imgData.required) return null
                      const isDisabled = !imgData.exists
                      return (
                        <span
                          key={viewType}
                          className={`image-badge ${isDisabled ? 'disabled' : 'available'}`}
                          style={{
                            backgroundColor: imgData.exists ? imgData.color : '#d1d5db',
                          }}
                          title={imgData.view_type}
                        >
                          {imgData.view_label}
                        </span>
                      )
                    })}
                  </div>

                  {/* Completion Bar */}
                  <div className="completion-bar-container">
                    <div
                      className="completion-bar"
                      style={{
                        width: `${completionPercentage}%`,
                      }}
                    />
                  </div>
                  <span className="completion-text">
                    {stats.required_available}/{stats.required_total}
                  </span>
                </div>
              </button>
            )
          })}
        </div>
      </div>

      {/* View Selection and Mode Toggle */}
      <div className="control-section">
        <div className="view-selector">
          <h3 className="selector-title">View Type</h3>

          <div className="view-tabs">
            {Object.entries(availableImages).map(([viewType, imgData]) => (
              <button
                key={viewType}
                className={`view-tab ${selectedView === viewType ? 'active' : ''} ${
                  imgData.exists ? 'disabled' : ''
                }`}
                onClick={() => imgData.exists && setSelectedView(viewType)}
                disabled={!imgData.exists}
                style={{
                  borderBottomColor: selectedView === viewType ? imgData.color : 'transparent',
                }}
              >
                <span className="tab-label">{imgData.view_type}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="mode-selector">
          <h3 className="selector-title">Display Mode</h3>

          <div className="view-mode-toggle">
            <button
              className={`mode-button ${viewMode === 'single' ? 'active' : ''}`}
              onClick={() => setViewMode('single')}
            >
              Single View
            </button>
            <button
              className={`mode-button ${viewMode === 'compare' ? 'active' : ''}`}
              onClick={() => setViewMode('compare')}
            >
              Compare All
            </button>
          </div>
        </div>
      </div>

      {/* Image Display */}
      <div className="display-section">
        {viewMode === 'single' ? renderSingleImageView() : renderComparisonView()}
      </div>

      {/* Info Box */}
      {currentSeries && (
        <div className="info-box">
          <h4 className="info-title">{currentSeries.name}</h4>
          <p className="info-description">{currentSeries.description}</p>
          <p className="info-type"><strong>Type:</strong> {currentSeries.type}</p>
        </div>
      )}
    </div>
  )
}
