<template>
  <div>
    <BaseCard title="Overview">
      <div v-if="loading" class="space-y-2">
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
      </div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="!overview" class="text-sm text-gray-500">No overview available.</div>
      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">Game</div>
            <div class="font-medium">{{ overview.game }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Map</div>
            <div class="font-medium">{{ overview.map }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Players</div>
            <div class="font-medium">{{ overview.players }}</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Uptime</div>
            <div class="font-medium">{{ overview.uptime }}</div>
          </div>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { serversService } from '@/services/servers.service'
import BaseCard from '@/components/base/BaseCard.vue'

const route = useRoute()
const id = route.params.id as string

const overview = ref<any | null>(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    overview.value = await serversService.getOverview(id)
  } catch (e: any) {
    error.value = e?.message || 'Failed to load overview'
  } finally {
    loading.value = false
  }
})
</script>
