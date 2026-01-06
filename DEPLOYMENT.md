# WanderFlow 项目部署指南

本文档详细说明如何将 WanderFlow AI 旅行规划助手部署到腾讯云服务器。

---

## 📋 目录

1. [服务器要求](#服务器要求)
2. [域名配置](#域名配置)
3. [服务器准备](#服务器准备)
4. [项目部署](#项目部署)
5. [SSL 证书配置](#ssl-证书配置)
6. [常见问题](#常见问题)

---

## 服务器要求

- **操作系统**: Ubuntu 24.04 LTS 64位
- **CPU**: 2核
- **内存**: 2GB
- **带宽**: 3Mbps
- **域名**: zengyithiking.top

---

## 域名配置

### 1. 登录腾讯云控制台

1. 进入 [腾讯云 DNS 控制台](https://console.cloud.tencent.com/cns)
2. 找到你的域名 `zengyithiking.top`

### 2. 添加 DNS 解析记录

添加以下记录：

| 主机记录 | 记录类型 | 线路类型 | 记录值 | TTL |
|---------|---------|---------|--------|-----|
| @ | A | 默认 | 你的服务器公网 IP | 600 |
| www | A | 默认 | 你的服务器公网 IP | 600 |

**示例**: 如果你的服务器 IP 是 `123.45.67.89`，则记录值为 `123.45.67.89`

### 3. 验证 DNS 解析

在本地电脑运行：
```bash
ping zengyithiking.top
nslookup zengyithiking.top
```

确保返回的是你的服务器 IP。

---

## 服务器准备

### 连接到服务器

使用 SSH 连接：
```bash
ssh ubuntu@你的服务器IP
```

### 运行一键部署脚本

1. 上传 `deploy.sh` 到服务器
2. 赋予执行权限并运行：
```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

脚本会自动安装：
- Docker
- Docker Compose
- Nginx
- 防火墙规则

---

## 项目部署

### 1. 上传项目文件

将以下文件上传到服务器的 `/opt/wanderflow` 目录：

```bash
# 在服务器上创建项目目录
sudo mkdir -p /opt/wanderflow
sudo chown -R $USER:$USER /opt/wanderflow

# 使用 scp 上传文件（在本地电脑运行）
scp docker-compose.yml ubuntu@你的IP:/opt/wanderflow/
scp -r backend ubuntu@你的IP:/opt/wanderflow/
scp -r frontend ubuntu@你的IP:/opt/wanderflow/
```

### 2. 配置环境变量

在服务器上：
```bash
cd /opt/wanderflow
cp .env.example .env
nano .env  # 或使用你喜欢的编辑器
```

修改以下配置：
```bash
DB_NAME=wanderflow
DB_USER=wanderflow
DB_PASSWORD=强密码_here

SECRET_KEY=随机生成的密钥

CORS_ORIGINS=https://zengyithiking.top,https://www.zengyithiking.top
```

### 3. 启动数据库

```bash
cd /opt/wanderflow
docker-compose up -d db
```

等待数据库启动（约10秒）

### 4. 初始化数据库

```bash
docker-compose exec backend alembic upgrade head
```

### 5. 启动所有服务

```bash
docker-compose up -d
```

### 6. 验证服务状态

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试后端 API
curl http://localhost:8000/api/v1/health
```

---

## SSL 证书配置

### 申请 Let's Encrypt 免费证书

在服务器上运行：
```bash
sudo certbot --nginx -d zengyithiking.top -d www.zengyithiking.top
```

按照提示：
1. 输入邮箱地址
2. 同意服务条款
3. 选择是否共享邮箱（选 No）
4. 选择重定向 HTTP 到 HTTPS（选 2）

### 自动续期

Certbot 会自动设置 cron 任务来续期证书。验证：
```bash
sudo certbot renew --dry-run
```

---

## 验证部署

### 1. 访问前端

在浏览器打开：
- https://zengyithiking.top
- https://www.zengyithiking.top

应该能看到 WanderFlow 前端界面

### 2. 测试后端 API

```bash
curl https://zengyithiking.top/api/v1/health
```

应该返回健康检查信息

### 3. 测试注册和登录

1. 点击"注册"
2. 填写信息并提交
3. 登录测试

---

## 更新项目

当代码更新后：

```bash
cd /opt/wanderflow
git pull origin master
docker-compose up -d --build
```

如果数据库结构有变化：
```bash
docker-compose exec backend alembic upgrade head
```

---

## 常用命令

### 查看服务状态
```bash
docker-compose ps
```

### 查看日志
```bash
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

### 重启服务
```bash
docker-compose restart
```

### 停止服务
```bash
docker-compose down
```

### 进入后端容器
```bash
docker-compose exec backend bash
```

### 备份数据库
```bash
docker-compose exec db mysqldump -u root -p wanderflow > backup.sql
```

### 恢复数据库
```bash
docker-compose exec -T db mysql -u root -p wanderflow < backup.sql
```

---

## 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
sudo netstat -tulpn | grep :8000

# 停止占用端口的服务
sudo systemctl stop nginx
```

### 2. Docker 容器无法启动

```bash
# 查看详细日志
docker-compose logs backend

# 重建容器
docker-compose up -d --force-recreate
```

### 3. 数据库连接失败

```bash
# 检查数据库是否运行
docker-compose ps db

# 查看 DB 日志
docker-compose logs db

# 重启数据库
docker-compose restart db
```

### 4. 前端无法访问后端

1. 检查 CORS 配置
2. 检查 Nginx 配置
3. 查看后端日志

### 5. 内存不足

对于 2GB 内存的服务器，建议：
- 只运行必要的容器
- 限制 Docker 内存使用
- 考虑升级到 4GB 内存

编辑 `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

## 安全建议

1. ✅ 使用强密码
2. ✅ 配置防火墙（UFW）
3. ✅ 使用 SSL/TLS
4. ✅ 定期更新系统和软件
5. ✅ 限制 SSH 访问（密钥认证）
6. ✅ 定期备份数据库
7. ✅ 监控服务器资源使用

---

## 监控和维护

### 查看服务器资源

```bash
# CPU 和内存
htop

# 磁盘使用
df -h

# Docker 资源使用
docker stats
```

### 设置日志轮转

创建 `/etc/logrotate.d/docker-compose`:
```
/opt/wanderflow/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0644 ubuntu ubuntu
}
```

---

## 获取帮助

如遇到问题，请查看：
1. Docker 日志: `docker-compose logs`
2. Nginx 日志: `sudo tail -f /var/log/nginx/error.log`
3. 系统日志: `sudo journalctl -xe`

---

## 快速参考

| 操作 | 命令 |
|------|------|
| 启动服务 | `docker-compose up -d` |
| 停止服务 | `docker-compose down` |
| 重启服务 | `docker-compose restart` |
| 查看日志 | `docker-compose logs -f` |
| 更新代码 | `git pull && docker-compose up -d --build` |
| 数据库迁移 | `docker-compose exec backend alembic upgrade head` |
| SSL 续期 | `sudo certbot renew` |
| 重启 Nginx | `sudo systemctl restart nginx` |

---

**部署完成后，访问**: https://zengyithiking.top

🎉 祝你部署成功！
