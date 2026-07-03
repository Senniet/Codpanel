<template>
  <DashboardLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-xl font-semibold mb-4">Server Details</h1>
        <div class="bg-white dark:bg-gray-800 rounded shadow p-4">
          <div class="text-lg font-medium">{{ server.name }}</div>
          <div class="text-sm text-gray-500">IP: {{ server.ip }}</div>
          <div class="mt-3">Status: <span class="font-semibold">{{ server.status }}</span></div>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import type { Server } from '@/types'

const route = useRoute()
const id = route.params.id

const server = ref<Server>({ id: id ?? '1', name: `Server ${id}`, ip: '192.168.1.x', status: 'online' })
</script>
