<template>
  <div>
    <BaseCard title="Console">
      <div v-if="loading" class="h-40 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"></div>
      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
      <div v-else-if="lines.length === 0" class="text-sm text-gray-500">No console output.</div>
      <div v-else class="font-mono text-sm bg-black text-white p-2 rounded overflow-auto max-h-96">
        <div v-for="(l,i) in lines" :key="i">{{ l }}</div>
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

const lines = ref<string[]>([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const res = await serversService.getConsole(id)
    // Expect an array of strings or objects; normalize to strings
    lines.value = Array.isArray(res) ? res.map((r: any) => (typeof r === 'string' ? r : r.line || JSON.stringify(r))) : []
  } catch (e: any) {
    error.value = e?.message || 'Failed to load console'
  } finally {
    loading.value = false
  }
})
</script>
