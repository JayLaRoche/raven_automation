import axios, { type AxiosInstance } from 'axios'

// API Response Types
export interface FrameSeries {
  id: string
  name: string
  series: string
  image_url?: string
}

export interface FrameSeriesResponse {
  series: string[]
}

export interface FrameSeriesWithImagesResponse {
  series: FrameSeries[]
}

export interface DrawingParameters {
  series?: string
  productType?: string
  width?: number
  height?: number
  glassType?: string
  frameColor?: string
  itemNumber?: string
  poNumber?: string
  panelCount?: number
  configuration?: string
}

export interface UnitData {
  series: string
  productType: string
  width: number
  height: number
  glassType: string
  frameColor: string
  configuration?: string
  hasGrids?: boolean
  itemNumber?: string
  panelCount?: number
  swingOrientation?: string
  handleSide?: string
}

export interface AddUnitToProjectRequest {
  projectId: string | number
  unitData: UnitData
}

export interface AddUnitToProjectResponse {
  success: boolean
  unitId: number
  projectId: number
  unitData: UnitData
}

export interface DrawingResponse {
  success: boolean
  drawing?: string
  error?: string
}

export interface Project {
  id: string | number
  clientName: string
  date: string
  address: string
  unitCount: number
}

export interface ProjectsResponse {
  projects: Project[]
}

export interface CreateProjectRequest {
  clientName: string
  address: string
  date: string
}

export interface CreateProjectResponse {
  success: boolean
  id: number
  clientName: string
  address: string
  date: string
  unitCount: number
}

export interface DeleteProjectResponse {
  success: boolean
  message: string
  deletedId: number
}

export interface SaveDrawingRequest {
  unitId: number
  projectId: number
  pdfBase64: string
  parameters: {
    series: string
    productType: string
    width: number
    height: number
    glassType: string
    frameColor: string
    configuration?: string
    hasGrids?: boolean
    panelCount?: number
    swingOrientation?: string
    handleSide?: string
  }
}

export interface SaveDrawingResponse {
  success: boolean
  drawingId: number
  version: number
  message: string
}

export interface DrawingVersion {
  drawingId: number
  filename: string
  version: number
  isCurrent: boolean
  createdAt: string
}

export interface DrawingVersionsResponse {
  versions: DrawingVersion[]
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getFrameSeries = async (): Promise<FrameSeriesResponse> => {
  const response = await api.get<FrameSeriesResponse>('/api/frames/series')
  return response.data
}

export const getFrameSeriesWithImages = async (): Promise<FrameSeriesWithImagesResponse> => {
  const response = await api.get<FrameSeriesWithImagesResponse>('/api/frames/series-with-images')
  return response.data
}

export const getProductTypes = async () => {
  const response = await api.get('/api/frames/product-types')
  return response.data
}

export const getSwingOrientations = async () => {
  const response = await api.get('/api/frames/swing-orientations')
  return response.data
}

export const generateDrawing = async (parameters: DrawingParameters): Promise<DrawingResponse> => {
  const response = await api.post<DrawingResponse>('/api/drawings/generate', parameters)
  return response.data
}

export const getProjects = async (): Promise<ProjectsResponse> => {
  const response = await api.get<ProjectsResponse>('/api/projects')
  return response.data
}

export const createProject = async (data: CreateProjectRequest): Promise<CreateProjectResponse> => {
  const response = await api.post<CreateProjectResponse>('/api/projects/', data)
  return response.data
}

export const getProject = async (projectId: number): Promise<Project> => {
  const response = await api.get<Project>(`/api/projects/${projectId}`)
  return response.data
}

export const exportPDF = async (parameters: DrawingParameters): Promise<Blob> => {
  const response = await api.post<Blob>('/api/drawings/export/pdf', parameters, {
    responseType: 'blob',
  })
  return response.data
}

export const addUnitToProject = async (
  projectId: string | number,
  unitData: UnitData
): Promise<AddUnitToProjectResponse> => {
  try {
    console.log(`📤 Sending unit to project ${projectId}:`, unitData)
    const response = await api.post<AddUnitToProjectResponse>(
      `/api/projects/${projectId}/units`,
      unitData
    )
    console.log('✅ Unit creation response:', response.data)
    return response.data
  } catch (error) {
    console.error('Failed to add unit:', error)
    throw error
  }
}

export const deleteProject = async (projectId: number): Promise<DeleteProjectResponse> => {
  try {
    console.log(`🗑️ Deleting project ${projectId}`)
    const response = await api.delete<DeleteProjectResponse>(`/api/projects/${projectId}`)
    console.log('✅ Project deleted:', response.data)
    return response.data
  } catch (error) {
    console.error(`Failed to delete project ${projectId}:`, error)
    throw error
  }
}

export const saveDrawing = async (data: SaveDrawingRequest): Promise<SaveDrawingResponse> => {
  try {
    console.log('💾 Saving drawing to database...', data)
    const response = await api.post<SaveDrawingResponse>('/api/drawings/save', data)
    console.log('✅ Drawing saved:', response.data)
    return response.data
  } catch (error) {
    console.error('Failed to save drawing:', error)
    throw error
  }
}

export const getCurrentDrawing = async (unitId: number) => {
  try {
    const response = await api.get(`/api/drawings/unit/${unitId}/current`)
    return response.data
  } catch (error) {
    console.error(`Failed to get current drawing for unit ${unitId}:`, error)
    throw error
  }
}

export const getDrawingVersions = async (unitId: number): Promise<DrawingVersionsResponse> => {
  try {
    const response = await api.get<DrawingVersionsResponse>(`/api/drawings/unit/${unitId}/versions`)
    return response.data
  } catch (error) {
    console.error(`Failed to get drawing versions for unit ${unitId}:`, error)
    throw error
  }
}

export const downloadDrawing = async (drawingId: number): Promise<Blob> => {
  try {
    const response = await api.get<Blob>(`/api/drawings/${drawingId}/download`, {
      responseType: 'blob'
    })
    return response.data
  } catch (error) {
    console.error(`Failed to download drawing ${drawingId}:`, error)
    throw error
  }
}

export default api
