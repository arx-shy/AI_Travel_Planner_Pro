<template>
  <button
    type="button"
    class="btn-primary w-full justify-center mt-auto py-3 text-lg"
    @click="$emit('generate')"
  >
    <i class="fas fa-magic"></i> {{ label }}
  </button>
</template>

<script setup lang="ts">
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
