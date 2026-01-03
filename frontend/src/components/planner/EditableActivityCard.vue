<template>
  <div class="editable-activity-card" :class="`activity-type-${activity.type}`">
    <!-- 查看模式 -->
    <div v-if="!isEditing" class="activity-view">
      <div class="activity-header">
        <div class="activity-time">{{ activity.time }}</div>
        <div class="activity-type-badge">{{ typeLabels[activity.type] }}</div>
        <AppButton
          v-if="editable"
          size="sm"
          variant="ghost"
          icon="edit"
          class="edit-btn"
          @click="startEdit"
        >
          编辑
        </AppButton>
      </div>
      <h5 class="activity-title">{{ activity.title }}</h5>
      <p class="activity-description">{{ activity.description }}</p>

      <!-- 扩展信息 -->
      <div v-if="showDetails" class="activity-details">
        <div v-if="activity.address" class="detail-row">
          <AppIcon name="map-marker" class="text-gray-500" />
          <span>{{ activity.address }}</span>
        </div>
        <div v-if="activity.duration" class="detail-row">
          <AppIcon name="clock" class="text-blue-500" />
          <span>时长：{{ activity.duration }}</span>
        </div>
        <div v-if="activity.ticket_price" class="detail-row">
          <AppIcon name="ticket" class="text-green-500" />
          <span>门票：¥{{ activity.ticket_price }}</span>
        </div>
        <div v-if="activity.average_cost" class="detail-row">
          <AppIcon name="credit-card" class="text-purple-500" />
          <span>人均花费：¥{{ activity.average_cost }}</span>
        </div>
        <div v-if="activity.need_booking" class="detail-row warning">
          <AppIcon name="exclamation-triangle" class="text-orange-500" />
          <span>需要预订</span>
        </div>
        <AppButton
          v-if="hasMoreDetails"
          size="sm"
          variant="ghost"
          @click="showDetails = !showDetails"
          class="toggle-btn"
        >
          {{ showDetails ? '收起' : '更多' }}
        </AppButton>
      </div>
    </div>

    <!-- 编辑模式 -->
    <div v-else class="activity-edit">
      <div class="edit-header">
        <h5 class="edit-title">编辑活动</h5>
        <AppButton size="sm" variant="ghost" icon="times" @click="cancelEdit" />
      </div>

      <div class="edit-form">
        <div class="form-group">
          <label>活动名称</label>
          <input v-model="editData.title" type="text" class="form-input" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>时间</label>
            <input v-model="editData.time" type="time" class="form-input" />
          </div>
          <div class="form-group">
            <label>类型</label>
            <select v-model="editData.type" class="form-input">
              <option value="attraction">景点</option>
              <option value="meal">餐饮</option>
              <option value="transport">交通</option>
              <option value="accommodation">住宿</option>
              <option value="shopping">购物</option>
              <option value="entertainment">娱乐</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>描述</label>
          <textarea v-model="editData.description" class="form-textarea" rows="2" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>时长</label>
            <input v-model="editData.duration" type="text" class="form-input" placeholder="如：2小时" />
          </div>
          <div class="form-group">
            <label>人均花费</label>
            <input v-model.number="editData.average_cost" type="number" class="form-input" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>门票价格</label>
            <input v-model.number="editData.ticket_price" type="number" class="form-input" placeholder="选填" />
          </div>
          <div class="form-group">
            <label>地址</label>
            <input v-model="editData.address" type="text" class="form-input" placeholder="选填" />
          </div>
        </div>

        <div class="form-group">
          <label class="checkbox-label">
            <input v-model="editData.need_booking" type="checkbox" />
            <span>需要预订</span>
          </label>
        </div>

        <div class="edit-actions">
          <AppButton variant="secondary" @click="cancelEdit">取消</AppButton>
          <AppButton variant="primary" @click="saveEdit">保存</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'
import type { Activity } from '@/types/api'

interface Props {
  activity: Activity
  editable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  editable: false
})

const emit = defineEmits<{
  update: [activity: Activity]
}>()

const isEditing = ref(false)
const showDetails = ref(false)

const editData = reactive<Activity>({
  title: props.activity.title,
  type: props.activity.type,
  time: props.activity.time,
  duration: props.activity.duration,
  description: props.activity.description,
  address: props.activity.address || '',
  ticket_price: props.activity.ticket_price,
  need_booking: props.activity.need_booking || false,
  average_cost: props.activity.average_cost,
  highlights: props.activity.highlights || [],
  recommended_dishes: props.activity.recommended_dishes || [],
  best_time: props.activity.best_time || '',
  tips: props.activity.tips || []
})

const typeLabels = {
  attraction: '景点',
  meal: '餐饮',
  transport: '交通',
  accommodation: '住宿',
  shopping: '购物',
  entertainment: '娱乐'
}

const hasMoreDetails = computed(() => {
  return !!(
    props.activity.address ||
    props.activity.ticket_price ||
    props.activity.average_cost ||
    props.activity.need_booking
  )
})

const startEdit = () => {
  Object.assign(editData, props.activity)
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const saveEdit = () => {
  emit('update', { ...editData })
  isEditing.value = false
}
</script>

<style scoped>
.editable-activity-card {
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  border-left: 3px solid #10b981;
  margin-bottom: 0.75rem;
  transition: all 0.2s;
}

.activity-type-attraction { border-left-color: #10b981; }
.activity-type-meal { border-left-color: #f97316; }
.activity-type-transport { border-left-color: #3b82f6; }
.activity-type-accommodation { border-left-color: #8b5cf6; }
.activity-type-shopping { border-left-color: #ec4899; }
.activity-type-entertainment { border-left-color: #eab308; }

/* 查看模式 */
.activity-view {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.activity-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.activity-time {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
  min-width: 60px;
}

.activity-type-badge {
  padding: 0.25rem 0.625rem;
  background: #f1f5f9;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: #475569;
}

.activity-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.activity-description {
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.5;
}

.activity-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-top: 0.5rem;
  margin-top: 0.5rem;
  border-top: 1px solid #e2e8f0;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
  color: #64748b;
}

.detail-row.warning {
  color: #d97706;
  font-weight: 500;
}

.toggle-btn {
  align-self: flex-start;
  margin-top: 0.25rem;
}

/* 编辑模式 */
.activity-edit {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

.edit-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-group label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #475569;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.form-input,
.form-textarea {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #14b8a6;
}

.form-textarea {
  resize: vertical;
  min-height: 60px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #475569;
  cursor: pointer;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e2e8f0;
}
</style>
