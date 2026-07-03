import { get } from './api/axios'
import type { Server } from '@/types/server'

export const serversService = {
  async list(): Promise<Server[]> {
    const res = await get<Server[]>('/servers')
    return res
  },
  async get(id: string | number): Promise<Server> {
    const res = await get<Server>(`/servers/${id}`)
    return res
  }
}
