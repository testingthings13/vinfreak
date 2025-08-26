import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/cars': {
        target: process.env.VITE_API_BASE || 'https://vinfreak.onrender.com',
        changeOrigin: true,
        secure: true,
      }
    }
  }
})
