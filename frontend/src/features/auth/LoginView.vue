<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-2xl font-semibold mb-4">Sign in to CodPanel</h2>
        <form @submit.prevent="submit">
          <div class="mb-4">
            <label class="block text-sm mb-1">Username</label>
            <input v-model="username" type="text" class="w-full px-3 py-2 border rounded bg-gray-50 dark:bg-gray-700" />
          </div>
          <div class="mb-4">
            <label class="block text-sm mb-1">Password</label>
            <input v-model="password" type="password" class="w-full px-3 py-2 border rounded bg-gray-50 dark:bg-gray-700" />
          </div>
          <div class="flex items-center justify-between">
            <button class="px-4 py-2 bg-blue-600 text-white rounded">Sign in</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/app/stores/auth'

const username = ref('')
const password = ref('')

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const submit = async () => {
  const redirect = (route.query.redirect as string) || '/dashboard'
  try {
    await auth.login(username.value, password.value, redirect)
    // auth.login navigates via window.location.href on success
  } catch (e: any) {
    // Show a basic error; in a real app you'd use a toast or inline error
    alert(e?.message || 'Login failed')
  }
}
</script>
