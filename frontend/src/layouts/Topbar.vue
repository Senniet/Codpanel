<template>
  <header class="flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-800 border-b dark:border-gray-700">
    <div class="flex items-center space-x-4">
      <button @click="$emit('toggleSidebar')" class="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 5h14a1 1 0 010 2H3a1 1 0 010-2zm0 4h14a1 1 0 010 2H3a1 1 0 010-2zm0 4h14a1 1 0 010 2H3a1 1 0 010-2z" clip-rule="evenodd" /></svg>
      </button>
      <div class="text-lg font-semibold">Dashboard</div>
    </div>
    <div class="flex items-center space-x-3">
      <button @click="toggleDark" class="px-3 py-1 rounded bg-gray-100 dark:bg-gray-700">Toggle</button>
      <div class="w-8 h-8 rounded bg-gray-200 dark:bg-gray-600"></div>
      <button @click="logout" class="px-3 py-1 rounded bg-red-600 text-white">Logout</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useUiStore } from '@/app/stores/ui'
import { useDark } from '@/composables/useDarkMode'
import { useAuthStore } from '@/app/stores/auth'

const ui = useUiStore()
const { isDark, toggle } = useDark()
const auth = useAuthStore()

const toggleDark = () => {
  toggle()
  ui.dark = isDark.value
}

const logout = async () => {
  await auth.logout()
}
</script>
