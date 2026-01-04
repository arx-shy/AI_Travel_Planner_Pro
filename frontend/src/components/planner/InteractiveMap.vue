<template>
  <div class="interactive-map-container">
    <!-- 地图容器 -->
    <div
      ref="mapContainer"
      class="map-container"
      :style="{ height: height }"
    ></div>

    <!-- 加载状态 -->
    <div v-if="loading" class="map-loading">
      <div class="spinner"></div>
      <p>地图加载中...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="map-error">
      <AppIcon name="exclamation-triangle" size="lg" />
      <p>{{ error }}</p>
      <AppButton size="sm" variant="outline" @click="retryLoad">
        重试
      </AppButton>
    </div>

    <!-- 地图控制面板 -->
    <div v-if="!loading && !error && map" class="map-controls">
      <!-- 图例 -->
      <div class="legend-panel">
        <h5>图例</h5>
        <div class="legend-items">
          <div class="legend-item" @click="toggleLayer('attraction')">
            <span class="legend-icon attraction" :class="{ active: layers.attraction }">
              <AppIcon name="camera" size="sm" />
            </span>
            <span>景点</span>
          </div>
          <div class="legend-item" @click="toggleLayer('meal')">
            <span class="legend-icon meal" :class="{ active: layers.meal }">
              <AppIcon name="utensils" size="sm" />
            </span>
            <span>美食</span>
          </div>
          <div class="legend-item" @click="toggleLayer('accommodation')">
            <span class="legend-icon accommodation" :class="{ active: layers.accommodation }">
              <AppIcon name="bed" size="sm" />
            </span>
            <span>住宿</span>
          </div>
          <div class="legend-item" @click="toggleLayer('transport')">
            <span class="legend-icon transport" :class="{ active: layers.transport }">
              <AppIcon name="car" size="sm" />
            </span>
            <span>交通</span>
          </div>
        </div>
      </div>

      <!-- 天数切换 -->
      <div v-if="daysCount > 1" class="day-selector">
        <h5>天数</h5>
        <div class="day-buttons">
          <AppButton
            v-for="day in daysCount"
            :key="day"
            size="sm"
            :variant="selectedDay === day ? 'primary' : 'ghost'"
            @click="selectDay(day)"
          >
            第{{ day }}天
          </AppButton>
          <AppButton
            size="sm"
            :variant="selectedDay === null ? 'primary' : 'ghost'"
            @click="selectDay(null)"
          >
            全部
          </AppButton>
        </div>
      </div>

      <!-- 全屏按钮 -->
      <button class="fullscreen-btn" @click="toggleFullscreen">
        <AppIcon :name="isFullscreen ? 'compress' : 'expand'" size="sm" />
      </button>
    </div>

    <!-- 活动详情弹窗 -->
    <div
      v-if="selectedActivity"
      class="activity-popup"
      :style="{ left: popupPosition.x + 'px', top: popupPosition.y + 'px' }"
    >
      <div class="popup-header">
        <h6>{{ selectedActivity.title }}</h6>
        <button class="close-btn" @click="closePopup">
          <AppIcon name="times" size="sm" />
        </button>
      </div>
      <div class="popup-content">
        <p v-if="selectedActivity.description">{{ selectedActivity.description }}</p>
        <div class="popup-meta">
          <span v-if="selectedActivity.time" class="meta-item">
            <AppIcon name="clock" size="sm" />
            {{ selectedActivity.time }}
          </span>
          <span v-if="selectedActivity.location" class="meta-item">
            <AppIcon name="map-marker-alt" size="sm" />
            {{ selectedActivity.location }}
          </span>
          <span v-if="selectedActivity.duration" class="meta-item">
            <AppIcon name="hourglass-half" size="sm" />
            {{ selectedActivity.duration }}
          </span>
          <span v-if="selectedActivity.cost" class="meta-item">
            <AppIcon name="money-bill" size="sm" />
            ¥{{ selectedActivity.cost }}
          </span>
        </div>
        <div v-if="selectedActivity.tips && selectedActivity.tips.length" class="popup-tips">
          <AppIcon name="lightbulb" size="sm" />
          <ul>
            <li v-for="(tip, i) in selectedActivity.tips" :key="i">{{ tip }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import AppIcon from '@/components/common/AppIcon.vue'
import AppButton from '@/components/common/AppButton.vue'

/**
 * 活动接口定义
 */
interface Activity {
  time: string
  title: string
  description?: string
  location?: string
  duration?: string
  cost?: number
  tips?: string[]
  type: 'attraction' | 'meal' | 'transport' | 'accommodation' | 'shopping'
  coordinates?: {
    lng: number
    lat: number
  }
}

/**
 * 每日计划接口
 */
interface DayPlan {
  day_number: number
  title?: string
  activities: Activity[]
}

/**
 * 组件 Props
 */
interface Props {
  height?: string
  itinerary?: {
    destination: string
    days_detail?: DayPlan[]
  }
}

const props = withDefaults(defineProps<Props>(), {
  height: '500px'
})

// 地图相关状态
const mapContainer = ref<HTMLDivElement>()
const map = ref<L.Map>()
const markers = ref<L.Marker[]>([])
const polylines = ref<L.Polyline[]>([])
const loading = ref(true)
const error = ref('')

// 弹窗相关状态
const selectedActivity = ref<Activity | null>(null)
const popupPosition = ref({ x: 0, y: 0 })

// 图层控制
const layers = ref({
  attraction: true,
  meal: true,
  accommodation: true,
  transport: true,
  shopping: true
})

// 天数选择
const selectedDay = ref<number | null>(null)

// 全屏状态
const isFullscreen = ref(false)

// 计算属性
const daysCount = computed(() => {
  return props.itinerary?.days_detail?.length || 0
})

/**
 * 初始化地图
 */
async function initMap() {
  try {
    loading.value = true
    error.value = ''

    // 等待 DOM 准备好
    await new Promise(resolve => setTimeout(resolve, 100))

    if (!mapContainer.value) {
      throw new Error('地图容器未找到')
    }

    // 创建地图实例
    map.value = L.map(mapContainer.value, {
      center: [30.5728, 104.0668], // 成都中心
      zoom: 12,
      zoomControl: true,
      attributionControl: false
    })

    // 添加地图瓦片层（使用 OpenStreetMap，兼容百度地图坐标）
    const tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      minZoom: 3,
      maxZoom: 19
    })

    map.value.addLayer(tileLayer)

    // 添加标记和路线
    if (props.itinerary?.days_detail) {
      addMarkersAndRoutes()
    }

    loading.value = false
  } catch (err) {
    console.error('地图初始化失败:', err)
    error.value = '地图加载失败，请检查网络连接'
    loading.value = false
  }
}

