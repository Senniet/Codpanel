export interface Server {
  id?: number | string
  name: string
  status: 'running' | 'offline' | 'failed' | 'starting' | string
  cpu_percent: number
  memory_mb: number
  uptime: string
  pid: number | null
  started_at?: string | null
  ip?: string
  game?: string
  map?: string
  cpu?: number
  ram?: number
  players?: number
}
