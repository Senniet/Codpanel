<template>
  <input
    :class="classes"
    :value="modelValue"
    @input="onInput"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{ modelValue?: string }>(), { modelValue: '' })
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const classes = computed(() => 'w-full px-3 py-2 border rounded bg-gray-50 dark:bg-gray-700')

function onInput(e: Event) {
  const target = e.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>
