export interface User {
  id: number
  username: string
  email?: string
  token?: string
}

export interface Server {
  id: number | string
  name: string
  ip: string
  status?: 'online' | 'offline' | 'maintenance'
  players?: number
}

export interface ApiResponse<T = any> {
  data?: T
  success?: boolean
  message?: string
}
