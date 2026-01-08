import { DrawingParams } from '../../store/drawingStore'
import { useToast } from '../ui/Toast'
import { Button } from '../ui/Button'

interface QuickExportProps {
  drawing: any
  parameters: DrawingParams
}

export function QuickExport({ drawing, parameters }: QuickExportProps) {
  const toast = useToast()
  
  const handleExport = () => {
    if (!drawing) {
      toast.error('No drawing to export')
      return
    }
    
    const canvas = document.querySelector('canvas') as HTMLCanvasElement
    if (!canvas) {
      toast.error('Canvas not found')
      return
    }
    
    // Generate filename
    const timestamp = new Date().toISOString().split('T')[0]
    const filename = `${parameters.poNumber || 'drawing'}_${parameters.itemNumber || 'item'}_${timestamp}.png`
    
    // Export
    const link = document.createElement('a')
    link.download = filename
    link.href = canvas.toDataURL()
    link.click()
    
    toast.success('Drawing exported!')
  }
  
  return (
    <Button
      variant="success"
      size="md"
      disabled={!drawing}
      onClick={handleExport}
    >
      💾 Export
    </Button>
  )
}
