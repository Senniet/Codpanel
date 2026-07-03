<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div class="absolute inset-0 bg-black opacity-50" @click="close"></div>
    <div class="bg-white dark:bg-gray-800 rounded shadow p-4 z-10 w-full max-w-lg">
      <div class="flex justify-end">
        <button @click="close" class="text-gray-600 dark:text-gray-300">✕</button>
      </div>
      <div>
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

const props = defineProps<{ show: boolean }>()
const emit = defineEmits(['update:show'])

function close() {
  emit('update:show', false)
}
</script>
