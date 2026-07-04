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
          <div v-for="i in 6" :key="i" class="p-4 bg-white dark:bg-gray-800 rounded shadow">
            <div class="flex items-start justify-between">
              <div class="flex-1 pr-2 space-y-2">
                <div class="h-5 w-2/3 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="h-4 w-1/2 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="h-4 w-1/3 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="grid grid-cols-2 gap-2 mt-2">
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                  <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                </div>
              </div>
              <div class="space-y-2 shrink-0">
                <div class="h-5 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="h-7 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="h-7 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
              </div>
            </div>
          </div>
        </div>

        <div v-else>
          <div v-if="servers.length === 0" class="flex flex-col items-center justify-center py-16 text-center">
            <div class="text-4xl mb-4">🖥️</div>
            <div class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-1">No servers found</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">
              No servers match your current filters.
              <span v-if="!q && !status">Configure servers in <router-link to="/settings" aria-label="Configure servers in Settings" class="underline text-blue-500">Settings</router-link> to get started.</span>
              <span v-else>Try clearing your search or status filter.</span>
            </div>
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

import { ref, watch, onMounted } from 'vue'
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

onMounted(load)

watch([q, status], () => {
  // small debounce could be added
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
