/**
 * Vue Router Configuration
 */

import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/planner',
    name: 'Planner',
    component: () => import('@/views/Planner.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/map-test',
    name: 'MapTest',
    component: () => import('@/views/MapTest.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/qa',
    name: 'QA',
    component: () => import('@/views/QA.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/copywriter',
    name: 'Copywriter',
    component: () => import('@/views/Copywriter.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile/edit',
    name: 'ProfileEdit',
    component: () => import('@/views/ProfileEdit.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route guards
router.beforeEach(async (to, from, next) => {
  // 动态导入 authStore 以避免循环依赖
  const { useAuthStore } = await import('@/stores/auth')
  const authStore = useAuthStore()

  // 如果 localStorage 有 token，尝试验证其有效性
  if (!authStore.isAuthenticated && localStorage.getItem('token')) {
    authStore.initFromStorage()

    // 验证 token 是否真正有效
    try {
      // 导入 api 工具来验证 token
      const api = (await import('@/utils/api')).default
      await api.get('/api/v1/auth/me')
      // Token 有效，继续
    } catch (error) {
      // Token 无效，清除本地存储
      console.warn('Token 验证失败，清除本地存储:', error)
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      authStore.user = null
      authStore.token = null
      authStore.isAuthenticated = false
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/planner')
  } else {
    next()
  }
})

export default router
