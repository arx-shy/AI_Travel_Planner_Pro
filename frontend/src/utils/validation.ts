/**
 * 表单验证工具函数
 */

// 邮箱验证
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// 密码强度验证
export const validatePassword = (password: string): {
  valid: boolean
  score: number
  feedback: string[]
} => {
  const feedback: string[] = []
  let score = 0

  if (password.length < 8) {
    feedback.push('密码至少需要8个字符')
  } else {
    score += 1
  }

  if (!/[a-z]/.test(password)) {
    feedback.push('密码应包含小写字母')
  } else {
    score += 1
  }

  if (!/[A-Z]/.test(password)) {
    feedback.push('密码应包含大写字母')
  } else {
    score += 1
  }

  if (!/[0-9]/.test(password)) {
    feedback.push('密码应包含数字')
  } else {
    score += 1
  }

  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    feedback.push('密码应包含特殊字符')
  } else {
    score += 1
  }

  return {
    valid: score >= 4,
    score,
    feedback
  }
}

// 手机号验证
export const validatePhone = (phone: string): boolean => {
  const phoneRegex = /^1[3-9]\d{9}$/
  return phoneRegex.test(phone)
}

// 必填字段验证
export const validateRequired = (value: any): boolean => {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  return true
}

// URL验证
export const validateURL = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// 数字范围验证
export const validateNumberRange = (
  value: number,
  min: number,
  max: number
): boolean => {
  return value >= min && value <= max
}

// 长度验证
export const validateLength = (
  value: string,
  min?: number,
  max?: number
): boolean => {
  if (min && value.length < min) return false
  if (max && value.length > max) return false
  return true
}

// 文件类型验证
export const validateFileType = (
  file: File,
  allowedTypes: string[]
): boolean => {
  return allowedTypes.includes(file.type)
}

// 文件大小验证（单位：MB）
export const validateFileSize = (file: File, maxSizeMB: number): boolean => {
  const maxSizeBytes = maxSizeMB * 1024 * 1024
  return file.size <= maxSizeBytes
}

// 身份证号验证
export const validateIdCard = (idCard: string): boolean => {
  const idCardRegex = /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
  return idCardRegex.test(idCard)
}
