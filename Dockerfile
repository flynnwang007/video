FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 设置环境变量，确保Python不缓存.pyc文件
ENV PYTHONDONTWRITEBYTECODE=1
# 确保Python输出直接发送到终端，不进行缓冲
ENV PYTHONUNBUFFERED=1

# 运行API服务
CMD ["python", "video_api_client.py"] 