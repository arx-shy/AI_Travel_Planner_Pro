<template>
  <div class="glass-card flex-1 p-8 flex flex-col itinerary-card">
    <!-- 卡片头部 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex-1">
        <h3 class="text-xl font-bold text-slate-800 mb-2">
          {{ itinerary.title }}
        </h3>
        <div v-if="itinerary.summary" class="text-sm text-slate-600 line-clamp-2">
          {{ itinerary.summary }}
        </div>
      </div>

      <div class="flex gap-2">
        <AppButton
          v-if="!showDetails"
          size="sm"
          variant="primary"
          icon="eye"
          @click="showDetails = true"
        >
          查看详情
        </AppButton>
        <AppButton
          v-else
          size="sm"
          variant="outline"
          icon="eye-slash"
          @click="showDetails = false"
        >
          收起
        </AppButton>
      </div>
    </div>

    <!-- 折叠状态：摘要信息 -->
    <div v-if="!showDetails" class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
      <div class="stat-card">
        <AppIcon name="map-marker" class="text-teal-500" />
        <div>
          <div class="text-xs text-slate-500">目的地</div>
          <div class="font-bold text-slate-700">{{ itinerary.destination }}</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="calendar" class="text-blue-500" />
        <div>
          <div class="text-xs text-slate-500">天数</div>
          <div class="font-bold text-slate-700">{{ itinerary.days }}天</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="wallet" class="text-green-500" />
        <div>
          <div class="text-xs text-slate-500">预算</div>
          <div class="font-bold text-slate-700">¥{{ itinerary.budget }}</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="check-circle" class="text-purple-500" />
        <div>
          <div class="text-xs text-slate-500">状态</div>
          <div class="font-bold" :class="statusColorClass">{{ statusLabels[itinerary.status] }}</div>
        </div>
      </div>
    </div>

    <!-- 展开状态：详细内容 -->
    <div v-else class="details-content">
      <!-- 操作栏 -->
      <div class="flex items-center justify-between mb-6 pb-6 border-b border-slate-100">
        <div class="flex gap-2">
          <AppButton
            size="sm"
            variant="secondary"
            icon="refresh"
            @click="handleGenerateDetail"
            :loading="isGenerating"
          >
            {{ isGenerating ? '生成中...' : 'AI生成详细行程' }}
          </AppButton>
          <AppButton
            size="sm"
            variant="ghost"
            icon="lightbulb"
            @click="showOptimizeDialog = true"
          >
            AI优化
          </AppButton>
        </div>
        <div class="flex gap-2">
          <AppButton size="sm" variant="primary" icon="edit">
            编辑
          </AppButton>
          <AppButton
            size="sm"
            variant="ghost"
            icon="trash"
            @click="$emit('delete', itinerary.id)"
          >
            删除
          </AppButton>
        </div>
      </div>

      <!-- 面板1：行程亮点 -->
      <div v-if="itinerary.highlights?.length" class="panel highlights-panel">
        <h4 class="panel-title">
          <AppIcon name="star" class="text-yellow-500" />
          行程亮点
        </h4>
        <div class="highlights-grid">
          <div
            v-for="(highlight, index) in itinerary.highlights.slice(0, 5)"
            :key="index"
            class="highlight-card"
          >
            <span class="highlight-number">{{ index + 1 }}</span>
            <span class="highlight-text">{{ highlight }}</span>
          </div>
        </div>
      </div>

      <!-- 面板2：费用概览 -->
      <div v-if="itinerary.actual_cost" class="panel cost-panel">
        <h4 class="panel-title">
          <AppIcon name="pie-chart" class="text-green-500" />
          费用概览
        </h4>
        <div class="cost-overview">
          <div class="cost-comparison">
            <div class="cost-item">
              <span class="label">预算</span>
              <span class="value budget">¥{{ itinerary.budget }}</span>
            </div>
            <div class="vs-divider">VS</div>
            <div class="cost-item">
              <span class="label">预计花费</span>
              <span class="value actual">¥{{ itinerary.actual_cost }}</span>
            </div>
            <div class="cost-diff" :class="{ 'positive': itinerary.budget > itinerary.actual_cost }">
              {{ (itinerary.budget - itinerary.actual_cost).toFixed(0) }}元
            </div>
          </div>
        </div>
      </div>

      <!-- 面板3：行前准备 -->
      <div v-if="itinerary.preparation" class="panel preparation-panel">
        <h4 class="panel-title">
          <AppIcon name="clipboard-check" class="text-blue-500" />
          行前准备
        </h4>

        <!-- 必备证件 -->
        <div v-if="itinerary.preparation.documents?.length" class="prep-section">
          <h5 class="section-title">
            <AppIcon name="id-card" />
            必备证件
          </h5>
          <div class="tags-container">
            <span
              v-for="doc in itinerary.preparation.documents"
              :key="doc"
              class="tag tag-blue"
            >
              {{ doc }}
            </span>
          </div>
        </div>

        <!-- 必备物品 -->
        <div v-if="itinerary.preparation.essentials?.length" class="prep-section">
          <h5 class="section-title">
            <AppIcon name="suitcase" />
            必备物品
          </h5>
          <div class="tags-container">
            <span
              v-for="item in itinerary.preparation.essentials"
              :key="item"
              class="tag tag-teal"
            >
              {{ item }}
            </span>
          </div>
        </div>

        <!-- 预订提醒 -->
        <div v-if="itinerary.preparation.booking_reminders?.length" class="prep-section">
          <h5 class="section-title">
            <AppIcon name="bell" />
            预订提醒
          </h5>
          <ul class="checklist">
            <li v-for="reminder in itinerary.preparation.booking_reminders" :key="reminder">
              {{ reminder }}
            </li>
          </ul>
        </div>
      </div>

      <!-- 面板4：每日行程详情 -->
      <div v-if="itinerary.days_detail?.length" class="panel days-panel">
        <h4 class="panel-title">
          <AppIcon name="calendar-days" class="text-purple-500" />
          每日行程
        </h4>

        <div class="days-container">
          <div
            v-for="day in itinerary.days_detail"
            :key="day.day_number"
            class="day-card"
          >
            <DailyDetail :day="day" />
          </div>
        </div>
      </div>

      <!-- 面板5：实用提示 -->
      <div v-if="itinerary.tips" class="panel tips-panel">
        <h4 class="panel-title">
          <AppIcon name="lightbulb" class="text-orange-500" />
          实用提示
        </h4>

        <div class="tips-grid">
          <TipCard
            v-if="itinerary.tips.transportation"
            icon="bus"
            title="交通"
            :content="itinerary.tips.transportation"
          />
          <TipCard
            v-if="itinerary.tips.accommodation"
            icon="bed"
            title="住宿"
            :content="itinerary.tips.accommodation"
          />
          <TipCard
            v-if="itinerary.tips.food"
            icon="utensils"
            title="餐饮"
            :content="itinerary.tips.food"
          />
          <TipCard
            v-if="itinerary.tips.shopping"
            icon="shopping-bag"
            title="购物"
            :content="itinerary.tips.shopping"
          />
          <TipCard
            v-if="itinerary.tips.safety"
            icon="shield"
            title="安全"
            :content="itinerary.tips.safety"
          />
        </div>

        <div v-if="itinerary.tips.other?.length" class="other-tips">
          <h5 class="section-title">其他提示</h5>
          <ul>
            <li v-for="tip in itinerary.tips.other" :key="tip">{{ tip }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- AI优化对话框 -->
    <div v-if="showOptimizeDialog" class="modal-overlay" @click.self="showOptimizeDialog = false">
      <div class="modal-content">
        <h4 class="modal-title">AI优化行程</h4>
        <p class="modal-description">
          描述您不满意的地方，AI会为您重新规划行程
        </p>
        <textarea
          v-model="optimizeFeedback"
          class="feedback-textarea"
          placeholder="例如：第一天太累了，想轻松一点；第二天想去更多美食..."
          rows="4"
        ></textarea>
        <div class="modal-actions">
          <AppButton variant="secondary" @click="showOptimizeDialog = false">
            取消
          </AppButton>
          <AppButton
            variant="primary"
            @click="handleOptimize"
            :loading="isOptimizing"
          >
            {{ isOptimizing ? '优化中...' : '开始优化' }}
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'
import DailyDetail from './DailyDetail.vue'
import TipCard from './TipCard.vue'
import { useItineraryStore } from '@/stores/itinerary'

const props = defineProps<{
  itinerary: any
}>()

const emit = defineEmits<{
  delete: [number]
}>()

const showDetails = ref(false)
const showOptimizeDialog = ref(false)
const isGenerating = ref(false)
const isOptimizing = ref(false)
const optimizeFeedback = ref('')

const itineraryStore = useItineraryStore()

const statusLabels = {
  draft: '草稿',
  active: '进行中',
  completed: '已完成',
  archived: '已归档'
}

const statusColorClass = computed(() => {
  const colors = {
    draft: 'text-slate-600',
    active: 'text-blue-600',
    completed: 'text-green-600',
    archived: 'text-gray-500'
  }
  return colors[props.itinerary.status] || colors.draft
})

const handleGenerateDetail = async () => {
  isGenerating.value = true
  try {
    await itineraryStore.generateDetailedItinerary(props.itinerary.id, true)
  } finally {
    isGenerating.value = false
  }
}

const handleOptimize = async () => {
  if (!optimizeFeedback.value.trim()) {
    alert('请输入优化建议')
    return
  }

  isOptimizing.value = true
  try {
    await itineraryStore.optimizeItinerary(props.itinerary.id, {
      feedback: optimizeFeedback.value,
      affected_days: []
    })
    showOptimizeDialog.value = false
    optimizeFeedback.value = ''
  } finally {
    isOptimizing.value = false
  }
}
</script>

<style scoped>
.itinerary-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
  backdrop-filter: blur(10px);
}

