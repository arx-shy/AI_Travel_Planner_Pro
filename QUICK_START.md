# 🚀 WanderFlow 快速部署指南

## 准备工作

### 1️⃣ 配置域名 DNS

登录 [腾讯云 DNS 控制台](https://console.cloud.tencent.com/cns)，添加：

```
类型: A记录
主机记录: @
记录值: 你的服务器公网IP

类型: A记录
主机记录: www
记录值: 你的服务器公网IP
```

### 2️⃣ 连接服务器

```bash
ssh ubuntu@你的服务器IP
```

---

## ⚡ 一键部署

### 步骤 1: 安装依赖

在服务器上运行：

```bash
# 下载部署脚本
wget https://raw.githubusercontent.com/zengyi-thinking/AI_Travel_Planner_Pro/master/deploy.sh

# 运行脚本
chmod +x deploy.sh
sudo ./deploy.sh
```

### 步骤 2: 上传项目文件

**方法 A: 使用 Git（推荐）**

```bash
cd /opt/wanderflow
git clone https://github.com/zengyi-thinking/AI_Travel_Planner_Pro.git .
```

**方法 B: 手动上传**

```bash
# 在本地电脑运行
scp -r docker-compose.yml backend frontend ubuntu@你的IP:/opt/wanderflow/
```

### 步骤 3: 配置环境变量

```bash
cd /opt/wanderflow
cp .env.example .env
nano .env
```

修改以下内容：
```bash
DB_PASSWORD=你的强密码
SECRET_KEY=$(openssl rand -hex 32)
```

### 步骤 4: 启动服务

```bash
# 启动数据库
docker-compose up -d db

# 等待10秒
sleep 10

# 初始化数据库
docker-compose exec backend alembic upgrade head

# 启动所有服务
docker-compose up -d
```

### 步骤 5: 配置 SSL

```bash
sudo certbot --nginx -d zengyithiking.top -d www.zengyithiking.top
```

选择：**2** - 重定向 HTTP 到 HTTPS

---

## ✅ 验证部署

### 测试访问

浏览器打开：
- 前端: https://zengyithiking.top
- 后端: https://zengyithiking.top/api/v1/health

### 查看状态

```bash
cd /opt/wanderflow
docker-compose ps
docker-compose logs -f
```

---

## 🔧 常用命令

| 操作 | 命令 |
|------|------|
| 查看日志 | `docker-compose logs -f` |
| 重启服务 | `docker-compose restart` |
| 更新项目 | `git pull && docker-compose up -d --build` |
| 数据库迁移 | `docker-compose exec backend alembic upgrade head` |

---

## 📚 详细文档

查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 获取完整部署文档。

---

**访问地址**: https://zengyithiking.top 🎉
