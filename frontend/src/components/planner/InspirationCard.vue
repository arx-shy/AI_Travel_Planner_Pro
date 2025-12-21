<template>
  <div class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
    <AppIcon name="robot" size="xl" class="absolute -right-4 -bottom-4 text-8xl text-white/10" />
    <h4 class="font-bold text-lg mb-2">需要灵感?</h4>
    <p class="text-blue-100 text-sm mb-4">不知道去哪玩？让 AI 根据您的历史喜好推荐。</p>
    <AppButton variant="ghost" size="sm" class="bg-white/20 hover:bg-white/30 text-white">
      试试手气
    </AppButton>
  </div>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
</script>
