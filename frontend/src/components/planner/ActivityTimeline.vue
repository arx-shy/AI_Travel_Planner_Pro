<template>
  <div class="activity-timeline">
    <div
      v-for="(activity, index) in activities"
      :key="index"
      class="activity-item"
    >
      <div class="time-badge">
        {{ activity.time }}
      </div>
      <div class="activity-content">
        <h5 class="activity-title">{{ activity.title }}</h5>
        <p v-if="activity.description" class="activity-description">
          {{ activity.description }}
        </p>
        <div class="activity-meta">
          <span v-if="activity.location" class="meta-item">
            <AppIcon name="map-marker-alt" size="sm" />
            {{ activity.location }}
          </span>
          <span v-if="activity.duration" class="meta-item">
            <AppIcon name="clock" size="sm" />
            {{ activity.duration }}
          </span>
          <span v-if="activity.cost !== undefined" class="meta-item">
            <AppIcon name="money-bill" size="sm" />
            ¥{{ activity.cost }}
          </span>
        </div>
        <div v-if="activity.tips && activity.tips.length" class="tips">
          <span
            v-for="(tip, i) in activity.tips"
            :key="i"
            class="tip"
          >
            <AppIcon name="lightbulb" size="sm" />
            {{ tip }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'

interface Activity {
  time: string
  title: string
  description?: string
  location?: string
  duration?: string
  cost?: number
  tips?: string[]
}

defineProps<{
  activities: Activity[]
}>()
</script>

<style scoped>
.activity-timeline {
  position: relative;
  padding-left: 2rem;
}

.activity-item {
  position: relative;
  padding-bottom: 1.5rem;
}

.activity-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #cbd5e1;
}

.activity-item:last-child::before {
  display: none;
}

.time-badge {
  position: absolute;
  left: -2rem;
  top: 0;
  transform: translateX(-50%);
  background: #14b8a6;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.activity-content {
  padding-left: 0.5rem;
}

.activity-title {
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.activity-description {
  color: #64748b;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.activity-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #64748b;
  font-size: 0.875rem;
}

.tips {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 0.5rem;
}

.tip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #fef3c7;
  border-radius: 0.375rem;
  color: #92400e;
  font-size: 0.875rem;
}
</style>
