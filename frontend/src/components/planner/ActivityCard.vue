<template>
  <div class="activity-card" :class="`activity-${activity.type}`">
    <!-- 活动标题区 -->
    <div class="activity-header">
      <div class="activity-icon">
        <AppIcon :name="getTypeIcon(activity.type)" />
      </div>
      <div class="activity-title-block">
        <h5 class="activity-title">{{ activity.title }}</h5>
        <div class="activity-meta">
          <span class="duration">{{ activity.duration }}</span>
          <span class="type">{{ getTypeLabel(activity.type) }}</span>
        </div>
      </div>
      <div v-if="activity.average_cost" class="cost-badge">
        ¥{{ activity.average_cost }}
      </div>
    </div>

    <!-- 活动描述 -->
    <p v-if="activity.description" class="activity-description">
      {{ activity.description }}
    </p>

    <!-- 亮点（景点类型） -->
    <div v-if="activity.highlights && activity.highlights.length" class="highlights">
      <div v-for="(highlight, index) in activity.highlights.slice(0, 3)" :key="index" class="highlight-item">
        ⭐ {{ highlight }}
      </div>
    </div>

    <!-- 门票信息（景点类型） -->
    <div v-if="activity.ticket_price !== undefined" class="ticket-info">
      <AppIcon name="ticket" class="text-purple-500" />
      <span class="label">门票</span>
      <span v-if="activity.ticket_price === 0" class="value free">免费</span>
      <span v-else class="value">¥{{ activity.ticket_price }}</span>
      <span v-if="activity.need_booking" class="booking-tag">需预订</span>
      <span v-if="activity.booking_info" class="booking-info">{{ activity.booking_info }}</span>
    </div>

    <!-- 菜品推荐（餐饮类型） -->
    <div v-if="activity.recommended_dishes && activity.recommended_dishes.length" class="dishes">
      <div class="dishes-title">🍽️ 必点菜品</div>
      <div class="dishes-list">
        <span v-for="dish in activity.recommended_dishes.slice(0, 5)" :key="dish" class="dish-tag">
          {{ dish }}
        </span>
      </div>
    </div>

    <!-- 实用提示 -->
    <div v-if="activity.tips && activity.tips.length" class="activity-tips">
      <div v-for="(tip, index) in activity.tips.slice(0, 3)" :key="index" class="tip-item">
        💡 {{ tip }}
      </div>
    </div>

    <!-- 交通信息 -->
    <div v-if="activity.transportation" class="transportation-info">
      <AppIcon name="route" class="text-blue-500" />
      <div class="transport-details">
        <span class="method">{{ activity.transportation.method }}</span>
        <span v-if="activity.transportation.duration" class="duration">
          {{ activity.transportation.duration }}
        </span>
        <span v-if="activity.transportation.cost" class="cost">
          ¥{{ activity.transportation.cost }}
        </span>
        <span v-if="activity.transportation.tips" class="tips">
          {{ activity.transportation.tips }}
        </span>
      </div>
    </div>

    <!-- 地址信息 -->
    <div v-if="activity.address" class="address">
      <AppIcon name="map-marker" class="text-red-500" />
      <span>{{ activity.address }}</span>
    </div>

    <!-- 最佳游览时间 -->
    <div v-if="activity.best_time" class="best-time">
      <AppIcon name="clock" class="text-orange-500" />
      <span class="label">最佳时间</span>
      <span class="value">{{ activity.best_time }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import type { Activity } from '@/types/api'

const props = defineProps<{
  activity: Activity
}>()

function getTypeIcon(type: string): string {
  const icons: Record<string, string> = {
    attraction: 'camera',
    meal: 'utensils',
    transport: 'bus',
    accommodation: 'bed',
    shopping: 'shopping-bag',
    entertainment: 'gamepad'
  }
  return icons[type] || 'circle'
}

function getTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    attraction: '景点',
    meal: '餐饮',
    transport: '交通',
    accommodation: '住宿',
    shopping: '购物',
    entertainment: '娱乐'
  }
  return labels[type] || '其他'
}
</script>

