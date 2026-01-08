import { useEffect } from 'react'
import { useDrawingStore } from '../store/drawingStore'
import { useProjectStore } from '../store/projectStore'

interface KeyboardShortcuts {
  onGenerateNow?: () => void
  onExportPDF?: () => void
  onPresentationMode?: () => void
}

export const useKeyboardShortcuts = (callbacks: KeyboardShortcuts) => {
  const { presentationMode, setPresentationMode } = useDrawingStore()
  const { currentProject, nextItem, previousItem } = useProjectStore()
  
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger in inputs
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      ) {
        return
      }
      
      // Cmd/Ctrl + G: Generate now
      if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
        e.preventDefault()
        callbacks.onGenerateNow?.()
      }
      
      // Cmd/Ctrl + E: Export PDF
      if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault()
        callbacks.onExportPDF?.()
      }
      
      // Cmd/Ctrl + P: Presentation mode
      if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault()
        setPresentationMode(!presentationMode)
      }
      
      // Arrow keys: Navigate items
      if (currentProject) {
        if (e.key === 'ArrowRight') {
          e.preventDefault()
          nextItem()
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault()
          previousItem()
        }
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [presentationMode, currentProject, callbacks, setPresentationMode, nextItem, previousItem])
}
