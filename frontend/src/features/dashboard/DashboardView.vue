<template>
  <AppLayout>
    <template #default>
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-semibold">Dashboard</h1>
          <div class="text-sm text-gray-500">Refreshes every 5 seconds</div>
        </div>

        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="i in 6" :key="i" class="h-36 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        </div>

        <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

        <div v-else-if="servers.length === 0" class="text-sm text-gray-500">No servers found.</div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <ServerCard v-for="(server, index) in servers" :key="server.id ?? `${server.name}-${index}`" :server="server" />
        </div>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import ServerCard from '@/components/ServerCard.vue'
import { serversService } from '@/services/servers.service'
import type { Server } from '@/types/server'

const servers = ref<Server[]>([])
const loading = ref(false)
const error = ref('')

let pollTimer: ReturnType<typeof setInterval> | null = null

async function loadServers() {
  loading.value = servers.value.length === 0
  error.value = ''
  try {
    servers.value = await serversService.list()
  } catch (e: any) {
    error.value = e?.message || 'Failed to load servers'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadServers()
  pollTimer = setInterval(loadServers, 5000)
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
})
</script>
