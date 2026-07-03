<template>
  <DashboardLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-xl font-semibold mb-4">Servers</h1>
        <div class="space-y-3">
          <div v-if="loading" class="text-sm text-gray-500">Loading...</div>
          <div v-else>
            <div v-for="s in servers" :key="s.id" class="p-4 bg-white dark:bg-gray-800 rounded shadow flex items-center justify-between">
              <div>
                <div class="font-medium">{{ s.name }}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400">{{ s.ip }}</div>
              </div>
              <router-link :to="`/servers/${s.id}`" class="text-blue-600 dark:text-blue-400">View</router-link>
            </div>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ref, onMounted } from 'vue'
import type { Server } from '@/types/server'
import { serversService } from '@/services/servers.service'

const servers = ref<Server[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    servers.value = await serversService.list()
  } catch (e) {
    console.error('Failed to fetch servers', e)
  } finally {
    loading.value = false
  }
})
</script>
