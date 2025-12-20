<template>
  <div>
    <label class="block text-sm font-bold text-slate-500 mb-2">2. 选择平台风格</label>
    <div class="grid grid-cols-3 gap-3">
      <button
        type="button"
        class="border py-3 rounded-xl font-bold transition-colors"
        :class="modelValue === 'xiaohongshu' ? 'border-red-200 bg-red-50 text-red-500 hover:bg-red-100' : 'border-slate-200 bg-white hover:bg-red-50'"
        @click="$emit('update:modelValue', 'xiaohongshu')"
      >
        <i class="fab fa-instagram"></i> 小红书
      </button>
      <button
        type="button"
        class="border py-3 rounded-xl font-bold transition-colors"
        :class="modelValue === 'wechat' ? 'border-green-200 bg-green-50 text-green-600 hover:bg-green-100' : 'border-slate-200 bg-white hover:bg-green-50'"
        @click="$emit('update:modelValue', 'wechat')"
      >
        <i class="fab fa-weixin"></i> 朋友圈
      </button>
      <button
        type="button"
        class="border py-3 rounded-xl font-bold transition-colors"
        :class="modelValue === 'weibo' ? 'border-blue-200 bg-blue-50 text-blue-500 hover:bg-blue-100' : 'border-slate-200 bg-white hover:bg-blue-50'"
        @click="$emit('update:modelValue', 'weibo')"
      >
        <i class="fab fa-twitter"></i> 微博
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: 'xiaohongshu' | 'wechat' | 'weibo'
}>()

defineEmits<{
  'update:modelValue': ['xiaohongshu' | 'wechat' | 'weibo']
}>()
</script>
