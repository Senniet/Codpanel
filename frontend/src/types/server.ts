export interface Server {
  id: number | string
  name: string
  ip: string
  status?: 'online' | 'offline' | 'maintenance'
  players?: number
}
