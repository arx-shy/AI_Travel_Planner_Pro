<template>
  <div class="glass-card flex-1 p-8 flex flex-col">
    <!-- 标题和操作按钮 -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-bold text-slate-800">
        {{ itinerary.title }}
      </h3>
      <div class="flex gap-2">
        <!-- 查看详情/收起按钮 -->
        <AppButton
          v-if="!showDetails && !isEditing"
          size="sm"
          variant="outline"
          icon="eye"
          @click="showDetails = true"
        >
          查看详情
        </AppButton>
        <AppButton
          v-else-if="showDetails && !isEditing"
          size="sm"
          variant="outline"
          icon="eye-slash"
          @click="showDetails = false"
        >
          收起
        </AppButton>

        <!-- 展开状态下的操作按钮 -->
        <template v-if="showDetails">
          <AppButton
            size="sm"
            variant="ghost"
            icon="refresh"
            @click="handleGenerateDetail"
            :loading="isGenerating"
          >
            AI生成详细行程
          </AppButton>
          <AppButton
            size="sm"
            variant="ghost"
            icon="lightbulb"
            @click="showOptimizeDialog = true"
          >
            AI优化
          </AppButton>
          <AppButton
            v-if="!isEditing"
            size="sm"
            variant="primary"
            icon="edit"
            @click="isEditing = true"
          >
            编辑行程
          </AppButton>
          <AppButton
            v-else
            size="sm"
            variant="outline"
            icon="times"
            @click="isEditing = false"
          >
            取消编辑
          </AppButton>
          <AppButton
            size="sm"
            variant="ghost"
            icon="trash"
            @click="$emit('delete', itinerary.id)"
          >
            删除
          </AppButton>
        </template>
      </div>
    </div>

    <!-- 折叠状态：4个统计卡片 -->
    <div v-if="!showDetails" class="grid grid-cols-2 gap-3 mb-6">
      <div class="stat-card">
        <AppIcon name="map-marker" class="text-teal-500" />
        <div class="stat-content">
          <div class="stat-label">目的地</div>
          <div class="stat-value">{{ itinerary.destination }}</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="calendar" class="text-blue-500" />
        <div class="stat-content">
          <div class="stat-label">天数</div>
          <div class="stat-value">{{ itinerary.days }} 天</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="credit-card" class="text-green-500" />
        <div class="stat-content">
          <div class="stat-label">预算</div>
          <div class="stat-value">¥{{ itinerary.budget }}</div>
        </div>
      </div>
      <div class="stat-card">
        <AppIcon name="flag" class="text-purple-500" />
        <div class="stat-content">
          <div class="stat-label">状态</div>
          <div class="stat-value">{{ statusLabels[itinerary.status] }}</div>
        </div>
      </div>
    </div>

    <!-- 展开状态：V2详细信息 -->
    <div v-else class="itinerary-details">
      <!-- AI生成状态提示 -->
      <div v-if="isGenerating || isOptimizing || props.isGeneratingDetail" class="ai-status-banner">
        <div class="flex items-center gap-3">
          <div class="w-5 h-5 border-2 border-teal-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="status-text">
            {{ isGenerating ? 'AI正在生成详细行程...' : isOptimizing ? 'AI正在优化行程...' : 'AI正在规划行程...' }}
          </span>
          <span class="status-hint">（后台进行中，请稍候）</span>
        </div>
      </div>
      <!-- AI优化弹窗 -->
      <div v-if="showOptimizeDialog" class="optimize-dialog">
        <div class="dialog-content">
          <h4>AI优化</h4>
          <textarea
            v-model="optimizeFeedback"
            class="feedback-input"
            placeholder="描述不满意的地方，AI会优化相应的部分"
            rows="3"
          />
          <div class="dialog-actions">
            <AppButton variant="secondary" @click="showOptimizeDialog = false">
              取消
            </AppButton>
            <AppButton
              @click="handleOptimize"
              :loading="isOptimizing"
            >
              优化行程
            </AppButton>
          </div>
        </div>
      </div>

      <!-- 面板1：行程概览 -->
      <div v-if="hasOverviewData" class="panel-section overview-panel">
        <div class="panel-header">
          <AppIcon name="compass" class="text-yellow-500" />
          <h4 class="panel-title">行程概览</h4>
        </div>

        <!-- 摘要 -->
        <p v-if="itinerary.summary" class="overview-summary">
          {{ itinerary.summary }}
        </p>

        <!-- 亮点 -->
        <div v-if="itinerary.highlights && itinerary.highlights.length" class="highlights-grid">
          <div v-for="(highlight, index) in itinerary.highlights" :key="index" class="highlight-card">
            <span class="highlight-number">{{ index + 1 }}</span>
            <span class="highlight-text">{{ highlight }}</span>
          </div>
        </div>

        <!-- 费用对比 -->
        <div v-if="itinerary.actual_cost" class="cost-comparison">
          <div class="cost-item budget">
            <div class="cost-label">预算</div>
            <div class="cost-value">¥{{ itinerary.budget }}</div>
          </div>
          <div class="cost-item actual">
            <div class="cost-label">预计花费</div>
            <div class="cost-value">¥{{ itinerary.actual_cost }}</div>
          </div>
          <div class="cost-item saved">
            <div class="cost-label">节省</div>
            <div class="cost-value">¥{{ itinerary.budget - itinerary.actual_cost }}</div>
          </div>
        </div>

        <!-- 最佳季节和天气 -->
        <div class="season-weather-row">
          <div v-if="itinerary.best_season" class="info-item">
            <AppIcon name="flower" class="text-pink-500" />
            <span class="info-label">最佳季节</span>
            <span class="info-value">{{ itinerary.best_season }}</span>
          </div>
          <div v-if="itinerary.weather" class="info-item">
            <AppIcon name="cloud" class="text-gray-500" />
            <span class="info-label">天气提示</span>
            <span class="info-value">{{ itinerary.weather }}</span>
          </div>
        </div>
      </div>

      <!-- 面板2：行前准备 -->
      <div v-if="hasPreparationData" class="panel-section preparation-panel">
        <div class="panel-header">
          <AppIcon name="suitcase" class="text-blue-500" />
          <h4 class="panel-title">行前准备</h4>
        </div>

        <!-- 必备证件 -->
        <div v-if="itinerary.preparation?.documents?.length" class="preparation-section">
          <h5 class="section-title">
            <AppIcon name="id-card" class="text-blue-500" />
            必备证件
          </h5>
          <div class="tags-list">
            <span
              v-for="doc in itinerary.preparation.documents"
              :key="doc"
              class="tag-tag document-tag"
            >
              {{ doc }}
            </span>
          </div>
        </div>

        <!-- 必备物品 -->
        <div v-if="itinerary.preparation?.essentials?.length" class="preparation-section">
          <h5 class="section-title">
            <AppIcon name="package" class="text-orange-500" />
            必备物品
          </h5>
          <div class="tags-list">
            <span
              v-for="item in itinerary.preparation.essentials"
              :key="item"
              class="tag-tag essential-tag"
            >
              {{ item }}
            </span>
          </div>
        </div>

        <!-- 预订提醒 -->
        <div v-if="itinerary.preparation?.booking_reminders?.length" class="preparation-section">
          <h5 class="section-title">
            <AppIcon name="bell" class="text-red-500" />
            预订提醒
          </h5>
          <ul class="reminders-list">
            <li v-for="(reminder, index) in itinerary.preparation.booking_reminders" :key="index">
              {{ reminder }}
            </li>
          </ul>
        </div>
      </div>

      <!-- 面板3：每日行程 -->
      <div v-if="displayDays.length" class="panel-section days-panel">
        <div class="panel-header">
          <AppIcon name="calendar-days" class="text-purple-500" />
          <h4 class="panel-title">每日行程</h4>
        </div>

        <div class="days-container">
          <DailyDetail
            v-for="day in displayDays"
            :key="day.day_number"
            :day="day"
            :editable="isEditing"
            @edit="handleEditDay(day.day_number)"
            @updateDay="handleUpdateDay"
          />
        </div>
      </div>

      <!-- 面板4：实用提示 -->
      <div v-if="hasTipsData" class="panel-section tips-panel">
        <div class="panel-header">
          <AppIcon name="lightbulb" class="text-teal-500" />
          <h4 class="panel-title">实用提示</h4>
        </div>

        <div class="tips-grid">
          <TipCard
            v-if="itinerary.tips?.transportation"
            icon="bus"
            title="交通"
            :content="itinerary.tips.transportation"
          />
          <TipCard
            v-if="itinerary.tips?.accommodation"
            icon="bed"
            title="住宿"
            :content="itinerary.tips.accommodation"
          />
          <TipCard
            v-if="itinerary.tips?.food"
            icon="utensils"
            title="餐饮"
            :content="itinerary.tips.food"
          />
          <TipCard
            v-if="itinerary.tips?.shopping"
            icon="shopping-bag"
            title="购物"
            :content="itinerary.tips.shopping"
          />
          <TipCard
            v-if="itinerary.tips?.safety"
            icon="shield"
            title="安全"
            :content="itinerary.tips.safety"
          />
          <TipCard
            v-if="itinerary.tips?.other && itinerary.tips.other.length"
            icon="info-circle"
            title="其他提示"
            :content="itinerary.tips.other.join('; ')"
          />
        </div>
      </div>

      <!-- 保存按钮（编辑模式） -->
      <div v-if="isEditing" class="edit-actions flex justify-center gap-3 mt-6">
        <AppButton
          @click="handleSave"
          variant="primary"
          icon="save"
          :loading="isSaving"
        >
          保存修改
        </AppButton>
        <AppButton
          @click="isEditing = false"
          variant="secondary"
        >
          取消
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'
import TipCard from './TipCard.vue'
import DailyDetail from './DailyDetail.vue'
import { useItineraryStore } from '@/stores/itinerary'
import type { Itinerary } from '@/types/api'

