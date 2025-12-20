<template>
  <div class="h-screen flex bg-slate-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-slate-100 flex flex-col">
      <div class="p-6 flex items-center gap-2 text-teal-500">
        <i class="fas fa-paper-plane text-2xl"></i>
        <span class="font-bold text-xl">WanderFlow</span>
      </div>
      <nav class="flex-1 px-4 space-y-2 mt-4">
        <router-link to="/planner" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-map w-6 mr-2"></i> 规划行程
        </router-link>
        <router-link to="/qa" class="block px-4 py-2 text-slate-800 bg-teal-50 rounded-lg">
          <i class="fas fa-comment-dots w-6 mr-2"></i> AI 助手
        </router-link>
        <router-link to="/copywriter" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-pen-nib w-6 mr-2"></i> 文案生成
        </router-link>
        <router-link to="/settings" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-cog w-6 mr-2"></i> 账户设置
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col">
      <header class="h-16 bg-white/80 backdrop-blur border-b border-slate-100 flex items-center px-6">
        <h2 class="text-xl font-bold text-slate-700">WanderBot 智能向导</h2>
      </header>

      <div class="flex-1 overflow-y-auto p-6">
        <div class="max-w-3xl mx-auto">
          <!-- Welcome Message -->
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-gradient-to-br from-teal-400 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl">
              <i class="fas fa-robot"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-800 mb-2">嗨，我是您的旅行助理！</h3>
            <p class="text-slate-500">您可以问我关于目的地天气、签证政策、景点推荐或任何旅行问题。</p>
          </div>

          <!-- Chat Messages -->
          <div class="space-y-4">
            <div v-for="message in messages" :key="message.id" class="flex gap-4">
              <div v-if="message.role === 'assistant'" class="w-10 h-10 bg-gradient-to-br from-teal-400 to-blue-500 rounded-full flex items-center justify-center text-white">
                <i class="fas fa-robot"></i>
              </div>
              <div :class="message.role === 'user' ? 'ml-auto' : ''" class="max-w-lg">
                <div :class="message.role === 'user' ? 'bg-white' : 'bg-teal-50'" class="p-4 rounded-2xl">
                  <p class="text-slate-700">{{ message.content }}</p>
                </div>
              </div>
              <img v-if="message.role === 'user'" src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full">
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-6 bg-white border-t border-slate-100">
        <div class="max-w-3xl mx-auto relative">
          <input
            type="text"
            v-model="inputMessage"
            @keypress.enter="sendMessage"
            class="w-full bg-slate-50 border-2 border-slate-200 rounded-full py-4 pl-6 pr-16 focus:outline-none focus:border-teal-400"
            placeholder="输入您的问题..."
          >
          <button
            @click="sendMessage"
            class="absolute right-2 top-2 w-10 h-10 bg-teal-500 hover:bg-teal-600 text-white rounded-full flex items-center justify-center transition-colors"
          >
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<ChatMessage[]>([
  {
    id: 1,
    role: 'assistant',
    content: '您好！我是WanderBot，您的AI旅行助理。我可以帮您查询天气、推荐景点、制定行程等。有什么可以帮助您的吗？'
  }
])

const inputMessage = ref('')

const sendMessage = () => {
  if (!inputMessage.value.trim()) return

  // Add user message
  messages.value.push({
    id: messages.value.length + 1,
    role: 'user',
    content: inputMessage.value
  })

  // Clear input
  const userMessage = inputMessage.value
  inputMessage.value = ''

  // Simulate AI response
  setTimeout(() => {
    messages.value.push({
      id: messages.value.length + 1,
      role: 'assistant',
      content: `我理解您的问题是："${userMessage}"。我可以为您提供相关的旅行建议和信息。`
    })
  }, 1000)
}
</script>