/**
 * 添加标记点和路线
 */
function addMarkersAndRoutes() {
  if (!map.value || !props.itinerary?.days_detail) return

  // 清除旧的标记和路线
  clearMarkersAndRoutes()

  const dayPlans = selectedDay.value
    ? props.itinerary.days_detail.filter(d => d.day_number === selectedDay.value)
    : props.itinerary.days_detail

  const allCoordinates: [number, number][] = []
  const allActivities: Array<{ activity: Activity; position: [number, number] }> = []

  // 遍历每一天
  dayPlans.forEach(dayPlan => {
    dayPlan.activities.forEach(activity => {
      if (!activity.coordinates || !layers.value[activity.type]) return

      const position: [number, number] = [activity.coordinates.lat, activity.coordinates.lng]
      allCoordinates.push(position)
      allActivities.push({ activity, position })

      // 创建自定义图标
      const icon = createCustomIcon(activity.type)

      // 创建标记
      const marker = L.marker(position, { icon })
        .addTo(map.value!)

      // 绑定点击事件
      marker.on('click', () => showActivityPopup(activity, marker))

      markers.value.push(marker)
    })
  })

  // 绘制路线（按顺序连接）
  if (allCoordinates.length > 1) {
    const polyline = L.polyline(allCoordinates, {
      color: '#14b8a6',
      weight: 4,
      opacity: 0.7,
      dashArray: '10, 10'
    }).addTo(map.value!)

    polylines.value.push(polyline)

    // 调整地图视图以显示所有标记
    map.value.fitBounds(polyline.getBounds(), { padding: [50, 50] })
  } else if (allCoordinates.length === 1) {
    // 如果只有一个点，居中显示
    map.value.setView(allCoordinates[0], 14)
  }
}

/**
 * 创建自定义图标
 */
