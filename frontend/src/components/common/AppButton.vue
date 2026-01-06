<template>
  <component
    :is="componentTag"
    :to="to"
    :type="to ? undefined : type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <AppIcon v-if="icon && !iconRight" :name="icon" :prefix="iconPrefix" :size="iconSize" />
    <slot />
    <AppIcon v-if="iconRight" :name="iconRight" :prefix="iconRightPrefix" :size="iconSize" />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppIcon from '@/components/common/AppIcon.vue'

type Variant = 'primary' | 'secondary' | 'ghost' | 'outline'
type Size = 'sm' | 'md' | 'lg'

const props = withDefaults(
  defineProps<{
    to?: string
    type?: 'button' | 'submit' | 'reset'
    variant?: Variant
    size?: Size
    block?: boolean
    disabled?: boolean
    loading?: boolean
    icon?: string
    iconRight?: string
    iconPrefix?: 'fas' | 'far' | 'fab'
    iconRightPrefix?: 'fas' | 'far' | 'fab'
    iconSize?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  }>(),
  {
    type: 'button',
    variant: 'primary',
    size: 'md',
    block: false,
    disabled: false,
    loading: false,
    iconPrefix: 'fas',
    iconRightPrefix: 'fas',
    iconSize: 'md'
  }
)

const emit = defineEmits<{
  click: [MouseEvent]
}>()

const componentTag = computed(() => (props.to ? RouterLink : 'button'))

const sizeClasses: Record<Size, string> = {
  sm: 'text-sm px-4 py-2',
  md: 'text-sm px-6 py-3',
  lg: 'text-lg px-8 py-4'
}

const variantClasses: Record<Variant, string> = {
  primary: 'btn-primary',
  secondary:
    'rounded-lg border border-slate-200 text-slate-600 hover:border-teal-400 hover:text-teal-600',
  ghost: 'rounded-lg text-slate-600 hover:text-teal-600',
  outline:
    'rounded-lg border-2 border-teal-500 text-teal-600 hover:bg-teal-50 hover:border-teal-600'
}

const buttonClasses = computed(() => [
  'inline-flex items-center justify-center gap-2 font-semibold transition-all',
  variantClasses[props.variant],
  sizeClasses[props.size],
  props.block ? 'w-full' : '',
  props.loading ? 'opacity-70 cursor-not-allowed' : ''
])

const handleClick = (event: MouseEvent) => {
  if (props.loading || props.disabled) return
  emit('click', event)
}
</script>
