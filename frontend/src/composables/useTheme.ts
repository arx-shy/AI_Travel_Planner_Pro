/**
 * 主题切换组合式函数
 */
import { ref, onMounted, watch } from 'vue'
import { useLocalStorage } from './useLocalStorage'

type Theme = 'light' | 'dark' | 'system'

export function useTheme() {
  // 主题状态
  const theme = useLocalStorage<Theme>('theme', 'system')
  const isDark = ref(false)

  // 初始化主题
  const initTheme = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

    const updateTheme = () => {
      if (theme.value === 'system') {
        isDark.value = mediaQuery.matches
      } else {
        isDark.value = theme.value === 'dark'
      }

      // 更新 DOM 类名
      if (isDark.value) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    // 监听系统主题变化
    mediaQuery.addEventListener('change', updateTheme)

    // 初始更新
    updateTheme()

    // 监听主题变化
    watch(theme, updateTheme, { immediate: true })
  }

  // 设置主题
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme
  }

  // 切换主题
  const toggleTheme = () => {
    const themes: Theme[] = ['light', 'dark', 'system']
    const currentIndex = themes.indexOf(theme.value)
    const nextIndex = (currentIndex + 1) % themes.length
    theme.value = themes[nextIndex]
  }

  onMounted(() => {
    initTheme()
  })

  return {
    theme,
    isDark,
    setTheme,
    toggleTheme
  }
}
