import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { CopywritingRequest, CopywritingResult } from '@/types/api'

export const useCopywritingStore = defineStore('copywriting', () => {
  // 状态
  const results = ref<CopywritingResult[]>([])
  const isGenerating = ref(false)
  const currentResult = ref<CopywritingResult | null>(null)
  const selectedPlatform = ref<'xiaohongshu' | 'wechat' | 'weibo'>('xiaohongshu')
  const keywords = ref<string>('')
  const emotionLevel = ref(50)
  const uploadedImages = ref<string[]>([])

  // 生成文案
  const generateCopywriting = async (request: CopywritingRequest) => {
    isGenerating.value = true
    try {
      // TODO: 调用AI文案生成API
      // const response = await api.post<CopywritingResult>('/copywriting/generate', request)

      // 模拟生成
      const templates = {
        xiaohongshu: {
          title: '✨【{keyword}】真的绝了！',
          content: `今天来看{keyword}啦！✨

{emotion}的大海配上橙红色的晚霞，这就是最治愈的画面。

生活不止眼前的苟且，还有诗和远方的田野。

#旅行 #风景 #治愈 #{keyword}`
        },
        wechat: {
          title: '今日分享：{keyword}',
          content: `今天来到{keyword}，真的是太美了！

{emotion}的景色让人流连忘返，工作的疲惫一扫而空。

有时候，旅行不需要太多理由，只需要一个出发的心。

生活不止眼前的苟且，还有诗和远方的田野。

📍 位置：{keyword}`
        },
        weibo: {
          title: '今日份美好：{keyword}',
          content: `今天来看{keyword}啦！{emotion}

蔚蓝的大海配上橙红色的晚霞，这就是最治愈的画面。

生活不止眼前的苟且，还有诗和远方的田野。[心]

#旅行 #风景 #治愈 #{keyword} `
        }
      }

      const template = templates[request.platform]
      const emotionWords = {
        0: '忧郁',
        25: '宁静',
        50: '治愈',
        75: '兴奋',
        100: '激情澎湃'
      }

      const emotionText = emotionWords[request.emotion_level as keyof typeof emotionWords] || '美好'

      const content = template.content
        .replace(/{keyword}/g, request.keywords.join('、') || '日落')
        .replace(/{emotion}/g, emotionText)

      const result: CopywritingResult = {
        id: Date.now(),
        content,
        platform: request.platform,
        keywords: request.keywords,
        created_at: new Date().toISOString()
      }

      results.value.unshift(result)
      currentResult.value = result

      return { success: true, data: result }
    } catch (error) {
      console.error('Failed to generate copywriting:', error)
      return { success: false, error: '生成文案失败' }
    } finally {
      isGenerating.value = false
    }
  }

  // 重新生成
  const regenerate = async () => {
    const request: CopywritingRequest = {
      platform: selectedPlatform.value,
      keywords: keywords.value.split(',').map(k => k.trim()).filter(Boolean),
      emotion_level: emotionLevel.value,
      images: uploadedImages.value
    }

    return await generateCopywriting(request)
  }

  // 上传图片
  const uploadImages = async (files: File[]) => {
    try {
      // TODO: 调用图片上传API
      // const response = await api.post<{ urls: string[] }>('/upload', formData)

      // 模拟上传
      const urls = files.map(file => URL.createObjectURL(file))
      uploadedImages.value.push(...urls)

      return { success: true, data: urls }
    } catch (error) {
      console.error('Failed to upload images:', error)
      return { success: false, error: '图片上传失败' }
    }
  }

  // 删除图片
  const removeImage = (index: number) => {
    uploadedImages.value.splice(index, 1)
  }

  // 获取历史生成记录
  const fetchResults = async () => {
    try {
      // TODO: 调用API获取历史记录
      // const response = await api.get<CopywritingResult[]>('/copywriting/results')

      // 模拟数据
      results.value = []
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch results:', error)
      return { success: false, error: '获取历史记录失败' }
    }
  }

  // 删除结果
  const deleteResult = async (id: number) => {
    try {
      // TODO: 调用API删除结果
      // await api.delete(`/copywriting/results/${id}`)

      results.value = results.value.filter(r => r.id !== id)

      if (currentResult.value?.id === id) {
        currentResult.value = null
      }

      return { success: true }
    } catch (error) {
      console.error('Failed to delete result:', error)
      return { success: false, error: '删除失败' }
    }
  }

  return {
    // 状态
    results,
    isGenerating,
    currentResult,
    selectedPlatform,
    keywords,
    emotionLevel,
    uploadedImages,

    // 方法
    generateCopywriting,
    regenerate,
    uploadImages,
    removeImage,
    fetchResults,
    deleteResult
  }
})
