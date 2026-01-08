import { create } from 'zustand'

export interface Project {
  id?: string
  poNumber: string
  projectName: string
  customerName?: string
  items: ProjectItem[]
}

export interface ProjectItem {
  id: string
  itemNumber: string
  series: string
  productType: string
  width: number
  height: number
  glassType: string
  frameColor: string
  configuration?: string
}

interface ProjectState {
  currentProject: Project | null
  currentItemIndex: number
  
  // Actions
  setProject: (project: Project) => void
  setCurrentItemIndex: (index: number) => void
  nextItem: () => void
  previousItem: () => void
  getCurrentItem: () => ProjectItem | null
  clearProject: () => void
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  currentProject: null,
  currentItemIndex: 0,
  
  setProject: (project) => set({ currentProject: project, currentItemIndex: 0 }),
  
  setCurrentItemIndex: (index) => set({ currentItemIndex: index }),
  
  nextItem: () => {
    const { currentProject, currentItemIndex } = get()
    if (currentProject && currentItemIndex < currentProject.items.length - 1) {
      set({ currentItemIndex: currentItemIndex + 1 })
    }
  },
  
  previousItem: () => {
    const { currentItemIndex } = get()
    if (currentItemIndex > 0) {
      set({ currentItemIndex: currentItemIndex - 1 })
    }
  },
  
  getCurrentItem: () => {
    const { currentProject, currentItemIndex } = get()
    if (currentProject && currentProject.items[currentItemIndex]) {
      return currentProject.items[currentItemIndex]
    }
    return null
  },
  
  clearProject: () => set({ currentProject: null, currentItemIndex: 0 }),
}))
