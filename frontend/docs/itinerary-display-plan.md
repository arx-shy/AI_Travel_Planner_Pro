# 行程展示前端设计方案

## 1. 数据展示层级

### 页面布局 (Planner.vue)
```
┌─────────────────────────────────────────────────────┐
│  Planner.vue                                         │
│  ┌─────────────┬─────────────────────────────────┐   │
│  │ 左侧栏      │ 右侧主区域                      │   │
│  │             │                                 │   │
│  │ ┌─────────┐ │ ┌─────────────────────────────┐ │   │
│  │ │行程表单 │ │ │ 顶部：PlannerHeader         │ │   │
│  │ │         │ │ └─────────────────────────────┘ │   │
│  │ │目的地   │ │                                 │   │
│  │ │天数     │ │ ┌─────────────────────────────┐ │   │
│  │ │预算     │ │ │ MapPreview (地图预览)      │ │   │
│  │ │风格     │ │ │ - 可选展开/收起             │ │   │
│  │ │         │ │ │ - 显示行程路线              │ │   │
│  │ │[生成]   │ │ └─────────────────────────────┘ │   │
│  │ └─────────┘ │                                 │   │
│  │             │ ┌─────────────────────────────┐ │   │
│  │ ┌─────────┐ │ │ ItineraryCard (行程卡片)    │ │   │
│  │ │灵感卡片 │ │ │                             │ │   │
│  │ └─────────┘ │ │ 【折叠状态】                │ │   │
│  │             │ │ - 标题                       │ │   │
│  └─────────────┘ │ - 目的地、天数、预算、状态  │ │
│                  │ - [查看详情] 按钮            │ │
│                  │ │                             │ │
│                  │ │ 【展开状态】                │ │
│                  │ │ ┌─────────────────────────┐ │ │
│                  │ │ │ 行程概览面板            │ │ │
│                  │ │ │ - 摘要                   │ │ │
│                  │ │ │ - 亮点                   │ │ │
│                  │ │ │ - 费用概览              │ │ │
│                  │ │ │ - 最佳季节、天气        │ │ │
│                  │ │ └─────────────────────────┘ │ │
│                  │ │                             │ │
│                  │ │ ┌─────────────────────────┐ │ │
│                  │ │ │ 行前准备面板            │ │ │
│                  │ │ │ - 必备证件              │ │ │
│                  │ │ │ - 必备物品              │ │ │
│                  │ │ │ - 预订提醒              │ │ │
│                  │ │ └─────────────────────────┘ │ │
│                  │ │                             │ │
│                  │ │ ┌─────────────────────────┐ │ │
│                  │ │ │ 每日行程详情            │ │ │
│                  │ │ │ Day 1: 标题             │ │ │
│                  │ │ │   - 活动时间线          │ │ │
│                  │ │ │   - 住宿、餐饮          │ │ │
│                  │ │ │   - 备注                │ │ │
│                  │ │ │ Day 2: 标题             │ │ │
│                  │ │ │   ...                   │ │ │
│                  │ │ │ Day 3: 标题             │ │ │
│                  │ │ │   ...                   │ │ │
│                  │ │ └─────────────────────────┘ │ │
│                  │ │                             │ │
│                  │ │ ┌─────────────────────────┐ │ │
│                  │ │ │ 实用提示面板            │ │ │
│                  │ │ │ - 交通、住宿、餐饮      │ │ │
│                  │ │ │ - 购物、安全提示        │ │ │
│                  │ │ └─────────────────────────┘ │ │
│                  │ │                             │ │
│                  │ │ [收起] [AI优化] [编辑] [删除]│ │
│                  │ └─────────────────────────────┘ │
│                  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## 2. ItineraryCard 组件结构

### 2.1 折叠状态（默认）
```vue
<div class="itinerary-card">
  <div class="card-header">
    <h3>{{ itinerary.title }}</h3>
    <button>查看详情</button>
  </div>

  <div class="info-grid">
    <div class="info-item">📍 目的地：{{ itinerary.destination }}</div>
    <div class="info-item">📅 天数：{{ itinerary.days }}天</div>
    <div class="info-item">💰 预算：¥{{ itinerary.budget }}</div>
    <div class="info-item">✨ 状态：{{ statusLabels[itinerary.status] }}</div>
  </div>