/* 统计卡片 */
.stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(255,255,255,0.8);
  border: 1px solid rgba(226,232,240,0.8);
  border-radius: 0.75rem;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* 面板样式 */
.panel {
  padding: 1.5rem;
  background: rgba(255,255,255,0.6);
  border: 1px solid rgba(226,232,240,0.8);
  border-radius: 1rem;
  margin-bottom: 1rem;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
}

/* 亮点卡片 */
.highlights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
}

.highlight-card {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
  border-radius: 0.5rem;
  border: 1px solid #fde047;
}

.highlight-number {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eab308;
  color: white;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: bold;
}

.highlight-text {
  font-size: 0.875rem;
  color: #854d0e;
  line-height: 1.4;
}

/* 费用概览 */
.cost-overview {
  display: flex;
  justify-content: center;
}

.cost-comparison {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.cost-item {
  text-align: center;
}

.cost-item .label {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.cost-item .value {
  font-size: 1.25rem;
  font-weight: 700;
}

.cost-item .value.budget {
  color: #3b82f6;
}

.cost-item .value.actual {
  color: #10b981;
}

.vs-divider {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
}

.cost-diff {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.cost-diff.positive {
  background: #dcfce7;
  color: #166534;
}

/* 准备部分 */
.prep-section {
  margin-bottom: 1rem;
}

.prep-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.5rem;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag-blue {
  background: #dbeafe;
  color: #1e40af;
}

.tag-teal {
  background: #ccfbf1;
  color: #115e59;
}

.checklist {
  list-style: none;
  padding: 0;
}

.checklist li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.5;
}

.checklist li:before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: bold;
}

/* 每日行程容器 */
.days-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 提示网格 */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.other-tips {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.other-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.other-tips li {
  padding: 0.375rem 0;
  padding-left: 1.25rem;
  position: relative;
  font-size: 0.875rem;
  color: #64748b;
}

.other-tips li:before {
  content: '•';
  position: absolute;
  left: 0;
  color: #94a3b8;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.modal-description {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.feedback-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  resize: vertical;
  font-family: inherit;
}

.feedback-textarea:focus {
  outline: none;
  border-color: #14b8a6;
  box-shadow: 0 0 0 3px rgba(20,184,166,0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
