import { useState, useCallback } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'

export interface DrawingParameters {
  series: string
  product_type: string
  width: number
  height: number
  glass_type: string
  frame_color: string
  configuration: string
  item_number: string
  po_number?: string
  notes?: string
  special_notes?: string
}

/**
 * Hook for generating reference layout shop drawings as PDF
 */
export function useReferencePDFGeneration() {
  const [pdfUrl, setPdfUrl] = useState<string | undefined>(undefined)

  const mutation = useMutation({
    mutationFn: async (params: DrawingParameters) => {
      console.log('Generating reference layout PDF with params:', params)

      // Capture canvas as Base64 image
      const canvas = document.querySelector('canvas') as HTMLCanvasElement
      if (!canvas) {
        throw new Error('Canvas not found - cannot generate PDF')
      }

      // Convert canvas to high-quality PNG Base64
      const imageSnapshot = canvas.toDataURL('image/png', 1.0)
      console.log('Canvas captured as image:', {
        width: canvas.width,
        height: canvas.height,
        dataLength: imageSnapshot.length
      })

      // Send parameters + image snapshot to backend
      const response = await fetch('/api/drawings/generate-pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...params,
          imageSnapshot: imageSnapshot  // Add captured canvas image
        }),
      })

      if (!response.ok) {
        // Try to extract detailed error message from response
        let errorMessage = `Failed to generate drawing (${response.status})`
        
        try {
          const errorData = await response.json()
          if (errorData.detail) {
            errorMessage = errorData.detail
          }
        } catch (parseError) {
          // If response isn't JSON, use status text
          errorMessage = response.statusText || errorMessage
        }
        
        console.error('[PDF Generation Error]', {
          status: response.status,
          statusText: response.statusText,
          message: errorMessage,
          params: params,
        })
        
        throw new Error(errorMessage)
      }

      // Get PDF blob
      const blob = await response.blob()

      // Validate blob size
      if (blob.size === 0) {
        throw new Error('Generated PDF is empty')
      }

      // Create object URL for display and download
      const url = URL.createObjectURL(blob)
      setPdfUrl(url)

      console.log('[PDF Generation Success]', {
        size: blob.size,
        type: blob.type,
      })

      // Also store blob for download
      return { url, blob }
    },
    onError: (error: Error) => {
      console.error('[PDF Hook Error Caught]', error.message)
      setPdfUrl(undefined)
    },
  })

  const generatePDF = useCallback(
    (params: DrawingParameters) => {
      mutation.mutate(params)
    },
    [mutation]
  )

  const downloadPDF = useCallback(
    (filename: string = 'shop_drawing.pdf') => {
      if (!pdfUrl) return

      const link = document.createElement('a')
      link.href = pdfUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    [pdfUrl]
  )

  const clearPDF = useCallback(() => {
    if (pdfUrl) {
      URL.revokeObjectURL(pdfUrl)
    }
    setPdfUrl(undefined)
    mutation.reset()
  }, [pdfUrl, mutation])

  return {
    // State
    pdfUrl,
    isLoading: mutation.isPending,
    error: mutation.error?.message,
    
    // Methods
    generatePDF,
    downloadPDF,
    clearPDF,
  }
}