</div>
```

### 2.2 展开状态
```vue
<div class="itinerary-card expanded">
  <!-- 顶部操作栏 -->
  <div class="card-header">
    <h3>{{ itinerary.title }}</h3>
    <div class="actions">
      <button>收起</button>
      <button>AI生成详细行程</button>
      <button>AI优化</button>
      <button>编辑</button>
      <button>删除</button>
    </div>
  </div>

  <!-- 面板1：行程概览 -->
  <div class="panel overview-panel">
    <h4>✨ 行程概览</h4>
    <div class="summary">{{ itinerary.summary }}</div>

    <div class="highlights">
      <h5>行程亮点</h5>
      <ul>
        <li v-for="highlight in itinerary.highlights" :key="highlight">
          {{ highlight }}
        </li>
      </ul>
    </div>

    <div class="cost-info">
      <div class="cost-item">
        <span class="label">预算</span>
        <span class="value">¥{{ itinerary.budget }}</span>
      </div>
      <div class="cost-item">
        <span class="label">预计花费</span>
        <span class="value">¥{{ itinerary.actual_cost }}</span>
      </div>
    </div>

    <div class="meta-info">
      <div v-if="itinerary.best_season">
        <span>🌸 最佳季节：{{ itinerary.best_season }}</span>
      </div>
      <div v-if="itinerary.weather">
        <span>🌤️ 天气提示：{{ itinerary.weather }}</span>
      </div>
    </div>
  </div>

  <!-- 面板2：行前准备 -->
  <div class="panel preparation-panel">
    <h4>📋 行前准备</h4>

    <div class="preparation-section">
      <div class="section-title">
        <AppIcon name="id-card" />
        <h5>必备证件</h5>
      </div>
      <div class="tags">
        <span v-for="doc in itinerary.preparation?.documents" :key="doc">
          {{ doc }}
        </span>
      </div>
    </div>

    <div class="preparation-section">
      <div class="section-title">
        <AppIcon name="suitcase" />
        <h5>必备物品</h5>
      </div>
      <div class="tags">
        <span v-for="item in itinerary.preparation?.essentials" :key="item">
          {{ item }}
        </span>
      </div>
    </div>

    <div class="preparation-section">
      <div class="section-title">
        <AppIcon name="calendar-check" />
        <h5>预订提醒</h5>
      </div>
      <ul class="checklist">
        <li v-for="reminder in itinerary.preparation?.booking_reminders" :key="reminder">
          {{ reminder }}
        </li>
      </ul>
    </div>
  </div>

  <!-- 面板3：每日行程详情 -->
  <div class="panel days-panel">
    <h4>📅 每日行程</h4>

    <div v-for="day in itinerary.days_detail" :key="day.day_number" class="day-section">
      <DailyDetail :day="day" :editable="isEditing" />
    </div>
  </div>

  <!-- 面板4：实用提示 -->
  <div class="panel tips-panel">
    <h4>💡 实用提示</h4>

    <div class="tip-sections">
      <div class="tip-section">
        <div class="section-title">
          <AppIcon name="bus" />
          <h5>交通</h5>
        </div>
        <p>{{ itinerary.tips?.transportation }}</p>
      </div>

      <div class="tip-section">
        <div class="section-title">
          <AppIcon name="bed" />
          <h5>住宿</h5>
        </div>
        <p>{{ itinerary.tips?.accommodation }}</p>
      </div>

      <div class="tip-section">
        <div class="section-title">
          <AppIcon name="utensils" />
          <h5>餐饮</h5>
        </div>
        <p>{{ itinerary.tips?.food }}</p>
      </div>

      <div class="tip-section">
        <div class="section-title">
          <AppIcon name="shopping-bag" />
          <h5>购物</h5>
        </div>
        <p>{{ itinerary.tips?.shopping }}</p>
      </div>

      <div class="tip-section">
        <div class="section-title">
          <AppIcon name="shield" />
          <h5>安全</h5>
        </div>
        <p>{{ itinerary.tips?.safety }}</p>
      </div>

      <div v-if="itinerary.tips?.other?.length" class="tip-section">
        <div class="section-title">
          <AppIcon name="lightbulb" />
          <h5>其他</h5>
        </div>
        <ul>
          <li v-for="tip in itinerary.tips.other" :key="tip">{{ tip }}</li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

