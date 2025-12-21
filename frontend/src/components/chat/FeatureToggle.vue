<template>
  <button
    type="button"
    :class="active ? activeClass : inactiveClass"
    class="text-xs px-3 py-1 rounded-full transition-colors"
    @click="$emit('toggle')"
  >
    <AppIcon :name="icon" :prefix="iconPrefix" class="mr-1" />{{ label }}
  </button>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'

interface Props {
  label: string
  icon: string
  iconPrefix?: 'fas' | 'far' | 'fab'
  active: boolean
  activeClass: string
  inactiveClass: string
}

defineProps<Props>()
defineEmits<{
  toggle: []
}>()
</script>
