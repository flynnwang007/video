# 部署指南

## 环境要求
- Docker
- Docker Compose
- Git

## 本地开发

1. 克隆代码库
   ```bash
   git clone https://github.com/yourusername/video_tool.git
   cd video_tool
   ```

2. 复制环境变量配置文件并修改
   ```bash
   cp .env.example .env
   # 编辑.env文件，填入你的API密钥
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 运行服务
   ```bash
   python video_api_client.py
   ```

## Docker部署

1. 克隆代码库
   ```bash
   git clone https://github.com/yourusername/video_tool.git
   cd video_tool
   ```

2. 复制环境变量配置文件并修改
   ```bash
   cp .env.example .env
   # 编辑.env文件，填入你的API密钥
   ```

3. 使用Docker Compose构建并启动服务
   ```bash
   docker-compose up -d
   ```

4. 查看日志
   ```bash
   docker-compose logs -f
   ```

## 使用Nginx进行反向代理

1. 复制Nginx配置文件
   ```bash
   cp nginx.conf.example /etc/nginx/conf.d/video_tool.conf
   ```

2. 修改配置文件中的域名
   ```bash
   # 编辑 /etc/nginx/conf.d/video_tool.conf，将 your_domain.com 替换为你的域名
   ```

3. 重新加载Nginx配置
   ```bash
   sudo nginx -t      # 检查配置是否正确
   sudo systemctl reload nginx  # 重新加载配置
   ```

## 故障排除

如果遇到问题，可以检查以下几点：

1. 确认API密钥已正确设置在`.env`文件中
2. 检查Docker容器是否正常运行：`docker-compose ps`
3. 查看应用日志：`docker-compose logs app`
4. 检查网络连接：确保8000端口可访问 