<template>
  <div>
    <label class="block text-sm font-bold text-slate-500 mb-2">3. 核心关键词</label>
    <input
      :value="modelValue"
      type="text"
      class="input-field px-4 !pl-4"
      :placeholder="placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    >
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
  }>(),
  {
    placeholder: '例如：日落、治愈、大海、特种兵'
  }
)

defineEmits<{
  'update:modelValue': [string]
}>()
</script>
