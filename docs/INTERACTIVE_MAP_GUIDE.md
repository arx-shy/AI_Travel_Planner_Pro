# 交互式地图集成指南

## 📦 前端集成

### 1. 安装依赖

```bash
cd frontend
npm install leaflet @types/leaflet
```

### 2. 更新 MapPreview.vue 组件

```vue
<template>
  <div class="map-preview-section">
    <InteractiveMap
      :height="'500px'"
      :itinerary="currentItinerary"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import InteractiveMap from '@/components/planner/InteractiveMap.vue'
import { useItineraryStore } from '@/stores/itinerary'

const itineraryStore = useItineraryStore()
const currentItinerary = computed(() => itineraryStore.currentItinerary)
</script>
```

### 3. 使用示例数据测试

```vue
<template>
  <div>
    <h2>示例行程地图</h2>

    <!-- 选择行程 -->
    <div class="mb-4">
      <label>选择示例行程：</label>
      <select v-model="selectedItinerary" @change="loadItinerary">
        <option value="chengdu">成都慢生活3日游</option>
        <option value="yunnan">云南户外探险5日游</option>
        <option value="guangzhou">广州美食寻味4日游</option>
      </select>
    </div>

    <!-- 地图展示 -->
    <InteractiveMap
      :height="'600px'"
      :itinerary="displayItinerary"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import InteractiveMap from '@/components/planner/InteractiveMap.vue'
import {
  chengLeisureItinerary,
  yunnanAdventureItinerary,
  guangzhouFoodieItinerary
} from '@/data/sample-itineraries'

const selectedItinerary = ref('chengdu')

const sampleItineraries = {
  chengdu: chengLeisureItinerary,
  yunnan: yunnanAdventureItinerary,
  guangzhou: guangzhouFoodieItinerary
}

const displayItinerary = computed(() => {
  return sampleItineraries[selectedItinerary.value]
})
</script>
```

---

## 🔧 后端集成

### 1. 安装依赖

```bash
cd backend
pip install httpx
```

### 2. 配置高德地图 API 密钥

在 `backend/app/core/config.py` 中添加：

```python
class Settings(BaseSettings):
    # ... 其他配置 ...

    # 高德地图API配置
    AMAP_API_KEY: str = Field(
        default="",
        description="高德地图API密钥"
    )

    # ... 其他配置 ...
```

在 `.env` 文件中添加：

```env
# 高德地图API密钥（申请地址：https://console.amap.com/dev/key/app）
AMAP_API_KEY=your_api_key_here
```

### 3. 在 Planner Agent 中集成地理编码

修改 `backend/app/modules/planner/agents/planner_agent.py`：

```python
from app.services.geocoding_service import geocoding_service

class TravelPlannerAgent:
    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        # ... 其他参数
    ) -> Dict[str, Any]:
        """
        生成行程并添加地理坐标
        """
        # 原有的生成逻辑
        result = await self._generate_with_llm(destination, days, ...)

        # 使用地理编码服务添加坐标
        enriched_result = await geocoding_service.enrich_itinerary_with_coordinates(result)

        return enriched_result
```

### 4. 创建地理编码 API 端点（可选）

创建 `backend/app/modules/planner/api/geocoding.py`：

```python
from fastapi import APIRouter, Depends, HTTPException
from app.services.geocoding_service import geocoding_service
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/geocode")
async def geocode_address(
    address: str,
    city: str = None,
    current_user = Depends(get_current_user)
):
    """地址解析接口"""
    result = await geocoding_service.geocode(address, city)
    if not result:
        raise HTTPException(status_code=404, detail="地址解析失败")
    return result

@router.get("/search")
async def search_poi(
    keywords: str,
    city: str = None,
    current_user = Depends(get_current_user)
):
    """POI搜索接口"""
    results = await geocoding_service.text_search(keywords, city)
    return {"results": results}
```

---

