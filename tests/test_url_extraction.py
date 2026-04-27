#!/usr/bin/env python3
import re
from pathlib import Path

def test_url_extraction():
    # 模拟日志内容
    test_log_content = """03-22 00:24:24 [info] [NapCat] [WebUi] WebUi Token: 2094b8e144af
03-22 00:24:24 [info] [NapCat] [WebUi] WebUi User Panel Url: http://127.0.0.1:6103/webui?token=2094b8e144af
03-22 00:24:24 [info] [NapCat] [WebUi] WebUi User Panel Url: http://[::]:6103/webui?token=2094b8e144af
03-22 00:24:24 [info] 等待网络连接..."""
    
    # 测试正则表达式
    pattern = re.compile(r"WebUi User Panel Url:\s*(https?://\S+)")
    
    lines = test_log_content.split('\n')
    urls = []
    for line in lines:
        match = pattern.search(line)
        if match:
            urls.append(match.group(1).strip())
    
    print("找到的URLs:")
    for url in urls:
        print(f"  - {url}")
    
    # 测试优先选择逻辑
    preferred_url = None
    for url in urls:
        if "127.0.0.1" in url:
            preferred_url = url
            break
    
    if not preferred_url:
        for url in urls:
            if "localhost" in url:
                preferred_url = url
                break
    
    if not preferred_url and urls:
        preferred_url = urls[0]
    
    print(f"\n优先选择的URL: {preferred_url}")
    
    # 验证URL包含token
    if preferred_url and "token=" in preferred_url:
        print("✓ URL包含token参数")
    else:
        print("✗ URL不包含token参数")

if __name__ == "__main__":
    test_url_extraction()