import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { X } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { getFrameSeriesWithImages, addUnitToProject } from '../../services/api'
import { useDrawingStore } from '../../store/drawingStore'
import styles from './AddUnitModal.module.css'

interface FrameSeries {
  id: string
  name: string
  series: string
  image_url?: string
}

interface AddUnitModalProps {
  isOpen: boolean
  onClose: () => void
  onAddUnit: (unitData: UnitFormData) => void
  projectId: string | number
  projectName?: string
}

export interface UnitFormData {
  series: string
  productType: string
  width: number
  height: number
  glassType: string
  frameColor: string
  configuration?: string
  hasGrids?: boolean
  itemNumber?: string
  panelCount?: number
  swingOrientation?: string
  handleSide?: string
}

const WINDOW_TYPES = [
  'Standard Sliding Window',
  'Folding Window',
  'Fold Up Window',
  'Slim Frame Casement Window',
  'Fixed Window',
]

const DOOR_TYPES = [
  'Standard Sliding Door',
  'Casement Door',
  'Lift Slide Door',
  'Accordion Door',
  'Slim Frame Interior Door',
  'Slim Frame Sliding Door',
  'Pivot Door',
]

const GLASS_TYPES = [
  'Single Pane Clear',
  'Dual Pane Clear',
  'Low-E',
  'Low-E + Argon',
  'Tempered',
  'Laminated',
]

const FRAME_COLORS = ['White', 'Bronze', 'Black', 'Mill Finish', 'Custom']

