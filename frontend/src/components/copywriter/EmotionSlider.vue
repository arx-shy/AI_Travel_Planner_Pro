<template>
  <div>
    <label class="block text-sm font-bold text-slate-500 mb-2">4. 情感基调</label>
    <input
      :value="modelValue"
      type="range"
      min="0"
      max="100"
      class="w-full accent-teal-500"
      @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))"
    >
    <div class="flex justify-between text-xs text-slate-400 mt-1">
      <span>文艺忧郁</span>
      <span>幽默搞怪</span>
      <span>激情澎湃</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: number
}>()

defineEmits<{
  'update:modelValue': [number]
}>()
</script>
