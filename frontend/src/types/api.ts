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
  membership_level: 'free' | 'pro'
  created_at: string
  updated_at: string
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
  budget: number | null
  travel_style: 'leisure' | 'adventure' | 'foodie'
  status: 'draft' | 'active' | 'completed' | 'archived'
  ai_generated?: boolean

  // V2 新增字段
  summary?: string
  highlights?: string[]
  best_season?: string
  weather?: string
  actual_cost?: number
  cost_breakdown?: CostBreakdown
  preparation?: PreparationInfo
  tips?: TravelTips
  cover_image?: string

  days_detail?: DayPlan[]
  created_at: string
  updated_at: string
}

export interface ItineraryCreateRequest {
  title: string
  destination: string
  departure?: string | null
  days: number
  budget?: number | null
  travel_style: 'leisure' | 'adventure' | 'foodie'
  use_strict_json?: boolean
}

// 费用明细
export interface CostBreakdown {
  transportation: number
  accommodation: number
  food: number
  tickets: number
  shopping: number
  other: number
}

// 行前准备
export interface PreparationInfo {
  documents: string[]
  essentials: string[]
  suggestions: string[]
  booking_reminders: string[]
}

// 实用提示
export interface TravelTips {
  transportation?: string
  accommodation?: string
  food?: string
  shopping?: string
  safety?: string
  other?: string[]
}

// 每日行程 (V2.0)
export interface DayPlan {
  day_number: number
  title: string
  date?: string
  summary?: string
  activities: Activity[]
  notes?: string
  total_cost?: number
  accommodation?: AccommodationInfo
}

// 活动信息 (V2.0 - 用户友好设计)
export interface Activity {
  // 基本信息
  title: string
  type: 'attraction' | 'meal' | 'transport' | 'accommodation' | 'shopping' | 'entertainment'
  time: string
  duration: string

  // 景点/活动信息
  description: string
  highlights?: string[]
  address?: string
  ticket_price?: number
  need_booking?: boolean
  booking_info?: string

  // 餐饮信息
  cuisine?: string
  average_cost: number
  recommended_dishes?: string[]
  wait_time?: string
  opening_hours?: string

  // 贴士信息
  best_time?: string
  tips?: string[]
  dress_code?: string

  // 交通信息
  transportation?: TransportationInfo
  parking_info?: string

  // 技术数据（用于地图）
  coordinates?: {
    lng: number
    lat: number
  }
}

// 交通信息
export interface TransportationInfo {
  method: string
  from_location?: string
  to_location?: string
  duration: string
  cost: number
  tips?: string
}

// 住宿信息
export interface AccommodationInfo {
  name: string
  address: string
  type: string
  facilities?: string[]
  rating?: number
  booking_status?: string
}

// QA 聊天相关类型
export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  session_id: number
  message_type?: 'text' | 'voice'
  created_at?: string
  timestamp?: string
  metadata?: Record<string, any>
}

export interface ChatSession {
  id: number
  user_id: number
  title: string
  features?: {
    knowledge_base?: boolean
    weather?: boolean
    voice?: boolean
  }
  created_at: string
  updated_at: string
}

export interface QaRequest {
  question: string
  session_id?: string
  context?: Record<string, any>
}

// 文案生成相关类型
export interface CopywritingRequest {
  platform: 'xiaohongshu' | 'wechat' | 'weibo'
  keywords: string[]
  emotion_level: number
  images?: string[]
  custom_style?: string
}

export interface CopywritingResult {
  id: number
  content: string
  platform: string
  keywords: string[]
  created_at: string
  rating?: number | null
}

// 认证相关类型
export interface AuthToken {
  access_token: string
  token_type: string
  expires_in: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface LoginResponse extends AuthResponse {}
export interface RegisterResponse extends AuthResponse {}
