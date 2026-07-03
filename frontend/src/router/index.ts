import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/features/auth/LoginView.vue'
import DashboardView from '@/features/dashboard/DashboardView.vue'
import ServersView from '@/features/servers/ServersView.vue'
import ServerDetailsView from '@/features/servers/ServerDetailsView.vue'
import SettingsView from '@/features/settings/SettingsView.vue'
import { useAuthStore } from '@/app/stores/auth'

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
    component: ServerDetailsView,
    meta: { requiresAuth: true },
    props: true
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

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
