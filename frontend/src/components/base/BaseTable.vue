<template>
  <div class="overflow-auto">
    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
      <thead class="bg-gray-50 dark:bg-gray-900">
        <tr>
          <th v-for="h in headers" :key="h" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ h }}</th>
        </tr>
      </thead>
      <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
        <tr v-for="row in rows" :key="rowKey(row)">
          <td v-for="(cell, idx) in rowCells(row)" :key="idx" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{ headers: string[]; rows: any[]; rowKey?: (r: any) => string | number }>()

function rowKey(row: any) {
  return props.rowKey ? props.rowKey(row) : JSON.stringify(row)
}

function rowCells(row: any) {
  if (Array.isArray(row)) return row
  // Return object values
  return Object.values(row)
}
</script>
