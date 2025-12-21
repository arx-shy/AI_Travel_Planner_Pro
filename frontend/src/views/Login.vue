<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-teal-50 to-blue-50">
    <div class="max-w-md w-full bg-white/80 backdrop-blur p-8 rounded-2xl shadow-xl">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">欢迎回来!</h1>
        <p class="text-slate-500">请输入您的账号信息以继续</p>
      </div>

      <form class="space-y-5">
        <div>
          <input
            type="email"
            v-model="email"
            class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
            placeholder="电子邮箱"
          >
        </div>

        <div>
          <input
            type="password"
            v-model="password"
            class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
            placeholder="密码"
          >
        </div>

        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center gap-2 text-slate-600">
            <input type="checkbox" v-model="rememberMe" class="rounded text-teal-500">
            记住我
          </label>
          <a href="#" class="text-teal-600 hover:text-teal-700">忘记密码?</a>
        </div>

        <button
          type="button"
          @click="handleLogin"
          class="w-full bg-gradient-to-r from-teal-400 to-blue-500 text-white font-semibold py-3 rounded-lg hover:shadow-lg transition-all"
        >
          立即登录
        </button>

        <button
          type="button"
          @click="handleGuestLogin"
          class="w-full border border-slate-200 text-slate-600 font-semibold py-3 rounded-lg hover:border-teal-400 hover:text-teal-600 transition-all"
        >
          游客登录（免输入）
        </button>

        <p v-if="errorMessage" class="text-sm text-red-500 text-center">
          {{ errorMessage }}
        </p>
      </form>

      <div class="mt-8 text-center">
        <p class="text-slate-600">
          还没有账号?
          <router-link to="/register" class="text-teal-600 font-bold hover:underline">免费注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''
  const result = await authStore.login({
    email: email.value,
    password: password.value
  })

  if (result.success) {
    router.push('/planner')
  } else if (result.error) {
    errorMessage.value = result.error
  }
}

const handleGuestLogin = async () => {
  errorMessage.value = ''
  const result = await authStore.login({
    email: 'guest@wanderflow.app',
    password: 'guest'
  })

  if (result.success) {
    router.push('/planner')
  } else if (result.error) {
    errorMessage.value = result.error
  }
}
</script>
