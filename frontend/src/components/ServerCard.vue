<template>
  <div class="p-4 bg-white dark:bg-gray-800 rounded shadow">
    <div class="flex items-start justify-between">
      <div class="font-semibold text-lg">{{ server.name }}</div>
      <BaseBadge :variant="statusVariant">{{ server.status }}</BaseBadge>
    </div>

    <div class="mt-3 space-y-1 text-sm text-gray-700 dark:text-gray-200">
      <div>CPU: {{ formatCpu(server.cpu_percent) }}</div>
      <div>RAM: {{ formatMemory(server.memory_mb) }}</div>
      <div>Uptime: {{ formatUptime(server.uptime) }}</div>
      <div>PID: {{ server.pid ?? '-' }}</div>
      <div>Started: {{ formatStartedAt(server.started_at) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseBadge from '@/components/base/BaseBadge.vue'
import type { Server } from '@/types/server'

const props = defineProps<{
  server: Server
}>()

const statusVariant = computed(() => {
  if (props.server.status === 'running') return 'success'
  if (props.server.status === 'failed') return 'danger'
  if (props.server.status === 'starting') return 'warning'
  return 'default'
})

function formatCpu(value: number) {
  return `${Math.round(Number(value) || 0)}%`
}

function formatMemory(value: number) {
  return `${Math.trunc(Number(value) || 0)} MB`
}

function formatUptime(value: string) {
  const seconds = Math.max(0, Number.parseInt(String(value).replace(/[^\d]/g, ''), 10) || 0)
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  return `${hours}h ${minutes}m ${secs}s`
}

function formatStartedAt(value?: string | null) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return '-'
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${pad(date.getDate())}-${pad(date.getMonth() + 1)}-${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}`
}
</script>
