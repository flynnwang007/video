# 视频工具 (Video Tool)

一个简单易用的视频平台API工具，支持抖音、西瓜视频、今日头条、哔哩哔哩等平台的视频无水印下载。

## 功能特点

- 支持多个平台的视频链接解析
  - 抖音 (Douyin)
  - 西瓜视频 (Xigua)
  - 今日头条 (Toutiao)
  - 哔哩哔哩 (Bilibili)
  - 更多平台逐步添加中...
- 提供无水印视频下载
- 简单易用的API接口
- 支持Docker部署
- 详细的日志记录
- 高性能并发处理

## 安装说明

### 本地安装

1. 克隆仓库
   ```bash
   git clone https://github.com/yourusername/video_tool.git
   cd video_tool
   ```

2. 设置环境变量
   ```bash
   cp .env.example .env
   # 编辑.env文件，填入API密钥
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 运行服务
   ```bash
   python video_api_client.py
   ```

### Docker安装

请参考 [Docker部署指南](README.docker.md) 获取详细信息。

## 使用方法

### API使用

示例：解析抖音视频

```python
import requests

url = "http://localhost:8000/api/parse"
params = {
    "url": "https://v.douyin.com/your_video_code/",
    "platform": "douyin"
}
response = requests.get(url, params=params)
data = response.json()
print(data)
```

## 项目结构

```
video_tool/
├── app/                    # 应用主目录
│   └── __init__.py         # 包初始化文件
├── .env.example            # 环境变量示例
├── .gitignore              # Git忽略文件
├── Dockerfile              # Docker配置
├── README.md               # 项目说明
├── README.docker.md        # Docker部署说明
├── DEPLOYMENT.md           # 部署指南
├── docker-compose.yml      # Docker Compose配置
├── nginx.conf.example      # Nginx配置示例
├── requirements.txt        # 项目依赖
└── video_api_client.py     # 应用入口
```

## 贡献指南

欢迎提交问题报告和功能请求！如果您想贡献代码：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

- 感谢所有贡献者的付出
- 使用了 [52api.cn](https://52api.cn) 的API服务
