# 行程数据结构重构说明

## 📋 设计理念变更

### 旧版本（V1）问题
- ❌ 过度关注技术细节（经纬度坐标）
- ❌ 缺少用户真正关心的实用信息
- ❌ 没有考虑用户实际使用场景
- ❌ 缺少行前准备和实用提示

### 新版本（V2）改进
- ✅ 基于真实用户需求设计
- ✅ 隐藏技术细节，突出实用信息
- ✅ 参考专业旅游攻略平台设计
- ✅ 完整的行前准备和提示信息

---

## 📊 数据结构对比

### Activity（活动）结构对比

| 字段 | 旧版本（V1） | 新版本（V2） | 改进说明 |
|------|-------------|-------------|----------|
| **基本信息** |
| 标题 | ✅ title | ✅ title | 保持 |
| 类型 | ✅ type | ✅ type | 保持 |
| 时间 | ✅ time | ✅ time | 保持 |
| 时长 | ✅ duration (数字) | ✅ duration (文字) | **改为用户友好的文字描述** |
| **景点信息** |
| 描述 | ✅ description | ✅ description | 保持 |
| 地址 | ✅ location | ✅ address | 重命名更清晰 |
| 门票价格 | ❌ 缺失 | ✅ ticket_price | **新增** |
| 是否需预订 | ❌ 缺失 | ✅ need_booking | **新增** |
| 预订信息 | ❌ 缺失 | ✅ booking_info | **新增** |
| 推荐理由 | ❌ 缺失 | ✅ highlights | **新增** |
| 最佳时间 | ❌ 缺失 | ✅ best_time | **新增** |
| **餐饮信息** |
| 菜系 | ❌ 缺失 | ✅ cuisine | **新增** |
| 人均消费 | ✅ cost | ✅ average_cost | 重命名更清晰 |
| 必点菜品 | ❌ 缺失 | ✅ recommended_dishes | **新增** |
| 排队时间 | ❌ 缺失 | ✅ wait_time | **新增** |
| 营业时间 | ❌ 缺失 | ✅ opening_hours | **新增** |
| **实用信息** |
| 贴士 | ✅ tips | ✅ tips | 保持 |
| 穿衣建议 | ❌ 缺失 | ✅ dress_code | **新增** |
| 交通方式 | ❌ 缺失 | ✅ transportation | **新增** |
| 停车信息 | ❌ 缺失 | ✅ parking_info | **新增** |
| **技术数据** |
| 经纬度 | ✅ coordinates (可见) | ✅ _coordinates (隐藏) | **改为隐藏字段，用户不可见** |

---

### DayPlan（每日行程）结构对比

| 字段 | 旧版本（V1） | 新版本（V2） | 改进说明 |
|------|-------------|-------------|----------|
| 天数 | ✅ day | ✅ day_number | 重命名更清晰 |
| 主题 | ✅ title | ✅ title | 保持 |
| 日期 | ✅ date | ✅ date | 保持 |
| 概述 | ❌ 缺失 | ✅ summary | **新增** |
| 活动列表 | ✅ activities | ✅ activities | 保持 |
| 备注 | ✅ notes | ✅ notes | 保持 |
| 今日花费 | ❌ 缺失 | ✅ total_cost | **新增** |
| 住宿信息 | ❌ 分散在activities中 | ✅ accommodation (结构化) | **新增独立结构** |

---

### Itinerary（行程）结构对比

