<template>
  <AppLayout>
    <template #default>
      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-3">
            <BaseInput v-model="q" placeholder="Search servers..." @input="onSearch" />
            <BaseButton @click="toggleView">{{ view === 'grid' ? 'Table' : 'Grid' }}</BaseButton>
          </div>
          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600 dark:text-gray-300">Status:</label>
            <select v-model="status" @change="onFilterChange" class="px-2 py-1 border rounded bg-white dark:bg-gray-800">
              <option value="">All</option>
              <option value="running">Running</option>
              <option value="stopped">Stopped</option>
              <option value="starting">Starting</option>
              <option value="stopping">Stopping</option>
              <option value="crashed">Crashed</option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="i in 6" :key="i" class="bg-white dark:bg-gray-800 rounded-lg p-4 animate-pulse">
            <div class="flex items-start justify-between">
              <div class="flex-1 space-y-2">
                <div class="h-5 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
              </div>
              <div class="ml-4 flex flex-col items-end gap-2 flex-shrink-0">
                <div class="h-5 w-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <div class="h-7 w-14 bg-gray-200 dark:bg-gray-700 rounded"></div>
                <div class="h-7 w-14 bg-gray-200 dark:bg-gray-700 rounded"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <div v-if="servers.length === 0" class="flex flex-col items-center justify-center py-12 text-center">
            <svg class="w-12 h-12 text-gray-400 dark:text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
            </svg>
            <p class="text-gray-500 dark:text-gray-400 mb-2">No servers found.</p>
            <router-link to="/settings" aria-label="Configure servers in Settings" class="text-blue-600 hover:underline text-sm dark:text-blue-400">Configure in Settings</router-link>
          </div>

          <div v-else>
            <ServersGrid v-if="view === 'grid'" :servers="servers" @action="onAction" />
            <ServersTable v-else :servers="servers" @action="onAction" />
          </div>
        </div>

        <BaseModal v-model:show="showActionModal">
          <template #default>
            <div class="space-y-4">
              <div class="text-lg font-semibold">Confirm {{ modalAction?.label }}</div>
              <div>Are you sure you want to {{ modalAction?.label.toLowerCase() }} <strong>{{ modalServer?.name }}</strong>?</div>
              <div class="flex justify-end gap-2">
                <BaseButton @click="showActionModal = false">Cancel</BaseButton>
                <BaseButton variant="danger" @click="confirmAction">Proceed</BaseButton>
              </div>
            </div>
          </template>
        </BaseModal>

        <div v-if="actionError" class="text-sm text-red-600">{{ actionError }}</div>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseModal from '@/components/base/BaseModal.vue'
import ServersGrid from '@/features/servers/ServersGrid.vue'
import ServersTable from '@/features/servers/ServersTable.vue'

import { ref, watch, onMounted, onUnmounted } from 'vue'
import { serversService } from '@/services/servers.service'
import type { Server } from '@/types/server'

const servers = ref<Server[]>([])
const loading = ref(false)
const q = ref('')
const status = ref('')
const view = ref<'grid' | 'table'>('grid')

const showActionModal = ref(false)
const modalServer = ref<Server | null>(null)
const modalAction = ref<{ key: string; label: string } | null>(null)
const actionError = ref('')

let pollTimer: ReturnType<typeof setInterval> | null = null

async function load() {
  loading.value = true
  try {
    servers.value = await serversService.list({ q: q.value || undefined, status: status.value || undefined })
  } catch (e: any) {
    console.error('Failed to load servers', e)
  } finally {
    loading.value = false
  }
}

async function pollLoad() {
  try {
    servers.value = await serversService.list({ q: q.value || undefined, status: status.value || undefined })
  } catch (e: any) {
    console.error('Failed to poll servers', e)
  }
}

onMounted(() => {
  load()
  pollTimer = setInterval(pollLoad, 5000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

watch([q, status], () => {
  load()
})

function toggleView() {
  view.value = view.value === 'grid' ? 'table' : 'grid'
}

function onSearch() {
  // handled by watch
}

function onFilterChange() {
  // handled by watch
}

function onAction(payload: { server: Server; action: string }) {
  modalServer.value = payload.server
  modalAction.value = { key: payload.action, label: payload.action.charAt(0).toUpperCase() + payload.action.slice(1) }
  actionError.value = ''
  showActionModal.value = true
}

async function confirmAction() {
  if (!modalServer.value || !modalAction.value) return
  const id = modalServer.value.id
  const key = modalAction.value.key as any
  try {
    await serversService.performAction(id, key)
    showActionModal.value = false
    // reload servers
    await load()
  } catch (e: any) {
    actionError.value = e?.message || 'Action failed'
  }
}
</script>
