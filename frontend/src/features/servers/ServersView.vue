<template>
  <DashboardLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-xl font-semibold mb-4">Servers</h1>
        <div class="space-y-3">
          <div v-for="s in servers" :key="s.id" class="p-4 bg-white dark:bg-gray-800 rounded shadow flex items-center justify-between">
            <div>
              <div class="font-medium">{{ s.name }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ s.ip }}</div>
            </div>
            <router-link :to="`/servers/${s.id}`" class="text-blue-600 dark:text-blue-400">View</router-link>
          </div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ref } from 'vue'
import type { Server } from '@/types'

const servers = ref<Server[]>([
  { id: 1, name: 'COD Server 1', ip: '192.168.1.10', status: 'online', players: 12 },
  { id: 2, name: 'COD Server 2', ip: '192.168.1.11', status: 'offline', players: 0 }
])
</script>
