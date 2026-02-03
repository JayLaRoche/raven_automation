import { CSSProperties } from 'react'

export interface WindowElevationViewProps {
  parameters?: {
    series?: string
    width?: number
    height?: number
    productType?: string
    glassType?: string
    frameColor?: string
    configuration?: string
    itemNumber?: string
    panelCount?: number
  }
  selectedFrameView?: 'head' | 'sill' | 'jamb'
  style?: CSSProperties
  className?: string
}

declare const WindowElevationView: React.FC<WindowElevationViewProps>
export default WindowElevationView
