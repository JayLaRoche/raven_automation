import { useNavigate } from 'react-router-dom'
import { Calendar, MapPin, Trash2, Plus } from 'lucide-react'
import styles from './ProjectCard.module.css'

import type { Project } from '../../types/project'

interface ProjectCardProps {
  project: Project
  onView?: (id: string | number) => void
  onEdit?: (id: string | number) => void
  onDelete?: (id: string | number) => void
  onAddUnit?: (id: string | number) => void
  isDeleting?: boolean
}

export function ProjectCard({ project, onView, onEdit, onDelete, onAddUnit, isDeleting = false }: Readonly<ProjectCardProps>) {
  const navigate = useNavigate()

  const handleViewDetails = () => {
    if (onView) {
      onView(project.id)
    } else {
      navigate(`/project/${project.id}`)
    }
  }

  const handleAddUnit = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onAddUnit) {
      onAddUnit(project.id)
    }
  }

  const handleDelete = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (onDelete) {
      onDelete(project.id)
    }
  }

  const formatDate = (date: string | Date) => {
    const d = new Date(date)
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <div className={styles.card}>
      {/* Card Header */}
      <div className={styles.cardHeader}>
        <h3 className={styles.clientName}>{project.clientName}</h3>
        <span className={styles.unitBadge}>{project.unitCount} units</span>
      </div>

      {/* Card Details */}
      <div className={styles.cardDetails}>
        {/* Date */}
        <div className={styles.detailRow}>
          <Calendar size={16} className={styles.icon} />
          <span className={styles.detailText}>{formatDate(project.date)}</span>
        </div>

        {/* Address */}
        <div className={styles.detailRow}>
          <MapPin size={16} className={styles.icon} />
          <span className={styles.detailText}>{project.address}</span>
        </div>
      </div>

      {/* Card Footer */}
      <div className={styles.cardFooter}>
        <button onClick={handleViewDetails} className={styles.viewButton}>
          View Details
        </button>
        <button
          onClick={handleAddUnit}
          className={styles.addUnitButton}
          title="Add unit to project"
          aria-label="Add unit to project"
        >
          <Plus size={16} />
          Add Unit
        </button>
        <button
          onClick={handleDelete}
          className={styles.deleteButton}
          title="Delete project"
          aria-label="Delete project"
          disabled={isDeleting}
        >
          {isDeleting ? '...' : <Trash2 size={18} />}
        </button>
      </div>
    </div>
  )
}
