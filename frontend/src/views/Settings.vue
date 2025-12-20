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
        <router-link to="/copywriter" class="block px-4 py-2 text-slate-600 hover:bg-slate-50 rounded-lg">
          <i class="fas fa-pen-nib w-6 mr-2"></i> 文案生成
        </router-link>
        <router-link to="/settings" class="block px-4 py-2 text-slate-800 bg-teal-50 rounded-lg">
          <i class="fas fa-cog w-6 mr-2"></i> 账户设置
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8">
      <h1 class="text-3xl font-bold text-slate-800 mb-8">账户与设置</h1>

      <div class="max-w-5xl mx-auto space-y-8">
        <!-- User Profile -->
        <div class="bg-white rounded-2xl shadow-lg p-8 flex items-center gap-6">
          <div class="relative">
            <img src="https://i.pravatar.cc/150?img=12" class="w-24 h-24 rounded-full border-4 border-white shadow-md">
            <button class="absolute bottom-0 right-0 w-8 h-8 bg-teal-500 text-white rounded-full flex items-center justify-center hover:bg-teal-600">
              <i class="fas fa-camera text-sm"></i>
            </button>
          </div>
          <div class="flex-1">
            <h3 class="text-xl font-bold text-slate-800">Alex Chen</h3>
            <p class="text-slate-500 mb-2">alex.traveler@example.com</p>
            <div class="flex gap-2">
              <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-bold rounded-full">👑 Pro 会员</span>
              <span class="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-bold rounded-full">Lv.5 旅行家</span>
            </div>
          </div>
          <button class="px-4 py-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 font-medium">
            编辑资料
          </button>
        </div>

        <!-- Settings Grid -->
        <div class="grid md:grid-cols-2 gap-6">
          <!-- General Preferences -->
          <div class="bg-white rounded-2xl shadow-lg p-6">
            <h4 class="font-bold text-slate-700 mb-4">通用偏好</h4>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-slate-600 flex items-center gap-2">
                  <i class="fas fa-globe w-5 text-slate-400"></i> 语言
                </span>
                <select class="bg-slate-50 border-none rounded-lg text-sm p-2 text-slate-600">
                  <option>简体中文</option>
                  <option>English</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-600 flex items-center gap-2">
                  <i class="fas fa-coins w-5 text-slate-400"></i> 货币单位
                </span>
                <select class="bg-slate-50 border-none rounded-lg text-sm p-2 text-slate-600">
                  <option>CNY (¥)</option>
                  <option>USD ($)</option>
                </select>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-600 flex items-center gap-2">
                  <i class="fas fa-moon w-5 text-slate-400"></i> 深色模式
                </span>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-teal-500"></div>
                </label>
              </div>
            </div>
          </div>

          <!-- Privacy & Security -->
          <div class="bg-white rounded-2xl shadow-lg p-6">
            <h4 class="font-bold text-slate-700 mb-4">隐私与安全</h4>
            <div class="space-y-2">
              <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center">
                <span class="text-slate-600">
                  <i class="fas fa-lock w-5 text-slate-400 mr-2"></i> 修改密码
                </span>
                <i class="fas fa-chevron-right text-slate-300"></i>
              </button>
              <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center">
                <span class="text-slate-600">
                  <i class="fas fa-shield-alt w-5 text-slate-400 mr-2"></i> 双重验证 (2FA)
                </span>
                <span class="text-xs bg-green-100 text-green-600 px-2 py-0.5 rounded">已开启</span>
              </button>
              <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center">
                <span class="text-slate-600">
                  <i class="fas fa-history w-5 text-slate-400 mr-2"></i> 登录活动记录
                </span>
                <i class="fas fa-chevron-right text-slate-300"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
// Settings page component
</script>
