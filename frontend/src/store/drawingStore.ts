import { create } from 'zustand'
import { persist } from 'zustand/middleware'

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
  panelCount?: number
  swingOrientation?: string
  handleSide?: string
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
  projectId: number | null
  unitId: number | null
  
  // Actions
  setParameters: (params: Partial<DrawingParams>) => void
  setDrawing: (drawing: any) => void
  setIsGenerating: (generating: boolean) => void
  setAutoUpdate: (autoUpdate: boolean) => void
  setPresentationMode: (mode: boolean) => void
  setSelectedFrameView: (view: 'head' | 'sill' | 'jamb') => void
  setProjectId: (id: number | null) => void
  setUnitId: (id: number | null) => void
  resetParameters: () => void
}

const defaultParams: DrawingParams = {
  series: '65',
  productType: 'FIXED',
  width: 0,
  height: 0,
  glassType: 'Dual Pane Clear',
  frameColor: 'White',
  hasGrids: false,
  itemNumber: '',
  poNumber: '',
  panelCount: 1,
  swingOrientation: '',
  handleSide: '',
}

export const useDrawingStore = create<DrawingState>()(persist(
  (set) => ({
    parameters: defaultParams,
    drawing: null,
    isGenerating: false,
    autoUpdate: true,
    presentationMode: false,
    selectedFrameView: 'head',
    projectId: null,
    unitId: null,
    
    setParameters: (params) =>
      set((state) => ({
        parameters: { ...state.parameters, ...params },
      })),
    
    setDrawing: (drawing) => set({ drawing }),
    
    setIsGenerating: (generating) => set({ isGenerating: generating }),
    
    setAutoUpdate: (autoUpdate) => set({ autoUpdate }),
    
    setPresentationMode: (mode) => set({ presentationMode: mode }),
    
    setSelectedFrameView: (view) => set({ selectedFrameView: view }),
    
    setProjectId: (id) => set({ projectId: id }),
    
    setUnitId: (id) => set({ unitId: id }),
    
    resetParameters: () => set({ parameters: defaultParams, drawing: null }),
  }),
  {
    name: 'raven-drawing-storage',
    partialize: (state) => ({
      parameters: state.parameters,
      autoUpdate: state.autoUpdate,
      selectedFrameView: state.selectedFrameView,
    }),
  }
))
