<template>
  <div class="glass-card p-8 flex items-center gap-6">
    <div class="relative">
      <img :src="avatarUrl" class="w-24 h-24 rounded-full border-4 border-white shadow-md" alt="用户头像">
      <button class="absolute bottom-0 right-0 w-8 h-8 bg-teal-500 text-white rounded-full flex items-center justify-center hover:bg-teal-600 shadow-sm">
        <i class="fas fa-camera text-sm"></i>
      </button>
    </div>
    <div class="flex-1">
      <h3 class="text-xl font-bold text-slate-800">{{ userName }}</h3>
      <p class="text-slate-500 mb-2">{{ email }}</p>
      <div class="flex gap-2">
        <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-bold rounded-full border border-yellow-200">{{ membership }}</span>
        <span class="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-bold rounded-full">{{ level }}</span>
      </div>
    </div>
    <button class="px-4 py-2 border border-slate-200 rounded-lg text-slate-600 hover:bg-slate-50 font-medium transition-colors">
      编辑资料
    </button>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    userName?: string
    email?: string
    membership?: string
    level?: string
    avatarUrl?: string
  }>(),
  {
    userName: 'Alex Chen',
    email: 'alex.traveler@example.com',
    membership: 'Pro 会员',
    level: 'Lv.5 旅行家',
    avatarUrl: 'https://i.pravatar.cc/150?img=12'
  }
)
</script>
