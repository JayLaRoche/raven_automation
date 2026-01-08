import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: process.env.VITE_PORT || 3000,
    proxy: {
      '/api': {
        // Development: proxy to local backend
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false, // Disable sourcemaps in production for security
    // Override sourcemaps for development
    minify: 'terser',
  },
  // Environment-aware configuration
  define: {
    __DEV__: process.env.NODE_ENV === 'development',
  },
})

