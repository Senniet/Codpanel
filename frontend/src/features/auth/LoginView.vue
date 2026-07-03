<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <BaseCard>
        <template #default>
          <h2 class="text-2xl font-semibold mb-4">Sign in to {{ appName }}</h2>
          <form @submit.prevent="submit">
            <div class="mb-4">
              <label class="block text-sm mb-1">Username</label>
              <BaseInput v-model="username" type="text" />
            </div>
            <div class="mb-4">
              <label class="block text-sm mb-1">Password</label>
              <BaseInput v-model="password" type="password" />
            </div>

            <div v-if="error" class="mb-4 text-sm text-red-600">{{ error }}</div>

            <div class="flex items-center justify-between">
              <BaseButton type="submit" :disabled="loading">
                <span v-if="loading">Signing in…</span>
                <span v-else>Sign in</span>
              </BaseButton>
            </div>
          </form>
        </template>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/app/stores/auth'
import BaseCard from '@/components/base/BaseCard.vue'
import BaseInput from '@/components/base/BaseInput.vue'
import BaseButton from '@/components/base/BaseButton.vue'

const appName = import.meta.env.VITE_APP_NAME || 'CodPanel'
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const submit = async () => {
  error.value = ''
  loading.value = true
  const redirect = (route.query.redirect as string) || '/dashboard'
  try {
    await auth.login(username.value, password.value, redirect)
    // auth.login will navigate via router
  } catch (e: any) {
    error.value = e?.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
