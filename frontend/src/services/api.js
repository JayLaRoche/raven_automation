import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getFrameSeries = async () => {
  const response = await api.get('/api/frames/series')
  return response.data
}

export const getFrameSeriesWithImages = async () => {
  const response = await api.get('/api/frames/series-with-images')
  return response.data
}

export const generateDrawing = async (parameters) => {
  const response = await api.post('/api/drawings/generate', parameters)
  return response.data
}

export const getProjects = async () => {
  const response = await api.get('/api/projects')
  return response.data
}

export const exportPDF = async (parameters) => {
  const response = await api.post('/api/drawings/export/pdf', parameters, {
    responseType: 'blob',
  })
  return response.data
}

export default api
