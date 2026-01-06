#!/bin/bash

# WanderFlow 项目部署脚本
# 适用于 Ubuntu 24.04 LTS

set -e

echo "========================================"
echo "  WanderFlow 项目一键部署脚本"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 步骤 1: 更新系统
echo -e "\n${GREEN}[1/8] 更新系统包...${NC}"
apt update && apt upgrade -y

# 步骤 2: 安装 Docker
echo -e "\n${GREEN}[2/8] 安装 Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
    echo -e "${GREEN}✓ Docker 安装完成${NC}"
else
    echo -e "${YELLOW}✓ Docker 已安装，跳过${NC}"
fi

# 步骤 3: 安装 Docker Compose
echo -e "\n${GREEN}[3/8] 安装 Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✓ Docker Compose 安装完成${NC}"
else
    echo -e "${YELLOW}✓ Docker Compose 已安装，跳过${NC}"
fi

# 步骤 4: 安装 Nginx（用于反向代理）
echo -e "\n${GREEN}[4/8] 安装 Nginx...${NC}"
apt install -y nginx certbot python3-certbot-nginx

# 步骤 5: 配置防火墙
echo -e "\n${GREEN}[5/8] 配置防火墙...${NC}"
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp    # SSH
    ufw allow 80/tcp    # HTTP
    ufw allow 443/tcp   # HTTPS
    ufw --force enable
    echo -e "${GREEN}✓ 防火墙配置完成${NC}"
else
    echo -e "${YELLOW}⚠ UFW 未安装，跳过防火墙配置${NC}"
fi

# 步骤 6: 创建项目目录
echo -e "\n${GREEN}[6/8] 创建项目目录...${NC}"
PROJECT_DIR="/opt/wanderflow"
mkdir -p $PROJECT_DIR
echo -e "${GREEN}✓ 项目目录: $PROJECT_DIR${NC}"

# 步骤 7: 提示上传代码
echo -e "\n${GREEN}[7/8] 准备项目文件...${NC}"
echo -e "${YELLOW}请将以下文件上传到服务器 $PROJECT_DIR ：${NC}"
echo -e "  - docker-compose.yml"
echo -e "  - backend/Dockerfile"
echo -e "  - backend/requirements.txt"
echo -e "  - frontend/Dockerfile"
echo -e "  - frontend/nginx.conf"
echo -e "  - .env (从 .env.example 复制并修改)"
echo ""
read -p "文件上传完成后按 Enter 继续..."

# 步骤 8: 生成安全密钥
echo -e "\n${GREEN}[8/8] 生成安全密钥...${NC}"
if [ ! -f "$PROJECT_DIR/.env" ]; then
    SECRET_KEY=$(openssl rand -hex 32)
    DB_PASSWORD=$(openssl rand -hex 16)

    cat > $PROJECT_DIR/.env << EOF
# 数据库配置
DB_NAME=wanderflow
DB_USER=wanderflow
DB_PASSWORD=$DB_PASSWORD

# JWT 密钥
SECRET_KEY=$SECRET_KEY

# CORS 配置
CORS_ORIGINS=https://zengyithiking.top,https://www.zengyithiking.top
EOF

    echo -e "${GREEN}✓ 环境变量文件已创建${NC}"
    echo -e "${YELLOW}数据库密码: $DB_PASSWORD${NC}"
    echo -e "${RED}请妥善保存以上信息！${NC}"
else
    echo -e "${YELLOW}✓ .env 文件已存在${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  系统准备完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "接下来的步骤："
echo ""
echo "1. 创建数据库并初始化："
echo "   cd $PROJECT_DIR"
echo "   docker-compose up -d db"
echo "   sleep 10"
echo "   docker-compose exec backend alembic upgrade head"
echo ""
echo "2. 启动所有服务："
echo "   docker-compose up -d"
echo ""
echo "3. 配置 SSL 证书（HTTPS）："
echo "   certbot --nginx -d zengyithiking.top"
echo ""
echo "4. 查看服务状态："
echo "   docker-compose ps"
echo "   docker-compose logs -f"
echo ""
echo "5. 更新项目时："
echo "   cd $PROJECT_DIR"
echo "   git pull"
echo "   docker-compose up -d --build"
echo ""
