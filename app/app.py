from flask import Flask, request, jsonify
from functools import wraps
from video_api_client import VideoApiClient
import os
import logging

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建视频API客户端实例
video_client = None

# API密钥，用于验证API调用
API_KEY = os.getenv("SERVICE_API_KEY", "test_api_key")

def require_api_key(f):
    """API密钥验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if provided_key and provided_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"code": 401, "message": "未授权访问", "data": None}), 401
    return decorated

@app.before_request
def initialize_client():
    """在首次请求前初始化视频客户端"""
    global video_client
    if video_client is None:
        api_key = os.getenv("API52_KEY")
        video_client = VideoApiClient(api_key=api_key, debug=(os.getenv("DEBUG", "false").lower() == "true"))
        logger.info("视频API客户端初始化完成")

@app.route('/api/v1/parse', methods=['POST'])
@require_api_key
def parse_video():
    """视频解析接口"""
    try:
        data = request.json
        if not data or 'url' not in data:
            return jsonify({
                "code": 400,
                "message": "缺少URL参数",
                "data": None
            }), 400
        
        url = data['url']
        platform = data.get('platform', 'auto')
        logger.info(f"接收到解析请求: {url}, 平台: {platform}")
        
        # 解析视频
        if platform == 'auto':
            result = video_client.get_video_by_url(url)
        else:
            result = video_client.parse_video(url, platform)
        
        if result:
            return jsonify({
                "code": 200,
                "message": "success",
                "data": result
            })
        else:
            return jsonify({
                "code": 404,
                "message": "无法解析视频",
                "data": None
            }), 404
            
    except Exception as e:
        logger.exception(f"解析视频时出错: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"服务器错误: {str(e)}",
            "data": None
        }), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    port = int(os.getenv("PORT", "8088"))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)