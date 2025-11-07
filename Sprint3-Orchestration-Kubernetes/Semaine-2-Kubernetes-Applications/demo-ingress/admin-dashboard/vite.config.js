import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3200,
    host: '0.0.0.0'
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  },
  define: {
    'process.env': process.env
  }
});
