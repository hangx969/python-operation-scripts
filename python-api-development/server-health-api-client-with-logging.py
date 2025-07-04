#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务器健康状态监控客户端 (带日志记录)

功能描述:
    本脚本作为健康检查 API 的客户端，通过 HTTP 请求获取服务器健康状态数据，
    并基于预设阈值进行告警判断。集成完善的日志记录功能，将监控数据和告警信息
    记录到日志文件中，实现持久化的监控历史和问题追踪。

技术实现:
    - 使用 requests 库进行 HTTP API 调用
    - 使用 logging 模块实现结构化日志记录
    - 采用 JSON 数据格式进行 API 数据交换
    - 使用自定义 Formatter 格式化日志输出
    - 支持 UTF-8 编码确保中文日志正常显示

数据结构:
    API 响应数据格式:
    {
        "cpu_usage": float,     // CPU 使用率百分比
        "mem_usage": float,     // 内存使用率百分比
        "disk_usage": float,    // 磁盘使用率百分比 (未使用)
        "status": string        // 健康状态 ("healthy" | "unhealthy")
    }

API 接口规范:
    - URL: http://192.168.71.56:5000/api/health
    - 方法: GET
    - 响应格式: JSON
    - 状态码: 200 表示成功，其他表示失败
"""

import requests, logging
from logging import Formatter

# 配置基本日志记录器
logging.basicConfig(
    level=logging.INFO,
    filename='health_monitor/health.log',
    format='%(asctime)s-%(levelname)s: %(message)s',
    encoding='utf-8'
    )

# 自定义时间格式化器
formatter = Formatter('%(asctime)s-%(levelname)s: %(message)s', datefmt='%Y%m%d %H:%M:%S')
# logging.getLogger返回房前日志记录器
# .handlers是日志记录器中负责输出日志的处理器（比如输出到控制台、文件等）
for handler in logging.getLogger().handlers:
    # 这里遍历了所有处理器，都给他应用自定义好的格式化器
    handler.setFormatter(formatter)

# 定义api接口和报警阈值
url = 'http://192.168.71.56:5000/api/health'
threshold_cpu = 80
threshold_mem = 75

def check_health():
    # GET api获取数据
    response = requests.get(url)
    if response.status_code == 200:
        # 返回内容的json格式
        data = response.json()

        # 直接用get方法获取json的某个字段
        cpu_usage = data.get('cpu_usage')
        mem_usage = data.get('mem_usage')
        status = data.get('status')

        # 告警逻辑，超过阈值就输出到日志
        if cpu_usage > threshold_mem:
            logging.warning(f"Warning: CPU Usage {threshold_cpu}%, exceed threshold {threshold_cpu}%.")
        if mem_usage > threshold_mem:
            logging.warning(f"Warning: CPU Usage {threshold_mem}%, exceed threshold {threshold_mem}%.")

        # 日志输出获取到的数据
        logging.info(f"Status: {status}.")
        logging.info(f"CPU Usage: {cpu_usage}%.")
        logging.info(f"Memory Usage: {mem_usage}%.")
    else:
        logging.error('Cannot get server health status')

if __name__ == '__main__':
    check_health()