import { useMemo } from 'react'
import {
  getFrameSeriesConfig,
  getProductTypeConfig,
  getHeadProfile,
  getSillProfile,
  getJambProfile,
} from '../config/ComponentRegistry'

/**
 * Hook for accessing component registry data
 *
 * Provides easy access to frame series and product type configurations
 * with memoization for performance optimization
 *
 * @param {string} seriesId - Frame series ID (e.g., '65', '86')
 * @param {string} productType - Product type (e.g., 'CASEMENT', 'FIXED')
 * @returns {object} Registry data including series config, product config, and helper methods
 */
export function useComponentRegistry(seriesId, productType) {
  const seriesConfig = useMemo(() => getFrameSeriesConfig(seriesId), [seriesId])
  const productConfig = useMemo(() => getProductTypeConfig(productType), [productType])

  const headProfile = useMemo(() => getHeadProfile(seriesId), [seriesId])
  const sillProfile = useMemo(() => getSillProfile(seriesId), [seriesId])
  const jambProfile = useMemo(() => getJambProfile(seriesId), [seriesId])

  return {
    seriesId,
    productType,
    seriesConfig,
    productConfig,
    headProfile,
    sillProfile,
    jambProfile,
    seriesName: seriesConfig.name,
    productName: productConfig.name,
    openingStyle: productConfig.openingStyle,
    schematicType: productConfig.schematicType,
  }
}
