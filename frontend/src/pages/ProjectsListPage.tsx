import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ProjectCard } from '../components/dashboard/ProjectCard'
import { CreateProjectModal } from '../components/dashboard/CreateProjectModal'
import { AddUnitModal, type UnitFormData } from '../components/dashboard/AddUnitModal'
import { addUnitToProject, getProjects, createProject as createProjectAPI, deleteProject } from '../services/api'
import styles from './ProjectsListPage.module.css'

import type { Project } from '../types/project'

export function ProjectsListPage() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<Project[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isAddUnitModalOpen, setIsAddUnitModalOpen] = useState(false)
  const [selectedProjectId, setSelectedProjectId] = useState<string | number | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isCreating, setIsCreating] = useState(false)
  const [deletingProjectId, setDeletingProjectId] = useState<string | number | null>(null)

  // Fetch projects on mount
  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const response = await getProjects()
      console.log('📋 Loaded projects:', response)
      setProjects(response.projects || [])
    } catch (err) {
      console.error('Failed to load projects:', err)
      setError('Failed to load projects. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  // Filter projects based on search query
  const filteredProjects = projects.filter((project) => {
    const query = searchQuery.toLowerCase()
    return (
      project.clientName.toLowerCase().includes(query) ||
      project.address.toLowerCase().includes(query)
    )
  })

  const handleDeleteProject = async (projectId: string | number, projectName: string, event?: React.MouseEvent) => {
    // Prevent card click navigation if event exists
    if (event) {
      event.stopPropagation()
    }
    
    // Confirm deletion
    const confirmed = window.confirm(
      `Are you sure you want to delete "${projectName}"?\n\nThis will permanently delete the project and all its units.`
    )
    
    if (!confirmed) return
    
    try {
      setDeletingProjectId(projectId)
      console.log(`🗑️ Deleting project ${projectId}...`)
      
      const response = await deleteProject(Number(projectId))
      
      console.log('✅ Delete successful:', response)
      
      // Show success message
      alert(response.message || 'Project deleted successfully')
      
      // Reload projects list
      await loadProjects()
      
    } catch (err: any) {
      console.error('❌ Delete failed:', err)
      const errorMessage = err.response?.data?.detail || 'Failed to delete project. Please try again.'
      alert(`Error: ${errorMessage}`)
    } finally {
      setDeletingProjectId(null)
    }
  }

  const handleViewProject = (id: string | number) => {
    navigate(`/project/${id}`)
  }

  const handleEditProject = (id: string | number) => {
    navigate(`/project/${id}`)
  }

  const handleNewProject = () => {
    setIsModalOpen(true)
  }

  const handleCreateProject = async (data: { clientName: string; address: string; date: string }) => {
    try {
      setIsCreating(true)
      console.log('Creating project:', data)
      const response = await createProjectAPI(data)
      console.log('✅ Project created:', response)
      
      // Reload projects to show new one
      await loadProjects()
      
      // Close modal
      setIsModalOpen(false)
      
      // Navigate to the new project
      if (response.id) {
        navigate(`/project/${response.id}`)
      }
    } catch (err) {
      console.error('Failed to create project:', err)
      setError('Failed to create project. Please try again.')
    } finally {
      setIsCreating(false)
    }
  }

  const handleAddUnit = (projectId: string | number) => {
    setSelectedProjectId(projectId)
    setIsAddUnitModalOpen(true)
  }

  const handleAddUnitSubmit = async (unitData: UnitFormData) => {
    if (!selectedProjectId) return

    try {
      // Call API to add unit to project
      await addUnitToProject(selectedProjectId, unitData)
      
      // Update local state - increment unit count
      setProjects(projects.map(p => 
        p.id === selectedProjectId 
          ? { ...p, unitCount: p.unitCount + 1 }
          : p
      ))

      // Show success message (optional)
      console.log('Unit added successfully to project', selectedProjectId)
    } catch (error) {
      console.error('Failed to add unit:', error)
      // Show error message to user (implement toast/notification)
    } finally {
      setIsAddUnitModalOpen(false)
      setSelectedProjectId(null)
    }
  }

  const selectedProject = projects.find(p => p.id === selectedProjectId)

  return (
    <div className={styles.container}>
      {/* Page Header */}
      <div className={styles.pageHeader}>
        <div className={styles.headerContent}>
          <h1 className={styles.pageTitle}>All Projects</h1>
          <p className={styles.subtitle}>
            Manage your window and door specification projects
          </p>
        </div>
        <button className={styles.newProjectButton} onClick={handleNewProject}>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          New Project
        </button>
      </div>

      {/* Search Bar */}
      <div className={styles.searchContainer}>
        <input
          type="text"
          placeholder="Search by client name or job site address..."
          className={styles.searchInput}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className={styles.errorBanner}>
          <p>{error}</p>
          <button onClick={loadProjects}>Retry</button>
        </div>
      )}

      {/* Loading State */}
      {isLoading ? (
        <div className={styles.loading}>
          <p>Loading projects...</p>
        </div>
      ) : filteredProjects.length > 0 ? (
        <div className={styles.projectsGrid}>
          {filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onView={handleViewProject}
              onEdit={handleEditProject}
              onDelete={(id) => handleDeleteProject(id, project.clientName)}
              onAddUnit={handleAddUnit}
              isDeleting={deletingProjectId === project.id}
            />
          ))}
        </div>
      ) : (
        <div className={styles.emptyState}>
          <p className={styles.emptyMessage}>
            {searchQuery
              ? 'No projects match your search'
              : 'No projects yet. Create your first project to get started.'}
          </p>
          {!searchQuery && (
            <button className={styles.newProjectButton} onClick={handleNewProject}>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14"></path>
                <path d="M12 5v14"></path>
              </svg>
              Create First Project
            </button>
          )}
        </div>
      )}

      {/* Modal Integration */}
      <CreateProjectModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateProject}
        isLoading={isCreating}
      />

      {/* Add Unit Modal */}
      <AddUnitModal
        isOpen={isAddUnitModalOpen}
        onClose={() => {
          setIsAddUnitModalOpen(false)
          setSelectedProjectId(null)
        }}
        onAddUnit={handleAddUnitSubmit}
        projectId={selectedProjectId || 0}
        projectName={selectedProject?.clientName}
      />
    </div>
  )
}
