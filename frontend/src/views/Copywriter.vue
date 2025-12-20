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
        <router-link to="/qa" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-comment-dots w-6 mr-2"></i> AI 助手
        </router-link>
        <router-link to="/copywriter" class="block px-4 py-2 text-slate-800 bg-teal-50 rounded-lg">
          <i class="fas fa-pen-nib w-6 mr-2"></i> 文案生成
        </router-link>
        <router-link to="/settings" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-cog w-6 mr-2"></i> 账户设置
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8">
      <h1 class="text-3xl font-bold text-slate-800 mb-8">朋友圈/小红书 文案生成</h1>

      <div class="max-w-5xl mx-auto grid lg:grid-cols-2 gap-8">
        <!-- Input Panel -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-slate-700 mb-4">生成配置</h2>

          <form class="space-y-6">
            <div>
              <label class="block text-sm font-bold text-slate-500 mb-2">1. 上传照片</label>
              <div class="border-2 border-dashed border-slate-300 rounded-2xl h-32 flex flex-col items-center justify-center text-slate-400 hover:border-teal-400 hover:bg-teal-50/50 transition-colors cursor-pointer">
                <i class="fas fa-cloud-upload-alt text-3xl mb-2"></i>
                <span class="text-sm">点击或拖拽上传照片</span>
              </div>
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-500 mb-2">2. 选择平台风格</label>
              <div class="grid grid-cols-3 gap-3">
                <button
                  type="button"
                  @click="platform = 'xiaohongshu'"
                  :class="platform === 'xiaohongshu' ? 'bg-red-100 border-red-500 text-red-700' : 'bg-white border-slate-200'"
                  class="border py-3 rounded-xl font-bold hover:bg-red-50 transition-colors"
                >
                  <i class="fab fa-instagram"></i> 小红书
                </button>
                <button
                  type="button"
                  @click="platform = 'wechat'"
                  :class="platform === 'wechat' ? 'bg-green-100 border-green-500 text-green-700' : 'bg-white border-slate-200'"
                  class="border py-3 rounded-xl font-bold hover:bg-green-50 transition-colors"
                >
                  <i class="fab fa-weixin"></i> 朋友圈
                </button>
                <button
                  type="button"
                  @click="platform = 'weibo'"
                  :class="platform === 'weibo' ? 'bg-blue-100 border-blue-500 text-blue-700' : 'bg-200'"
                 -white border-slate class="border py-3 rounded-xl font-bold hover:bg-blue-50 transition-colors"
                >
                  <i class="fab fa-twitter"></i> 微博
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-500 mb-2">3. 核心关键词</label>
              <input
                type="text"
                v-model="keywords"
                class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
                placeholder="例如：日落、治愈、大海"
              >
            </div>

            <div>
              <label class="block text-sm font-bold text-slate-500 mb-2">4. 情感基调</label>
              <input
                type="range"
                v-model="emotion"
                min="0"
                max="100"
                class="w-full accent-teal-500"
              >
              <div class="flex justify-between text-xs text-slate-400 mt-1">
                <span>文艺忧郁</span>
                <span>幽默搞怪</span>
                <span>激情澎湃</span>
              </div>
            </div>

            <button
              type="button"
              @click="generateContent"
              class="w-full bg-gradient-to-r from-teal-400 to-blue-500 text-white font-semibold py-3 rounded-lg hover:shadow-lg transition-all"
            >
              <i class="fas fa-magic mr-2"></i> 一键生成文案
            </button>
          </form>
        </div>

        <!-- Output Panel -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-slate-700 mb-4">生成结果预览</h2>

          <div v-if="generatedContent" class="space-y-4">
            <div class="flex items-center gap-3 mb-4">
              <img src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full">
              <div>
                <div class="font-bold text-sm">Alex Chen</div>
                <div class="text-xs text-slate-400">刚刚发布于 冰岛</div>
              </div>
            </div>

            <div class="text-slate-600 leading-relaxed whitespace-pre-line">
              {{ generatedContent }}
            </div>
          </div>

          <div v-else class="text-center text-slate-400 py-16">
            <i class="fas fa-magic text-4xl mb-4"></i>
            <p>点击生成按钮开始创作</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const platform = ref('xiaohongshu')
const keywords = ref('')
const emotion = ref(50)
const generatedContent = ref('')

const generateContent = () => {
  generatedContent.value = `今天来看日落啦！✨\n\n蔚蓝的大海配上橙红色的晚霞，这就是最治愈的画面。\n\n生活不止眼前的苟且，还有诗和远方的田野。`
}
</script>