function createCustomIcon(type: string): L.DivIcon {
  const colors = {
    attraction: '#ef4444',
    meal: '#f59e0b',
    accommodation: '#3b82f6',
    transport: '#8b5cf6',
    shopping: '#ec4899'
  }

  const icons = {
    attraction: 'camera',
    meal: 'utensils',
    accommodation: 'bed',
    transport: 'car',
    shopping: 'shopping-bag'
  }

  const color = colors[type as keyof typeof colors] || '#6b7280'

  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        border: 3px solid white;
      ">
        <i class="fa fa-${icons[type as keyof typeof icons]}"></i>
      </div>
    `,
    className: 'custom-marker',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
  })
}

/**
 * 显示活动详情弹窗
 */
function showActivityPopup(activity: Activity, marker: L.Marker) {
  selectedActivity.value = activity

  // 获取标记的屏幕位置
  const point = map.value!.latLngToContainerPoint(marker.getLatLng()!)
  popupPosition.value = { x: point.x + 20, y: point.y - 20 }
}

/**
 * 关闭弹窗
 */
function closePopup() {
  selectedActivity.value = null
}

/**
 * 清除所有标记和路线
 */
function clearMarkersAndRoutes() {
  markers.value.forEach(marker => map.value!.removeLayer(marker))
  polylines.value.forEach(line => map.value!.removeLayer(line))
  markers.value = []
  polylines.value = []
}

/**
 * 切换图层显示
 */
function toggleLayer(type: string) {
  layers.value[type as keyof typeof layers.value] = !layers.value[type as keyof typeof layers.value]
  addMarkersAndRoutes()
}

/**
 * 选择天数
 */
function selectDay(day: number | null) {
  selectedDay.value = day
  addMarkersAndRoutes()
}

/**
 * 切换全屏
 */
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    mapContainer.value?.requestFullscreen()
    isFullscreen.value = true
  } else {
    document.exitFullscreen()
    isFullscreen.value = false
  }
}

/**
 * 重试加载地图
 */
function retryLoad() {
  initMap()
}

// 监听行程数据变化
watch(() => props.itinerary, () => {
  if (map.value) {
    addMarkersAndRoutes()
  }
}, { deep: true })

// 组件挂载时初始化地图
onMounted(() => {
  initMap()
})

// 组件卸载时清理
onUnmounted(() => {
  if (map.value) {
    map.value.remove()
    map.value = undefined
  }
})
</script>

<style scoped>
.interactive-map-container {
  position: relative;
  width: 100%;
  background: #f1f5f9;
  border-radius: 1rem;
  overflow: hidden;
}

.map-container {
  width: 100%;
  min-height: 400px;
}

/* 加载状态 */
.map-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  z-index: 10;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #14b8a6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.map-loading p {
  margin-top: 1rem;
  color: #64748b;
  font-size: 0.875rem;
}

/* 错误状态 */
.map-error {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fef2f2;
  color: #dc2626;
  z-index: 10;
}

.map-error p {
  margin: 1rem 0;
}

/* 地图控制面板 */
.map-controls {
  position: absolute;
  top: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  z-index: 5;
}

.legend-panel,
.day-selector {
  background: white;
  padding: 0.75rem;
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 150px;
}

.legend-panel h5,
.day-selector h5 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem 0;
  transition: opacity 0.2s;
}

.legend-item:hover {
  opacity: 0.7;
}

.legend-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  opacity: 0.3;
  transition: opacity 0.2s;
}

.legend-icon.active {
  opacity: 1;
}

.legend-icon.attraction { background: #ef4444; }
.legend-icon.meal { background: #f59e0b; }
.legend-icon.accommodation { background: #3b82f6; }
.legend-icon.transport { background: #8b5cf6; }

.day-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.day-buttons button {
  width: 100%;
  text-align: left;
}

.fullscreen-btn {
  background: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.fullscreen-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

/* 活动详情弹窗 */
.activity-popup {
  position: absolute;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  min-width: 280px;
  max-width: 350px;
  z-index: 1000;
  animation: popupFadeIn 0.2s ease-out;
}

@keyframes popupFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.popup-header h6 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  color: #64748b;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1e293b;
}

.popup-content {
  padding: 1rem;
}

.popup-content > p {
  margin: 0 0 0.75rem 0;
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
}

.popup-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #64748b;
}

.popup-tips {
  background: #fef3c7;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.popup-tips ul {
  margin: 0.5rem 0 0 0;
  padding-left: 1.25rem;
  color: #92400e;
}

.popup-tips li {
  margin-bottom: 0.25rem;
}
</style>
