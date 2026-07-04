<template>
  <div class="fixed inset-0 flex items-center justify-center z-50">
    <div class="absolute inset-0 bg-black opacity-50" @click="$emit('cancel')"></div>
    <div class="bg-white dark:bg-gray-800 rounded shadow p-4 z-10 w-full max-w-lg space-y-4">
      <div class="flex items-center justify-between">
        <div class="text-lg font-semibold">Start Server: {{ serverName }}</div>
        <button @click="$emit('cancel')" class="text-gray-600 dark:text-gray-300">✕</button>
      </div>

      <div v-if="loading" class="flex items-center gap-2 text-sm text-gray-500">
        <BaseSpinner />
        <span>Loading maps…</span>
      </div>

      <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>

      <div v-else-if="maps.length === 0" class="text-sm text-gray-500">No maps available.</div>

      <div v-else>
        <label class="block text-sm font-medium mb-1">Map</label>
        <select
          v-model="selectedMap"
          class="w-full border rounded px-2 py-1 bg-white dark:bg-gray-800 dark:text-gray-100"
        >
          <option v-for="map in maps" :key="map" :value="map">{{ map }}</option>
        </select>
      </div>

      <div class="flex justify-end gap-2">
        <BaseButton @click="$emit('cancel')">Cancel</BaseButton>
        <BaseButton :disabled="!canStart" @click="onConfirm">Start</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import BaseButton from '@/components/base/BaseButton.vue'
import BaseSpinner from '@/components/base/BaseSpinner.vue'
import { useMaps } from '@/composables/useMaps'

const props = defineProps<{
  serverId: string
  serverName: string
}>()

const emit = defineEmits<{
  (e: 'confirm', map: string): void
  (e: 'cancel'): void
}>()

const { maps, loading, error, selectedMap, loadMaps, canStart } = useMaps(props.serverId)

onMounted(() => {
  loadMaps()
})

function onConfirm() {
  if (selectedMap.value) {
    emit('confirm', selectedMap.value)
  }
}
</script>
