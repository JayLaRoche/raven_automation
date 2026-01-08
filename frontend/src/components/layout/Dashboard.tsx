import { useNavigate } from 'react-router-dom'
import { Plus, ArrowRight } from 'lucide-react'
import styles from './Dashboard.module.css'


interface RecentProject {
  id: number
  clientName: string
  date: string
  address: string
  unitCount: number
}

// Mock recent projects - these would come from Google Sheets in production
const MOCK_RECENT_PROJECTS: RecentProject[] = [
  {
    id: 1,
    clientName: 'Steve Delrosa',
    date: '2025-01-15',
    address: '1234 Maple Avenue, Springfield, IL 62701',
    unitCount: 35,
  },
  {
    id: 2,
    clientName: 'Bridgette Fallon',
    date: '2025-01-12',
    address: '5678 Oak Street, Chicago, IL 60601',
    unitCount: 22,
  },
  {
    id: 3,
    clientName: 'Marcus Johnson',
    date: '2025-01-10',
    address: '9012 Elm Road, Naperville, IL 60540',
    unitCount: 18,
  },
]

export function Dashboard() {
  const navigate = useNavigate()

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
            onClick={() => navigate('/generator')}
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
            onClick={() => navigate('/')}
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

      {/* Recent Projects Section */}
      <div className={styles.recentSection}>
        <h2 className={styles.sectionTitle}>Recent Projects</h2>
        <div className={styles.projectsList}>
          {MOCK_RECENT_PROJECTS.map((project) => (
            <div key={project.id} className={styles.projectItem}>
              <div className={styles.projectHeader}>
                <h3 className={styles.projectName}>{project.clientName}</h3>
                <span className={styles.unitBadge}>{project.unitCount} units</span>
              </div>
              <div className={styles.projectDetails}>
                <p className={styles.projectDate}>📅 {new Date(project.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
                <p className={styles.projectAddress}>📍 {project.address}</p>
              </div>
              <button
                className={styles.openButton}
                onClick={() => navigate(`/project/${project.id}`)}
              >
                Open Project <ArrowRight size={16} />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className={styles.statsSection}>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>24</div>
          <div className={styles.statLabel}>Total Projects</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>156</div>
          <div className={styles.statLabel}>Total Units</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statNumber}>12</div>
          <div className={styles.statLabel}>This Month</div>
        </div>
      </div>
    </div>
  )
}
