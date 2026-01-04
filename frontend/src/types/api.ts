// API 响应类型定义
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应类型
export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// API 请求参数类型
export interface ApiRequest {
  [key: string]: any
}

// 用户相关类型
export interface User {
  id: number
  email: string
  name: string
  avatar?: string
  avatar_url?: string
  phone?: string
  gender?: 'male' | 'female' | 'other' | 'unspecified'
  birth_date?: string
  city?: string
  country?: string
  bio?: string
  preferred_language?: string
  preferred_currency?: string
  social_accounts?: Record<string, string>
  membership_level: 'free' | 'pro'
  plan_usage_count?: number
  copywriter_usage_count?: number
  last_quota_reset?: string | null
  created_at: string
  updated_at: string
}

export interface UserQuotaInfo {
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

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
}

// 行程规划相关类型 (V2.0 - 支持丰富的实用信息)
export interface Itinerary {
  id: number
  user_id: number
  title: string
  destination: string
  departure?: string | null
  days: number
  budget?: number | null
  travel_style?: string | null
  created_at: string
  updated_at: string

  // V2.0 新增字段
  summary?: string
  highlights?: string[]
  best_season?: string
  weather?: string
  actual_cost?: number
  preparation?: PreparationInfo
  tips?: TravelTips

  // 详细行程（V2.0）
  days_detail?: DayPlan[]
}

export interface PreparationInfo {
  visa?: string
  currency?: string
  language?: string
  electricity?: string
  packing_list?: string[]
  budget_breakdown?: BudgetBreakdown
}

export interface BudgetBreakdown {
  accommodation?: number
  transportation?: number
  food?: number
  activities?: number
  other?: number
}

export interface TravelTips {
  transport?: string
  accommodation?: string
  food?: string
  culture?: string
  safety?: string
}

export interface DayPlan {
  id: number
  itinerary_id: number
  day_number: number
  title: string
  date?: string | null
  summary?: string
  activities?: Activity[]
  total_cost?: number
}

export interface Activity {
  title: string
  type: 'attraction' | 'meal' | 'transport' | 'accommodation'
  description: string
  time: string
  duration: string
  average_cost: number
  location?: string
  coordinates?: {
    lng: number
    lat: number
  }
  tips?: string[]
}

// 文案生成相关类型
export interface CopywritingRequest {
  platform: 'xiaohongshu' | 'wechat' | 'weibo'
  keywords: string[]
  emotion_level: number
  images?: string[]
}

export interface CopywritingResult {
  id: number
  content: string
  platform: string
  keywords: string[]
  images: string[]
  rating?: number | null
  created_at: string
}

// AI 对话相关类型
export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  session_id: number
  created_at: string
}

export interface ChatRequest {
  message: string
  session_id?: number
}

export interface ChatResponse {
  message: string
  session_id: number
}