const props = defineProps<{
  itinerary: Itinerary
  isGeneratingDetail?: boolean
}>()

const emit = defineEmits<{
  delete: [number]
  edit: [number]
  generateComplete: [success: boolean]
  optimizeComplete: [success: boolean]
  updateItinerary: [itinerary: Itinerary]
}>()

const showDetails = ref(false)
const isEditing = ref(false)
const isGenerating = ref(false)
const isOptimizing = ref(false)
const isSaving = ref(false)
const showOptimizeDialog = ref(false)
const optimizeFeedback = ref('')

// 本地编辑的行程数据（用于编辑模式）
const editableItinerary = ref<Itinerary>({ ...props.itinerary })

// 监听行程更新，同步到编辑数据
watch(() => props.itinerary, (newItinerary) => {
  editableItinerary.value = { ...newItinerary }
}, { deep: true })

const itineraryStore = useItineraryStore()

const statusLabels = {
  draft: '草稿',
  active: '进行中',
  completed: '已完成',
  archived: '已归档'
}

// V2数据检查
const hasOverviewData = computed(() => {
  return !!(
    props.itinerary.summary ||
    (props.itinerary.highlights && props.itinerary.highlights.length) ||
    props.itinerary.actual_cost ||
    props.itinerary.best_season ||
    props.itinerary.weather
  )
})

