<template>
  <aside class="w-64 bg-white border-r border-slate-100 flex flex-col z-20 shadow-sm flex-shrink-0">
    <div class="p-6 flex items-center gap-2 text-teal-500">
      <i class="fas fa-paper-plane text-2xl"></i>
      <span class="font-bold text-xl text-slate-800">WanderFlow</span>
    </div>

    <nav class="flex-1 mt-4">
      <router-link
        v-for="item in items"
        :key="item.key"
        :to="item.to"
        :class="navClass(item.key)"
      >
        <i :class="item.icon" class="w-6"></i> {{ item.label }}
      </router-link>
    </nav>

    <slot name="afterNav" />
    <slot name="footer" />
  </aside>
</template>

<script setup lang="ts">
type ActiveKey = 'planner' | 'qa' | 'copywriter' | 'settings'

interface SidebarItem {
  key: ActiveKey
  label: string
  to: string
  icon: string
}

const props = withDefaults(
  defineProps<{
    active: ActiveKey
    items?: SidebarItem[]
  }>(),
  {
    items: () => [
      { key: 'planner', label: '规划行程', to: '/planner', icon: 'fas fa-map' },
      { key: 'qa', label: 'AI 助手', to: '/qa', icon: 'fas fa-comment-dots' },
      { key: 'copywriter', label: '文案生成', to: '/copywriter', icon: 'fas fa-pen-nib' },
      { key: 'settings', label: '账户设置', to: '/settings', icon: 'fas fa-cog' }
    ]
  }
)

const navClass = (key: ActiveKey) => (props.active === key ? 'nav-item active' : 'nav-item')
</script>