<style scoped>
.activity-card {
  padding: 1rem;
  background: rgba(255,255,255,0.8);
  border: 1px solid rgba(226,232,240,0.8);
  border-radius: 0.75rem;
  margin-bottom: 0.75rem;
  transition: all 0.2s;
}

.activity-card:hover {
  background: rgba(255,255,255,0.95);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* 活动类型颜色 */
.activity-attraction { border-left: 3px solid #10b981; }
.activity-meal { border-left: 3px solid #f97316; }
.activity-transport { border-left: 3px solid #3b82f6; }
.activity-accommodation { border-left: 3px solid #8b5cf6; }
.activity-shopping { border-left: 3px solid #ec4899; }
.activity-entertainment { border-left: 3px solid #eab308; }

/* 头部 */
.activity-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.activity-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 0.5rem;
  color: #10b981;
  font-size: 1.125rem;
}

.activity-attraction .activity-icon { background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); color: #10b981; }
.activity-meal .activity-icon { background: linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%); color: #f97316; }
.activity-transport .activity-icon { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); color: #3b82f6; }
.activity-accommodation .activity-icon { background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); color: #8b5cf6; }
.activity-shopping .activity-icon { background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); color: #ec4899; }
.activity-entertainment .activity-icon { background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%); color: #eab308; }

.activity-title-block {
  flex: 1;
  min-width: 0;
}

.activity-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
  line-height: 1.3;
}

.activity-meta {
  display: flex;
  gap: 0.5rem;
  font-size: 0.75rem;
}

.activity-meta .duration {
  color: #64748b;
}

.activity-meta .type {
  padding: 0.125rem 0.5rem;
  background: #f1f5f9;
  color: #475569;
  border-radius: 0.25rem;
  font-weight: 500;
}

.cost-badge {
  flex-shrink: 0;
  padding: 0.375rem 0.75rem;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #166534;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
}

.activity-description {
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
}

/* 亮点 */
.highlights {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-bottom: 0.75rem;
}

.highlight-item {
  font-size: 0.8125rem;
  color: #65a30d;
  padding: 0.375rem 0.5rem;
  background: #ecfccb;
  border-radius: 0.375rem;
  line-height: 1.4;
}

/* 门票信息 */
.ticket-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #faf5ff;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.8125rem;
}

.ticket-info .label {
  font-weight: 600;
  color: #7c3aed;
}

.ticket-info .value {
  font-weight: 600;
  color: #6d28d9;
}

.ticket-info .value.free {
  color: #16a34a;
}

.booking-tag {
  margin-left: auto;
  padding: 0.125rem 0.5rem;
  background: #fef3c7;
  color: #92400e;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.booking-info {
  font-size: 0.75rem;
  color: #92400e;
  font-style: italic;
}

/* 菜品 */
.dishes {
  margin-bottom: 0.75rem;
}

.dishes-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.375rem;
}

.dishes-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.375rem;
}

.dish-tag {
  padding: 0.25rem 0.625rem;
  background: #fff7ed;
  color: #c2410c;
  border: 1px solid #fed7aa;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 500;
}

/* 提示 */
.activity-tips {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.75rem;
}

.tip-item {
  font-size: 0.8125rem;
  color: #475569;
  padding: 0.375rem 0.5rem;
  background: #f8fafc;
  border-radius: 0.375rem;
  line-height: 1.4;
}

/* 交通信息 */
.transportation-info {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #eff6ff;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  font-size: 0.8125rem;
}

.transport-details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.transport-details .method {
  font-weight: 600;
  color: #1e40af;
}

.transport-details .duration {
  color: #3b82f6;
}

.transport-details .cost {
  font-weight: 600;
  color: #1e40af;
}

.transport-details .tips {
  font-size: 0.75rem;
  color: #64748b;
  font-style: italic;
}

/* 地址 */
.address {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.5rem;
  background: #fef2f2;
  border-radius: 0.375rem;
  margin-bottom: 0.75rem;
  font-size: 0.8125rem;
  color: #991b1b;
}

/* 最佳时间 */
.best-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.5rem;
  background: #fff7ed;
  border-radius: 0.375rem;
  font-size: 0.8125rem;
}

.best-time .label {
  font-weight: 600;
  color: #9a3412;
}

.best-time .value {
  color: #7c2d12;
}
</style>
