<template>
  <AppButton block icon="magic" size="lg" @click="$emit('generate')">
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
    label: '一键生成文案'
  }
)

defineEmits<{
  generate: []
}>()
</script>
