import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/index.css'
import { useAuthStore } from '@/app/stores/auth'
import { authService } from './services/auth.service'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()
  app.use(pinia)
  app.use(router)

  // Hydrate auth state by calling /auth/me. Backend must set HttpOnly cookie.
  const auth = useAuthStore()
  try {
    const user = await authService.me()
    auth.setUser(user)
  } catch (e) {
    // Not authenticated or backend unreachable — continue unauthenticated
    // Do not store tokens in localStorage/sessionStorage (HttpOnly cookie approach)
    // console.warn('Auth hydration failed', e)
  }

  app.mount('#app')
}

bootstrap()
