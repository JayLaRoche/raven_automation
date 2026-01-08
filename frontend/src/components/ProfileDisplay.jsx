import React, { useState, useEffect } from 'react'
import { useComponentRegistry } from '../hooks/useComponentRegistry'

/**
 * ProfileDisplay Component
 *
 * Dynamically displays profile sections (HEAD, SILL, JAMB) based on the
 * selected frame series. Uses the ComponentRegistry to look up the correct
 * asset paths for each profile.
 *
 * @param {string} seriesId - Frame series ID (e.g., '65', '86')
 * @param {string} profileType - Profile type: 'HEAD', 'SILL', or 'JAMB'
 * @param {number} width - Display width in pixels (default: 300)
 * @param {number} height - Display height in pixels (default: 200)
 */
export default function ProfileDisplay({ seriesId = '65', profileType = 'HEAD', width = 300, height = 200 }) {
  const { seriesConfig, seriesName } = useComponentRegistry(seriesId, null)
  const [imageError, setImageError] = useState(false)
  const [loading, setLoading] = useState(true)

  // Map profile type to config key
  const profileKey = profileType.toLowerCase()
  const profileMap = {
    head: seriesConfig.headProfile,
    sill: seriesConfig.sillProfile,
    jamb: seriesConfig.jambProfile,
  }

  const profileAsset = profileMap[profileKey]

  useEffect(() => {
    setImageError(false)
    setLoading(true)
  }, [seriesId, profileType])

  const handleImageLoad = () => {
    setLoading(false)
  }

  const handleImageError = () => {
    setImageError(true)
    setLoading(false)
  }

  // If no profile asset is available, show placeholder
  if (!profileAsset || !profileAsset.path) {
    return (
      <div
        style={{
          width,
          height,
          border: '1px solid #ddd',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#f5f5f5',
          borderRadius: '4px',
        }}
      >
        <div style={{ textAlign: 'center', color: '#999' }}>
          <p style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: '500' }}>
            {profileType} Profile Not Available
          </p>
          <p style={{ margin: 0, fontSize: '12px' }}>
            Series {seriesId} - {profileType}
          </p>
        </div>
      </div>
    )
  }

  // If image failed to load, show error placeholder
  if (imageError) {
    return (
      <div
        style={{
          width,
          height,
          border: '2px solid #ff6b6b',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#ffe0e0',
          borderRadius: '4px',
        }}
      >
        <div style={{ textAlign: 'center', color: '#d32f2f' }}>
          <p style={{ margin: '0 0 8px 0', fontSize: '14px', fontWeight: '500' }}>
            Failed to Load {profileType} Profile
          </p>
          <p style={{ margin: 0, fontSize: '12px' }}>
            {profileAsset.path}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div
      style={{
        width,
        height,
        border: '1px solid #ddd',
        borderRadius: '4px',
        overflow: 'hidden',
        backgroundColor: '#fafafa',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      {loading && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            zIndex: 1,
          }}
        >
          <div style={{ fontSize: '12px', color: '#999' }}>Loading...</div>
        </div>
      )}

      {profileAsset.type === 'svg' ? (
        <img
          src={profileAsset.path}
          alt={profileAsset.alt || `${profileType} profile for ${seriesName}`}
          style={{
            maxWidth: '100%',
            maxHeight: '100%',
            objectFit: 'contain',
          }}
          onLoad={handleImageLoad}
          onError={handleImageError}
        />
      ) : (
        <img
          src={profileAsset.path}
          alt={profileAsset.alt || `${profileType} profile for ${seriesName}`}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
          onLoad={handleImageLoad}
          onError={handleImageError}
        />
      )}
    </div>
  )
}
