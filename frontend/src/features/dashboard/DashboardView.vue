<template>
  <DashboardLayout>
    <template #default>
      <div class="p-6">
        <h1 class="text-2xl font-semibold mb-4">Welcome back</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <BaseCard title="Servers">
            <p class="text-sm text-gray-600 dark:text-gray-300">Manage your game servers.</p>
          </BaseCard>
          <BaseCard title="Players">
            <p class="text-sm text-gray-600 dark:text-gray-300">Live player information.</p>
          </BaseCard>
          <BaseCard title="Settings">
            <p class="text-sm text-gray-600 dark:text-gray-300">Configure your account and panel.</p>
          </BaseCard>
        </div>
      </div>
    </template>
  </DashboardLayout>
</template>

<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import BaseCard from '@/components/base/BaseCard.vue'
</script>
