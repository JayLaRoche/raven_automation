import { create } from 'zustand'

export interface DrawingParams {
  series?: string
  productType?: string
  width?: number
  height?: number
  glassType?: string
  frameColor?: string
  configuration?: string
  hasGrids?: boolean
  itemNumber?: string
  poNumber?: string
  notes?: string
}

export interface DrawingData {
  svg?: string
  base64?: string
  url?: string
  timestamp?: number
  [key: string]: any  // Allow flexibility if needed
}

interface DrawingState {
  parameters: DrawingParams
  drawing: DrawingData | null
  isGenerating: boolean
  autoUpdate: boolean
  presentationMode: boolean
  selectedFrameView: 'head' | 'sill' | 'jamb'
  
  // Actions
  setParameters: (params: Partial<DrawingParams>) => void
  setDrawing: (drawing: any) => void
  setIsGenerating: (generating: boolean) => void
  setAutoUpdate: (autoUpdate: boolean) => void
  setPresentationMode: (mode: boolean) => void
  setSelectedFrameView: (view: 'head' | 'sill' | 'jamb') => void
  resetParameters: () => void
}

const defaultParams: DrawingParams = {
  series: '65',
  productType: 'FIXED',
  width: 48,
  height: 60,
  glassType: 'Dual Pane Clear',
  frameColor: 'White',
  hasGrids: false,
  itemNumber: '',
  poNumber: '',
}

export const useDrawingStore = create<DrawingState>((set) => ({
  parameters: defaultParams,
  drawing: null,
  isGenerating: false,
  autoUpdate: true,
  presentationMode: false,
  selectedFrameView: 'head',
  
  setParameters: (params) =>
    set((state) => ({
      parameters: { ...state.parameters, ...params },
    })),
  
  setDrawing: (drawing) => set({ drawing }),
  
  setIsGenerating: (generating) => set({ isGenerating: generating }),
  
  setAutoUpdate: (autoUpdate) => set({ autoUpdate }),
  
  setPresentationMode: (mode) => set({ presentationMode: mode }),
  
  setSelectedFrameView: (view) => set({ selectedFrameView: view }),
  
  resetParameters: () => set({ parameters: defaultParams, drawing: null }),
}))
