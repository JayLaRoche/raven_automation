import { useState, useEffect } from 'react'

interface ToastMessage {
  id: string
  message: string
  type: 'success' | 'error' | 'info'
  duration?: number
}

let toastId = 0
const toastCallbacks: ((msg: ToastMessage) => void)[] = []

export const useToast = () => {
  return {
    success: (message: string, duration = 3000) => {
      const id = String(toastId++)
      const msg: ToastMessage = { id, message, type: 'success', duration }
      toastCallbacks.forEach((cb) => cb(msg))
    },
    error: (message: string, duration = 5000) => {
      const id = String(toastId++)
      const msg: ToastMessage = { id, message, type: 'error', duration }
      toastCallbacks.forEach((cb) => cb(msg))
    },
    info: (message: string, duration = 3000) => {
      const id = String(toastId++)
      const msg: ToastMessage = { id, message, type: 'info', duration }
      toastCallbacks.forEach((cb) => cb(msg))
    },
  }
}

export const ToastContainer = () => {
  const [toasts, setToasts] = useState<ToastMessage[]>([])
  
  useEffect(() => {
    const handleToast = (msg: ToastMessage) => {
      setToasts((prev) => [...prev, msg])
      
      if (msg.duration) {
        setTimeout(() => {
          setToasts((prev) => prev.filter((t) => t.id !== msg.id))
        }, msg.duration)
      }
    }
    
    toastCallbacks.push(handleToast)
    return () => {
      const idx = toastCallbacks.indexOf(handleToast)
      if (idx > -1) toastCallbacks.splice(idx, 1)
    }
  }, [])
  
  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`px-4 py-3 rounded-lg shadow-lg text-white animate-pulse ${
            toast.type === 'success'
              ? 'bg-green-600'
              : toast.type === 'error'
              ? 'bg-red-600'
              : 'bg-blue-600'
          }`}
        >
          {toast.message}
        </div>
      ))}
    </div>
  )
}
