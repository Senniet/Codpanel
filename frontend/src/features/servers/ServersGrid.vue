<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="s in servers" :key="s.id">
      <BaseCard>
        <div class="flex items-start justify-between">
          <div>
            <div class="text-lg font-semibold">{{ s.name }}</div>
            <div class="text-sm text-gray-500">{{ s.game }} — {{ s.map }}</div>
            <div class="mt-2 text-sm text-gray-600">Players: {{ s.players ?? 0 }}</div>
            <div class="mt-1 text-sm text-gray-600">CPU: {{ s.cpu ?? 0 }}% • RAM: {{ s.ram ?? 0 }}%</div>
          </div>
          <div class="flex flex-col items-end gap-2">
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
  if (s === 'stopped') return 'default'
  if (s === 'crashed') return 'danger'
  return 'default'
}

function openDetails(id: string | number) {
  router.push({ name: 'ServerDetails', params: { id } })
}
</script>
