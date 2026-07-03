import { get, post } from './api/axios'
import type { Server } from '@/types/server'
import type { PaginatedResponse } from '@/types/api'

export interface ServerListParams {
  q?: string
  status?: string
  page?: number
  per_page?: number
}

export const serversService = {
  async list(params?: ServerListParams): Promise<Server[]> {
    const query = new URLSearchParams()
    if (params) {
      if (params.q) query.set('q', params.q)
      if (params.status) query.set('status', params.status)
      if (params.page) query.set('page', String(params.page))
      if (params.per_page) query.set('per_page', String(params.per_page))
    }
    const path = query.toString() ? `/servers?${query.toString()}` : '/servers'
    return await get<Server[]>(path)
  },

  async get(id: string | number): Promise<Server> {
    return await get<Server>(`/servers/${id}`)
  },

  async performAction(id: string | number, action: 'start' | 'stop' | 'restart' | 'kill'): Promise<void> {
    // POST /servers/:id/actions { action }
    await post(`/servers/${id}/actions`, { action })
  },

  // Tabs
  async getOverview(id: string | number): Promise<any> {
    return await get(`/servers/${id}/overview`)
  },

  async getConsole(id: string | number): Promise<any> {
    return await get(`/servers/${id}/console`) // may return recent lines
  },

  async getFiles(id: string | number): Promise<any> {
    return await get(`/servers/${id}/files`)
  },

  async getConfig(id: string | number): Promise<any> {
    return await get(`/servers/${id}/config`)
  },

  async getBackups(id: string | number): Promise<any> {
    return await get(`/servers/${id}/backups`)
  },

  async getMetrics(id: string | number): Promise<any> {
    return await get(`/servers/${id}/metrics`)
  }
}
