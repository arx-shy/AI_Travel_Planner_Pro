<template>
  <div class="glass-card p-6 bg-white/80 md:col-span-2">
    <div class="flex justify-between items-center mb-4">
      <h4 class="font-bold text-slate-700">会员订阅</h4>
      <span v-if="user" class="text-sm text-slate-400">
        会员等级: {{ membershipLabel }}
      </span>
    </div>
    <div :class="`rounded-xl p-6 text-white flex justify-between items-center gap-6 ${planClass}`">
      <div>
        <div class="text-2xl font-bold mb-1">
          WanderFlow <span :class="planTextClass">{{ planLabel }}</span>
        </div>
        <div class="text-slate-400 text-sm">{{ planDescription }}</div>
      </div>
      <AppButton
        variant="secondary"
        size="sm"
        class="bg-white text-slate-900 hover:bg-slate-200"
        @click="handleManageSubscription"
      >
        {{ isPremium ? '管理订阅' : '升级会员' }}
      </AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppButton from '@/components/common/AppButton.vue'

interface User {
  membership_level?: string
}

defineProps<{
  user?: User | null
}>()

const isPremium = computed(() => {
  return true
})

const membershipLevel = computed(() => {
  return 'free'
})

const planLabel = computed(() => {
  const labels: Record<string, string> = {
    'free': 'Free',
    'basic': 'Basic',
    'pro': 'Pro',
    'premium': 'Premium'
  }
  return labels[membershipLevel.value] || 'Free'
})

const membershipLabel = computed(() => {
  const labels: Record<string, string> = {
    'free': '免费会员',
    'basic': '基础会员',
    'pro': 'Pro 会员',
    'premium': '高级会员'
  }
  return labels[membershipLevel.value] || '免费会员'
})

const planClass = computed(() => {
  const classes: Record<string, string> = {
    'free': 'bg-gradient-to-r from-slate-600 to-slate-700',
    'basic': 'bg-gradient-to-r from-blue-600 to-blue-700',
    'pro': 'bg-gradient-to-r from-slate-800 to-slate-900',
    'premium': 'bg-gradient-to-r from-yellow-600 to-yellow-700'
  }
  return classes[membershipLevel.value] || classes['free']
})

const planTextClass = computed(() => {
  const classes: Record<string, string> = {
    'free': 'text-slate-300',
    'basic': 'text-blue-300',
    'pro': 'text-yellow-400',
    'premium': 'text-yellow-300'
  }
  return classes[membershipLevel.value] || classes['free']
})

const planDescription = computed(() => {
  const descriptions: Record<string, string> = {
    'free': '享受基础的行程规划功能，每日有限次数的AI生成。',
    'basic': '享受更多AI生成次数和基础客服支持。',
    'pro': '享受无限 AI 生成、离线地图和专属客服支持。',
    'premium': '享受全部高级功能、优先支持和专属定制服务。'
  }
  return descriptions[membershipLevel.value] || descriptions['free']
})

const handleManageSubscription = () => {
  console.log('Manage subscription')
}
</script>
