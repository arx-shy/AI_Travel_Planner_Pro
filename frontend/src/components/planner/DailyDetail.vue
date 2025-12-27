<template>
  <div class="daily-detail glass-card p-6 mb-4">
    <div class="flex items-center justify-between mb-4">
      <h4 class="text-lg font-bold text-slate-800">
        第{{ day.day_number }}天 - {{ day.title || '自由探索' }}
      </h4>
      <div class="flex gap-2">
        <AppButton
          v-if="editable"
          size="sm"
          variant="ghost"
          icon="edit"
          @click="$emit('edit', day.day_number)"
        >
          编辑
        </AppButton>
      </div>
    </div>

    <ActivityTimeline :activities="day.activities" />

    <!-- 住宿和餐饮信息 -->
    <div v-if="hasExtraInfo" class="info-grid mt-6">
      <div v-if="accommodation" class="info-item">
        <AppIcon name="bed" class="text-teal-500" />
        <span class="label">住宿</span>
        <span class="value">{{ accommodation }}</span>
      </div>
      <div v-if="meals && meals.length" class="info-item">
        <AppIcon name="utensils" class="text-teal-500" />
        <span class="label">餐饮</span>
        <span class="value">{{ meals.join('、') }}</span>
      </div>
    </div>

    <!-- 备注 -->
    <div v-if="day.notes" class="notes mt-4">
      <AppIcon name="info-circle" class="text-blue-500" />
      <span>{{ day.notes }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import ActivityTimeline from './ActivityTimeline.vue'

interface DayPlan {
  day_number: number
  title: string
  activities: any[]
  notes?: string
}

interface Props {
  day: DayPlan
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})

const emit = defineEmits<{
  edit: [number]
}>()

const accommodation = computed(() => {
  const activities = props.day.activities || []
  return activities.find(a => a.type === 'accommodation')?.title || null
})

const meals = computed(() => {
  const activities = props.day.activities || []
  return activities
    .filter(a => a.type === 'meal')
    .map(a => a.title)
})

const hasExtraInfo = computed(() => {
  return Boolean(accommodation.value || (meals.value && meals.value.length > 0))
})
</script>

<style scoped>
.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.info-item .label {
  font-weight: 600;
  color: #64748b;
  margin-right: 0.5rem;
}

.info-item .value {
  color: #334155;
}

.notes {
  padding: 0.75rem;
  background: #fffbeb;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #854d0e;
}
</style>
