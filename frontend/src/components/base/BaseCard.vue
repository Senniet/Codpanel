<template>
  <div class="p-4 bg-white dark:bg-gray-800 rounded shadow">
    <div class="font-semibold mb-2">{{ title }}</div>
    <div><slot /></div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{ title?: string }>()
</script>
