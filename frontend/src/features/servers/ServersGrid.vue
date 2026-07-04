<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="s in servers" :key="s.id">
      <BaseCard>
        <div class="flex items-start justify-between">
          <div class="flex-1 min-w-0 pr-2">
            <div class="text-lg font-semibold truncate">{{ s.name }}</div>
            <div class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              <span>Map: <span class="text-gray-700 dark:text-gray-200">{{ s.map ?? '—' }}</span></span>
            </div>
            <div class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              <span>Version: <span class="text-gray-700 dark:text-gray-200">{{ s.version ?? '—' }}</span></span>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-sm text-gray-600 dark:text-gray-300">
              <div>
                Players:
                <span class="font-medium">
                  {{ s.players !== null && s.players !== undefined ? s.players : '—' }}/{{ s.max_players !== null && s.max_players !== undefined ? s.max_players : '—' }}
                </span>
              </div>
              <div>
                CPU:
                <span class="font-medium">{{ s.cpu_percent !== null && s.cpu_percent !== undefined ? Math.round(s.cpu_percent) + '%' : '—' }}</span>
              </div>
              <div>
                RAM:
                <span class="font-medium">{{ s.memory_mb !== null && s.memory_mb !== undefined ? Math.round(s.memory_mb) + ' MB' : '—' }}</span>
              </div>
              <div>
                PID:
                <span class="font-medium">{{ s.pid ?? '—' }}</span>
              </div>
              <div class="col-span-2">
                Uptime:
                <span class="font-medium">{{ s.uptime ?? '—' }}</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end gap-2 shrink-0">
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

function statusVariant(s: string | undefined) {
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
