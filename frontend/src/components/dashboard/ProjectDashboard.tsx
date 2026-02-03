import { useState } from 'react'
import { Plus, Settings } from 'lucide-react'
import { ProjectCard } from './ProjectCard'
import { CreateProjectModal } from './CreateProjectModal'
import styles from './ProjectDashboard.module.css'

import type { Project } from '../../types/project'

// Mock data - replace with API call in production
const MOCK_PROJECTS: Project[] = [
  {
    id: 1,
    clientName: 'Steve Delrosa',
    date: '2025-01-15',
    address: '1234 Maple Avenue, Springfield, IL 62701',
    unitCount: 35,
    status: 'active',
  },
  {
    id: 2,
    clientName: 'Bridgette Fallon',
    date: '2025-01-10',
    address: '5678 Oak Street, Chicago, IL 60601',
    unitCount: 22,
    status: 'active',
  },
  {
    id: 3,
    clientName: 'Marcus Johnson',
    date: '2025-01-05',
    address: '9012 Elm Drive, Naperville, IL 60540',
    unitCount: 18,
    status: 'active',
  },
  {
    id: 4,
    clientName: 'Jennifer Lee',
    date: '2024-12-28',
    address: '3456 Pine Road, Aurora, IL 60505',
    unitCount: 28,
    status: 'completed',
  },
  {
    id: 5,
    clientName: 'Robert Williams',
    date: '2024-12-20',
    address: '7890 Cedar Lane, Evanston, IL 60201',
    unitCount: 15,
    status: 'active',
  },
  {
    id: 6,
    clientName: 'Angela Martinez',
    date: '2024-12-15',
    address: '2345 Birch Way, Schaumburg, IL 60173',
    unitCount: 42,
    status: 'active',
  },
]

export function ProjectDashboard() {
  const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS)
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState<'projects' | 'settings'>('projects')
  const [isModalOpen, setIsModalOpen] = useState(false)

  // Filter projects based on search query
  const filteredProjects = projects.filter((project) => {
    const query = searchQuery.toLowerCase()
    return (
      project.clientName.toLowerCase().includes(query) ||
      project.address.toLowerCase().includes(query)
    )
  })

  const handleDeleteProject = (id: string | number) => {
    setProjects(projects.filter((p) => p.id !== id))
  }

  const handleNewProject = () => {
    setIsModalOpen(true)
  }

  const handleCreateProject = (data: { clientName: string; address: string; date: string }) => {
    const newProject: Project = {
      id: Date.now(), // Generate a unique ID
      clientName: data.clientName,
      address: data.address,
      date: data.date,
      unitCount: 0, // Default to 0 units for new project
      status: 'active', // Default status
    }
    
    // Add new project to the beginning of the list
    setProjects([newProject, ...projects])
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          {/* Replaced Text with Logo Image */}
          <img 
            src="/raven-logo.PNG" 
            alt="Raven Doors & Windows" 
            className={styles.logoImage} 
          />
          <nav className={styles.nav}>
            <button
              className={`${styles.navButton} ${activeTab === 'projects' ? styles.active : ''}`}
              onClick={() => setActiveTab('projects')}
            >
              Projects
            </button>
            <button
              className={`${styles.navButton} ${activeTab === 'settings' ? styles.active : ''}`}
              onClick={() => setActiveTab('settings')}
            >
              <Settings size={18} />
              Settings
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className={styles.main}>
        {activeTab === 'projects' ? (
          <>
            {/* Quick Actions Section */}
            <div className={styles.quickActionsSection}>
              <h2 className={styles.sectionTitle}>Quick Actions</h2>
              <div className={styles.quickActionsGrid}>
                {/* Start New Drawing Button */}
                <button 
                  className={styles.quickActionCard}
                  onClick={handleNewProject}
                >
                  <div className={styles.quickActionIcon}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <path d="M12 18v-6"></path>
                      <path d="M9 15h6"></path>
                    </svg>
                  </div>
                  <h3 className={styles.quickActionTitle}>Start New Drawing</h3>
                  <p className={styles.quickActionDescription}>Create a custom shop drawing</p>
                  <div className={styles.quickActionArrow}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </button>

                {/* View All Projects Button */}
                <button 
                  className={styles.quickActionCard}
                  onClick={() => setActiveTab('projects')}
                >
                  <div className={styles.quickActionIcon}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M3 9h18v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V9Z"></path>
                      <path d="m3 9 2.45-4.9A2 2 0 0 1 7.24 3h9.52a2 2 0 0 1 1.8 1.1L21 9"></path>
                      <path d="M12 3v6"></path>
                    </svg>
                  </div>
                  <h3 className={styles.quickActionTitle}>View All Projects</h3>
                  <p className={styles.quickActionDescription}>Browse your project library</p>
                  <div className={styles.quickActionArrow}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </button>

                {/* Settings Button */}
                <button 
                  className={styles.quickActionCard}
                  onClick={() => setActiveTab('settings')}
                >
                  <div className={styles.quickActionIcon}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
                      <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                  </div>
                  <h3 className={styles.quickActionTitle}>Settings</h3>
                  <p className={styles.quickActionDescription}>Configure your preferences</p>
                  <div className={styles.quickActionArrow}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </button>
              </div>
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

            {/* Projects Grid */}
            {filteredProjects.length > 0 ? (
              <div className={styles.projectsGrid}>
                {filteredProjects.map((project) => (
                  <ProjectCard
                    key={project.id}
                    project={project}
                    onDelete={handleDeleteProject}
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
                    <Plus size={20} />
                    Create First Project
                  </button>
                )}

      <CreateProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreate={handleCreateProject}
      />
              </div>
            )}
          </>
        ) : (
          // Settings tab
          <div className={styles.settingsSection}>
            <h2 className={styles.settingsTitle}>Settings</h2>
            <p className={styles.settingsText}>Settings page coming soon...</p>
          </div>
        )}
      </main>
    </div>
  )
}
