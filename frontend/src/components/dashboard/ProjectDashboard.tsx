import { useState } from 'react'
import { Plus, Settings } from 'lucide-react'
import { ProjectCard } from './ProjectCard'
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
    // TODO: Open create project modal or navigate to form
    alert('New Project feature coming soon')
  }

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.logo}>Raven Doors & Windows</h1>
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
            {/* Title Section */}
            <section className={styles.titleSection}>
              <div className={styles.titleContent}>
                <h2 className={styles.pageTitle}>Projects</h2>
                <p className={styles.subtitle}>
                  Manage your window specification projects
                </p>
              </div>
              <button className={styles.newProjectButton} onClick={handleNewProject}>
                <Plus size={20} />
                New Project
              </button>
            </section>

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
