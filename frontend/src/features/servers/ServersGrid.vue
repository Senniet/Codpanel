<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="s in servers" :key="s.id">
      <BaseCard>
        <div class="flex items-start justify-between">
          <div>
            <div class="text-lg font-semibold">{{ s.name }}</div>
            <div class="text-sm text-gray-500">Version: {{ textOrDash(s.version) }} • Map: {{ textOrDash(s.map) }}</div>
            <div class="mt-2 text-sm text-gray-600">Players: {{ numberOrDash(s.players) }} / {{ numberOrDash(s.max_players) }}</div>
            <div class="mt-1 text-sm text-gray-600">CPU: {{ percentOrDash(s.cpu_percent) }} • Memory: {{ memoryOrDash(s.memory_mb) }}</div>
            <div class="mt-1 text-sm text-gray-600">Uptime: {{ textOrDash(s.uptime) }} • PID: {{ numberOrDash(s.pid) }}</div>
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
  if (s === 'starting' || s === 'stopping') return 'warning'
  if (s === 'stopped') return 'default'
  if (s === 'crashed') return 'danger'
  return 'default'
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

function openDetails(id: string | number) {
  router.push({ name: 'ServerDetails', params: { id } })
}
</script>
