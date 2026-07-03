<template>
  <div>
    <BaseCard title="Metrics">
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 4" :key="i" class="h-6 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"></div>
      </div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="!metrics" class="text-sm text-gray-500">No metrics available.</div>
      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-gray-500">CPU Usage</div>
            <div class="text-lg font-semibold">{{ metrics.cpu_percent }}%</div>
          </div>
          <div>
            <div class="text-sm text-gray-500">Memory Usage</div>
            <div class="text-lg font-semibold">{{ metrics.memory_percent }}%</div>
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

const metrics = ref<any | null>(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    metrics.value = await serversService.getMetrics(id)
  } catch (e: any) {
    error.value = e?.message || 'Failed to load metrics'
  } finally {
    loading.value = false
  }
})
</script>
