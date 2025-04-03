# Docker部署指南

本文档提供了使用Docker部署video_tool服务的详细说明。

## 预备条件

- 安装Docker (19.03+)
- 安装Docker Compose (1.25+)
- 基本的命令行操作知识

## 项目结构

- `Dockerfile`: 包含构建Docker镜像的指令
- `docker-compose.yml`: 定义和运行Docker容器的配置
- `nginx.conf.example`: Nginx配置文件示例，用于反向代理
- `.env.example`: 环境变量模板文件

## 快速开始

1. 复制环境变量文件并填入API密钥:
   ```bash
   cp .env.example .env
   # 编辑.env文件填入你的API密钥
   ```

2. 构建和启动服务:
   ```bash
   docker-compose up -d
   ```

3. 验证服务是否运行:
   ```bash
   curl http://localhost:8000/status
   ```

## 使用Docker Compose的命令

- 启动服务:
  ```bash
  docker-compose up -d
  ```

- 停止服务:
  ```bash
  docker-compose down
  ```

- 查看日志:
  ```bash
  docker-compose logs -f
  ```

- 重建镜像:
  ```bash
  docker-compose build
  ```

## 配置项

服务的所有配置都通过环境变量提供，主要包括:

- `API52_KEY`: 52api.cn的API密钥
- `DEBUG`: 调试模式开关 (true/false)
- `SERVICE_API_KEY`: 服务API密钥

## 生产环境部署

对于生产环境，建议配置:

1. 使用Nginx作为反向代理
2. 启用TLS加密 (HTTPS)
3. 设置适当的日志轮转策略
4. 实施容器健康检查
5. 设置自动重启策略

## 故障排除

1. 如果容器无法启动，检查日志:
   ```bash
   docker-compose logs app
   ```

2. 如果API请求失败，确认:
   - API密钥是否正确配置
   - 网络连接是否正常
   - Docker容器是否有网络访问权限

3. 如果容器启动但服务不可访问:
   - 检查端口映射配置
   - 确认防火墙设置