## 🗺️ 地图功能特性

### 前端 InteractiveMap 组件功能

| 功能 | 说明 |
|------|------|
| 📍 **标记点显示** | 不同类型使用不同颜色和图标 |
| 🔗 **路线绘制** | 自动连接各个活动点，形成行程路线 |
| 🎛️ **图层控制** | 可切换显示不同类型的活动（景点、美食等） |
| 📅 **天数切换** | 可按天查看路线，或查看全部 |
| 📱 **响应式设计** | 自适应不同屏幕尺寸 |
| 🖼️ **全屏模式** | 支持全屏查看地图 |
| 💬 **详情弹窗** | 点击标记查看活动详情 |
| 🎨 **自定义样式** | 使用高德地图瓦片，中文显示 |

### 后端 GeocodingService 功能

| 功能 | 说明 |
|------|------|
| 🔍 **地址解析** | 地址 → 经纬度 |
| 🔄 **逆地理编码** | 经纬度 → 地址 |
| 🏢 **POI搜索** | 关键字搜索兴趣点 |
| 🚗 **驾车路径** | 驾车路线规划 |
| 🚶 **步行路径** | 步行路线规划 |
| 📦 **批量处理** | 批量地址解析 |
| ✨ **行程增强** | 自动为行程添加坐标信息 |

---

## 🎨 小红书风格卡片

### 更新 ItineraryCard.vue

创建一个更美观的小红书风格版本：

```vue
<template>
  <div class="xiaohongshu-card">
    <!-- 封面图 -->
    <div class="card-cover">
      <img :src="itinerary.cover_image" :alt="itinerary.title" />
      <div class="cover-overlay">
        <span class="style-badge">{{ styleLabels[itinerary.travel_style] }}</span>
      </div>
    </div>

    <!-- 卡片内容 -->
    <div class="card-content">
      <h3 class="card-title">{{ itinerary.title }}</h3>
      <p class="card-summary">{{ itinerary.summary }}</p>

      <!-- 标签 -->
      <div class="card-tags">
        <span class="tag">
          <i class="fa fa-map-marker-alt"></i>
          {{ itinerary.destination }}
        </span>
        <span class="tag">
          <i class="fa fa-calendar"></i>
          {{ itinerary.days }}天
        </span>
        <span class="tag">
          <i class="fa fa-yen-sign"></i>
          {{ itinerary.budget }}
        </span>
      </div>

      <!-- 统计信息 -->
      <div class="card-stats">
        <div class="stat-item">
          <span class="stat-value">{{ itinerary.days_detail?.length || 0 }}</span>
          <span class="stat-label">天行程</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ totalActivities }}</span>
          <span class="stat-label">个活动</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">¥{{ itinerary.total_cost }}</span>
          <span class="stat-label">总花费</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="card-actions">
        <button class="btn-view" @click="showDetails = !showDetails">
          {{ showDetails ? '收起详情' : '查看详情' }}
        </button>
        <button class="btn-map" @click="$emit('showMap')">
          <i class="fa fa-map"></i>
          查看地图
        </button>
      </div>
    </div>

    <!-- 详情区域 -->
    <div v-if="showDetails" class="card-details">
      <div v-for="day in itinerary.days_detail" :key="day.day_number" class="day-section">
        <h4>第{{ day.day_number }}天 - {{ day.title }}</h4>
        <ActivityTimeline :activities="day.activities" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ActivityTimeline from './ActivityTimeline.vue'

const props = defineProps<{
  itinerary: any
}>()

const emit = defineEmits<{
  showMap: []
}>()

const showDetails = ref(false)

const styleLabels = {
  leisure: '🍵 休闲',
  adventure: '🏔️ 冒险',
  foodie: '🍜 美食'
}

const totalActivities = computed(() => {
  return props.itinerary.days_detail?.reduce((sum, day) => {
    return sum + (day.activities?.length || 0)
  }, 0) || 0
})
</script>

<style scoped>
.xiaohongshu-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.xiaohongshu-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-cover {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
}

.style-badge {
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.card-content {
  padding: 16px;
}

.card-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
}

.card-summary {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.card-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.tag {
  background: #f5f5f5;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 12px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-stats {
  display: flex;
  justify-content: space-around;
  padding: 12px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin-bottom: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #ff2442;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-actions button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-view {
  background: #ff2442;
  color: white;
}

.btn-view:hover {
  background: #e01f3a;
}

.btn-map {
  background: white;
  color: #ff2442;
  border: 1px solid #ff2442;
}

.btn-map:hover {
  background: #fff5f6;
}

.card-details {
  padding: 16px;
  background: #fafafa;
}

.day-section {
  margin-bottom: 24px;
}

.day-section h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}
</style>
```

