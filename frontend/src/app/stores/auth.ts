import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types/user'
import { authService } from '@/services/auth.service'
import router from '@/router'

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
      // After successful login, navigate via router
      if (redirect) {
        router.replace(redirect)
      } else {
        router.replace({ name: 'Dashboard' })
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
      // ignore errors
    }
    setUser(null)
    // Redirect to login
    const redirect = router.currentRoute.value.fullPath
    router.replace({ name: 'Login', query: { redirect } })
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

  async function handleUnauthenticated() {
    setUser(null)
    const redirect = router.currentRoute.value.fullPath
    await router.replace({ name: 'Login', query: { redirect } })
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
