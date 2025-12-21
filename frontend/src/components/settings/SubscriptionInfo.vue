<template>
  <div class="glass-card p-6 bg-white/80 md:col-span-2">
    <div class="flex justify-between items-center mb-4">
      <h4 class="font-bold text-slate-700">会员订阅</h4>
      <span class="text-sm text-slate-400">下次扣费日: {{ nextBillingDate }}</span>
    </div>
    <div class="bg-gradient-to-r from-slate-800 to-slate-900 rounded-xl p-6 text-white flex justify-between items-center gap-6">
      <div>
        <div class="text-2xl font-bold mb-1">WanderFlow <span class="text-yellow-400">Pro</span></div>
        <div class="text-slate-400 text-sm">享受无限 AI 生成、离线地图和专属客服支持。</div>
      </div>
      <AppButton variant="secondary" size="sm" class="bg-white text-slate-900 hover:bg-slate-200">
        管理订阅
      </AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'

withDefaults(
  defineProps<{
    nextBillingDate?: string
  }>(),
  {
    nextBillingDate: '2023-12-01'
  }
)
</script>
