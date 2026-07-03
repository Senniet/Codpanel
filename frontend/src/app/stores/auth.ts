import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types/user'
import { authService } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)

  const setUser = (u: User | null) => { user.value = u }

  const isAuthenticated = () => !!user.value

  async function login(username: string, password: string, redirect?: string) {
    loading.value = true
    try {
      const u = await authService.login(username, password)
      setUser(u)
      // After successful login, navigate to redirect if provided
      if (redirect) {
        window.location.href = redirect
      } else {
        window.location.href = '/dashboard'
      }
      return u
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await authService.logout()
    } catch (e) {
      // ignore
    }
    setUser(null)
    // Redirect to login
    const redirect = window.location.pathname
    window.location.href = `/login?redirect=${encodeURIComponent(redirect)}`
    loading.value = false
  }

  async function hydrate() {
    loading.value = true
    try {
      const u = await authService.me()
      setUser(u)
      return u
    } catch (e) {
      setUser(null)
      return null
    } finally {
      loading.value = false
    }
  }

  function handleUnauthenticated() {
    setUser(null)
    // Perform redirect to login preserving current location
    const redirect = window.location.pathname + window.location.search
    window.location.href = `/login?redirect=${encodeURIComponent(redirect)}`
  }

  // Attach global listener for unauthenticated events emitted by the API client
  if (typeof window !== 'undefined') {
    window.addEventListener('unauthenticated', () => {
      handleUnauthenticated()
    })
  }

  return {
    user,
    loading,
    setUser,
    isAuthenticated,
    login,
    logout,
    hydrate,
    handleUnauthenticated
  }
})
