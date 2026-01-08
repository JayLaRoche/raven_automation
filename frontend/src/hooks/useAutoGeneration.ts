import { useEffect, useRef } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { debounce } from 'lodash'
import { DrawingParams } from '../store/drawingStore'
import { generateDrawing } from '../services/api'

export const useAutoGeneration = (parameters: DrawingParams, autoUpdate: boolean) => {
  const queryClient = useQueryClient()
  
  const { mutate: generate, isPending } = useMutation({
    mutationFn: generateDrawing,
    onSuccess: (data) => {
      queryClient.setQueryData(['current-drawing'], data)
    },
    onError: (error) => {
      console.error('Failed to generate drawing:', error)
    },
  })
  
  // Debounced auto-generation - wait 800ms after last parameter change
  const debouncedGenerateRef = useRef(
    debounce((params: DrawingParams) => {
      generate(params)
    }, 800)
  ).current
  
  useEffect(() => {
    if (autoUpdate && parameters.series && parameters.width && parameters.height) {
      debouncedGenerateRef(parameters)
    }
  }, [parameters, autoUpdate, debouncedGenerateRef])
  
  // Manual generation (skips debounce)
  const generateNow = () => {
    generate(parameters)
  }
  
  return { 
    generateNow,
    isGenerating: isPending 
  }
}
