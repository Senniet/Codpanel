<template>
  <input
    :class="classes"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ modelValue?: string }>()
const classes = computed(() => 'w-full px-3 py-2 border rounded bg-gray-50 dark:bg-gray-700')
</script>
