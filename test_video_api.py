#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试简化版视频API客户端
"""

import os
import json
from dotenv import load_dotenv
from video_api_client import VideoApiClient

# 加载环境变量
load_dotenv()

# 测试URL列表
TEST_URLS = [
    # 抖音
    "https://v.douyin.com/FNbmuUAQUBI/",
    # 快手
    "https://v.kuaishou.com/t4fab5",
    # 小红书
    "http://xhslink.com/a/9sKpxg36vxk9",
    # 哔哩哔哩
    "https://www.bilibili.com/video/BV1TK42187M5",
    # 微博
    "https://video.weibo.com/show?fid=1034:5149917279354940",
    # 今日头条
    "https://m.toutiao.com/is/CQVQ9BRCD-I/"
]

def save_result(platform, result, success):
    """保存测试结果到文件"""
    # 创建结果目录（如果不存在）
    os.makedirs("results", exist_ok=True)
    
    # 创建一个文件名
    status = "success" if success else "failed"
    filename = f"results/{platform}_{status}.json"
    
    # 保存结果到文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到文件: {filename}")

def test_all_platforms():
    """测试所有平台"""
    print("开始测试简化版视频API客户端...")
    
    # 检查API密钥是否设置
    api_key = os.getenv("API52_KEY")
    if not api_key:
        print("错误: 未设置API52_KEY环境变量，请在.env文件中设置")
        return
    
    # 初始化客户端
    client = VideoApiClient(debug=True)
    
    success_count = 0
    failed_count = 0
    
    try:
        for url in TEST_URLS:
            print(f"\n===== 测试 {url} =====")
            
            # 检测平台
            platform = client.detect_platform(url)
            print(f"检测到平台: {platform}")
            
            if not platform:
                print("无法识别平台，跳过")
                failed_count += 1
                continue
            
            # 获取视频信息
            result = client.get_video_by_url(url)
            
            if result and result.get("video_url"):
                success_count += 1
                print(f"标题: {result.get('title', '')[:50]}...")
                print(f"作者: {result.get('author', {}).get('name', '')}")
                print(f"无水印视频URL: {result.get('video_url', '')[:60]}...")
                
                # 保存成功结果
                save_result(platform, result, True)
            else:
                failed_count += 1
                print("解析失败")
                
                # 保存失败结果
                save_result(platform, {"url": url, "platform": platform, "error": "解析失败"}, False)
    
    finally:
        client.close()
    
    # 打印测试汇总
    print("\n===== 测试汇总 =====")
    print(f"总测试数: {len(TEST_URLS)}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"成功率: {success_count / len(TEST_URLS) * 100:.2f}%")
    
    if success_count > 0:
        print("\n测试完成，至少有一个成功的测试，客户端可以正常工作！")
    else:
        print("\n测试失败，请检查API密钥和网络连接。")

def test_single_url(url):
    """测试单个URL"""
    print(f"测试单个URL: {url}")
    
    # 检查API密钥是否设置
    api_key = os.getenv("API52_KEY")
    if not api_key:
        print("错误: 未设置API52_KEY环境变量，请在.env文件中设置")
        return
    
    # 初始化客户端
    client = VideoApiClient(debug=True)
    
    try:
        # 检测平台
        platform = client.detect_platform(url)
        print(f"检测到平台: {platform}")
        
        if not platform:
            print("无法识别平台")
            return
        
        # 获取视频信息
        result = client.get_video_by_url(url)
        
        if result:
            print(f"\n标题: {result.get('title', '')}")
            print(f"作者: {result.get('author', {}).get('name', '')}")
            print(f"描述: {result.get('description', '')[:100]}...")
            print(f"封面: {result.get('cover_url', '')}")
            print(f"视频URL: {result.get('video_url', '')}")
            
            # 保存详细结果
            save_result(platform, result, True)
            
            print("\n解析成功！")
        else:
            print("解析失败")
    
    finally:
        client.close()

if __name__ == "__main__":
    # 如果传入了URL参数，则只测试该URL
    import sys
    if len(sys.argv) > 1:
        test_single_url(sys.argv[1])
    else:
        test_all_platforms() 