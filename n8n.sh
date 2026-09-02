#!/bin/bash
set -e

# 检查root权限
if [[ $EUID -ne 0 ]]; then
   echo "请使用sudo运行此脚本"
   exit 1
fi

echo "[1/6] 安装基础依赖..."
apt update
apt install -y curl ufw

echo "[2/6] 安装Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

echo "[3/6] 使用淘宝镜像安装n8n..."
npm config set registry https://registry.npmmirror.com
npm install -g n8n

echo "[4/6] 创建n8n用户和目录..."
useradd -r -s /bin/false n8n || true
mkdir -p /opt/n8n
chown n8n:n8n /opt/n8n

echo "[5/6] 创建环境配置..."
cat > /opt/n8n/.env << 'EOF'
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_SECURE_COOKIE=false
N8N_PROTOCOL=http
GENERIC_TIMEZONE=Asia/Shanghai
EOF
chown n8n:n8n /opt/n8n/.env

echo "[6/6] 创建systemd服务..."
N8N_PATH=$(which n8n)
cat > /etc/systemd/system/n8n.service << EOF
[Unit]
Description=n8n
After=network.target

[Service]
Type=simple
User=n8n
Group=n8n
EnvironmentFile=/opt/n8n/.env
WorkingDirectory=/opt/n8n
ExecStart=${N8N_PATH} start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "启动服务..."
systemctl daemon-reload
systemctl enable n8n
systemctl start n8n

echo "配置防火墙..."
ufw allow 5678/tcp
ufw --force enable

echo "获取访问地址..."
echo "=================================="
echo "n8n 安装完成！"
echo "访问地址："
hostname -I | tr ' ' '\n' | grep -v '^127\.' | while read ip; do
    echo "  http://$ip:5678"
done
echo "=================================="
echo "服务状态："
systemctl status n8n --no-pager