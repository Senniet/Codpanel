<template>
  <AppLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-xl font-semibold mb-4">Settings</h1>
        <BaseCard>
          <p class="text-sm text-gray-600 dark:text-gray-300">User and application settings will be available here.</p>
        </BaseCard>
      </div>
    </template>
  </AppLayout>
</template>

<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue'
import BaseCard from '@/components/base/BaseCard.vue'
</script>
