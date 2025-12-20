import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Itinerary, ItineraryCreateRequest, DayPlan } from '@/types/api'

export const useItineraryStore = defineStore('itinerary', () => {
  // 状态
  const itineraries = ref<Itinerary[]>([])
  const currentItinerary = ref<Itinerary | null>(null)
  const isLoading = ref(false)
  const generatedPlans = ref<Record<number, DayPlan[]>>({})

  // 获取所有行程
  const fetchItineraries = async () => {
    isLoading.value = true
    try {
      // TODO: 调用API获取行程列表
      // const response = await api.get<PaginatedResponse<Itinerary>>('/itineraries')
      // itineraries.value = response.data.items

      // 模拟数据
      itineraries.value = []
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch itineraries:', error)
      return { success: false, error: '获取行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 创建行程
  const createItinerary = async (data: ItineraryCreateRequest) => {
    isLoading.value = true
    try {
      // TODO: 调用API创建行程
      // const response = await api.post<Itinerary>('/itineraries', data)

      // 模拟创建
      const newItinerary: Itinerary = {
        id: Date.now(),
        user_id: 1,
        title: data.title,
        destination: data.destination,
        days: data.days,
        budget: data.budget,
        travel_style: data.travel_style,
        status: 'draft',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }

      itineraries.value.unshift(newItinerary)
      currentItinerary.value = newItinerary

      return { success: true, data: newItinerary }
    } catch (error) {
      console.error('Failed to create itinerary:', error)
      return { success: false, error: '创建行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 更新行程
  const updateItinerary = async (id: number, data: Partial<ItineraryCreateRequest>) => {
    try {
      // TODO: 调用API更新行程
      // const response = await api.patch<Itinerary>(`/itineraries/${id}`, data)

      // 模拟更新
      const index = itineraries.value.findIndex(item => item.id === id)
      if (index !== -1) {
        itineraries.value[index] = {
          ...itineraries.value[index],
          ...data,
          updated_at: new Date().toISOString()
        }
      }

      if (currentItinerary.value?.id === id) {
        currentItinerary.value = {
          ...currentItinerary.value,
          ...data,
          updated_at: new Date().toISOString()
        }
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to update itinerary:', error)
      return { success: false, error: '更新行程失败' }
    }
  }

  // 删除行程
  const deleteItinerary = async (id: number) => {
    try {
      // TODO: 调用API删除行程
      // await api.delete(`/itineraries/${id}`)

      itineraries.value = itineraries.value.filter(item => item.id !== id)

      if (currentItinerary.value?.id === id) {
        currentItinerary.value = null
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to delete itinerary:', error)
      return { success: false, error: '删除行程失败' }
    }
  }

  // AI 生成行程
  const generateItineraryPlan = async (itineraryId: number, preferences: any) => {
    isLoading.value = true
    try {
      // TODO: 调用AI生成API
      // const response = await api.post<DayPlan[]>(`/itineraries/${itineraryId}/generate`, preferences)

      // 模拟生成
      const mockPlans: DayPlan[] = Array.from({ length: preferences.days || 3 }, (_, i) => ({
        day: i + 1,
        activities: [
          {
            time: '09:00',
            title: '早餐',
            description: '当地特色早餐',
            location: '酒店附近',
            duration: '1小时'
          },
          {
            time: '10:00',
            title: '景点游览',
            description: '参观著名景点',
            location: '市中心',
            duration: '3小时'
          }
        ],
        meals: ['早餐', '午餐', '晚餐']
      }))

      generatedPlans.value[itineraryId] = mockPlans

      return { success: true, data: mockPlans }
    } catch (error) {
      console.error('Failed to generate itinerary:', error)
      return { success: false, error: 'AI生成行程失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取生成的行程计划
  const getGeneratedPlans = (itineraryId: number) => {
    return generatedPlans.value[itineraryId] || []
  }

  return {
    // 状态
    itineraries,
    currentItinerary,
    isLoading,
    generatedPlans,

    // 方法
    fetchItineraries,
    createItinerary,
    updateItinerary,
    deleteItinerary,
    generateItineraryPlan,
    getGeneratedPlans
  }
})
