<template>
  <div>
    <BaseTable :headers="['Name', 'Version', 'Map', 'Players', 'CPU%', 'RAM MB', 'Status', 'Actions']" :rows="rows" :rowKey="r => r.id" />
    <div class="mt-4 space-y-2">
      <div v-for="s in servers" :key="s.id" class="p-2 bg-white dark:bg-gray-800 rounded flex items-center justify-between">
        <div>
          <div class="font-medium">{{ s.name }}</div>
          <div class="text-sm text-gray-500">
            {{ s.map ?? '—' }}<span v-if="s.version"> · v{{ s.version }}</span>
          </div>
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

const rows = computed(() => props.servers.map(s => [
  s.name,
  s.version ?? '—',
  s.map ?? '—',
  s.players !== null && s.players !== undefined
    ? (s.max_players !== null && s.max_players !== undefined ? `${s.players}/${s.max_players}` : String(s.players))
    : '—',
  s.cpu_percent !== null && s.cpu_percent !== undefined ? s.cpu_percent + '%' : '—',
  s.memory_mb !== null && s.memory_mb !== undefined ? s.memory_mb.toFixed(0) + ' MB' : '—',
  s.status || '—',
  ''
]))

function openDetails(id: string | number) {
  router.push({ name: 'ServerDetails', params: { id } })
}
</script>
