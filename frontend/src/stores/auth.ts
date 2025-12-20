import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User, AuthToken, LoginRequest, RegisterRequest } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

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
      // TODO: 调用登录API
      // const response = await api.post<AuthResponse>('/auth/login', credentials)

      // 模拟登录成功
      const mockUser: User = {
        id: 1,
        email: credentials.email,
        name: 'Alex Chen',
        membership_level: 'pro',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      const mockToken: AuthToken = {
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
        expires_in: 3600
      }

      user.value = mockUser
      token.value = mockToken.access_token
      isAuthenticated.value = true

      // 存储到本地
      localStorage.setItem('token', mockToken.access_token)
      localStorage.setItem('user', JSON.stringify(mockUser))

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
      // TODO: 调用注册API
      // const response = await api.post<AuthResponse>('/auth/register', data)

      // 模拟注册成功
      const mockUser: User = {
        id: 1,
        email: data.email,
        name: data.name,
        membership_level: 'free',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      const mockToken: AuthToken = {
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
        expires_in: 3600
      }

      user.value = mockUser
      token.value = mockToken.access_token
      isAuthenticated.value = true

      // 存储到本地
      localStorage.setItem('token', mockToken.access_token)
      localStorage.setItem('user', JSON.stringify(mockUser))

      return { success: true }
    } catch (error) {
      console.error('Register failed:', error)
      return { success: false, error: '注册失败，请稍后重试' }
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false

    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 更新用户信息
  const updateProfile = async (data: Partial<User>) => {
    if (!user.value) return { success: false, error: '用户未登录' }

    try {
      // TODO: 调用更新API
      // await api.patch(`/users/${user.value.id}`, data)

      user.value = { ...user.value, ...data }
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

    // 方法
    initFromStorage,
    login,
    register,
    logout,
    updateProfile
  }
})
