<template>
  <span :class="badgeClasses"><slot /></span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { defineProps } from 'vue'

const props = defineProps<{ variant?: 'default' | 'success' | 'danger' }>()

const badgeClasses = computed(() => {
  const base = 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium'
  if (props.variant === 'success') return base + ' bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  if (props.variant === 'danger') return base + ' bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  return base + ' bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
})
</script>
