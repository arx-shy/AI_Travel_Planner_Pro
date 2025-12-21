<template>
  <div>
    <label class="block text-sm font-bold text-slate-500 mb-2">1. 上传照片 (AI 将识别内容)</label>
    <div class="border-2 border-dashed border-slate-300 rounded-2xl h-32 flex flex-col items-center justify-center text-slate-400 hover:border-teal-400 hover:bg-teal-50/50 transition-colors cursor-pointer group">
      <AppIcon name="cloud-upload-alt" size="xl" class="mb-2 group-hover:scale-110 transition-transform" />
      <span class="text-sm">点击或拖拽上传照片</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'
</script>
