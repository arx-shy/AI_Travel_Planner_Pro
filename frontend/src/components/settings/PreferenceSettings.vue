<template>
  <div class="glass-card p-6 bg-white/80">
    <h4 class="font-bold text-slate-700 mb-4 pb-2 border-b border-slate-100">通用偏好</h4>
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-slate-600 flex items-center gap-2">
          <i class="fas fa-globe w-5 text-slate-400"></i> 语言
        </span>
        <select
          class="bg-slate-50 border-none rounded-lg text-sm p-2 text-slate-600 outline-none cursor-pointer"
          :value="language"
          @change="$emit('update:language', ($event.target as HTMLSelectElement).value)"
        >
          <option>简体中文</option>
          <option>English</option>
        </select>
      </div>
      <div class="flex items-center justify-between">
        <span class="text-slate-600 flex items-center gap-2">
          <i class="fas fa-coins w-5 text-slate-400"></i> 货币单位
        </span>
        <select
          class="bg-slate-50 border-none rounded-lg text-sm p-2 text-slate-600 outline-none cursor-pointer"
          :value="currency"
          @change="$emit('update:currency', ($event.target as HTMLSelectElement).value)"
        >
          <option>CNY (￥)</option>
          <option>USD ($)</option>
        </select>
      </div>
      <div class="flex items-center justify-between">
        <span class="text-slate-600 flex items-center gap-2">
          <i class="fas fa-moon w-5 text-slate-400"></i> 深色模式
        </span>
        <label class="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            class="sr-only peer"
            :checked="darkMode"
            @change="$emit('update:darkMode', ($event.target as HTMLInputElement).checked)"
          >
          <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-teal-500"></div>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    language?: string
    currency?: string
    darkMode?: boolean
  }>(),
  {
    language: '简体中文',
    currency: 'CNY (￥)',
    darkMode: false
  }
)

defineEmits<{
  'update:language': [string]
  'update:currency': [string]
  'update:darkMode': [boolean]
}>()
</script>
