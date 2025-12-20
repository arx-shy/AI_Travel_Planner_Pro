/**
 * API 请求组合式函数
 */
import { ref } from 'vue'
import type { ApiResponse } from '@/types/api'

interface UseApiOptions {
  immediate?: boolean
  onSuccess?: (data: any) => void
  onError?: (error: any) => void
}

export const useApi = <T = any>(
  apiFunction: (...args: any[]) => Promise<ApiResponse<T>>,
  options: UseApiOptions = {}
) => {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { immediate = false, onSuccess, onError } = options

  const execute = async (...args: any[]) => {
    loading.value = true
    error.value = null

    try {
      const response = await apiFunction(...args)
      data.value = response.data

      if (onSuccess) {
        onSuccess(response.data)
      }

      return response
    } catch (err: any) {
      error.value = err.message || '请求失败'
      if (onError) {
        onError(err)
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  if (immediate) {
    execute()
  }

  return {
    data,
    loading,
    error,
    execute
  }
}

/**
 * GET 请求组合式函数
 */
export const useApiGet = <T = any>(
  url: string,
  params?: any,
  options: UseApiOptions = {}
) => {
  const { onSuccess, onError } = options

  const apiFunction = async () => {
    // TODO: 实现实际的API调用
    // return await api.get<T>(url, { params })
    return { data: null } as ApiResponse<T>
  }

  return useApi(apiFunction, options)
}

/**
 * POST 请求组合式函数
 */
export const useApiPost = <T = any>(
  url: string,
  body?: any,
  options: UseApiOptions = {}
) => {
  const { onSuccess, onError } = options

  const apiFunction = async () => {
    // TODO: 实现实际的API调用
    // return await api.post<T>(url, body)
    return { data: null } as ApiResponse<T>
  }

  return useApi(apiFunction, options)
}

/**
 * PUT 请求组合式函数
 */
export const useApiPut = <T = any>(
  url: string,
  body?: any,
  options: UseApiOptions = {}
) => {
  const { onSuccess, onError } = options

  const apiFunction = async () => {
    // TODO: 实现实际的API调用
    // return await api.put<T>(url, body)
    return { data: null } as ApiResponse<T>
  }

  return useApi(apiFunction, options)
}

/**
 * DELETE 请求组合式函数
 */
export const useApiDelete = <T = any>(
  url: string,
  options: UseApiOptions = {}
) => {
  const { onSuccess, onError } = options

  const apiFunction = async () => {
    // TODO: 实现实际的API调用
    // return await api.delete<T>(url)
    return { data: null } as ApiResponse<T>
  }

  return useApi(apiFunction, options)
}
