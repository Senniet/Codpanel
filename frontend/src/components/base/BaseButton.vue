<template>
  <button :class="classes" @click="$emit('click')"><slot /></button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const classes = computed(() => 'px-3 py-1 rounded bg-blue-600 text-white')
</script>
