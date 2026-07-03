<template>
  <div>
    <BaseCard title="Configuration">
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 4" :key="i" class="h-6 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"></div>
      </div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="!config" class="text-sm text-gray-500">No configuration available.</div>
      <div v-else>
        <pre class="bg-gray-50 dark:bg-gray-900 p-3 rounded text-sm overflow-auto">{{ JSON.stringify(config, null, 2) }}</pre>
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

const config = ref<any | null>(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    config.value = await serversService.getConfig(id)
  } catch (e: any) {
    error.value = e?.message || 'Failed to load configuration'
  } finally {
    loading.value = false
  }
})
</script>
