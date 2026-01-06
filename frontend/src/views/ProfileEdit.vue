<template>
  <div class="bg-[#F8FAFC] min-h-screen flex overflow-hidden">
    <AppSidebar active="settings" />

    <main class="flex-1 overflow-y-auto p-8 relative">
      <div class="fixed top-0 right-0 w-[500px] h-[500px] bg-blue-50 rounded-full filter blur-[80px] -z-10"></div>

      <div class="max-w-3xl mx-auto space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold text-slate-800">编辑资料</h2>
          <AppButton variant="ghost" size="sm" @click="goBack">返回设置</AppButton>
        </div>

        <div class="glass-card p-6 bg-white/90">
          <div class="flex items-center gap-6 pb-6 border-b border-slate-100">
            <img
              :src="avatarPreview"
              class="w-20 h-20 rounded-full border-4 border-white shadow-md object-cover"
              alt="用户头像"
            >
            <div>
              <p class="text-sm text-slate-500">当前头像预览</p>
              <p class="text-xs text-slate-400 mt-1">可粘贴头像 URL 来更新</p>
            </div>
          </div>

          <form class="mt-6 space-y-6" @submit.prevent="handleSubmit">
            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">用户名</label>
              <input
                v-model="form.name"
                type="text"
                class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                placeholder="请输入用户名"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">邮箱</label>
              <input
                v-model="form.email"
                type="email"
                class="w-full bg-slate-100 border border-slate-200 rounded-lg px-4 py-2 text-slate-400 cursor-not-allowed"
                disabled
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">手机号</label>
              <input
                v-model="form.phone"
                type="tel"
                class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                placeholder="请输入手机号"
              >
            </div>

            <div class="grid sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">性别</label>
                <select
                  v-model="form.gender"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                >
                  <option value="unspecified">不透露</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">生日</label>
                <input
                  v-model="form.birthDate"
                  type="date"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                >
              </div>
            </div>

            <div class="grid sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">城市</label>
                <input
                  v-model="form.city"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="例如：上海"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">国家</label>
                <input
                  v-model="form.country"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="例如：中国"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">头像 URL</label>
              <input
                v-model="form.avatarUrl"
                type="text"
                class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                placeholder="https://example.com/avatar.jpg"
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">个人简介</label>
              <textarea
                v-model="form.bio"
                rows="3"
                class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                placeholder="简单介绍一下你自己"
              ></textarea>
            </div>

            <div class="grid sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">偏好语言</label>
                <input
                  v-model="form.preferredLanguage"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="例如：zh-CN"
                >
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">偏好货币</label>
                <input
                  v-model="form.preferredCurrency"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="例如：CNY"
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-600 mb-2">社交账号</label>
              <div class="grid sm:grid-cols-2 gap-4">
                <input
                  v-model="form.socialAccounts.wechat"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="微信号"
                >
                <input
                  v-model="form.socialAccounts.weibo"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="微博"
                >
                <input
                  v-model="form.socialAccounts.x"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="X (Twitter)"
                >
                <input
                  v-model="form.socialAccounts.instagram"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="Instagram"
                >
                <input
                  v-model="form.socialAccounts.tiktok"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="TikTok"
                >
                <input
                  v-model="form.socialAccounts.other"
                  type="text"
                  class="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 text-slate-700 outline-none focus:border-teal-400"
                  placeholder="其他账号"
                >
              </div>
            </div>

            <div class="flex items-center gap-3 pt-2">
              <AppButton type="submit" :disabled="isSaving">
                {{ isSaving ? '保存中...' : '保存修改' }}
              </AppButton>
              <p v-if="feedback" :class="feedback.type === 'success' ? 'text-teal-600' : 'text-red-500'" class="text-sm">
                {{ feedback.message }}
              </p>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import AppSidebar from '@/components/common/AppSidebar.vue'
import AppButton from '@/components/common/AppButton.vue'
import { useAuthStore } from '@/stores/auth'
import type { User } from '@/types/api'

const router = useRouter()
const authStore = useAuthStore()
const { user } = storeToRefs(authStore)

const isSaving = ref(false)
const feedback = ref<{ type: 'success' | 'error'; message: string } | null>(null)

const form = reactive({
  name: '',
  email: '',
  avatarUrl: '',
  phone: '',
  gender: 'unspecified' as User['gender'] | undefined,
  birthDate: '',
  city: '',
  country: '',
  bio: '',
  preferredLanguage: '',
  preferredCurrency: '',
  socialAccounts: {
    wechat: '',
    weibo: '',
    x: '',
    instagram: '',
    tiktok: '',
    other: ''
  }
})

const avatarPreview = computed(() => {
  return form.avatarUrl || user.value?.avatar_url || user.value?.avatar || 'https://i.pravatar.cc/150?img=12'
})

const syncForm = () => {
  form.name = user.value?.name || ''
  form.email = user.value?.email || ''
  form.avatarUrl = user.value?.avatar_url || ''
  form.phone = user.value?.phone || ''
  form.gender = user.value?.gender || 'unspecified'
  form.birthDate = user.value?.birth_date || ''
  form.city = user.value?.city || ''
  form.country = user.value?.country || ''
  form.bio = user.value?.bio || ''
  form.preferredLanguage = user.value?.preferred_language || ''
  form.preferredCurrency = user.value?.preferred_currency || ''
  const socials = user.value?.social_accounts || {}
  form.socialAccounts = {
    wechat: socials.wechat || '',
    weibo: socials.weibo || '',
    x: socials.x || '',
    instagram: socials.instagram || '',
    tiktok: socials.tiktok || '',
    other: socials.other || ''
  }
}

onMounted(async () => {
  await authStore.fetchCurrentUser()
  syncForm()
})

const handleSubmit = async () => {
  feedback.value = null
  if (!form.name.trim()) {
    feedback.value = { type: 'error', message: '用户名不能为空' }
    return
  }

  isSaving.value = true
  const socialAccounts: Record<string, string> = {}
  Object.entries(form.socialAccounts).forEach(([key, value]) => {
    if (value.trim()) {
      socialAccounts[key] = value.trim()
    }
  })
  const result = await authStore.updateProfile({
    name: form.name.trim(),
    avatar_url: form.avatarUrl.trim() || null,
    phone: form.phone.trim() || null,
    gender: form.gender,
    birth_date: form.birthDate || null,
    city: form.city.trim() || null,
    country: form.country.trim() || null,
    bio: form.bio.trim() || null,
    preferred_language: form.preferredLanguage.trim() || null,
    preferred_currency: form.preferredCurrency.trim() || null,
    social_accounts: Object.keys(socialAccounts).length ? socialAccounts : null
  })
  isSaving.value = false

  if (result.success) {
    feedback.value = { type: 'success', message: '用户信息已更新' }
    syncForm()
  } else {
    feedback.value = { type: 'error', message: result.error || '更新失败' }
  }
}

const goBack = () => {
  router.push('/settings')
}
</script>
