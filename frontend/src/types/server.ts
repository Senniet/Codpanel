export interface Server {
  id: string | number
  name: string
  status: string
  // Process/system stats (nullable)
  cpu_percent?: number | null
  memory_mb?: number | null
  uptime?: string | null
  pid?: number | null
  started_at?: string | null
  // Game info (nullable)
  map?: string | null
  players?: number | null
  max_players?: number | null
  version?: string | null
  // Optional metadata
  type?: string | null
  active_state?: string | null
  // Legacy fields (kept for backward compatibility with mock data)
  ip?: string
  game?: string
  cpu?: number
  ram?: number
}
