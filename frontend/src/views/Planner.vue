<template>
  <div class="bg-[#F8FAFC] h-screen flex overflow-hidden">
    <AppSidebar active="planner">
      <template #footer>
        <div class="p-4 border-t border-slate-100">
          <div class="flex items-center gap-3 p-2 hover:bg-slate-50 rounded-lg cursor-pointer transition-colors">
            <img src="https://i.pravatar.cc/100?img=12" class="w-10 h-10 rounded-full" alt="用户头像">
            <div>
              <div class="text-sm font-bold text-slate-700">Alex Chen</div>
              <div class="text-xs text-slate-400">Pro 用户</div>
            </div>
          </div>
        </div>
      </template>
    </AppSidebar>

    <main class="flex-1 flex flex-col relative overflow-hidden">
      <PlannerHeader />

      <div class="flex-1 overflow-y-auto p-8 relative">
        <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-teal-50 rounded-full filter blur-[100px] -z-10 pointer-events-none"></div>

        <div class="grid lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
          <div class="lg:col-span-1 space-y-6">
            <ItineraryForm
              :destination="destination"
              :days="days"
              :budget="budget"
              :travel-style="travelStyle"
              @update:destination="destination = $event"
              @update:days="days = $event"
              @update:budget="budget = $event"
              @update:travelStyle="travelStyle = $event"
              @generate="generateItinerary"
            />

            <InspirationCard class="fade-in-up" />
          </div>

          <div class="lg:col-span-2 flex flex-col gap-6">
            <MapPreview />

            <ItineraryCard v-if="generatedItinerary" :itinerary="generatedItinerary" />
            <EmptyStateCard v-else />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import AppSidebar from '@/components/common/AppSidebar.vue'
import ItineraryForm from '@/components/planner/ItineraryForm.vue'
import ItineraryCard from '@/components/planner/ItineraryCard.vue'
import MapPreview from '@/components/planner/MapPreview.vue'
import PlannerHeader from '@/components/planner/PlannerHeader.vue'
import InspirationCard from '@/components/planner/InspirationCard.vue'
import EmptyStateCard from '@/components/planner/EmptyStateCard.vue'
import { useItineraryStore } from '@/stores/itinerary'

const destination = ref('')
const days = ref(3)
const budget = ref(5000)
const travelStyle = ref('leisure')
const itineraryStore = useItineraryStore()
const { currentItinerary } = storeToRefs(itineraryStore)

const styleLabelMap: Record<string, string> = {
  leisure: '休闲放松',
  adventure: '特种兵打卡',
  foodie: '美食探索'
}

const generatedItinerary = computed(() => {
  if (!currentItinerary.value) return null
  return {
    title: currentItinerary.value.title,
    summary: '行程已生成，点击右上角导出或继续调整参数优化线路。',
    destination: currentItinerary.value.destination,
    days: currentItinerary.value.days,
    budget: currentItinerary.value.budget,
    styleLabel: styleLabelMap[currentItinerary.value.travel_style] || currentItinerary.value.travel_style
  }
})

const generateItinerary = async () => {
  await itineraryStore.createItinerary({
    title: `${destination.value} ${days.value}日游`,
    destination: destination.value,
    days: days.value,
    budget: budget.value,
    travel_style: travelStyle.value as 'leisure' | 'adventure' | 'foodie'
  })
}
</script>
