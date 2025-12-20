/**
 * 本地存储组合式函数
 */
import { ref, watch, onMounted } from 'vue'
import { storage } from '@/utils/common'

export function useLocalStorage<T>(
  key: string,
  defaultValue: T
) {
  const storedValue = storage.get(key, defaultValue)
  const value = ref<T>(storedValue as T)

  watch(value, (newValue) => {
    storage.set(key, newValue)
  }, { deep: true })

  onMounted(() => {
    const stored = storage.get(key, defaultValue)
    value.value = stored as T
  })

  return value
}

/**
 * 会话存储组合式函数
 */
export function useSessionStorage<T>(
  key: string,
  defaultValue: T
) {
  const storedValue = window.sessionStorage.getItem(key)
  const value = ref<T>(storedValue ? JSON.parse(storedValue) : defaultValue)

  watch(value, (newValue) => {
    window.sessionStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })

  onMounted(() => {
    const stored = window.sessionStorage.getItem(key)
    value.value = stored ? JSON.parse(stored) : defaultValue
  })

  return value
}
