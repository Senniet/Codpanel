import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)

  const setUser = (u: User | null) => {
    user.value = u
  }

  const isLoggedIn = !!user.value

  return { user, setUser, get isLoggedIn() { return !!user.value } }
})
