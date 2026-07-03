<template>
  <button :class="buttonClasses" @click="$emit('click')"><slot /></button>
</template>

<script setup lang="ts">
import { computed, defineProps } from 'vue'

const props = defineProps<{ variant?: 'primary' | 'danger' }>()

const buttonClasses = computed(() => {
  const base = 'px-3 py-1 rounded '
  if (props.variant === 'danger') return base + 'bg-red-600 text-white'
  return base + 'bg-blue-600 text-white'
})
</script>
