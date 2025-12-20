<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-teal-50">
    <div class="max-w-md w-full bg-white/80 backdrop-blur p-8 rounded-2xl shadow-xl">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">创建新账户</h1>
        <p class="text-slate-500">只需 30 秒，开启您的智能旅行</p>
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
            type="text"
            v-model="name"
            class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
            placeholder="姓名"
          >
        </div>

        <div>
          <input
            type="password"
            v-model="password"
            class="w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
            placeholder="设置密码"
          >
        </div>

        <button
          type="button"
          @click="handleRegister"
          class="w-full bg-gradient-to-r from-teal-400 to-blue-500 text-white font-semibold py-3 rounded-lg hover:shadow-lg transition-all"
        >
          立即注册
        </button>
      </form>

      <div class="mt-8 text-center">
        <p class="text-slate-600">
          已有账号?
          <router-link to="/login" class="text-teal-600 font-bold hover:underline">直接登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const name = ref('')
const password = ref('')

const handleRegister = () => {
  // Handle register logic
  router.push('/planner')
}
</script>
