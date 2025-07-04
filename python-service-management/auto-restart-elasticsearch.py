#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elasticsearch 服务自动重启监控脚本

功能描述:
    本脚本用于监控 Elasticsearch 服务的运行状态，通过 HTTP API 检查集群健康状态，
    当检测到服务异常或停止时自动重启服务。提供基于 API 的智能监控和自动恢复机制。

技术实现:
    - 使用 requests 库进行 HTTP API 调用
    - 通过 subprocess 模块执行系统服务管理命令
    - 基于集群健康检查的服务状态判断
    - 循环监控机制确保持续可用性
"""

import subprocess, time, requests

def check_es() -> bool:
    try:
        response = requests.get('http://172.16.183.101:9200/_cluster/health')
        if response.status_code == 200:
            print("ES is running.")
            return True
        else:
            return False
    except requests.exceptions.RequestException: # 这里会包括ConnectionError、Timeout、InvalidURL、SSLError等
        print("ES is not running.")
        return False

def restart_es():
    try:
        print("Restarting ES.")
        result = subprocess.run(["systemctl", "restart","elasticsearch"], check=True, capture_output=True, text=True)
        print("ES restarted.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart es: {e}.")

if __name__ == '__main__':
    while True:
        if not check_es():
            restart_es()
        else:
            print("ES is running, do nothing.")
        time.sleep(60)