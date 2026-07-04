<template>
  <div>
    <BaseTable :headers="['Name', 'Version', 'Map', 'Players', 'CPU', 'Memory', 'Uptime', 'PID', 'Status']" :rows="rows" :rowKey="r => r.id" />
    <!-- Actions rendered below table per-row via slot imitation: we'll show simple inline action buttons under table -->
    <div class="mt-4 space-y-2">
      <div v-for="s in servers" :key="s.id" class="p-2 bg-white dark:bg-gray-800 rounded flex items-center justify-between">
        <div>
          <div class="font-medium">{{ s.name }}</div>
          <div class="text-sm text-gray-500">Version: {{ textOrDash(s.version) }} — Map: {{ textOrDash(s.map) }}</div>
        </div>
        <div class="flex items-center gap-2">
          <BaseButton @click="$emit('action', { server: s, action: 'start' })">Start</BaseButton>
          <BaseButton @click="$emit('action', { server: s, action: 'stop' })">Stop</BaseButton>
          <BaseButton @click="$emit('action', { server: s, action: 'restart' })">Restart</BaseButton>
          <BaseButton variant="danger" @click="$emit('action', { server: s, action: 'kill' })">Kill</BaseButton>
          <BaseButton @click="openDetails(s.id)">Open</BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseTable from '@/components/base/BaseTable.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import { useRouter } from 'vue-router'
import type { Server } from '@/types/server'
import { defineProps, computed } from 'vue'

const props = defineProps<{ servers: Server[] }>()
const router = useRouter()

const rows = computed(() =>
  props.servers.map(s => [
    s.name,
    textOrDash(s.version),
    textOrDash(s.map),
    `${numberOrDash(s.players)} / ${numberOrDash(s.max_players)}`,
    percentOrDash(s.cpu_percent),
    memoryOrDash(s.memory_mb),
    textOrDash(s.uptime),
    numberOrDash(s.pid),
    textOrDash(s.status)
  ])
)

function openDetails(id: string | number) {
  router.push({ name: 'ServerDetails', params: { id } })
}

function textOrDash(value: unknown) {
  if (value === null || value === undefined) return '—'
  const text = String(value).trim()
  return text ? text : '—'
}

function numberOrDash(value: unknown) {
  return typeof value === 'number' ? String(value) : '—'
}

function percentOrDash(value: unknown) {
  return typeof value === 'number' ? `${value}%` : '—'
}

function memoryOrDash(value: unknown) {
  return typeof value === 'number' ? `${value} MB` : '—'
}
</script>
