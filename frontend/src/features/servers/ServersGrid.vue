<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="s in servers" :key="s.id">
      <BaseCard>
        <div class="flex items-start justify-between">
          <div class="flex-1 min-w-0">
            <div class="text-lg font-semibold truncate">{{ s.name }}</div>
            <div class="text-sm text-gray-500 mt-0.5">
              {{ s.map ?? '—' }}<span v-if="s.version"> · v{{ s.version }}</span>
            </div>
            <div class="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Players: {{ s.players !== null && s.players !== undefined ? s.players : '—' }}
              <span v-if="s.max_players !== null && s.max_players !== undefined"> / {{ s.max_players }}</span>
            </div>
            <div class="mt-1 text-sm text-gray-600 dark:text-gray-400">
              CPU: {{ s.cpu_percent !== null && s.cpu_percent !== undefined ? s.cpu_percent + '%' : '—' }}
              · RAM: {{ s.memory_mb !== null && s.memory_mb !== undefined ? s.memory_mb.toFixed(0) + ' MB' : '—' }}
            </div>
            <div class="mt-1 text-sm text-gray-600 dark:text-gray-400">
              Uptime: {{ s.uptime ?? '—' }}
              <span v-if="s.pid !== null && s.pid !== undefined"> · PID: {{ s.pid }}</span>
            </div>
          </div>
          <div class="flex flex-col items-end gap-2 ml-4 flex-shrink-0">
            <BaseBadge :variant="statusVariant(s.status)">{{ s.status }}</BaseBadge>
            <div class="flex flex-col gap-1">
              <BaseButton @click="$emit('action', { server: s, action: 'start' })">Start</BaseButton>
              <BaseButton @click="$emit('action', { server: s, action: 'stop' })">Stop</BaseButton>
              <BaseButton @click="$emit('action', { server: s, action: 'restart' })">Restart</BaseButton>
              <BaseButton variant="danger" @click="$emit('action', { server: s, action: 'kill' })">Kill</BaseButton>
              <BaseButton @click="openDetails(s.id)">Open</BaseButton>
            </div>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '@/components/base/BaseCard.vue'
import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import { useRouter } from 'vue-router'
import type { Server } from '@/types/server'
import { defineProps } from 'vue'

const props = defineProps<{ servers: Server[] }>()
const router = useRouter()

function statusVariant(s: string | undefined): 'success' | 'warning' | 'danger' | 'default' {
  if (!s) return 'default'
  if (s === 'running') return 'success'
  if (s === 'starting') return 'warning'
  if (s === 'failed' || s === 'crashed') return 'danger'
  return 'default'
}

function openDetails(id: string | number) {
  router.push({ name: 'ServerDetails', params: { id } })
}
</script>