## 3. DailyDetail 组件结构

```vue
<template>
  <div class="daily-detail-card">
    <!-- 天数标题 -->
    <div class="day-header">
      <div class="day-badge">第{{ day.day_number }}天</div>
      <h4>{{ day.title }}</h4>

      <!-- 天数统计 -->
      <div class="day-stats">
        <span v-if="day.activities">
          {{ day.activities.length }}个活动
        </span>
        <span v-if="day.total_cost">
          花费¥{{ day.total_cost }}
        </span>
      </div>
    </div>

    <!-- 活动时间线 -->
    <div class="activities-timeline">
      <ActivityTimeline :activities="day.activities" />
    </div>

    <!-- 住宿信息（如果有） -->
    <div v-if="day.accommodation" class="accommodation-box">
      <AppIcon name="bed" class="text-teal-500" />
      <div class="accommodation-info">
        <div class="hotel-name">{{ day.accommodation.name }}</div>
        <div class="hotel-address">{{ day.accommodation.address }}</div>
        <div v-if="day.accommodation.rating" class="hotel-rating">
          评分：{{ day.accommodation.rating }}/5
        </div>
      </div>
    </div>

    <!-- 备注 -->
    <div v-if="day.notes" class="notes-box">
      <AppIcon name="info-circle" />
      <span>{{ day.notes }}</span>
    </div>
  </div>
</template>
```

## 4. ActivityTimeline 组件结构

```vue
<template>
  <div class="activity-timeline">
    <div
      v-for="(activity, index) in activities"
      :key="index"
      class="timeline-item"
      :class="`type-${activity.type}`"
    >
      <!-- 时间标记 -->
      <div class="time-badge">
        {{ activity.time }}
      </div>

      <!-- 活动卡片 -->
      <ActivityCard :activity="activity" />

      <!-- 连接线（除了最后一个） -->
      <div v-if="index < activities.length - 1" class="timeline-connector"></div>
    </div>
  </div>
</template>
```

## 5. ActivityCard 组件结构

