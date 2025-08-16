import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/Ariel495/',   // exacto al nombre del repo (A mayúscula)
})