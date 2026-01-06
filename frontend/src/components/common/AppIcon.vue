<template>
  <i :class="[prefixClass, iconClass, sizeClass]" aria-hidden="true"></i>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    name: string
    prefix?: 'fas' | 'far' | 'fab'
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2x' | '3x' | '4x' | '5x'
  }>(),
  {
    prefix: 'fas',
    size: 'md'
  }
)

const sizeMap: Record<string, string> = {
  xs: 'text-xs',
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
  xl: 'text-xl',
  '2x': 'text-2xl',
  '3x': 'text-3xl',
  '4x': 'text-4xl',
  '5x': 'text-5xl'
}

const prefixClass = props.prefix
const iconClass = `fa-${props.name}`
const sizeClass = sizeMap[props.size] || sizeMap.md
</script>
