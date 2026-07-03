<template>
  <DashboardLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-xl font-semibold mb-4">Settings</h1>
        <div class="bg-white dark:bg-gray-800 rounded shadow p-4">
          <p class="text-sm text-gray-600 dark:text-gray-300">User and application settings will be available here.</p>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
</script>
