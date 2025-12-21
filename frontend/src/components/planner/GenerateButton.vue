<template>
  <AppButton block icon="magic" @click="$emit('generate')">
    {{ label }}
  </AppButton>
</template>

<script setup lang="ts">
import AppButton from '@/components/common/AppButton.vue'

withDefaults(
  defineProps<{
    label?: string
  }>(),
  {
    label: 'AI 生成行程'
  }
)

defineEmits<{
  generate: []
}>()
</script>
