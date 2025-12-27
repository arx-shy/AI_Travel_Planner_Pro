<template>
  <div class="glass-card flex-1 p-8 flex flex-col">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-bold text-slate-800">
        {{ itinerary.title }}
      </h3>
      <div class="flex gap-2">
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
        <AppButton
          v-if="showDetails"
          size="sm"
          variant="ghost"
          icon="refresh"
          @click="handleGenerateDetail"
          :loading="isGenerating"
        >
          AI生成详细行程
        </AppButton>
        <AppButton
          v-if="showDetails"
          size="sm"
          variant="ghost"
          icon="lightbulb"
          @click="showOptimizeDialog = true"
        >
          AI优化
        </AppButton>
        <AppButton
          v-if="showDetails && !isEditing"
          size="sm"
          variant="primary"
          icon="edit"
          @click="isEditing = true"
        >
          编辑行程
        </AppButton>
        <AppButton
          v-else-if="showDetails && isEditing"
          size="sm"
          variant="secondary"
          icon="times"
          @click="isEditing = false"
        >
          取消编辑
        </AppButton>
        <AppButton
          v-if="showDetails"
          size="sm"
          variant="secondary"
          icon="refresh"
          @click="handleGenerateDetail"
          :loading="isGenerating"
        >
          AI生成详细行程
        </AppButton>
        <AppButton
          v-if="showDetails"
          size="sm"
          variant="secondary"
          icon="lightbulb"
          @click="showOptimizeDialog = true"
        >
          AI优化
        </AppButton>
        <AppButton
          v-if="showDetails && !isEditing"
          size="sm"
          variant="primary"
          icon="edit"
          @click="isEditing = true"
        >
          编辑行程
        </AppButton>
        <AppButton
          v-else-if="showDetails && isEditing"
          size="sm"
          variant="outline"
          icon="times"
          @click="isEditing = false"
        >
          取消编辑
        </AppButton>
        <div class="inline-flex">
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
    </div>

    <!-- 摘要信息 -->
    <div v-if="!showDetails" class="grid grid-cols-2 gap-3 mb-6">
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        目的地：{{ itinerary.destination }}
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        天数：{{ itinerary.days }} 天
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        预算：¥{{ itinerary.budget }}
      </div>
      <div class="bg-white/80 rounded-xl px-4 py-3 border border-slate-100">
        状态：{{ statusLabels[itinerary.status] }}
      </div>
    </div>

    <!-- 详细行程展示 -->
    <div v-else class="itinerary-details">
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

      <!-- 每日详情 -->
      <div v-for="(day, index) in displayDays" :key="day.day" class="mb-6">
        <DailyDetail
          :day="day"
          :editable="isEditing"
          @edit="handleEditDay(day.day)"
        />
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
import { ref, computed } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import { useItineraryStore } from '@/stores/itinerary'
import DailyDetail from './DailyDetail.vue'

const props = defineProps<{
  itinerary: any
}>()

const emit = defineEmits<{
  delete: [number]
}>()

const showDetails = ref(false)
const isEditing = ref(false)
const isGenerating = ref(false)
const isOptimizing = ref(false)
const isSaving = ref(false)
const showOptimizeDialog = ref(false)
const optimizeFeedback = ref('')

const itineraryStore = useItineraryStore()

const statusLabels = {
  draft: '草稿',
  active: '进行中',
  completed: '已完成',
  archived: '已归档'
}

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
  if (result.success) {
    console.log('详细行程生成成功')
  }
}

const handleOptimize = async () => {
  isOptimizing.value = true
  const result = await itineraryStore.optimizeItinerary(
    props.itinerary.id,
    {
      feedback: optimizeFeedback.value,
      affected_days: []  // 可以扩展为选择具体的天数
    }
  )
  isOptimizing.value = false
  showOptimizeDialog.value = false
  if (result.success) {
    console.log('行程优化成功')
  }
}

const handleEditDay = (dayNumber: number) => {
  emit('edit', dayNumber)
}

const handleSave = async () => {
  isSaving.value = true
  const result = await itineraryStore.updateItinerary(props.itinerary.id, {
    title: props.itinerary.title
  })
  isSaving.value = false
  isEditing.value = false
  if (result.success) {
    console.log('行程保存成功')
  }
}
</script>

<style scoped>
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
}

.feedback-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.itinerary-details {
  max-height: 600px;
  overflow-y: auto;
}
</style>

