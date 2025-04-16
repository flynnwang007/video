#!/bin/bash
# 部署隐私政策页面脚本

# 创建网站目录
sudo mkdir -p /var/www/html

# 复制隐私政策文件
sudo cp privacy_policy.html /var/www/html/index.html

# 设置正确的权限
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 755 /var/www/html

# 创建Nginx配置文件
sudo tee /etc/nginx/sites-available/api.aibase123.com > /dev/null << 'EOF'
server {
    listen 80;
    listen 443 ssl;
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

# 创建符号链接
sudo ln -sf /etc/nginx/sites-available/api.aibase123.com /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 如果配置正确，重启Nginx
if [ $? -eq 0 ]; then
    sudo systemctl restart nginx
    echo "隐私政策页面部署成功！请访问 https://api.aibase123.com 查看"
else
    echo "Nginx配置有误，请修复后再重启Nginx"
fi 