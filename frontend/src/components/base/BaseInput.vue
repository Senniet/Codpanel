<template>
  <input :class="classes" v-bind="$attrs" />
</template>

<script setup lang="ts">
import { computed } from 'vue'

const classes = computed(() => 'w-full px-3 py-2 border rounded bg-gray-50 dark:bg-gray-700')
</script>
