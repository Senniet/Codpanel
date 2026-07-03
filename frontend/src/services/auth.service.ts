import api, { post, get } from './api/axios'
import type { User } from '@/types'

export const authService = {
  async login(username: string, password: string): Promise<User> {
    // Backend should create an HttpOnly session cookie on success and return the current user
    const res = await post<User>('/auth/login', { username, password })
    return res
  },

  async me(): Promise<User> {
    // Returns the current user if session cookie is present; will return 401 if not authenticated
    const res = await get<User>('/auth/me')
    return res
  },

  async logout(): Promise<void> {
    await post('/auth/logout')
  }
}
