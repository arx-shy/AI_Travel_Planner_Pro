/**
 * 日期格式化工具函数
 */

/**
 * 格式化日期为 YYYY-MM-DD
 */
export const formatDate = (date: Date | string | number): string => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

/**
 * 格式化日期为 YYYY年MM月DD日
 */
export const formatDateCN = (date: Date | string | number): string => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = d.getMonth() + 1
  const day = d.getDate()
  return `${year}年${month}月${day}日`
}

/**
 * 格式化日期为相对时间（如：2小时前）
 */
export const formatRelativeTime = (date: Date | string | number): string => {
  const now = new Date()
  const target = new Date(date)
  const diff = now.getTime() - target.getTime()

  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  const months = Math.floor(days / 30)
  const years = Math.floor(days / 365)

  if (seconds < 60) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`
  if (months < 12) return `${months}个月前`
  return `${years}年前`
}

/**
 * 获取日期区间
 */
export const getDateRange = (startDate: Date | string, endDate: Date | string) => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const dates: string[] = []

  while (start <= end) {
    dates.push(formatDate(start))
    start.setDate(start.getDate() + 1)
  }

  return dates
}

/**
 * 计算两个日期间的天数
 */
export const getDaysBetween = (startDate: Date | string, endDate: Date | string): number => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diff = end.getTime() - start.getTime()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

/**
 * 获取今天是星期几
 */
export const getWeekday = (date: Date | string | number): string => {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const d = new Date(date)
  return weekdays[d.getDay()]
}

/**
 * 获取今天是星期几（英文）
 */
export const getWeekdayEN = (date: Date | string | number): string => {
  const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  const d = new Date(date)
  return weekdays[d.getDay()]
}

/**
 * 判断是否为今天
 */
export const isToday = (date: Date | string | number): boolean => {
  const today = new Date()
  const target = new Date(date)
  return (
    today.getFullYear() === target.getFullYear() &&
    today.getMonth() === target.getMonth() &&
    today.getDate() === target.getDate()
  )
}

/**
 * 判断是否为昨天
 */
export const isYesterday = (date: Date | string | number): boolean => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const target = new Date(date)
  return (
    yesterday.getFullYear() === target.getFullYear() &&
    yesterday.getMonth() === target.getMonth() &&
    yesterday.getDate() === target.getDate()
  )
}
