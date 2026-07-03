import api from './api/axios'
import type { User } from '@/types'

export const authService = {
  async login(username: string, password: string): Promise<User> {
    const res = await api.post('/auth/login', { username, password })
    return res.data
  },
  async me(): Promise<User> {
    const res = await api.get('/auth/me')
    return res.data
  }
}
