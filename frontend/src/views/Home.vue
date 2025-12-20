<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-blue-50">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 bg-white/80 backdrop-blur border-b border-slate-100">
      <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-2 text-teal-600">
          <i class="fas fa-paper-plane text-2xl"></i>
          <span class="font-bold text-xl">WanderFlow</span>
        </div>
        <div class="hidden md:flex gap-8 text-slate-600 font-medium">
          <a href="#" class="hover:text-teal-500 transition-colors">功能</a>
          <a href="#" class="hover:text-teal-500 transition-colors">目的地</a>
          <a href="#" class="hover:text-teal-500 transition-colors">关于我们</a>
        </div>
        <div class="flex gap-3">
          <router-link to="/login" class="px-5 py-2 text-slate-600 font-medium hover:text-teal-600">
            登录
          </router-link>
          <router-link to="/register" class="btn-primary py-2 px-6 text-sm">
            开始规划
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-20">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <div class="inline-block px-4 py-1 mb-4 rounded-full bg-teal-50 border border-teal-100 text-teal-600 text-sm font-semibold">
              ✨ AI 驱动的下一代旅行助手
            </div>
            <h1 class="text-5xl md:text-7xl font-bold text-slate-800 leading-tight mb-6">
              让旅行 <br>
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500">简单而纯粹</span>
            </h1>
            <p class="text-lg text-slate-500 mb-8 leading-relaxed">
              告别繁琐的攻略查询。输入您的预算和偏好，WanderFlow 在几秒钟内为您生成包含景点、交通、美食的完美行程。
            </p>
            <div class="flex gap-4">
              <router-link to="/planner" class="btn-primary text-lg px-8 py-4">
                立即创建行程 <i class="fas fa-magic ml-2"></i>
              </router-link>
              <button class="px-8 py-4 rounded-full border-2 border-slate-200 text-slate-600 font-bold hover:border-teal-500 hover:text-teal-500 transition-all">
                <i class="fas fa-play-circle text-xl mr-2"></i> 观看演示
              </button>
            </div>
          </div>
          <div>
            <img
              src="https://images.unsplash.com/photo-1500835556837-99ac94a94552"
              alt="Travel"
              class="rounded-2xl shadow-2xl w-full object-cover h-[500px]"
            >
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Home page component
</script>
