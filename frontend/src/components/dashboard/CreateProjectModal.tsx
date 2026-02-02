import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import styles from './CreateProjectModal.module.css'

interface CreateProjectModalProps {
  isOpen: boolean
  onClose: () => void
  onCreate: (data: { clientName: string; address: string; date: string }) => void
  isLoading?: boolean
}

export function CreateProjectModal({ isOpen, onClose, onCreate, isLoading = false }: Readonly<CreateProjectModalProps>) {
  const [date, setDate] = useState('')
  const [clientName, setClientName] = useState('')
  const [address, setAddress] = useState('')

  useEffect(() => {
    if (isOpen) {
      setDate(new Date().toISOString().split('T')[0])
      setClientName('')
      setAddress('')
    }
  }, [isOpen])

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onCreate({ clientName, address, date })
    onClose()
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <div className={styles.headerText}>
            <h2 className={styles.title}>Create New Project</h2>
            <p className={styles.subtitle}>Enter the project details to get started.</p>
          </div>
          <button onClick={onClose} className={styles.closeButton} aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="clientName" className={styles.label}>Client Name</label>
            <input
              id="clientName"
              type="text"
              className={styles.input}
              placeholder="Enter client name"
              value={clientName}
              onChange={(e) => setClientName(e.target.value)}
              required
              autoFocus
              disabled={isLoading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="address" className={styles.label}>Job Site Address</label>
            <textarea
              id="address"
              className={styles.textarea}
              placeholder="Enter the job site address"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              required
              rows={3}
              disabled={isLoading}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="date" className={styles.label}>Project Date</label>
            <input
              id="date"
              type="date"
              className={styles.input}
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>

          <div className={styles.footer}>
            <button type="button" onClick={onClose} className={styles.cancelButton} disabled={isLoading}>
              Cancel
            </button>
            <button type="submit" className={styles.createButton} disabled={isLoading}>
              {isLoading ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