---

## 🚀 使用示例

### 在 Planner.vue 中集成

```vue
<template>
  <div class="grid lg:grid-cols-3 gap-8">
    <!-- 左侧：表单 + 示例选择 -->
    <div class="lg:col-span-1 space-y-6">
      <ItineraryForm />

      <!-- 示例行程选择 -->
      <div class="glass-card p-6">
        <h3 class="text-lg font-bold mb-4">📚 参考行程</h3>
        <div class="space-y-3">
          <button
            v-for="sample in sampleItineraries"
            :key="sample.id"
            @click="loadSampleItinerary(sample)"
            class="sample-btn w-full"
          >
            <div class="flex items-center justify-between">
              <span>{{ sample.title }}</span>
              <span class="text-sm text-slate-500">{{ sample.days }}天</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧：地图 + 行程卡片 -->
    <div class="lg:col-span-2 space-y-6">
      <!-- 地图预览 -->
      <MapPreview />

      <!-- 当前行程 -->
      <ItineraryCard
        v-if="currentItinerary"
        :itinerary="currentItinerary"
        @showMap="showMapModal"
      />

      <!-- 空状态 -->
      <EmptyStateCard v-else />
    </div>
  </div>

  <!-- 地图弹窗 -->
  <div v-if="mapModalOpen" class="map-modal">
    <div class="modal-content">
      <button class="close-btn" @click="mapModalOpen = false">
        <i class="fa fa-times"></i>
      </button>
      <InteractiveMap
        :height="'700px'"
        :itinerary="currentItinerary"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useItineraryStore } from '@/stores/itinerary'
import { sampleItineraries } from '@/data/sample-itineraries'
import InteractiveMap from '@/components/planner/InteractiveMap.vue'

const itineraryStore = useItineraryStore()
const currentItinerary = computed(() => itineraryStore.currentItinerary)
const mapModalOpen = ref(false)

function loadSampleItinerary(sample: any) {
  // 加载示例行程到状态中
  itineraryStore.setCurrentItinerary(sample)
}

function showMapModal() {
  mapModalOpen.value = true
}
</script>
```

---

## 📝 总结

### 已创建的文件

| 文件路径 | 说明 |
|---------|------|
| `frontend/src/data/sample-itineraries.ts` | 3个示例行程数据 |
| `frontend/src/components/planner/InteractiveMap.vue` | 交互式地图组件 |
| `backend/app/services/geocoding_service.py` | 地理编码服务 |
| `docs/INTERACTIVE_MAP_GUIDE.md` | 本文档 |

### 下一步操作

1. ✅ 安装前端依赖：`npm install leaflet @types/leaflet`
2. ✅ 申请高德地图API密钥：https://console.amap.com/dev/key/app
3. ✅ 配置后端环境变量：`AMAP_API_KEY=your_key`
4. ✅ 安装后端依赖：`pip install httpx`
5. ✅ 更新 Planner.vue 集成地图组件
6. ✅ 测试示例行程数据展示
7. ✅ 测试地图功能是否正常

需要我帮你执行哪一步？