```vue
<template>
  <div class="activity-card" :class="`activity-${activity.type}`">
    <!-- 活动标题 -->
    <div class="activity-header">
      <div class="activity-icon">
        <AppIcon :name="getTypeIcon(activity.type)" />
      </div>
      <div class="activity-title-block">
        <h5>{{ activity.title }}</h5>
        <div class="activity-meta">
          <span class="duration">{{ activity.duration }}</span>
          <span class="type">{{ getTypeLabel(activity.type) }}</span>
        </div>
      </div>

      <!-- 费用标签 -->
      <div v-if="activity.average_cost" class="cost-badge">
        ¥{{ activity.average_cost }}
      </div>
    </div>

    <!-- 活动描述 -->
    <p v-if="activity.description" class="activity-description">
      {{ activity.description }}
    </p>

    <!-- 亮点（景点类型） -->
    <div v-if="activity.highlights?.length" class="highlights">
      <div v-for="highlight in activity.highlights" :key="highlight" class="highlight-item">
        ⭐ {{ highlight }}
      </div>
    </div>

    <!-- 门票信息（景点类型） -->
    <div v-if="activity.ticket_price !== undefined" class="ticket-info">
      <span class="label">门票</span>
      <span v-if="activity.ticket_price === 0" class="value free">免费</span>
      <span v-else class="value">¥{{ activity.ticket_price }}</span>
      <span v-if="activity.need_booking" class="booking-tag">需预订</span>
    </div>

    <!-- 菜品推荐（餐饮类型） -->
    <div v-if="activity.recommended_dishes?.length" class="dishes">
      <div class="dishes-title">🍽️ 必点菜品</div>
      <div class="dishes-list">
        <span v-for="dish in activity.recommended_dishes" :key="dish" class="dish-tag">
          {{ dish }}
        </span>
      </div>
    </div>

    <!-- 实用提示 -->
    <div v-if="activity.tips?.length" class="activity-tips">
      <div v-for="tip in activity.tips" :key="tip" class="tip-item">
        💡 {{ tip }}
      </div>
    </div>

    <!-- 交通信息 -->
    <div v-if="activity.transportation" class="transportation-info">
      <AppIcon name="route" />
      <span>{{ activity.transportation.method }}</span>
      <span v-if="activity.transportation.cost">
        ¥{{ activity.transportation.cost }}
      </span>
      <span v-if="activity.transportation.duration">
        {{ activity.transportation.duration }}
      </span>
    </div>

    <!-- 地址信息 -->
    <div v-if="activity.address" class="address">
      <AppIcon name="map-marker" />
      <span>{{ activity.address }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'

const props = defineProps<{
  activity: any
}>()

function getTypeIcon(type: string) {
  const icons = {
    attraction: 'camera',
    meal: 'utensils',
    transport: 'bus',
    accommodation: 'bed',
    shopping: 'shopping-bag',
    entertainment: 'gamepad'
  }
  return icons[type] || 'circle'
}

function getTypeLabel(type: string) {
  const labels = {
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
```

## 6. 样式设计

### 6.1 类型颜色方案
```css
/* 景点 - 绿色 */
.activity-attraction { --accent: #10b981; }

/* 餐饮 - 橙色 */
.activity-meal { --accent: #f97316; }

/* 交通 - 蓝色 */
.activity-transport { --accent: #3b82f6; }

/* 住宿 - 紫色 */
.activity-accommodation { --accent: #8b5cf6; }

/* 购物 - 粉色 */
.activity-shopping { --accent: #ec4899; }

/* 娱乐 - 黄色 */
.activity-entertainment { --accent: #eab308; }
```

### 6.2 卡片风格
- 使用毛玻璃效果（glass-card）
- 圆角边框（rounded-xl）
- 柔和阴影（shadow-sm）
- 渐变背景装饰

## 7. 交互流程

### 7.1 生成流程
```typescript
// 用户点击"生成"按钮
1. 显示生成进度条
2. 调用 createItinerary() 创建基础行程
3. 自动调用 generateDetailedItinerary() 生成详细行程
4. 显示加载动画："AI正在为您规划行程..."
5. 生成完成后自动展开ItineraryCard
6. 显示成功提示
```

### 7.2 优化流程
```typescript
// 用户点击"AI优化"按钮
1. 弹出优化对话框
2. 用户输入反馈："第一天太累了，想轻松点"
3. 调用 optimizeItinerary() API
4. 显示优化中动画
5. 更新展示优化后的行程
```

## 8. 数据流

```typescript
// Store (itinerary.ts)
interface ItineraryState {
  currentItinerary: PlanResponse | null
  isGenerating: boolean
  isOptimizing: boolean
  error: string | null
}

// PlanResponse 数据结构
interface PlanResponse {
  id: number
  title: string
  destination: string
  days: number
  budget: number
  status: string

  // V2 新增字段
  summary: string
  highlights: string[]
  best_season: string
  weather: string
  actual_cost: number

  preparation: {
    documents: string[]
    essentials: string[]
    suggestions: string[]
    booking_reminders: string[]
  }

  tips: {
    transportation: string
    accommodation: string
    food: string
    shopping: string
    safety: string
    other?: string[]
  }

  days_detail: DayPlan[]
}
```

## 9. 移动端适配

- 使用响应式网格布局
- 小屏幕时面板折叠为卡片
- 支持左右滑动查看更多活动
- 底部固定操作栏
