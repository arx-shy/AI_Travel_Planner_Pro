<template>
  <i :class="[prefixClass, iconClass, sizeClass]" aria-hidden="true"></i>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    name: string
    prefix?: 'fas' | 'far' | 'fab'
    size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
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
  xl: 'text-xl'
}

const prefixClass = props.prefix
const iconClass = `fa-${props.name}`
const sizeClass = sizeMap[props.size] || sizeMap.md
</script>
