<template>
  <div class="test-page">
    <h1>用户信息更新测试</h1>

    <div class="test-section">
      <h2>当前用户信息</h2>
      <pre>{{ JSON.stringify(user, null, 2) }}</pre>
    </div>

    <div class="test-section">
      <h2>更新表单</h2>
      <input v-model="newName" placeholder="输入新用户名" />
      <button @click="updateName">更新用户名</button>
    </div>

    <div class="test-section">
      <h2>API 测试日志</h2>
      <div v-for="(log, index) in logs" :key="index" :class="['log', log.type]">
        [{{ log.time }}] {{ log.message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import api from '@/utils/api'

const authStore = useAuthStore()
const { user } = storeToRefs(authStore)
const newName = ref('')
const logs = ref<any[]>([])

function addLog(message: string, type: 'info' | 'success' | 'error' = 'info') {
  logs.value.push({
    time: new Date().toLocaleTimeString(),
    message,
    type
  })
}

onMounted(async () => {
  addLog('页面已加载')
  await authStore.fetchCurrentUser()
  addLog('用户信息已获取')
  if (user.value) {
    newName.value = user.value.name
    addLog(`当前用户名: ${user.value.name}`)
  }
})

async function updateName() {
  if (!newName.value.trim()) {
    addLog('错误：用户名不能为空', 'error')
    return
  }

  addLog(`开始更新用户名为: ${newName.value}`)

  try {
    addLog('发送 PUT 请求到 /api/v1/auth/me')

    const response = await api.put('/api/v1/auth/me', {
      name: newName.value
    })

    addLog('API 响应成功: ' + JSON.stringify(response), 'success')

    // 重新获取用户信息
    await authStore.fetchCurrentUser()
    addLog('用户信息已刷新', 'success')

    if (user.value) {
      addLog(`新用户名: ${user.value.name}`, 'success')
    }

  } catch (error: any) {
    addLog('请求失败: ' + error.message, 'error')
    if (error.response) {
      addLog('错误状态: ' + error.response.status, 'error')
      addLog('错误数据: ' + JSON.stringify(error.response.data), 'error')
    }
  }
}
</script>

<style scoped>
.test-page {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
}

.test-section {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.test-section h2 {
  margin-top: 0;
  margin-bottom: 15px;
}

input {
  padding: 10px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  margin-right: 10px;
  font-size: 14px;
}

button {
  padding: 10px 20px;
  background: #00d4aa;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background: #00b894;
}

.log {
  padding: 8px;
  margin-bottom: 4px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
}

.log.info {
  background: #f0f9ff;
  color: #0369a1;
}

.log.success {
  background: #f0fdf4;
  color: #15803d;
}

.log.error {
  background: #fef2f2;
  color: #b91c1c;
}

pre {
  background: #f1f5f9;
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
}
</style>
