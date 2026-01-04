<template>
  <div class="glass-card p-8 flex items-center gap-6">
    <div class="relative">
      <img :src="avatarUrl" class="w-24 h-24 rounded-full border-4 border-white shadow-md" alt="用户头像">
      <button class="absolute bottom-0 right-0 w-8 h-8 bg-teal-500 text-white rounded-full flex items-center justify-center hover:bg-teal-600 shadow-sm">
        <AppIcon name="camera" size="sm" />
      </button>
    </div>
    <div class="flex-1">
      <h3 class="text-xl font-bold text-slate-800">{{ userName }}</h3>
      <p class="text-slate-500 mb-2">{{ email }}</p>
      <div class="flex gap-2">
        <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-bold rounded-full border border-yellow-200">{{ membership }}</span>
        <span class="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-bold rounded-full">{{ level }}</span>
      </div>
      <div class="mt-3 text-xs text-slate-500 space-y-1">
        <p v-if="phone">手机号：{{ phone }}</p>
        <p v-if="genderLabel">性别：{{ genderLabel }}</p>
        <p v-if="birthDate">生日：{{ birthDate }}</p>
        <p v-if="location">城市/国家：{{ location }}</p>
        <p v-if="preferredLanguage || preferredCurrency">
          偏好：{{ preferredLanguage || '未设置' }} / {{ preferredCurrency || '未设置' }}
        </p>
        <p v-if="bio">简介：{{ bio }}</p>
      </div>
    </div>
    <AppButton variant="secondary" size="sm" @click="handleEdit">编辑资料</AppButton>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import AppIcon from '@/components/common/AppIcon.vue'

const emit = defineEmits<{
  edit: []
}>()

const handleEdit = () => {
  emit('edit')
}

const props = withDefaults(
  defineProps<{
    userName?: string
    email?: string
    membership?: string
    level?: string
    avatarUrl?: string
    phone?: string
    gender?: string
    birthDate?: string
    city?: string
    country?: string
    bio?: string
    preferredLanguage?: string
    preferredCurrency?: string
  }>(),
  {
    userName: 'Alex Chen',
    email: 'alex.traveler@example.com',
    membership: 'Pro 会员',
    level: 'Lv.5 旅行家',
    avatarUrl: 'https://i.pravatar.cc/150?img=12'
  }
)

const genderLabel = computed(() => {
  if (props.gender === 'male') return '男'
  if (props.gender === 'female') return '女'
  if (props.gender === 'other') return '其他'
  if (props.gender === 'unspecified') return '不透露'
  return ''
})

const location = computed(() => {
  if (props.city && props.country) return `${props.city} / ${props.country}`
  return props.city || props.country || ''
})
</script>
