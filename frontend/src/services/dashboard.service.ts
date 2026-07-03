import { get } from './api/axios'
import type { DashboardOverview, ActivityItem, QuickAction, LogEntry } from '@/types/dashboard'

export const dashboardService = {
  async getOverview(): Promise<DashboardOverview> {
    return await get<DashboardOverview>('/dashboard/overview')
  },

  async getRecentActivity(): Promise<ActivityItem[]> {
    return await get<ActivityItem[]>('/dashboard/activity')
  },

  async getQuickActions(): Promise<QuickAction[]> {
    return await get<QuickAction[]>('/dashboard/quick-actions')
  },

  async getLatestLogs(): Promise<LogEntry[]> {
    return await get<LogEntry[]>('/dashboard/logs')
  }
}
