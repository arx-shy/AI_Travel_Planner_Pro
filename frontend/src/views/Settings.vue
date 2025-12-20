<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <AppSidebar active="settings" />

    <main class="flex-1 overflow-y-auto p-8 relative">
      <div class="fixed top-0 right-0 w-[500px] h-[500px] bg-blue-50 rounded-full filter blur-[80px] -z-10"></div>

      <div class="max-w-5xl mx-auto space-y-8">
        <h2 class="text-2xl font-bold text-slate-800">账户与设置</h2>

        <UserProfile />

        <div class="grid md:grid-cols-2 gap-6">
          <PreferenceSettings
            :language="language"
            :currency="currency"
            :dark-mode="darkMode"
            @update:language="language = $event"
            @update:currency="currency = $event"
            @update:darkMode="darkMode = $event"
          />
          <SecuritySettings />
          <SubscriptionInfo />
        </div>

        <div class="text-center pt-8">
          <button class="text-red-500 text-sm font-medium hover:underline">退出登录</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import UserProfile from '@/components/settings/UserProfile.vue'
import PreferenceSettings from '@/components/settings/PreferenceSettings.vue'
import SecuritySettings from '@/components/settings/SecuritySettings.vue'
import SubscriptionInfo from '@/components/settings/SubscriptionInfo.vue'

const language = ref('简体中文')
const currency = ref('CNY (￥)')
const darkMode = ref(false)
</script>
