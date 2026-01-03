<template>
  <div class="tip-card">
    <div class="tip-icon">
      <AppIcon :name="icon" />
    </div>
    <div class="tip-content">
      <h5 class="tip-title">{{ title }}</h5>
      <p class="tip-text">{{ content }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/common/AppIcon.vue'

defineProps<{
  icon: string
  title: string
  content: string
}>()
</script>

<style scoped>
.tip-card {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%);
  border: 1px solid rgba(226,232,240,0.8);
  border-radius: 0.75rem;
  transition: all 0.2s;
}

.tip-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  border-color: rgba(20,184,166,0.2);
}

.tip-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ccfbf1 0%, #99f6e4 100%);
  border-radius: 0.5rem;
  color: #14b8a6;
  font-size: 1.25rem;
}

.tip-content {
  flex: 1;
  min-width: 0;
}

.tip-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 0.25rem;
}

.tip-text {
  font-size: 0.8125rem;
  color: #64748b;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