export function AddUnitModal({ 
  isOpen, 
  onClose, 
  onAddUnit,
  projectId,
  projectName 
}: Readonly<AddUnitModalProps>) {
  const navigate = useNavigate()
  const { setParameters } = useDrawingStore()
  
  const [series, setSeries] = useState('')
  const [productType, setProductType] = useState('Standard Sliding Window')
  const [productCategory, setProductCategory] = useState<'window' | 'door'>('window')
  const [width, setWidth] = useState<number>(0)
  const [height, setHeight] = useState<number>(0)
  const [glassType, setGlassType] = useState('Dual Pane Clear')
  const [frameColor, setFrameColor] = useState('White')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Fetch available frame series (matches SmartParameterPanel query)
  const { data: frameSeriesData = { series: [] }, isLoading: isLoadingFrameSeries } = useQuery<{ series: FrameSeries[] }>({
    queryKey: ['frameSeriesWithImages'],
    queryFn: getFrameSeriesWithImages,
  })

  const frameSeries = frameSeriesData?.series || []

  useEffect(() => {
    if (isOpen) {
      // Reset form when modal opens
      setSeries(frameSeries[0]?.series || '')
      setProductType('Standard Sliding Window')
      setProductCategory('window')
      setWidth(0)
      setHeight(0)
      setGlassType('Dual Pane Clear')
      setFrameColor('White')
    }
  }, [isOpen, frameSeries])

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate width and height
    if (width < 12 || width > 300) {
      alert('Width must be between 12 and 300 inches')
      return
    }
    
    if (height < 12 || height > 300) {
      alert('Height must be between 12 and 300 inches')
      return
    }
    
    const unitData: UnitFormData = {
      series,
      productType,
      width,
      height,
      glassType,
      frameColor,
    }

    try {
      setIsSubmitting(true)
      setError(null)

      console.log('📤 Submitting unit to project:', projectId, unitData)

      // Save to database via API
      const response = await addUnitToProject(Number(projectId), unitData)
      
      console.log('✅ Unit saved successfully:', response)

      // Update Zustand store for immediate drawing generator access
      setParameters(response.unitData)

      // Notify parent to refresh project list
      onAddUnit(response.unitData)

      // Close modal
      onClose()

      // Navigate to drawing generator with unit data
      navigate(`/project/${projectId}`, {
        state: { 
          initialDrawingData: response.unitData,
          unitId: response.unitId,
          fromAddUnit: true
        }
      })

    } catch (err: any) {
      console.error('❌ Failed to add unit:', err)
      setError(err.response?.data?.detail || 'Failed to save unit. Please try again.')
      setIsSubmitting(false)
    }
  }

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        {/* Modal Header */}
        <div className={styles.header}>
          <div className={styles.headerText}>
            <h2 className={styles.title}>Add New Unit</h2>
            <p className={styles.subtitle}>
              {projectName ? `Add to ${projectName}` : 'Specify unit details'}
            </p>
          </div>
          <button onClick={onClose} className={styles.closeButton} aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className={styles.form}>
          {/* Frame Series */}
          <div className={styles.formGroup}>
            <label htmlFor="series" className={styles.label}>Frame Series</label>
            <select
              id="series"
              className={styles.select}
              value={series}
              onChange={(e) => setSeries(e.target.value)}
              required
              disabled={isLoadingFrameSeries}
            >
              <option value="">
                {isLoadingFrameSeries ? 'Loading frame series...' : 'Select series...'}
              </option>
              {frameSeries.map((s) => (
                <option key={s.id} value={s.series}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>

          {/* Product Category */}
          <div className={styles.formGroup}>
            <label className={styles.label}>Product Category</label>
            <div className={styles.categoryButtons}>
              <button
                type="button"
                className={`${styles.categoryButton} ${productCategory === 'window' ? styles.active : ''}`}
                onClick={() => {
                  setProductCategory('window')
                  setProductType('Standard Sliding Window')
                }}
              >
                Window
              </button>
              <button
                type="button"
                className={`${styles.categoryButton} ${productCategory === 'door' ? styles.active : ''}`}
                onClick={() => {
                  setProductCategory('door')
                  setProductType('Standard Sliding Door')
                }}
              >
                Door
              </button>
            </div>
          </div>

          {/* Product Type */}
          <div className={styles.formGroup}>
            <label htmlFor="productType" className={styles.label}>
              {productCategory === 'window' ? 'Window Type' : 'Door Type'}
            </label>
            <select
              id="productType"
              className={styles.select}
              value={productType}
              onChange={(e) => setProductType(e.target.value)}
              required
            >
              {(productCategory === 'window' ? WINDOW_TYPES : DOOR_TYPES).map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Dimensions */}
          <div className={styles.dimensionsRow}>
            <div className={styles.formGroup}>
              <label htmlFor="width" className={styles.label}>Width (inches)</label>
              <input
                id="width"
                type="number"
                className={styles.input}
                placeholder="Enter width (12-300)"
                value={width || ''}
                onChange={(e) => setWidth(Number(e.target.value))}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="height" className={styles.label}>Height (inches)</label>
              <input
                id="height"
                type="number"
                className={styles.input}
                placeholder="Enter height (12-300)"
                value={height || ''}
                onChange={(e) => setHeight(Number(e.target.value))}
                required
              />
            </div>
          </div>

          {/* Glass Type */}
          <div className={styles.formGroup}>
            <label htmlFor="glassType" className={styles.label}>Glass Type</label>
            <select
              id="glassType"
              className={styles.select}
              value={glassType}
              onChange={(e) => setGlassType(e.target.value)}
              required
            >
              {GLASS_TYPES.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Frame Color */}
          <div className={styles.formGroup}>
            <label htmlFor="frameColor" className={styles.label}>Frame Color</label>
            <select
              id="frameColor"
              className={styles.select}
              value={frameColor}
              onChange={(e) => setFrameColor(e.target.value)}
              required
            >
              {FRAME_COLORS.map((color) => (
                <option key={color} value={color}>
                  {color}
                </option>
              ))}
            </select>
          </div>

          {/* Modal Footer */}
          <div className={styles.footer}>
            <button type="button" onClick={onClose} className={styles.cancelButton}>
              Cancel
            </button>
            <button type="submit" className={styles.addButton}>
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