| 字段 | 旧版本（V1） | 新版本（V2） | 改进说明 |
|------|-------------|-------------|----------|
| **基本信息** |
| 标题 | ✅ title | ✅ title | 保持 |
| 目的地 | ✅ destination | ✅ destination | 保持 |
| 出发地 | ✅ departure | ✅ departure | 保持 |
| 天数 | ✅ days | ✅ days | 保持 |
| 预算 | ✅ budget | ✅ budget | 保持 |
| 实际花费 | ❌ 缺失 | ✅ actual_cost | **新增** |
| 费用明细 | ❌ 缺失 | ✅ cost_breakdown | **新增** |
| **展示信息** |
| 封面图 | ✅ cover_image | ✅ cover_image | 保持 |
| 概述 | ✅ summary | ✅ summary | 保持 |
| 行程亮点 | ❌ 缺失 | ✅ highlights | **新增** |
| 最佳季节 | ❌ 缺失 | ✅ best_season | **新增** |
| 天气提示 | ❌ 缺失 | ✅ weather | **新增** |
| **行前准备** |
| 证件清单 | ❌ 缺失 | ✅ preparation.documents | **新增** |
| 必带物品 | ❌ 缺失 | ✅ preparation.essentials | **新增** |
| 建议携带 | ❌ 缺失 | ✅ preparation.suggestions | **新增** |
| 预订提醒 | ❌ 缺失 | ✅ preparation.booking_reminders | **新增** |
| **实用提示** |
| 交通提示 | ❌ 缺失 | ✅ tips.transportation | **新增** |
| 住宿提示 | ❌ 缺失 | ✅ tips.accommodation | **新增** |
| 餐饮提示 | ❌ 缺失 | ✅ tips.food | **新增** |
| 购物提示 | ❌ 缺失 | ✅ tips.shopping | **新增** |
| 安全提示 | ❌ 缺失 | ✅ tips.safety | **新增** |

---

## 🎨 新增的用户友好字段详解

### 1. 景点活动信息
```typescript
{
  // 门票信息
  ticket_price: 58,           // 门票价格
  need_booking: true,         // 是否需要提前预订
  booking_info: "需提前3天在公众号预约",  // 预订方式

  // 推荐理由
  highlights: [
    "世界文化遗产",
    "必打卡景点",
    "适合亲子游"
  ],

  // 最佳时间
  best_time: "早上8-10点人少",

  // 穿衣建议
  dress_code: "舒适的鞋子，建议穿浅色衣服"
}
```

### 2. 餐饮信息
```typescript
{
  // 菜系类型
  cuisine: "川菜",

  // 必点菜品
  recommended_dishes: [
    "麻婆豆腐",
    "回锅肉",
    "宫保鸡丁"
  ],

  // 排队提示
  wait_time: "周末需等位，建议11:30前到",

  // 营业时间
  opening_hours: "11:00-21:00"
}
```

### 3. 交通信息
```typescript
{
  method: "地铁",           // 交通方式
  from: "春熙路",          // 出发地
  to: "熊猫基地",          // 目的地
  duration: "约1小时",     // 耗时（文字描述）
  cost: 8,                 // 费用
  tips: "地铁3号线到熊猫大道站"  // 实用提示
}
```

### 4. 住宿信息
```typescript
{
  name: "成都如家酒店",
  address: "春熙路附近",
  type: "酒店",                    // 酒店/民宿/青旅
  facilities: [                    // 设施
    "WiFi",
    "24小时热水",
    "电梯",
    "早餐"
  ],
  rating: 4.5,                     // 评分
  booking_status: "已预订"         // 预订状态
}
```

### 5. 行前准备
```typescript
{
  documents: [                     // 必备证件
    "身份证",
    "学生证（门票优惠）"
  ],
  essentials: [                    // 必带物品
    "防晒霜",
    "舒适的鞋子",
    "充电宝"
  ],
  suggestions: [                   // 建议携带
    "相机",
    "雨伞"
  ],
  booking_reminders: [             // 预订提醒
    "提前预订往返机票",
    "热门景点需提前预约"
  ]
}
```

### 6. 费用明细
```typescript
{
  transportation: 1200,    // 交通费用
  accommodation: 864,      // 住宿费用
  food: 520,               // 餐饮费用
  tickets: 198,            // 门票费用
  shopping: 68,            // 购物费用
  other: 0                 // 其他费用
}
```

---

## 🔄 迁移指南

### 前端迁移

