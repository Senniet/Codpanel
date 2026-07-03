<template>
  <div>
    <BaseCard title="Files">
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 6" :key="i" class="h-6 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"></div>
      </div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="files.length === 0" class="text-sm text-gray-500">No files available.</div>
      <div v-else>
        <BaseTable :headers="['Name', 'Size']" :rows="files.map(f => [f.name, f.size])" :rowKey="r => r.name" />
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { serversService } from '@/services/servers.service'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseTable from '@/components/base/BaseTable.vue'

const route = useRoute()
const id = route.params.id as string

const files = ref<any[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    files.value = await serversService.getFiles(id)
  } catch (e: any) {
    error.value = e?.message || 'Failed to load files'
  } finally {
    loading.value = false
  }
})
</script>
