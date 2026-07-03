<template>
  <aside class="w-64 bg-white dark:bg-gray-800 border-r dark:border-gray-700 min-h-screen p-4">
    <div class="mb-6">
      <div class="text-xl font-bold">{{ appName }}</div>
      <div class="text-xs text-gray-500">Admin</div>
    </div>

    <nav class="space-y-2">
      <router-link to="/dashboard" class="block px-2 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">Dashboard</router-link>
      <router-link to="/servers" class="block px-2 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">Servers</router-link>
      <router-link to="/settings" class="block px-2 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700">Settings</router-link>
    </nav>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const appName = import.meta.env.VITE_APP_NAME || 'CodPanel'
</script>
