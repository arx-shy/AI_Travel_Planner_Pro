import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'
import type { User, LoginRequest, RegisterRequest } from '@/types/api'

interface UserQuotaInfo {
  membership_level: string
  is_pro: boolean
  plan_usage_count: number
  plan_limit: number
  remaining_plans: number
  copywriter_usage_count: number
  copywriter_limit: number
  last_reset: string | null
  unlimited: boolean
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const quotaInfo = ref<UserQuotaInfo | null>(null)

  // 计算属性
  const isPro = computed(() => user.value?.membership_level === 'pro')
  const remainingPlans = computed(() => {
    if (!quotaInfo.value) return 0
    return quotaInfo.value.unlimited ? -1 : quotaInfo.value.remaining_plans
  })

  // 从本地存储初始化
  const initFromStorage = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
      isAuthenticated.value = true
    }
  }

  // 登录
  const login = async (credentials: LoginRequest) => {
    isLoading.value = true
    try {
      console.log('Login request:', credentials)
      const response = await api.post<any>('/api/v1/auth/login', credentials)
      console.log('Login response:', response)

      // 直接从response中获取数据
      user.value = response.user
      token.value = response.access_token
      isAuthenticated.value = true

      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      // 加载配额信息
      await fetchQuota()

      return { success: true }
    } catch (error) {
      console.error('Login failed:', error)
      return { success: false, error: '登录失败，请检查邮箱和密码' }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const register = async (data: RegisterRequest) => {
    isLoading.value = true
    try {
      console.log('Register request:', data)
      const response = await api.post<any>('/api/v1/auth/register', data)
      console.log('Register response:', response)

      // 直接从response中获取数据
      user.value = response.user
      token.value = response.access_token
      isAuthenticated.value = true

      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      // 加载配额信息
      await fetchQuota()

      return { success: true }
    } catch (error) {
      console.error('Register failed:', error)
      return { success: false, error: '注册失败，请稍后重试' }
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = async () => {
    try {
      await api.post('/api/v1/auth/logout')
    } catch (error) {
      console.warn('Logout request failed:', error)
    }
    user.value = null
    token.value = null
    isAuthenticated.value = false
    quotaInfo.value = null

    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 获取当前用户信息
  const fetchCurrentUser = async () => {
    if (!isAuthenticated.value) return

    try {
      const response = await api.get<User>('/api/v1/auth/me')
      user.value = response
      localStorage.setItem('user', JSON.stringify(response))
    } catch (error) {
      console.error('Fetch current user failed:', error)
    }
  }

  // 获取配额信息
  const fetchQuota = async () => {
    if (!isAuthenticated.value) return

    try {
      const response = await api.get<UserQuotaInfo>('/api/v1/auth/quota')
      quotaInfo.value = response
      console.log('Quota info:', response)
    } catch (error) {
      console.error('Fetch quota failed:', error)
    }
  }

  // 更新用户信息
  const updateProfile = async (data: Partial<User>) => {
    if (!user.value) return { success: false, error: '用户未登录' }

    try {
      const response = await api.put<User>('/api/v1/auth/me', data)
      user.value = response
      localStorage.setItem('user', JSON.stringify(user.value))

      return { success: true }
    } catch (error) {
      console.error('Update profile failed:', error)
      return { success: false, error: '更新失败' }
    }
  }

  return {
    // 状态
    user,
    token,
    isAuthenticated,
    isLoading,
    quotaInfo,

    // 计算属性
    isPro,
    remainingPlans,

    // 方法
    initFromStorage,
    login,
    register,
    logout,
    fetchCurrentUser,
    fetchQuota,
    updateProfile
  }
})
