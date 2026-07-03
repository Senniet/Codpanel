<template>
  <AppLayout>
    <template #default>
      <div class="space-y-6">
        <!-- Metrics grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <BaseCard v-for="card in metricCards" :key="card.key">
            <div class="flex items-start justify-between">
              <div>
                <div class="text-sm text-gray-500 dark:text-gray-400">{{ card.title }}</div>
                <div class="mt-2 text-2xl font-semibold">{{ card.display }}</div>
                <div v-if="card.sub" class="text-sm text-gray-500 dark:text-gray-400">{{ card.sub }}</div>
              </div>
              <div class="ml-4 flex items-center">
                <BaseBadge :variant="card.badgeVariant">{{ card.badge }}</BaseBadge>
              </div>
            </div>
            <div class="mt-3">
              <div v-if="loadingOverview" class="h-3 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
              <div v-else class="h-3 bg-gray-100 dark:bg-gray-800 rounded overflow-hidden">
                <div class="h-3 bg-blue-600 dark:bg-blue-400" :style="{ width: card.percent + '%' }"></div>
              </div>
            </div>
          </BaseCard>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Recent Activity -->
          <div class="lg:col-span-2">
            <BaseCard title="Recent Activity">
              <div v-if="loadingActivity" class="space-y-3">
                <div v-for="i in 5" :key="i" class="h-12 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
              </div>
              <div v-else>
                <div v-if="activity.length === 0" class="text-sm text-gray-500">No recent activity.</div>
                <div v-else class="space-y-3">
                  <div v-for="act in activity" :key="act.id" class="flex items-start justify-between">
                    <div>
                      <div class="text-sm font-medium">{{ act.message }}</div>
                      <div class="text-xs text-gray-500">{{ formatDate(act.created_at) }}</div>
                    </div>
                    <div>
                      <BaseBadge :variant="badgeFor(act.type)">{{ act.type }}</BaseBadge>
                    </div>
                  </div>
                </div>
              </div>
            </BaseCard>

            <!-- Quick Actions -->
            <BaseCard title="Quick Actions" class="mt-4">
              <div v-if="loadingActions" class="space-y-3">
                <div v-for="i in 3" :key="i" class="h-12 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
              </div>
              <div v-else>
                <div v-if="quickActions.length === 0" class="text-sm text-gray-500">No quick actions available.</div>
                <div v-else class="space-y-3">
                  <div v-for="a in quickActions" :key="a.id" class="flex items-center justify-between">
                    <div>
                      <div class="font-medium">{{ a.name }}</div>
                      <div class="text-sm text-gray-500">{{ a.description }}</div>
                    </div>
                    <div>
                      <BaseButton @click="runAction(a)">Run</BaseButton>
                    </div>
                  </div>
                </div>
              </div>
            </BaseCard>
          </div>

          <!-- Latest Logs -->
          <div>
            <BaseCard title="Latest Logs">
              <div v-if="loadingLogs" class="space-y-2">
                <div v-for="i in 6" :key="i" class="h-8 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
              </div>
              <div v-else>
                <div v-if="logs.length === 0" class="text-sm text-gray-500">No logs available.</div>
                <div v-else>
                  <BaseTable :headers="['Time', 'Level', 'Message']" :rows="logRows" :rowKey="r => r.id" />
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseTable from '@/components/base/BaseTable.vue'
import BaseSpinner from '@/components/base/BaseSpinner.vue'

import { ref, computed, onMounted } from 'vue'
import { dashboardService } from '@/services/dashboard.service'
import type { DashboardOverview, ActivityItem, QuickAction, LogEntry } from '@/types/dashboard'

const overview = ref<DashboardOverview | null>(null)
const activity = ref<ActivityItem[]>([])
const quickActions = ref<QuickAction[]>([])
const logs = ref<LogEntry[]>([])

const loadingOverview = ref(false)
const loadingActivity = ref(false)
const loadingActions = ref(false)
const loadingLogs = ref(false)

onMounted(async () => {
  await loadOverview()
  loadActivity()
  loadQuickActions()
  loadLogs()
})

async function loadOverview() {
  loadingOverview.value = true
  try {
    overview.value = await dashboardService.getOverview()
  } catch (e) {
    console.error('Failed to load overview', e)
  } finally {
    loadingOverview.value = false
  }
}

async function loadActivity() {
  loadingActivity.value = true
  try {
    activity.value = await dashboardService.getRecentActivity()
  } catch (e) {
    console.error('Failed to load activity', e)
  } finally {
    loadingActivity.value = false
  }
}

async function loadQuickActions() {
  loadingActions.value = true
  try {
    quickActions.value = await dashboardService.getQuickActions()
  } catch (e) {
    console.error('Failed to load quick actions', e)
  } finally {
    loadingActions.value = false
  }
}

async function loadLogs() {
  loadingLogs.value = true
  try {
    logs.value = await dashboardService.getLatestLogs()
  } catch (e) {
    console.error('Failed to load logs', e)
  } finally {
    loadingLogs.value = false
  }
}

const metricCards = computed(() => {
  const o = overview.value
  return [
    {
      key: 'total',
      title: 'Total Servers',
      display: o ? o.totalServers : '—',
      sub: '',
      badge: o ? String(o.totalServers) : '-',
      badgeVariant: 'default',
      percent: o ? Math.min(100, (o.totalServers ? (o.onlineServers / Math.max(1, o.totalServers)) * 100 : 0)) : 0
    },
    {
      key: 'online',
      title: 'Online Servers',
      display: o ? o.onlineServers : '—',
      sub: '',
      badge: o ? String(o.onlineServers) : '-',
      badgeVariant: 'success',
      percent: o ? Math.min(100, (o.onlineServers / Math.max(1, o.totalServers)) * 100) : 0
    },
    {
      key: 'offline',
      title: 'Offline Servers',
      display: o ? o.offlineServers : '—',
      sub: '',
      badge: o ? String(o.offlineServers) : '-',
      badgeVariant: 'danger',
      percent: o ? Math.min(100, (o.offlineServers / Math.max(1, o.totalServers)) * 100) : 0
    },
    {
      key: 'players',
      title: 'Connected Players',
      display: o ? o.connectedPlayers : '—',
      sub: '',
      badge: o ? String(o.connectedPlayers) : '-',
      badgeVariant: 'default',
      percent: o ? Math.min(100, (o.connectedPlayers / Math.max(1, o.totalServers * 100)) * 100) : 0
    },
    {
      key: 'cpu',
      title: 'CPU Usage',
      display: o ? o.cpuUsagePercent + '%' : '—',
      sub: '',
      badge: o ? o.cpuUsagePercent + '%' : '-',
      badgeVariant: 'default',
      percent: o ? o.cpuUsagePercent : 0
    },
    {
      key: 'memory',
      title: 'Memory Usage',
      display: o ? o.memoryUsagePercent + '%' : '—',
      sub: '',
      badge: o ? o.memoryUsagePercent + '%' : '-',
      badgeVariant: 'default',
      percent: o ? o.memoryUsagePercent : 0
    }
  ]
})

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleString()
  } catch (e) {
    return iso
  }
}

function badgeFor(type: string) {
  if (type === 'warning') return 'warning'
  if (type === 'error') return 'danger'
  return 'default'
}

function logRows() {
  return logs.value.map(l => ({ id: l.id, time: new Date(l.timestamp).toLocaleString(), level: l.level, message: l.message }))
}

async function runAction(a: QuickAction) {
  // For now, show an alert — in a real app we'd call an endpoint
  alert(`Running action: ${a.name}`)
}
</script>
