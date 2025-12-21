<template>
  <div class="glass-card p-6 bg-white/80">
    <h4 class="font-bold text-slate-700 mb-4 pb-2 border-b border-slate-100">隐私与安全</h4>
    <div class="space-y-2">
      <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center group transition-colors">
        <span class="text-slate-600 flex items-center gap-2">
          <AppIcon name="lock" class="w-5 text-slate-400" /> 修改密码
        </span>
        <AppIcon name="chevron-right" class="text-slate-300 group-hover:text-teal-500" />
      </button>
      <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center group transition-colors">
        <span class="text-slate-600 flex items-center gap-2">
          <AppIcon name="shield-alt" class="w-5 text-slate-400" /> 双重验证 (2FA)
        </span>
        <span class="text-xs bg-green-100 text-green-600 px-2 py-0.5 rounded">已开启</span>
      </button>
      <button class="w-full text-left p-3 hover:bg-slate-50 rounded-lg flex justify-between items-center group transition-colors">
        <span class="text-slate-600 flex items-center gap-2">
          <AppIcon name="history" class="w-5 text-slate-400" /> 登录活动记录
        </span>
        <AppIcon name="chevron-right" class="text-slate-300 group-hover:text-teal-500" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'
</script>
