<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Navigation -->
    <nav class="bg-white border-b border-slate-200 px-8 py-4">
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2 text-teal-500">
          <i class="fas fa-paper-plane text-2xl"></i>
          <span class="font-bold text-xl">WanderFlow</span>
        </div>
        <div class="flex gap-4">
          <router-link to="/qa" class="text-slate-600 hover:text-teal-500">AI 助手</router-link>
          <router-link to="/copywriter" class="text-slate-600 hover:text-teal-500">文案生成</router-link>
          <router-link to="/settings" class="text-slate-600 hover:text-teal-500">设置</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto p-8">
      <h1 class="text-3xl font-bold text-slate-800 mb-8">我的新旅程</h1>

      <!-- Itinerary Form -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-slate-700 mb-4">旅程设定</h2>

        <form class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-600 mb-2">目的地</label>
            <input
              type="text"
              v-model="destination"
              class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
              placeholder="例如：京都, 日本"
            >
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-slate-600 mb-2">天数</label>
              <input
                type="number"
                v-model="days"
                class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
                placeholder="5"
              >
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-600 mb-2">预算 (¥)</label>
              <input
                type="number"
                v-model="budget"
                class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
                placeholder="5000"
              >
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-600 mb-2">旅行风格</label>
            <div class="flex gap-2">
              <button
                type="button"
                @click="travelStyle = 'leisure'"
                :class="travelStyle === 'leisure' ? 'bg-teal-100 border-teal-500 text-teal-700' : 'bg-white border-slate-200 text-slate-600'"
                class="px-4 py-2 rounded-lg border transition-colors"
              >
                🧘 休闲放松
              </button>
              <button
                type="button"
                @click="travelStyle = 'adventure'"
                :class="travelStyle === 'adventure' ? 'bg-teal-100 border-teal-500 text-teal-700' : 'bg-white border-slate-200 text-slate-600'"
                class="px-4 py-2 rounded-lg border transition-colors"
              >
                📸 特种兵打卡
              </button>
              <button
                type="button"
                @click="travelStyle = 'foodie'"
                :class="travelStyle === 'foodie' ? 'bg-teal-100 border-teal-500 text-teal-700' : 'bg-white border-slate-200 text-slate-600'"
                class="px-4 py-2 rounded-lg border transition-colors"
              >
                🍜 美食探索
              </button>
            </div>
          </div>

          <button
            type="button"
            @click="generateItinerary"
            class="w-full bg-gradient-to-r from-teal-400 to-blue-500 text-white font-semibold py-3 rounded-lg hover:shadow-lg transition-all"
          >
            <i class="fas fa-magic mr-2"></i> AI 生成行程
          </button>
        </form>
      </div>

      <!-- Generated Itinerary -->
      <div v-if="generatedItinerary" class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-xl font-bold text-slate-700 mb-4">{{ generatedItinerary.title }}</h2>
        <div class="space-y-4">
          <p class="text-slate-600">目的地：{{ generatedItinerary.destination }}</p>
          <p class="text-slate-600">天数：{{ generatedItinerary.days }}天</p>
          <p class="text-slate-600">预算：¥{{ generatedItinerary.budget }}</p>
          <p class="text-slate-600">风格：{{ generatedItinerary.travelStyle }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const destination = ref('')
const days = ref(3)
const budget = ref(5000)
const travelStyle = ref('leisure')
const generatedItinerary = ref(null)

const generateItinerary = () => {
  generatedItinerary.value = {
    title: `${destination.value} ${days.value}日游`,
    destination: destination.value,
    days: days.value,
    budget: budget.value,
    travelStyle: travelStyle.value
  }
}
</script>