```typescript
// 旧版本导入
import { SampleItinerary, SampleActivity } from '@/data/sample-itineraries'

// 新版本导入
import { Itinerary, Activity } from '@/data/sample-itineraries-v2'
```

主要变更：
1. `coordinates` → `_coordinates`（隐藏字段）
2. `location` → `address`
3. `cost` → `average_cost`（餐饮）
4. 新增：`highlights`, `best_time`, `ticket_price` 等字段

### 后端迁移

```python
# 旧版本导入
from app.modules.planner.schemas.plan_schema import PlanResponse, DayDetail

# 新版本导入
from app.modules.planner.schemas.plan_schema_v2 import PlanResponse, DayPlan
```

主要变更：
1. Activity 结构大幅扩展
2. DayPlan 新增 `summary`, `total_cost`, `accommodation`
3. PlanResponse 新增 `preparation`, `tips`, `cost_breakdown`

---

## 📝 AI Prompt 优化

### 旧版本 AI Prompt
```
请生成{destination}{days}天的旅游行程，包括：
- 景点名称、时间、描述
- 地址、经纬度坐标
- 费用、时长
```

### 新版本 AI Prompt
```
请生成{destination}{days}天的旅游行程，包括：

【每日行程】
- 主题和概述
- 详细活动安排（时间、地点、特色）
- 住宿信息
- 当日小结和花费

【每个活动需要包含】
- 景点：推荐理由、门票价格、是否需预订、最佳时间、穿衣建议
- 餐饮：菜系、必点菜品、人均消费、排队时间、营业时间
- 交通：交通方式、耗时、费用、实用提示
- 贴士：注意事项、避坑指南

【行前准备】
- 必备证件、必带物品、建议携带
- 预订提醒

【实用提示】
- 交通、住宿、餐饮、购物、安全等各方面提示
```

---

## ✅ 改进效果对比

### 用户视角

**旧版本：**
```
❌ 我看到一堆数字（经纬度），但不知道有什么用
❌ 不知道景点有什么特色，为什么要去
❌ 不知道需要准备什么
❌ 不知道门票多少钱，要不要提前预订
```

**新版本：**
```
✅ 清晰看到每个景点的特色和推荐理由
✅ 知道门票价格和预订方式
✅ 有完整的行前准备清单
✅ 有详细的实用提示和避坑指南
✅ 费用明细清楚，知道钱花在哪里
```

### 实际使用场景

**场景1：查看景点**
- 旧：显示"成都大熊猫基地，104.1469, 30.7354"
- 新：显示"世界著名的大熊猫基地，可以看到熊猫宝宝，门票58元，需提前3天预约"

**场景2：查看餐饮**
- 旧：显示"陈麻婆豆腐，120元"
- 新：显示"百年老字号川菜馆，必点麻婆豆腐和回锅肉，人均120元，周末需排队"

**场景3：行前准备**
- 旧：没有任何提示
- 新：完整的准备清单，包括证件、物品、预订提醒

---

## 🎯 总结

### 核心改进
1. **隐藏技术细节**：coordinates 改为 `_coordinates`，用户不可见
2. **突出实用信息**：新增大量用户真正关心的字段
3. **结构化数据**：交通、住宿、费用等信息独立结构化
4. **完整体验**：从规划到行前准备到实用提示的完整闭环

### 设计原则
- **用户为中心**：从用户需求出发，而非技术实现
- **实用至上**：每个字段都应该对用户有价值
- **清晰易懂**：字段名称和内容都要让普通用户能理解
- **完整闭环**：覆盖旅行前中后的全流程

### 参考来源
- 少数派旅游攻略制作方法
- 小红书优秀旅游笔记
- 专业旅游平台（马蜂窝、携程）的设计

---

**下一步：**
- [ ] 更新 AI Agent 的 Prompt 生成逻辑
- [ ] 更新前端展示组件
- [ ] 更新地图组件（使用隐藏的 `_coordinates`）
- [ ] 添加其他两个示例行程（云南、广州）
