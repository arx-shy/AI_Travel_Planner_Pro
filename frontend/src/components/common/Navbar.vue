<template>
  <nav class="fixed top-0 z-50 w-full px-6 py-6">
    <div class="glass-card mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
        <div class="flex items-center gap-2 text-teal-600">
          <AppIcon name="paper-plane" size="lg" />
          <span class="text-xl font-bold text-slate-800">WanderFlow</span>
        </div>
      <div class="hidden gap-8 text-slate-600 font-medium md:flex">
        <a href="#" class="hover:text-teal-500 transition-colors">功能</a>
        <a href="#" class="hover:text-teal-500 transition-colors">目的地</a>
        <a href="#" class="hover:text-teal-500 transition-colors">关于我们</a>
      </div>
        <div class="flex gap-3">
          <AppButton to="/login" variant="ghost" size="sm">登录</AppButton>
          <AppButton to="/register" variant="primary" size="sm">开始规划</AppButton>
        </div>
      </div>
    </nav>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'
</script>
