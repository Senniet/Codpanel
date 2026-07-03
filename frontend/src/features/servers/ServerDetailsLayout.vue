<template>
  <div>
    <BaseCard>
      <div class="flex items-center justify-between">
        <div>
          <div class="text-xl font-semibold">{{ server?.name || 'Server' }}</div>
          <div class="text-sm text-gray-500">ID: {{ server?.id }}</div>
        </div>
        <div class="flex items-center gap-2">
          <BaseBadge :variant="statusVariant(server?.status)">{{ server?.status || 'unknown' }}</BaseBadge>
          <BaseButton @click="refresh">Refresh</BaseButton>
        </div>
      </div>
    </BaseCard>

    <div class="mt-4">
      <nav class="flex space-x-2 border-b pb-2">
        <router-link :to="{ name: 'ServerOverview', params: { id: serverId } }" class="px-3 py-2">Overview</router-link>
        <router-link :to="{ name: 'ServerConsole', params: { id: serverId } }" class="px-3 py-2">Console</router-link>
        <router-link :to="{ name: 'ServerFiles', params: { id: serverId } }" class="px-3 py-2">Files</router-link>
        <router-link :to="{ name: 'ServerConfiguration', params: { id: serverId } }" class="px-3 py-2">Configuration</router-link>
        <router-link :to="{ name: 'ServerBackups', params: { id: serverId } }" class="px-3 py-2">Backups</router-link>
        <router-link :to="{ name: 'ServerMetrics', params: { id: serverId } }" class="px-3 py-2">Metrics</router-link>
      </nav>

      <div class="mt-4">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { serversService } from '@/services/servers.service'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseBadge from '@/components/base/BaseBadge.vue'
import BaseButton from '@/components/base/BaseButton.vue'

const route = useRoute()
const serverId = route.params.id as string
const server = ref(null as any)

async function refresh() {
  try {
    server.value = await serversService.get(serverId)
  } catch (e) {
    // error will be displayed in child routes
  }
}

onMounted(refresh)

function statusVariant(s: string | undefined) {
  if (!s) return 'default'
  if (s === 'running') return 'success'
  if (s === 'stopped') return 'default'
  if (s === 'crashed') return 'danger'
  return 'default'
}
</script>
