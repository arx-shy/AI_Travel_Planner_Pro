<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="modal-overlay" @click.self="handleClose">
        <div class="modal-content">
          <div class="modal-icon">
            <AppIcon name="exclamation-circle" size="4x" class="text-orange-500" />
          </div>

          <h3>已达到免费配额上限</h3>

          <p class="message">
            您本月已使用 {{ usage }}/{{ limit }} 次行程生成。
            <br>升级到 Pro 版本，即可无限量使用。
          </p>

          <div class="benefits">
            <div class="benefit-item">
              <AppIcon name="check-circle" class="text-green-500" />
              <span>无限量生成行程和文案</span>
            </div>
            <div class="benefit-item">
              <AppIcon name="check-circle" class="text-green-500" />
              <span>优先 AI 响应速度</span>
            </div>
            <div class="benefit-item">
              <AppIcon name="check-circle" class="text-green-500" />
              <span>专属客服支持</span>
            </div>
            <div class="benefit-item">
              <AppIcon name="check-circle" class="text-green-500" />
              <span>高清 PDF 导出</span>
            </div>
          </div>

          <div class="price-tag">
            <span class="price-symbol">¥</span>
            <span class="price-amount">29</span>
            <span class="price-period">/月</span>
          </div>

          <div class="actions">
            <AppButton variant="secondary" @click="handleClose">
              暂不升级
            </AppButton>
            <AppButton @click="handleUpgrade">
              立即升级
            </AppButton>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import AppIcon from './AppIcon.vue'
import AppButton from './AppButton.vue'

const props = defineProps<{
  show: boolean
  usage: number
  limit: number
}>()

const emit = defineEmits<{
  close: []
  upgrade: []
}>()

const handleClose = () => {
  emit('close')
}

const handleUpgrade = () => {
  emit('upgrade')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 480px;
  width: 100%;
  padding: 32px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-icon {
  text-align: center;
  margin-bottom: 16px;
}

.modal-content h3 {
  font-size: 24px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 12px;
  color: #1e293b;
}

.message {
  text-align: center;
  color: #64748b;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 24px;
}

.benefits {
  background: linear-gradient(135deg, #f0fdfa 0%, #f0f9ff 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #334155;
  font-size: 15px;
  margin-bottom: 12px;
}

.benefit-item:last-child {
  margin-bottom: 0;
}

.price-tag {
  text-align: center;
  margin-bottom: 24px;
}

.price-symbol {
  font-size: 24px;
  color: #64748b;
  vertical-align: top;
}

.price-amount {
  font-size: 48px;
  font-weight: 700;
  background: linear-gradient(135deg, #00d4aa 0%, #45b7d1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.price-period {
  font-size: 18px;
  color: #64748b;
}

.actions {
  display: flex;
  gap: 12px;
}

.actions button {
  flex: 1;
}

/* Modal 过渡动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}
</style>
