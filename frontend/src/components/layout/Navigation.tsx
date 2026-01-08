import { useLocation, useNavigate } from 'react-router-dom'
import styles from './Navigation.module.css'


export function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()

  const isDashboardActive = location.pathname === '/'
  const isGeneratorActive = location.pathname === '/generator'

  return (
    <nav className={styles.navContainer}>
      <div className={styles.navContent}>
        <div className={styles.logo}>
          Raven Doors & Windows
        </div>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${isDashboardActive ? styles.active : ''}`}
            onClick={() => navigate('/')}
          >
            Dashboard
          </button>
          <button
            className={`${styles.tab} ${isGeneratorActive ? styles.active : ''}`}
            onClick={() => navigate('/generator')}
          >
            Drawing Generator
          </button>
        </div>
      </div>

      {/* Active indicator line */}
      <div className={styles.indicatorLine}></div>
    </nav>
  )
}