const hasPreparationData = computed(() => {
  return !!(
    props.itinerary.preparation?.documents?.length ||
    props.itinerary.preparation?.essentials?.length ||
    props.itinerary.preparation?.booking_reminders?.length
  )
})

const hasTipsData = computed(() => {
  return !!(
    props.itinerary.tips?.transportation ||
    props.itinerary.tips?.accommodation ||
    props.itinerary.tips?.food ||
    props.itinerary.tips?.shopping ||
    props.itinerary.tips?.safety ||
    (props.itinerary.tips?.other && props.itinerary.tips.other.length)
  )
})

const displayDays = computed(() => {
  if (!props.itinerary.days_detail || !Array.isArray(props.itinerary.days_detail)) {
    return []
  }
  return props.itinerary.days_detail
})

const handleGenerateDetail = async () => {
  isGenerating.value = true
  const result = await itineraryStore.generateDetailedItinerary(
    props.itinerary.id,
    true  // 使用严格JSON格式
  )
  isGenerating.value = false
  emit('generateComplete', result.success)
}

const handleOptimize = async () => {
  isOptimizing.value = true
  const result = await itineraryStore.optimizeItinerary(
    props.itinerary.id,
    {
      feedback: optimizeFeedback.value,
      affected_days: []
    }
  )
  isOptimizing.value = false
  showOptimizeDialog.value = false
  emit('optimizeComplete', result.success)
}

const handleEditDay = (dayNumber: number) => {
  emit('edit', dayNumber)
}

// 处理活动更新
const handleUpdateDay = (dayNumber: number, updatedActivities: any[]) => {
  if (!editableItinerary.value.days_detail) {
    editableItinerary.value.days_detail = []
  }

  const dayIndex = editableItinerary.value.days_detail.findIndex(
    d => d.day_number === dayNumber
  )

  if (dayIndex !== -1) {
    editableItinerary.value.days_detail[dayIndex].activities = updatedActivities
  }
}

