<template>
  <div class="daily-detail glass-card p-6 mb-4">
    <!-- 天数标题 -->
    <div class="day-header">
      <div class="day-badge">第{{ day.day_number }}天</div>
      <div class="day-info">
        <h4 class="day-title">{{ day.title || '自由探索' }}</h4>
        <!-- 天数统计 -->
        <div class="day-stats">
          <span v-if="day.activities && day.activities.length" class="stat">
            {{ day.activities.length }}个活动
          </span>
          <span v-if="day.total_cost" class="stat cost">
            花费¥{{ day.total_cost }}
          </span>
        </div>
      </div>
      <!-- 操作按钮 -->
      <div class="day-actions">
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

    <!-- 活动时间线 -->
    <div class="activities-container">
      <EditableActivityCard
        v-for="(activity, index) in day.activities"
        :key="index"
        :activity="activity"
        :editable="editable"
        @update="handleActivityUpdate($event, index)"
      />
    </div>

    <!-- 住宿信息（如果有） -->
    <div v-if="day.accommodation" class="accommodation-box">
      <AppIcon name="bed" class="text-purple-500" />
      <div class="accommodation-info">
        <div class="hotel-name">{{ day.accommodation.name }}</div>
        <div class="hotel-address">{{ day.accommodation.address }}</div>
        <div v-if="day.accommodation.rating" class="hotel-rating">
          评分：{{ day.accommodation.rating }}/5
        </div>
        <div v-if="day.accommodation.booking_status" class="booking-status">
          {{ day.accommodation.booking_status }}
        </div>
      </div>
    </div>

    <!-- 备注 -->
    <div v-if="day.notes" class="notes-box">
      <AppIcon name="info-circle" class="text-yellow-500" />
      <span>{{ day.notes }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'
import EditableActivityCard from './EditableActivityCard.vue'
import type { DayPlan } from '@/types/api'
import type { Activity } from '@/types/api'

interface Props {
  day: DayPlan
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})

const emit = defineEmits<{
  edit: [number]
  updateDay: [dayNumber: number, activities: Activity[]]
}>()

const handleActivityUpdate = (updatedActivity: Activity, index: number) => {
  const updatedActivities = [...props.day.activities]
  updatedActivities[index] = updatedActivity
  emit('updateDay', props.day.day_number, updatedActivities)
}
</script>

<style scoped>
.day-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(226,232,240,0.8);
  margin-bottom: 1rem;
}

.day-badge {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  color: white;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 1rem;
}

.day-info {
  flex: 1;
  min-width: 0;
}

.day-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.day-stats {
  display: flex;
  gap: 0.75rem;
}

.day-stats .stat {
  font-size: 0.8125rem;
  color: #64748b;
}

.day-stats .stat.cost {
  color: #16a34a;
  font-weight: 600;
}

.day-actions {
  flex-shrink: 0;
}

.activities-container {
  display: flex;
  flex-direction: column;
}

/* 住宿信息 */
.accommodation-box {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
  border: 1px solid rgba(168, 85, 247, 0.2);
  border-radius: 0.75rem;
  margin-top: 1rem;
}

.accommodation-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 0.5rem;
  font-size: 1.25rem;
}

.accommodation-info {
  flex: 1;
}

.hotel-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #581c87;
  margin-bottom: 0.25rem;
}

.hotel-address {
  font-size: 0.8125rem;
  color: #7c3aed;
  margin-bottom: 0.25rem;
}

.hotel-rating {
  font-size: 0.8125rem;
  color: #6d28d9;
  font-weight: 600;
}

.booking-status {
  display: inline-block;
  padding: 0.25rem 0.625rem;
  background: #ddd6fe;
  color: #5b21b6;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

/* 备注 */
.notes-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 0.5rem;
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #92400e;
  line-height: 1.5;
}
</style>
