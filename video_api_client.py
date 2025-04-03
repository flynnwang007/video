#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版短视频解析客户端 - HTTP服务版
只使用52api.cn作为API提供商
支持抖音、快手、小红书等短视频平台的视频解析和去水印功能
"""

import time
import json
import logging
import os
import re
from typing import Dict, Optional, List, Any, Union
from urllib.parse import urlparse, parse_qs

import httpx
# 禁用不安全请求的警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# 加载环境变量
load_dotenv()


class VideoApiClient:
    """简化版短视频解析API客户端，只使用52api.cn作为API提供商"""
    
    # 支持的平台映射
    PLATFORM_MAPPING = {
        "douyin": "抖音",
        "kuaishou": "快手",
        "xiaohongshu": "小红书",
        "bilibili": "哔哩哔哩",
        "weibo": "微博",
        "toutiao": "今日头条",
        "xigua": "西瓜视频",
        "pipixia": "皮皮虾",
        "weishi": "微视"
    }
    
    # 域名与平台的对应关系
    DOMAIN_TO_PLATFORM = {
        "douyin.com": "douyin",
        "iesdouyin.com": "douyin",
        "kuaishou.com": "kuaishou",
        "xiaohongshu.com": "xiaohongshu",
        "xhslink.com": "xiaohongshu",
        "bilibili.com": "bilibili",
        "weibo.com": "weibo",
        "weibo.cn": "weibo",
        "ixigua.com": "xigua",
        "huoshan.com": "huoshan",
        "pipix.com": "pipixia",
        "weishi.qq.com": "weishi",
        "toutiao.com": "toutiao"
    }
    
    # 短链域名映射
    SHORT_URL_DOMAINS = {
        "v.douyin.com": "douyin",
        "w.kuaishou.com": "kuaishou",
        "xhsurl.com": "xiaohongshu",
        "t.cn": "weibo",
        "b23.tv": "bilibili",
        "h5.pipix.com": "pipixia",
        "isee.weishi.qq.com": "weishi",
        "m.toutiao.com": "toutiao"
    }
    
    # 平台到API端点的映射
    PLATFORM_TO_ENDPOINT = {
        "douyin": "douyin",
        "kuaishou": "kuaishou",
        "xiaohongshu": "xiaohongshu",
        "bilibili": "bilibili",
        "weibo": "weibo",
        "xigua": "xigua",
        "pipixia": "pipix",
        "weishi": "weishi",
        "toutiao": "toutiao"
    }
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30, 
                 max_retries: int = 3, debug: bool = False):
        """初始化短视频解析客户端
        
        Args:
            api_key: 52api.cn的API密钥，如果为None则从环境变量获取
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
            debug: 是否启用调试模式
        """
        # 获取API密钥
        if api_key is None:
            self.api_key = os.getenv("API52_KEY")
        else:
            self.api_key = api_key
            
        if not self.api_key:
            raise ValueError("未提供52api.cn的API密钥，请设置参数或在.env文件中设置API52_KEY")
        
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug
        
        # 设置日志
        self.logger = logging.getLogger("video_api_client")
        if debug or os.getenv("DEBUG") == "true":
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        self.logger.info(f"初始化52api.cn客户端，API密钥: {self.api_key[:5]}...")
        
        # 设置API基础URL
        self.base_url = "https://www.52api.cn/api"
        
        # 初始化HTTP客户端
        self.client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            verify=False  # 禁用SSL证书验证
        )
        
        # 添加通用请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def _make_request(self, endpoint: str, params: Dict, retry_count: int = 0) -> Optional[Dict]:
        """发送API请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            retry_count: 当前重试次数
            
        Returns:
            API响应数据或None（如果请求失败）
        """
        # 构建完整URL和参数
        url = f"{self.base_url}/{endpoint}"
        request_params = {
            "key": self.api_key,
            **params
        }
        
        try:
            self.logger.debug(f"请求 GET {url}")
            self.logger.debug(f"请求参数: {request_params}")
            
            response = self.client.get(
                url, 
                params=request_params, 
                headers=self.headers
            )
            
            # 检查响应状态
            if response.status_code != 200:
                self.logger.error(f"API请求失败，状态码: {response.status_code}")
                
                # 处理需要重试的错误
                if retry_count < self.max_retries:
                    retry_count += 1
                    sleep_time = 2 ** retry_count  # 指数退避策略
                    self.logger.info(f"等待 {sleep_time} 秒后重试 ({retry_count}/{self.max_retries})")
                    time.sleep(sleep_time)
                    return self._make_request(endpoint, params, retry_count)
                
                return None
            
            # 尝试解析JSON响应
            try:
                data = response.json()
                self.logger.debug(f"API响应: {str(data)[:200]}...")
                
                # 检查API错误
                if data.get("code") != 0 and data.get("code") != 200:
                    error_msg = data.get("msg", "未知错误")
                    self.logger.error(f"API错误: {error_msg}")
                    return data
                
                return data
            except json.JSONDecodeError:
                self.logger.error(f"响应不是有效的JSON: {response.text[:200]}")
                return None
                
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP错误: {e}")
        except httpx.RequestError as e:
            self.logger.error(f"请求错误: {e}")
        except Exception as e:
            self.logger.error(f"未知错误: {e}")
        
        # 重试逻辑
        if retry_count < self.max_retries:
            retry_count += 1
            sleep_time = 2 ** retry_count
            self.logger.info(f"等待 {sleep_time} 秒后重试 ({retry_count}/{self.max_retries})")
            time.sleep(sleep_time)
            return self._make_request(endpoint, params, retry_count)
        
        return None
    
    def detect_platform(self, url: str) -> Optional[str]:
        """检测URL对应的平台
        
        Args:
            url: 视频分享链接
            
        Returns:
            平台标识符或None（如果无法识别）
        """
        # 清理URL
        url = url.strip()
        
        try:
            # 解析URL
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # 检查是否是短链接域名
            if domain in self.SHORT_URL_DOMAINS:
                return self.SHORT_URL_DOMAINS[domain]
            
            # 移除www.前缀
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # 检查主域名
            for known_domain, platform in self.DOMAIN_TO_PLATFORM.items():
                if known_domain in domain:
                    return platform
            
            self.logger.warning(f"无法识别URL的平台: {url}")
            return None
        except Exception as e:
            self.logger.error(f"解析URL时出错: {e}")
            return None
    
    def parse_video(self, url: str, platform: Optional[str] = None) -> Optional[Dict]:
        """解析视频信息
        
        Args:
            url: 视频分享链接
            platform: 平台标识符（如果为None则自动检测）
            
        Returns:
            视频信息字典或None（如果解析失败）
        """
        if not platform:
            platform = self.detect_platform(url)
            if not platform:
                self.logger.error(f"无法识别视频平台: {url}")
                return None
        
        self.logger.info(f"解析{self.PLATFORM_MAPPING.get(platform, platform)}视频: {url}")
        
        # 获取对应的API端点
        endpoint = self.PLATFORM_TO_ENDPOINT.get(platform)
        if not endpoint:
            self.logger.error(f"不支持的平台: {platform}")
            return None
        
        # 构建请求参数
        params = {
            "url": url
        }
        
        # 发送请求
        response = self._make_request(endpoint, params)
        
        if response:
            # 提取并规范化结果
            try:
                # 52api通常将数据放在data字段中
                result = response.get("data", {})
                
                # 处理不同平台返回格式的差异，统一返回结构
                normalized_result = {
                    "platform": platform,
                    "platform_name": self.PLATFORM_MAPPING.get(platform, platform),
                    "title": result.get("title", ""),
                    "description": result.get("desc", result.get("description", "")),
                    "cover_url": result.get("cover", result.get("cover_url", "")),
                    "author": {
                        "name": result.get("author", {}).get("name", result.get("username", "")),
                        "avatar": result.get("author", {}).get("avatar", "")
                    },
                    "video_url": result.get("url", result.get("video_url", result.get("playAddr", result.get("work_url", "")))),
                    "music_url": result.get("music", {}).get("url", ""),
                    "statistics": {
                        "likes": result.get("statistics", {}).get("like_count", 0),
                        "comments": result.get("statistics", {}).get("comment_count", 0),
                        "shares": result.get("statistics", {}).get("share_count", 0)
                    },
                    "original_url": url,
                    "raw_data": result  # 保留原始数据，以备需要
                }
                
                # 特殊处理微博的视频URL（它返回的是一个包含不同清晰度的对象）
                if platform == "weibo" and isinstance(result.get("video_url"), dict):
                    video_urls = result.get("video_url", {})
                    if "高清 720P" in video_urls:
                        normalized_result["video_url"] = video_urls["高清 720P"]
                    elif video_urls:
                        # 获取第一个可用URL
                        normalized_result["video_url"] = next(iter(video_urls.values()))
                
                # 特殊处理今日头条视频URL（它返回的是一个视频清晰度数组）
                if platform == "toutiao" and isinstance(result.get("video_url"), list):
                    video_urls = result.get("video_url", [])
                    # 首先尝试找到720p清晰度
                    for video in video_urls:
                        if video.get("definition") == "720p":
                            normalized_result["video_url"] = video.get("url", "")
                            break
                    # 如果没有找到720p且video_url仍然是列表，使用第一个可用URL
                    if isinstance(normalized_result["video_url"], list) and video_urls:
                        normalized_result["video_url"] = video_urls[0].get("url", "")
                
                return normalized_result
            except Exception as e:
                self.logger.error(f"处理解析结果时出错: {e}")
                return None
        
        return None
    
    def get_video_by_url(self, url: str) -> Optional[Dict]:
        """通过URL获取视频信息（无水印）
        
        Args:
            url: 视频分享链接
            
        Returns:
            视频信息字典或None（如果获取失败）
        """
        return self.parse_video(url)
    
    def get_no_watermark_url(self, url: str) -> Optional[str]:
        """获取无水印视频URL
        
        Args:
            url: 视频分享链接
            
        Returns:
            无水印视频URL或None（如果获取失败）
        """
        result = self.parse_video(url)
        if result and result.get("video_url"):
            return result["video_url"]
        return None
    
    def close(self):
        """关闭HTTP客户端"""
        if hasattr(self, 'client'):
            self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# 创建Flask应用
app = Flask(__name__)

# 创建全局客户端实例
client = VideoApiClient(debug=os.getenv("DEBUG") == "true")

@app.route('/')
def home():
    """API首页，显示基本使用信息"""
    return jsonify({
        "status": "ok",
        "message": "视频解析API服务正在运行",
        "usage": {
            "解析视频": "/api/parse?url=视频链接&platform=平台(可选)",
            "获取无水印链接": "/api/no_watermark?url=视频链接&platform=平台(可选)",
            "获取支持的平台": "/api/platforms"
        },
        "version": "1.0"
    })

@app.route('/api/parse')
def parse_video():
    """解析视频API接口"""
    url = request.args.get('url')
    platform = request.args.get('platform')
    
    if not url:
        return jsonify({"error": "缺少url参数"}), 400
    
    result = client.get_video_by_url(url) if not platform else client.parse_video(url, platform)
    
    if result:
        return jsonify({"status": "ok", "data": result})
    else:
        return jsonify({"status": "error", "message": "无法解析视频"}), 404

@app.route('/api/no_watermark')
def get_no_watermark():
    """获取无水印视频链接API接口"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "缺少url参数"}), 400
    
    video_url = client.get_no_watermark_url(url)
    
    if video_url:
        return jsonify({
            "status": "ok", 
            "data": {
                "url": video_url
            }
        })
    else:
        return jsonify({"status": "error", "message": "无法获取无水印视频链接"}), 404

@app.route('/api/platforms')
def get_platforms():
    """获取支持的平台列表"""
    return jsonify({
        "status": "ok",
        "data": {
            "platforms": client.PLATFORM_MAPPING
        }
    })

@app.errorhandler(404)
def page_not_found(e):
    """处理404错误"""
    return jsonify({
        "status": "error",
        "message": "接口不存在"
    }), 404

@app.errorhandler(500)
def internal_server_error(e):
    """处理500错误"""
    return jsonify({
        "status": "error",
        "message": "服务器内部错误"
    }), 500

if __name__ == "__main__":
    # 获取端口号，默认为8000
    port = int(os.getenv("PORT", 8000))
    
    # 获取绑定地址，默认绑定所有接口
    host = os.getenv("HOST", "0.0.0.0")
    
    # 是否开启调试模式
    debug = os.getenv("DEBUG") == "true"
    
    # 启动Flask服务
    app.logger.info(f"启动视频解析API服务，监听 {host}:{port}")
    app.run(host=host, port=port, debug=debug) 