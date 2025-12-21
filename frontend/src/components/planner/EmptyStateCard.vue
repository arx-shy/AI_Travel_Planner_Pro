<template>
  <div class="glass-card flex-1 p-8 flex flex-col items-center justify-center text-center">
    <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
      <AppIcon :name="icon" size="xl" class="text-slate-300" />
    </div>
    <h3 class="text-lg font-bold text-slate-700">{{ title }}</h3>
    <p class="text-slate-400 max-w-xs mt-2">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'

withDefaults(
  defineProps<{
    title?: string
    description?: string
    icon?: string
  }>(),
  {
    title: '等待生成行程...',
    description: '填写左侧信息，AI 将为您定制专属路线，包括景点、交通和美食推荐。',
    icon: 'clipboard-list'
  }
)
</script>
