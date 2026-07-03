import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarOpen = ref(true)
  const dark = ref(false)

  const toggleSidebar = () => { sidebarOpen.value = !sidebarOpen.value }
  const toggleDark = () => { dark.value = !dark.value }

  return { sidebarOpen, dark, toggleSidebar, toggleDark }
})
