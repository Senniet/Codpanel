<template>
  <div>
    <BaseCard title="Backups">
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 4" :key="i" class="h-6 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"></div>
      </div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="backups.length === 0" class="text-sm text-gray-500">No backups found.</div>
      <div v-else>
        <BaseTable :headers="['Name', 'Created']" :rows="backups.map(b => [b.name, new Date(b.created_at).toLocaleString()])" :rowKey="r => r[0]" />
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

const backups = ref<any[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    backups.value = await serversService.getBackups(id)
  } catch (e: any) {
    error.value = e?.message || 'Failed to load backups'
  } finally {
    loading.value = false
  }
})
</script>
