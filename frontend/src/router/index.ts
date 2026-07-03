import { createRouter, createWebHistory } from 'vue-router'
import type { RouteLocationNormalized } from 'vue-router'

import LoginView from '@/features/auth/LoginView.vue'
import DashboardView from '@/features/dashboard/DashboardView.vue'
import ServersView from '@/features/servers/ServersView.vue'
// Server details layout is lazy loaded below
import SettingsView from '@/features/settings/SettingsView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'Login', component: LoginView },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/servers',
    name: 'Servers',
    component: ServersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/servers/:id',
    name: 'ServerDetails',
    component: () => import('@/features/servers/ServerDetailsLayout.vue'),
    meta: { requiresAuth: true },
    props: true,
    children: [
      { path: '', redirect: { name: 'ServerOverview' } },
      { path: 'overview', name: 'ServerOverview', component: () => import('@/features/servers/details/OverviewTab.vue'), props: true },
      { path: 'console', name: 'ServerConsole', component: () => import('@/features/servers/details/ConsoleTab.vue'), props: true },
      { path: 'files', name: 'ServerFiles', component: () => import('@/features/servers/details/FilesTab.vue'), props: true },
      { path: 'configuration', name: 'ServerConfiguration', component: () => import('@/features/servers/details/ConfigurationTab.vue'), props: true },
      { path: 'backups', name: 'ServerBackups', component: () => import('@/features/servers/details/BackupsTab.vue'), props: true },
      { path: 'metrics', name: 'ServerMetrics', component: () => import('@/features/servers/details/MetricsTab.vue'), props: true }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Router guards using dynamic import of the auth store to avoid circular deps
router.beforeEach(async (to: RouteLocationNormalized) => {
  // Public route: /login
  if (to.path === '/login') {
    try {
      const mod = await import('@/app/stores/auth')
      const { useAuthStore } = mod
      const auth = useAuthStore()
      if (auth.isAuthenticated()) {
        return { name: 'Dashboard' }
      }
    } catch (e) {
      // ignore
    }
    return true
  }

  // Protected routes
  if (to.meta.requiresAuth) {
    try {
      const mod = await import('@/app/stores/auth')
      const { useAuthStore } = mod
      const auth = useAuthStore()
      if (!auth.isAuthenticated()) {
        return { name: 'Login', query: { redirect: to.fullPath } }
      }
    } catch (e) {
      return { name: 'Login', query: { redirect: to.fullPath } }
    }
  }

  return true
})

export default router
