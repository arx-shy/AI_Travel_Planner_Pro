import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatMessage, ChatSession } from '@/types/api'

export const useQaStore = defineStore('qa', () => {
  // 状态
  const sessions = ref<ChatSession[]>([])
  const currentSession = ref<ChatSession | null>(null)
  const messages = ref<ChatMessage[]>([])
  const isLoading = ref(false)
  const isTyping = ref(false)

  // 创建新会话
  const createSession = async (title?: string) => {
    try {
      // TODO: 调用API创建会话
      // const response = await api.post<ChatSession>('/qa/sessions', { title })

      // 模拟创建
      const newSession: ChatSession = {
        id: `session-${Date.now()}`,
        user_id: 1,
        title: title || '新对话',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      sessions.value.unshift(newSession)
      currentSession.value = newSession
      messages.value = []

      return { success: true, data: newSession }
    } catch (error) {
      console.error('Failed to create session:', error)
      return { success: false, error: '创建对话失败' }
    }
  }

  // 获取所有会话
  const fetchSessions = async () => {
    try {
      // TODO: 调用API获取会话列表
      // const response = await api.get<ChatSession[]>('/qa/sessions')

      // 模拟数据
      sessions.value = []
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch sessions:', error)
      return { success: false, error: '获取对话列表失败' }
    }
  }

  // 切换会话
  const switchSession = async (sessionId: string) => {
    try {
      // TODO: 调用API获取会话消息
      // const response = await api.get<ChatMessage[]>(`/qa/sessions/${sessionId}/messages`)

      // 模拟切换
      const session = sessions.value.find(s => s.id === sessionId)
      if (session) {
        currentSession.value = session
        // TODO: 加载消息历史
        messages.value = []
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to switch session:', error)
      return { success: false, error: '切换对话失败' }
    }
  }

  // 发送消息
  const sendMessage = async (content: string, sessionId?: string) => {
    const targetSessionId = sessionId || currentSession.value?.id

    if (!targetSessionId) {
      // 如果没有当前会话，创建新会话
      await createSession()
    }

    isLoading.value = true
    isTyping.value = true

    try {
      // 添加用户消息
      const userMessage: ChatMessage = {
        id: Date.now(),
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
        session_id: targetSessionId!
      }

      messages.value.push(userMessage)

      // TODO: 调用API发送消息
      // const response = await api.post<ChatMessage>('/qa/chat', {
      //   message: content,
      //   session_id: targetSessionId
      // })

      // 模拟AI响应
      setTimeout(() => {
        const assistantMessage: ChatMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: `我理解您的问题是："${content}"。我可以为您提供相关的旅行建议和信息。作为您的AI旅行助手，我可以帮助您：\n\n1. 查询目的地天气和最佳旅行时间\n2. 推荐热门景点和隐藏宝藏\n3. 制定详细的行程计划\n4. 提供签证、货币、通讯等实用信息\n\n请问您还有什么想了解的吗？`,
          timestamp: new Date().toISOString(),
          session_id: targetSessionId!
        }

        messages.value.push(assistantMessage)
        isTyping.value = false
      }, 1000)

      return { success: true }
    } catch (error) {
      console.error('Failed to send message:', error)
      isTyping.value = false
      return { success: false, error: '发送消息失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 删除会话
  const deleteSession = async (sessionId: string) => {
    try {
      // TODO: 调用API删除会话
      // await api.delete(`/qa/sessions/${sessionId}`)

      sessions.value = sessions.value.filter(s => s.id !== sessionId)

      if (currentSession.value?.id === sessionId) {
        currentSession.value = null
        messages.value = []
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to delete session:', error)
      return { success: false, error: '删除对话失败' }
    }
  }

  // 清空当前对话
  const clearCurrentSession = () => {
    messages.value = []
  }

  return {
    // 状态
    sessions,
    currentSession,
    messages,
    isLoading,
    isTyping,

    // 方法
    createSession,
    fetchSessions,
    switchSession,
    sendMessage,
    deleteSession,
    clearCurrentSession
  }
})
