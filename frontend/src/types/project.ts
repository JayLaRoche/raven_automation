/**
 * Project Type Definitions
 */

export interface Project {
  id: string | number
  clientName: string
  date: string | Date
  address: string
  unitCount: number
  city?: string
  state?: string
  zipCode?: string
  createdAt?: string
  updatedAt?: string
  status?: 'active' | 'completed' | 'archived'
}

export interface ProjectFormData {
  clientName: string
  address: string
  city: string
  state: string
  zipCode: string
  unitCount: number
}

export interface ProjectsState {
  projects: Project[]
  selectedProject: Project | null
  isLoading: boolean
  error: string | null
}
