<template>
  <header class="h-16 border-b border-slate-200/60 flex items-center px-8 bg-white/50 backdrop-blur">
    <h2 class="text-xl font-bold text-slate-700">{{ title }}</h2>
  </header>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string
  }>(),
  {
    title: '朋友圈/小红书 文案生成'
  }
)
</script>
