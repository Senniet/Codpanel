export interface Server {
  id: string | number
  name: string
  type?: string | null
  status: string
  active_state?: string | null
  pid?: number | null
  uptime?: string | null
  started_at?: string | null
  cpu_percent?: number | null
  memory_mb?: number | null
  players?: number | null
  max_players?: number | null
  map?: string | null
  version?: string | null
}
