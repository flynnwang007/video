#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频解析API服务测试脚本
用于测试API服务的健康状态和视频解析功能
"""

import os
import json
import sys
import requests
import urllib3
from typing import Dict, Any, List, Optional, Tuple

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API配置
API_BASE_URL = "http://localhost:8088"  # 使用8088端口
API_KEY = os.getenv("SERVICE_API_KEY", "test_api_key")

# 测试URL列表（各平台的代表性URL）
TEST_URLS = [
    "https://v.douyin.com/JcjJ5Tq/",
    "https://v.kuaishou.com/t4fab5",
    "https://www.bilibili.com/video/BV1GJ411x7h7",
    "https://weibo.com/tv/show/1034:4661455556252703",
    "https://www.xiaohongshu.com/explore/6390c4a6000000001f0243a3",
    "https://m.toutiao.com/is/JkJgiVh/"
]

def test_health_check() -> bool:
    """测试API健康状态检查"""
    try:
        print(f"正在检查健康状态: {API_BASE_URL}/api/v1/health")
        response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=10, verify=False)
        print(f"健康检查响应: 状态码={response.status_code}, 内容={response.text[:100]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功 - 状态: {data.get('status')}, 版本: {data.get('version')}")
            return True
        else:
            print(f"❌ 健康检查失败 - 状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常 - {str(e)}")
        return False

def test_video_parsing(url: str) -> Tuple[bool, Optional[Dict]]:
    """测试视频解析功能
    
    Args:
        url: 需要测试的视频URL
        
    Returns:
        测试是否成功的标志和响应数据
    """
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    payload = {
        "url": url
    }
    
    try:
        print(f"正在解析URL: {url}")
        response = requests.post(
            f"{API_BASE_URL}/api/v1/parse", 
            headers=headers,
            json=payload,
            timeout=30,
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                result = data.get("data", {})
                platform = result.get("platform_name", "未知")
                video_url = result.get("video_url", "")
                
                if video_url:
                    print(f"✅ 解析成功 - 平台: {platform}")
                    print(f"   🎬 视频链接: {video_url[:60]}..." if len(video_url) > 60 else f"   🎬 视频链接: {video_url}")
                    return True, result
                else:
                    print(f"❌ 解析返回成功但未获取到视频URL - 平台: {platform}")
                    return False, result
            else:
                print(f"❌ 解析请求成功但API返回错误 - 错误码: {data.get('code')}, 消息: {data.get('message')}")
                return False, data
        else:
            print(f"❌ 解析请求失败 - 状态码: {response.status_code}, 响应: {response.text[:100]}")
            return False, None
    except Exception as e:
        print(f"❌ 解析请求异常 - {str(e)}")
        return False, None

def test_all() -> None:
    """测试所有功能"""
    print("=" * 50)
    print("开始测试视频解析API服务")
    print("=" * 50)
    
    # 1. 测试健康检查
    health_ok = test_health_check()
    if not health_ok:
        print("健康检查失败，中止测试")
        return
    
    print("\n")
    
    # 2. 测试视频解析
    results = []
    for url in TEST_URLS:
        success, data = test_video_parsing(url)
        results.append((url, success, data))
        print("-" * 50)
    
    # 3. 汇总测试结果
    success_count = sum(1 for _, success, _ in results if success)
    print("\n" + "=" * 50)
    print(f"测试结果汇总: 共测试 {len(results)} 个URL, 成功 {success_count} 个, 失败 {len(results) - success_count} 个")
    print(f"成功率: {success_count / len(results) * 100:.1f}%")
    print("=" * 50)

def test_single_url(url: str) -> None:
    """测试单个URL"""
    print("=" * 50)
    print(f"测试单个URL: {url}")
    print("=" * 50)
    
    # 1. 测试健康检查
    health_ok = test_health_check()
    if not health_ok:
        print("健康检查失败，中止测试")
        return
    
    print("\n")
    
    # 2. 测试视频解析
    success, data = test_video_parsing(url)
    
    # 3. 打印详细结果
    if success and data:
        print("\n详细信息:")
        print(f"标题: {data.get('title', '无标题')}")
        print(f"平台: {data.get('platform_name', '未知')}")
        print(f"视频URL: {data.get('video_url', '无')[:100]}...")
        print(f"封面URL: {data.get('cover_url', '无')[:100]}..." if data.get('cover_url') else "封面URL: 无")
        
        author = data.get('author', {})
        if author:
            print(f"作者: {author.get('name', '未知')}")
        
        stats = data.get('statistics', {})
        if stats:
            print(f"点赞: {stats.get('likes', 0)}, 评论: {stats.get('comments', 0)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 如果提供了URL参数，则测试单个URL
        test_single_url(sys.argv[1])
    else:
        # 否则测试所有预设URL
        test_all() 