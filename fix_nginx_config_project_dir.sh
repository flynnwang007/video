#!/bin/bash
# 修复Nginx配置脚本 - 使用项目目录中的隐私政策文件

echo "===== 开始修复Nginx配置 ====="

# 0. 设置项目目录路径
PROJECT_DIR=$(pwd)
echo "当前项目目录: $PROJECT_DIR"

# 检查项目目录下是否有隐私政策文件
if [ ! -f "$PROJECT_DIR/privacy_policy.html" ]; then
  echo "错误: 在项目目录下找不到隐私政策文件"
  exit 1
fi

# 1. 创建网站目录并复制隐私政策文件
echo "复制隐私政策文件到网站目录..."
sudo mkdir -p /var/www/html
sudo cp "$PROJECT_DIR/privacy_policy.html" /var/www/html/index.html
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html
echo "隐私政策文件已复制到 /var/www/html/index.html"

# 2. 检查Nginx默认网站配置
echo "检查Nginx默认网站配置..."
if [ -f "/etc/nginx/sites-enabled/default" ]; then
  echo "发现默认网站配置，禁用它..."
  sudo rm /etc/nginx/sites-enabled/default
  echo "默认网站配置已禁用"
fi

# 3. 重新创建配置文件
echo "重新创建Nginx配置文件..."
sudo tee /etc/nginx/sites-available/api.aibase123.com > /dev/null << 'EOF'
server {
    listen 80 default_server;
    listen 443 ssl default_server;
    server_name api.aibase123.com;

    ssl_certificate /etc/letsencrypt/live/api.aibase123.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.aibase123.com/privkey.pem;

    # SSL 配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # 隐私政策页面 - 当访问根路径时显示
    location = / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # 验证 ACME 挑战
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # API 路径 - 代理到后端服务
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 4. 确保配置文件存在于sites-enabled目录
echo "创建符号链接..."
sudo ln -sf /etc/nginx/sites-available/api.aibase123.com /etc/nginx/sites-enabled/

# 确保默认配置不存在
sudo rm -f /etc/nginx/sites-enabled/default

# 5. 检查配置文件语法
echo "检查Nginx配置语法..."
if sudo nginx -t; then
  echo "Nginx配置语法正确，重启Nginx..."
  sudo systemctl restart nginx
  echo "Nginx已重启"
else
  echo "Nginx配置语法错误，请手动修复"
  exit 1
fi

# 6. 输出隐私政策页面的内容，用于调试
echo "当前隐私政策文件内容预览（前100个字符）:"
head -c 100 /var/www/html/index.html
echo "..."

# 7. 验证网站访问
echo "尝试访问网站..."
if curl -s http://localhost | grep -q "隐私政策"; then
  echo "成功！隐私政策页面已正确配置"
else
  echo "警告：无法在本地验证隐私政策页面"
  echo "可能原因："
  echo "1. 隐私政策HTML文件内容不含'隐私政策'文字"
  echo "2. 服务器配置问题"
fi

echo "===== 修复完成 ====="
echo "请尝试访问 https://api.aibase123.com 验证隐私政策页面"
echo "如果仍然看到Nginx默认页面，请检查Nginx日志:"
echo "sudo tail -n 50 /var/log/nginx/error.log" 