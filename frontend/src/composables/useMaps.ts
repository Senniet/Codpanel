import { ref, computed } from 'vue'
import api from '@/services/api/axios'

export function useMaps(serverId: string) {
  const maps = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedMap = ref<string | null>(null)

  const loadMaps = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await api.get<string[]>(`/servers/${serverId}/maps`)
      maps.value = response || []

      if (maps.value.length > 0) {
        selectedMap.value = maps.value[0]
      }
    } catch (err: any) {
      error.value = err?.message || 'Failed to load maps'
      maps.value = []
    } finally {
      loading.value = false
    }
  }

  const canStart = computed(() => !loading.value && maps.value.length > 0)

  return {
    maps,
    loading,
    error,
    selectedMap,
    loadMaps,
    canStart,
  }
}
