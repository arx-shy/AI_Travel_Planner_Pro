<template>
  <div class="glass-card p-6 flex flex-col h-full bg-white/60 relative overflow-hidden">
    <div class="absolute top-0 right-0 p-4 opacity-10 pointer-events-none">
      <i class="fas fa-quote-right text-9xl text-slate-800"></i>
    </div>

    <h3 class="text-lg font-bold text-slate-700 mb-4">生成结果预览</h3>

    <div class="flex-1 bg-white border border-slate-100 rounded-2xl p-6 shadow-inner overflow-y-auto">
      <div v-if="content" class="space-y-4">
        <div class="flex items-center gap-3 mb-4">
          <img src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full" alt="用户头像">
          <div>
            <div class="font-bold text-sm">{{ userName }}</div>
            <div class="text-xs text-slate-400">刚刚发布于 {{ location }}</div>
          </div>
        </div>

        <div class="text-slate-600 leading-relaxed whitespace-pre-line">
          {{ content }}
        </div>

        <div class="grid grid-cols-2 gap-2 mt-4">
          <div class="h-32 bg-slate-200 rounded-lg animate-pulse"></div>
          <div class="h-32 bg-slate-200 rounded-lg animate-pulse"></div>
        </div>
      </div>

      <div v-else class="text-center text-slate-400 py-16">
        <i class="fas fa-magic text-4xl mb-4"></i>
        <p>点击生成按钮开始创作</p>
      </div>
    </div>

    <div class="flex gap-3 mt-4">
      <button class="flex-1 py-2 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
        <i class="far fa-copy"></i> 复制
      </button>
      <button class="flex-1 py-2 border border-slate-200 rounded-xl text-slate-600 hover:bg-slate-50 transition-colors">
        <i class="fas fa-share-alt"></i> 分享
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    content: string
    userName?: string
    location?: string
  }>(),
  {
    userName: 'Alex Chen',
    location: '冰岛'
  }
)
</script>
