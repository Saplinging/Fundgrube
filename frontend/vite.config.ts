import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/items": "http://backend:8000",
      "/chat": "http://backend:8000",
      "/search": "http://backend:8000",
      "/health": "http://backend:8000",
      "/rag": "http://backend:8000"
    }
  }
})
