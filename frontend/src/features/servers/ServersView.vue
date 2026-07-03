<template>
  <AppLayout>
    <template #default>
      <div>
        <h1 class="text-xl font-semibold mb-4">Servers</h1>
        <div class="space-y-3">
          <div v-if="loading" class="text-sm text-gray-500"><BaseSpinner /></div>
          <div v-else>
            <div v-for="s in servers" :key="s.id">
              <BaseCard>
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium">{{ s.name }}</div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">{{ s.ip }}</div>
                  </div>
                  <router-link :to="`/servers/${s.id}`" class="text-blue-600 dark:text-blue-400">View</router-link>
                </div>
              </BaseCard>
            </div>
          </div>
        </div>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'
import { ref, onMounted } from 'vue'
import type { Server } from '@/types/server'
import { serversService } from '@/services/servers.service'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseSpinner from '@/components/base/BaseSpinner.vue'

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
