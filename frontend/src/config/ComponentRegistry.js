/**
 * Component Registry - Maps frame series and product types to their corresponding
 * profile sections, schematic icons, and configuration flags.
 *
 * This registry acts as a single source of truth for dynamic asset loading
 * across the drawing canvas and parameter panels.
 */

// Frame Series Profile Configurations
export const FRAME_SERIES_MAP = {
  '65': {
    name: 'Series 65',
    headProfile: {
      path: '/assets/profiles/series65-head.svg',
      type: 'svg',
      alt: 'Series 65 Head Profile',
    },
    sillProfile: {
      path: '/assets/profiles/series65-sill.svg',
      type: 'svg',
      alt: 'Series 65 Sill Profile',
    },
    jambProfile: {
      path: '/assets/profiles/series65-jamb.svg',
      type: 'svg',
      alt: 'Series 65 Jamb Profile',
    },
    nailFlange: true,
    material: 'Aluminum',
    features: ['thermal-break', 'weather-seal'],
  },
  '86': {
    name: 'Series 86',
    headProfile: {
      path: '/assets/profiles/series86-head.svg',
      type: 'svg',
      alt: 'Series 86 Head Profile',
    },
    sillProfile: {
      path: '/assets/profiles/series86-sill.svg',
      type: 'svg',
      alt: 'Series 86 Sill Profile',
    },
    jambProfile: {
      path: '/assets/profiles/series86-jamb.svg',
      type: 'svg',
      alt: 'Series 86 Jamb Profile',
    },
    nailFlange: true,
    material: 'Aluminum',
    features: ['thermal-break', 'weather-seal', 'heavy-duty'],
  },
  '135': {
    name: 'Series 135',
    headProfile: {
      path: '/assets/profiles/series135-head.svg',
      type: 'svg',
      alt: 'Series 135 Head Profile',
    },
    sillProfile: {
      path: '/assets/profiles/series135-sill.svg',
      type: 'svg',
      alt: 'Series 135 Sill Profile',
    },
    jambProfile: {
      path: '/assets/profiles/series135-jamb.svg',
      type: 'svg',
      alt: 'Series 135 Jamb Profile',
    },
    nailFlange: false,
    material: 'Aluminum',
    features: ['thermal-break', 'weather-seal', 'commercial-grade'],
  },
  '4518': {
    name: 'Series 4518',
    headProfile: {
      path: '/assets/profiles/series4518-head.svg',
      type: 'svg',
      alt: 'Series 4518 Head Profile',
    },
    sillProfile: {
      path: '/assets/profiles/series4518-sill.svg',
      type: 'svg',
      alt: 'Series 4518 Sill Profile',
    },
    jambProfile: {
      path: '/assets/profiles/series4518-jamb.svg',
      type: 'svg',
      alt: 'Series 4518 Jamb Profile',
    },
    nailFlange: true,
    material: 'Aluminum',
    features: ['thermal-break', 'weather-seal', 'slim-profile'],
  },
}

// Product Type Configurations
export const PRODUCT_TYPE_MAP = {
  'FIXED': {
    name: 'Fixed Window',
    schematicType: 'fixed',
    icon: 'fixed-window-icon',
    description: 'Non-operating fixed pane',
    openingStyle: 'none',
  },
  'CASEMENT': {
    name: 'Casement Window',
    schematicType: 'casement',
    icon: 'casement-swing-icon',
    description: 'Side-hinged swinging window',
    openingStyle: 'swing',
  },
  'DOUBLE-HUNG': {
    name: 'Double Hung Window',
    schematicType: 'double-hung',
    icon: 'double-hung-icon',
    description: 'Vertically sliding window',
    openingStyle: 'slide',
  },
  'SLIDING': {
    name: 'Sliding Window',
    schematicType: 'sliding',
    icon: 'sliding-window-icon',
    description: 'Horizontally sliding window',
    openingStyle: 'slide',
  },
  'PATIO-DOOR': {
    name: 'Patio Door',
    schematicType: 'patio-door',
    icon: 'patio-door-icon',
    description: 'Sliding or hinged patio door',
    openingStyle: 'slide',
  },
  'AWNING': {
    name: 'Awning Window',
    schematicType: 'awning',
    icon: 'awning-window-icon',
    description: 'Top-hinged outward opening window',
    openingStyle: 'swing',
  },
}

/**
 * Get frame series configuration
 * @param {string} seriesId - The frame series ID (e.g., '65', '86')
 * @returns {object} Series configuration or default empty object
 */
export const getFrameSeriesConfig = (seriesId) => {
  return FRAME_SERIES_MAP[seriesId] || {
    name: `Series ${seriesId}`,
    headProfile: { path: null, type: 'svg', alt: 'Default profile' },
    sillProfile: { path: null, type: 'svg', alt: 'Default profile' },
    jambProfile: { path: null, type: 'svg', alt: 'Default profile' },
  }
}

/**
 * Get product type configuration
 * @param {string} productType - The product type (e.g., 'CASEMENT', 'FIXED')
 * @returns {object} Product type configuration or default empty object
 */
export const getProductTypeConfig = (productType) => {
  return PRODUCT_TYPE_MAP[productType?.toUpperCase()] || {
    name: productType || 'Unknown',
    schematicType: 'unknown',
    icon: null,
    openingStyle: 'none',
  }
}

/**
 * Get head profile asset for a specific frame series
 * @param {string} seriesId - Frame series ID
 * @returns {object|null} Profile asset object or null if not found
 */
export const getHeadProfile = (seriesId) => {
  const config = getFrameSeriesConfig(seriesId)
  return config.headProfile || null
}

/**
 * Get sill profile asset for a specific frame series
 * @param {string} seriesId - Frame series ID
 * @returns {object|null} Profile asset object or null if not found
 */
export const getSillProfile = (seriesId) => {
  const config = getFrameSeriesConfig(seriesId)
  return config.sillProfile || null
}

/**
 * Get jamb profile asset for a specific frame series
 * @param {string} seriesId - Frame series ID
 * @returns {object|null} Profile asset object or null if not found
 */
export const getJambProfile = (seriesId) => {
  const config = getFrameSeriesConfig(seriesId)
  return config.jambProfile || null
}

/**
 * Check if a frame series has nail flanges
 * @param {string} seriesId - Frame series ID
 * @returns {boolean} True if series supports nail flanges
 */
export const hasNailFlange = (seriesId) => {
  const config = getFrameSeriesConfig(seriesId)
  return config.nailFlange ?? false
}

/**
 * Get all available frame series
 * @returns {array} Array of frame series IDs
 */
export const getAvailableFrameSeries = () => {
  return Object.keys(FRAME_SERIES_MAP)
}

/**
 * Get all available product types
 * @returns {array} Array of product type keys
 */
export const getAvailableProductTypes = () => {
  return Object.keys(PRODUCT_TYPE_MAP)
}
