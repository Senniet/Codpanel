export interface DashboardOverview {
  totalServers: number
  onlineServers: number
  offlineServers: number
  connectedPlayers: number
  cpuUsagePercent: number // 0-100
  memoryUsagePercent: number // 0-100
}

export interface ActivityItem {
  id: string | number
  type: 'info' | 'warning' | 'error'
  message: string
  created_at: string // ISO timestamp
}

export interface QuickAction {
  id: string | number
  name: string
  description?: string
  endpoint?: string
}

export interface LogEntry {
  id: string | number
  level: 'info' | 'warning' | 'error'
  message: string
  timestamp: string // ISO timestamp
}
