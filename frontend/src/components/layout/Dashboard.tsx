import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, ArrowRight } from 'lucide-react'
import { CreateProjectModal } from '../dashboard/CreateProjectModal'
import { createProject, getProjects } from '../../services/api'
import styles from './Dashboard.module.css'

export function Dashboard() {
  const navigate = useNavigate()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isCreating, setIsCreating] = useState(false)
  const [totalProjects, setTotalProjects] = useState(0)
  const [totalUnits, setTotalUnits] = useState(0)
  const [isLoadingStats, setIsLoadingStats] = useState(true)

  // Load stats on mount
  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      setIsLoadingStats(true)
      const response = await getProjects()
      
      // Count total projects
      const projectCount = response.projects.length
      
      // Sum up all unit counts across projects
      const unitCount = response.projects.reduce((sum, project) => sum + (project.unitCount || 0), 0)
      
      setTotalProjects(projectCount)
      setTotalUnits(unitCount)
    } catch (error) {
      console.error('Failed to load stats:', error)
      // Keep at 0 if error
    } finally {
      setIsLoadingStats(false)
    }
  }

  const handleCreateProject = async (data: { clientName: string; address: string; date: string }) => {
    try {
      setIsCreating(true)
      
      // Validate data before sending
      if (!data.clientName || !data.address || !data.date) {
        alert('Please fill in all required fields.')
        return
      }
      
      // Create project in database
      const response = await createProject({
        clientName: data.clientName.trim(),
        address: data.address.trim(),
        date: data.date
      })
      
      if (response.success && response.id) {
        // Close modal first
        setIsModalOpen(false)
        
        // Reload stats to reflect new project
        await loadStats()
        
        // Navigate to the new project's drawing generator
        navigate(`/project/${response.id}`)
      } else {
        throw new Error('Project creation did not return a valid ID')
      }
    } catch (error) {
      console.error('Failed to create project:', error)
      
      // More detailed error message
      const errorMessage = error instanceof Error 
        ? `Failed to create project: ${error.message}` 
        : 'Failed to create project. Please check the server connection and try again.'
      
      alert(errorMessage)
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <div className={styles.container}>
      {/* Hero Section */}
      <div className={styles.hero}>
        <h1 className={styles.heroTitle}>Welcome Back</h1>
        <p className={styles.heroSubtitle}>
          Manage your projects and create custom shop drawings for window and door frames.
        </p>
      </div>

      {/* Quick Actions Section */}
      <div className={styles.quickActionsSection}>
        <h2 className={styles.sectionTitle}>Quick Actions</h2>
        <div className={styles.quickActionsGrid}>
          <button
            className={styles.quickActionCard}
            onClick={() => setIsModalOpen(true)}
          >
            <div className={styles.quickActionIcon}>
              <Plus size={32} />
            </div>
            <h3 className={styles.quickActionTitle}>Start New Drawing</h3>
            <p className={styles.quickActionDescription}>
              Create a new shop drawing from scratch
            </p>
            <div className={styles.quickActionArrow}>
              <ArrowRight size={20} />
            </div>
          </button>

          <button
            className={styles.quickActionCard}
            onClick={() => navigate('/projects')}
          >
            <div className={styles.quickActionIcon}>
              <Plus size={32} />
            </div>
            <h3 className={styles.quickActionTitle}>View All Projects</h3>
            <p className={styles.quickActionDescription}>
              Browse your project library
            </p>
            <div className={styles.quickActionArrow}>
              <ArrowRight size={20} />
            </div>
          </button>
        </div>
      </div>

      {/* Stats Section */}
      <div className={styles.statsSection}>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {isLoadingStats ? '...' : totalProjects}
          </div>
          <div className={styles.statLabel}>Total Projects</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {isLoadingStats ? '...' : totalUnits}
          </div>
          <div className={styles.statLabel}>Total Units</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>
            {isLoadingStats ? '...' : totalProjects}
          </div>
          <div className={styles.statLabel}>This Month</div>
        </div>
      </div>

      <CreateProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateProject}
        isLoading={isCreating}
      />
    </div>
  )
}
