import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default ({ mode }) => {
  // Load environment variables based on the current mode (dev, production, etc.)
  const env = loadEnv(mode, process.cwd(), '')
  const backend = env.VITE_BACKEND || 'http://localhost:8000'

  return defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      }
    },
    server: {
      proxy: {
        // Proxy all /api requests to the backend dev server. The target can be configured via VITE_BACKEND.
        '/api': {
          target: backend,
          changeOrigin: true,
          secure: false,
          ws: true
        }
      }
    }
  })
}
