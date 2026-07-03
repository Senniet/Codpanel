import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/index.css'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()
  app.use(pinia)
  app.use(router)

  // Hydrate auth store (will call /auth/me and set user if session cookie exists)
  try {
    const { useAuthStore } = await import('@/app/stores/auth')
    const auth = useAuthStore()
    await auth.hydrate()
  } catch (e) {
    // ignore
  }

  app.mount('#app')
}

bootstrap()
