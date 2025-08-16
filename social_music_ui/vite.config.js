// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // 👇 nombre EXACTO del repo, con mayúscula inicial
  base: '/Ariel495/',
})
