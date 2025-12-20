<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <AppSidebar active="copywriter" />

    <main class="flex-1 flex flex-col h-full relative">
      <div class="absolute inset-0 bg-gradient-to-br from-teal-50/50 to-blue-50/50 -z-10"></div>
      <CopywriterHeader />

      <div class="flex-1 overflow-hidden p-6">
        <div class="max-w-6xl mx-auto h-full grid lg:grid-cols-2 gap-6">
          <CopywriterForm
            :platform="platform"
            :keywords="keywords"
            :emotion="emotion"
            @update:platform="platform = $event"
            @update:keywords="keywords = $event"
            @update:emotion="emotion = $event"
            @generate="generateContent"
          />

          <ResultPreview :content="generatedContent" class="fade-in-up" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import CopywriterHeader from '@/components/copywriter/CopywriterHeader.vue'
import CopywriterForm from '@/components/copywriter/CopywriterForm.vue'
import ResultPreview from '@/components/copywriter/ResultPreview.vue'

const platform = ref<'xiaohongshu' | 'wechat' | 'weibo'>('xiaohongshu')
const keywords = ref('')
const emotion = ref(50)
const generatedContent = ref('')

const generateContent = () => {
  generatedContent.value =
    '终于来到了世界的尽头！\n\n当极光在头顶舞动的那一刻，所有的长途跋涉都值了。\n这里不仅有黑沙滩的冷峻，还有钻石沙滩的璀璨。\n\n在这片孤独而浪漫的土地上，感觉时间都静止了。\n如果你也想逃离城市的喧嚣，一定要来一次冰岛！\n\n#冰岛旅行 #极光 #治愈系风景 #旅行日记'
}
</script>
