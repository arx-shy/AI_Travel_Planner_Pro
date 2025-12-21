<template>
  <header class="h-16 bg-white/80 backdrop-blur border-b border-slate-100 flex justify-between items-center px-8 z-10">
    <h2 class="text-xl font-bold text-slate-700">{{ title }}</h2>
    <div class="flex gap-4">
      <AppButton variant="secondary" size="sm" class="rounded-full w-10 h-10 !p-0">
        <AppIcon name="bell" />
      </AppButton>
      <AppButton variant="primary" size="sm">导出行程</AppButton>
    </div>
  </header>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

withDefaults(
  defineProps<{
    title?: string
  }>(),
  {
    title: '我的新旅程'
  }
)
</script>
