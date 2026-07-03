<template>
  <div class="min-h-screen flex">
    <Sidebar />
    <div class="flex-1 flex flex-col min-h-screen">
      <Topbar />
      <main class="flex-1 bg-gray-50 dark:bg-gray-900">
        <div class="p-6">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/layouts/Sidebar.vue'
import Topbar from '@/layouts/Topbar.vue'
</script>