const handleSave = async () => {
  isSaving.value = true

  // 计算更新后的总花费
  let totalCost = 0
  if (editableItinerary.value.days_detail) {
    editableItinerary.value.days_detail.forEach(day => {
      day.activities?.forEach(activity => {
        totalCost += activity.average_cost || 0
      })
    })
  }
  editableItinerary.value.actual_cost = totalCost

  const result = await itineraryStore.updateItinerary(
    props.itinerary.id,
    editableItinerary.value
  )

  isSaving.value = false
  isEditing.value = false

  if (result.success) {
    emit('updateItinerary', editableItinerary.value)
  }
}
</script>

<style scoped>
/* 统计卡片 */
.stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  border: 1px solid rgba(226,232,240,0.8);
  border-radius: 0.75rem;
  transition: all 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.stat-card .stat-content {
  flex: 1;
}

.stat-card .stat-label {
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.stat-card .stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

/* 详细信息容器 */
.itinerary-details {
  max-height: 600px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* AI状态横幅 */
.ai-status-banner {
  position: sticky;
  top: 0;
  z-index: 10;
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 1rem 1rem 0 0;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
}

.ai-status-banner .status-text {
  flex: 1;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #065f46;
}

.ai-status-banner .status-hint {
  font-size: 0.8125rem;
  color: #059669;
  opacity: 0.8;
}

/* 面板通用样式 */
.panel-section {
  padding: 1.5rem;
  border-radius: 1rem;
  margin-bottom: 1rem;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(0,0,0,0.08);
}

.panel-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}

/* 概览面板 */
.overview-panel {
  background: linear-gradient(135deg, #fef9c3 0%, #fef08a 100%);
  border: 1px solid rgba(234,179,8,0.2);
}

.overview-summary {
  font-size: 0.9375rem;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: rgba(255,255,255,0.6);
  border-radius: 0.5rem;
}

.highlights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.highlight-card {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.75rem;
  background: rgba(255,255,255,0.7);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
  line-height: 1.5;
}

.highlight-number {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
  color: #9a3412;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 600;
}

.cost-comparison {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.cost-item {
  padding: 1rem;
  background: rgba(255,255,255,0.7);
  border-radius: 0.5rem;
  text-align: center;
}

.cost-item .cost-label {
  font-size: 0.8125rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.cost-item .cost-value {
  font-size: 1.125rem;
  font-weight: 700;
}

.cost-item.budget .cost-value { color: #3b82f6; }
.cost-item.actual .cost-value { color: #10b981; }
.cost-item.saved .cost-value { color: #16a34a; }

.season-weather-row {
  display: flex;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: rgba(255,255,255,0.7);
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.info-item .info-label {
  font-weight: 600;
  color: #475569;
}

.info-item .info-value {
  color: #64748b;
}

/* 准备面板 */
.preparation-panel {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 1px solid rgba(59,130,246,0.2);
}

.preparation-section {
  margin-bottom: 1rem;
}

.preparation-section:last-child {
  margin-bottom: 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 0.5rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-tag {
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.8125rem;
  font-weight: 500;
}

.document-tag {
  background: rgba(255,255,255,0.8);
  color: #1e40af;
  border: 1px solid rgba(59,130,246,0.3);
}

.essential-tag {
  background: rgba(255,255,255,0.8);
  color: #c2410c;
  border: 1px solid rgba(249,115,22,0.3);
}

.reminders-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.reminders-list li {
  padding: 0.5rem 0.75rem;
  background: rgba(255,255,255,0.7);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
  margin-bottom: 0.375rem;
  line-height: 1.5;
}

.reminders-list li:last-child {
  margin-bottom: 0;
}

/* 每日行程面板 */
.days-panel {
  background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
  border: 1px solid rgba(139,92,246,0.2);
}

.days-container {
  display: flex;
  flex-direction: column;
}

/* 提示面板 */
.tips-panel {
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
  border: 1px solid rgba(249,115,22,0.2);
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 0.75rem;
}

/* 弹窗样式 */
.optimize-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.dialog-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
}

.dialog-content h4 {
  margin-bottom: 1rem;
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}

.feedback-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  font-family: inherit;
  resize: vertical;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>

