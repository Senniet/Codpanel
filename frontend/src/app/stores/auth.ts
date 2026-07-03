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

  function sanitizeRedirect(raw?: string | null): string | undefined {
    if (!raw) return undefined
    try {
      // Only allow pathnames, strip query params and hashes
      // If full URL provided, use its pathname
      let path = raw
      if (raw.startsWith('http://') || raw.startsWith('https://')) {
        const url = new URL(raw)
        path = url.pathname
      }
      // Strip query and fragment
      path = path.split('?')[0].split('#')[0]
      // Do not allow redirect back to login
      if (path === '/login' || path.startsWith('/login')) return undefined
      return path || undefined
    } catch (e) {
      return undefined
    }
  }

  async function login(username: string, password: string, redirect?: string) {
    loading.value = true
    try {
      const u = await authService.login(username, password)
      setUser(u)
      // After successful login, navigate via router
      const dest = sanitizeRedirect(redirect)
      if (dest) {
        router.replace(dest)
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
    const current = router.currentRoute.value
    let redirect = undefined as string | undefined
    // If we're already on the login page, preserve any intended destination but avoid nesting
    if (current.name === 'Login') {
      redirect = sanitizeRedirect((current.query && (current.query.redirect as string)) || undefined)
    } else {
      redirect = sanitizeRedirect(current.fullPath)
    }

    const to = redirect ? { name: 'Login', query: { redirect } } : { name: 'Login' }
    router.replace(to)
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
    const current = router.currentRoute.value
    // If already on login page, avoid redirect loops. If login has a redirect param, keep it single-level.
    if (current.name === 'Login') {
      const intended = (current.query && (current.query.redirect as string)) || undefined
      const dest = sanitizeRedirect(intended) || undefined
      const to = dest ? { name: 'Login', query: { redirect: dest } } : { name: 'Login' }
      await router.replace(to)
      return
    }

    const dest = sanitizeRedirect(current.fullPath) || undefined
    const to = dest ? { name: 'Login', query: { redirect: dest } } : { name: 'Login' }
    await router.replace(to)
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
